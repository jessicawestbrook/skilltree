#!/usr/bin/env python3

import csv
import os

class DifficultyCalculator:
    def __init__(self):
        self.phonetic_patterns = {
            'silent_letters': ['k', 'w', 'l', 'b', 't', 'h'],
            'irregular_sounds': ['ph', 'gh', 'ough', 'augh', 'eigh'],
            'double_letters': ['ss', 'll', 'tt', 'nn', 'mm', 'pp', 'ff', 'cc', 'dd'],
            'vowel_teams': ['ea', 'oa', 'ie', 'ai', 'ey', 'ay', 'ow', 'ou']
        }
        
        self.morphological_markers = {
            'prefixes': ['un', 'pre', 'dis', 'mis', 'over', 'under', 'sub', 'super', 'anti', 're', 'de', 'ex'],
            'suffixes': ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ous', 'ious', 'ly', 'ing', 'ed', 'er', 'est'],
            'roots': ['spect', 'dict', 'graph', 'phon', 'bio', 'geo', 'auto', 'tele']
        }

    def calculate_phonetic_transparency(self, word):
        score = 0
        word_lower = word.lower()
        
        for pattern in self.phonetic_patterns['silent_letters']:
            if pattern in word_lower and not word_lower.endswith(pattern + 'e'):
                score += 1
                
        for pattern in self.phonetic_patterns['irregular_sounds']:
            if pattern in word_lower:
                score += 2
                
        for pattern in self.phonetic_patterns['double_letters']:
            if pattern in word_lower:
                score += 0.5
                
        return min(score, 5)

    def calculate_word_frequency(self, word):
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
        
        word_lower = word.lower()
        if word_lower in common_words:
            return 1
        elif len(word) <= 4:
            return 2
        elif len(word) <= 6:
            return 3
        elif len(word) <= 8:
            return 4
        else:
            return 5

    def calculate_morphological_complexity(self, word):
        score = 0
        word_lower = word.lower()
        
        prefix_count = sum(1 for prefix in self.morphological_markers['prefixes'] if word_lower.startswith(prefix))
        suffix_count = sum(1 for suffix in self.morphological_markers['suffixes'] if word_lower.endswith(suffix))
        root_count = sum(1 for root in self.morphological_markers['roots'] if root in word_lower)
        
        total_morphemes = prefix_count + suffix_count + root_count
        
        if total_morphemes == 0:
            score = 1
        elif total_morphemes == 1:
            score = 2
        elif total_morphemes == 2:
            score = 3
        elif total_morphemes == 3:
            score = 4
        else:
            score = 5
            
        return score

    def calculate_etymology_complexity(self, word):
        etymology_indicators = {
            'latin': ['tion', 'sion', 'ous', 'ious', 'able', 'ible'],
            'greek': ['ph', 'th', 'ch', 'ps', 'pt', 'rh'],
            'french': ['eau', 'eur', 'oir', 'ique'],
            'german': ['sch', 'tch', 'tz'],
            'other': ['kh', 'gh', 'zh', 'x']
        }
        
        word_lower = word.lower()
        complexity_score = 1
        
        for origin, patterns in etymology_indicators.items():
            for pattern in patterns:
                if pattern in word_lower:
                    if origin in ['greek', 'other']:
                        complexity_score += 2
                    elif origin in ['french', 'german']:
                        complexity_score += 1.5
                    else:
                        complexity_score += 1
                    break
                    
        return min(complexity_score, 5)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'output', 'batch_160_words.csv')
    output_file = os.path.join(script_dir, 'output', 'batch_160_processed.csv')
    
    calculator = DifficultyCalculator()
    
    # Comprehensive word data with educational content
    word_data = {
        'shrapnel': {
            'definition': 'Shrapnel refers to fragments of metal, glass, or other material thrown out by an explosion, particularly from artillery shells, bombs, or improvised explosive devices. Originally, shrapnel was a specific type of artillery shell invented by British Army officer Henry Shrapnel in 1784, designed to explode in the air and shower enemy troops with metal balls. In modern usage, the term broadly describes any dangerous debris created by explosions, including pieces of the explosive device itself and nearby objects fragmented by the blast. Shrapnel poses significant danger to people and property, as these high-velocity fragments can cause severe injuries or damage. The word has also entered metaphorical use to describe scattered remnants or fallout from conflicts or disasters.',
            'pronunciation': '/ˈʃræpnəl/',
            'example_sentence': 'The bomb disposal expert carefully examined the area for dangerous _____ after the controlled explosion.',
            'etymology': 'Named after British Army officer Henry Shrapnel (1761-1842), who invented the shrapnel shell in 1784.',
            'mnemonic': 'Think "SHARP-NEL = SHARP metal pieces" - shrapnel consists of sharp fragments from explosions.',
            'source': 'Claude'
        },
        'shrike': {
            'definition': 'A shrike is a carnivorous songbird belonging to the family Laniidae, known for its distinctive hunting behavior of impaling prey on thorns, barbed wire, or sharp twigs to create a "larder" for later consumption. These medium-sized birds have hooked beaks similar to raptors and hunt insects, small mammals, reptiles, and even other birds. Shrikes are sometimes called "butcher birds" due to their habit of storing prey by skewering it on sharp objects. They inhabit open country with scattered trees and bushes across various continents. Despite their predatory nature, shrikes are technically songbirds with complex vocalizations. Their hunting strategy of impaling prey serves both to secure food for lean times and to help them tear apart prey too large to swallow whole.',
            'pronunciation': '/ʃraɪk/',
            'example_sentence': 'The _____ perched on the fence post, scanning the field for insects to catch and impale on nearby thorns.',
            'etymology': 'From Old English "scrīc," related to "shriek," referring to the bird\'s harsh call.',
            'mnemonic': 'Think "SHRIKE = SHarp beaR-IKE hunter" - a sharp-beaked bird that hunts like a small bear.',
            'source': 'Claude'
        },
        'shrimp': {
            'definition': 'Shrimp are small, swimming crustaceans found in both marine and freshwater environments worldwide, characterized by their elongated bodies, long antennae, and multiple pairs of swimming legs called pleopods. These decapod crustaceans are closely related to lobsters and crabs but typically have more compressed bodies adapted for swimming rather than walking. Shrimp play crucial roles in aquatic food webs, serving as both predators of small organisms and prey for fish, birds, and marine mammals. Many species are commercially important for human consumption, with shrimp farming and fishing representing major global industries. The term encompasses hundreds of species ranging from tiny transparent creatures to large prawns several inches long.',
            'pronunciation': '/ʃrɪmp/',
            'example_sentence': 'The chef prepared a delicious pasta dish featuring fresh Gulf _____ with garlic and herbs.',
            'etymology': 'From Middle English "shrimpe," possibly related to Middle High German "schrimpfen" meaning "to wrinkle" or "to shrivel."',
            'mnemonic': 'Think "SHRIMP = SHRInk-sized creature that swiMs in water Permanently" - small swimming crustaceans.',
            'source': 'Claude'
        },
        'shrine': {
            'definition': 'A shrine is a sacred or holy place dedicated to a specific deity, saint, ancestor, hero, or religious figure, often containing relics, images, or other objects of veneration. Shrines can range from elaborate temples and churches to simple roadside markers or household altars, serving as focal points for prayer, meditation, and religious devotion. They exist in virtually all religious traditions and cultures, sometimes marking places where miraculous events allegedly occurred or where holy people lived or died. Shrines often become pilgrimage destinations, drawing visitors seeking spiritual connection, healing, or blessing. The concept extends beyond religion to include memorials honoring secular figures or commemorating significant events.',
            'pronunciation': '/ʃraɪn/',
            'example_sentence': 'Pilgrims traveled hundreds of miles to visit the mountain _____ dedicated to the patron saint of their village.',
            'etymology': 'From Old English "scrīn," from Latin "scrinium" meaning "case" or "chest," originally referring to a container for sacred objects.',
            'mnemonic': 'Think "SHRINE = Sacred Holy Religious Important Named place" - a sacred place for worship.',
            'source': 'Claude'
        },
        'shrivellimbering': {
            'definition': '[COMBINED WORD ERROR] This appears to be two or more words incorrectly combined: likely "shrivel" and "limbering." Shrivel means to wrinkle and contract or to become dried up and withered. Limbering refers to the process of making something flexible and supple, often through stretching exercises or warm-up activities. These are distinct concepts that should not be combined. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈʃrɪvəl ˈlɪmbərɪŋ/',
            'example_sentence': 'The leaves will _____ in the heat, so athletes should start _____ up before their workout.',
            'etymology': 'Shrivel: from Middle English "shrivelen." Limbering: from "limber" + "-ing," meaning to make flexible.',
            'mnemonic': 'Remember these as SEPARATE words: SHRIVEL (to dry up) + LIMBERING (making flexible).',
            'source': 'Claude'
        },
        'shrugged': {
            'definition': 'Shrugged is the past tense of "shrug," meaning to raise one\'s shoulders briefly to express doubt, indifference, ignorance, or uncertainty about something. This gesture is a universal form of non-verbal communication that conveys "I don\'t know," "I don\'t care," or "what can you do?" The movement typically involves lifting both shoulders simultaneously toward the ears and then releasing them. Shrugging can also mean to dismiss or disregard something casually, as in "shrugging off" criticism or problems. The gesture often accompanies verbal expressions of uncertainty and can range from a subtle shoulder movement to an exaggerated display depending on the intensity of the emotion being conveyed.',
            'pronunciation': '/ʃrʌɡd/',
            'example_sentence': 'When asked about the missing homework, the student simply _____ and said he had forgotten about it.',
            'etymology': 'From Middle English, possibly from Old Norse "skrukka" meaning "to shrink" or from the gesture\'s resemblance to contracting.',
            'mnemonic': 'Think "SH-RUGGED = SHowing uncertainty with shoulders RUGGED upward" - lifting shoulders to show doubt.',
            'source': 'Claude'
        },
        'shruthika': {
            'definition': 'Shruthika is a feminine given name of Sanskrit origin, derived from "shruti," which means "that which is heard" and refers to the sacred texts and divine revelations in Hindu tradition, particularly the Vedas. In Hindu philosophy, shruti represents the eternal truths that were "heard" by ancient sages in deep meditation and later transmitted orally before being written down. The name suggests someone connected to divine knowledge, sacred learning, or spiritual wisdom. Names ending in "-ika" are common in Sanskrit, often indicating possession of a quality or association with something. As a personal name, Shruthika would typically be given to girls with hopes that they will be wise, learned, or spiritually inclined.',
            'pronunciation': '/ʃruˈθikə/',
            'example_sentence': '_____ excelled in her Sanskrit studies, living up to the meaning of her name which connects to sacred knowledge.',
            'etymology': 'From Sanskrit "shruti" (that which is heard, sacred knowledge) + suffix "-ika" (possessing, characterized by).',
            'mnemonic': 'Think "SHRUTI-KA = Knowledge of Sacred Hearing, Understanding Truth, Inspiring Keeping Ancient wisdom" - connected to sacred learning.',
            'source': 'Claude'
        },
        'shubunkin': {
            'definition': 'A shubunkin is a variety of goldfish characterized by its calico coloration, combining blue, red, orange, black, and white patches in mottled patterns across its body. These hardy ornamental fish were originally developed in Japan in the early 1900s and are prized for their vibrant, multicolored appearance and active swimming behavior. Shubunkins typically have longer, more streamlined bodies than common goldfish and can grow quite large in suitable conditions. They are popular in outdoor ponds and water gardens because of their tolerance for temperature variations and their ability to coexist peacefully with other pond fish. The nacreous (pearlescent) scales create an iridescent effect that enhances their distinctive coloration patterns.',
            'pronunciation': '/ʃuˈbʌŋkɪn/',
            'example_sentence': 'The pond owner added several colorful _____ goldfish to complement the water lilies and create a more diverse aquatic display.',
            'etymology': 'From Japanese, where "shu" relates to "vermillion/red" and the name describes the mixed coloration pattern.',
            'mnemonic': 'Think "SHU-BUNKIN = SHiny, Unique, Beautiful fish with UNusual coloring, Blue/white/red IN patches" - multicolored goldfish.',
            'source': 'Claude'
        },
        'shuffle': {
            'definition': 'Shuffle means to walk without lifting the feet completely off the ground, creating a sliding or dragging motion that produces a distinctive sound. This gait pattern can result from fatigue, illness, advanced age, or simply casual movement. The term also describes the act of mixing cards by sliding and rearranging them to randomize their order before dealing. In music, shuffle refers to a specific rhythmic pattern where eighth notes are played with uneven timing, creating a swinging feel common in blues and jazz. Metaphorically, shuffle can mean to rearrange items, reorganize responsibilities, or move things around without clear purpose or direction.',
            'pronunciation': '/ˈʃʌfəl/',
            'example_sentence': 'The elderly man would _____ slowly down the hallway, his slippers making a soft scraping sound on the floor.',
            'etymology': 'From Middle Dutch "schoffelen" meaning "to shove" or "to scrape," related to pushing or sliding movements.',
            'mnemonic': 'Think "SH-UFFLE = SHuffling feet make a scrUFFLE sound" - sliding feet create a scuffling noise.',
            'source': 'Claude'
        },
        'shui': {
            'definition': 'Shui, most commonly encountered in the term "feng shui," is a Chinese word meaning "water" in Mandarin Chinese. In the context of feng shui, it represents the flow of energy (qi) and the balance between elements in environmental design and spatial arrangement. Water symbolizes wealth, abundance, and the flow of positive energy in Chinese philosophy and culture. The concept emphasizes how the placement and movement of water, whether actual or symbolic, can influence harmony, prosperity, and well-being in living and working spaces. As a standalone term, shui appears in various Chinese cultural and philosophical contexts related to water\'s symbolic and practical importance.',
            'pronunciation': '/ʃweɪ/',
            'example_sentence': 'The interior designer incorporated principles of feng _____ to create a harmonious flow of energy throughout the home.',
            'etymology': 'From Mandarin Chinese "水" (shuǐ) meaning "water," fundamental to Chinese philosophy and environmental design.',
            'mnemonic': 'Think "SHUI = water SHUffles In harmony" - water represents flow and harmony in Chinese philosophy.',
            'source': 'Claude'
        },
        'shute': {
            'definition': 'Shute is an alternative spelling of "chute," referring to a sloped or vertical passage down which things can slide or fall, such as a laundry chute, mail chute, or water slide. The term also applies to parachutes, particularly in informal contexts where "pulling the shute" means deploying a parachute. In some regions, shute describes natural geographical features like narrow valleys or ravines. The word can also function as a surname, most famously associated with author Nevil Shute. In industrial contexts, shutes direct the flow of materials from higher to lower elevations, utilizing gravity to facilitate efficient movement of goods, waste, or other materials.',
            'pronunciation': '/ʃut/',
            'example_sentence': 'The miners used a wooden _____ to send ore down from the mountainside quarry to the processing facility below.',
            'etymology': 'Variant spelling of "chute," from French "chute" meaning "fall," from "choir" (to fall).',
            'mnemonic': 'Think "SHUTE = SHifl down vertical tUTE (tube)" - a tube or passage for things to slide down.',
            'source': 'Claude'
        },
        'shutterscorner': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "shutters" and "corner." Shutters are hinged panels used to cover windows for protection, privacy, or decoration, typically made of wood, vinyl, or metal. A corner is the point where two lines, surfaces, or edges meet at an angle, or a secluded or remote area. These are distinct architectural and spatial concepts that should not be combined. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈʃʌtərz ˈkɔrnər/',
            'example_sentence': 'The old house had green wooden _____ on every window, and roses growing around the quiet _____ of the garden.',
            'etymology': 'Shutters: from "shut" + "-er." Corner: from Old French "cornier," from Latin "cornu" meaning "horn" or "angle."',
            'mnemonic': 'Remember these as TWO words: SHUTTERS (window coverings) + CORNER (where two edges meet).',
            'source': 'Claude'
        },
        'sibilant': {
            'definition': 'Sibilant describes speech sounds characterized by a hissing quality, produced when air flows through a narrow channel formed by the tongue and teeth or palate. The primary sibilant sounds in English include /s/, /z/, /ʃ/ (sh), /ʒ/ (zh), and the affricate sounds /tʃ/ (ch) and /dʒ/ (j). These sounds are distinguished by their high-frequency acoustic energy that creates the characteristic hissing or hushing effect. In phonetics and linguistics, sibilants form an important category for understanding speech production and sound patterns across languages. The term can also describe any sound that resembles the hissing of a snake, extending beyond linguistic contexts to describe natural phenomena or mechanical sounds.',
            'pronunciation': '/ˈsɪbələnt/',
            'example_sentence': 'The speech therapist worked with the child to correctly produce _____ sounds like "s" and "sh" without lisping.',
            'etymology': 'From Latin "sibilans" (hissing), from "sibilare" meaning "to hiss" or "to whistle," imitating the snake-like sound.',
            'mnemonic': 'Think "SIB-ILANT = Snake-lIke hissing Bouncing In Language ANd Talk" - hissing speech sounds.',
            'source': 'Claude'
        },
        'siblings': {
            'definition': 'Siblings are brothers and sisters who share at least one parent, forming some of the most enduring relationships in human experience. This familial bond encompasses full siblings (sharing both parents), half-siblings (sharing one parent), and adopted siblings (sharing no biological parents but raised in the same family). Sibling relationships significantly influence personality development, social skills, and lifelong behavioral patterns through shared experiences, competition, cooperation, and mutual support. Birth order among siblings has been studied extensively for its effects on personality traits and life outcomes. The sibling dynamic often involves complex emotions including love, rivalry, protection, and companionship that evolve throughout life stages.',
            'pronunciation': '/ˈsɪblɪŋz/',
            'example_sentence': 'The three _____ took turns caring for their elderly parents, sharing responsibilities based on their different strengths.',
            'etymology': 'From Old English "sibling," meaning "relative" or "kinsman," from "sib" (kinship) + "-ling" (diminutive suffix).',
            'mnemonic': 'Think "SIB-LINGS = Same famIly Background, Living togetherINGS" - family members who grow up together.',
            'source': 'Claude'
        },
        'sidekick': {
            'definition': 'A sidekick is a close companion or assistant who loyally supports and accompanies a main character or leader, often providing help, comic relief, or specialized skills. The term originated in stories and entertainment media, describing characters like Robin to Batman or Watson to Sherlock Holmes, but has expanded to describe real-life relationships where one person consistently supports another\'s endeavors. Sidekicks typically possess complementary abilities that enhance the main character\'s effectiveness while remaining secondary in importance or recognition. The relationship usually involves trust, loyalty, and mutual benefit, though the sidekick traditionally receives less credit or attention than the primary figure they assist.',
            'pronunciation': '/ˈsaɪdˌkɪk/',
            'example_sentence': 'The detective relied on his trusted _____ to notice important details he might miss during investigations.',
            'etymology': 'American slang from the 1900s, possibly from "side" (beside) + "kick" (companion), originally referring to a pickpocket\'s partner.',
            'mnemonic': 'Think "SIDE-KICK = stays by your SIDE and gives you a KICK (boost)" - a loyal helper who supports you.',
            'source': 'Claude'
        },
        'sideways': {
            'definition': 'Sideways means oriented, moving, or facing toward one side rather than forward, backward, or straight ahead. This directional term describes lateral movement or positioning where something is turned at a right angle to its normal orientation. In driving, sideways movement might result from skidding or drifting. The word also has metaphorical uses, such as "looking sideways" at someone to express suspicion or disapproval, or situations "going sideways" meaning they become problematic or chaotic. In various contexts, sideways positioning can be intentional for practical purposes or accidental due to external forces, and the orientation often affects functionality or stability.',
            'pronunciation': '/ˈsaɪdˌweɪz/',
            'example_sentence': 'The large sofa had to be turned _____ to fit through the narrow doorway during the move.',
            'etymology': 'From "side" + "ways," indicating direction or manner, similar to "always" or "sideward."',
            'mnemonic': 'Think "SIDE-WAYS = traveling in SIDE direction inWAYS" - moving or facing to the side.',
            'source': 'Claude'
        },
        'sieve': {
            'definition': 'A sieve is a utensil consisting of a mesh or perforated surface stretched across a frame, used to separate larger particles from smaller ones by allowing fine materials to pass through while retaining coarser materials. Sieves are essential tools in cooking for straining liquids, sifting flour, or separating solids from liquids. In scientific and industrial applications, sieves help classify particles by size for quality control or analysis. The term extends metaphorically to describe something that allows selective passage, such as a "leaky sieve" for someone who cannot keep secrets. Archaeological excavations use sieves to recover small artifacts from soil, and the concept applies to data filtering and information processing.',
            'pronunciation': '/sɪv/',
            'example_sentence': 'The chef used a fine-mesh _____ to remove lumps from the flour before making the delicate pastry.',
            'etymology': 'From Old English "sife," related to German "Sieb," ultimately from a root meaning "to drip" or "to strain."',
            'mnemonic': 'Think "SIEVE = Separates Items by Varying sizE" - a tool that separates by letting small things through.',
            'source': 'Claude'
        },
        'sifting': {
            'definition': 'Sifting is the process of separating materials of different sizes by passing them through a sieve or similar screening device, allowing fine particles to fall through while retaining larger ones. In cooking, sifting flour removes lumps and aerates the ingredient, creating lighter, more evenly textured baked goods. The term also describes careful examination or analysis, as in "sifting through evidence" or "sifting facts from fiction." Archaeological sifting helps recover small artifacts from excavated soil. Gold prospectors historically used sifting techniques to separate gold particles from sand and gravel. The process requires patience and systematic approach to achieve effective separation or thorough examination.',
            'pronunciation': '/ˈsɪftɪŋ/',
            'example_sentence': 'The detective spent hours _____ through the documents, looking for any clue that might solve the case.',
            'etymology': 'From "sift," which comes from Old English "siftan," meaning "to strain" or "to separate," related to "sieve."',
            'mnemonic': 'Think "SIFT-ING = Separating Items by Fine-mesh Through careful examinING" - carefully separating or examining.',
            'source': 'Claude'
        },
        'sighed': {
            'definition': 'Sighed is the past tense of "sigh," meaning to emit a long, deep audible breath that typically expresses sadness, relief, fatigue, or resignation. This involuntary or deliberate respiratory action often accompanies emotional states and serves as a form of non-verbal communication. Sighing can indicate disappointment when things don\'t go as expected, relief when stress is released, or weariness from physical or emotional exhaustion. The action involves a deeper inhalation followed by a prolonged, often audible exhalation. Research suggests that sighing also serves physiological functions, helping to reset lung function and maintain proper breathing patterns even during sleep.',
            'pronunciation': '/saɪd/',
            'example_sentence': 'She _____ deeply as she looked at the long list of chores that still needed to be completed.',
            'etymology': 'From Middle English "sighen," possibly from Old English "sīcan" meaning "to sigh," imitative of the sound.',
            'mnemonic': 'Think "SIGHED = Sad, tIred, Gave Heavy Exhausted breath" - a deep breath expressing emotion.',
            'source': 'Claude'
        },
        'sights': {
            'definition': 'Sights refers to things that are seen or worth seeing, often describing notable landmarks, attractions, or interesting visual experiences in a particular location. In the context of tourism, sights are destinations or features that draw visitors, such as historical monuments, natural wonders, or cultural attractions. The term also applies to the visual targeting devices on firearms used to aim accurately. Additionally, "sights" can mean one\'s range of vision or ambitions, as in "setting one\'s sights" on a goal. The word encompasses both the physical act of seeing and the objects or experiences that are visually remarkable or significant enough to warrant attention.',
            'pronunciation': '/saɪts/',
            'example_sentence': 'The tourists spent the week visiting all the famous _____ in the historic city center.',
            'etymology': 'From Old English "siht," meaning "something seen" or "vision," related to "see" and "sight."',
            'mnemonic': 'Think "SIGHTS = Scenic Interesting Geographic Historic Tourism Spots" - places worth seeing.',
            'source': 'Claude'
        },
        'sign': {
            'definition': 'A sign is a visual display that conveys information, warnings, directions, or identification, typically using text, symbols, or images to communicate with viewers. Signs serve countless purposes in society, from traffic control and business advertising to safety warnings and wayfinding. The term also refers to evidence or indication of something\'s presence or occurrence, such as signs of spring or signs of illness. In linguistics, a sign represents the relationship between a signifier (the form) and signified (the meaning). Sign language uses hand gestures and body movements as signs to communicate. The act of signing involves writing one\'s name or marking documents to indicate approval, agreement, or authentication.',
            'pronunciation': '/saɪn/',
            'example_sentence': 'The bright neon _____ outside the diner made it easy to spot from the highway.',
            'etymology': 'From Old French "signe," from Latin "signum" meaning "mark," "token," or "indication."',
            'mnemonic': 'Think "SIGN = Shows Important iNformation Giving direction" - displays that give information.',
            'source': 'Claude'
        },
        'signal': {
            'definition': 'A signal is a gesture, sound, light, or other indicator used to convey information, instructions, or warnings to others, often across distances or in situations where direct communication is difficult. Signals can be simple, like a wave of the hand, or complex, like digital data transmission in telecommunications. Traffic signals control vehicle and pedestrian movement using standardized color codes. In technology, signals carry information through various media including radio waves, electrical currents, and fiber optic cables. The term also describes any detectable change or pattern that indicates the presence or state of something, such as biological signals in medical monitoring or market signals in economics.',
            'pronunciation': '/ˈsɪɡnəl/',
            'example_sentence': 'The lighthouse sent a bright _____ across the water to warn ships of the dangerous rocks below.',
            'etymology': 'From Old French "signal," from Medieval Latin "signale," from Latin "signum" meaning "mark" or "sign."',
            'mnemonic': 'Think "SIG-NAL = SIGn that\'s Notably Audible or Luminous" - a sign that can be seen or heard from far away.',
            'source': 'Claude'
        },
        'signatory': {
            'definition': 'A signatory is a person, organization, or nation that has signed a formal document, agreement, treaty, or contract, thereby indicating their consent, approval, or commitment to its terms. Signatories bear legal and moral responsibility for adhering to the provisions of the documents they sign. In international relations, signatory countries to treaties agree to uphold specific obligations and cooperate on shared goals. Business signatories to contracts become legally bound to fulfill their stated commitments. The term emphasizes the formal nature of agreement and the accountability that comes with adding one\'s signature to important documents. Multiple signatories to the same document create binding multilateral agreements.',
            'pronunciation': '/ˈsɪɡnəˌtɔri/',
            'example_sentence': 'As a _____ to the international climate agreement, the country committed to reducing carbon emissions by thirty percent.',
            'etymology': 'From Latin "signatorius," meaning "of or relating to sealing or signing," from "signare" (to sign or seal).',
            'mnemonic': 'Think "SIGN-A-TORY = one who SIGNs A Treaty, taking Obligation and Responsibility for Years" - someone who formally signs agreements.',
            'source': 'Claude'
        },
        'sikhism': {
            'definition': 'Sikhism is a monotheistic religion founded in the 15th century by Guru Nanak in the Punjab region of South Asia, emphasizing devotion to one God, equality of all people, and service to humanity. The faith is guided by the teachings of ten Gurus and the sacred text called the Guru Granth Sahib. Core principles include meditation on God\'s name, honest work, and sharing with others. Sikhs reject the caste system and advocate for gender equality and social justice. The religion combines elements of Hindu and Islamic traditions while maintaining its distinct identity. Visible symbols include the turban and five Ks (uncut hair, comb, steel bracelet, cotton undergarment, and ceremonial sword), representing spiritual commitment and readiness to defend the innocent.',
            'pronunciation': '/ˈsikˌɪzəm/',
            'example_sentence': 'The principles of _____ emphasize serving others regardless of their background or beliefs.',
            'etymology': 'From Punjabi "sikhi," derived from Sanskrit "śiṣya" meaning "disciple" or "student," referring to followers of the Guru\'s teachings.',
            'mnemonic': 'Think "SIKH-ISM = Seeking Inner Knowledge and Helping others, following Indian Spiritual Movement" - religion of disciples seeking truth.',
            'source': 'Claude'
        },
        'silence': {
            'definition': 'Silence is the absence of sound or noise, creating a state of quietness that can be profound, peaceful, or sometimes uncomfortable depending on the context. Beyond mere acoustic emptiness, silence carries deep psychological and cultural significance, often representing contemplation, respect, secrecy, or sometimes oppression. In communication, silence can be as meaningful as words, conveying disagreement, thoughtfulness, or emotional overwhelm. Different cultures interpret silence differently - some viewing it as wisdom and restraint, others as rudeness or disengagement. Silence is essential for concentration, meditation, and healing, while imposed silence can represent censorship or punishment. The quality and meaning of silence varies greatly depending on circumstances, duration, and cultural context.',
            'pronunciation': '/ˈsaɪləns/',
            'example_sentence': 'The library maintained perfect _____ to help students concentrate on their research and studies.',
            'etymology': 'From Old French "silence," from Latin "silentium," from "silere" meaning "to be quiet" or "to be still."',
            'mnemonic': 'Think "SIL-ENCE = Sound Is Less, Everything Naturally Calm and Encore-free" - the absence of sound.',
            'source': 'Claude'
        },
        'silent': {
            'definition': 'Silent describes the state of being quiet, making no sound, or choosing not to speak, either voluntarily or involuntarily. The term applies to people who remain quiet during conversations, machines that operate without noise, or environments devoid of sound. Silent can indicate respectful restraint, as in silent prayer or silent mourning, or strategic withholding of information. In language, silent letters are written but not pronounced, like the "k" in "knife." Silent films from early cinema relied on visual storytelling without synchronized sound. The concept extends to abstract ideas like silent suffering or silent approval, where communication occurs without verbal expression.',
            'pronunciation': '/ˈsaɪlənt/',
            'example_sentence': 'The classroom fell completely _____ when the principal entered to make an important announcement.',
            'etymology': 'From Latin "silens," present participle of "silere" meaning "to be quiet" or "to keep still."',
            'mnemonic': 'Think "SIL-ENT = Sound Is Less, Everyone\'s Not Talking" - making no sound or speech.',
            'source': 'Claude'
        },
        'silhouette': {
            'definition': 'A silhouette is the dark outline or shadow of someone or something visible against a lighter background, creating a distinctive shape without internal details. Originally, silhouettes were profile portraits cut from black paper or filled in with solid color, popular in the 18th and 19th centuries as affordable alternatives to painted portraits. The technique emphasizes form and contour while eliminating color and fine detail, often creating dramatic or artistic effects. In photography and art, silhouettes are created by backlighting subjects, making them appear as dark shapes against bright backgrounds. The term extends to any outline or general form that resembles this visual effect, such as city skylines or mountain ridges against the sky.',
            'pronunciation': '/ˌsɪluˈɛt/',
            'example_sentence': 'The mountain\'s _____ stood out dramatically against the orange and pink colors of the sunset.',
            'etymology': 'Named after Étienne de Silhouette, French finance minister (1767), known for his austere economic policies, hence "reduced to outline."',
            'mnemonic': 'Think "SIL-HOU-ETTE = SILly HOUse shape, Every Thing shown as outline" - just the outline shape without details.',
            'source': 'Claude'
        },
        'silico': {
            'definition': 'Silico, commonly appearing in the term "in silico," refers to computer simulation or computational analysis, particularly in biological and scientific research. This Latin phrase parallels "in vitro" (in glass) and "in vivo" (in living organisms), describing experiments or studies conducted through computer modeling rather than physical laboratory work or living systems. In silico research uses mathematical models, algorithms, and computer simulations to study complex biological processes, drug interactions, genetic sequences, or molecular behavior. This approach allows scientists to test hypotheses rapidly and cost-effectively before conducting physical experiments. The term emphasizes the growing importance of computational methods in modern scientific discovery and pharmaceutical development.',
            'pronunciation': '/sɪˈlɪkoʊ/',
            'example_sentence': 'The researchers used _____ modeling to predict how the new drug would interact with various proteins before beginning laboratory testing.',
            'etymology': 'Modern Latin, meaning "in silicon," referring to the silicon chips in computers, coined to parallel "in vitro" and "in vivo."',
            'mnemonic': 'Think "SIL-ICO = SILicon computer ICOn/interface" - research done inside computer simulations.',
            'source': 'Claude'
        },
        'silicon': {
            'definition': 'Silicon is a chemical element with the symbol Si and atomic number 14, representing the second most abundant element in Earth\'s crust after oxygen. This metalloid forms the basis of most rocks, sand, and clay minerals, appearing primarily in compounds rather than pure form. Silicon\'s unique properties make it essential for semiconductor technology, forming the foundation of computer chips, solar panels, and electronic devices. The element can exist in crystalline forms like quartz or amorphous forms like glass. Industrial applications include silicone polymers, glass manufacturing, and metallurgy. Silicon Valley, the famous technology hub, derives its name from the semiconductor industry\'s reliance on this element for creating integrated circuits.',
            'pronunciation': '/ˈsɪlɪkən/',
            'example_sentence': 'The computer processor contained millions of transistors etched onto a _____ wafer using advanced photolithography techniques.',
            'etymology': 'From Latin "silex" meaning "flint" or "hard stone," with the suffix "-on" added to indicate its non-metallic nature.',
            'mnemonic': 'Think "SIL-ICON = SILver-like element for Integrated Computer and Electronic Networks" - the element that powers electronics.',
            'source': 'Claude'
        },
        'silique': {
            'definition': 'A silique is an elongated seed pod characteristic of plants in the Brassicaceae family (mustards, cabbages, and their relatives), distinguished by its length being at least three times its width. These specialized fruits consist of two chambers separated by a membranous partition called a replum, with seeds attached along the edges. When mature, siliques split open from bottom to top, allowing seeds to disperse. Common examples include the seed pods of mustard, wallflower, and stock plants. The structure efficiently protects developing seeds while facilitating dispersal when conditions are favorable. Siliques differ from silicles, which are shorter and wider, but both represent important identifying features for botanists classifying plants in this large family.',
            'pronunciation': '/sɪˈlik/',
            'example_sentence': 'The botanist examined the plant\'s long, narrow _____ to confirm it belonged to the mustard family.',
            'etymology': 'From Latin "siliqua" meaning "pod" or "husk," originally referring to the carob pod used as a unit of weight.',
            'mnemonic': 'Think "SIL-IQUE = Seed pod that\'s In Length, extending far, Indicating QUality of mustard family" - long seed pods.',
            'source': 'Claude'
        },
        'silk': {
            'definition': 'Silk is a natural protein fiber produced by certain insects, most notably the domesticated silkworm (Bombyx mori), prized for its lustrous appearance, smooth texture, and strength. The fiber consists of proteins called fibroin, which silkworms secrete to create cocoons during metamorphosis. Silk production, or sericulture, involves carefully tending silkworms, harvesting cocoons, and unwinding the continuous filaments to create thread. The resulting fabric is valued for its beauty, drape, and versatility in clothing and textiles. Wild silks from other moth species offer different textures and characteristics. Silk has played crucial roles in trade, culture, and economics throughout history, famously connecting East and West through the Silk Road trade routes.',
            'pronunciation': '/sɪlk/',
            'example_sentence': 'The bride\'s dress was made from pure _____ that shimmered elegantly in the cathedral\'s stained-glass light.',
            'etymology': 'From Old English "seolc," from Latin "sericum," from Greek "serikos" meaning "of the Seres (Chinese people)."',
            'mnemonic': 'Think "SILK = Smooth, Iridescent, Luxurious fabric from Kimono tradition" - smooth, shiny fabric from silkworms.',
            'source': 'Claude'
        },
        'silly': {
            'definition': 'Silly describes behavior, ideas, or situations that are foolish, lacking in good sense, or amusingly trivial, often in a lighthearted rather than seriously problematic way. The word can characterize harmless fun, childish antics, or decisions that seem unwise but not dangerous. Silly behavior might include making funny faces, telling nonsensical jokes, or engaging in playful activities that others might consider beneath their dignity. The term often carries affectionate connotations when describing children or loved ones, suggesting endearing foolishness rather than serious criticism. Context determines whether "silly" implies gentle teasing, mild disapproval, or simply acknowledgment of something\'s amusing absurdity.',
            'pronunciation': '/ˈsɪli/',
            'example_sentence': 'The children burst into giggles at their teacher\'s _____ impression of a dancing penguin.',
            'etymology': 'From Middle English "sely" meaning "blessed" or "innocent," which evolved through "simple" to "foolish."',
            'mnemonic': 'Think "SIL-LY = Simple, Innocent, Laughable behavior that\'s Light and Young-hearted" - harmlessly foolish.',
            'source': 'Claude'
        },
        'silver': {
            'definition': 'Silver is a precious metal with the chemical symbol Ag (from Latin argentum), renowned for its brilliant white metallic luster, malleability, and excellent electrical and thermal conductivity. Throughout history, silver has served as currency, jewelry, and decorative objects, ranking second only to gold in value among precious metals. The metal possesses antimicrobial properties, making it useful in medical applications and water purification. Industrial uses include electronics, photography, mirrors, and solar panels. Silver naturally occurs in ore deposits and as a byproduct of mining other metals. The term also describes the color resembling polished silver and serves as a metaphor for eloquence, as in "silver tongue," or aging, as in "silver hair."',
            'pronunciation': '/ˈsɪlvər/',
            'example_sentence': 'The antique _____ tea set had been passed down through four generations of the family.',
            'etymology': 'From Old English "seolfor," related to German "Silber," from a Germanic root meaning "silver."',
            'mnemonic': 'Think "SIL-VER = Shiny, Important, Lustrous, Valuable Element for Riches" - precious shiny metal.',
            'source': 'Claude'
        },
        'similar': {
            'definition': 'Similar means having qualities, characteristics, or appearances that are alike or comparable to something else, though not necessarily identical. The concept involves recognizing patterns, shared features, or analogous properties between different objects, people, situations, or ideas. Similar items might differ in minor details while maintaining fundamental resemblances in structure, function, or essential qualities. In mathematics, similar figures have the same shape but may differ in size, maintaining proportional relationships. The degree of similarity can vary greatly, from nearly identical to sharing only a few key features. Understanding similarity helps in classification, comparison, learning, and making predictions based on previous experiences with comparable situations.',
            'pronunciation': '/ˈsɪmələr/',
            'example_sentence': 'The two paintings had _____ color schemes and composition, though they were created by different artists decades apart.',
            'etymology': 'From French "similaire," from Latin "similis" meaning "like" or "resembling."',
            'mnemonic': 'Think "SIM-ILAR = Same In Many aspects, Including Length And Range" - alike in many ways.',
            'source': 'Claude'
        },
        'simmer': {
            'definition': 'Simmer is a cooking technique involving heating liquid to a temperature just below boiling point, where small bubbles occasionally break the surface but the liquid doesn\'t reach a full rolling boil. This gentle cooking method allows flavors to develop slowly while preventing delicate ingredients from breaking apart or becoming tough. Simmering typically occurs between 185-205°F (85-96°C), making it ideal for soups, stews, sauces, and braised dishes. The term also has metaphorical uses, describing emotions or tensions that are barely contained, as in "simmering anger" or "simmering conflict." The controlled heat of simmering allows for gradual cooking that tenderizes tough cuts of meat and allows spices and herbs to infuse throughout the dish.',
            'pronunciation': '/ˈsɪmər/',
            'example_sentence': 'The chef let the tomato sauce _____ for two hours to concentrate the flavors and achieve the perfect consistency.',
            'etymology': 'From Middle English "simeren," possibly from Middle Dutch "simeren" meaning "to simmer" or "to glimmer."',
            'mnemonic': 'Think "SIM-MER = Slight heat, In Moderation, Makes Everything Right" - gentle cooking below boiling.',
            'source': 'Claude'
        },
        'simpatico': {
            'definition': 'Simpatico describes a relationship or interaction characterized by mutual understanding, harmony, and natural compatibility between people who share similar attitudes, interests, or temperaments. The term suggests an effortless connection where individuals feel comfortable and in sync with each other, often without need for extensive explanation or adjustment. Simpatico relationships involve genuine liking, emotional resonance, and the sense that personalities complement each other well. The word implies more than mere politeness or tolerance, indicating authentic affinity and the pleasure of compatible company. Such relationships often develop quickly when people discover shared values, humor, or perspectives that create immediate rapport.',
            'pronunciation': '/ˌsɪmpəˈtiko/',
            'example_sentence': 'The business partners found they were completely _____, sharing the same vision and working style from their first meeting.',
            'etymology': 'From Italian and Spanish "simpatico," meaning "likeable" or "agreeable," from Greek "sympathetikos" (sympathetic).',
            'mnemonic': 'Think "SIM-PATICO = SIMilarly-minded, Perfectly Agreeable, Together In Compatible Outlook" - naturally harmonious relationship.',
            'source': 'Claude'
        },
        'simple': {
            'definition': 'Simple describes something that is easy to understand, do, or use, lacking complexity, elaboration, or unnecessary complications. The concept applies across many domains: simple explanations are clear and straightforward, simple designs are uncluttered and functional, and simple living emphasizes basic needs over luxury. Simplicity often represents elegance and efficiency, as in mathematical proofs or technological solutions that achieve maximum effect with minimum means. The term can also describe people who are honest, unpretentious, or lacking in sophistication. In various contexts, simple implies accessibility, clarity, and the absence of confusing or extraneous elements that might obscure understanding or function.',
            'pronunciation': '/ˈsɪmpəl/',
            'example_sentence': 'The recipe was so _____ that even beginning cooks could prepare the dish successfully on their first attempt.',
            'etymology': 'From Old French "simple," from Latin "simplex" meaning "single" or "unmixed," from "sim-" (one) + "plicare" (to fold).',
            'mnemonic': 'Think "SIM-PLE = Straightforward, Intelligible, Made for People Learning Easily" - easy to understand or do.',
            'source': 'Claude'
        },
        'simplicity': {
            'definition': 'Simplicity is the quality or condition of being simple, characterized by the absence of complexity, pretense, or unnecessary ornamentation. This concept values clarity, directness, and the essential elements needed to achieve a purpose without extraneous additions. In design, simplicity emphasizes clean lines, minimal elements, and intuitive functionality. In lifestyle, simplicity might involve reducing possessions, focusing on basic needs, and avoiding complications. Intellectual simplicity involves presenting ideas clearly and accessibly. The pursuit of simplicity often requires sophisticated understanding to distill complex concepts into their most essential forms. Simplicity is frequently associated with elegance, effectiveness, and peace of mind.',
            'pronunciation': '/sɪmˈplɪsəti/',
            'example_sentence': 'The architect\'s design philosophy emphasized _____, creating buildings that were both beautiful and highly functional.',
            'etymology': 'From Old French "simplicité," from Latin "simplicitas," from "simplex" meaning "simple" or "unmixed."',
            'mnemonic': 'Think "SIMPLIC-ITY = SIMPLe, Intelligent, Clear arrangements, and ITalian-style minimalism" - the quality of being simple.',
            'source': 'Claude'
        },
        'simulacrum': {
            'definition': 'A simulacrum is a representation, image, or simulation of something that may not accurately reflect the original or may exist without any real original at all. In philosophy and critical theory, particularly in the work of Jean Baudrillard, simulacra represent copies that have become disconnected from their supposed reality, sometimes replacing the original in people\'s understanding. The concept explores how media, technology, and culture create representations that shape perception more than actual reality does. Simulacra can range from realistic portraits and maps to virtual environments and media representations that take on lives of their own. The term raises questions about authenticity, representation, and the relationship between appearance and reality.',
            'pronunciation': '/ˌsɪmjəˈlækrəm/',
            'example_sentence': 'The theme park created a _____ of an ancient civilization that was more vivid and "real" to visitors than actual historical sites.',
            'etymology': 'From Latin "simulacrum," meaning "likeness" or "image," from "simulare" (to imitate or represent).',
            'mnemonic': 'Think "SIMUL-ACRUM = SIMULated thing ACting as Real but Ultimately Mock" - a copy that replaces the original.',
            'source': 'Claude'
        },
        'simultaneity': {
            'definition': 'Simultaneity refers to the occurrence of two or more events at exactly the same time, or the quality of existing or happening concurrently. This concept becomes particularly complex in physics, where Einstein\'s theory of relativity demonstrates that simultaneity is relative to the observer\'s frame of reference - events that appear simultaneous to one observer may not be simultaneous to another moving at different speeds. In everyday experience, simultaneity describes coordinated actions, coincidental events, or the challenge of managing multiple tasks at once. The concept is crucial in various fields including music (simultaneous notes creating harmony), theater (actors performing together), and technology (parallel processing in computers).',
            'pronunciation': '/ˌsaɪməlˈteɪniəti/',
            'example_sentence': 'The orchestra conductor achieved perfect _____ among all the musicians, creating a harmonious and unified performance.',
            'etymology': 'From Medieval Latin "simultaneitas," from "simul" meaning "at the same time" + "-taneous" (relating to time).',
            'mnemonic': 'Think "SIMUL-TANE-ITY = Same time occurring, Including Many Unique things, Linked Together ANd Even-timed" - happening at exactly the same time.',
            'source': 'Claude'
        },
        'simultaneously': {
            'definition': 'Simultaneously means occurring, existing, or operating at exactly the same time as something else, without any temporal gap or sequence. This adverb describes the precise coordination of multiple actions, events, or processes that happen in perfect synchronization. Examples include musicians playing simultaneously in an orchestra, multiple computer processes running simultaneously, or simultaneous translation during international conferences. The word emphasizes the concurrent nature of activities rather than sequential occurrence. In complex systems, simultaneous operations often require careful coordination to avoid conflicts or interference, while in other contexts, simultaneous events may be coincidental rather than deliberately coordinated.',
            'pronunciation': '/ˌsaɪməlˈteɪniəsli/',
            'example_sentence': 'The fireworks display required all the pyrotechnicians to light their charges _____ for maximum visual impact.',
            'etymology': 'From "simultaneous" + "-ly," where simultaneous comes from Medieval Latin "simultaneus" meaning "at the same time."',
            'mnemonic': 'Think "SIMUL-TANEOUS-LY = Same time occurring, Including Many things, Utterly Linked Together, ANd Everything Operating UnifiedlY" - at exactly the same time.',
            'source': 'Claude'
        },
        'sinai': {
            'definition': 'Sinai refers to the triangular peninsula in northeastern Egypt between the Mediterranean Sea and the Red Sea, historically and religiously significant as the location where Moses received the Ten Commandments according to biblical tradition. Mount Sinai (also called Mount Horeb) within this region is considered one of the most sacred sites in Judaism, Christianity, and Islam. The peninsula has been strategically important throughout history due to its position connecting Africa and Asia. Modern Sinai includes popular Red Sea resort destinations, Bedouin communities, and Saint Catherine\'s Monastery, one of the world\'s oldest Christian monasteries. The region has also been the site of various military conflicts and remains geopolitically significant.',
            'pronunciation': '/ˈsaɪˌnaɪ/',
            'example_sentence': 'Pilgrims from around the world journey to Mount _____ to visit the site where Moses is believed to have received the commandments.',
            'etymology': 'From Hebrew "Sinai," possibly from the Semitic root related to "bush" or from the moon god Sin worshipped in the region.',
            'mnemonic': 'Think "SIN-AI = Sacred place where SINs were Addressed through divine Instructions" - the holy mountain of biblical law.',
            'source': 'Claude'
        },
        'since': {
            'definition': 'Since functions as both a preposition and conjunction indicating a point in time from which something began and continues to the present, or establishing a causal relationship between events. As a temporal marker, "since" connects past events to current situations, as in "since yesterday" or "since childhood." As a causal conjunction, it introduces reasons or explanations, similar to "because" or "given that." The word establishes continuity and connection across time periods or logical relationships. In everyday usage, "since" helps speakers and writers create coherent narratives by linking past circumstances to present conditions or explaining why certain situations exist.',
            'pronunciation': '/sɪns/',
            'example_sentence': '_____ the weather has been so pleasant, we decided to have our meeting outside in the garden.',
            'etymology': 'From Middle English "sins," from Old English "siððan" meaning "after that" or "from then till now."',
            'mnemonic': 'Think "SIN-CE = Starting IN time, Continuing Even now" - from a past time until now.',
            'source': 'Claude'
        },
        'sinciput': {
            'definition': 'The sinciput is the upper and front part of the head or skull, specifically the region above the forehead extending back to the crown. In anatomical terms, it represents the anterosuperior portion of the cranium, distinguished from the occiput (back of the head). This area includes parts of the frontal and parietal bones that form the dome-like structure protecting the brain\'s frontal and parietal lobes. The sinciput is important in medical contexts for describing head injuries, measurements, and developmental assessments. In obstetrics, fetal position during birth is sometimes described in relation to sinciput and occiput orientation. The term is primarily used in medical, anatomical, and anthropological contexts.',
            'pronunciation': '/ˈsɪnsɪˌpʌt/',
            'example_sentence': 'The anatomist pointed out the _____ region when explaining the different parts of the human skull to medical students.',
            'etymology': 'From Latin "sinciput," from "semi-" (half) + "caput" (head), literally meaning "half a head" or "front part of the head."',
            'mnemonic': 'Think "SIN-CIPUT = front SectIoN of head, where Crown Is Present, Under forehead Top" - the front upper part of the head.',
            'source': 'Claude'
        },
        'singapore': {
            'definition': 'Singapore is a sovereign city-state and island nation in Southeast Asia, located at the southern tip of the Malay Peninsula between Malaysia and Indonesia. Known for its strategic port, multicultural society, and economic prosperity, Singapore serves as a major financial and trading hub connecting East and West. The nation consists of the main island and several smaller islands, with a highly developed urban environment characterized by efficient infrastructure, strict laws, and cultural diversity. Singapore\'s success story involves transformation from a developing nation to one of the world\'s wealthiest countries through strategic planning, education, and international trade. The country is famous for its cleanliness, safety, food culture, and distinctive architecture blending modern and traditional elements.',
            'pronunciation': '/ˈsɪŋɡəˌpɔr/',
            'example_sentence': 'The business conference in _____ attracted delegates from across Asia to discuss international trade opportunities.',
            'etymology': 'From Sanskrit "Singapura," meaning "lion city," from "simha" (lion) + "pura" (city), though lions were not native to the region.',
            'mnemonic': 'Think "SING-A-PORE = Successful city where International merchants SING A song of PORt prosperity and success" - the prosperous lion city.',
            'source': 'Claude'
        },
        'singing': {
            'definition': 'Singing is the act of producing musical sounds with the voice through controlled pitch, rhythm, and tone, typically involving words set to melody. This fundamental form of musical expression utilizes the vocal cords, breath support, and resonance within the body to create organized sound patterns. Singing can range from simple humming and folk songs to complex operatic performances requiring years of training. The activity serves multiple purposes: artistic expression, entertainment, religious worship, cultural tradition, and emotional release. Different singing styles exist across cultures and musical genres, each with unique techniques, vocal qualities, and aesthetic goals. Singing also provides physical and psychological benefits, including improved breathing, stress relief, and social connection.',
            'pronunciation': '/ˈsɪŋɪŋ/',
            'example_sentence': 'The children\'s choir spent months practicing their _____ technique before the holiday concert performance.',
            'etymology': 'From Old English "singan," related to German "singen," from a Germanic root meaning "to make music with the voice."',
            'mnemonic': 'Think "SING-ING = Sound IN melodic Groups, Including Notes and Graceful vocal expression" - making music with the voice.',
            'source': 'Claude'
        },
        'single': {
            'definition': 'Single describes something that is one only, individual, or separate from others, existing alone or without a partner, pair, or group. The term applies across many contexts: single people are unmarried, single items are sold individually, and single actions happen once. In music, a single is a recording featuring one main song. Single also means undivided or whole, as in "single focus" or "single purpose." The word can indicate simplicity or isolation depending on context. In sports, a single might refer to a one-base hit in baseball or an individual player competition. The concept emphasizes unity, individuality, or the absence of multiplicity.',
            'pronunciation': '/ˈsɪŋɡəl/',
            'example_sentence': 'She preferred to buy a _____ rose rather than an entire bouquet for the small occasion.',
            'etymology': 'From Old French "sengle," from Latin "singulus" meaning "one by one" or "individual."',
            'mnemonic': 'Think "SING-LE = Solitary, Individual, Not with Groups, Living Exclusively alone" - one only, not paired.',
            'source': 'Claude'
        },
        'singultus': {
            'definition': 'Singultus is the medical term for hiccups, describing the involuntary spasmodic contraction of the diaphragm followed by rapid closure of the vocal cords, producing the characteristic "hic" sound. This reflex action occurs when the phrenic nerve, which controls the diaphragm, becomes irritated or stimulated inappropriately. Common causes include eating too quickly, consuming carbonated beverages, sudden temperature changes, or excitement. While usually harmless and self-limiting, persistent singultus lasting more than 48 hours may indicate underlying medical conditions affecting the nervous system, metabolism, or drug reactions. Various remedies exist, from holding breath and drinking water to medical interventions for severe cases.',
            'pronunciation': '/sɪŋˈɡʌltəs/',
            'example_sentence': 'The patient\'s persistent _____ lasted for three days, prompting the doctor to investigate potential underlying causes.',
            'etymology': 'From Latin "singultus," meaning "sobbing" or "hiccup," from "singultire" (to sob or catch one\'s breath).',
            'mnemonic': 'Think "SING-ULTUS = Sound INcluding sharp Gasps, Uncontrollable spasms Through diaphragm muscle" - the medical term for hiccups.',
            'source': 'Claude'
        },
        'sinister': {
            'definition': 'Sinister describes something threatening, ominous, or suggesting evil intent, often creating an atmosphere of foreboding or danger. The word characterizes people, situations, or objects that seem menacing or harboring harmful purposes, though the threat may be subtle rather than obvious. Sinister elements in stories create tension and unease, while sinister characters often possess hidden malevolent motives. In heraldry, sinister refers to the left side of a coat of arms from the bearer\'s perspective. The term has evolved from its original meaning of "left-handed" to its current association with evil or threat, reflecting historical cultural biases against left-handedness that equated it with wrongness or bad luck.',
            'pronunciation': '/ˈsɪnəstər/',
            'example_sentence': 'The abandoned mansion had a _____ appearance that made even brave visitors hesitate before entering.',
            'etymology': 'From Latin "sinister" meaning "left" or "on the left side," which came to mean "unlucky" or "evil" due to cultural superstitions.',
            'mnemonic': 'Think "SIN-ISTER = Something IN dark places, suggesting danger, Including Some Threatening Evil elements" - threatening or evil.',
            'source': 'Claude'
        },
        'sink': {
            'definition': 'Sink has multiple related meanings: as a noun, it refers to a basin with faucets and drainage used for washing, typically found in kitchens and bathrooms. As a verb, sink means to descend below the surface of water or other fluid, to fall or drop to a lower level, or to decline in value, quality, or condition. The word also describes the gradual penetration or absorption of something, as in "sink into thought" or "let the news sink in." In environmental science, a carbon sink is something that absorbs more carbon than it releases. The concept generally involves downward movement, absorption, or receptacles designed to collect and drain liquids.',
            'pronunciation': '/sɪŋk/',
            'example_sentence': 'The kitchen _____ was full of dirty dishes that needed to be washed before dinner.',
            'etymology': 'From Old English "sincan," meaning "to sink" or "to fall," related to German "sinken."',
            'mnemonic': 'Think "SINK = Something that INtakes Kitchen water" (noun) or "Submerging IN liquids, going down" (verb) - basin or going down.',
            'source': 'Claude'
        }
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            words = list(reader)
        
        print(f"Processing {len(words)} words from batch 160...")
        
        processed_data = []
        combined_errors = []
        
        for i, row in enumerate(words, 1):
            word = row['word'].strip()
            print(f"Processing word {i}: {word}")
            
            if word in word_data:
                data = word_data[word]
                
                # Check for combined word errors
                is_combined_error = '[COMBINED WORD ERROR]' in data['definition']
                if is_combined_error:
                    combined_errors.append(word)
                
                # Calculate difficulty scores
                phonetic_score = calculator.calculate_phonetic_transparency(word)
                frequency_score = calculator.calculate_word_frequency(word)
                morphological_score = calculator.calculate_morphological_complexity(word)
                etymology_score = calculator.calculate_etymology_complexity(word)
                
                processed_row = {
                    'word': word,
                    'definition': data['definition'],
                    'pronunciation': data['pronunciation'],
                    'example_sentence': data['example_sentence'],
                    'etymology': data['etymology'],
                    'mnemonic': data['mnemonic'],
                    'phonetic_transparency_score': phonetic_score,
                    'word_frequency_score': frequency_score,
                    'morphological_complexity_score': morphological_score,
                    'etymology_complexity_score': etymology_score,
                    'average_difficulty_score': round((phonetic_score + frequency_score + morphological_score + etymology_score) / 4, 2),
                    'source_years': row['years'],
                    'source_files': row['source_files'], 
                    'source_difficulties': row['source_difficulties'],
                    'definition_source': data['source'],
                    'pronunciation_source': data['source'],
                    'example_sentence_source': data['source'],
                    'etymology_source': data['source'],
                    'mnemonic_source': data['source'],
                    'final_difficulty_level': None,
                    'review_status': 'auto_processed',
                    'notes': 'Combined word error detected and flagged' if is_combined_error else 'Processed successfully'
                }
                
                processed_data.append(processed_row)
            else:
                print(f"Warning: No data found for word '{word}'")
        
        # Write to CSV
        if processed_data:
            fieldnames = [
                'word', 'definition', 'pronunciation', 'example_sentence', 'etymology', 'mnemonic',
                'phonetic_transparency_score', 'word_frequency_score', 'morphological_complexity_score', 'etymology_complexity_score', 'average_difficulty_score',
                'source_years', 'source_files', 'source_difficulties',
                'definition_source', 'pronunciation_source', 'example_sentence_source', 'etymology_source', 'mnemonic_source',
                'final_difficulty_level', 'review_status', 'notes'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_data)
        
        print(f"\nBatch 160 processing complete!")
        print(f"Successfully processed {len(processed_data)}/{len(words)} words")
        print(f"Output saved to: {output_file}")
        
        if combined_errors:
            print(f"\nCombined word errors detected: {len(combined_errors)}")
            for error in combined_errors:
                print(f"  - {error}")
        
    except Exception as e:
        print(f"Error processing batch 160: {str(e)}")
        raise

if __name__ == "__main__":
    main()