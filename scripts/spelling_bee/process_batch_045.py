#!/usr/bin/env python3

import pandas as pd
import math

# Combined word error data
COMBINED_WORD_ERRORS = ['curiecurmudgeon']

class DifficultyCalculator:
    def calculate_difficulty_score(self, word):
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._estimate_word_frequency(word)
        morphological_score = self._calculate_morphological_complexity(word)
        etymology_score = self._calculate_etymology_complexity(word)
        
        return {
            'difficulty_phonetic': phonetic_score,
            'difficulty_frequency': frequency_score, 
            'difficulty_morphological': morphological_score,
            'difficulty_etymology': etymology_score
        }
    
    def _calculate_phonetic_transparency(self, word):
        irregular_patterns = ['gh', 'ph', 'ch', 'tion', 'sion', 'eau', 'ough']
        silent_letters = ['b', 'k', 'l', 'w', 'h']
        
        score = 1.0
        word_lower = word.lower()
        
        for pattern in irregular_patterns:
            if pattern in word_lower:
                score += 0.5
                
        for i, char in enumerate(word_lower):
            if char in silent_letters and i > 0:
                score += 0.3
                
        return min(score, 4.0)
    
    def _estimate_word_frequency(self, word):
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'man', 'men', 'run', 'too', 'use', 'way', 'where', 'come', 'from', 'have', 'here', 'just', 'like', 'long', 'look', 'made', 'make', 'many', 'over', 'said', 'some', 'time', 'very', 'when', 'will', 'your']
        
        word_lower = word.lower()
        word_len = len(word)
        
        if word_lower in common_words:
            return 1.0
        elif word_len <= 4:
            return 1.5
        elif word_len <= 6:
            return 2.0
        elif word_len <= 8:
            return 2.5
        elif word_len <= 10:
            return 3.0
        else:
            return 3.5
    
    def _calculate_morphological_complexity(self, word):
        prefixes = ['un', 're', 'in', 'dis', 'en', 'non', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'under']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'ness', 'ment', 'ful', 'less', 'able', 'ous', 'ive', 'al', 'ic', 'ance', 'ence', 'age', 'ary', 'ery', 'ity', 'fy', 'ize', 'ise']
        
        score = 1.0
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix) and len(word) > len(prefix) + 2:
                score += 0.5
                break
                
        for suffix in suffixes:
            if word_lower.endswith(suffix) and len(word) > len(suffix) + 2:
                score += 0.5
                break
                
        syllable_count = max(1, len([c for c in word_lower if c in 'aeiou']))
        if syllable_count >= 4:
            score += 1.0
        elif syllable_count >= 3:
            score += 0.5
            
        return min(score, 4.0)
    
    def _calculate_etymology_complexity(self, word):
        etymology_indicators = {
            'greek': ['ph', 'ch', 'th', 'ps', 'rh', 'pt'],
            'latin': ['tion', 'sion', 'ct', 'sc', 'qu'],
            'french': ['eau', 'eur', 'oux', 'ille'],
            'other': ['sch', 'tsch', 'cz', 'sz']
        }
        
        word_lower = word.lower()
        
        for origin, patterns in etymology_indicators.items():
            for pattern in patterns:
                if pattern in word_lower:
                    if origin in ['greek', 'other']:
                        return 3.5
                    elif origin == 'latin':
                        return 3.0
                    elif origin == 'french':
                        return 2.5
                        
        return 2.0

# Word data with comprehensive educational definitions
WORD_DATA = {
    'crouched': {
        'definition': 'Past tense of crouch; positioned low with knees bent and body close to the ground. This position involves bending the knees and lowering the torso while keeping the feet planted, often used for hiding, stability, or preparing to spring into action. Crouching is a common defensive posture in both humans and animals, providing better balance and making one less visible. Athletes frequently crouch at starting lines to maximize their explosive power when beginning a race. The position distributes weight evenly and lowers the center of gravity for enhanced stability.',
        'part_of_speech': 'verb (past tense)',
        'pronunciation_guide': 'KROWCHD (/kraʊtʃt/)',
        'etymology': 'From Middle English "crouchen," possibly from Old French "crochir" (to become bent)',
        'memory_tips': 'Think "crouch + ed" - bent down low position in the past',
        'alternate_spellings': 'None',
        'language_origin': 'Middle English/Old French',
        'example_sentence': 'The cat _____ behind the bushes, waiting for the perfect moment to pounce on the unsuspecting bird.'
    },
    'croustade': {
        'definition': 'A crispy pastry shell or bread case used to hold savory or sweet fillings, often served as an appetizer or dessert. Croustades are typically made from puff pastry, phyllo dough, or bread that is shaped into small cups or baskets and baked until golden brown. These versatile vessels can be filled with ingredients like creamed seafood, vegetables, fruits, or custards. The term encompasses both individual serving-sized portions and larger presentations. French cuisine frequently features croustades as elegant hors d\'oeuvres at formal gatherings.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kroo-STAHD (/kruˈstɑd/)',
        'etymology': 'French, from "croustade," related to "croûte" (crust)',
        'memory_tips': 'Think "crust + ade" - a crusty shell that holds fillings like lemonade holds liquid',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The chef filled each delicate _____ with a mixture of lobster and herbs for the elegant reception.'
    },
    'crowd': {
        'definition': 'A large group of people gathered together in one place; to fill a space with too many people or things; to press closely together. Crowds form naturally at events, gatherings, or popular locations where many individuals converge. The psychological dynamics of crowds can influence individual behavior, sometimes leading to collective actions. Managing crowds requires careful planning to ensure safety and smooth movement. In marketing, businesses often leverage crowd appeal to attract more customers.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KROWD (/kraʊd/)',
        'etymology': 'From Old English "crudan" (to press, push)',
        'memory_tips': 'Think of a "loud crowd" - many people making noise together',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'A large _____ gathered in the town square to celebrate the annual harvest festival.'
    },
    'crown': {
        'definition': 'A circular ornamental headdress worn by monarchs as a symbol of sovereignty; the top or highest part of something; to place a crown on someone\'s head; to complete or perfect something. Crowns represent power, authority, and achievement across cultures. In dentistry, a crown is a cap placed over a damaged tooth. The crown of a tree refers to its uppermost branches and foliage. Figuratively, crowning achievements represent the pinnacle of success.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KROWN (/kraʊn/)',
        'etymology': 'From Old French "corone," from Latin "corona" (garland, crown)',
        'memory_tips': 'Think of a king\'s golden crown - the ultimate symbol of royal power',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The jeweled _____ sparkled magnificently as the new queen was coronated in the ancient cathedral.'
    },
    'crucial': {
        'definition': 'Extremely important or essential; decisive in determining the outcome of something. Crucial elements are those that significantly impact success or failure. In medical contexts, crucial decisions can mean the difference between life and death. Business strategies often depend on crucial timing and market conditions. The word implies that without this particular element, the desired result cannot be achieved.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KROO-shuhl (/ˈkruʃəl/)',
        'etymology': 'From Latin "crux" (cross), referring to a critical decision point',
        'memory_tips': 'Think "cross + ial" - like standing at a crossroads where the decision is critical',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The final exam score was _____ for determining whether she would graduate with honors.'
    },
    'cruciferous': {
        'definition': 'Belonging to the mustard family of plants (Brassicaceae), characterized by flowers with four petals arranged in a cross shape. Cruciferous vegetables include broccoli, cauliflower, cabbage, kale, Brussels sprouts, and radishes. These plants are renowned for their nutritional value and cancer-fighting compounds called glucosinolates. The cross-shaped flower structure gives this plant family its distinctive name. Many cruciferous vegetables are cool-season crops that thrive in temperate climates.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kroo-SIF-er-uhs (/kruˈsɪfərəs/)',
        'etymology': 'From Latin "crux" (cross) + "ferre" (to bear), referring to cross-shaped flowers',
        'memory_tips': 'Think "crucifix + erous" - plants that bear cross-shaped flowers',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The nutritionist recommended eating more _____ vegetables like broccoli and kale for their health benefits.'
    },
    'cruising': {
        'definition': 'Traveling smoothly at a steady, moderate speed; sailing for pleasure; moving effortlessly through water, air, or land. In aviation, cruising altitude is the optimal height for fuel efficiency during long flights. Cruise ships provide leisurely vacation experiences on the ocean. Cars cruise at highway speeds for optimal fuel economy. The term implies a relaxed, unhurried pace rather than maximum speed or effort.',
        'part_of_speech': 'verb (present participle), noun',
        'pronunciation_guide': 'KROO-zing (/ˈkruzɪŋ/)',
        'etymology': 'From Dutch "kruisen" (to cross, cruise)',
        'memory_tips': 'Think of a cruise ship sailing smoothly across the ocean',
        'alternate_spellings': 'None',
        'language_origin': 'Dutch',
        'example_sentence': 'The family spent their vacation _____ through the Mediterranean, stopping at various historic ports.'
    },
    'crumpet': {
        'definition': 'A small, round, spongy cake with a flat bottom and holey top surface, typically toasted and served with butter. Crumpets are a traditional British teatime treat made from a yeasted batter cooked in metal rings on a griddle. The distinctive texture comes from the yeast fermentation process, creating numerous small holes that absorb butter and other toppings. Unlike English muffins, crumpets are not sliced before toasting. They represent comfort food in British cuisine.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRUHM-pit (/ˈkrʌmpɪt/)',
        'etymology': 'Origin uncertain, possibly from "crompid cake" (curled-up cake)',
        'memory_tips': 'Think "crumb + pet" - a spongy bread full of holes for catching crumbs',
        'alternate_spellings': 'None',
        'language_origin': 'English (uncertain origin)',
        'example_sentence': 'She spread honey on the warm _____ and enjoyed it with her afternoon tea.'
    },
    'crust': {
        'definition': 'The hard, outer layer of bread; the solid outermost layer of the Earth; any hard surface layer; to form a hard outer coating. Earth\'s crust is the thin, rocky shell that forms our planet\'s surface. Bread crust provides texture contrast and helps preserve the soft interior. In geology, crustal movements cause earthquakes and mountain formation. Medical conditions can cause skin to crust over during healing processes.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KRUHST (/krʌst/)',
        'etymology': 'From Latin "crusta" (rind, shell, crust)',
        'memory_tips': 'Think of the crusty outer layer of fresh bread',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The baker scored the _____ of the sourdough loaf to create an attractive pattern.'
    },
    'crustaceans': {
        'definition': 'A large class of arthropods including crabs, lobsters, shrimp, and barnacles, characterized by hard exoskeletons and jointed legs. These marine animals have segmented bodies, compound eyes, and typically shed their shells as they grow. Most crustaceans breathe through gills and live in aquatic environments, though some like pill bugs are terrestrial. They play crucial roles in marine ecosystems as both predators and prey. Many species are commercially important as seafood.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kruhs-TAY-shuhnz (/krʌˈsteɪʃənz/)',
        'etymology': 'From Latin "crusta" (shell) + suffix indicating animals with that characteristic',
        'memory_tips': 'Think "crust + aceans" - ocean animals with crusty shells',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The marine biologist studied various _____ to understand their molting patterns and behavior.'
    },
    'crusts': {
        'definition': 'Plural of crust; multiple hard outer layers or surfaces. In baking, crusts refer to the outer portions of bread, pie, or pizza. Geological crusts describe the outermost solid layers of planetary bodies. When wounds heal, they often form protective crusts. Bread crusts can vary in thickness and texture depending on baking methods and ingredients.',
        'part_of_speech': 'noun (plural), verb (third person singular)',
        'pronunciation_guide': 'KRUHSTS (/krʌsts/)',
        'etymology': 'Plural of "crust," from Latin "crusta" (rind, shell)',
        'memory_tips': 'Think of multiple bread loaves with their hard outer crusts',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The children removed the _____ from their sandwiches, preferring only the soft interior bread.'
    },
    'crux': {
        'definition': 'The decisive or most important point of an issue; the central feature or essence of a matter. In climbing, a crux is the most difficult section of a route. The crux of an argument is its fundamental core that determines validity. Legal cases often hinge on identifying the crux of the dispute. Understanding the crux helps focus attention on what truly matters rather than peripheral details.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRUHKS (/krʌks/)',
        'etymology': 'Latin "crux" (cross), referring to a crucial intersection or decision point',
        'memory_tips': 'Think of standing at a crossroads - the crux is the critical decision point',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ of the matter was whether the company had properly disclosed all financial risks to investors.'
    },
    'cryogenic': {
        'definition': 'Relating to the production and effects of very low temperatures, typically below -150°C (-238°F). Cryogenic technology involves storing materials at extremely cold temperatures to preserve them or achieve specific properties. Liquid nitrogen and liquid helium are common cryogenic fluids. Medical applications include cryosurgery and preservation of biological samples. Space exploration relies on cryogenic fuels for rocket propulsion.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'krahy-uh-JEN-ik (/ˌkraɪəˈdʒɛnɪk/)',
        'etymology': 'From Greek "kryos" (frost, cold) + "genes" (born, produced)',
        'memory_tips': 'Think "cry + genic" - so cold it makes you cry, generated by extreme cold',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The laboratory used _____ storage tanks to preserve biological samples at ultra-low temperatures.'
    },
    'cryptozoa': {
        'definition': 'Small animals that live hidden in concealed habitats such as under rocks, logs, bark, or in soil and leaf litter. This ecological group includes various invertebrates like millipedes, centipedes, isopods, beetles, and spiders that prefer dark, moist environments. Cryptozoa play important roles in decomposition and nutrient cycling in ecosystems. Their hidden lifestyle protects them from predators and environmental extremes. Many cryptozoans are sensitive indicators of environmental health.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'krip-tuh-ZOH-uh (/ˌkrɪptəˈzoʊə/)',
        'etymology': 'From Greek "kryptos" (hidden) + "zoa" (animals)',
        'memory_tips': 'Think "crypto (hidden) + zoa (animals)" - secretly hidden animals',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The researcher carefully lifted logs and stones to study the diverse _____ living in the forest floor.'
    },
    'crystalline': {
        'definition': 'Having the structure or form of crystals; extremely clear and transparent like crystal; relating to the organized, geometric arrangement of atoms in solid materials. Crystalline structures exhibit regular, repeating patterns that determine physical properties. Many minerals display crystalline forms with distinct facets and angles. Crystalline materials often have unique optical, electrical, and mechanical properties due to their ordered atomic structure.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KRIS-tuh-lahyn (/ˈkrɪstəˌlaɪn/)',
        'etymology': 'From Latin "crystallum" (crystal) + suffix "-ine" (having the nature of)',
        'memory_tips': 'Think "crystal + line" - arranged in crystal-like lines and patterns',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The geologist examined the _____ structure of the mineral sample under a powerful microscope.'
    },
    'crystallized': {
        'definition': 'Past tense of crystallize; formed into crystals; made clear and definite; preserved in sugar syrup. When solutions cool or evaporate, dissolved substances can crystallize into solid forms. Ideas crystallize when they become clear and well-defined. Crystallized fruits are preserved by coating them in concentrated sugar solutions. The process involves organized arrangement of molecules into regular patterns.',
        'part_of_speech': 'verb (past tense), adjective',
        'pronunciation_guide': 'KRIS-tuh-lahyzd (/ˈkrɪstəˌlaɪzd/)',
        'etymology': 'From "crystallize," derived from Latin "crystallum" (crystal)',
        'memory_tips': 'Think of sugar crystallizing into hard, clear chunks',
        'alternate_spellings': 'Crystallised (British)',
        'language_origin': 'Latin',
        'example_sentence': 'Her thoughts about the project _____ after the lengthy brainstorming session with her team.'
    },
    'crystals': {
        'definition': 'Plural of crystal; solid materials with atoms arranged in highly ordered, repeating patterns; clear, transparent pieces of quartz or glass; regular geometric forms with flat faces and sharp edges. Natural crystals form through geological processes over thousands of years. Different crystal systems produce various shapes including cubic, hexagonal, and octahedral forms. Many crystals have optical properties useful in technology and jewelry.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KRIS-tuhlz (/ˈkrɪstəlz/)',
        'etymology': 'Plural of "crystal," from Latin "crystallum," from Greek "krystallos" (ice, crystal)',
        'memory_tips': 'Think of sparkling gems with geometric faces reflecting light',
        'alternate_spellings': 'None',
        'language_origin': 'Latin/Greek',
        'example_sentence': 'The cave was filled with magnificent _____ that had formed over millions of years.'
    },
    'cubic': {
        'definition': 'Having the shape of a cube; relating to measurement in three dimensions with length, width, and height; involving the third power in mathematics. Cubic units measure volume, such as cubic feet or cubic meters. In crystallography, the cubic system is one of seven crystal systems characterized by three equal axes at right angles. Cubic equations involve variables raised to the third power.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KYOO-bik (/ˈkyubɪk/)',
        'etymology': 'From Latin "cubus," from Greek "kybos" (cube, die)',
        'memory_tips': 'Think of a cube - equal sides meeting at right angles in three dimensions',
        'alternate_spellings': 'None',
        'language_origin': 'Latin/Greek',
        'example_sentence': 'The room measured 200 _____ feet, making it quite spacious for the family gathering.'
    },
    'cubicle': {
        'definition': 'A small, partitioned workspace in an office; a small enclosed space or compartment. Cubicles became popular in open office designs to provide some privacy while maintaining efficient use of space. They typically feature low walls that allow supervision while reducing noise and distractions. Modern workplace design often debates the benefits and drawbacks of cubicle environments versus open offices.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KYOO-bi-kuhl (/ˈkyubɪkəl/)',
        'etymology': 'From Latin "cubiculum" (bedroom, sleeping chamber)',
        'memory_tips': 'Think "cube + icle" - a small cube-shaped workspace',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She decorated her office _____ with family photos and plants to make it feel more personal.'
    },
    'cubism': {
        'definition': 'An early 20th-century art movement characterized by the representation of subjects from multiple viewpoints using geometric shapes and fragmented forms. Developed by Pablo Picasso and Georges Braque, cubism revolutionized artistic representation by breaking away from traditional perspective. The movement emphasized the two-dimensional nature of the canvas while depicting three-dimensional subjects. Cubist works often appear abstract and angular, challenging viewers to interpret familiar subjects in new ways.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KYOO-bizm (/ˈkyuˌbɪzəm/)',
        'etymology': 'From "cube" + suffix "-ism," referring to the geometric cubic forms used',
        'memory_tips': 'Think "cube + ism" - art style using cube-like geometric shapes',
        'alternate_spellings': 'None',
        'language_origin': 'English (from Latin root)',
        'example_sentence': 'The museum\'s _____ collection featured groundbreaking works by Picasso and Braque.'
    },
    'cuckoo': {
        'definition': 'A bird known for its distinctive call and parasitic breeding behavior of laying eggs in other birds\' nests; the sound made by this bird; crazy or silly (informal). Cuckoo clocks imitate the bird\'s characteristic call to mark time. Many cuckoo species migrate long distances between breeding and wintering grounds. The bird\'s name is onomatopoetic, derived from its call.',
        'part_of_speech': 'noun, adjective, exclamation',
        'pronunciation_guide': 'KOO-koo (/ˈkukuː/)',
        'etymology': 'Imitative of the bird\'s call, from Old French "cucu"',
        'memory_tips': 'Think of the sound "coo-coo" that the bird makes',
        'alternate_spellings': 'None',
        'language_origin': 'Imitative/Old French',
        'example_sentence': 'The _____ clock chimed midnight with its characteristic two-note call.'
    },
    'cucumber': {
        'definition': 'A long, green vegetable with watery flesh and mild flavor, technically a fruit botanically. Cucumbers belong to the gourd family and are composed of about 95% water, making them refreshing and hydrating. They\'re commonly used in salads, pickles, and skincare treatments. The phrase "cool as a cucumber" refers to staying calm under pressure, relating to the vegetable\'s cooling properties.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KYOO-kuhm-ber (/ˈkyukʌmbər/)',
        'etymology': 'From Latin "cucumis," possibly related to Greek "kikuon"',
        'memory_tips': 'Think of its cool, refreshing taste and green color',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She sliced the fresh _____ to add a crisp texture to the summer salad.'
    },
    'cudgel': {
        'definition': 'A short, thick stick used as a weapon; to beat with such a stick; to think hard about a problem. Cudgels were common weapons in medieval times and remain symbols of primitive but effective force. The phrase "take up the cudgels" means to defend someone or something vigorously. In intellectual contexts, "cudgel one\'s brains" means to think intensively about a difficult problem.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KUHJ-uhl (/ˈkʌdʒəl/)',
        'etymology': 'From Old English "cycgel," related to Middle Low German "kuggel"',
        'memory_tips': 'Think "cuddle + gel" but it\'s actually a hard stick for fighting',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'The village constable carried a wooden _____ as his primary means of maintaining order.'
    },
    'cuirass': {
        'definition': 'A piece of armor consisting of breastplate and backplate fastened together, protecting the torso. Cuirasses were essential components of medieval and Renaissance armor, typically made of metal plates shaped to fit the body. Modern usage extends to protective gear for police and military personnel. The design evolved from simple leather protection to sophisticated articulated metal armor.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kwi-RAS (/kwɪˈræs/)',
        'etymology': 'French, from "cuir" (leather), originally referring to leather armor',
        'memory_tips': 'Think "queer + ass" - strange protection for your torso',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The knight\'s polished _____ gleamed in the sunlight as he prepared for the tournament.'
    },
    'culinary': {
        'definition': 'Relating to cooking or the kitchen; connected with the preparation and presentation of food. Culinary arts encompass professional cooking, food preparation techniques, and kitchen management. Culinary traditions vary widely across cultures, reflecting local ingredients and historical influences. Professional culinary education combines technical skills with creativity and business knowledge.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KYOO-luh-ner-ee (/ˈkyuləˌnɛri/)',
        'etymology': 'From Latin "culina" (kitchen)',
        'memory_tips': 'Think "cool + nary" - cool cooking skills that are extraordinary',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Her _____ skills impressed the guests with creative combinations of flavors and beautiful presentation.'
    },
    'culminate': {
        'definition': 'To reach the highest point or final stage; to end or result in a particular outcome. Events culminate when they reach their peak intensity or importance. Academic programs culminate in graduation ceremonies. Athletic seasons culminate in championship competitions. The term suggests a natural progression toward a climactic moment.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'KUHL-muh-nayt (/ˈkʌlməˌneɪt/)',
        'etymology': 'From Latin "culminatus," from "culmen" (summit, top)',
        'memory_tips': 'Think "climb + inate" - climbing to the highest point',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Years of training will _____ in her performance at the Olympic Games next summer.'
    },
    'culpa': {
        'definition': 'A Latin term meaning fault, blame, or guilt, used in legal contexts. "Mea culpa" means "my fault" or "I am to blame." In legal terminology, culpa refers to negligence or fault that results in liability. The concept distinguishes between intentional wrongdoing and negligent behavior. Understanding culpa is important in determining legal responsibility and damages.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUHL-pah (/ˈkʌlpə/)',
        'etymology': 'Latin "culpa" (fault, blame)',
        'memory_tips': 'Think "gulp + a" - you gulp when admitting fault',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The defendant\'s attorney argued there was no _____ on their client\'s part for the accident.'
    },
    'cultivated': {
        'definition': 'Past tense of cultivate; grown or developed through care and effort; refined or educated through training. Cultivated land has been prepared and maintained for growing crops. Cultivated people have developed refined tastes and sophisticated knowledge through education and experience. The term applies to both agricultural and intellectual development.',
        'part_of_speech': 'verb (past tense), adjective',
        'pronunciation_guide': 'KUHL-tuh-vay-tid (/ˈkʌltəˌveɪtɪd/)',
        'etymology': 'From Latin "cultivatus," from "colere" (to tend, cultivate)',
        'memory_tips': 'Think "cult + ivated" - devoted to growing or developing something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She _____ a beautiful garden with rare orchids and exotic plants from around the world.'
    },
    'cultural': {
        'definition': 'Relating to culture, especially the arts, customs, beliefs, and social behaviors of particular societies. Cultural differences shape how people communicate, celebrate, and organize their lives. Cultural heritage includes traditions passed down through generations. Understanding cultural context is essential for effective communication across diverse groups.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KUHL-cher-uhl (/ˈkʌltʃərəl/)',
        'etymology': 'From "culture," from Latin "cultura" (cultivation)',
        'memory_tips': 'Think "culture + al" - relating to the culture of a group',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The museum\'s _____ exchange program brought traditional artists from five different countries.'
    },
    'cultures': {
        'definition': 'Plural of culture; the customs, arts, social institutions, and achievements of particular societies; growths of bacteria or cells in laboratory conditions. Different cultures have unique languages, religions, and social practices. In science, cultures refer to controlled environments for growing microorganisms. Cultural diversity enriches human experience through varied perspectives and traditions.',
        'part_of_speech': 'noun (plural), verb (third person singular)',
        'pronunciation_guide': 'KUHL-cherz (/ˈkʌltʃərz/)',
        'etymology': 'Plural of "culture," from Latin "cultura" (cultivation)',
        'memory_tips': 'Think of different societies with their unique ways of life',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The anthropologist studied indigenous _____ to understand their traditional ecological knowledge.'
    },
    'cumbersome': {
        'definition': 'Large, heavy, and difficult to carry or manage; slow and complicated in operation or method. Cumbersome objects require significant effort to move or manipulate. Bureaucratic processes can be cumbersome, involving excessive paperwork and delays. The term suggests inefficiency due to size, weight, or complexity.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KUHM-ber-suhm (/ˈkʌmbərsəm/)',
        'etymology': 'From "cumber" (to burden) + suffix "-some"',
        'memory_tips': 'Think "lumber + some" - like heavy lumber that\'s difficult to carry',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The old computer system was _____ and frequently crashed during important presentations.'
    },
    'cumulus': {
        'definition': 'A type of cloud with a flat base and puffy, rounded top, often resembling cotton balls; in general, a heaped or accumulated mass. Cumulus clouds typically indicate fair weather but can develop into towering cumulonimbus clouds that produce thunderstorms. They form through convection when warm air rises and cools. The term also applies to any accumulated pile or mass.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KYOO-myuh-luhs (/ˈkyuməˌləs/)',
        'etymology': 'Latin "cumulus" (heap, pile)',
        'memory_tips': 'Think "come + you + lus" - fluffy clouds that come to you',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ clouds drifted lazily across the bright blue summer sky.'
    },
    'cupola': {
        'definition': 'A small, dome-shaped structure on top of a building, often used for observation or decoration; a rounded vault forming a roof. Cupolas traditionally provide light and ventilation to the spaces below. Many government buildings, churches, and barns feature distinctive cupolas. They serve both functional and aesthetic purposes in architecture.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KYOO-puh-luh (/ˈkyupələ/)',
        'etymology': 'Italian "cupola," from Latin "cupula" (small cup)',
        'memory_tips': 'Think "cup + ola" - a cup-shaped dome on top of buildings',
        'alternate_spellings': 'None',
        'language_origin': 'Italian/Latin',
        'example_sentence': 'The historic courthouse featured an elegant _____ topped with a weathervane.'
    },
    'cups': {
        'definition': 'Plural of cup; small, round containers typically used for drinking; units of measurement in cooking; trophy prizes in sports competitions. Cups come in various materials including ceramic, glass, plastic, and metal. In cooking, a cup equals 8 fluid ounces or 240 milliliters. Sports cups symbolize championship victories and excellence.',
        'part_of_speech': 'noun (plural), verb (third person singular)',
        'pronunciation_guide': 'KUHPS (/kʌps/)',
        'etymology': 'Plural of "cup," from Old English "cuppe," from Latin "cuppa"',
        'memory_tips': 'Think of drinking vessels arranged on a table',
        'alternate_spellings': 'None',
        'language_origin': 'Old English/Latin',
        'example_sentence': 'She arranged the delicate china _____ and saucers for the afternoon tea service.'
    },
    'curator': {
        'definition': 'A person responsible for selecting, organizing, and managing collections in museums, galleries, or exhibitions; someone who carefully selects and presents content. Curators possess specialized knowledge about their collections and create educational experiences for visitors. Digital curators manage online content and databases. The role combines scholarship with public education.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kyoor-AY-ter (/kyʊˈreɪtər/)',
        'etymology': 'Latin "curator" (caretaker), from "curare" (to take care of)',
        'memory_tips': 'Think "cure + ator" - one who cares for and heals collections',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The museum _____ spent years researching the artifacts before creating the new exhibition.'
    },
    'curfew': {
        'definition': 'A regulation requiring people to remain indoors during specified hours, typically at night; the time when such restrictions begin. Curfews are imposed for public safety during emergencies, civil unrest, or wartime. Parents often set curfews for their children. The original curfew was a medieval fire safety measure requiring fires to be extinguished at a certain time.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KER-fyoo (/ˈkɜrfyu/)',
        'etymology': 'From Old French "cuevrefeu" (cover fire), a signal to extinguish fires',
        'memory_tips': 'Think "cur + few" - time when only a few people should be out',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The city implemented an emergency _____ requiring all residents to be indoors by 10 PM.'
    },
    'curie': {
        'definition': 'A unit of radioactivity equal to 37 billion disintegrations per second, named after Marie and Pierre Curie; relating to the Curie family of scientists. The curie measures the activity of radioactive materials, though it has largely been replaced by the becquerel in scientific use. Marie Curie was the first woman to win a Nobel Prize and the only person to win Nobel Prizes in two different sciences.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KYOOR-ee (/ˈkyʊri/)',
        'etymology': 'Named after Marie and Pierre Curie, pioneering radioactivity researchers',
        'memory_tips': 'Think of Marie Curie\'s groundbreaking work with radioactive elements',
        'alternate_spellings': 'None',
        'language_origin': 'Named after scientists',
        'example_sentence': 'The radioactive sample measured 2.5 _____ on the laboratory\'s detection equipment.'
    },
    'curiecurmudgeon': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "curie" (unit of radioactivity named after Marie Curie) + "curmudgeon" (a bad-tempered, difficult person). These should be separate words with completely different meanings.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "curie" and "curmudgeon"',
        'alternate_spellings': 'curie + curmudgeon (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'curio': {
        'definition': 'A rare, unusual, or intriguing object; something considered interesting because of its rarity or uniqueness. Curios are often collected for their novelty value or cultural significance. Antique shops frequently feature curios from different time periods and cultures. The term suggests something that arouses curiosity due to its distinctive or mysterious nature.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KYOOR-ee-oh (/ˈkyʊrioʊ/)',
        'etymology': 'Short for "curiosity," from Latin "curiosus" (careful, inquisitive)',
        'memory_tips': 'Think "curious + io" - an object that makes you curious',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The old sailor\'s cabin was filled with nautical _____ collected during his travels.'
    },
    'curiosity': {
        'definition': 'A strong desire to know or learn something; an unusual or interesting object or fact. Curiosity drives scientific discovery and learning throughout life. The phrase "curiosity killed the cat" warns against excessive inquisitiveness, though it\'s often completed with "but satisfaction brought it back." Healthy curiosity promotes intellectual growth and understanding.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kyoor-ee-OS-i-tee (/ˌkyʊriˈɒsɪti/)',
        'etymology': 'From Latin "curiositas," from "curiosus" (careful, inquisitive)',
        'memory_tips': 'Think of being curious about everything around you',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The child\'s natural _____ led her to ask endless questions about how things work.'
    },
    'curly': {
        'definition': 'Having curves, spirals, or ringlets; twisted or coiled in shape. Curly hair has a natural tendency to form spirals or waves. Curly brackets in writing are { }. The term describes anything with a curved, twisted, or spiral form. Different degrees of curliness create various textures and patterns.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KER-lee (/ˈkɜrli/)',
        'etymology': 'From "curl," from Middle English "crulle"',
        'memory_tips': 'Think of hair that curls naturally into spirals',
        'alternate_spellings': 'None',
        'language_origin': 'Middle English',
        'example_sentence': 'Her _____ hair bounced with each step as she walked down the hallway.'
    },
    'curmudgeon': {
        'definition': 'A bad-tempered, difficult, cantankerous person; someone who is often angry and annoyed. Curmudgeons typically complain frequently and resist change or new ideas. The term often applies to older people who seem perpetually grumpy. Despite negative connotations, some curmudgeons are valued for their honest, direct communication style.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'ker-MUHJ-uhn (/kərˈmʌdʒən/)',
        'etymology': 'Origin uncertain, possibly from French "coeur méchant" (evil heart)',
        'memory_tips': 'Think "cur + mudge + on" - a cranky person who mudges (grumbles) on and on',
        'alternate_spellings': 'None',
        'language_origin': 'Uncertain (possibly French)',
        'example_sentence': 'The neighborhood _____ complained loudly about children playing in his yard.'
    },
    'curries': {
        'definition': 'Plural of curry; spiced dishes with sauce, typically from South Asian cuisine; third person singular of "curry" (to groom a horse with a curry comb). Curries feature complex spice blends and can include vegetables, meat, or legumes. Regional variations create distinct flavor profiles. The cooking technique involves building layers of flavor through careful spice preparation.',
        'part_of_speech': 'noun (plural), verb (third person singular)',
        'pronunciation_guide': 'KER-eez (/ˈkɛriz/)',
        'etymology': 'From Tamil "kari" (sauce, relish)',
        'memory_tips': 'Think of various spiced dishes from Indian cuisine',
        'alternate_spellings': 'None',
        'language_origin': 'Tamil',
        'example_sentence': 'The restaurant menu featured twelve different _____ ranging from mild to extremely spicy.'
    },
    'currycomb': {
        'definition': 'A grooming tool with metal ridges or rubber teeth used to clean and massage horses\' coats; to groom a horse with such a tool. Currycombs remove dirt, loose hair, and debris while stimulating circulation in the horse\'s skin. Regular currying keeps horses\' coats healthy and shiny. The tool is typically used in circular motions during grooming routines.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KER-ee-kohm (/ˈkɛriˌkoʊm/)',
        'etymology': 'From "curry" (to groom) + "comb"',
        'memory_tips': 'Think "curry + comb" - a special comb for grooming horses',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'She used the _____ to remove mud and loose hair from her horse\'s winter coat.'
    },
    'cursive': {
        'definition': 'A style of handwriting where letters are joined together in a flowing manner; running or flowing. Cursive writing was traditionally taught in schools to improve writing speed and elegance. The connected letters create a continuous flow across the page. Modern education debates whether cursive instruction remains necessary in the digital age.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'KER-siv (/ˈkɜrsɪv/)',
        'etymology': 'From Latin "cursivus" (running), from "currere" (to run)',
        'memory_tips': 'Think "curse + ive" - letters that seem to run together in a flowing curse',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The teacher demonstrated proper _____ letter formation on the blackboard.'
    },
    'curtail': {
        'definition': 'To reduce in extent or quantity; to impose a restriction on something; to cut short or truncate. Economic downturns often force companies to curtail expansion plans. Governments may curtail civil liberties during emergencies. The term suggests deliberate limitation rather than gradual reduction.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'ker-TAYL (/kərˈteɪl/)',
        'etymology': 'From "curtail" (to cut the tail), from Old French "courtault" (short)',
        'memory_tips': 'Think "cur + tail" - cutting off a dog\'s tail to make it shorter',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The company decided to _____ spending on non-essential projects to improve profitability.'
    },
    'curtains': {
        'definition': 'Plural of curtain; pieces of fabric hung to cover windows, divide spaces, or provide privacy; the end of something (colloquial). Window curtains control light and privacy while adding decoration. Theater curtains mark the beginning and end of performances. "It\'s curtains" means something is finished or doomed.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KER-tuhnz (/ˈkɜrtənz/)',
        'etymology': 'Plural of "curtain," from Old French "courtine"',
        'memory_tips': 'Think of fabric panels hanging over windows',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'She drew the _____ to block the bright morning sunlight from the bedroom.'
    },
    'curtly': {
        'definition': 'In a brief, blunt, or abrupt manner; rudely concise; with discourteous brevity. Curtly spoken words are often perceived as unfriendly or dismissive. The adverb suggests efficient communication that lacks warmth or politeness. Speaking curtly can indicate impatience, anger, or social distance.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'KERT-lee (/ˈkɜrtli/)',
        'etymology': 'From "curt" + suffix "-ly," from Latin "curtus" (short)',
        'memory_tips': 'Think "curt + ly" - speaking in a curt, brief manner',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'He replied _____ to her question, clearly annoyed by the interruption.'
    },
    'curve': {
        'definition': 'A smooth, gradually bending line without sharp angles; to bend or turn in a smooth, continuous arc. Curves appear throughout nature in rivers, coastlines, and organic forms. In mathematics, curves are defined by specific equations. Baseball pitchers throw curve balls that change direction mid-flight. Road curves require reduced speed for safety.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KERV (/kɜrv/)',
        'etymology': 'From Latin "curvus" (bent, curved)',
        'memory_tips': 'Think of a smooth, bending line like a snake or river',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The mountain road had a sharp _____ that required drivers to slow down significantly.'
    },
    'cushag': {
        'definition': 'A Manx Gaelic word for a grass or weed, particularly referring to tangled or troublesome vegetation; sometimes used for ragwort or similar plants. This term is specific to the Isle of Man dialect and reflects the island\'s Celtic linguistic heritage. The word appears in regional literature and local botanical discussions.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOOSH-ag (/ˈkuʃæɡ/)',
        'etymology': 'From Manx Gaelic "cushag" (weed, grass)',
        'memory_tips': 'Think "cushion + ag" - soft grass that cushions the ground',
        'alternate_spellings': 'None',
        'language_origin': 'Manx Gaelic',
        'example_sentence': 'The farmer complained about the _____ growing wild in his pasture fields.'
    }
}

def main():
    # Read the input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_045_words.csv'
    df = pd.read_csv(input_file)
    
    print(f"Processing {len(df)} words from batch 045...")
    
    # Initialize difficulty calculator
    calc = DifficultyCalculator()
    
    # Prepare output data
    output_data = []
    
    for index, row in df.iterrows():
        word = row['word']
        
        if word in WORD_DATA:
            # Get difficulty scores
            difficulty_scores = calc.calculate_difficulty_score(word)
            
            # Create output row
            output_row = {
                'word': word,
                'definition': WORD_DATA[word]['definition'],
                'part_of_speech': WORD_DATA[word]['part_of_speech'],
                'pronunciation_guide': WORD_DATA[word]['pronunciation_guide'],
                'etymology': WORD_DATA[word]['etymology'],
                'memory_tips': WORD_DATA[word]['memory_tips'],
                'alternate_spellings': WORD_DATA[word]['alternate_spellings'],
                'language_origin': WORD_DATA[word]['language_origin'],
                'example_sentence': WORD_DATA[word]['example_sentence'],
                'years': row['years'],
                'source_files': row['source_files'],
                'source_difficulties': row['source_difficulties'],
                'difficulty_phonetic': difficulty_scores['difficulty_phonetic'],
                'difficulty_frequency': difficulty_scores['difficulty_frequency'],
                'difficulty_morphological': difficulty_scores['difficulty_morphological'],
                'difficulty_etymology': difficulty_scores['difficulty_etymology'],
                'difficulty_final': '',  # Leave empty as requested
                'etymology_source': 'Claude',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude'
            }
            
            output_data.append(output_row)
    
    # Create output DataFrame
    output_df = pd.DataFrame(output_data)
    
    # Save to CSV
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_045_processed.csv'
    output_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Successfully processed {len(output_data)}/{len(df)} words")
    print(f"Output saved to: {output_file}")
    
    # Check for combined word errors
    errors_found = [word for word in df['word'] if word in COMBINED_WORD_ERRORS]
    if errors_found:
        print(f"Found {len(errors_found)} combined word errors:")
        for error in errors_found:
            print(f"   - {error}")
    else:
        print("No combined word errors found in this batch")

if __name__ == "__main__":
    main()