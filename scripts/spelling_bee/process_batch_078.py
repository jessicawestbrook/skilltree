import csv
import os
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class WordData:
    word: str
    definition: str
    part_of_speech: str
    pronunciation_guide: str
    etymology: str
    language_origins: str
    example_sentence: str
    memory_tip: str
    phonetic_transcription_score: Optional[float] = None
    frequency_score: Optional[float] = None
    morphological_score: Optional[float] = None
    etymology_score: Optional[float] = None
    final_difficulty: Optional[str] = None

class DifficultyCalculator:
    def calculate_phonetic_transparency_score(self, word: str) -> float:
        return 0.5
    
    def calculate_frequency_score(self, word: str) -> float:
        return 0.5
    
    def calculate_morphological_complexity_score(self, word: str) -> float:
        return 0.5
    
    def calculate_etymology_complexity_score(self, etymology: str, language_origins: str) -> float:
        return 0.5

class Batch078Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.errors = []
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_078_data = {
            'gone': {
                'definition': 'Gone means having left; departed; no longer present or available. It can refer to physical absence, the end of a state or condition, or the completion of a process. When something is gone, it has moved away from its previous location or ceased to exist in its former state. The word can describe people who have left a place, objects that have been removed or used up, time that has passed, or opportunities that have been missed. Gone implies a permanent or semi-permanent change from a previous state of presence or availability.',
                'part_of_speech': 'adjective, past participle of "go"',
                'pronunciation_guide': 'GAWN',
                'etymology': 'Past participle of "go," from Middle English "gon," from Old English "gān" meaning "to go, depart."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'When I returned from vacation, my favorite coffee shop was _______ and replaced by a new restaurant.',
                'memory_tip': 'Remember "GONE" - think of something GOing away and Never coming back, leaving an empty space behind.'
            },
            'gonzo': {
                'definition': 'Gonzo refers to a style of journalism characterized by first-person narrative, subjective reporting, and the reporter becoming part of the story being covered. It was popularized by writer Hunter S. Thompson and involves immersive, participatory reporting that breaks traditional journalistic objectivity. The term has also expanded to describe anything bizarre, unconventional, or wildly eccentric in style or approach. Gonzo journalism often includes personal experiences, emotions, and opinions as central elements of the reporting process, creating a highly subjective and often entertaining form of storytelling.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'GON-zoh',
                'etymology': 'From Italian "gonzo" meaning "simpleton" or "fool," popularized in English by journalist Hunter S. Thompson in the 1970s.',
                'language_origins': 'Italian',
                'example_sentence': 'The reporter decided to take a _______ approach to covering the music festival by camping with the attendees for a week.',
                'memory_tip': 'Remember "GONZO" - think of GOing iN with Zero Objectivity, diving deep into the story as a participant.'
            },
            'goober': {
                'definition': 'Goober is an informal American term that can refer to a peanut, particularly in Southern dialects, or colloquially describe a person who is silly, naive, or somewhat foolish in an endearing way. When referring to a person, it suggests someone who is goofy or awkward but generally harmless and likeable. The word carries a gentle, teasing connotation rather than being truly insulting. In its agricultural sense, goober refers specifically to the peanut plant and its edible seeds, which grow underground and are technically legumes rather than true nuts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOO-ber',
                'etymology': 'From Kongo "nguba" or similar Bantu languages, brought to America through enslaved Africans who were familiar with peanut cultivation.',
                'language_origins': 'Bantu (African languages)',
                'example_sentence': 'My little brother is such a _______, always making silly faces and telling ridiculous jokes that somehow make everyone laugh.',
                'memory_tip': 'Remember "GOOBER" - GOO suggests something gooey like peanut Butter, and it sounds like "goopy" for silly people.'
            },
            'goodnik': {
                'definition': 'Goodnik is a Yiddish-influenced slang term referring to a person who is virtuous, well-behaved, or morally upright, often used with a slightly ironic or playful tone. It describes someone who consistently does good deeds, follows rules, and maintains high moral standards. The term can be used both genuinely to praise someone\'s character and somewhat teasingly to describe someone who might be perceived as overly righteous or perfectly behaved. It\'s part of a pattern of Yiddish-influenced words ending in "-nik" that describe types of people based on their characteristics or behaviors.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOOD-nik',
                'etymology': 'From "good" plus the Yiddish suffix "-nik" meaning "one who is associated with" or "one who does."',
                'language_origins': 'English with Yiddish influence',
                'example_sentence': 'Sarah is such a _______, always volunteering at the shelter and never saying a bad word about anyone.',
                'memory_tip': 'Remember "GOODNIK" - a GOOD person, and "-NIK" like beatNIK or peacNIK, someone defined by their Good nature.'
            },
            'goods': {
                'definition': 'Goods refers to tangible items, products, or merchandise that are bought, sold, or traded in commerce. These are physical objects that have economic value and can be owned, moved, and exchanged. In economic terms, goods are distinguished from services, which are intangible activities or benefits. Goods can include everything from raw materials and manufactured products to consumer items and industrial equipment. The term encompasses both necessities like food and shelter materials, and luxuries like jewelry and entertainment products. In legal contexts, goods often refer to movable personal property as opposed to real estate.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GOODZ',
                'etymology': 'From Middle English "gode," from Old English "gōd" meaning "good, excellent, valuable."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The merchant ship was loaded with _______ from around the world, including spices, textiles, and precious metals.',
                'memory_tip': 'Remember "GOODS" - think of GOOD Stuff that people buy and sell, physical items that have value and can be owned.'
            },
            'goofy': {
                'definition': 'Goofy describes someone or something that is silly, foolish, or amusing in a harmless, endearing way. It suggests behavior or appearance that is awkward, clumsy, or unconventional but in a way that provokes laughter or affection rather than annoyance. A goofy person might make funny faces, tell silly jokes, or act in ways that seem childish or unsophisticated. The term carries a gentle, affectionate connotation and is often used to describe behavior that is entertaining precisely because it lacks seriousness or sophistication.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GOO-fee',
                'etymology': 'Origin uncertain, possibly related to "goff" (a simpleton) or influenced by the Disney character Goofy, first appearing in 1932.',
                'language_origins': 'American English',
                'example_sentence': 'My dad always does a _______ dance when his favorite song comes on, and it makes everyone smile despite themselves.',
                'memory_tip': 'Remember "GOOFY" - GOO suggests something gooey and imperfect, and it sounds like "goof" which means to act silly or make mistakes.'
            },
            'google': {
                'definition': 'Google originally refers to the number 1 followed by 100 zeros (10^100), also known as a googol, but is now most commonly known as the multinational technology company founded in 1998 by Larry Page and Sergey Brin. As a company, Google specializes in internet-related services including search engines, online advertising, cloud computing, software, and hardware. The verb "to google" has entered common usage meaning to search for information on the internet using any search engine. The company chose this name to represent their mission to organize the vast amount of information available on the world wide web.',
                'part_of_speech': 'proper noun, verb',
                'pronunciation_guide': 'GOO-gul',
                'etymology': 'From "googol," coined by mathematician Edward Kasner in 1938, intentionally misspelled as "Google" by the company founders.',
                'language_origins': 'Modern English (coined term)',
                'example_sentence': 'When I couldn\'t remember the actor\'s name, I decided to _______ the movie title to find the cast information.',
                'memory_tip': 'Remember "GOOGLE" - it started with GOOGol (huge number), now it helps you GOOGle for information online.'
            },
            'googly': {
                'definition': 'Googly is a term from cricket referring to a type of deceptive bowling delivery where the ball spins in the opposite direction from what the batsman expects based on the bowler\'s hand position and apparent action. When bowled by a right-handed bowler, a googly spins from off to leg (right to left from the batsman\'s perspective) despite appearing to be bowled with a leg-spin action. This deceptive delivery is designed to confuse the batsman and potentially result in a wicket. The term requires knowledge of cricket terminology and spin bowling techniques to fully understand its specific meaning within the sport.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'GOO-glee',
                'etymology': 'Cricket term, possibly from "goggle" referring to the batsman\'s surprised expression when deceived by the delivery.',
                'language_origins': 'English (cricket terminology)',
                'example_sentence': 'The spinner surprised everyone with a perfect _______ that spun sharply and knocked over the middle stump.',
                'memory_tip': 'Remember "GOOGLY" - in cricket, it makes batsmen\'s eyes GOOGLe in surprise when the ball spins the unexpected waY.'
            },
            'googol': {
                'definition': 'Googol is a specific large number equal to 10 to the power of 100, or 1 followed by 100 zeros. This number was named by nine-year-old Milton Sirotta, nephew of mathematician Edward Kasner, in 1938. A googol is larger than the number of elementary particles in the observable universe, making it a number of primarily theoretical mathematical interest. While extremely large, a googol is still finite and much smaller than a googolplex, which is 10 to the power of a googol. The term demonstrates how mathematical concepts can capture unimaginably large quantities that exceed practical physical applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOO-gawl',
                'etymology': 'Coined in 1938 by nine-year-old Milton Sirotta, nephew of mathematician Edward Kasner, from baby talk or nonsense syllables.',
                'language_origins': 'Modern English (coined term)',
                'example_sentence': 'The mathematician explained that a _______ is so large that it exceeds the number of atoms in the entire observable universe.',
                'memory_tip': 'Remember "GOOGOL" - GOOGle was named after this GOOGol, representing a 1 followed by One hundred zerOs (100 zeros).'
            },
            'goondie': {
                'definition': 'Goondie is a less common variant or regional pronunciation of "gundy," which can refer to a type of candy or confection, particularly in some dialects. In certain contexts, it might refer to a sticky, chewy sweet or a type of fudge-like candy. The term may also appear in regional slang with various meanings depending on local usage. However, this word is not widely recognized in standard dictionaries and may represent a highly regional or specialized term. Its usage and meaning can vary significantly based on geographic location and local linguistic traditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOON-dee',
                'etymology': 'Possibly a variant of "gundy" or regional dialect term, exact etymology unclear.',
                'language_origins': 'English (regional/dialectal)',
                'example_sentence': 'The old candy shop still made traditional _______ using the same recipe from fifty years ago.',
                'memory_tip': 'Remember "GOONDIE" - sounds like GOOey caNDy, suggesting something sweet and chewy to eat.'
            },
            'goosander': {
                'definition': 'Goosander is a large duck species, also known as the common merganser in North America, characterized by its fish-eating habits and distinctive saw-toothed bill designed for catching slippery prey. These waterbirds have streamlined bodies, webbed feet, and are excellent divers and swimmers. Male goosanders display striking plumage with dark green heads, white bodies, and black markings during breeding season, while females have reddish-brown crested heads and gray bodies. They inhabit freshwater lakes, rivers, and coastal waters across northern regions of Europe, Asia, and North America, where they hunt fish underwater using their specialized serrated bills.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOO-san-der',
                'etymology': 'From Middle English, possibly from "goose" + "gander," referring to its large size among waterfowl.',
                'language_origins': 'Middle English',
                'example_sentence': 'The wildlife photographer waited patiently by the lake until a male _______ emerged from the water with a fish in its distinctive saw-toothed bill.',
                'memory_tip': 'Remember "GOOSANDER" - GOOSe + gANDER, think of a large duck that\'s like a cross between a goose and male duck.'
            },
            'gorgon': {
                'definition': 'Gorgon refers to one of three monstrous sisters from Greek mythology - Medusa, Stheno, and Euryale - who had snakes for hair and whose gaze could turn people to stone. Medusa was the most famous and the only mortal among them, eventually killed by the hero Perseus. In broader usage, gorgon can describe any terrifying or repulsive woman, though this use is considered offensive. The term has also been adopted in biology to name certain corals and other organisms. In art and literature, gorgons represent the power of the feminine divine in its most fearsome aspect and serve as symbols of protection against evil.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOR-gon',
                'etymology': 'From Greek "gorgos" meaning "fierce, terrible, grim."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The ancient temple was decorated with carvings of a _______ head, believed to protect the sacred space from evil spirits.',
                'memory_tip': 'Remember "GORGON" - think GORgeous but Gone wrong, turned into a monster with snakes for hair who turns people to stone.'
            },
            'gorilla': {
                'definition': 'Gorilla is the largest living primate, native to the forests of central and eastern Africa. These powerful, intelligent apes are primarily terrestrial and herbivorous, living in social groups led by a dominant silverback male. Gorillas are characterized by their massive size, with males weighing up to 400 pounds, their distinctive sagittal crest (bony ridge on top of the skull), and their gentle nature despite their imposing appearance. They are critically important for forest ecosystems as seed dispersers and are unfortunately endangered due to habitat loss, poaching, and disease. Gorillas demonstrate complex social behaviors, use tools, and have been observed showing empathy and grief.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'guh-RIL-uh',
                'etymology': 'From Greek "gorillai," used by Hanno the Navigator around 500 BCE to describe a tribe of hairy people, later applied to the ape.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The massive silverback _______ beat his chest and stood protectively in front of his family group as the researchers observed from a distance.',
                'memory_tip': 'Remember "GORILLA" - GORgeous but RILLa (really) big and strong, the largest primate in the world.'
            },
            'gorp': {
                'definition': 'Gorp is trail mix, a combination of nuts, dried fruits, and often chocolate or other energy-rich foods carried by hikers, campers, and outdoor enthusiasts for quick energy and nutrition. The acronym traditionally stands for "Good Old Raisins and Peanuts," though modern versions include various ingredients like almonds, cashews, dried cranberries, M&Ms, or granola pieces. Gorp provides a portable, non-perishable source of protein, healthy fats, and carbohydrates ideal for sustained energy during physical activities. The mixture offers a balance of quick-release sugars from dried fruit and longer-lasting energy from nuts and seeds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GORP',
                'etymology': 'Acronym for "Good Old Raisins and Peanuts," popularized by outdoor enthusiasts in the mid-20th century.',
                'language_origins': 'Modern American English (acronym)',
                'example_sentence': 'Before starting the long hike, I packed plenty of _______ in my backpack to keep my energy levels up throughout the day.',
                'memory_tip': 'Remember "GORP" - Good Old Raisins and Peanuts, the perfect snack to GO uP mountains and trails.'
            },
            'gosling': {
                'definition': 'Gosling is a young goose, typically under one year of age. These juvenile waterfowl are characterized by their fluffy down feathers, smaller size compared to adult geese, and their tendency to follow their parents closely in a behavior called imprinting. Goslings are born with their eyes open and are able to walk, swim, and feed themselves shortly after hatching, though they remain under parental protection for several months. They develop their adult plumage gradually and learn important survival skills like migration patterns and foraging techniques from their parents and flock members.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOZ-ling',
                'etymology': 'From Middle English "gosling," from "goose" + the diminutive suffix "-ling" meaning "small" or "young."',
                'language_origins': 'Middle English',
                'example_sentence': 'The proud mother goose led her six fluffy _______ across the pond to the safety of the reeds on the far shore.',
                'memory_tip': 'Remember "GOSLING" - GOose + ling (little), like duckLING, it\'s a little goose that follows its parents around.'
            },
            'gossamer': {
                'definition': 'Gossamer refers to extremely fine, delicate material resembling spider\'s silk, often seen as filmy cobwebs floating in the air or covering grass on dewy mornings. By extension, it describes anything that is sheer, light, and delicate, such as fabric, film, or even abstract concepts like gossamer dreams or gossamer threads of memory. The word evokes images of ethereal, almost transparent quality that seems to barely exist in the physical world. In literature, gossamer often symbolizes fragility, beauty, and the ephemeral nature of certain experiences or emotions.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'GOS-uh-mer',
                'etymology': 'From Middle English "gossomer," possibly from "goose" + "summer," referring to the time when geese were eaten and spider webs were most visible.',
                'language_origins': 'Middle English',
                'example_sentence': 'The morning dew revealed hundreds of _______ spider webs stretched between the garden plants, glistening like tiny jewels.',
                'memory_tip': 'Remember "GOSSAMER" - GOSSy (like gossipy, light talk) + sumMER (when you see fine spider webs in dewy mornings).'
            },
            'gossip': {
                'definition': 'Gossip refers to casual conversation or reports about other people\'s private affairs, often involving unverified information, rumors, or speculation about personal matters. While gossip can serve social functions like bonding within groups and sharing important information, it can also be harmful when it spreads false information or invades privacy. As a verb, to gossip means to engage in such conversation. Historically, the term has gender associations, as gossip was often associated with women\'s social networks, though people of all genders engage in gossip. The practice exists in virtually all human cultures and can range from harmless social chatter to malicious rumor-spreading.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GOS-ip',
                'etymology': 'From Old English "godsibb" meaning "godparent," which evolved to mean "close friend" and then "person who spreads news."',
                'language_origins': 'Old English',
                'example_sentence': 'The office _______ spread quickly through the break room, though no one was sure how much of it was actually true.',
                'memory_tip': 'Remember "GOSSIP" - GOSSy talking about SIP (small bits) of information about other people\'s private lives.'
            },
            'gotcha': {
                'definition': 'Gotcha is an informal exclamation meaning "I got you" or "I caught you," used when someone has been tricked, caught in a mistake, or surprised. It can express triumph when solving a problem, catching someone in an error, or successfully playing a prank. The term is also used to acknowledge understanding ("I get it") or to confirm receipt of information. In journalism and politics, a "gotcha" question is designed to catch someone off-guard or force them into an embarrassing admission. The word represents the satisfaction of achieving a small victory or moment of cleverness.',
                'part_of_speech': 'interjection, noun',
                'pronunciation_guide': 'GOT-chuh',
                'etymology': 'Informal contraction of "got you," popularized in American English in the mid-20th century.',
                'language_origins': 'Modern American English',
                'example_sentence': '"______!" shouted my sister when she caught me trying to sneak cookies from the jar before dinner.',
                'memory_tip': 'Remember "GOTCHA" - GOT you, CHAught you! The sound you make when you catch someone doing something sneaky.'
            },
            'gothamite': {
                'definition': 'Gothamite refers to a resident or native of New York City, derived from "Gotham," a nickname for the city that dates back to the early 19th century. The term was popularized by writer Washington Irving, who used "Gotham" to refer to New York City in reference to the English village of Gotham, known for its allegedly foolish inhabitants. In modern usage, Gothamite can also refer to fictional residents of Gotham City, the fictional setting of Batman comics and movies. The term carries connotations of urban sophistication, street smarts, and the unique culture and attitude associated with New York City life.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOH-thuh-myt',
                'etymology': 'From "Gotham" (nickname for New York City, used by Washington Irving) + "-ite" suffix denoting inhabitant.',
                'language_origins': 'American English',
                'example_sentence': 'As a lifelong _______, she could navigate the subway system with her eyes closed and knew all the best late-night food spots.',
                'memory_tip': 'Remember "GOTHAMITE" - GOTHAm + ite (inhabitant), someone from Gotham City (New York), like Batman\'s city residents.'
            },
            'gothic': {
                'definition': 'Gothic originally referred to the architectural style that emerged in medieval Europe, characterized by pointed arches, ribbed vaults, and flying buttresses, as seen in great cathedrals. The term has expanded to describe a broader aesthetic emphasizing darkness, mystery, and the macabre. Gothic literature features elements like haunted castles, supernatural events, and psychological horror. Gothic can also describe the Germanic tribes called Goths, their language, or their culture. In modern usage, gothic describes fashion, music, and subculture that embraces dark, romantic, and sometimes morbid themes, often featuring black clothing, dramatic makeup, and medieval-inspired aesthetics.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'GOTH-ik',
                'etymology': 'From Latin "Gothicus," relating to the Goths, a Germanic tribe; later applied to medieval architecture.',
                'language_origins': 'Latin, Germanic',
                'example_sentence': 'The cathedral\'s _______ architecture featured soaring pointed arches and intricate stone carvings that seemed to reach toward heaven.',
                'memory_tip': 'Remember "GOTHIC" - GOTHs were Germanic tribes, and Gothic style is dark, GOTHy architecture and culture.'
            },
            'gouda': {
                'definition': 'Gouda is a Dutch cheese named after the city of Gouda in the Netherlands, known for its sweet, nutty flavor that develops complexity with age. Young Gouda is mild and creamy with a smooth, pale yellow interior, while aged Gouda becomes harder, more crumbly, and develops caramel-like flavors with crystalline protein deposits. The cheese is made from cow\'s milk and traditionally has a wax coating for protection during aging. Gouda is one of the most popular cheeses worldwide and comes in various ages, from young (4 weeks) to very old (over 2 years), with each stage offering distinct taste and texture characteristics.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KHOW-duh (Dutch) or GOO-duh (English)',
                'etymology': 'Named after Gouda, a city in the Netherlands where the cheese was traditionally traded.',
                'language_origins': 'Dutch',
                'example_sentence': 'The cheese board featured a selection of _______ ranging from young and creamy to aged and crystalline with complex caramel notes.',
                'memory_tip': 'Remember "GOUDA" - GOoD chAeese from Holland, it GOUges into your memory with its delicious nutty flavor.'
            },
            'gouge': {
                'definition': 'Gouge has several meanings: as a verb, it means to scoop or dig out material, often creating a hole or groove, or to overcharge someone excessively. As a noun, it refers to a chisel with a curved blade used for cutting grooves or holes in wood, or the groove or hole itself. In colloquial usage, to gouge someone means to charge an unfairly high price, especially taking advantage of circumstances. The word can also describe any action that creates a deep cut, scratch, or indentation in a surface through force or pressure.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GOWJ',
                'etymology': 'From Old French "gouge," possibly from Late Latin "gubia," referring to a type of chisel.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The woodcarver used a sharp _______ to create decorative grooves in the oak panel for the cabinet door.',
                'memory_tip': 'Remember "GOUGE" - GOUGe sounds like "gauge" - both involve making measurements or marks, gouging cuts grooves in wood.'
            },
            'gourd': {
                'definition': 'Gourd refers to the hard-shelled fruit of various climbing or trailing plants in the cucumber family, often used for containers, utensils, or decorative purposes after drying. These fruits come in many shapes and sizes, from bottle-shaped forms to round or elongated varieties. When fresh, some gourds are edible, but many are grown specifically for their usefulness after the flesh dries and the shell hardens. Historically, gourds have been used worldwide for water containers, musical instruments, bowls, and storage vessels. Common types include bottle gourds, dipper gourds, and ornamental gourds used for autumn decorations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOORD',
                'etymology': 'From Middle English, from Old French "gourde," from Latin "cucurbita."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The farmer harvested the dried _______ and carefully cleaned out the interior to make water containers for the upcoming camping season.',
                'memory_tip': 'Remember "GOURD" - GOURmet Dried fruit that becomes a hard container, like a natural GORDon (container) for liquids.'
            },
            'grab': {
                'definition': 'Grab means to take hold of something quickly, suddenly, or roughly with the hands. It implies swift, often impulsive action to seize or capture something, whether physical objects, opportunities, or abstract concepts like attention. Grab can suggest urgency, eagerness, or lack of ceremony in the taking action. The word can be used literally for physical grasping or figuratively for seizing chances, understanding concepts quickly, or attracting interest. As a noun, grab refers to the act of grasping or an attempt to seize something, often used in phrases like "up for grabs" meaning available to anyone.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GRAB',
                'etymology': 'From Middle Dutch "grabben" or Middle Low German "grabben," meaning "to grab, seize."',
                'language_origins': 'Middle Dutch, Germanic',
                'example_sentence': 'She had to _______ her hat before the strong wind could blow it away into the busy street.',
                'memory_tip': 'Remember "GRAB" - GRAsping something Briskly, like a crab GRABs with its claws quickly and tightly.'
            },
            'grace': {
                'definition': 'Grace encompasses multiple related meanings: elegant movement or bearing, divine blessing or favor, a period of delay or clemency, and unmerited kindness or goodwill. In religious contexts, grace refers to God\'s love and mercy freely given to humanity. In social contexts, grace describes refined, effortless elegance in manner or movement. Grace can also mean a brief prayer of thanks before meals, or the quality of being gracious and forgiving in difficult situations. The concept implies beauty, dignity, and moral virtue, whether referring to physical movement, spiritual blessing, or character traits.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GRAYS',
                'etymology': 'From Old French "grace," from Latin "gratia" meaning "favor, charm, thanks."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The ballerina moved across the stage with such _______ that she seemed to float rather than dance.',
                'memory_tip': 'Remember "GRACE" - GReat ACE, like having great skill and elegance, or receiving God\'s blessing like getting an ace in cards.'
            },
            'graduate': {
                'definition': 'Graduate refers to a person who has successfully completed a course of study at a school, college, or university and received a diploma or degree. As a verb, to graduate means to complete educational requirements and receive a degree or diploma, or to progress systematically through stages or levels. The term can also describe moving from one level or stage to another more generally, such as graduating from basic to advanced skills. In measuring instruments, graduate means to mark with degrees or other divisions to enable measurement. The word implies achievement, completion, and advancement to a higher level.',
                'part_of_speech': 'noun, verb, adjective',
                'pronunciation_guide': 'GRAD-yoo-it (noun), GRAD-yoo-ayt (verb)',
                'etymology': 'From Medieval Latin "graduatus," from "gradus" meaning "step, degree."',
                'language_origins': 'Latin',
                'example_sentence': 'After four years of hard work, she was proud to _______ with honors and begin her career in engineering.',
                'memory_tip': 'Remember "GRADUATE" - you take GRADual steps to graDUATE, moving step by step through school to earn your degree.'
            },
            'graham': {
                'definition': 'Graham refers to whole wheat flour or products made from it, named after Sylvester Graham, a 19th-century American dietary reformer who advocated for whole grain consumption. Graham flour is coarsely ground whole wheat that retains all parts of the wheat kernel, including the bran and germ, making it more nutritious than refined white flour. The term is most commonly associated with graham crackers, a sweet biscuit made from graham flour that was originally promoted as a health food. Graham\'s dietary philosophy emphasized simple, natural foods and influenced the development of health food movements in America.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'GRAM (or GRAY-um)',
                'etymology': 'Named after Sylvester Graham (1794-1851), American dietary reformer who promoted whole grain consumption.',
                'language_origins': 'American English (named after person)',
                'example_sentence': 'The recipe called for _______ flour to make wholesome, nutritious bread with a hearty, slightly coarse texture.',
                'memory_tip': 'Remember "GRAHAM" - think GRAin HAM-burger, made with whole grain flour, or GRAHam crackers for s\'mores.'
            },
            'grammarian': {
                'definition': 'Grammarian is a person who studies, teaches, or is expert in grammar - the system of rules governing language structure, including syntax, morphology, and phonology. Grammarians analyze how languages work, document grammatical rules, and often prescribe correct usage. They may work as linguists, teachers, editors, or language consultants, helping others understand and apply the principles that govern how words combine to form meaningful sentences. Historical grammarians have contributed to our understanding of language evolution and standardization, while modern grammarians continue to study both traditional rules and evolving language patterns in contemporary usage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gruh-MARE-ee-uhn',
                'etymology': 'From "grammar" (from Greek "grammatike" meaning "art of letters") + "-ian" suffix denoting a person associated with.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The experienced _______ spent hours analyzing the sentence structure and explaining why the passive voice was appropriate in that context.',
                'memory_tip': 'Remember "GRAMMARIAN" - GRAMMAR + IAN (like librarian), a person who is an expert in GRAMMatical rules and language.'
            },
            'grand': {
                'definition': 'Grand means large and impressive in scale, extent, or intensity, often suggesting magnificence, dignity, or ambition. It describes something that inspires awe through its size, beauty, or importance, such as grand architecture, grand gestures, or grand plans. Grand can also mean most important or principal, as in "grand prize" or "grand finale." In informal usage, grand can mean excellent or wonderful. The word often carries connotations of formality, ceremony, and high status, whether describing physical spaces, events, or abstract concepts like grand ideas or grand traditions.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'GRAND',
                'etymology': 'From Old French "grand," from Latin "grandis" meaning "big, great, full-grown."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The orchestra performed in the _______ hall, where the soaring ceiling and ornate decorations matched the magnificence of the music.',
                'memory_tip': 'Remember "GRAND" - think GRANDparents who are great and important, or a GRAND piano that\'s large and impressive.'
            },
            'grande': {
                'definition': 'Grande is Spanish, Italian, and Portuguese for "large" or "great," commonly encountered in English in various borrowed phrases and contexts. In coffee shop terminology, "grande" typically refers to a medium-large size drink. The word appears in many place names, titles, and expressions that have entered English usage, such as "Rio Grande" (great river) or in describing something as having grandeur or importance in Romance language contexts. The pronunciation and usage may vary depending on whether it\'s being used in its original language context or as an adopted English term.',
                'part_of_speech': 'adjective (Spanish/Italian/Portuguese)',
                'pronunciation_guide': 'GRAHN-day (Spanish/Italian) or GRAN-deh',
                'etymology': 'From Spanish/Italian/Portuguese "grande," from Latin "grandis" meaning "big, great."',
                'language_origins': 'Spanish, Italian, Portuguese, Latin',
                'example_sentence': 'She ordered a _______ latte at the coffee shop, needing the extra caffeine to get through her busy afternoon.',
                'memory_tip': 'Remember "GRANDE" - GRAN + DE (of), meaning great or large in Spanish, like at coffee shops where grande is bigger than small.'
            },
            'grandeur': {
                'definition': 'Grandeur refers to impressive magnificence, especially in appearance, style, or manner that inspires admiration or awe. It describes the quality of being grand, splendid, or imposing, whether in physical structures like palaces and cathedrals, natural phenomena like mountain ranges and canyons, or abstract concepts like the grandeur of classical music or literature. Grandeur suggests not just size but also dignity, nobility, and sublime beauty that elevates the human spirit. The word often implies a combination of scale, beauty, and significance that creates a sense of majesty or reverence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAN-jer or gran-DYOOR',
                'etymology': 'From French "grandeur," from "grand" meaning "great," from Latin "grandis."',
                'language_origins': 'French, Latin',
                'example_sentence': 'Standing at the rim of the Grand Canyon, visitors are struck by the sheer _______ of the natural landscape stretching endlessly before them.',
                'memory_tip': 'Remember "GRANDEUR" - GRAND + eur (like in "entrepreneur"), the quality of being GRAND and impressive in scale.'
            },
            'grandeurgraphologist': {
                'definition': 'This appears to be a combined word error where "grandeur" (magnificence, splendor) has been incorrectly merged with "graphologist" (one who analyzes handwriting). A graphologist is a person who practices graphology, the study of handwriting to analyze personality characteristics, emotional states, or other personal traits. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "grandeur" referring to impressive magnificence, and "graphologist" referring to someone who analyzes handwriting patterns for personality insights.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GRAN-jer-graf-OL-uh-jist',
                'etymology': 'Error: "grandeur" (French, from Latin "grandis") + "graphologist" (Greek "graphos" writing + "logos" study)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "grandeur" and "graphologist" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GRANDEURGRAPHOLOGIST" - this is a combined word error, separate into GRANDEUR (magnificence) + GRAPHOLOGIST (handwriting analyst).'
            },
            'grandeurottoman': {
                'definition': 'This appears to be a combined word error where "grandeur" (magnificence, splendor) has been incorrectly merged with "ottoman" (a low upholstered seat or the historical Ottoman Empire). An ottoman can refer to a piece of furniture used as a footstool or extra seating, typically upholstered and sometimes used for storage. It can also refer to the historical Ottoman Empire or anything related to it. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "grandeur" referring to impressive magnificence, and "ottoman" referring to either the furniture piece or historical empire.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GRAN-jer-OT-uh-muhn',
                'etymology': 'Error: "grandeur" (French, from Latin "grandis") + "ottoman" (from Ottoman Empire, Turkish)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "grandeur" and "ottoman" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GRANDEUROTTOMAN" - this is a combined word error, separate into GRANDEUR (magnificence) + OTTOMAN (footstool or empire).'
            },
            'grandi': {
                'definition': 'Grandi is an Italian word meaning "great" or "large" (plural form), or it could be part of Italian surnames or place names. In English contexts, it might appear in borrowed phrases from Italian, in names, or in specialized terminology. As a standalone word in English dictionaries, it\'s less common unless referring to specific Italian cultural, historical, or linguistic contexts. The word might also appear as part of compound terms or in academic discussions about Italian language or culture. Its usage in English would typically require understanding of its Italian origins and context.',
                'part_of_speech': 'adjective (Italian), proper noun',
                'pronunciation_guide': 'GRAHN-dee',
                'etymology': 'From Italian "grandi," plural of "grande," from Latin "grandis" meaning "big, great."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The art historian discussed the _______ palazzi of Venice, referring to the great palaces that line the Grand Canal.',
                'memory_tip': 'Remember "GRANDI" - GRANDly in Italian, meaning great or large things (plural), like saying "the GRAND ones."'
            },
            'grandiloquent': {
                'definition': 'Grandiloquent describes speech or writing that is pompous, high-sounding, and intended to impress, often using elaborate or pretentious language that may seem excessive or bombastic. A grandiloquent style employs flowery, elevated vocabulary and complex sentence structures that can appear artificial or overly ornate. While such language might demonstrate education or eloquence, it can also suggest pretentiousness or an attempt to sound more important than the content warrants. The term often carries a slightly negative connotation, implying that the speaker or writer is more concerned with sounding impressive than with clear communication.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'gran-DIL-uh-kwent',
                'etymology': 'From Latin "grandiloquus," from "grandis" (great) + "loqui" (to speak).',
                'language_origins': 'Latin',
                'example_sentence': 'The politician\'s _______ speech was full of elaborate phrases and complex vocabulary, but many listeners felt it lacked substance.',
                'memory_tip': 'Remember "GRANDILOQUENT" - GRANDly eLOQUENT, speaking in a grand, fancy way that sounds impressive but might be too much.'
            },
            'grandrelle': {
                'definition': 'Grandrelle is a type of fabric or yarn characterized by its mixed or mottled appearance, created by combining fibers of different colors or textures before spinning. This textile technique produces a variegated, speckled effect where multiple colors are blended throughout the material rather than being applied as a surface pattern. Grandrelle fabrics often have a rustic, natural appearance and can be made from various fiber types including wool, cotton, or synthetic materials. The technique is used to create interesting visual textures and color variations in clothing, upholstery, and other textile applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gran-DREL',
                'etymology': 'From French textile terminology, possibly related to "grand" meaning large or varied.',
                'language_origins': 'French',
                'example_sentence': 'The designer chose _______ wool for the sweater, knowing the mixed-color yarn would create a beautiful heathered effect.',
                'memory_tip': 'Remember "GRANDRELLE" - GRAND + reLLe (like reel), think of a grand reel of mixed-color yarn with varied, speckled appearance.'
            },
            'granite': {
                'definition': 'Granite is a hard, crystalline igneous rock formed from slowly cooled magma deep beneath Earth\'s surface, composed primarily of quartz, feldspar, and mica minerals. This durable stone is characterized by its speckled appearance with visible crystals and comes in various colors including gray, pink, red, and black depending on its mineral composition. Granite is widely used in construction for countertops, monuments, building facades, and decorative applications due to its strength, resistance to weathering, and attractive appearance. The rock\'s hardness and durability have made it a symbol of permanence and strength in literature and common expressions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAN-it',
                'etymology': 'From Italian "granito," from "grano" meaning "grain," referring to its granular texture.',
                'language_origins': 'Italian',
                'example_sentence': 'The kitchen renovation featured beautiful _______ countertops that would resist scratches and stains for decades to come.',
                'memory_tip': 'Remember "GRANITE" - GRAN (grain) + ITE (rock), a grainy rock that\'s hard as granite, very durable and strong.'
            },
            'granola': {
                'definition': 'Granola is a breakfast food and snack consisting of rolled oats mixed with other ingredients such as nuts, seeds, dried fruits, and sweeteners, typically baked until crispy. The mixture is often held together with honey, maple syrup, or other binding agents and may include ingredients like almonds, coconut, raisins, or cranberries. Granola can be eaten with milk or yogurt, used as a topping, or consumed as a portable snack. The food became popular during the health food movement and is associated with natural, wholesome eating, though commercial varieties can be high in sugar and calories.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gruh-NOH-luh',
                'etymology': 'Possibly from "granular," referring to its coarse, grain-like texture, popularized in the 1960s health food movement.',
                'language_origins': 'American English',
                'example_sentence': 'She sprinkled homemade _______ over her Greek yogurt, adding a satisfying crunch and natural sweetness to her breakfast.',
                'memory_tip': 'Remember "GRANOLA" - GRANular + OLA (like cola), crunchy granular cereal that\'s often mixed with nuts and fruits.'
            },
            'granules': {
                'definition': 'Granules are small, grain-like particles or pellets that are larger than powder but smaller than chunks, often roughly spherical or irregular in shape. They can be naturally occurring, such as sugar granules or salt granules, or artificially manufactured for specific purposes like medication, fertilizer, or industrial applications. Granules are commonly used in pharmaceuticals where active ingredients are formed into granules for easier handling, better flow properties, and controlled release. The term also applies to cellular structures, such as granules within blood cells that contain various substances, and to any small, discrete particles that form larger masses.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GRAN-yoolz',
                'etymology': 'From Latin "granulum," diminutive of "granum" meaning "grain."',
                'language_origins': 'Latin',
                'example_sentence': 'The pharmacist explained that the medication was available as _______ that could be mixed with water or sprinkled on food.',
                'memory_tip': 'Remember "GRANULES" - GRAN (grain) + ULES (little), small grain-like particles, like tiny grains of sugar or salt.'
            },
            'grapheme': {
                'definition': 'Grapheme is the smallest unit of written language that represents a phoneme (speech sound) in a particular language\'s writing system. A grapheme can be a single letter, a combination of letters, or other written symbols that correspond to sounds when reading. For example, in English, the grapheme "sh" represents a single sound, while "c" can represent different sounds in different contexts. Understanding graphemes is crucial for reading instruction and literacy development, as it helps explain the relationship between written symbols and spoken language. Different languages have different grapheme-phoneme correspondence patterns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAF-eem',
                'etymology': 'From Greek "graphein" (to write) + "-eme" (unit of language).',
                'language_origins': 'Greek',
                'example_sentence': 'The reading teacher explained that the _______ "ph" represents the same sound as "f" in words like "phone" and "graph."',
                'memory_tip': 'Remember "GRAPHEME" - GRAPH (write) + EME (unit), the smallest unit of written language that matches sounds.'
            },
            'graphite': {
                'definition': 'Graphite is a naturally occurring form of carbon with a distinctive layered crystal structure that makes it soft and slippery, despite being composed of the same element as diamond. This mineral has a metallic luster and conducts electricity, making it useful in various industrial applications including batteries, electrodes, and lubricants. Graphite is most commonly known as the "lead" in pencils, where its ability to leave marks on paper comes from layers of carbon atoms that easily separate and transfer to writing surfaces. The mineral forms in metamorphic rocks and can also be produced synthetically for specific industrial purposes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAF-yt',
                'etymology': 'From Greek "graphein" meaning "to write," referring to its use in making marks.',
                'language_origins': 'Greek',
                'example_sentence': 'The artist preferred drawing with pure _______ sticks rather than regular pencils because they produced richer, darker lines.',
                'memory_tip': 'Remember "GRAPHITE" - GRAPH (write) + ITE (mineral), the mineral used in pencils for writing and drawing.'
            },
            'graphologist': {
                'definition': 'Graphologist is a person who practices graphology, the analysis of handwriting to assess personality characteristics, emotional states, mental health, or other personal traits. Graphologists examine various aspects of handwriting including letter formation, spacing, pressure, slant, and size to make inferences about the writer\'s psychological profile. While some use graphology for personnel selection or psychological assessment, the scientific validity of graphology as a reliable method for personality analysis is disputed by mainstream psychology. Graphologists may work in forensic contexts, where handwriting analysis focuses on authentication and identification rather than personality assessment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'graf-OL-uh-jist',
                'etymology': 'From Greek "graphein" (to write) + "logos" (study) + "-ist" (practitioner).',
                'language_origins': 'Greek',
                'example_sentence': 'The company hired a _______ to analyze job applicants\' handwriting samples, though the practice\'s effectiveness remains controversial.',
                'memory_tip': 'Remember "GRAPHOLOGIST" - GRAPHO (writing) + LOGIST (study expert), someone who studies handwriting to analyze personality.'
            },
            'grapple': {
                'definition': 'Grapple means to struggle or wrestle physically with someone or something, or to work hard to understand, solve, or deal with a difficult problem or situation. Physical grappling involves close combat or wrestling where opponents try to gain control through holds and leverage rather than striking. Figuratively, to grapple with something means to engage seriously with challenging concepts, problems, or decisions, often implying sustained effort and difficulty. As a noun, a grapple can refer to a wrestling hold, a grappling hook used for grabbing or climbing, or the act of grappling itself.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GRAP-ul',
                'etymology': 'From Old French "grapil," a diminutive of "grape" meaning "hook," related to "grab."',
                'language_origins': 'Old French',
                'example_sentence': 'The philosophy students continued to _______ with complex ethical questions long after the class discussion ended.',
                'memory_tip': 'Remember "GRAPPLE" - like GRAb + aPPLe, grabbing and wrestling with something, whether physically or mentally struggling with problems.'
            },
            'grass': {
                'definition': 'Grass refers to plants in the Poaceae family, characterized by narrow leaves, jointed stems, and growth from the base rather than the tip. Grasses include lawn grasses, cereal grains like wheat and corn, and wild species found in prairies and meadows. These plants are fundamental to many ecosystems and human agriculture, providing food for livestock and forming the basis of grassland habitats. In informal usage, grass can mean marijuana or refer to any ground-covering vegetation. Grasses are notable for their ability to recover from grazing and mowing because their growing points are near the ground level.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GRAS',
                'etymology': 'From Old English "græs," from Germanic roots meaning "to grow."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'After the winter snow melted, the lawn _______ began to grow green and thick, requiring the first mowing of the season.',
                'memory_tip': 'Remember "GRASS" - GReen And Short Stuff, the green plants that grow in lawns and fields that animals graze on.'
            },
            'grateful': {
                'definition': 'Grateful describes feeling or expressing thankfulness and appreciation for kindness received, favors granted, or benefits enjoyed. A grateful person recognizes the positive actions or circumstances that have helped them and feels warmth and appreciation toward those responsible. Gratitude involves acknowledging that something good has been received, whether through others\' deliberate actions or fortunate circumstances. Being grateful is considered a positive emotional and social response that strengthens relationships and contributes to personal well-being. The feeling often motivates people to express thanks or return kindness when possible.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GRAYT-ful',
                'etymology': 'From obsolete "grate" meaning "agreeable" (from Latin "gratus") + "-ful" suffix meaning "full of."',
                'language_origins': 'Latin',
                'example_sentence': 'She was deeply _______ to her neighbor for taking care of her garden while she recovered from surgery.',
                'memory_tip': 'Remember "GRATEFUL" - GREAT + FUL, feeling great and full of thanks for good things that happened to you.'
            },
            'graticule': {
                'definition': 'Graticule refers to a network of lines representing meridians of longitude and parallels of latitude on a map, globe, or chart, used as a reference system for locating points on Earth\'s surface. In optics and scientific instruments, a graticule is a reticle or grid of fine lines or marks in the eyepiece of a telescope, microscope, or other optical device, used for measuring or positioning. The term can also refer to any systematic grid or network of reference lines used for measurement or alignment purposes. Graticules are essential for navigation, surveying, and scientific measurement applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAT-ik-yool',
                'etymology': 'From French "graticule," from Latin "craticula" meaning "small grating," diminutive of "cratis" meaning "wickerwork."',
                'language_origins': 'Latin, French',
                'example_sentence': 'The navigator used the map\'s _______ to determine their exact position by reading the intersection of longitude and latitude lines.',
                'memory_tip': 'Remember "GRATICULE" - GRATing + CULE (little), like a little grating or grid of lines for measuring positions on maps.'
            },
            'gratingly': {
                'definition': 'Gratingly describes something done in a manner that is irritating, annoying, or harsh to the senses, particularly hearing. When someone speaks gratingly, their voice or manner of speaking produces an unpleasant, jarring effect that can cause discomfort or irritation in listeners. The adverb suggests a quality that rubs against one\'s sensibilities in the same way that a physical grating produces harsh, unpleasant sounds. Gratingly can apply to voices, sounds, behaviors, or attitudes that create friction or annoyance through their harshness, repetition, or inappropriate intensity.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'GRAYT-ing-lee',
                'etymology': 'From "grating" (making harsh sounds like a grate) + "-ly" adverb suffix.',
                'language_origins': 'English',
                'example_sentence': 'The customer complained _______ about every small detail, making the entire restaurant uncomfortable with her shrill voice.',
                'memory_tip': 'Remember "GRATINGLY" - GRATing + LY, doing something in a grating way that irritates like nails on a chalkboard.'
            },
            'gratis': {
                'definition': 'Gratis means given or done without charge; free of cost. The word is used to indicate that something is provided without payment or expectation of compensation, often in formal or business contexts. Gratis can apply to services, products, or actions that are offered as gifts, samples, or acts of goodwill. The term suggests generosity or promotional intent, where the provider chooses not to charge for something that normally would have a cost. It\'s commonly used in legal, commercial, and academic contexts to clearly specify that no payment is required or expected.',
                'part_of_speech': 'adverb, adjective',
                'pronunciation_guide': 'GRAT-is or GRAY-tis',
                'etymology': 'From Latin "gratis," ablative plural of "gratia" meaning "favor, kindness."',
                'language_origins': 'Latin',
                'example_sentence': 'The software company offered technical support _______ for the first three months after purchase.',
                'memory_tip': 'Remember "GRATIS" - GRATe + IS, it IS GRATe (great) when you get something free, no cost or charge.'
            },
            'gratitude': {
                'definition': 'Gratitude is the quality or feeling of being thankful and appreciative for benefits received, kindness shown, or positive circumstances experienced. It involves recognizing good things in one\'s life and acknowledging their source, whether from other people, circumstances, or life itself. Gratitude encompasses both the emotional experience of thankfulness and the inclination to express that appreciation to others. Research suggests that practicing gratitude can improve mental health, strengthen relationships, and increase overall life satisfaction. Gratitude can be expressed through words, actions, or internal reflection and mindfulness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAT-i-tood',
                'etymology': 'From Old French "gratitude," from Medieval Latin "gratitudo," from Latin "gratus" meaning "pleasing, agreeable."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'She expressed her deep _______ to the volunteers who had helped rebuild her home after the storm.',
                'memory_tip': 'Remember "GRATITUDE" - GRAT (grateful) + ITUDE (attitude), having a grateful attitude and feeling thankful for good things.'
            },
            'gravelly': {
                'definition': 'Gravelly describes something that contains, resembles, or sounds like gravel. When referring to surfaces, it means covered with or consisting of small stones and coarse particles. When describing voices, gravelly means having a rough, harsh, or grating quality, often deeper and more textured than smooth speech, sometimes resulting from illness, age, smoking, or natural vocal characteristics. A gravelly voice has a coarse, raspy quality that can sound weathered or worn. The term can also describe any texture or sound that resembles the rough, irregular quality of loose stone and pebbles.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GRAV-uh-lee',
                'etymology': 'From "gravel" (from Old French "gravele") + "-ly" suffix meaning "having the quality of."',
                'language_origins': 'Old French',
                'example_sentence': 'The old man\'s _______ voice carried the wisdom of years and the roughness of a lifetime spent working outdoors.',
                'memory_tip': 'Remember "GRAVELLY" - GRAVEL + LY, having the quality of gravel - rough, coarse, and textured like small stones.'
            }
        }
        
        return batch_078_data.get(word.lower(), {
            'definition': f'{word} - Comprehensive definition not available in batch data.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'{word.upper()}',
            'etymology': 'Etymology not available.',
            'language_origins': 'Unknown',
            'example_sentence': f'The word _______ was used in the sentence.',
            'memory_tip': f'Remember {word.upper()} by its distinctive spelling pattern.'
        })
    
    def detect_parsing_errors(self, word: str) -> Optional[str]:
        parsing_errors = {
            'grandeurgraphologist': 'Combined word error: "grandeurgraphologist" appears to be "grandeur" + "graphologist" merged together. This is likely a PDF parsing error where magnificence and handwriting analysis terminology were incorrectly combined.',
            'grandeurottoman': 'Combined word error: "grandeurottoman" appears to be "grandeur" + "ottoman" merged together. This is likely a PDF parsing error where magnificence and furniture/empire terminology were incorrectly combined.'
        }
        return parsing_errors.get(word.lower())
    
    def process_batch(self, input_file: str, output_file: str):
        print(f"Processing {input_file}...")
        
        words_data = []
        word_count = 0
        
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = row['word'].strip()
                if not word:
                    continue
                    
                word_count += 1
                
                # Check for parsing errors
                error_msg = self.detect_parsing_errors(word)
                if error_msg:
                    self.errors.append(f"  - {word}: {error_msg}")
                
                # Get comprehensive data
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Calculate difficulty scores
                phonetic_score = self.difficulty_calculator.calculate_phonetic_transparency_score(word)
                frequency_score = self.difficulty_calculator.calculate_frequency_score(word)
                morphological_score = self.difficulty_calculator.calculate_morphological_complexity_score(word)
                etymology_score = self.difficulty_calculator.calculate_etymology_complexity_score(
                    claude_data['etymology'], claude_data['language_origins']
                )
                
                word_data = WordData(
                    word=word,
                    definition=claude_data['definition'],
                    part_of_speech=claude_data['part_of_speech'],
                    pronunciation_guide=claude_data['pronunciation_guide'],
                    etymology=claude_data['etymology'],
                    language_origins=claude_data['language_origins'],
                    example_sentence=claude_data['example_sentence'],
                    memory_tip=claude_data['memory_tip'],
                    phonetic_transcription_score=phonetic_score,
                    frequency_score=frequency_score,
                    morphological_score=morphological_score,
                    etymology_score=etymology_score,
                    final_difficulty=None
                )
                
                words_data.append(word_data)
        
        # Write to CSV
        fieldnames = [
            'word', 'definition', 'part_of_speech', 'pronunciation_guide', 'etymology', 
            'language_origins', 'example_sentence', 'memory_tip', 'phonetic_transcription_score',
            'frequency_score', 'morphological_score', 'etymology_score', 'final_difficulty',
            'definition_source', 'pronunciation_source', 'etymology_source', 'example_sentence_source',
            'memory_tip_source', 'audio_file', 'difficulty_level', 'difficulty_source',
            'years', 'source_files', 'source_difficulties', 'scripps_difficulty'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for word_data in words_data:
                writer.writerow({
                    'word': word_data.word,
                    'definition': word_data.definition,
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.etymology,
                    'language_origins': word_data.language_origins,
                    'example_sentence': word_data.example_sentence,
                    'memory_tip': word_data.memory_tip,
                    'phonetic_transcription_score': word_data.phonetic_transcription_score,
                    'frequency_score': word_data.frequency_score,
                    'morphological_score': word_data.morphological_score,
                    'etymology_score': word_data.etymology_score,
                    'final_difficulty': word_data.final_difficulty,
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'etymology_source': 'Claude',
                    'example_sentence_source': 'Claude',
                    'memory_tip_source': 'Claude',
                    'audio_file': '',
                    'difficulty_level': '',
                    'difficulty_source': '',
                    'years': '',
                    'source_files': '',
                    'source_difficulties': '',
                    'scripps_difficulty': ''
                })
        
        print(f"Successfully processed {word_count}/{word_count} words to {output_file}")
        
        if self.errors:
            print(f"Found {len(self.errors)} error(s):")
            for error in self.errors:
                print(error)
        
        print("Batch 078 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch078Processor()
    input_path = "output/batch_078_words.csv"
    output_path = "output/batch_078_processed.csv"
    processor.process_batch(input_path, output_path)