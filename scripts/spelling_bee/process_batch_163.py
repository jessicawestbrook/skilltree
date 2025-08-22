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
    input_file = os.path.join(script_dir, 'output', 'batch_163_words.csv')
    output_file = os.path.join(script_dir, 'output', 'batch_163_processed.csv')
    
    calculator = DifficultyCalculator()
    
    # Comprehensive word data with educational content
    word_data = {
        'soap': {
            'definition': 'Soap is a cleansing agent made from fats or oils combined with an alkali, typically sodium hydroxide (lye), through a chemical process called saponification that creates a substance capable of removing dirt, grease, and other contaminants from surfaces. This essential hygiene product works by reducing surface tension of water and forming emulsions that allow oil-based dirt to be washed away with water. Soap comes in various forms including bar soap, liquid soap, and specialty formulations for different purposes. The basic chemistry involves fatty acid molecules with hydrophilic (water-loving) and hydrophobic (water-repelling) ends that surround and lift away dirt particles. Soap has been crucial for public health and personal hygiene throughout human civilization.',
            'pronunciation': '/soʊp/',
            'example_sentence': 'She washed her hands thoroughly with _____ and warm water to remove all traces of paint from her fingers.',
            'etymology': 'From Old English "sāpe," from Proto-Germanic "*saipōn," possibly related to Latin "sebum" (tallow).',
            'mnemonic': 'Think "SOAP = Substance that\'s Only for cleaning And Purifying" - cleaning agent that removes dirt.',
            'source': 'Claude'
        },
        'sobersides': {
            'definition': 'Sobersides is a noun referring to a person who is habitually serious, grave, or solemn in demeanor, often to the point of being perceived as humorless or overly earnest. This term describes someone who rarely jokes, laughs, or engages in lighthearted behavior, preferring to maintain a dignified, responsible, or scholarly attitude. While sobersides individuals may be respected for their reliability and thoughtfulness, they might also be seen as lacking spontaneity or fun. The word can be used both descriptively and mildly critically, suggesting that while seriousness has its place, excessive gravity can make someone seem dull or unapproachable. Such people often excel in serious professions requiring careful judgment.',
            'pronunciation': '/ˈsoʊbərˌsaɪdz/',
            'example_sentence': 'Despite his reputation as a _____, the professor occasionally surprised students with his dry wit.',
            'etymology': 'Compound of "sober" (serious, temperate) + "sides" (aspects), referring to someone who shows only serious aspects.',
            'mnemonic': 'Think "SOBER-SIDES = Shows Only the serious, Businesslike, Earnest aspects, Reserved personality, SIDES that are always serious" - habitually serious person.',
            'source': 'Claude'
        },
        'sobriety': {
            'definition': 'Sobriety refers to the state of being sober, which has two primary meanings: abstinence from alcohol or other intoxicating substances, and the quality of being serious, sensible, and thoughtful in behavior or judgment. In addiction recovery contexts, sobriety represents a crucial goal involving complete abstinence from substances that cause impairment. The term also describes clear-headed thinking free from emotional extremes or irrational influences. Sobriety often involves developing healthy coping mechanisms, building support networks, and making significant lifestyle changes. The concept emphasizes both physical health (avoiding substances) and mental clarity (maintaining rational thought and emotional stability). Achieving and maintaining sobriety typically requires ongoing effort and commitment.',
            'pronunciation': '/səˈbraɪəti/',
            'example_sentence': 'After years of struggle, she celebrated five years of _____ with her support group.',
            'etymology': 'From Old French "sobrieté," from Latin "sobrietas," from "sobrius" (not drunk, temperate).',
            'mnemonic': 'Think "SOBR-IETY = State Of Being Responsible, Including abstinence, Emotionally balanced, Thoughtful behavior" - being sober and serious.',
            'source': 'Claude'
        },
        'social': {
            'definition': 'Social refers to anything relating to society, human interaction, or the relationships between individuals and groups within communities. This fundamental concept encompasses how people connect, communicate, and organize themselves in various contexts from families and friendships to institutions and governments. Social behavior involves the ways people interact, share resources, establish norms, and create cultural practices. The term appears in numerous contexts: social media for online interaction, social services for community support, and social skills for interpersonal effectiveness. Understanding social dynamics is crucial for navigating relationships, contributing to communities, and participating effectively in democratic societies. Social structures influence individual opportunities and outcomes significantly.',
            'pronunciation': '/ˈsoʊʃəl/',
            'example_sentence': 'The new employee joined the company\'s _____ committee to help organize community outreach events.',
            'etymology': 'From Latin "socialis," from "socius" (companion, ally), referring to relationships between people.',
            'mnemonic': 'Think "SOC-IAL = Society Of people Connecting, Including All types of human relationships" - relating to human interaction and society.',
            'source': 'Claude'
        },
        'societal': {
            'definition': 'Societal describes things that relate to or affect society as a whole, particularly large-scale social structures, institutions, and cultural patterns that influence entire communities or populations. This adjective emphasizes the broad, collective aspects of human organization rather than individual or small-group dynamics. Societal issues include topics like inequality, education systems, healthcare access, and environmental policy that impact large numbers of people. Societal changes occur over long time periods and often result from multiple factors working together. Understanding societal forces helps explain why certain problems persist, how institutions develop, and what kinds of interventions might create positive change on a large scale.',
            'pronunciation': '/səˈsaɪətəl/',
            'example_sentence': 'The research examined _____ factors that contribute to educational inequality across different regions.',
            'etymology': 'From "society" + "-al" suffix, where "society" comes from Latin "societas" (fellowship, association).',
            'mnemonic': 'Think "SOCI-ETAL = SOCIety-wide effects, Everything Touching All Lives" - affecting all of society.',
            'source': 'Claude'
        },
        'sockets': {
            'definition': 'Sockets are receptacles, openings, or hollow spaces designed to receive and hold something else, most commonly referring to electrical outlets that accept plugs to provide power connections. In anatomy, sockets are hollow spaces in bones that hold other structures, such as eye sockets (orbits) that contain the eyes, or tooth sockets that hold teeth roots. Mechanical sockets receive bolts, light bulbs, or other components, while computer sockets connect processors, memory modules, or network cables. The design of sockets ensures secure, functional connections while allowing for removal or replacement when necessary. Proper socket design is crucial for safety, especially in electrical applications where poor connections can cause fires or electrocution.',
            'pronunciation': '/ˈsɑkɪts/',
            'example_sentence': 'The electrician installed additional power _____ in the kitchen to accommodate all the new appliances.',
            'etymology': 'From Old French "soket," diminutive of "soc" (plowshare), referring to a hollow receptacle.',
            'mnemonic': 'Think "SOCK-ETS = Spaces that reCeive other items, Including Electrical connections, Tool receptacles, Secure connections" - receptacles that hold other things.',
            'source': 'Claude'
        },
        'sodaseal': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "soda" and "seal." Soda can refer to carbonated soft drinks, sodium carbonate (washing soda), or sodium bicarbonate (baking soda). A seal can be an aquatic marine mammal, a device that prevents leakage, or an official mark of authentication. These are completely unrelated concepts that should not be combined. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈsoʊdə sil/',
            'example_sentence': 'The bottle of _____ had a tight _____ to prevent the carbonation from escaping.',
            'etymology': 'Soda: from Arabic "suwwād" (saltwort plant). Seal: from Old English "seolh" (marine mammal) or Old French "seel" (official mark).',
            'mnemonic': 'Remember these as TWO words: SODA (carbonated drink or sodium compound) + SEAL (marine mammal or closure device).',
            'source': 'Claude'
        },
        'sodden': {
            'definition': 'Sodden describes something that is thoroughly soaked, saturated, or drenched with liquid, typically water, to the point of being heavy, soft, or waterlogged. This adjective suggests complete saturation where the material has absorbed as much liquid as possible and may be dripping or soggy. Sodden ground after heavy rain becomes muddy and difficult to walk on, while sodden clothing feels heavy and uncomfortable. The term can also describe things that have lost their original texture or structure due to excessive moisture absorption. Metaphorically, sodden can describe minds or thinking that are dulled or heavy, as if waterlogged with confusion or fatigue.',
            'pronunciation': '/ˈsɑdən/',
            'example_sentence': 'The hikers\' boots became _____ after walking through the marsh, making each step increasingly difficult.',
            'etymology': 'Past participle of obsolete "sod" meaning "to soak," related to "seethe" and "soak."',
            'mnemonic': 'Think "SODD-EN = SOaked Down completely, Drenched ENtirely" - thoroughly soaked with liquid.',
            'source': 'Claude'
        },
        'sodium': {
            'definition': 'Sodium is a highly reactive chemical element with the symbol Na (from Latin natrium) and atomic number 11, classified as an alkali metal that is essential for human health but dangerous in its pure metallic form. This silvery-white metal reacts violently with water and must be stored under oil to prevent contact with moisture or air. In biological systems, sodium plays crucial roles in nerve transmission, muscle function, and fluid balance, primarily consumed as sodium chloride (table salt). Sodium compounds are widely used in industry, food processing, and household products. While necessary for life, excessive sodium intake can contribute to high blood pressure and cardiovascular problems, making dietary sodium management important for health.',
            'pronunciation': '/ˈsoʊdiəm/',
            'example_sentence': 'The doctor advised reducing _____ intake to help manage the patient\'s high blood pressure.',
            'etymology': 'From "soda" + "-ium" suffix, where "soda" comes from Arabic "suwwād" referring to saltwort plants.',
            'mnemonic': 'Think "SODI-UM = Salt Or other compounds, Dangerous pure metal, Important for body, Used in many products" - essential but reactive metal element.',
            'source': 'Claude'
        },
        'sofa': {
            'definition': 'A sofa is a long, upholstered seat designed to accommodate multiple people, typically featuring a back and armrests, used for comfortable sitting or reclining in living rooms, offices, or other social spaces. This essential piece of furniture comes in various styles, sizes, and configurations, from simple two-seaters to elaborate sectional sofas that can seat many people. Sofas are usually constructed with wooden or metal frames, spring or foam cushioning, and fabric or leather upholstery. The design emphasizes comfort for extended sitting, conversation, or relaxation. Modern sofas may include additional features like reclining mechanisms, built-in storage, or convertible designs that transform into beds for overnight guests.',
            'pronunciation': '/ˈsoʊfə/',
            'example_sentence': 'The family gathered on the comfortable _____ to watch movies together on weekend evenings.',
            'etymology': 'From Arabic "ṣuffa" meaning "bench" or "platform," through Turkish and French into English.',
            'mnemonic': 'Think "SOFA = Seating Object For multiple people, Always comfortable" - long upholstered seat for multiple people.',
            'source': 'Claude'
        },
        'soft': {
            'definition': 'Soft describes a texture, surface, or material that yields easily to pressure, feels smooth and pleasant to touch, or lacks hardness and firmness. This versatile adjective applies to physical properties (soft fabric, soft skin), sounds (soft music, soft voice), lighting (soft glow), and even abstract concepts (soft approach, soft skills). Soft materials compress easily and conform to shapes, while soft sounds are gentle and not harsh or loud. In personality or behavior, soft suggests gentleness, kindness, or lack of severity. The concept of softness often implies comfort, safety, and pleasantness across various sensory and emotional contexts, making it generally associated with positive experiences.',
            'pronunciation': '/sɔft/',
            'example_sentence': 'The baby\'s _____ blanket provided comfort and warmth throughout the cold night.',
            'etymology': 'From Old English "sōfte," related to Old High German "semfti," meaning "gentle" or "mild."',
            'mnemonic': 'Think "SOFT = Surface that yields easily, Objects that Feel pleasant, Textures that are gentle" - yielding easily to pressure.',
            'source': 'Claude'
        },
        'softly': {
            'definition': 'Softly is an adverb describing actions performed in a gentle, quiet, or tender manner, with reduced force, volume, or intensity compared to normal or possible levels. This word applies to various behaviors: speaking softly means using a quiet voice, moving softly suggests careful, quiet movement, and touching softly indicates gentle contact. The adverb often conveys consideration for others, such as softly closing a door to avoid disturbing sleeping people. Softly can also describe the manner of light, music, or other sensory experiences that are pleasant and not overwhelming. The concept emphasizes care, gentleness, and awareness of impact on surroundings or other people.',
            'pronunciation': '/ˈsɔftli/',
            'example_sentence': 'She spoke _____ to avoid waking the sleeping children in the next room.',
            'etymology': 'From "soft" + "-ly" adverbial suffix, where "soft" comes from Old English "sōfte."',
            'mnemonic': 'Think "SOFT-LY = in a SOFT manner, LightlY and gently" - in a gentle, quiet manner.',
            'source': 'Claude'
        },
        'software': {
            'definition': 'Software refers to the collection of computer programs, applications, and instructions that tell hardware components what to do and how to perform specific tasks. Unlike hardware (physical components), software is intangible and consists of code written in programming languages that creates functionality users can interact with. Software categories include operating systems that manage computer resources, applications that perform specific tasks, and utilities that maintain system performance. Modern software ranges from simple mobile apps to complex enterprise systems that manage entire organizations. Software development involves designing, coding, testing, and maintaining programs that solve problems or provide entertainment. The software industry has become one of the world\'s most important economic sectors.',
            'pronunciation': '/ˈsɔftˌwɛr/',
            'example_sentence': 'The company invested in new accounting _____ to streamline their financial reporting processes.',
            'etymology': 'Coined in the 1960s as the opposite of "hardware," combining "soft" (changeable) + "ware" (goods).',
            'mnemonic': 'Think "SOFT-WARE = SOFT programmable instructions, Without physical form, Applications and programs, Running Electronically" - computer programs and applications.',
            'source': 'Claude'
        },
        'sohum': {
            'definition': 'Sohum is a Sanskrit mantra meaning "I am That" or "I am He," used in Hindu and yogic meditation practices to connect the individual self with universal consciousness or divine reality. This sacred sound combines "so" (That/He) referring to the divine or universal spirit, and "hum" (I am) referring to the individual self. Practitioners often synchronize the mantra with breathing, mentally saying "so" on inhalation and "hum" on exhalation, creating a meditative rhythm that promotes self-awareness and spiritual connection. The mantra appears in ancient Vedic texts and represents the fundamental unity between individual consciousness and cosmic consciousness, serving as a tool for self-realization and spiritual development.',
            'pronunciation': '/ˈsoʊhʌm/',
            'example_sentence': 'During meditation, she repeatedly chanted _____ to deepen her sense of spiritual connection.',
            'etymology': 'From Sanskrit "so\'ham," literally "so" (that, he) + "aham" (I), meaning "I am That."',
            'mnemonic': 'Think "SO-HUM = Sacred chant meaning I am connected to the divine, Helps Unite with universal consciousness, Meditative practice" - Sanskrit mantra meaning "I am That."',
            'source': 'Claude'
        },
        'soiree': {
            'definition': 'Soiree is an alternative spelling of "soirée," referring to an elegant evening party or social gathering, typically featuring sophisticated entertainment, conversation, and refreshments. These events often occur in private homes or refined venues and emphasize cultural activities such as music performances, literary readings, or intellectual discussions. Soirees traditionally begin in the early evening and create opportunities for social networking among educated or affluent individuals. The atmosphere tends to be more formal and refined than casual parties, with attention paid to proper etiquette, dress, and conversation. Such gatherings have historically played important roles in cultural and political circles, providing venues for artistic patronage and social influence.',
            'pronunciation': '/ˌswɑˈreɪ/',
            'example_sentence': 'The ambassador hosted an elegant _____ featuring chamber music and political discussions.',
            'etymology': 'From French "soirée," from "soir" (evening), referring to an evening social gathering.',
            'mnemonic': 'Think "SOIR-EE = SOcial gathering In the evening, Refined Entertainment, Elegant Evening party" - sophisticated evening social gathering.',
            'source': 'Claude'
        },
        'soirée': {
            'definition': 'Soirée is a French word referring to an elegant evening party or social gathering, typically featuring sophisticated entertainment, refined conversation, and cultural activities. These events often take place in private homes or upscale venues and emphasize intellectual or artistic pursuits such as music performances, poetry readings, or philosophical discussions. Soirées traditionally attract educated, cultured, or influential individuals who gather to socialize, network, and enjoy high-quality entertainment. The atmosphere is generally more formal and refined than typical parties, with attention to proper etiquette, appropriate dress, and stimulating conversation. Historically, soirées have served as important venues for cultural patronage, political discourse, and the development of artistic and intellectual movements.',
            'pronunciation': '/ˌswɑˈreɪ/',
            'example_sentence': 'The literary _____ featured readings by famous poets and attracted intellectuals from across the city.',
            'etymology': 'From French "soirée," from "soir" (evening) + "-ée" suffix, literally meaning "an evening\'s duration."',
            'mnemonic': 'Think "SOIR-ÉE = SOcial gathering In the evening, Refined cultural Entertainment, Elegant Evening affair" - sophisticated French evening party.',
            'source': 'Claude'
        },
        'sojourner': {
            'definition': 'A sojourner is a person who travels to and stays temporarily in a place, typically for a specific purpose such as work, study, pilgrimage, or personal exploration, with the intention of eventually returning home or moving elsewhere. This term suggests a temporary resident who maintains connections to another place they consider home, distinguishing sojourners from permanent immigrants or settlers. Sojourners might include seasonal workers, students studying abroad, missionaries, or people taking extended travels. The concept emphasizes the temporary nature of the stay and often implies that the person retains cultural, emotional, or practical ties to their place of origin. Historical sojourners have included migrant laborers, religious pilgrims, and explorers.',
            'pronunciation': '/ˈsoʊdʒərnər/',
            'example_sentence': 'As a _____ in the foreign country, she maintained strong connections to her homeland while learning new customs.',
            'etymology': 'From Old French "sojorner," from "sojorn" (sojourn), meaning "to dwell temporarily."',
            'mnemonic': 'Think "SO-JOURN-ER = SOmeone on a JOURNEY, staying temporarily, Expecting to Return" - temporary resident or traveler.',
            'source': 'Claude'
        },
        'solace': {
            'definition': 'Solace refers to comfort, consolation, or relief from distress, grief, or disappointment, often found through emotional support, pleasant activities, or changes in perspective that ease psychological pain. This comfort can come from various sources: human companionship, spiritual practices, creative activities, nature, or simple pleasures that provide emotional relief during difficult times. Solace doesn\'t necessarily solve problems but offers temporary respite that helps people cope with challenging circumstances. The word can function as both a noun (finding solace in music) and a verb (to solace someone in grief). Seeking and providing solace represents an important human capacity for healing and supporting one another through life\'s inevitable hardships.',
            'pronunciation': '/ˈsɑləs/',
            'example_sentence': 'After losing her job, she found _____ in long walks through the peaceful forest.',
            'etymology': 'From Old French "solas," from Latin "solacium," from "solari" (to console, comfort).',
            'mnemonic': 'Think "SOL-ACE = Soothing comfort during sadness, Obtaining peace, Lessening grief, Always Comforting, Easing pain" - comfort during distress.',
            'source': 'Claude'
        },
        'solar': {
            'definition': 'Solar refers to anything relating to the sun, our nearest star and the central body of our solar system that provides light and heat energy essential for life on Earth. The term appears in numerous contexts: solar energy harnesses sunlight for electricity or heating, solar panels convert sunlight to power, and solar calendars track time based on Earth\'s orbit around the sun. Solar radiation drives weather patterns, ocean currents, and the water cycle that sustains ecosystems. Solar technology has become increasingly important for renewable energy production as societies seek alternatives to fossil fuels. Understanding solar phenomena helps explain everything from daily weather patterns to long-term climate cycles and seasonal changes.',
            'pronunciation': '/ˈsoʊlər/',
            'example_sentence': 'The house featured _____ panels on the roof to generate clean electricity from sunlight.',
            'etymology': 'From Latin "solaris," from "sol" (sun), referring to anything related to the sun.',
            'mnemonic': 'Think "SOL-AR = relating to SOL (sun), Always about sun energy, Radiating from the sun" - relating to the sun.',
            'source': 'Claude'
        },
        'solder': {
            'definition': 'Solder is a fusible metal alloy used to join together metal components by melting the solder material and allowing it to flow into the joint, where it cools and solidifies to create a permanent connection. This process, called soldering, is fundamental in electronics manufacturing, plumbing, and metalworking. Common solder alloys include combinations of tin, lead, silver, or copper, chosen based on melting point requirements and application needs. Electronic soldering uses fine solder wire and heated tools to connect components to circuit boards, while plumbing soldering uses different alloys and torches for pipe joints. Proper soldering requires clean surfaces, appropriate temperatures, and flux materials that help the solder flow and bond effectively.',
            'pronunciation': '/ˈsɑdər/',
            'example_sentence': 'The technician used fine _____ and a precision iron to attach the tiny electronic components to the circuit board.',
            'etymology': 'From Old French "soudure," from "souder" (to solder), from Latin "solidare" (to make solid).',
            'mnemonic': 'Think "SOLD-ER = SOLiDifying metal to join components, Electronic Repairs use this" - metal alloy for joining components.',
            'source': 'Claude'
        },
        'solderinterim': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "solder" and "interim." Solder is a fusible metal alloy used to join metal components through a heating and cooling process. Interim refers to a temporary period between two events or a provisional arrangement during a transition. These are completely unrelated concepts - one from metalworking/electronics and the other from time management. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈsɑdər ˈɪntərɪm/',
            'example_sentence': 'He used _____ to repair the circuit board during the _____ period before the permanent technician arrived.',
            'etymology': 'Solder: from Latin "solidare" (to make solid). Interim: from Latin "interim" (in the meantime).',
            'mnemonic': 'Remember these as TWO words: SOLDER (metal joining alloy) + INTERIM (temporary time period).',
            'source': 'Claude'
        },
        'soldier': {
            'definition': 'A soldier is a person who serves in an army or military organization, trained and equipped to engage in warfare or other military operations in defense of their country, cause, or mission. Soldiers undergo rigorous physical and tactical training to develop skills in combat, weapons handling, strategy, and teamwork necessary for military effectiveness. Modern soldiers may serve in various roles including infantry, artillery, engineering, medical support, or specialized units like special forces. The profession requires courage, discipline, loyalty, and willingness to risk personal safety for larger purposes. Soldiers have played crucial roles throughout history in defending territories, maintaining peace, providing disaster relief, and supporting humanitarian missions worldwide.',
            'pronunciation': '/ˈsoʊldʒər/',
            'example_sentence': 'The young _____ wrote letters home describing the camaraderie and challenges of military training.',
            'etymology': 'From Old French "soldier," from "solde" (pay), referring to one who serves for pay.',
            'mnemonic': 'Think "SOLD-IER = SOLDier who serves, In military, Everyone trained for defense, Ready for duty" - military service member.',
            'source': 'Claude'
        },
        'soldiers': {
            'definition': 'Soldiers is the plural form of "soldier," referring to multiple members of military forces who are trained and equipped for warfare or other military operations. These individuals collectively form the backbone of armies and defense forces worldwide, working together in units that combine individual skills into effective team operations. Soldiers serve various functions including combat roles, support services, peacekeeping missions, and humanitarian assistance. Their coordinated efforts, discipline, and specialized training enable military organizations to accomplish complex missions requiring precise teamwork. Throughout history, soldiers have shaped the outcomes of conflicts, defended civilian populations, and contributed to international stability through their service and sacrifice.',
            'pronunciation': '/ˈsoʊldʒərz/',
            'example_sentence': 'The commanding officer addressed the _____ about their upcoming peacekeeping mission in the troubled region.',
            'etymology': 'Plural of "soldier," from Old French "soldier," from "solde" (pay).',
            'mnemonic': 'Think "SOLD-IERS = multiple SOLDiers, In military units, Everyone working together, Ready for Service" - multiple military service members.',
            'source': 'Claude'
        },
        'sole': {
            'definition': 'Sole has multiple related meanings: as an adjective, it means being the only one, single, or exclusive; as a noun, it refers to the bottom surface of the foot or shoe, or to a type of flatfish. When describing exclusivity, sole emphasizes that there are no others of the same kind or that someone has complete control or responsibility. The anatomical sole is the weight-bearing bottom surface of the foot, while shoe soles provide protection and traction. Sole fish are flatfish species popular in cuisine for their delicate flavor. The word\'s various meanings share the concept of being fundamental, bottom-most, or uniquely important in their respective contexts.',
            'pronunciation': '/soʊl/',
            'example_sentence': 'As the _____ heir to the family business, she inherited complete responsibility for its operations.',
            'etymology': 'From Old French "sol," from Latin "solus" (alone) for the adjective, and "solea" (sandal, flatfish) for the noun.',
            'mnemonic': 'Think "SOLE = Single Only instance, or bottom part, Like Exclusively one" - only one, or bottom surface.',
            'source': 'Claude'
        },
        'solecism': {
            'definition': 'Solecism refers to a grammatical error or violation of conventional language usage, such as incorrect syntax, improper word choice, or faulty sentence construction that deviates from accepted linguistic standards. The term has expanded beyond grammar to include any breach of etiquette, social convention, or proper behavior that violates established norms or expectations. In linguistic contexts, solecisms might include subject-verb disagreement, misplaced modifiers, or inappropriate register for the situation. Social solecisms involve breaches of manners, protocol, or cultural expectations. While some solecisms result from ignorance or carelessness, others occur when language naturally evolves or when speakers creatively bend rules for effect.',
            'pronunciation': '/ˈsɑləˌsɪzəm/',
            'example_sentence': 'The editor carefully reviewed the manuscript to eliminate any grammatical _____ before publication.',
            'etymology': 'From Latin "soloecismus," from Greek "soloikismos," named after Soloi, a city where Greek was supposedly spoken incorrectly.',
            'mnemonic': 'Think "SOLE-CISM = Speaking Only incorrectly, Language Error, Conventional rules Ignored, Social Mistake" - grammatical or social error.',
            'source': 'Claude'
        },
        'soleil': {
            'definition': 'Soleil is the French word for "sun," commonly encountered in English contexts through borrowed phrases, place names, or artistic references that maintain the French spelling for stylistic or cultural reasons. The word appears in expressions like "Cirque du Soleil" (Circus of the Sun), luxury brand names, wine appellations, and poetic or literary works that use French terminology for aesthetic effect. In French, soleil represents not just the astronomical body but also concepts of warmth, light, life, and positive energy. The retention of French spelling in English usage often serves to evoke sophistication, international flair, or specific cultural associations with French art, cuisine, or lifestyle.',
            'pronunciation': '/soʊˈleɪ/',
            'example_sentence': 'The famous performance troupe Cirque du _____ combines acrobatics with theatrical storytelling.',
            'etymology': 'From Latin "soliculus," diminutive of "sol" (sun), meaning "little sun."',
            'mnemonic': 'Think "SOL-EIL = SOL (sun) in French, Everyone knows from Cirque du Soleil, Illuminating Like the sun" - French word for sun.',
            'source': 'Claude'
        },
        'solemnzealous': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "solemn" and "zealous." Solemn describes something serious, grave, or formal in character, often associated with religious ceremonies or important occasions. Zealous describes someone who is fervent, enthusiastic, or passionate about a cause or belief. These are distinct adjectives that should not be combined. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈsɑləm ˈzɛləs/',
            'example_sentence': 'The ceremony was _____ and dignified, led by a _____ advocate for peace.',
            'etymology': 'Solemn: from Latin "sollemnis" (ceremonial). Zealous: from Greek "zelos" (zeal, eagerness).',
            'mnemonic': 'Remember these as TWO words: SOLEMN (serious, grave) + ZEALOUS (fervent, enthusiastic).',
            'source': 'Claude'
        },
        'solenoid': {
            'definition': 'A solenoid is an electromagnetic device consisting of a coil of wire that creates a magnetic field when electric current flows through it, often used to convert electrical energy into linear mechanical motion. The basic design features multiple turns of insulated wire wound in a cylindrical or helical shape, which generates a uniform magnetic field along its central axis when energized. Solenoids commonly operate valves, locks, switches, and other mechanical devices by attracting or repelling a movable iron core (plunger) that creates linear motion. Applications include automotive starters, irrigation valves, electronic door locks, and industrial automation systems. The strength of the magnetic field depends on factors like current, number of wire turns, and core material.',
            'pronunciation': '/ˈsoʊləˌnɔɪd/',
            'example_sentence': 'The automatic sprinkler system used a _____ valve to control water flow to different zones.',
            'etymology': 'From French "solénoïde," from Greek "solen" (tube, channel) + "-oid" (resembling).',
            'mnemonic': 'Think "SOLE-NOID = SOLEnoid creates motion, Operating Linear movement, Electronic coil, Not complex mechanism, Operates using Induced magnetism, Device with coiled wire" - electromagnetic coil device.',
            'source': 'Claude'
        },
        'solicit': {
            'definition': 'Solicit means to ask for, request, or seek something from someone, often in a formal, persistent, or professional manner. The term can refer to seeking various things: donations for charity, business proposals, votes in elections, or services for payment. Solicitation often involves approaching potential respondents systematically or professionally rather than casual asking. In legal contexts, soliciting can refer to specific regulated activities like practicing law or engaging in certain business practices. The word carries implications of active seeking rather than passive waiting, and may suggest professional or organized efforts to obtain desired responses. Some forms of solicitation are regulated by law to protect consumers from unwanted contact or fraudulent practices.',
            'pronunciation': '/səˈlɪsɪt/',
            'example_sentence': 'The nonprofit organization decided to _____ donations through a professional fundraising campaign.',
            'etymology': 'From Latin "sollicitare," from "sollicitus" (anxious, concerned), meaning "to disturb" or "to arouse."',
            'mnemonic': 'Think "SOLIC-IT = Seeking Out what you want, Looking for responses, Inquiring for donations, Calling for support, Including Targeted requests" - to ask for or seek something.',
            'source': 'Claude'
        },
        'solicitsolidity': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "solicit" and "solidity." Solicit means to ask for, request, or seek something from someone, often in a formal or persistent manner. Solidity refers to the state of being solid, firm, stable, or having substance and reliability. These are completely unrelated concepts - one describing a communication action and the other describing physical or metaphorical firmness. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/səˈlɪsɪt səˈlɪdɪti/',
            'example_sentence': 'The organization decided to _____ feedback to ensure the _____ of their planning process.',
            'etymology': 'Solicit: from Latin "sollicitare" (to arouse). Solidity: from Latin "solidus" (solid, firm).',
            'mnemonic': 'Remember these as TWO words: SOLICIT (to ask for or seek) + SOLIDITY (firmness, stability).',
            'source': 'Claude'
        },
        'solidity': {
            'definition': 'Solidity refers to the quality or state of being solid, firm, stable, or having substantial physical or metaphorical strength that can be relied upon. In physical terms, solidity describes materials that maintain their shape, resist deformation, and provide structural integrity. Metaphorically, solidity applies to concepts like financial stability, reliable character, sound reasoning, or dependable institutions that demonstrate consistency and trustworthiness over time. The term suggests permanence, reliability, and resistance to change or disruption. Solidity in relationships implies enduring commitment, while solidity in arguments indicates logical soundness. Understanding solidity helps evaluate the dependability and long-term viability of both physical structures and abstract concepts.',
            'pronunciation': '/səˈlɪdɪti/',
            'example_sentence': 'The bank\'s financial _____ gave customers confidence during the economic uncertainty.',
            'etymology': 'From Latin "soliditas," from "solidus" (solid, firm), referring to the quality of being solid.',
            'mnemonic': 'Think "SOLID-ITY = SOLID quality, Including stability, Dependable like rock, Integrity and firmness, Trustworthy foundation" - the quality of being solid and reliable.',
            'source': 'Claude'
        },
        'solipsist': {
            'definition': 'A solipsist is someone who adheres to solipsism, the philosophical position that only one\'s own mind and experiences can be known to exist with certainty, making it impossible to verify the existence of anything outside one\'s own consciousness. This extreme skeptical viewpoint suggests that other people, the external world, and even one\'s own body might be illusions or mental constructs rather than independently existing realities. While few people seriously maintain pure solipsistic beliefs in daily life, the concept raises important questions about knowledge, consciousness, and the nature of reality. Solipsism represents one of the most radical forms of philosophical skepticism, challenging basic assumptions about shared reality and interpersonal communication.',
            'pronunciation': '/ˈsɑlɪpsɪst/',
            'example_sentence': 'The philosophy student struggled with the _____ argument that questioned whether other minds truly exist.',
            'etymology': 'From Latin "solus" (alone) + "ipse" (self), literally meaning "self alone."',
            'mnemonic': 'Think "SOL-IPS-IST = believes only the SELF exists, Only I am sure, Living in Personal reality, I alone exist, Philosophical position of Self-only, I cannot prove others exist" - believer that only one\'s own mind exists.',
            'source': 'Claude'
        },
        'solitaire': {
            'definition': 'Solitaire refers to card games designed for a single player, typically involving arranging cards according to specific rules to achieve a winning configuration, with the goal of clearing the table or building complete sequences. The most common version involves dealing cards into columns and moving them according to rank and suit rules to build foundation piles. Solitaire has become a popular computer game, offering entertainment and mental exercise through pattern recognition and strategic planning. The term also applies to other solo activities or to jewelry featuring a single prominent stone, particularly diamond rings with one central gem. The concept emphasizes individual activity and self-contained challenge.',
            'pronunciation': '/ˌsɑləˈtɛr/',
            'example_sentence': 'During her lunch break, she enjoyed playing _____ on her computer to relax and clear her mind.',
            'etymology': 'From French "solitaire," from Latin "solitarius" (solitary, alone), referring to games played alone.',
            'mnemonic': 'Think "SOLIT-AIRE = SOLITary game played by one person, All by yourself, Individual card game, Really Entertaining alone" - card game for one player.',
            'source': 'Claude'
        },
        'solitairedishevel': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "solitaire" and "dishevel." Solitaire refers to card games played by one person or jewelry featuring a single prominent stone. Dishevel means to make messy, untidy, or disordered, particularly referring to hair, clothing, or appearance. These are completely unrelated concepts - one describing games or jewelry and the other describing messiness. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˌsɑləˈtɛr dɪˈʃɛvəl/',
            'example_sentence': 'She played _____ while trying not to _____ her carefully styled hair.',
            'etymology': 'Solitaire: from French "solitaire" (solitary). Dishevel: from Old French "descheveler" (to disarrange hair).',
            'mnemonic': 'Remember these as TWO words: SOLITAIRE (solo card game or single-stone jewelry) + DISHEVEL (make messy or untidy).',
            'source': 'Claude'
        },
        'solitude': {
            'definition': 'Solitude refers to the state of being alone or isolated from others, either by choice or circumstance, often associated with peace, reflection, and personal contemplation rather than loneliness or abandonment. Unlike loneliness, which involves feelings of sadness or disconnection, solitude can be a positive, restorative experience that allows for introspection, creativity, and spiritual growth. Many people seek solitude to think clearly, make important decisions, engage in artistic pursuits, or simply recharge from social interactions. Solitude has been valued by philosophers, artists, and spiritual practitioners throughout history as essential for personal development. The quality of solitude depends largely on whether it\'s chosen voluntarily and how it\'s used.',
            'pronunciation': '/ˈsɑləˌtud/',
            'example_sentence': 'She cherished the _____ of her mountain cabin, where she could write without distractions.',
            'etymology': 'From Latin "solitudo," from "solus" (alone), referring to the state of being alone.',
            'mnemonic': 'Think "SOLIT-UDE = SOLITary state, Used for reflection, Deliberately Alone, Ultimate peace, Deliberately chosen aloneness, Everyone needs some" - peaceful state of being alone.',
            'source': 'Claude'
        },
        'solitudeoptician': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "solitude" and "optician." Solitude refers to the peaceful state of being alone, often chosen for reflection or personal time. An optician is a healthcare professional who fits and dispenses eyeglasses, contact lenses, and other vision correction devices based on prescriptions from eye doctors. These are completely unrelated concepts - one describing a state of aloneness and the other describing a healthcare profession. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈsɑləˌtud ɑpˈtɪʃən/',
            'example_sentence': 'She enjoyed the _____ of reading while waiting for her appointment with the _____.',
            'etymology': 'Solitude: from Latin "solitudo" (aloneness). Optician: from French "opticien," from "optique" (optics).',
            'mnemonic': 'Remember these as TWO words: SOLITUDE (peaceful aloneness) + OPTICIAN (eye care professional).',
            'source': 'Claude'
        },
        'solomon': {
            'definition': 'Solomon refers to the legendary king of ancient Israel renowned for his wisdom, wealth, and building projects, particularly the First Temple in Jerusalem, who ruled during the 10th century BCE according to biblical accounts. Historical and religious traditions credit Solomon with extraordinary judicial wisdom, demonstrated in famous stories like his proposal to split a disputed baby to determine the true mother. He is traditionally associated with several biblical books including Proverbs, Ecclesiastes, and Song of Songs. Solomon\'s reign represented the height of Israel\'s power and prosperity, featuring extensive trade relationships and magnificent construction projects. The name has become synonymous with wisdom, and "Solomonic" decisions refer to wise, fair judgments in complex situations.',
            'pronunciation': '/ˈsɑləmən/',
            'example_sentence': 'The judge\'s decision was praised as _____ in its wisdom and fairness to all parties involved.',
            'etymology': 'From Hebrew "Shlomo," possibly related to "shalom" (peace), meaning "peaceful."',
            'mnemonic': 'Think "SOLO-MON = Sole ruler MOst famous for wisdom, Notably wise king, Making Outstanding judgments" - biblical king famous for wisdom.',
            'source': 'Claude'
        },
        'solon': {
            'definition': 'Solon refers to a wise lawgiver or a member of a legislative body, derived from Solon of Athens (630-560 BCE), an ancient Greek statesman and poet who instituted important legal and constitutional reforms. The historical Solon is credited with laying foundations for Athenian democracy through laws that reduced the power of aristocrats and protected ordinary citizens from debt slavery. In modern usage, "solon" has become a somewhat formal or literary term for legislators, senators, or other government officials involved in making laws. The word carries connotations of wisdom, experience, and thoughtful governance, suggesting that the person referred to possesses the judgment and integrity associated with the historical figure.',
            'pronunciation': '/ˈsoʊlɑn/',
            'example_sentence': 'The veteran _____ was respected by colleagues for his deep understanding of constitutional law.',
            'etymology': 'Named after Solon of Athens, ancient Greek lawgiver and poet (c. 630-560 BCE).',
            'mnemonic': 'Think "SOL-ON = wise SOLution maker, Often makes New laws, Outstanding legislator" - wise lawmaker or legislator.',
            'source': 'Claude'
        },
        'solstice': {
            'definition': 'Solstice refers to either of two times each year when the sun reaches its highest or lowest point in the sky at noon, marking the longest and shortest days of the year in each hemisphere. The summer solstice occurs around June 21st in the Northern Hemisphere (December 21st in the Southern Hemisphere), creating the longest day and shortest night. The winter solstice occurs around December 21st in the Northern Hemisphere (June 21st in the Southern Hemisphere), producing the shortest day and longest night. These astronomical events result from Earth\'s tilted axis as it orbits the sun, causing seasonal variations in daylight hours. Solstices have been celebrated across cultures throughout history as important markers of seasonal change.',
            'pronunciation': '/ˈsɑlstɪs/',
            'example_sentence': 'Many ancient cultures built monuments aligned with the _____ to track the changing seasons.',
            'etymology': 'From Latin "solstitium," from "sol" (sun) + "sistere" (to stand still), referring to the sun\'s apparent pause.',
            'mnemonic': 'Think "SOL-STICE = SOL (sun) STands still at highest/lowest point, Including longest/shortest days, Causing Extreme daylight" - when sun reaches extreme position.',
            'source': 'Claude'
        },
        'solution': {
            'definition': 'Solution has multiple related meanings: a method or process for solving a problem, or a liquid mixture where one substance is dissolved in another. In problem-solving contexts, a solution provides an answer, resolution, or way to address challenges effectively. In chemistry, a solution is a homogeneous mixture where a solute (dissolved substance) is evenly distributed throughout a solvent (dissolving medium), such as salt dissolved in water. Mathematical solutions represent answers to equations or proofs of theorems. The concept emphasizes resolution, clarity, and the successful addressing of questions or problems. Effective solutions often require analysis, creativity, and systematic approaches to achieve desired outcomes while considering constraints and consequences.',
            'pronunciation': '/səˈluʃən/',
            'example_sentence': 'The engineering team developed an innovative _____ to reduce energy consumption by thirty percent.',
            'etymology': 'From Latin "solutio," from "solvere" (to loosen, solve), referring to the act of solving or dissolving.',
            'mnemonic': 'Think "SOLUT-ION = SOLving something, Using Thought and planning, Including ONgoing process, Overcoming the problem, Now resolved" - answer or method for solving problems.',
            'source': 'Claude'
        },
        'solve': {
            'definition': 'Solve means to find an answer, explanation, or resolution to a problem, puzzle, mystery, or challenging situation through analysis, reasoning, or systematic investigation. This process typically involves understanding the nature of the problem, gathering relevant information, applying appropriate methods or strategies, and arriving at a satisfactory conclusion. Solving can apply to mathematical equations, scientific questions, personal dilemmas, technical issues, or social problems. Effective problem-solving often requires creativity, logical thinking, persistence, and sometimes collaboration with others. The ability to solve problems is fundamental to learning, innovation, and progress in virtually all fields of human endeavor.',
            'pronunciation': '/sɑlv/',
            'example_sentence': 'The detective worked tirelessly to _____ the mysterious case that had puzzled the department for months.',
            'etymology': 'From Latin "solvere," meaning "to loosen," "to untie," or "to resolve."',
            'mnemonic': 'Think "SOLVE = Search Out answers, Look for solutions, Verify results, Eventually find the answer" - find solution to problem.',
            'source': 'Claude'
        },
        'solvency': {
            'definition': 'Solvency refers to the financial condition where an individual, business, or organization has sufficient assets and income to meet long-term debts and financial obligations as they become due. This crucial financial concept indicates that total assets exceed total liabilities, suggesting the entity can continue operating and fulfilling commitments without facing bankruptcy. Solvency analysis involves examining balance sheets, cash flow statements, and debt-to-equity ratios to assess financial stability. Strong solvency provides confidence to creditors, investors, and business partners, while weak solvency signals potential financial distress. Maintaining solvency requires careful financial management, adequate reserves, and sustainable business practices that generate sufficient revenue to cover expenses and debt service.',
            'pronunciation': '/ˈsɑlvənsi/',
            'example_sentence': 'The bank\'s _____ report showed strong financial health despite the economic downturn.',
            'etymology': 'From "solvent" + "-cy," where "solvent" comes from Latin "solvere" (to pay, discharge debt).',
            'mnemonic': 'Think "SOLV-ENCY = SOLVing financial problems, Enough money, No debt troubles, Can pay bills, Years of financial stability" - ability to pay debts and obligations.',
            'source': 'Claude'
        },
        'solvencysoprano': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "solvency" and "soprano." Solvency refers to the financial ability to meet long-term debts and obligations. Soprano refers to the highest female voice type in music or a singer with this voice range. These are completely unrelated concepts - one from finance and the other from music. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈsɑlvənsi səˈprɑnoʊ/',
            'example_sentence': 'The opera company\'s financial _____ allowed them to hire the world-famous _____.',
            'etymology': 'Solvency: from Latin "solvere" (to pay debts). Soprano: from Italian "soprano" (above, highest).',
            'mnemonic': 'Remember these as TWO words: SOLVENCY (financial ability to pay debts) + SOPRANO (highest female voice).',
            'source': 'Claude'
        },
        'somatotype': {
            'definition': 'Somatotype refers to a classification system for human body types developed by psychologist William Sheldon in the 1940s, categorizing physiques into three primary types: ectomorph (thin, linear build), mesomorph (muscular, athletic build), and endomorph (rounded, softer build). This system assigns individuals ratings on a 1-7 scale for each component, creating a three-number somatotype like 2-6-3. While originally linked to personality theories that have been largely debunked, somatotyping continues to be used in sports science, nutrition, and fitness to understand how body composition affects athletic performance and training responses. Modern applications focus on physical characteristics rather than psychological correlations, helping athletes and trainers develop appropriate exercise and nutrition strategies.',
            'pronunciation': '/ˈsoʊmətoʊˌtaɪp/',
            'example_sentence': 'The sports scientist analyzed each athlete\'s _____ to design personalized training programs.',
            'etymology': 'From Greek "soma" (body) + "typos" (type, form), referring to body type classification.',
            'mnemonic': 'Think "SOMATO-TYPE = SOMA (body) TYPE classification, Organizing people by physical build, Mesomorph/Ectomorph/Endomorph, Athletic Training uses this, Three main body categories, Organizing by Physical characteristics" - system for classifying body types.',
            'source': 'Claude'
        },
        'somber': {
            'definition': 'Somber describes a mood, atmosphere, or appearance that is serious, grave, melancholy, or subdued, often associated with sadness, solemnity, or thoughtful reflection. This adjective characterizes situations, expressions, colors, or environments that convey weightiness or lack of brightness and cheerfulness. Somber occasions might include funerals, memorial services, or serious discussions about difficult topics. Somber colors are typically dark and muted, like deep grays, browns, or blacks. The word suggests dignity and respect for serious matters rather than inappropriate lightness or frivolity. Somber moods often accompany contemplation of significant losses, challenges, or profound responsibilities that require thoughtful, respectful attention.',
            'pronunciation': '/ˈsɑmbər/',
            'example_sentence': 'The memorial service had a _____ atmosphere as people gathered to honor the fallen soldiers.',
            'etymology': 'From French "sombre," possibly from Latin "sub umbra" (under shadow), referring to darkness or gloom.',
            'mnemonic': 'Think "SOMBER = Serious Outlook, Mournful feelings, Brooding atmosphere, Everyone Reflective" - serious and melancholy.',
            'source': 'Claude'
        },
        'sombre': {
            'definition': 'Sombre is the British/Commonwealth spelling of "somber," describing a mood, atmosphere, or appearance that is serious, grave, melancholy, or subdued, often associated with sadness, solemnity, or thoughtful reflection. This adjective characterizes situations, expressions, colors, or environments that convey weightiness or lack of brightness and cheerfulness. Sombre occasions include funerals, memorial services, or serious discussions about difficult topics. Sombre colors are typically dark and muted. The spelling variation reflects British English conventions while maintaining the same meaning as the American spelling, suggesting dignity and respect for serious matters rather than inappropriate lightness.',
            'pronunciation': '/ˈsɑmbər/',
            'example_sentence': 'The painting\'s _____ tones reflected the artist\'s contemplative mood during that difficult period.',
            'etymology': 'British spelling of "somber," from French "sombre," possibly from Latin "sub umbra" (under shadow).',
            'mnemonic': 'Think "SOMBRE = Serious Outlook, Mournful feelings, Brooding atmosphere, Reflective Everyone" - British spelling of serious and melancholy.',
            'source': 'Claude'
        },
        'someone': {
            'definition': 'Someone is a pronoun referring to an unspecified person, used when the identity of the individual is unknown, irrelevant, or deliberately kept vague. This indefinite pronoun serves important grammatical and communicative functions, allowing speakers to discuss actions, characteristics, or situations involving people without naming specific individuals. Someone can refer to any person in general contexts ("someone should help") or to particular but unnamed individuals ("someone called for you"). The word emphasizes the human element while maintaining anonymity or generality. Understanding how to use someone correctly is fundamental to English grammar and effective communication, particularly in situations requiring discretion or when specific identity is unnecessary.',
            'pronunciation': '/ˈsʌmˌwʌn/',
            'example_sentence': '_____ left their umbrella in the conference room during yesterday\'s meeting.',
            'etymology': 'Compound of "some" + "one," meaning "some person" or "a person of unspecified identity."',
            'mnemonic': 'Think "SOME-ONE = SOME unspecified pErsOn, Not Everyone, Everyone knows it means a person" - an unspecified person.',
            'source': 'Claude'
        },
        'something': {
            'definition': 'Something is a pronoun referring to an unspecified thing, object, concept, or situation when the exact nature or identity is unknown, unimportant, or deliberately vague. This indefinite pronoun allows communication about items, ideas, or events without precise specification, serving crucial roles in everyday language. Something can refer to physical objects ("something on the table"), abstract concepts ("something bothering me"), or situations ("something happened"). The word provides flexibility in expression while maintaining meaning when specificity is unnecessary or impossible. Understanding how to use something effectively is essential for clear communication, particularly when discussing unknown quantities, expressing uncertainty, or maintaining appropriate vagueness in conversation.',
            'pronunciation': '/ˈsʌmθɪŋ/',
            'example_sentence': 'There\'s _____ unusual about the way the computer is running today.',
            'etymology': 'Compound of "some" + "thing," meaning "some unspecified thing or matter."',
            'mnemonic': 'Think "SOME-THING = SOME unspecified THING, Not Everything, Everyone knows it means an object/concept" - an unspecified thing or concept.',
            'source': 'Claude'
        },
        'sometime': {
            'definition': 'Sometime functions as an adverb meaning "at some unspecified time in the future or past," indicating that an event will occur or has occurred but without specifying exactly when. This temporal reference provides useful flexibility when precise timing is unknown, unimportant, or deliberately vague. Sometime can refer to future plans ("we should meet sometime"), past events ("sometime last year"), or general time frames ("sometime during the day"). The word differs from "sometimes" (occasionally) and "some time" (a period of time). Understanding the distinction between these similar terms is important for clear communication about temporal relationships and scheduling.',
            'pronunciation': '/ˈsʌmˌtaɪm/',
            'example_sentence': '_____ next week we should schedule a meeting to discuss the project progress.',
            'etymology': 'Compound of "some" + "time," meaning "at some unspecified time."',
            'mnemonic': 'Think "SOME-TIME = at SOME unspecified TIME point, Not every time, Eventually it will happen" - at an unspecified time.',
            'source': 'Claude'
        },
        'sometimes': {
            'definition': 'Sometimes is an adverb meaning "occasionally" or "now and then," indicating that something happens at irregular intervals but not always or never. This frequency adverb describes the middle ground between "always" and "never," suggesting partial or intermittent occurrence of events, behaviors, or conditions. Sometimes implies variability and unpredictability in timing, distinguishing it from regular patterns. The word helps express qualified statements that acknowledge exceptions or variations rather than absolute claims. Understanding how to use sometimes correctly is important for accurate communication about habits, tendencies, and recurring but not constant phenomena. It differs from "sometime" (at some point) and "some time" (a duration).',
            'pronunciation': '/ˈsʌmˌtaɪmz/',
            'example_sentence': '_____ the weather is unpredictable, making it difficult to plan outdoor activities.',
            'etymology': 'From "sometime" + adverbial "-s," meaning "at some times" or "on some occasions."',
            'mnemonic': 'Think "SOME-TIMES = SOME occasions, not all TIMES, Multiple instances, Everyone knows it means occasionally" - occasionally or now and then.',
            'source': 'Claude'
        }
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            words = list(reader)
        
        print(f"Processing {len(words)} words from batch 163...")
        
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
        
        print(f"\nBatch 163 processing complete!")
        print(f"Successfully processed {len(processed_data)}/{len(words)} words")
        print(f"Output saved to: {output_file}")
        
        if combined_errors:
            print(f"\nCombined word errors detected: {len(combined_errors)}")
            for error in combined_errors:
                print(f"  - {error}")
        
    except Exception as e:
        print(f"Error processing batch 163: {str(e)}")
        raise

if __name__ == "__main__":
    main()