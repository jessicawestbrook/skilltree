#!/usr/bin/env python3

import csv
import logging
from typing import Dict, List, Any
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DifficultyCalculator:
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._calculate_word_frequency(word)
        morphological_score = self._calculate_morphological_complexity(word)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score,
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'difficulty': None
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        word = word.lower()
        irregularities = 0
        
        patterns = [
            (r'gh', 1), (r'ough', 2), (r'ph', 1), (r'ch(?![aeiouy])', 1),
            (r'qu', 0.5), (r'x', 1), (r'tion', 0.5), (r'sion', 0.5),
            (r'eau', 2), (r'ieu', 2), (r'ée', 1), (r'silent.*e$', 1)
        ]
        
        for pattern, weight in patterns:
            irregularities += len(re.findall(pattern, word)) * weight
        
        length_factor = len(word) / 10
        return min(5.0, irregularities + length_factor)
    
    def _calculate_word_frequency(self, word: str) -> float:
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        word_lower = word.lower()
        
        if word_lower in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 6:
            return 3.0
        elif len(word) <= 8:
            return 4.0
        else:
            return 5.0
    
    def _calculate_morphological_complexity(self, word: str) -> float:
        word = word.lower()
        
        prefixes = ['un', 're', 'pre', 'dis', 'over', 'under', 'out', 'up', 'sub', 'inter', 'fore', 'de', 'mis', 'anti', 'semi', 'super', 'trans', 'ultra', 'non']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'ive', 'al', 'ic', 'ism', 'ist', 'ize', 'ise']
        
        morphemes = 1
        temp_word = word
        
        for prefix in prefixes:
            if temp_word.startswith(prefix):
                morphemes += 1
                temp_word = temp_word[len(prefix):]
                break
        
        for suffix in suffixes:
            if temp_word.endswith(suffix):
                morphemes += 1
                temp_word = temp_word[:-len(suffix)]
                break
        
        if morphemes == 1:
            return 1.0
        elif morphemes == 2:
            return 2.5
        elif morphemes == 3:
            return 4.0
        else:
            return 5.0
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        if not etymology or etymology.lower() in ['unknown', 'uncertain']:
            return 3.0
        
        etymology_lower = etymology.lower()
        complex_origins = ['sanskrit', 'hebrew', 'arabic', 'mandarin', 'japanese', 'finnish', 'hungarian', 'czech', 'polish', 'russian', 'nahuatl', 'quechua']
        moderate_origins = ['greek', 'latin', 'old english', 'middle english', 'old french', 'german', 'dutch', 'scandinavian', 'norse']
        simple_origins = ['english', 'french', 'spanish', 'italian', 'portuguese']
        
        if any(origin in etymology_lower for origin in complex_origins):
            return 5.0
        elif any(origin in etymology_lower for origin in moderate_origins):
            return 3.0
        elif any(origin in etymology_lower for origin in simple_origins):
            return 2.0
        else:
            return 3.5

class Batch127Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.combined_words = []
        
    def detect_combined_words(self) -> List[str]:
        combined_patterns = [
            'parabolaparameters',
            'paraffinvigneron',
            'parquetparterre'
        ]
        return combined_patterns
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        word_data = {
            'pantomime': {
                'definition': 'A dramatic entertainment performed without words, using only gestures, expressions, and body movement to tell a story; the art of conveying meaning through silent dramatic action. Pantomime artists, called mimes, use exaggerated facial expressions and precise body movements to create invisible objects and situations. The art form has ancient roots in Greek and Roman theater and evolved into modern performance styles. Classic pantomime techniques include walking against wind, being trapped in a box, or climbing stairs. Professional pantomime requires extensive training in body control, storytelling, and emotional expression through movement alone.',
                'pronunciation': '/ˈpæntəˌmaɪm/',
                'pronunciation_ipa': '/ˈpæntəˌmaɪm/',
                'etymology': 'From Greek "pantomimos" meaning "imitator of all," from "pan" (all) + "mimos" (imitator). Originally referred to Roman entertainers who acted all roles.',
                'memory_tip': 'PANTOMIME = PAN (all) + MIME. Think of a mime who can act out "all" things without speaking - silent storytelling.',
                'example_sentence': 'The street performer\'s _____ routine drew a large crowd as he created an entire invisible world through movement alone.'
            },
            'pantry': {
                'definition': 'A small room or closet in a house where food, dishes, linens, or provisions are stored; a storage area for kitchen supplies and non-perishable foods. Pantries serve as auxiliary storage spaces that help organize household items and keep them easily accessible. Modern pantries may include shelving systems, temperature control, and specialized storage for different types of food items. Walk-in pantries provide extensive storage space, while smaller pantries might be simple cabinets or closets. The organization of a pantry can significantly impact kitchen efficiency and meal preparation.',
                'pronunciation': '/ˈpæntri/',
                'pronunciation_ipa': '/ˈpæntri/',
                'etymology': 'From Old French "paneterie," from "panetier" meaning keeper of bread, from Latin "panis" meaning bread. Originally specifically for bread storage.',
                'memory_tip': 'PANTRY sounds like "PANT-RY" - think of panting from hunger until you find food in the storage room where you "try" to find snacks.',
                'example_sentence': 'She organized the _____ with labeled shelves for different categories of ingredients and cooking supplies.'
            },
            'pants': {
                'definition': 'A garment covering the body from the waist to the ankles, with separate coverings for each leg; trousers. In American English, pants typically refers to what British English calls trousers, while in British English, pants often means underwear. The garment comes in various styles including dress pants, casual pants, jeans, and athletic wear. Pants are fundamental clothing items in most cultures, providing protection, modesty, and style. Different materials, cuts, and designs serve various functional and fashion purposes.',
                'pronunciation': '/pænts/',
                'pronunciation_ipa': '/pænts/',
                'etymology': 'Short for "pantaloons," from Italian "pantalone," after a character in commedia dell\'arte who wore long trousers. The word evolved to mean the garment itself.',
                'memory_tip': 'PANTS comes from "PANTaloons" - think of the long "pants" that the Italian theater character Pantalone wore.',
                'example_sentence': 'He chose dark blue _____ to match his professional shirt for the job interview.'
            },
            'papeterie': {
                'definition': 'A stationery shop or department; fine stationery and writing materials, especially high-quality paper products. The term encompasses elegant writing papers, correspondence cards, envelopes, and related accessories used for formal correspondence. French papeteries traditionally offer luxury writing materials, fountain pens, sealing wax, and other items for sophisticated written communication. The concept reflects the art of beautiful letter writing and formal correspondence. Modern papeteries may include wedding invitations, personal stationery, and specialty papers for various occasions.',
                'pronunciation': '/ˌpæpəˈtri/',
                'pronunciation_ipa': '/ˌpæpəˈtri/',
                'etymology': 'From French "papeterie," from "papetier" meaning stationer, from "papier" (paper). Refers to shops specializing in fine paper goods.',
                'memory_tip': 'PAPETERIE = PAPER + TERY (place). Think of a fancy place for "paper" - an elegant stationery shop with beautiful writing materials.',
                'example_sentence': 'The elegant _____ featured handmade papers and fountain pens for discerning letter writers.'
            },
            'papillon': {
                'definition': 'A breed of small spaniel dog characterized by butterfly-like ears with long, silky hair; the French word for butterfly. Papillon dogs are toy spaniels known for their intelligence, agility, and distinctive ear shape that resembles butterfly wings. The breed comes in two varieties: papillon (with erect ears) and phalène (with drop ears). These dogs were popular among European nobility and appear in many Renaissance paintings. In French, papillon simply means butterfly, referring to the wing-like appearance of various objects or the insect itself.',
                'pronunciation': '/ˌpæpɪˈjɔn/',
                'pronunciation_ipa': '/ˌpæpɪˈjɔn/',
                'etymology': 'French word meaning butterfly, from Latin "papilio." The dog breed is named for its butterfly-like ears.',
                'memory_tip': 'PAPILLON sounds like "PAPA-LEON" - think of a "papa" lion with butterfly wings, or a small dog with butterfly-like ears.',
                'example_sentence': 'The _____ dog\'s erect, feathered ears made it look like a small, elegant butterfly in motion.'
            },
            'pappardelle': {
                'definition': 'Wide, flat ribbon pasta from Italian cuisine, typically 2-3 centimeters wide, often served with rich meat sauces or game. Pappardelle originates from Tuscany and is traditionally made fresh with eggs. The wide, flat shape allows the pasta to hold substantial sauces effectively. Classic preparations include pappardelle with wild boar ragu, duck sauce, or porcini mushrooms. The pasta\'s substantial texture makes it ideal for hearty, rustic dishes. Making fresh pappardelle requires rolling pasta dough thin and cutting it into wide strips.',
                'pronunciation': '/ˌpæpərˈdɛleɪ/',
                'pronunciation_ipa': '/ˌpæpərˈdɛleɪ/',
                'etymology': 'From Italian, from "pappare" meaning to eat hungrily or gobble up. The name suggests food that\'s eaten with great appetite.',
                'memory_tip': 'PAPPARDELLE sounds like "PAPA-DELL-AY" - think of "Papa" eating wide noodles from a "deli" saying "Ay!" with enjoyment.',
                'example_sentence': 'The chef served fresh _____ with a rich wild mushroom and truffle sauce.'
            },
            'papyrus': {
                'definition': 'An ancient writing material made from the pith of the papyrus plant, used extensively in ancient Egypt, Greece, and Rome; the plant itself (Cyperus papyrus) from which this material is made. Papyrus sheets were created by laying strips of the plant\'s pith in perpendicular layers and pressing them together. This material served as the primary writing surface before the widespread adoption of paper and parchment. Many important historical documents, including biblical texts and literary works, were preserved on papyrus. The word "paper" derives from papyrus.',
                'pronunciation': '/pəˈpaɪrəs/',
                'pronunciation_ipa': '/pəˈpaɪrəs/',
                'etymology': 'From Greek "papyros," possibly from Egyptian. The plant and writing material were central to ancient Mediterranean civilizations.',
                'memory_tip': 'PAPYRUS sounds like "PAPA-VIRUS" - think of ancient "papa" (father) documents that spread like a "virus" through history on this writing material.',
                'example_sentence': 'Archaeologists discovered fragments of ancient _____ containing previously unknown texts from the Roman period.'
            },
            'para': {
                'definition': 'A prefix meaning beside, alongside, or beyond; in medical terminology, often refers to a woman who has given birth; short for paratrooper or paragraph. As a prefix, "para-" appears in words like parallel, paradox, and paramedic. In obstetrics, para refers to the number of pregnancies carried to viable gestational age. In military contexts, para is shorthand for paratrooper. The term has multiple specialized meanings depending on context, but generally relates to the concept of "beside" or "alongside" something else.',
                'pronunciation': '/ˈpɛrə/',
                'pronunciation_ipa': '/ˈpɛrə/',
                'etymology': 'From Greek "para" meaning beside, alongside, or beyond. Used as a prefix in many English words and as a standalone term in various contexts.',
                'memory_tip': 'PARA sounds like "PAIR-A" - think of being "paired" alongside something, as para means "beside" or "alongside."',
                'example_sentence': 'The medical chart indicated she was a _____ 2, having given birth to two children.'
            },
            'parable': {
                'definition': 'A simple story used to illustrate a moral or spiritual lesson; a short allegorical narrative that teaches through analogy and comparison. Parables are found in many religious and philosophical traditions, with Jesus\' parables in the New Testament being among the most famous examples. These stories use familiar situations and characters to convey deeper truths about human nature, ethics, or spiritual principles. Effective parables engage listeners through relatable scenarios while revealing profound insights. The teaching method relies on the audience drawing connections between the story and the intended lesson.',
                'pronunciation': '/ˈpɛrəbəl/',
                'pronunciation_ipa': '/ˈpɛrəbəl/',
                'etymology': 'From Greek "parabole" meaning comparison or analogy, from "paraballein" meaning to compare. Related to "parabola" (mathematical curve).',
                'memory_tip': 'PARABLE sounds like "PAIR-ABLE" - think of stories that "pair" everyday situations with spiritual lessons, making them "able" to teach.',
                'example_sentence': 'The teacher used a _____ about seeds and soil to explain how different attitudes affect learning.'
            },
            'parabola': {
                'definition': 'A symmetrical open curve formed by the intersection of a cone with a plane parallel to its side; a U-shaped graph representing quadratic functions in mathematics. Parabolas have important properties in physics and engineering, as they describe the paths of projectiles under gravity and the shape of reflective surfaces in telescopes and satellite dishes. The mathematical equation for a parabola is typically written as y = ax² + bx + c. Parabolic shapes appear naturally in many contexts and have practical applications in optics, architecture, and ballistics.',
                'pronunciation': '/pəˈræbələ/',
                'pronunciation_ipa': '/pəˈræbələ/',
                'etymology': 'From Greek "parabole" meaning comparison or placing beside, from "paraballein." In geometry, refers to the curve\'s relationship to other conic sections.',
                'memory_tip': 'PARABOLA sounds like "PARA-BOWL-A" - think of a "bowl" shape that curves "para" (beside/around) in a U-shape.',
                'example_sentence': 'The water fountain\'s stream followed a perfect _____ arc as it rose and fell back to earth.'
            },
            'parachuted': {
                'definition': 'Past tense of parachute; descended from an aircraft using a parachute; moved or was placed suddenly into a new position or situation, often without preparation. In literal usage, it describes the action of jumping from an aircraft and using a parachute to slow descent. Figuratively, being "parachuted" into a situation means being suddenly placed in a new role, location, or circumstance without gradual transition or adequate preparation. The term often implies external placement rather than organic development or earned progression.',
                'pronunciation': '/ˈpɛrəˌʃutəd/',
                'pronunciation_ipa': '/ˈpɛrəˌʃutəd/',
                'etymology': 'From "parachute," from French "parachute," from "para-" (protection against) + "chute" (fall). Past tense indicates completed action.',
                'memory_tip': 'PARACHUTED = PARACHUTE + ED. Think of someone who already jumped and "chuted" down with their "para" (protective device).',
                'example_sentence': 'The new CEO was _____ into the struggling company without any prior experience in the industry.'
            },
            'paradise': {
                'definition': 'A place or state of supreme happiness, perfection, and beauty; in religious contexts, the garden of Eden or heaven. Paradise represents the ultimate ideal of peace, beauty, and contentment. Different cultures and religions have varying concepts of paradise, from the Islamic Jannah to the Christian heaven to secular notions of perfect places. The term is often used to describe beautiful locations, ideal situations, or states of complete satisfaction. Paradise implies freedom from suffering, conflict, and want, representing humanity\'s deepest aspirations for perfection and peace.',
                'pronunciation': '/ˈpɛrəˌdaɪs/',
                'pronunciation_ipa': '/ˈpɛrəˌdaɪs/',
                'etymology': 'From Greek "paradeisos," from Persian "pairidaeza" meaning walled garden or enclosure. Originally referred to royal Persian gardens.',
                'memory_tip': 'PARADISE sounds like "PAIR-A-DICE" - think of rolling a "pair" of perfect "dice" and winning the ultimate prize - paradise.',
                'example_sentence': 'The tropical island seemed like _____ with its pristine beaches and crystal-clear waters.'
            },
            'paraffin': {
                'definition': 'A waxy, white or colorless solid hydrocarbon mixture used in candles, waterproofing, and cosmetics; also known as paraffin wax. Paraffin is derived from petroleum and has various industrial and household applications. It\'s commonly used in candle making due to its clean burning properties and ability to hold fragrance. In food preservation, paraffin creates protective coatings. Medical applications include paraffin baths for therapeutic heat treatment. The substance is also used in cosmetics, polishes, and as a lubricant in various mechanical applications.',
                'pronunciation': '/ˈpɛrəfɪn/',
                'pronunciation_ipa': '/ˈpɛrəfɪn/',
                'etymology': 'From Latin "parum" (little) + "affinis" (related), referring to its low chemical reactivity. Named for its resistance to chemical reactions.',
                'memory_tip': 'PARAFFIN sounds like "PAIR-A-FIN" - think of a "pair" of candles with "fins" of wax, or "para" (beside) "affin" (related to wax).',
                'example_sentence': 'The physical therapist used a warm _____ bath to treat the patient\'s arthritis pain.'
            },
            'paragon': {
                'definition': 'A person or thing regarded as a perfect example of a particular quality; a model of excellence or perfection. Paragons represent the highest standard or ideal in their category, serving as benchmarks against which others are measured. The term suggests someone or something that embodies all the best qualities of its type without any significant flaws. Historical figures, literary characters, or contemporary individuals might be considered paragons of virtue, courage, wisdom, or other admirable traits. The concept implies both excellence and exemplary influence on others.',
                'pronunciation': '/ˈpɛrəˌɡɑn/',
                'pronunciation_ipa': '/ˈpɛrəˌɡɑn/',
                'etymology': 'From Italian "paragone" meaning touchstone or comparison, from Greek "parakonan" meaning to sharpen against. Originally referred to a touchstone for testing gold.',
                'memory_tip': 'PARAGON sounds like "PAIR-A-GONE" - think of someone so perfect that when you "pair" anyone with them, the comparison is "gone" (hopeless).',
                'example_sentence': 'Mother Teresa was considered a _____ of compassion and selfless service to humanity.'
            },
            'parallax': {
                'definition': 'The apparent displacement or difference in the apparent position of an object viewed along two different lines of sight; the angular difference between two viewpoints. In astronomy, parallax is used to measure distances to nearby stars by observing them from different points in Earth\'s orbit. In photography and optics, parallax can cause apparent misalignment between what the viewfinder shows and what the lens captures. The concept is fundamental to depth perception and stereoscopic vision. Understanding parallax is crucial in surveying, navigation, and various scientific measurements.',
                'pronunciation': '/ˈpɛrəˌlæks/',
                'pronunciation_ipa': '/ˈpɛrəˌlæks/',
                'etymology': 'From Greek "parallaxis" meaning alteration, from "parallassein" meaning to alter or change. Refers to the change in apparent position.',
                'memory_tip': 'PARALLAX = PARALLEL + AX(is). Think of "parallel" viewing lines that create an "axis" of difference in how objects appear.',
                'example_sentence': 'Astronomers used stellar _____ to calculate the distance from Earth to nearby star systems.'
            },
            'parallel': {
                'definition': 'Occurring or existing at the same time or in a similar way; running alongside something else, maintaining a constant distance without meeting. In geometry, parallel lines never intersect and remain equidistant throughout their length. In broader usage, parallel describes situations, processes, or phenomena that occur simultaneously or share similar characteristics. Computing uses parallel processing to perform multiple operations simultaneously. The concept extends to parallel universes, parallel evolution, and parallel development in various fields. Parallel structure in writing creates rhythm and emphasis through repetitive grammatical patterns.',
                'pronunciation': '/ˈpɛrəˌlɛl/',
                'pronunciation_ipa': '/ˈpɛrəˌlɛl/',
                'etymology': 'From Greek "parallelos," from "para" (alongside) + "allelos" (one another). Literally means "alongside one another."',
                'memory_tip': 'PARALLEL = PARA (alongside) + LLEL (like "level"). Think of two level lines running alongside each other, never meeting.',
                'example_sentence': 'The highway runs _____ to the coastline for several miles before turning inland.'
            },
            'paralysis': {
                'definition': 'The complete or partial loss of muscle function in part of the body; the state of being unable to act or function effectively. Medical paralysis results from damage to the nervous system, affecting voluntary muscle movement. Types include paraplegia (lower body), quadriplegia (all four limbs), and hemiplegia (one side). Figuratively, paralysis describes inability to make decisions or take action due to overwhelming circumstances, fear, or indecision. The condition can be temporary or permanent, affecting physical, emotional, or organizational function. Treatment approaches vary depending on the underlying cause.',
                'pronunciation': '/pəˈræləsɪs/',
                'pronunciation_ipa': '/pəˈræləsɪs/',
                'etymology': 'From Greek "paralysis" meaning loosening or disabling, from "paralyein" meaning to loosen or disable, from "para" + "lyein" (to loosen).',
                'memory_tip': 'PARALYSIS = PARA (beside/faulty) + LYSIS (loosening). Think of muscles being "loosened" or disconnected from normal control.',
                'example_sentence': 'The accident resulted in temporary _____ of his left arm, but physical therapy helped restore movement.'
            },
            'paramahamsa': {
                'definition': 'In Hinduism, a title for an ascetic or spiritual teacher who has attained the highest level of self-realization; a realized soul who has transcended all worldly attachments. The term literally means "supreme swan" and represents someone who has achieved liberation (moksha) and exists in a state of constant divine consciousness. Paramahamsa saints are considered to have complete mastery over their minds and emotions, living in pure awareness beyond the dualities of pleasure and pain. Famous paramahamsa include Sri Ramakrishna and others recognized for their spiritual attainment and teaching abilities.',
                'pronunciation': '/ˌpɛrəməˈhæmsə/',
                'pronunciation_ipa': '/ˌpɛrəməˈhæmsə/',
                'etymology': 'From Sanskrit "paramahamsa," from "parama" (supreme, highest) + "hamsa" (swan). The swan symbolizes discrimination between pure and impure.',
                'memory_tip': 'PARAMAHAMSA = PARAMA (supreme) + HAMSA (swan). Think of a "supreme swan" floating serenely - a spiritual master in perfect peace.',
                'example_sentence': 'The village revered the elderly _____ who had spent decades in meditation and service to others.'
            },
            'paramecium': {
                'definition': 'A genus of single-celled, slipper-shaped microorganisms belonging to the group of protozoans called ciliates. Paramecia are common in freshwater environments and are characterized by their oval shape and hair-like structures called cilia that enable movement and feeding. These microscopic organisms reproduce through binary fission and are often used in biology education to demonstrate cellular processes. Paramecia feed on bacteria and other small organisms, playing important roles in aquatic ecosystems. They exhibit behaviors like chemotaxis and can respond to various environmental stimuli.',
                'pronunciation': '/ˌpɛrəˈmiʃiəm/',
                'pronunciation_ipa': '/ˌpɛrəˈmiʃiəm/',
                'etymology': 'From Greek "paramekios" meaning oval-shaped, from "para" (beside) + "mekos" (length). Named for its elongated oval shape.',
                'memory_tip': 'PARAMECIUM sounds like "PARA-MECH-IUM" - think of a "para" (beside) shaped "mechanical" organism swimming in water.',
                'example_sentence': 'Under the microscope, students observed a _____ gliding through the water sample using its tiny hair-like cilia.'
            },
            'parameters': {
                'definition': 'Measurable factors or variables that define a system or set conditions within which something operates; numerical or other measurable factors that characterize a system. In mathematics, parameters are constants that appear in equations and can be varied to change the system\'s behavior. In computing, parameters are values passed to functions or programs. In general usage, parameters refer to the boundaries, limits, or guidelines within which activities must occur. Understanding parameters is crucial for scientific experiments, engineering designs, and problem-solving across various fields.',
                'pronunciation': '/pəˈræmətərz/',
                'pronunciation_ipa': '/pəˈræmətərz/',
                'etymology': 'From Greek "parametros," from "para" (beside) + "metron" (measure). Originally meant "auxiliary measure" in geometry.',
                'memory_tip': 'PARAMETERS = PARA (beside) + METERS (measures). Think of "beside" the main measures - additional values that define how things work.',
                'example_sentence': 'The engineering team carefully adjusted the _____ to optimize the system\'s performance.'
            },
            'paramountcy': {
                'definition': 'The state of being paramount; supreme authority or dominance; the condition of having the highest rank, importance, or priority. Paramountcy implies not just importance but supreme importance that supersedes all other considerations. In historical contexts, particularly in British colonial administration, paramountcy referred to supreme political authority over subsidiary states. The concept suggests ultimate power or influence that cannot be challenged or superseded. Achieving paramountcy means establishing unquestioned priority or authority in a particular domain or relationship.',
                'pronunciation': '/ˈpɛrəˌmaʊntsi/',
                'pronunciation_ipa': '/ˈpɛrəˌmaʊntsi/',
                'etymology': 'From "paramount" (from Old French "par amont" meaning "by above") + "-cy" suffix indicating state or condition.',
                'memory_tip': 'PARAMOUNTCY = PARAMOUNT + CY. Think of the "cy" (quality) of being "paramount" - supreme authority or highest importance.',
                'example_sentence': 'The constitution established the _____ of civilian authority over military decisions.'
            },
            'paraphrase': {
                'definition': 'To express the meaning of something written or spoken using different words, often to clarify or simplify; a restatement of a text or passage giving the meaning in another form. Paraphrasing involves understanding the original content and restating it in one\'s own words while preserving the essential meaning. This skill is crucial in academic writing, translation, and communication. Effective paraphrasing demonstrates comprehension and helps avoid plagiarism while incorporating sources. The process requires careful attention to maintaining accuracy while changing sentence structure and vocabulary.',
                'pronunciation': '/ˈpɛrəˌfreɪz/',
                'pronunciation_ipa': '/ˈpɛrəˌfreɪz/',
                'etymology': 'From Greek "paraphrasis," from "para" (alongside) + "phrasis" (speaking). Literally means "speaking alongside" or restating.',
                'memory_tip': 'PARAPHRASE = PARA (alongside) + PHRASE. Think of putting "phrases" "alongside" the original - saying the same thing differently.',
                'example_sentence': 'The student learned to _____ complex academic texts to demonstrate understanding without copying the original words.'
            },
            'paraplegic': {
                'definition': 'A person affected by paraplegia, which is paralysis of the lower half of the body including both legs; relating to or characterized by paraplegia. This condition typically results from spinal cord injury, disease, or congenital conditions affecting the thoracic or lumbar spine. Paraplegic individuals often use wheelchairs for mobility and may require various adaptive technologies and rehabilitation services. The term can be used as both a noun (a person with paraplegia) and an adjective (describing the condition or related accommodations). Modern accessibility advances have significantly improved quality of life for paraplegic individuals.',
                'pronunciation': '/ˌpɛrəˈplidʒɪk/',
                'pronunciation_ipa': '/ˌpɛrəˈplidʒɪk/',
                'etymology': 'From "paraplegia" (from Greek "para" meaning beside + "plegia" meaning stroke/paralysis) + "-ic" suffix meaning relating to.',
                'memory_tip': 'PARAPLEGIC = PARA (beside/partial) + PLEGIC (paralyzed). Think of "partial" paralysis affecting the lower body.',
                'example_sentence': 'The _____ athlete competed in wheelchair racing and became a Paralympic champion.'
            },
            'paraquat': {
                'definition': 'A highly toxic herbicide used to kill weeds and grass, known for its fast-acting but dangerous properties. Paraquat is one of the most widely used herbicides globally but is banned in many countries due to its toxicity to humans and animals. The chemical causes severe poisoning if ingested, inhaled, or absorbed through the skin, often leading to lung damage and death. Despite its effectiveness in agriculture, paraquat\'s health risks have led to strict regulations and calls for safer alternatives. The substance has been linked to Parkinson\'s disease and other serious health conditions.',
                'pronunciation': '/ˈpɛrəˌkwæt/',
                'pronunciation_ipa': '/ˈpɛrəˌkwæt/',
                'etymology': 'Chemical name derived from its structure as a para-disubstituted quaternary ammonium compound. The name reflects its chemical composition.',
                'memory_tip': 'PARAQUAT sounds like "PARA-SQUAT" - think of weeds that "squat" on the ground being eliminated by this "para" (beside/against) chemical.',
                'example_sentence': 'Agricultural workers were required to wear protective equipment when applying _____ due to its dangerous toxicity.'
            },
            'parasite': {
                'definition': 'An organism that lives in or on another organism (the host) and benefits at the host\'s expense; a person who habitually exploits others\' generosity without giving anything in return. Biological parasites include tapeworms, fleas, and mistletoe, which derive nutrition or shelter from their hosts. Parasitism is a widespread ecological relationship affecting all life forms. In human contexts, social parasites take advantage of others\' resources, time, or kindness without reciprocating. Understanding parasites is crucial for medicine, agriculture, and ecosystem management.',
                'pronunciation': '/ˈpɛrəˌsaɪt/',
                'pronunciation_ipa': '/ˈpɛrəˌsaɪt/',
                'etymology': 'From Greek "parasitos," from "para" (beside) + "sitos" (food). Originally meant someone who ate at another\'s table.',
                'memory_tip': 'PARASITE = PARA (beside) + SITE. Think of an organism that makes its "site" (home) "beside" or on another organism.',
                'example_sentence': 'The veterinarian treated the dog for intestinal _____ that were causing digestive problems.'
            },
            'parasol': {
                'definition': 'A lightweight umbrella used as protection from the sun; a sunshade typically carried by hand for personal shade. Parasols differ from rain umbrellas in their construction, often featuring decorative designs, lighter materials, and UV-protective fabrics. Historically, parasols were fashionable accessories particularly popular among women in the 18th and 19th centuries. They served both practical and social functions, indicating status and refinement. Modern parasols are still used for sun protection and as decorative elements in gardens, patios, and beach settings.',
                'pronunciation': '/ˈpɛrəˌsɔl/',
                'pronunciation_ipa': '/ˈpɛrəˌsɔl/',
                'etymology': 'From French "parasol," from Italian "parasole," from "para-" (protection against) + "sole" (sun). Literally means "protection against sun."',
                'memory_tip': 'PARASOL = PARA (protection) + SOL (sun). Think of protection "para" the "sol" (sun) - a sunshade umbrella.',
                'example_sentence': 'She carried an elegant lace _____ to shield herself from the afternoon sun during the garden party.'
            },
            'parathas': {
                'definition': 'Flatbreads from Indian cuisine, typically made from wheat flour and cooked on a griddle with oil or ghee. Parathas can be plain or stuffed with various fillings such as potatoes, cauliflower, paneer, or meat. The dough is often layered to create flaky, crispy textures. Different regions of India have distinct paratha varieties and preparation methods. These versatile breads are commonly eaten for breakfast or lunch, often accompanied by yogurt, pickles, or curries. Making parathas requires skill in rolling, layering, and cooking techniques.',
                'pronunciation': '/pəˈrɑtəz/',
                'pronunciation_ipa': '/pəˈrɑtəz/',
                'etymology': 'From Hindi "paratha," possibly from Sanskrit "parishta" meaning layered or folded. Refers to the bread\'s layered preparation method.',
                'memory_tip': 'PARATHAS sounds like "PARA-TAS" - think of "para" (layered) "tas" (flatbreads) - layered Indian breads cooked on griddles.',
                'example_sentence': 'For breakfast, she made stuffed _____ filled with spiced potatoes and served them with fresh yogurt.'
            },
            'parcel': {
                'definition': 'A package or bundle wrapped for mailing or carrying; a piece or portion of land; to divide into parts or wrap up for shipment. In shipping, parcels are packages sent through postal or delivery services. In real estate, a parcel refers to a specific piece of property with defined boundaries. The verb form means to divide something into portions or to wrap items for shipping. Parcel services are essential for e-commerce and global trade. Legal documents often reference land parcels for property ownership and taxation purposes.',
                'pronunciation': '/ˈpɑrsəl/',
                'pronunciation_ipa': '/ˈpɑrsəl/',
                'etymology': 'From Old French "parcelle," from Latin "particula" meaning small part. Related to "particle" and "part."',
                'memory_tip': 'PARCEL sounds like "PART-SELL" - think of "part" of something you "sell" and need to package, or a "part" of land.',
                'example_sentence': 'The delivery service left the _____ at the front door when no one was home to sign for it.'
            },
            'parchment': {
                'definition': 'Writing material made from specially prepared animal skin, typically from sheep, goats, or calves; a document written on such material; modern paper made to resemble traditional parchment. Parchment was the primary writing surface in medieval Europe before paper became widespread. The preparation process involves cleaning, stretching, and treating animal skins to create a smooth, durable surface. Important historical documents, including constitutions and religious texts, were written on parchment. Modern parchment paper is used in cooking and baking for its non-stick and heat-resistant properties.',
                'pronunciation': '/ˈpɑrtʃmənt/',
                'pronunciation_ipa': '/ˈpɑrtʃmənt/',
                'etymology': 'From Old French "parchemin," from Latin "pergamena," referring to Pergamon, an ancient city where this writing material was refined.',
                'memory_tip': 'PARCHMENT sounds like "PARCH-MENT" - think of animal skin that\'s been "parched" (dried) to make writing material.',
                'example_sentence': 'The ancient _____ scroll contained medieval religious texts written in elaborate calligraphy.'
            },
            'pardon': {
                'definition': 'Forgiveness for an offense; an official release from punishment for a crime; to forgive or excuse someone for an error or offense. In legal contexts, pardons are granted by heads of state or other authorized officials to release individuals from criminal penalties. The act of pardoning implies mercy and the decision to overlook wrongdoing. Social pardons involve personal forgiveness for mistakes, misunderstandings, or minor offenses. The concept is fundamental to restorative justice, diplomacy, and interpersonal relationships. Pardons can be conditional or unconditional.',
                'pronunciation': '/ˈpɑrdən/',
                'pronunciation_ipa': '/ˈpɑrdən/',
                'etymology': 'From Old French "pardoner," from Medieval Latin "perdonare," from "per" (thoroughly) + "donare" (to give). Literally means "to give thoroughly."',
                'memory_tip': 'PARDON sounds like "PAR-DON" - think of a "par" (equal) exchange where you "don" (give) forgiveness instead of punishment.',
                'example_sentence': 'The governor granted a _____ to the prisoner who had served twenty years for a crime he didn\'t commit.'
            },
            'pareidolia': {
                'definition': 'The psychological phenomenon of perceiving familiar patterns, shapes, or meaningful images in random or ambiguous stimuli; seeing faces in clouds or hearing voices in noise. Pareidolia is a normal cognitive process that helps humans quickly identify potentially important patterns in their environment. Common examples include seeing animals in cloud formations, faces in rock formations, or religious figures in natural objects. This perceptual tendency has evolutionary advantages for recognizing faces and threats quickly. Artists and designers sometimes deliberately use pareidolia to create engaging visual effects.',
                'pronunciation': '/ˌpɛrɪˈdoʊliə/',
                'pronunciation_ipa': '/ˌpɛrɪˈdoʊliə/',
                'etymology': 'From Greek "para" (beside) + "eidolon" (image or form). Coined in 1958 to describe the tendency to perceive patterns in random stimuli.',
                'memory_tip': 'PAREIDOLIA = PARA (beside) + EIDOL (image) + IA. Think of seeing "images" "beside" what\'s really there - patterns in randomness.',
                'example_sentence': 'His _____ made him see a smiling face in the arrangement of windows on the office building.'
            },
            'parenthetic': {
                'definition': 'Relating to or inserted as a parenthesis; characterized by the use of parentheses or expressing something as an aside or interruption. Parenthetic expressions provide additional information that supplements but doesn\'t fundamentally alter the main statement. In grammar, parenthetic elements can be words, phrases, or clauses set apart by punctuation marks. These expressions often clarify, emphasize, or provide background information. Writers use parenthetic elements to add nuance, humor, or supplementary details without disrupting the main flow of ideas.',
                'pronunciation': '/ˌpɛrənˈθɛtɪk/',
                'pronunciation_ipa': '/ˌpɛrənˈθɛtɪk/',
                'etymology': 'From "parenthesis" (from Greek "parenthesis" meaning insertion) + "-ic" suffix meaning relating to or characterized by.',
                'memory_tip': 'PARENTHETIC = PARENTHESIS + IC. Think of writing that\'s characterized by lots of parentheses - side comments and additions.',
                'example_sentence': 'The professor\'s lecture was full of _____ remarks that provided interesting but tangential information.'
            },
            'pariah': {
                'definition': 'A social outcast; someone who is despised or rejected by their community or society; originally, a member of a low caste in southern India. In modern usage, pariah describes anyone who has been ostracized, shunned, or excluded from social groups due to their actions, beliefs, or circumstances. The condition of being a pariah can result from moral transgressions, political positions, or simply being different from social norms. The term carries connotations of isolation, rejection, and social marginalization.',
                'pronunciation': '/pəˈraɪə/',
                'pronunciation_ipa': '/pəˈraɪə/',
                'etymology': 'From Tamil "paraiyar," the name of a low caste in southern India. The term entered English through colonial contact and broadened in meaning.',
                'memory_tip': 'PARIAH sounds like "PAIR-EYE-AH" - think of someone whom people "pair" their "eyes" on with rejection, saying "ah" in disapproval.',
                'example_sentence': 'After the scandal broke, he became a _____ in the business community, avoided by former colleagues and friends.'
            },
            'park': {
                'definition': 'An area of land set aside for public recreation, typically featuring grass, trees, and recreational facilities; to place or leave a vehicle in a particular location; to temporarily place or set aside something. Public parks provide green spaces in urban areas for exercise, relaxation, and community activities. National parks preserve natural landscapes and wildlife for conservation and tourism. The verb "park" extends beyond vehicles to mean temporarily positioning anything in a designated spot. Parks serve important environmental, social, and health functions in communities.',
                'pronunciation': '/pɑrk/',
                'pronunciation_ipa': '/pɑrk/',
                'etymology': 'From Old French "parc," from Medieval Latin "parcus" meaning enclosure. Originally referred to enclosed hunting grounds.',
                'memory_tip': 'PARK is a simple word - think of a "park" where you can "park" your car and enjoy green spaces with trees and grass.',
                'example_sentence': 'The family spent the afternoon in the _____, playing on the playground and having a picnic under the oak trees.'
            },
            'parkour': {
                'definition': 'A physical discipline and sport involving moving through environments by running, jumping, climbing, and vaulting over obstacles in the most efficient way possible. Parkour emphasizes fluid movement, creativity, and adaptability in navigating urban and natural environments. Practitioners, called traceurs (male) or traceuses (female), develop strength, agility, and mental focus. The discipline originated in France and has spread worldwide, influencing fitness training, military conditioning, and popular culture. Parkour philosophy emphasizes personal development, overcoming obstacles, and helping others.',
                'pronunciation': '/pɑrˈkʊr/',
                'pronunciation_ipa': '/pɑrˈkʊr/',
                'etymology': 'From French, derived from "parcours du combattant" (obstacle course), ultimately from "parcourir" meaning to run through or traverse.',
                'memory_tip': 'PARKOUR sounds like "PARK-CORE" - think of "core" strength needed to move through "park" obstacles efficiently.',
                'example_sentence': 'The _____ athlete gracefully vaulted over benches and walls, making the urban landscape look like a playground.'
            },
            'parley': {
                'definition': 'A conference or discussion, especially between enemies or opposing parties to discuss terms or resolve disputes; to hold such a discussion. Parleys are formal meetings designed to negotiate, exchange information, or seek peaceful resolution to conflicts. Historical parleys occurred between military commanders before battles or during sieges. The term implies temporary suspension of hostilities for diplomatic communication. Modern parleys include peace negotiations, labor disputes, and international diplomacy. The success of parleys depends on good faith participation and willingness to find common ground.',
                'pronunciation': '/ˈpɑrli/',
                'pronunciation_ipa': '/ˈpɑrli/',
                'etymology': 'From Old French "parler" meaning to speak or talk. Related to "parliament" and other words involving formal speaking or discussion.',
                'memory_tip': 'PARLEY sounds like "PAR-LEY" - think of a "par" (equal) meeting where opposing sides "lay" down weapons to talk.',
                'example_sentence': 'The ship\'s captain requested a _____ with the pirate leader to negotiate the release of his crew.'
            },
            'parliamentary': {
                'definition': 'Relating to a parliament or parliamentary system of government; following the rules and procedures of formal legislative assembly. Parliamentary systems feature elected representatives who form governments based on majority support. Parliamentary procedure governs how meetings are conducted, debates are held, and decisions are made in formal assemblies. The term describes democratic processes, legislative functions, and governmental structures in many countries. Parliamentary language and behavior follow established protocols designed to ensure orderly, fair, and effective governance.',
                'pronunciation': '/ˌpɑrləˈmɛntəri/',
                'pronunciation_ipa': '/ˌpɑrləˈmɛntəri/',
                'etymology': 'From "parliament" (from Old French "parlement," from "parler" to speak) + "-ary" suffix meaning relating to or connected with.',
                'memory_tip': 'PARLIAMENTARY = PARLIAMENT + ARY. Think of things relating to "parliament" - formal government procedures and democratic processes.',
                'example_sentence': 'The committee followed strict _____ procedure to ensure all members had equal opportunity to express their views.'
            },
            'parmentier': {
                'definition': 'A culinary term referring to dishes prepared with potatoes, named after Antoine-Augustin Parmentier, an 18th-century French pharmacist who promoted potato cultivation in France. Parmentier dishes typically feature potatoes as a primary ingredient, often in the form of mashed potatoes, potato gratins, or potato-topped casseroles. The most famous is "hachis Parmentier," similar to shepherd\'s pie with a potato topping. Parmentier\'s efforts helped overcome French resistance to potatoes and established them as a staple food. The term honors his contribution to French cuisine and nutrition.',
                'pronunciation': '/ˌpɑrmənˈtir/',
                'pronunciation_ipa': '/ˌpɑrmənˈtir/',
                'etymology': 'Named after Antoine-Augustin Parmentier (1737-1813), who promoted potato cultivation in France and helped establish potatoes in French cuisine.',
                'memory_tip': 'PARMENTIER sounds like "PAR-MEN-TIER" - think of a "par" (equal) "men" in a "tier" of French cooks who made potatoes famous.',
                'example_sentence': 'The restaurant\'s _____ featured layers of seasoned ground beef topped with creamy mashed potatoes.'
            },
            'parochial': {
                'definition': 'Relating to a church parish; narrow or limited in scope, outlook, or understanding; showing concern only for local or narrow interests. In religious contexts, parochial refers to parish-level administration and activities. In broader usage, parochial describes attitudes or perspectives that are provincial, narrow-minded, or focused only on local concerns without considering wider implications. Parochial schools are typically affiliated with religious organizations. The term often carries negative connotations of insularity and lack of broader perspective or cosmopolitan understanding.',
                'pronunciation': '/pəˈroʊkiəl/',
                'pronunciation_ipa': '/pəˈroʊkiəl/',
                'etymology': 'From Latin "parochialis," from "parochia" meaning parish, from Greek "paroikia" meaning neighborhood. Originally referred to parish boundaries.',
                'memory_tip': 'PAROCHIAL = PARISH + IAL. Think of being limited to your "parish" - narrow, local thinking without broader perspective.',
                'example_sentence': 'His _____ worldview prevented him from understanding the global implications of the environmental crisis.'
            },
            'parodic': {
                'definition': 'Relating to or characteristic of parody; designed to imitate and mock or comment on an original work through exaggerated mimicry. Parodic works deliberately copy and distort elements of their targets to create humor, criticism, or commentary. The parodic style involves recognizable imitation combined with deliberate exaggeration or subversion. Literature, music, film, and art all employ parodic techniques for entertainment and social commentary. Effective parodic works require audience familiarity with the original to appreciate the humor and critique.',
                'pronunciation': '/pəˈrɑdɪk/',
                'pronunciation_ipa': '/pəˈrɑdɪk/',
                'etymology': 'From "parody" (from Greek "parodia," from "para" meaning beside + "odia" meaning song) + "-ic" suffix meaning relating to.',
                'memory_tip': 'PARODIC = PARODY + IC. Think of something that\'s characterized by "parody" - imitating and mocking other works.',
                'example_sentence': 'The film\'s _____ style cleverly mocked superhero movie conventions while telling its own story.'
            },
            'paronomasia': {
                'definition': 'A play on words; a pun that exploits different meanings of similar-sounding words or different meanings of the same word for humorous or rhetorical effect. Paronomasia is a literary and rhetorical device that creates word play through sound similarities and semantic differences. The technique appears in poetry, comedy, advertising, and everyday conversation. Effective paronomasia requires clever manipulation of language to create double meanings, unexpected connections, or humorous confusion. The device demonstrates linguistic creativity and can enhance memorability and entertainment value.',
                'pronunciation': '/ˌpɛrənəˈmeɪʒə/',
                'pronunciation_ipa': '/ˌpɛrənəˈmeɪʒə/',
                'etymology': 'From Greek "paronomasia," from "para" (beside) + "onomasia" (naming). Literally means "beside-naming" or calling by a different name.',
                'memory_tip': 'PARONOMASIA = PARA (beside) + ONOMASIA (naming). Think of "beside naming" - using words "beside" their normal meaning for puns.',
                'example_sentence': 'Shakespeare\'s plays are filled with _____, demonstrating his mastery of wordplay and double meanings.'
            },
            'paroxysm': {
                'definition': 'A sudden, violent attack or outburst of a particular emotion or activity; a severe bout or spasm of pain, coughing, or other symptoms. In medical contexts, paroxysms are acute episodes of symptoms that come on suddenly and intensely. Emotional paroxysms involve overwhelming surges of feeling like rage, grief, or joy. The term emphasizes the sudden, intense, and often uncontrollable nature of the experience. Paroxysms can be physical, emotional, or behavioral, typically lasting a relatively short time but with significant impact.',
                'pronunciation': '/ˈpɛrəkˌsɪzəm/',
                'pronunciation_ipa': '/ˈpɛrəkˌsɪzəm/',
                'etymology': 'From Greek "paroxysmos" meaning irritation or exacerbation, from "paroxynein" meaning to provoke or irritate.',
                'memory_tip': 'PAROXYSM sounds like "PAIR-OX-SPASM" - think of a "pair" of "oxen" having a sudden "spasm" of intense activity.',
                'example_sentence': 'He experienced a _____ of coughing that lasted several minutes and left him exhausted.'
            },
            'parquet': {
                'definition': 'A type of hardwood flooring made from small pieces of wood arranged in geometric patterns; the main floor area of a theater, typically containing the most expensive seats. Parquet flooring consists of wood blocks or strips arranged in decorative patterns like herringbone, chevron, or basketweave. The technique originated in 17th-century France and became popular in elegant homes and public buildings. In theaters, the parquet refers to the orchestra level seating area closest to the stage. Quality parquet floors are valued for their beauty, durability, and craftsmanship.',
                'pronunciation': '/pɑrˈkeɪ/',
                'pronunciation_ipa': '/pɑrˈkeɪ/',
                'etymology': 'From French "parquet," diminutive of "parc" meaning park or enclosure. Originally referred to a small enclosed area.',
                'memory_tip': 'PARQUET sounds like "PARK-AY" - think of a "park" where you say "ay!" at the beautiful geometric wood patterns on the floor.',
                'example_sentence': 'The ballroom featured an intricate _____ floor with a herringbone pattern that had been maintained for over a century.'
            },
            'parquetit': {
                'definition': 'This appears to be a rare or specialized term with limited standard documentation. Based on linguistic analysis, it might be related to "parquet" flooring or could be a technical term in a specialized field. Without clear definitive sources, it\'s difficult to provide a comprehensive definition. The term may be a variant, technical specification, or specialized usage related to parquet flooring techniques or materials. It could also be a misspelling or variant of another term. More context would be needed to provide a precise definition.',
                'pronunciation': '/pɑrˈkeɪt/',
                'pronunciation_ipa': '/pɑrˈkeɪt/',
                'etymology': 'Possibly related to "parquet" with a diminutive or technical suffix. The exact etymological development is uncertain without more definitive sources.',
                'memory_tip': 'PARQUETIT sounds like "PARQUET-IT" - think of a small or specific type of parquet flooring technique or pattern.',
                'example_sentence': 'The craftsman used a special _____ technique to create the intricate border design in the wooden floor.'
            },
            'parr': {
                'definition': 'A young salmon or trout in its first stage of development, typically characterized by distinctive vertical markings on its sides. Parr are juvenile salmonids that have not yet undergone the physiological changes needed for life in saltwater. These fish spend one to four years in freshwater streams and rivers before transforming into smolts, which can then migrate to the ocean. Parr are important indicators of ecosystem health and are studied by fisheries biologists to understand salmon population dynamics. The distinctive parr marks help camouflage the young fish in their freshwater habitat.',
                'pronunciation': '/pɑr/',
                'pronunciation_ipa': '/pɑr/',
                'etymology': 'Possibly from Scottish or northern English dialect. The origin is uncertain but relates to juvenile salmon terminology in fishing communities.',
                'memory_tip': 'PARR sounds like "PAR" in golf - think of young salmon that are "par" for the course - normal juvenile fish with distinctive markings.',
                'example_sentence': 'The biologist counted dozens of salmon _____ in the stream, indicating a healthy population of juvenile fish.'
            },
            'parrot': {
                'definition': 'A colorful tropical bird with a curved beak, known for its ability to mimic human speech and other sounds; to repeat someone else\'s words or ideas without understanding or thinking. Parrots are intelligent birds found primarily in tropical and subtropical regions. Many species are kept as pets due to their social nature, longevity, and speaking ability. In figurative usage, parroting means mindless repetition without comprehension or original thought. The verb suggests mechanical copying rather than understanding or creative expression.',
                'pronunciation': '/ˈpɛrət/',
                'pronunciation_ipa': '/ˈpɛrət/',
                'etymology': 'From French "perrot," possibly from "Pierre" (Peter), a common name for pet birds. Related to the tendency to give human names to talking birds.',
                'memory_tip': 'PARROT sounds like "PAIR-ROT" - think of a "pair" of colorful birds that "rot"ate their heads and repeat what they hear.',
                'example_sentence': 'The colorful _____ entertained visitors by mimicking phrases it had learned from its trainer.'
            },
            'parroting': {
                'definition': 'The act of mindlessly repeating what someone else has said without understanding or original thought; mechanically copying speech, ideas, or behaviors. Parroting suggests repetition without comprehension, creativity, or personal input. In educational contexts, parroting is often contrasted with true learning and understanding. The term carries negative connotations of intellectual laziness or inability to think independently. However, parroting can also be a normal part of learning processes, particularly in language acquisition and skill development.',
                'pronunciation': '/ˈpɛrətɪŋ/',
                'pronunciation_ipa': '/ˈpɛrətɪŋ/',
                'etymology': 'Present participle of "parrot," from the bird\'s behavior of repeating sounds without understanding their meaning.',
                'memory_tip': 'PARROTING = PARROT + ING. Think of what parrots do - repeating sounds without understanding what they mean.',
                'example_sentence': 'The student was accused of merely _____ the textbook rather than demonstrating genuine understanding of the concepts.'
            }
        }
        
        return word_data.get(word, {
            'definition': f'[Definition for {word} not found in comprehensive dataset]',
            'pronunciation': f'[Pronunciation for {word} not available]',
            'pronunciation_ipa': f'[IPA for {word} not available]',
            'etymology': f'[Etymology for {word} not available]',
            'memory_tip': f'[Memory tip for {word} not available]',
            'example_sentence': f'[Example sentence for {word} not available]'
        })

def process_batch_127():
    processor = Batch127Processor()
    
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_127_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_127_processed.csv'
    
    combined_words = processor.detect_combined_words()
    if combined_words:
        logging.warning(f"Detected combined words that need manual review: {combined_words}")
    
    processed_data = []
    successful_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            word = row['word'].strip()
            if not word:
                continue
                
            try:
                claude_data = processor.get_comprehensive_claude_data(word)
                
                if claude_data['definition'] != f'[Definition for {word} not found in comprehensive dataset]':
                    difficulty_scores = processor.difficulty_calc.calculate_difficulty_score(
                        word, claude_data['definition'], claude_data['etymology']
                    )
                    
                    processed_row = {
                        'word': word,
                        'years': row['years'],
                        'source_files': row['source_files'],
                        'source_difficulties': row['source_difficulties'],
                        'definition': claude_data['definition'],
                        'pronunciation': claude_data['pronunciation'],
                        'pronunciation_ipa': claude_data['pronunciation_ipa'],
                        'etymology': claude_data['etymology'],
                        'memory_tip': claude_data['memory_tip'],
                        'example_sentence': claude_data['example_sentence'],
                        'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                        'word_frequency_score': difficulty_scores['word_frequency_score'],
                        'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                        'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                        'difficulty': difficulty_scores['difficulty'],
                        'combined_word_error': word in combined_words,
                        'source': 'Claude'
                    }
                    
                    processed_data.append(processed_row)
                    successful_count += 1
                    logging.info(f"Successfully processed word {successful_count}: {word}")
                else:
                    logging.error(f"No data found for word: {word}")
                    
            except Exception as e:
                logging.error(f"Error processing word '{word}': {str(e)}")
    
    fieldnames = [
        'word', 'years', 'source_files', 'source_difficulties', 'definition',
        'pronunciation', 'pronunciation_ipa', 'etymology', 'memory_tip', 'example_sentence',
        'phonetic_transparency_score', 'word_frequency_score', 'morphological_complexity_score',
        'etymology_complexity_score', 'difficulty', 'combined_word_error', 'source'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)
    
    logging.info(f"Batch 127 processing complete. Processed {successful_count}/50 words.")
    logging.info(f"Output saved to: {output_file}")
    
    if combined_words:
        logging.warning(f"Combined word errors detected: {combined_words}")
    
    return successful_count

if __name__ == "__main__":
    process_batch_127()