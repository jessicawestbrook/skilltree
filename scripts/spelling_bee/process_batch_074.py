import pandas as pd
from typing import Dict
from dataclasses import dataclass

@dataclass
class WordData:
    definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    language_origins: str = ""
    example_sentence: str = ""
    memory_tip: str = ""
    phonetic_complexity: float = 0.0
    frequency_complexity: float = 0.0
    morphological_complexity: float = 0.0
    etymological_complexity: float = 0.0

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_complexity(word: str) -> float:
        score = 0.0
        silent_letters = ['gh', 'kn', 'mb', 'mn', 'ps', 'pt', 'rh']
        unusual_combos = ['eau', 'ough', 'augh', 'ious', 'eous', 'sce', 'sci']
        
        for combo in silent_letters:
            if combo in word.lower():
                score += 0.3
                
        for combo in unusual_combos:
            if combo in word.lower():
                score += 0.2
                
        double_letters = len([i for i in range(len(word)-1) if word[i] == word[i+1]])
        score += double_letters * 0.1
        
        return min(score, 1.0)
    
    @staticmethod 
    def estimate_frequency(word: str) -> float:
        common_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it'}
        if word.lower() in common_words:
            return 0.1
        elif len(word) <= 4:
            return 0.3
        elif len(word) <= 7:
            return 0.5
        else:
            return 0.8
    
    @staticmethod
    def calculate_morphological_complexity(word: str) -> float:
        prefixes = ['un', 're', 'pre', 'dis', 'over', 'under', 'out', 'up', 'mis', 'sub', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'non']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'eous', 'ious']
        
        morphemes = 1
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                morphemes += 1
                break
                
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                morphemes += 1
                break
                
        return min((morphemes - 1) * 0.3, 1.0)
    
    @staticmethod
    def calculate_etymological_complexity(etymology: str, language_origins: str) -> float:
        if not etymology or not language_origins:
            return 0.5
            
        complex_origins = ['Greek', 'Latin', 'Sanskrit', 'Hebrew', 'Arabic']
        simple_origins = ['English', 'Germanic', 'Old English']
        
        score = 0.5
        for origin in complex_origins:
            if origin.lower() in language_origins.lower():
                score += 0.2
                
        for origin in simple_origins:
            if origin.lower() in language_origins.lower():
                score -= 0.1
                
        return max(0.0, min(score, 1.0))

class Batch074Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for a word using Claude knowledge"""
        
        batch_074_data = {
            'galahad': {
                'definition': 'Galahad refers to Sir Galahad, the legendary knight in Arthurian romance who was known for his purity, nobility, and spiritual perfection. As the most virtuous of the Knights of the Round Table, Galahad was the only knight deemed pure enough to achieve the Holy Grail. In modern usage, calling someone a "Galahad" means describing them as chivalrous, noble, or heroically virtuous, though sometimes with ironic undertones suggesting naivety or impracticality.',
                'part_of_speech': 'proper noun, noun',
                'pronunciation_guide': 'GAL-uh-had',
                'etymology': 'From medieval romance literature, possibly derived from Welsh "Gwalchmei" or related to Hebrew "Gil\'ad" (heap of testimony), popularized in Arthurian legends.',
                'language_origins': 'Medieval Romance, possibly Welsh or Hebrew',
                'example_sentence': 'He fancied himself a _______, always rushing to help others even when his assistance wasn\'t needed.',
                'memory_tip': 'Remember "GALAHAD" - the GALant knight who HAD the purest heart and found the Holy Grail.'
            },
            'galahadgalatea': {
                'definition': 'Galahadgalatea appears to be a combined word error where "Galahad" (the Arthurian knight) and "Galatea" (the mythological figure) were incorrectly merged during PDF processing. Galahad was the pure knight who found the Holy Grail, while Galatea was the ivory statue brought to life by Aphrodite in Greek mythology. This represents a data quality issue where two distinct mythological names were improperly joined.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'GAL-uh-had-gal-uh-TEE-ah',
                'etymology': 'Corrupted combination of "Galahad" (Arthurian legend) and "Galatea" (Greek mythology).',
                'language_origins': 'Medieval Romance, Greek (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining two distinct mythological figures.',
                'memory_tip': 'This is a data error - remember that "Galahad" (knight) and "Galatea" (statue) should be separate names.'
            },
            'galapago': {
                'definition': 'Galapago is an archaic or variant term related to "Galápagos," referring to the famous islands known for their unique wildlife and Charles Darwin\'s evolutionary studies. The word originally comes from the Spanish term for giant tortoises found on these Pacific islands. In historical contexts, galapago might refer to the tortoises themselves or the islands, representing one of the world\'s most important natural laboratories for understanding evolution and biodiversity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gah-LAH-pah-goh',
                'etymology': 'From Spanish "galápago" meaning "tortoise," ultimately from a pre-Roman Iberian word for turtle or tortoise.',
                'language_origins': 'Spanish, pre-Roman Iberian',
                'example_sentence': 'The naturalist studied the unique _______ species that had evolved in isolation on the volcanic islands.',
                'memory_tip': 'Remember "GALAPAGO" - sounds like GALloping tortoises on the GaLAPagos islands where Darwin studied evolution.'
            },
            'galapagogallic': {
                'definition': 'Galapagogallic appears to be a combined word error where "Galapago" (relating to Galápagos islands/tortoises) and "gallic" (relating to France or ancient Gaul) were incorrectly merged during PDF processing. These terms represent completely different geographical and cultural references - one relating to Pacific islands and evolution, the other to French or ancient Gallic culture. This represents a data quality issue where unrelated terms were improperly joined.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'gah-LAH-pah-goh-GAL-ik',
                'etymology': 'Corrupted combination of "galapago" (Spanish for tortoise) and "gallic" (Latin relating to Gaul/France).',
                'language_origins': 'Spanish, Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining Pacific island and French cultural terminology.',
                'memory_tip': 'This is a data error - remember that "galapago" (islands/tortoises) and "gallic" (French) should be separate.'
            },
            'galatea': {
                'definition': 'Galatea refers to the ivory statue of a beautiful woman created by the sculptor Pygmalion in Greek mythology, which was brought to life by the goddess Aphrodite in response to Pygmalion\'s love for his creation. The story represents themes of art, love, and the power of desire to transform reality. The name has been used in literature and art to symbolize the transformation of art into life, or the idealization of beauty and perfection.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'gal-uh-TEE-ah',
                'etymology': 'From Greek mythology, possibly meaning "milk-white" from Greek "gala" (milk), referring to the white marble or ivory of the statue.',
                'language_origins': 'Greek',
                'example_sentence': 'The artist\'s sculpture reminded viewers of _______, the mythical statue that came to life through love.',
                'memory_tip': 'Remember "GALATEA" - the statue made of GALa (milk-white marble) that came to life, like getting a TEA with a living statue.'
            },
            'galaxy': {
                'definition': 'A galaxy is a massive collection of stars, star systems, stellar remnants, interstellar gas, dust, and dark matter bound together by gravitational forces. Our solar system is part of the Milky Way galaxy, which contains billions of stars. The universe contains countless galaxies of various sizes and shapes. Metaphorically, galaxy can refer to any large group or collection of outstanding people or things.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAL-ak-see',
                'etymology': 'From Greek "galaxias" meaning "milky," referring to the Milky Way\'s appearance as a milky band of light across the night sky.',
                'language_origins': 'Greek',
                'example_sentence': 'The Hubble telescope captured stunning images of a distant _______ containing billions of stars.',
                'memory_tip': 'Remember "GALAXY" - a huge collection of stars that looks GALa (milky) in the sky, like our Milky Way.'
            },
            'galena': {
                'definition': 'Galena is a mineral composed primarily of lead sulfide (PbS), serving as the most important ore of lead. This metallic gray mineral has a distinctive cubic crystal structure and high density. Galena has been used since ancient times for extracting lead and was historically important in the development of radio technology, as galena crystals were used in early crystal radio receivers as detectors.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'guh-LEE-nuh',
                'etymology': 'From Latin "galena" meaning "lead ore," possibly from Greek "galene" (calmness) due to the mineral\'s smooth, calm appearance.',
                'language_origins': 'Latin, possibly Greek',
                'example_sentence': 'The miners extracted _______ from the deposit to process into pure lead for industrial use.',
                'memory_tip': 'Remember "GALENA" - the GALient (brave) mineral that LEads to lead production, the main lead ore.'
            },
            'gallant': {
                'definition': 'Gallant describes someone who is brave, noble, and chivalrous, especially in the face of danger or when showing courtesy to others. The word emphasizes courage combined with courteous behavior, particularly toward women or those in need of protection. Gallant can also describe actions, efforts, or attempts that show courage and determination, even if unsuccessful. The term suggests both physical bravery and moral elegance.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'GAL-ant or guh-LANT',
                'etymology': 'From Old French "galant" meaning "courtly, elegant," originally from "galer" (to rejoice, make merry).',
                'language_origins': 'Old French',
                'example_sentence': 'The _______ knight rode forth to defend the village from the attacking bandits.',
                'memory_tip': 'Remember "GALLANT" - someone GALloping to help others, brave and noble like a knight on horseback.'
            },
            'galley': {
                'definition': 'A galley has several meanings: historically, it was a low, flat ship propelled by oars and sometimes sails, used in ancient and medieval warfare and trade. In printing, a galley is a metal tray for holding composed type before it\'s arranged into pages. In modern usage, galley most commonly refers to a ship\'s kitchen or the compact kitchen area in an aircraft, train, or small living space.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAL-ee',
                'etymology': 'From Old French "galie," ultimately from Byzantine Greek "galea" (galley ship), possibly related to "galeos" (shark) due to the ship\'s sleek shape.',
                'language_origins': 'Old French, Byzantine Greek',
                'example_sentence': 'The flight attendant prepared meals in the aircraft\'s compact _______.',
                'memory_tip': 'Remember "GALLEY" - where you GALlop to get food, whether on a ship\'s kitchen or airplane kitchen.'
            },
            'gallic': {
                'definition': 'Gallic means relating to ancient Gaul (roughly modern France and surrounding areas) or its Celtic inhabitants, or more broadly, relating to France and French culture. The term can describe characteristics, customs, or attitudes considered typically French. In historical contexts, Gallic refers specifically to the Celtic tribes that inhabited Gaul before Roman conquest. The word often carries connotations of French cultural distinctiveness or national character.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GAL-ik',
                'etymology': 'From Latin "Gallicus" meaning "of or relating to Gaul," from "Gallia" (Gaul, ancient name for France).',
                'language_origins': 'Latin',
                'example_sentence': 'His _______ sense of style was evident in his elegant clothing and sophisticated mannerisms.',
                'memory_tip': 'Remember "GALLIC" - relating to ancient GAuL and modern French culture, like Gallic roosters representing France.'
            },
            'gallipot': {
                'definition': 'A gallipot is a small glazed earthenware jar or pot, traditionally used by apothecaries and pharmacists to store medicines, ointments, and other pharmaceutical preparations. These containers were typically cylindrical with wide mouths and were often labeled with the contents. Gallipots were essential equipment in historical pharmacies and medical practices, representing the careful storage and dispensing of medicinal compounds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAL-ih-pot',
                'etymology': 'Possibly from "galley pot," referring to pots imported by galley ships, or from Dutch "gleypot" (glazed pot).',
                'language_origins': 'English, possibly Dutch',
                'example_sentence': 'The old apothecary shop was lined with _______ containers holding various herbal remedies.',
                'memory_tip': 'Remember "GALLIPOT" - a small pot that GALleys (ships) brought to pharmacies, or a GLAzed pot for medicine.'
            },
            'gallium': {
                'definition': 'Gallium is a soft, silvery metallic chemical element with symbol Ga and atomic number 31. It has the unusual property of melting at just above room temperature (about 30°C or 86°F), so it can melt in your hand. Gallium is used in semiconductors, LED lights, solar panels, and various electronic applications. It\'s also notable for expanding when it solidifies, unlike most metals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAL-ee-um',
                'etymology': 'Named after Gallia (Latin name for France) by its discoverer, French chemist Paul-Émile Lecoq de Boisbaudran, in 1875.',
                'language_origins': 'Modern Latin (named after France)',
                'example_sentence': 'The _______ metal melted in the scientist\'s warm hand, demonstrating its low melting point.',
                'memory_tip': 'Remember "GALLIUM" - the metal from GALlia (France) that melts so easily it seems to GALlop away in your hand.'
            },
            'gallivat': {
                'definition': 'A gallivat is a type of small, fast sailing vessel that was common in the Indian Ocean, particularly around the coasts of India and the Arabian Peninsula. These boats were typically used for coastal trading, fishing, and sometimes piracy. Gallivats were known for their speed and maneuverability, making them popular among both merchants and naval forces in the region during the colonial period.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAL-ih-vat',
                'etymology': 'From Portuguese "galeota" (small galley), adapted into English through maritime contact in the Indian Ocean region.',
                'language_origins': 'Portuguese',
                'example_sentence': 'The merchant\'s _______ quickly navigated through the shallow coastal waters of the Arabian Sea.',
                'memory_tip': 'Remember "GALLIVAT" - a boat that GALlivants (roams) around the Indian Ocean, fast and nimble.'
            },
            'gallivatcharcuterie': {
                'definition': 'Gallivatcharcuterie appears to be a combined word error where "gallivat" (a type of sailing vessel) and "charcuterie" (prepared meat products) were incorrectly merged during PDF processing. These are completely unrelated terms - one referring to maritime vessels and the other to culinary arts. This represents a data quality issue where nautical and culinary terminology were improperly joined together.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'GAL-ih-vat-shar-KOO-ter-ee',
                'etymology': 'Corrupted combination of "gallivat" (Portuguese maritime term) and "charcuterie" (French culinary term).',
                'language_origins': 'Portuguese, French (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining sailing vessel and meat preparation terminology.',
                'memory_tip': 'This is a data error - remember that "gallivat" (boat) and "charcuterie" (meat preparation) should be separate.'
            },
            'gallon': {
                'definition': 'A gallon is a unit of measurement for liquid capacity, though the exact volume differs between countries. In the United States, a gallon equals 3.785 liters or 128 fluid ounces, while in the UK, an imperial gallon equals 4.546 liters. Gallons are commonly used to measure fuel, milk, water, and other liquids. The unit provides a practical way to quantify larger volumes of liquid for commercial and everyday use.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAL-un',
                'etymology': 'From Old French "galon," ultimately from a Gaulish word meaning "container," related to measuring vessels.',
                'language_origins': 'Old French, Gaulish',
                'example_sentence': 'The car\'s fuel tank holds fifteen _______ of gasoline.',
                'memory_tip': 'Remember "GALLON" - a GAL carrying a LONg container of liquid, a large unit for measuring fluids.'
            },
            'gallop': {
                'definition': 'Gallop is the fastest gait of a horse, characterized by a three-beat rhythm where all four hooves leave the ground simultaneously during each stride. As a verb, gallop means to move at this rapid pace, or more generally, to move very quickly. The word can also describe rapid progress or development in non-physical contexts, suggesting speed, urgency, or energetic forward motion.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GAL-up',
                'etymology': 'From Old French "galoper," possibly from Frankish "*wala hlaupan" (to run well) or related to "galop" (a dance).',
                'language_origins': 'Old French, possibly Frankish',
                'example_sentence': 'The horse began to _______ across the open meadow, its hooves thundering on the ground.',
                'memory_tip': 'Remember "GALLOP" - when a horse GALs (runs) and hOP-s forward at maximum speed.'
            },
            'galoot': {
                'definition': 'A galoot is an awkward, ungainly, or foolish person, often used affectionately or humorously rather than as a serious insult. The term typically describes someone who is clumsy, unsophisticated, or bumbling in their actions or demeanor. Galoot suggests someone who is well-meaning but lacks grace, skill, or social polish, often used in informal American speech with a tone of gentle mockery or fond exasperation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'guh-LOOT',
                'etymology': 'Origin uncertain, possibly from nautical slang, first recorded in American English in the 1860s, possibly related to "galoot" meaning soldier or sailor.',
                'language_origins': 'American English (uncertain origin)',
                'example_sentence': 'That loveable _______ knocked over three displays while trying to help organize the store.',
                'memory_tip': 'Remember "GALOOT" - an awkward person who GALs (moves clumsily) and acts like a LOOT-er who bumps into things.'
            },
            'galvanize': {
                'definition': 'Galvanize means to stimulate someone into action through shock, excitement, or urgency, or technically, to coat metal with zinc to prevent corrosion. In the metaphorical sense, galvanize describes spurring people to act decisively, often in response to a crisis or inspiring event. The technical meaning involves the electrochemical process of applying a protective zinc coating to steel or iron to prevent rust and corrosion.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'GAL-vuh-nyz',
                'etymology': 'Named after Luigi Galvani (1737-1798), Italian scientist who studied bioelectricity, with the suffix "-ize" meaning to cause or make.',
                'language_origins': 'Modern English (named after Italian scientist)',
                'example_sentence': 'The inspiring speech served to _______ the volunteers into immediate action.',
                'memory_tip': 'Remember "GALVANIZE" - to shock people into action like GALvani\'s electrical experiments, energizing them to move.'
            },
            'gambit': {
                'definition': 'A gambit is a calculated move or strategy, especially an opening move that involves some sacrifice or risk to gain an advantage later. Originally from chess, where a gambit involves sacrificing a piece (usually a pawn) early in the game for positional advantage, the term now applies to any strategic maneuver in business, politics, or life that involves initial risk for potential future gain.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAM-bit',
                'etymology': 'From Italian "gambetto" meaning "a trip, a wrestling hold," from "gamba" (leg), referring to tripping someone up as a strategic move.',
                'language_origins': 'Italian',
                'example_sentence': 'His opening _______ in the negotiation was to offer a lower salary but include attractive benefits.',
                'memory_tip': 'Remember "GAMBIT" - a GAMe strategy where you BIT off more than you can chew, risking something for advantage.'
            },
            'gambol': {
                'definition': 'Gambol means to run, jump, or skip about playfully, expressing joy and high spirits through energetic, carefree movement. The word typically describes the playful behavior of young animals like lambs, foals, or puppies, but can also apply to humans engaged in joyful, spontaneous physical activity. Gambol emphasizes the innocent, exuberant nature of such playful movement.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GAM-bul',
                'etymology': 'From French "gambader" meaning "to leap, bound," from Italian "gamba" (leg), related to the movement of legs in playful jumping.',
                'language_origins': 'French, Italian',
                'example_sentence': 'The spring lambs began to _______ joyfully across the green pasture.',
                'memory_tip': 'Remember "GAMBOL" - animals GAMing and BOuncing with their legs, playing joyfully like in a gambling game of fun.'
            },
            'game': {
                'definition': 'Game has multiple meanings: an activity with rules played for entertainment or competition; wild animals hunted for sport or food; a person\'s level of skill or performance in a particular area; or willingness to participate or take risks. As an adjective, game means willing, ready, or eager to do something. The word emphasizes structured activity, competition, skill, or adventurous spirit.',
                'part_of_speech': 'noun, adjective, verb',
                'pronunciation_guide': 'GAYM',
                'etymology': 'From Old English "gamen" meaning "joy, fun, amusement," related to German "Spiel" and ultimately from a root meaning "to leap joyfully."',
                'language_origins': 'Old English',
                'example_sentence': 'Are you _______ for trying the new adventure sport this weekend?',
                'memory_tip': 'Remember "GAME" - an activity that brings joy and GAins fun, whether playing or hunting.'
            },
            'games': {
                'definition': 'Games is the plural of game, referring to multiple organized activities with rules designed for entertainment, education, or competition. This can include sports competitions, board games, video games, or Olympic Games. Games represent structured play that often involves strategy, skill, luck, or physical ability. The word encompasses both casual recreational activities and serious competitive events.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GAYMZ',
                'etymology': 'Plural of "game," from Old English "gamen" meaning "amusement, sport."',
                'language_origins': 'Old English',
                'example_sentence': 'The children played various _______ during the rainy afternoon indoors.',
                'memory_tip': 'Remember "GAMES" - multiple GAMEs that bring amusement, whether sports, puzzles, or competitions.'
            },
            'gamma': {
                'definition': 'Gamma is the third letter of the Greek alphabet (Γ, γ), used in mathematics, science, and engineering to represent various concepts including gamma rays (high-energy electromagnetic radiation), the gamma function in mathematics, or color correction values in photography and displays. In finance, gamma measures the rate of change of an option\'s delta. The letter appears frequently in scientific notation and Greek organizations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAM-ah',
                'etymology': 'From Greek "gamma" (Γ), the third letter of the Greek alphabet, ultimately from Phoenician "gimel" (camel).',
                'language_origins': 'Greek',
                'example_sentence': 'The physicist studied _______ radiation emitted by the radioactive material.',
                'memory_tip': 'Remember "GAMMA" - the Greek letter that\'s GAMing in science, used for radiation and mathematical functions.'
            },
            'ganache': {
                'definition': 'Ganache is a smooth, rich mixture of chocolate and cream used as a filling, frosting, or glaze for pastries, cakes, and confections. This French culinary preparation can be made with different ratios of chocolate to cream to achieve various consistencies, from pourable glazes to firm truffle centers. Ganache is fundamental in professional pastry making and fine chocolate work.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'guh-NAHSH',
                'etymology': 'From French "ganache," originally meaning "jaw" or "jowl," possibly referring to the smooth, rich texture resembling something smooth and soft.',
                'language_origins': 'French',
                'example_sentence': 'The pastry chef prepared a silky chocolate _______ to fill the elegant truffles.',
                'memory_tip': 'Remember "GANACHE" - GANa (rich) chocolate that\'s so smooth it melts in your CHEeks like cream.'
            },
            'gander': {
                'definition': 'A gander is a male goose, the counterpart to the female goose. In informal usage, "take a gander" means to look at something, to have a look or glance. The word can also refer to a foolish or simple-minded person, though this usage is less common. The term emphasizes both the specific male waterfowl and the act of stretching one\'s neck to look, like a goose might do.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GAN-der',
                'etymology': 'From Old English "gandra" meaning "male goose," related to "goos" (goose) and the masculine suffix "-er."',
                'language_origins': 'Old English',
                'example_sentence': 'The farmer watched the _______ protectively guard his flock of geese.',
                'memory_tip': 'Remember "GANDER" - a male goose who GANders (looks around) to guard his flock, or when you take a gander (look).'
            },
            'gandhasri': {
                'definition': 'Gandhasri appears to be a Sanskrit-derived term, possibly referring to a fragrant or aromatic substance, plant, or goddess, as "gandha" means "fragrance" or "smell" in Sanskrit, and "sri" often indicates prosperity, beauty, or respect. This term might appear in contexts related to Indian culture, Ayurveda, or spiritual practices. The specific meaning would depend on the particular cultural or religious context in which it is used.',
                'part_of_speech': 'noun (Sanskrit-derived)',
                'pronunciation_guide': 'gan-DAH-shree',
                'etymology': 'From Sanskrit, combining "gandha" (fragrance, smell) and "sri" (prosperity, beauty, respect).',
                'language_origins': 'Sanskrit',
                'example_sentence': 'The ancient text described _______ as a sacred aromatic offering used in temple ceremonies.',
                'memory_tip': 'Remember "GANDHASRI" - GANDHA (fragrance) that brings SRI (prosperity), a beautiful aromatic blessing.'
            },
            'ganges': {
                'definition': 'Ganges refers to the sacred river in India and Bangladesh, known in Hindi as Ganga, which flows from the Himalayas to the Bay of Bengal. This river is considered sacred in Hinduism and is central to Indian culture, religion, and daily life. The Ganges supports hundreds of millions of people and is both a vital water resource and a spiritual symbol representing purity, life, and divine blessing.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GAN-jeez',
                'etymology': 'From Sanskrit "Ganga," the name of the river goddess in Hindu mythology, possibly from a root meaning "swift-moving."',
                'language_origins': 'Sanskrit',
                'example_sentence': 'Millions of pilgrims travel to bathe in the sacred waters of the _______ River.',
                'memory_tip': 'Remember "GANGES" - the GAN(ga) river where people GAther for spiritual blessings, India\'s holy waterway.'
            },
            'gannet': {
                'definition': 'A gannet is a large seabird known for its spectacular diving behavior, plunging into the ocean from great heights to catch fish. These birds have long wings, streamlined bodies, and pointed bills adapted for diving and fishing. Gannets are found in coastal areas and are known for their impressive aerial abilities and distinctive white plumage with yellowish head coloring in adults.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAN-it',
                'etymology': 'From Old English "ganot," related to Dutch "gent" and German "Gans" (goose), though gannets are not closely related to geese.',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ dove from 60 feet above the ocean surface to catch fish with remarkable precision.',
                'memory_tip': 'Remember "GANNET" - a seabird that GANgs up in colonies and dives like a NET into the sea for fish.'
            },
            'gardenesque': {
                'definition': 'Gardenesque refers to a style of landscape garden design that emphasizes the display of individual plants as specimens, rather than creating naturalistic compositions. This 19th-century gardening philosophy, promoted by J.C. Loudon, focused on showcasing the beauty and characteristics of individual trees, shrubs, and flowers. Gardenesque gardens typically feature well-spaced plants that can be appreciated individually for their unique forms and qualities.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'gar-den-ESK',
                'etymology': 'From "garden" plus the suffix "-esque" (in the style of), literally meaning "in the manner or style of a garden."',
                'language_origins': 'English',
                'example_sentence': 'The Victorian estate featured a _______ landscape where each rare tree could be admired individually.',
                'memory_tip': 'Remember "GARDENESQUE" - a GARDENing style that\'s like a gARDEN but more ESQuisite, showcasing individual plant specimens.'
            },
            'garderobe': {
                'definition': 'A garderobe historically refers to a wardrobe or closet for storing clothes, or in medieval castles, a private chamber that served as both a dressing room and lavatory. The term originally meant a room where garments were kept, but in medieval architecture, it often designated a latrine built into the castle walls. In modern usage, it can refer to a wardrobe or the collection of someone\'s clothing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAR-der-ohb',
                'etymology': 'From Old French "garderobe," literally meaning "guard the robe," from "garder" (to guard) plus "robe" (garment).',
                'language_origins': 'Old French',
                'example_sentence': 'The medieval castle\'s _______ was built into the thick stone walls for privacy and convenience.',
                'memory_tip': 'Remember "GARDEROBE" - a place to GUARD your ROBE (clothes), like a wardrobe or medieval dressing room.'
            },
            'gargle': {
                'definition': 'Gargle means to wash or rinse the throat by holding liquid in the mouth and forcing air through it, creating a bubbling sound. This action is typically done with mouthwash, salt water, or medication to clean the throat, soothe soreness, or treat infections. As a noun, gargle refers to the liquid used for gargling or the sound made during the process.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GAR-gul',
                'etymology': 'From Old French "gargouiller" meaning "to gurgle, bubble," imitative of the sound made when gargling.',
                'language_origins': 'Old French (imitative)',
                'example_sentence': 'The doctor recommended that she _______ with warm salt water to soothe her sore throat.',
                'memory_tip': 'Remember "GARGLE" - making a GARgling sound in your throat like a bubbling GAR-GAR sound.'
            },
            'gargoyles': {
                'definition': 'Gargoyles are carved stone figures, typically grotesque creatures or faces, that serve as decorative water spouts on Gothic buildings, particularly cathedrals and churches. These architectural features channel rainwater away from building walls while often depicting fantastical monsters, demons, or mythical creatures. Beyond their practical function, gargoyles were believed to ward off evil spirits and have become iconic symbols of medieval Gothic architecture.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GAR-goylz',
                'etymology': 'From Old French "gargouille" meaning "throat, waterspout," ultimately from Latin "gurgulio" (gullet), referring to the water flowing through them.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The cathedral\'s stone _______ stood as silent guardians, directing rainwater away from the sacred walls.',
                'memory_tip': 'Remember "GARGOYLES" - stone creatures that GARgle water and GOYl (spout) it away from Gothic buildings.'
            },
            'garish': {
                'definition': 'Garish describes something that is excessively bright, colorful, or decorated in a way that is unpleasantly conspicuous or vulgar. It refers to colors, patterns, or designs that are so bold or flashy that they become offensive to good taste rather than attractive. Garish suggests a lack of subtlety or refinement, emphasizing ostentation over elegance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GAIR-ish',
                'etymology': 'Origin uncertain, possibly from "gare" (to stare) plus "-ish," suggesting something that makes you stare due to its excessive brightness.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The _______ neon lights of the casino created an overwhelming and tasteless display.',
                'memory_tip': 'Remember "GARISH" - colors so GAR (harsh) and bright they make you GAWK-ish, unpleasantly flashy.'
            },
            'garland': {
                'definition': 'A garland is a circular or draped arrangement of flowers, leaves, or other decorative materials, typically used for ornamentation during celebrations, ceremonies, or as symbols of honor and achievement. Garlands can be worn as crowns or necklaces, hung as decorations, or placed as tributes. The word also means to decorate with or as if with a garland.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GAR-land',
                'etymology': 'From Old French "garlande," possibly from Frankish "*wierland" (something twisted), referring to the twisted or woven nature of garlands.',
                'language_origins': 'Old French, possibly Frankish',
                'example_sentence': 'She wore a beautiful flower _______ in her hair for the spring festival.',
                'memory_tip': 'Remember "GARLAND" - a decorative chain that you GAR (gather) from the LAND, like flowers woven together.'
            },
            'garlic': {
                'definition': 'Garlic is a pungent bulbous plant (Allium sativum) widely used as a seasoning and flavoring in cooking around the world. The bulb consists of individual segments called cloves, each wrapped in papery skin. Garlic is prized for its distinctive sharp, spicy flavor that mellows when cooked. It has also been used medicinally throughout history and is believed to have various health benefits.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAR-lik',
                'etymology': 'From Old English "garleac," literally meaning "spear leek," from "gar" (spear) plus "leac" (leek), referring to the pointed shape of garlic cloves.',
                'language_origins': 'Old English',
                'example_sentence': 'The chef minced fresh _______ to add aromatic flavor to the pasta sauce.',
                'memory_tip': 'Remember "GARLIC" - GAR (spear-like) cloves that you LICK for flavor, with a strong taste and smell.'
            },
            'garment': {
                'definition': 'A garment is any article of clothing or apparel worn on the body, including shirts, pants, dresses, coats, and other items of dress. The term encompasses all types of clothing from undergarments to outerwear, whether functional or decorative. Garment emphasizes the constructed, manufactured nature of clothing as items designed and made for wearing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAR-ment',
                'etymology': 'From Old French "garnement" meaning "equipment, attire," from "garnir" (to equip, furnish, warn).',
                'language_origins': 'Old French',
                'example_sentence': 'The designer carefully examined each _______ for quality and proper fit before the fashion show.',
                'memory_tip': 'Remember "GARMENT" - clothing that GARnishes your body, something to WEAR that covers and protects you.'
            },
            'garnet': {
                'definition': 'Garnet is a group of silicate minerals commonly used as gemstones and abrasives, typically appearing in deep red colors but also found in orange, yellow, green, and other hues. As gemstones, garnets are prized for their brilliance and durability. The mineral also has industrial uses in sandpaper, water filtration, and sandblasting due to its hardness and abrasive properties.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAR-nit',
                'etymology': 'From Old French "grenate," from Latin "granatum" (pomegranate), referring to the similarity in color and appearance to pomegranate seeds.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'Her grandmother\'s ring featured a beautiful deep red _______ surrounded by small diamonds.',
                'memory_tip': 'Remember "GARNET" - a red gemstone like GRANate (pomegranate) seeds, GARnishing jewelry with ruby-red color.'
            },
            'garniture': {
                'definition': 'Garniture refers to decorative elements, embellishments, or accessories that enhance or complete something, particularly in cooking (garnish for dishes) or decoration (ornamental accessories for furniture, rooms, or objects). In culinary contexts, garniture encompasses the vegetables, herbs, or other ingredients that accompany and enhance a main dish. In decorative arts, it refers to complementary ornamental pieces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAR-ni-chur',
                'etymology': 'From French "garniture" meaning "decoration, trimming," from "garnir" (to furnish, equip, decorate).',
                'language_origins': 'French',
                'example_sentence': 'The elaborate _______ around the roast included perfectly arranged vegetables and fresh herbs.',
                'memory_tip': 'Remember "GARNITURE" - GAR-ni-TURE, decorative elements that GAR(nish) and add beauty to furnish something.'
            },
            'garnituretwilight': {
                'definition': 'Garnituretwilight appears to be a combined word error where "garniture" (decorative elements or garnish) and "twilight" (the dim light period between day and night) were incorrectly merged during PDF processing. These are completely unrelated concepts - one relating to decoration and culinary arts, the other to natural lighting conditions. This represents a data quality issue where decorative and temporal terminology were improperly joined.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'GAR-ni-chur-TWY-lyt',
                'etymology': 'Corrupted combination of "garniture" (French decorative term) and "twilight" (Old English time period).',
                'language_origins': 'French, Old English (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining culinary decoration with evening lighting terminology.',
                'memory_tip': 'This is a data error - remember that "garniture" (garnish) and "twilight" (evening) should be separate words.'
            },
            'garou': {
                'definition': 'Garou typically refers to "loup-garou," the French term for werewolf - a mythological creature that transforms from human to wolf form. In folklore and popular culture, garou represents the concept of lycanthropy and shape-shifting between human and wolf forms. The term appears in French-Canadian folklore and has been adopted into English through literary and gaming contexts, particularly in supernatural fiction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gah-ROO',
                'etymology': 'From French "loup-garou" meaning "werewolf," literally "wolf-werewolf," from "loup" (wolf) and "garou" (werewolf, from Frankish).',
                'language_origins': 'French, Frankish',
                'example_sentence': 'The old French legend told of a _______ that roamed the forest during full moons.',
                'memory_tip': 'Remember "GAROU" - a were-wolf that GARs (growls) and ROUls (prowls) in French folklore, a shape-shifting creature.'
            },
            'garrulous': {
                'definition': 'Garrulous describes someone who is excessively talkative, especially about trivial matters; loquacious in a rambling or tedious way. A garrulous person tends to talk continuously without much consideration for their audience\'s interest or the importance of what they\'re saying. The word suggests not just talkativeness but specifically verbose, often tiresome chatter about unimportant topics.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GAIR-uh-lus',
                'etymology': 'From Latin "garrulus" meaning "talkative, chattering," from "garrire" (to chatter, prattle), imitative of the sound of chattering.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ neighbor kept everyone on the street informed about every minor detail of his daily activities.',
                'memory_tip': 'Remember "GARRULOUS" - someone who GARbles and chatters continuously, RULing conversations with endless talk.'
            },
            'gasiform': {
                'definition': 'Gasiform means having the form, nature, or characteristics of gas; existing in a gaseous state or resembling gas in behavior. This scientific term describes substances that exhibit the properties of gases, such as having no fixed shape or volume, expanding to fill containers, and being easily compressible. The word is used in chemistry and physics to describe matter in its gas phase.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GAS-ih-form',
                'etymology': 'From "gas" (coined by Jan Baptist van Helmont from Greek "chaos") plus Latin "forma" (form, shape).',
                'language_origins': 'Modern scientific term (Greek, Latin)',
                'example_sentence': 'The heated substance became _______, expanding rapidly to fill the entire container.',
                'memory_tip': 'Remember "GASIFORM" - in the FORM of GAS, having gas-like properties and behavior in matter.'
            },
            'gasket': {
                'definition': 'A gasket is a mechanical seal that fills the space between two or more mating surfaces to prevent leakage from or into the joined objects while under compression. Gaskets are commonly made from rubber, cork, metal, or composite materials and are used in engines, plumbing, and various mechanical applications. They ensure tight seals in everything from car engines to household appliances.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAS-kit',
                'etymology': 'Possibly from French "garcette" (small rope), originally referring to rope used for sealing, later applied to mechanical sealing devices.',
                'language_origins': 'Possibly French',
                'example_sentence': 'The mechanic replaced the worn _______ to stop the oil leak in the engine.',
                'memory_tip': 'Remember "GASKET" - a seal that prevents GAS or liquid from esKEeTing (escaping) through joints.'
            },
            'gasped': {
                'definition': 'Gasped is the past tense of "gasp," meaning to catch one\'s breath with an open mouth, especially due to shock, surprise, exertion, or difficulty breathing. It describes the sharp, audible intake of breath that occurs when someone is startled, out of breath, or struggling to breathe. Gasped suggests a sudden, involuntary breathing reaction to physical or emotional stimuli.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'GASPD',
                'etymology': 'From Middle English "gaspen," possibly from Old Norse "geispa" (to yawn), referring to opening the mouth wide for air.',
                'language_origins': 'Middle English, possibly Old Norse',
                'example_sentence': 'She _______ in amazement when she saw the surprise party waiting for her.',
                'memory_tip': 'Remember "GASPED" - when you\'re so surprised you need to GASP for air, breathing sharply and suddenly.'
            },
            'gaspesian': {
                'definition': 'Gaspesian refers to the Gaspé Peninsula (Gaspésie) in eastern Quebec, Canada, or things relating to this region. The peninsula is known for its rugged coastline, fishing communities, and natural beauty along the Gulf of St. Lawrence. Gaspesian might describe the geography, culture, people, or characteristics associated with this distinctive Atlantic Canadian region.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'gas-PEE-see-an',
                'etymology': 'From "Gaspé," possibly from Mi\'kmaq "gespeg" meaning "land\'s end," referring to the peninsula that extends into the Atlantic.',
                'language_origins': 'Mi\'kmaq, French',
                'example_sentence': 'The _______ coastline offers breathtaking views of the Atlantic Ocean and rugged cliffs.',
                'memory_tip': 'Remember "GASPESIAN" - relating to GASPé peninsula, where you might GASP at the stunning coastal views.'
            },
            'gasthaus': {
                'definition': 'A gasthaus is a German-style inn, tavern, or restaurant, typically offering lodging, meals, and beverages in a traditional, hospitable atmosphere. These establishments are common in Germany, Austria, and other German-speaking regions, often serving local cuisine and providing a social gathering place for the community. Gasthäuser (plural) combine accommodation with dining and drinking facilities in a cozy, welcoming environment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAHST-hows',
                'etymology': 'From German "Gasthaus," literally meaning "guest house," from "Gast" (guest) plus "Haus" (house).',
                'language_origins': 'German',
                'example_sentence': 'The traditional _______ served hearty German meals and local beer to weary travelers.',
                'memory_tip': 'Remember "GASTHAUS" - a German GUEST HOUSE where travelers can eat, drink, and rest.'
            },
            'gastritis': {
                'definition': 'Gastritis is inflammation of the stomach lining (gastric mucosa), which can be acute (sudden onset) or chronic (long-lasting). This condition can cause symptoms including stomach pain, nausea, vomiting, indigestion, and loss of appetite. Gastritis can be caused by bacterial infection (especially H. pylori), excessive alcohol consumption, certain medications, stress, or other factors that irritate the stomach lining.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gas-TRY-tis',
                'etymology': 'From Greek "gaster" (stomach) plus "-itis" (inflammation), literally meaning "stomach inflammation."',
                'language_origins': 'Greek',
                'example_sentence': 'The doctor diagnosed _______ and recommended avoiding spicy foods and alcohol.',
                'memory_tip': 'Remember "GASTRITIS" - when your GASTer (stomach) is inflamed with -ITIS, causing pain and discomfort.'
            },
            'gastronome': {
                'definition': 'A gastronome is a person with refined taste in food and drink; a connoisseur who appreciates fine cuisine and has extensive knowledge about culinary arts. Gastronomes are passionate about high-quality ingredients, skilled preparation, and the cultural aspects of food. They often seek out exceptional dining experiences and may be involved in food criticism, culinary education, or gourmet cooking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAS-truh-nohm',
                'etymology': 'From French "gastronome," from Greek "gastronimos" meaning "knowing the stomach," from "gaster" (stomach) plus "nomos" (law, knowledge).',
                'language_origins': 'French, Greek',
                'example_sentence': 'As a dedicated _______, she could identify the subtle flavors and cooking techniques in any dish.',
                'memory_tip': 'Remember "GASTRONOME" - someone who knows their GASTer (stomach) like a profeSSional, a food connoisseur.'
            },
            'gateway': {
                'definition': 'A gateway is an opening or passage that serves as an entrance or exit, often through a wall, fence, or barrier. Metaphorically, gateway refers to a means of access or entry to something, such as education being a gateway to opportunity. In computing, a gateway is a network device that connects different networks. The word emphasizes the function of providing access or passage between different spaces or systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAYT-way',
                'etymology': 'Compound of "gate" (from Old English "geat," opening, entrance) plus "way" (path, route).',
                'language_origins': 'Old English',
                'example_sentence': 'Education serves as a _______ to better career opportunities and personal growth.',
                'memory_tip': 'Remember "GATEWAY" - a GATE that shows the WAY, providing passage from one place or state to another.'
            },
            'gather': {
                'definition': 'Gather means to come together or bring together in one place; to collect, assemble, or accumulate people, things, or information. The word can describe both the action of collecting items and the process of people congregating. Gather also means to infer or conclude from available information, or to pull fabric together to create folds or pleats in sewing.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GATH-er',
                'etymology': 'From Old English "gaderian" meaning "to bring together, collect," related to "gador" (together).',
                'language_origins': 'Old English',
                'example_sentence': 'The family will _______ at grandmother\'s house for the holiday celebration.',
                'memory_tip': 'Remember "GATHER" - people GAining together, like a GAThering where everyone comes to one place.'
            }
        }
        
        return batch_074_data.get(word, {
            'definition': f'Educational definition for {word} would be provided here.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'Pronunciation guide for {word}',
            'etymology': f'Etymology information for {word}',
            'language_origins': 'Unknown origins',
            'example_sentence': f'Example sentence with _______ blank for {word}.',
            'memory_tip': f'Memory tip for remembering {word}.'
        })

    def process_batch(self, input_file: str, output_file: str):
        """Process a batch of words with comprehensive Claude data"""
        print(f"Processing {input_file}...")
        
        df = pd.read_csv(input_file)
        processed_words = []
        errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            
            # Skip empty rows
            if not word:
                continue
                
            # Check for combined word errors
            if word == 'galahadgalatea':
                errors.append(f"{word}: Combined word error: \"galahadgalatea\" appears to be \"Galahad\" + \"Galatea\" merged together. This is likely a PDF parsing error where two distinct mythological names were incorrectly combined.")
            elif word == 'galapagogallic':
                errors.append(f"{word}: Combined word error: \"galapagogallic\" appears to be \"galapago\" + \"gallic\" merged together. This is likely a PDF parsing error where island/tortoise and French cultural terms were incorrectly combined.")
            elif word == 'gallivatcharcuterie':
                errors.append(f"{word}: Combined word error: \"gallivatcharcuterie\" appears to be \"gallivat\" + \"charcuterie\" merged together. This is likely a PDF parsing error where sailing vessel and meat preparation terms were incorrectly combined.")
            elif word == 'garnituretwilight':
                errors.append(f"{word}: Combined word error: \"garnituretwilight\" appears to be \"garniture\" + \"twilight\" merged together. This is likely a PDF parsing error where culinary decoration and evening time terms were incorrectly combined.")
                
            # Get comprehensive Claude data
            claude_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty components  
            phonetic_score = self.difficulty_calc.calculate_phonetic_complexity(word)
            frequency_score = self.difficulty_calc.estimate_frequency(word)
            morphological_score = self.difficulty_calc.calculate_morphological_complexity(word)
            etymological_score = self.difficulty_calc.calculate_etymological_complexity(
                claude_data['etymology'], claude_data['language_origins']
            )
            
            processed_word = {
                'word': word,
                'years': row['years'],
                'source_files': row['source_files'],
                'source_difficulties': row['source_difficulties'],
                'definition': claude_data['definition'],
                'part_of_speech': claude_data['part_of_speech'],
                'pronunciation_guide': claude_data['pronunciation_guide'],
                'pronunciation_source': 'Claude',
                'etymology': claude_data['etymology'],
                'etymology_source': 'Claude',
                'language_origins': claude_data['language_origins'],
                'example_sentence': claude_data['example_sentence'],
                'example_sentence_source': 'Claude',
                'memory_tip': claude_data['memory_tip'],
                'phonetic_complexity': phonetic_score,
                'frequency_complexity': frequency_score,
                'morphological_complexity': morphological_score,
                'etymological_complexity': etymological_score,
                'final_difficulty_rating': None,  # Will be assigned later
                'difficulty_justification': None,  # Will be provided later
                'audio_file_path': None,  # Will be generated later
                'image_file_path': None,  # Will be added later
                'last_updated': '2024-08-20'
            }
            
            processed_words.append(processed_word)
        
        # Create output dataframe and save
        output_df = pd.DataFrame(processed_words)
        output_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"Successfully processed {len(processed_words)}/{len(df)} words to {output_file}")
        if errors:
            print(f"Found {len(errors)} error(s):")
            for error in errors:
                print(f"  - {error}")
        print("Batch 074 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch074Processor()
    processor.process_batch(
        "output/batch_074_words.csv",
        "output/batch_074_processed.csv"
    )