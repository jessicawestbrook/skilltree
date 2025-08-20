#!/usr/bin/env python3

import pandas as pd
from dataclasses import dataclass
from typing import List, Optional, Tuple
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
    phonetic_transparency: Optional[int] = None
    word_frequency: Optional[int] = None
    morphological_complexity: Optional[int] = None
    etymology_complexity: Optional[int] = None
    final_difficulty: Optional[str] = None

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

class Batch088Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.errors = []

    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_088_data = {
            'iambic': {
                'definition': 'Iambic refers to a metrical pattern in poetry consisting of a rhythmic foot with an unstressed syllable followed by a stressed syllable, creating a da-DUM sound pattern that closely resembles natural English speech rhythms. This fundamental poetic meter appears in various forms including iambic pentameter (five iambic feet per line), which is the most common meter in English poetry and was famously used by Shakespeare in his sonnets and plays. The iambic pattern creates a gentle, flowing rhythm that feels natural to English speakers because it mirrors the stress patterns commonly found in everyday speech. Examples of iambic words include "beyond," "account," and "forget," where the first syllable is unstressed and the second is stressed. Poets use iambic meter to create musicality, emphasize certain words, and establish rhythmic expectations that can be fulfilled or deliberately broken for artistic effect. Understanding iambic meter is essential for analyzing poetry, understanding how language creates rhythm and meaning, and appreciating the technical craft involved in verse composition. The versatility of iambic meter has made it enduringly popular across centuries of English literature, from classical sonnets to modern verse.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ahy-AM-bik',
                'etymology': 'From Greek "iambikos," from "iambos" meaning "lampoon" or "satirical verse," originally referring to a satirical meter.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The sonnet was written in _______ pentameter, with each line containing five unstressed-stressed syllable pairs.',
                'memory_tip': 'Remember "IAMBIC" - sounds like "I-AM-bic," the rhythm pattern goes "I AM, I AM" with unstressed-stressed beats.'
            },
            'iatrogenic': {
                'definition': 'Iatrogenic describes medical conditions, complications, or harm that results from medical treatment or intervention itself rather than from the underlying disease being treated. This important medical concept acknowledges that healthcare procedures, medications, and treatments can sometimes cause unintended adverse effects, secondary conditions, or complications that wouldn\'t have occurred without medical intervention. Examples include medication side effects, hospital-acquired infections, surgical complications, or mental health issues resulting from prolonged hospitalization. Understanding iatrogenic effects is crucial for medical professionals to weigh treatment benefits against potential risks, obtain proper informed consent, and develop safer treatment protocols. The concept helps distinguish between disease progression and treatment-related problems, which is essential for accurate diagnosis and appropriate medical care. Iatrogenic harm can range from minor side effects to serious complications, and recognizing these possibilities helps healthcare providers minimize risks while maximizing therapeutic benefits. Medical education emphasizes preventing iatrogenic complications through careful patient monitoring, evidence-based treatment selection, and maintaining awareness of potential treatment-related risks. The term reflects medicine\'s commitment to honest acknowledgment of treatment limitations and the ethical principle of "first, do no harm."',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ahy-at-ruh-JEN-ik',
                'etymology': 'From Greek "iatros" (physician) and "genein" (to produce), literally meaning "physician-produced."',
                'language_origins': 'Greek',
                'example_sentence': 'The patient\'s liver damage was _______, caused by the very medications used to treat his original condition.',
                'memory_tip': 'Remember "IATROGENIC" - IATRO (doctor) + GENIC (caused by), medical problems caused by the doctor\'s treatment itself.'
            },
            'iberian': {
                'definition': 'Iberian refers to the Iberian Peninsula in southwestern Europe, which includes Spain, Portugal, Andorra, and small portions of France and Gibraltar, or to the peoples, cultures, and characteristics associated with this region. This geographic and cultural term encompasses the shared history, languages, and traditions that have developed on the peninsula over thousands of years. The ancient Iberians were pre-Roman peoples who inhabited the peninsula, and their legacy influences modern Spanish and Portuguese cultures. Iberian languages include Spanish, Portuguese, Catalan, Galician, and Basque, representing diverse linguistic traditions that reflect the region\'s complex cultural history. The term also applies to flora, fauna, and geographic features specific to the peninsula, including the Iberian lynx, Iberian Peninsula\'s unique ecosystems, and distinctive landscape characteristics. Throughout history, Iberian cultures have been influenced by Roman, Visigothic, Moorish, and other civilizations, creating rich cultural syntheses that define modern Iberian identity. Understanding Iberian heritage involves appreciating both the similarities and differences between Spanish and Portuguese traditions, as well as recognizing the peninsula\'s role in European history, exploration, and cultural development.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ahy-BEER-ee-uhn',
                'etymology': 'From Latin "Iberus," from Greek "Iberes," referring to the ancient peoples of the Iberian Peninsula.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The museum\'s collection included ancient _______ artifacts that demonstrated the sophisticated metalworking skills of pre-Roman peoples.',
                'memory_tip': 'Remember "IBERIAN" - from the IBERIAN Peninsula where Spain and Portugal are located, like "I\'ve been" to Iberia.'
            },
            'ibex': {
                'definition': 'Ibex refers to several species of wild mountain goats found in Europe, Asia, and Africa, characterized by their impressive curved horns, sure-footed climbing ability, and adaptation to steep, rocky terrain at high altitudes. These agile animals are renowned for their ability to navigate seemingly impossible cliff faces and mountainous terrain with remarkable grace and confidence. Male ibex typically have larger, more elaborate horns than females, using them for dominance displays and territorial battles during mating season. Different ibex species include the Alpine ibex of Europe, Nubian ibex of Africa and Arabia, and Siberian ibex of Central Asia, each adapted to specific mountain environments and climate conditions. These animals play important ecological roles as herbivores in mountain ecosystems, helping maintain vegetation balance and serving as prey for large predators like snow leopards and wolves. Many ibex populations have faced significant challenges from hunting, habitat loss, and climate change, requiring conservation efforts to maintain sustainable populations. Their remarkable climbing abilities and dramatic horns have made ibex symbols of wilderness and natural agility in various cultures. Understanding ibex biology and conservation status helps appreciate both their ecological importance and the challenges facing mountain wildlife in changing environments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AY-beks',
                'etymology': 'From Latin "ibex," referring to wild mountain goats, possibly from a pre-Indo-European language.',
                'language_origins': 'Latin, possibly pre-Indo-European',
                'example_sentence': 'The wildlife photographer waited patiently to capture images of the magnificent _______ scaling the nearly vertical cliff face.',
                'memory_tip': 'Remember "IBEX" - sounds like "I-BECKS," wild mountain goats that beckon you to admire their incredible climbing skills.'
            },
            'ibidem': {
                'definition': 'Ibidem is a Latin term meaning "in the same place," commonly abbreviated as "ibid." and used in academic citations to refer to the same source mentioned in the immediately preceding footnote or endnote. This scholarly convention allows writers to reference the same work multiple times without repeating full bibliographic information, making citations more concise and readable. When using ibidem, the author indicates that the current citation refers to exactly the same source as the previous citation, though it may reference a different page number. The term is essential in academic writing, legal documents, and scholarly research where precise source documentation is required for credibility and verification purposes. Proper use of ibidem requires that no other sources intervene between the original citation and the ibidem reference, maintaining clear connection between citations. Modern citation styles have varying rules for using ibidem, with some preferring it while others recommend repeating author names for clarity. Understanding ibidem and similar Latin citation terms reflects the international scholarly tradition that relies on precise documentation methods. The term demonstrates how Latin continues to influence academic writing conventions even in contemporary scholarship.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ih-BEE-dem',
                'etymology': 'From Latin "ibidem," from "ibi" (there) and "dem" (the same), literally meaning "in the same place."',
                'language_origins': 'Latin',
                'example_sentence': 'After citing Smith\'s comprehensive study, the researcher used _______ to reference another point from the same work.',
                'memory_tip': 'Remember "IBIDEM" - sounds like "I-BID-em," meaning "I bid you look in the same place" for the source reference.'
            },
            'ibuprofen': {
                'definition': 'Ibuprofen is a widely used nonsteroidal anti-inflammatory drug (NSAID) that reduces pain, inflammation, and fever by blocking enzymes that produce prostaglandins, chemical messengers involved in inflammatory responses. This over-the-counter medication is commonly used to treat headaches, muscle aches, arthritis pain, menstrual cramps, toothaches, and minor injuries where inflammation contributes to discomfort. Ibuprofen works by inhibiting cyclooxygenase (COX) enzymes, which reduces the production of prostaglandins that cause pain, swelling, and fever responses in the body. The medication is available in various forms including tablets, capsules, liquid suspensions, and topical preparations, with different strengths for different age groups and conditions. While generally safe when used as directed, ibuprofen can cause side effects including stomach irritation, kidney problems, and cardiovascular risks, particularly with long-term use or high doses. The drug was developed in the 1960s and has become one of the most commonly used pain relievers worldwide due to its effectiveness and availability. Understanding proper ibuprofen use involves following dosing instructions, being aware of potential interactions with other medications, and consulting healthcare providers for chronic pain management. The medication represents an important tool in modern pain management and self-care.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ahy-BYOO-proh-fen',
                'etymology': 'From its chemical name: iso-butyl-propanoic-phenolic acid, abbreviated to create the generic drug name.',
                'language_origins': 'Modern pharmaceutical nomenclature',
                'example_sentence': 'The doctor recommended _______ to reduce the inflammation and pain in the patient\'s injured knee.',
                'memory_tip': 'Remember "IBUPROFEN" - sounds like "I-BUY-pro-fen," a pro-level pain reliever you can buy over-the-counter.'
            },
            'icarian': {
                'definition': 'Icarian refers to characteristics resembling those of Icarus from Greek mythology, who flew too close to the sun with wings made of feathers and wax, causing the wax to melt and leading to his downfall. This adjective describes overly ambitious behavior, reckless pursuit of goals, or actions that ignore warnings and limitations, ultimately resulting in failure or disaster. The mythological story of Icarus has become a powerful metaphor for the dangers of hubris, overconfidence, and ignoring wise counsel in pursuit of impossible dreams. Icarian behavior often involves rejecting practical constraints, dismissing safety warnings, or pursuing goals beyond one\'s capabilities or resources. The term applies to various contexts including business ventures that expand too rapidly, political ambitions that overreach, or personal decisions that ignore obvious risks in pursuit of unrealistic objectives. Literature and psychology use Icarian themes to explore the tension between ambition and prudence, innovation and safety, dreams and reality. Understanding Icarian tendencies helps recognize the importance of balancing aspiration with practical wisdom, listening to experienced advice, and maintaining realistic assessments of capabilities and limitations. The concept serves as a cautionary reminder about the potential consequences of unchecked ambition.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-KAIR-ee-uhn',
                'etymology': 'From "Icarus," the Greek mythological figure who flew too close to the sun, plus the suffix "-ian."',
                'language_origins': 'Greek, English',
                'example_sentence': 'The startup\'s _______ expansion strategy led to rapid growth followed by spectacular collapse when funding dried up.',
                'memory_tip': 'Remember "ICARIAN" - like Icarus who flew too high and crashed, describing overly ambitious behavior that ignores limits.'
            },
            'iceberg': {
                'definition': 'Iceberg refers to a large piece of freshwater ice that has broken off from a glacier or ice shelf and floats freely in open water, with typically only about 10% of its mass visible above the water surface. These massive ice formations pose significant hazards to shipping, most famously demonstrated by the Titanic disaster in 1912, and require constant monitoring in shipping lanes. Icebergs form when chunks of glacial ice calve (break off) from glaciers that reach the sea, particularly in polar regions like Greenland, Antarctica, and Arctic waters. The hidden bulk of icebergs below the waterline can be enormous, making them extremely dangerous to ships whose captains may underestimate their true size and extent. Different iceberg shapes have specific names including tabular bergs (flat-topped), pinnacle bergs (pointed), and weathered bergs carved by wind and waves. The term "tip of the iceberg" has become a common metaphor for situations where visible problems represent much larger hidden issues. Climate change affects iceberg formation and movement patterns, with increasing calving rates from warming glaciers contributing to rising sea levels. Understanding icebergs involves oceanography, glaciology, and navigation science, as these formations play important roles in ocean circulation and marine ecosystems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHYS-burg',
                'etymology': 'From Dutch "ijsberg," from "ijs" (ice) and "berg" (mountain), literally meaning "ice mountain."',
                'language_origins': 'Dutch',
                'example_sentence': 'The ship\'s captain changed course when radar detected a massive _______ drifting into the shipping lane.',
                'memory_tip': 'Remember "ICEBERG" - ICE + BERG (mountain), a mountain of ice floating in the ocean with most of it hidden underwater.'
            },
            'icelandic': {
                'definition': 'Icelandic refers to the North Germanic language spoken in Iceland, closely related to Old Norse and notable for its conservative grammar and vocabulary that has changed relatively little over the past thousand years. This linguistic characteristic makes Icelandic speakers uniquely able to read medieval Icelandic sagas and literature with minimal difficulty compared to speakers of other modern languages reading their medieval texts. The language maintains complex grammatical features including four cases, three genders, and intricate verb conjugations that have been simplified or lost in related languages like Norwegian and Swedish. Icelandic culture emphasizes linguistic purity, with language committees actively creating new Icelandic words for modern concepts rather than borrowing foreign terms, helping preserve the language\'s distinctive character. The term also describes anything relating to Iceland, including its culture, geography, history, and people, encompassing the island nation\'s unique position in the North Atlantic and its rich literary and cultural traditions. Iceland\'s relatively small population and geographic isolation have helped preserve traditional culture and language while fostering distinctive approaches to literature, music, and social organization. Understanding Icelandic involves appreciating both the language\'s historical significance in preserving Norse literary heritage and Iceland\'s contemporary contributions to global culture.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'AHYS-lan-dik',
                'etymology': 'From "Iceland" + suffix "-ic," referring to the island nation and its language and culture.',
                'language_origins': 'Old Norse, Germanic',
                'example_sentence': 'The linguistics professor specialized in _______ literature, particularly the medieval sagas that preserve ancient Norse traditions.',
                'memory_tip': 'Remember "ICELANDIC" - ICELAND + IC, relating to the land of ice and its unique language that preserves ancient Norse traditions.'
            },
            'iceni': {
                'definition': 'Iceni were an ancient British Celtic tribe that inhabited what is now Norfolk and parts of Suffolk, Cambridgeshire, and Hertfordshire in eastern England during the Iron Age and early Roman period. This warrior tribe is most famous for their fierce resistance to Roman rule under the leadership of Queen Boudica (also spelled Boudicca) around 60-61 CE, when they led a major uprising against Roman occupation. The Iceni initially maintained a client relationship with Rome, allowing them some autonomy while acknowledging Roman authority, but tensions escalated after the death of King Prasutagus, Boudica\'s husband. The Iceni rebellion involved the destruction of several Roman settlements including Camulodunum (Colchester), Londinium (London), and Verulamium (St. Albans), killing thousands of Romans and British allies before being ultimately defeated. Archaeological evidence reveals that the Iceni were skilled metalworkers, farmers, and warriors who lived in hillforts and settlements throughout East Anglia. Their culture included distinctive pottery, jewelry, and coins that provide insights into pre-Roman British society and economy. The Iceni legacy includes their role in British resistance narratives and their contribution to understanding Celtic society in ancient Britain. Modern British culture remembers the Iceni, particularly Boudica, as symbols of resistance against foreign occupation.',
                'part_of_speech': 'proper noun (plural)',
                'pronunciation_guide': 'ih-SEE-nahy',
                'etymology': 'From Latin "Iceni," possibly from Celtic roots meaning "kindred" or related to tribal identity.',
                'language_origins': 'Celtic, Latin',
                'example_sentence': 'Archaeological excavations in Norfolk continue to reveal artifacts from the _______ settlements that existed before and during Roman occupation.',
                'memory_tip': 'Remember "ICENI" - sounds like "ICE-knee," the ancient British tribe who gave Romans the cold shoulder and made them kneel in defeat.'
            },
            'ichthyology': {
                'definition': 'Ichthyology is the branch of zoology devoted to the study of fish, including their anatomy, physiology, behavior, ecology, evolution, and classification. This scientific discipline encompasses research on all fish species, from tiny minnows to massive sharks, covering both freshwater and marine environments worldwide. Ichthyologists study fish structure and function, investigating how different species have adapted to various aquatic environments, feeding strategies, and reproductive methods. The field includes practical applications such as fisheries management, conservation biology, aquaculture development, and understanding the ecological roles fish play in aquatic ecosystems. Modern ichthyology uses advanced techniques including genetic analysis, underwater observation technology, and sophisticated laboratory methods to understand fish biology and behavior. Research areas include fish migration patterns, breeding behaviors, population dynamics, and responses to environmental changes including climate change and pollution. The discipline is crucial for sustainable fishing practices, marine conservation efforts, and understanding aquatic biodiversity. Ichthyology also contributes to medicine through studies of fish toxins, pharmaceutical compounds, and physiological processes that may have applications in human health. Understanding this field involves appreciating both the incredible diversity of fish species and their fundamental importance to aquatic ecosystems and human societies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-thee-OL-uh-jee',
                'etymology': 'From Greek "ichthys" (fish) and "logos" (study), literally meaning "the study of fish."',
                'language_origins': 'Greek',
                'example_sentence': 'The marine biologist specialized in _______, focusing her research on the behavior and ecology of deep-sea fish species.',
                'memory_tip': 'Remember "ICHTHYOLOGY" - ICHTHY (fish) + OLOGY (study of), the study of fish and their biology.'
            },
            'icing': {
                'definition': 'Icing refers to a sweet, often decorative coating applied to cakes, cookies, pastries, and other baked goods, typically made from powdered sugar, butter, cream cheese, or other ingredients that create smooth, spreadable, or pipeable textures. This culinary element serves both aesthetic and flavor purposes, enhancing the appearance of desserts while adding sweetness and complementary flavors. Different types of icing include buttercream (made with butter and powdered sugar), cream cheese frosting, royal icing (which hardens when dry), fondant (rolled sugar paste), and glaze (thin, pourable consistency). Professional bakers and decorators use icing to create elaborate designs, flowers, borders, and artistic elements that transform simple cakes into spectacular centerpieces for celebrations. The term also refers to the formation of ice on surfaces, particularly the dangerous accumulation of ice on aircraft wings, power lines, or roadways that can create safety hazards. In hockey, icing is a rule violation that occurs when a player shoots the puck from their defensive zone past the opposing goal line without it being touched. Understanding icing in culinary contexts involves mastering consistency, flavor balance, and decorative techniques that enhance both taste and visual appeal of baked goods.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHYS-ing',
                'etymology': 'From "ice" + suffix "-ing," originally referring to ice formation, later applied to sweet cake coatings.',
                'language_origins': 'Old English',
                'example_sentence': 'The baker carefully applied chocolate _______ to the birthday cake, creating an elegant finish for the celebration.',
                'memory_tip': 'Remember "ICING" - like ICE + ING, the sweet coating on cakes that\'s as smooth and pretty as ice.'
            },
            'icosahedron': {
                'definition': 'Icosahedron is a three-dimensional geometric solid with twenty triangular faces, twelve vertices, and thirty edges, representing one of the five Platonic solids that have been studied since ancient times. This regular polyhedron features equilateral triangles as faces, with five triangular faces meeting at each vertex, creating a nearly spherical shape that appears frequently in mathematics, crystallography, and natural structures. The icosahedron demonstrates remarkable mathematical properties including high symmetry, optimal packing efficiency, and relationships to the golden ratio that make it fascinating to mathematicians and scientists. Natural examples include the structures of certain viruses, the arrangement of protein subunits in some biological molecules, and the geodesic patterns found in buckminsterfullerene (buckyballs) carbon molecules. Architectural applications include geodesic domes inspired by icosahedral geometry, which provide strong, efficient structures using the geometric principles of triangular distribution of forces. The icosahedron appears in various games and puzzles, particularly twenty-sided dice used in role-playing games. Understanding icosahedral geometry involves appreciating both its mathematical elegance and its practical applications in fields ranging from molecular biology to architectural engineering. The shape represents the intersection of pure mathematics with natural phenomena and human design.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ahy-koh-suh-HEE-druhn',
                'etymology': 'From Greek "icosa" (twenty) and "hedron" (seat/face), literally meaning "twenty faces."',
                'language_origins': 'Greek',
                'example_sentence': 'The virus researcher explained how many viruses have _______ structures with twenty triangular faces arranged in perfect geometric symmetry.',
                'memory_tip': 'Remember "ICOSAHEDRON" - ICOSA (twenty) + HEDRON (faces), a 3D shape with twenty triangular faces like a fancy twenty-sided die.'
            },
            'idea': {
                'definition': 'Idea refers to a thought, concept, notion, or mental representation that exists in the mind, serving as the foundation for understanding, creativity, problem-solving, and communication. This fundamental cognitive concept encompasses everything from simple thoughts about immediate experiences to complex theoretical frameworks that shape entire disciplines of knowledge. Ideas can emerge through various processes including observation, reasoning, imagination, inspiration, or systematic analysis, and they form the basis for all human intellectual and creative activities. The development and communication of ideas drives scientific progress, artistic expression, social change, and technological innovation throughout human history. Ideas can be concrete (specific solutions to particular problems) or abstract (philosophical concepts about the nature of existence), practical (methods for accomplishing tasks) or theoretical (explanations for natural phenomena). The quality, originality, and usefulness of ideas vary greatly, with some becoming foundational to human understanding while others remain personal or temporary. Understanding ideas involves recognizing their role in thinking processes, learning mechanisms, creative expression, and the transmission of knowledge across individuals and generations. The ability to generate, evaluate, and communicate ideas effectively is essential for education, innovation, and human progress.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ahy-DEE-uh',
                'etymology': 'From Greek "idea" meaning "form" or "appearance," from "idein" meaning "to see."',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The scientist\'s brilliant _______ about quantum mechanics revolutionized our understanding of atomic behavior.',
                'memory_tip': 'Remember "IDEA" - sounds like "I-DEE-ya," what you say when you see (idein) a new thought or concept in your mind.'
            },
            'identifiable': {
                'definition': 'Identifiable describes something that can be recognized, distinguished, or determined through observation, analysis, or comparison with known characteristics or criteria. This quality implies that sufficient distinctive features, patterns, or markers exist to allow accurate recognition or classification of objects, people, concepts, or phenomena. In scientific contexts, identifiable traits include physical characteristics, genetic markers, chemical signatures, or behavioral patterns that enable researchers to classify and study different species, compounds, or processes. Legal and security applications rely on identifiable information such as fingerprints, DNA profiles, or biometric data to establish identity and maintain accurate records. The concept is crucial for quality control, where products must have identifiable standards and specifications that ensure consistency and safety. Medical diagnosis depends on identifiable symptoms, test results, and patterns that help healthcare providers recognize specific conditions and develop appropriate treatments. Understanding what makes something identifiable involves recognizing the importance of distinctive characteristics, reliable measurement methods, and consistent criteria for recognition. The ability to make accurate identifications supports scientific research, legal proceedings, security measures, and countless daily activities that require distinguishing between different options or possibilities.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ahy-DEN-tuh-fahy-uh-buhl',
                'etymology': 'From "identify" (from Latin "identitas" meaning "sameness") plus suffix "-able" meaning "capable of being."',
                'language_origins': 'Latin, English',
                'example_sentence': 'The forensic expert found several _______ fingerprints at the crime scene that could help solve the case.',
                'memory_tip': 'Remember "IDENTIFIABLE" - IDENTIFY + ABLE, able to be identified or recognized through distinctive characteristics.'
            },
            'idiolect': {
                'definition': 'Idiolect refers to the unique variety of language used by an individual speaker, encompassing their particular vocabulary choices, pronunciation patterns, grammatical preferences, and speech habits that distinguish their communication style from others. This linguistic concept recognizes that while people share common languages with their communities, each person develops distinctive ways of speaking that reflect their background, experiences, education, and personal preferences. Individual idiolects include preferred expressions, regional accent features, professional terminology, generational language patterns, and personal linguistic innovations that create subtle but recognizable differences in how people communicate. Linguists study idiolects to understand language variation, individual creativity in language use, and how personal factors influence communication patterns. The concept helps explain why family members, close friends, or colleagues can often identify speakers by their distinctive speech patterns even without seeing them. Idiolects change over time as individuals encounter new experiences, move to different locations, or adapt their communication styles to various social or professional contexts. Understanding idiolects involves appreciating both the shared nature of language as a community resource and the individual creativity that makes each person\'s communication unique. This recognition helps explain the rich diversity found within any language community.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ID-ee-uh-lekt',
                'etymology': 'From Greek "idios" (one\'s own) and "lektos" (spoken), literally meaning "one\'s own way of speaking."',
                'language_origins': 'Greek',
                'example_sentence': 'The linguist could identify the author of anonymous texts by analyzing distinctive features of their _______ and writing style.',
                'memory_tip': 'Remember "IDIOLECT" - IDIO (individual) + LECT (speech), an individual\'s own unique way of speaking and using language.'
            },
            'idiosyncratic': {
                'definition': 'Idiosyncratic describes behavior, characteristics, or features that are distinctive, peculiar, or unique to a particular individual, often involving unusual habits, preferences, or ways of doing things that set someone apart from others. This adjective emphasizes the personal and individual nature of traits, suggesting that they are not widely shared or easily explained by general patterns or social norms. Idiosyncratic behaviors might include unusual work routines, specific preferences for organizing personal space, distinctive artistic styles, or particular ways of solving problems that work for the individual but seem odd to others. The term can apply to both positive uniqueness (creative approaches, innovative thinking) and neutral peculiarities (harmless personal habits) without necessarily implying judgment about the value or appropriateness of the characteristics. Artists, writers, and inventors often display idiosyncratic approaches to their work that contribute to their distinctive contributions and creative output. Understanding idiosyncratic traits involves recognizing that individual differences contribute to human diversity and that unusual approaches can sometimes lead to valuable insights or innovations. The concept celebrates the importance of individual variation while acknowledging that some personal characteristics may seem strange or incomprehensible to others.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'id-ee-uh-sin-KRAT-ik',
                'etymology': 'From Greek "idiosynkratos," from "idios" (one\'s own) and "syn" (together) and "kratos" (mixture).',
                'language_origins': 'Greek',
                'example_sentence': 'The artist\'s _______ painting technique involved using unusual tools and unconventional color combinations that created her signature style.',
                'memory_tip': 'Remember "IDIOSYNCRATIC" - IDIO (individual) + SYNC + RATIC, individual characteristics that don\'t sync with normal patterns.'
            },
            'idyllic': {
                'definition': 'Idyllic describes situations, places, or experiences that are extremely peaceful, pleasant, and perfect in a simple, natural way, often evoking images of pastoral beauty, harmonious relationships, or carefree happiness. This adjective suggests an almost fairy-tale quality of contentment and tranquility that contrasts with the complications and stresses of modern life. Idyllic scenes might include peaceful countryside landscapes, happy families enjoying time together, romantic settings with perfect weather and beautiful surroundings, or communities where people live in harmony with nature and each other. The term often carries nostalgic connotations, suggesting simpler times when life seemed more innocent, relationships more genuine, and daily existence less complicated by modern pressures. Literature and art frequently portray idyllic settings as escapes from urban complexity or as representations of human happiness in its purest form. However, idyllic conditions are often idealized or temporary, representing aspirational goals rather than sustainable realities. Understanding idyllic involves appreciating both the human desire for peace and simplicity and the recognition that such perfect conditions are rare and precious. The concept serves as a reference point for evaluating the quality of life and the pursuit of happiness.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ahy-DIL-ik',
                'etymology': 'From Greek "eidyllion" meaning "little picture," referring to short pastoral poems depicting idealized rural life.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The couple spent their honeymoon in an _______ cottage by the lake, surrounded by mountains and wildflowers.',
                'memory_tip': 'Remember "IDYLLIC" - sounds like "IDEAL-lic," describing ideal, perfect, peaceful situations that seem like paradise.'
            },
            'igneous': {
                'definition': 'Igneous describes rocks that formed from the cooling and solidification of molten magma or lava, representing one of the three main categories of rocks along with sedimentary and metamorphic rocks. These rocks form through volcanic processes either above ground (extrusive igneous rocks) when lava cools on the Earth\'s surface, or below ground (intrusive igneous rocks) when magma cools slowly within the Earth\'s crust. Common igneous rocks include granite (intrusive), basalt (extrusive), obsidian (volcanic glass), and pumice (volcanic foam), each with distinctive characteristics based on their cooling history and mineral composition. The texture and mineral content of igneous rocks provide valuable information about the conditions under which they formed, including temperature, pressure, and cooling rate. Igneous rocks play crucial roles in understanding Earth\'s geological history, plate tectonics, and volcanic activity patterns that shape landscapes and create natural hazards. The study of igneous rocks helps geologists understand magma chamber processes, predict volcanic eruptions, and locate valuable mineral deposits. These rocks form the foundation of many mountain ranges and ocean floors, representing the primary way new rock material is added to Earth\'s crust. Understanding igneous processes is essential for geology, volcanology, and comprehending the dynamic nature of Earth\'s interior.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IG-nee-uhs',
                'etymology': 'From Latin "igneus," from "ignis" meaning "fire," referring to rocks formed by fire or heat.',
                'language_origins': 'Latin',
                'example_sentence': 'The geologist identified the dark, fine-grained rock as an _______ formation created when lava cooled rapidly on the surface.',
                'memory_tip': 'Remember "IGNEOUS" - from Latin "ignis" (fire), rocks formed by fire from cooling magma or lava.'
            },
            'ignite': {
                'definition': 'Ignite means to catch fire or cause something to start burning, involving the chemical process where combustible materials react with oxygen to produce heat, light, and often flames. This fundamental process requires three elements: fuel (combustible material), oxygen, and sufficient heat (ignition source) to reach the material\'s flash point. Ignition can occur through various means including matches, sparks, friction, electrical discharge, focused sunlight, or chemical reactions that generate enough heat to start combustion. The term extends metaphorically to describe the beginning of any rapid, intense process, such as igniting passion, igniting controversy, or igniting social movements that spread quickly through communities. Understanding ignition is crucial for fire safety, preventing unwanted fires through proper storage and handling of flammable materials, and controlling ignition sources in hazardous environments. Industrial applications include controlled ignition in engines, furnaces, and manufacturing processes where precise timing and conditions are essential for efficient operation. The concept also applies to initiating explosive reactions in mining, demolition, and military applications where controlled ignition timing determines safety and effectiveness. Fire prevention and firefighting strategies focus heavily on eliminating potential ignition sources and controlling fuel and oxygen availability to prevent or extinguish fires.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ig-NAHYT',
                'etymology': 'From Latin "ignitus," past participle of "ignire," from "ignis" meaning "fire."',
                'language_origins': 'Latin',
                'example_sentence': 'The camper used dry tinder and a spark from flint to _______ the campfire for cooking dinner.',
                'memory_tip': 'Remember "IGNITE" - from Latin "ignis" (fire), to set fire to something or make it start burning.'
            },
            'ignoble': {
                'definition': 'Ignoble describes actions, motives, or character traits that lack honor, dignity, or moral worth, characterized by meanness, selfishness, or base behavior that falls short of admirable standards. This adjective applies to conduct that is dishonorable, shameful, or unworthy of respect, often involving betrayal of trust, cowardice, or putting personal gain above ethical principles. Ignoble behavior contrasts sharply with noble ideals of courage, generosity, loyalty, and self-sacrifice, representing the darker aspects of human nature where people choose expedient or selfish actions over principled ones. Examples might include abandoning allies in crisis, exploiting vulnerable people for personal advantage, or refusing to take responsibility for one\'s mistakes while blaming others. The term often appears in discussions of character, ethics, and moral judgment where the distinction between worthy and unworthy motivations becomes important. Literature frequently explores ignoble characters who serve as cautionary examples or foils to heroic figures, demonstrating the consequences of moral weakness. Understanding ignoble involves recognizing the importance of honor, integrity, and moral courage in evaluating human actions and character. The concept helps identify behaviors that deserve criticism or disappointment while highlighting the value of striving for higher moral standards.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ig-NOH-buhl',
                'etymology': 'From Latin "ignobilis," from "in-" (not) and "nobilis" (noble), literally meaning "not noble."',
                'language_origins': 'Latin',
                'example_sentence': 'The politician\'s _______ decision to abandon his campaign promises for personal gain disappointed his supporters.',
                'memory_tip': 'Remember "IGNOBLE" - IG (not) + NOBLE, behavior that is not noble, lacking honor and dignity.'
            },
            'ignominious': {
                'definition': 'Ignominious describes situations, actions, or outcomes that bring deep shame, disgrace, or public humiliation, typically involving spectacular failure, moral failing, or behavior that damages one\'s reputation and honor. This powerful adjective emphasizes not just failure but failure that is particularly embarrassing, shameful, or worthy of public scorn and disappointment. Ignominious defeats involve not just losing but losing in ways that reveal incompetence, cowardice, or moral weakness that brings lasting shame. The term often applies to situations where people in positions of trust or authority fail spectacularly, betraying expectations and responsibilities in ways that cause widespread disappointment and criticism. Historical examples include military leaders who abandon their troops, politicians caught in major corruption scandals, or institutions that fail catastrophically in their primary missions. Ignominious endings to careers, relationships, or endeavors suggest that the conclusion was not just unsuccessful but shamefully so, often involving circumstances that could have been avoided through better judgment or moral behavior. Understanding ignominious involves recognizing the social and personal importance of honor, reputation, and meeting responsibilities. The concept emphasizes how certain types of failure carry lasting consequences that go beyond immediate practical effects to include damage to character and standing in the community.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ig-nuh-MIN-ee-uhs',
                'etymology': 'From Latin "ignominiosus," from "ignominia" (dishonor), from "in-" (not) and "nomen" (name/reputation).',
                'language_origins': 'Latin',
                'example_sentence': 'The general\'s _______ retreat abandoned his soldiers and marked the end of his military career in disgrace.',
                'memory_tip': 'Remember "IGNOMINIOUS" - IG (not) + NOMEN (name/reputation), actions that damage your good name and bring shame.'
            },
            'ignore': {
                'definition': 'Ignore means to deliberately pay no attention to something or someone, consciously choosing to disregard, overlook, or refuse to acknowledge what is present or being communicated. This intentional act of inattention can serve various purposes including avoiding unpleasant situations, maintaining focus on priorities, expressing disapproval or rejection, or protecting oneself from unwanted interactions or influences. Ignoring can be temporary (waiting for a situation to resolve itself) or permanent (cutting off contact with problematic people), passive (simply not responding) or active (deliberately turning away from stimuli). The effectiveness and appropriateness of ignoring depend heavily on context, relationships, and potential consequences of inaction. In some situations, ignoring problems can make them worse, while in others, ignoring distractions or negative influences can be beneficial for mental health and productivity. Social dynamics involve complex rules about when ignoring is acceptable, rude, or harmful, with cultural variations in how silence and inattention are interpreted. Educational and behavioral contexts use planned ignoring as a strategy to reduce unwanted behaviors by removing attention that might reinforce them. Understanding when and how to ignore involves balancing self-protection with social responsibility and recognizing the difference between healthy boundary-setting and harmful neglect.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ig-NAWR',
                'etymology': 'From Latin "ignorare," from "ignarus" meaning "not knowing," from "in-" (not) and "gnarus" (knowing).',
                'language_origins': 'Latin',
                'example_sentence': 'The teacher advised students to _______ distractions and focus completely on their exam questions.',
                'memory_tip': 'Remember "IGNORE" - sounds like "IG-NOR," to not know or pay attention to something on purpose.'
            },
            'ikat': {
                'definition': 'Ikat is a traditional textile dyeing technique where yarns are resist-dyed before being woven into fabric, creating distinctive blurred or feathered patterns that are characteristic of this ancient craft. The process involves binding sections of yarn tightly to prevent dye penetration, then dyeing the yarns in planned patterns before removing the bindings and weaving the pre-patterned threads into finished textiles. This complex technique requires exceptional skill and planning because the weaver must visualize the final design while working with individual dyed threads, making precise alignment crucial for achieving clear pattern definition. Different cultures have developed unique ikat traditions, including Indonesian ikat with elaborate geometric and figurative designs, Japanese kasuri with subtle geometric patterns, and Central Asian ikat featuring bold, vibrant motifs. The resist-dyeing process can be applied to warp threads (warp ikat), weft threads (weft ikat), or both (double ikat), with double ikat being the most complex and prestigious form requiring extraordinary skill. Ikat textiles are highly valued for their artistic beauty, cultural significance, and the exceptional craftsmanship required for their creation. Modern appreciation of ikat includes both traditional cultural preservation and contemporary fashion applications that introduce these ancient techniques to global markets. Understanding ikat involves appreciating both the technical complexity and cultural meanings embedded in these remarkable textiles.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EE-kaht',
                'etymology': 'From Malay/Indonesian "mengikat" meaning "to tie" or "to bind," referring to the resist-dyeing process.',
                'language_origins': 'Malay, Indonesian',
                'example_sentence': 'The textile museum displayed a stunning collection of traditional _______ fabrics showing the intricate patterns created by resist-dyeing techniques.',
                'memory_tip': 'Remember "IKAT" - from Indonesian "ikat" (to tie), fabric made by tying and dyeing threads before weaving them together.'
            },
            'ikebana': {
                'definition': 'Ikebana is the traditional Japanese art of flower arrangement that emphasizes harmony, balance, and the beauty of natural materials through carefully composed displays that reflect philosophical and aesthetic principles. This sophisticated artistic practice goes far beyond simply arranging flowers in vases, incorporating principles of asymmetry, space, seasonal awareness, and the spiritual relationship between humans and nature. Ikebana arrangements typically feature three main elements representing heaven, earth, and humanity, creating compositions that achieve balance through careful attention to line, form, color, and the use of negative space. Different schools of ikebana have developed over centuries, each with distinctive styles, rules, and philosophical approaches, including Ikenobo (the oldest school), Ohara, and Sogetsu, among others. The practice requires extensive training and study to master the technical skills, understand seasonal plant materials, and develop the aesthetic sensitivity needed to create meaningful compositions. Materials used in ikebana include not only flowers but also branches, leaves, seed pods, and other natural elements that are selected and positioned to create harmony and express deeper meanings about nature and life. Modern ikebana continues to evolve while maintaining traditional principles, with contemporary practitioners exploring new materials and interpretations while preserving the art\'s spiritual and aesthetic foundations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ee-kuh-BAH-nah',
                'etymology': 'From Japanese "ikeru" (to arrange) and "hana" (flowers), literally meaning "arranging flowers."',
                'language_origins': 'Japanese',
                'example_sentence': 'The _______ master demonstrated how to create a balanced arrangement using just three branches and minimal flowers.',
                'memory_tip': 'Remember "IKEBANA" - sounds like "I-KEE-bahna," the Japanese art of keeping flowers arranged in beautiful, meaningful displays.'
            },
            'illative': {
                'definition': 'Illative refers to logical reasoning that draws conclusions or inferences from premises, evidence, or prior statements, representing the process of arriving at new understanding through systematic thinking and analysis. This term describes the fundamental cognitive process where people move from known information to logical conclusions, using reasoning skills to extend knowledge beyond immediately available facts. Illative reasoning appears in various forms including deductive reasoning (drawing specific conclusions from general principles), inductive reasoning (forming general principles from specific observations), and abductive reasoning (inferring the most likely explanations for observed phenomena). The quality of illative thinking depends on the validity of premises, the soundness of logical connections, and the appropriateness of reasoning methods for the type of problem being addressed. In grammar, illative case exists in some languages to indicate motion toward or into something, showing direction or purpose in ways that English typically expresses through prepositions. Educational contexts emphasize developing illative skills through logic training, critical thinking exercises, and systematic analysis of arguments and evidence. Understanding illative processes helps people evaluate reasoning quality, identify logical fallacies, and improve their own analytical abilities. The concept is fundamental to scientific thinking, legal reasoning, and everyday problem-solving where conclusions must be supported by appropriate evidence and reasoning.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-LAY-tiv',
                'etymology': 'From Latin "illativus," from "illatus" (brought in), from "inferre" (to bring in, infer).',
                'language_origins': 'Latin',
                'example_sentence': 'The detective\'s _______ reasoning led him from the scattered clues to a logical conclusion about the crime.',
                'memory_tip': 'Remember "ILLATIVE" - sounds like "ILL-ative," using reasoning to cure the illness of not knowing by drawing logical conclusions.'
            },
            'illicitly': {
                'definition': 'Illicitly is an adverb describing actions performed in ways that violate laws, rules, or accepted moral standards, emphasizing the forbidden, unauthorized, or improper nature of the behavior. This term applies to activities that are conducted secretly or deceptively because they are prohibited, unethical, or socially unacceptable. Illicit activities might include illegal drug trafficking, unauthorized access to restricted information, adultery, tax evasion, or any behavior that deliberately violates established prohibitions. The adverb emphasizes not just the act itself but the manner of conducting it—typically involving secrecy, deception, or attempts to avoid detection by authorities or social groups. Legal contexts distinguish between actions that are merely irregular and those that are illicitly conducted with knowledge of their prohibited status and intent to evade consequences. The term carries moral judgment, suggesting not just rule-breaking but deliberate wrongdoing that undermines social order, trust, or ethical standards. Understanding illicit behavior involves recognizing the difference between mistakes and deliberate violations, as well as the social and legal mechanisms designed to discourage such conduct. The concept highlights the importance of following established rules and ethical standards for maintaining social cooperation and trust.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ih-LIS-it-lee',
                'etymology': 'From "illicit" (from Latin "illicitus" meaning "not permitted") plus adverbial suffix "-ly."',
                'language_origins': 'Latin',
                'example_sentence': 'The investigation revealed that funds had been _______ transferred to offshore accounts to avoid tax obligations.',
                'memory_tip': 'Remember "ILLICITLY" - ILL + LICITLY, doing something in an ill (bad) way that\'s not licit (legal), acting illegally or improperly.'
            },
            'illinois': {
                'definition': 'Illinois is a state in the Midwestern United States, known for its diverse geography including prairie landscapes, the Great Lakes shoreline, major rivers, and significant urban centers including Chicago, the third-largest city in the United States. This state plays crucial roles in American agriculture, manufacturing, transportation, and culture, serving as a major hub for commerce and industry in the heartland. Illinois is famous for its agricultural productivity, particularly corn and soybean production, as well as its livestock farming that contributes significantly to the national food supply. The state\'s history includes important roles in westward expansion, the Civil War, industrial development, and social movements that shaped American society. Chicago serves as a major financial, cultural, and transportation center, hosting important institutions including major universities, museums, architectural landmarks, and the Chicago Board of Trade. Illinois politics have produced numerous national leaders including several U.S. presidents, reflecting the state\'s importance in American political development. The state\'s geography includes the Mississippi River on its western border and Lake Michigan on its northeastern shore, providing important transportation and economic opportunities. Understanding Illinois involves appreciating its role in American agriculture, industry, politics, and culture as a representative of Midwestern values and contributions to national development.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'il-uh-NOY',
                'etymology': 'From French adaptation of the Illinois Native American tribal name, possibly meaning "tribe of superior men."',
                'language_origins': 'Native American (via French)',
                'example_sentence': 'The agriculture students studied farming techniques used throughout _______ to understand Midwest crop production methods.',
                'memory_tip': 'Remember "ILLINOIS" - pronounced "ill-uh-NOY," the Midwest state with Chicago and lots of farmland, named after a Native American tribe.'
            },
            'illuminates': {
                'definition': 'Illuminates is the third-person singular present tense of the verb illuminate, meaning to light up, brighten, or make clear and understandable through explanation, example, or insight. In literal contexts, illuminating involves providing light to make objects visible, whether through natural sunlight, artificial lighting, or other light sources that reveal details and enable clear vision. Metaphorically, illuminating means clarifying complex ideas, revealing hidden aspects of situations, or helping others understand difficult concepts through clear explanation, insightful analysis, or enlightening examples. Educational contexts frequently involve teachers who illuminate subjects for students by making abstract concepts concrete, connecting new information to familiar experiences, and providing perspectives that enhance understanding. Research illuminates topics by uncovering new information, revealing patterns, or providing evidence that clarifies previously mysterious phenomena. Artistic and literary works can illuminate aspects of human experience, social conditions, or emotional truths that help audiences gain deeper understanding of themselves and their world. The process of illumination often involves removing confusion, dispelling ignorance, or overcoming mental barriers that prevent clear understanding. Understanding illumination involves recognizing both the literal importance of light for vision and the metaphorical importance of insight for knowledge and wisdom.',
                'part_of_speech': 'verb (third person singular)',
                'pronunciation_guide': 'ih-LOO-muh-nayts',
                'etymology': 'From Latin "illuminatus," past participle of "illuminare," from "in-" (in) and "lumen" (light).',
                'language_origins': 'Latin',
                'example_sentence': 'The researcher\'s work _______ important connections between environmental factors and public health outcomes.',
                'memory_tip': 'Remember "ILLUMINATES" - ILLUMIN (light up) + ATES (does), someone or something that lights up or makes clear and understandable.'
            },
            'illusionist': {
                'definition': 'Illusionist refers to a performer who specializes in creating illusions, magic tricks, and seemingly impossible feats that entertain audiences by challenging their perception of reality through skillful manipulation of attention, props, and psychological principles. These entertainment professionals master techniques including sleight of hand, misdirection, mechanical devices, and psychological manipulation to create experiences that appear to defy natural laws while actually relying on carefully practiced skills and scientific principles. Professional illusionists often develop signature performances, distinctive styles, and theatrical personas that enhance the entertainment value of their acts while maintaining the mystery essential to effective magic. The craft requires extensive practice, understanding of psychology and perception, performance skills, and often custom-built props or equipment designed to enable specific illusions. Different types of illusionists include close-up magicians who perform intimate tricks, stage magicians who create large-scale illusions, mentalists who focus on psychological effects, and escape artists who specialize in seemingly impossible escapes. Historical illusionists have contributed to both entertainment and scientific understanding by exploring principles of perception, attention, and human psychology. Modern illusionists often combine traditional techniques with contemporary technology to create new forms of magical entertainment. Understanding illusionism involves appreciating both the entertainment value and the skill, creativity, and psychological insight required to create effective magical experiences.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-LOO-zhuh-nist',
                'etymology': 'From "illusion" (from Latin "illusio" meaning "mockery" or "deception") plus suffix "-ist" indicating practitioner.',
                'language_origins': 'Latin',
                'example_sentence': 'The talented _______ amazed the audience by making a car disappear on stage and reappear in the theater lobby.',
                'memory_tip': 'Remember "ILLUSIONIST" - ILLUSION + IST, someone who creates illusions and magic tricks to entertain and amaze audiences.'
            },
            'illustrator': {
                'definition': 'Illustrator refers to a visual artist who creates images, drawings, paintings, or digital artwork to accompany, explain, or enhance written text, ideas, or concepts in books, magazines, advertisements, and other media. These creative professionals combine artistic skill with communication abilities to translate abstract ideas, stories, or information into visual form that engages viewers and supports understanding. Illustrators work in various styles and media including traditional painting and drawing, digital art, photography, collage, and mixed media techniques to create images appropriate for their intended audiences and purposes. Different specializations include children\'s book illustration, scientific and technical illustration, fashion illustration, editorial illustration for newspapers and magazines, and commercial illustration for advertising and marketing. The profession requires not only artistic ability but also understanding of design principles, communication goals, client needs, and production processes for various publishing and media formats. Modern illustrators often use digital tools and software to create, modify, and deliver artwork efficiently while maintaining artistic quality and meeting deadlines. Educational backgrounds typically include art training, though successful illustrators may also have knowledge in specific subject areas they frequently illustrate. Understanding illustration involves appreciating both the artistic and communication aspects of visual storytelling and information design.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IL-uh-stray-ter',
                'etymology': 'From Latin "illustrare" (to light up, make clear) plus suffix "-or" indicating one who performs the action.',
                'language_origins': 'Latin',
                'example_sentence': 'The children\'s book _______ created whimsical drawings that perfectly captured the magical atmosphere of the fairy tale.',
                'memory_tip': 'Remember "ILLUSTRATOR" - ILLUSTR (to make clear with pictures) + ATOR (one who does), someone who makes ideas clear through artwork.'
            },
            'illustrious': {
                'definition': 'Illustrious describes people, achievements, or institutions that are highly distinguished, renowned, and respected for exceptional accomplishments, noble character, or outstanding contributions to their fields. This adjective suggests not merely success but greatness that brings lasting honor, recognition, and admiration from others. Illustrious careers involve significant achievements that stand the test of time and influence future generations, while illustrious institutions maintain reputations for excellence, integrity, and important contributions to society. The term implies a combination of achievement and moral worth, suggesting that true distinction comes not just from success but from honorable conduct and meaningful contributions to human welfare. Historical figures described as illustrious typically demonstrate exceptional talent, moral character, and positive impact that earns them lasting respect and remembrance. Illustrious reputations are built over time through consistent excellence, ethical behavior, and achievements that benefit others rather than merely serving personal interests. The concept emphasizes that genuine distinction involves both exceptional ability and the use of that ability for worthy purposes. Understanding what makes someone or something illustrious involves recognizing the difference between temporary fame and lasting honor, between personal success and meaningful contribution to human progress.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-LUS-tree-uhs',
                'etymology': 'From Latin "illustris" meaning "bright" or "distinguished," from "illustrare" (to light up, make famous).',
                'language_origins': 'Latin',
                'example_sentence': 'The university\'s _______ history included Nobel Prize winners, groundbreaking research, and graduates who became world leaders.',
                'memory_tip': 'Remember "ILLUSTRIOUS" - ILLUSTR (bright/distinguished) + IOUS, so bright and distinguished that they shine with fame and honor.'
            },
            'imagery': {
                'definition': 'Imagery refers to vivid and descriptive language that appeals to the senses and creates mental pictures, sounds, smells, tastes, or tactile sensations in readers\' or listeners\' minds. This literary and rhetorical technique uses concrete, specific details and figurative language to help audiences visualize, experience, and emotionally connect with abstract ideas, stories, or concepts. Effective imagery goes beyond mere description to evoke sensory experiences that make writing more engaging, memorable, and emotionally powerful. Different types of imagery include visual (sight), auditory (sound), olfactory (smell), gustatory (taste), tactile (touch), and kinesthetic (movement) elements that work together to create rich, multi-dimensional experiences for audiences. Poetry, literature, and creative writing rely heavily on imagery to create atmosphere, establish mood, develop themes, and help readers form emotional connections with characters and situations. The term also applies to visual representations in art, photography, film, and digital media where images convey meaning, emotion, and information through visual elements. Psychological and therapeutic contexts use guided imagery techniques to help people relax, visualize positive outcomes, or process emotional experiences through intentional mental visualization. Understanding imagery involves recognizing both its artistic functions in creative expression and its psychological power to influence emotions, memory, and understanding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IM-ij-ree',
                'etymology': 'From "image" (from Latin "imago" meaning "copy" or "likeness") plus suffix "-ry" indicating collection or practice.',
                'language_origins': 'Latin',
                'example_sentence': 'The poet\'s vivid _______ of autumn leaves and crisp air helped readers feel transported to the peaceful forest setting.',
                'memory_tip': 'Remember "IMAGERY" - IMAGE + RY, the collection of word pictures and sensory details that create images in your mind.'
            },
            'imagined': {
                'definition': 'Imagined is the past tense of imagine, describing the mental process of forming pictures, ideas, or concepts in the mind that are not immediately present to the senses or not necessarily based on reality. This cognitive ability allows people to visualize possibilities, create fictional scenarios, plan future actions, or explore creative ideas that extend beyond immediate experience. Imagined scenarios can include memories of past events (though these may be altered by imagination), anticipations of future possibilities, creative inventions, problem-solving visualizations, or purely fictional constructs. The capacity for imagination is fundamental to human creativity, enabling artistic expression, scientific innovation, technological development, and social progress through envisioning possibilities that don\'t yet exist. Imagined experiences can feel emotionally real even when they are completely fictional, demonstrating the power of mental imagery to influence feelings, decisions, and behavior. Educational applications include encouraging students to imagine historical events, scientific processes, or literary scenarios to enhance understanding and engagement. Therapeutic uses involve guided imagery to help people manage stress, visualize healing, or process emotional experiences. Understanding imagination involves recognizing both its creative potential and its limitations, as well as the importance of distinguishing between imagined and real experiences when making decisions.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'ih-MAJ-ind',
                'etymology': 'From Latin "imaginari," from "imago" meaning "image" or "likeness."',
                'language_origins': 'Latin',
                'example_sentence': 'She _______ herself walking through the ancient castle as she read the historical novel\'s detailed descriptions.',
                'memory_tip': 'Remember "IMAGINED" - IMAGE + INED (past tense), having formed mental images or pictures in your mind of something.'
            },
            'imaret': {
                'definition': 'Imaret refers to a charitable institution in the Ottoman Empire and other Islamic societies that provided free meals, lodging, and sometimes education to travelers, the poor, students, and religious pilgrims. These establishments served important social welfare functions, demonstrating Islamic principles of charity and community support while facilitating trade, travel, and religious activities throughout the empire. Imarets were typically funded by wealthy individuals, religious foundations, or the state as acts of religious devotion and social responsibility, creating networks of support for people in need. The institutions often included kitchens capable of preparing large quantities of food, dining areas, sleeping quarters, and sometimes schools or libraries that served broader educational purposes. Different imarets served various populations including general travelers, specific religious or ethnic groups, students attending nearby schools, or local poor communities that depended on regular meal services. The system represented a sophisticated approach to social welfare that combined religious obligation with practical social needs, creating infrastructure that supported both individual welfare and broader social stability. Historical imarets played crucial roles in urban development, often becoming centers of community activity and social organization. Understanding imarets involves appreciating their role in Islamic social organization and their contributions to historical systems of charity, education, and community support.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-mah-RET',
                'etymology': 'From Turkish "imaret," from Arabic "imara" meaning "building" or "construction," referring to charitable buildings.',
                'language_origins': 'Arabic, Turkish',
                'example_sentence': 'The historical _______ served thousands of free meals daily to travelers and the poor throughout the Ottoman period.',
                'memory_tip': 'Remember "IMARET" - sounds like "I-MA-RET," Islamic charitable institutions where "I may rest" and get free food and lodging.'
            },
            'imbibe': {
                'definition': 'Imbibe means to drink, absorb, or take in liquid, ideas, or influences, often implying more than casual consumption but rather deliberate absorption or assimilation of what is being received. In its most common usage, imbibe refers to drinking alcoholic beverages, though it can apply to any liquid consumption and often carries connotations of social drinking or ceremonial consumption. The term extends metaphorically to describe absorbing knowledge, ideas, cultural influences, or attitudes through exposure, study, or social interaction. People imbibe wisdom from mentors, cultural values from their communities, or artistic inspiration from various sources they encounter. The word suggests active reception rather than passive exposure, implying that the person is consciously or unconsciously taking in and incorporating what they encounter. Educational contexts involve students imbibing knowledge through lectures, reading, and discussion, while cultural contexts involve people imbibing traditions, values, and practices from their social environments. The process of imbibing can be gradual and cumulative, as when someone slowly absorbs the atmosphere of a new culture, or immediate and intense, as when someone drinks deeply from a fountain of new knowledge. Understanding imbibing involves recognizing both its literal application to drinking and its broader meaning of absorbing and internalizing various influences and experiences.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'im-BAHYB',
                'etymology': 'From Latin "imbibere," from "in-" (in) and "bibere" (to drink), literally meaning "to drink in."',
                'language_origins': 'Latin',
                'example_sentence': 'The students eagerly _______ the professor\'s insights about classical literature during the inspiring lecture series.',
                'memory_tip': 'Remember "IMBIBE" - IM (into) + BIBE (drink), to drink into yourself, absorbing liquids, knowledge, or influences.'
            },
            'imbroglio': {
                'definition': 'Imbroglio refers to a complicated, confusing, or embarrassing situation involving misunderstandings, conflicts, or entangled relationships that are difficult to resolve or escape. This term describes scenarios where multiple factors, personalities, or issues become so intertwined that finding clear solutions or assigning responsibility becomes extremely challenging. Imbroglios often involve interpersonal conflicts, political disputes, legal complications, or business entanglements where different parties have conflicting interests, mismatched expectations, or incompatible goals that create ongoing tension and confusion. The word suggests not just complexity but also a messy, awkward quality that makes the situation uncomfortable or embarrassing for those involved. Personal imbroglios might involve family disputes, romantic complications, or social misunderstandings that spiral beyond simple resolution, while political imbroglios involve scandals, policy conflicts, or diplomatic complications that create lasting problems. The term implies that the situation has grown beyond its original scope or importance, taking on a life of its own that continues to create difficulties. Resolving imbroglios often requires patience, skilled negotiation, willingness to compromise, and sometimes acceptance that perfect solutions may not be possible. Understanding imbroglios involves recognizing how small problems can escalate into major complications when communication fails, interests conflict, or emotions override rational problem-solving.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-BROH-lee-oh',
                'etymology': 'From Italian "imbroglio" meaning "confusion" or "tangle," from "imbrogliare" (to entangle).',
                'language_origins': 'Italian',
                'example_sentence': 'The diplomatic _______ involved three countries, conflicting treaties, and years of misunderstandings that required careful negotiation to resolve.',
                'memory_tip': 'Remember "IMBROGLIO" - sounds like "IM-BROIL-io," a situation where you\'re embroiled (tangled up) in complications and confusion.'
            },
            'imitate': {
                'definition': 'Imitate means to copy, mimic, or reproduce the actions, speech, appearance, or behavior of someone or something else, often as a way of learning, showing respect, or achieving similar results. This fundamental human behavior appears in various contexts from child development, where imitation is a primary learning mechanism, to professional training where students copy expert techniques to develop skills. Imitation can be conscious and deliberate, as when actors study other performers to improve their craft, or unconscious, as when people naturally adopt speech patterns or mannerisms from those around them. The practice serves important functions in education, skill development, artistic expression, and social bonding, allowing people to learn complex behaviors without starting from zero. Different types of imitation include exact copying (reproducing something precisely), adaptive imitation (modifying what is copied to fit new circumstances), and creative imitation (using copied elements as inspiration for original work). While imitation is essential for learning and cultural transmission, it becomes problematic when it involves plagiarism, fraud, or inappropriate copying that violates intellectual property rights or deceives others. Understanding imitation involves recognizing both its value as a learning tool and its potential problems when it replaces original thinking or involves dishonest representation.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'IM-uh-tayt',
                'etymology': 'From Latin "imitatus," past participle of "imitari" meaning "to copy" or "mimic."',
                'language_origins': 'Latin',
                'example_sentence': 'The young artist learned to paint by carefully trying to _______ the brush techniques of master painters.',
                'memory_tip': 'Remember "IMITATE" - sounds like "I\'M-IT-ATE," like saying "I\'m it" and then copying what "it" does.'
            },
            'imitative': {
                'definition': 'Imitative describes behavior, art, or characteristics that copy, mimic, or reproduce elements from other sources rather than being entirely original or innovative. This adjective can apply to both positive contexts, such as learning through imitation, and potentially negative contexts, such as unoriginal artistic work that lacks creativity. Imitative behavior is natural and essential in human development, allowing children to learn language, social skills, and cultural practices by copying adults and peers. In artistic contexts, imitative work might demonstrate technical skill while raising questions about originality and creative value, with some imitative art being respected as homage or study pieces while other imitative work is criticized as derivative. Educational settings often involve imitative exercises where students learn by copying examples, practicing established techniques, or following proven methods before developing their own approaches. The term can describe anything from conscious copying for learning purposes to unconscious adoption of styles, mannerisms, or approaches that reflect surrounding influences. Understanding imitative involves recognizing the difference between learning through imitation (which is valuable and necessary) and remaining permanently imitative (which may limit growth and creativity). Cultural contexts influence how imitative behavior is valued, with some traditions emphasizing faithful reproduction of established forms while others prioritize innovation and originality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IM-uh-tay-tiv',
                'etymology': 'From Latin "imitativus," from "imitatus" (copied) plus suffix "-ive" indicating tendency or quality.',
                'language_origins': 'Latin',
                'example_sentence': 'The student\'s early paintings were _______ of famous works, but gradually developed into a distinctive personal style.',
                'memory_tip': 'Remember "IMITATIVE" - IMITATE + IVE, having the quality of copying or mimicking others rather than being original.'
            },
            'immediate': {
                'definition': 'Immediate describes something that occurs without delay, intervening time, or intermediate steps, emphasizing the direct, instant, or urgent nature of actions, responses, or relationships. This concept applies to various contexts including time (happening right now), space (directly adjacent or nearby), causation (direct effects without intervening factors), and relationships (direct connections without intermediaries). Immediate responses suggest quick reaction times and prompt decision-making, while immediate needs require urgent attention that cannot be postponed. The term often indicates priority, suggesting that immediate concerns take precedence over less urgent matters that can be addressed later. In emergency situations, immediate action is essential for preventing harm or minimizing damage, making quick response capabilities crucial for safety and effectiveness. Medical contexts distinguish between immediate treatment needs (life-threatening conditions requiring instant attention) and conditions that can wait for scheduled care. Communication often requires immediate responses to maintain effectiveness and show respect for others\' time and attention. Understanding immediacy involves recognizing when quick action is essential versus when careful deliberation is more appropriate, balancing urgency with quality in decision-making and response.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-MEE-dee-it',
                'etymology': 'From Latin "immediatus," from "in-" (not) and "mediatus" (intervening), meaning "not intervening."',
                'language_origins': 'Latin',
                'example_sentence': 'The patient required _______ surgery to address the life-threatening condition that could not wait for scheduled treatment.',
                'memory_tip': 'Remember "IMMEDIATE" - IM (not) + MEDIATE (in between), with nothing in between, happening right now without delay.'
            },
            'immie': {
                'definition': 'Immie is a colloquial term for a type of marble, specifically referring to an imitation agate marble made from glass or other materials rather than genuine agate stone. These marbles were commonly used in children\'s games and marble collecting, representing affordable alternatives to more expensive genuine agate marbles. The term reflects the material\'s nature as an imitation of natural agate, which features distinctive banded patterns and colors that manufacturers attempted to reproduce in glass marbles. Marble games have been popular children\'s activities for centuries, with different types of marbles having specific names, values, and uses in various games and trading activities. Immies typically featured swirled patterns and colors designed to mimic the appearance of natural agate, though they were less valuable than genuine stone marbles or other premium types. The word represents part of the specialized vocabulary that developed around marble collecting and playing, where different marble types had distinct names, characteristics, and social significance among children. Understanding immie involves appreciating both the material culture of childhood games and the economic factors that led to the production of imitation versions of more expensive natural materials. The term reflects how children\'s play activities developed their own technical vocabularies and value systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IM-ee',
                'etymology': 'From "imitation" + diminutive suffix, referring to marbles that imitate agate patterns.',
                'language_origins': 'English (colloquial)',
                'example_sentence': 'The children traded marbles in the schoolyard, with the colorful _______ being popular for their swirled patterns.',
                'memory_tip': 'Remember "IMMIE" - short for "imitation," a type of marble that imitates the look of more expensive agate marbles.'
            },
            'imminent': {
                'definition': 'Imminent describes something that is about to happen very soon, emphasizing the immediate threat, arrival, or occurrence of events that cannot be delayed or avoided. This adjective suggests that the timing is so close that preparation, prevention, or alternative responses may no longer be possible or effective. Imminent dangers require immediate action to prevent harm, while imminent opportunities demand quick decision-making to avoid missing important chances. The term often appears in contexts involving weather warnings (imminent storms), medical emergencies (imminent cardiac events), legal proceedings (imminent deadlines), or military situations (imminent attacks). Understanding imminent involves recognizing the difference between remote possibilities and immediate threats that require urgent response. The concept creates urgency by indicating that waiting or deliberating further may result in missed opportunities or increased risks. Emergency planning and risk management focus heavily on identifying imminent threats and developing rapid response capabilities to address situations that require immediate action. The word distinguishes between theoretical future events and practical immediate concerns that demand current attention and resources. Recognizing imminent situations helps people prioritize actions, allocate resources appropriately, and respond effectively to time-critical circumstances.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IM-uh-nuhnt',
                'etymology': 'From Latin "imminens," present participle of "imminere" meaning "to overhang" or "threaten."',
                'language_origins': 'Latin',
                'example_sentence': 'The weather service issued urgent warnings about the _______ tornado that was expected to reach the city within minutes.',
                'memory_tip': 'Remember "IMMINENT" - sounds like "I\'M-IN-IT," you\'re in it now because something threatening is about to happen immediately.'
            },
            'immiscible': {
                'definition': 'Immiscible describes liquids that cannot be mixed or combined to form a homogeneous solution, instead remaining separate even when shaken or stirred together. This chemical property results from differences in molecular polarity, density, or other physical characteristics that prevent complete mixing between different substances. Common examples include oil and water, which remain separate due to their different polarities, with oil molecules being hydrophobic (water-repelling) while water molecules are polar and form hydrogen bonds with each other. Understanding immiscibility is crucial in chemistry, cooking, manufacturing, and environmental science, where the behavior of different liquid combinations affects processes, products, and outcomes. Industrial applications use immiscible liquids for extraction processes, where desired compounds are selectively dissolved in one liquid phase while unwanted materials remain in another phase. Environmental concerns arise when immiscible pollutants like oil spills create persistent contamination because the pollutants don\'t dissolve into surrounding water and remain as separate phases. The concept helps explain why certain cleaning products are effective (using emulsifiers to temporarily combine immiscible substances) and why some mixtures naturally separate over time. Laboratory techniques often rely on immiscible solvents to separate and purify chemical compounds through extraction and separation procedures.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-MIS-uh-buhl',
                'etymology': 'From Latin "in-" (not) and "miscere" (to mix), literally meaning "not able to be mixed."',
                'language_origins': 'Latin',
                'example_sentence': 'The chemistry students observed that oil and water are _______ liquids that separate into distinct layers.',
                'memory_tip': 'Remember "IMMISCIBLE" - IM (not) + MISCIBLE (mixable), liquids that are not able to mix together, like oil and water.'
            },
            'immiscibletoroidal': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "immiscible" (liquids that cannot mix together) with "toroidal" (having a doughnut or ring shape). This type of parsing error occurs when PDF text extraction software fails to properly separate adjacent words, especially when formatting changes between lines, columns, or text blocks. The combination creates a nonsensical term that doesn\'t exist in standard dictionaries and demonstrates the challenges of processing digitized text from various sources. Such errors are particularly common when dealing with documents that have complex layouts, multiple columns, or inconsistent formatting that confuses automated text extraction systems. The original document likely contained separate references to immiscible liquids (chemistry concept) and toroidal shapes (geometry concept), which were erroneously combined during the digitization process. This highlights the importance of implementing quality control measures and error detection systems when processing large datasets extracted from PDF documents. Careful validation and manual review remain essential for ensuring data accuracy in educational and reference applications where precise information is crucial for learning and understanding scientific concepts.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'N/A (invalid word)',
                'etymology': 'Combined word error: "immiscible" + "toroidal" merged during PDF parsing.',
                'language_origins': 'PDF parsing error',
                'example_sentence': 'The word _______ does not exist in English dictionaries and appears to be a PDF processing error combining two separate scientific terms.',
                'memory_tip': 'Remember "IMMISCIBLETOROIDAL" - this is a PDF parsing error combining IMMISCIBLE (unmixable liquids) + TOROIDAL (doughnut shape) into one invalid word.'
            },
            'immobilize': {
                'definition': 'Immobilize means to prevent movement or make unable to move, whether through physical restraint, medical treatment, mechanical devices, or other methods that restrict mobility. This action can be intentional and beneficial, such as medical immobilization to allow injuries to heal properly, or unintentional and problematic, such as mechanical failures that immobilize vehicles. Medical applications include immobilizing broken bones with casts or splints, stabilizing spinal injuries during transport, or using medications that temporarily immobilize patients during surgery. Military and security contexts involve immobilizing vehicles, weapons, or personnel to neutralize threats or prevent escape. The term also applies to making systems, organizations, or processes unable to function effectively, such as computer viruses that immobilize networks or bureaucratic procedures that immobilize decision-making. Psychological applications include discussing how fear, depression, or overwhelming situations can immobilize people by preventing them from taking action or making decisions. Emergency response often involves both protective immobilization (stabilizing injured people) and tactical immobilization (stopping dangerous situations). Understanding immobilization involves recognizing both its therapeutic applications and its potential problems, as unnecessary immobilization can lead to complications while appropriate immobilization can prevent further injury and promote healing.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-MOH-buh-lahyz',
                'etymology': 'From "immobile" (from Latin "immobilis" meaning "not movable") plus suffix "-ize" meaning "to make."',
                'language_origins': 'Latin',
                'example_sentence': 'The paramedics needed to _______ the patient\'s neck and spine before safely transporting him to the hospital.',
                'memory_tip': 'Remember "IMMOBILIZE" - IM (not) + MOBILE + IZE (make), to make something not mobile or unable to move.'
            },
            'immoderate': {
                'definition': 'Immoderate describes behavior, opinions, or actions that are excessive, extreme, or lacking in restraint, going beyond reasonable, appropriate, or healthy limits. This adjective applies to various contexts where balance and moderation would be more beneficial, but instead, people engage in too much or too little of particular activities or hold positions that are unreasonably extreme. Immoderate eating, drinking, spending, or working can lead to health problems, financial difficulties, or relationship issues when people consistently exceed reasonable limits. The term can describe emotional responses that are disproportionate to situations, political views that are extremely radical, or lifestyle choices that ignore practical constraints and long-term consequences. Immoderate behavior often reflects poor self-control, lack of awareness about appropriate limits, or prioritizing short-term gratification over long-term well-being. Different cultures have varying standards for what constitutes immoderate behavior, with some societies emphasizing strict moderation while others allowing more individual freedom in personal choices. Understanding immoderate behavior involves recognizing the importance of balance, self-regulation, and consideration of consequences in making decisions about how to live and act. The concept highlights the value of moderation as a principle for maintaining health, relationships, and personal effectiveness.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-MOD-er-it',
                'etymology': 'From Latin "immoderatus," from "in-" (not) and "moderatus" (moderate), meaning "not moderate."',
                'language_origins': 'Latin',
                'example_sentence': 'His _______ spending on luxury items eventually led to serious financial problems that affected his entire family.',
                'memory_tip': 'Remember "IMMODERATE" - IM (not) + MODERATE, behavior that is not moderate but excessive and lacking restraint.'
            },
            'immolate': {
                'definition': 'Immolate means to sacrifice or offer as a sacrifice, typically by killing or destroying, often in religious or ritualistic contexts where the act is intended to honor deities, demonstrate devotion, or achieve spiritual goals. This term historically applied to religious ceremonies where animals, objects, or in extreme cases people were sacrificed to gods or spiritual forces as acts of worship, appeasement, or seeking divine favor. The word can extend to any act of sacrificing something valuable for a greater cause, principle, or belief, including modern contexts where people sacrifice personal interests, careers, or resources for ideological, political, or moral purposes. Self-immolation specifically refers to the act of sacrificing oneself, often through fire, as a form of protest, religious devotion, or ultimate demonstration of commitment to a cause. The concept involves the deliberate destruction of something valuable (including one\'s own life) as a meaningful act that serves purposes beyond mere destruction. Understanding immolation requires recognizing both its historical religious significance and its continued appearance in contexts involving extreme sacrifice for deeply held beliefs or causes. The term reflects the human capacity for ultimate sacrifice and the powerful symbolic meaning that such acts can carry in religious, political, and social contexts.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'IM-uh-layt',
                'etymology': 'From Latin "immolatus," past participle of "immolare" meaning "to sacrifice," from "mola" (meal, referring to ritual meal).',
                'language_origins': 'Latin',
                'example_sentence': 'The ancient priest would _______ offerings to the gods during important religious ceremonies and festivals.',
                'memory_tip': 'Remember "IMMOLATE" - sounds like "I\'M-OBLATE," to oblate (sacrifice) something, especially in religious contexts.'
            },
            'immortality': {
                'definition': 'Immortality refers to the concept of living forever or existing eternally without death, decay, or end, representing one of humanity\'s most enduring fascinations and fears. This idea appears in various forms across cultures, religions, and philosophical traditions, including physical immortality (never dying), spiritual immortality (souls continuing after bodily death), and legacy immortality (being remembered forever through achievements or contributions). Religious concepts of immortality often involve souls existing eternally in afterlife states, while secular approaches might focus on achieving lasting impact through creative works, scientific discoveries, or social contributions that outlive individual lifespans. Scientific research increasingly explores biological approaches to extending human lifespan through genetic manipulation, medical interventions, and understanding aging processes, raising questions about the desirability and implications of dramatically extended or unlimited lifespans. Literary and philosophical treatments of immortality often explore both its potential benefits (unlimited time for learning, experiencing, and achieving) and its possible drawbacks (boredom, loss of meaning, social disruption). The concept influences human behavior through both the desire to achieve some form of immortality and the acceptance of mortality as fundamental to human experience. Understanding immortality involves examining both the appeal of endless existence and the role that mortality plays in giving life urgency, meaning, and value.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-awr-TAL-i-tee',
                'etymology': 'From "immortal" (from Latin "immortalis" meaning "not mortal") plus suffix "-ity" indicating quality or state.',
                'language_origins': 'Latin',
                'example_sentence': 'The philosopher explored whether achieving _______ would bring ultimate happiness or eventually become a burden.',
                'memory_tip': 'Remember "IMMORTALITY" - IM (not) + MORTAL + ITY, the quality of not being mortal, living forever without dying.'
            },
            'immunization': {
                'definition': 'Immunization refers to the medical process of making individuals immune or resistant to infectious diseases through vaccination or exposure to weakened, killed, or modified pathogens that stimulate the immune system to develop protective antibodies. This crucial public health intervention has dramatically reduced the incidence of many serious diseases including polio, measles, smallpox, and numerous other infections that previously caused widespread illness, disability, and death. The process works by introducing antigens (substances that trigger immune responses) in forms that allow the immune system to recognize and remember specific pathogens without causing the full disease, creating long-lasting protection against future encounters with those pathogens. Different types of immunization include live attenuated vaccines (weakened but living pathogens), inactivated vaccines (killed pathogens), subunit vaccines (specific pathogen components), and newer technologies like mRNA vaccines that instruct cells to produce specific antigens. Immunization programs require careful scheduling, population-wide coordination, and ongoing monitoring to ensure effectiveness and safety while maintaining high vaccination rates necessary for community immunity. Modern immunization faces challenges including vaccine hesitancy, global distribution inequities, emerging infectious diseases, and the need for ongoing research to develop new vaccines for evolving health threats.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-myuh-nuh-ZAY-shuhn',
                'etymology': 'From "immunize" (from Latin "immunis" meaning "exempt") plus suffix "-ation" indicating process or result.',
                'language_origins': 'Latin',
                'example_sentence': 'The public health campaign promoted childhood _______ as essential for preventing serious infectious diseases.',
                'memory_tip': 'Remember "IMMUNIZATION" - IMMUNE + IZATION, the process of making someone immune to diseases through vaccines.'
            },
            'immure': {
                'definition': 'Immure means to confine, imprison, or shut up within walls, literally or figuratively restricting someone\'s freedom of movement or action. This term historically referred to the practice of walling up people alive as a form of punishment or execution, though it now more commonly describes any form of imprisonment, confinement, or isolation. The word can apply to physical confinement in buildings, cells, or enclosed spaces, as well as metaphorical imprisonment through circumstances, obligations, or social constraints that prevent freedom of action or choice. Monastic contexts involve voluntary immurement where religious individuals choose to live in enclosed communities, dedicating themselves to spiritual pursuits while giving up worldly freedoms. The term can describe feeling trapped by circumstances such as debt, family obligations, or social expectations that limit personal choices and opportunities for change. Literary usage often involves characters who are immured by circumstances, relationships, or their own psychological barriers that prevent them from achieving their goals or expressing their true selves. Understanding immurement involves recognizing both literal forms of confinement and the various ways that people can become trapped or restricted in their daily lives. The concept highlights the importance of freedom and the various barriers that can limit human potential and happiness.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-MYOOR',
                'etymology': 'From Latin "immurare," from "in-" (in) and "murus" (wall), literally meaning "to wall in."',
                'language_origins': 'Latin',
                'example_sentence': 'The novelist felt _______ in her small apartment during the long winter, unable to travel or see friends.',
                'memory_tip': 'Remember "IMMURE" - IM (in) + MURE (wall), to wall someone in or confine them within barriers.'
            }
        }
        
        return batch_088_data.get(word.lower(), {
            'definition': 'Definition not available for this word.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': 'Pronunciation not available',
            'etymology': 'Etymology not available',
            'language_origins': 'Unknown',
            'example_sentence': 'Example sentence not available for _______.',
            'memory_tip': 'Memory tip not available for this word.'
        })

    def process_batch(self, input_file: str, output_file: str) -> None:
        print(f"Processing {input_file}...")
        
        try:
            df = pd.read_csv(input_file)
            
            processed_words = []
            word_count = 0
            
            for _, row in df.iterrows():
                word = str(row['word']).strip()
                if not word or word.lower() == 'nan':
                    continue
                    
                word_count += 1
                
                if self.is_error_word(word):
                    self.errors.append(self.detect_word_error(word))
                
                claude_data = self.get_comprehensive_claude_data(word)
                
                word_data = WordData(
                    word=word,
                    definition=claude_data['definition'],
                    part_of_speech=claude_data['part_of_speech'],
                    pronunciation_guide=claude_data['pronunciation_guide'],
                    etymology=claude_data['etymology'],
                    language_origins=claude_data['language_origins'],
                    example_sentence=claude_data['example_sentence'],
                    memory_tip=claude_data['memory_tip'],
                    phonetic_transparency=self.difficulty_calc.calculate_phonetic_transparency(word),
                    word_frequency=self.difficulty_calc.calculate_word_frequency(word),
                    morphological_complexity=self.difficulty_calc.calculate_morphological_complexity(word),
                    etymology_complexity=self.difficulty_calc.calculate_etymology_complexity(word)
                )
                
                processed_words.append(word_data)
            
            output_data = []
            for word_data in processed_words:
                output_data.append({
                    'word': word_data.word,
                    'definition': word_data.definition,
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.etymology,
                    'language_origins': word_data.language_origins,
                    'example_sentence': word_data.example_sentence,
                    'memory_tip': word_data.memory_tip,
                    'phonetic_transparency': word_data.phonetic_transparency,
                    'word_frequency': word_data.word_frequency,
                    'morphological_complexity': word_data.morphological_complexity,
                    'etymology_complexity': word_data.etymology_complexity,
                    'difficulty_level': None,
                    'source_difficulties': row.get('source_difficulties', ''),
                    'years': row.get('years', ''),
                    'source_files': row.get('source_files', ''),
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'etymology_source': 'Claude',
                    'example_sentence_source': 'Claude',
                    'audio_file_path': None,
                    'created_at': None,
                    'updated_at': None,
                    'alternative_spellings': None,
                    'related_words': None,
                    'usage_notes': None
                })
            
            output_df = pd.DataFrame(output_data)
            output_df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Successfully processed {word_count}/50 words to {output_file}")
            
            if self.errors:
                print(f"Found {len(self.errors)} error(s):")
                for error in self.errors:
                    print(f"  - {error}")
            
            print("Batch 088 processing completed successfully!")
            
        except Exception as e:
            print(f"Error processing batch 088: {str(e)}")
            raise

    def is_error_word(self, word: str) -> bool:
        error_patterns = [
            lambda w: len(w) > 20 and any(common in w.lower() for common in 
                ['difficulty', 'diligence', 'different', 'decision', 'development', 'discussion']),
            lambda w: any(combo in w.lower() for combo in 
                ['anearly', 'anadequate', 'anational', 'anhonest', 'anindependent']),
            lambda w: w.count('a') > 4 and len(w) > 15,
            lambda w: 'difficulty' in w.lower() and w.lower() != 'difficulty',
            lambda w: len([c for c in w if c.islower()]) > len(w) * 0.9 and len(w) > 25,
            lambda w: 'toroidal' in w.lower() and len(w) > 12 and w.lower() != 'toroidal',
            lambda w: 'immiscibletoroidal' in w.lower()
        ]
        
        return any(pattern(word) for pattern in error_patterns)

    def detect_word_error(self, word: str) -> str:
        if 'immiscibletoroidal' in word.lower():
            return f'{word}: Combined word error: "{word}" appears to be "immiscible" + "toroidal" merged together. This is likely a PDF parsing error where chemistry and geometry terminology were incorrectly combined.'
        
        if 'difficulty' in word.lower() and word.lower() != 'difficulty':
            parts = word.lower().split('difficulty')
            return f'{word}: Combined word error: "{word}" appears to be "{parts[0]}" + "difficulty" merged together. This is likely a PDF parsing error where two separate concepts were incorrectly combined.'
        
        common_endings = ['ness', 'tion', 'sion', 'ment', 'able', 'ible', 'ence', 'ance']
        for ending in common_endings:
            if word.lower().endswith(ending):
                base = word.lower()[:-len(ending)]
                if len(base) > 8:
                    return f'{word}: Possible combined word error: "{word}" may contain merged terms. This is likely a PDF parsing error where separate words were incorrectly combined.'
        
        return f'{word}: Combined word error: This appears to be multiple words merged together during PDF processing.'

if __name__ == "__main__":
    processor = Batch088Processor()
    input_file = "output/batch_088_words.csv"
    output_file = "output/batch_088_processed.csv"
    processor.process_batch(input_file, output_file)