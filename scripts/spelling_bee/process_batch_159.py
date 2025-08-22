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
    input_file = os.path.join(script_dir, 'output', 'batch_159_words.csv')
    output_file = os.path.join(script_dir, 'output', 'batch_159_processed.csv')
    
    calculator = DifficultyCalculator()
    
    # Comprehensive word data with educational content
    word_data = {
        'shares': {
            'definition': 'Shares refer to units of ownership in a corporation or mutual fund, representing a claim on part of the company\'s assets and earnings. When you own shares, you become a shareholder with rights that may include voting on company matters and receiving dividends. The value of shares fluctuates based on market conditions, company performance, and investor sentiment. Shares can be traded on stock exchanges, making them liquid investments. Different types of shares exist, including common shares that typically come with voting rights, and preferred shares that often provide fixed dividends but limited voting power. The concept of shares forms the foundation of modern corporate finance and investment markets.',
            'pronunciation': '/ʃɛrz/',
            'example_sentence': 'The investor decided to buy 100 _____ of the technology company after researching its quarterly earnings report.',
            'etymology': 'From Middle English "share," from Old English "scearu" meaning "a cutting, division," related to "shear." The financial meaning developed in the 17th century as joint-stock companies emerged.',
            'mnemonic': 'Think "SHARE the ownership" - shares literally share ownership of a company among many people.',
            'source': 'Claude'
        },
        'sharp': {
            'definition': 'Sharp describes something having a pointed edge or tip capable of cutting or piercing, or having a well-defined outline or detail. In music, sharp indicates a note raised by a semitone, marked with the ♯ symbol. The word can describe mental qualities like keen intelligence or quick wit, as in "sharp mind." Sharp can also mean sudden or abrupt, like a sharp turn or sharp pain. In visual contexts, it refers to clear focus and definition, opposite of blurry. When describing taste, sharp indicates a strong, pungent, or acidic flavor. The versatility of this word makes it applicable across physical, mental, sensory, and temporal domains.',
            'pronunciation': '/ʃɑrp/',
            'example_sentence': 'The chef used a _____ knife to precisely cut the vegetables into uniform pieces.',
            'etymology': 'From Old English "scearp," from Proto-Germanic "*skarpaz," related to "scrape" and "shear." The musical meaning dates to the 16th century.',
            'mnemonic': 'Remember "SHARP cuts through" - whether it\'s a blade, mind, or musical note, sharp things penetrate and stand out.',
            'source': 'Claude'
        },
        'shawl': {
            'definition': 'A shawl is a rectangular or triangular piece of fabric worn over the shoulders, around the neck, or draped over the head for warmth, modesty, or fashion. Traditionally, shawls have been important garments in many cultures, often handwoven with intricate patterns and designs that reflect cultural heritage. Materials range from wool and cashmere for warmth to silk and cotton for lighter wear. Shawls can be simple everyday items or elaborate ceremonial pieces adorned with embroidery, beading, or fringe. The Kashmir shawl, prayer shawl (tallit), and Spanish mantilla are examples of culturally significant shawls. Modern shawls serve both practical and aesthetic purposes in contemporary fashion.',
            'pronunciation': '/ʃɔl/',
            'example_sentence': 'She wrapped the warm woolen _____ around her shoulders as the evening air grew chilly.',
            'etymology': 'From Persian "shal," possibly through Hindi "sal." The word entered English in the 17th century through trade with South Asia.',
            'mnemonic': 'Think "SHALL wrap" - a shawl is something you shall wrap around yourself for warmth or style.',
            'source': 'Claude'
        },
        'shawwal': {
            'definition': 'Shawwal is the tenth month of the Islamic lunar calendar, following immediately after the holy month of Ramadan. This month holds special significance in Islamic tradition as it begins with Eid al-Fitr, the celebration marking the end of the Ramadan fasting period. The month consists of either 29 or 30 days, depending on the lunar cycle. During Shawwal, many Muslims observe six days of voluntary fasting, which is considered spiritually rewarding. The name Shawwal comes from Arabic, relating to the time when camels typically give birth and their udders are lifted or raised. This month represents a time of celebration, gratitude, and continued spiritual practice in the Islamic faith.',
            'pronunciation': '/ʃɑwˈwɑl/',
            'example_sentence': 'The Islamic community celebrated Eid al-Fitr on the first day of _____, marking the joyful end of Ramadan.',
            'etymology': 'From Arabic "Shawwāl," derived from "shāla" meaning "to lift up" or "to raise," referring to the time when female camels lift their tails when ready to mate.',
            'mnemonic': 'Remember "SHAW-wal follows RAW-madan" - Shawwal comes right after Ramadan in the Islamic calendar.',
            'source': 'Claude'
        },
        'shazam': {
            'definition': 'Shazam is an exclamation expressing sudden transformation, surprise, or the successful completion of something magical or remarkable. Originally popularized as the magic word used by the comic book character Captain Marvel (later called Shazam) to transform from Billy Batson into his superhero form, the word has entered general usage as an expression of amazement or to announce sudden success. The term embodies the concept of instant, dramatic change or the revelation of something extraordinary. In modern usage, "Shazam" is also known as a mobile app that identifies music, but the exclamatory use remains tied to moments of wonder, discovery, or magical transformation.',
            'pronunciation': '/ʃəˈzæm/',
            'example_sentence': 'The magician waved his wand and shouted "_____!" as the rabbit appeared in the previously empty hat.',
            'etymology': 'Created in 1940 for DC Comics, combining the first letters of six mythological figures: Solomon, Hercules, Atlas, Zeus, Achilles, and Mercury.',
            'mnemonic': 'Think "SHA-ZAM = Something Happening Amazingly, Zap And Magic!" - it\'s the sound of instant magical transformation.',
            'source': 'Claude'
        },
        'sheathed': {
            'definition': 'Sheathed means enclosed in a protective covering or case, particularly referring to a blade, sword, or knife being placed into its sheath. The term extends beyond weapons to describe anything covered or protected by an outer casing, such as electrical wires covered in insulation or cables wrapped in protective material. In biological contexts, sheathed can describe structures surrounded by protective membranes or coverings. The past tense form indicates the action has been completed - the item is now safely enclosed and protected. Sheathing serves purposes of safety, preservation, and organization, preventing damage to both the sheathed object and surrounding materials.',
            'pronunciation': '/ʃiðd/',
            'example_sentence': 'The medieval knight _____ his sword after the tournament, sliding the blade safely into its ornate scabbard.',
            'etymology': 'From Old English "scēað" meaning "case" or "covering," related to "shed" in the sense of a protective structure.',
            'mnemonic': 'Think "SHE-ATHED her blade" - she put it in its protective covering (sheath).',
            'source': 'Claude'
        },
        'sheaves': {
            'definition': 'Sheaves are bundles of grain stalks, such as wheat, barley, or oats, that have been cut and tied together during harvest time. This traditional agricultural practice allows grain to dry properly and makes transportation and storage more efficient. Sheaves are typically bound with twine or strips of the grain itself and left in fields to cure before threshing. The term also has mathematical applications in advanced geometry and topology, where a sheaf is a mathematical structure that systematically tracks locally defined data. In biblical and literary contexts, sheaves often symbolize abundance, harvest, and divine provision. The process of bundling grain into sheaves represents the culmination of agricultural labor and the gathering of sustenance.',
            'pronunciation': '/ʃivz/',
            'example_sentence': 'The farm workers gathered the wheat into neat _____ that dotted the golden harvest field.',
            'etymology': 'Plural of "sheaf," from Old English "scēaf," related to "shove" - originally meaning something that is pushed or thrust together.',
            'mnemonic': 'Think "SHE-AVES grain" - she saves grain by bundling it into sheaves for storage.',
            'source': 'Claude'
        },
        'shebang': {
            'definition': 'Shebang refers to an entire situation, affair, or organized event, often used in the phrase "the whole shebang" to mean everything or the complete package. The term suggests a comprehensive, all-inclusive situation or elaborate affair. In computing, shebang has a specific technical meaning as the character sequence "#!" at the beginning of script files that tells the system which interpreter to use. The word conveys a sense of completeness, totality, or an entire undertaking from start to finish. It can describe anything from a party or celebration to a business operation or complex project. The informal nature of the word makes it particularly suitable for casual conversation about comprehensive situations.',
            'pronunciation': '/ʃɪˈbæŋ/',
            'example_sentence': 'When they decided to redecorate the house, they went for the whole _____ - new furniture, paint, and even landscaping.',
            'etymology': 'American slang from the 1860s, possibly from Irish "síbín" (illegal drinking establishment) or from "she-bang" meaning a temporary shelter.',
            'mnemonic': 'Think "SHE-BANG, the whole thing!" - when she bangs, everything happens at once.',
            'source': 'Claude'
        },
        'shedding': {
            'definition': 'Shedding refers to the natural process of discarding or losing outer layers, coverings, or parts of a living organism. In animals, this includes the loss of fur, feathers, skin, or scales as part of normal growth and renewal cycles. Plants shed leaves, bark, or seeds as seasonal changes occur. The term also applies to non-biological contexts, such as shedding light on a subject (illuminating or clarifying it) or shedding tears (crying). Shedding can be voluntary, like an animal molting its winter coat, or involuntary, like hair loss due to stress. Understanding shedding processes is important in biology, veterinary care, and environmental science.',
            'pronunciation': '/ˈʃɛdɪŋ/',
            'example_sentence': 'The golden retriever was _____ so much fur during spring that the family had to vacuum daily.',
            'etymology': 'From Old English "scēadan" meaning "to separate, divide, or part." Related to "shed" as both a structure and the act of casting off.',
            'mnemonic': 'Think "SHED-ding = getting rid of" - like a shed stores things, shedding gets rid of things.',
            'source': 'Claude'
        },
        'sheen': {
            'definition': 'Sheen refers to a soft, lustrous shine or glossy appearance on a surface, characterized by a gentle brilliance that reflects light without being harshly bright. Unlike harsh glare or mirror-like reflection, sheen provides a subtle, attractive glow that enhances the appearance of materials like silk, polished wood, or healthy hair. Sheen can be natural, such as the lustrous quality of pearls or the glossy coat of a well-groomed animal, or artificially created through polishing, waxing, or special finishes. The quality suggests smoothness, health, and careful maintenance. In photography and art, sheen adds depth and visual interest to surfaces, creating appealing contrasts between matte and glossy areas.',
            'pronunciation': '/ʃin/',
            'example_sentence': 'The mahogany table had a beautiful _____ that reflected the candlelight softly across its polished surface.',
            'etymology': 'From Old English "scīene" meaning "beautiful, bright," related to "shine" and "show." The word emphasizes gentle rather than harsh brilliance.',
            'mnemonic': 'Think "SHE-EN-joys the shine" - sheen is the gentle, enjoyable kind of shine that\'s pleasing to see.',
            'source': 'Claude'
        },
        'sheepish': {
            'definition': 'Sheepish describes the feeling or appearance of being embarrassed, bashful, or awkwardly self-conscious, particularly after making a mistake or being caught in an awkward situation. The term draws from the perceived timid and easily startled nature of sheep, suggesting someone who appears meek, hesitant, or apologetic. A sheepish expression typically includes behaviors like looking down, blushing, or offering a tentative smile while feeling uncomfortable. This emotional state often occurs when someone realizes they\'ve done something foolish, inappropriate, or wrong and feels mild shame or embarrassment about it. The word captures that particular combination of guilt, embarrassment, and the desire to make amends that follows minor social missteps.',
            'pronunciation': '/ˈʃipɪʃ/',
            'example_sentence': 'He gave a _____ grin when his mother found the empty cookie jar hidden under his bed.',
            'etymology': 'From "sheep" + "-ish," referring to the perceived timid, easily embarrassed nature of sheep when caught or startled.',
            'mnemonic': 'Think "SHEEP-ish = shy like a sheep" - sheep look embarrassed when caught, just like people do.',
            'source': 'Claude'
        },
        'sheesh': {
            'definition': 'Sheesh is an informal exclamation used to express exasperation, disbelief, frustration, or mild annoyance at a situation or someone\'s behavior. This interjection serves as a somewhat polite alternative to stronger expressions of irritation, allowing the speaker to convey their feelings without using offensive language. The word can express amazement at something unreasonable or excessive, or serve as a reaction to an awkward or annoying circumstance. Sheesh often accompanies eye-rolling or head-shaking gestures and is commonly used in casual conversation, particularly among younger people. The tone can range from mildly annoyed to genuinely astonished, depending on the context and delivery.',
            'pronunciation': '/ʃiʃ/',
            'example_sentence': '_____! I can\'t believe you forgot your keys again after I reminded you three times.',
            'etymology': 'American slang from the 1950s, possibly a euphemistic alteration of "Jesus" or related to Yiddish expressions of exasperation.',
            'mnemonic': 'Think "SHEESH = She\'s Expressing Extreme Shock Here" - it\'s what you say when something is just too much.',
            'source': 'Claude'
        },
        'sheetrock': {
            'definition': 'Sheetrock is a trademarked brand name for drywall, also known as wallboard or plasterboard, consisting of gypsum plaster sandwiched between thick sheets of paper. This building material revolutionized interior construction by providing a quick, cost-effective alternative to traditional plaster walls. Sheetrock panels are manufactured in standard sizes and can be easily cut, installed, and finished to create smooth interior wall and ceiling surfaces. The material is fire-resistant, relatively lightweight, and provides good sound insulation. Installation involves screwing or nailing the panels to wooden or metal framing, then applying joint compound and tape to seams before sanding and painting. The term has become genericized, with many people using "sheetrock" to refer to any brand of drywall.',
            'pronunciation': '/ˈʃitˌrɑk/',
            'example_sentence': 'The contractors hung _____ throughout the new house before applying primer and paint to the walls.',
            'etymology': 'Trademark coined in 1917 by United States Gypsum Company, combining "sheet" and "rock" to describe the rock-based sheet material.',
            'mnemonic': 'Think "SHEET of ROCK" - it\'s literally sheets made from rock (gypsum) that form walls.',
            'source': 'Claude'
        },
        'sheldrake': {
            'definition': 'A sheldrake is a large waterfowl, specifically referring to several species of ducks in the genus Tadorna, characterized by their distinctive colorful plumage and slightly upturned bills. The most common is the Common Sheldrake (Tadorna tadorna), which features striking black, white, and chestnut coloring with a bright red bill and legs. These birds inhabit coastal areas, estuaries, and large inland waters across Europe and Asia. Sheldrakes are known for their unique nesting habits, often choosing burrows in sandy cliffs or dunes, and their diet consists primarily of mollusks, crustaceans, and marine worms. The name reflects their preference for sheltered coastal waters and their intermediate characteristics between typical ducks and geese.',
            'pronunciation': '/ˈʃɛlˌdreɪk/',
            'example_sentence': 'The ornithologist spotted a pair of _____ nesting in the sand dunes along the protected coastline.',
            'etymology': 'From Middle English, combining "sheld" (variegated, spotted) and "drake" (male duck), referring to the bird\'s distinctive multicolored plumage.',
            'mnemonic': 'Think "SHELL-DRAKE" - a drake (duck) that lives near shells on the shore.',
            'source': 'Claude'
        },
        'shelf': {
            'definition': 'A shelf is a flat, horizontal surface attached to a wall or supported by a framework, designed to hold and display objects such as books, decorative items, or storage containers. Shelves can be made from various materials including wood, metal, glass, or plastic, and come in numerous designs from simple floating shelves to elaborate built-in units. The concept extends beyond furniture to geological formations like continental shelves, which are underwater plateaus extending from continents. In retail, shelving systems organize and present merchandise. The plural form "shelves" follows an irregular pattern where "f" changes to "v." Shelves provide both functional storage and aesthetic display opportunities in homes, offices, and commercial spaces.',
            'pronunciation': '/ʃɛlf/',
            'example_sentence': 'She arranged her favorite novels alphabetically on the wooden _____ above her desk.',
            'etymology': 'From Middle Low German "schelf" meaning "shelf, ledge," related to "shelve" and ultimately from the concept of something that splits or divides space.',
            'mnemonic': 'Think "SHELF = Storage Helper for Everything Light and Flat" - it holds flat items at different levels.',
            'source': 'Claude'
        },
        'shell': {
            'definition': 'A shell is a hard, protective outer covering found on various animals, including mollusks, turtles, and crustaceans, serving as defense against predators and environmental hazards. Shells come in diverse shapes, sizes, and compositions, from the spiral chambers of nautiluses to the hinged structures of clams. The term extends to other contexts: explosive shells in warfare, computer shells as command-line interfaces, and architectural shells as structural frameworks. In geology, shell refers to fossilized remains that provide insights into ancient life. Metaphorically, "coming out of one\'s shell" means becoming less shy or reserved. Shells have cultural significance in art, jewelry, and decoration across many civilizations.',
            'pronunciation': '/ʃɛl/',
            'example_sentence': 'The hermit crab quickly retreated into its _____ when the child reached down to touch it.',
            'etymology': 'From Old English "scell," related to "scale" and "skill," originally meaning "to separate" or "to split off."',
            'mnemonic': 'Think "SHE\'LL protect herself" - a shell protects the creature inside it.',
            'source': 'Claude'
        },
        'shelter': {
            'definition': 'Shelter refers to a structure or covering that provides protection from weather, danger, or discomfort, ranging from temporary refuge to permanent housing. The concept encompasses physical buildings like houses, tents, or caves, as well as abstract protection such as financial shelter through insurance or emotional shelter through supportive relationships. Shelter represents one of humanity\'s basic needs alongside food and water. Animal shelters specifically house homeless or abandoned pets, while homeless shelters provide temporary accommodation for people without homes. The verb form means to protect or shield from harm. Emergency shelters become crucial during natural disasters, providing life-saving protection when regular housing is unavailable or damaged.',
            'pronunciation': '/ˈʃɛltər/',
            'example_sentence': 'The hikers sought _____ under the rocky overhang when the sudden thunderstorm began.',
            'etymology': 'From Old English "scyldtruma" meaning "shield troop," later influenced by "shield" and meaning a protective covering.',
            'mnemonic': 'Think "SHE\'LL-TER protect you" - shelter will protect you from the elements.',
            'source': 'Claude'
        },
        'shenandoah': {
            'definition': 'Shenandoah refers to a river valley region in Virginia and West Virginia, famous for its natural beauty, including Shenandoah National Park and the scenic Skyline Drive. The Shenandoah River flows through this valley, creating one of America\'s most celebrated landscapes. The area holds significant historical importance, having witnessed numerous Civil War battles and serving as a crucial agricultural region. Shenandoah National Park, established in 1935, protects over 200,000 acres of wilderness, waterfalls, and diverse wildlife. The name has cultural resonance through folk songs, particularly "Oh Shenandoah," and represents the romanticized American frontier spirit. The region attracts millions of visitors annually for hiking, camping, and scenic drives through the Blue Ridge Mountains.',
            'pronunciation': '/ˌʃɛnənˈdoʊə/',
            'example_sentence': 'The family planned their autumn vacation to drive through _____ National Park to see the spectacular fall foliage.',
            'etymology': 'From Algonquian Native American language, possibly meaning "spruce place" or "big flat place," though the exact origin is disputed among linguists.',
            'mnemonic': 'Think "SHEN-AN-DO-AH = Scenic Hills Everyone Naturally Admires Near Diverse Outstanding American Heritage."',
            'source': 'Claude'
        },
        'shenanigans': {
            'definition': 'Shenanigans refers to mischievous, playful, or deceptive activities that are typically harmless but involve trickery, pranks, or underhanded behavior. The word suggests actions that are questionable or suspicious but not necessarily malicious, often involving clever schemes or elaborate jokes. Shenanigans can describe anything from children\'s pranks to political maneuvering that bends rules without breaking them outright. The term carries a somewhat lighthearted connotation despite describing potentially annoying or problematic behavior. It often implies that the perpetrator is being sneaky or trying to get away with something, but in a way that might be amusing rather than truly harmful. The word is frequently used to dismiss or call attention to suspicious activities.',
            'pronunciation': '/ʃəˈnænɪɡənz/',
            'example_sentence': 'The teacher suspected some _____ when she found all the classroom clocks mysteriously running five minutes slow.',
            'etymology': 'American slang from the 1850s, possibly from Irish "sionnach" (fox) or "sionnachuighim" (I play the fox), referring to cunning behavior.',
            'mnemonic': 'Think "SHE-NAN-I-GANS are up to no good" - when she and her gang are plotting, there are shenanigans happening.',
            'source': 'Claude'
        },
        'shepherd': {
            'definition': 'A shepherd is a person who tends, guards, and guides sheep, traditionally living with flocks in pastures and moving them to fresh grazing areas. This ancient occupation requires extensive knowledge of animal behavior, weather patterns, and terrain, as well as skills in protecting livestock from predators and disease. Shepherds use trained dogs and various tools like staffs and whistles to control their flocks. The term extends metaphorically to describe leaders who guide and protect groups of people, particularly in religious contexts where spiritual leaders are called shepherds of their congregations. Modern shepherding combines traditional methods with contemporary technologies like GPS tracking and veterinary science. The role symbolizes care, guidance, and protection across many cultures.',
            'pronunciation': '/ˈʃɛpərd/',
            'example_sentence': 'The young _____ guided his flock to higher pastures as the summer grass grew scarce in the valley.',
            'etymology': 'From Old English "scēaphierde," combining "scēap" (sheep) and "hierde" (herder), literally meaning "sheep herder."',
            'mnemonic': 'Think "SHEEP-HERD = one who herds sheep" - a shepherd herds and protects sheep.',
            'source': 'Claude'
        },
        'sherifftarry': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "sheriff" and "tarry." A sheriff is a law enforcement officer responsible for maintaining peace in a county or jurisdiction, with duties including serving legal papers, operating jails, and enforcing court orders. "Tarry" means to delay departure or linger in a place. These are distinct words that should not be combined. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈʃɛrɪf ˈtæri/',
            'example_sentence': 'The _____ decided not to _____ at the scene once backup arrived to handle the situation.',
            'etymology': 'Sheriff: from Old English "scīrgerēfa" (shire reeve). Tarry: from Middle English "tarien," meaning to delay or wait.',
            'mnemonic': 'Remember these as TWO words: SHERIFF (law officer) + TARRY (to delay or linger).',
            'source': 'Claude'
        },
        'shetland': {
            'definition': 'Shetland refers to the Shetland Islands, an archipelago of over 100 islands located northeast of mainland Scotland, known for their rugged beauty, rich cultural heritage, and unique wildlife. The islands are famous for Shetland ponies, small hardy horses originally bred for work in mines and farms, and Shetland sheepdogs, intelligent herding dogs with flowing coats. Shetland wool comes from the native sheep that graze on the islands\' sparse vegetation, producing exceptionally fine fiber prized for traditional knitting. The islands have a distinct culture influenced by both Scottish and Norse heritage, with their own dialect and traditional music. The economy relies on fishing, oil industry, agriculture, and tourism, with visitors drawn to the dramatic landscapes and archaeological sites.',
            'pronunciation': '/ˈʃɛtlənd/',
            'example_sentence': 'The tourists visited _____ specifically to see the famous ponies and experience the islands\' unique cultural traditions.',
            'etymology': 'From Old Norse "Hjaltland," possibly meaning "hilt land" referring to the shape of the main island, later adapted through Scots.',
            'mnemonic': 'Think "SHET-LAND = where SHEep and Tiny ponies live" - the land known for small animals and wool.',
            'source': 'Claude'
        },
        'shhh': {
            'definition': 'Shhh is an onomatopoeia representing the sound made to request silence or quiet, universally recognized as a gentle shushing sound. This interjection serves as a non-verbal or semi-verbal way to signal that someone should lower their voice or stop talking entirely. The elongated "h" sound mimics the natural hushing noise made by forcing air through slightly parted lips and tongue. Shhh can be used in various contexts: calming a baby, requesting quiet in a library, or asking for discretion about sensitive information. The intensity and length of the sound can convey different levels of urgency or politeness. Unlike spoken words, shhh transcends language barriers and is understood across cultures.',
            'pronunciation': '/ʃ/',
            'example_sentence': 'The librarian quietly said "_____" when the students\' discussion became too loud for the reading room.',
            'etymology': 'Onomatopoeia imitating the natural sound of forced breath used to create quiet, found in various forms across languages.',
            'mnemonic': 'The sound itself IS the meaning - "SHHH" is the actual sound you make to create silence.',
            'source': 'Claude'
        },
        'shiba': {
            'definition': 'Shiba refers to the Shiba Inu, a compact, agile spitz-type dog breed originating from Japan, known for its fox-like appearance, curled tail, and independent personality. These dogs typically weigh 15-25 pounds and have a double coat in colors including red, black and tan, or cream. Shiba Inus are among Japan\'s oldest native breeds, originally used for hunting small game in mountainous regions. They possess a confident, alert temperament and are known for their cleanliness, intelligence, and sometimes stubborn nature. The breed gained international popularity and became an internet sensation as the face of the "Doge" meme and Dogecoin cryptocurrency. Shibas require consistent training and socialization due to their strong-willed character.',
            'pronunciation': '/ˈʃibə/',
            'example_sentence': 'The _____ Inu trotted confidently through the park, its curled tail held high and fox-like ears alert to every sound.',
            'etymology': 'From Japanese "shiba," possibly meaning "brushwood" (referring to hunting terrain) or "small" (referring to the dog\'s size).',
            'mnemonic': 'Think "SHI-BA = Small, Handsome, Independent, Bold Attitude" - describing the Shiba Inu\'s personality.',
            'source': 'Claude'
        },
        'shield': {
            'definition': 'A shield is a protective device held or worn to deflect attacks, traditionally made of wood, metal, or leather and used in warfare to guard against weapons like swords, arrows, or spears. Historical shields varied greatly in design, from small bucklers to large tower shields, often decorated with heraldic symbols representing family or military units. The concept extends beyond physical protection to include metaphorical shields such as legal protections, emotional defenses, or technological safeguards like antivirus software. In geology, a shield refers to large areas of exposed Precambrian rock. Modern applications include radiation shields in medical equipment and heat shields on spacecraft. The verb form means to protect or defend from harm or danger.',
            'pronunciation': '/ʃild/',
            'example_sentence': 'The medieval knight raised his _____ just in time to deflect the arrow aimed at his chest.',
            'etymology': 'From Old English "scield," related to "skill" and originally meaning "to divide" or "to separate," referring to its protective function.',
            'mnemonic': 'Think "SHI-ELD = Stops Hits, Ensures Life Defense" - a shield stops attacks to protect life.',
            'source': 'Claude'
        },
        'shieldtiger': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "shield" and "tiger." A shield is a protective device used to deflect attacks or guard against danger. A tiger is a large, carnivorous cat native to Asia, known for its distinctive orange coat with black stripes. These are completely separate concepts that should not be combined. The error likely occurred during document scanning or data processing where spacing between words was lost, creating this nonsensical combination.',
            'pronunciation': '/ʃild ˈtaɪɡər/',
            'example_sentence': 'The warrior carried his _____ while hunting the dangerous _____ in the jungle.',
            'etymology': 'Shield: from Old English "scield." Tiger: from Old French "tigre," from Latin "tigris," from Greek "tigris."',
            'mnemonic': 'Remember these as TWO words: SHIELD (protective device) + TIGER (striped big cat).',
            'source': 'Claude'
        },
        'shimmery': {
            'definition': 'Shimmery describes something that gleams with a soft, wavering light or exhibits a gentle, flickering radiance that seems to dance or move across a surface. This quality often results from light reflecting off textured or iridescent materials, creating an effect that catches the eye without being harsh or overwhelming. Shimmery surfaces might include silk fabric, water rippling in sunlight, metallic finishes, or cosmetic products designed to add luminous highlights. The effect suggests movement, elegance, and visual interest, often associated with beauty, magic, or luxury. Unlike static shine, shimmery implies a dynamic quality where the light appears to move or shift, creating an enchanting visual experience that draws attention and admiration.',
            'pronunciation': '/ˈʃɪməri/',
            'example_sentence': 'Her dress had a _____ quality that made it sparkle beautifully under the ballroom\'s crystal chandeliers.',
            'etymology': 'From "shimmer" + "-y," where shimmer comes from Old English "scimerian," meaning "to glitter" or "to shine with a wavering light."',
            'mnemonic': 'Think "SHIMMER-Y = light that SHIMs and MERs (moves)" - shimmery things have moving, dancing light.',
            'source': 'Claude'
        },
        'shindig': {
            'definition': 'A shindig is an elaborate party, celebration, or social gathering, typically featuring music, dancing, food, and entertainment. The term suggests a lively, festive event that might be larger or more elaborate than a simple party, often with a somewhat informal or folksy character. Shindigs can range from backyard barbecues and barn dances to wedding receptions and community festivals. The word implies fun, exuberance, and social connection, often with an element of down-to-earth enjoyment rather than formal sophistication. Originally associated with rural or working-class celebrations, the term has broadened to describe any spirited gathering where people come together to enjoy themselves in a relaxed, convivial atmosphere.',
            'pronunciation': '/ˈʃɪnˌdɪɡ/',
            'example_sentence': 'The whole town was invited to the annual harvest _____ featuring live bluegrass music and homemade apple pie.',
            'etymology': 'American slang from the 1840s, possibly from "shin" (to dance) + "dig" (to work hard), referring to energetic dancing.',
            'mnemonic': 'Think "SHIN-DIG = people SHIN-kicking while they DIG the music" - a lively party with dancing.',
            'source': 'Claude'
        },
        'shine': {
            'definition': 'Shine refers to bright light reflected from a surface, or the quality of giving off or reflecting light in a brilliant, luminous way. The word can describe both the light itself and the surface\'s ability to produce that light, whether from polishing, natural properties, or artificial illumination. Shine can be applied to physical objects like polished shoes, clean windows, or metallic surfaces, as well as metaphorical uses describing someone\'s talent or personality "shining" through their work or behavior. The verb form means to emit or reflect light, to excel at something, or to polish something until it gleams. Shine suggests clarity, brightness, excellence, and positive attention.',
            'pronunciation': '/ʃaɪn/',
            'example_sentence': 'The morning sun created a brilliant _____ on the freshly waxed car\'s hood.',
            'etymology': 'From Old English "scīnan," related to German "scheinen," meaning "to appear" or "to give light."',
            'mnemonic': 'Think "SH-INE = light SHows INside Everything" - shine is light showing on surfaces.',
            'source': 'Claude'
        },
        'shingle': {
            'definition': 'A shingle is a rectangular piece of building material, typically wood, slate, or asphalt, used to cover roofs and walls in overlapping rows to shed water and provide weather protection. Traditional wooden shingles are split or sawn from cedar, creating naturally weather-resistant coverings that can last decades. The overlapping installation pattern ensures water runs off without penetrating the structure. The term also refers to small professional practice signs hung outside offices, particularly for lawyers, doctors, or consultants, giving rise to the phrase "hanging out your shingle" meaning starting a professional practice. Beach shingles are small, smooth stones worn by wave action. The overlapping pattern principle makes shingles effective waterproofing systems.',
            'pronunciation': '/ˈʃɪŋɡəl/',
            'example_sentence': 'The old farmhouse had a cedar _____ roof that had weathered to a beautiful silver-gray color over the decades.',
            'etymology': 'From Middle English "schindle," from Latin "scindula," meaning "a split piece of wood," related to "split" or "cleave."',
            'mnemonic': 'Think "SHIN-GLE = SHeds water IN Gradual Layers Effectively" - shingles shed water by overlapping.',
            'source': 'Claude'
        },
        'shipping': {
            'definition': 'Shipping refers to the transportation of goods or cargo from one location to another, typically by ship, truck, train, or aircraft, encompassing the entire logistics process of moving products from sellers to buyers. Modern shipping involves complex networks of transportation methods, warehouses, tracking systems, and international regulations. The industry includes freight shipping for large commercial shipments and package shipping for individual consumers. Shipping costs, speed, and reliability significantly impact global commerce and e-commerce. The term also extends to maritime transportation specifically, where shipping companies operate fleets of vessels carrying containers across oceans. Digital tracking systems now allow real-time monitoring of shipments throughout their journey.',
            'pronunciation': '/ˈʃɪpɪŋ/',
            'example_sentence': 'The company offered free _____ on all orders over fifty dollars to encourage online purchases.',
            'etymology': 'From "ship" + "-ing," originally referring specifically to maritime transport but expanded to include all forms of cargo transportation.',
            'mnemonic': 'Think "SHIP-PING = SHIP-ing products from Point to Point" - moving things from place to place.',
            'source': 'Claude'
        },
        'ships': {
            'definition': 'Ships are large watercraft designed for navigation on oceans, seas, or other substantial bodies of water, capable of carrying passengers, cargo, or both across significant distances. These vessels range from massive container ships and cruise liners to naval warships and research vessels, each designed for specific purposes. Ships differ from boats primarily by size and their ability to carry other watercraft. Modern ships incorporate advanced technology including GPS navigation, radar systems, and automated engines. Historical ships like galleons and clipper ships shaped global exploration and trade. The term extends metaphorically to describe anything that transports or carries, such as "flagship" products or "relationships" as ships that sail through life\'s waters.',
            'pronunciation': '/ʃɪps/',
            'example_sentence': 'The harbor was filled with cargo _____ from around the world, their containers stacked high on deck.',
            'etymology': 'From Old English "scip," related to Old Norse "skip," meaning "vessel" or "boat," from Proto-Germanic "*skipam."',
            'mnemonic': 'Think "SHIPS = Sea-going Heavy Industrial Passenger Systems" - large vessels that cross seas.',
            'source': 'Claude'
        },
        'shirk': {
            'definition': 'Shirk means to avoid or neglect responsibility, duty, or work through deliberate evasion or unwillingness to engage. The term implies a conscious choice to avoid obligations rather than inability to perform them. Someone who shirks might delegate tasks inappropriately, make excuses, or simply not show up when expected to fulfill commitments. The behavior suggests a lack of accountability and reliability, often frustrating others who depend on the person\'s contributions. Shirking can occur in workplace settings, family responsibilities, civic duties, or personal commitments. The word carries negative connotations as it describes behavior that undermines trust and places unfair burdens on others who must compensate for the shirker\'s absence.',
            'pronunciation': '/ʃɜrk/',
            'example_sentence': 'The team member would always _____ his responsibilities during difficult projects, leaving others to handle the challenging work.',
            'etymology': 'Possibly from German "schurke" meaning "rogue" or "villain," referring to someone who avoids proper behavior or duty.',
            'mnemonic': 'Think "SHIRK = SHy away from woRK" - shirking is shying away from work and responsibility.',
            'source': 'Claude'
        },
        'shirt': {
            'definition': 'A shirt is a garment worn on the upper body, typically having sleeves and covering the torso from neck to waist or hips, designed to be worn over undergarments and sometimes under outer clothing like jackets or sweaters. Shirts come in numerous styles including dress shirts for formal occasions, casual t-shirts for everyday wear, and specialized shirts for work or sports. Materials range from cotton and linen to synthetic blends, each offering different properties like breathability, durability, or wrinkle resistance. Cultural and historical variations include traditional shirts like the kurta, guayabera, or dashiki. The shirt\'s basic design has remained relatively consistent throughout history, though fashion trends influence details like collar styles, sleeve lengths, and fits.',
            'pronunciation': '/ʃɜrt/',
            'example_sentence': 'He ironed his white dress _____ carefully before the important job interview.',
            'etymology': 'From Old English "scyrte," meaning "skirt" or "tunic," related to "short" - originally referring to a short garment.',
            'mnemonic': 'Think "SHIRT = SHort garment that covers your toRso Top" - a short top garment.',
            'source': 'Claude'
        },
        'shoal': {
            'definition': 'A shoal is a shallow area in a body of water, such as a sandbar, reef, or bank, where the water depth is significantly reduced, often creating hazards for navigation. Shoals can be permanent features formed by sediment deposits or coral growth, or temporary formations created by shifting sands or tides. The term also refers to a large group of fish swimming together, similar to a school but typically describing fish in shallower waters. For mariners, shoals represent serious navigation challenges requiring careful attention to depth charts and local knowledge. Many shoals are marked with buoys or beacons to warn vessels. Some shoals become islands at low tide, while others remain just below the surface.',
            'pronunciation': '/ʃoʊl/',
            'example_sentence': 'The experienced captain carefully navigated around the dangerous _____ that had claimed several ships over the years.',
            'etymology': 'From Old English "scol," meaning "shallow place" or "multitude," related to "shallow" and "school" (of fish).',
            'mnemonic': 'Think "SHOAL = SHallow place where bOAts might get stuck on Land" - shallow water danger.',
            'source': 'Claude'
        },
        'shoe': {
            'definition': 'A shoe is a protective covering for the human foot, typically made of leather, fabric, or synthetic materials, designed to provide protection, comfort, and sometimes fashion appeal while walking or standing. Shoes evolved from simple wrappings and moccasins to complex engineered products featuring soles, heels, laces, or straps. Different types serve specific purposes: athletic shoes for sports, dress shoes for formal occasions, work boots for protection, and sandals for casual wear. The shoe industry encompasses design, manufacturing, and retail of footwear worldwide. Proper shoe fit is crucial for foot health, posture, and comfort. Cultural and regional variations in shoe styles reflect climate, tradition, and social customs.',
            'pronunciation': '/ʃu/',
            'example_sentence': 'She tied her running _____ tightly before heading out for her morning jog through the park.',
            'etymology': 'From Old English "scōh," related to Old Norse "skór," meaning "covering for the foot."',
            'mnemonic': 'Think "SHOE = Something Humans Only wear on fEet" - foot protection and covering.',
            'source': 'Claude'
        },
        'shoji': {
            'definition': 'Shoji are traditional Japanese sliding door panels or room dividers consisting of translucent paper (traditionally washi) stretched over a wooden frame with a distinctive grid pattern of thin wooden slats. These architectural elements serve multiple functions: creating flexible interior spaces, allowing soft diffused light to pass through while maintaining privacy, and contributing to the aesthetic harmony of Japanese interior design. Shoji panels can be easily moved or removed to reconfigure living spaces according to need. The paper used is specially treated to be durable yet translucent, creating a warm, gentle lighting effect. Modern adaptations may use synthetic materials but maintain the traditional appearance and functionality.',
            'pronunciation': '/ˈʃoʊdʒi/',
            'example_sentence': 'The morning light filtered beautifully through the _____ screens, creating a peaceful atmosphere in the meditation room.',
            'etymology': 'From Japanese "shōji," written with characters meaning "barrier" and "child," referring to a room partition.',
            'mnemonic': 'Think "SHO-JI = SHOws Japanese Interior design" - traditional Japanese sliding paper screens.',
            'source': 'Claude'
        },
        'shoo': {
            'definition': 'Shoo is an exclamation used to drive away or dismiss someone or something, particularly animals or children, in a gentle but firm manner. The word serves as both an interjection and a verb, expressing the desire for the target to leave immediately. Commonly used with pets, birds, or insects that are in unwanted places, "shoo" provides a non-threatening way to encourage departure without aggression. The sound itself often mimics the noise people naturally make when waving their hands to drive something away. In casual conversation, "shoo" can be used playfully with children or friends, though it might be considered rude in formal contexts. The word\'s effectiveness comes from its sharp, attention-getting sound.',
            'pronunciation': '/ʃu/',
            'example_sentence': 'The farmer would _____ the chickens out of the vegetable garden whenever they tried to eat the tender seedlings.',
            'etymology': 'Onomatopoeia imitating the natural sound made to drive away animals, similar across many languages.',
            'mnemonic': 'Think "SHOO = get away!" - the sound itself means "go away" or "leave."',
            'source': 'Claude'
        },
        'shoot': {
            'definition': 'Shoot has multiple meanings: to discharge a projectile from a weapon, to photograph or film, to move rapidly, or to score in sports by propelling a ball toward a goal. In firearms context, shooting involves aiming and firing bullets or other projectiles. Photography shooting captures images with cameras, while film shooting records moving pictures. Sports shooting includes basketball shots, soccer shots, or archery. The word also describes rapid movement, as in "shooting across the room." Plant biology uses "shoot" for new growth stems emerging from seeds or existing plants. Each context maintains the core concept of propelling something toward a target or growing/moving in a specific direction.',
            'pronunciation': '/ʃut/',
            'example_sentence': 'The photographer asked the model to _____ several different poses for the magazine cover.',
            'etymology': 'From Old English "scēotan," meaning "to project" or "to propel," related to "shot" and "shut."',
            'mnemonic': 'Think "SHOOT = Send HOt Objects To target" - propelling something toward an aim.',
            'source': 'Claude'
        },
        'shop': {
            'definition': 'A shop is a retail establishment where goods or services are sold directly to consumers, ranging from small specialty stores to large retail outlets. The term encompasses various business types: grocery shops for food, clothing shops for apparel, repair shops for services, and workshop spaces for manufacturing or crafting. Shopping involves the act of visiting these establishments to purchase items or compare products. Online shops have expanded the concept to digital marketplaces accessible through websites and applications. The word also functions as a verb meaning to browse and purchase goods. Traditional shops often serve as community gathering places, contributing to local economic and social life.',
            'pronunciation': '/ʃɑp/',
            'example_sentence': 'The antique _____ on Main Street had fascinating vintage items from the early 1900s.',
            'etymology': 'From Old English "sceoppa," meaning "booth" or "stall," related to "shed" as a place of shelter for commerce.',
            'mnemonic': 'Think "SHOP = Store Helping Offer Products" - a place that offers products for sale.',
            'source': 'Claude'
        },
        'shopaholic': {
            'definition': 'A shopaholic is a person who has an excessive or compulsive desire to shop and purchase items, often beyond their financial means or actual need for the products. This behavior pattern, sometimes called retail therapy or compulsive buying disorder, can become problematic when it interferes with daily life, relationships, or financial stability. Shopaholics may experience temporary emotional highs from purchasing but often feel guilt, anxiety, or regret afterward. The condition might stem from various psychological factors including stress relief, social pressure, or attempts to fill emotional voids. Treatment may involve therapy, financial counseling, and developing healthier coping mechanisms for underlying emotional issues.',
            'pronunciation': '/ˈʃɑpəˌhɔlɪk/',
            'example_sentence': 'She recognized she was becoming a _____ when her credit card bills exceeded her monthly income three months in a row.',
            'etymology': 'Coined in the 1980s, combining "shop" + "aholic" (from "alcoholic"), suggesting addiction-like behavior toward shopping.',
            'mnemonic': 'Think "SHOP-A-HOLIC = addicted to SHOPping A whole LOT" - someone who shops compulsively.',
            'source': 'Claude'
        },
        'shops': {
            'definition': 'Shops are retail establishments where merchants sell goods or services to customers, forming the backbone of commercial districts and shopping areas. These businesses range from small independent stores specializing in specific products to large chain retailers offering diverse merchandise. Traditional shopping districts feature rows of shops along streets, while modern shopping centers and malls house multiple shops under one roof. Online shops have revolutionized retail by allowing customers to browse and purchase from home. Different types include grocery shops, clothing stores, bookshops, repair shops, and specialty boutiques. Shops serve both economic functions by facilitating trade and social functions by creating community gathering spaces.',
            'pronunciation': '/ʃɑps/',
            'example_sentence': 'The historic downtown area featured charming local _____ selling handmade crafts and regional specialties.',
            'etymology': 'Plural of "shop," from Old English "sceoppa," meaning "booth" or "stall" for selling goods.',
            'mnemonic': 'Think "SHOPS = Several Helpful Outlets Providing Stuff" - multiple stores offering various products.',
            'source': 'Claude'
        },
        'shore': {
            'definition': 'Shore refers to the land along the edge of a large body of water such as an ocean, sea, or lake, characterized by the meeting point between water and land. This area experiences constant interaction between aquatic and terrestrial environments, creating unique ecosystems that support diverse plant and animal life. Shores can be sandy beaches, rocky coasts, mudflats, or cliff faces, each shaped by waves, tides, and weather patterns over time. The term extends metaphorically to mean providing support or strengthening something, as in "shoring up" a weak structure. Coastal shores are popular recreational areas for swimming, fishing, and tourism, while also serving crucial roles in marine ecology and coastal protection.',
            'pronunciation': '/ʃɔr/',
            'example_sentence': 'The family spent their vacation walking along the rocky _____, collecting seashells and watching seabirds.',
            'etymology': 'From Middle Dutch "schore," meaning "land cut off" or "boundary," referring to the edge between water and land.',
            'mnemonic': 'Think "SHORE = where Sea Hits Our Real Earth" - the boundary between water and land.',
            'source': 'Claude'
        },
        'short': {
            'definition': 'Short describes something having little length, height, duration, or extent in comparison to what is normal, expected, or desired. In physical terms, it refers to reduced dimensions, such as short hair, short people, or short distances. Temporally, short indicates brief duration, like short meetings or short stories. The word can describe insufficient quantities, as in "short of money" or "short supply." In finance, short selling involves selling borrowed securities. Short can also mean abrupt or curt in communication style. The versatility of this word makes it applicable across physical, temporal, quantitative, and behavioral contexts, always indicating reduction or abbreviation from a standard or expected measure.',
            'pronunciation': '/ʃɔrt/',
            'example_sentence': 'The _____ story captivated readers with its powerful message delivered in just three pages.',
            'etymology': 'From Old English "sceort," related to "shirt" and "skirt," originally meaning "cut off" or "abbreviated."',
            'mnemonic': 'Think "SHORT = Smaller Height Or Reduced Time" - anything that is less than normal length or duration.',
            'source': 'Claude'
        },
        'shortfall': {
            'definition': 'A shortfall is a deficiency or shortage in the amount or quantity of something that was expected, needed, or promised, particularly in financial contexts where actual income, production, or resources fail to meet projected targets. This gap between expectations and reality can occur in business revenues, budget allocations, crop yields, or any situation where planned outcomes exceed actual results. Shortfalls often require corrective action such as additional funding, revised strategies, or alternative resource allocation. The term implies a measurable difference between what was anticipated and what was achieved, creating problems that need addressing. Understanding and managing potential shortfalls is crucial for effective planning and risk management in various fields.',
            'pronunciation': '/ˈʃɔrtˌfɔl/',
            'example_sentence': 'The company faced a significant budget _____ when sales dropped twenty percent below projected figures.',
            'etymology': 'Compound word from "short" (insufficient) + "fall" (to come short of a mark), dating to the early 20th century.',
            'mnemonic': 'Think "SHORT-FALL = falling SHORT of expectations" - not reaching the expected target or amount.',
            'source': 'Claude'
        },
        'shoulder': {
            'definition': 'The shoulder is the joint connecting the arm to the torso, consisting of several bones (clavicle, scapula, and humerus) that work together to provide the arm\'s remarkable range of motion. This ball-and-socket joint allows movement in multiple directions, making it one of the most mobile but also most vulnerable joints in the human body. Beyond anatomy, "shoulder" metaphorically represents taking on responsibility, as in "shouldering a burden." The word also describes the edge or margin of roads, mountains, or other structures. Shoulder muscles and tendons enable arm movement and support upper body posture. Injury prevention and strengthening exercises are important for maintaining shoulder health.',
            'pronunciation': '/ˈʃoʊldər/',
            'example_sentence': 'The baseball pitcher felt pain in his throwing _____ after practicing curveballs for three hours.',
            'etymology': 'From Old English "sculdor," related to Dutch "schouder" and German "Schulter," meaning "the part that carries."',
            'mnemonic': 'Think "SHOULD-ER carry things" - shoulders are what should carry weight and responsibility.',
            'source': 'Claude'
        },
        'shouldn': {
            'definition': 'This appears to be an incomplete contraction, likely intended to be "shouldn\'t" (should not), which expresses that something is not advisable, appropriate, or recommended. "Shouldn\'t" combines the modal verb "should" (indicating obligation, propriety, or expectation) with the negative "not," creating advice against a particular action or situation. The contraction is commonly used in informal speech and writing to express gentle prohibition, recommendation against something, or indication that an action would be improper or unwise. Without the apostrophe and "t," "shouldn" is not a complete English word and likely represents a typographical error or incomplete transcription.',
            'pronunciation': '/ˈʃʊdənt/',
            'example_sentence': 'You _____ eat that expired food; it could make you sick.',
            'etymology': 'Contraction of "should not," where "should" comes from Old English "scolde" (past tense of "shall").',
            'mnemonic': 'Think "SHOULD-N\'T = SHOULD NOT do something" - advice against an action.',
            'source': 'Claude'
        },
        'shout': {
            'definition': 'Shout means to speak or call out loudly, typically to attract attention, express strong emotion, or communicate across distance or noise. This vocal behavior involves increased volume and often higher pitch than normal speech, requiring greater respiratory effort and vocal cord tension. Shouting can express various emotions including anger, excitement, fear, or joy, and serves practical functions like warning of danger or calling to someone far away. In social contexts, shouting might be considered rude or aggressive, while in others like sporting events or celebrations, it\'s perfectly appropriate. The word also functions as a noun describing the loud vocalization itself.',
            'pronunciation': '/ʃaʊt/',
            'example_sentence': 'She had to _____ over the loud music to get her friend\'s attention across the crowded party.',
            'etymology': 'Middle English, possibly from Old Norse "skuta" meaning "to shoot" or "to project," referring to projecting the voice.',
            'mnemonic': 'Think "SH-OUT = SHoot your voice OUT loud" - projecting your voice loudly outward.',
            'source': 'Claude'
        },
        'showed': {
            'definition': 'Showed is the past tense of the verb "show," meaning to display, demonstrate, or present something to others so they can see, understand, or experience it. This action involves making something visible or comprehensible that might otherwise be hidden, unclear, or unknown. Showing can involve physical demonstration, like showing someone how to use a tool, or abstract presentation, like showing kindness or showing the way. The word encompasses both intentional acts of revelation and unintentional displays where something becomes apparent. In various contexts, showed can mean guided, proved, exhibited, revealed, or indicated, making it a versatile verb for describing communication and demonstration.',
            'pronunciation': '/ʃoʊd/',
            'example_sentence': 'The teacher _____ the students how to solve the complex equation step by step.',
            'etymology': 'Past tense of "show," from Old English "scēawian," meaning "to look at" or "to see."',
            'mnemonic': 'Think "SHO-WED = SHOwed What Everyone Desired to see" - displayed what others wanted to see.',
            'source': 'Claude'
        },
        'shower': {
            'definition': 'A shower can refer to a brief fall of rain, snow, or other precipitation, typically lighter and shorter than sustained weather patterns. In personal hygiene, a shower is a method of washing the body using a spray of water, usually in a specially designed bathroom fixture. The term also describes a gathering where guests bring gifts for someone celebrating a special occasion, such as a baby shower or bridal shower. Metaphorically, shower can mean to give abundantly, as in "showering someone with praise." The word encompasses both the delivery system that produces the spray pattern and the act of using such a system for cleansing or precipitation from the sky.',
            'pronunciation': '/ˈʃaʊər/',
            'example_sentence': 'The afternoon _____ cooled the air and watered the garden just when the plants needed it most.',
            'etymology': 'From Old English "scūr," meaning "storm" or "heavy fall," related to "shear" and the idea of cutting through the air.',
            'mnemonic': 'Think "SHOW-ER water" - something that shows or sprays water from above.',
            'source': 'Claude'
        }
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            words = list(reader)
        
        print(f"Processing {len(words)} words from batch 159...")
        
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
        
        print(f"\nBatch 159 processing complete!")
        print(f"Successfully processed {len(processed_data)}/{len(words)} words")
        print(f"Output saved to: {output_file}")
        
        if combined_errors:
            print(f"\nCombined word errors detected: {len(combined_errors)}")
            for error in combined_errors:
                print(f"  - {error}")
        
    except Exception as e:
        print(f"Error processing batch 159: {str(e)}")
        raise

if __name__ == "__main__":
    main()