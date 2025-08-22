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
    input_file = os.path.join(script_dir, 'output', 'batch_162_words.csv')
    output_file = os.path.join(script_dir, 'output', 'batch_162_processed.csv')
    
    calculator = DifficultyCalculator()
    
    # Comprehensive word data with educational content
    word_data = {
        'slogan': {
            'definition': 'A slogan is a memorable phrase, motto, or tagline used to express an idea, promote a product, or rally support for a cause, designed to be easily remembered and repeated. Effective slogans capture the essence of a brand, political campaign, or movement in a few words that resonate with audiences and stick in their minds. These concise phrases often employ rhetorical devices like alliteration, rhyme, or rhythm to enhance memorability. Classic examples include "Just Do It" for Nike, "I Have a Dream" for civil rights, and "Yes We Can" for political campaigns. Slogans serve as powerful communication tools that can influence public opinion, consumer behavior, and social movements through their simplicity and emotional appeal.',
            'pronunciation': '/ˈsloʊɡən/',
            'example_sentence': 'The advertising team spent weeks crafting the perfect _____ that would capture the company\'s innovative spirit in just three words.',
            'etymology': 'From Scottish Gaelic "sluagh-ghairm" meaning "battle cry," from "sluagh" (army) + "gairm" (shout).',
            'mnemonic': 'Think "SLO-GAN = Short Line Or phrase that Gets Attention with memorable wording" - a memorable motto or phrase.',
            'source': 'Claude'
        },
        'sloop': {
            'definition': 'A sloop is a single-masted sailing vessel with a fore-and-aft rigged mainsail and a jib or headsail, representing one of the most popular and versatile sailboat configurations. This design provides excellent sailing performance with relatively simple operation, making sloops favorites among recreational sailors and racing enthusiasts. The single mast setup is easier to handle than multi-masted vessels while still providing good speed and maneuverability. Modern sloops range from small dinghies to large oceangoing yachts, with variations including fractional rigs and masthead rigs depending on sail configuration. The sloop\'s efficiency and ease of handling have made it the predominant sailboat design for pleasure sailing worldwide.',
            'pronunciation': '/slup/',
            'example_sentence': 'The experienced sailor preferred his 30-foot _____ for weekend cruising because it was easy to handle single-handedly.',
            'etymology': 'From Dutch "sloep," meaning a small sailing vessel, possibly related to "slupen" (to slip or glide).',
            'mnemonic': 'Think "SLOOP = Single-masted sailing boat, Light and Operating with One mast, Practical design" - one-masted sailboat.',
            'source': 'Claude'
        },
        'slouch': {
            'definition': 'Slouch refers to a drooping, careless posture where the body bends forward with rounded shoulders and a curved spine, often indicating laziness, fatigue, or lack of attention to proper posture. As a verb, slouching describes the act of sitting, standing, or walking with this poor posture. The term can also describe someone who is incompetent or lazy in their work or behavior. Good posture is important for physical health, professional appearance, and projecting confidence, while slouching can cause back problems and convey negative impressions. The word extends metaphorically to describe lackluster performance or effort in various activities.',
            'pronunciation': '/slaʊtʃ/',
            'example_sentence': 'The teacher reminded students not to _____ in their chairs during the important presentation.',
            'etymology': 'Of uncertain origin, possibly from Old Norse "slokr" meaning "slothful person" or related to "slump."',
            'mnemonic': 'Think "SLOUCH = Slumping posture, Lacking Organized stance, Under-confident posture, Careless Habits" - poor, drooping posture.',
            'source': 'Claude'
        },
        'slovenly': {
            'definition': 'Slovenly describes someone or something that is careless about appearance, cleanliness, or organization, characterized by untidiness, sloppiness, and lack of attention to proper standards. A slovenly person might have messy hair, wrinkled clothes, or poor hygiene habits, while slovenly work lacks care and attention to detail. The term suggests habitual neglect rather than temporary messiness, indicating a pattern of not maintaining proper standards. Slovenly behavior can affect professional opportunities, personal relationships, and self-perception. The concept emphasizes the importance of taking care in one\'s appearance, work quality, and living environment.',
            'pronunciation': '/ˈslʌvənli/',
            'example_sentence': 'His _____ appearance and messy workspace gave clients a poor impression of his professional capabilities.',
            'etymology': 'From "sloven" (a careless person) + "-ly" suffix, where "sloven" may come from Flemish "slof" meaning "careless."',
            'mnemonic': 'Think "SLOV-ENLY = SLOppy style, Very careless, ENtirely careless, Lacking tidiness, messy" - careless and untidy.',
            'source': 'Claude'
        },
        'slow': {
            'definition': 'Slow describes movement, progress, or action that occurs at a reduced speed or rate compared to normal, expected, or desired pace. This fundamental concept applies across many contexts: slow traffic moves below normal speed, slow learners need more time to understand concepts, and slow cooking uses low heat over extended periods. Slow can indicate deliberation and care, as in slow, thoughtful decision-making, or it can suggest problems, as in slow economic growth. The term also describes mental processing, reaction times, and the passage of time. Understanding when to go slow versus when speed is needed is important for safety, quality, and effectiveness.',
            'pronunciation': '/sloʊ/',
            'example_sentence': 'The chef used a _____ cooking method to ensure the flavors developed properly over several hours.',
            'etymology': 'From Old English "slāw," related to Old Norse "slǣr" and German "schlau," meaning "dull" or "blunt."',
            'mnemonic': 'Think "SLOW = Speed Less than Optimal Wanted pace" - moving at reduced speed.',
            'source': 'Claude'
        },
        'sluggardbedlam': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "sluggard" and "bedlam." A sluggard is a lazy, idle person who avoids work and exertion. Bedlam refers to a scene of noisy confusion or chaos, originally referring to the Bethlem Royal Hospital (Bedlam) in London. These are distinct concepts that should not be combined - one describing a lazy person and the other describing chaotic situations. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈslʌɡərd ˈbɛdləm/',
            'example_sentence': 'The teacher called him a _____ for avoiding all work, while the classroom erupted into complete _____ during the fire drill.',
            'etymology': 'Sluggard: from "slug" (slow creature) + "-ard" (one who does). Bedlam: from "Bethlem," corruption of Bethlehem Hospital in London.',
            'mnemonic': 'Remember these as TWO words: SLUGGARD (lazy person) + BEDLAM (noisy chaos).',
            'source': 'Claude'
        },
        'slumgullion': {
            'definition': 'Slumgullion is a hearty, simple stew traditionally made from whatever ingredients are available, often including meat, vegetables, and sometimes beans or grains, cooked together in one pot. This frontier-style dish originated during westward expansion in America when travelers and miners needed to create filling meals from limited, preserved ingredients. The term can also refer to any watery, unappetizing liquid or muddy mixture. Different regions have varying recipes for slumgullion, but the common theme is using available ingredients to create a nutritious, economical meal. The dish represents resourcefulness and the ability to create sustenance from simple, humble ingredients.',
            'pronunciation': '/slʌmˈɡʌljən/',
            'example_sentence': 'The camp cook prepared a hearty _____ using leftover beef, potatoes, and whatever vegetables remained from their supplies.',
            'etymology': 'American frontier slang of uncertain origin, possibly from "slum" (watery food) + "gullion" (variant of "scullion," a kitchen servant).',
            'mnemonic': 'Think "SLUM-GULLION = Simple stew made from Limited resources, Using whatever ingredients, Many different ingredients thrown together" - frontier stew made from available ingredients.',
            'source': 'Claude'
        },
        'slumped': {
            'definition': 'Slumped is the past tense of "slump," meaning to have fallen or drooped heavily, typically due to fatigue, exhaustion, loss of strength, or emotional defeat. The word can describe physical collapse, such as slumping in a chair when tired, or metaphorical decline, such as sales that have slumped. When someone slumps, they lose their upright posture and may appear defeated or overwhelmed. The term suggests a sudden or gradual loss of energy, support, or vitality rather than a controlled movement. Slumping can indicate both temporary fatigue requiring rest and more serious issues requiring attention or intervention.',
            'pronunciation': '/slʌmpt/',
            'example_sentence': 'After the long exam, she _____ in her chair, completely exhausted from hours of intense concentration.',
            'etymology': 'From Middle Low German "slumpen" meaning "to fall into a bog," related to sudden, heavy falling or sinking.',
            'mnemonic': 'Think "SLUMP-ED = Suddenly Lost strength, Unable to Maintain Posture, Extremely tired, Drooped heavily" - fell or drooped from exhaustion.',
            'source': 'Claude'
        },
        'slurry': {
            'definition': 'Slurry is a semi-liquid mixture consisting of fine particles suspended in water or another liquid, creating a thick, pourable consistency between solid and liquid states. This mixture appears in various industrial processes: cement slurry in construction, coal slurry in mining, and ceramic slurry in pottery. Agricultural slurry consists of animal waste mixed with water for fertilizer application. The suspension allows solid materials to be transported through pipes, mixed easily, or applied evenly. Slurries must be kept agitated to prevent settling, and their consistency can be adjusted by changing the ratio of solids to liquid. Understanding slurry properties is important in engineering, agriculture, and manufacturing.',
            'pronunciation': '/ˈslɜri/',
            'example_sentence': 'The construction crew pumped concrete _____ through long hoses to reach the upper floors of the building.',
            'etymology': 'From Middle English "slory," related to "slur" meaning "thin mud" or "liquid mixture."',
            'mnemonic': 'Think "SLUR-RY = Semi-Liquid mixture, Using fine particles, Relatively thick, Running through pipes easily" - thick liquid mixture with suspended particles.',
            'source': 'Claude'
        },
        'slush': {
            'definition': 'Slush refers to partially melted snow or ice that creates a wet, mushy mixture of ice crystals and water, typically occurring during temperature fluctuations around the freezing point. This sloppy, semi-liquid state creates challenging walking and driving conditions as it\'s neither solid nor liquid but a slippery, unpredictable combination. Slush forms during spring thaws, winter warming periods, or when snow encounters warmer surfaces. The term also describes any soft, watery mixture, such as flavored ice drinks called slushies. Understanding slush conditions is important for safety, as it can be more hazardous than either solid ice or clear water.',
            'pronunciation': '/slʌʃ/',
            'example_sentence': 'The warm afternoon sun turned the morning\'s fresh snow into treacherous _____ on the sidewalks.',
            'etymology': 'Probably from Scandinavian origin, related to Norwegian "slusk" meaning "slush" or "sludge."',
            'mnemonic': 'Think "SLUSH = Snow and ice that\'s Lost its solidity, Under-frozen, Semi-liquid, Half-melted" - partially melted snow and ice.',
            'source': 'Claude'
        },
        'small': {
            'definition': 'Small describes something that is limited in size, amount, degree, or importance compared to what is normal, average, or expected in its category. This fundamental descriptive concept helps us understand and categorize the world through relative size relationships. Small can refer to physical dimensions, quantities, significance, or scope. The perception of smallness depends on context - a small elephant is still much larger than a large mouse. Small businesses employ fewer people than large corporations, small problems require less attention than major issues, and small gestures can sometimes have large impacts. Understanding scale and relative size is crucial for communication, measurement, and decision-making.',
            'pronunciation': '/smɔl/',
            'example_sentence': 'The _____ café on the corner served the best coffee in the neighborhood despite its limited seating.',
            'etymology': 'From Old English "smæl," related to German "schmal," meaning "narrow" or "thin."',
            'mnemonic': 'Think "SMALL = Size Much smaller than All Large things" - limited in size or amount.',
            'source': 'Claude'
        },
        'smaller': {
            'definition': 'Smaller is the comparative form of "small," indicating that something is more limited in size, amount, or degree than another thing or than previously. This comparative adjective helps establish relationships between objects, quantities, or concepts by showing relative differences in scale. Smaller can describe physical dimensions, numerical values, importance levels, or any measurable characteristic. The comparison can be explicit (comparing two specific things) or implicit (compared to a general standard or previous state). Understanding comparative relationships is essential for analysis, decision-making, and describing changes over time or differences between options.',
            'pronunciation': '/ˈsmɔlər/',
            'example_sentence': 'The architect designed a _____ version of the original building to fit the constrained urban lot.',
            'etymology': 'From "small" + comparative suffix "-er," following standard English comparative formation.',
            'mnemonic': 'Think "SMALL-ER = More SMALL than something Else that\'s being compared to it" - more limited in size than another thing.',
            'source': 'Claude'
        },
        'smart': {
            'definition': 'Smart describes intelligence, cleverness, or the ability to learn quickly and solve problems effectively, though the term has multiple related meanings. A smart person demonstrates good judgment, quick thinking, and practical intelligence in various situations. Smart can also mean neat and fashionable in appearance, as in "smart attire." In modern usage, smart technology refers to devices that can respond to user input and adapt their behavior. The word can describe sharp physical pain or emotional hurt, as in "smarting from criticism." Smart choices show wisdom and foresight, while smart remarks might be cleverly witty or inappropriately sarcastic depending on context.',
            'pronunciation': '/smɑrt/',
            'example_sentence': 'The _____ student solved the complex math problem using an innovative approach that impressed the teacher.',
            'etymology': 'From Old English "smeortan" meaning "to cause sharp pain," later extended to mean "quick" or "clever."',
            'mnemonic': 'Think "SMART = Shows Mental Ability, Really Thoughtful and intelligent" - demonstrating intelligence and quick thinking.',
            'source': 'Claude'
        },
        'smattering': {
            'definition': 'Smattering refers to a small, superficial amount of knowledge or understanding about a subject, suggesting familiarity without depth or expertise. This term describes the kind of limited knowledge gained from brief exposure or casual study rather than thorough education or extensive experience. A smattering might come from conversations, reading headlines, or basic courses without comprehensive study. While a smattering can provide useful general awareness, it\'s insufficient for expertise or professional application. The word can also describe a small, scattered amount of anything, such as a smattering of applause or a smattering of rain. The concept highlights the difference between surface-level familiarity and genuine understanding.',
            'pronunciation': '/ˈsmætərɪŋ/',
            'example_sentence': 'Although he had only a _____ of French from high school, he managed to order dinner successfully in Paris.',
            'etymology': 'From "smatter" meaning "to talk superficially," possibly from Middle English "smateren" (to prattle).',
            'mnemonic': 'Think "SMAT-TERING = Small Amount That\'s just skimming the surface, Thin knowledge, Extremely limited understanding" - superficial knowledge.',
            'source': 'Claude'
        },
        'smell': {
            'definition': 'Smell functions as both a noun referring to the sense that detects airborne chemical compounds through the nose, and as a verb meaning to perceive odors through this sensory system. The sense of smell plays crucial roles in detecting danger, enjoying food, triggering memories, and influencing emotions through the connection between olfactory receptors and the brain\'s limbic system. Smells can be pleasant (flowers, baking bread), unpleasant (garbage, smoke), or neutral (fresh air). This chemical sense helps identify food quality, environmental hazards, and social information. The human ability to distinguish thousands of different odors makes smell an important but often underappreciated sense that significantly impacts daily life and survival.',
            'pronunciation': '/smɛl/',
            'example_sentence': 'The delicious _____ of fresh bread baking in the oven made everyone hungry for dinner.',
            'etymology': 'From Middle English "smellen," possibly from Old English "smiellan," related to the sense of detecting odors.',
            'mnemonic': 'Think "SMELL = Sense that detects Molecules in air through nasal passages, Evaluating odors" - detecting odors through the nose.',
            'source': 'Claude'
        },
        'smellfungus': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "smell" and "fungus." Smell is the sense that detects airborne chemical compounds through the nose, while fungus refers to organisms like mushrooms, molds, and yeasts that lack chlorophyll and obtain nutrients by decomposing organic matter. These are distinct concepts - one being a sensory function and the other being a type of organism. However, there may be a historical literary reference to "Smelfungus," a character created by Laurence Sterne representing a fault-finding traveler. The error likely occurred during document scanning or data processing.',
            'pronunciation': '/smɛl ˈfʌŋɡəs/',
            'example_sentence': 'You can _____ the musty _____ growing in the damp basement corner.',
            'etymology': 'Smell: from Middle English "smellen." Fungus: from Latin "fungus" meaning "mushroom" or "sponge."',
            'mnemonic': 'Remember these as TWO words: SMELL (detect odors) + FUNGUS (mushroom-like organism).',
            'source': 'Claude'
        },
        'smelters': {
            'definition': 'Smelters are industrial facilities where metals are extracted from their ores through the process of smelting, which involves heating ore to high temperatures to separate the desired metal from waste rock and other materials. These operations typically use furnaces, flux materials, and chemical reduction to produce pure or refined metals like copper, iron, aluminum, or lead. Smelters represent crucial links in the industrial supply chain, converting raw materials into usable metals for manufacturing. The process requires significant energy input and produces both valuable metals and waste products that must be managed carefully. Modern smelters employ pollution control technologies to minimize environmental impact while maintaining efficient metal production.',
            'pronunciation': '/ˈsmɛltərz/',
            'example_sentence': 'The copper _____ operated around the clock to meet the demand for refined metal from electronics manufacturers.',
            'etymology': 'From "smelt" (to melt ore to extract metal) + "-er" (one who does) + "-s" (plural), from Middle Dutch "smelten."',
            'mnemonic': 'Think "SMELT-ERS = facilities that SMELT metal from ores, Extracting Raw materials, Separating metals" - industrial metal extraction facilities.',
            'source': 'Claude'
        },
        'smiled': {
            'definition': 'Smiled is the past tense of "smile," meaning to have formed a pleased, kind, or amused facial expression by turning up the corners of the mouth, often accompanied by brightening of the eyes. This universal human expression typically indicates happiness, friendliness, amusement, or social acknowledgment. Smiling can be voluntary (deliberately showing pleasure or politeness) or involuntary (automatic response to positive emotions). The act of smiling has psychological benefits, potentially improving mood and reducing stress, while also serving important social functions by signaling approachability and positive intentions to others. Smiles can range from subtle lip movements to broad, enthusiastic expressions.',
            'pronunciation': '/smaɪld/',
            'example_sentence': 'She _____ warmly when she saw her old friend unexpectedly at the coffee shop.',
            'etymology': 'Past tense of "smile," from Middle English "smilen," possibly from Scandinavian origin meaning "to smile."',
            'mnemonic': 'Think "SMIL-ED = Showed happiness by turning up corners of mouth, Making a pleasant Expression, Displayed joy" - made a happy facial expression.',
            'source': 'Claude'
        },
        'smirk': {
            'definition': 'Smirk is a facial expression characterized by a conceited, knowing, or slightly mocking smile that suggests superiority, self-satisfaction, or secret amusement at someone else\'s expense. Unlike a genuine smile that conveys warmth and friendliness, a smirk often appears smug or condescending, indicating that the person feels they have an advantage or know something others don\'t. This expression can irritate others because it suggests arrogance or hidden mockery. Smirks frequently appear when someone feels clever, vindicated, or amused by another person\'s misfortune or mistake. The subtle nature of smirks makes them particularly effective at conveying disdain while maintaining plausible deniability.',
            'pronunciation': '/smɜrk/',
            'example_sentence': 'His annoying _____ after winning the argument made it clear he was more interested in being right than finding solutions.',
            'etymology': 'From Old English "smearcian" meaning "to smile in an affected manner," related to "smirk" as self-satisfied expression.',
            'mnemonic': 'Think "SMIRK = Smug smile, Making fun Indirectly, Really conceited, Knowing expression" - conceited, mocking smile.',
            'source': 'Claude'
        },
        'smite': {
            'definition': 'Smite is an archaic or literary verb meaning to strike forcefully, attack with great power, or defeat decisively, often with implications of divine punishment or righteous retribution. In religious and mythological contexts, deities smite evildoers with lightning, plagues, or other supernatural forces. The word can also mean to be suddenly affected by strong emotion, as in being "smitten" with love or admiration. Modern usage sometimes employs "smite" humorously or dramatically to describe overwhelming defeat or powerful impact. The term carries connotations of swift, decisive action and often implies that the striking is deserved or justified by the target\'s wrongdoing.',
            'pronunciation': '/smaɪt/',
            'example_sentence': 'In the ancient tale, the gods would _____ those who showed hubris and defied divine will.',
            'etymology': 'From Old English "smītan" meaning "to smear" or "to strike," related to German "schmeissen" (to throw).',
            'mnemonic': 'Think "SMITE = Strike Mightily with Intent To punish Evildoers" - strike forcefully, often as punishment.',
            'source': 'Claude'
        },
        'smithereens': {
            'definition': 'Smithereens refers to small fragments or pieces that result from something being completely destroyed, shattered, or broken apart, typically used in the phrase "blown to smithereens" or "smashed to smithereens." This colorful term emphasizes total destruction where the original object is reduced to tiny, scattered pieces that cannot be easily reassembled. The word suggests violent, thorough destruction rather than careful breaking or minor damage. Smithereens implies that the fragments are so small and numerous that recovering or repairing the original item is impossible. The term adds dramatic emphasis to descriptions of destruction, whether from explosions, impacts, or other forceful events.',
            'pronunciation': '/ˌsmɪðəˈrinz/',
            'example_sentence': 'The vase fell from the high shelf and shattered into _____, leaving tiny pieces scattered across the floor.',
            'etymology': 'From Irish "smidirín," diminutive of "smiodar" meaning "fragment," related to complete destruction into small pieces.',
            'mnemonic': 'Think "SMITH-EREENS = Smashed Into Tiny Hundreds of fragments, Everything Reduced to tiny pieces" - completely shattered into small fragments.',
            'source': 'Claude'
        },
        'smithereenscurator': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "smithereens" and "curator." Smithereens refers to small fragments or pieces resulting from complete destruction or shattering. A curator is a professional responsible for managing, organizing, and overseeing collections in museums, galleries, libraries, or other cultural institutions. These are completely unrelated concepts - one describing destruction and the other describing cultural preservation. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˌsmɪðəˈrinz kjʊˈreɪtər/',
            'example_sentence': 'The ancient pot was broken into _____, and the museum _____ carefully cataloged each fragment for potential restoration.',
            'etymology': 'Smithereens: from Irish "smidirín" (fragment). Curator: from Latin "curator" (caretaker), from "curare" (to take care of).',
            'mnemonic': 'Remember these as TWO words: SMITHEREENS (tiny fragments from destruction) + CURATOR (museum professional).',
            'source': 'Claude'
        },
        'smock': {
            'definition': 'A smock is a loose-fitting protective garment worn over regular clothing to keep it clean during work, traditionally featuring a simple, practical design that covers the torso and sometimes extends to mid-thigh or knee length. Originally associated with agricultural workers and craftspeople, smocks protected clothing from dirt, paint, chemicals, or other materials encountered during labor. Modern smocks include medical scrubs, artist\'s aprons, and laboratory coats, all serving the primary function of protection while allowing freedom of movement. The garment typically features easy-care fabrics, simple construction, and sometimes pockets for tools or supplies. Smocks represent the practical human need to protect valuable clothing while working.',
            'pronunciation': '/smɑk/',
            'example_sentence': 'The art teacher put on her paint-splattered _____ before demonstrating watercolor techniques to the class.',
            'etymology': 'From Old English "smocc," meaning "loose garment," related to the idea of a protective outer layer.',
            'mnemonic': 'Think "SMOCK = Simple protective garment, Made to cover Ordinary Clothes, Keeping them clean" - protective work garment.',
            'source': 'Claude'
        },
        'smoldering': {
            'definition': 'Smoldering describes the process of burning slowly without flame, producing smoke and heat while consuming material gradually over extended periods. This type of combustion occurs when there\'s insufficient oxygen for open flame but enough heat to maintain chemical decomposition. Smoldering can be dangerous because it\'s less obvious than flaming fires but can persist for hours or days, potentially rekindling into open flame when conditions change. The term also applies metaphorically to emotions or situations that persist at low intensity but could intensify suddenly, such as smoldering anger or smoldering romantic tension. Smoldering represents the middle ground between complete extinguishment and active burning.',
            'pronunciation': '/ˈsmoʊldərɪŋ/',
            'example_sentence': 'The campfire appeared extinguished, but _____ embers hidden in the ashes reignited when the wind picked up.',
            'etymology': 'From Middle English "smolderen," possibly from "smolder" related to "smother," meaning to burn without flame.',
            'mnemonic': 'Think "SMOL-DERING = SMOLdering fire burning without flames, Developing heat Even while appearing dead" - burning slowly without flame.',
            'source': 'Claude'
        },
        'smooshed': {
            'definition': 'Smooshed is the past tense of "smoosh," an informal verb meaning to squash, compress, or deform something by applying pressure, typically resulting in a flattened or misshapen form. This playful word often describes accidental damage to soft or malleable objects, such as stepping on a sandwich, sitting on a hat, or crushing delicate items. Smooshing can be intentional, like smooshing clay for pottery, or unintentional, like finding a smooshed banana in a backpack. The word conveys a sense of gentle or moderate compression rather than violent destruction, often with slightly humorous or endearing connotations. The result is usually messier or less organized than the original form.',
            'pronunciation': '/smuʃt/',
            'example_sentence': 'She discovered that her beautiful birthday cake had been _____ when someone accidentally placed a heavy box on top of it.',
            'etymology': 'Informal past tense of "smoosh," possibly a blend of "smash" and "squish," representing gentle compression.',
            'mnemonic': 'Think "SMOOSH-ED = Something was Mashed by pressure, Objects Obtained a Squashed form, Happened to flatten Everything" - flattened by pressure.',
            'source': 'Claude'
        },
        'smooth': {
            'definition': 'Smooth describes a surface or texture that is even, regular, and free from roughness, bumps, or irregularities, creating a pleasing tactile experience when touched. The concept extends beyond physical texture to describe movement that is fluid and uninterrupted, processes that proceed without problems or obstacles, and personalities that are suave or sophisticated. Smooth can characterize sounds that are pleasant and harmonious, transitions that are seamless, or social interactions that are effortless and comfortable. In cooking, smooth sauces have uniform consistency without lumps. The quality of smoothness often indicates refinement, skill, or careful preparation in various contexts.',
            'pronunciation': '/smuð/',
            'example_sentence': 'The carpenter sanded the wood until it had a perfectly _____ finish that felt like silk to the touch.',
            'etymology': 'From Old English "smōth," related to Old High German "smōdi," meaning "smooth" or "level."',
            'mnemonic': 'Think "SMOOTH = Surface without bumps, Maintaining One consistent texture, Objects That Have no roughness" - even and regular surface.',
            'source': 'Claude'
        },
        'smoother': {
            'definition': 'Smoother is the comparative form of "smooth," indicating that something has an even more regular, refined, or fluid quality than another thing or than previously. This comparison can apply to physical surfaces that feel more pleasant to touch, movements that are more graceful and flowing, processes that operate with fewer disruptions, or personalities that are more suave and sophisticated. A smoother operation has fewer problems, smoother skin has fewer blemishes, and smoother music has better harmony. The comparative form helps establish quality relationships and describe improvements or differences in the degree of smoothness across various contexts.',
            'pronunciation': '/ˈsmuðər/',
            'example_sentence': 'The new highway provided a much _____ ride than the old, pothole-filled road they replaced.',
            'etymology': 'From "smooth" + comparative suffix "-er," following standard English comparative formation.',
            'mnemonic': 'Think "SMOOTH-ER = More SMOOTH than something Else being compared" - more even or refined than another thing.',
            'source': 'Claude'
        },
        'smorgasbord': {
            'definition': 'Smorgasbord refers to a buffet-style meal featuring a wide variety of hot and cold dishes arranged on a table for self-service, originating from Swedish cuisine where it traditionally includes fish, meats, salads, and other specialties. The term has expanded metaphorically to describe any extensive array or variety of options, choices, or elements available for selection. A smorgasbord offers abundance and variety, allowing people to choose according to their preferences and appetites. Modern usage applies the concept to any situation offering multiple options: a smorgasbord of entertainment choices, educational opportunities, or business services. The word emphasizes both variety and the freedom to select from available options.',
            'pronunciation': '/ˈsmɔrɡəsˌbɔrd/',
            'example_sentence': 'The conference offered a _____ of workshops, allowing attendees to customize their learning experience.',
            'etymology': 'From Swedish "smörgåsbord," literally "bread and butter table," from "smörgås" (open sandwich) + "bord" (table).',
            'mnemonic': 'Think "SMOR-GAS-BORD = Swedish MORning meal, Great Array of food, Served on a Big dining table" - varied buffet with many choices.',
            'source': 'Claude'
        },
        'smouldering': {
            'definition': 'Smouldering is the British spelling of "smoldering," describing the process of burning slowly without flame, producing smoke and heat while consuming material gradually over extended periods. This type of combustion occurs when there\'s insufficient oxygen for open flame but enough heat to maintain chemical decomposition. Smouldering can persist for hours or days and may reignite into open flame when oxygen becomes available. The term also applies metaphorically to emotions or situations that persist at low intensity but could intensify suddenly, such as smouldering resentment or romantic tension. This spelling variation reflects British English conventions while maintaining the same meaning as the American spelling.',
            'pronunciation': '/ˈsmoʊldərɪŋ/',
            'example_sentence': 'The ruins of the building were still _____ three days after the fire, requiring constant monitoring by firefighters.',
            'etymology': 'British spelling of "smoldering," from Middle English "smolderen," meaning to burn without flame.',
            'mnemonic': 'Think "SMOUL-DERING = SMOking fire burning without flames, Using Limited oxygen, Developing heat Even while appearing dormant" - British spelling of slow burning.',
            'source': 'Claude'
        },
        'smriti': {
            'definition': 'Smriti is a Sanskrit term meaning "that which is remembered" or "memory," referring to a category of Hindu religious texts that are considered to be based on human memory and interpretation of divine knowledge, as opposed to shruti (divine revelation). Smriti texts include the epics (Ramayana and Mahabharata), Puranas, Dharma Shastras, and various law books that provide guidance for religious practice, social conduct, and moral behavior. These texts are considered authoritative but secondary to shruti texts like the Vedas. Smriti literature plays a crucial role in preserving cultural traditions, ethical teachings, and practical guidance for Hindu religious and social life, representing the human effort to interpret and apply divine principles.',
            'pronunciation': '/ˈsmrɪti/',
            'example_sentence': 'The scholar spent years studying _____ texts to understand the evolution of Hindu legal and ethical traditions.',
            'etymology': 'From Sanskrit "smṛti," from the root "smṛ" meaning "to remember," related to memory and recollection.',
            'mnemonic': 'Think "SMRI-TI = Sacred Memory texts, Religious Interpretations by humans, Traditional Instructions" - Hindu texts based on memory and tradition.',
            'source': 'Claude'
        },
        'smrti': {
            'definition': 'Smrti is an alternative transliteration of "smriti," a Sanskrit term meaning "memory" or "that which is remembered," referring to Hindu religious texts based on human memory and interpretation rather than direct divine revelation. These texts include epics, law books, and traditional stories that guide religious practice and social behavior. Smrti represents the human effort to preserve, interpret, and apply divine knowledge through successive generations. Unlike shruti texts which are considered directly revealed, smrti texts acknowledge their human authorship while maintaining religious authority. The slight spelling variation reflects different systems of romanizing Sanskrit but refers to the same important category of Hindu religious literature.',
            'pronunciation': '/ˈsmrɪti/',
            'example_sentence': 'The religious teacher explained how _____ texts complement the revealed scriptures by providing practical guidance for daily life.',
            'etymology': 'Alternative transliteration of Sanskrit "smṛti," from "smṛ" (to remember), meaning memory or remembered knowledge.',
            'mnemonic': 'Think "SMR-TI = Sacred Memory texts, Religious Traditions by humans, Instructions based on remembrance" - Hindu tradition texts based on memory.',
            'source': 'Claude'
        },
        'smudge': {
            'definition': 'Smudge refers to a dirty mark, stain, or blurred area created by smearing, rubbing, or imperfect application of substances like ink, paint, makeup, or dirt. As a verb, smudging means to make such marks or to blur clear lines and edges through contact or movement. Smudges often occur accidentally when wet materials are touched or when clean surfaces contact dirty ones. The term also applies to intentional techniques in art where edges are softened or blended for specific effects. In some Native American traditions, smudging refers to burning sacred herbs for spiritual cleansing. Understanding smudging helps in both preventing unwanted marks and creating desired artistic effects.',
            'pronunciation': '/smʌdʒ/',
            'example_sentence': 'She noticed an ink _____ on her important document just before the meeting began.',
            'etymology': 'From Middle English "smogen," possibly related to "smoke," meaning to make dirty marks or blur.',
            'mnemonic': 'Think "SMUDGE = Smearing creates Marks, Unclear lines, Dirty marks, Getting Everything blurred" - dirty mark from smearing.',
            'source': 'Claude'
        },
        'smug': {
            'definition': 'Smug describes an attitude of excessive self-satisfaction, self-righteousness, or complacency, often displayed through facial expressions, tone of voice, or behavior that suggests superiority over others. A smug person typically feels pleased with themselves in an annoying way, believing they are better, smarter, or more virtuous than those around them. This attitude often involves looking down on others while maintaining an air of false modesty or condescension. Smugness can be particularly irritating because it combines arrogance with self-righteousness, making the person appear both conceited and morally superior. The behavior often reflects a lack of genuine humility or empathy for others.',
            'pronunciation': '/smʌɡ/',
            'example_sentence': 'His _____ expression after proving everyone wrong made it clear he cared more about being right than solving the problem.',
            'etymology': 'From Low German "smuk" meaning "neat" or "trim," later developing the sense of self-satisfied appearance.',
            'mnemonic': 'Think "SMUG = Self-satisfied, Making everyone Uncomfortable with arrogance, Generally annoying attitude" - excessively self-satisfied.',
            'source': 'Claude'
        },
        'snack': {
            'definition': 'Snack refers to a small portion of food eaten between regular meals, typically to satisfy hunger, provide quick energy, or simply for enjoyment. Snacks are usually smaller and less formal than main meals, often consisting of convenient, portable foods that require little or no preparation. Common snacks include fruits, nuts, crackers, chips, or small sandwiches. The timing of snacks varies among cultures and individuals, but they often occur mid-morning, mid-afternoon, or evening. Healthy snacking can help maintain steady blood sugar levels and energy throughout the day, while excessive or unhealthy snacking may contribute to weight gain or interfere with appetite for regular meals.',
            'pronunciation': '/snæk/',
            'example_sentence': 'She packed a healthy _____ of apple slices and almonds to eat during her afternoon break.',
            'etymology': 'From Middle Dutch "snacken" meaning "to bite" or "to snap," referring to quick, small bites of food.',
            'mnemonic': 'Think "SNACK = Small Nutritious Amount between meals, Convenient to eat, Keeps hunger away" - small food portion between meals.',
            'source': 'Claude'
        },
        'snail': {
            'definition': 'Snail refers to a gastropod mollusk characterized by a coiled shell, soft body, and distinctively slow movement using a muscular foot that secretes slime for locomotion. These creatures exist in terrestrial, freshwater, and marine environments, with land snails being most familiar to people. Snails play important ecological roles as decomposers, food sources for other animals, and sometimes as agricultural pests. Their shells provide protection from predators and environmental stress, while their tentacles carry eyes and chemoreceptors for navigation. The phrase "at a snail\'s pace" has become synonymous with extremely slow movement. Some snail species are considered culinary delicacies, particularly in French cuisine.',
            'pronunciation': '/sneɪl/',
            'example_sentence': 'The garden _____ slowly crossed the wet sidewalk, leaving a silvery trail of slime behind it.',
            'etymology': 'From Old English "snægl," related to German "Schnecke," referring to the spiral-shelled gastropod.',
            'mnemonic': 'Think "SNAIL = Slow creature with Nasty slime, Always carrying its shell, In gardens Leaving trails" - slow-moving shelled gastropod.',
            'source': 'Claude'
        },
        'snake': {
            'definition': 'Snake refers to a legless reptile with an elongated, cylindrical body covered in scales, capable of moving through undulating motions and found in diverse habitats worldwide. These carnivorous animals vary greatly in size, from tiny thread snakes to massive pythons, and employ various hunting strategies including constriction and venom injection. Snakes play crucial ecological roles as both predators and prey, helping control rodent populations while serving as food for birds, mammals, and other animals. Cultural attitudes toward snakes vary widely, from fear and revulsion to reverence and worship in different societies. The term also applies metaphorically to describe treacherous people or winding paths.',
            'pronunciation': '/sneɪk/',
            'example_sentence': 'The harmless garden _____ helped control the mouse population around the barn.',
            'etymology': 'From Old English "snaca," related to Old Norse "snākr," referring to the legless reptile.',
            'mnemonic': 'Think "SNAKE = Slithering reptile, No legs for movement, Always using undulation, Keeping close to ground, Elongated body" - legless reptile that slithers.',
            'source': 'Claude'
        },
        'snap': {
            'definition': 'Snap has multiple related meanings: to break suddenly with a sharp cracking sound, to move or act quickly and decisively, to take a photograph, or to fasten with a snap fastener. The word can describe physical breaking under stress, emotional breaking under pressure, quick movements or actions, or the sound produced by sudden separation or impact. In photography, taking a snap means capturing a quick, informal picture. Snap decisions are made rapidly without lengthy deliberation. The versatility of this word makes it useful across many contexts, from describing mechanical failures to describing energetic actions or quick responses.',
            'pronunciation': '/snæp/',
            'example_sentence': 'The dry twig began to _____ under the hiker\'s weight as she stepped carefully across the fallen log.',
            'etymology': 'From Middle Dutch "snappen" meaning "to snap at" or "to bite," imitative of the sharp sound.',
            'mnemonic': 'Think "SNAP = Sharp sound when something breaks, Naturally quick action, Always sudden, Produces cracking noise" - sudden breaking or quick action.',
            'source': 'Claude'
        },
        'snarl': {
            'definition': 'Snarl describes both an aggressive vocal sound made by animals (particularly dogs and cats) when threatening or angry, and a tangled, confused mass of threads, hair, or other materials. As an animal behavior, snarling involves baring teeth while making low, menacing sounds to warn of potential attack. As a noun referring to tangles, snarls create complicated knots that are difficult to untangle. The word also applies to traffic conditions where vehicles become backed up and movement is slow or impossible. Metaphorically, snarling can describe human expressions or voices that convey anger, irritation, or hostility through tone and facial expression.',
            'pronunciation': '/snɑrl/',
            'example_sentence': 'The protective dog began to _____ when the stranger approached too close to the children.',
            'etymology': 'From Middle English "snarren," possibly imitative of the aggressive sound, later extended to mean tangled mass.',
            'mnemonic': 'Think "SNARL = Sound showing anger, Nasty warning noise, Animals make it when Agitated, Really threatening" - aggressive sound or tangle.',
            'source': 'Claude'
        },
        'snazzy': {
            'definition': 'Snazzy is an informal adjective describing something that is stylish, fashionable, attractive, or impressive in appearance, often with a sense of modern flair or eye-catching design. This upbeat word suggests something that stands out positively due to its smart appearance, sophisticated style, or appealing visual qualities. Snazzy can describe clothing, cars, gadgets, decorations, or any object that has an attractive, contemporary look. The term carries positive connotations of style and taste, suggesting that something is not only functional but also aesthetically pleasing and up-to-date. Snazzy items often reflect current trends or innovative design approaches that make them particularly appealing.',
            'pronunciation': '/ˈsnæzi/',
            'example_sentence': 'She wore a _____ new dress to the party that perfectly complemented her confident personality.',
            'etymology': 'American slang from the 1930s, possibly a blend of "snappy" and "jazzy," both meaning stylish or attractive.',
            'mnemonic': 'Think "SNAZ-ZY = Stylish, Nice And attractive, Zippy design, attractively modern" - stylish and attractive.',
            'source': 'Claude'
        },
        'sneer': {
            'definition': 'Sneer refers to a contemptuous or mocking facial expression or tone of voice that shows scorn, disdain, or superior amusement at someone else\'s expense. This expression typically involves raising one side of the upper lip while narrowing the eyes, creating a look of disgust or derision. Sneering can be accompanied by sarcastic comments or dismissive gestures that reinforce the message of superiority or contempt. The behavior often reflects arrogance, prejudice, or the desire to belittle others. Sneers are particularly effective at conveying social rejection or intellectual condescension, making them powerful tools for expressing disapproval or establishing social hierarchy.',
            'pronunciation': '/snɪr/',
            'example_sentence': 'The critic\'s _____ at the amateur performance revealed more about his own arrogance than the quality of the show.',
            'etymology': 'Possibly from Middle English "sneren," related to "snarl," meaning to show contempt through facial expression.',
            'mnemonic': 'Think "SNEER = Scornful expression, Nasty attitude, Everyone feels the contempt, Really dismissive" - contemptuous facial expression.',
            'source': 'Claude'
        },
        'snell': {
            'definition': 'Snell is a Scottish and Northern English dialect word meaning keen, sharp, or bitterly cold, particularly when describing weather conditions like wind or air temperature. This adjective captures the penetrating quality of cold that seems to cut through clothing and chill to the bone. A snell wind is one that is not just cold but piercingly sharp and unforgiving. The word can also describe anything that is acute, severe, or intensely felt. In fishing terminology, a snell is also a length of line attached to a fishhook. The dialect nature of this word makes it particularly evocative of harsh northern climates and traditional ways of describing severe weather.',
            'pronunciation': '/snɛl/',
            'example_sentence': 'The _____ wind from the north made everyone hurry indoors to escape the bitter cold.',
            'etymology': 'From Old English "snell" meaning "keen" or "sharp," related to Old Norse "snjallr" (bold, keen).',
            'mnemonic': 'Think "SNELL = Sharp, bitterly cold weather, Northern dialect word, Everyone feels the cold, Literally cutting wind" - keen, bitterly cold.',
            'source': 'Claude'
        },
        'sniffle': {
            'definition': 'Sniffle refers to the act of breathing in audibly through the nose in short, repeated actions, typically due to nasal congestion, crying, or cold weather. This sound occurs when nasal passages are partially blocked by mucus or when trying to prevent nasal discharge from dripping. Sniffling often accompanies colds, allergies, emotional crying, or exposure to irritants. The action serves to clear nasal passages temporarily and prevent embarrassing dripping. Chronic sniffling can be annoying to others and may indicate underlying health issues requiring attention. The sound is universally recognizable and often prompts offers of tissues or expressions of sympathy.',
            'pronunciation': '/ˈsnɪfəl/',
            'example_sentence': 'The child began to _____ during the sad movie, trying to hold back tears.',
            'etymology': 'Frequentative form of "sniff," with "-le" suffix indicating repeated action, meaning to sniff repeatedly.',
            'mnemonic': 'Think "SNIFF-LE = Short Nasal breathing, Including repeated inhalation, Frequently with mucus, Little sounds through nose" - repeated nasal breathing sounds.',
            'source': 'Claude'
        },
        'snippet': {
            'definition': 'Snippet refers to a small piece, fragment, or brief extract of something larger, such as a short passage from text, a brief musical phrase, or a small portion of code. This term emphasizes the incomplete nature of the sample while suggesting it represents or gives a taste of the whole. Snippets are often used to preview content, provide examples, or share interesting portions without reproducing entire works. In digital contexts, code snippets are small, reusable pieces of programming code that perform specific functions. News snippets provide brief summaries of longer stories. The value of snippets lies in their ability to convey essential information or flavor in a condensed format.',
            'pronunciation': '/ˈsnɪpɪt/',
            'example_sentence': 'The teacher shared a fascinating _____ from the novel to encourage students to read the complete work.',
            'etymology': 'From "snip" (to cut) + diminutive suffix "-et," meaning a small piece cut off.',
            'mnemonic': 'Think "SNIP-PET = Small piece that\'s been SNIPped off, Pretty tiny Extract, just a Taste" - small fragment of something larger.',
            'source': 'Claude'
        },
        'snitch': {
            'definition': 'Snitch functions as both a verb meaning to inform on someone or report their wrongdoing to authorities, and as a noun referring to a person who regularly reports on others\' activities to those in power. This behavior often carries negative connotations in peer groups, where snitching is seen as betrayal or disloyalty. However, reporting genuine wrongdoing can serve important purposes in maintaining safety and justice. The term appears frequently in criminal contexts, schools, and workplaces where there may be conflicts between loyalty to peers and responsibility to report problems. Cultural attitudes toward snitching vary widely, with some viewing it as necessary civic duty and others as treacherous betrayal.',
            'pronunciation': '/snɪtʃ/',
            'example_sentence': 'Nobody wanted to _____ on their classmate, even though they knew cheating was wrong.',
            'etymology': 'Possibly from "sneak" or related to "snatch," meaning to catch or inform on someone secretly.',
            'mnemonic': 'Think "SNITCH = Someone who tells authorities, Notifying officials about wrongdoing, Informing on others, Telling secrets, CHoosing to report" - inform on someone to authorities.',
            'source': 'Claude'
        },
        'snivel': {
            'definition': 'Snivel means to cry or complain in a whining, self-pitying manner, often while sniffling or showing other signs of distress that evoke more annoyance than sympathy. This behavior typically involves both physical actions (nasal congestion, tears) and emotional expressions (whining, self-pity) that others find irritating rather than genuinely moving. Sniveling suggests weakness, self-indulgence, or manipulation rather than legitimate grief or complaint. The word carries distinctly negative connotations, implying that the person\'s distress is either exaggerated, self-inflicted, or expressed in an particularly unappealing way. Adults who snivel often lose credibility and sympathy from observers.',
            'pronunciation': '/ˈsnɪvəl/',
            'example_sentence': 'Instead of taking responsibility for his mistakes, he began to _____ about how unfair everyone was treating him.',
            'etymology': 'From Old English "snyflan," related to "sniff," meaning to run at the nose or cry weakly.',
            'mnemonic': 'Think "SNIV-EL = Self-pitying cry, Nasal whining, Irritating complaints, Very annoying, Extremely whiny behavior" - whine and cry in annoying way.',
            'source': 'Claude'
        },
        'snooty': {
            'definition': 'Snooty describes someone who behaves in a superior, condescending, or arrogant manner, often looking down on others they consider inferior in social status, education, or sophistication. This attitude typically involves pretentiousness, where people act as if they are more refined, cultured, or important than they actually are or than others around them. Snooty behavior includes dismissive comments, contemptuous looks, and an general air of superiority that makes others feel unwelcome or inadequate. Such people often judge others based on superficial criteria like wealth, education, or social connections rather than character or merit. The behavior stems from insecurity or genuine belief in one\'s superiority.',
            'pronunciation': '/ˈsnuti/',
            'example_sentence': 'The _____ restaurant staff made the casual diners feel unwelcome with their condescending attitudes.',
            'etymology': 'From "snoot" (nose, snout) + "-y" suffix, suggesting someone who looks down their nose at others.',
            'mnemonic': 'Think "SNOOT-Y = Stuck-up, acting like they\'re better, NOse in the air, Others treated badly, Thinking they\'re superior" - arrogant and condescending.',
            'source': 'Claude'
        },
        'snore': {
            'definition': 'Snore refers to the loud breathing sound that occurs during sleep when airflow through the mouth and nose is partially obstructed, causing vibration of the soft tissues in the throat and nasal passages. This common phenomenon affects people of all ages but becomes more frequent with age, weight gain, or certain medical conditions. Snoring can range from quiet breathing sounds to loud, disruptive noises that disturb sleep partners and even the snorer themselves. Factors contributing to snoring include sleeping position, nasal congestion, alcohol consumption, and anatomical features. While often harmless, chronic loud snoring may indicate sleep apnea or other health issues requiring medical attention.',
            'pronunciation': '/snɔr/',
            'example_sentence': 'His loud _____ kept his roommate awake all night during their camping trip.',
            'etymology': 'From Middle English "snoren," imitative of the sound made during obstructed breathing while sleeping.',
            'mnemonic': 'Think "SNORE = Sound during sleep, Nasal obstruction, Often very loud, Really disrupts sleep, Everyone hears it" - loud breathing sound during sleep.',
            'source': 'Claude'
        },
        'snorkels': {
            'definition': 'Snorkels are breathing tubes that allow swimmers to breathe air from the surface while floating face-down in water, enabling extended observation of underwater environments without repeatedly lifting the head. These simple devices typically consist of a curved tube with a mouthpiece and sometimes include features like purge valves or splash guards. Snorkeling equipment usually includes a mask, fins, and the snorkel itself, providing an accessible way to explore shallow marine environments. The activity requires basic swimming skills and comfort with breathing through the mouth underwater. Snorkeling offers educational and recreational opportunities to observe marine life, coral reefs, and underwater landscapes without requiring scuba diving certification.',
            'pronunciation': '/ˈsnɔrkəlz/',
            'example_sentence': 'The tourists rented masks, fins, and _____ to explore the colorful coral reef in the shallow lagoon.',
            'etymology': 'From German "Schnorchel," originally a submarine breathing tube, applied to swimming equipment.',
            'mnemonic': 'Think "SNORK-ELS = Swimming aids for breathing, Nose and mouth tubes, Observing underwater, Relatively simple Equipment, Looking at Sea life" - breathing tubes for surface swimming.',
            'source': 'Claude'
        },
        'snout': {
            'definition': 'Snout refers to the projecting nose and mouth area of an animal, particularly mammals like pigs, dogs, and bears, which typically extends beyond the face and serves functions including smelling, breathing, eating, and sometimes digging. This anatomical feature varies greatly among species, from the sensitive, mobile snouts of pigs used for rooting to the powerful snouts of bears used for foraging. Snouts often contain highly developed olfactory systems that provide superior scent detection compared to human noses. The term can be used derogatorily when applied to human noses that are considered unusually large or prominent. Snouts represent important evolutionary adaptations for survival and feeding.',
            'pronunciation': '/snaʊt/',
            'example_sentence': 'The pig used its sensitive _____ to search for truffles buried beneath the forest floor.',
            'etymology': 'From Middle English "snoute," possibly from Middle Dutch "snute," meaning the projecting nose of an animal.',
            'mnemonic': 'Think "SNOUT = projecting nose area, Nose Of animals, Used for smelling, Typically on mammals" - animal\'s projecting nose and mouth.',
            'source': 'Claude'
        },
        'snowy': {
            'definition': 'Snowy describes conditions, landscapes, or objects characterized by the presence of snow or resembling snow in appearance, typically indicating white, cold, and winter-like qualities. This adjective can describe weather conditions during snowfall, landscapes covered with snow, or objects that are white and pristine like fresh snow. Snowy conditions often create beautiful but challenging environments, affecting transportation, outdoor activities, and daily routines. The term extends metaphorically to describe things that are pure white, clean, or having a pristine appearance. Snowy weather evokes various emotions and associations, from childhood joy and winter sports to concerns about safety and warmth.',
            'pronunciation': '/ˈsnoʊi/',
            'example_sentence': 'The _____ mountain peaks created a breathtaking backdrop for the winter landscape photography.',
            'etymology': 'From "snow" + "-y" suffix, meaning characterized by or resembling snow.',
            'mnemonic': 'Think "SNOW-Y = covered with SNOW, making everything white, Yonder mountains all white" - characterized by snow or snow-like appearance.',
            'source': 'Claude'
        }
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            words = list(reader)
        
        print(f"Processing {len(words)} words from batch 162...")
        
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
        
        print(f"\nBatch 162 processing complete!")
        print(f"Successfully processed {len(processed_data)}/{len(words)} words")
        print(f"Output saved to: {output_file}")
        
        if combined_errors:
            print(f"\nCombined word errors detected: {len(combined_errors)}")
            for error in combined_errors:
                print(f"  - {error}")
        
    except Exception as e:
        print(f"Error processing batch 162: {str(e)}")
        raise

if __name__ == "__main__":
    main()