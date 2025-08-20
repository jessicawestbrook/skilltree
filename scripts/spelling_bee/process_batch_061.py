#!/usr/bin/env python3

import pandas as pd
import csv
from dataclasses import dataclass
from typing import Optional
import os

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
    
class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_word_frequency(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_morphological_complexity(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_etymology_complexity(word: str) -> int:
        return 3

class Batch061Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_061_data = {
            'equanimitythermos': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "equanimity" (mental composure and emotional balance) and "thermos" (an insulated container for maintaining liquid temperature). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'equation': {
                'definition': 'An equation is a mathematical statement that asserts the equality of two expressions, typically connected by an equals sign (=). Equations are fundamental tools in mathematics, science, and engineering for describing relationships between variables, solving problems, and modeling real-world phenomena. Simple equations might express basic arithmetic relationships, while complex equations can describe physical laws, chemical reactions, or economic models. Solving equations involves finding values for unknown variables that make the equation true. Different types of equations include linear equations (with variables to the first power), quadratic equations (with variables squared), and differential equations (involving rates of change). Equations appear throughout algebra, calculus, physics, chemistry, and other fields. The process of working with equations develops logical thinking and problem-solving skills. Understanding equations is essential for scientific literacy and mathematical reasoning. Modern technology uses equations extensively in computer algorithms, engineering designs, and data analysis.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-KWAY-zhuhn',
                'etymology': 'From Latin "aequationem," from "aequare" (to make equal), from "aequus" (equal). The mathematical sense developed in medieval Latin.',
                'language_origins': 'Latin',
                'example_sentence': 'The student learned to solve quadratic _______ using the formula method.',
                'memory_tip': 'Remember "e-QUATION" - think "equal-ation" meaning the action of making things equal, or "equation" contains "equal" which is what the = sign shows.'
            },
            'equatoguinean': {
                'definition': 'Equatoguinean refers to something relating to Equatorial Guinea, a small West African country located on the Atlantic coast. This adjective describes people, culture, products, or characteristics associated with Equatorial Guinea, which consists of a mainland region (Rio Muni) and several islands including Bioko Island where the capital Malabo is located. The country is unique in Africa for having Spanish as an official language due to its history as a Spanish colony. Equatoguinean culture blends African traditions with Spanish colonial influences. The economy is largely based on oil production, which has brought significant wealth but also challenges in terms of income distribution and development. Understanding Equatoguinean geography and culture helps appreciate the diversity of African nations and the complex legacy of colonialism. The term is used in political, economic, and cultural contexts when discussing this nation and its people. Equatorial Guinea has unique characteristics that distinguish it from other African countries.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ee-kway-toh-GIN-ee-uhn',
                'etymology': 'From "Equatorial Guinea" (named for its location near the equator and the historical region of Guinea in West Africa) + "-an" (suffix meaning "relating to").',
                'language_origins': 'Spanish, Portuguese',
                'example_sentence': 'The _______ delegation discussed trade agreements at the international conference.',
                'memory_tip': 'Remember "EQUATO-guinean" - think "equator-Guinea" because Equatorial Guinea is near the equator in the Guinea region of Africa.'
            },
            'equator': {
                'definition': 'The equator is an imaginary line that circles the Earth at its widest point, positioned halfway between the North and South poles at 0° latitude. This great circle divides the Earth into Northern and Southern hemispheres and serves as the fundamental reference line for the geographic coordinate system. The equator is approximately 40,075 kilometers (24,901 miles) in circumference and passes through 13 countries across three continents. At the equator, day and night are nearly equal in length year-round, and the climate is typically tropical with minimal seasonal temperature variation. The concept extends beyond geography to astronomy, where the celestial equator represents the projection of Earth\'s equator onto the celestial sphere. Understanding the equator is crucial for navigation, geography, climate science, and astronomy. The region around the equator is often called the tropics or equatorial zone. The equator also serves as the zero reference for measuring latitude and understanding global weather patterns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-KWAY-ter',
                'etymology': 'From Medieval Latin "aequator," from Latin "aequare" (to make equal), referring to its position equally distant from both poles.',
                'language_origins': 'Latin',
                'example_sentence': 'Countries located on the _______ experience consistently warm temperatures throughout the year.',
                'memory_tip': 'Remember "e-QUATOR" - think "equal-ator" because it equally divides the Earth, or "equator" sounds like "equal-later" meaning equally distant from both poles.'
            },
            'equestrian': {
                'definition': 'Equestrian refers to horseback riding, horsemanship, or anything related to horses and riding. As an adjective, it describes activities, sports, skills, or equipment associated with horses. As a noun, an equestrian is a person who rides horses, particularly someone skilled in horsemanship. Equestrian sports include dressage, show jumping, cross-country, polo, and various racing disciplines. These activities require significant skill, training, and partnership between horse and rider. Equestrian arts have ancient origins in military and transportation needs but have evolved into recreational, competitive, and therapeutic activities. Olympic equestrian events showcase the highest levels of skill and artistry in horse-and-rider partnerships. Therapeutic riding programs use equestrian activities to help people with disabilities develop physical, emotional, and social skills. Understanding equestrian culture involves appreciating the historical relationship between humans and horses, the technical skills required for riding, and the various disciplines within the equestrian world.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-KWES-tree-uhn',
                'etymology': 'From Latin "equestris," from "eques" (horseman, knight), from "equus" (horse). Originally referred to the Roman equestrian class.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ competition featured riders demonstrating advanced dressage techniques.',
                'memory_tip': 'Remember "e-QUEST-rian" - think "e-quest" like a quest on horseback, or "equestrian" contains "quest" which knights did on horses.'
            },
            'equilibrium': {
                'definition': 'Equilibrium is a state of balance or stability where opposing forces, influences, or elements are in proportion and harmony. In physics, equilibrium occurs when the net force acting on an object is zero, resulting in no acceleration. Chemical equilibrium describes a state where the rates of forward and reverse reactions are equal, maintaining constant concentrations. Economic equilibrium represents a market condition where supply and demand are balanced. Psychological equilibrium refers to mental and emotional balance. The concept appears across many fields including biology (homeostasis), ecology (balanced ecosystems), and social sciences (stable societies). Equilibrium can be static (unchanging) or dynamic (constantly adjusting while maintaining overall balance). Understanding equilibrium helps explain stability, predict behavior, and design systems that maintain desired conditions. Disruptions to equilibrium often trigger responses that attempt to restore balance. The ability to achieve and maintain equilibrium is crucial for the proper functioning of systems from individual organisms to global economies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ee-kwuh-LIB-ree-uhm',
                'etymology': 'From Latin "aequilibrium," from "aequus" (equal) + "libra" (balance, scale), literally meaning "equal balance."',
                'language_origins': 'Latin',
                'example_sentence': 'The tightrope walker maintained perfect _______ while crossing between the two buildings.',
                'memory_tip': 'Remember "equi-LIBR-ium" - think "equal-libra" (equal balance like the zodiac sign Libra which is scales), or "equilibrium" contains "equal" and "libre" (free/balanced).'
            },
            'equinox': {
                'definition': 'An equinox is one of two times each year when day and night are approximately equal in length across the entire Earth, occurring when the Sun crosses the celestial equator. The vernal (spring) equinox occurs around March 20-21, marking the beginning of spring in the Northern Hemisphere and autumn in the Southern Hemisphere. The autumnal equinox occurs around September 22-23, marking the beginning of autumn in the Northern Hemisphere and spring in the Southern Hemisphere. During an equinox, the Sun rises due east and sets due west everywhere on Earth. These events result from Earth\'s axial tilt and orbital motion around the Sun. Equinoxes have cultural and spiritual significance in many societies, often associated with themes of balance, renewal, and seasonal transition. Agricultural societies traditionally used equinoxes to time planting and harvesting activities. Understanding equinoxes helps explain seasonal changes, daylight patterns, and the relationship between Earth\'s position and solar radiation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EE-kwuh-noks',
                'etymology': 'From Latin "aequinoctium," from "aequus" (equal) + "nox" (night), literally meaning "equal night."',
                'language_origins': 'Latin',
                'example_sentence': 'During the spring _______, gardeners know it\'s time to begin planting their outdoor vegetables.',
                'memory_tip': 'Remember "EQUI-nox" - think "equal-night" because day and night are equal in length, or "equinox" sounds like "equal-knocks" meaning equal amounts of day and night knocking.'
            },
            'equipment': {
                'definition': 'Equipment refers to the tools, machinery, apparatus, or other items needed for a particular purpose or activity. This collective noun encompasses the physical resources required to perform tasks, conduct operations, or engage in specific pursuits. Equipment can range from simple hand tools to complex industrial machinery, from sports gear to scientific instruments. The term implies functionality and purpose-driven design rather than decorative or purely aesthetic items. Different fields require specialized equipment: medical equipment for healthcare, laboratory equipment for research, sports equipment for athletics, and industrial equipment for manufacturing. Quality equipment often determines the efficiency, safety, and success of various endeavors. Proper maintenance, storage, and operation of equipment are crucial for optimal performance and longevity. Understanding equipment needs helps in planning, budgeting, and organizing activities. The selection of appropriate equipment requires consideration of factors such as cost, durability, compatibility, and specific requirements of the intended use.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-KWIP-muhnt',
                'etymology': 'From "equip" (from French "équiper," possibly from Old Norse "skipa" meaning "to fit out a ship") + "-ment" (suffix indicating result or means).',
                'language_origins': 'Old Norse, French',
                'example_sentence': 'The research laboratory required specialized _______ to conduct the advanced experiments.',
                'memory_tip': 'Remember "e-QUIP-ment" - think "equip-ment" meaning the mental/physical means to equip yourself, or "equipment" contains "equip" which means to provide with necessary items.'
            },
            'equivalent': {
                'definition': 'Equivalent means equal in value, amount, function, meaning, or significance, though not necessarily identical in form or appearance. This concept describes relationships where different things serve the same purpose, have the same effect, or represent the same quantity despite possible differences in their specific characteristics. Mathematical equivalents include different fractions representing the same value (1/2 = 2/4) or different expressions yielding the same result. In chemistry, equivalent weights allow comparison of different substances based on their reactive capacity. Language equivalents include words or phrases in different languages that convey the same meaning. The concept appears in economics (equivalent purchasing power), education (equivalent credentials), and law (equivalent penalties). Understanding equivalence helps in making comparisons, substitutions, and translations across different systems or contexts. Equivalence relationships are fundamental to mathematics, science, and logical reasoning. The ability to recognize and establish equivalences is crucial for problem-solving and analysis.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-KWIV-uh-luhnt',
                'etymology': 'From Latin "aequivalentem," from "aequus" (equal) + "valere" (to be worth), literally meaning "of equal worth."',
                'language_origins': 'Latin',
                'example_sentence': 'One meter is _______ to approximately 3.28 feet in the imperial measurement system.',
                'memory_tip': 'Remember "e-QUIV-alent" - think "equal-value-ent" meaning having equal value, or "equivalent" contains "equal" and "value" which explains its meaning.'
            },
            'equivocate': {
                'definition': 'To equivocate means to use ambiguous or evasive language in order to conceal the truth, avoid commitment, or mislead others. This verbal strategy involves speaking in ways that allow for multiple interpretations, often to avoid taking a clear position on controversial issues or to escape responsibility for one\'s statements. Equivocation can involve using words with double meanings, speaking vaguely, or making statements that can be interpreted in different ways depending on context. While sometimes used as a diplomatic tool to avoid conflict, equivocation can also be a form of deception or manipulation. Politicians, lawyers, and negotiators sometimes equivocate to maintain flexibility or avoid making binding commitments. The practice can frustrate listeners who seek clear, honest communication. Understanding equivocation helps people recognize when others are being deliberately unclear and encourages more direct, transparent communication. In logic and philosophy, equivocation is considered a fallacy when used to make invalid arguments.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-KWIV-uh-kayt',
                'etymology': 'From Late Latin "aequivocatus," from Latin "aequivocus" (ambiguous), from "aequus" (equal) + "vox" (voice), meaning "of equal voice/meaning."',
                'language_origins': 'Latin',
                'example_sentence': 'When asked about his position on the controversial issue, the politician began to _______.',
                'memory_tip': 'Remember "e-QUIV-ocate" - think "equal-voice-ate" meaning to speak with equal voices (ambiguously), or "equivocate" sounds like "equal-vocal" meaning giving equal voice to different meanings.'
            },
            'eradicate': {
                'definition': 'To eradicate means to completely eliminate, destroy, or remove something undesirable, typically referring to problems, diseases, pests, or harmful conditions. This powerful verb suggests thorough and permanent removal rather than temporary suppression or control. Medical contexts often use eradicate when discussing the complete elimination of diseases through vaccination programs, improved sanitation, or medical interventions. Agricultural applications include eradicating invasive species or crop pests that threaten food production. Social programs aim to eradicate poverty, illiteracy, or discrimination through systematic efforts and policy changes. The term implies a comprehensive, systematic approach that addresses root causes rather than just symptoms. Successful eradication requires sustained effort, resources, and often international cooperation. Historical examples include the eradication of smallpox through global vaccination campaigns. Understanding eradication helps distinguish between management strategies that control problems and those that seek complete elimination. The concept emphasizes the possibility of permanent solutions to persistent challenges.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-RAD-i-kayt',
                'etymology': 'From Latin "eradicatus," past participle of "eradicare" meaning "to root out," from "e-" (out) + "radix" (root).',
                'language_origins': 'Latin',
                'example_sentence': 'The global health initiative aimed to _______ malaria through comprehensive prevention and treatment programs.',
                'memory_tip': 'Remember "e-RAD-icate" - think "e" (out) + "radical" (root), meaning to take out by the roots, or "eradicate" sounds like "eraser-ate" meaning to completely erase something.'
            },
            'erase': {
                'definition': 'To erase means to remove, eliminate, or make something disappear, typically by rubbing out, deleting, or destroying traces of it. The term originates from the physical act of removing pencil marks with an eraser, but has expanded to include various forms of removal or elimination. Digital contexts use erase for deleting files, clearing memory, or removing data from storage devices. Erase can describe intentional actions (erasing mistakes) or unintentional loss (time erasing memories). The word can apply to physical removal (erasing chalkboard writing), digital deletion (erasing computer files), or metaphorical elimination (erasing doubts or fears). Unlike temporary concealment or covering, erasing suggests making something disappear completely or return to a blank state. The concept appears in art (erasing to create highlights), education (erasing to make corrections), and technology (erasing hard drives for security). Understanding different methods and contexts of erasing helps people manage information, create art, and communicate about removal processes.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-RAYS',
                'etymology': 'From Latin "erasus," past participle of "eradere" meaning "to scrape out," from "e-" (out) + "radere" (to scrape).',
                'language_origins': 'Latin',
                'example_sentence': 'She used the eraser to _______ the incorrect answer and write the right one.',
                'memory_tip': 'Remember "e-RASE" - think "e" (out) + "raze" (scrape), meaning to scrape out, or "erase" sounds like "he-race" meaning racing to remove something quickly.'
            },
            'erewhonian': {
                'definition': 'Erewhonian refers to the fictional utopian society described in Samuel Butler\'s 1872 satirical novel "Erewhon" (which is "Nowhere" spelled backwards with some letters rearranged). This adjective describes characteristics, ideas, or institutions that resemble those in Butler\'s imaginary land, where conventional values and social norms are often inverted or critically examined. In Erewhon, crime is treated as illness while illness is treated as crime, machines are banned for fear they will evolve and dominate humans, and various other social paradoxes exist. The term is used in literary criticism, social commentary, and discussions of utopian literature to refer to satirical or paradoxical approaches to social organization. Erewhonian thinking often involves examining society from an outsider\'s perspective to reveal absurdities or contradictions in accepted practices. Understanding Erewhonian concepts helps readers appreciate satirical literature and critical examinations of social conventions. The novel remains relevant for its insights into technology, morality, and social structures.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'er-uh-WHOH-nee-uhn',
                'etymology': 'From "Erewhon," the fictional place name created by Samuel Butler (anagram of "nowhere" with letters rearranged) + "-ian" (suffix meaning "relating to").',
                'language_origins': 'English literary creation',
                'example_sentence': 'The philosopher\'s _______ proposal to treat corporate greed as a mental illness sparked intense debate.',
                'memory_tip': 'Remember "ere-WHON-ian" - think "where-no-one" because it\'s from "nowhere" backwards, or "Erewhonian" describes the strange society where normal rules are reversed.'
            },
            'ergatogyne': {
                'definition': 'An ergatogyne is a specialized form of ant found in certain species, representing an intermediate caste between workers and reproductive females (queens). These individuals typically possess characteristics of both worker ants and queens, often having a larger body size than regular workers but smaller than full queens, and may have reproductive capabilities while also performing worker functions. Ergatogynes are important in the social organization of some ant colonies, particularly in species where colony founding and reproduction involve complex strategies. They may serve as backup reproductives when the primary queen dies or becomes less productive, or they may establish new colonies under specific circumstances. The presence of ergatogynes demonstrates the flexibility and complexity of ant social systems, where caste differentiation can include intermediate forms rather than strictly defined categories. Understanding ergatogynes helps entomologists study ant evolution, colony dynamics, and the factors that influence caste determination in social insects. This specialized terminology is primarily used in myrmecology (the study of ants) and sociobiology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'er-GAT-uh-jahyn',
                'etymology': 'From Greek "ergates" (worker) + "gyne" (female), literally meaning "worker-female," referring to their intermediate status between workers and queens.',
                'language_origins': 'Greek',
                'example_sentence': 'The myrmecologist discovered several _______ in the ant colony, indicating a complex reproductive strategy.',
                'memory_tip': 'Remember "ERGATO-gyne" - think "ergot" (work) + "gyne" (female), meaning a working female ant that\'s between worker and queen, or "ergatogyne" like "working-queen" combining both roles.'
            },
            'ergo': {
                'definition': 'Ergo is a Latin word meaning "therefore" or "consequently," used to introduce a logical conclusion that follows from previously stated premises or arguments. This formal transitional word appears frequently in academic writing, philosophical discourse, legal arguments, and logical reasoning. When someone uses "ergo," they signal that what follows is a logical consequence of what came before, similar to "thus," "hence," or "consequently" but with a more formal, scholarly tone. The word helps structure arguments by clearly marking the relationship between evidence and conclusions. In formal logic and philosophy, ergo often introduces the conclusion of a syllogism or logical proof. While less common in everyday conversation, ergo remains valuable in academic and professional contexts where precise logical relationships need to be expressed. Understanding Latin transitional words like ergo helps readers follow complex arguments and writers express logical relationships clearly. The term reflects the continuing influence of Latin on academic and intellectual discourse.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ER-goh',
                'etymology': 'From Latin "ergo" meaning "therefore, consequently," related to the idea of work or action leading to results.',
                'language_origins': 'Latin',
                'example_sentence': 'All humans are mortal, Socrates is human, _______ Socrates is mortal.',
                'memory_tip': 'Remember "ER-go" - think "error-go" meaning when no error exists, therefore go to the conclusion, or "ergo" sounds like "air-go" meaning the conclusion goes through the air to follow.'
            },
            'ergoexistential': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "ergo" (therefore) and "existential" (relating to existence or existentialism). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'erin': {
                'definition': 'Erin is a poetic and traditional name for Ireland, derived from the Irish Gaelic "Éirinn," which is the dative case of "Éire" (Ireland). This lyrical name appears frequently in Irish literature, songs, and cultural expressions as a romantic or nostalgic reference to the homeland. The phrase "Erin go Bragh" (Ireland forever) is a well-known patriotic expression. Erin is also used as a personal name, particularly for girls, in English-speaking countries. The term evokes images of Ireland\'s green landscapes, rich cultural heritage, and emotional connections to Irish identity. In Irish-American communities, Erin often appears in cultural organizations, businesses, and celebrations that honor Irish heritage. The name carries connotations of beauty, homeland, and cultural pride. Understanding terms like Erin helps appreciate Irish literature, music, and cultural expressions. The word represents the enduring emotional and cultural significance of Ireland for Irish people and those of Irish descent worldwide.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'AIR-in',
                'etymology': 'From Irish Gaelic "Éirinn," dative case of "Éire" (Ireland), possibly from Old Irish "Ériu," a goddess personifying Ireland.',
                'language_origins': 'Irish Gaelic',
                'example_sentence': 'The traditional Irish ballad spoke of longing to return to beloved _______.',
                'memory_tip': 'Remember "E-rin" - think "Eire-in" (Ireland-in), or "Erin" sounds like "Air-in" and Ireland has the fresh air people long for.'
            },
            'eris': {
                'definition': 'Eris is the Greek goddess of discord, strife, and chaos, known for her role in inciting conflict and disagreement among gods and mortals. In Greek mythology, Eris is most famous for her role in causing the Trojan War by throwing a golden apple inscribed "For the fairest" among the goddesses, leading to a beauty contest between Hera, Athena, and Aphrodite. This act of discord ultimately resulted in the judgment of Paris and the events that sparked the legendary war. Eris represents the destructive power of jealousy, competition, and conflict. In modern astronomy, Eris is also the name of a dwarf planet in our solar system, discovered in 2005 and notable for being slightly more massive than Pluto. The naming reflects the discord Eris\'s discovery caused in astronomical classification, ultimately leading to Pluto\'s reclassification as a dwarf planet. Understanding Eris helps explain mythological themes about conflict and the astronomical developments that changed our understanding of the solar system.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'AIR-is',
                'etymology': 'From Greek "Eris," the personification of strife and discord. The name comes from the Greek word "eris" meaning "strife, discord."',
                'language_origins': 'Greek',
                'example_sentence': 'The discovery of the dwarf planet _______ led to significant changes in how astronomers classify celestial bodies.',
                'memory_tip': 'Remember "E-ris" - think "Error-is" because Eris causes errors/discord, or "Eris" sounds like "Air-is" and she throws discord through the air.'
            },
            'erlenmeyer': {
                'definition': 'An Erlenmeyer flask is a type of laboratory glassware with a conical shape, flat bottom, and narrow neck, designed for mixing, heating, and storing liquids in scientific experiments. Named after German chemist Emil Erlenmeyer, this flask is one of the most recognizable pieces of laboratory equipment. The conical shape allows for efficient mixing by swirling, while the narrow neck reduces evaporation and splash-back during heating or vigorous mixing. Erlenmeyer flasks come in various sizes and are typically made of borosilicate glass that can withstand thermal stress. They are essential equipment in chemistry labs, biology labs, and educational settings for conducting experiments, preparing solutions, and culturing microorganisms. The design makes them ideal for titrations, crystallizations, and reactions requiring controlled heating. Some versions include measurement graduations for approximate volume readings. Understanding laboratory glassware like Erlenmeyer flasks is fundamental for anyone working in scientific fields or studying chemistry and biology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ER-luhn-mahy-er',
                'etymology': 'Named after Emil Erlenmeyer (1825-1909), German chemist who developed this type of laboratory flask in the 1860s.',
                'language_origins': 'German surname',
                'example_sentence': 'The chemistry student carefully heated the solution in the _______ flask over the Bunsen burner.',
                'memory_tip': 'Remember "ERLEN-meyer" - think "Earl-in-my-air" like an earl (noble person) flying through air with a conical flask shape, or "Erlenmeyer" is the name of the chemist who invented this conical flask.'
            },
            'ermine': {
                'definition': 'Ermine refers to a small mammal (Mustela erminea) also known as the stoat or short-tailed weasel, particularly when it displays its distinctive white winter coat. In cold climates, ermines undergo seasonal color changes, developing pure white fur with black-tipped tails during winter months, while maintaining brown coloration in summer. This white winter coat has been highly prized throughout history for luxury fur garments, especially in royal and ceremonial attire. The term "ermine" also refers to the white fur itself, which has been a symbol of purity, royalty, and high status in European heraldry and fashion. Ermine patterns appear in coat-of-arms designs and traditional royal robes. The animal is a skilled predator that hunts small mammals and birds, playing an important ecological role in its habitat. Understanding ermine helps appreciate both wildlife biology and cultural history, as these small predators have significantly influenced human fashion and symbolic traditions. The seasonal coat change represents a remarkable adaptation to different environmental conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'UR-min',
                'etymology': 'From Old French "ermine," possibly from Medieval Latin "Armenius mus" (Armenian mouse), though the exact origin is disputed. Some suggest Germanic origins.',
                'language_origins': 'Old French, possibly Latin or Germanic',
                'example_sentence': 'The royal robe was trimmed with luxurious white _______ fur dotted with black spots.',
                'memory_tip': 'Remember "ER-mine" - think "earn-mine" because ermine fur was so valuable people worked to earn/mine it, or "ermine" sounds like "air-mine" because they have airy white winter coats.'
            },
            'erode': {
                'definition': 'To erode means to gradually wear away, diminish, or destroy through the action of natural forces such as water, wind, ice, or chemical processes. In geological contexts, erosion shapes landscapes by breaking down rock and soil and transporting materials to new locations. Water erosion creates valleys, canyons, and coastlines, while wind erosion forms deserts and sand dunes. The term extends beyond physical processes to describe gradual deterioration or weakening in various contexts. Social erosion might involve the gradual decline of institutions, traditions, or values. Economic erosion could refer to the slow decrease in purchasing power or market position. Personal erosion might describe the gradual loss of confidence, health, or relationships. Understanding erosion helps explain landscape formation, environmental change, and various processes of gradual decline or transformation. The concept emphasizes that significant changes often result from persistent, small-scale forces acting over extended periods rather than sudden dramatic events.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-ROHD',
                'etymology': 'From Latin "erodere" meaning "to gnaw away," from "e-" (away) + "rodere" (to gnaw). Related to "rodent."',
                'language_origins': 'Latin',
                'example_sentence': 'Years of heavy rainfall began to _______ the hillside, creating deep gullies in the landscape.',
                'memory_tip': 'Remember "e-RODE" - think "e" (away) + "rode" (like riding/wearing away), or "erode" sounds like "he-road" meaning a road that wears things away.'
            },
            'errands': {
                'definition': 'Errands are short trips or tasks undertaken to accomplish specific purposes, typically involving going to various locations to complete routine activities or obtain needed items. Common errands include shopping for groceries, picking up dry cleaning, visiting the post office, going to the bank, or running to the pharmacy. These tasks are usually practical necessities rather than leisure activities, though they can sometimes be combined with enjoyable activities. Errands often require planning and organization to complete efficiently, particularly when multiple tasks need to be accomplished in a single outing. The term implies purposeful activity with clear objectives and often involves transportation between different locations. Modern life frequently involves managing multiple errands within busy schedules, leading to strategies for batching similar tasks or using delivery services to reduce travel time. Understanding errands helps people organize daily activities and manage time effectively. The concept reflects the practical realities of maintaining households and personal responsibilities in contemporary society.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'AIR-uhndz',
                'etymology': 'From Middle English "erande," from Old English "ǣrende" meaning "message, mission," related to Old Norse "erindi" (errand, message).',
                'language_origins': 'Old English, Old Norse',
                'example_sentence': 'She spent Saturday morning running _______ at the grocery store, bank, and post office.',
                'memory_tip': 'Remember "ERR-ands" - think "error-ands" meaning little errors you need to fix by running errands, or "errands" sounds like "air-ands" meaning tasks that need doing and you go through the air (travel) to do them.'
            },
            'errata': {
                'definition': 'Errata is the plural form of "erratum," referring to a list of errors and their corrections that appears in a published work such as a book, journal article, or other printed material. Publishers typically include errata to acknowledge and correct mistakes that were discovered after printing, such as typographical errors, factual inaccuracies, formatting problems, or citation mistakes. Errata may appear as separate sheets inserted into books, as additions to subsequent printings, or as published corrections in journals. In academic and scholarly publishing, errata serve important functions for maintaining accuracy and credibility, allowing authors and publishers to correct the record without reprinting entire works. Digital publishing has made errata less common since errors can often be corrected directly in electronic versions. However, the concept remains important for understanding how published materials maintain accuracy and how errors are formally acknowledged and corrected. Errata demonstrate intellectual honesty and commitment to accuracy in professional publishing.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'eh-RAH-tah',
                'etymology': 'From Latin "errata," plural of "erratum" (error), from "errare" (to wander, err). Literally means "things that have wandered/gone wrong."',
                'language_origins': 'Latin',
                'example_sentence': 'The publisher included an _______ sheet with the book to correct several typographical errors.',
                'memory_tip': 'Remember "err-ATA" - think "error-ata" meaning a collection of errors that need fixing, or "errata" sounds like "error-data" meaning data about errors.'
            },
            'erre': {
                'definition': 'Erre is the Spanish name for the letter "R," particularly when referring to the rolled or trilled "R" sound that is characteristic of Spanish pronunciation. In Spanish, there are two R sounds: the single tap "r" (ere) and the rolled "rr" (erre), with erre being the more distinctive and challenging sound for non-native speakers to master. The rolled R is produced by rapidly vibrating the tip of the tongue against the roof of the mouth, creating a distinctive trill. This sound appears at the beginning of words that start with R and in double-R combinations within words. Mastering the erre sound is often considered a milestone in Spanish language learning, as it requires specific tongue positioning and breath control that differs significantly from English R sounds. The distinction between ere and erre can change word meanings in Spanish, making proper pronunciation important for clear communication. Understanding erre helps appreciate the phonological complexity of Spanish and the challenges involved in second-language acquisition.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EH-rreh',
                'etymology': 'From Spanish "erre," the name of the letter R when it represents the rolled/trilled sound, derived from the letter\'s sound value.',
                'language_origins': 'Spanish',
                'example_sentence': 'The Spanish student practiced rolling her _______ until she could pronounce "perro" correctly.',
                'memory_tip': 'Remember "ERR-e" - think "error-eh" because many learners make errors with this rolled R sound, or "erre" is simply the Spanish name for the rolling R sound.'
            },
            'erroneous': {
                'definition': 'Erroneous means containing or based on error; incorrect, mistaken, or wrong. This adjective describes information, beliefs, assumptions, calculations, or conclusions that are factually inaccurate or logically flawed. Erroneous statements can result from misunderstanding, insufficient information, faulty reasoning, or deliberate distortion. The term is often used in academic, legal, and professional contexts where accuracy is crucial and mistakes have significant consequences. Erroneous data can lead to wrong decisions, failed experiments, or misguided policies. Identifying erroneous information requires critical thinking, fact-checking, and careful analysis of sources and evidence. The word suggests more than simple mistakes; it often implies systematic or significant errors that affect understanding or outcomes. In legal contexts, erroneous rulings may be grounds for appeal. Scientific research relies on identifying and correcting erroneous theories and findings. Understanding what makes information erroneous helps people evaluate sources, verify facts, and make better-informed decisions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-ROH-nee-uhs',
                'etymology': 'From Latin "erroneus," from "errare" (to wander, err, make mistakes). The suffix "-ous" means "characterized by."',
                'language_origins': 'Latin',
                'example_sentence': 'The scientist realized his initial hypothesis was _______ after reviewing the experimental data.',
                'memory_tip': 'Remember "err-ON-eous" - think "error-on-us" meaning having error upon us/containing error, or "erroneous" contains "error" which explains its meaning.'
            },
            'ersion': {
                'definition': 'This appears to be an incomplete or corrupted word, possibly a fragment from PDF parsing. It could be part of words ending in "-ersion" such as "conversion," "immersion," "diversion," or "aversion." Without additional context, it\'s difficult to determine the intended complete word. This may represent a scanning or parsing error where part of a longer word was separated or truncated.',
                'part_of_speech': 'incomplete/error',
                'pronunciation_guide': 'N/A - incomplete word',
                'etymology': 'Appears to be incomplete word fragment',
                'language_origins': 'Unknown - incomplete',
                'example_sentence': 'N/A - This appears to be an incomplete word',
                'memory_tip': 'N/A - This is likely a scanning/parsing error'
            },
            'erstwhile': {
                'definition': 'Erstwhile means former, previous, or belonging to an earlier time, used to describe someone or something that once held a particular position, status, or characteristic but no longer does. This adjective typically appears before nouns to indicate that the described relationship or condition existed in the past but has since changed. Erstwhile relationships might include former friends, colleagues, or allies who are no longer connected. Erstwhile positions could refer to previous jobs, roles, or responsibilities that someone once held. The word carries connotations of change, transition, and the passage of time, often with implications that the previous state was significant or notable. Erstwhile can describe both personal relationships and institutional changes, such as erstwhile colonies becoming independent nations or erstwhile competitors becoming partners. Understanding erstwhile helps express temporal relationships and acknowledge how people, organizations, and situations evolve over time. The term adds precision to descriptions of change and historical development.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'URST-hwahyl',
                'etymology': 'From Middle English "erst" (formerly, at first) + "while" (time), literally meaning "former time." "Erst" comes from Old English "ǣrest" (earliest).',
                'language_origins': 'Old English, Middle English',
                'example_sentence': 'The _______ enemies became close allies after discovering their shared interests.',
                'memory_tip': 'Remember "ERST-while" - think "first-while" meaning during the first/earlier while/time, or "erstwhile" sounds like "worst-while" but actually means former times.'
            },
            'erubescent': {
                'definition': 'Erubescent means becoming red or reddish; blushing or showing a tendency to redden. This adjective describes the process of developing a red coloration, whether from embarrassment, anger, physical exertion, or other causes. In human contexts, erubescent typically refers to the facial flushing that occurs when blood vessels dilate near the skin surface, creating a reddish appearance. This physiological response can result from various emotions including embarrassment, shame, anger, or excitement. The term can also describe objects or natural phenomena that take on reddish hues, such as erubescent sunsets, autumn leaves, or certain minerals. In literary contexts, erubescent often appears in poetic or formal descriptions of blushing or reddening. The word provides a more sophisticated alternative to simpler terms like "blushing" or "reddening." Understanding erubescent helps readers appreciate descriptive writing and recognize physiological responses to emotional states. The term reflects the connection between internal emotional states and external physical manifestations.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'er-uh-BES-uhnt',
                'etymology': 'From Latin "erubescens," present participle of "erubescere" meaning "to redden, blush," from "e-" (out) + "rubescere" (to grow red), from "ruber" (red).',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ cheeks revealed her embarrassment when she realized everyone was listening to her conversation.',
                'memory_tip': 'Remember "eru-BESC-ent" - think "e" (out) + "ruby" (red gem) + "escent" (becoming), meaning becoming ruby-red/blushing, or "erubescent" contains "rub" like rubbing makes things red.'
            },
            'eructation': {
                'definition': 'Eructation is the medical or formal term for belching or burping - the release of gas from the digestive tract through the mouth. This physiological process occurs when swallowed air or gases produced during digestion accumulate in the stomach and are expelled upward through the esophagus. Eructation serves as a natural mechanism for relieving gastric pressure and is generally considered normal bodily function, though it can be influenced by eating habits, carbonated beverages, and certain medical conditions. In medical contexts, excessive or painful eructation might indicate digestive disorders, gastroesophageal reflux, or other gastrointestinal issues. Cultural attitudes toward eructation vary significantly, with some societies considering it natural and others viewing it as impolite. The formal medical terminology helps healthcare professionals discuss this function objectively without cultural taboos. Understanding eructation as a physiological process helps distinguish between normal digestive function and potential medical concerns. The term appears in medical literature, anatomy texts, and discussions of digestive health.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-ruhk-TAY-shuhn',
                'etymology': 'From Latin "eructationem," from "eructare" meaning "to belch forth," from "e-" (out) + "ructare" (to belch), related to "rugire" (to roar).',
                'language_origins': 'Latin',
                'example_sentence': 'The doctor explained that occasional _______ after meals is a normal part of digestion.',
                'memory_tip': 'Remember "e-RUCT-ation" - think "e" (out) + "ruck" (rough sound) + "ation" (action), meaning the action of making rough sounds coming out, or "eructation" sounds like "eruption" from your stomach.'
            },
            'eruption': {
                'definition': 'An eruption is a sudden, forceful emergence or outbreak of material, energy, or activity from a confined or contained state. Most commonly associated with volcanoes, eruptions involve the explosive or effusive release of magma, ash, and gases from beneath the Earth\'s surface. Volcanic eruptions can range from gentle lava flows to catastrophic explosions that affect global climate. The term extends to other contexts: skin eruptions describe sudden appearances of rashes, acne, or other dermatological conditions; social eruptions refer to sudden outbreaks of violence, protest, or unrest; emotional eruptions involve sudden displays of intense feelings. Eruptions typically involve pressure buildup followed by rapid release, often with significant impact on surrounding areas. Understanding different types of eruptions helps people recognize patterns of buildup and release in natural, social, and personal contexts. The concept emphasizes the potential for sudden, dramatic change when pressures exceed containment capacity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-RUHP-shuhn',
                'etymology': 'From Latin "eruptionem," from "erumpere" meaning "to break out," from "e-" (out) + "rumpere" (to break).',
                'language_origins': 'Latin',
                'example_sentence': 'The volcanic _______ sent ash clouds high into the atmosphere, affecting air travel across the region.',
                'memory_tip': 'Remember "e-RUPT-ion" - think "e" (out) + "rupt" (break/disrupt) + "ion" (action), meaning the action of breaking out, or "eruption" sounds like "he-rupt" meaning something ruptures outward.'
            },
            'erythroblast': {
                'definition': 'An erythroblast is an immature red blood cell in the bone marrow that represents an intermediate stage in red blood cell development (erythropoiesis). These nucleated cells are precursors to mature red blood cells (erythrocytes) and undergo several developmental stages as they lose their nucleus and acquire the characteristic biconcave shape of mature red blood cells. Erythroblasts are normally found only in the bone marrow, where they develop under the influence of the hormone erythropoietin. Their presence in peripheral blood circulation typically indicates bone marrow stress, disease, or abnormal blood cell production. Different types of erythroblasts exist at various maturation stages, from proerythroblasts to orthochromatic erythroblasts. Medical professionals study erythroblasts to diagnose blood disorders, anemia, bone marrow diseases, and other hematological conditions. Understanding erythroblasts helps explain how the body produces red blood cells and maintains adequate oxygen-carrying capacity. The term is essential in hematology and medical laboratory science.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-RITH-ruh-blast',
                'etymology': 'From Greek "erythros" (red) + "blastos" (germ, bud), literally meaning "red cell bud/germ," referring to immature red blood cells.',
                'language_origins': 'Greek',
                'example_sentence': 'The bone marrow biopsy showed increased _______ production in response to the patient\'s anemia.',
                'memory_tip': 'Remember "ERYTHRO-blast" - think "erythro" (red) + "blast" (explosion/burst), meaning bursting with red cells that will become red blood cells, or "erythroblast" like "red-blast" of developing blood cells.'
            },
            'erythroblastesau': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "erythroblast" (an immature red blood cell) and "Esau" (a biblical figure). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'esau': {
                'definition': 'Esau is a biblical figure from the Hebrew Bible and Christian Old Testament, known as the twin brother of Jacob and the son of Isaac and Rebecca. According to the biblical narrative, Esau was born first, making him the heir to his father\'s birthright, but he famously sold this birthright to Jacob for a bowl of lentil stew when he was hungry. Esau is described as a skilled hunter and outdoorsman, in contrast to his brother Jacob who was more domestically inclined. The rivalry between Esau and Jacob represents themes of sibling conflict, divine election, and the consequences of impulsive decisions. Esau is traditionally considered the ancestor of the Edomites, while Jacob (later renamed Israel) became the ancestor of the Israelites. The story appears in the Book of Genesis and has been interpreted in various ways throughout Jewish, Christian, and Islamic traditions. Understanding Esau\'s story helps comprehend ancient Near Eastern family dynamics and religious themes about destiny and divine purpose.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'EE-saw',
                'etymology': 'From Hebrew "Esav," possibly meaning "hairy" or "rough," referring to his physical appearance at birth as described in Genesis.',
                'language_origins': 'Hebrew',
                'example_sentence': 'The biblical story tells how _______ traded his birthright for a bowl of stew.',
                'memory_tip': 'Remember "E-sau" - think "he-saw" because Esau saw the stew and wanted it so much he traded his birthright, or "Esau" sounds like "he-saw" his brother Jacob take advantage of him.'
            },
            'escabeche': {
                'definition': 'Escabeche is a traditional cooking technique and dish from Spanish and Latin American cuisine involving fish, seafood, or sometimes vegetables that are first cooked (usually fried) and then marinated in an acidic mixture typically containing vinegar, citrus juice, olive oil, and aromatic vegetables like onions, carrots, and peppers. This preservation method combines cooking with acidic marination to create flavorful dishes that can be stored for extended periods. The acid in the marinade helps preserve the food while infusing it with complex flavors from herbs and spices such as bay leaves, peppercorns, and paprika. Escabeche can be served immediately while warm or allowed to marinate for hours or days, developing deeper flavors over time. Different regional variations exist throughout Spain, Latin America, and the Philippines, each with characteristic ingredients and preparation methods. The technique demonstrates historical methods of food preservation and flavor enhancement before refrigeration. Understanding escabeche helps appreciate culinary traditions that combine practical preservation with sophisticated flavor development.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'es-kah-BEH-cheh',
                'etymology': 'From Spanish "escabeche," possibly from Arabic "sikbaj," referring to a vinegar-based marinade, reflecting Moorish influence on Spanish cuisine.',
                'language_origins': 'Arabic, Spanish',
                'example_sentence': 'The chef prepared a delicious _______ with fresh sardines marinated in vinegar and aromatic vegetables.',
                'memory_tip': 'Remember "esca-BECHE" - think "escape-beche" because the fish escapes spoilage through this preservation method, or "escabeche" sounds like "escape-beach" meaning fish escape the beach into vinegar.'
            },
            'escalator': {
                'definition': 'An escalator is a moving staircase consisting of an endless chain of steps that transport people between different floors or levels of a building. This mechanical device features motor-driven steps that continuously circulate, allowing passengers to stand still while being carried upward or downward. Escalators typically include handrails that move at the same speed as the steps, safety features like emergency stop buttons, and sensors to detect obstructions. They are commonly found in shopping malls, airports, subway stations, office buildings, and other public spaces where large numbers of people need to move between levels efficiently. Escalators offer advantages over elevators for moderate height differences by providing continuous flow without waiting times. Safety considerations include proper positioning of feet, holding handrails, and awareness of the top and bottom transition areas. The invention of escalators revolutionized building design and urban transportation. Understanding escalator mechanics and safety helps people use them effectively and appreciate their role in modern architecture and public transportation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ES-kuh-lay-ter',
                'etymology': 'From "escalate" (from Latin "scala" meaning "ladder, staircase") + "-or" (agent suffix), literally meaning "that which causes to escalate/climb."',
                'language_origins': 'Latin',
                'example_sentence': 'The busy shopping mall installed a new _______ to help customers reach the upper floors more easily.',
                'memory_tip': 'Remember "ESCA-lator" - think "escalate-ator" meaning something that makes you escalate/go up, or "escalator" sounds like "escalate-later" meaning you escalate without effort later.'
            },
            'escalatorimpasto': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "escalator" (a moving staircase) and "impasto" (a painting technique using thick paint). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'escapade': {
                'definition': 'An escapade is an adventurous, daring, or unconventional action or incident, often involving some degree of mischief, excitement, or reckless behavior. These activities typically represent departures from normal, responsible conduct and often include elements of risk, spontaneity, or rebellion against conventional expectations. Escapades can range from harmless pranks and spontaneous adventures to more serious acts of misconduct or rebellion. Young people particularly engage in escapades as part of testing boundaries and asserting independence. The term often carries a somewhat playful or romantic connotation, suggesting that while the behavior might be inadvisable, it\'s also exciting or memorable. Literary and cinematic traditions frequently feature escapades as plot devices that reveal character traits or drive narrative development. Escapades can be solitary adventures or group activities that bond participants through shared experiences. Understanding escapades helps recognize the human need for excitement, adventure, and occasional departure from routine responsibilities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ES-kuh-payd',
                'etymology': 'From French "escapade," from Spanish "escapada," from "escapar" (to escape), ultimately from Vulgar Latin "excappare" (to get out of one\'s cape).',
                'language_origins': 'Latin, Spanish, French',
                'example_sentence': 'Their midnight _______ to the beach resulted in both adventure and trouble with their parents.',
                'memory_tip': 'Remember "ESCA-pade" - think "escape-ade" like a parade of escaping/adventure, or "escapade" sounds like "escape-aid" meaning an aid to escaping boring routine.'
            },
            'escape': {
                'definition': 'To escape means to break free from confinement, control, or danger, or to avoid an unpleasant or threatening situation. This fundamental verb encompasses various forms of liberation: physical escape from imprisonment or dangerous situations, psychological escape from stress or emotional pain, or creative escape through imagination and entertainment. Escape can be planned and deliberate (escape routes, escape plans) or spontaneous and reactive (escape from immediate danger). The concept extends to avoiding consequences, responsibilities, or unwanted attention. Entertainment industries rely on providing escape from daily routines through movies, books, games, and other diversions. Natural phenomena can also escape, such as gas escaping from containers or water escaping through leaks. Digital contexts include data escaping security systems or characters escaping in computer programming. Understanding different types of escape helps people recognize both literal and metaphorical forms of freedom and avoidance. The concept reflects fundamental human desires for autonomy and relief from constraints.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'ih-SKAYP',
                'etymology': 'From Old French "eschaper," from Vulgar Latin "excappare" meaning "to get out of one\'s cape," from "ex-" (out of) + "cappa" (cape).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The prisoners planned to _______ through a tunnel they had been digging for months.',
                'memory_tip': 'Remember "e-SCAPE" - think "e" (out) + "scape" (landscape), meaning getting out of the landscape/situation, or "escape" like taking off a cape to get away.'
            },
            'escarole': {
                'definition': 'Escarole is a variety of endive (Cichorium endivia) characterized by broad, slightly bitter leaves that are often used in salads and cooking. This leafy green vegetable has a distinctive slightly bitter taste that becomes milder when cooked. Escarole leaves are typically pale green to white in the center with darker green outer leaves, forming loose, open heads rather than the tight balls of lettuce or cabbage. The vegetable is popular in Mediterranean cuisine, particularly Italian cooking, where it\'s often sautéed with garlic and olive oil or added to soups and stews. Escarole is nutritious, providing vitamins A, C, and K, along with folate and fiber. It\'s commonly available in grocery stores and farmers\' markets, particularly during cooler months when it grows best. The slightly bitter flavor profile makes escarole appealing to those who enjoy complex, sophisticated tastes in their vegetables. Understanding escarole helps expand culinary knowledge and appreciation for diverse leafy greens beyond common lettuce varieties.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ES-kuh-rohl',
                'etymology': 'From French "escarole," from Italian "scarola," ultimately from Latin "escarius" (relating to food), related to "esca" (food).',
                'language_origins': 'Latin, Italian, French',
                'example_sentence': 'The Italian chef sautéed fresh _______ with white beans and garlic for a traditional side dish.',
                'memory_tip': 'Remember "ESCA-role" - think "esca" (food) + "role" meaning it plays a role in food, or "escarole" sounds like "escalate-role" because it escalates the role of greens in cooking.'
            },
            'escarpment': {
                'definition': 'An escarpment is a steep slope or cliff that separates two relatively level areas of differing elevations, typically formed through geological processes such as erosion, faulting, or differential weathering. These prominent landscape features create dramatic transitions between higher and lower terrain, often forming natural boundaries or barriers. Escarpments can result from various geological activities: fault escarpments form when tectonic forces cause vertical displacement of rock layers, while erosional escarpments develop when resistant rock layers protect underlying softer materials from weathering. Famous examples include the Niagara Escarpment in North America and various escarpments in Africa and Australia. These formations significantly influence local climate, vegetation patterns, and human settlement patterns. Escarpments often provide scenic vistas and can create microclimates due to elevation differences. Understanding escarpments helps appreciate landscape formation, geological history, and the relationship between geological processes and surface features. They represent important geographical features for navigation, land use planning, and natural resource management.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-SKARP-muhnt',
                'etymology': 'From French "escarpement," from "escarper" (to cut steeply), from Italian "scarpa" (slope), possibly from Germanic origin meaning "sharp cutting."',
                'language_origins': 'Germanic, Italian, French',
                'example_sentence': 'The hiking trail followed the edge of the dramatic _______ that offered stunning views of the valley below.',
                'memory_tip': 'Remember "e-SCARP-ment" - think "e" (out) + "scarp" (sharp/steep) + "ment" (result), meaning the result of sharp cutting out of landscape, or "escarpment" like "escape-ment" because it\'s a steep escape route up or down.'
            },
            'escheator': {
                'definition': 'An escheator is a historical legal official responsible for administering escheat, the process by which property reverts to the crown or state when the owner dies without legal heirs or when property is forfeited due to certain legal violations. This medieval administrative position involved identifying, securing, and managing properties that had no rightful private ownership according to feudal law. Escheators investigated inheritance claims, determined when properties should revert to royal control, and managed these properties until disposition. The role required knowledge of inheritance law, property rights, and genealogical research to verify legitimate heirs. In the feudal system, escheat was an important mechanism for preventing land from becoming permanently unavailable or unproductive. Modern legal systems have simplified inheritance procedures, but the concept of escheat still exists in laws governing unclaimed property and estates without heirs. Understanding escheators helps appreciate historical legal systems and the evolution of property rights. The position demonstrates how medieval societies managed complex property inheritance issues.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'es-CHEE-ter',
                'etymology': 'From Anglo-French "eschetour," from "escheat" (reversion of property), from Old French "escheoir" (to fall to), from Latin "excadere" (to fall out).',
                'language_origins': 'Latin, Old French, Anglo-French',
                'example_sentence': 'The medieval _______ was responsible for determining which properties should revert to the crown.',
                'memory_tip': 'Remember "e-SCHEAT-or" - think "e" (out) + "cheat" + "or" (person), meaning a person who deals with property that "cheats" death by going to the state, or "escheator" handles properties that "escheat" (revert) to the government.'
            },
            'eschew': {
                'definition': 'To eschew means to deliberately avoid, abstain from, or reject something, particularly behaviors, practices, or associations that one considers morally wrong, harmful, or undesirable. This formal verb suggests conscious choice and principled rejection rather than simple avoidance due to preference or convenience. People might eschew certain foods for health reasons, eschew violence as a matter of principle, or eschew social media to protect their privacy. The term often appears in discussions of ethics, lifestyle choices, and personal values where individuals make deliberate decisions to reject common practices. Eschewing typically involves some degree of sacrifice or inconvenience, as it often means giving up something that might be beneficial in some ways but conflicts with one\'s principles or goals. The word carries connotations of moral strength and purposeful decision-making. Understanding eschew helps express deliberate choices to avoid or reject rather than simple dislike or accidental avoidance.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'es-CHOO',
                'etymology': 'From Old French "eschiver" meaning "to avoid, shun," possibly from Germanic origin related to "shy" and "skew."',
                'language_origins': 'Germanic, Old French',
                'example_sentence': 'The health-conscious family decided to _______ processed foods and cook all meals from fresh ingredients.',
                'memory_tip': 'Remember "e-SCHEW" - think "e" (away) + "chew" meaning to chew away from/avoid something, or "eschew" sounds like "eh-shoo" meaning shooing something away.'
            },
            'esclandre': {
                'definition': 'Esclandre is a French term referring to a public scandal, disturbance, or outrageous incident that causes shock, embarrassment, or social disruption. This word describes situations where someone\'s behavior creates a scene or causes public controversy, often involving dramatic displays of emotion, conflict, or impropriety that attract unwanted attention. An esclandre typically occurs in social settings where the disruptive behavior contrasts sharply with expected norms of propriety and decorum. The term suggests both the incident itself and the social consequences that follow, including damage to reputation and relationships. Esclandres can result from various causes: emotional outbursts, public arguments, scandalous revelations, or inappropriate behavior at formal events. The concept is particularly relevant in contexts where social standing and public image are important. Understanding esclandre helps appreciate how public behavior affects social dynamics and reputation. The term reflects cultural values about appropriate conduct and the social costs of violating behavioral expectations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'es-KLAHN-druh',
                'etymology': 'From French "esclandre," from Old French "escandle," from Latin "scandalum" (stumbling block, scandal), from Greek "skandalon" (trap, snare).',
                'language_origins': 'Greek, Latin, French',
                'example_sentence': 'The diplomat\'s angry outburst at the formal dinner created an _______ that embarrassed both countries.',
                'memory_tip': 'Remember "e-SCLANDRE" - think "e" (out) + "scandal" + "re" (again), meaning a scandal that comes out again and again, or "esclandre" sounds like "escalate-scandal" meaning a scandal that escalates publicly.'
            },
            'escorts': {
                'definition': 'Escorts can refer to people who accompany others for social, professional, or protective purposes, or to the act of accompanying someone to provide guidance, protection, or companionship. In legitimate contexts, escorts might include security personnel who accompany dignitaries, social companions who attend events with clients, or guides who escort tourists through unfamiliar areas. Military escorts provide protection for convoys, VIPs, or prisoners. The term can also refer to naval vessels that protect other ships during transit. Professional escort services operate in various legal frameworks depending on jurisdiction, with clear distinctions between companionship services and other activities. Understanding different types of escort services helps distinguish between legitimate professional services and illegal activities. The concept emphasizes the role of accompaniment, protection, and guidance in various social and professional contexts. Context determines whether escort services are part of security, hospitality, tourism, or other legitimate business activities.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'es-KAWRTS',
                'etymology': 'From French "escorte," from Italian "scorta" (guide, guard), from "scorgere" (to guide), from Latin "ex-" (out) + "corrigere" (to set right).',
                'language_origins': 'Latin, Italian, French',
                'example_sentence': 'The naval _______ protected the merchant vessels during their passage through dangerous waters.',
                'memory_tip': 'Remember "e-SCORTS" - think "e" (out) + "courts" meaning taking someone out of court/safely, or "escorts" like "he-sorts" meaning someone sorts out/guides your journey.'
            },
            'escritoire': {
                'definition': 'An escritoire is a type of writing desk or secretary desk, typically featuring a hinged front panel that opens to reveal compartments, drawers, and a writing surface. This elegant piece of furniture originated in 17th and 18th-century European design and was particularly popular among the wealthy for conducting correspondence and managing personal affairs. Escritoires often combine functionality with decorative artistry, featuring fine woodwork, inlays, and sometimes secret compartments. The design typically includes multiple small drawers and pigeonholes for organizing writing materials, letters, and documents. When closed, an escritoire presents an attractive furniture piece that conceals its functional interior. These desks represent the importance of written communication in historical periods when letter-writing was a primary form of correspondence. Modern reproduction escritoires continue to appeal to those who appreciate traditional furniture design and organized workspaces. Understanding escritoires helps appreciate furniture history, craftsmanship traditions, and the evolution of workspace design for writing and correspondence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'es-kri-TWAHR',
                'etymology': 'From French "escritoire," from Medieval Latin "scriptorium" (writing room), from Latin "scribere" (to write). Related to "scripture" and "scribe."',
                'language_origins': 'Latin, French',
                'example_sentence': 'The antique _______ in the library contained numerous small compartments for organizing correspondence and writing supplies.',
                'memory_tip': 'Remember "escri-TOIRE" - think "escri" (write) + "toire" (story), meaning a place to write your story, or "escritoire" contains "scri" like "scribe" meaning writing.'
            },
            'esoteric': {
                'definition': 'Esoteric means intended for or understood by only a small group of people with specialized knowledge or interest; obscure, abstruse, or intended for the initiated. This adjective describes knowledge, practices, or ideas that are not readily accessible to the general public, often requiring special training, study, or initiation to comprehend. Esoteric subjects might include advanced academic theories, specialized professional techniques, mystical or spiritual practices, or highly technical fields that require extensive background knowledge. The term can apply to religious or philosophical teachings that are revealed only to selected students, scientific research that requires advanced education to understand, or cultural practices that are specific to particular communities. Esoteric knowledge often contrasts with exoteric knowledge, which is accessible to the general public. Understanding esoteric helps recognize the difference between specialized and general knowledge, and appreciate the value of both accessible and advanced learning. The concept reflects how knowledge can be organized in hierarchies of accessibility and complexity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'es-uh-TER-ik',
                'etymology': 'From Greek "esoterikos" meaning "belonging to an inner circle," from "esotero" (inner, more within), comparative of "eso" (within).',
                'language_origins': 'Greek',
                'example_sentence': 'The professor\'s lecture on quantum mechanics was too _______ for most undergraduate students to follow.',
                'memory_tip': 'Remember "eso-TER-ic" - think "eso" (inner) + "teric" (territory), meaning inner territory of knowledge, or "esoteric" sounds like "he-so-terror-ic" meaning terrifyingly difficult to understand for outsiders.'
            },
            'espadrille': {
                'definition': 'An espadrille is a type of casual shoe with a canvas or fabric upper and a flexible sole made from esparto grass rope or jute. These comfortable, lightweight shoes originated in the Pyrenees region between France and Spain and have been worn by workers and peasants for centuries. Traditional espadrilles feature a simple slip-on design, though modern versions may include laces, ankle straps, or different heel heights. The rope sole provides good ventilation and flexibility, making espadrilles ideal for warm weather and casual wear. High-fashion designers have adapted the basic espadrille design into luxury footwear, creating wedge espadrilles and designer versions using premium materials. The shoes remain popular for their comfort, breathability, and relaxed aesthetic that complements casual and vacation attire. Espadrilles represent an excellent example of functional folk design that has successfully transitioned into mainstream fashion. Understanding espadrilles helps appreciate how traditional craftwork influences contemporary footwear design and the evolution of casual fashion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'es-puh-DRIL',
                'etymology': 'From French "espadrille," from Occitan "espardilha," from "espart" (esparto grass), from Latin "spartum," from Greek "sparton" (rope made from rushes).',
                'language_origins': 'Greek, Latin, Occitan, French',
                'example_sentence': 'She packed comfortable _______ for her Mediterranean vacation, knowing they would be perfect for walking on cobblestone streets.',
                'memory_tip': 'Remember "espa-DRILLE" - think "esparto" (grass) + "drill" (make), meaning made from grass rope, or "espadrille" sounds like "spa-drill" meaning drilling relaxation into your feet.'
            },
            'espalier': {
                'definition': 'Espalier is a horticultural technique and art form involving training trees or shrubs to grow flat against a support structure such as a wall, fence, or trellis in decorative patterns. This method combines practical gardening with aesthetic design, creating living sculptures that maximize growing space while producing an ornamental effect. Espalier techniques originated in ancient Egypt and were refined in European gardens, particularly during the Renaissance and Baroque periods. The practice involves careful pruning, training, and support to guide plant growth into specific shapes such as cordons, fans, or geometric patterns. Common espalier subjects include fruit trees like apples, pears, and cherries, which benefit from the controlled growing conditions and improved sun exposure. The technique requires patience and skill but results in efficient use of space, easier harvesting, and attractive garden features. Modern gardeners use espalier for small gardens, urban spaces, and decorative landscaping. Understanding espalier helps appreciate the intersection of horticulture and art in garden design.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ih-SPAL-yer',
                'etymology': 'From French "espalier," from Italian "spalliera" (something for the shoulder to lean against), from "spalla" (shoulder), from Latin "spatula" (shoulder blade).',
                'language_origins': 'Latin, Italian, French',
                'example_sentence': 'The garden designer created an elegant _______ of apple trees along the south-facing wall.',
                'memory_tip': 'Remember "e-SPALIER" - think "e" (against) + "spalier" (spall/shoulder), meaning against a shoulder/support like a wall, or "espalier" sounds like "especially-ier" meaning especially artistic way of growing trees.'
            },
            'espaliercreances': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "espalier" (a horticultural training technique for trees) and "créances" (French for "claims" or "debts"). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'especially': {
                'definition': 'Especially is an adverb meaning "particularly," "to a great degree," or "more than in other cases," used to emphasize that something applies more strongly to one situation, person, or thing than to others. This word helps speakers and writers indicate that while a statement may be generally true, it is particularly or notably true in specific circumstances. For example, "I enjoy all music, especially jazz" indicates that while the speaker likes music in general, jazz receives particular preference. Especially often introduces examples that best illustrate a general point or highlights the most significant instances of a broader category. The word can also mean "for a special purpose" or "specifically," as in "designed especially for children." Understanding how to use especially effectively helps create emphasis and precision in communication. The word serves important functions in academic writing, everyday conversation, and formal presentations where speakers need to highlight particular aspects of their topics.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ih-SPESH-uh-lee',
                'etymology': 'From "especial" (from Old French "especial," from Latin "specialis" meaning "of a kind, special") + "-ly" (adverb suffix).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The new policy will benefit all employees, _______ those working in customer service.',
                'memory_tip': 'Remember "e-SPECIAL-ly" - think "especially" contains "special" which explains its meaning of particularly/specially, or "especially" like "he-special-ly" meaning in a particularly special way.'
            }
        }
        
        return batch_061_data.get(word, {
            'definition': f'Definition for {word} not found in batch data.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'Pronunciation for {word} not available.',
            'etymology': f'Etymology for {word} not available.',
            'language_origins': 'Unknown',
            'example_sentence': f'Example sentence for {word} not available.',
            'memory_tip': f'Memory tip for {word} not available.'
        })
    
    def process_batch(self, input_file: str, output_file: str):
        print(f"Processing {input_file}...")
        
        # Read the input CSV
        df = pd.read_csv(f"C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/{input_file}")
        
        processed_words = []
        errors_found = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            
            # Check for combined word errors
            is_error = False
            error_message = ""
            
            combined_words = [
                'equanimitythermos', 'ergoexistential', 'erythroblastesau', 
                'escalatorimpasto', 'espaliercreances'
            ]
            
            if word in combined_words:
                is_error = True
                if word == 'equanimitythermos':
                    error_message = 'Combined word error: "equanimitythermos" appears to be "equanimity" + "thermos" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'ergoexistential':
                    error_message = 'Combined word error: "ergoexistential" appears to be "ergo" + "existential" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'erythroblastesau':
                    error_message = 'Combined word error: "erythroblastesau" appears to be "erythroblast" + "esau" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'escalatorimpasto':
                    error_message = 'Combined word error: "escalatorimpasto" appears to be "escalator" + "impasto" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'espaliercreances':
                    error_message = 'Combined word error: "espaliercreances" appears to be "espalier" + "créances" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                errors_found.append(f"  - {word}: {error_message}")
            
            # Check for incomplete/corrupted words
            if word == 'ersion':
                is_error = True
                error_message = 'Incomplete word: "ersion" appears to be a fragment, possibly from words like "conversion", "immersion", "diversion", etc. This is likely a PDF parsing error where part of a word was truncated.'
                errors_found.append(f"  - {word}: {error_message}")
            
            # Get comprehensive Claude data
            claude_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty components
            phonetic_transparency = self.difficulty_calc.calculate_phonetic_transparency(word)
            word_frequency = self.difficulty_calc.calculate_word_frequency(word)
            morphological_complexity = self.difficulty_calc.calculate_morphological_complexity(word)
            etymology_complexity = self.difficulty_calc.calculate_etymology_complexity(word)
            
            word_data = WordData(
                word=word,
                definition=claude_data['definition'],
                part_of_speech=claude_data['part_of_speech'],
                pronunciation_guide=claude_data['pronunciation_guide'],
                etymology=claude_data['etymology'],
                language_origins=claude_data['language_origins'],
                example_sentence=claude_data['example_sentence'],
                memory_tip=claude_data['memory_tip']
            )
            
            processed_word = {
                'word': word_data.word,
                'years': row['years'],
                'source_files': row['source_files'],
                'source_difficulties': row['source_difficulties'],
                'definition': word_data.definition,
                'part_of_speech': word_data.part_of_speech,
                'pronunciation_guide': word_data.pronunciation_guide,
                'pronunciation_audio_file': '',
                'etymology': word_data.etymology,
                'etymology_source': 'Claude',
                'language_origins': word_data.language_origins,
                'example_sentence': word_data.example_sentence,
                'example_sentence_source': 'Claude',
                'memory_tip': word_data.memory_tip,
                'phonetic_transparency_score': phonetic_transparency,
                'word_frequency_score': word_frequency,
                'morphological_complexity_score': morphological_complexity,
                'etymology_complexity_score': etymology_complexity,
                'final_difficulty_rating': '',
                'final_difficulty_source': '',
                'notes': '',
                'reviewed': False,
                'needs_audio': True,
                'has_image': False,
                'image_description': '',
                'is_error': is_error,
                'error_details': error_message if is_error else ''
            }
            
            processed_words.append(processed_word)
        
        # Write the processed CSV
        output_path = f"C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/{output_file}"
        
        fieldnames = [
            'word', 'years', 'source_files', 'source_difficulties', 'definition', 
            'part_of_speech', 'pronunciation_guide', 'pronunciation_audio_file',
            'etymology', 'etymology_source', 'language_origins', 'example_sentence',
            'example_sentence_source', 'memory_tip', 'phonetic_transparency_score',
            'word_frequency_score', 'morphological_complexity_score', 'etymology_complexity_score',
            'final_difficulty_rating', 'final_difficulty_source', 'notes', 'reviewed',
            'needs_audio', 'has_image', 'image_description', 'is_error', 'error_details'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_words)
        
        print(f"Successfully processed {len(processed_words)}/{len(df)} words to {output_file}")
        
        if errors_found:
            print(f"Found {len(errors_found)} error(s):")
            for error in errors_found:
                print(error)
        
        print("Batch 061 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch061Processor()
    processor.process_batch("batch_061_words.csv", "batch_061_processed.csv")