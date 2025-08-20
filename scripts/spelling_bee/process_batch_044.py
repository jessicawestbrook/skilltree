import csv
import pandas as pd

class DifficultyCalculator:
    def calculate_phonetic_transparency(self, word):
        irregular_patterns = ['ough', 'augh', 'eigh', 'tion', 'sion', 'cial', 'tial', 'ph', 'gh', 'kn', 'wr', 'gn', 'mb', 'sc', 'ps']
        silent_letters = ['b', 'c', 'd', 'g', 'h', 'k', 'l', 'n', 'p', 's', 't', 'w']
        
        score = 1.0
        word_lower = word.lower()
        
        for pattern in irregular_patterns:
            if pattern in word_lower:
                score += 0.3
        
        for i, char in enumerate(word_lower):
            if char in silent_letters:
                if (char == 'b' and i > 0 and word_lower[i-1] == 'm') or \
                   (char == 'k' and i < len(word_lower)-1 and word_lower[i+1] == 'n') or \
                   (char == 'w' and i < len(word_lower)-1 and word_lower[i+1] == 'r'):
                    score += 0.2
        
        return min(score, 4.0)
    
    def calculate_frequency_score(self, word):
        common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their']
        
        if word.lower() in common_words:
            return 1.0
        elif len(word) <= 4:
            return 1.5
        elif len(word) <= 6:
            return 2.0
        elif len(word) <= 8:
            return 2.5
        elif len(word) <= 10:
            return 3.0
        else:
            return 3.5
    
    def calculate_morphological_complexity(self, word):
        prefixes = ['un', 're', 'in', 'dis', 'en', 'non', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'under']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'ious', 'al', 'ial', 'ic', 'ive', 'ary', 'ory']
        
        score = 1.0
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                score += 0.5
                break
        
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                score += 0.5
                break
        
        if len(word) > 10:
            score += 0.5
        if len(word) > 15:
            score += 0.5
        
        return min(score, 4.0)
    
    def calculate_etymology_complexity(self, etymology_info):
        if not etymology_info or etymology_info.lower() in ['unknown', 'english']:
            return 1.0
        
        complex_origins = ['greek', 'latin', 'sanskrit', 'arabic', 'hebrew', 'chinese', 'japanese']
        moderate_origins = ['french', 'german', 'spanish', 'italian', 'dutch', 'portuguese']
        
        etymology_lower = etymology_info.lower()
        
        for origin in complex_origins:
            if origin in etymology_lower:
                return 3.5
        
        for origin in moderate_origins:
            if origin in etymology_lower:
                return 2.5
        
        return 2.0

def calculate_difficulty_scores(word, etymology):
    calculator = DifficultyCalculator()
    
    phonetic = calculator.calculate_phonetic_transparency(word)
    frequency = calculator.calculate_frequency_score(word)
    morphological = calculator.calculate_morphological_complexity(word)
    etymology_score = calculator.calculate_etymology_complexity(etymology)
    
    return phonetic, frequency, morphological, etymology_score

batch_044_data = {
    'crannies': {
        'definition': 'Plural of cranny; small, narrow openings or crevices, especially in walls or rocks; hidden or secluded places. The phrase "nooks and crannies" describes small, often overlooked spaces that can hide objects or provide secret areas. These tiny gaps or recesses often accumulate dust, debris, or small items.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KRAN-eez (/ˈkræniːz/)',
        'etymology': 'Plural of "cranny," from Old French "cren" (notch)',
        'memory_tips': 'Think "cracks + nannies" - tiny cracks where small things hide like children hiding from nannies',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'She searched every nook and _____ of the attic for the missing jewelry box.'
    },
    'crate': {
        'definition': 'A large wooden, plastic, or metal container used for transporting or storing goods; to pack items into such a container. Crates provide sturdy protection for shipping fragile or heavy items. They often have slatted sides for ventilation and can be stacked for efficient storage.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KRAYT (/kreɪt/)',
        'etymology': 'From Latin "cratis" (wickerwork, hurdle)',
        'memory_tips': 'Think "create + ate" - you create storage by putting things in a crate',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The movers loaded the fragile dishes into a wooden _____ for protection.'
    },
    'crawl': {
        'definition': 'To move slowly on hands and knees or with the body close to the ground; to move very slowly; a swimming stroke performed face-down with alternating arm movements. Crawling is typically the first form of independent locomotion in human infants.',
        'part_of_speech': 'verb, noun',
        'pronunciation_guide': 'KRAWL (/krɔːl/)',
        'etymology': 'From Old Norse "krafla" (to claw)',
        'memory_tips': 'Think of using claws or hands to slowly move across the ground',
        'alternate_spellings': 'None',
        'language_origin': 'Old Norse',
        'example_sentence': 'The baby learned to _____ before taking his first steps.'
    },
    'crayfish': {
        'definition': 'A freshwater crustacean resembling a small lobster, also called crawfish or crawdads in different regions. These arthropods have a segmented body, ten legs, and large claws. They inhabit streams, rivers, and ponds, serving as both predators and prey in aquatic ecosystems.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRAY-fish (/ˈkreɪˌfɪʃ/)',
        'etymology': 'From Middle English "crevis" + "fish" (though not actually a fish)',
        'memory_tips': 'Think "cray (like crab) + fish" - a crab-like creature in fresh water',
        'alternate_spellings': 'Crawfish, Crawdad',
        'language_origin': 'Middle English',
        'example_sentence': 'The children caught _____ in the shallow creek using small nets.'
    },
    'crayon': {
        'definition': 'A stick of colored wax, charcoal, or chalk used for drawing or coloring; to color or draw with such a stick. Crayons are popular art supplies for children and artists, available in numerous colors and formulations. They provide an easy, non-messy way to add color to artwork.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KRAY-on (/ˈkreɪˌɒn/) or KRAY-ahn (/ˈkreɪɑːn/)',
        'etymology': 'French, from "craie" (chalk), from Latin "creta" (chalk)',
        'memory_tips': 'Think "cray (like gray) + on" - colored sticks that go on paper',
        'alternate_spellings': 'None',
        'language_origin': 'French/Latin',
        'example_sentence': 'The child carefully selected a red _____ to color the fire truck.'
    },
    'creak': {
        'definition': 'A sharp, high-pitched sound made by something moving or under pressure, typically old wood or metal; to make such a sound. Creaking often indicates age, wear, or stress in materials. The sound serves as an auditory warning of potential structural issues.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KREEK (/kriːk/)',
        'etymology': 'Imitative of the sound, related to "crack"',
        'memory_tips': 'Think of old stairs that "creek" (like a creek flows) when you step on them',
        'alternate_spellings': 'None',
        'language_origin': 'Imitative/English',
        'example_sentence': 'The old wooden floor began to _____ under the weight of the heavy furniture.'
    },
    'cream': {
        'definition': 'The thick, fatty layer that rises to the top of milk; a cosmetic or medicinal preparation with a smooth, thick consistency; the best part of something; a pale yellowish-white color. Cream represents richness, quality, and luxury in various contexts.',
        'part_of_speech': 'noun, verb, adjective',
        'pronunciation_guide': 'KREEM (/kriːm/)',
        'etymology': 'From Old French "cresme," from Latin "chrisma" (ointment)',
        'memory_tips': 'Think of the rich, smooth layer on top of milk - the best part',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'She whipped the heavy _____ until it formed soft peaks for the dessert.'
    },
    'creances': {
        'definition': 'In falconry, long lines or tethers attached to hawks or falcons during training to prevent them from flying away while learning to hunt. Creances allow birds of prey to practice flying and hunting while remaining under the falconer\'s control. This training method ensures the bird\'s safety during the learning process.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kree-AHN-siz (/kriˈɑnsɪz/)',
        'etymology': 'French, meaning "beliefs" or "trust," from falconry context of trusting the bird',
        'memory_tips': 'Think "cre (create) + ances" - creating trust/control with training lines',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The falconer attached _____ to the young hawk before its first hunting lesson.'
    },
    'crease': {
        'definition': 'A line or ridge made by folding, pressing, or crushing something; to make such a line; in cricket, the line marking the batsman\'s position. Creases can be intentional (pants crease) or accidental (wrinkles). They alter the appearance and sometimes functionality of materials.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KREES (/kriːs/)',
        'etymology': 'Possibly from Middle English "crest" or related to "crisp"',
        'memory_tips': 'Think of pressing clothes to create sharp lines - "crees" or creases',
        'alternate_spellings': 'None',
        'language_origin': 'Middle English',
        'example_sentence': 'He carefully ironed a sharp _____ down the front of his dress pants.'
    },
    'create': {
        'definition': 'To bring something into existence; to produce or design something new; to cause or bring about a situation or condition. Creation involves imagination, skill, and effort to produce original works, solutions, or experiences. It represents fundamental human creativity and innovation.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kree-AYT (/kriˈeɪt/)',
        'etymology': 'From Latin "creare" (to make, produce)',
        'memory_tips': 'Think "cre + ate" - you ate (consumed) inspiration to create something new',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The artist spent months working to _____ her masterpiece sculpture.'
    },
    'created': {
        'definition': 'Past tense of create; brought into existence or produced something new; made or designed something original. This term indicates completed acts of creation, whether artistic, intellectual, physical, or conceptual. Created implies successful completion of the creative process.',
        'part_of_speech': 'verb (past tense)',
        'pronunciation_guide': 'kree-AY-ted (/kriˈeɪtəd/)',
        'etymology': 'From Latin "creare" (to make) + past tense suffix "-ed"',
        'memory_tips': 'Think "create + -ed" - something that was successfully created in the past',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The software developer _____ an innovative app that solved scheduling problems.'
    },
    'creating': {
        'definition': 'Present participle of create; in the process of bringing something into existence; producing or designing something new. This ongoing action involves active imagination, effort, and skill application. Creating represents dynamic, purposeful activity toward producing original works.',
        'part_of_speech': 'verb (present participle)',
        'pronunciation_guide': 'kree-AY-ting (/kriˈeɪtɪŋ/)',
        'etymology': 'From Latin "creare" + present participle suffix "-ing"',
        'memory_tips': 'Think "create + -ing" - actively in the process of creating something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The team is _____ a new marketing strategy for the product launch.'
    },
    'credence': {
        'definition': 'Belief in or acceptance of something as true; the quality of being trusted and believed in. Credence involves giving mental assent to claims, statements, or ideas based on evidence, authority, or personal judgment. It represents the foundation of trust and acceptance.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KREE-duhns (/ˈkriːdəns/)',
        'etymology': 'From Latin "credentia," from "credere" (to believe)',
        'memory_tips': 'Think "cred (believe) + ence" - the state of believing or trusting',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The witness\'s consistent story lent _____ to her testimony.'
    },
    'credit': {
        'definition': 'Recognition or acknowledgment of merit; a system allowing deferred payment; to attribute something to someone; trust in someone\'s ability to pay. Credit encompasses financial trust, academic recognition, and attribution of achievement or responsibility.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KRED-it (/ˈkrɛdɪt/)',
        'etymology': 'From Latin "creditum," from "credere" (to believe, trust)',
        'memory_tips': 'Think "cred (believe) + it" - believing someone will pay it back',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She received full _____ for developing the innovative teaching method.'
    },
    'credulity': {
        'definition': 'A tendency to be too ready to believe things; gullibility or excessive willingness to accept claims without sufficient evidence. Credulity represents a cognitive bias toward acceptance rather than skeptical evaluation. It can make individuals vulnerable to deception or misinformation.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kruh-DOO-li-tee (/krəˈduːləti/)',
        'etymology': 'From Latin "credulitas," from "credulus" (too ready to believe)',
        'memory_tips': 'Think "cred (believe) + ulous (full of)" - being too full of belief',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'His _____ made him an easy target for online scams and false claims.'
    },
    'creeks': {
        'definition': 'Plural of creek; small streams or waterways, typically smaller than rivers; narrow inlets or bays. Creeks serve as natural drainage systems, wildlife habitats, and recreational areas. They often connect larger water bodies or provide seasonal water flow.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KREEKS (/kriːks/)',
        'etymology': 'Plural of Middle English "creke," from Old Norse "kriki" (nook)',
        'memory_tips': 'Think of small streams that "creak" quietly as water flows over rocks',
        'alternate_spellings': 'None',
        'language_origin': 'Old Norse',
        'example_sentence': 'The hiking trail crossed several shallow _____ on its way to the summit.'
    },
    'creel': {
        'definition': 'A wicker basket used by anglers to hold caught fish; a framework or structure used in fishing or textile production. Creels keep fish fresh and alive during fishing expeditions. In textile manufacturing, creels hold yarn or thread for weaving processes.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KREEL (/kriːl/)',
        'etymology': 'From Middle English "crele," from Old French "creil" (gridiron)',
        'memory_tips': 'Think "creek + eel" - a basket for holding fish like eels from creeks',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The fly fisherman carried his daily catch in a traditional wicker _____.'
    },
    'creelboniface': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "creel" (fishing basket) + "boniface" (innkeeper or jolly host). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "creel" and "boniface"',
        'alternate_spellings': 'creel + boniface (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'creosote': {
        'definition': 'A dark, oily liquid obtained from coal tar or wood tar, used as a wood preservative and disinfectant; a shrub native to desert regions of southwestern North America. Industrial creosote protects railway ties and telephone poles from decay, while creosote plants are adapted to arid environments.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KREE-uh-soht (/ˈkriəˌsoʊt/)',
        'etymology': 'From Greek "kreas" (flesh) + "soter" (preserver)',
        'memory_tips': 'Think "cre (create) + osote" - creates protection by preserving wood',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The railroad treated wooden ties with _____ to prevent rot and insect damage.'
    },
    'crepuscular': {
        'definition': 'Active during twilight hours (dawn and dusk); relating to or resembling twilight. Many animals are crepuscular, becoming active when light levels are low but not completely dark. This behavior helps them avoid both diurnal and nocturnal predators while taking advantage of optimal hunting conditions.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kruh-PUS-kyuh-lur (/krəˈpʌskjələr/)',
        'etymology': 'From Latin "crepusculum" (twilight, dusk)',
        'memory_tips': 'Think "creep + uscular" - animals that creep out during twilight',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Rabbits are _____ animals, most active during dawn and dusk hours.'
    },
    'crescendo': {
        'definition': 'A gradual increase in loudness or intensity, especially in music; the climax or peak of such an increase. Crescendos create dramatic effect by building tension and excitement. The term applies to both musical dynamics and metaphorical increases in any activity or emotion.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'kruh-SHEN-doh (/krəˈʃɛndoʊ/)',
        'etymology': 'Italian, meaning "growing," from Latin "crescere" (to grow)',
        'memory_tips': 'Think "cre (grow) + scendo" - growing or ascending in volume',
        'alternate_spellings': 'None',
        'language_origin': 'Italian/Latin',
        'example_sentence': 'The symphony built to a powerful _____ before ending in sudden silence.'
    },
    'crescive': {
        'definition': 'Growing or increasing gradually; having the quality of growth or development. This formal term describes processes that expand, develop, or intensify over time. Crescive changes occur through natural progression rather than sudden transformation.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KRES-iv (/ˈkrɛsɪv/)',
        'etymology': 'From Latin "crescere" (to grow) + suffix "-ive"',
        'memory_tips': 'Think "cres (grow) + -ive" - having the quality of growing',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ influence of social media changed communication patterns gradually.'
    },
    'cress': {
        'definition': 'Any of various small, peppery-tasting plants of the mustard family, often used in salads or as garnish. Watercress, garden cress, and winter cress are common varieties. These plants grow quickly and provide sharp, spicy flavors that complement milder ingredients.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRES (/krɛs/)',
        'etymology': 'From Old English "cresse," related to German "Kresse"',
        'memory_tips': 'Think "cres (grow) + s" - fast-growing spicy salad plants',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'The chef garnished the soup with fresh water _____ for added flavor.'
    },
    'cretaceous': {
        'definition': 'Relating to the third and final period of the Mesozoic Era (145-66 million years ago), characterized by chalk deposits and ending with mass extinction. The Cretaceous period saw the dominance of dinosaurs, flowering plants, and warm global climates before the asteroid impact that ended the dinosaur age.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kruh-TAY-shus (/krəˈteɪʃəs/)',
        'etymology': 'From Latin "cretaceus," from "creta" (chalk)',
        'memory_tips': 'Think "creta (chalk) + ceous" - the period that left lots of chalk deposits',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ period ended with the extinction of non-avian dinosaurs.'
    },
    'crevices': {
        'definition': 'Plural of crevice; narrow openings or cracks, especially in rock or ice; small gaps or fissures. Crevices form through natural weathering, geological activity, or structural stress. They provide shelter for small organisms and can present challenges for climbers or explorers.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KREV-uh-siz (/ˈkrɛvəsɪz/)',
        'etymology': 'Plural of Old French "crevace," from "crever" (to break)',
        'memory_tips': 'Think "crev (crack) + ices" - cracks or openings like in ice',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'Small wildflowers grew in the rocky _____ along the mountain trail.'
    },
    'crew': {
        'definition': 'A group of people working together, especially on a ship, aircraft, or film production; the sport of rowing with multiple rowers; to serve as a crew member. Crews collaborate to accomplish complex tasks requiring coordination and specialized skills.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KROO (/kruː/)',
        'etymology': 'From Old French "creue," meaning "increase, reinforcement"',
        'memory_tips': 'Think "grew" - a group that grew together to work as a team',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The film _____ worked sixteen hours to complete the challenging scene.'
    },
    'cribbage': {
        'definition': 'A card game for two to four players, typically played with a special board having holes for keeping score with pegs. Cribbage involves creating combinations of cards that total fifteen or form pairs, runs, and flushes. The game combines strategy with chance and has been popular for centuries.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRIB-ij (/ˈkrɪbɪdʒ/)',
        'etymology': 'From "crib" (the extra hand of cards) + suffix "-age"',
        'memory_tips': 'Think "crib + age" - a game that\'s been around for ages using a crib of cards',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'They played _____ every evening, using the wooden board passed down through generations.'
    },
    'cribble': {
        'definition': 'To sift or screen through a coarse sieve; to perforate with holes; riddled with holes like a sieve. This process separates materials by size or removes impurities. Cribbling creates regular patterns of holes or filters substances through screening.',
        'part_of_speech': 'verb, adjective',
        'pronunciation_guide': 'KRIB-ul (/ˈkrɪbəl/)',
        'etymology': 'From "crib" (sieve) + suffix "-le" (diminutive)',
        'memory_tips': 'Think "crib + ble" - like a crib but with holes for sifting',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The miners used a screen to _____ the ore and separate valuable metals.'
    },
    'cribo': {
        'definition': 'A large, non-venomous snake native to Central and South America, also known as an indigo snake; these powerful constrictors can grow over eight feet long. Cribos are excellent climbers and swimmers, feeding on various prey including other snakes, mammals, and birds.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KREE-boh (/ˈkriboʊ/)',
        'etymology': 'Spanish/Portuguese, possibly from indigenous Central American languages',
        'memory_tips': 'Think "crib + o" - a snake so big it could fill a crib',
        'alternate_spellings': 'None',
        'language_origin': 'Spanish/Portuguese',
        'example_sentence': 'The zoo\'s _____ snake was an impressive eight-foot-long specimen from Costa Rica.'
    },
    'cricket': {
        'definition': 'A small jumping insect known for the chirping sound males make; a bat-and-ball sport played between two teams of eleven players. Cricket insects produce their characteristic sound by rubbing their wings together, while cricket the sport involves complex rules and can last for days.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRIK-it (/ˈkrɪkɪt/)',
        'etymology': 'From Old French "criquet," imitative of the insect\'s sound',
        'memory_tips': 'Think "crick + et" - the sound they make is like a "crick" sound',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The summer evening was filled with the gentle chirping of _____ in the grass.'
    },
    'criminal': {
        'definition': 'A person who has committed a crime; relating to crime or its punishment. Criminal behavior violates laws and social norms, resulting in legal consequences. The criminal justice system addresses both punishment and rehabilitation of offenders.',
        'part_of_speech': 'noun, adjective',
        'pronunciation_guide': 'KRIM-uh-nul (/ˈkrɪmənəl/)',
        'etymology': 'From Latin "criminalis," from "crimen" (crime, accusation)',
        'memory_tips': 'Think "crime + inal" - relating to or involving crime',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The detective worked tirelessly to solve the _____ case.'
    },
    'cringed': {
        'definition': 'Past tense of cringe; drew back or recoiled in fear, embarrassment, or distaste; showed servile deference. Cringing represents both physical recoiling from unpleasant stimuli and emotional responses to awkward or painful situations.',
        'part_of_speech': 'verb (past tense)',
        'pronunciation_guide': 'KRINJD (/krɪndʒd/)',
        'etymology': 'From Old English "cringan" (to yield, fall in battle) + past tense "-ed"',
        'memory_tips': 'Think "crin (like grin) + ged" - opposite of grinning, pulling back in discomfort',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'She _____ when she heard the fingernails scraping across the chalkboard.'
    },
    'crinoline': {
        'definition': 'A stiff fabric made of horsehair and cotton or linen; a hoop skirt or petticoat made with this fabric, worn to extend women\'s skirts in the 19th century. Crinolines created the distinctive bell-shaped silhouette fashionable in Victorian times.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRIN-uh-lin (/ˈkrɪnəlɪn/)',
        'etymology': 'French, from "crin" (horsehair) + "lin" (linen)',
        'memory_tips': 'Think "crin (horsehair) + line" - horsehair fabric that creates lines/shape',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The museum displayed Victorian dresses with elaborate _____ underskirts.'
    },
    'crisp': {
        'definition': 'Firm and brittle; fresh and sharp in quality; clear and decisive; a thin, crispy snack food. Crisp describes textures, weather conditions, communication styles, and food preparations that are clean, sharp, or well-defined.',
        'part_of_speech': 'adjective, noun, verb',
        'pronunciation_guide': 'KRISP (/krɪsp/)',
        'etymology': 'From Old English "crisp," from Latin "crispus" (curled)',
        'memory_tips': 'Think of fresh lettuce or crackers - firm, fresh, and making a snapping sound',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The autumn morning air was _____ and invigorating.'
    },
    'criteria': {
        'definition': 'Plural of criterion; standards or principles by which something is judged, evaluated, or decided. Criteria provide objective measures for assessment, selection, or comparison. They establish consistent frameworks for making decisions or evaluations.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'krahy-TEER-ee-uh (/kraɪˈtɪriə/)',
        'etymology': 'Plural of Greek "kriterion," from "krites" (judge)',
        'memory_tips': 'Think "crit (judge) + eria" - standards used for judging or evaluating',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The scholarship committee established clear _____ for selecting recipients.'
    },
    'crith': {
        'definition': 'A unit of mass used for gases, equal to the mass of one liter of hydrogen gas at standard temperature and pressure (approximately 0.0899 grams). This specialized scientific unit allows precise measurement of gaseous substances in chemistry and physics.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRITH (/krɪθ/)',
        'etymology': 'From Greek "krithos" (barley grain), referring to a small unit of measurement',
        'memory_tips': 'Think "crit (small) + h" - a very small unit for measuring gas mass',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The chemist measured the gas sample in _____ to ensure precise calculations.'
    },
    'critters': {
        'definition': 'Informal term for creatures or animals, especially small or wild ones; living beings, often used affectionately or colloquially. This folksy term encompasses various animals from insects to mammals, typically referring to creatures in natural settings.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KRIT-urz (/ˈkrɪtərz/)',
        'etymology': 'Dialect variation of "creatures"',
        'memory_tips': 'Think "crit (small) + ters" - small creatures or animals',
        'alternate_spellings': 'None',
        'language_origin': 'English dialect',
        'example_sentence': 'The forest was full of various _____ scurrying about in the underbrush.'
    },
    'critturs': {
        'definition': 'Dialectal or archaic spelling of "critters"; creatures or animals, especially as spoken in rural or regional dialects. This variant represents older or regional pronunciation patterns in American English, particularly in rural or frontier contexts.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KRIT-urz (/ˈkrɪtərz/)',
        'etymology': 'Dialectal variation of "creatures"',
        'memory_tips': 'Think "crit + turs" - old-fashioned way of saying creatures',
        'alternate_spellings': 'Critters, Creatures',
        'language_origin': 'English dialect',
        'example_sentence': 'The old farmer spoke of the _____ that lived in the woods behind his property.'
    },
    'crockerygauze': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "crockery" (dishes and pottery) + "gauze" (thin medical fabric). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "crockery" and "gauze"',
        'alternate_spellings': 'crockery + gauze (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'crocodile': {
        'definition': 'A large, predatory reptile with a long snout, powerful jaws, and armored skin, found in tropical waters worldwide. Crocodiles are ancient creatures that have survived virtually unchanged for millions of years. They are apex predators in their aquatic environments.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KROK-uh-dyl (/ˈkrɒkəˌdaɪl/)',
        'etymology': 'From Greek "krokodeilos," meaning "pebble worm"',
        'memory_tips': 'Think "crock + o + dile" - like a crock (pot) but dangerous, in the style of Nile',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The massive _____ basked motionless on the riverbank, waiting for prey.'
    },
    'crokinole': {
        'definition': 'A Canadian dexterity board game similar to carrom, played by flicking wooden discs across a circular board to land in scoring areas while knocking opponents\' pieces off. The game requires skill, strategy, and precise finger control.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KROH-ki-nohl (/ˈkroʊkɪˌnoʊl/)',
        'etymology': 'Possibly from French "croquignole" (flick) or Indigenous Canadian languages',
        'memory_tips': 'Think "crok (like crock) + i + nole" - flicking discs in a crock-shaped board',
        'alternate_spellings': 'None',
        'language_origin': 'Canadian (possibly French)',
        'example_sentence': 'The family gathered around the _____ board for their weekly tournament.'
    },
    'cronies': {
        'definition': 'Close friends or companions, especially those involved in politics or business together; associates who may engage in mutual favoritism or questionable practices. The term often implies relationships based on mutual benefit rather than genuine friendship.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KROH-neez (/ˈkroʊniːz/)',
        'etymology': 'From Greek "chronios" (long-lasting), originally Cambridge slang for old friend',
        'memory_tips': 'Think "chron (time) + ies" - people you\'ve known for a long time',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The mayor was accused of giving city contracts to his political _____.'
    },
    'crookedly': {
        'definition': 'In a crooked manner; not straight or aligned; dishonestly or unfairly. This adverb describes both physical deviation from straightness and metaphorical deviation from honest or proper behavior.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'KROOK-id-lee (/ˈkrʊkɪdli/)',
        'etymology': 'From "crooked" + adverbial suffix "-ly"',
        'memory_tips': 'Think "crooked + -ly" - in a bent, twisted, or dishonest manner',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The picture hung _____ on the wall after the earthquake.'
    },
    'crops': {
        'definition': 'Plural of crop; plants grown for food, fiber, or other economic purposes; the harvest of such plants; to cut or trim short. Crops represent agricultural production essential for human survival and economic activity.',
        'part_of_speech': 'noun (plural), verb',
        'pronunciation_guide': 'KROPS (/krɒps/)',
        'etymology': 'Plural of Old English "crop" (sprout, harvest)',
        'memory_tips': 'Think of plants that are "cropped" or harvested from fields',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'The drought severely affected this year\'s corn and soybean _____.'
    },
    'croquembouche': {
        'definition': 'A French pastry dessert consisting of choux pastry balls (profiteroles) bound together with caramel and often formed into a cone shape. This elaborate dessert is traditionally served at weddings and special celebrations, requiring considerable skill to construct properly.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'krok-ahm-BOOSH (/ˌkrɒkɑmˈbuʃ/)',
        'etymology': 'French, meaning "crunch in the mouth," from "croquer" (to crunch) + "en bouche" (in mouth)',
        'memory_tips': 'Think "crock + em + bouche (mouth)" - crunches in your mouth',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The wedding _____ towered elegantly above the dessert table.'
    },
    'croquignole': {
        'definition': 'A method of waving hair using special irons; a type of small, crisp biscuit or cookie; a flicking motion with the finger. This versatile term appears in hairdressing, baking, and games requiring finger dexterity.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'krok-een-YOHL (/ˌkrɒkɪnˈjoʊl/)',
        'etymology': 'French, from "croquer" (to crunch) + diminutive suffix',
        'memory_tips': 'Think "crock + ignole" - making crunchy things or crunchy hair waves',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The hairdresser used the _____ technique to create tight, permanent waves.'
    },
    'cross': {
        'definition': 'Two lines intersecting at right angles; a symbol of Christianity; to go from one side to another; to intersect; angry or annoyed. Cross encompasses geometric shapes, religious symbols, movement actions, and emotional states.',
        'part_of_speech': 'noun, verb, adjective',
        'pronunciation_guide': 'KROS (/krɔs/)',
        'etymology': 'From Old English "cros," from Latin "crux" (cross)',
        'memory_tips': 'Think of two lines crossing each other, or crossing a street',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Please look both ways before you _____ the busy street.'
    },
    'crossed': {
        'definition': 'Past tense of cross; went from one side to another; intersected; opposed or thwarted; marked with intersecting lines. Crossed indicates completed action of movement, intersection, or opposition.',
        'part_of_speech': 'verb (past tense), adjective',
        'pronunciation_guide': 'KROSD (/krɔst/)',
        'etymology': 'From "cross" + past tense suffix "-ed"',
        'memory_tips': 'Think "cross + -ed" - successfully completed crossing something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The hikers _____ the bridge safely despite the strong winds.'
    },
    'crosses': {
        'definition': 'Plural of cross; multiple intersecting lines or Christian symbols; third person singular present of cross. Crosses can be geometric figures, religious symbols, or the action of intersecting or traversing.',
        'part_of_speech': 'noun (plural), verb (third person singular)',
        'pronunciation_guide': 'KROS-iz (/ˈkrɔsɪz/)',
        'etymology': 'Plural/present tense of Latin "crux" (cross)',
        'memory_tips': 'Think of multiple crossing points or someone who crosses things',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The cemetery was filled with stone _____ marking the graves.'
    },
    'crossword': {
        'definition': 'A word puzzle consisting of a grid of squares, some filled with letters, where words reading across and down are guided by numbered clues. Crosswords challenge vocabulary, general knowledge, and pattern recognition skills while providing entertainment and mental exercise.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KROS-wurd (/ˈkrɔsˌwɜrd/)',
        'etymology': 'From "cross" + "word" (words crossing each other)',
        'memory_tips': 'Think "cross + word" - words that cross each other in a puzzle grid',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'She enjoyed solving the daily _____ puzzle in the newspaper.'
    }
}

def process_batch():
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_044_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_044_processed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"Processing {len(df)} words from batch 044...")
        
        processed_data = []
        combined_word_errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            if word in batch_044_data:
                data = batch_044_data[word]
                
                if data['part_of_speech'] == 'error - combined words':
                    combined_word_errors.append(word)
                
                phonetic, frequency, morphological, etymology_score = calculate_difficulty_scores(word, data['etymology'])
                
                processed_data.append({
                    'word': word,
                    'definition': data['definition'],
                    'part_of_speech': data['part_of_speech'],
                    'pronunciation_guide': data['pronunciation_guide'],
                    'etymology': data['etymology'],
                    'memory_tips': data['memory_tips'],
                    'alternate_spellings': data['alternate_spellings'],
                    'language_origin': data['language_origin'],
                    'example_sentence': data['example_sentence'],
                    'years': row['years'],
                    'source_files': row['source_files'],
                    'source_difficulties': row['source_difficulties'],
                    'difficulty_phonetic': round(phonetic, 2),
                    'difficulty_frequency': round(frequency, 2),
                    'difficulty_morphological': round(morphological, 2),
                    'difficulty_etymology': round(etymology_score, 2),
                    'difficulty_final': None,
                    'etymology_source': 'Claude',
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'example_sentence_source': 'Claude'
                })
        
        output_df = pd.DataFrame(processed_data)
        output_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"Successfully processed {len(processed_data)}/50 words")
        print(f"Output saved to: {output_file}")
        
        if combined_word_errors:
            print(f"Found {len(combined_word_errors)} combined word errors:")
            for error in combined_word_errors:
                print(f"   - {error}")
        else:
            print("No combined word errors found")
            
        return True
        
    except Exception as e:
        print(f"Error processing batch: {str(e)}")
        return False

if __name__ == "__main__":
    process_batch()