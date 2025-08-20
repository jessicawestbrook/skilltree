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

class Batch063Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_063_data = {
            'events': {
                'definition': 'Events are occurrences, happenings, or incidents that take place at specific times and locations. This plural noun encompasses a wide range of situations from planned activities like conferences, celebrations, and performances to spontaneous occurrences like accidents, discoveries, or natural phenomena. Events can be classified by their nature (social, cultural, political, scientific), scale (local, national, global), or significance (routine, milestone, historic). In project management and planning, events are scheduled activities with defined objectives, participants, and outcomes. Historical events are significant occurrences that influence the course of human development. Scientific events might include experiments, observations, or natural phenomena. Understanding events involves recognizing their context, causes, consequences, and relationships to other occurrences. Event planning and management have become specialized fields focused on organizing successful gatherings and experiences.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'ih-VENTS',
                'etymology': 'From Latin "eventus," past participle of "evenire" (to come out, happen), from "e-" (out) + "venire" (to come).',
                'language_origins': 'Latin',
                'example_sentence': 'The festival featured multiple cultural _______ including music performances, art exhibitions, and food tastings.',
                'memory_tip': 'Remember "e-VENTS" - think "e-vents" like electronic vents where things come out/happen, or "events" sounds like "he-vents" meaning things that vent/come out into reality.'
            },
            'everglades': {
                'definition': 'The Everglades is a unique ecosystem in southern Florida characterized by vast wetlands, sawgrass marshes, and diverse wildlife habitats. This internationally recognized natural treasure encompasses approximately 1.5 million acres and serves as a critical habitat for numerous endangered species including the American alligator, Florida panther, and various wading birds. The Everglades functions as a slow-moving river system, often called a "river of grass," where water flows gradually southward from Lake Okeechobee toward Florida Bay. This fragile ecosystem has faced significant environmental challenges due to agricultural development, urban expansion, and water management practices that have altered natural water flow patterns. Conservation efforts, including Everglades National Park designation and comprehensive restoration projects, work to preserve and restore this unique environment. The Everglades supports both freshwater and saltwater habitats, creating diverse ecological niches. Understanding the Everglades helps appreciate the complexity of wetland ecosystems and the importance of environmental conservation in maintaining biodiversity.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'EV-er-glaydz',
                'etymology': 'From "ever" (always) + "glades" (open spaces in forests or wetlands), describing the perpetually wet, open marshlands of southern Florida.',
                'language_origins': 'English',
                'example_sentence': 'The _______ provide crucial habitat for endangered species while serving as a natural water filtration system for South Florida.',
                'memory_tip': 'Remember "EVER-glades" - think "ever-glad" because people are ever glad this ecosystem exists, or "everlasting glades" meaning permanent wetland spaces.'
            },
            'everlasting': {
                'definition': 'Everlasting means continuing forever, eternal, or lasting for an extremely long time without end. This adjective describes things that persist indefinitely, endure through time, or seem to have no temporal boundaries. Everlasting can apply to abstract concepts like love, peace, or principles that are considered timeless and permanent. Religious contexts often use everlasting to describe divine attributes, spiritual rewards, or eternal life. The term can also describe physical objects designed for exceptional durability or natural phenomena that appear permanent from human perspective. Everlasting flowers are dried or preserved blooms that maintain their appearance for extended periods. The concept contrasts with temporary, fleeting, or mortal things. Understanding everlasting helps distinguish between different degrees of permanence and the human aspiration for things that transcend temporal limitations. The word often appears in contexts where permanence, reliability, and endurance are valued.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ev-er-LAS-ting',
                'etymology': 'From "ever" (always, at any time) + "lasting" (enduring), literally meaning "always lasting" or "lasting at all times."',
                'language_origins': 'Old English',
                'example_sentence': 'The couple exchanged rings as symbols of their _______ commitment to each other.',
                'memory_tip': 'Remember "EVER-lasting" - think "ever-last-ing" meaning lasting ever and ever, or "everlasting" means something that lasts forever.'
            },
            'everyone': {
                'definition': 'Everyone is an indefinite pronoun meaning all people without exception, every person in a group or general population. This inclusive term encompasses every individual within a specified or implied context, leaving no one out. Everyone functions grammatically as a singular pronoun despite referring to multiple people, requiring singular verb forms ("everyone is" not "everyone are"). The word can refer to all people in specific settings (everyone in the room), organizations (everyone at the company), or humanity in general (everyone deserves respect). Everyone often appears in statements about universal rights, shared experiences, or collective activities. The term emphasizes inclusion and comprehensiveness, suggesting no exceptions or exclusions. Understanding everyone helps with both grammar usage and inclusive communication that acknowledges all members of a group. The concept reflects democratic ideals and human equality by recognizing the importance of every individual.',
                'part_of_speech': 'pronoun',
                'pronunciation_guide': 'EV-ree-wuhn',
                'etymology': 'From "every" (each individual one) + "one" (single person), formed as a compound pronoun meaning "each single person."',
                'language_origins': 'Middle English',
                'example_sentence': 'The principal announced that _______ would receive a certificate of participation in the fundraiser.',
                'memory_tip': 'Remember "EVERY-one" - think "every single one" meaning every single person, or "everyone" means every individual one person.'
            },
            'everything': {
                'definition': 'Everything is an indefinite pronoun meaning all things, the whole of something, or all that exists within a particular context. This comprehensive term encompasses every object, concept, situation, or element within specified or implied boundaries. Everything can refer to all items in a physical space (everything in the room), all aspects of a situation (everything went wrong), or all elements of a concept (everything about the plan). The word emphasizes totality and completeness, suggesting nothing is excluded or left out. Everything often appears in contexts involving comprehensive coverage, total involvement, or complete understanding. Unlike everyone (which refers to people), everything refers to objects, ideas, situations, and non-human entities. The concept reflects human attempts to grasp totality and completeness in an complex world. Understanding everything helps express comprehensive scope and thoroughness in communication.',
                'part_of_speech': 'pronoun',
                'pronunciation_guide': 'EV-ree-thing',
                'etymology': 'From "every" (each individual) + "thing" (object, matter), formed as a compound pronoun meaning "each individual thing or matter."',
                'language_origins': 'Middle English',
                'example_sentence': 'After the storm, _______ in the garden needed to be replanted or repaired.',
                'memory_tip': 'Remember "EVERY-thing" - think "every single thing" meaning every object or matter, or "everything" means every individual thing that exists.'
            },
            'everywhere': {
                'definition': 'Everywhere is an adverb meaning in every place, at all locations, or throughout all areas within a particular scope. This comprehensive term describes universal presence or distribution across space, suggesting that something exists or occurs in all possible locations. Everywhere can refer to complete geographical coverage (found everywhere in the country), thorough distribution (everywhere you look), or universal occurrence (everywhere in the universe). The word emphasizes omnipresence and comprehensive spatial coverage. Everywhere often appears in descriptions of widespread phenomena, universal distributions, or thorough searches. The concept helps express ideas about ubiquity, universality, and complete spatial coverage. Understanding everywhere aids in describing comprehensive scope and universal presence. The term reflects human awareness of space and the desire to describe complete coverage or presence across all locations.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'EV-ree-wair',
                'etymology': 'From "every" (each individual) + "where" (at what place), formed as a compound adverb meaning "at each individual place."',
                'language_origins': 'Middle English',
                'example_sentence': 'The fragrance of blooming flowers could be detected _______ throughout the botanical garden.',
                'memory_tip': 'Remember "EVERY-where" - think "every single where" meaning every single place, or "everywhere" means every location where something can be.'
            },
            'eviction': {
                'definition': 'Eviction is the legal process of removing tenants from rental property, typically due to lease violations, non-payment of rent, or termination of rental agreements. This formal procedure must follow specific legal requirements and usually involves court proceedings to protect both landlord and tenant rights. Common grounds for eviction include failure to pay rent, property damage, unauthorized occupants, illegal activities, or lease term violations. The eviction process typically begins with proper notice to tenants, followed by legal filing if the issue remains unresolved. Successful eviction requires following state and local laws regarding notice periods, court procedures, and tenant rights. Tenants have various legal protections and may contest evictions in court. The process can be emotionally and financially difficult for all parties involved. Understanding eviction helps both landlords and tenants know their rights and responsibilities in rental relationships. Modern eviction laws balance property rights with housing security concerns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-VIK-shuhn',
                'etymology': 'From Latin "evictionem," from "evincere" (to overcome, expel), from "e-" (out) + "vincere" (to conquer).',
                'language_origins': 'Latin',
                'example_sentence': 'The landlord filed for _______ after the tenant failed to pay rent for three consecutive months.',
                'memory_tip': 'Remember "e-VIC-tion" - think "e-evict-tion" meaning the action of evicting, or "eviction" sounds like "he-victim" because it makes someone a victim of losing their home.'
            },
            'evidence': {
                'definition': 'Evidence consists of facts, information, objects, or testimony that support or prove a claim, theory, or belief. This crucial concept appears across multiple fields including law, science, history, and everyday reasoning. Legal evidence must meet specific standards of relevance, reliability, and admissibility to be accepted in court proceedings. Scientific evidence involves data, observations, and experimental results that support or refute hypotheses. Historical evidence includes documents, artifacts, and accounts that help reconstruct past events. Evidence can be direct (eyewitness testimony, photographs) or circumstantial (indirect indicators that suggest conclusions). The quality and quantity of evidence determine the strength of arguments and the credibility of conclusions. Evaluating evidence requires critical thinking skills to assess reliability, bias, and logical connections. Understanding evidence helps people make informed decisions, evaluate claims, and participate effectively in democratic processes that rely on factual information.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'EV-i-duhns',
                'etymology': 'From Old French "evidence," from Latin "evidentia" (clearness, proof), from "evidens" (clear, obvious), from "e-" (out) + "videre" (to see).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The detective carefully collected _______ from the crime scene to build a strong case.',
                'memory_tip': 'Remember "e-VID-ence" - think "e-video-ence" like video evidence that shows clearly, or "evidence" contains "vid" (see) meaning what you can see as proof.'
            },
            'evildoer': {
                'definition': 'An evildoer is a person who commits harmful, immoral, or wicked acts, deliberately causing suffering, damage, or injustice to others. This term encompasses individuals who engage in criminal behavior, moral wrongdoing, or actions that violate ethical standards and social norms. Evildoers may be motivated by personal gain, malice, ideology, or psychological factors that drive them to harm others. The concept appears frequently in religious, moral, and legal contexts where it\'s important to distinguish between those who cause harm and their victims. Historical and literary traditions often feature evildoers as antagonists who oppose justice, peace, and goodness. The term carries strong moral judgment and implies deliberate choice to engage in harmful behavior rather than accidental wrongdoing. Understanding evildoers helps recognize patterns of harmful behavior and the importance of justice systems designed to protect society from those who would cause deliberate harm.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EE-vuhl-doo-er',
                'etymology': 'From "evil" (Old English "yfel," meaning "bad, wicked") + "doer" (one who does), literally meaning "one who does evil."',
                'language_origins': 'Old English',
                'example_sentence': 'The community worked together to ensure that the _______ faced justice for their crimes.',
                'memory_tip': 'Remember "EVIL-doer" - think "evil-do-er" meaning someone who does evil things, or "evildoer" is simply someone who does evil actions.'
            },
            'evince': {
                'definition': 'To evince means to show, reveal, or demonstrate clearly, particularly qualities, emotions, or characteristics that might not be immediately obvious. This formal verb describes the act of making evident or manifest through actions, expressions, or behavior rather than direct statements. People evince intelligence through insightful comments, evince courage through brave actions, or evince concern through attentive behavior. The word suggests that internal qualities or feelings become visible through external manifestations. Evincing differs from simply showing because it often involves revealing something that was previously hidden or unclear. The term appears frequently in academic writing, literary criticism, and formal analysis where precise description of demonstrated qualities is important. Legal contexts might describe how evidence evinces guilt or innocence. Understanding evince helps recognize how people reveal their true nature, feelings, or capabilities through their actions and expressions rather than mere words.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-VINS',
                'etymology': 'From Latin "evincere" meaning "to overcome, prove clearly," from "e-" (out, thoroughly) + "vincere" (to conquer, prove).',
                'language_origins': 'Latin',
                'example_sentence': 'Her thoughtful questions and careful attention _______ a deep understanding of the complex subject.',
                'memory_tip': 'Remember "e-VINCE" - think "e-convince" meaning to convince by showing evidence, or "evince" sounds like "he-wins" meaning he wins by showing proof.'
            },
            'evolution': {
                'definition': 'Evolution is the process of gradual development and change over time, particularly referring to the biological theory that species develop and diversify through natural selection, genetic variation, and adaptation to environmental conditions. In biology, evolution explains how organisms change across generations through mechanisms including mutation, natural selection, genetic drift, and gene flow. The modern synthesis combines Darwin\'s theory of natural selection with Mendelian genetics and molecular biology to provide a comprehensive understanding of evolutionary processes. Evolution also applies to non-biological contexts, describing gradual development in technology, culture, ideas, languages, and institutions. Evolutionary thinking helps explain patterns of change, adaptation, and development across multiple disciplines. Evidence for biological evolution includes fossil records, comparative anatomy, molecular genetics, and observed natural selection. Understanding evolution provides insights into biodiversity, medicine, agriculture, and our understanding of life\'s history on Earth.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ev-uh-LOO-shuhn',
                'etymology': 'From Latin "evolutionem," from "evolvere" (to roll out, unfold), from "e-" (out) + "volvere" (to roll).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ of modern birds from dinosaur ancestors is supported by extensive fossil evidence.',
                'memory_tip': 'Remember "e-VOL-ution" - think "e-revolve-ution" meaning revolving/changing over time, or "evolution" contains "evolve" which means to develop gradually.'
            },
            'evolves': {
                'definition': 'Evolves is the third person singular present tense of "evolve," meaning develops gradually, changes over time, or transforms through natural processes. When something evolves, it undergoes gradual modification, adaptation, or development rather than sudden change. Biological evolution involves species changing across generations through genetic variation and natural selection. Cultural evolution describes how societies, languages, and traditions change over time. Technological evolution refers to gradual improvements and developments in tools, methods, and systems. Personal evolution might describe individual growth, learning, and development. The word suggests progressive change with direction and purpose rather than random variation. Understanding how things evolve helps recognize patterns of change, predict future developments, and appreciate the complexity of developmental processes. The concept emphasizes gradual transformation and adaptation in response to changing conditions or requirements.',
                'part_of_speech': 'verb (third person singular present)',
                'pronunciation_guide': 'ih-VOLVZ',
                'etymology': 'From "evolve" (from Latin "evolvere," meaning "to roll out, unfold") + "-s" (third person singular present ending).',
                'language_origins': 'Latin',
                'example_sentence': 'Technology _______ rapidly as engineers develop new solutions to emerging challenges.',
                'memory_tip': 'Remember "e-VOLVES" - think "e-revolves" meaning it revolves/turns into something new, or "evolves" is simply the present tense of evolve.'
            },
            'evzone': {
                'definition': 'An evzone is a member of an elite Greek military unit known for their distinctive traditional uniform and ceremonial duties, particularly famous for guarding the Tomb of the Unknown Soldier in Athens. These soldiers wear a unique outfit including a fustanella (kilt-like skirt), pom-pom shoes (tsarouchia), and other traditional elements that reflect Greek military heritage. The evzones perform an elaborate changing of the guard ceremony with precise, stylized movements that have become a popular tourist attraction and symbol of Greek national pride. Originally, evzones were light infantry units in the Greek army known for their agility and mountain warfare skills. The term comes from the Greek words meaning "well-girded" or "well-dressed," reflecting their distinctive appearance. Modern evzones are carefully selected based on height, physical fitness, and other criteria, and undergo extensive training in ceremonial duties. Understanding evzones helps appreciate Greek military tradition and the role of ceremonial units in preserving cultural heritage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EV-zohn',
                'etymology': 'From Greek "evzonos," from "eu-" (well) + "zone" (belt, girdle), literally meaning "well-belted" or "well-girded," referring to their distinctive dress.',
                'language_origins': 'Greek',
                'example_sentence': 'Tourists gathered to watch the _______ perform the ceremonial changing of the guard at the monument.',
                'memory_tip': 'Remember "EV-zone" - think "every-zone" because evzones guard every zone of Greek monuments, or "ev-zone" like "even-zone" meaning they keep even/precise formation.'
            },
            'ewer': {
                'definition': 'An ewer is a large pitcher or water jug with a wide mouth and handle, traditionally used for pouring water for washing hands and face. These vessels often feature an accompanying basin and were common household items before modern plumbing provided easy access to running water. Ewers were typically made from ceramic, metal, or glass and often featured decorative elements reflecting the artistic styles of their periods. In medieval and Renaissance times, ewers were essential items in wealthy households and were often ornately decorated with precious metals, enamel, or intricate patterns. The design usually includes a spout for controlled pouring and a handle for easy manipulation. Historical ewers serve as important artifacts for understanding daily life, artistic traditions, and technological development in different cultures and time periods. Modern ewers are primarily decorative items or specialized serving pieces used in formal dining or religious ceremonies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'YOO-er',
                'etymology': 'From Old French "ewiere," from Latin "aquaria" (relating to water), from "aqua" (water). Related to "aquarium" and other water-related terms.',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The antique _______ and basin set displayed the craftsman\'s skill in metalworking and decorative arts.',
                'memory_tip': 'Remember "EW-er" - think "water-er" because ewers hold water, or "ewer" sounds like "you-er" meaning you pour water with it.'
            },
            'exactly': {
                'definition': 'Exactly is an adverb meaning precisely, completely accurately, or in perfect agreement with something specified. This word emphasizes precision, correctness, and complete correspondence without deviation or approximation. Exactly can modify statements about measurements (exactly five inches), time (exactly noon), agreement (exactly right), or identity (exactly the same). The word often appears in contexts where precision is important, such as scientific measurements, legal documents, or technical specifications. Exactly can also express emphatic agreement or confirmation, as in responding "exactly!" to someone\'s statement. The term helps distinguish between approximate and precise descriptions, indicating that no margin of error or variation is intended. Understanding exactly helps communicate precision and accuracy while expressing strong agreement or confirmation. The word reflects human desire for precision and the importance of accuracy in many fields of endeavor.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ig-ZAKT-lee',
                'etymology': 'From "exact" (from Latin "exactus," meaning "precise, finished") + "-ly" (adverb suffix), literally meaning "in an exact manner."',
                'language_origins': 'Latin',
                'example_sentence': 'The recipe required _______ two cups of flour to achieve the proper consistency.',
                'memory_tip': 'Remember "e-XACT-ly" - think "exact-ly" meaning in an exact way, or "exactly" contains "exact" which means precise.'
            },
            'exaggerate': {
                'definition': 'To exaggerate means to represent something as larger, greater, better, or worse than it actually is; to overstate or magnify beyond the truth. This verb describes the act of stretching facts, embellishing details, or amplifying characteristics beyond their actual extent. Exaggeration can be intentional (for dramatic effect, humor, or persuasion) or unintentional (due to faulty memory, emotional influence, or misperception). Literary and artistic contexts often use exaggeration as a technique to create emphasis, comedy, or emotional impact. In everyday communication, people might exaggerate experiences to make stories more interesting or to express strong feelings. However, excessive exaggeration can undermine credibility and trust. The tendency to exaggerate is common in human communication and can serve social functions like entertainment or emphasis, but it requires balance with accuracy and honesty. Understanding exaggeration helps people evaluate information critically and communicate more effectively.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ig-ZAJ-uh-rayt',
                'etymology': 'From Latin "exaggeratus," from "exaggerare" (to heap up), from "ex-" (out, beyond) + "aggerare" (to pile up), from "agger" (heap).',
                'language_origins': 'Latin',
                'example_sentence': 'The fisherman tended to _______ the size of his catch when telling stories to his friends.',
                'memory_tip': 'Remember "ex-AGGER-ate" - think "extra-aggravate" meaning to aggravate/pile on extra details, or "exaggerate" sounds like "extra-great" meaning making things extra great/big.'
            },
            'examen': {
                'definition': 'Examen refers to a detailed examination, investigation, or spiritual practice of self-reflection and review. In religious contexts, particularly within Ignatian spirituality, the examen is a prayerful review of one\'s day, thoughts, and actions to discern God\'s presence and guidance. This spiritual discipline involves reflecting on experiences, recognizing moments of grace, acknowledging failings, and seeking direction for future actions. The practice typically includes gratitude for blessings, honest assessment of choices and responses, and prayer for guidance. Academic contexts use examen to describe thorough examination or investigation of subjects, texts, or problems. Legal contexts might refer to examen as detailed questioning or investigation of evidence and testimony. The word emphasizes careful, systematic review rather than casual observation. Understanding examen helps appreciate both spiritual practices aimed at growth and consciousness, and academic/professional practices focused on thorough investigation and analysis.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ig-ZAY-muhn',
                'etymology': 'From Latin "examen" meaning "examination, investigation," from "exigere" (to weigh, examine), from "ex-" (out) + "agere" (to drive, do).',
                'language_origins': 'Latin',
                'example_sentence': 'The daily _______ helped her reflect on her actions and grow in spiritual awareness.',
                'memory_tip': 'Remember "ex-AMEN" - think "ex-amen" like "examine-amen" combining examination with prayer, or "examen" sounds like "exam-in" meaning examining within oneself.'
            },
            'exas': {
                'definition': 'This appears to be an incomplete or corrupted word, possibly a fragment from PDF parsing. It could be part of words like "exasperate," "exact," "exalt," or other words beginning with "exa-." Without additional context, it\'s difficult to determine the intended complete word. This may represent a scanning or parsing error where part of a longer word was separated or truncated.',
                'part_of_speech': 'incomplete/error',
                'pronunciation_guide': 'N/A - incomplete word',
                'etymology': 'Appears to be incomplete word fragment',
                'language_origins': 'Unknown - incomplete',
                'example_sentence': 'N/A - This appears to be an incomplete word',
                'memory_tip': 'N/A - This is likely a scanning/parsing error'
            },
            'exasperate': {
                'definition': 'To exasperate means to irritate, annoy, or frustrate someone intensely, typically through persistent or repetitive actions that try their patience. This verb describes the process of causing someone to feel extremely annoyed, often to the point of anger or despair. Exasperation usually results from ongoing problems, repeated failures, or behaviors that seem unreasonable or unnecessary. Parents might become exasperated with children\'s misbehavior, teachers with students who don\'t listen, or customers with poor service. The word suggests that tolerance has been pushed to its limits through accumulated irritation rather than a single incident. Exasperating situations often involve elements beyond one\'s control or seemingly simple problems that prove persistently difficult to resolve. Understanding exasperation helps recognize when frustration reaches critical levels and the importance of patience, problem-solving, and sometimes stepping away from difficult situations. The emotion reflects human limits in dealing with ongoing stress and irritation.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ig-ZAS-puh-rayt',
                'etymology': 'From Latin "exasperatus," from "exasperare" (to make rough, irritate), from "ex-" (thoroughly) + "asper" (rough).',
                'language_origins': 'Latin',
                'example_sentence': 'The repeated computer crashes began to _______ the programmer working on the deadline.',
                'memory_tip': 'Remember "ex-ASPER-ate" - think "extra-asperity" (extra roughness/irritation), or "exasperate" sounds like "exhaust-rate" meaning it exhausts your patience at a high rate.'
            },
            'exaugural': {
                'definition': 'Exaugural refers to something relating to the end of an official term of office, particularly the conclusion of a presidency, governorship, or other high-ranking position. This adjective describes events, speeches, activities, or ceremonies that mark the departure from office rather than the beginning of service. Exaugural addresses are farewell speeches given by outgoing officials, often reflecting on their time in office and offering final thoughts or advice. The term contrasts with "inaugural," which relates to beginning a term of office. Exaugural events might include final ceremonies, transition activities, or symbolic acts that mark the end of an administration. The concept emphasizes the formal conclusion of official duties and the transfer of authority to successors. Understanding exaugural helps appreciate the ceremonial and practical aspects of political transitions and the importance of orderly transfer of power in democratic systems.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'eks-AW-gyuh-ruhl',
                'etymology': 'From Latin "ex-" (out of, from) + "augural" (relating to inauguration), literally meaning "out of inauguration" or "conclusion of office."',
                'language_origins': 'Latin',
                'example_sentence': 'The president\'s _______ address reflected on the achievements and challenges of his eight years in office.',
                'memory_tip': 'Remember "ex-AUGUR-al" - think "exit-inaugural" meaning the exit from inauguration/office, or "ex-augural" means formerly augural (formerly in office).'
            },
            'excavating': {
                'definition': 'Excavating is the present participle of "excavate," referring to the act of digging out, uncovering, or removing earth, rock, or other materials to create holes, trenches, or to uncover buried objects. This process is essential in construction, archaeology, mining, and landscaping projects. Archaeological excavating involves careful, systematic removal of soil layers to uncover artifacts, structures, and other evidence of past human activity. Construction excavating prepares sites for foundations, utilities, and infrastructure. The work requires specialized equipment ranging from hand tools for delicate archaeological work to heavy machinery for large-scale construction projects. Excavating must consider safety, environmental impact, and preservation of important findings. The process often reveals unexpected discoveries and requires expertise to interpret findings and proceed appropriately. Understanding excavating helps appreciate the complexity of earthwork operations and the importance of careful planning and execution in projects that disturb the ground.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'EKS-kuh-vay-ting',
                'etymology': 'From "excavate" (from Latin "excavatus," from "excavare" meaning "to hollow out") + "-ing" (present participle suffix).',
                'language_origins': 'Latin',
                'example_sentence': 'The archaeologists spent months carefully _______ the ancient settlement site.',
                'memory_tip': 'Remember "ex-CAV-ating" - think "ex-cave-ating" meaning creating caves/holes by removing material, or "excavating" contains "cave" which is what you make when digging.'
            },
            'excellence': {
                'definition': 'Excellence is the quality of being exceptionally good, superior, or outstanding in a particular area or overall performance. This noun represents the highest standard of achievement, characterized by exceptional skill, quality, or merit that distinguishes superior work from merely adequate performance. Excellence requires dedication, continuous improvement, attention to detail, and commitment to high standards. It appears in various contexts: academic excellence in scholarship, athletic excellence in sports, artistic excellence in creative works, and professional excellence in career performance. Excellence often involves not just meeting expectations but exceeding them consistently. The pursuit of excellence drives innovation, motivates personal growth, and raises standards across fields of endeavor. Understanding excellence helps recognize quality, set high goals, and appreciate exceptional achievement. The concept balances the aspiration for perfection with realistic acknowledgment of human limitations while inspiring continued improvement and dedication.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EK-suh-luhns',
                'etymology': 'From Latin "excellentia," from "excellens" (outstanding), from "excellere" (to surpass), from "ex-" (out, beyond) + "cellere" (to rise).',
                'language_origins': 'Latin',
                'example_sentence': 'The school\'s commitment to academic _______ attracted students from around the world.',
                'memory_tip': 'Remember "ex-CELL-ence" - think "extra-cellular" meaning going beyond normal cells/levels, or "excellence" sounds like "excel-ence" meaning the essence of excelling.'
            },
            'excelsior': {
                'definition': 'Excelsior has multiple meanings: it\'s a Latin word meaning "higher" or "ever upward" that serves as a motto for aspiration and improvement; it\'s also a trade name for fine wood shavings used as packing material or stuffing. As a motto, excelsior represents the drive to achieve greater heights, continuous improvement, and upward progress. The word appears on the New York State seal and has been adopted by various organizations as an inspirational motto. As a material, excelsior consists of thin, curled wood shavings traditionally used for packing fragile items, stuffing furniture, or as nesting material. The wood shavings are produced by specialized machines that create long, thin curls from wood blocks. Modern synthetic materials have largely replaced natural excelsior in many applications, but it remains useful for certain purposes. Understanding both meanings helps appreciate how the same word can represent both philosophical aspiration and practical material applications.',
                'part_of_speech': 'noun, interjection',
                'pronunciation_guide': 'ik-SEL-see-er',
                'etymology': 'From Latin "excelsior," comparative of "excelsus" (high, lofty), from "excellere" (to rise up, surpass), meaning "higher" or "more elevated."',
                'language_origins': 'Latin',
                'example_sentence': 'The organization adopted _______ as their motto to emphasize continuous improvement and reaching new heights.',
                'memory_tip': 'Remember "ex-CELS-ior" - think "excel-sior" meaning to excel more and more, or "excelsior" sounds like "excel-ior" meaning superior excelling.'
            },
            'except': {
                'definition': 'Except is a preposition and conjunction meaning "other than," "but," or "excluding," used to indicate that something is not included in a general statement or group. This word introduces exceptions to general rules, statements, or categories, specifying what is excluded from broader generalizations. Except can introduce single exceptions (everyone except John) or multiple exceptions (all colors except red and blue). The word helps create precise statements by clearly indicating what doesn\'t fall under general descriptions. In legal and formal writing, except serves important functions in defining scope, limitations, and specific exclusions. Understanding except helps create clear, accurate statements and avoid overgeneralization. The word reflects human need for precision in communication and the recognition that general rules often have specific exceptions. Proper use of except improves clarity and prevents misunderstanding in both spoken and written communication.',
                'part_of_speech': 'preposition, conjunction, verb',
                'pronunciation_guide': 'ik-SEPT',
                'etymology': 'From Latin "exceptus," past participle of "excipere" (to take out), from "ex-" (out) + "capere" (to take).',
                'language_origins': 'Latin',
                'example_sentence': 'All students passed the exam _______ those who missed the review session.',
                'memory_tip': 'Remember "ex-CEPT" - think "ex-accept" meaning not accepting/including something, or "except" sounds like "accept" but means the opposite - not accepting into the group.'
            },
            'exception': {
                'definition': 'An exception is something that is excluded from a general statement, rule, or principle; a case that does not conform to the usual pattern or expectation. This noun describes instances where normal rules, patterns, or generalizations do not apply, requiring special consideration or different treatment. Exceptions can be deliberate (legal exceptions to laws) or natural (unusual cases that don\'t fit typical patterns). The concept is fundamental to logical thinking, rule-making, and problem-solving, as it acknowledges that general principles rarely apply universally. Understanding exceptions helps people think more precisely, create better rules and policies, and recognize when special circumstances require different approaches. In computing, exceptions are error conditions that disrupt normal program flow. Legal exceptions provide specific circumstances where general laws don\'t apply. The phrase "the exception proves the rule" suggests that exceptions help define and confirm general principles by showing their boundaries.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SEP-shuhn',
                'etymology': 'From Latin "exceptionem," from "excipere" (to take out, exclude), from "ex-" (out) + "capere" (to take).',
                'language_origins': 'Latin',
                'example_sentence': 'With the _______ of rainy days, the outdoor market operates every Saturday throughout the year.',
                'memory_tip': 'Remember "ex-CEPT-ion" - think "ex-accept-ion" meaning the action of not accepting/including, or "exception" comes from "except" meaning something excepted from the rule.'
            },
            'excessive': {
                'definition': 'Excessive means going beyond what is normal, necessary, or appropriate; characterized by being too much, too extreme, or unreasonably abundant. This adjective describes quantities, behaviors, or conditions that exceed reasonable limits or proper boundaries. Excessive can apply to various contexts: excessive spending (beyond one\'s means), excessive noise (disturbing others), excessive heat (uncomfortable or dangerous), or excessive praise (more than warranted). The term implies negative judgment, suggesting that the amount or degree is problematic rather than beneficial. What constitutes excessive often depends on context, cultural norms, and individual circumstances. Excessive behaviors may indicate underlying problems, lack of self-control, or poor judgment. Understanding excessive helps recognize when moderation might be needed and appreciate the importance of balance in various aspects of life. The concept reflects human awareness of appropriate limits and the problems that can arise when those limits are exceeded.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-SES-iv',
                'etymology': 'From Latin "excessivus," from "excessus" (departure, excess), from "excedere" (to go beyond), from "ex-" (out) + "cedere" (to go).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ rainfall caused flooding throughout the river valley.',
                'memory_tip': 'Remember "ex-CESS-ive" - think "excess-ive" meaning having excess (too much), or "excessive" contains "excess" which means too much.'
            },
            'exchequer': {
                'definition': 'An exchequer is a treasury or government department responsible for collecting and managing public revenues and finances. The term originated in medieval England, where the royal treasury was called the Exchequer due to the checkered tablecloth used for counting money. Modern usage refers to national treasuries or finance departments in various countries, particularly those with British governmental traditions. The Chancellor of the Exchequer in the United Kingdom is equivalent to a finance minister or treasury secretary in other countries. Historical exchequers evolved from simple royal treasuries into complex governmental departments responsible for taxation, public spending, and financial administration. The exchequer system represents the development of systematic government finance management and the importance of organized revenue collection for state functioning. Understanding exchequers helps appreciate the evolution of public finance and the crucial role of treasury departments in modern government operations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EKS-chek-er',
                'etymology': 'From Old French "eschequier," from "eschec" (chess), referring to the checkered cloth used for calculations, related to "check" and "chess."',
                'language_origins': 'Old French',
                'example_sentence': 'The Chancellor of the _______ announced new tax policies in the annual budget speech.',
                'memory_tip': 'Remember "ex-CHEQ-uer" - think "ex-check-uer" because they check finances, or "exchequer" sounds like "exchange-er" meaning one who exchanges/manages money.'
            },
            'exchequerf': {
                'definition': 'This appears to be a corrupted or incomplete word, likely representing "exchequer" with an extra letter "f" added due to PDF parsing error. The intended word is probably "exchequer," which refers to a treasury or government finance department.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - corrupted word',
                'etymology': 'PDF parsing error - likely "exchequer" with added character',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This appears to be a corrupted word',
                'memory_tip': 'N/A - This is likely a parsing error'
            },
            'excision': {
                'definition': 'Excision is the surgical removal or cutting out of tissue, organs, or other body parts, typically performed to treat disease, remove tumors, or eliminate damaged tissue. This medical procedure involves precise cutting to remove specific areas while preserving surrounding healthy tissue. Excision can range from minor skin lesion removal to major organ resection. The term also applies more broadly to the act of cutting out or removing any unwanted part from something larger. Literary excision involves removing passages from texts, while editorial excision removes content from publications. The process requires skill and precision to achieve desired outcomes while minimizing damage to remaining structures. Post-excision care often involves wound healing, monitoring for complications, and sometimes reconstructive procedures. Understanding excision helps appreciate surgical precision and the medical decision-making involved in determining when removal is the best treatment option. The concept emphasizes targeted intervention to address specific problems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SIZH-uhn',
                'etymology': 'From Latin "excisionem," from "excidere" (to cut out), from "ex-" (out) + "caedere" (to cut).',
                'language_origins': 'Latin',
                'example_sentence': 'The surgeon performed a precise _______ to remove the tumor while preserving healthy tissue.',
                'memory_tip': 'Remember "ex-CIS-ion" - think "ex-scissors-ion" meaning cutting out with scissors, or "excision" contains "cision" (cutting) meaning cutting out.'
            },
            'exciting': {
                'definition': 'Exciting means causing enthusiasm, eagerness, or stimulation; characterized by the ability to generate strong positive emotions and interest. This adjective describes experiences, events, ideas, or situations that create feelings of anticipation, thrill, or energetic engagement. Exciting activities often involve novelty, challenge, adventure, or elements of unpredictability that capture attention and generate enthusiasm. What people find exciting varies greatly based on personality, interests, experience, and cultural background. Exciting can describe entertainment (exciting movies), opportunities (exciting job offers), discoveries (exciting research findings), or personal experiences (exciting travel). The word suggests positive arousal and engagement rather than anxiety or fear, though the physiological responses may be similar. Understanding what makes things exciting helps in planning engaging activities, creating compelling content, and recognizing factors that motivate and inspire people. The concept reflects human need for stimulation, novelty, and meaningful engagement.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-SAHY-ting',
                'etymology': 'From "excite" (from Latin "excitatus," meaning "to call forth, rouse") + "-ing" (adjective suffix).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ discovery of ancient artifacts transformed our understanding of the civilization.',
                'memory_tip': 'Remember "ex-CIT-ing" - think "ex-cite-ing" meaning calling forth excitement, or "exciting" comes from "excite" which means to stir up emotions.'
            },
            'exclamation': {
                'definition': 'An exclamation is a sudden cry or remark expressing strong emotion such as surprise, anger, delight, or pain. This form of expression typically involves heightened vocal intensity and emotional content that conveys the speaker\'s immediate reaction to events or situations. Exclamations can be single words (Help! Wow! Ouch!), phrases (What a surprise!), or longer statements delivered with emphatic tone. In writing, exclamations are marked by exclamation points to indicate the emotional intensity and vocal emphasis intended. Grammar recognizes exclamatory sentences as one of four basic sentence types, distinguished by their emotional expression rather than information content. Exclamations serve important social and emotional functions, allowing people to share immediate reactions and connect with others through emotional expression. Cultural differences affect what prompts exclamations and how they\'re expressed. Understanding exclamations helps recognize emotional communication and the role of spontaneous expression in human interaction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-skluh-MAY-shuhn',
                'etymology': 'From Latin "exclamationem," from "exclamare" (to cry out), from "ex-" (out) + "clamare" (to shout).',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ of joy could be heard throughout the house when she received the good news.',
                'memory_tip': 'Remember "ex-CLAM-ation" - think "ex-clamor-ation" meaning a loud clamor coming out, or "exclamation" contains "clam" (shout) meaning shouting out emotions.'
            },
            'excursion': {
                'definition': 'An excursion is a short journey or trip taken for pleasure, education, or specific purpose, typically involving departure from one\'s usual location and return the same day or after a brief stay. These organized or informal outings often focus on sightseeing, learning, recreation, or exploration of new places. School excursions provide educational experiences outside the classroom, while tourist excursions offer guided visits to local attractions. The term can also describe brief departures from main topics in conversation or writing, temporary deviations from normal routines, or exploratory investigations into new areas of interest. Excursions typically involve planning, specific destinations, and defined objectives or activities. Unlike extended vacations, excursions are characterized by their temporary nature and focus on particular experiences or goals. Understanding excursions helps appreciate the value of brief, focused travel experiences and the importance of stepping outside routine environments for learning and recreation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SKUR-zhuhn',
                'etymology': 'From Latin "excursionem," from "excurrere" (to run out), from "ex-" (out) + "currere" (to run).',
                'language_origins': 'Latin',
                'example_sentence': 'The nature club organized an _______ to the nearby botanical garden to study native plant species.',
                'memory_tip': 'Remember "ex-CURS-ion" - think "ex-course-ion" meaning going off course briefly, or "excursion" contains "cursor" (running) meaning running out for a trip.'
            },
            'execrable': {
                'definition': 'Execrable means extremely bad, detestable, or worthy of hatred and condemnation. This strong adjective describes things that are so poor in quality or offensive in nature that they provoke disgust, anger, or strong disapproval. Execrable can apply to various contexts: execrable behavior (morally reprehensible actions), execrable performance (extremely poor quality), execrable conditions (unbearably bad circumstances), or execrable taste (offensive aesthetic choices). The word carries much stronger negative connotation than merely "bad" or "poor," suggesting something that actively offends moral sensibilities or basic standards. Literary and critical contexts often use execrable to express particularly harsh judgment of artistic works, policies, or social conditions. The term implies not just inadequacy but active wrongness that deserves condemnation. Understanding execrable helps express strong negative judgment while recognizing degrees of badness and the human capacity for moral evaluation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EK-si-kruh-buhl',
                'etymology': 'From Latin "execrabilis," from "execrari" (to curse), from "ex-" (out, thoroughly) + "sacrare" (to consecrate), literally meaning "to curse thoroughly."',
                'language_origins': 'Latin',
                'example_sentence': 'The critic described the movie as an _______ waste of talent and resources.',
                'memory_tip': 'Remember "ex-ECRA-ble" - think "ex-excra" (extremely bad excrement), or "execrable" sounds like "execute-able" meaning worthy of execution because it\'s so bad.'
            },
            'exemplar': {
                'definition': 'An exemplar is a person, thing, or example that serves as a typical instance or excellent model of particular qualities or characteristics. This noun describes ideal representatives that embody the best features of their category and serve as standards for comparison or emulation. Exemplars can be individuals who demonstrate exceptional character (moral exemplars), achievements (professional exemplars), or skills (artistic exemplars). The term also applies to objects, works, or systems that represent the finest examples of their type. Unlike simple examples, exemplars carry connotations of excellence and worthiness of imitation. Scientific exemplars help establish standards and methods within fields, while cultural exemplars shape values and aspirations. Understanding exemplars helps recognize quality, set standards, and identify models worth emulating. The concept reflects human tendency to learn through imitation of superior examples and the importance of outstanding models in guiding development and improvement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ig-ZEM-plahr',
                'etymology': 'From Latin "exemplar," from "exemplum" (example), from "eximere" (to take out), from "ex-" (out) + "emere" (to take).',
                'language_origins': 'Latin',
                'example_sentence': 'She was considered an _______ of dedication and professionalism in her field.',
                'memory_tip': 'Remember "ex-EMPLAR" - think "example-ar" meaning a superior example, or "exemplar" sounds like "example-star" meaning a star example.'
            },
            'exercise': {
                'definition': 'Exercise refers to physical activity performed to improve or maintain health and fitness, or to the practice and application of skills, rights, or powers. As physical activity, exercise includes activities like walking, running, swimming, weightlifting, and sports that strengthen muscles, improve cardiovascular health, and enhance overall well-being. Regular exercise provides numerous health benefits including disease prevention, mood improvement, and increased longevity. Exercise can also mean the use or application of faculties, rights, or powers, such as exercising judgment, exercising authority, or exercising constitutional rights. Academic contexts use exercise to describe practice problems, drills, or activities designed to develop skills or knowledge. Military exercises are training activities that prepare forces for real situations. Understanding exercise helps appreciate both physical health maintenance and the important concept of actively using capabilities and rights to maintain and develop them.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'EK-ser-sahyz',
                'etymology': 'From Latin "exercitium," from "exercere" (to keep busy, practice), from "ex-" (out) + "arcere" (to keep away, confine).',
                'language_origins': 'Latin',
                'example_sentence': 'Regular _______ and proper nutrition are essential components of a healthy lifestyle.',
                'memory_tip': 'Remember "ex-ER-cise" - think "ex-exercise" meaning external activity for your body, or "exercise" sounds like "extra-size" meaning making muscles extra size.'
            },
            'exerts': {
                'definition': 'Exerts is the third person singular present tense of "exert," meaning applies force, pressure, or influence; puts forth effort or energy to accomplish something. When someone or something exerts, they actively use their power, strength, or influence to produce effects or achieve goals. Physical exertion involves applying muscular force or energy, while mental exertion involves concentrated thinking or problem-solving effort. Social or political exertion might involve using influence or authority to achieve desired outcomes. The word suggests active, purposeful application of available resources rather than passive existence or automatic function. Successful exertion often requires determination, persistence, and strategic application of effort. Understanding what exerts influence helps recognize power dynamics, cause-and-effect relationships, and the importance of active effort in achieving goals. The concept emphasizes human agency and the ability to influence outcomes through deliberate action.',
                'part_of_speech': 'verb (third person singular present)',
                'pronunciation_guide': 'ig-ZURTS',
                'etymology': 'From "exert" (from Latin "exertus," from "exerere" meaning "to put forth") + "-s" (third person singular ending).',
                'language_origins': 'Latin',
                'example_sentence': 'The moon _______ gravitational pull that influences ocean tides around the world.',
                'memory_tip': 'Remember "ex-ERTS" - think "extra-erts" meaning putting out extra effort, or "exerts" sounds like "experts" who expertly apply their skills.'
            },
            'exeunt': {
                'definition': 'Exeunt is a Latin stage direction meaning "they exit" or "they go out," used in theatrical scripts to indicate that multiple characters leave the stage simultaneously. This term appears frequently in classical drama, particularly in works by Shakespeare and other playwrights writing in Latin-influenced traditions. The word contrasts with "exit" (one person leaves) and represents formal theatrical terminology that has been preserved in modern dramatic literature. Exeunt typically appears at the end of scenes or acts when all or most characters depart together, often marking significant dramatic transitions. The term reflects the historical use of Latin in educated and artistic contexts, and its retention in modern theater demonstrates the continuity of theatrical traditions. Understanding exeunt helps appreciate theatrical conventions and the formal language used in dramatic literature. The word exemplifies how specialized terminology preserves historical practices and maintains precision in artistic contexts.',
                'part_of_speech': 'verb (stage direction)',
                'pronunciation_guide': 'EK-see-uhnt',
                'etymology': 'From Latin "exeunt," third person plural present of "exire" (to go out), from "ex-" (out) + "ire" (to go).',
                'language_origins': 'Latin',
                'example_sentence': 'The script indicated "_______ all" to show that every character should leave the stage together.',
                'memory_tip': 'Remember "ex-E-unt" - think "exit-unt" meaning they all exit, or "exeunt" sounds like "exit-hunt" meaning hunting for the exit together.'
            },
            'exhalation': {
                'definition': 'Exhalation is the process of breathing out, expelling air from the lungs through the nose or mouth as part of the respiratory cycle. This essential physiological function removes carbon dioxide and other waste gases from the body while helping regulate blood pH and body temperature. During exhalation, the diaphragm relaxes and moves upward, reducing lung volume and forcing air out. The term can also refer metaphorically to the release or emission of substances, emotions, or energy. In meditation and yoga practices, conscious control of exhalation is used for relaxation and mindfulness. Medical contexts study exhalation patterns to diagnose respiratory conditions and monitor lung function. Environmental science examines exhalation of gases from various sources. Understanding exhalation helps appreciate respiratory health, the importance of breathing techniques for wellness, and the continuous exchange of gases that sustains life.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eks-huh-LAY-shuhn',
                'etymology': 'From Latin "exhalationem," from "exhalare" (to breathe out), from "ex-" (out) + "halare" (to breathe).',
                'language_origins': 'Latin',
                'example_sentence': 'The yoga instructor emphasized slow, controlled _______ to promote relaxation and stress relief.',
                'memory_tip': 'Remember "ex-HAL-ation" - think "ex-inhale-ation" meaning the action of exhaling, or "exhalation" contains "hale" (breath) meaning breathing out.'
            },
            'exhaust': {
                'definition': 'Exhaust has multiple meanings: as a verb, it means to use up completely, drain of energy, or tire out thoroughly; as a noun, it refers to waste gases expelled from engines or the system that removes these gases. Exhausting someone involves depleting their physical or mental energy through demanding activities or prolonged effort. Exhausting resources means using them up completely, leaving nothing remaining. Vehicle exhaust consists of burned fuel byproducts expelled through exhaust systems, often containing pollutants that require environmental regulation. Industrial exhaust includes waste gases and heat removed from manufacturing processes. The word suggests thorough depletion or removal rather than partial use. Understanding exhaust helps recognize limits of human energy, resource conservation needs, and environmental impacts of combustion processes. The concept emphasizes the importance of rest, sustainable resource use, and pollution control in maintaining health and environmental quality.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'ig-ZAWST',
                'etymology': 'From Latin "exhaustus," from "exhaurire" (to draw out, drain), from "ex-" (out) + "haurire" (to draw, drain).',
                'language_origins': 'Latin',
                'example_sentence': 'The long hiking trail began to _______ even the most experienced climbers.',
                'memory_tip': 'Remember "ex-HAUST" - think "ex-haul" meaning hauling out all energy, or "exhaust" sounds like "exit-aust" meaning energy exits and is lost.'
            },
            'exhibition': {
                'definition': 'An exhibition is a public display of works of art, products, skills, or other items of interest organized for viewing by an audience. These curated presentations serve various purposes including education, entertainment, promotion, and cultural enrichment. Art exhibitions showcase paintings, sculptures, photography, or other creative works in galleries or museums. Trade exhibitions allow businesses to display products and services to potential customers and industry professionals. Educational exhibitions present information about scientific discoveries, historical events, or cultural topics. The term can also refer to demonstrations of skill or behavior, such as athletic exhibitions or public performances. Successful exhibitions require careful planning, organization, and presentation to effectively communicate with their intended audiences. Understanding exhibitions helps appreciate curatorial practices, the role of public display in education and culture, and the importance of accessibility in sharing knowledge and creativity with diverse audiences.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-suh-BISH-uhn',
                'etymology': 'From Latin "exhibitionem," from "exhibere" (to show, present), from "ex-" (out) + "habere" (to have, hold).',
                'language_origins': 'Latin',
                'example_sentence': 'The museum\'s new _______ featured contemporary sculptures from artists around the world.',
                'memory_tip': 'Remember "ex-HIB-ition" - think "ex-exhibit-ition" meaning the action of exhibiting, or "exhibition" contains "exhibit" which means to show publicly.'
            },
            'exhibits': {
                'definition': 'Exhibits can function as both a noun (plural of exhibit) and a verb (third person singular present). As a noun, exhibits are items displayed in museums, galleries, trade shows, or other venues for public viewing and education. These displayed objects, artworks, specimens, or demonstrations serve to inform, educate, or entertain audiences. Museum exhibits might include historical artifacts, scientific specimens, or interactive displays. Legal exhibits are pieces of evidence presented in court proceedings. As a verb, exhibits means shows, displays, or demonstrates particular qualities, behaviors, or characteristics. Someone exhibits courage through brave actions or exhibits symptoms when showing signs of illness. The word emphasizes the act of making visible or apparent what might otherwise be hidden or unclear. Understanding exhibits helps appreciate how institutions share knowledge and how individuals reveal their qualities through actions and expressions.',
                'part_of_speech': 'noun (plural), verb (third person singular present)',
                'pronunciation_guide': 'ig-ZIB-its',
                'etymology': 'From "exhibit" (from Latin "exhibitus," from "exhibere" meaning "to show, present") + "-s" (plural/verb ending).',
                'language_origins': 'Latin',
                'example_sentence': 'The natural history museum _______ a remarkable collection of dinosaur fossils.',
                'memory_tip': 'Remember "ex-HIB-its" - think "ex-habits" meaning showing external habits/behaviors, or "exhibits" comes from "exhibit" meaning to show or display.'
            },
            'exhilaration': {
                'definition': 'Exhilaration is an intense feeling of excitement, happiness, and energetic enthusiasm, often accompanied by a sense of freedom and elevated mood. This powerful emotional state involves heightened arousal and positive feelings that make people feel alive, energized, and joyful. Exhilaration can result from various experiences including physical activities (riding roller coasters, extreme sports), achievements (winning competitions, reaching goals), natural phenomena (beautiful sunsets, mountain views), or social interactions (celebrations, performances). The emotion often includes physical sensations such as increased heart rate, heightened awareness, and a sense of lightness or energy. Unlike simple happiness, exhilaration involves a more intense, almost euphoric quality that can be briefly overwhelming in its intensity. Understanding exhilaration helps recognize peak positive experiences and the activities or circumstances that generate these powerful emotional responses. The concept reflects human capacity for intense joy and the importance of experiences that elevate mood and energy.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ig-zil-uh-RAY-shuhn',
                'etymology': 'From Latin "exhilarationem," from "exhilarare" (to make cheerful), from "ex-" (thoroughly) + "hilarare" (to cheer), from "hilarus" (cheerful).',
                'language_origins': 'Latin',
                'example_sentence': 'The climbers felt overwhelming _______ when they finally reached the summit after days of difficult hiking.',
                'memory_tip': 'Remember "ex-HIL-aration" - think "extra-hilarious-ation" meaning extremely cheerful state, or "exhilaration" contains "hilar" (cheerful) meaning being thoroughly cheerful.'
            },
            'exiguous': {
                'definition': 'Exiguous means extremely scanty, meager, or inadequate in amount; pitifully small or insufficient for needs or requirements. This formal adjective describes quantities, resources, or provisions that are so limited as to be barely adequate or entirely insufficient. Exiguous can apply to various contexts: exiguous funds (very little money), exiguous portions (tiny servings), exiguous evidence (insufficient proof), or exiguous living conditions (cramped, inadequate housing). The word carries connotations of insufficiency that creates hardship or difficulty. Unlike simply "small," exiguous suggests that the smallness is problematic and creates challenges for those affected. Literary and academic writing often uses exiguous to describe circumstances of deprivation or scarcity. Understanding exiguous helps express degrees of inadequacy and recognize when limited resources create genuine hardship rather than mere inconvenience. The concept emphasizes the relationship between availability and need.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ig-ZIG-yoo-uhs',
                'etymology': 'From Latin "exiguus" meaning "scanty, small," from "exigere" (to weigh out, measure), from "ex-" (out) + "agere" (to drive).',
                'language_origins': 'Latin',
                'example_sentence': 'The refugees survived on _______ rations that barely provided enough nutrition to sustain them.',
                'memory_tip': 'Remember "ex-IG-uous" - think "extremely-insignificant-uous" meaning extremely insignificant in amount, or "exiguous" sounds like "exit-you-us" meaning so little it exits/leaves you with almost nothing.'
            },
            'exiguousexodus': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "exiguous" (extremely scanty or meager) and "exodus" (a mass departure of people). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'exile': {
                'definition': 'Exile is the state of being banished from one\'s native country or home, typically as a punishment or due to political circumstances, or it can refer to a person who has been banished. This condition involves forced separation from familiar places, people, and cultural contexts, often creating profound emotional and practical challenges. Political exile occurs when governments expel opponents or dissidents, while voluntary exile might involve leaving to escape persecution or seek better opportunities. Historical examples include religious exiles fleeing persecution and political exiles escaping authoritarian regimes. Exile can be temporary or permanent, depending on circumstances and possibilities for return. The experience often involves loss of citizenship rights, social connections, and cultural identity, while requiring adaptation to new environments. Understanding exile helps appreciate human displacement, refugee experiences, and the importance of home and belonging in human life. The concept reflects both punishment through separation and the resilience of displaced people.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'EG-zahyl',
                'etymology': 'From Old French "exil," from Latin "exilium," from "exul" (banished person), possibly from "ex-" (out of) + "solum" (soil, ground).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The political activist spent twenty years in _______ before returning to his homeland.',
                'memory_tip': 'Remember "ex-ILE" - think "exit-isle" meaning exiting your island/homeland, or "exile" sounds like "ex-aisle" meaning being pushed out of the aisle/community.'
            },
            'existence': {
                'definition': 'Existence is the fact or state of being alive, present, or real; the condition of having objective reality or being. This fundamental philosophical concept encompasses what it means to be, to have being, or to occur in reality. Existence can refer to individual life (human existence), the presence of things in the world (the existence of gravity), or abstract concepts (the existence of justice). Philosophical discussions of existence explore questions about consciousness, reality, purpose, and meaning. Different philosophical traditions offer varying perspectives on the nature of existence and its relationship to consciousness, experience, and reality. Scientific approaches study existence through observation and measurement of phenomena. Religious and spiritual traditions often connect existence to divine purpose or cosmic meaning. Understanding existence helps people grapple with fundamental questions about reality, meaning, and their place in the universe.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ig-ZIS-tuhns',
                'etymology': 'From Late Latin "existentia," from Latin "existens," present participle of "existere" (to emerge, appear), from "ex-" (out) + "sistere" (to stand).',
                'language_origins': 'Latin',
                'example_sentence': 'Philosophers have debated the nature and meaning of human _______ for thousands of years.',
                'memory_tip': 'Remember "ex-IS-tence" - think "exist-ence" meaning the quality of existing, or "existence" contains "exist" which means to be real.'
            },
            'existential': {
                'definition': 'Existential refers to human existence, particularly the experience of being alive and conscious, or to the philosophical movement that emphasizes individual existence, freedom, and choice. In philosophy, existentialism focuses on the condition of existence as experienced by individuals, emphasizing personal responsibility, authenticity, and the creation of meaning in an apparently meaningless universe. Existential questions explore fundamental concerns about purpose, death, freedom, isolation, and meaning. Existential psychology examines how people cope with universal human concerns and create meaning in their lives. The term can also describe situations or crises that threaten fundamental aspects of existence or identity. Existential literature and art often explore themes of alienation, anxiety, freedom, and the search for authentic existence. Understanding existential concepts helps people grapple with fundamental questions about life\'s meaning and their responsibility for creating purpose and direction in their own lives.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'eg-zi-STEN-shuhl',
                'etymology': 'From "existence" + "-ial" (suffix meaning "relating to"), meaning "relating to existence." Associated with existentialist philosophy developed in the 20th century.',
                'language_origins': 'Latin, modern philosophical usage',
                'example_sentence': 'The novel explored _______ themes about the meaning of life and individual responsibility.',
                'memory_tip': 'Remember "exist-ENT-ial" - think "exist-ential" meaning relating to existence, or "existential" comes from "existence" meaning relating to being alive and conscious.'
            },
            'exodus': {
                'definition': 'Exodus refers to a mass departure of people, particularly the biblical account of the Israelites\' departure from Egypt under Moses\' leadership, or any large-scale migration or evacuation. The biblical Exodus represents a foundational narrative in Jewish, Christian, and Islamic traditions, describing liberation from slavery and the journey toward the Promised Land. Modern usage extends to any significant mass movement of people, such as urban exodus to suburbs, rural exodus to cities, or refugee exodus from conflict zones. Exodus can be voluntary (seeking better opportunities) or forced (fleeing danger or persecution). The term emphasizes the scale and significance of departure rather than simple relocation. Historical and contemporary examples include population movements driven by economic, political, environmental, or social factors. Understanding exodus helps recognize patterns of human migration and the factors that drive large-scale population movements throughout history.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EK-suh-duhs',
                'etymology': 'From Greek "exodus," from "ex-" (out) + "hodos" (way, road), literally meaning "a way out." Adopted from the title of the second book of the Bible.',
                'language_origins': 'Greek',
                'example_sentence': 'The economic collapse triggered an _______ of young professionals seeking opportunities in other countries.',
                'memory_tip': 'Remember "ex-ODUS" - think "exit-odus" meaning a massive exit, or "exodus" sounds like "exit-us" meaning all of us exiting together.'
            },
            'exogenous': {
                'definition': 'Exogenous means originating from outside a particular system, organism, or process rather than arising internally. This scientific and academic term appears across multiple disciplines to distinguish external influences from internal ones. In biology, exogenous substances come from outside the body (exogenous hormones from medications vs. endogenous hormones produced naturally). Economics uses exogenous to describe external factors that influence systems but aren\'t determined by them (exogenous shocks like natural disasters affecting markets). Psychology might discuss exogenous depression caused by external events vs. endogenous depression from internal biochemical factors. The concept helps scientists and researchers identify sources of change, influence, or variation in their studies. Understanding exogenous factors is crucial for proper analysis, control of variables, and attribution of causes. The term emphasizes the importance of considering external influences when studying any system or process.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ek-SOJ-uh-nuhs',
                'etymology': 'From Greek "exo-" (outside) + "genes" (born, produced), literally meaning "produced outside" or "originating externally."',
                'language_origins': 'Greek',
                'example_sentence': 'The researcher controlled for _______ variables that might influence the experimental results.',
                'memory_tip': 'Remember "exo-GEN-ous" - think "external-generation" meaning generated externally, or "exogenous" contains "exo" (outside) meaning coming from outside.'
            },
            'exoneration': {
                'definition': 'Exoneration is the act of officially clearing someone from blame, fault, or responsibility for wrongdoing; the process of proving innocence or removing accusations. This legal and moral concept involves demonstrating that previously held beliefs about someone\'s guilt or responsibility were incorrect. Legal exoneration occurs when new evidence proves a convicted person\'s innocence, leading to overturned convictions and formal declarations of innocence. The process often involves reviewing evidence, investigating alternative explanations, and sometimes DNA testing or other scientific methods. Exoneration can be partial (clearing someone of some but not all charges) or complete (proving total innocence). The concept extends beyond legal contexts to include moral, social, or professional vindication. Exoneration projects work to identify and correct wrongful convictions, highlighting problems in justice systems. Understanding exoneration helps appreciate the importance of due process, the fallibility of human judgment, and the need for mechanisms to correct errors in accusation and conviction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ig-zon-uh-RAY-shuhn',
                'etymology': 'From Latin "exonerationem," from "exonerare" (to unburden, discharge), from "ex-" (off, away) + "onus" (burden, load).',
                'language_origins': 'Latin',
                'example_sentence': 'DNA evidence led to the _______ of the wrongfully convicted man after fifteen years in prison.',
                'memory_tip': 'Remember "ex-ONER-ation" - think "ex-owner-ation" meaning no longer owning the blame, or "exoneration" contains "onus" (burden) meaning removing the burden of guilt.'
            }
        }
        
        return batch_063_data.get(word, {
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
            
            # Check for combined word errors and corrupted words
            is_error = False
            error_message = ""
            
            combined_words = ['exiguousexodus']
            corrupted_words = ['exchequerf', 'exas']
            
            if word in combined_words:
                is_error = True
                if word == 'exiguousexodus':
                    error_message = 'Combined word error: "exiguousexodus" appears to be "exiguous" + "exodus" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                errors_found.append(f"  - {word}: {error_message}")
            elif word in corrupted_words:
                is_error = True
                if word == 'exchequerf':
                    error_message = 'Corrupted word: "exchequerf" appears to be "exchequer" with an extra "f" added. This is likely a PDF parsing error.'
                elif word == 'exas':
                    error_message = 'Incomplete word: "exas" appears to be a fragment, possibly from words like "exasperate", "exact", "exalt", etc. This is likely a PDF parsing error where part of a word was truncated.'
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
        
        print("Batch 063 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch063Processor()
    processor.process_batch("batch_063_words.csv", "batch_063_processed.csv")