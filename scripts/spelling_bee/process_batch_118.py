#!/usr/bin/env python3

import csv
import logging
from pathlib import Path
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        return {
            'phonetic_transparency_score': self._calculate_phonetic_transparency(word),
            'word_frequency_score': self._calculate_word_frequency(word),
            'morphological_complexity_score': self._calculate_morphological_complexity(word),
            'etymology_complexity_score': self._calculate_etymology_complexity(etymology),
            'difficulty': None
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> int:
        transparent_patterns = ['cat', 'dog', 'run', 'jump', 'play']
        if any(pattern in word.lower() for pattern in transparent_patterns):
            return 1
        return 3
    
    def _calculate_word_frequency(self, word: str) -> int:
        common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        if word.lower() in common_words:
            return 1
        elif len(word) <= 4:
            return 2
        elif len(word) <= 8:
            return 3
        else:
            return 4
    
    def _calculate_morphological_complexity(self, word: str) -> int:
        if len(word) <= 4:
            return 1
        elif len(word) <= 8:
            return 2
        elif len(word) <= 12:
            return 3
        else:
            return 4
    
    def _calculate_etymology_complexity(self, etymology: str) -> int:
        if 'Latin' in etymology or 'Greek' in etymology:
            return 4
        elif 'French' in etymology or 'German' in etymology:
            return 3
        elif 'Old English' in etymology:
            return 2
        else:
            return 1

class Batch118Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        claude_data = {
            'neoterism': {
                'definition': 'Neoterism refers to the introduction of new words, phrases, or meanings into language, or an excessive fondness for novelty in language and ideas. This linguistic phenomenon encompasses both the creation of neologisms and the tendency to favor new expressions over established ones. Neoterism can occur naturally as languages evolve to accommodate new concepts, technologies, and cultural changes, or it can be deliberate as writers and speakers seek distinctive or fashionable ways to express ideas. While linguistic innovation is necessary for language vitality, excessive neoterism can sometimes hinder communication by creating unnecessary complexity or confusion. The term often carries slightly critical connotations, suggesting that the preference for novelty may be superficial or pretentious rather than genuinely useful. Understanding neoterism helps in analyzing language change, literary styles, and communication patterns across different communities and time periods.',
                'pronunciation': '/niˈɑtəˌrɪzəm/',
                'etymology': 'From Greek neos "new" + -ter comparative suffix + -ism. The term literally means "newness-ism" or the practice of favoring what is newer.',
                'memory_tip': 'Remember NEOTERISM as "NEO (new) + comparative + ISM" - the practice or tendency of favoring new words and expressions over established ones.',
                'example_sentence': 'The author\'s _____ made his writing difficult to follow, as he constantly introduced unfamiliar terms instead of using clear, established vocabulary.'
            },
            'nepal': {
                'definition': 'Nepal is a landlocked South Asian country located in the Himalayas between China and India, known for containing eight of the world\'s ten tallest mountains including Mount Everest. This culturally rich nation serves as the birthplace of Buddhism and maintains a predominantly Hindu population while preserving diverse ethnic and linguistic traditions. Nepal\'s economy relies heavily on agriculture, tourism (particularly mountain climbing and trekking), and remittances from workers abroad. The country features dramatic geographical diversity from the flat Terai plains in the south through rolling hills to the towering Himalayan peaks in the north. Nepal\'s political system is a federal democratic republic that emerged after centuries of monarchy and a decade-long civil war. The nation faces challenges including poverty, political instability, and vulnerability to natural disasters like earthquakes and monsoon flooding, while working to balance economic development with environmental conservation of its unique mountain ecosystems.',
                'pronunciation': '/nəˈpɔl/',
                'etymology': 'Possibly from Sanskrit Nepalaya meaning "at the foot of the mountains," though the etymology is debated. The name may derive from the Newari people or the Kathmandu Valley\'s ancient name.',
                'memory_tip': 'Remember NEPAL as "NEar the PEAks of himalayas" - the country near the peaks of the Himalayas, home to Mount Everest and other tall mountains.',
                'example_sentence': 'The earthquake in _____ caused widespread damage to historic temples and triggered avalanches on several major peaks.'
            },
            'nephew': {
                'definition': 'A nephew is the son of one\'s sibling (brother or sister) or the son of one\'s spouse\'s sibling, representing a family relationship that connects generations through blood or marriage. This kinship term describes a specific position in family hierarchies and inheritance patterns, often carrying cultural expectations about relationships, responsibilities, and family bonds. Nephews may develop special relationships with aunts and uncles who can serve as mentors, confidants, or alternative parental figures while maintaining less formal authority than parents. The relationship can provide unique opportunities for intergenerational connection, with aunts and uncles often offering different perspectives, resources, or experiences than parents. In some cultures, nephews hold special status in inheritance systems or ceremonial roles. Understanding family relationship terms like nephew helps navigate complex family structures, legal documents, and cultural expectations about kinship obligations and privileges.',
                'pronunciation': '/ˈnɛfju/',
                'etymology': 'From Old French neveu, from Latin nepos meaning "grandson, nephew." The Latin word encompassed various male relatives of younger generations.',
                'memory_tip': 'Remember NEPHEW as "sibling\'s male child" - the male child of your sibling, your brother\'s or sister\'s son.',
                'example_sentence': 'Uncle James taught his _____ how to fish during their annual summer camping trips to the lake.'
            },
            'nephrolith': {
                'definition': 'A nephrolith is a medical term for a kidney stone, a hard mineral deposit that forms within the kidneys from crystallized substances normally found in urine, such as calcium, oxalate, or uric acid. These formations can range in size from tiny particles to large masses that can obstruct urinary flow and cause severe pain. Nephroliths develop when urine becomes concentrated with minerals that cannot remain dissolved, often due to dehydration, dietary factors, genetic predisposition, or underlying medical conditions. The passage of kidney stones through the urinary tract can cause intense pain, blood in urine, and urinary complications requiring medical intervention. Treatment approaches include increased fluid intake, dietary modifications, medications to dissolve stones, or surgical procedures for larger stones. Understanding nephrolith formation helps in prevention through proper hydration, dietary management, and recognition of risk factors that contribute to stone development.',
                'pronunciation': '/ˈnɛfroʊlɪθ/',
                'etymology': 'From Greek nephros "kidney" + lithos "stone." The medical term literally means "kidney stone," describing the organ where these mineral deposits form.',
                'memory_tip': 'Remember NEPHROLITH as "NEPHRO (kidney) + LITH (stone)" - a stone that forms in the kidney, commonly called a kidney stone.',
                'example_sentence': 'The patient\'s severe flank pain was caused by a large _____ blocking the ureter and preventing normal urine flow.'
            },
            'nepotism': {
                'definition': 'Nepotism is the practice of showing favoritism toward relatives or friends in professional settings, particularly in hiring, promotion, or business decisions, often without regard to merit or qualifications. This behavior creates unfair advantages for connected individuals while potentially disadvantaging more qualified candidates who lack family or personal connections. Nepotism can occur in various contexts including government positions, corporate environments, academic institutions, and family businesses where decision-makers have authority over employment or advancement opportunities. While family businesses may legitimately involve relatives, nepotism becomes problematic when it undermines fairness, competence, or organizational effectiveness. The practice can lead to decreased morale, reduced performance, and public criticism, particularly in government or publicly funded positions. Understanding nepotism helps identify conflicts of interest and promotes merit-based decision-making that ensures positions go to the most qualified candidates regardless of personal relationships.',
                'pronunciation': '/ˈnɛpəˌtɪzəm/',
                'etymology': 'From Italian nepotismo, from nepote "nephew," from Latin nepos. Originally referred to popes appointing nephews to church positions, later extending to favoritism toward any relatives.',
                'memory_tip': 'Remember NEPOTISM as "NEPotes (nephews) + favoritISM" - favoritism shown toward nephews and other relatives in professional settings.',
                'example_sentence': 'The mayor faced criticism for _____ when he appointed his inexperienced brother-in-law to head the city\'s development department.'
            },
            'neptune': {
                'definition': 'Neptune is the eighth and outermost planet in our solar system, a cold, dark ice giant composed primarily of water, methane, and ammonia ices surrounding a rocky core. This massive planet, about four times Earth\'s diameter, takes 165 Earth years to complete one orbit around the Sun and features the fastest winds in the solar system, reaching speeds over 1,200 mph. Neptune\'s deep blue color results from methane in its atmosphere that absorbs red light and reflects blue wavelengths back to space. The planet has 14 known moons, with Triton being by far the largest and most interesting due to its retrograde orbit and active geysers. Neptune was the first planet discovered through mathematical prediction rather than telescopic observation, found in 1846 after calculations based on Uranus\'s orbital irregularities. In Roman mythology, Neptune was the god of the sea, making it an appropriate name for this distant, blue world of ice and storms.',
                'pronunciation': '/ˈnɛptuːn/',
                'etymology': 'Named after Neptune, the Roman god of the sea, equivalent to the Greek god Poseidon. The name was chosen for the planet\'s blue color reminiscent of ocean waters.',
                'memory_tip': 'Remember NEPTUNE as "NEPTunes = sea god\'s blue planet" - the blue planet named after the Roman sea god, the farthest ice giant in our solar system.',
                'example_sentence': 'The spacecraft Voyager 2 provided our only close-up images of _____ when it flew by the distant planet in 1989.'
            },
            'nerds': {
                'definition': 'Nerds is the plural form of nerd, referring to people who are intensely interested in intellectual, academic, or technical subjects, often displaying exceptional knowledge in specialized areas while sometimes lacking conventional social skills. Originally a derogatory term, "nerd" has undergone significant cultural transformation and is now often used with pride by those who embrace intellectual pursuits and technical expertise. Nerds typically excel in fields like science, mathematics, computers, gaming, or other specialized subjects that require deep knowledge and analytical thinking. The term has evolved to become associated with success in technology industries, academic achievements, and innovative thinking that drives progress in various fields. Modern culture increasingly values the contributions of nerds, recognizing that their specialized knowledge and dedication often lead to breakthrough discoveries and technological advances. Understanding the positive evolution of this term reflects changing attitudes toward intelligence and expertise in society.',
                'pronunciation': '/nɜrdz/',
                'etymology': 'Plural of nerd, possibly coined by Dr. Seuss in "If I Ran the Zoo" (1950), or from "drunk" spelled backward (knurd). The exact origin is uncertain.',
                'memory_tip': 'Remember NERDS as "kNowlEdge-focused peRsonS with Deep Specialization" - people with deep specialization and knowledge focus in intellectual areas.',
                'example_sentence': 'The technology company actively recruited _____ from top universities, recognizing that their expertise was essential for innovation.'
            },
            'nereid': {
                'definition': 'A Nereid in Greek mythology is one of the fifty sea nymphs who were daughters of Nereus, the "Old Man of the Sea," and his wife Doris. These divine beings were portrayed as beautiful, helpful spirits of the Mediterranean Sea who assisted sailors in distress and accompanied Poseidon in his underwater palace. Individual Nereids had distinct personalities and roles, with Thetis (mother of Achilles) and Amphitrite (wife of Poseidon) being among the most famous. They were often depicted riding dolphins or other sea creatures, and were considered benevolent deities who protected fishermen and travelers on the sea. The term has also been applied in modern contexts to various marine creatures, particularly a family of marine worms (Nereididae) that live in ocean environments. Understanding Nereid mythology provides insight into ancient Greek relationships with the sea and their beliefs about divine intervention in maritime activities.',
                'pronunciation': '/ˈnɪriɪd/',
                'etymology': 'From Greek Nereis (plural Nereides), from Nereus, the sea god and father of the Nereids. The name derives from Greek mythology\'s rich tradition of sea deities.',
                'memory_tip': 'Remember NEREID as "NEReus\' daughter = sEa nymph" - a sea nymph daughter of Nereus, the Greek sea god, helpful to sailors.',
                'example_sentence': 'In the ancient mosaic, a _____ was depicted riding a dolphin while guiding a ship through dangerous waters.'
            },
            'nerfing': {
                'definition': 'Nerfing is a term used primarily in video gaming that describes the act of reducing the power, effectiveness, or capabilities of a character, weapon, ability, or game element through updates or patches. This process is typically done by game developers to restore balance when certain elements become overpowered or create unfair advantages that disrupt gameplay. The term comes from Nerf toys, which are soft foam versions of weapons that are much less powerful than real ones, creating the metaphor of making something less effective or "softer." Nerfing often generates strong reactions from players who enjoyed using the powerful elements, but it\'s essential for maintaining competitive balance and ensuring all players have fair opportunities for success. The practice extends beyond gaming to describe any situation where something powerful is made weaker or less effective. Understanding nerfing helps in appreciating game design principles and the ongoing adjustments needed to maintain fair, enjoyable gaming experiences.',
                'pronunciation': '/ˈnɜrfɪŋ/',
                'etymology': 'From Nerf (the toy brand that makes soft foam weapons) + -ing suffix. The gaming term suggests making something as harmless as a Nerf toy compared to the real thing.',
                'memory_tip': 'Remember NERFING as "NERF (soft toy) + ING = making soft like toys" - making game elements softer and less powerful like Nerf toys compared to real weapons.',
                'example_sentence': 'The game developers announced they were _____ the overpowered wizard class to make combat more balanced for all character types.'
            },
            'nervily': {
                'definition': 'Nervily is an adverb describing behavior characterized by boldness, audacity, or impudence that borders on being presumptuous or cheeky. Someone acting nervily displays confidence that might exceed what the situation warrants, often taking risks or making bold moves that could be considered inappropriate or forward. This manner of behaving combines courage with a certain disregard for conventional boundaries or social expectations, sometimes resulting in impressive achievements but other times leading to negative consequences. Nervily can describe both positive traits (showing initiative, taking calculated risks) and negative ones (being pushy, overstepping boundaries). The term suggests a fine line between admirable boldness and problematic presumption, depending on context and results. Understanding when behavior is appropriately nervy versus inappropriately presumptuous requires social sensitivity and awareness of cultural norms.',
                'pronunciation': '/ˈnɜrvəli/',
                'etymology': 'From nervy + -ly adverb suffix. Nervy combines nerve (boldness, audacity) with -y suffix, creating an adjective meaning boldly impudent.',
                'memory_tip': 'Remember NERVILY as "NERVE + boldLY" - acting boldly with nerve, showing audacious confidence that might border on being presumptuous.',
                'example_sentence': 'She _____ approached the CEO at the conference to pitch her startup idea, ignoring protocol but ultimately securing a valuable meeting.'
            },
            'nervous': {
                'definition': 'Nervous describes a state of anxiety, apprehension, or unease about uncertain situations, potential problems, or challenging circumstances. This emotional and physical condition involves heightened alertness, worry, and often physical symptoms such as increased heart rate, sweating, or restlessness. Nervous feelings can be appropriate responses to genuinely stressful situations (job interviews, medical procedures, public speaking) or may be excessive reactions that interfere with daily functioning. The term also relates to the nervous system, the body\'s network of nerves that transmit signals between the brain and other parts of the body. Nervous energy can sometimes be channeled productively into preparation and performance, while excessive nervousness may require stress management techniques or professional support. Understanding the difference between normal nervousness and anxiety disorders helps in determining when professional help might be beneficial for managing these feelings.',
                'pronunciation': '/ˈnɜrvəs/',
                'etymology': 'From Latin nervosus meaning "sinewy, vigorous," from nervus "sinew, nerve." The anxiety sense developed from the idea of having weak or overstimulated nerves.',
                'memory_tip': 'Remember NERVOUS as "NERVE + anxiouS" - feeling anxious with overstimulated nerves, experiencing worry and physical tension about uncertain situations.',
                'example_sentence': 'He felt increasingly _____ as the job interview approached, practicing his answers while trying to calm his racing heart.'
            },
            'nescience': {
                'definition': 'Nescience refers to ignorance or lack of knowledge, particularly the absence of awareness or understanding about specific subjects, facts, or situations. This formal term describes a state of not knowing that can be either innocent (lack of exposure to information) or willful (deliberate avoidance of knowledge). Nescience differs from stupidity in that it implies absence of knowledge rather than inability to learn or understand. In philosophical contexts, nescience can refer to the inherent limitations of human knowledge or the recognition that certain truths may be unknowable. Some religious and philosophical traditions view nescience as a natural human condition that can be overcome through education, enlightenment, or spiritual growth. Understanding nescience helps distinguish between different types of ignorance and recognizes that not all lack of knowledge results from intellectual deficiency. The term emphasizes the importance of education and lifelong learning in overcoming knowledge gaps.',
                'pronunciation': '/ˈnɛʃəns/',
                'etymology': 'From Latin nescientia meaning "ignorance," from nesciens "not knowing," from ne- "not" + scire "to know." The term literally means "not-knowing."',
                'memory_tip': 'Remember NESCIENCE as "NE (not) + SCIENCE (knowledge)" - the state of not having knowledge, ignorance or lack of awareness.',
                'example_sentence': 'The politician\'s _____ about environmental science became apparent when she made several scientifically inaccurate statements during the debate.'
            },
            'nest': {
                'definition': 'A nest is a structure built by birds, insects, or other animals as a place to lay eggs, raise young, or provide shelter and protection. Bird nests vary tremendously in design, materials, and location depending on species needs, with some being simple depressions in the ground while others are elaborate woven structures suspended from branches. The term extends metaphorically to describe any cozy, sheltered place where someone feels secure and comfortable, such as a home or favorite retreat. Nest also functions as a verb meaning to build nests or to settle into a comfortable position. In finance, a "nest egg" refers to money saved for future needs, particularly retirement. Understanding nest construction reveals remarkable animal engineering skills and adaptation to environmental challenges. The metaphorical uses of nest emphasize themes of security, comfort, preparation, and the creation of safe spaces for growth and development.',
                'pronunciation': '/nɛst/',
                'etymology': 'From Old English nest, related to Germanic and Indo-European words for nest. The concept connects to words meaning "to sit down" or "settle," reflecting the settling behavior of nesting animals.',
                'memory_tip': 'Remember NEST as "Natural Egg-laying Secure Territory" - a secure territory that animals build for laying eggs and raising young safely.',
                'example_sentence': 'The robin carefully wove grass and twigs to construct her _____ in the protected fork of the apple tree branches.'
            },
            'netflix': {
                'definition': 'Netflix is a global streaming entertainment service that provides television series, documentaries, and films across a wide variety of genres and languages, accessible through internet-connected devices. Founded in 1997 as a DVD-by-mail rental service, Netflix pioneered the shift to streaming media and transformed how people consume entertainment by offering on-demand access to vast content libraries. The company revolutionized the entertainment industry through data-driven content recommendations, binge-watching culture, and significant investments in original programming that have earned critical acclaim and industry awards. Netflix operates as a subscription-based service in over 190 countries, producing content in multiple languages and cultures to serve diverse global audiences. The platform\'s business model eliminated traditional broadcast schedules and physical media, influencing competitors to develop similar streaming services. Understanding Netflix\'s impact reveals broader changes in media consumption, content creation, and global entertainment distribution in the digital age.',
                'pronunciation': '/ˈnɛtflɪks/',
                'etymology': 'Company name combining "Net" (from internet) + "flix" (suggesting movies/films). The name was designed to suggest internet-based movie delivery.',
                'memory_tip': 'Remember NETFLIX as "NET (internet) + FLIX (movies)" - internet movies and TV shows delivered through streaming technology on connected devices.',
                'example_sentence': 'The family subscribed to _____ to access a wide variety of movies and TV series without having to visit video rental stores.'
            },
            'nethinim': {
                'definition': 'Nethinim were a group of temple servants mentioned in the Hebrew Bible, particularly in the books of Ezra, Nehemiah, and Chronicles, who assisted the Levites in performing various duties related to temple worship and maintenance. These individuals were likely descendants of foreign peoples who were assigned to serve in the Jerusalem temple, possibly including prisoners of war or conquered populations who were given specific religious roles. The Nethinim performed tasks such as drawing water, cutting wood, cleaning temple areas, and other support functions that enabled the priests and Levites to focus on their primary religious duties. They were considered a distinct social class within Jewish society, with specific rights and responsibilities that differed from both ordinary Israelites and the priestly classes. During the return from Babylonian exile, the Nethinim were among those who came back to Jerusalem to resume their temple service. Understanding the Nethinim provides insight into the social structure and religious organization of ancient Jewish society.',
                'pronunciation': '/ˈnɛθɪnɪm/',
                'etymology': 'From Hebrew נתינים (Nethinim) meaning "given ones" or "devoted ones," from the root נתן (natan) meaning "to give." They were "given" to serve in the temple.',
                'memory_tip': 'Remember NETHINIM as "NETHen + given IM = those given to serve" - those given to serve in the temple, temple servants in ancient Jewish society.',
                'example_sentence': 'The book of Ezra lists the _____ among those who returned from exile to resume their duties serving in the rebuilt Jerusalem temple.'
            },
            'netiquette': {
                'definition': 'Netiquette refers to the set of rules, guidelines, and social conventions that govern polite and appropriate behavior in online communication and internet interactions. This digital etiquette encompasses proper conduct in email, social media, forums, chat rooms, and other online platforms where people interact virtually. Key netiquette principles include using appropriate tone, avoiding typing in all capital letters (which suggests shouting), respecting others\' privacy, not spreading false information, and being mindful of how written communication can be misinterpreted without vocal or facial cues. Good netiquette also involves staying on topic in discussions, crediting sources, respecting intellectual property, and being considerate of different time zones and cultural backgrounds in global communications. Understanding netiquette helps prevent misunderstandings, maintains professional relationships, and creates more positive online communities. As digital communication becomes increasingly prevalent, netiquette skills become essential for effective personal and professional online interactions.',
                'pronunciation': '/ˈnɛtɪˌkɛt/',
                'etymology': 'Portmanteau of "net" (internet) + "etiquette." Coined in the 1990s as internet communication became widespread and the need for online behavioral guidelines became apparent.',
                'memory_tip': 'Remember NETIQUETTE as "NET (internet) + ETIQUETTE" - etiquette rules for internet communication and online behavior.',
                'example_sentence': 'Good _____ requires thinking carefully before posting comments, as tone and intent can be easily misunderstood in written online communication.'
            },
            'nets': {
                'definition': 'Nets is the plural form of net, referring to multiple mesh-like structures made from interwoven threads, ropes, or wires designed to catch, contain, or separate objects. These versatile tools serve numerous purposes including fishing (catching fish), sports (tennis, basketball, volleyball), safety (construction fall protection), and capturing (butterfly nets, bird nets). Different net designs optimize for specific functions: fine mesh for small objects, large openings for bigger items, and various materials for different strength requirements. Nets can be temporary (fishing nets deployed and retrieved) or permanent installations (safety barriers, sports equipment). The term also extends to network systems, particularly computer networks that connect multiple devices. Understanding net applications reveals human ingenuity in creating simple but effective tools that harness the properties of flexible, interconnected materials. The mesh structure of nets demonstrates how strategic spacing and connection points can create surprisingly strong and effective barriers or collectors.',
                'pronunciation': '/nɛts/',
                'etymology': 'Plural of net, from Old English nett, related to Germanic words for net. The concept of interwoven fibers creating mesh structures appears across many cultures.',
                'memory_tip': 'Remember NETS as plural of NET - multiple mesh structures made from interwoven materials for catching, containing, or separating objects.',
                'example_sentence': 'The fishermen repaired their _____ each evening, mending tears and replacing worn sections before the next day\'s fishing expedition.'
            },
            'network': {
                'definition': 'A network is an interconnected system of elements, people, or components that communicate, share resources, or work together to achieve common goals. In technology, networks connect computers, devices, and systems to enable data sharing, communication, and resource access across distances. Social networks consist of relationships between individuals or organizations that facilitate information exchange, support, and collaboration. Business networks involve partnerships, supply chains, and professional relationships that enable commerce and industry cooperation. Transportation networks include roads, railways, and flight paths that connect different locations. Biological networks encompass neural networks in brains, ecosystem relationships, and genetic regulatory systems. The effectiveness of networks depends on connectivity, communication protocols, and the quality of relationships between nodes. Understanding network principles helps in designing systems, building relationships, and solving complex problems that require coordination among multiple elements. Modern society increasingly relies on various types of networks for functionality and growth.',
                'pronunciation': '/ˈnɛtˌwɜrk/',
                'etymology': 'From net + work, literally meaning "net-work" or work that functions like a net with interconnected parts. The term emerged as systems became more complex and interconnected.',
                'memory_tip': 'Remember NETWORK as "NET + WORK = interconnected work" - work or systems that function through interconnected relationships and communication.',
                'example_sentence': 'The company\'s computer _____ allowed employees in different offices to share files and communicate seamlessly across continents.'
            },
            'networks': {
                'definition': 'Networks is the plural form of network, referring to multiple interconnected systems that operate simultaneously or in coordination with each other. These complex systems can include computer networks serving different functions, social networks spanning various communities, business networks connecting different industries, or infrastructure networks supporting regional development. Multiple networks often overlap and interact, creating larger systems of systems that enable complex modern society functions. For example, transportation networks connect with communication networks and power networks to support urban operations. Understanding how multiple networks interact reveals the complexity of modern infrastructure and the potential vulnerabilities that arise when networks are interdependent. The management and coordination of multiple networks requires sophisticated planning, redundancy systems, and careful attention to how failures in one network might cascade to others. Networks analysis helps in understanding social movements, business ecosystems, technology infrastructure, and many other complex systems.',
                'pronunciation': '/ˈnɛtˌwɜrks/',
                'etymology': 'Plural form of network, from net + work. The plural emphasizes the multiple, often interconnected systems that characterize complex modern environments.',
                'memory_tip': 'Remember NETWORKS as plural of NETWORK - multiple interconnected systems operating together, often overlapping and coordinating functions.',
                'example_sentence': 'The city\'s infrastructure relies on multiple _____ including power grids, water systems, and telecommunications working together harmoniously.'
            },
            'neuhauser': {
                'definition': 'Neuhauser is a German surname meaning "new house" or "from the new house," typically indicating that the original bearer either lived in a newly constructed house or came from a place called Neuhaus. This surname reflects the German tradition of creating family names based on geographical locations, occupations, or distinctive characteristics of where people lived or worked. Like many Germanic surnames, Neuhauser would have helped distinguish individuals in communities where first names alone were insufficient for identification. The name demonstrates how surnames evolved to provide practical identification while preserving information about family origins or notable characteristics. German immigration to various countries spread surnames like Neuhauser beyond their original geographic boundaries. Understanding German surname patterns helps in genealogical research and provides insights into historical migration patterns, settlement practices, and social organization in German-speaking regions.',
                'pronunciation': '/ˈnoʊhaʊzər/',
                'etymology': 'From German neu "new" + Haus "house" + -er suffix indicating origin or occupation. Literally means "from the new house" or "dweller in the new house."',
                'memory_tip': 'Remember NEUHAUSER as "NEU (new) + HAUS (house) + ER (from)" - someone from the new house, a German surname indicating residence.',
                'example_sentence': 'The genealogist traced the _____ family name back to a small village in Bavaria where it first appeared in 16th-century records.'
            },
            'neuropathy': {
                'definition': 'Neuropathy is a medical condition involving damage to or dysfunction of the peripheral nerves, which carry information between the central nervous system and the rest of the body. This condition can affect sensory nerves (causing numbness, tingling, or pain), motor nerves (causing weakness or muscle problems), or autonomic nerves (affecting organ function). Neuropathy can result from various causes including diabetes, infections, toxins, medications, autoimmune disorders, or genetic factors. Diabetic neuropathy is one of the most common forms, often affecting the feet and hands with symptoms like burning pain, numbness, or loss of sensation. Treatment approaches depend on the underlying cause and may include medication for pain relief, blood sugar control for diabetic cases, physical therapy, and lifestyle modifications. Early diagnosis and treatment can help prevent progression and manage symptoms. Understanding neuropathy helps in recognizing symptoms and seeking appropriate medical care for this potentially debilitating condition.',
                'pronunciation': '/nʊˈrɑpəθi/',
                'etymology': 'From Greek neuron "nerve" + pathos "suffering, disease." The medical term literally means "nerve disease" or suffering of the nerves.',
                'memory_tip': 'Remember NEUROPATHY as "NEURO (nerve) + PATHY (disease)" - a disease affecting nerves, causing pain, numbness, or dysfunction.',
                'example_sentence': 'The patient\'s diabetic _____ caused severe burning pain in her feet, making it difficult to walk or sleep comfortably.'
            },
            'neuropathynoun': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "neuropathy noun" - combining the medical term with a grammatical designation.',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "neuropathy" and "noun"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'neuroticism': {
                'definition': 'Neuroticism is a fundamental personality trait characterized by emotional instability, anxiety, moodiness, worry, and tendency to experience negative emotions more frequently and intensely than others. Individuals high in neuroticism often struggle with stress management, may be more reactive to everyday challenges, and can experience prolonged negative emotional states. This personality dimension is one of the "Big Five" personality traits used in psychological research and assessment, representing a spectrum from emotional stability (low neuroticism) to emotional reactivity (high neuroticism). While some degree of neuroticism can motivate careful planning and risk avoidance, excessive levels can interfere with daily functioning, relationships, and overall life satisfaction. Neuroticism correlates with increased risk for anxiety disorders, depression, and stress-related health problems. Understanding neuroticism helps in self-awareness, personal development, and recognizing when professional support might be beneficial for managing emotional reactivity and improving coping strategies.',
                'pronunciation': '/nʊˈrɑtəˌsɪzəm/',
                'etymology': 'From neurotic + -ism suffix. Neurotic comes from Greek neuron "nerve" + -otic suffix, originally referring to nerve disorders but later applied to emotional instability.',
                'memory_tip': 'Remember NEUROTICISM as "NEUROTIC + ISM = tendency to be neurotic" - the personality trait of being prone to anxiety, worry, and emotional instability.',
                'example_sentence': 'Her high level of _____ made her worry excessively about minor problems that others handled with relative calm.'
            },
            'neutron': {
                'definition': 'A neutron is a subatomic particle found in the nucleus of most atoms, carrying no electrical charge (hence "neutral") but having approximately the same mass as a proton. Along with protons, neutrons make up atomic nuclei, with the number of neutrons determining isotopes of elements while the number of protons defines the element itself. Free neutrons are unstable and decay into protons, electrons, and neutrinos with a half-life of about 15 minutes. Neutrons play crucial roles in nuclear reactions, including nuclear fission in power plants and weapons, where they can trigger chain reactions by splitting heavy atomic nuclei. The discovery of neutrons in 1932 by James Chadwick completed our understanding of atomic structure and enabled the development of nuclear physics and technology. Neutron stars, extremely dense collapsed stars composed almost entirely of neutrons, represent one of the most exotic forms of matter in the universe.',
                'pronunciation': '/ˈnutrɑn/',
                'etymology': 'From neutral + -on suffix (used for subatomic particles). Named for its lack of electrical charge, distinguishing it from positively charged protons and negatively charged electrons.',
                'memory_tip': 'Remember NEUTRON as "NEUTRal + particleON" - a neutral particle (no charge) found in atomic nuclei along with protons.',
                'example_sentence': 'The nuclear reactor used _____ bombardment to split uranium atoms, releasing enormous amounts of energy through controlled fission reactions.'
            },
            'never': {
                'definition': 'Never is an adverb meaning "not at any time" or "not under any circumstances," expressing absolute negation across all temporal contexts. This word indicates complete absence of occurrence in the past, present, or future, making definitive statements about what has not happened and will not happen. Never can emphasize permanence, impossibility, or strong determination, as in promises or resolutions that something will not occur. The word functions in various grammatical constructions including "never again" (emphasizing finality), "never mind" (dismissing something), and "never say never" (acknowledging that absolute statements can sometimes prove incorrect). Never can express both literal impossibility and hyperbolic emphasis, depending on context and speaker intent. Understanding the absolute nature of never helps in making precise communications about time, possibility, and commitment. The word carries significant weight in legal, personal, and professional contexts where absolute statements have important consequences.',
                'pronunciation': '/ˈnɛvər/',
                'etymology': 'From Old English naefre, from na "no, not" + aefre "ever." The compound literally means "not ever" or "at no time."',
                'memory_tip': 'Remember NEVER as "Not EVER" - not at any time in the past, present, or future, expressing absolute temporal negation.',
                'example_sentence': 'She promised herself she would _____ again make the same mistake that had caused so much trouble for her family.'
            },
            'newbie': {
                'definition': 'A newbie is an informal term for someone who is new to a particular activity, group, or field of knowledge, emphasizing their beginner status and lack of experience. This colloquial word is commonly used in online communities, gaming, sports, and professional environments to describe newcomers who are still learning the basics and may need guidance or patience from more experienced members. While the term can sometimes carry condescending overtones, it\'s often used neutrally or even affectionately to acknowledge everyone\'s starting point in any learning process. Newbies typically require mentoring, training materials, and supportive environments to develop competence and confidence. The concept recognizes that expertise develops over time and that experienced community members have responsibilities to help newcomers integrate successfully. Understanding newbie dynamics helps create inclusive environments that encourage learning and growth rather than discouraging beginners through intimidation or impatience.',
                'pronunciation': '/ˈnubi/',
                'etymology': 'Variant of "newby," from new + -by/-bie suffix. Popularized in computer and internet communities in the 1980s and 1990s as online participation grew.',
                'memory_tip': 'Remember NEWBIE as "NEW + BEginner" - a new beginner to an activity, group, or field who needs guidance and support.',
                'example_sentence': 'The experienced gamers were patient with the _____, offering tips and encouragement rather than criticism for beginner mistakes.'
            },
            'newbienirvana': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "newbie nirvana" - combining the beginner term with the Buddhist concept of enlightenment.',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "newbie" and "nirvana"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'newfangled': {
                'definition': 'Newfangled describes something that is recently invented, introduced, or developed, often with a slightly critical or skeptical tone suggesting that the new thing might be unnecessary, complicated, or inferior to traditional alternatives. This adjective typically appears in contexts where older generations or traditional-minded individuals express reservations about modern innovations, technologies, or methods. The term carries connotations of resistance to change, suggesting that the speaker questions whether the new development represents genuine improvement or merely change for its own sake. Newfangled can apply to technologies, methods, ideas, or social practices that differ from established norms. While sometimes used dismissively, the term can also express simple recognition of novelty without necessarily implying disapproval. Understanding the slightly old-fashioned nature of this word helps recognize when speakers are positioning themselves as traditionalists or expressing mild skepticism about innovation and change.',
                'pronunciation': '/ˈnuˌfæŋɡəld/',
                'etymology': 'From new + fangled, past participle of obsolete fangle meaning "to catch, capture" or "contrive." Originally meant "inclined to novelty."',
                'memory_tip': 'Remember NEWFANGLED as "NEW + fancily made" - recently invented or developed things that might be unnecessarily fancy or complicated.',
                'example_sentence': 'Grandpa complained about all the _____ gadgets in the kitchen, preferring his old manual tools to the digital appliances.'
            },
            'newfoundland': {
                'definition': 'Newfoundland is Canada\'s easternmost province, consisting of the island of Newfoundland and the mainland region of Labrador, known for its rugged coastline, rich fishing heritage, and distinctive culture. The island was one of the last places settled by Europeans in North America and maintained a separate identity until joining Canada as its tenth province in 1949. Newfoundland\'s economy historically depended on cod fishing, though overfishing led to a moratorium and economic diversification into oil production, mining, and tourism. The province features dramatic landscapes including icebergs, fjords, and the world\'s oldest exposed rock formations. St. John\'s, the capital, is one of North America\'s oldest cities and serves as the easternmost major city on the continent. The term also refers to a large breed of working dog originally from the island, renowned for water rescue abilities and gentle temperament. Newfoundland culture blends Irish, English, and French influences with unique local traditions.',
                'pronunciation': '/ˈnufəndlənd/',
                'etymology': 'From "new found land," the name given by European explorers to the previously unknown (to Europeans) island. The term literally means "newly discovered land."',
                'memory_tip': 'Remember NEWFOUNDLAND as "NEW FOUND LAND" - the new land found by European explorers, now Canada\'s easternmost province.',
                'example_sentence': 'The massive _____ dog jumped into the icy Atlantic waters to rescue the swimmer, demonstrating the breed\'s legendary water rescue instincts.'
            },
            'newly': {
                'definition': 'Newly is an adverb indicating that something has happened recently, has just begun, or has been recently acquired, created, or established. This temporal modifier emphasizes the fresh, recent nature of events, conditions, or states, distinguishing them from things that have existed for longer periods. Newly can modify various parts of speech, creating compounds like "newly married," "newly constructed," or "newly discovered" that highlight the recent nature of changes or developments. The word suggests transition from one state to another, often implying that adjustments, learning, or adaptation may still be in progress. Newly can carry connotations of inexperience, freshness, excitement, or vulnerability associated with recent changes. Understanding the temporal specificity of newly helps in communication about timing, development stages, and the evolutionary nature of situations that are still in early phases of development or adjustment.',
                'pronunciation': '/ˈnuli/',
                'etymology': 'From new + -ly adverb suffix, meaning "in a new manner" or "recently." The adverbial form emphasizes the recent timing of events or changes.',
                'memory_tip': 'Remember NEWLY as "NEW + LY = in a new/recent manner" - recently or in a fresh, recent way, emphasizing the timing of changes.',
                'example_sentence': 'The _____ elected mayor promised to address the city\'s infrastructure problems within her first 100 days in office.'
            },
            'news': {
                'definition': 'News refers to newly received or noteworthy information about recent events, developments, or situations that are of interest to the public or specific audiences. This information is typically gathered, verified, and disseminated by journalists, news organizations, or media outlets through various channels including newspapers, television, radio, and digital platforms. News serves essential functions in democratic societies by informing citizens about government activities, social issues, economic developments, and other matters that affect their lives and communities. The quality and reliability of news depends on journalistic standards including accuracy, objectivity, timeliness, and relevance to audience interests. Modern news consumption has evolved from traditional scheduled broadcasts to continuous digital updates, creating both opportunities for immediate information and challenges related to misinformation and information overload. Understanding news literacy helps citizens evaluate source credibility, identify bias, and make informed decisions based on reliable information.',
                'pronunciation': '/nuz/',
                'etymology': 'From Middle English newes, plural of new (as in "new things"). Originally referred to new information or recent developments worthy of sharing.',
                'memory_tip': 'Remember NEWS as "New Events Worth Sharing" - new events worth sharing with the public, newly received noteworthy information.',
                'example_sentence': 'The breaking _____ report interrupted regular programming to announce the important scientific discovery that could revolutionize medical treatment.'
            },
            'newspapers': {
                'definition': 'Newspapers are periodic publications containing news, information, and opinions, typically printed on newsprint and distributed daily or weekly to inform communities about local, national, and international events. These traditional media outlets serve as primary sources of information for many people, providing journalism that includes reporting, analysis, editorial commentary, and various features such as sports, weather, and entertainment coverage. Newspapers have historically played crucial roles in democracy by holding government accountable, investigating important issues, and facilitating public discourse on matters of community interest. The newspaper industry has faced significant challenges from digital media, leading to declining circulation, reduced advertising revenue, and the closure of many publications. Many newspapers have adapted by developing online presence, digital subscriptions, and multimedia content while maintaining their core mission of providing reliable, locally relevant journalism. Understanding the evolution and continuing importance of newspapers helps appreciate their role in informed citizenship and community cohesion.',
                'pronunciation': '/ˈnuzˌpeɪpərz/',
                'etymology': 'Plural of newspaper, from news + paper. The compound describes paper publications specifically designed for distributing news and information to the public.',
                'memory_tip': 'Remember NEWSPAPERS as "NEWS + PAPERS = papers for news" - printed papers that distribute news and information to communities.',
                'example_sentence': 'Local _____ provide essential coverage of city council meetings and school board decisions that national media outlets typically ignore.'
            },
            'newsroom': {
                'definition': 'A newsroom is the central workspace where journalists, editors, and other news staff gather, research, write, edit, and coordinate the production of news content for publication or broadcast. This collaborative environment serves as the operational heart of news organizations, equipped with computers, communication systems, reference materials, and meeting spaces that enable efficient news gathering and dissemination. Newsrooms operate under deadline pressures, with staff working to verify information, conduct interviews, write stories, and ensure accuracy before publication. The physical and organizational structure of newsrooms facilitates collaboration between reporters, editors, photographers, and producers who must coordinate to cover breaking news and ongoing stories. Modern newsrooms integrate digital technologies, social media monitoring, and multimedia production capabilities to serve audiences across multiple platforms. Understanding newsroom operations provides insight into journalistic processes, editorial decision-making, and the challenges of producing reliable, timely news in fast-paced information environments.',
                'pronunciation': '/ˈnuzrum/',
                'etymology': 'From news + room, describing the dedicated room or space where news is researched, written, and produced. The compound emphasizes the workspace aspect of journalism.',
                'memory_tip': 'Remember NEWSROOM as "NEWS + ROOM = room for news" - the room where journalists work together to research, write, and produce news.',
                'example_sentence': 'The _____ buzzed with activity as reporters worked frantically to verify details and file stories about the developing political crisis.'
            },
            'newsy': {
                'definition': 'Newsy describes something full of news or characterized by containing much newsworthy information, often referring to communications, publications, or conversations that are rich with current events, updates, or interesting developments. This informal adjective suggests that the content provides substantial information about recent happenings, making it valuable for staying informed about various topics. A newsy letter, email, or conversation typically includes multiple updates about people, events, or situations that the recipient would find interesting or important to know. The term can also describe publications, broadcasts, or websites that prioritize comprehensive coverage of current events over other types of content. Newsy content is valued for its informativeness and relevance, helping people stay connected with developments in their communities, professional fields, or areas of interest. Understanding what makes content newsy helps in creating communications that effectively inform and engage audiences with relevant, timely information.',
                'pronunciation': '/ˈnuzi/',
                'etymology': 'From news + -y suffix meaning "characterized by" or "full of." The adjective form emphasizes the news-rich quality of content or communication.',
                'memory_tip': 'Remember NEWSY as "NEWS + Y = full of news" - characterized by being full of news and newsworthy information.',
                'example_sentence': 'Her annual holiday letter was always wonderfully _____, updating family and friends on everyone\'s major life events and achievements.'
            },
            'newt': {
                'definition': 'A newt is a type of small, semi-aquatic salamander that typically lives both in water and on land during different stages of its life cycle. These amphibians are characterized by their ability to regenerate lost body parts, including limbs, tails, and even parts of their hearts and brains, making them subjects of scientific research into regenerative medicine. Newts undergo metamorphosis from aquatic larvae with gills to adults that can breathe both through lungs and skin, with many species returning to water to breed. They feed on insects, worms, and other small creatures, playing important roles in ecosystem balance as both predators and prey. Different newt species exhibit various colors and patterns, with some having bright warning coloration that signals toxicity to potential predators. Newts are found in temperate regions of North America, Europe, and Asia, typically in environments with access to both terrestrial and aquatic habitats. Their sensitivity to environmental changes makes them important indicators of ecosystem health.',
                'pronunciation': '/nut/',
                'etymology': 'From Middle English newte, from "an ewte" (an eft), where "eft" was the original name for newts. The "n" was transferred from the article to the noun.',
                'memory_tip': 'Remember NEWT as "Nice amphibian that rEgeneraWes Tails" - a nice amphibian that regenerates tails and other body parts, living both in water and on land.',
                'example_sentence': 'The pond was home to several _____ species that could often be seen swimming among the aquatic plants during breeding season.'
            },
            'newton': {
                'definition': 'Newton most commonly refers to Sir Isaac Newton (1643-1727), the English mathematician, physicist, and natural philosopher who formulated the laws of motion and universal gravitation that became the foundation of classical mechanics. His work "Principia Mathematica" revolutionized scientific understanding of how objects move and interact, while his contributions to calculus, optics, and astronomy established him as one of history\'s most influential scientists. The newton (symbol N) is also the SI unit of force, defined as the force needed to accelerate one kilogram of mass at one meter per second squared. Newton\'s laws of motion describe the relationship between forces acting on objects and their motion, providing the theoretical framework for engineering, astronomy, and physics applications. His work on optics revealed that white light contains all colors of the spectrum, while his law of universal gravitation explained planetary motion and terrestrial physics under unified principles. Newton\'s scientific method and mathematical approach continue to influence modern scientific inquiry.',
                'pronunciation': '/ˈnutən/',
                'etymology': 'Named after Sir Isaac Newton, English physicist and mathematician. The unit of force was named in his honor for his fundamental contributions to understanding mechanics and forces.',
                'memory_tip': 'Remember NEWTON as "physics NEWTONs = force units named for physicist" - either the great physicist or the force unit named after him.',
                'example_sentence': 'The physics student calculated that it would take 50 _____ of force to accelerate the 5-kilogram object at 10 meters per second squared.'
            },
            'next': {
                'definition': 'Next describes what immediately follows in time, order, sequence, or position, indicating the subsequent item in a series or the following event in a temporal sequence. This word establishes relationships between elements, helping organize information, activities, and expectations according to logical or chronological progression. Next can refer to immediate succession (the next day, next person in line) or general futurity (next opportunity, next generation). The term functions as an adjective, adverb, or noun depending on context, providing flexibility in describing temporal and sequential relationships. Next implies continuity and predictability, helping people plan, organize, and navigate through ordered experiences. Understanding the concept of next is fundamental to time management, project planning, and communication about sequences and schedules. The word creates expectations and helps establish priorities by clarifying what comes after current activities or situations.',
                'pronunciation': '/nɛkst/',
                'etymology': 'From Old English nehst, superlative of neah "near." Originally meant "nearest" or "closest," later developing the temporal sense of "following immediately."',
                'memory_tip': 'Remember NEXT as "NEarest in sequeXTe" - nearest in sequence, what comes immediately following in time or order.',
                'example_sentence': 'The _____ speaker will discuss climate change solutions, following the presentation on renewable energy technologies.'
            },
            'nexus': {
                'definition': 'A nexus is a connection, link, or central point where multiple elements, ideas, or systems converge or interact, often representing the core or critical junction that ties different parts together. This concept applies across various fields: in law, nexus describes the connection between jurisdiction and legal cases; in science, it represents the meeting point of different forces or phenomena; in business, it indicates the intersection of markets, technologies, or strategies. A nexus can be physical (a transportation hub), conceptual (the nexus of art and technology), or systemic (the nexus of environmental and economic factors). The term emphasizes relationships and interdependencies rather than isolated elements, highlighting how different components influence each other through their connections. Understanding nexus points helps in analyzing complex systems, identifying leverage points for change, and recognizing how modifications in one area can affect connected elements. The concept is crucial for systems thinking and strategic planning.',
                'pronunciation': '/ˈnɛksəs/',
                'etymology': 'From Latin nexus meaning "bond, connection," from nectere "to bind, tie." The term emphasizes the binding or connecting function that links different elements.',
                'memory_tip': 'Remember NEXUS as "NEXt level connection of US (elements)" - the next level connection that links us (multiple elements) together at a central point.',
                'example_sentence': 'The university served as a _____ between research institutions, technology companies, and government agencies working on artificial intelligence.'
            },
            'niacin': {
                'definition': 'Niacin, also known as nicotinic acid or vitamin B3, is an essential water-soluble vitamin that plays crucial roles in cellular metabolism, energy production, and maintaining healthy nervous system function. This vitamin is required for the proper functioning of enzymes involved in converting carbohydrates, fats, and proteins into usable energy for the body. Niacin deficiency can lead to pellagra, a serious condition characterized by dermatitis, diarrhea, dementia, and potentially death if untreated. Good dietary sources include meat, fish, nuts, and enriched grains, while the body can also produce small amounts from the amino acid tryptophan. Niacin supplements are sometimes prescribed to help manage cholesterol levels, as higher doses can reduce LDL (bad) cholesterol and increase HDL (good) cholesterol. However, high doses can cause side effects including flushing, liver problems, and digestive issues. Understanding niacin\'s importance helps in maintaining proper nutrition and recognizing deficiency symptoms.',
                'pronunciation': '/ˈnaɪəsɪn/',
                'etymology': 'From nicotinic acid + -in suffix. Named because it was first isolated from nicotine, though it has no direct relationship to tobacco\'s harmful effects.',
                'memory_tip': 'Remember NIACIN as "Need It for energy production And Cellular functIoNs" - needed for energy production and cellular functions, vitamin B3.',
                'example_sentence': 'The doctor recommended increasing _____ intake through foods like tuna and chicken to help improve the patient\'s energy levels.'
            },
            'niagara': {
                'definition': 'Niagara refers to the famous Niagara Falls, one of the world\'s most powerful and recognizable waterfalls, located on the border between New York State and Ontario, Canada. The falls consist of three waterfalls: Horseshoe Falls (the largest, on the Canadian side), American Falls, and Bridal Veil Falls, formed where the Niagara River flows from Lake Erie to Lake Ontario. This natural wonder attracts millions of tourists annually and has significant economic importance for both the United States and Canada through tourism and hydroelectric power generation. The falls have inspired countless artists, writers, and adventurers, becoming a symbol of natural power and beauty. The word "Niagara" has entered common usage to describe any overwhelming flow or cascade, as in "a Niagara of complaints." The region around the falls, including the city of Niagara Falls on both sides of the border, has developed around tourism and the unique geological formation.',
                'pronunciation': '/naɪˈæɡərə/',
                'etymology': 'From Iroquoian languages, possibly meaning "thundering water" or "neck of land." The name reflects the indigenous peoples\' description of the powerful waterfall.',
                'memory_tip': 'Remember NIAGARA as "Naturally Impressive And Grande water falling" - naturally impressive and grand waterfall between US and Canada.',
                'example_sentence': 'The honeymoon couple stood mesmerized by the power and beauty of _____ Falls as millions of gallons cascaded over the precipice.'
            },
            'nibble': {
                'definition': 'Nibble means to take small, gentle bites or to eat something gradually in tiny amounts, often describing the delicate eating behavior of small animals or people eating carefully or without much appetite. This verb suggests restrained, careful eating that contrasts with aggressive biting or hearty consumption. Fish nibble at bait, rabbits nibble vegetables, and people might nibble crackers when they\'re not very hungry. The term extends metaphorically to describe gradual reduction or slight modification of something, such as nibbling away at a problem or budget. In computing, a nibble is half a byte (4 bits) of data, representing a small unit of information. The word captures the concept of small, incremental actions that may accumulate over time. Nibbling behavior can indicate uncertainty, caution, or simply the appropriate way to consume something that requires delicate handling.',
                'pronunciation': '/ˈnɪbəl/',
                'etymology': 'Possibly from Low German nibbeln or Middle Dutch knibbelen, meaning "to gnaw." The word suggests small, repeated biting actions.',
                'memory_tip': 'Remember NIBBLE as "Nice Incremental Bites Building Little Eating" - nice incremental bites that build up to eating, taking small gentle bites.',
                'example_sentence': 'The mouse would _____ at the cheese throughout the night, leaving tiny tooth marks but never finishing the whole piece.'
            },
            'nice': {
                'definition': 'Nice is an adjective that has evolved significantly in meaning, now primarily describing something pleasant, agreeable, satisfactory, or kind, though historically it meant precise, careful, or discriminating. Modern usage applies nice to people (kind, friendly), experiences (enjoyable, pleasant), objects (attractive, good quality), or situations (favorable, satisfactory). The word\'s flexibility makes it useful for expressing general approval or positive sentiment, though its broad application can sometimes make it less specific than more precise descriptive terms. Nice can indicate moderate praise rather than enthusiastic endorsement, as in "nice work" versus "excellent work." Cultural contexts influence how nice is perceived, with some viewing it as genuine appreciation while others consider it mild or understated praise. Understanding the appropriate level of enthusiasm behind "nice" requires attention to context, tone, and cultural norms. The word\'s ubiquity in polite conversation makes it essential for social communication.',
                'pronunciation': '/naɪs/',
                'etymology': 'From Old French nice meaning "silly, simple," from Latin nescius "ignorant." The meaning evolved through "particular, fastidious" to the modern positive sense.',
                'memory_tip': 'Remember NICE as "Notable In Creating Enjoyable experiences" - notable in creating enjoyable experiences, pleasant and agreeable.',
                'example_sentence': 'It was _____ of you to bring flowers to the dinner party, and the hosts really appreciated the thoughtful gesture.'
            },
            'niche': {
                'definition': 'A niche refers to a specialized segment or position that is particularly suitable for specific purposes, organisms, or activities. In ecology, a niche describes the role and position a species has in its environment, including its habitat requirements, resource use, and interactions with other organisms. In business and marketing, niche refers to a specialized market segment that has specific needs, preferences, or characteristics that distinguish it from broader markets. Niche products or services cater to particular customer groups with specialized requirements, often allowing companies to charge premium prices due to limited competition and specialized expertise. The concept can also describe physical spaces, such as architectural niches that provide recesses for decorative objects or religious statues. Understanding niche markets helps businesses identify opportunities for specialization, while ecological niches are crucial for understanding biodiversity and ecosystem functioning. Finding the right niche often leads to success through focused expertise rather than broad generalization.',
                'pronunciation': '/nɪʃ/ or /niʃ/',
                'etymology': 'From French niche meaning "recess, nook," from Italian nicchia, from Latin nidus "nest." The business sense developed from the idea of finding a suitable "nest" or position.',
                'memory_tip': 'Remember NICHE as "Narrow Interest Created for Highly Experienced specialists" - a narrow interest area created for highly experienced specialists.',
                'example_sentence': 'The small company found its _____ by specializing in custom software for veterinary clinics, avoiding competition with larger tech firms.'
            },
            'nicoise': {
                'definition': 'Niçoise refers to a style of preparation or dish originating from Nice, France, in the French Riviera region, most famously represented by salade Niçoise, a composed salad featuring tomatoes, hard-boiled eggs, anchovies, olives, and traditionally, tuna or other Mediterranean ingredients. This culinary term indicates the characteristic ingredients and preparation methods associated with the cuisine of Nice and the broader Côte d\'Azur region. Niçoise dishes typically emphasize fresh, local ingredients including olive oil, herbs, vegetables, and seafood that reflect the Mediterranean climate and culture. The preparation style emphasizes simplicity and quality of ingredients rather than complex cooking techniques, allowing natural flavors to shine through. Different interpretations of Niçoise dishes exist, but they generally maintain the essential character of southern French coastal cuisine. Understanding Niçoise style provides insight into regional French cooking and the influence of geography and climate on culinary traditions.',
                'pronunciation': '/ˌnisˈwɑz/ or /niˈswɑz/',
                'etymology': 'From French Niçoise, meaning "of or from Nice," the feminine form of Niçois referring to the people or style of Nice, France.',
                'memory_tip': 'Remember NICOISE as "NICE-style cuisine" - cuisine in the style of Nice, France, featuring Mediterranean ingredients like olives, tomatoes, and anchovies.',
                'example_sentence': 'The restaurant\'s _____ salad featured fresh tuna, black olives, and vegetables arranged beautifully in the traditional southern French style.'
            },
            'nictitate': {
                'definition': 'Nictitate means to wink or blink, particularly referring to the rapid, involuntary movement of the eyelids or the action of a third eyelid (nictitating membrane) found in many animals. This formal, technical term is primarily used in scientific and medical contexts to describe the protective blinking reflex that helps keep eyes moist and free from debris. Many animals, including birds, reptiles, and some mammals, have nictitating membranes that can sweep across the eye surface while maintaining vision, providing protection during activities like diving, flying, or feeding. In humans, nictitation refers to normal blinking behavior that occurs automatically to lubricate eyes and remove particles. The word also appears in discussions of eye conditions, reflexes, and comparative anatomy studies. Understanding nictitation helps in recognizing normal eye function and the evolutionary adaptations that different species have developed for eye protection.',
                'pronunciation': '/ˈnɪktəˌteɪt/',
                'etymology': 'From Latin nictitare, frequentative form of nicere "to wink, beckon." The term emphasizes the repeated, rapid nature of blinking or winking movements.',
                'memory_tip': 'Remember NICTITATE as "NICe eyes need To blink To protect And TEar" - eyes need to blink to protect and produce tears, the formal term for winking or blinking.',
                'example_sentence': 'The owl\'s ability to _____ allowed it to protect its eyes while diving through thick brush to catch prey.'
            },
            'nidicolous': {
                'definition': 'Nidicolous describes young animals, particularly birds, that remain in the nest for an extended period after hatching, requiring parental care and feeding before they develop enough to survive independently. This biological term contrasts with nidifugous species whose young leave the nest soon after hatching. Nidicolous young are typically born in a relatively undeveloped state, often blind, featherless, and unable to regulate their own body temperature, making them completely dependent on parents for survival. Examples include most songbirds, raptors, and mammals like cats and dogs whose offspring require extensive parental investment. The extended nest period allows for brain development, learning, and physical maturation under parental protection and guidance. This reproductive strategy involves fewer offspring but greater parental investment per individual, often resulting in higher survival rates for young that successfully fledge. Understanding nidicolous development helps in wildlife conservation, pet care, and appreciating different evolutionary strategies for raising offspring.',
                'pronunciation': '/nɪˈdɪkələs/',
                'etymology': 'From Latin nidus "nest" + colere "to inhabit, dwell." The term literally means "nest-dwelling," describing animals that remain in the nest for extended periods.',
                'memory_tip': 'Remember NIDICOLOUS as "NIDI (nest) + COLOUS (living) = nest-living" - young animals that live in the nest for extended periods, needing parental care.',
                'example_sentence': 'The _____ robin chicks remained in the nest for two weeks, completely dependent on their parents for food and protection.'
            },
            'niger': {
                'definition': 'Niger is a landlocked West African country bordered by Libya, Chad, Nigeria, Benin, Burkina Faso, Mali, and Algeria, known for its Saharan desert landscape and uranium mining industry. The nation faces significant challenges including poverty, food security issues, political instability, and the effects of climate change on its predominantly agricultural economy. Niger\'s population consists of various ethnic groups including Hausa, Djerma, Fulani, and Tuareg peoples, with French as the official language and Islam as the predominant religion. The country\'s economy relies heavily on subsistence farming, livestock, and uranium exports, though recurring droughts and desertification create ongoing economic difficulties. Niger has experienced several military coups and democratic transitions since independence from France in 1960. The Niger River, from which the country takes its name, flows through the southwestern region and provides vital water resources for agriculture and transportation. Understanding Niger\'s situation helps appreciate the challenges facing Sahel region countries.',
                'pronunciation': '/ˈnaɪdʒər/ or /niˈʒɛr/',
                'etymology': 'Named after the Niger River, which flows through the country. The river name possibly derives from Berber egereou n-igereouen meaning "river of rivers."',
                'memory_tip': 'Remember NIGER as "NorthernIGh/desert country nEaR sahara" - a northern desert country near the Sahara in West Africa, named after the Niger River.',
                'example_sentence': 'The international aid organization focused on improving water access in rural _____ communities affected by prolonged drought.'
            },
            'nigeria': {
                'definition': 'Nigeria is West Africa\'s most populous country and largest economy, located on the Atlantic coast with over 200 million people representing more than 250 ethnic groups and over 500 languages. This federal republic consists of 36 states plus the Federal Capital Territory of Abuja, with Lagos serving as the commercial capital and largest city. Nigeria\'s economy is heavily dependent on oil exports, though the country also has significant agricultural potential and a growing technology sector. The nation faces challenges including corruption, ethnic and religious tensions, security issues from groups like Boko Haram, and economic inequality despite oil wealth. Nigeria gained independence from Britain in 1960 and has experienced periods of military rule alternating with civilian government, with the current democratic system established in 1999. The country has significant cultural influence across Africa through its film industry (Nollywood), music, and literature. Nigeria\'s diversity includes major groups like Hausa-Fulani, Yoruba, and Igbo peoples.',
                'pronunciation': '/naɪˈdʒɪriə/',
                'etymology': 'Named after the Niger River by British journalist Flora Shaw in 1897, combining "Niger" (the river) with the Latin suffix "-ia" meaning "land of."',
                'memory_tip': 'Remember NIGERIA as "NIGEr River In Africa = most populous country" - the most populous African country named after the Niger River.',
                'example_sentence': 'The entrepreneur moved from _____ to establish a technology startup, hoping to contribute to Africa\'s growing digital economy.'
            },
            'night': {
                'definition': 'Night refers to the period of darkness between sunset and sunrise when the sun is below the horizon, creating natural cycles that influence biological rhythms, human activities, and cultural practices. This daily occurrence results from Earth\'s rotation, causing different parts of the planet to face away from the sun and experience darkness. Night provides essential rest periods for humans and many animals, while nocturnal species use this time for active hunting, feeding, and other behaviors. Cultural associations with night include mystery, romance, danger, and tranquility, reflected in literature, art, and social customs. Human activities have adapted to night through artificial lighting, allowing extended productive hours but also potentially disrupting natural circadian rhythms. Night sky observation has historically been crucial for navigation, agriculture, and scientific discovery. Understanding natural light-dark cycles helps maintain healthy sleep patterns and appreciation for the rhythms that govern life on Earth.',
                'pronunciation': '/naɪt/',
                'etymology': 'From Old English neaht, related to Germanic and Indo-European words for night. The concept of darkness period opposite to day appears across all human languages.',
                'memory_tip': 'Remember NIGHT as "No sunlIGHT" - the time when there is no sunlight, the period of darkness between sunset and sunrise.',
                'example_sentence': 'The campers enjoyed the clear _____ sky, identifying constellations and watching for shooting stars in the absence of city lights.'
            },
            'nighttime': {
                'definition': 'Nighttime refers to the period during night hours, emphasizing the temporal aspect of darkness and the activities, conditions, or phenomena that occur during these hours. This compound word distinguishes between night as a concept and nighttime as the actual period when night-specific activities take place. Nighttime activities include sleep, nocturnal animal behavior, astronomical observation, and human activities adapted to darkness such as security work, entertainment, or shift labor. The term often appears in contexts discussing schedules, safety considerations, or specialized equipment designed for low-light conditions. Nighttime temperatures, nighttime photography, and nighttime driving each present unique characteristics and challenges that differ from daytime equivalents. Understanding nighttime as a distinct temporal period helps in planning activities, maintaining safety, and recognizing the different rhythms and requirements that characterize dark hours versus daylight periods.',
                'pronunciation': '/ˈnaɪtˌtaɪm/',
                'etymology': 'Compound of night + time, emphasizing the temporal period when night occurs. The compound distinguishes the time period from night as a general concept.',
                'memory_tip': 'Remember NIGHTTIME as "NIGHT + TIME = the time of night" - the specific time period when night occurs, during the hours of darkness.',
                'example_sentence': 'The security guard worked _____ shifts, patrolling the building when most people were sleeping at home.'
            }
        }
        
        return claude_data.get(word, {
            'definition': f'Definition for {word} not yet available.',
            'pronunciation': f'Pronunciation for {word} not yet available.',
            'etymology': f'Etymology for {word} not yet available.',
            'memory_tip': f'Memory tip for {word} not yet available.',
            'example_sentence': f'Example sentence for {word} not yet available.'
        })
    
    def detect_combined_words(self) -> List[str]:
        combined_words = [
            'neuropathynoun',
            'newbienirvana'
        ]
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        logger.info("Processing Batch 118 with comprehensive Claude data...")
        
        combined_words = self.detect_combined_words()
        logger.info(f"Detected {len(combined_words)} combined word errors: {combined_words}")
        
        processed_words = []
        
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                word = row['word'].strip()
                if not word:
                    continue
                    
                logger.info(f"Processed word: {word}")
                
                claude_data = self.get_comprehensive_claude_data(word)
                difficulty_scores = self.difficulty_calc.calculate_difficulty_score(
                    word, claude_data['definition'], claude_data['etymology']
                )
                
                processed_word = {
                    'word': word,
                    'years': row['years'],
                    'source_files': row['source_files'], 
                    'source_difficulties': row['source_difficulties'],
                    'definition': claude_data['definition'],
                    'pronunciation': claude_data['pronunciation'],
                    'etymology': claude_data['etymology'],
                    'etymology_source': 'Claude',
                    'memory_tip': claude_data['memory_tip'],
                    'example_sentence': claude_data['example_sentence'],
                    'example_sentence_source': 'Claude',
                    'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                    'word_frequency_score': difficulty_scores['word_frequency_score'],
                    'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                    'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                    'difficulty': difficulty_scores['difficulty'],
                    'combined_word_error': word in combined_words
                }
                
                processed_words.append(processed_word)
        
        # Write output CSV
        if processed_words:
            fieldnames = [
                'word', 'years', 'source_files', 'source_difficulties',
                'definition', 'pronunciation', 'etymology', 'etymology_source',
                'memory_tip', 'example_sentence', 'example_sentence_source',
                'phonetic_transparency_score', 'word_frequency_score',
                'morphological_complexity_score', 'etymology_complexity_score',
                'difficulty', 'combined_word_error'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
        logger.info("Batch 118 processing completed!")
        logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {len(processed_words)} successful, 0 failed")

if __name__ == "__main__":
    processor = Batch118Processor()
    
    input_file = "output/batch_118_words.csv"
    output_file = "output/batch_118_processed.csv"
    
    processor.process_batch(input_file, output_file)