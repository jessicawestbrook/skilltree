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

class Batch077Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for a word using Claude knowledge"""
        
        batch_077_data = {
            'gleaming': {
                'definition': 'Gleaming means shining brightly, especially with reflected light, or radiating a warm, lustrous glow. It describes surfaces that reflect light in a bright, polished way, such as clean metal, fresh paint, or well-maintained objects. Gleaming can also refer to eyes that shine with emotion or intelligence, or anything that appears bright, clean, and well-maintained.',
                'part_of_speech': 'adjective, verb (present participle)',
                'pronunciation_guide': 'GLEE-ming',
                'etymology': 'From "gleam" (from Old English "glǣm" meaning "brightness, splendor") plus the present participle suffix "-ing."',
                'language_origins': 'Old English',
                'example_sentence': 'The freshly waxed car sat in the driveway, its surface _______ in the morning sunlight.',
                'memory_tip': 'Remember "GLEAMING" - GLEaning and shining brightly, AMazing to see with its bright reflection.'
            },
            'glengarry': {
                'definition': 'A glengarry is a traditional Scottish military cap or bonnet, typically made of wool and featuring a boat-shaped crown with ribbons hanging from the back. This distinctive headpiece is associated with Scottish Highland regiments and is characterized by its flat top, side folds, and decorative elements. The glengarry remains part of ceremonial military dress in Scottish units.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'glen-GAIR-ee',
                'etymology': 'Named after Glengarry, a valley in the Scottish Highlands, where this style of military headgear originated or was popularized.',
                'language_origins': 'Scottish Gaelic',
                'example_sentence': 'The Highland regiment wore traditional _______ caps during the ceremonial parade.',
                'memory_tip': 'Remember "GLENGARRY" - a Scottish military cap from GLEN (valley) where soldiers would CARRY their traditions.'
            },
            'glib': {
                'definition': 'Glib describes speech or a person that is fluent and voluble but insincere or superficial, characterized by ease and smoothness that may lack depth or genuine feeling. Someone who is glib can speak persuasively and confidently but may be avoiding serious consideration of the topic or hiding their true thoughts behind polished words.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLIB',
                'etymology': 'From Middle Low German "glibberig" meaning "slippery," suggesting speech that slides smoothly but may be unreliable.',
                'language_origins': 'Middle Low German',
                'example_sentence': 'His _______ response to the serious question revealed that he hadn\'t really thought about the issue.',
                'memory_tip': 'Remember "GLIB" - speech that\'s so smooth it\'s sLIPpery, flowing easily but lacking depth or sincerity.'
            },
            'glide': {
                'definition': 'Glide means to move smoothly and effortlessly, typically through air or across a surface, without apparent effort or with minimal friction. In aviation, gliding refers to flight without engine power, using air currents for lift. The word emphasizes graceful, continuous motion that appears effortless and fluid.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GLYD',
                'etymology': 'From Old English "glīdan" meaning "to slip, slide," related to "glad" (smooth, bright).',
                'language_origins': 'Old English',
                'example_sentence': 'The swan seemed to _______ effortlessly across the mirror-like surface of the lake.',
                'memory_tip': 'Remember "GLIDE" - to move smoothly like you\'re GLIDing on ice, effortless and graceful motion.'
            },
            'glimmer': {
                'definition': 'Glimmer means to shine faintly with a wavering light, or to show a trace or faint indication of something. It can refer to weak, intermittent light that flickers gently, or metaphorically to a small sign or hint of hope, understanding, or possibility. Glimmer suggests something barely visible but present.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GLIM-er',
                'etymology': 'From Middle English "glimeren," related to "gleam," possibly from Old Norse "glimra" (to glitter).',
                'language_origins': 'Middle English, possibly Old Norse',
                'example_sentence': 'A _______ of hope appeared when the rescue team spotted movement in the debris.',
                'memory_tip': 'Remember "GLIMMER" - a GLInt that\'s diMMER, a faint shine or small sign of something positive.'
            },
            'glimpse': {
                'definition': 'A glimpse is a momentary or partial view of something, typically brief and incomplete, offering just enough sight to suggest the whole. It can also mean a brief experience or understanding of something larger or more complex. Glimpse emphasizes the fleeting, limited nature of the observation or experience.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GLIMPS',
                'etymology': 'From Middle English "glimsen," related to "gleam," meaning "to shine faintly" or "catch sight of briefly."',
                'language_origins': 'Middle English',
                'example_sentence': 'She caught a brief _______ of the celebrity before the crowd blocked her view.',
                'memory_tip': 'Remember "GLIMPSE" - a brief GLInt of what you see, a quick PEEK that gives you a hint.'
            },
            'glint': {
                'definition': 'A glint is a small flash of light, especially one reflected from a shiny surface, or a brief indication of a particular quality or emotion, particularly in someone\'s eyes. Glint suggests a quick, sharp reflection or a momentary reveal of inner thoughts or feelings through facial expression.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GLINT',
                'etymology': 'From Middle English, probably of Scandinavian origin, related to Old Swedish "glinta" (to shine).',
                'language_origins': 'Middle English, Scandinavian',
                'example_sentence': 'There was a mischievous _______ in her eye as she revealed the surprise.',
                'memory_tip': 'Remember "GLINT" - a quick GLIstening piNT of light, a sharp flash or twinkle that catches your eye.'
            },
            'gliriform': {
                'definition': 'Gliriform means resembling or relating to dormice or other small rodents of the family Gliridae. This scientific term describes characteristics, behaviors, or anatomical features similar to those of dormice, which are small, nocturnal rodents known for their hibernation patterns and arboreal lifestyle. The term is used in zoological and comparative anatomy contexts.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLY-rih-form',
                'etymology': 'From Latin "glis" (dormouse) plus "forma" (form, shape), literally meaning "having the form of a dormouse."',
                'language_origins': 'Latin',
                'example_sentence': 'The fossil exhibited _______ characteristics typical of ancient dormouse relatives.',
                'memory_tip': 'Remember "GLIRIFORM" - shaped like a GLIRis (dormouse), having the FORM of small hibernating rodents.'
            },
            'glissando': {
                'definition': 'A glissando is a musical technique involving a continuous slide between two notes, creating a smooth, uninterrupted transition rather than distinct separate pitches. This effect can be performed on various instruments including piano, violin, trombone, and harp, creating a swooping or sliding sound. The technique adds expressiveness and fluidity to musical passages.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'glis-SAHN-doh',
                'etymology': 'From Italian "glissando," from French "glisser" (to slide), referring to the sliding motion between musical notes.',
                'language_origins': 'Italian, French',
                'example_sentence': 'The pianist\'s dramatic _______ swept across the keyboard from low to high notes.',
                'memory_tip': 'Remember "GLISSANDO" - GLIding and Sliding music notes, a smooth transition that flows like a musical slide.'
            },
            'glisten': {
                'definition': 'Glisten means to shine with a sparkling or wet-looking light, typically due to moisture or a wet surface reflecting light. It suggests a bright, shimmering appearance that catches and reflects light in multiple small points, creating a sparkling effect. Glistening often implies freshness, cleanliness, or the presence of moisture.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'GLIS-en',
                'etymology': 'From Old English "glisnian" meaning "to glitter, shine," related to "glisian" (to shine).',
                'language_origins': 'Old English',
                'example_sentence': 'Dewdrops made the spider web _______ like diamonds in the morning sunlight.',
                'memory_tip': 'Remember "GLISTEN" - to GLItter and shiNe with moisture, sparkling like wet surfaces catching light.'
            },
            'glitterati': {
                'definition': 'Glitterati refers to fashionable people, especially celebrities, socialites, and wealthy individuals who are part of the glamorous social scene. This term combines the idea of glittering or sparkling with the concept of social elites, describing those who live glamorous, highly publicized lifestyles and attend exclusive social events.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'glit-er-AH-tee',
                'etymology': 'A blend of "glitter" and "literati" (learned people), coined to describe glamorous celebrities and social elites who "glitter" in society.',
                'language_origins': 'Modern English (blend word)',
                'example_sentence': 'The charity gala attracted members of the _______ from entertainment and fashion industries.',
                'memory_tip': 'Remember "GLITTERATI" - the glamorous people who GLITTER in society, celebrities and elites who sparkle in the spotlight.'
            },
            'glittery': {
                'definition': 'Glittery describes something that sparkles, shimmers, or is covered with small reflective particles that catch and reflect light. It can refer to decorative materials, makeup, clothing, or any surface that produces a sparkling, twinkling effect. Glittery suggests brightness, festivity, and eye-catching visual appeal.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLIT-er-ee',
                'etymology': 'From "glitter" (from Old Norse "glitra" meaning "to glitter") plus the adjectival suffix "-y."',
                'language_origins': 'Old Norse',
                'example_sentence': 'The children made _______ holiday decorations using colorful sparkles and sequins.',
                'memory_tip': 'Remember "GLITTERY" - full of GLITTERs that make things sparkly, shiny with lots of tiny reflective bits.'
            },
            'gloaming': {
                'definition': 'Gloaming is the time of evening twilight, the period between day and night when the sky is partially illuminated but the sun has set. This poetic term describes the gentle, dim light of dusk when darkness is gradually approaching. Gloaming suggests a peaceful, reflective time of day with soft, fading light.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLOH-ming',
                'etymology': 'From Old English "glōmung," from "glōm" (twilight, gloom), related to the gradual darkening of evening.',
                'language_origins': 'Old English',
                'example_sentence': 'They walked through the garden in the peaceful _______, enjoying the soft evening light.',
                'memory_tip': 'Remember "GLOAMING" - the GLOw that\'s diMMING, the beautiful twilight time when day becomes night.'
            },
            'global': {
                'definition': 'Global means relating to the whole world or affecting the entire planet, encompassing all countries, regions, or the complete scope of something worldwide. It can describe phenomena, issues, businesses, or perspectives that have international reach and influence. Global emphasizes comprehensive, universal scope rather than local or regional focus.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLOH-bul',
                'etymology': 'From Latin "globalis," from "globus" (sphere, ball), referring to the spherical shape of the Earth and hence worldwide scope.',
                'language_origins': 'Latin',
                'example_sentence': 'Climate change is a _______ issue that requires international cooperation to address.',
                'memory_tip': 'Remember "GLOBAL" - relating to the whole GLOBE, worldwide and affecting everyone on the spherical Earth.'
            },
            'globular': {
                'definition': 'Globular means having the shape of a globe or sphere, characterized by a rounded, ball-like form. In astronomy, globular clusters are spherical collections of stars. In biology, globular proteins have compact, rounded structures. The term emphasizes the three-dimensional spherical or nearly spherical shape of objects.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLOB-yuh-ler',
                'etymology': 'From Latin "globularis," from "globulus" (small sphere), diminutive of "globus" (ball, sphere).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ star cluster contained thousands of ancient stars arranged in a spherical formation.',
                'memory_tip': 'Remember "GLOBULAR" - shaped like a little GLOBE, spherical and round like a ball or bubble.'
            },
            'gloomy': {
                'definition': 'Gloomy describes conditions or moods that are dark, dim, or depressing, characterized by little light or by sadness and pessimism. It can refer to physical environments with poor lighting or weather, or to emotional states marked by despondency and lack of hope. Gloomy suggests an atmosphere of darkness or melancholy.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLOO-mee',
                'etymology': 'From "gloom" (from Middle English "glomen" meaning "to look sullen") plus the adjectival suffix "-y."',
                'language_origins': 'Middle English',
                'example_sentence': 'The _______ weather matched her sad mood as she walked through the rain.',
                'memory_tip': 'Remember "GLOOMY" - full of GLOOM, dark and sad like a cloudy day that makes you feel blue.'
            },
            'glossary': {
                'definition': 'A glossary is an alphabetical list of terms with their definitions, typically found at the end of a book or document to help readers understand specialized vocabulary used in the text. Glossaries serve as quick reference tools for technical, academic, or specialized language that may not be familiar to all readers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLOS-uh-ree',
                'etymology': 'From Latin "glossarium," from Greek "glossa" (tongue, language) plus the suffix "-ary," meaning "collection of words."',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'Students referred to the textbook\'s _______ to understand the scientific terminology.',
                'memory_tip': 'Remember "GLOSSARY" - a GLOSSy collection of definitions that helps clarify difficult words and terms.'
            },
            'glossolalia': {
                'definition': 'Glossolalia is the phenomenon of speaking in tongues, characterized by fluent speech-like vocalizations that are not recognized as belonging to any known language. This occurs in religious contexts, particularly in Pentecostal and charismatic Christian traditions, where it is considered a spiritual gift. The speech patterns follow linguistic rules but lack conventional meaning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'glos-oh-LAY-lee-uh',
                'etymology': 'From Greek "glossa" (tongue, language) plus "lalia" (speech, chatter), literally meaning "tongue-speech."',
                'language_origins': 'Greek',
                'example_sentence': 'During the religious service, several congregants engaged in _______ as an expression of their faith.',
                'memory_tip': 'Remember "GLOSSOLALIA" - GLOSSa (tongue) LALIa (babbling), speaking in unknown tongues during religious experiences.'
            },
            'glossopetrae': {
                'definition': 'Glossopetrae, historically known as "tongue stones," are fossilized shark teeth that were once thought to be petrified serpent tongues fallen from the sky. These fossil teeth were collected and often used in medieval times as supposed antidotes to poison. The term reflects ancient attempts to explain these mysterious triangular fossils before the understanding of shark evolution.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'glos-oh-PET-ree',
                'etymology': 'From Greek "glossa" (tongue) plus Latin "petra" (stone), literally meaning "tongue stones."',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'Medieval collectors prized _______ as magical stones, not knowing they were ancient shark teeth.',
                'memory_tip': 'Remember "GLOSSOPETRAE" - GLOSSa (tongue) shaped PETRA (stones), ancient shark teeth that looked like stone tongues.'
            },
            'gloves': {
                'definition': 'Gloves are coverings for the hands, typically with individual sections for each finger and thumb, designed to protect, warm, or provide grip for the hands during various activities. They can be made from various materials including leather, fabric, rubber, or synthetic materials, and serve purposes ranging from warmth and protection to sterile medical procedures.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GLUVZ',
                'etymology': 'From Old English "glōf," related to Old Norse "glōfi," possibly from a root meaning "palm of the hand."',
                'language_origins': 'Old English, Old Norse',
                'example_sentence': 'The surgeon put on sterile _______ before beginning the medical procedure.',
                'memory_tip': 'Remember "GLOVES" - hand coverings you LOVE when it\'s cold, protecting your fingers and giving you grip.'
            },
            'glowquick': {
                'definition': 'Glowquick appears to be a combined word error where "glow" (emit light) and "quick" (fast or rapid) were incorrectly merged during PDF processing. These could be related in context (something that glows quickly), but they represent separate concepts that should not be joined as one word. This represents a data quality issue where lighting and speed terminology were improperly combined.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'GLOH-kwik',
                'etymology': 'Corrupted combination of "glow" (Old English "glōwan") and "quick" (Old English "cwicu").',
                'language_origins': 'Old English (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining light emission with speed terminology.',
                'memory_tip': 'This is a data error - remember that "glow" (emit light) and "quick" (fast) should be separate words.'
            },
            'glucose': {
                'definition': 'Glucose is a simple sugar (monosaccharide) that serves as the primary source of energy for living cells, particularly important for brain function and cellular metabolism. Found naturally in fruits and honey, glucose is also produced by the body through the breakdown of carbohydrates. Blood glucose levels are carefully regulated by hormones like insulin.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLOO-kohs',
                'etymology': 'From Greek "glukus" (sweet) plus the chemical suffix "-ose" indicating a sugar, literally meaning "sweet sugar."',
                'language_origins': 'Greek',
                'example_sentence': 'The diabetic patient monitored her blood _______ levels throughout the day.',
                'memory_tip': 'Remember "GLUCOSE" - GLUe-like sweet sugar that gives you energy, the main fuel your body uses.'
            },
            'glue': {
                'definition': 'Glue is an adhesive substance used to stick objects or materials together, typically liquid when applied but hardening to form a strong bond. Glue can be made from natural materials like animal proteins or synthetic polymers. Metaphorically, glue represents anything that holds things together or creates unity.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GLOO',
                'etymology': 'From Old French "glu," from Late Latin "glus," from Latin "glūten" (glue), related to "glūtinōsus" (sticky).',
                'language_origins': 'Old French, Late Latin',
                'example_sentence': 'The children used _______ to attach the paper pieces to their art project.',
                'memory_tip': 'Remember "GLUE" - sticky stuff that makes things stick together, holds pieces in place like GLUing puzzle pieces.'
            },
            'glumly': {
                'definition': 'Glumly is an adverb meaning in a glum manner, characterized by sadness, dejection, or morose silence. It describes actions or expressions performed with evident unhappiness, despondency, or sullen disappointment. Glumly suggests visible emotional heaviness and lack of cheerfulness or enthusiasm.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'GLUM-lee',
                'etymology': 'From "glum" (meaning "dejected, morose," possibly from Middle English "gloumen") plus the adverbial suffix "-ly."',
                'language_origins': 'Middle English',
                'example_sentence': 'He stared _______ out the window after hearing the disappointing news.',
                'memory_tip': 'Remember "GLUMLY" - acting in a GLUM way, sadLY and with visible dejection and unhappiness.'
            },
            'gluten': {
                'definition': 'Gluten is a mixture of proteins found in wheat and other grains like barley and rye, responsible for the elastic texture of dough and the chewy quality of baked goods. Gluten gives bread its structure and helps it rise. Some people have celiac disease or gluten sensitivity, requiring them to avoid gluten-containing foods.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLOO-ten',
                'etymology': 'From Latin "gluten" meaning "glue," referring to the sticky, adhesive quality of this protein mixture.',
                'language_origins': 'Latin',
                'example_sentence': 'The bakery offered ______-free bread for customers with celiac disease.',
                'memory_tip': 'Remember "GLUTEN" - the protein GLUe in grains that makes bread stretchy, but some people can\'t EAT it.'
            },
            'gluttonous': {
                'definition': 'Gluttonous describes excessive indulgence in food or drink, characterized by greedy or voracious consumption beyond normal appetite or need. It can also apply metaphorically to excessive desire for anything, not just food. Gluttonous behavior suggests lack of self-control and overindulgence that may be harmful or wasteful.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLUT-uh-nus',
                'etymology': 'From Latin "gluttonous," from "gluttire" (to swallow, gulp down) plus the adjectival suffix "-ous."',
                'language_origins': 'Latin',
                'example_sentence': 'His _______ eating habits at the buffet embarrassed his dinner companions.',
                'memory_tip': 'Remember "GLUTTONOUS" - GLUTTing yourself with food, overeating in an excessive and greedy way.'
            },
            'glyceraldehyde': {
                'definition': 'Glyceraldehyde is a simple sugar (triose) that plays important roles in cellular metabolism, particularly in glycolysis and gluconeogenesis pathways. This three-carbon molecule serves as an intermediate in the breakdown and synthesis of glucose. Glyceraldehyde exists in two mirror-image forms and is fundamental to understanding carbohydrate chemistry and biochemistry.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'glis-er-AL-duh-hyd',
                'etymology': 'From "glycerin" (from Greek "glukeros" meaning "sweet") plus "aldehyde" (a type of organic compound), referring to the sweet alcohol derivative.',
                'language_origins': 'Greek, Modern chemical terminology',
                'example_sentence': 'The biochemistry student learned about _______ as a key intermediate in glucose metabolism.',
                'memory_tip': 'Remember "GLYCERALDEHYDE" - GLYCERin (sweet) ALDEhyde, a simple sugar molecule important in metabolism.'
            },
            'gnarled': {
                'definition': 'Gnarled describes something twisted, knotted, or contorted, especially tree branches or roots that are bent and rough from age or weathering. The word can also describe hands that are rough and twisted from hard work or arthritis. Gnarled suggests a rugged, weathered appearance that shows the effects of time and hardship.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'NAHRLD',
                'etymology': 'From "gnarl" (meaning "to growl" or "a knot in wood"), possibly related to Middle Low German "gnarlen" (to snarl).',
                'language_origins': 'Middle Low German',
                'example_sentence': 'The ancient oak tree had _______ branches that twisted in fascinating patterns.',
                'memory_tip': 'Remember "GNARLED" - GNArled and twisted like wood that\'s been weathered, rough and knotted from age.'
            },
            'gnash': {
                'definition': 'Gnash means to grind or strike the teeth together, typically as an expression of anger, pain, or extreme emotion. The word often appears in the phrase "gnash one\'s teeth," which describes a physical manifestation of frustration, rage, or anguish. Gnashing suggests violent, involuntary jaw movements driven by intense emotion.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'NASH',
                'etymology': 'From Old English "gnæstan," possibly imitative of the sound of grinding teeth.',
                'language_origins': 'Old English',
                'example_sentence': 'In his fury, he began to _______ his teeth and clench his fists.',
                'memory_tip': 'Remember "GNASH" - to GriNd teeth together when you\'re ANgry, making grinding sounds from emotion.'
            },
            'gnathic': {
                'definition': 'Gnathic relates to the jaws or the process of chewing, used primarily in medical and anatomical contexts. The term appears in words like "gnathology" (study of jaw function) and describes conditions, procedures, or measurements involving the jaw bones, teeth alignment, or chewing mechanisms. Gnathic is fundamental to dental and maxillofacial terminology.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'NATH-ik',
                'etymology': 'From Greek "gnathos" (jaw) plus the adjectival suffix "-ic," literally meaning "relating to the jaw."',
                'language_origins': 'Greek',
                'example_sentence': 'The orthodontist studied the patient\'s _______ measurements to plan the jaw surgery.',
                'memory_tip': 'Remember "GNATHIC" - relating to your GNawing apparatus, the JAWS used for chewing and biting.'
            },
            'gnaw': {
                'definition': 'Gnaw means to bite or chew persistently, typically wearing away at something gradually through repeated biting or scraping. Animals gnaw on bones or wood, while the word can also describe persistent worry or anxiety that seems to "eat away" at someone mentally. Gnawing suggests steady, continuous action that gradually causes change.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'NAW',
                'etymology': 'From Old English "gnagan," related to Old Norse "gnaga," imitative of the sound of persistent chewing.',
                'language_origins': 'Old English, Old Norse',
                'example_sentence': 'The dog continued to _______ on the bone until there was nothing left.',
                'memory_tip': 'Remember "GNAW" - to GNaw like a rodent, continuously chewing and wearing something down bit by bit.'
            },
            'gnocchi': {
                'definition': 'Gnocchi are small Italian dumplings typically made from potatoes, flour, and eggs, though variations exist using ricotta, semolina, or other ingredients. These pillowy pasta-like pieces are usually boiled and served with various sauces. Traditional gnocchi are often shaped with ridges to help hold sauce and are considered a comfort food in Italian cuisine.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'NYOH-kee',
                'etymology': 'From Italian "gnocchi," plural of "gnocco," possibly from "nocchio" (knot in wood) referring to the dumpling\'s shape.',
                'language_origins': 'Italian',
                'example_sentence': 'The restaurant served homemade potato _______ with sage butter sauce.',
                'memory_tip': 'Remember "GNOCCHI" - Italian dumplings that are NOt quite pasta, soft potato pillows you eat with sauce.'
            },
            'gnome': {
                'definition': 'A gnome is a mythological creature typically depicted as a small, bearded humanoid who lives underground or in gardens, often associated with earth, mining, or tending plants. In folklore, gnomes are usually portrayed as wise, industrious beings who guard treasures or help with gardening. Garden gnomes are popular decorative statues representing these mythical creatures.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'NOHM',
                'etymology': 'From French "gnome," coined by Paracelsus from Greek "genomos" (earth-dweller), from "ge" (earth) plus "nomos" (inhabitant).',
                'language_origins': 'French, Greek',
                'example_sentence': 'The garden was decorated with colorful _______ statues among the flowers.',
                'memory_tip': 'Remember "GNOME" - a small mythical being who makes his HOME in the earth, often seen in gardens.'
            },
            'gnomon': {
                'definition': 'A gnomon is the triangular blade or pointer of a sundial that casts a shadow to indicate the time, or more generally, any object used to cast a shadow for measuring time or angles. In geometry, a gnomon is also the L-shaped figure remaining when a parallelogram is removed from a similar larger parallelogram.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'NOH-mon',
                'etymology': 'From Greek "gnomon" meaning "one who discerns or examines," from "gignoskein" (to know, perceive).',
                'language_origins': 'Greek',
                'example_sentence': 'The ancient sundial\'s _______ cast a precise shadow that indicated it was noon.',
                'memory_tip': 'Remember "GNOMON" - the part that helps you KNOW the time, the pointer that creates shadows on sundials.'
            },
            'goals': {
                'definition': 'Goals are desired outcomes, objectives, or targets that individuals or organizations aim to achieve through planned effort and action. Goals provide direction, motivation, and measurable endpoints for various endeavors, from personal development to business strategy. Effective goals are typically specific, measurable, achievable, relevant, and time-bound.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GOHLZ',
                'etymology': 'From Middle English "gol" meaning "boundary, limit," possibly related to Old English "gāl" (obstacle, barrier).',
                'language_origins': 'Middle English, Old English',
                'example_sentence': 'The company set ambitious _______ for increasing sales by 25% this year.',
                'memory_tip': 'Remember "GOALS" - what you GO toward with ALl your effort, targets you aim to achieve and reach.'
            },
            'goanna': {
                'definition': 'A goanna is an Australian term for monitor lizards, large reptiles known for their size, intelligence, and powerful claws. These lizards are found throughout Australia and are characterized by their long necks, forked tongues, and ability to stand on their hind legs. Goannas range from small species to the large perentie, Australia\'s largest lizard.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'goh-AN-uh',
                'etymology': 'Australian alteration of "iguana," adapted by early settlers who saw similarities between monitor lizards and iguanas.',
                'language_origins': 'Australian English (from Spanish "iguana")',
                'example_sentence': 'The large _______ sunned itself on the rock, monitoring the area with its keen eyes.',
                'memory_tip': 'Remember "GOANNA" - Australian for big monitor lizards, like an iGUANA that\'s GOing to be large and powerful.'
            },
            'goatee': {
                'definition': 'A goatee is a style of facial hair consisting of hair on the chin but not the cheeks, resembling the beard of a goat. This beard style can range from a small tuft of hair on the chin to a more extensive growth covering the entire chin area. The goatee has been a popular facial hair style across various cultures and time periods.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'goh-TEE',
                'etymology': 'From "goat" plus the diminutive suffix "-ee," referring to the resemblance to a goat\'s beard.',
                'language_origins': 'English',
                'example_sentence': 'The actor grew a neat _______ for his role as the sophisticated villain.',
                'memory_tip': 'Remember "GOATEE" - facial hair like a GOAT\'s beard, hair on the chin that looks like a goat\'s.'
            },
            'goblet': {
                'definition': 'A goblet is a drinking vessel, typically made of glass or metal, characterized by a bowl-shaped cup mounted on a stem with a flared base. Goblets are often used for wine or ceremonial drinks and are distinguished from regular cups by their elegant, stemmed design. They suggest formality and often appear in fine dining or religious contexts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOB-lit',
                'etymology': 'From Old French "gobelet," diminutive of "gobel" (cup), possibly from Gaulish or Celtic origins.',
                'language_origins': 'Old French, possibly Celtic',
                'example_sentence': 'The king raised his ornate silver _______ in a toast to the visiting dignitaries.',
                'memory_tip': 'Remember "GOBLET" - a fancy cup you GOB (drink) from, usually with a stem like wine glasses for special occasions.'
            },
            'goblins': {
                'definition': 'Goblins are mythological creatures typically portrayed as small, mischievous, and often malevolent beings in folklore and fantasy literature. Usually depicted as ugly, greenish creatures with pointed ears and a propensity for causing trouble, goblins are often associated with caves, forests, or underground dwellings. They appear in various cultural traditions and modern fantasy works.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GOB-linz',
                'etymology': 'From Old French "gobelin," possibly from Medieval Latin "gobelinus," perhaps related to the name of a troublesome spirit.',
                'language_origins': 'Old French, Medieval Latin',
                'example_sentence': 'The fairy tale warned children about mischievous _______ who lived in the dark forest.',
                'memory_tip': 'Remember "GOBLINS" - small, green creatures who GOBble up trouble, mythical beings that cause mischief.'
            },
            'gods': {
                'definition': 'Gods are supernatural beings worshipped as having power over nature and human affairs, typically considered immortal and possessing abilities far beyond those of mortals. Different religions and mythologies feature various gods with specific domains, powers, and characteristics. The concept of gods reflects human attempts to understand and relate to forces beyond their control.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GODZ',
                'etymology': 'From Old English "god," related to Germanic and possibly Indo-European roots meaning "to call upon" or "invoked one."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'Ancient civilizations built temples to honor their _______ and seek their protection.',
                'memory_tip': 'Remember "GODS" - divine beings who are GOOD and powerful, worshipped by people for protection and guidance.'
            },
            'godspeed': {
                'definition': 'Godspeed is an expression of good wishes for someone\'s success and safety, especially when they are starting a journey or new endeavor. Originally meaning "may God cause you to succeed," it\'s now used as a farewell blessing hoping for favorable outcomes. The word combines spiritual protection with wishes for swift, successful progress.',
                'part_of_speech': 'interjection, noun',
                'pronunciation_guide': 'GOD-speed',
                'etymology': 'From Middle English "God spede," literally meaning "God prosper (you)," a contraction of "God speed you."',
                'language_origins': 'Middle English',
                'example_sentence': 'The family wished the astronauts _______ as they departed for their mission to the space station.',
                'memory_tip': 'Remember "GODSPEED" - wishing someone GOD\'s blessing for SPEED and success on their journey.'
            },
            'goggles': {
                'definition': 'Goggles are protective eyewear designed to shield the eyes from dust, water, chemicals, bright light, or other hazards. Unlike regular glasses, goggles form a seal around the eyes and are often used for swimming, skiing, welding, laboratory work, or other activities requiring eye protection. They provide more comprehensive coverage than standard eyeglasses.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GOG-ulz',
                'etymology': 'Possibly from "goggle" meaning "to stare with wide eyes," referring to the wide-eyed appearance they create.',
                'language_origins': 'English',
                'example_sentence': 'The swimmer adjusted her _______ before diving into the chlorinated pool.',
                'memory_tip': 'Remember "GOGGLES" - eye protection that makes you look like you\'re GOGgling (staring wide-eyed), covering your eyes completely.'
            },
            'going': {
                'definition': 'Going can refer to the act of moving, traveling, or departing from one place to another, or it can describe current conditions, progress, or the state of affairs. As a verb form, it indicates ongoing or future movement. As a noun, it refers to conditions for travel or progress, such as "rough going" meaning difficult conditions.',
                'part_of_speech': 'verb (present participle), noun, adjective',
                'pronunciation_guide': 'GOH-ing',
                'etymology': 'From "go" (from Old English "gān" meaning "to go, walk, depart") plus the present participle suffix "-ing."',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ was slow due to heavy traffic on the highway.',
                'memory_tip': 'Remember "GOING" - the act of GOing somewhere, movement and progress toward a destination.'
            },
            'goji': {
                'definition': 'Goji refers to the bright red berries of the Lycium barbarum plant, native to Asia and often marketed as a superfood due to their high antioxidant content and purported health benefits. These small, sweet-tart berries are commonly dried and eaten as snacks, added to smoothies, or used in traditional Chinese medicine.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOH-jee',
                'etymology': 'From Chinese dialects, possibly Mandarin "gǒuqǐ" (枸杞), the traditional Chinese name for these berries.',
                'language_origins': 'Chinese',
                'example_sentence': 'The health-conscious consumer added _______ berries to her morning smoothie for extra antioxidants.',
                'memory_tip': 'Remember "GOJI" - bright red berries that help you GO with energy, superfruits from Asia for health.'
            },
            'gold': {
                'definition': 'Gold is a precious metal valued for its beauty, rarity, and resistance to corrosion, used throughout history for jewelry, currency, and decorative objects. Chemically represented as Au, gold has been a symbol of wealth, purity, and achievement across cultures. The word also describes the bright yellow color characteristic of this metal.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'GOHLD',
                'etymology': 'From Old English "gold," related to Germanic words and ultimately from Indo-European roots meaning "to shine, gleam."',
                'language_origins': 'Old English, Indo-European',
                'example_sentence': 'The Olympic champion proudly wore her _______ medal during the awards ceremony.',
                'memory_tip': 'Remember "GOLD" - the precious metal that\'s been treasured throughout history, shiny and valuable like captured sunlight.'
            },
            'golden': {
                'definition': 'Golden describes something made of gold, having the color of gold, or characterized by exceptional quality, prosperity, or happiness. The word can refer to the actual metal, the bright yellow color, or metaphorically to something precious, favorable, or marking a period of success and achievement.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GOHL-den',
                'etymology': 'From "gold" (Old English "gold") plus the adjectival suffix "-en," meaning "made of gold" or "resembling gold."',
                'language_origins': 'Old English',
                'example_sentence': 'The elderly couple celebrated their _______ wedding anniversary after fifty years of marriage.',
                'memory_tip': 'Remember "GOLDEN" - made of GOLD or like gold, precious and shining with the color or quality of gold.'
            },
            'golem': {
                'definition': 'A golem is a creature from Jewish folklore, typically made from clay or mud and brought to life through mystical means to serve or protect a community. The most famous golem story involves Rabbi Judah Loew of Prague creating one to defend the Jewish ghetto. In modern usage, golem can refer to any artificial being or mindless servant.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOH-lem',
                'etymology': 'From Hebrew "golem" meaning "shapeless mass" or "embryo," from "galam" (to wrap up, fold).',
                'language_origins': 'Hebrew',
                'example_sentence': 'The legend tells of a rabbi who created a clay _______ to protect his people from persecution.',
                'memory_tip': 'Remember "GOLEM" - a creature GOing through the motions, made of clay and brought to life to serve and protect.'
            },
            'goliath': {
                'definition': 'Goliath refers to the giant Philistine warrior from the biblical story who was defeated by the young David with a sling and stone. More generally, Goliath represents any person or thing of enormous size, strength, or power, especially when confronting something much smaller. The name symbolizes seemingly insurmountable challenges that can be overcome.',
                'part_of_speech': 'proper noun, noun',
                'pronunciation_guide': 'goh-LY-uth',
                'etymology': 'From Hebrew "Golyat," the name of the biblical giant, possibly meaning "exile" or related to "galah" (to uncover).',
                'language_origins': 'Hebrew',
                'example_sentence': 'The small startup faced a _______ in competing against the industry\'s dominant corporation.',
                'memory_tip': 'Remember "GOLIATH" - the giant who GOt defeated by little David, representing huge challenges that can be overcome.'
            },
            'gondolas': {
                'definition': 'Gondolas are traditional flat-bottomed Venetian boats propelled by a single oar, used for navigating the canals of Venice. These distinctive black boats are operated by gondoliers and are primarily used for tourist rides and special occasions. The term also refers to the passenger compartments of cable cars or aerial lifts.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GON-duh-lahz',
                'etymology': 'From Italian "gondola," possibly from Greek "kondu" (drinking cup) referring to the boat\'s curved shape.',
                'language_origins': 'Italian, possibly Greek',
                'example_sentence': 'Tourists enjoyed romantic rides through Venice\'s canals in traditional black _______.',
                'memory_tip': 'Remember "GONDOLAS" - elegant boats that GO through Venice canals, romantic vessels steered by gondoliers.'
            },
            'gondwana': {
                'definition': 'Gondwana refers to the ancient supercontinent that existed in the Southern Hemisphere, comprising what are now South America, Africa, Antarctica, Australia, and the Indian subcontinent. This landmass began breaking apart about 180 million years ago during the Jurassic period. The concept is crucial for understanding continental drift, biogeography, and the distribution of fossils and species.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'gond-WAH-nuh',
                'etymology': 'Named after the Gondi people and the ancient Gondwana region of central India, where characteristic rock formations were first studied.',
                'language_origins': 'Sanskrit (from the Gondi people)',
                'example_sentence': 'The fossil evidence supports the theory that _______ was a massive southern supercontinent.',
                'memory_tip': 'Remember "GONDWANA" - the ancient supercontinent that\'s GONe now, WANdering apart to form southern continents.'
            }
        }
        
        return batch_077_data.get(word, {
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
            if word == 'glowquick':
                errors.append(f"{word}: Combined word error: \"glowquick\" appears to be \"glow\" + \"quick\" merged together. This is likely a PDF parsing error where light emission and speed terminology were incorrectly combined.")
                
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
        print("Batch 077 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch077Processor()
    processor.process_batch(
        "output/batch_077_words.csv",
        "output/batch_077_processed.csv"
    )