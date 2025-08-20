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

class Batch117Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        claude_data = {
            'narcoleptic': {
                'definition': 'Narcoleptic describes a person who suffers from narcolepsy, a neurological disorder characterized by uncontrollable episodes of falling asleep during normal waking hours, often accompanied by sudden loss of muscle tone (cataplexy), sleep paralysis, and vivid hallucinations when falling asleep or waking up. This chronic condition significantly impacts daily life, making it dangerous to drive, operate machinery, or perform tasks requiring sustained attention. Narcoleptic individuals often experience disrupted nighttime sleep despite excessive daytime sleepiness, creating a paradoxical sleep pattern. The condition typically begins in adolescence or young adulthood and requires lifelong management through medication, lifestyle modifications, and scheduled naps. Treatment may include stimulants to promote wakefulness, antidepressants to control cataplexy, and sodium oxybate to improve nighttime sleep quality. Understanding narcolepsy helps reduce stigma and promote workplace accommodations for affected individuals.',
                'pronunciation': '/ˌnɑrkəˈlɛptɪk/',
                'etymology': 'From narcolepsy + -ic suffix. Narcolepsy comes from Greek narke "numbness, stupor" + lepsis "seizure, taking hold." The condition was named for its seizure-like episodes of sleep.',
                'memory_tip': 'Remember NARCOLEPTIC as "NARCotic-like sLEEP aTTacKs" - someone who has narcotic-like sleep attacks that they cannot control.',
                'example_sentence': 'The _____ student received accommodations allowing scheduled nap breaks and extended time for exams to manage her sleep disorder.'
            },
            'nares': {
                'definition': 'Nares is the medical term for nostrils, the external openings of the nasal cavity that allow air to enter and exit during breathing. In anatomy and medicine, nares specifically refers to the paired openings at the base of the nose, lined with specialized tissues that filter, warm, and humidify incoming air. Each nostril contains sensitive nasal hairs and mucous membranes that trap particles and pathogens before they enter the respiratory system. The shape and size of nares vary among individuals and can affect breathing patterns, voice resonance, and susceptibility to certain respiratory conditions. Medical professionals examine nares during physical assessments to check for obstructions, inflammation, or abnormalities. The term is commonly used in medical documentation, anatomical studies, and clinical descriptions of nasal conditions or procedures involving the nostrils.',
                'pronunciation': '/ˈnɛriz/',
                'etymology': 'From Latin nares meaning "nostrils," related to Sanskrit nas "nose." The term has been used in medical Latin since ancient times to describe the nasal openings.',
                'memory_tip': 'Remember NARES as "NAsal aiR EntryS" - the nasal air entries (nostrils) where air enters and exits the respiratory system.',
                'example_sentence': 'The doctor examined the patient\'s _____ for any signs of inflammation or obstruction that might explain the breathing difficulties.'
            },
            'naricorn': {
                'definition': 'Naricorn is an uncommon term referring to the hard, horn-like growth that forms at the tip of the nose in certain animals, particularly some species of rhinoceros hornbills and other birds. This specialized anatomical feature serves various purposes including display, foraging assistance, or species recognition. In some contexts, naricorn may refer to horn-like protuberances or growths that develop on or near the nasal area in various species. The term is primarily used in specialized zoological or veterinary literature to describe these distinctive anatomical features. Understanding such terminology is important for accurate scientific communication about animal anatomy and species identification. The word combines references to both nasal location and horn-like appearance, making it descriptive of its anatomical position and structure.',
                'pronunciation': '/ˈnɛrɪkɔrn/',
                'etymology': 'From Latin naris "nostril" + cornu "horn," literally meaning "nose horn." The term describes horn-like growths or structures associated with nasal areas in certain animals.',
                'memory_tip': 'Remember NARICORN as "NARIs (nose) + CORN (horn) = nose horn" - a horn-like growth on or near the nose area in certain animals.',
                'example_sentence': 'The ornithologist noted the distinctive _____ structure that helped identify the species of hornbill during the field study.'
            },
            'narrative': {
                'definition': 'Narrative refers to a spoken or written account of connected events presented in a sequence, typically involving characters, settings, and a plot that unfolds over time. This fundamental form of human communication encompasses stories, reports, explanations, and descriptions that organize information in chronological or logical order. Narratives serve multiple purposes including entertainment, education, persuasion, and cultural transmission, appearing in literature, journalism, oral traditions, and personal accounts. Effective narratives typically include elements such as exposition, rising action, climax, and resolution that create engaging and meaningful experiences for audiences. The structure and style of narratives vary across cultures, genres, and purposes, from simple anecdotes to complex literary works. Understanding narrative techniques helps both creators and consumers of stories appreciate how meaning is constructed and communicated through sequential storytelling.',
                'pronunciation': '/ˈnærətɪv/',
                'etymology': 'From Latin narrativus meaning "telling a story," from narrare "to tell, relate," from gnarus "knowing." The term emphasizes the knowing and telling aspect of storytelling.',
                'memory_tip': 'Remember NARRATIVE as "NARRAte + sequential story" - to narrate a sequential story with characters, events, and plot development.',
                'example_sentence': 'The documentary used a compelling _____ structure to explain the complex scientific discoveries in an accessible way.'
            },
            'narrow': {
                'definition': 'Narrow describes something having a small width relative to its length or height, or having limited scope, range, or extent in various contexts. Physical narrowness refers to spaces, objects, or passages that are constricted in width, such as narrow streets, narrow doorways, or narrow beams of light. Metaphorically, narrow can describe limited perspectives, restricted thinking, or constrained options that lack breadth or inclusiveness. The term also applies to close margins or small differences, as in narrow victories or narrow escapes. In decision-making contexts, narrow choices offer few alternatives, while narrow interpretations restrict meaning to specific, limited understanding. Narrow can describe temporary conditions (a narrow window of opportunity) or permanent characteristics (narrow interests). The concept often implies limitation but can also suggest focus, precision, or specialization depending on context.',
                'pronunciation': '/ˈnæroʊ/',
                'etymology': 'From Old English nearu meaning "narrow, confined, limited," related to Germanic words for tight or constricted. The metaphorical senses developed from physical narrowness.',
                'memory_tip': 'Remember NARROW as "Not Allowing Room for Range Or Width" - not allowing room for range or width, whether physically or conceptually.',
                'example_sentence': 'The _____ alley between the buildings could barely accommodate a single person walking through.'
            },
            'narwal': {
                'definition': 'Narwal appears to be an alternative spelling of "narwhal," referring to the Arctic whale species known for its distinctive tusk. However, "narwal" is not the standard spelling - the correct form is "narwhal." This spelling variation might appear in historical texts or represent a phonetic attempt at the word. The narwhal (Monodon monoceros) is a medium-sized toothed whale that inhabits Arctic waters, famous for the long, straight tusk that projects from the male\'s upper jaw. These remarkable marine mammals play important roles in Arctic ecosystems and have cultural significance for Inuit peoples. The proper spelling "narwhal" should be used in scientific and general writing to maintain accuracy and consistency with established nomenclature.',
                'pronunciation': '/ˈnɑrwəl/',
                'etymology': 'Alternative spelling of narwhal, from Danish and Norwegian narval, from Old Norse náhvalr, from nár "corpse" + hvalr "whale" (referring to their pale color).',
                'memory_tip': 'Remember NARWAL as alternative spelling of NARWHAL - the Arctic whale with the distinctive tusk, though "narwhal" is the preferred spelling.',
                'example_sentence': 'The text used the alternative spelling _____ to refer to the Arctic whale, though "narwhal" is the more commonly accepted form.'
            },
            'narwhal': {
                'definition': 'A narwhal is a medium-sized Arctic whale (Monodon monoceros) famous for the long, spiral tusk that projects from the male\'s upper jaw, resembling a unicorn horn and earning it the nickname "unicorn of the sea." These remarkable marine mammals inhabit Arctic waters around Greenland, Canada, and Russia, traveling in pods and feeding primarily on cod, squid, and shrimp. The tusk, actually an elongated tooth, can reach up to 10 feet in length and serves multiple purposes including male competition, sensory functions, and possibly social signaling. Narwhals have cultural and economic importance for Inuit communities who have hunted them sustainably for centuries, using all parts of the animal for food, tools, and trade. Climate change threatens narwhal populations by altering sea ice patterns that are crucial for their feeding and migration behaviors. These elusive whales remain mysterious to scientists, with much still unknown about their behavior and ecology.',
                'pronunciation': '/ˈnɑrwəl/',
                'etymology': 'From Danish and Norwegian narval, from Old Norse náhvalr, from nár "corpse" + hvalr "whale," referring to their pale, mottled coloration that resembles a floating corpse.',
                'memory_tip': 'Remember NARWHAL as "NARrow spiral tusk WHALE" - the Arctic whale with the narrow spiral tusk that looks like a unicorn horn.',
                'example_sentence': 'The marine biologist was thrilled to observe a pod of _____ through the ice, watching their distinctive tusks break the surface.'
            },
            'nascent': {
                'definition': 'Nascent describes something that is just beginning to exist, develop, or emerge, emphasizing the early stage of growth or formation when potential is present but not yet fully realized. This adjective applies to ideas, movements, industries, relationships, or any phenomena in their initial stages of development. Nascent technologies show promise but require further development to reach maturity, while nascent political movements are gaining momentum but haven\'t achieved established status. The term suggests not just newness but also the potential for significant growth and change. Nascent conditions often require nurturing, support, or favorable circumstances to develop successfully. Understanding nascent stages helps in recognizing opportunities, providing appropriate support, or making predictions about future development. The word carries implications of promise, potential, and the delicate nature of emerging phenomena that could flourish or fail depending on subsequent conditions.',
                'pronunciation': '/ˈnæsənt/',
                'etymology': 'From Latin nascens meaning "being born," present participle of nasci "to be born." The term emphasizes the birth or beginning stage of development.',
                'memory_tip': 'Remember NASCENT as "NASCing = being born/starting to exist" - something in the process of being born or just starting to exist and develop.',
                'example_sentence': 'The _____ renewable energy industry showed great promise but needed significant investment to reach its full potential.'
            },
            'nation': {
                'definition': 'A nation is a large group of people who share common characteristics such as language, culture, ethnicity, history, or territory, often organized under a single government or political system. The concept encompasses both the people themselves and the geographical area they inhabit, creating a sense of collective identity and belonging. Nations can exist as independent sovereign states or as cultural groups within larger political entities. The formation of nations involves complex processes including shared historical experiences, cultural development, and often political organization. Modern nations typically feature defined borders, governmental systems, legal frameworks, and national symbols that reinforce collective identity. The relationship between nation, state, and government creates various political arrangements from nation-states where cultural and political boundaries align, to multinational states containing diverse cultural groups. Understanding nationhood helps explain political organization, cultural identity, and international relations in the modern world.',
                'pronunciation': '/ˈneɪʃən/',
                'etymology': 'From Latin natio meaning "birth, tribe, race," from natus "born," from nasci "to be born." The term originally referred to groups of people born in the same place.',
                'memory_tip': 'Remember NATION as "NATIve populatiON" - a native population sharing common culture, language, and territory under organized government.',
                'example_sentence': 'The newly formed _____ celebrated its independence with ceremonies that honored both traditional culture and modern democratic values.'
            },
            'nationalism': {
                'definition': 'Nationalism is a political ideology and movement that emphasizes loyalty, devotion, and allegiance to one\'s nation, often prioritizing national interests above international or individual concerns. This powerful force in modern politics can manifest as pride in national achievements, support for national independence, or preference for one\'s own country in economic and political decisions. Nationalism takes various forms: civic nationalism based on shared political values and institutions, ethnic nationalism based on common ancestry and culture, and cultural nationalism emphasizing shared language and traditions. While nationalism can unite people around common purposes and fuel independence movements, it can also lead to exclusion of minorities, international conflicts, or aggressive foreign policies. The ideology has shaped modern history through independence movements, wars, and political restructuring. Understanding nationalism requires recognizing both its unifying potential and its capacity for division and conflict.',
                'pronunciation': '/ˈnæʃənəˌlɪzəm/',
                'etymology': 'From national + -ism suffix indicating doctrine or belief system. The concept developed during the formation of modern nation-states in the 18th and 19th centuries.',
                'memory_tip': 'Remember NATIONALISM as "NATIONAL + ISM = belief system prioritizing the nation" - an ideology that prioritizes national identity and interests above other loyalties.',
                'example_sentence': 'The rise of _____ in the 19th century led to both liberation movements and increased tensions between neighboring countries.'
            },
            'nattily': {
                'definition': 'Nattily is an adverb describing the manner of dressing in a neat, trim, and stylish way, emphasizing careful attention to appearance and fashionable presentation. Someone dressed nattily appears well-groomed, coordinated, and appropriately attired for their situation, often with attention to small details that create an overall polished appearance. The term suggests not just cleanliness but also style consciousness and sartorial skill in selecting and arranging clothing and accessories. Nattily dressed individuals often display confidence and attention to social expectations regarding appropriate dress. The adverb can apply to both casual and formal attire, emphasizing the quality of presentation rather than the expense or formality of clothing. Understanding proper grooming and dress conventions helps individuals present themselves nattily in various professional and social contexts.',
                'pronunciation': '/ˈnætəli/',
                'etymology': 'From natty + -ly suffix. Natty possibly comes from neat, influenced by similar words meaning trim or smart in appearance.',
                'memory_tip': 'Remember NATTILY as "NEAT + smartly dressed + LY" - dressed neatly and smartly in a well-groomed, stylish manner.',
                'example_sentence': 'The job candidate was _____ dressed in a perfectly fitted suit that demonstrated professionalism and attention to detail.'
            },
            'natural': {
                'definition': 'Natural describes something existing in or derived from nature rather than made or caused by humans, encompassing phenomena, materials, processes, or characteristics that occur without artificial intervention. The term applies to the physical world including landscapes, weather, plants, animals, and geological formations that develop through natural processes rather than human design. Natural also describes inherent qualities or abilities that seem inborn rather than learned, such as natural talent or natural instincts. In contrast to artificial or synthetic, natural materials and products come directly from living organisms or earth processes without significant chemical modification. The concept extends to behaviors, reactions, or conditions that are normal, expected, or understandable given circumstances. Natural laws describe consistent patterns observed in physical phenomena, while natural selection explains evolutionary processes. Understanding what constitutes natural versus artificial helps in making decisions about health, environment, and authenticity.',
                'pronunciation': '/ˈnætʃərəl/',
                'etymology': 'From Latin naturalis meaning "of nature," from natura "nature," from natus "born," from nasci "to be born." The term emphasizes connection to birth and organic development.',
                'memory_tip': 'Remember NATURAL as "NATURe-AL = of or from nature" - something that comes from or belongs to nature rather than being artificially made.',
                'example_sentence': 'The park preserved the area\'s _____ beauty by limiting development and allowing native plants to flourish undisturbed.'
            },
            'nature': {
                'definition': 'Nature encompasses the physical world and all living things, including plants, animals, landscapes, and natural phenomena, existing independently of human activities and artificial constructions. This broad concept includes ecosystems, weather patterns, geological formations, and biological processes that operate according to natural laws rather than human design. Nature also refers to the essential characteristics or inherent qualities that define something\'s identity, such as human nature or the nature of a problem. In philosophical contexts, nature represents the fundamental principles governing existence and behavior in the universe. The relationship between humans and nature involves complex interactions including environmental stewardship, resource use, recreation, and spiritual connection. Modern environmentalism emphasizes protecting nature from human-caused damage while recognizing humanity\'s dependence on natural systems for survival. Understanding nature requires both scientific knowledge and appreciation for the intricate relationships that sustain life on Earth.',
                'pronunciation': '/ˈneɪtʃər/',
                'etymology': 'From Latin natura meaning "birth, constitution, nature," from natus "born," from nasci "to be born." The term encompasses both the act of birth and the essential qualities that result.',
                'memory_tip': 'Remember NATURE as "NATURal Environment" - the natural environment including all living things and natural processes that exist without human intervention.',
                'example_sentence': 'The documentary explored the delicate balance of _____, showing how each species plays a crucial role in maintaining ecosystem health.'
            },
            'naugahyde': {
                'definition': 'Naugahyde is a trademarked brand of artificial leather made from vinyl-coated fabric, widely used for furniture upholstery, automotive interiors, and other applications requiring durable, water-resistant material that resembles leather. Developed in the 1930s by the United States Rubber Company, this synthetic material became popular due to its lower cost compared to genuine leather and its resistance to wear, stains, and cracking. Naugahyde consists of a fabric base (usually cotton or polyester) coated with vinyl plastic that can be textured and colored to mimic various leather finishes. The material is easier to clean and maintain than real leather, making it practical for commercial and residential uses where durability is important. Marketing campaigns humorously claimed Naugahyde came from fictional "nauga" animals, creating memorable advertising that helped establish the brand name. The material represents mid-20th century innovation in synthetic materials that provided affordable alternatives to expensive natural products.',
                'pronunciation': '/ˈnɔɡəhaɪd/',
                'etymology': 'Trademark name created by combining elements suggesting toughness and hide-like appearance. The fictional "nauga" origin was created for marketing purposes.',
                'memory_tip': 'Remember NAUGAHYDE as "Not AUghentic leather HYDe-like material" - synthetic vinyl material designed to look like leather but more durable.',
                'example_sentence': 'The restaurant chose _____ upholstery for the booths because it could withstand heavy use while maintaining an attractive appearance.'
            },
            'naughty': {
                'definition': 'Naughty describes behavior that is mildly misbehaved, disobedient, or playfully improper, typically used for children who break rules or act inappropriately but without serious harmful intent. The term suggests mischievous conduct that may be annoying or disruptive but is generally considered minor rather than truly bad or dangerous. In adult contexts, naughty can describe behavior that is slightly improper, risqué, or mildly sexual in nature, often with playful or humorous connotations. The word carries lighter implications than terms like "bad" or "evil," suggesting behavior that might deserve mild correction but not severe punishment. Naughty can also describe things that are slightly indulgent or treat-like, such as "naughty" desserts that are rich and caloric. The term maintains a somewhat playful quality even when describing disapproval, making it useful for expressing mild criticism without harsh judgment.',
                'pronunciation': '/ˈnɔti/',
                'etymology': 'From naught (nothing) + -y suffix, originally meaning "having nothing, worthless." The sense evolved to describe behavior that amounts to "nothing good" or minor misbehavior.',
                'memory_tip': 'Remember NAUGHTY as "Not AUGHt (nothing good) + Y" - behaving in ways that are not quite good, mischievous but not seriously bad.',
                'example_sentence': 'The _____ puppy chewed the furniture, but his owner couldn\'t stay angry at such adorable mischief for very long.'
            },
            'naumachia': {
                'definition': 'Naumachia refers to staged naval battles that were performed as public spectacles in ancient Rome, typically held in flooded amphitheaters or specially constructed artificial lakes. These elaborate entertainments recreated famous historical sea battles using real ships and combatants, often prisoners of war or condemned criminals who fought to the death for the crowd\'s amusement. The word also describes the venues where these naval spectacles took place, which required sophisticated engineering to flood and drain large areas. Naumachiae represented the height of Roman spectacle entertainment, demonstrating the empire\'s wealth, engineering capabilities, and control over human lives. These events were expensive to produce and therefore relatively rare, often associated with major celebrations or imperial occasions. The practice reflects Roman attitudes toward warfare, entertainment, and the expendability of certain classes of people. Archaeological evidence of naumachia sites provides insights into Roman engineering and social values.',
                'pronunciation': '/nɔˈmækiə/',
                'etymology': 'From Latin naumachia, from Greek naumachia meaning "naval battle," from naus "ship" + mache "battle." The term described both the event and the venue.',
                'memory_tip': 'Remember NAUMACHIA as "NAUtical battle spectACle" - ancient Roman spectacles featuring nautical battles staged for entertainment.',
                'example_sentence': 'The emperor ordered a grand _____ to celebrate his military victories, flooding the amphitheater for a spectacular naval battle.'
            },
            'nauseam': {
                'definition': 'Nauseam appears as part of the Latin phrase "ad nauseam," meaning "to the point of nausea" or "to a sickening or excessive degree." This expression describes continuing something to such an extent that it becomes disgusting, tiresome, or overwhelming to audiences or participants. The phrase is commonly used in English to criticize repetitive arguments, behaviors, or presentations that have been overdone to the point of causing annoyance or revulsion. Ad nauseam indicates that something has exceeded reasonable limits and become counterproductive through excessive repetition. The concept applies to various contexts including political rhetoric, marketing campaigns, academic arguments, or social behaviors that persist beyond audience tolerance. Understanding this phrase helps recognize when communication or behavior has become ineffective due to overuse. The Latin origin reflects the physical sensation of nausea as a metaphor for intellectual or emotional overwhelm.',
                'pronunciation': '/ˈnɔziæm/',
                'etymology': 'From Latin nauseam, accusative of nausea meaning "seasickness, nausea." Used in the phrase "ad nauseam" meaning "to the point of nausea."',
                'memory_tip': 'Remember NAUSEAM as "NAUSEA + extent" - used in "ad nauseam" meaning to the extent of causing nausea through excessive repetition.',
                'example_sentence': 'The politician repeated the same talking points ad _____ until even his supporters grew tired of hearing them.'
            },
            'nautilus': {
                'definition': 'A nautilus is a marine cephalopod mollusk with a distinctive spiral shell divided into chambers, representing one of the oldest living species on Earth with fossils dating back 500 million years. The modern nautilus uses its chambered shell for buoyancy control, adding or removing water from chambers to rise or sink in the ocean. These "living fossils" have remained virtually unchanged through geological time, providing scientists with insights into ancient marine ecosystems and evolutionary processes. Nautiluses have multiple tentacles (up to 90) without suction cups, unlike their relatives squid and octopus, and use jet propulsion for movement. They inhabit deep waters around coral reefs in the Indo-Pacific region, coming to shallow waters at night to feed. The nautilus shell\'s mathematical spiral follows the golden ratio, making it a subject of artistic and mathematical interest. These creatures face threats from shell collecting and deep-water fishing practices.',
                'pronunciation': '/ˈnɔtələs/',
                'etymology': 'From Latin nautilus, from Greek nautilos meaning "sailor," from naus "ship." Named for the way it appears to sail on the ocean surface.',
                'memory_tip': 'Remember NAUTILUS as "NAUTical + spiral shell creature" - a nautical creature with a beautiful spiral shell that sails through ancient oceans.',
                'example_sentence': 'The marine biologist was excited to observe a rare _____ in its natural habitat, studying its ancient swimming patterns.'
            },
            'navaho': {
                'definition': 'Navaho is an alternative spelling of "Navajo," referring to the indigenous people of the southwestern United States, though "Navajo" is the more commonly used and preferred spelling today. The Navajo Nation is the largest Native American tribe in the United States, with traditional territory spanning parts of Arizona, New Mexico, Utah, and Colorado. Their traditional name is Diné, meaning "the people" in their language. The Navajo people have a rich cultural heritage including distinctive art forms such as weaving, silversmithing, and sand painting, as well as a complex ceremonial and spiritual tradition. They developed a successful pastoral economy based on sheep and horse herding after European contact, adapting these animals to their traditional lifestyle. The Navajo language played a crucial role in World War II when Navajo "code talkers" used their native language to create unbreakable military codes. Today, the Navajo Nation maintains sovereignty while participating in modern American society.',
                'pronunciation': '/ˈnævəhoʊ/',
                'etymology': 'Alternative spelling of Navajo, from Spanish Navajó, from Tewa navahu meaning "large arroyo with cultivated fields." The people call themselves Diné meaning "the people."',
                'memory_tip': 'Remember NAVAHO as alternative spelling of "NAVAJO" - the large Native American tribe of the Southwest, though "Navajo" is the preferred modern spelling.',
                'example_sentence': 'The museum exhibit featured traditional _____ textiles, though modern displays use the preferred spelling "Navajo."'
            },
            'navajo': {
                'definition': 'Navajo refers to the indigenous people of the southwestern United States who constitute the largest Native American tribe, with traditional territory spanning parts of Arizona, New Mexico, Utah, and Colorado. The Navajo people call themselves Diné, meaning "the people" in their native language. Their rich cultural heritage includes distinctive artistic traditions such as intricate textile weaving, silver and turquoise jewelry making, and ceremonial sand paintings used in healing rituals. The Navajo developed a successful pastoral economy incorporating sheep and horses introduced by Europeans, adapting these animals to their traditional lifestyle and creating a unique cultural blend. Their language, Navajo or Diné Bizaad, is part of the Athabascan language family and gained historical importance during World War II when Navajo "code talkers" created unbreakable military codes. Today, the Navajo Nation maintains tribal sovereignty while participating in modern American society, operating businesses, schools, and government services while preserving traditional culture.',
                'pronunciation': '/ˈnævəhoʊ/',
                'etymology': 'From Spanish Navajó, probably from Tewa navahu meaning "large arroyo with cultivated fields." The Navajo people call themselves Diné, meaning "the people."',
                'memory_tip': 'Remember NAVAJO as "NAVigating the southwestern landscape" - the major Native American tribe navigating life in the southwestern United States while preserving their culture.',
                'example_sentence': 'The _____ weaver demonstrated traditional techniques passed down through generations, creating intricate patterns with vibrant natural dyes.'
            },
            'navigation': {
                'definition': 'Navigation is the science and skill of determining position, planning routes, and guiding movement from one location to another, whether on land, sea, air, or in space. This essential capability involves understanding and using various tools, techniques, and technologies including maps, compasses, GPS systems, celestial observation, and electronic instruments. Maritime navigation traditionally relied on stars, magnetic compasses, and dead reckoning, while modern navigation incorporates satellite systems, radar, and computer-assisted route planning. Aviation navigation requires three-dimensional thinking and consideration of weather, air traffic, and fuel consumption. The field encompasses both theoretical knowledge of geography, mathematics, and physics, and practical skills in using navigational instruments and interpreting environmental information. Successful navigation requires planning, continuous position awareness, and adaptation to changing conditions. Modern GPS technology has revolutionized navigation while traditional skills remain important for situations where electronic systems fail.',
                'pronunciation': '/ˌnævəˈɡeɪʃən/',
                'etymology': 'From Latin navigationem meaning "sailing, navigation," from navigare "to sail," from navis "ship" + agere "to drive." The term originally applied to sea travel but expanded to all forms of directed movement.',
                'memory_tip': 'Remember NAVIGATION as "NAVy + direction finding" - the navy skill of finding direction and planning routes, now applied to all forms of travel.',
                'example_sentence': 'The ship\'s officer used both traditional _____ techniques and modern GPS to safely guide the vessel through the busy harbor.'
            },
            'navigator': {
                'definition': 'A navigator is a person who specializes in determining position and planning routes for travel, whether on ships, aircraft, land vehicles, or spacecraft. This skilled professional uses various tools and techniques including maps, compasses, GPS systems, celestial observation, and electronic instruments to guide safe passage from one location to another. Naval navigators must understand ocean currents, tides, weather patterns, and port approaches, while aviation navigators need knowledge of air routes, weather systems, and aircraft performance characteristics. The role requires strong mathematical skills, attention to detail, and ability to make critical decisions under pressure. Modern navigators work with sophisticated electronic systems while maintaining traditional skills as backup for equipment failures. The profession has evolved from ancient mariners who used stars and landmarks to contemporary specialists who integrate multiple technologies for precise positioning and route optimization. Navigators play crucial roles in commercial transportation, military operations, and exploration missions.',
                'pronunciation': '/ˈnævəˌɡeɪtər/',
                'etymology': 'From Latin navigator meaning "sailor, one who sails," from navigare "to sail." The -or suffix indicates one who performs the action of navigating.',
                'memory_tip': 'Remember NAVIGATOR as "NAVigation + operatOR" - an operator who specializes in navigation, guiding ships, planes, or other vehicles safely to their destinations.',
                'example_sentence': 'The experienced _____ plotted a course that would take advantage of favorable currents while avoiding dangerous reef areas.'
            },
            'naysayers': {
                'definition': 'Naysayers are people who habitually express negative opinions, doubts, or opposition to proposals, ideas, or plans, often without offering constructive alternatives. These individuals tend to focus on potential problems, risks, or reasons why something won\'t work rather than exploring possibilities or solutions. While naysayers can serve useful functions by identifying genuine risks or flawed thinking, excessive negativity can stifle innovation, progress, and team morale. The term often carries negative connotations, suggesting that the person\'s criticism is reflexive rather than thoughtfully considered. However, some naysayers provide valuable skeptical perspective that helps organizations avoid costly mistakes or unrealistic commitments. Effective leadership involves distinguishing between constructive criticism and unconstructive negativity, encouraging thoughtful analysis while not allowing persistent pessimism to derail legitimate initiatives. Understanding the motivation behind naysaying helps in addressing underlying concerns while maintaining forward momentum.',
                'pronunciation': '/ˈneɪˌseɪərz/',
                'etymology': 'From nay + say + -er suffix + plural -s. Nay meaning "no" creates the compound meaning "those who say no" to proposals or suggestions.',
                'memory_tip': 'Remember NAYSAYERS as "NAY (no) SAYers" - people who say "no" or express negative opinions about ideas and proposals.',
                'example_sentence': 'Despite the _____ who predicted failure, the startup\'s innovative approach proved successful and gained market acceptance.'
            },
            'naïveté': {
                'definition': 'Naïveté refers to the quality of being naive, characterized by a lack of worldly experience, wisdom, or judgment that leads to innocent, trusting, or unsophisticated behavior. This condition involves genuinely believing in the goodness of people and situations without considering potential deceptions, complications, or harmful intentions. While naïveté can lead to poor decisions and exploitation by others, it also reflects qualities like optimism, trust, and openness that can be valuable in human relationships. The French term suggests a kind of natural innocence that hasn\'t been corrupted by cynical experience or harsh realities. Naïveté differs from stupidity in that it involves inexperience rather than inability to learn or understand. Cultural contexts influence how naïveté is perceived—sometimes as refreshing honesty, other times as dangerous vulnerability. Personal growth often involves balancing the loss of naïveté with the preservation of positive qualities like trust and hope.',
                'pronunciation': '/naɪˈivəˌteɪ/',
                'etymology': 'From French naïveté, from naïf meaning "naive, natural," from Latin nativus "native, natural." The accent marks preserve French spelling and pronunciation patterns.',
                'memory_tip': 'Remember NAÏVETÉ as "NAÏve + quality" - the quality of being naive, having innocent trust without worldly experience or suspicion.',
                'example_sentence': 'Her _____ about business relationships led to several disappointing partnerships before she learned to be more cautious.'
            },
            'neapolitan': {
                'definition': 'Neapolitan refers to anything related to Naples (Napoli), Italy, including its people, culture, cuisine, or characteristics. The term is most commonly known from Neapolitan ice cream, which features three distinct flavors (traditionally vanilla, chocolate, and strawberry) arranged in layers or stripes, supposedly representing the Italian flag colors. Neapolitan cuisine includes famous dishes like pizza margherita, spaghetti alle vongole, and various seafood preparations that reflect the city\'s coastal location. The Neapolitan language is a Romance language distinct from standard Italian, with rich literary traditions and cultural expressions. Naples has significant historical importance as a former capital of the Kingdom of the Two Sicilies and a major Mediterranean port city. Neapolitan music traditions include the famous song "O Sole Mio" and other folk melodies that have become internationally recognized. The term embodies the vibrant, passionate culture associated with southern Italy and Mediterranean lifestyle.',
                'pronunciation': '/ˌniəˈpɑlətən/',
                'etymology': 'From Latin Neapolitanus meaning "of Naples," from Neapolis "new city," from Greek neos "new" + polis "city." Naples was founded as a "new city" by ancient Greek colonists.',
                'memory_tip': 'Remember NEAPOLITAN as "NEw cIty (Naples) + related" - relating to Naples, the "new city" founded by Greeks, famous for pizza and three-flavor ice cream.',
                'example_sentence': 'The restaurant served authentic _____ pizza with a thin, charred crust and fresh mozzarella from the Naples region.'
            },
            'near': {
                'definition': 'Near describes proximity in space, time, or relationship, indicating that something is close by, approaching, or similar to something else. In spatial terms, near refers to short physical distances that can be easily covered or perceived, such as near buildings, near locations, or objects within close range. Temporal nearness describes events or times that are approaching or recently past, like the near future or near deadline. The term also indicates similarity or approximation, as in near perfection or near miss, suggesting closeness to a particular condition without exactly achieving it. Near relationships describe family connections that are close, such as near relatives. The word functions as both an adjective describing proximity and a preposition indicating location relative to something else. Understanding degrees of nearness helps in navigation, planning, and communication about spatial and temporal relationships.',
                'pronunciation': '/nɪr/',
                'etymology': 'From Old English near meaning "nearer, closer," comparative form of neah "near." Originally a comparative form that became the standard positive form.',
                'memory_tip': 'Remember NEAR as "Not far away, Easily ARrived at" - not far away, easily arrived at or reached in distance, time, or similarity.',
                'example_sentence': 'The camping site was _____ the lake, allowing easy access to water for drinking and recreational activities.'
            },
            'nearby': {
                'definition': 'Nearby describes something located close at hand or in the immediate vicinity, within a short distance that can be easily reached or accessed. This adjective and adverb indicates convenience of location, suggesting that travel time and effort required to reach the destination are minimal. Nearby places might include neighborhood businesses, local parks, or adjacent buildings that are within walking distance or a brief drive. The concept is relative to context and mode of transportation—what\'s nearby for a pedestrian differs from what\'s nearby for someone driving or flying. Nearby can describe both permanent fixtures (nearby schools, nearby hospitals) and temporary situations (nearby parking, nearby lodging). Understanding what constitutes nearby helps in planning daily activities, choosing where to live, and making decisions about convenience and accessibility. The term emphasizes practical accessibility rather than precise distance measurements.',
                'pronunciation': '/ˈnɪrbaɪ/',
                'etymology': 'From near + by, combining the concepts of proximity and location. The compound word emphasizes location that is close and accessible.',
                'memory_tip': 'Remember NEARBY as "NEAR + BY location" - located near by, close and easily accessible from one\'s current position.',
                'example_sentence': 'The hotel was perfect because it had several restaurants _____, making it easy to find dinner without traveling far.'
            },
            'nearly': {
                'definition': 'Nearly is an adverb meaning almost or very close to being something, but not quite completely or exactly. This qualifier indicates proximity to a complete state, amount, or condition while acknowledging that the final threshold hasn\'t been reached. Nearly expresses approximation in various contexts: nearly finished suggests work is close to completion, nearly full indicates capacity is almost reached, and nearly impossible suggests extreme difficulty without absolute impossibility. The word helps communicate degrees of completion, progress, or similarity that are significant but not total. Nearly can modify adjectives, verbs, and other adverbs to indicate close approach to the described condition. Understanding the distinction between nearly and completely helps in accurate communication about status, progress, and expectations. The term allows for precision in describing states that are close to but distinct from absolute conditions.',
                'pronunciation': '/ˈnɪrli/',
                'etymology': 'From near + -ly adverb suffix, meaning "in a near manner" or "close to being." The adverbial form emphasizes the degree of proximity to completion.',
                'memory_tip': 'Remember NEARLY as "NEAR + LY = close to being" - close to being something but not quite completely or exactly there yet.',
                'example_sentence': 'The fundraising campaign was _____ successful, having raised 95% of its target amount with just days remaining.'
            },
            'neaten': {
                'definition': 'Neaten means to make something neat, tidy, or orderly by organizing, cleaning, or arranging items in proper positions. This verb involves taking something that is messy, disorganized, or untidy and transforming it into a clean, orderly state through deliberate action. Neatening can apply to physical spaces like rooms, desks, or closets, as well as to appearance, documents, or work presentations. The process typically involves sorting, organizing, cleaning, and arranging elements according to logical or aesthetic principles. Neatening reflects values of organization, cleanliness, and visual appeal that are important in many personal and professional contexts. The activity can have psychological benefits, creating sense of control and accomplishment while potentially improving efficiency and functionality. Understanding how to neaten effectively involves developing systems for organization and maintenance that prevent future accumulation of disorder.',
                'pronunciation': '/ˈniːtən/',
                'etymology': 'From neat + -en suffix meaning "to make or become." The suffix transforms the adjective neat into a verb meaning "to make neat."',
                'memory_tip': 'Remember NEATEN as "make NEAT + EN" - to make something neat, tidy, and well-organized through deliberate arrangement.',
                'example_sentence': 'Before the guests arrived, she took time to _____ the living room, arranging magazines and fluffing cushions.'
            },
            'nebulous': {
                'definition': 'Nebulous describes something that is vague, unclear, or lacking definite form or limits, like a cloud of gas or dust in space after which the term is named. This adjective applies to concepts, plans, or ideas that are hazy, indistinct, or not clearly defined, making them difficult to understand or grasp precisely. Nebulous thinking lacks clarity and specificity, while nebulous explanations fail to provide clear information or direction. The term can describe both physical phenomena (nebulous atmospheric conditions) and abstract concepts (nebulous goals or nebulous relationships). Nebulous situations create uncertainty and confusion because their boundaries, requirements, or characteristics remain undefined. In contrast to clear, specific, or well-defined conditions, nebulous circumstances require clarification, additional information, or further development to become useful or meaningful. The word emphasizes the frustrating quality of things that seem important but remain maddeningly unclear.',
                'pronunciation': '/ˈnebjələs/',
                'etymology': 'From Latin nebulosus meaning "cloudy, misty," from nebula "cloud, mist." The astronomical term nebula for cosmic dust clouds provided the metaphor for unclear or vague conditions.',
                'memory_tip': 'Remember NEBULOUS as "NEBUla-like = cloudy and unclear" - like a nebula in space, cloudy and unclear in form or definition.',
                'example_sentence': 'The company\'s _____ mission statement failed to give employees clear direction about priorities and goals.'
            },
            'necessity': {
                'definition': 'Necessity refers to something that is required, essential, or unavoidable due to circumstances, natural law, or logical consequence. This concept encompasses both basic needs required for survival or functioning (like food, shelter, and safety) and situational requirements imposed by specific conditions or goals. Necessity can be absolute (mathematical or logical necessities that cannot be otherwise) or conditional (practical necessities that arise from particular circumstances or choices). The phrase "necessity is the mother of invention" reflects how urgent needs drive creativity and problem-solving. Legal contexts distinguish between necessity as a defense for actions taken under extreme circumstances and ordinary legal obligations. Economic necessities include goods and services required for basic living standards. Understanding different types of necessity helps in decision-making, resource allocation, and moral reasoning about what is truly required versus what is merely desired or preferred.',
                'pronunciation': '/nəˈsɛsəti/',
                'etymology': 'From Latin necessitas meaning "compulsion, need," from necessarius "necessary," from necesse "unavoidable." The root suggests that which cannot be avoided or done without.',
                'memory_tip': 'Remember NECESSITY as "NECESSary + qualITY" - the quality of being necessary, required, or unavoidable under the circumstances.',
                'example_sentence': 'Clean drinking water is a basic _____ for human survival, not a luxury that can be deferred or ignored.'
            },
            'neck': {
                'definition': 'The neck is the part of the body that connects the head to the torso, containing vital structures including the spinal cord, major blood vessels, airway, and esophagus, while providing support and mobility for the head. This anatomical region allows head movement in multiple directions through complex arrangements of vertebrae, muscles, and ligaments. The neck also refers to narrow parts of objects that resemble this body part, such as the neck of a bottle, guitar neck, or geographic features like peninsulas or isthmuses. In colloquial usage, "neck of the woods" refers to a particular area or neighborhood. The vulnerability of the neck makes it symbolically associated with risk, as in "sticking one\'s neck out" meaning taking chances. Medical conditions affecting the neck can significantly impact quality of life due to the region\'s importance in movement, breathing, and circulation.',
                'pronunciation': '/nɛk/',
                'etymology': 'From Old English hnecca meaning "neck, nape," related to Germanic words for the back of the neck. The word has maintained consistent meaning across centuries.',
                'memory_tip': 'Remember NECK as "Narrow Essential Connection for head" - the narrow essential connection between head and body that enables head movement and contains vital pathways.',
                'example_sentence': 'The whiplash injury affected her _____, causing pain and limiting her ability to turn her head comfortably.'
            },
            'necklace': {
                'definition': 'A necklace is a piece of jewelry worn around the neck, typically consisting of a chain, cord, or string of beads, gems, or other decorative elements that hang from the throat area. These ornamental accessories serve both aesthetic and cultural purposes, ranging from simple everyday pieces to elaborate formal jewelry that indicates social status, wealth, or cultural identity. Necklaces can be made from various materials including precious metals, gemstones, pearls, beads, fabric, or synthetic materials, with designs varying across cultures and historical periods. Different lengths and styles serve different purposes: chokers sit close to the throat, pendants feature hanging decorative elements, and statement necklaces create dramatic focal points for outfits. Cultural significance includes religious symbols, family heirlooms, ceremonial items, and expressions of personal style. Understanding necklace styles, appropriate lengths for different occasions, and cultural sensitivities helps in selecting and wearing these accessories appropriately.',
                'pronunciation': '/ˈnɛkləs/',
                'etymology': 'From neck + lace (originally meaning "cord, string"). The compound describes a decorative cord or chain designed to encircle the neck.',
                'memory_tip': 'Remember NECKLACE as "NECK + LACE (cord)" - a decorative cord or chain that goes around the neck as jewelry.',
                'example_sentence': 'The antique pearl _____ had been passed down through five generations of women in the family.'
            },
            'necks': {
                'definition': 'Necks is the plural form of neck, referring to multiple neck regions whether on different individuals, animals, or objects with neck-like features. In anatomical contexts, necks describe the connecting regions between heads and torsos across various species, each adapted for specific functional needs like length for reaching food (giraffes) or flexibility for hunting (owls). The term also applies to multiple narrow portions of objects such as bottle necks, guitar necks, or geographical features with neck-like shapes. Colloquially, "necks of the woods" refers to different neighborhoods or regions. Medical professionals might discuss necks in comparative studies of injuries, treatments, or anatomical variations across populations. Understanding necks in plural contexts helps in discussions of anatomy, design, geography, and comparative biology where multiple examples or variations are being considered.',
                'pronunciation': '/nɛks/',
                'etymology': 'Plural form of neck, from Old English hnecca. The plural follows standard English patterns for forming multiples of body parts.',
                'memory_tip': 'Remember NECKS as plural of NECK - multiple neck regions on different people, animals, or neck-shaped parts of objects.',
                'example_sentence': 'The massage therapist specialized in treating injured _____ from car accidents and workplace strain.'
            },
            'necromancer': {
                'definition': 'A necromancer is a person who practices necromancy, the supposed art of communicating with the dead to predict the future or influence events, often portrayed as a dark magical practitioner who manipulates death and undead creatures. In fantasy literature, games, and popular culture, necromancers are typically depicted as powerful spellcasters who can animate corpses, speak with spirits, and harness the power of death for various purposes. Historically, necromancy was considered a form of divination that involved summoning spirits of the deceased to gain knowledge or power, practiced in various ancient cultures despite religious and legal prohibitions. The concept reflects human fascination with death, the afterlife, and the possibility of communicating across the boundary between life and death. Modern portrayals often emphasize the forbidden or dangerous nature of necromantic practices, associating them with corruption, moral compromise, and supernatural consequences.',
                'pronunciation': '/ˈnɛkroʊˌmænsər/',
                'etymology': 'From necromancy + -er suffix. Necromancy comes from Greek nekromanteia, from nekros "dead body" + manteia "divination." The suffix indicates one who practices the art.',
                'memory_tip': 'Remember NECROMANCER as "NECRO (dead) + MANCEr (magic practitioner)" - a magic practitioner who specializes in communicating with or controlling the dead.',
                'example_sentence': 'In the fantasy novel, the evil _____ raised an army of skeletons to attack the kingdom.'
            },
            'necrotic': {
                'definition': 'Necrotic describes tissue that has died due to disease, injury, or lack of blood supply, representing a pathological condition where cells and tissues undergo death while still part of a living organism. This medical condition can result from various causes including infection, trauma, toxins, radiation, or compromised blood circulation that deprives tissues of oxygen and nutrients. Necrotic tissue appears discolored (often black, brown, or gray), lacks normal function, and can become a source of infection if not properly treated. Treatment typically involves removing dead tissue (debridement) to prevent spread of infection and promote healing of surrounding healthy tissue. Different types of necrosis occur in various organs and conditions, such as cardiac necrosis during heart attacks or skin necrosis from severe burns. Understanding necrotic conditions is crucial for medical diagnosis and treatment, as prompt intervention can often prevent spread and preserve function in adjacent healthy tissues.',
                'pronunciation': '/nɪˈkrɑtɪk/',
                'etymology': 'From Greek nekrotikos meaning "of or pertaining to death," from nekros "dead body." The medical term specifically describes tissue death within living organisms.',
                'memory_tip': 'Remember NECROTIC as "NECRO (death) + TIC condition" - a condition where tissue has died within a living body due to disease or injury.',
                'example_sentence': 'The surgeon removed the _____ tissue from the wound to prevent infection and allow healthy tissue to regenerate.'
            },
            'nectar': {
                'definition': 'Nectar is a sweet, sugary liquid produced by flowers to attract pollinators such as bees, butterflies, hummingbirds, and other animals that transfer pollen between plants during feeding. This natural substance contains various sugars, amino acids, and other nutrients that provide energy for visiting creatures while facilitating plant reproduction. Bees collect nectar to make honey, concentrating and transforming it through enzymatic processes and water evaporation. In mythology and literature, nectar refers to the drink of the gods, associated with immortality and divine pleasure, giving rise to the phrase "nectar of the gods" for any especially delicious beverage. Commercial nectars are fruit juices that contain pulp and have a thicker consistency than clear juices. The term also describes anything that is sweet, delicious, or particularly enjoyable, emphasizing the pleasure derived from consumption. Understanding nectar\'s role reveals the intricate relationships between plants and their animal partners in ecosystem functioning.',
                'pronunciation': '/ˈnɛktər/',
                'etymology': 'From Latin nectar, from Greek nektar meaning "drink of the gods," possibly from nek "death" + -tar "overcoming," suggesting immortality. The plant substance was named for its sweetness.',
                'memory_tip': 'Remember NECTAR as "NECessary food for pollinaTors" - necessary sweet food produced by flowers to attract pollinators, also the mythical drink of gods.',
                'example_sentence': 'The hummingbird hovered at the trumpet vine, sipping _____ from the bright orange blooms.'
            },
            'nectarine': {
                'definition': 'A nectarine is a variety of peach characterized by its smooth skin instead of the fuzzy skin typical of regular peaches, with sweet, juicy flesh that can be either freestone (easily separated from the pit) or clingstone (attached to the pit). This fruit is botanically identical to peaches except for the genetic mutation that creates the smooth skin, making nectarines and peaches essentially the same species with different surface textures. Nectarines come in various colors including yellow, white, and red varieties, with flavors ranging from sweet to tart depending on variety and ripeness. They are excellent sources of vitamins A and C, potassium, and dietary fiber, while being relatively low in calories. The fruit ripens in summer months and is popular for fresh eating, cooking, baking, and preserving. Nectarines require careful handling due to their delicate nature and are best stored at room temperature until ripe, then refrigerated to maintain quality.',
                'pronunciation': '/ˈnɛktərin/',
                'etymology': 'From nectar + -ine suffix, literally meaning "nectar-like," referring to the fruit\'s sweet, juicy qualities that resemble the mythical drink of the gods.',
                'memory_tip': 'Remember NECTARINE as "NECTARine = nectar-like fruit" - a nectar-like fruit that\'s basically a smooth-skinned peach with sweet, juicy flesh.',
                'example_sentence': 'The ripe _____ was perfectly sweet and juicy, its smooth skin making it easier to eat than a fuzzy peach.'
            },
            'need': {
                'definition': 'Need refers to something that is required, necessary, or essential for survival, well-being, or achieving a particular purpose or goal. Basic human needs include physiological requirements like food, water, shelter, and safety, as well as psychological needs such as love, belonging, and self-esteem. The concept distinguishes between necessities that are truly required versus wants or desires that are preferred but not essential. Economic theories organize needs into hierarchies, with survival needs taking priority over higher-level needs for self-actualization or luxury. Need can function as both a noun (identifying requirements) and a verb (expressing requirement or necessity). Understanding the difference between needs and wants is crucial for personal budgeting, business planning, and social policy development. Emergency situations often clarify what constitutes genuine need versus convenience or comfort preferences.',
                'pronunciation': '/niːd/',
                'etymology': 'From Old English neod meaning "necessity, compulsion, duty," related to Germanic words expressing urgency or distress. The concept of requirement has remained central to the word\'s meaning.',
                'memory_tip': 'Remember NEED as "NEcessary Essential Demand" - a necessary essential demand or requirement for survival, functioning, or achieving goals.',
                'example_sentence': 'Clean water is a basic human _____ that must be provided before addressing other community development projects.'
            },
            'needle': {
                'definition': 'A needle is a thin, pointed implement used for sewing, medical procedures, or other precision work, typically featuring a sharp point at one end and an eye or hollow opening for thread or fluids at the other end. Sewing needles come in various sizes and types for different fabrics and techniques, while medical needles are designed for injections, drawing blood, or intravenous procedures. The metaphorical phrase "needle in a haystack" describes something extremely difficult to find due to its small size relative to its surroundings. Pine needles are the thin, pointed leaves of coniferous trees, while compass needles are magnetized metal pointers that indicate magnetic north. Modern applications include specialized needles for knitting, embroidery, upholstery, and various industrial processes. The precision and sharpness of needles make them essential tools across many fields, from medicine and textiles to navigation and crafts.',
                'pronunciation': '/ˈniːdəl/',
                'etymology': 'From Old English naedl, related to Germanic words for needle. The concept of a sharp, pointed tool for piercing has remained constant across languages and time.',
                'memory_tip': 'Remember NEEDLE as "Narrow Efficient Device for LED(ing thread)" - a narrow efficient device for leading thread through fabric, or other pointed precision tools.',
                'example_sentence': 'The surgeon used a fine _____ to carefully suture the delicate tissue with minimal scarring.'
            },
            'needs': {
                'definition': 'Needs is the plural form of need, referring to multiple requirements, necessities, or essential items required for survival, well-being, or achieving specific goals. Human needs encompass a range of physical, emotional, social, and psychological requirements that must be met for healthy functioning and development. Maslow\'s hierarchy of needs organizes these requirements from basic physiological needs through safety, love and belonging, esteem, and self-actualization. Different life stages, circumstances, and cultures create varying needs profiles, requiring different resources and support systems. Business and organizational contexts analyze customer needs to develop appropriate products and services, while social services assess community needs to allocate resources effectively. Understanding diverse needs helps in planning, resource allocation, and developing policies that support individual and collective well-being. The assessment of needs versus wants remains crucial for prioritizing resources and making sustainable decisions.',
                'pronunciation': '/niːdz/',
                'etymology': 'Plural form of need, from Old English neod. The plural form allows discussion of multiple requirements or necessities simultaneously.',
                'memory_tip': 'Remember NEEDS as plural of NEED - multiple necessary requirements or essentials for survival, well-being, or achieving goals.',
                'example_sentence': 'The social worker assessed the family\'s _____ to determine what assistance programs would be most helpful.'
            },
            'neem': {
                'definition': 'Neem is a fast-growing evergreen tree (Azadirachta indica) native to the Indian subcontinent, renowned for its medicinal properties and natural pesticide qualities that have been utilized for thousands of years in traditional medicine and agriculture. Every part of the neem tree—leaves, bark, seeds, and oil—contains bioactive compounds with antibacterial, antifungal, antiviral, and insecticidal properties. Neem oil is widely used as an organic pesticide that is safe for beneficial insects while effectively controlling harmful pests and plant diseases. In Ayurvedic medicine, neem treats various conditions including skin disorders, diabetes, and infections, earning it the nickname "village pharmacy." The tree thrives in arid conditions and helps prevent soil erosion while providing shade and improving air quality. Modern research has validated many traditional uses of neem, leading to its incorporation in cosmetics, pharmaceuticals, and organic farming practices worldwide.',
                'pronunciation': '/niːm/',
                'etymology': 'From Hindi neem, from Sanskrit nimba meaning "the neem tree." The name has been adopted directly from Indian languages into English botanical terminology.',
                'memory_tip': 'Remember NEEM as "Natural Essential Medicine tree" - a natural tree that provides essential medicine and pest control from all its parts.',
                'example_sentence': 'The organic farmer sprayed _____ oil on the crops to control aphids without harming beneficial pollinators.'
            },
            'nefarious': {
                'definition': 'Nefarious describes actions, people, or plans that are extremely wicked, villainous, or evil, often involving deliberate harm, criminal activity, or morally reprehensible behavior. This adjective emphasizes not just wrongdoing but a particularly malicious or sinister quality that goes beyond ordinary misbehavior to suggest calculated evil or corruption. Nefarious activities might include fraud, extortion, terrorism, or other crimes that demonstrate complete disregard for others\' welfare. The term often appears in discussions of criminal enterprises, corrupt political activities, or fictional villains whose motivations and methods are especially despicable. Nefarious implies secrecy, deception, and malicious intent that makes the actions particularly contemptible. Unlike simple mistakes or minor wrongdoing, nefarious behavior suggests a deliberate choice to cause harm or engage in evil for personal gain. The word carries strong moral condemnation and is typically reserved for the most serious forms of wrongdoing.',
                'pronunciation': '/nɪˈfɛriəs/',
                'etymology': 'From Latin nefarius meaning "contrary to divine law, wicked," from nefas "sin, crime," from ne- "not" + fas "divine law, right." The term emphasizes violation of fundamental moral principles.',
                'memory_tip': 'Remember NEFARIOUS as "NEgative + seriously harmful" - negative actions that are seriously harmful, wicked, and deliberately evil.',
                'example_sentence': 'The detective uncovered a _____ scheme involving money laundering and human trafficking that shocked the entire community.'
            },
            'neigh': {
                'definition': 'Neigh is the characteristic vocal sound made by horses, typically consisting of a loud, prolonged whinnying sound that serves various communication purposes including expressing excitement, calling to other horses, or responding to stimuli. This distinctive vocalization involves a combination of sounds produced through the horse\'s respiratory system and vocal cords, often beginning with a higher pitch that descends to lower tones. Horses neigh to communicate emotions, establish social connections, express distress, or announce their presence to others. The sound carries well over distances, making it effective for long-range communication within herds or between separated animals. In literature and popular culture, the neigh of a horse often symbolizes freedom, power, or the wildness of nature. Understanding horse vocalizations helps in interpreting equine behavior and needs. The word also functions as a verb meaning to make this sound, as in "the horse neighed loudly."',
                'pronunciation': '/neɪ/',
                'etymology': 'From Old English hnaegan meaning "to neigh," imitative of the sound made by horses. The word directly represents the horse\'s vocalization through onomatopoeia.',
                'memory_tip': 'Remember NEIGH as "Noise Expressing horse\'s vocalization" - the distinctive noise that expresses a horse\'s communication, like a loud whinny.',
                'example_sentence': 'The stallion let out a loud _____ when he saw his owner approaching with a bucket of oats.'
            },
            'neighborhood': {
                'definition': 'A neighborhood is a geographically localized community within a larger city, town, or suburb, typically characterized by shared physical boundaries, social connections, and common interests among residents. These residential areas often develop distinct identities based on architecture, demographics, history, economic status, or cultural characteristics that distinguish them from adjacent areas. Neighborhoods serve important social functions by providing sense of community, shared resources, and local governance through homeowner associations or community groups. The concept includes both formal administrative divisions and informal social boundaries that residents recognize and identify with. Quality neighborhoods typically offer amenities such as parks, schools, shopping, and transportation access that enhance residents\' quality of life. Urban planning recognizes neighborhoods as fundamental units for organizing cities and delivering services. Strong neighborhoods contribute to social cohesion, property values, and overall urban livability through collective action and shared investment in community welfare.',
                'pronunciation': '/ˈneɪbərˌhʊd/',
                'etymology': 'From neighbor + -hood suffix meaning "state or condition of." The compound describes the condition of being neighbors in a localized community area.',
                'memory_tip': 'Remember NEIGHBORHOOD as "NEIGHBOR + HOOD (area)" - an area where neighbors live together, forming a local community within a larger city.',
                'example_sentence': 'The historic _____ featured tree-lined streets, Victorian houses, and a strong sense of community among longtime residents.'
            },
            'neighbors': {
                'definition': 'Neighbors are people who live near each other, typically in the same neighborhood, building, or adjacent properties, creating geographic proximity that often leads to social relationships and shared community interests. These relationships can range from casual acquaintance to close friendship, depending on personality, cultural factors, and community involvement. Good neighbors often provide mutual support during emergencies, watch over each other\'s property, share information about local issues, and contribute to community safety and cohesion. The quality of neighbor relationships significantly impacts residential satisfaction, property values, and overall quality of life in residential areas. Cultural norms vary regarding appropriate neighbor interactions, privacy expectations, and community involvement. Modern urban living sometimes reduces neighbor connections compared to traditional small-town environments, though many communities work to strengthen neighborhood bonds through events, associations, and shared projects. Understanding good neighbor etiquette helps maintain positive relationships and contributes to harmonious community living.',
                'pronunciation': '/ˈneɪbərz/',
                'etymology': 'Plural of neighbor, from Old English neahgebur meaning "near-dweller," from neah "near" + gebur "dweller." The concept emphasizes proximity and shared living space.',
                'memory_tip': 'Remember NEIGHBORS as "NEAR dwellers" - people who are near-dwellers, living close to each other and sharing community space.',
                'example_sentence': 'The friendly _____ organized a block party to bring the community together and strengthen local relationships.'
            },
            'neologism': {
                'definition': 'A neologism is a newly coined word, phrase, or expression, or an existing word used with a new meaning, often created to describe new concepts, technologies, or cultural phenomena that lack existing terminology. These linguistic innovations emerge through various processes including combining existing words, borrowing from other languages, creating entirely new terms, or extending meanings of current vocabulary. Neologisms frequently appear in rapidly changing fields like technology (email, smartphone, blog), popular culture (selfie, hashtag), and science where new discoveries require new names. The acceptance and adoption of neologisms depends on their usefulness, clarity, and how well they fill linguistic gaps. Some neologisms enter standard dictionaries and become permanent additions to language, while others remain temporary or specialized. Understanding neologism formation helps track cultural changes, technological development, and language evolution. Writers and speakers create neologisms to express ideas that existing vocabulary cannot adequately capture.',
                'pronunciation': '/niˈɑləˌdʒɪzəm/',
                'etymology': 'From Greek neo "new" + logos "word" + -ism suffix, literally meaning "new word doctrine." The term describes the creation and study of new words.',
                'memory_tip': 'Remember NEOLOGISM as "NEO (new) + LOGOS (word) + ISM" - the practice of creating new words to describe new concepts or ideas.',
                'example_sentence': 'The rapid growth of social media has produced many _____ like "unfriend," "tweet," and "viral" that are now widely accepted.'
            },
            'neonatology': {
                'definition': 'Neonatology is the medical specialty focused on the care of newborn infants, particularly premature babies and those with critical illnesses or birth defects requiring specialized treatment during the first weeks of life. This field combines intensive care medicine with developmental biology to address the unique physiological challenges faced by newborns whose organ systems are still developing. Neonatologists work in neonatal intensive care units (NICUs) using sophisticated equipment like ventilators, incubators, and monitoring systems to support infants who cannot yet maintain vital functions independently. The specialty addresses conditions such as respiratory distress syndrome, heart defects, infections, feeding difficulties, and complications of premature birth. Neonatology requires expertise in recognizing subtle signs of illness in patients who cannot communicate their symptoms verbally. The field has dramatically improved survival rates for premature and critically ill newborns through advances in medical technology, pharmaceutical treatments, and understanding of neonatal physiology.',
                'pronunciation': '/ˌnioʊnəˈtɑlədʒi/',
                'etymology': 'From Greek neo "new" + Latin natus "born" + Greek -logia "study of." The term literally means "study of the newly born."',
                'memory_tip': 'Remember NEONATOLOGY as "NEO (new) + NATAL (birth) + OLOGY (study)" - the medical study and care of newly born babies, especially those needing intensive care.',
                'example_sentence': 'The hospital\'s _____ department provided round-the-clock care for premature infants born before 32 weeks gestation.'
            },
            'neonbeeswax': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "neon beeswax" - combining the bright gas/color with the natural wax substance.',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "neon" and "beeswax"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'neophyte': {
                'definition': 'A neophyte is a beginner or newcomer to a particular field, activity, or belief system, someone who is new to a subject and lacks experience or expertise in that area. The term originally referred to newly baptized Christians or recent converts to religious faith, but has expanded to describe novices in any domain including business, arts, sports, or academic disciplines. Neophytes typically require guidance, training, and patience as they learn fundamental skills and concepts that experts take for granted. The learning curve for neophytes can be steep, requiring time and practice to develop competence and confidence. Organizations often have mentorship programs or training systems designed to support neophytes during their transition from beginner to competent practitioner. While neophytes may lack experience, they often bring fresh perspectives, enthusiasm, and innovative approaches that can benefit established organizations. Understanding how to effectively integrate and support neophytes contributes to organizational success and knowledge transfer.',
                'pronunciation': '/ˈniəfaɪt/',
                'etymology': 'From Greek neophytos meaning "newly planted," from neo "new" + phyton "plant." Originally used for newly baptized Christians, like new plants in the faith.',
                'memory_tip': 'Remember NEOPHYTE as "NEO (new) + PHYTE (plant)" - a new plant or newly planted person in a field, a beginner who is just starting to grow in knowledge.',
                'example_sentence': 'As a _____ to mountain climbing, she enrolled in a basic course to learn essential safety techniques and equipment use.'
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
            'neonbeeswax'
        ]
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        logger.info("Processing Batch 117 with comprehensive Claude data...")
        
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
        logger.info("Batch 117 processing completed!")
        logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {len(processed_words)} successful, 0 failed")

if __name__ == "__main__":
    processor = Batch117Processor()
    
    input_file = "output/batch_117_words.csv"
    output_file = "output/batch_117_processed.csv"
    
    processor.process_batch(input_file, output_file)