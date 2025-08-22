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
    input_file = os.path.join(script_dir, 'output', 'batch_161_words.csv')
    output_file = os.path.join(script_dir, 'output', 'batch_161_processed.csv')
    
    calculator = DifficultyCalculator()
    
    # Comprehensive word data with educational content
    word_data = {
        'sinophile': {
            'definition': 'A sinophile is a person who has a strong interest in, appreciation for, or love of Chinese culture, history, language, or customs. This term describes individuals who actively seek to learn about China, study Chinese language, collect Chinese art, or engage deeply with Chinese philosophy, literature, and traditions. Sinophiles may be scholars, travelers, collectors, or simply enthusiasts who find Chinese civilization fascinating and worthy of study. The interest can span various aspects of Chinese culture, from ancient history and classical literature to modern developments and contemporary society. Many sinophiles dedicate significant time to understanding China\'s complex cultural heritage and its influence on world civilization.',
            'pronunciation': '/ˈsaɪnoʊˌfaɪl/',
            'example_sentence': 'The _____ spent years learning Mandarin and studying ancient Chinese poetry to better understand the culture he admired.',
            'etymology': 'From "Sino-" (relating to China, from Late Latin "Sinae") + "-phile" (lover, from Greek "philos" meaning loving).',
            'mnemonic': 'Think "SINO-PHILE = Someone who\'s IN love with Chinese culture, Studying It Naturally Over time, seeking PHIlosophy and Learning Everything" - a lover of Chinese culture.',
            'source': 'Claude'
        },
        'sinuously': {
            'definition': 'Sinuously describes movement or form that is characterized by smooth, flowing curves or winding patterns, like the graceful undulation of a snake or the meandering path of a river. This adverb suggests elegant, serpentine motion that is both fluid and rhythmic, often associated with natural grace and beauty. The word applies to physical movement, such as a dancer moving sinuously across the stage, or to describe shapes and paths that curve and wind rather than proceeding in straight lines. Sinuous movement implies flexibility, adaptability, and a kind of organic flow that follows natural contours rather than rigid geometric patterns.',
            'pronunciation': '/ˈsɪnjuəsli/',
            'example_sentence': 'The river wound _____ through the valley, creating a series of elegant curves around the rolling hills.',
            'etymology': 'From Latin "sinuosus" meaning "winding" or "curved," from "sinus" (curve, fold, bay) + adverbial suffix "-ly."',
            'mnemonic': 'Think "SIN-UOUS-LY = Snake-like IN its movement, Using Organic Undulations, Smoothly winding Like a river" - moving in smooth curves.',
            'source': 'Claude'
        },
        'sinus': {
            'definition': 'A sinus is a hollow cavity or space within a structure, most commonly referring to the air-filled spaces in the bones of the skull that connect to the nasal passages. The four main pairs of paranasal sinuses (frontal, ethmoid, sphenoid, and maxillary) help humidify and warm inhaled air while reducing the weight of the skull. When these become inflamed or infected, the condition is called sinusitis. In medical terminology, sinus also refers to any cavity or channel in the body, such as the cavernous sinus in the brain or the coronary sinus in the heart. The term extends to other fields, describing any hollow recess or cavity in various structures.',
            'pronunciation': '/ˈsaɪnəs/',
            'example_sentence': 'The doctor explained that the patient\'s chronic headaches were caused by inflammation in the frontal _____.',
            'etymology': 'From Latin "sinus" meaning "bay," "curve," or "fold," referring to the curved, hollow spaces in anatomy.',
            'mnemonic': 'Think "SIN-US = Space IN Nose, Under Skull" - hollow spaces in the head that can cause trouble when blocked.',
            'source': 'Claude'
        },
        'sioux': {
            'definition': 'Sioux refers to a group of Native American tribes, also known as the Dakota, Lakota, and Nakota peoples, who historically inhabited the Great Plains region of North America. The three main divisions speak related but distinct languages within the Siouan language family. The Sioux were traditionally nomadic buffalo hunters known for their horsemanship, warrior culture, and resistance to westward expansion during the 19th century. Famous leaders like Sitting Bull and Crazy Horse led struggles against U.S. military forces. Today, Sioux communities maintain their cultural traditions while living on reservations primarily in South Dakota, North Dakota, Minnesota, and Nebraska, working to preserve their languages and customs.',
            'pronunciation': '/su/',
            'example_sentence': 'The museum displayed traditional _____ beadwork and ceremonial clothing from the 19th century Plains tribes.',
            'etymology': 'From French "Sioux," shortened from "Nadouessioux," from Ojibwe "Nadowessi" meaning "little snake" or "enemy."',
            'mnemonic': 'Think "SIOUX = Strong Indigenous tribe of the plains, OUtstanding Warriors who fought for their homeland" - Great Plains Native American people.',
            'source': 'Claude'
        },
        'sips': {
            'definition': 'Sips refers to small quantities of liquid taken into the mouth in single drinking actions, or the act of drinking in such small amounts. This method of consumption is often used when tasting beverages to assess flavor, when drinking very hot liquids to avoid burning the mouth, or when trying to make a drink last longer. Sipping demonstrates restraint and mindfulness in consumption, allowing the drinker to savor flavors gradually. The word can apply to various contexts, from sipping fine wine to appreciate its complexity, to taking medicinal sips of tea when feeling ill. The measured approach of sipping contrasts with gulping or drinking large quantities quickly.',
            'pronunciation': '/sɪps/',
            'example_sentence': 'She took careful _____ of the hot coffee to avoid burning her tongue while enjoying the rich flavor.',
            'etymology': 'From Middle English "sippen," possibly from Old English "sypian," related to "soak" or "absorb," meaning to drink in small quantities.',
            'mnemonic': 'Think "SIPS = Small Intake Portions, Slowly consuming liquid" - drinking in tiny amounts.',
            'source': 'Claude'
        },
        'sirenian': {
            'definition': 'Sirenian refers to any member of the order Sirenia, a group of large, herbivorous marine mammals commonly known as sea cows, including manatees and dugongs. These gentle, slow-moving creatures inhabit warm coastal waters and rivers, feeding primarily on seagrass and aquatic vegetation. Sirenians have paddle-like flippers, rounded tails, and can grow to significant sizes, with some species reaching over 10 feet in length. They are believed to be the source of mermaid legends due to their human-like behavior when surfacing to breathe. Unfortunately, sirenians are vulnerable to extinction due to habitat loss, boat strikes, and human interference, making conservation efforts crucial for their survival.',
            'pronunciation': '/saɪˈriniən/',
            'example_sentence': 'The marine biologist studied _____ behavior in the warm waters where manatees gather during winter months.',
            'etymology': 'From "Sirenia" (the order name) + "-an," where Sirenia comes from "siren," referencing the mythical creatures that inspired mermaid legends.',
            'mnemonic': 'Think "SIREN-IAN = like mythical SIRENs, these gentle sea creatures Inspired Ancient tales of mermaids" - sea cows that inspired mermaid myths.',
            'source': 'Claude'
        },
        'sirius': {
            'definition': 'Sirius is the brightest star in the night sky as viewed from Earth, located in the constellation Canis Major (the Greater Dog), which is why it\'s often called the "Dog Star." This binary star system consists of Sirius A, a main-sequence star about twice the mass of our Sun, and Sirius B, a white dwarf companion. Ancient civilizations, particularly the Egyptians, used Sirius for calendar calculations, as its heliacal rising coincided with the annual Nile flood. The star has played important roles in navigation, mythology, and astronomy throughout human history. At a distance of about 8.6 light-years from Earth, Sirius is one of our nearest stellar neighbors.',
            'pronunciation': '/ˈsɪriəs/',
            'example_sentence': 'The astronomer pointed out _____, the brilliant Dog Star, shining brightly in the winter constellation Canis Major.',
            'etymology': 'From Latin "Sirius," from Greek "Seirios" meaning "glowing" or "scorching," referring to its brilliant brightness.',
            'mnemonic': 'Think "SIRIUS = Super Intense star, Really an Important star, Unmistakably bright Star" - the brightest star in our night sky.',
            'source': 'Claude'
        },
        'sirjana': {
            'definition': 'Sirjana is a name of Sanskrit origin meaning "creation," "artistic creation," or "creative work." In South Asian cultures, particularly Nepal and India, this name is often given to girls with the hope that they will be creative, artistic, or innovative in their pursuits. The word encompasses the concept of bringing something new into existence through imagination, skill, and effort. In literary and artistic contexts, sirjana refers to the creative process itself - the act of creating poetry, art, music, or other forms of cultural expression. The name reflects cultural values that celebrate creativity, innovation, and the ability to create beauty or meaning through artistic endeavors.',
            'pronunciation': '/sɪrˈdʒɑnə/',
            'example_sentence': '_____ excelled in her art classes, living up to her name which means "creation" in Sanskrit.',
            'etymology': 'From Sanskrit "sṛjana" meaning "creation" or "creative work," from the root "sṛj" (to create, emit, produce).',
            'mnemonic': 'Think "SIR-JANA = Someone who\'s artIstically gifted at creating, Generating ART through Natural Ability" - a name meaning creative work.',
            'source': 'Claude'
        },
        'sirloindeodorant': {
            'definition': '[COMBINED WORD ERROR] This appears to be two completely unrelated words incorrectly combined: "sirloin" and "deodorant." Sirloin is a cut of beef from the rear back portion of the cow, prized for its tenderness and flavor in steaks and roasts. Deodorant is a personal hygiene product designed to prevent or mask body odor by inhibiting bacterial growth or neutralizing odors. These are entirely different concepts from food and personal care that should never be combined. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈsɜrˌlɔɪn diˈoʊdərənt/',
            'example_sentence': 'The restaurant served perfectly grilled _____ steaks, and everyone remembered to use _____ before the dinner party.',
            'etymology': 'Sirloin: from Old French "surlonge" (above the loin). Deodorant: from "de-" (removing) + "odor" + "-ant" (agent).',
            'mnemonic': 'Remember these as TWO separate words: SIRLOIN (beef cut) + DEODORANT (hygiene product).',
            'source': 'Claude'
        },
        'sister': {
            'definition': 'Sister refers to a female sibling who shares at least one parent with another person, creating one of the most fundamental family relationships. The sisterly bond often involves shared experiences, mutual support, competition, and lifelong connection that evolves throughout different life stages. Sisters may be biological (sharing genetic heritage), half-sisters (sharing one parent), step-sisters (related through marriage of parents), or adopted sisters (joined through adoption into the same family). The term extends to close female friends ("sister-like"), members of religious communities (nuns), and solidarity among women ("sisterhood"). Sister relationships significantly influence personality development, social skills, and emotional growth through shared childhood experiences and ongoing family dynamics.',
            'pronunciation': '/ˈsɪstər/',
            'example_sentence': 'My _____ and I have always been close, supporting each other through both challenges and celebrations.',
            'etymology': 'From Old English "sweostor," from Proto-Germanic "*swestēr," related to Latin "soror" and Sanskrit "svasā."',
            'mnemonic': 'Think "SIS-TER = female Sibling, Intimate bond, Sharing Together through Every life stage" - female family member.',
            'source': 'Claude'
        },
        'sitcom': {
            'definition': 'Sitcom is a shortened form of "situational comedy," referring to a television comedy series that features the same characters in recurring settings, typically involving humorous situations that arise from their personalities and relationships. Sitcoms usually run for about 30 minutes per episode and employ laugh tracks or live studio audiences to enhance comedic timing. Classic examples include "I Love Lucy," "Friends," and "The Office." The format relies on character development, witty dialogue, and relatable situations that audiences can connect with. Modern sitcoms have evolved to include various styles, from traditional multi-camera productions to single-camera mockumentary formats, but they maintain the core principle of extracting humor from everyday situations.',
            'pronunciation': '/ˈsɪtˌkɑm/',
            'example_sentence': 'The new _____ about office workers became incredibly popular due to its clever writing and relatable characters.',
            'etymology': 'Compound word formed from "situation" + "comedy," coined in the 1950s to describe the emerging television comedy format.',
            'mnemonic': 'Think "SIT-COM = SITuational COMedy show" - a TV comedy about everyday situations.',
            'source': 'Claude'
        },
        'situation': {
            'definition': 'Situation refers to the combination of circumstances, conditions, and context that exist at a particular time and place, creating the environment in which events occur or decisions must be made. This comprehensive concept encompasses all the relevant factors - physical, social, emotional, and temporal - that influence how things unfold. Situations can be simple and straightforward or complex and challenging, requiring different approaches and responses. Understanding a situation involves analyzing multiple variables, recognizing relationships between factors, and considering potential outcomes. The term appears in various contexts, from everyday personal situations to complex business scenarios, emergency situations requiring immediate response, and social situations involving interpersonal dynamics.',
            'pronunciation': '/ˌsɪtʃuˈeɪʃən/',
            'example_sentence': 'The emergency responders quickly assessed the _____ before determining the best course of action.',
            'etymology': 'From French "situation," from Medieval Latin "situatio," from "situare" (to place or position), from "situs" (position).',
            'mnemonic': 'Think "SITU-ATION = Set of circumstances Including Time, place, Understanding, and contextual information" - the complete circumstances.',
            'source': 'Claude'
        },
        'sixth': {
            'definition': 'Sixth is the ordinal number corresponding to the number six, indicating position in a sequence or order. As a fraction, one-sixth represents one part of something divided into six equal parts. In music, a sixth is an interval spanning six letter names in the scale, creating harmonious sounds in compositions. The term appears in various contexts: sixth grade in education, sixth sense referring to intuitive perception beyond the five physical senses, and sixth place in competitions. Mathematically, sixth can represent both position (6th) and fraction (1/6). The concept of "sixth" implies completion of more than half but less than the total of a sequence, suggesting substantial progress toward a goal.',
            'pronunciation': '/sɪksθ/',
            'example_sentence': 'She finished in _____ place in the marathon, which was a personal best for her running career.',
            'etymology': 'From Old English "siexta," from "siex" (six) + ordinal suffix "-ta," related to other Germanic ordinal formations.',
            'mnemonic': 'Think "SIX-TH = SIX plus ordinal ending, THe number that comes after fifth" - the 6th position in order.',
            'source': 'Claude'
        },
        'size': {
            'definition': 'Size refers to the physical dimensions, magnitude, or extent of something, indicating how large or small an object, space, or quantity is in relation to other things. This fundamental concept helps us categorize, compare, and understand the world around us through measurements of length, width, height, volume, or mass. Size can be absolute (specific measurements) or relative (compared to other objects). The concept applies across numerous domains: clothing sizes for fit, font sizes for readability, population sizes for demographics, and file sizes for digital storage. Understanding size relationships is crucial for practical decisions, scientific analysis, and everyday tasks like purchasing, organizing, and planning.',
            'pronunciation': '/saɪz/',
            'example_sentence': 'The architect needed to know the exact _____ of the room before designing the custom furniture.',
            'etymology': 'From Old French "sise," meaning "assize" or "regulation," originally referring to fixed portions or standards.',
            'mnemonic': 'Think "SIZE = Scale Indicating how big something is, measuring its Z-axis, Y-axis, and X-axis Extent" - how big or small something is.',
            'source': 'Claude'
        },
        'sized': {
            'definition': 'Sized is the past tense of the verb "size," meaning having been measured, evaluated for dimensions, or fitted to particular specifications. The word also functions as an adjective describing something that has been made to fit specific size requirements or has been categorized by size. In manufacturing and retail, items are sized to meet standardized measurements for consistency and proper fit. The term can also mean having assessed or evaluated the scope or extent of something, as in "sized up the competition." Sizing processes ensure that products meet dimensional requirements and that customers can select appropriate fits for their needs.',
            'pronunciation': '/saɪzd/',
            'example_sentence': 'The tailor carefully _____ the suit to ensure a perfect fit for the wedding ceremony.',
            'etymology': 'From "size" + past tense suffix "-ed," where "size" comes from Old French "sise" meaning regulation or standard.',
            'mnemonic': 'Think "SIZED = Size measured and fit Exactly according to Dimensions" - measured and fitted to specific dimensions.',
            'source': 'Claude'
        },
        'skaamoogs': {
            'definition': 'Skaamoogs appears to be a very uncommon or potentially invented word that does not have a standard definition in English dictionaries. It might be a regional dialect term, a proper noun, a brand name, or a specialized term from a particular field or community. Without more context about its origin or usage, it\'s difficult to provide a definitive meaning. The word structure suggests it could be of Scandinavian or Germanic origin, but this is speculative. In spelling bee contexts, such unusual words often test contestants\' ability to work with unfamiliar terms and apply general spelling principles even when they don\'t know the word\'s meaning.',
            'pronunciation': '/ˈskɑˌmuɡz/',
            'example_sentence': 'The contestant had never heard the word _____ before and had to rely on phonetic spelling patterns.',
            'etymology': 'Origin uncertain; possibly a regional term, proper noun, or specialized vocabulary from a particular field or community.',
            'mnemonic': 'Think "SKAA-MOOGS = Spelling Challenge requires Applying All Approaches, Making Our Only Goal correct Spelling" - an unfamiliar word requiring careful spelling.',
            'source': 'Claude'
        },
        'skateboard': {
            'definition': 'A skateboard is a narrow board with wheels attached underneath, designed for riding and performing tricks by balancing and propelling oneself with one foot while the other remains on the board. This recreational and athletic equipment evolved from surfing culture in California during the 1950s and 1960s, allowing surfers to practice when waves were unavailable. Modern skateboards consist of a wooden deck (usually maple), trucks (metal axles), wheels (polyurethane), and bearings for smooth rolling. Skateboarding has become both a popular recreational activity and a competitive sport, featuring in the Olympics since 2021. The culture surrounding skateboarding includes artistic expression, urban exploration, and a unique subculture with its own fashion and terminology.',
            'pronunciation': '/ˈskeɪtˌbɔrd/',
            'example_sentence': 'The teenager practiced tricks on his _____ every day after school in the empty parking lot.',
            'etymology': 'Compound word from "skate" (to glide) + "board" (flat piece of wood), coined in the 1960s.',
            'mnemonic': 'Think "SKATE-BOARD = SKATE on a BOARD with wheels" - a board you skate on with wheels underneath.',
            'source': 'Claude'
        },
        'skedaddle': {
            'definition': 'Skedaddle is an informal verb meaning to leave quickly or hurriedly, often to escape from trouble, danger, or an unwanted situation. This lively word suggests rapid departure with a sense of urgency or playful haste, typically used in casual conversation rather than formal contexts. The term conveys more personality and color than simple words like "leave" or "go," often implying a somewhat comical or frantic exit. Skedaddle might be used when someone needs to escape before getting caught, when avoiding an uncomfortable confrontation, or simply when departing rapidly for any reason. The word adds a whimsical, folksy flavor to descriptions of quick departures.',
            'pronunciation': '/skɪˈdædəl/',
            'example_sentence': 'When the children heard their mother calling for chores, they decided to _____ to the playground.',
            'etymology': 'American slang from the 1860s, possibly from Irish "sceidil" (to scatter, spill) or from dialectal "scaddle" (to run away).',
            'mnemonic': 'Think "SKE-DADDLE = SKEr away quickly like a duck waDDLEs fast when scared" - to leave in a hurry.',
            'source': 'Claude'
        },
        'skeltonic': {
            'definition': 'Skeltonic refers to a specific verse form created by English poet John Skelton (1463-1529), characterized by short, irregular lines, simple rhyme schemes, and a bouncing, energetic rhythm. Skeltonic verse typically features lines of varying lengths, often quite short (two to five stressed syllables), with frequent rhymes that may continue for several lines before changing. This poetic style creates a rapid, almost breathless effect that can be humorous, satirical, or intensely emotional. The form allows for considerable freedom in meter and line length while maintaining the driving force of rhyme. Modern poets occasionally use skeltonic verse for comic effect or to create particular rhythmic emphasis in their work.',
            'pronunciation': '/skɛlˈtɑnɪk/',
            'example_sentence': 'The poetry class studied _____ verse to understand how irregular meter can create unique rhythmic effects.',
            'etymology': 'Named after John Skelton (c.1463-1529), English poet who developed and popularized this distinctive verse form.',
            'mnemonic': 'Think "SKEL-TONIC = SKELton\'s poetic style, TONally bouncing with short lines, Including Characteristic rhyme" - poetry style of John Skelton.',
            'source': 'Claude'
        },
        'skeptical': {
            'definition': 'Skeptical describes an attitude of doubt, questioning, or critical examination toward claims, beliefs, or statements, particularly those lacking sufficient evidence or proof. A skeptical person doesn\'t accept information at face value but instead applies critical thinking, demands evidence, and considers alternative explanations before forming conclusions. This intellectual approach is fundamental to scientific inquiry, journalism, and rational decision-making. Healthy skepticism helps distinguish between reliable and unreliable information, protects against fraud and misinformation, and promotes evidence-based thinking. However, excessive skepticism can become cynicism, while balanced skepticism maintains openness to changing views when presented with convincing evidence.',
            'pronunciation': '/ˈskɛptɪkəl/',
            'example_sentence': 'She remained _____ about the investment opportunity until she could review all the financial documents.',
            'etymology': 'From Greek "skeptikos" meaning "inquiring" or "reflective," from "skeptesthai" (to look, consider, examine).',
            'mnemonic': 'Think "SKEP-TICAL = Scrutinizing Knowledge, Examining Proof, Testing Information Carefully And Logically" - questioning and demanding proof.',
            'source': 'Claude'
        },
        'skerrick': {
            'definition': 'Skerrick is an Australian and New Zealand slang term meaning a tiny amount, scrap, or small portion of something, often used in negative constructions to emphasize the complete absence of something. The word typically appears in phrases like "not a skerrick" to mean "not even the smallest bit." This colorful term adds emphasis and regional flavor to expressions of scarcity or absence, similar to how "smidgen" or "iota" function in other English dialects. Skerrick reflects the Australian tendency toward distinctive slang that creates vivid, memorable expressions for common concepts. The word is particularly useful for emphasizing the thoroughness of consumption or the completeness of absence.',
            'pronunciation': '/ˈskɛrɪk/',
            'example_sentence': 'After the family reunion picnic, there wasn\'t a _____ of food left on any of the tables.',
            'etymology': 'Australian slang of uncertain origin, possibly from dialectal "skerick" or related to "skerrick" meaning a small fragment.',
            'mnemonic': 'Think "SKER-RICK = SKinny amount, Extremely Reduced, Really tiny amount, Including even the smallest bit" - a very tiny amount.',
            'source': 'Claude'
        },
        'skerricksmriti': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "skerrick" and "smriti." Skerrick is Australian slang for a tiny amount or small scrap of something. Smriti is a Sanskrit term meaning "memory" or "remembrance," referring to traditional Hindu texts based on memory and human authority, as opposed to shruti (divine revelation). These are completely unrelated concepts from different linguistic and cultural traditions that should not be combined. The error likely occurred during document scanning or data processing.',
            'pronunciation': '/ˈskɛrɪk ˈsmrɪti/',
            'example_sentence': 'There wasn\'t a _____ of evidence left, and the scholar studied _____ texts about ancient traditions.',
            'etymology': 'Skerrick: Australian slang origin uncertain. Smriti: from Sanskrit "smṛti" meaning "memory" or "remembrance."',
            'mnemonic': 'Remember these as TWO words: SKERRICK (tiny amount in Australian slang) + SMRITI (Hindu memory texts).',
            'source': 'Claude'
        },
        'sketch': {
            'definition': 'Sketch refers to a rough, preliminary drawing or outline that captures the basic elements of a subject without detailed finishing. Artists use sketches to explore ideas, practice techniques, or plan larger works, emphasizing essential forms, proportions, and composition over fine details. The term also applies to brief written descriptions, preliminary plans, or short dramatic performances that outline key points without full development. In comedy, a sketch is a short scene or vignette performed for humorous effect. Sketching requires keen observation and the ability to distill complex subjects into their most important visual or conceptual elements, making it a fundamental skill in art, design, and creative planning.',
            'pronunciation': '/skɛtʃ/',
            'example_sentence': 'The artist made a quick _____ of the landscape before the lighting changed too dramatically.',
            'etymology': 'From Dutch "schets," from Italian "schizzo," meaning "splash" or "rough drawing," implying quick, spontaneous execution.',
            'mnemonic': 'Think "SKETCH = Start Creating, Keep it Extremely Tentative, Capture the Highlights" - a rough preliminary drawing.',
            'source': 'Claude'
        },
        'skeuomorph': {
            'definition': 'A skeuomorph is a design element that retains the ornamental or functional features of an older, often obsolete technology or material, even when those features are no longer necessary for the new version\'s function. This design principle helps users understand new technologies by referencing familiar objects from the past. Common examples include digital camera shutter sounds, computer desktop metaphors with folders and files, or smartphone icons that look like physical objects. Skeuomorphic design can ease the transition to new technologies by providing visual and conceptual bridges to familiar experiences. However, as users become more comfortable with digital interfaces, many designers have moved toward flatter, more abstract design approaches.',
            'pronunciation': '/ˈskjuːoʊˌmɔrf/',
            'example_sentence': 'The app\'s calculator icon was a classic _____, designed to look exactly like a traditional handheld calculator.',
            'etymology': 'From Greek "skeuos" (container, tool) + "morphē" (shape, form), literally meaning "tool-shaped."',
            'mnemonic': 'Think "SKEUO-MORPH = Simulating Known Equipment Using Old visual style, Making Objects Remember Past Habits" - new things designed to look like old things.',
            'source': 'Claude'
        },
        'skidded': {
            'definition': 'Skidded is the past tense of "skid," meaning to slide uncontrollably across a surface, typically due to loss of traction between wheels or feet and the ground. This usually occurs when surfaces are slippery from water, ice, oil, or loose materials, or when stopping or turning forces exceed the available friction. Vehicles commonly skid during sudden braking or sharp turns, especially in adverse weather conditions. The term also applies to feet slipping on smooth surfaces or objects sliding across floors. Understanding skidding is important for driving safety, as controlled responses to skids can prevent accidents, while panic reactions often worsen the situation.',
            'pronunciation': '/ˈskɪdəd/',
            'example_sentence': 'The car _____ on the icy road when the driver applied the brakes too suddenly.',
            'etymology': 'From "skid," possibly from Old Norse "skīth" meaning "stick of wood" or "ski," referring to sliding wooden runners.',
            'mnemonic': 'Think "SKID-DED = Slipping because of poor grip, lost control, Dangerously sliDing with Difficulty stopping" - slid uncontrollably.',
            'source': 'Claude'
        },
        'skiff': {
            'definition': 'A skiff is a small, shallow-draft boat designed for use in protected waters such as rivers, lakes, or coastal areas with calm conditions. These versatile watercraft are typically lightweight and easy to maneuver, making them ideal for fishing, transportation across short distances, or recreational boating. Skiffs can be powered by oars, small motors, or sails, and their shallow draft allows access to areas where deeper boats cannot go. Traditional skiffs were often built of wood, though modern versions may use fiberglass, aluminum, or inflatable materials. The simple, practical design of skiffs has made them popular among fishermen, hunters, and recreational boaters who need reliable, uncomplicated watercraft.',
            'pronunciation': '/skɪf/',
            'example_sentence': 'The fisherman paddled his small _____ into the shallow marsh where larger boats couldn\'t navigate.',
            'etymology': 'From French "esquif," from Old French "escuif," possibly from Germanic origin related to "ship."',
            'mnemonic': 'Think "SKIFF = Small Kayak-like watercraft, Ideal For Fishing in shallow water" - a small, shallow boat.',
            'source': 'Claude'
        },
        'skiing': {
            'definition': 'Skiing is a recreational and competitive sport involving gliding over snow on long, narrow skis attached to the feet, using poles for balance and propulsion. The activity encompasses various disciplines including alpine (downhill) skiing, cross-country skiing, ski jumping, and freestyle skiing, each requiring different techniques and equipment. Skiing originated thousands of years ago as a practical means of winter transportation in snowy regions, particularly Scandinavia. Modern skiing combines physical fitness, balance, coordination, and technique, offering both recreational enjoyment and competitive challenges. Popular ski destinations feature groomed slopes, ski lifts, and facilities that support winter tourism. Skiing provides excellent cardiovascular exercise while allowing participants to enjoy winter mountain environments.',
            'pronunciation': '/ˈskiɪŋ/',
            'example_sentence': 'The family planned their winter vacation around _____ at the mountain resort with fresh powder snow.',
            'etymology': 'From Norwegian "ski," from Old Norse "skīth" meaning "split piece of wood" or "stick," referring to the wooden runners.',
            'mnemonic': 'Think "SKI-ING = Sliding down snow with Keep-balance gear, Including poles for Navigation and Going fast" - gliding on snow with skis.',
            'source': 'Claude'
        },
        'skimmed': {
            'definition': 'Skimmed is the past tense of "skim," with multiple related meanings: removing the top layer of something (like cream from milk), reading quickly without deep attention to capture main points, or moving lightly and rapidly over a surface without penetrating deeply. In dairy processing, skimmed milk has had most fat content removed. When reading, skimming involves rapid scanning to identify key information without thorough comprehension. Physical skimming describes light contact with surfaces, such as a stone skipping across water or an aircraft flying close to the ground. The common thread involves surface-level interaction rather than deep penetration or thorough engagement.',
            'pronunciation': '/skɪmd/',
            'example_sentence': 'She _____ through the lengthy report to find the essential budget information before the meeting.',
            'etymology': 'From Middle English "skimmen," related to "scum," originally meaning to remove the scum or foam from liquid surfaces.',
            'mnemonic': 'Think "SKIM-MED = Surface level interaction, Keeping it Minimal, Moving across Efficiently without Deep engagement" - light, surface-level contact.',
            'source': 'Claude'
        },
        'skin': {
            'definition': 'Skin is the outer protective covering of humans and animals, serving as the body\'s largest organ with multiple vital functions including protection from environmental hazards, temperature regulation, sensation, and vitamin D synthesis. Human skin consists of three main layers: the epidermis (outer layer), dermis (middle layer containing hair follicles and sweat glands), and hypodermis (deeper fatty tissue). Skin acts as a barrier against bacteria, chemicals, and physical damage while allowing necessary exchanges of heat and moisture. The term extends to outer coverings of fruits, vegetables, and other objects. Skin health affects overall well-being and appearance, making skincare an important aspect of personal hygiene and health maintenance.',
            'pronunciation': '/skɪn/',
            'example_sentence': 'The dermatologist examined the patient\'s _____ for any signs of unusual changes or potential problems.',
            'etymology': 'From Old English "scinn," from Old Norse "skinn," related to "shin" and meaning "outer covering."',
            'mnemonic': 'Think "SKIN = Surface Keeping Internal organs protected, Natural barrier" - the protective outer covering of the body.',
            'source': 'Claude'
        },
        'skip': {
            'definition': 'Skip has several related meanings: to move with light, bouncing steps alternating feet; to omit or pass over something in sequence; or to cause an object to bounce across a surface, especially water. As a movement, skipping combines walking and hopping in a rhythmic, playful gait often associated with childhood joy and carefree behavior. In sequential contexts, skipping means deliberately leaving out items, steps, or stages, sometimes to save time or because certain elements are unnecessary. Stone skipping is a popular pastime involving throwing flat stones across water to achieve multiple bounces. The word suggests lightness, playfulness, and selective omission across its various uses.',
            'pronunciation': '/skɪp/',
            'example_sentence': 'The children decided to _____ down the path instead of walking, their laughter echoing through the park.',
            'etymology': 'From Middle English "skippen," possibly from Old Norse "skopa" meaning "to run" or from imitative origin.',
            'mnemonic': 'Think "SKIP = Step with light bouncing, Keep It Playful" or "leave out items, Keeping It short, Passing over" - light bouncing movement or omitting things.',
            'source': 'Claude'
        },
        'skipped': {
            'definition': 'Skipped is the past tense of "skip," indicating that someone moved with light, bouncing steps, omitted something from a sequence, or caused an object to bounce across a surface. The action might describe a child who skipped happily to school, a student who skipped a class, or someone who skipped stones across a pond. The word carries implications of intentional omission, playful movement, or the completed action of making something bounce repeatedly. Context determines whether skipped refers to physical movement, deliberate avoidance, or the act of making objects ricochet. The past tense form indicates these actions have already occurred.',
            'pronunciation': '/skɪpt/',
            'example_sentence': 'He _____ the boring lecture and went to the library to study for his upcoming exam instead.',
            'etymology': 'Past tense of "skip," from Middle English "skippen," possibly from Old Norse "skopa" or imitative origin.',
            'mnemonic': 'Think "SKIP-PED = Something was Kept out, Intentionally Passed over, or Playfully Executed as bouncing movement" - past tense of omitting or bouncing.',
            'source': 'Claude'
        },
        'skirmish': {
            'definition': 'A skirmish is a small-scale battle or brief clash between opposing forces, typically involving light troops or advance units rather than main armies. These limited engagements often serve as reconnaissance, harassment, or preliminary actions before larger battles. In military contexts, skirmishes help gather intelligence about enemy positions and strength while testing defenses. The term extends beyond warfare to describe any brief conflict, dispute, or competitive encounter between individuals or groups. Political skirmishes involve verbal battles or minor conflicts over issues. Sports commentators might describe intense but brief competitive exchanges as skirmishes. The word suggests limited scope, brief duration, and relatively minor stakes compared to major confrontations.',
            'pronunciation': '/ˈskɜrmɪʃ/',
            'example_sentence': 'The cavalry unit engaged in a brief _____ with enemy scouts before retreating to report their findings.',
            'etymology': 'From Old French "escrimir," meaning "to fence" or "to fight with swords," from Germanic "skirmjan" (to protect).',
            'mnemonic': 'Think "SKIR-MISH = Small Conflict, Keeping It Relatively Minor, Making It Short Hostilities" - a brief, small-scale battle.',
            'source': 'Claude'
        },
        'skydiving': {
            'definition': 'Skydiving is an extreme sport involving jumping from an aircraft at high altitude and free-falling through the air before deploying a parachute to slow descent for a safe landing. This adrenaline-fueled activity combines the thrill of free fall with the peaceful, controlled descent under an open parachute. Skydivers typically jump from altitudes between 10,000 and 15,000 feet, experiencing approximately 60 seconds of free fall at speeds around 120 mph. The sport requires extensive training, proper equipment, and adherence to strict safety protocols. Many people skydive for recreation, while others pursue it competitively in disciplines like formation skydiving, freestyle, and accuracy landing. Tandem jumps allow beginners to experience skydiving while attached to experienced instructors.',
            'pronunciation': '/ˈskaɪˌdaɪvɪŋ/',
            'example_sentence': 'For her 50th birthday, she decided to try _____ to experience the ultimate thrill of free-falling through the clouds.',
            'etymology': 'Compound word from "sky" + "diving," referring to diving through the sky from high altitude.',
            'mnemonic': 'Think "SKY-DIVING = SKY-high jumping, DIVing through air, Including parachute for safe landing" - jumping from aircraft and falling through sky.',
            'source': 'Claude'
        },
        'slab': {
            'definition': 'A slab is a thick, flat piece of solid material, typically stone, concrete, metal, or wood, used in construction, paving, or as work surfaces. Slabs serve various purposes: concrete slabs form building foundations and floors, stone slabs create countertops and walkways, and metal slabs provide industrial work surfaces. The term also applies to thick cuts of meat, cheese, or other foods, and to flat geological formations. In construction, slab-on-grade foundations are popular for their simplicity and cost-effectiveness. The key characteristics of slabs are their substantial thickness, flat surfaces, and solid composition, making them suitable for bearing weight and providing stable, level surfaces for various applications.',
            'pronunciation': '/slæb/',
            'example_sentence': 'The mason carefully positioned each stone _____ to create an attractive and durable patio surface.',
            'etymology': 'From Middle English "slabbe," possibly from Scandinavian origin, related to "slab" meaning a flat piece split off.',
            'mnemonic': 'Think "SLAB = Solid, Large, And Big flat piece" - a thick, flat piece of solid material.',
            'source': 'Claude'
        },
        'slabs': {
            'definition': 'Slabs is the plural form of "slab," referring to multiple thick, flat pieces of solid material such as stone, concrete, metal, or wood. These substantial pieces are commonly used in construction projects, landscaping, and industrial applications where durable, level surfaces are needed. Multiple slabs might form a large foundation, create an expansive patio, or provide work surfaces in a workshop. The plural form suggests larger projects or installations requiring numerous individual pieces working together to create functional surfaces. Different types of slabs serve various purposes: concrete slabs for structural support, stone slabs for decorative elements, and metal slabs for industrial applications.',
            'pronunciation': '/slæbz/',
            'example_sentence': 'The construction crew poured several concrete _____ to create the foundation for the new apartment building.',
            'etymology': 'Plural of "slab," from Middle English "slabbe," possibly from Scandinavian origin meaning flat pieces split off.',
            'mnemonic': 'Think "SLABS = Several Large And Big flat pieces" - multiple thick, flat pieces of solid material.',
            'source': 'Claude'
        },
        'slakes': {
            'definition': 'Slakes is the third-person singular present tense of "slake," meaning to satisfy or quench thirst, desires, or needs, typically through providing what is required. The term most commonly appears in the phrase "slake one\'s thirst," describing the act of drinking to relieve thirst completely. In chemistry, slaking refers to the process of combining quicklime (calcium oxide) with water to produce slaked lime (calcium hydroxide), an important reaction in construction and manufacturing. The word suggests thorough satisfaction or completion of a need rather than partial relief. Slaking implies a restorative process that brings something from a state of want or tension to fulfillment and relief.',
            'pronunciation': '/sleɪks/',
            'example_sentence': 'The cold mountain spring water _____ the hiker\'s thirst after the long, hot climb to the summit.',
            'etymology': 'From Old English "slacian," meaning "to slacken" or "to become slack," related to satisfying needs that create tension.',
            'mnemonic': 'Think "SLAKES = Satisfies Lack by giving what Alleviates, Keeps thirst Eliminated, Satisfies" - satisfies or quenches completely.',
            'source': 'Claude'
        },
        'slalom': {
            'definition': 'Slalom is a skiing discipline involving navigating a zigzag course marked by poles or gates, requiring quick turns and precise control as competitors weave between obstacles. The term originated in alpine skiing but has expanded to other sports including water skiing, windsurfing, skateboarding, and automobile racing. In slalom events, participants must pass through all gates in the correct sequence while maintaining speed and control. Missing a gate typically results in disqualification or time penalties. The sport emphasizes technical skill, agility, and the ability to make rapid directional changes while maintaining momentum. Slalom courses test competitors\' ability to combine speed with precision navigation through challenging obstacle patterns.',
            'pronunciation': '/ˈslɑləm/',
            'example_sentence': 'The Olympic skier trained daily on the _____ course, perfecting her technique for rapid turns between the gates.',
            'etymology': 'From Norwegian "slalåm," literally meaning "sloping track," from "sla" (sloping) + "låm" (track).',
            'mnemonic': 'Think "SLA-LOM = Skiing Left And right, around obstacles, Learning to Overcome the zigzag path quickly" - skiing in zigzag pattern around obstacles.',
            'source': 'Claude'
        },
        'slang': {
            'definition': 'Slang refers to informal language consisting of words and expressions that are more casual, playful, or culturally specific than standard vocabulary, often used by particular groups or subcultures to create identity and solidarity. Slang terms frequently originate from specific communities - whether based on age, profession, region, or interests - and may not be understood by outsiders. These expressions often carry emotional or cultural connotations beyond their literal meanings and tend to evolve rapidly, with new terms emerging while others become outdated. Slang serves important social functions: building group cohesion, expressing creativity, and providing fresh ways to articulate experiences that standard language might not capture effectively.',
            'pronunciation': '/slæŋ/',
            'example_sentence': 'The teenager used modern _____ that confused her grandparents but was perfectly understood by her friends.',
            'etymology': 'Origin uncertain, possibly from Norwegian "sleng" meaning "to sling" or "throw," referring to casual, thrown-off speech.',
            'mnemonic': 'Think "SLANG = Special Language for certain Groups" - informal, group-specific vocabulary.',
            'source': 'Claude'
        },
        'slate': {
            'definition': 'Slate is a fine-grained metamorphic rock formed from compressed shale or mudstone, prized for its ability to split into thin, flat sheets with smooth surfaces. This natural material has been used for centuries in roofing, flooring, writing surfaces, and decorative applications due to its durability, water resistance, and attractive appearance. The term also refers to a list of candidates for election, a clean beginning (as in "clean slate"), or the dark gray color characteristic of the stone. In film and television, a slate is a board displaying scene information used for organizing footage during editing. Educational slate boards were historically used for writing practice with chalk.',
            'pronunciation': '/sleɪt/',
            'example_sentence': 'The historic building featured a beautiful _____ roof that had weathered storms for over a century.',
            'etymology': 'From Old French "esclate," meaning "splinter" or "fragment," referring to the stone\'s tendency to split into flat pieces.',
            'mnemonic': 'Think "SLATE = Stone that\'s LAminaTed Excellently, splits into flat pieces" - rock that splits into flat sheets.',
            'source': 'Claude'
        },
        'slather': {
            'definition': 'Slather means to spread or apply something thickly and liberally, often in a somewhat careless or enthusiastic manner. The word typically describes applying substances like butter, cream, paint, or lotion in generous amounts rather than thin, careful layers. Slathering suggests abundance and lack of restraint in application, whether spreading peanut butter on bread, applying sunscreen before beach activities, or covering surfaces with paint. The term carries connotations of generosity and thoroughness, implying that enough of the substance has been applied to completely cover the intended surface. The action is often quick and informal rather than precise or measured.',
            'pronunciation': '/ˈslæðər/',
            'example_sentence': 'She decided to _____ butter on the warm bread rather than applying it sparingly.',
            'etymology': 'Possibly from dialectal "slather" meaning "to splash" or "to spread messily," of uncertain origin.',
            'mnemonic': 'Think "SLATHER = Spread Liberally And THickly Everywhere with Reckless abundance" - apply thickly and generously.',
            'source': 'Claude'
        },
        'sleek': {
            'definition': 'Sleek describes something that is smooth, glossy, and elegant in appearance, often suggesting refined design, excellent condition, or sophisticated styling. The term commonly applies to hair, animals, vehicles, or objects that exhibit a polished, streamlined quality that appeals to the eye and suggests efficiency or luxury. Sleek designs typically feature clean lines, minimal ornamentation, and surfaces that reflect light attractively. In describing animals, sleek often indicates health and good grooming, as in a sleek cat\'s shiny coat. When applied to technology or vehicles, sleek suggests modern, aerodynamic design that combines aesthetic appeal with functional efficiency.',
            'pronunciation': '/slik/',
            'example_sentence': 'The new sports car had a _____ design that turned heads wherever it was parked.',
            'etymology': 'From Middle English "slik," possibly from Old Norse "slīkr" meaning "smooth," related to "slick."',
            'mnemonic': 'Think "SLEEK = Smooth, Lustrous, Elegant, Excellent appearance, Kept polished" - smooth and elegantly styled.',
            'source': 'Claude'
        },
        'sleepy': {
            'definition': 'Sleepy describes the state of feeling drowsy, tired, or ready for sleep, characterized by heavy eyelids, reduced alertness, and the desire to rest. This condition can result from natural circadian rhythms, physical exhaustion, mental fatigue, or medical conditions affecting sleep patterns. Sleepy can also describe places or situations that are quiet, inactive, or conducive to rest, such as a sleepy village or a sleepy afternoon. The word suggests a peaceful, restful quality rather than energetic activity. Understanding sleepiness is important for safety, as drowsy driving or operating machinery while sleepy can be dangerous. Healthy sleep patterns help prevent excessive daytime sleepiness.',
            'pronunciation': '/ˈslipi/',
            'example_sentence': 'After the long flight, she felt too _____ to concentrate on work and decided to take a nap.',
            'etymology': 'From Old English "slǣpiġ," from "slǣp" (sleep) + "-y" suffix, meaning "inclined to sleep."',
            'mnemonic': 'Think "SLEEP-Y = ready for SLEEP, feeling drowsY and tired" - feeling tired and ready for sleep.',
            'source': 'Claude'
        },
        'slender': {
            'definition': 'Slender describes something that is thin, graceful, and elongated, often conveying elegance and delicacy rather than mere thinness. When applied to people, slender suggests an attractive, lean build that appears healthy and proportioned. The term can describe objects like slender tree branches, slender columns in architecture, or slender fingers that appear graceful and refined. Slender often carries positive connotations of elegance and refinement, distinguishing it from words like "thin" or "skinny" which might suggest frailty or inadequacy. In some contexts, slender can mean small in amount or degree, as in "slender chances" or "slender resources," indicating limited but not necessarily insufficient quantities.',
            'pronunciation': '/ˈslɛndər/',
            'example_sentence': 'The ballet dancer\'s _____ frame allowed her to move with exceptional grace and fluidity across the stage.',
            'etymology': 'From Middle English "slendre," possibly from Old French "esclendre" meaning "thin" or "slender."',
            'mnemonic': 'Think "SLENDER = Slim, Light, Elegant, Narrow, Delicate, Elongated, Refined" - thin and graceful.',
            'source': 'Claude'
        },
        'sliced': {
            'definition': 'Sliced is the past tense of "slice," meaning to have cut something into thin, flat pieces using a knife or similar cutting tool. This common food preparation technique creates uniform pieces that cook evenly, are easy to serve, or fit specific recipe requirements. Slicing can be done in various thicknesses depending on the intended use: thin slices for sandwiches, thick slices for grilling, or decorative slices for presentation. The term extends beyond food to describe cutting any material into flat pieces, such as sliced lumber or sliced geological specimens. Proper slicing technique involves consistent thickness, clean cuts, and attention to safety when using sharp tools.',
            'pronunciation': '/slaɪst/',
            'example_sentence': 'She _____ the fresh tomatoes for the salad, making sure each piece was uniform in thickness.',
            'etymology': 'Past tense of "slice," from Old French "esclice," meaning "a piece split off," from "esclicier" (to split).',
            'mnemonic': 'Think "SLIC-ED = Something was cut Like thin pieces, Including Consistent thickness, Every piece Divided" - cut into thin pieces.',
            'source': 'Claude'
        },
        'slide': {
            'definition': 'Slide can function as both a verb meaning to move smoothly across a surface without rolling, and as a noun referring to various objects including playground equipment, photographic transparencies, or presentation displays. As movement, sliding involves continuous contact with a surface while gliding rather than stepping or rolling. Children use playground slides to descend inclined surfaces for fun. In presentations, slides are individual screens or pages displaying information sequentially. The term also describes gradual changes or declines, as in sliding prices or sliding into bad habits. Musical instruments like trombones use slides to change pitch smoothly between notes.',
            'pronunciation': '/slaɪd/',
            'example_sentence': 'The children took turns going down the tall _____ at the playground while their parents watched nearby.',
            'etymology': 'From Old English "slīdan," meaning "to glide" or "to slip," related to "sled" and "sleigh."',
            'mnemonic': 'Think "SLIDE = Smooth movement Like glIding, Downward or across surfaces Easily" - smooth gliding movement.',
            'source': 'Claude'
        },
        'slimy': {
            'definition': 'Slimy describes something covered with or having the texture of slime - a slippery, viscous substance that feels wet and greasy to the touch. This physical characteristic often occurs naturally in certain animals like snails, slugs, and some fish, where slime provides protection and aids movement. The word also has metaphorical uses, describing people whose behavior is considered untrustworthy, insincere, or morally questionable. In this context, "slimy" suggests someone who is slippery in character, difficult to pin down, or engaging in underhanded activities. The negative connotations stem from the generally unpleasant tactile experience of touching actual slime.',
            'pronunciation': '/ˈslaɪmi/',
            'example_sentence': 'The children were fascinated but reluctant to touch the _____ garden slug they found under the rock.',
            'etymology': 'From "slime" + "-y" suffix, where "slime" comes from Old English "slīm," related to slippery substances.',
            'mnemonic': 'Think "SLIM-Y = SLippery, Including Mucus-like texture, Yucky to touch" - covered with slippery, viscous substance.',
            'source': 'Claude'
        },
        'slippery': {
            'definition': 'Slippery describes surfaces or conditions that are difficult to grip, hold, or walk on safely due to reduced friction, often caused by moisture, ice, oil, or smooth textures. This physical property can create dangerous situations where people or vehicles lose traction and control. The term extends metaphorically to describe people or situations that are hard to pin down, understand, or trust. A slippery person might be evasive, unreliable, or prone to changing positions to avoid commitment. Slippery slopes refer to situations where one action leads to increasingly problematic consequences. Understanding slippery conditions is crucial for safety in driving, walking, and handling objects.',
            'pronunciation': '/ˈslɪpəri/',
            'example_sentence': 'The wet bathroom tiles were so _____ that she had to hold the wall while getting out of the shower.',
            'etymology': 'From "slip" + "-er" + "-y," where "slip" comes from Middle Low German "slippen" meaning "to glide."',
            'mnemonic': 'Think "SLIP-PER-Y = causes people to SLIP PER every step, making it dangeroUS" - causing loss of grip or traction.',
            'source': 'Claude'
        },
        'slipshod': {
            'definition': 'Slipshod describes work, behavior, or appearance that is careless, sloppy, or done without proper attention to quality or detail. This adjective characterizes efforts that are hasty, poorly executed, or failing to meet reasonable standards of competence or care. Slipshod work might involve cutting corners, ignoring important steps, or accepting substandard results instead of striving for excellence. The term can apply to various contexts: slipshod construction that fails safety standards, slipshod research that lacks proper methodology, or slipshod appearance that suggests lack of self-care. The word implies criticism of inadequate effort or attention to proper procedures and quality control.',
            'pronunciation': '/ˈslɪpˌʃɑd/',
            'example_sentence': 'The inspector criticized the contractor\'s _____ workmanship, noting numerous safety violations and poor craftsmanship.',
            'etymology': 'Originally meant "wearing slippers or loose shoes," from "slip" + "shod" (wearing shoes), later extended to mean careless generally.',
            'mnemonic': 'Think "SLIP-SHOD = SLIP-ping standards, SHODdy work quality" - carelessly done with poor quality.',
            'source': 'Claude'
        },
        'slither': {
            'definition': 'Slither means to move smoothly and sinuously, like a snake gliding across the ground with a continuous, undulating motion that flows from side to side. This distinctive form of locomotion involves the entire body moving in coordinated waves without the use of legs or appendages. The word can describe the movement of actual snakes and similar creatures, or metaphorically refer to any smooth, sneaky, or serpentine movement. People might slither through tight spaces, under obstacles, or when trying to move stealthily. The term often carries connotations of stealth, fluidity, and sometimes something slightly unsettling or mysterious about the movement pattern.',
            'pronunciation': '/ˈslɪðər/',
            'example_sentence': 'The garden snake began to _____ quietly through the tall grass toward its hiding place under the rock.',
            'etymology': 'From Old English "slidrian," meaning "to slip" or "to slide," related to "slide" and describing smooth, gliding motion.',
            'mnemonic': 'Think "SLITHER = Slide LIke a snake, Together coordinated movement, Hissing and Elongated, Rippling" - snake-like sliding movement.',
            'source': 'Claude'
        },
        'slivers': {
            'definition': 'Slivers are thin, narrow pieces or fragments that have been cut, split, or broken off from a larger object, typically wood, metal, glass, or other solid materials. These small, sharp fragments can be problematic when they penetrate skin, causing minor injuries that are often called splinters. Slivers can result from cutting lumber, breaking glass, or working with materials that tend to fragment. The term also describes very thin strips or small portions of anything, such as slivers of cheese, slivers of light, or slivers of hope. The word emphasizes the narrow, elongated shape and typically small size of these fragments or portions.',
            'pronunciation': '/ˈslɪvərz/',
            'example_sentence': 'After working with the rough wood all day, he had several painful _____ embedded in his hands.',
            'etymology': 'From "sliver," from Middle English "sliveren," meaning "to split" or "to cleave," related to "cleave" and "split."',
            'mnemonic': 'Think "SLIVERS = Small pieces that are Long, thin, Including Very narrow fragments that hurt when they Enter the skin" - thin, sharp fragments.',
            'source': 'Claude'
        }
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            words = list(reader)
        
        print(f"Processing {len(words)} words from batch 161...")
        
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
        
        print(f"\nBatch 161 processing complete!")
        print(f"Successfully processed {len(processed_data)}/{len(words)} words")
        print(f"Output saved to: {output_file}")
        
        if combined_errors:
            print(f"\nCombined word errors detected: {len(combined_errors)}")
            for error in combined_errors:
                print(f"  - {error}")
        
    except Exception as e:
        print(f"Error processing batch 161: {str(e)}")
        raise

if __name__ == "__main__":
    main()