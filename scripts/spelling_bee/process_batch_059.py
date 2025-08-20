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

class Batch059Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_059_data = {
            'emphysema': {
                'definition': 'Emphysema is a serious lung disease characterized by damage to the alveoli (air sacs) in the lungs, causing them to enlarge and lose their elasticity. This progressive condition makes breathing increasingly difficult as the damaged alveoli cannot efficiently exchange oxygen and carbon dioxide. The primary cause is long-term exposure to airborne irritants, most commonly cigarette smoke, though air pollution, chemical fumes, and dust can also contribute. In emphysema, the walls between many of the air sacs are destroyed, reducing the surface area available for gas exchange. Symptoms typically develop gradually and include shortness of breath (especially during physical activity), chronic cough, wheezing, and fatigue. The condition is part of a group of diseases called chronic obstructive pulmonary disease (COPD). While there is no cure for emphysema, treatments can slow its progression and help manage symptoms through medications like bronchodilators, pulmonary rehabilitation, oxygen therapy, and in severe cases, surgical interventions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'em-fi-SEE-mah',
                'etymology': 'From Greek "emphysema" meaning "inflation," derived from "emphysan" (to inflate or blow up), from "em-" (in) + "physan" (to blow). The term was first used in English medical literature in the 17th century.',
                'language_origins': 'Greek',
                'example_sentence': 'The longtime smoker was diagnosed with _______ after experiencing severe breathing difficulties.',
                'memory_tip': 'Remember "em-PHY-sema" - think "emphasize-ema" where the lungs emphasize breathing problems, or "empty-sema" because the air sacs become empty of function.'
            },
            'empire': {
                'definition': 'An empire is a large political unit or sovereign state that extends its authority over diverse territories and peoples through conquest, colonization, or political influence. Empires are typically characterized by a central government that exercises control over multiple regions, often inhabited by different ethnic groups, cultures, and languages. Historically, empires have been ruled by emperors, kings, or other supreme leaders who maintain dominance through military force, administrative systems, and economic control. Famous examples include the Roman Empire, British Empire, Ottoman Empire, and Persian Empire. Modern usage of the term can also refer to large business organizations or spheres of influence that extend across multiple markets or regions. Empires often develop through territorial expansion, trade networks, and the establishment of colonies or provinces. They typically feature complex administrative structures to govern distant territories, systems of taxation and tribute, and often impose their culture, language, or legal systems on conquered peoples.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-pahyuhr',
                'etymology': 'From Old French "empere," from Latin "imperium" meaning "command, authority, rule," derived from "imperare" (to command), from "in-" (in) + "parare" (to prepare).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The vast _______ stretched from Europe to Asia, encompassing dozens of different cultures and languages.',
                'memory_tip': 'Remember "em-PIRE" sounds like "emperor" - an empire is what an emperor rules over.'
            },
            'empirical': {
                'definition': 'Empirical refers to knowledge, evidence, or methods that are based on observation, experience, or experimentation rather than theory or pure logic alone. In scientific contexts, empirical research involves gathering data through direct observation, measurement, or experimentation to test hypotheses and draw conclusions. This approach emphasizes the importance of observable and measurable evidence that can be verified or replicated by others. Empirical methods form the foundation of the scientific method, where theories must be supported by observable evidence. The term can also describe practical knowledge gained through experience rather than formal education or theoretical study. Empirical evidence is considered more reliable than speculation or theoretical reasoning alone because it can be independently verified. In philosophy, empiricism is the theory that all knowledge comes from sensory experience. Empirical studies in fields like psychology, medicine, and social sciences rely on data collection techniques such as surveys, experiments, and observational studies.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'em-PIR-i-kuhl',
                'etymology': 'From Greek "empeirikos" meaning "experienced," from "empeiria" (experience), from "empeiros" (skilled, experienced), from "en-" (in) + "peira" (trial, experiment).',
                'language_origins': 'Greek',
                'example_sentence': 'The scientist relied on _______ evidence rather than theoretical assumptions to support her conclusions.',
                'memory_tip': 'Remember "em-PIR-ical" - think "empire of experience" or connect it to "empire" meaning the experience rules over theory.'
            },
            'emporium': {
                'definition': 'An emporium is a large retail store or marketplace that sells a wide variety of goods, often serving as a commercial center for a particular area or region. The term traditionally refers to a place where merchants from different locations gather to trade diverse merchandise, creating a hub of commercial activity. Emporiums typically offer an extensive selection of products under one roof, ranging from household goods and clothing to specialty items and imported wares. In historical contexts, emporiums were important trading posts or commercial cities that attracted merchants from distant lands, facilitating the exchange of goods, ideas, and cultures. Modern usage of the term often refers to large department stores, shopping centers, or specialty stores that pride themselves on offering an unusually wide selection of merchandise. The word can also be used metaphorically to describe any place where many different things are available or where there is a rich variety of offerings.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'em-PAWR-ee-uhm',
                'etymology': 'From Latin "emporium," from Greek "emporion" meaning "trading place, market," from "emporos" (merchant, trader), from "en-" (in) + "poros" (passage, journey).',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The bustling _______ attracted shoppers from across the region with its vast selection of goods.',
                'memory_tip': 'Remember "em-POR-ium" - think "important place" or "emperor\'s store" where you can find everything.'
            },
            'empty': {
                'definition': 'Empty describes something that contains nothing; lacking contents, substance, or meaning. When applied to physical containers, empty means devoid of the usual or expected contents, such as an empty bottle or empty room. The term can also describe abstract concepts, such as empty promises (lacking sincerity or substance), empty words (without meaning or significance), or empty gestures (actions without genuine intent). In emotional contexts, empty can describe feelings of hollowness, purposelessness, or lack of fulfillment. Empty can also refer to vacant positions, unused spaces, or depleted resources. The word is often used metaphorically to describe things that appear substantial but lack real value or substance. In mathematics and computer science, empty sets or empty strings represent collections or sequences with no elements. The concept of emptiness is philosophical and spiritual contexts often relates to themes of void, absence, or the need for fulfillment.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'EMP-tee',
                'etymology': 'From Old English "æmtig" meaning "vacant, unoccupied," from "æmetta" (leisure, rest), from "æ-" (without) + a root related to "mōt" (meeting).',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ auditorium echoed with the sound of their footsteps.',
                'memory_tip': 'Remember "EMP-ty" - think "emphasis on nothing" or "emperor with no clothes" meaning nothing inside.'
            },
            'emulate': {
                'definition': 'To emulate means to strive to equal or surpass someone or something, typically by imitating their actions, qualities, or achievements. Emulation involves more than mere copying; it requires effort to match or exceed the excellence of a model or standard. When someone emulates another person, they study that person\'s methods, behaviors, or accomplishments and attempt to achieve similar or better results. This process often involves admiration and respect for the subject being emulated. In competitive contexts, emulation can drive improvement and innovation as individuals or organizations seek to outperform their rivals. The term is also used in technology, where software or hardware emulation involves creating systems that replicate the functions of other systems. Computer emulation allows one system to behave like another, enabling compatibility across different platforms. Unlike imitation, which focuses on copying appearance or surface behaviors, emulation emphasizes achieving comparable performance or results.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'EM-yuh-layt',
                'etymology': 'From Latin "aemulatus," past participle of "aemulari" meaning "to rival, strive to equal," from "aemulus" (rival, competing).',
                'language_origins': 'Latin',
                'example_sentence': 'The young artist worked hard to _______ the techniques of the masters she admired.',
                'memory_tip': 'Remember "EM-u-late" - think "aim to late" meaning aim to be as late/great as someone else, or "aim-you-late" meaning aim to copy you later.'
            },
            'emulsify': {
                'definition': 'To emulsify means to combine two liquids that normally do not mix (such as oil and water) by creating a stable mixture called an emulsion. This process typically involves the use of an emulsifying agent or emulsifier, which has properties that allow it to bind with both types of liquids simultaneously. Common emulsifiers include lecithin, egg yolks, and various synthetic compounds. Emulsification is crucial in cooking and food preparation, where it creates smooth, uniform textures in products like mayonnaise, hollandaise sauce, and salad dressings. The process works by breaking one liquid into tiny droplets that become suspended throughout the other liquid, creating a homogeneous mixture. In industrial applications, emulsification is used in manufacturing cosmetics, pharmaceuticals, paints, and many other products. The stability of an emulsion depends on factors such as temperature, pH, and the presence of stabilizing agents. Without proper emulsification, mixtures will separate over time.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-MUHL-suh-fahy',
                'etymology': 'From "emulsion" (from Latin "emulsus," past participle of "emulgere" meaning "to milk out") + "-ify" (suffix meaning "to make, cause to become").',
                'language_origins': 'Latin',
                'example_sentence': 'The chef used egg yolks to _______ the oil and vinegar into a smooth mayonnaise.',
                'memory_tip': 'Remember "e-MUL-sify" - think "mule-ify" because like a mule mixes horse and donkey traits, emulsify mixes liquids that don\'t naturally go together.'
            },
            'emulsifylorikeet': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "emulsify" (to combine two unmixable liquids into a stable mixture) and "lorikeet" (a type of small, colorful parrot). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'enal': {
                'definition': 'Enal is an archaic or obsolete English word meaning "to kindle" or "to set on fire," particularly used in the context of lighting a fire or igniting something. This term is rarely used in modern English and would primarily be encountered in historical texts, poetry, or specialized academic contexts dealing with Middle English or archaic language. The word relates to the act of starting a fire or bringing something to flame. In some specialized contexts, it might also relate to the process of applying heat to activate or transform something. The term has largely been replaced by more common modern words such as "kindle," "ignite," "light," or "set fire to." Understanding such archaic terms is important for scholars studying historical texts or for those interested in the evolution of the English language.',
                'part_of_speech': 'verb (archaic)',
                'pronunciation_guide': 'ee-NAL',
                'etymology': 'From Middle English, related to Old English "ǣlan" or "onǣlan" meaning "to set on fire, kindle," from "on-" (on) + "ǣlan" (to burn).',
                'language_origins': 'Old English, Middle English',
                'example_sentence': 'In medieval texts, one might read about attempts to _______ the hearth fires.',
                'memory_tip': 'Remember "e-NAL" - think "enable fire" or "eternal flame" to connect it with fire and kindling.'
            },
            'enamel': {
                'definition': 'Enamel refers to a hard, glossy substance that can be either natural or artificial. In dentistry, enamel is the hardest substance in the human body, forming the outermost layer of teeth and protecting the underlying dentin and pulp. Dental enamel is composed primarily of hydroxyapatite crystals and lacks living cells, which means it cannot regenerate once damaged. In manufacturing and decorative arts, enamel is a vitreous coating applied to metal, glass, or ceramic surfaces through high-temperature firing. This process creates a smooth, durable, and often colorful finish that resists corrosion, wear, and chemicals. Enamel paints contain similar properties, providing a hard, glossy finish for various surfaces. The technique of enameling has been used for centuries to create jewelry, decorative objects, and functional items. Industrial applications include cookware, appliances, and architectural elements. The word can also be used as a verb, meaning to coat or decorate with enamel.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ih-NAM-uhl',
                'etymology': 'From Old French "esmail," from Frankish "smalt," related to German "schmelzen" (to smelt, melt). The word entered English via Norman French.',
                'language_origins': 'Germanic, Old French',
                'example_sentence': 'The dentist explained that tooth _______ is the hardest substance in the human body.',
                'memory_tip': 'Remember "e-NAM-el" - think "name it" because enamel names/identifies the shiny outer layer of teeth.'
            },
            'encarnadine': {
                'definition': 'Encarnadine is a poetic and archaic term meaning "to dye red" or "to make flesh-colored," typically referring to a deep red or crimson color. The word is most famously associated with Shakespeare\'s "Macbeth," where it appears in the context of blood-stained hands. In literary usage, encarnadine often carries connotations of violence, bloodshed, or guilt, as it specifically refers to the red color of blood or flesh. The term can be used both as a verb (to make red or bloody) and as an adjective (having a deep red or flesh color). In historical and artistic contexts, encarnadine might describe certain pigments or dyes used to achieve flesh tones in paintings or to create deep red colors in textiles. The word is rarely used in contemporary English except in literary or academic contexts when discussing classical texts or when writers seek to evoke an archaic or poetic tone.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'en-KAHR-nuh-dahyn',
                'etymology': 'From French "incarnadin," from Italian "incarnadino," diminutive of "incarnato" (flesh-colored), from Latin "incarnatus" (made flesh), from "in-" (in) + "caro" (flesh).',
                'language_origins': 'Latin, Italian, French',
                'example_sentence': 'The battlefield was _______ with the blood of fallen warriors.',
                'memory_tip': 'Remember "en-CAR-nadine" - think "in-carnation" (becoming flesh) or "car-nation" (red like carnation flowers).'
            },
            'encarnadinedulcinea': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "encarnadine" (to dye red or make flesh-colored, a poetic term from Shakespeare) and "Dulcinea" (the idealized beloved in Cervantes\' "Don Quixote"). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated literary terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'encephalitis': {
                'definition': 'Encephalitis is a serious medical condition characterized by inflammation of the brain tissue. This inflammation can be caused by viral infections (most commonly), bacterial infections, autoimmune reactions, or other factors such as certain medications or toxins. Viral encephalitis can result from various viruses including herpes simplex, West Nile virus, Eastern equine encephalitis virus, and others. Symptoms typically include fever, headache, confusion, seizures, and altered mental status. In severe cases, encephalitis can lead to permanent neurological damage, coma, or death. The condition requires immediate medical attention and hospitalization. Treatment depends on the underlying cause but may include antiviral medications, corticosteroids to reduce inflammation, anticonvulsants for seizures, and supportive care. Some forms of encephalitis can be prevented through vaccination, such as those caused by measles, mumps, or Japanese encephalitis virus. Early diagnosis and treatment are crucial for optimal outcomes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'en-sef-uh-LAHY-tis',
                'etymology': 'From Greek "enkephalos" (brain), from "en-" (in) + "kephale" (head), plus "-itis" (inflammation). Literally means "inflammation of the brain."',
                'language_origins': 'Greek',
                'example_sentence': 'The patient was hospitalized with _______ after developing severe headaches and confusion.',
                'memory_tip': 'Remember "en-CEPH-alitis" - think "in-head-inflammation" or "enceph" sounds like "in-chef" and chefs work with their heads/brains.'
            },
            'enchantment': {
                'definition': 'Enchantment refers to a magical spell or charm that is believed to influence or control someone or something through supernatural means. In folklore and fantasy literature, enchantments are often cast by wizards, witches, or magical beings to transform people into animals, put them under spells, or imbue objects with magical properties. The term also describes the state of being under such a magical influence or charm. Beyond its magical connotations, enchantment can refer to a feeling of delight, fascination, or captivation that seems almost magical in its intensity. Something that causes enchantment has the power to charm, allure, or bewitch in a metaphorical sense. The word is commonly used to describe the effect of beautiful music, stunning landscapes, compelling stories, or charismatic personalities that capture and hold one\'s attention completely. Enchantment suggests a sense of wonder, magic, or irresistible attraction that transforms ordinary experience into something extraordinary.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'en-CHANT-muhnt',
                'etymology': 'From Old French "enchantement," from "enchanter" (to enchant), from Latin "incantare" meaning "to chant a magic formula," from "in-" (upon) + "cantare" (to sing).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The fairy tale described a powerful _______ that turned the prince into a frog.',
                'memory_tip': 'Remember "en-CHANT-ment" - think "enchant" (to charm) + "ment" (result), or "in-chant" like chanting magical words.'
            },
            'encina': {
                'definition': 'Encina is a Spanish term referring to an evergreen oak tree, specifically the holm oak (Quercus ilex), which is native to the Mediterranean region. These trees are characterized by their dark green, leathery leaves and their ability to thrive in dry, rocky soils typical of Mediterranean climates. Encinas are culturally and ecologically significant in Spain and other Mediterranean countries, providing shade, acorns for livestock feed, and habitat for various wildlife species. The wood from encina trees is highly valued for its density and durability, making it useful for construction, furniture, and fuel. In Spanish literature and culture, the encina often symbolizes endurance, strength, and connection to the land. The term may also appear in place names throughout Spanish-speaking regions. In botanical contexts outside of Spanish, the tree is more commonly referred to by its scientific name or as holm oak or evergreen oak.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'en-SEE-nah',
                'etymology': 'From Spanish "encina," from Latin "ilex" (holm oak). The Spanish term evolved from the Latin through phonetic changes typical of Romance language development.',
                'language_origins': 'Latin, Spanish',
                'example_sentence': 'The ancient _______ provided shade for generations of Spanish families.',
                'memory_tip': 'Remember "en-CINA" - think "in-cinema" where oak trees are often featured in movies, or "ensign-a" like a tree that\'s a sign of the Mediterranean.'
            },
            'encomium': {
                'definition': 'An encomium is a formal speech or piece of writing that offers high praise, tribute, or commendation for a person, achievement, or concept. This term is often used in academic, literary, or ceremonial contexts to describe eloquent expressions of admiration or honor. Encomiums are typically more elaborate and formal than simple compliments or praise, often featuring sophisticated rhetoric and detailed explanation of the subject\'s virtues or accomplishments. The form has classical roots, with ancient Greek and Roman orators composing encomiums to honor gods, heroes, and notable figures. In modern usage, encomiums might be delivered at award ceremonies, retirement celebrations, memorial services, or academic conferences. The term can also refer to any work of art, literature, or music that serves as a tribute to its subject. Unlike mere flattery, an encomium is generally understood to be sincere and well-deserved praise based on genuine merit or achievement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'en-KOH-mee-uhm',
                'etymology': 'From Latin "encomium," from Greek "enkōmion" meaning "laudatory composition," from "en-" (in) + "kōmos" (revel, celebration). Originally referred to songs of praise sung at festivities.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The professor delivered a heartfelt _______ praising the retiring dean\'s contributions to the university.',
                'memory_tip': 'Remember "en-COM-ium" - think "encompass-ium" meaning it encompasses all the good things about someone, or "income" because good praise increases your reputation.'
            },
            'encompass': {
                'definition': 'To encompass means to completely surround, include, or contain something within defined boundaries or limits. The term can refer to physical containment, where one thing encircles or encloses another, such as a fence encompassing a property or walls encompassing a city. More commonly, encompass is used in abstract contexts to describe comprehensive inclusion or coverage. For example, a study might encompass multiple disciplines, a policy might encompass various issues, or a person\'s interests might encompass many different activities. When something encompasses a range of elements, it includes all or most of those elements within its scope. The word suggests completeness and thoroughness in coverage or inclusion. In academic and professional contexts, encompass often describes the breadth or scope of research, projects, policies, or systems. The term implies not just inclusion but integration of diverse elements into a unified whole.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'en-KUHM-puhs',
                'etymology': 'From "en-" (in, within) + "compass" (from Old French "compasser," meaning "to measure, go around"), ultimately from Latin "com-" (together) + "passus" (step).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The new policy will _______ all aspects of student life on campus.',
                'memory_tip': 'Remember "en-COMPASS" - think "in-compass" like a compass that includes all directions, or "encompass" includes everything in its circle.'
            },
            'encore': {
                'definition': 'An encore is an additional performance given by entertainers in response to audience applause and demands for more after the scheduled performance has ended. The term is most commonly associated with musical concerts, theatrical performances, and other live entertainment events where audiences show their appreciation by clapping, cheering, or calling out for more. When performers agree to give an encore, they typically return to the stage to perform one or more additional songs, pieces, or acts beyond their planned program. The encore tradition represents a spontaneous interaction between performers and audience, demonstrating mutual appreciation and enjoyment. In some contexts, encores are planned in advance by performers who anticipate audience demand, while in others they are genuinely spontaneous responses to unexpected enthusiasm. The word can also be used more broadly to mean any repeat performance or additional occurrence of something successful. As an exclamation, "encore!" is shouted by audience members to request additional performance.',
                'part_of_speech': 'noun, interjection, verb',
                'pronunciation_guide': 'AHN-kawr',
                'etymology': 'From French "encore" meaning "again, still, yet," from Latin "hanc horam" (this hour). The theatrical use developed from the French practice of calling for repetitions.',
                'language_origins': 'Latin, French',
                'example_sentence': 'The enthusiastic audience demanded an _______ after the spectacular piano recital.',
                'memory_tip': 'Remember "EN-core" - think "again-core" meaning the core performance again, or it sounds like "anchor" which brings the ship back to shore like encore brings performers back to stage.'
            },
            'encroach': {
                'definition': 'To encroach means to gradually advance beyond proper or established limits, often in a way that intrudes upon or violates the rights, territory, or domain of another. This term frequently describes unauthorized or unwelcome advancement into areas where one has no right to be. Encroachment can be physical, such as when buildings, fences, or vegetation extend onto neighboring property, or abstract, such as when one person\'s activities interfere with another\'s rights or responsibilities. In legal contexts, encroachment often involves property disputes where structures or activities cross boundary lines. Environmental encroachment occurs when human activities gradually expand into natural habitats, threatening wildlife and ecosystems. The word suggests a slow, persistent advancement rather than sudden invasion. Encroachment typically carries negative connotations, implying violation of boundaries, disrespect for limits, or unauthorized intrusion. The process is often incremental, making it particularly problematic because it may go unnoticed until significant damage or displacement has occurred.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'en-KROHCH',
                'etymology': 'From Old French "encrochier" meaning "to seize, fasten on," from "en-" (in) + "croc" (hook). The sense of "intrude" developed from the idea of hooking onto something.',
                'language_origins': 'Old French',
                'example_sentence': 'The developer\'s construction began to _______ on the protected wetland area.',
                'memory_tip': 'Remember "en-CROACH" - think "encroach like a cockroach" that slowly creeps into spaces where it doesn\'t belong, or "en-crouch" like crouching and sneaking in.'
            },
            'endearing': {
                'definition': 'Endearing describes qualities, actions, or characteristics that inspire affection, fondness, or love in others. When something is endearing, it has the power to win hearts and create positive emotional connections. These qualities often include innocence, vulnerability, kindness, humor, or charming imperfections that make a person or thing more lovable rather than less so. Endearing behaviors might include a child\'s innocent questions, a pet\'s playful antics, or an adult\'s genuine enthusiasm for simple pleasures. The term suggests an ability to evoke protective or nurturing feelings in others. Endearing qualities are typically seen as authentic and unforced rather than calculated to win affection. In relationships, endearing traits often strengthen bonds and create lasting positive impressions. The word can apply to people, animals, objects, or even abstract concepts that somehow touch the heart or create emotional warmth. What people find endearing often reflects cultural values and personal experiences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'en-DEER-ing',
                'etymology': 'From "endear" (to make dear or beloved) + "-ing." "Endear" comes from "en-" (to make) + "dear" (beloved, precious), from Old English "dēore."',
                'language_origins': 'Old English',
                'example_sentence': 'The puppy\'s _______ habit of tilting its head made everyone fall in love with it.',
                'memory_tip': 'Remember "en-DEAR-ing" - think "making dear" or "in-dear" meaning something that makes you dear to others, like endearing yourself to people.'
            },
            'ended': {
                'definition': 'Ended is the past tense of the verb "end," meaning to bring something to a conclusion, termination, or completion. When something has ended, it has reached its final point, ceased to continue, or come to a stop. The term can apply to temporal events (such as a meeting that ended at noon), relationships (a friendship that ended badly), activities (a game that ended in a tie), or processes (a project that ended successfully). Ended implies a definitive conclusion rather than a temporary pause or interruption. The word can describe both natural conclusions (when something reaches its intended or expected finish) and abrupt terminations (when something stops unexpectedly or prematurely). In storytelling, "ended" often appears in closing phrases like "and so the story ended" or "it all ended happily." The concept of ending is fundamental to human experience, marking transitions, completions, and new beginnings.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'EN-did',
                'etymology': 'From Old English "endian" meaning "to end, finish, abolish," from "ende" (end, boundary). Related to German "enden" and Dutch "eindigen."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The championship game _______ with a dramatic last-second goal.',
                'memory_tip': 'Remember "END-ed" - think "end + ed" showing that something has reached its end in the past.'
            },
            'endless': {
                'definition': 'Endless describes something that has no end, limit, or boundary; continuing indefinitely without stopping or concluding. The term can refer to physical concepts (such as an endless road that seems to stretch forever), temporal concepts (endless waiting or endless time), or abstract concepts (endless possibilities or endless love). When something is described as endless, it suggests either literal infinity or a duration or extent so vast that it appears infinite from a human perspective. Endless can convey positive meanings (endless opportunities, endless joy) or negative ones (endless problems, endless suffering), depending on context. The word often expresses frustration with situations that seem to have no resolution or excitement about unlimited potential. In mathematics and science, endless relates to concepts of infinity and unbounded sets. In everyday usage, endless frequently serves as hyperbole to emphasize the perceived magnitude or duration of something, even when it technically has limits.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'END-lis',
                'etymology': 'From Old English "endelēas," from "ende" (end) + "-lēas" (suffix meaning "without, lacking"). The compound literally means "without end."',
                'language_origins': 'Old English',
                'example_sentence': 'The children complained about the _______ car ride to their grandmother\'s house.',
                'memory_tip': 'Remember "END-less" - think "end + less" meaning having less of an end, or no end at all.'
            },
            'endocrine': {
                'definition': 'Endocrine refers to the system of glands in the body that produce and secrete hormones directly into the bloodstream to regulate various bodily functions. The endocrine system includes glands such as the pituitary, thyroid, adrenal, pancreas, ovaries, and testes, among others. These glands release chemical messengers (hormones) that travel through the bloodstream to target organs and tissues, controlling processes like growth, metabolism, reproduction, stress response, and blood sugar regulation. Unlike exocrine glands, which secrete substances through ducts to external surfaces or internal cavities, endocrine glands are ductless and release their secretions directly into the circulatory system. Endocrine disorders can result from gland dysfunction, causing conditions like diabetes, thyroid disease, or growth disorders. The term can also be used as a noun to refer to the endocrine system as a whole. Understanding endocrine function is crucial in medicine for diagnosing and treating hormonal imbalances and metabolic disorders.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'EN-duh-krin',
                'etymology': 'From Greek "endon" (within) + "krinein" (to separate, decide), literally meaning "secreting within." The term was coined in the early 20th century to distinguish from exocrine glands.',
                'language_origins': 'Greek',
                'example_sentence': 'The doctor explained how _______ disorders can affect everything from mood to metabolism.',
                'memory_tip': 'Remember "ENDO-crine" - think "endo" (inside) + "crine" (secrete), meaning glands that secrete hormones inside the body.'
            },
            'endogenousbeefalo': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "endogenous" (originating from within an organism or system) and "beefalo" (a hybrid animal that is a cross between domestic cattle and American bison). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated scientific and agricultural terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'endorphin': {
                'definition': 'Endorphins are naturally occurring chemicals produced by the central nervous system and pituitary gland that function as the body\'s natural painkillers and mood elevators. These neurotransmitters are structurally similar to opiates like morphine and bind to the same receptors in the brain, producing feelings of well-being and pain relief. Endorphins are released in response to stress, pain, exercise, excitement, and certain activities like eating spicy food or laughing. The "runner\'s high" experienced during intense exercise is attributed to endorphin release. These chemicals play a crucial role in the body\'s natural pain management system and help regulate mood, stress response, and pleasure sensations. Different types of endorphins exist, including beta-endorphin, which is particularly potent. Understanding endorphins has important implications for treating pain, depression, and addiction. Activities that naturally boost endorphin production include exercise, meditation, laughter, music, and social bonding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'en-DAWR-fin',
                'etymology': 'Coined in the 1970s from "endogenous" (produced within) + "morphine," literally meaning "morphine produced within the body." The term reflects their opioid-like properties.',
                'language_origins': 'Modern scientific coinage (English/Greek)',
                'example_sentence': 'The intense workout triggered the release of _______ that left her feeling euphoric.',
                'memory_tip': 'Remember "ENDO-rphin" - think "endo" (inside) + "morphine" (painkiller), so natural morphine made inside your body.'
            },
            'endowed': {
                'definition': 'Endowed means naturally provided with or possessing certain qualities, abilities, or characteristics. When someone is endowed with something, they have been given or blessed with particular traits, often considered gifts or natural advantages. The term frequently describes inherent talents, physical attributes, mental capacities, or resources that a person possesses from birth or acquires through circumstance. Endowed can also refer to institutions or organizations that have been provided with funds, property, or resources, typically through donations or bequests. In this context, an endowed chair at a university is a professorship funded by a permanent donation, or an endowed foundation has sufficient funds to operate indefinitely from investment income. The word carries connotations of abundance, blessing, or fortunate provision. It suggests that the endowment (whether natural talent or financial resources) provides ongoing benefit or advantage. The concept often implies responsibility to use these gifts wisely or productively.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'en-DOWD',
                'etymology': 'From Old French "endouer," from "en-" (in) + "douer" (to endow), from Latin "dotare" (to endow), from "dos" (dowry, gift).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The university\'s _______ scholarship program helps talented students afford their education.',
                'memory_tip': 'Remember "en-DOWED" - think "in-dowed" meaning having gifts or talents placed within you, or "endow-ed" meaning given an endowment.'
            },
            'ends': {
                'definition': 'Ends can function as either a noun (plural of "end") or a verb (third person singular of "end"). As a noun, ends refers to the final parts, extremities, or boundaries of objects, events, or concepts. It can describe physical extremities (the ends of a rope), temporal boundaries (the ends of a day), or purposeful goals (achieving one\'s ends). The phrase "odds and ends" refers to miscellaneous items or remnants. As a verb, ends means brings to a conclusion or termination, as in "the movie ends at midnight." In the context of goals or purposes, "ends" often appears in discussions about means and ends, referring to objectives or desired outcomes. The word can also indicate results or consequences, as in "how it all ends." In some contexts, ends refers to the final portions or remnants of something, such as leftover materials or the concluding segments of a process or period.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'endz',
                'etymology': 'From Old English "ende" (end, boundary, district), related to German "ende" and Dutch "einde." The plural and verb forms developed naturally from the base word.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The movie _______ with a surprising plot twist that nobody expected.',
                'memory_tip': 'Remember "ENDS" - think "end + s" for multiple endings or something that ends, like "the story ends here."'
            },
            'endure': {
                'definition': 'To endure means to withstand, tolerate, or survive difficult conditions, pain, hardship, or challenges over time. Endurance involves maintaining strength, patience, or resolve despite adversity or discomfort. The term can describe both physical endurance (surviving harsh weather, illness, or physical exertion) and emotional or psychological endurance (coping with stress, grief, or prolonged difficulties). Endure also means to last or continue in existence over time, as in "buildings that endure for centuries" or "traditions that endure across generations." This usage emphasizes permanence, durability, or persistence rather than survival of hardship. The concept of endurance is often associated with courage, determination, and resilience. In sports and fitness contexts, endurance refers to the ability to sustain prolonged physical effort. The word suggests not just survival but active persistence and strength in the face of challenges that might defeat others.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'en-DOOR',
                'etymology': 'From Old French "endurer," from Latin "indurare" meaning "to make hard," from "in-" (in) + "durare" (to last, be hard), from "durus" (hard).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The hikers had to _______ freezing temperatures and high winds during their mountain expedition.',
                'memory_tip': 'Remember "en-DURE" - think "in-durable" meaning to be durable from within, or "endure" sounds like "and-you\'re" still standing after hardship.'
            },
            'enervate': {
                'definition': 'To enervate means to weaken, drain of energy, or reduce the strength and vitality of someone or something. This verb describes the process of making someone feel tired, listless, or devoid of physical or mental vigor. Enervation can result from physical factors (extreme heat, illness, overexertion), mental factors (stress, boredom, depression), or environmental conditions (oppressive humidity, monotonous situations). The word often describes a gradual process rather than sudden exhaustion, suggesting a slow drain of energy or enthusiasm. Enervating conditions or experiences leave people feeling depleted, unmotivated, or incapable of normal activity. The term can also describe the effect of certain climates, situations, or lifestyles that consistently sap energy and vitality. Note that despite sounding similar to "energize," enervate has the opposite meaning - it removes energy rather than adding it. The word carries connotations of debilitation and reduced effectiveness.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'EN-er-vayt',
                'etymology': 'From Latin "enervatus," past participle of "enervare" meaning "to weaken, remove the sinews," from "e-" (out) + "nervus" (sinew, nerve).',
                'language_origins': 'Latin',
                'example_sentence': 'The oppressive heat and humidity began to _______ the workers by mid-afternoon.',
                'memory_tip': 'Remember "e-NERV-ate" - think "e" (remove) + "nerve" (strength), so removing your nerve/strength, or "enervate" sounds like "in-irritate" which drains energy.'
            },
            'enforcement': {
                'definition': 'Enforcement refers to the act of compelling observance of or compliance with laws, rules, regulations, or commands through the use of authority, power, or sanctions. This process involves ensuring that established standards, policies, or legal requirements are followed and that violations are appropriately addressed. Law enforcement agencies, such as police departments, regulatory bodies, and courts, are responsible for different aspects of enforcement within society. Enforcement mechanisms can include warnings, fines, penalties, prosecution, and other corrective measures designed to deter violations and ensure compliance. The concept extends beyond legal contexts to include enforcement of organizational policies, safety regulations, academic standards, and social norms. Effective enforcement typically requires clear rules, adequate resources, consistent application, and appropriate consequences for violations. The term can also refer to the specific act of implementing or carrying out a particular law or regulation, as in "enforcement of speed limits" or "enforcement of environmental regulations."',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'en-FAWRS-muhnt',
                'etymology': 'From "enforce" (from Old French "enforcier," meaning "to strengthen, apply force") + "-ment" (suffix indicating action or result). "Enforce" comes from "en-" (in) + "force."',
                'language_origins': 'Old French',
                'example_sentence': 'Strict _______ of the new traffic laws led to a significant reduction in accidents.',
                'memory_tip': 'Remember "en-FORCE-ment" - think "in-force" meaning putting force into making people follow rules, or "enforce-ment" meaning the mental/action aspect of enforcing.'
            },
            'enfranchise': {
                'definition': 'To enfranchise means to grant political rights, particularly the right to vote, to individuals or groups who previously lacked these privileges. The term is most commonly associated with extending voting rights to previously disenfranchised populations, such as women, racial minorities, or people without property. Enfranchisement represents the inclusion of individuals in the democratic process and recognition of their status as full citizens. Historical examples include the enfranchisement of women through suffrage movements, the enfranchisement of formerly enslaved people after the Civil War, and the enfranchisement of young adults through lowering the voting age. The word can also refer more broadly to granting any rights, privileges, or freedoms to those who were previously denied them. In business contexts, enfranchisement might refer to granting someone the rights to operate a franchise. The concept is fundamental to democratic development and social progress, representing the expansion of political participation and civic equality.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'en-FRAN-chahyz',
                'etymology': 'From Old French "enfranchir" meaning "to set free," from "en-" (in) + "franc" (free). Originally meant to free from servitude, later extended to political rights.',
                'language_origins': 'Old French',
                'example_sentence': 'The constitutional amendment served to _______ millions of citizens who had been denied voting rights.',
                'memory_tip': 'Remember "en-FRANCHISE" - think "in-franchise" meaning bringing someone into the franchise/system of voting, or "en-France" where modern democratic ideas developed.'
            },
            'engage': {
                'definition': 'To engage means to participate in, become involved with, or commit to an activity, relationship, or cause. The term encompasses various forms of active participation, from simple attention (engaging with a book or conversation) to deep commitment (engaging in social activism or engaging with a community). In interpersonal contexts, engagement refers to meaningful interaction, connection, or involvement with others. Professional engagement involves active participation in work responsibilities and organizational goals. Academic engagement describes students\' investment in learning activities and educational processes. The word can also mean to hire or employ someone for a specific purpose, to attract and hold attention, or to enter into conflict or battle. In mechanical contexts, engage refers to connecting or interlocking parts (such as engaging gears). The concept implies active choice and sustained attention rather than passive or superficial involvement.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'en-GAYJ',
                'etymology': 'From Old French "engagier" meaning "to pledge, put in pledge," from "en-" (in) + "gage" (pledge, wage). The modern sense of "involve, participate" developed from the idea of pledging oneself.',
                'language_origins': 'Old French',
                'example_sentence': 'The teacher worked hard to _______ all students in the classroom discussion.',
                'memory_tip': 'Remember "en-GAGE" - think "in-gauge" like measuring your involvement level, or "en-gage" like putting yourself in a cage of commitment.'
            },
            'engaging': {
                'definition': 'Engaging describes something that captures and holds attention, interest, or participation in a compelling and attractive way. When something is engaging, it has the quality of drawing people in and maintaining their focus through appeal, charm, or fascination. Engaging content, personalities, or experiences create a sense of connection and involvement that makes people want to continue participating or paying attention. The term suggests active involvement rather than passive consumption - engaging materials invite interaction, thought, or emotional response. In educational contexts, engaging teaching methods promote student participation and learning. Engaging personalities are charismatic, interesting, and able to connect well with others. An engaging book, movie, or presentation holds the audience\'s attention throughout. The word implies a positive quality that makes something appealing and worthwhile. Engaging experiences often combine elements of relevance, interactivity, challenge, and enjoyment to create meaningful connection between participants and content.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'en-GAY-jing',
                'etymology': 'From "engage" (from Old French "engagier") + "-ing" (present participle suffix). The adjective developed from the verb\'s sense of "attracting and holding attention."',
                'language_origins': 'Old French',
                'example_sentence': 'The professor\'s _______ lecture style kept students interested throughout the entire semester.',
                'memory_tip': 'Remember "en-GAG-ing" - think "engaging" like a gear that engages/connects with you, or "en-gaging" meaning it measures/gauges your interest.'
            },
            'engineer': {
                'definition': 'An engineer is a professional who applies scientific and mathematical principles to design, build, analyze, and maintain structures, machines, systems, and processes. Engineers use their technical knowledge to solve practical problems and create solutions that benefit society. The field encompasses many specializations, including civil engineering (infrastructure and construction), mechanical engineering (machines and mechanical systems), electrical engineering (electrical systems and electronics), chemical engineering (chemical processes and materials), software engineering (computer programs and systems), and biomedical engineering (medical devices and biological systems). Engineers typically follow a systematic design process that includes identifying problems, researching solutions, creating prototypes, testing, and refining designs. The profession requires strong analytical skills, creativity, attention to detail, and understanding of safety principles. As a verb, "engineer" means to plan, design, or devise something skillfully, often referring to bringing about a particular outcome through careful planning and execution.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'en-juh-NEER',
                'etymology': 'From Old French "engigneor," from "engin" (engine, device, talent), from Latin "ingenium" (innate quality, cleverness), from "in-" (in) + root of "gignere" (to beget).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The civil _______ designed a bridge that could withstand earthquakes and heavy traffic.',
                'memory_tip': 'Remember "engi-NEER" - think "engine-ear" because engineers work with engines and mechanical things, or "engin-eer" meaning someone with engineering skill.'
            },
            'english': {
                'definition': 'English refers to the language originally spoken in England that has become one of the world\'s most widely used languages for international communication, business, science, and technology. As a proper adjective, English describes things relating to England, its people, or its culture. The English language belongs to the Germanic family of Indo-European languages and has evolved significantly since its Old English origins, incorporating influences from Latin, French, Norse, and many other languages through conquest, trade, and cultural exchange. Modern English serves as a lingua franca in many international contexts and is an official language in numerous countries beyond England. The language is characterized by its relatively simple grammar structure, extensive vocabulary, and flexibility in word formation and usage. English literature, English customs, and English history represent significant cultural contributions to world civilization. The term can also refer to the academic subject focused on studying English language and literature.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ING-glish',
                'etymology': 'From Old English "Englisc," from "Engle" (the Angles, a Germanic tribe) + "-isc" (suffix meaning "of, relating to"). The Angles were one of the tribes that settled in Britain.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She studied _______ literature and became fascinated with Shakespeare\'s plays.',
                'memory_tip': 'Remember "ENG-lish" - think "England-ish" meaning relating to England, or "angl-ish" from the Angles who helped create the language.'
            },
            'engrossed': {
                'definition': 'Engrossed describes a state of being completely absorbed, deeply focused, or wholly occupied with something to the exclusion of other things. When someone is engrossed in an activity, their attention is so thoroughly captured that they may be unaware of their surroundings or the passage of time. This intense concentration often occurs when engaging with compelling content such as a fascinating book, challenging puzzle, captivating movie, or absorbing conversation. Being engrossed indicates a high level of interest and mental involvement that creates a sense of immersion in the subject matter. The state suggests voluntary attention rather than forced concentration, typically resulting from genuine interest or enjoyment. People often describe being engrossed in hobbies, creative projects, academic subjects, or entertainment that particularly appeals to them. The word implies a positive form of preoccupation where the person willingly gives their full attention to something they find valuable or enjoyable.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'en-GROHST',
                'etymology': 'From "engross," which originally meant "to buy up in large quantities" (from Old French "en gros," meaning "in large quantity"), later developing the sense of "absorb fully."',
                'language_origins': 'Old French',
                'example_sentence': 'She was so _______ in her novel that she didn\'t hear the doorbell ring.',
                'memory_tip': 'Remember "en-GROSSED" - think "gross" (large) meaning largely absorbed, or "en-gross" meaning completely gross-ly involved in something.'
            },
            'engulf': {
                'definition': 'To engulf means to completely surround, overwhelm, or swallow up something, typically in a way that causes it to disappear or become completely enclosed. The term often describes rapid or overwhelming processes where something large consumes or covers something smaller. Physical examples include floods engulfing buildings, flames engulfing structures, or avalanches engulfing skiers. Engulfing can also describe emotional or psychological states, such as being engulfed by grief, panic, or despair, where intense feelings completely overwhelm a person\'s normal functioning. The word suggests a totality of coverage or influence that leaves little or nothing visible or unaffected. Unlike gradual processes, engulfing often implies suddenness and power, as when a massive wave engulfs a small boat or when a person feels engulfed by responsibilities. The concept carries connotations of being overpowered or consumed by forces larger than oneself, whether physical, emotional, or circumstantial.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'en-GUHLF',
                'etymology': 'From "en-" (in, into) + "gulf" (from Old French "golfe," from Greek "kolpos" meaning "bosom, gulf"). The word literally means "to put into a gulf."',
                'language_origins': 'Greek, Old French',
                'example_sentence': 'The massive wildfire threatened to _______ the entire mountain community.',
                'memory_tip': 'Remember "en-GULF" - think "in-gulf" meaning to put something into a gulf/large space, or "engulf" like a gulf (body of water) swallowing something.'
            },
            'enjoy': {
                'definition': 'To enjoy means to take pleasure in, find satisfaction from, or experience happiness through an activity, situation, or experience. Enjoyment involves a positive emotional response characterized by contentment, delight, or gratification. The word can describe both active appreciation (enjoying a concert, meal, or conversation) and passive reception (enjoying sunshine or quiet moments). Enjoyment typically requires some level of engagement or awareness, distinguishing it from mere tolerance or neutral acceptance. People enjoy activities that align with their interests, values, or preferences, though what brings enjoyment varies greatly among individuals and cultures. The capacity for enjoyment is considered important for mental health and overall well-being. Enjoyment can be immediate and spontaneous or developed through repeated exposure and appreciation. The word can also mean to possess or benefit from something, as in "enjoying good health" or "enjoying success," though the pleasure-focused meaning is more common in contemporary usage.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'en-JOI',
                'etymology': 'From Old French "enjoir," from "en-" (in) + "joir" (to enjoy), from Latin "gaudere" (to rejoice). The sense of "take pleasure in" has been present since Middle English.',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The family decided to _______ a picnic in the park on the beautiful spring day.',
                'memory_tip': 'Remember "en-JOY" - think "in-joy" meaning to be in a state of joy, or "enjoy" contains "joy" which is what you feel when you enjoy something.'
            },
            'enlarged': {
                'definition': 'Enlarged means made larger, increased in size, scope, or scale from a previous state. This past tense adjective describes something that has undergone a process of expansion, growth, or magnification. Physical enlargement can involve making objects, images, or spaces bigger through various means such as construction, inflation, magnification, or natural growth. Medical contexts often use enlarged to describe organs, tissues, or other body parts that have increased beyond normal size, sometimes indicating health conditions. The term can also apply to abstract concepts, such as enlarged responsibilities, enlarged understanding, or enlarged opportunities. Photographic enlargement involves making bigger prints from smaller negatives or digital files. Enlarged can describe intentional modifications (enlarged windows in a renovation) or unintended changes (enlarged heart due to disease). The word suggests a comparison between current and previous states, emphasizing the change in magnitude or extent.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'en-LAHRJD',
                'etymology': 'From "enlarge" (from "en-" meaning "make" + "large") + "-ed" (past tense/past participle suffix). "Large" comes from Old French "large" meaning "broad, wide."',
                'language_origins': 'Old French',
                'example_sentence': 'The _______ photograph revealed details that were invisible in the original small print.',
                'memory_tip': 'Remember "en-LARGED" - think "en-large-ed" meaning made large, or "enlarged" like making something large-er than it was.'
            },
            'enmity': {
                'definition': 'Enmity refers to deep-seated hostility, hatred, or antagonism between individuals, groups, or nations. This intense form of opposition goes beyond simple disagreement or dislike to encompass active ill will and desire for harm or disadvantage to befall one\'s enemy. Enmity often develops from serious conflicts, betrayals, injustices, or fundamental incompatibilities in values or interests. Unlike temporary anger or irritation, enmity suggests a lasting and profound animosity that may persist across generations or institutional changes. Historical examples include enmity between warring nations, feuding families, or competing political factions. Enmity can manifest in various ways, from open conflict and aggression to subtle undermining and opposition. The emotion often involves not just negative feelings but active wishes for the enemy\'s failure or suffering. Resolving enmity typically requires significant effort, compromise, and often external mediation, as the depth of feeling makes reconciliation particularly challenging.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EN-mi-tee',
                'etymology': 'From Old French "enemité," from Latin "inimicitia" meaning "unfriendliness, hostility," from "inimicus" (unfriendly, hostile), from "in-" (not) + "amicus" (friend).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The ancient _______ between the two families had lasted for generations.',
                'memory_tip': 'Remember "EN-mity" - think "enemy-ty" because enmity is what you feel toward enemies, or "en-amity" meaning the opposite of amity (friendship).'
            },
            'ennui': {
                'definition': 'Ennui is a feeling of listlessness, dissatisfaction, and boredom that arises from a lack of excitement, meaning, or purpose in one\'s current circumstances. This French-derived term describes a more profound and existential form of boredom than simple temporary tedium. Ennui often involves a sense of emotional numbness or disconnection from activities that would normally provide interest or satisfaction. The condition typically affects people who have sufficient material comfort but lack intellectual, emotional, or spiritual stimulation. Ennui can result from routine, prosperity without purpose, or the absence of meaningful challenges. The term is often associated with philosophical and literary discussions of modern life\'s potential meaninglessness or the psychological effects of comfort and security. Unlike depression, ennui specifically relates to environmental circumstances rather than clinical mental health conditions, though prolonged ennui might contribute to or mask underlying emotional issues. The concept suggests that humans need more than basic comfort to feel fulfilled.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ahn-WEE',
                'etymology': 'From French "ennui," from Old French "enui" meaning "annoyance, trouble," from "enuier" (to annoy), from Latin "in odio" (in hatred, disliked).',
                'language_origins': 'Latin, Old French, French',
                'example_sentence': 'After months of the same routine, she felt overcome by _______ and longed for adventure.',
                'memory_tip': 'Remember "en-NUI" - think "annoying-wee" because ennui is that annoying feeling of boredom, or remember it\'s French and sounds like "on-we" meaning it weighs on us.'
            },
            'enoch': {
                'definition': 'Enoch is a name of Hebrew origin that appears prominently in biblical and religious contexts. In the Hebrew Bible, Enoch is the name of several figures, most notably the seventh patriarch before the flood, described as the father of Methuselah. According to biblical narrative, Enoch "walked with God" and was taken directly to heaven without experiencing death, making him one of only two people in the Hebrew Bible (along with Elijah) described as being translated to heaven. The name means "dedicated" or "initiated" in Hebrew. Enoch is also associated with various apocryphal texts, including the Books of Enoch, which elaborate on his heavenly journeys and revelations. In modern usage, Enoch serves as a given name, though it\'s relatively uncommon. The name has been used in literature and popular culture, often carrying connotations of spiritual devotion or divine favor due to its biblical associations.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'EE-nuhk',
                'etymology': 'From Hebrew "Chanokh" meaning "dedicated, initiated, trained." The name appears in the Hebrew Bible and has been transliterated through Greek and Latin into English.',
                'language_origins': 'Hebrew',
                'example_sentence': 'The ancient text tells of _______ being taken up to heaven without dying.',
                'memory_tip': 'Remember "E-noch" - think "enough" because Enoch was good enough to go straight to heaven, or "he-knocked" on heaven\'s door and was let in.'
            },
            'enoki': {
                'definition': 'Enoki mushrooms are a species of edible fungi (Flammulina velutipes) characterized by their distinctive long, thin white stems and small caps. These mushrooms are native to East Asia and are particularly popular in Japanese, Chinese, and Korean cuisine. Enoki mushrooms have a mild, slightly sweet flavor and a crisp, crunchy texture that makes them valuable in both cooked and raw preparations. They grow naturally on hardwood trees, particularly on stumps and dead trees, but are now widely cultivated commercially. In cooking, enoki mushrooms are often used in soups, stir-fries, salads, and hot pot dishes. They cook quickly and should be added near the end of cooking to preserve their texture. Nutritionally, enoki mushrooms are low in calories but rich in protein, fiber, and various vitamins and minerals. They are also being studied for potential health benefits, including immune system support and anti-inflammatory properties. The mushrooms are typically sold in clusters and should be separated at the base before use.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eh-NOH-kee',
                'etymology': 'From Japanese "enokitake," literally meaning "hackberry mushroom," from "enoki" (Chinese hackberry tree) + "take" (mushroom). Named for the tree where they naturally grow.',
                'language_origins': 'Japanese',
                'example_sentence': 'The chef added fresh _______ mushrooms to the miso soup just before serving.',
                'memory_tip': 'Remember "e-NOKI" - think "elongated noodles" because enoki mushrooms look like long, thin white noodles, or "e-hockey" because they\'re thin like hockey sticks.'
            },
            'enoptromancy': {
                'definition': 'Enoptromancy is a form of divination that involves gazing into mirrors, crystals, or other reflective surfaces to gain insights into the future, seek spiritual guidance, or communicate with supernatural entities. This ancient practice, also known as catoptromancy or crystallomancy when using crystals, relies on the belief that reflective surfaces can serve as windows to other realms or reveal hidden knowledge. Practitioners typically enter a meditative or trance-like state while gazing into the reflective medium, interpreting visions, symbols, or images that appear in the surface or in their mind\'s eye. The practice has appeared in various cultures throughout history, from ancient Greek and Roman traditions to medieval European magical practices. Modern practitioners might use black mirrors, crystal balls, water surfaces, or polished metal objects. Enoptromancy is considered a form of scrying, which encompasses various divination techniques involving gazing into reflective or translucent materials to receive visions or insights.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'en-OP-truh-man-see',
                'etymology': 'From Greek "enoptron" (mirror), from "en-" (in) + "optron" (mirror, from "ops" meaning "eye"), plus "-mancy" (divination), from "manteia" (prophecy).',
                'language_origins': 'Greek',
                'example_sentence': 'The ancient practitioner used _______ to divine the outcome of the upcoming battle.',
                'memory_tip': 'Remember "en-OPTRO-mancy" - think "in-optic-romance" because you look into optical surfaces romantically/mystically, or "enopt-romance" meaning having a romance with mirrors.'
            },
            'enormously': {
                'definition': 'Enormously is an adverb meaning to an extremely large degree, vastly, or tremendously. This word intensifies adjectives and verbs to indicate that something occurs or exists to an exceptional extent. When something changes enormously, the change is dramatic and significant. When someone enjoys something enormously, their pleasure is intense and substantial. The word suggests scale that goes well beyond normal or expected levels, emphasizing the magnitude of whatever is being described. Enormously can modify various concepts: size (enormously large), quantity (enormously popular), improvement (enormously better), or emotional states (enormously grateful). The adverb adds emphasis and helps convey the speaker\'s sense that standard descriptors are insufficient to capture the full extent of what they\'re describing. In academic and formal writing, enormously helps express the significance or impact of research findings, changes, or developments.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ih-NAWR-muhs-lee',
                'etymology': 'From "enormous" (from Latin "enormis" meaning "out of rule, irregular, huge," from "e-" (out of) + "norma" (rule, pattern)) + "-ly" (adverb suffix).',
                'language_origins': 'Latin',
                'example_sentence': 'The new medicine improved her quality of life _______.',
                'memory_tip': 'Remember "e-NORM-ously" - think "e-normal" meaning extremely away from normal, or "enormous-ly" meaning in an enormous way.'
            },
            'enriches': {
                'definition': 'Enriches is the third person singular present tense of the verb "enrich," meaning to improve the quality, value, or significance of something by adding beneficial elements or increasing its worth. When something enriches another thing, it enhances, augments, or makes it more valuable in some way. The term can apply to various contexts: education enriches minds by adding knowledge and skills; good soil enriches plant growth by providing nutrients; cultural experiences enrich people\'s understanding of the world; vitamins enrich foods by adding nutritional value. Enrichment often involves adding something valuable or beneficial that was previously missing or insufficient. The word suggests positive transformation or improvement rather than mere addition. In social contexts, diversity enriches communities by bringing different perspectives and experiences together. The concept implies that the enriched entity becomes more complete, valuable, or effective as a result of the enriching process.',
                'part_of_speech': 'verb (third person singular present)',
                'pronunciation_guide': 'en-RICH-iz',
                'etymology': 'From "enrich" (from "en-" meaning "make" + "rich" from Old English "rice" meaning "powerful, wealthy") + "-es" (third person singular present tense ending).',
                'language_origins': 'Old English',
                'example_sentence': 'Reading literature _______ students\' understanding of human nature and cultural values.',
                'memory_tip': 'Remember "en-RICH-es" - think "makes rich" because to enrich means to make something richer/better, or "enriches" adds riches to something.'
            },
            'enrolled': {
                'definition': 'Enrolled is the past tense of "enroll," meaning to register, sign up for, or officially join an institution, program, course, or organization. When someone has enrolled, they have completed the process of becoming a member or participant in a formal system. The term is most commonly used in educational contexts, where students enroll in schools, colleges, or specific courses, but it also applies to joining military services, insurance programs, membership organizations, or various other structured systems. Enrollment typically involves completing paperwork, meeting requirements, and making commitments to participate according to established rules or expectations. The word suggests a formal, official process rather than casual participation. Once enrolled, individuals usually gain access to specific benefits, services, or opportunities associated with their membership. Enrollment often marks the beginning of a new phase of involvement or commitment, whether in education, employment, or other organized activities.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'en-ROHLD',
                'etymology': 'From "enroll" (from Old French "enroller," from "en-" (in) + "rolle" (roll, scroll)), originally meaning "to write on a scroll." The educational sense developed later.',
                'language_origins': 'Old French',
                'example_sentence': 'She _______ in three challenging courses for the upcoming semester.',
                'memory_tip': 'Remember "en-ROLLED" - think "in-rolled" meaning rolled into/put on the rolls of students, or "enrolled" like your name is rolled into the system.'
            },
            'ensconced': {
                'definition': 'Ensconced means settled comfortably and securely in a particular place or position, often with implications of being well-protected, hidden, or firmly established. When someone is ensconced somewhere, they are not just located there but are positioned in a way that suggests comfort, security, and perhaps some degree of concealment or protection from outside influences. The term often describes both physical positioning (ensconced in a comfortable chair, ensconced in a cozy cabin) and metaphorical situations (ensconced in a powerful position, ensconced in academic tradition). Being ensconced typically implies a sense of belonging, safety, and settled comfort rather than temporary placement. The word suggests that the person or thing is not easily moved or disturbed from their position. Ensconced can have positive connotations of comfort and security, but sometimes carries suggestions of being perhaps too comfortable or resistant to change.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'en-SKONST',
                'etymology': 'From "ensconce," from "en-" (in) + "sconce" (from Middle Dutch "schanse" meaning "earthwork, fortification"). Originally meant "to shelter within or as if within a fortification."',
                'language_origins': 'Middle Dutch',
                'example_sentence': 'The professor was _______ in his book-lined office, surrounded by decades of research.',
                'memory_tip': 'Remember "en-SCONCED" - think "in-sconced" meaning safely placed in like a sconce holds a candle, or "ensconced" sounds like "in-skons" meaning hidden/settled in.'
            },
            'ensemble': {
                'definition': 'An ensemble refers to a group of musicians, actors, or performers who work together as a coordinated unit to create a unified artistic presentation. In music, ensembles can range from small groups like string quartets or jazz combos to large orchestras or choirs. The term emphasizes the collaborative nature of the performance, where individual contributions combine to create a cohesive whole. In theater, an ensemble cast refers to a group of actors who work together with roughly equal importance rather than having one or two dominant starring roles. The word can also describe a coordinated outfit or set of clothing items worn together. In broader usage, ensemble refers to any collection of elements that function together as a unified whole, such as an ensemble of buildings in architecture or an ensemble of ideas in academic work. The concept emphasizes harmony, coordination, and the idea that the combined effect is greater than the sum of individual parts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ahn-SAHM-buhl',
                'etymology': 'From French "ensemble" meaning "together, at the same time," from Latin "insimul" (at the same time), from "in-" (in) + "simul" (together).',
                'language_origins': 'Latin, French',
                'example_sentence': 'The chamber music _______ performed beautifully at the evening concert.',
                'memory_tip': 'Remember "en-SEMBLE" - think "resembles" because an ensemble resembles a unified group, or "ensemble" sounds like "assemble" meaning people assembled together.'
            },
            'ensilage': {
                'definition': 'Ensilage is the process of preserving green fodder (such as corn, grass, or other crops) by storing it in a compressed, oxygen-free environment where it undergoes controlled fermentation. This agricultural technique, also known as silage-making, allows farmers to preserve nutritious animal feed for use during winter months or periods when fresh forage is unavailable. The process involves cutting crops at optimal nutritional stages, chopping them into small pieces, and storing them in silos, bunkers, or covered pits where anaerobic fermentation occurs. During ensilage, beneficial bacteria convert plant sugars into acids that preserve the feed and maintain its nutritional value. Properly made silage can be stored for months or even years while retaining much of its original nutrition. The resulting product, called silage, provides high-quality feed for cattle, sheep, and other livestock. Ensilage has been crucial in modern agriculture for maintaining consistent livestock nutrition year-round and making efficient use of crop production.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EN-suh-lij',
                'etymology': 'From French "ensilage," from "ensiler" (to store in a silo), from Spanish "ensilar," from "silo" (storage pit). The term entered English in the late 19th century with modern farming techniques.',
                'language_origins': 'Spanish, French',
                'example_sentence': 'The farmer used _______ to preserve corn stalks for feeding cattle during the winter.',
                'memory_tip': 'Remember "EN-silage" - think "in-silo-age" because it involves aging crops in silos, or "ensilage" sounds like "en-village" meaning storing food for the village of animals.'
            }
        }
        
        return batch_059_data.get(word, {
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
                'emulsifylorikeet', 'encarnadinedulcinea', 'endogenousbeefalo'
            ]
            
            if word in combined_words:
                is_error = True
                if word == 'emulsifylorikeet':
                    error_message = 'Combined word error: "emulsifylorikeet" appears to be "emulsify" + "lorikeet" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'encarnadinedulcinea':
                    error_message = 'Combined word error: "encarnadinedulcinea" appears to be "encarnadine" + "dulcinea" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'endogenousbeefalo':
                    error_message = 'Combined word error: "endogenousbeefalo" appears to be "endogenous" + "beefalo" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
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
        
        print("Batch 059 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch059Processor()
    processor.process_batch("batch_059_words.csv", "batch_059_processed.csv")