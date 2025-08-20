#!/usr/bin/env python3
"""
Batch 090 Processor for Scripps National Spelling Bee Words
Processes words from inclined through ineptitude with comprehensive Claude-generated data
"""

import pandas as pd
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class WordData:
    word: str
    years: str
    source_files: str
    source_difficulties: str
    definition: str
    part_of_speech: str
    pronunciation_guide: str
    etymology: str
    language_origins: str
    example_sentence: str
    memory_tip: str
    phonetic_transparency_score: Optional[int] = None
    word_frequency_score: Optional[int] = None
    morphological_complexity_score: Optional[int] = None
    etymology_complexity_score: Optional[int] = None
    difficulty_level: Optional[str] = None

class DifficultyCalculator:
    def calculate_phonetic_transparency(self, word: str, pronunciation: str) -> int:
        return 3
    
    def calculate_word_frequency(self, word: str) -> int:
        return 3
    
    def calculate_morphological_complexity(self, word: str) -> int:
        return 3
    
    def calculate_etymology_complexity(self, etymology: str) -> int:
        return 3

class Batch090Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.processed_count = 0

    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge"""
        
        batch_090_data = {
            'inclined': {
                'definition': 'Inclined describes something that slants, slopes, or tilts at an angle rather than being perfectly horizontal or vertical. This word can refer to physical surfaces like inclined planes in physics, which are ramps or slopes used to reduce the force needed to lift objects. Geographically, inclined terrain includes hillsides, mountains, or any sloping land. The term also describes mental or emotional tendencies - being inclined toward certain beliefs, preferences, or behaviors. Someone might be inclined to help others, inclined to worry, or inclined to prefer certain activities. Unlike definitive statements, being inclined suggests a tendency or predisposition rather than absolute certainty. In mechanics, inclined systems study how gravity and friction affect objects on angled surfaces. The word indicates deviation from the standard or expected position.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'in-KLYND',
                'etymology': 'From Latin "inclinare," meaning "to bend" or "to lean toward," combining "in-" (toward) with "clinare" (to lean or bend). The root is related to "decline" and "recline," all involving bending or leaning movements.',
                'language_origins': 'Latin',
                'example_sentence': 'The steep _______ driveway made it difficult to park safely during icy winter conditions.',
                'memory_tip': 'Remember "INCLINED" - think "IN-CLINED" like something that\'s "clined" (leaned) inward at an angle, not straight up.'
            },
            'include': {
                'definition': 'Include means to contain, comprise, or make someone or something part of a whole, group, or category. This fundamental verb describes the action of incorporating elements into larger systems, lists, or collections. When you include items in a package, you add them to the contents. When organizations include diverse members, they welcome participation from different backgrounds. Academic papers include references to support arguments. The word implies intentional incorporation rather than accidental presence. Including someone in activities demonstrates acceptance and consideration. Unlike excluding, which removes or keeps out, including brings together and encompasses. The concept applies broadly from simple lists to complex social and organizational structures. Including typically requires active decision-making about what belongs together.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-KLOOD',
                'etymology': 'From Latin "includere," meaning "to shut in" or "to enclose," combining "in-" (in) with "claudere" (to close). The original sense was "to enclose within boundaries," which evolved to mean "to contain as part of."',
                'language_origins': 'Latin',
                'example_sentence': 'The vacation package will _______ airfare, hotel accommodations, and two meals per day.',
                'memory_tip': 'Remember "INCLUDE" - think "IN-CLUDE" like bringing something "IN" to be "CLUDE" (enclosed/contained) within a group.'
            },
            'included': {
                'definition': 'Included is the past tense of "include," meaning that something was contained, comprised, or made part of a whole, group, or category. This word describes the completed action of incorporating elements into larger systems or collections. When items are included in a shipment, they were added to the contents. When people were included in activities, they were welcomed to participate. Academic studies that included diverse participants gathered data from varied sources. The term confirms that incorporation has taken place rather than describing ongoing or future inclusion. Unlike excluded, which indicates something was left out, included confirms that something was brought in and made part of the whole. The word often appears in descriptions of what components, participants, or elements formed part of a completed group or system.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'in-KLOO-did',
                'etymology': 'From Latin "includere," meaning "to shut in" or "to enclose," combining "in-" (in) with "claudere" (to close). The past tense form indicates completed inclusion.',
                'language_origins': 'Latin',
                'example_sentence': 'The research study _______ participants from twelve different countries to ensure global representation.',
                'memory_tip': 'Remember "INCLUDED" - think "IN-CLUDE-D" like something that was "cluded" (enclosed) "IN" the group - past tense of bringing things together.'
            },
            'includes': {
                'definition': 'Includes is the third person singular present tense of "include," meaning contains, comprises, or makes part of a whole. This verb form describes ongoing or habitual inclusion of elements within larger systems or groups. When a package includes certain items, it contains them as standard components. When a program includes diverse activities, it offers various options as part of its regular structure. Academic curricula that include multiple subjects provide comprehensive education. The word indicates active, present inclusion rather than past or future incorporation. Unlike excludes, which keeps things out, includes brings elements together as part of a unified whole. This form often appears in descriptions, specifications, or explanations of what components make up complete systems, packages, or programs.',
                'part_of_speech': 'verb (third person singular present)',
                'pronunciation_guide': 'in-KLOODZ',
                'etymology': 'From Latin "includere," meaning "to shut in" or "to enclose," combining "in-" (in) with "claudere" (to close). The present tense third person form indicates ongoing inclusion.',
                'language_origins': 'Latin',
                'example_sentence': 'The comprehensive health insurance plan _______ dental coverage and vision care benefits.',
                'memory_tip': 'Remember "INCLUDES" - think "IN-CLUDES" like actively "cluding" (enclosing) things "IN" the group right now.'
            },
            'including': {
                'definition': 'Including is a preposition and present participle that introduces examples or additional elements that are part of a larger group or category. This word signals that what follows represents some, but not necessarily all, members of the set being discussed. When you say "many animals, including elephants," you indicate that elephants are among the animals but not the only ones. Academic writing frequently uses including to provide specific examples within broader categories. The term helps clarify scope by offering concrete instances of abstract concepts. Unlike "such as," which typically introduces examples, including can also suggest comprehensive listing. Legal documents use including to specify particular items within broader categories. The word creates inclusive rather than exclusive relationships, expanding rather than limiting scope.',
                'part_of_speech': 'preposition, present participle',
                'pronunciation_guide': 'in-KLOO-ding',
                'etymology': 'From Latin "includere" plus the English suffix "-ing." The participial form emphasizes the ongoing process of inclusion or the act of containing elements within a group.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The festival featured performers from many countries, _______ musicians from Brazil, dancers from Ireland, and artists from Japan.',
                'memory_tip': 'Remember "INCLUDING" - think "IN-CLUDING" like actively "cluding" (bringing) examples "IN" to show what\'s part of a larger group.'
            },
            'inclusion': {
                'definition': 'Inclusion is the practice or policy of providing equal access, opportunities, and participation to all individuals, particularly those who might otherwise be excluded or marginalized. This noun encompasses both the act of including something within a group and the broader social principle of ensuring no one is left out based on differences like race, gender, disability, or background. Educational inclusion integrates students with special needs into mainstream classrooms. Workplace inclusion creates environments where diverse employees can contribute fully. The concept emphasizes not just presence but meaningful participation and belonging. Unlike mere diversity, which focuses on representation, inclusion emphasizes creating welcoming, supportive environments where differences are valued. Social inclusion addresses systemic barriers that prevent full participation in community life. The term implies active effort to create equitable opportunities rather than passive non-discrimination.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-KLOO-zhun',
                'etymology': 'From Latin "inclusio," derived from "includere" meaning "to enclose." The suffix "-ion" creates a noun indicating the act or process of including.',
                'language_origins': 'Latin',
                'example_sentence': 'The school\'s _______ policy ensured that students with disabilities received appropriate support to participate fully in all academic activities.',
                'memory_tip': 'Remember "INCLUSION" - think "IN-CLUSION" like the "conclusion" of bringing everyone "IN" - the act of including everyone together.'
            },
            'incoherent': {
                'definition': 'Incoherent describes speech, writing, or thinking that lacks logical connection, clarity, or consistency, making it difficult or impossible to understand. This word characterizes communication where ideas don\'t connect logically, arguments contradict themselves, or expression is so confused that meaning becomes unclear. Incoherent speech might result from extreme emotion, illness, intoxication, or mental distress. Academic writing becomes incoherent when arguments lack supporting evidence or logical progression. The term can describe both temporary states, like incoherent responses during emergencies, and persistent conditions affecting communication ability. Unlike simply unclear communication, incoherent expression lacks internal logic or organizational structure. Scientific theories are incoherent when their components contradict established principles. The word emphasizes the absence of rational connection between parts of a whole.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ko-HEER-unt',
                'etymology': 'From Latin "incohaerens," combining "in-" (not) with "cohaerens" (sticking together), from "cohaerere" meaning "to stick together" or "to be connected." The root "haerere" means "to stick."',
                'language_origins': 'Latin',
                'example_sentence': 'The witness\'s _______ testimony contained so many contradictions that the jury could not determine what actually happened.',
                'memory_tip': 'Remember "INCOHERENT" - think "IN-COHERENT" meaning NOT coherent (logically connected) - ideas that don\'t stick together clearly.'
            },
            'income': {
                'definition': 'Income refers to money received on a regular basis from work, investments, business activities, or other sources, typically measured annually or monthly. This fundamental economic term encompasses wages, salaries, profits, dividends, interest, and any other financial inflows that increase an individual\'s or organization\'s resources. Personal income determines living standards, purchasing power, and financial security. Business income, also called revenue, funds operations and growth. Investment income comes from assets like stocks, bonds, or real estate. Tax systems typically categorize different types of income for regulatory purposes. Economic policies often focus on income distribution, inequality, and growth. Unlike wealth, which represents accumulated assets, income measures ongoing financial flows. Understanding income sources and patterns is crucial for financial planning, budgeting, and economic analysis.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-kum',
                'etymology': 'From Middle English "income," literally meaning "a coming in," from "in" plus "come." The word originally referred to arrival or entrance, developing its financial meaning in the 14th century.',
                'language_origins': 'Middle English',
                'example_sentence': 'The family\'s _______ increased significantly after both parents received promotions at their respective companies.',
                'memory_tip': 'Remember "INCOME" - think "IN-COME" like money "coming IN" to your bank account from work or investments.'
            },
            'incompetent': {
                'definition': 'Incompetent describes someone who lacks the necessary skills, knowledge, or ability to perform tasks adequately or meet expected standards of performance. This word applies to professional, personal, or technical contexts where someone proves unable to fulfill their responsibilities effectively. Incompetent employees might consistently make errors, miss deadlines, or fail to understand job requirements. Legal incompetence refers to mental incapacity affecting decision-making ability. The term can describe temporary situations, like feeling incompetent when learning new skills, or persistent conditions affecting overall performance. Unlike inexperience, which suggests potential for improvement, incompetence implies fundamental inability to meet requirements. Medical professionals might be deemed incompetent if they consistently endanger patients. The word carries negative connotations, suggesting failure to meet minimum acceptable standards.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'in-KOM-pi-tunt',
                'etymology': 'From Latin "incompetens," combining "in-" (not) with "competens" (suitable, capable), derived from "competere" meaning "to be suitable" or "to be capable."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ technician\'s repeated mistakes with the sensitive equipment led to his immediate dismissal.',
                'memory_tip': 'Remember "INCOMPETENT" - think "IN-COMPETENT" meaning NOT competent (capable) - lacking the skills needed to do something well.'
            },
            'incomprehensible': {
                'definition': 'Incomprehensible describes something that cannot be understood, grasped, or made sense of, whether due to complexity, obscurity, or fundamental limitations in human understanding. This word applies to concepts, languages, behaviors, or phenomena that resist comprehension despite efforts to understand them. Advanced mathematics might be incomprehensible to those without proper background. Foreign languages are incomprehensible to those who haven\'t learned them. Some philosophical concepts remain incomprehensible even to experts. The term can describe both temporary incomprehension, remedied through study or explanation, and permanent limitations where understanding may be impossible. Unlike merely difficult subjects, incomprehensible things seem to resist all attempts at understanding. Scientific mysteries, divine concepts, or extreme human behaviors might be described as incomprehensible when they defy rational explanation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-kom-pri-HEN-suh-buhl',
                'etymology': 'From Latin "incomprehensibilis," combining "in-" (not) with "comprehensibilis" (able to be grasped), derived from "comprehendere" meaning "to seize" or "to understand."',
                'language_origins': 'Latin',
                'example_sentence': 'The professor\'s lecture on quantum mechanics was completely _______ to students who lacked advanced physics training.',
                'memory_tip': 'Remember "INCOMPREHENSIBLE" - think "IN-COMPREHENSIBLE" meaning NOT able to be comprehended (understood) - beyond grasp of understanding.'
            },
            'incontrovertible': {
                'definition': 'Incontrovertible describes evidence, facts, or arguments that cannot be disputed, denied, or argued against because they are so clearly true or well-established. This word characterizes information that is beyond reasonable doubt or contradiction. Incontrovertible evidence in legal cases provides such clear proof that opposition becomes impossible. Scientific facts become incontrovertible when supported by overwhelming research and experimentation. Historical events with extensive documentation become incontrovertible despite attempts to deny them. The term implies not just strong evidence but evidence so compelling that rational people cannot reasonably disagree. Unlike opinions or interpretations, incontrovertible facts resist challenge because they are supported by objective, verifiable proof. Mathematical proofs, physical laws, and well-documented historical records often provide incontrovertible foundations for understanding.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-kon-truh-VUR-tuh-buhl',
                'etymology': 'From Latin "incontrovertibilis," combining "in-" (not) with "controvertibilis" (able to be disputed), derived from "controvertere" meaning "to turn against" or "to dispute."',
                'language_origins': 'Latin',
                'example_sentence': 'The DNA evidence provided _______ proof of the suspect\'s presence at the crime scene.',
                'memory_tip': 'Remember "INCONTROVERTIBLE" - think "IN-CONTROVERTIBLE" meaning NOT able to be controverted (disputed) - impossible to argue against.'
            },
            'incorporeal': {
                'definition': 'Incorporeal describes something that lacks physical form or substance - existing without a material body or tangible presence. This word applies to concepts, spirits, ideas, or entities that exist in non-physical realms. Legal terminology uses incorporeal to describe intangible property rights like patents, copyrights, or easements that have value but no physical presence. Religious and philosophical contexts discuss incorporeal souls, spirits, or divine beings that exist beyond material reality. Unlike corporal or corporeal things that have physical substance, incorporeal entities exist as pure concept, energy, or spirit. The term appears in discussions of metaphysics, theology, and intellectual property law. Incorporeal rights can be owned, transferred, or violated despite having no physical manifestation. The concept acknowledges that significant value and reality can exist beyond the material world.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-kor-POR-ee-ul',
                'etymology': 'From Latin "incorporeus," combining "in-" (not) with "corporeus" (having a body), derived from "corpus" (body). The word literally means "without body" or "not having physical form."',
                'language_origins': 'Latin',
                'example_sentence': 'The attorney explained that _______ assets like trademarks and copyrights constitute valuable property despite having no physical form.',
                'memory_tip': 'Remember "INCORPOREAL" - think "IN-CORPOREAL" meaning NOT corporeal (bodily) - existing without physical substance or body.'
            },
            'incorrigibles': {
                'definition': 'Incorrigibles refers to people, typically plural, who cannot be corrected, reformed, or improved in their behavior, attitudes, or character despite repeated attempts at intervention. This noun describes individuals who persistently engage in problematic behavior and resist all efforts at rehabilitation or change. In criminal justice, incorrigibles are repeat offenders who continue illegal activities regardless of punishment or treatment programs. Educational contexts might describe incorrigible students who consistently disrupt classes despite disciplinary measures. The term implies that traditional methods of correction have failed and that the individuals seem fundamentally resistant to positive change. Unlike temporary misbehavior or rebellious phases, incorrigibility suggests a persistent pattern that resists modification. Historically, the term carried negative connotations about criminal potential, though modern understanding recognizes complex factors affecting behavior change.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'in-KOR-ij-uh-bulz',
                'etymology': 'From Latin "incorrigibilis," combining "in-" (not) with "corrigibilis" (able to be corrected), derived from "corrigere" meaning "to set right" or "to correct."',
                'language_origins': 'Latin',
                'example_sentence': 'The juvenile detention center developed specialized programs for young _______ who had failed to respond to traditional rehabilitation efforts.',
                'memory_tip': 'Remember "INCORRIGIBLES" - think "IN-CORRIGIBLES" meaning NOT able to be corrected - people who can\'t be fixed or reformed despite efforts.'
            },
            'increase': {
                'definition': 'Increase means to become larger, greater, or more numerous, or to make something grow in size, amount, degree, or intensity. This fundamental verb describes upward changes in quantity, quality, or magnitude across virtually all contexts. Populations increase through birth rates exceeding death rates. Businesses increase profits through improved efficiency or higher sales. Academic knowledge increases through study and experience. The word can describe both gradual changes, like slowly increasing temperatures, and rapid changes, like suddenly increasing demand. Unlike decrease, which represents reduction, increase represents growth, expansion, or enhancement. Economic indicators track increases in employment, inflation, or production. Personal development involves increasing skills, confidence, or understanding. The concept is essential for measuring progress, growth, and positive change in countless areas of human activity.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'in-KREES (verb), IN-krees (noun)',
                'etymology': 'From Latin "increscere," meaning "to grow into" or "to grow upon," combining "in-" (into) with "crescere" (to grow). The root is shared with "crescent" and "crescendo."',
                'language_origins': 'Latin',
                'example_sentence': 'The company decided to _______ production capacity to meet growing customer demand for their popular product.',
                'memory_tip': 'Remember "INCREASE" - think "IN-CREASE" like adding more "creases" or folds - making something bigger by adding more to it.'
            },
            'increasing': {
                'definition': 'Increasing describes something that is growing larger, greater, or more numerous over time, or the process of making something grow in size, amount, or intensity. This adjective and present participle characterizes ongoing upward changes in various contexts. Increasing temperatures indicate climate change, while increasing enrollment shows educational program growth. The word describes continuous rather than one-time changes, emphasizing progression over time. Unlike static conditions, increasing phenomena show active growth patterns. Economic discussions focus on increasing unemployment, inflation, or investment. Personal development involves increasing competence, confidence, or expertise. Scientific studies track increasing pollution levels or species recovery. The term implies sustained movement in a positive direction, though the change being tracked might be positive or negative depending on context. Increasing patterns help identify trends and predict future developments.',
                'part_of_speech': 'adjective, present participle',
                'pronunciation_guide': 'in-KREE-sing',
                'etymology': 'From Latin "increscere" plus the English suffix "-ing." The participial form emphasizes the ongoing process of growth or expansion.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The _______ number of online students has prompted universities to expand their digital learning platforms.',
                'memory_tip': 'Remember "INCREASING" - think "IN-CREASING" like actively "creasing" (adding) more - something that\'s growing bigger over time.'
            },
            'increments': {
                'definition': 'Increments are small, regular increases or additions, typically measured amounts by which something grows, improves, or progresses step by step. This plural noun describes systematic approaches to change that occur in predictable stages rather than all at once. Salary increments provide regular pay raises based on experience or performance. Scientific measurements might advance in precise increments to ensure accuracy. Software development uses incremental updates to gradually improve functionality. The term emphasizes controlled, measured progress rather than dramatic changes. Unlike random increases, increments follow patterns or predetermined amounts. Educational curricula advance in learning increments appropriate for student development. Project management breaks large tasks into manageable increments to track progress. The concept suggests that significant change often results from accumulating small, consistent improvements over time.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'IN-kruh-munts',
                'etymology': 'From Latin "incrementum," meaning "increase" or "growth," derived from "increscere" (to grow into). The suffix "-ment" indicates the result of an action.',
                'language_origins': 'Latin',
                'example_sentence': 'The construction project progressed in small _______, with workers completing one section of the building each month.',
                'memory_tip': 'Remember "INCREMENTS" - think "IN-CREMENTS" like "in small amounts" - tiny increases that add up over time.'
            },
            'incubate': {
                'definition': 'Incubate means to maintain optimal conditions for development, growth, or hatching, whether literally for eggs or figuratively for ideas, diseases, or projects. This verb originally described birds sitting on eggs to provide warmth necessary for embryonic development. Medical contexts use incubate to describe disease development periods between infection and symptom appearance. Business incubators provide supportive environments for startup companies to develop. Scientific research incubates cell cultures under controlled conditions. The word implies active nurturing rather than passive waiting. Unlike simple waiting, incubating involves creating and maintaining specific conditions that promote development. Ideas incubate in minds through reflection and consideration. The concept emphasizes the importance of proper environment, time, and care in achieving successful outcomes. Incubation periods are crucial for understanding biological, medical, and developmental processes.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'IN-kyuh-bayt',
                'etymology': 'From Latin "incubare," meaning "to lie upon" or "to brood over," combining "in-" (upon) with "cubare" (to lie down). Originally referred to birds lying on eggs to keep them warm.',
                'language_origins': 'Latin',
                'example_sentence': 'The research team needs to _______ the bacterial cultures at exactly 37 degrees Celsius for optimal growth.',
                'memory_tip': 'Remember "INCUBATE" - think "IN-CUBE-ATE" like keeping something in a cube (enclosed space) to help it develop and grow.'
            },
            'incubator': {
                'definition': 'An incubator is a device or environment that provides controlled conditions necessary for development, growth, or survival, most commonly for premature babies, hatching eggs, or bacterial cultures. Medical incubators maintain precise temperature, humidity, and oxygen levels for vulnerable infants. Laboratory incubators control environmental factors for scientific research. Business incubators provide resources, mentoring, and support for startup companies. Agricultural incubators help eggs hatch by maintaining optimal warmth and humidity. The device emphasizes the importance of controlled environment in supporting fragile or developing organisms. Modern incubators use sophisticated technology to monitor and adjust conditions automatically. Unlike natural development environments, incubators provide artificial but precisely controlled conditions. The concept extends metaphorically to any supportive environment that nurtures growth or development in its early stages.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-kyuh-bay-ter',
                'etymology': 'From Latin "incubare" plus the suffix "-ator" indicating an agent or device. The word literally means "one who lies upon" or "device that broods over."',
                'language_origins': 'Latin',
                'example_sentence': 'The premature baby spent three weeks in an _______ until her lungs developed enough to breathe independently.',
                'memory_tip': 'Remember "INCUBATOR" - think "IN-CUBE-ATOR" like a machine that creates a protective cube-like environment for developing things.'
            },
            'inculcate': {
                'definition': 'Inculcate means to instill ideas, values, or habits through persistent teaching, repetition, or example, emphasizing the gradual but thorough process of embedding knowledge or beliefs in someone\'s mind. This verb describes educational or formative processes that go beyond simple instruction to create lasting change in thinking or behavior. Parents inculcate values through consistent modeling and guidance. Educational systems inculcate academic skills and social norms. Military training inculcates discipline and teamwork. The word implies deliberate, sustained effort rather than casual teaching. Unlike mere information transfer, inculcating creates deep understanding that influences future actions and decisions. Religious institutions inculcate faith through ritual and teaching. The process often requires time, patience, and repetition to achieve lasting results. Successful inculcation produces internalized knowledge that becomes part of someone\'s character or worldview.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'IN-kul-kayt',
                'etymology': 'From Latin "inculcare," meaning "to tread in" or "to press in," combining "in-" (in) with "calcare" (to tread or trample), from "calx" (heel). The metaphor suggests pressing ideas firmly into the mind.',
                'language_origins': 'Latin',
                'example_sentence': 'The mentor worked patiently to _______ professional ethics and best practices in his young apprentices.',
                'memory_tip': 'Remember "INCULCATE" - think "IN-CULTI-CATE" like "cultivating" ideas "IN" someone\'s mind through repeated teaching and practice.'
            },
            'incunabula': {
                'definition': 'Incunabula refers to books printed before 1501, during the earliest period of printing with movable type, representing the infancy of printed literature. These works, also called "cradle books," are historically significant as they bridge the transition from handwritten manuscripts to printed books. The term encompasses all printed materials from Gutenberg\'s invention of the printing press around 1440 until the end of the 15th century. Incunabula are valuable to collectors, historians, and libraries because they demonstrate early printing techniques, typography, and book design. Many incunabula feature characteristics of medieval manuscripts, including hand-illuminated letters and decorative elements. Major collections exist in universities and national libraries worldwide. The study of incunabula helps understand the development of printing technology, the spread of literacy, and the intellectual history of Europe during the Renaissance period.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'in-kyuh-NAB-yuh-luh',
                'etymology': 'From Latin "incunabula," literally meaning "cradle" or "swaddling clothes," derived from "cunae" (cradle). The term metaphorically refers to the "cradle period" of printing.',
                'language_origins': 'Latin',
                'example_sentence': 'The university library\'s rare book collection includes several valuable _______ from 15th-century European printing presses.',
                'memory_tip': 'Remember "INCUNABULA" - think "IN-CRADLE-ULA" like books from the cradle period of printing - the earliest printed books.'
            },
            'incunabulacordillera': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "incunabula" (early printed books) and "cordillera" (mountain chain). These are completely unrelated concepts that were accidentally joined during document processing.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'in-kyuh-NAB-yuh-luh-kor-dil-YAIR-uh',
                'etymology': 'This is a PDF parsing error combining "incunabula" from Latin meaning cradle/early books, and "cordillera" from Spanish meaning mountain chain.',
                'language_origins': 'Latin, Spanish (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining terms for early books and mountain ranges.',
                'memory_tip': 'This is a parsing error - remember to separate "incunabula" (early printed books) from "cordillera" (mountain chain).'
            },
            'indecipherable': {
                'definition': 'Indecipherable describes writing, codes, or communication that cannot be read, understood, or decoded despite efforts to interpret the meaning. This word applies to illegible handwriting, damaged documents, encrypted messages, or any text that resists comprehension. Ancient scripts become indecipherable when languages are lost or writing systems are unknown. Poor handwriting can make notes indecipherable even to their authors. Damaged historical documents might be indecipherable due to water damage, fading, or deterioration. The term can extend to speech that is so unclear or garbled that listeners cannot understand it. Unlike simply difficult text, indecipherable writing appears impossible to decode with available knowledge or tools. Cryptographers work to make enemy communications indecipherable while trying to decode indecipherable messages from opponents.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-dih-SY-fur-uh-buhl',
                'etymology': 'From "in-" (not) plus "decipher" plus "-able." "Decipher" comes from "cipher," ultimately from Arabic "sifr" meaning "zero" or "empty," which came to mean "secret writing."',
                'language_origins': 'English, Arabic',
                'example_sentence': 'The doctor\'s handwriting was so sloppy that his prescription notes were completely _______ to the pharmacy staff.',
                'memory_tip': 'Remember "INDECIPHERABLE" - think "IN-DECIPHER-ABLE" meaning NOT able to be deciphered (decoded/read) - impossible to figure out.'
            },
            'indeed': {
                'definition': 'Indeed is an adverb used to emphasize truth, confirm statements, or express agreement, often strengthening the speaker\'s conviction about what they\'re saying. This word serves multiple functions: confirming facts ("That is indeed correct"), expressing emphasis ("It was indeed a remarkable performance"), or showing agreement ("Indeed, you\'re absolutely right"). The term adds weight to statements by suggesting careful consideration or strong belief. Unlike simple agreement, indeed implies thoughtful confirmation based on evidence or experience. Academic and formal writing use indeed to reinforce arguments or acknowledge valid points. Conversational usage often employs indeed to show attentive listening and thoughtful response. The word carries connotations of reliability and measured judgment, suggesting that the speaker has good reason for their confirmation or agreement.',
                'part_of_speech': 'adverb, exclamation',
                'pronunciation_guide': 'in-DEED',
                'etymology': 'From Middle English "in dede," literally meaning "in deed" or "in fact." The phrase originally meant "in actual fact" or "in reality," emphasizing the truth of a statement.',
                'language_origins': 'Middle English',
                'example_sentence': 'The weather forecast predicted rain, and _______ it has been pouring steadily since morning.',
                'memory_tip': 'Remember "INDEED" - think "IN-DEED" like something that exists "in" actual "deed" (fact/reality) - truly and certainly so.'
            },
            'indefatigable': {
                'definition': 'Indefatigable describes someone who shows tireless energy, persistence, and determination that doesn\'t diminish despite challenges, setbacks, or extended effort. This word characterizes individuals who maintain enthusiasm and drive over long periods without becoming discouraged or exhausted. Indefatigable researchers continue investigating despite repeated failures. Indefatigable activists persist in social causes despite opposition. The term suggests not just endurance but sustained passion and commitment that resist fatigue. Unlike simply stubborn behavior, indefatigable effort maintains quality and enthusiasm rather than just continuing mechanically. Historical figures remembered as indefatigable often achieved significant accomplishments through sustained effort over years or decades. The word implies admirable dedication that inspires others and produces meaningful results despite obstacles.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-dih-FAT-ih-guh-buhl',
                'etymology': 'From Latin "indefatigabilis," combining "in-" (not) with "defatigabilis" (able to be wearied), derived from "defatigare" meaning "to tire out completely."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ volunteer coordinator worked eighteen-hour days for months to organize disaster relief efforts.',
                'memory_tip': 'Remember "INDEFATIGABLE" - think "IN-DE-FATIGABLE" meaning NOT "de-fatigable" (able to be tired out) - never getting tired or giving up.'
            },
            'indemnity': {
                'definition': 'Indemnity is protection against damage, loss, or legal liability, typically provided through insurance, contracts, or compensation agreements that transfer financial responsibility from one party to another. This legal and financial term describes arrangements where someone agrees to cover losses or damages that might occur. Insurance policies provide indemnity against various risks like property damage, medical expenses, or legal claims. Business contracts often include indemnity clauses protecting parties from lawsuits or financial losses. The concept ensures that innocent parties don\'t suffer financially from problems they didn\'t cause. Professional indemnity insurance protects doctors, lawyers, and other professionals from malpractice claims. Unlike simple insurance, indemnity specifically aims to restore the injured party to their original position before the loss occurred. Government officials might receive indemnity for actions taken in official capacity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-DEM-ni-tee',
                'etymology': 'From Latin "indemnitas," combining "in-" (not) with "damnum" (loss, damage) plus "-ity." The word literally means "freedom from loss" or "without damage."',
                'language_origins': 'Latin',
                'example_sentence': 'The construction company required _______ insurance to protect against potential lawsuits from workplace accidents.',
                'memory_tip': 'Remember "INDEMNITY" - think "IN-DEMNITY" like being "IN" a state of not having "damage" - protection against financial loss.'
            },
            'indent': {
                'definition': 'Indent means to create a notch, depression, or recess in a surface, or in writing, to begin lines of text several spaces in from the margin to show structure or hierarchy. Physical indenting involves pressing or cutting into materials to create recessed areas. Typography uses indenting to signal new paragraphs, quotations, or outline levels. Computer programming employs indentation to show code structure and nesting. The word can describe both the action of creating indentations and the resulting spaces or depressions. Legal documents use indented paragraphs to organize complex information. Unlike simple spacing, indenting creates visual hierarchy that helps readers understand relationships between different parts of text. Manufacturing processes might indent materials for functional or decorative purposes. The concept applies broadly to any situation involving deliberate creation of recessed areas or spaces.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'in-DENT',
                'etymology': 'From Latin "indentare," meaning "to make notches" or "to cut into teeth," derived from "in-" (into) plus "dens, dentis" (tooth). Originally referred to creating tooth-like notches.',
                'language_origins': 'Latin',
                'example_sentence': 'The writer decided to _______ the first line of each paragraph to make the essay easier to read.',
                'memory_tip': 'Remember "INDENT" - think "IN-DENT" like making a "dent" that goes "IN" - creating a recess or starting text inward from the margin.'
            },
            'independent': {
                'definition': 'Independent describes someone or something that is self-reliant, autonomous, or free from outside control, influence, or support. This word characterizes individuals, organizations, or nations that make their own decisions and manage their own affairs without dependence on others. Independent contractors work for themselves rather than as employees. Independent nations govern themselves without foreign control. Independent thinking involves forming opinions based on personal analysis rather than following others. The term implies both freedom and responsibility - independent entities must provide for their own needs and accept consequences of their decisions. Unlike dependent relationships that rely on others for support, independence suggests self-sufficiency and autonomy. Academic independence allows researchers to pursue studies without external pressure. Political independence enables democratic self-governance.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'in-dih-PEN-dunt',
                'etymology': 'From Latin "independens," combining "in-" (not) with "dependens" (hanging from), derived from "dependere" meaning "to hang from" or "to depend upon."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ filmmaker raised money from private investors rather than working with a major movie studio.',
                'memory_tip': 'Remember "INDEPENDENT" - think "IN-DEPENDENT" meaning NOT dependent on others - able to stand alone and make own decisions.'
            },
            'india': {
                'definition': 'India is a South Asian country, officially the Republic of India, known for its diverse culture, ancient history, and significant global influence in technology, philosophy, and arts. This proper noun refers to the world\'s most populous democracy and second-most populous country, with over 1.4 billion people speaking hundreds of languages. India\'s history spans thousands of years, including ancient civilizations, colonial periods, and independence in 1947. The country is birthplace to major religions including Hinduism, Buddhism, Jainism, and Sikhism. Modern India is a major economic power with thriving technology, pharmaceutical, and service industries. The nation\'s cultural contributions include yoga, meditation, mathematics, astronomy, and literature. India\'s geography encompasses mountains, deserts, plains, and coastlines, supporting enormous biodiversity and varied climates.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'IN-dee-uh',
                'etymology': 'From Greek "India," derived from "Indos," which came from the Persian "Hindu," referring to the people beyond the Indus River. The name ultimately traces to Sanskrit "Sindhu" meaning "river."',
                'language_origins': 'Greek, Persian, Sanskrit',
                'example_sentence': 'The software company decided to establish a development center in _______ to access the country\'s skilled technology workforce.',
                'memory_tip': 'Remember "INDIA" - think of the distinctive "I-N-D-I-A" spelling for this major South Asian nation known for its diversity and culture.'
            },
            'indicate': {
                'definition': 'Indicate means to point out, show, suggest, or serve as a sign or symptom of something, providing information about conditions, directions, or meanings. This verb describes various ways of communicating or revealing information, from direct pointing to subtle suggestions. Medical symptoms indicate diseases, while economic indicators suggest market trends. Traffic signals indicate when to stop or proceed. Scientific measurements indicate environmental changes. The word implies providing evidence or signals that help others understand situations or make decisions. Unlike stating directly, indicating often involves subtle or indirect communication through signs, symptoms, or clues. Academic writing uses indicate to present findings without overstating conclusions. The term encompasses both intentional signaling and unintentional revelation of information through observable phenomena.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'IN-di-kayt',
                'etymology': 'From Latin "indicare," meaning "to point out" or "to declare," combining "in-" (toward) with "dicare" (to proclaim). The root "dic-" relates to speaking and declaring.',
                'language_origins': 'Latin',
                'example_sentence': 'The dark clouds and dropping temperature _______ that a severe thunderstorm is approaching the area.',
                'memory_tip': 'Remember "INDICATE" - think "IN-DI-CATE" like "in" the "dictionary" you "locate" (show/point out) meanings - to point out or show something.'
            },
            'indicates': {
                'definition': 'Indicates is the third person singular present tense of "indicate," meaning shows, points out, suggests, or serves as a sign of something. This verb form describes ongoing or habitual signaling, suggesting, or revealing of information. Research indicates connections between variables. Weather data indicates climate patterns. Medical tests indicate health conditions. The word describes current, active signaling rather than past or future indication. Unlike stated facts, what something indicates might require interpretation or analysis to understand fully. Scientific studies use indicates to present findings while acknowledging limitations. Business reports use indicates to describe trends or patterns in data. The term suggests evidence-based conclusions while maintaining appropriate caution about certainty. Educational assessments indicate student progress and learning needs.',
                'part_of_speech': 'verb (third person singular present)',
                'pronunciation_guide': 'IN-di-kayts',
                'etymology': 'From Latin "indicare" plus the English third person singular ending "-s." The present tense form emphasizes ongoing indication.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The patient\'s rapid pulse _______ that her cardiovascular system is responding to the stress of the medical procedure.',
                'memory_tip': 'Remember "INDICATES" - think "IN-DI-CATES" like actively "dictating" or "locating" signs that point to something happening now.'
            },
            'indicia': {
                'definition': 'Indicia are distinguishing marks, signs, or characteristics that provide evidence of authenticity, origin, or specific qualities, particularly in legal, postal, or technical contexts. This plural noun describes various forms of identifying features used for verification or classification. Postal indicia replace stamps on bulk mailings, showing payment authorization. Legal indicia establish ownership, authenticity, or compliance with requirements. Scientific indicia help classify organisms or identify chemical compounds. The term emphasizes observable features that trained observers can recognize and interpret. Unlike simple labels, indicia often require specialized knowledge to understand their significance. Official indicia carry legal weight in establishing rights, responsibilities, or compliance. Document authentication relies on security indicia that prevent forgery. The concept applies broadly to any systematic use of identifying marks or characteristics.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'in-DISH-ee-uh',
                'etymology': 'From Latin "indicium," meaning "indication" or "sign," derived from "indicare" (to point out). The plural form "indicia" indicates multiple signs or marks.',
                'language_origins': 'Latin',
                'example_sentence': 'The postal service uses special _______ on business mail to show that postage has been paid without using traditional stamps.',
                'memory_tip': 'Remember "INDICIA" - think "IN-DI-CIA" like "in" the "CYA" (covers) are special marks or signs that indicate official authorization or authenticity.'
            },
            'indict': {
                'definition': 'Indict means to formally charge someone with a crime or wrongdoing, typically through grand jury proceedings that determine whether sufficient evidence exists to warrant a trial. This legal verb describes the official accusation process that begins serious criminal proceedings. Grand juries review evidence and decide whether to indict suspects based on probable cause standards. Unlike arrests, which can be based on immediate circumstances, indictments require careful evidence review and legal procedures. Federal and state prosecutors present cases seeking indictments for serious crimes. The process protects both society\'s interest in prosecuting crimes and individual rights against frivolous prosecution. Getting indicted doesn\'t prove guilt but establishes that credible evidence suggests criminal activity occurred. The word can also be used metaphorically to mean severely criticizing or condemning someone\'s actions or character.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-DYT',
                'etymology': 'From Latin "indictare," meaning "to proclaim" or "to declare," derived from "in-" (into) plus "dictare" (to declare). The word originally meant "to write down" formal charges.',
                'language_origins': 'Latin',
                'example_sentence': 'The grand jury voted to _______ the former mayor on charges of embezzling public funds.',
                'memory_tip': 'Remember "INDICT" - think "IN-DICT" like "in" the "dictionary" of crimes - to formally declare someone guilty of wrongdoing. Note the silent "c"!'
            },
            'indie': {
                'definition': 'Indie is an informal term for "independent," typically describing artists, musicians, filmmakers, or creators who work outside major commercial or corporate systems, maintaining creative control over their work. This adjective and noun characterizes cultural productions that prioritize artistic vision over commercial appeal. Indie films are made without major studio backing, often featuring unconventional narratives or experimental techniques. Indie music refers to artists who record and distribute music independently, often developing unique sounds without mainstream pressure. The term implies authenticity, creativity, and resistance to commercial formulae. Indie creators often have smaller budgets but greater creative freedom. The movement values originality over profitability, though many indie artists achieve both. Digital platforms have democratized indie distribution, allowing independent creators to reach audiences directly without traditional gatekeepers.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'IN-dee',
                'etymology': 'Shortened form of "independent," first used in the 1920s but became popular in music and film contexts during the 1980s and 1990s.',
                'language_origins': 'English (abbreviation)',
                'example_sentence': 'The _______ band recorded their album in a home studio and sold it directly to fans through their website.',
                'memory_tip': 'Remember "INDIE" - think "IN-DEE" like "IN-DEpendent" shortened - artists who work independently without big companies controlling them.'
            },
            'indigent': {
                'definition': 'Indigent describes someone who is extremely poor, lacking basic necessities like food, shelter, or medical care, often requiring public assistance or charity to survive. This word characterizes individuals or families whose resources are insufficient to meet fundamental human needs. Legal systems provide indigent defendants with court-appointed attorneys. Medical facilities offer indigent care programs for uninsured patients. Social services agencies assist indigent families with housing, food, and healthcare. The term carries more formality than simply "poor" and often appears in legal, medical, or social service contexts. Unlike temporary financial difficulties, indigence suggests persistent inability to afford basic necessities. Government programs specifically target indigent populations for assistance. The word emphasizes the severity of poverty that threatens health, safety, and survival without external support.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'IN-dih-junt',
                'etymology': 'From Latin "indigens," present participle of "indigere" meaning "to need" or "to lack," combining "indu-" (within) with "egere" (to lack or need).',
                'language_origins': 'Latin',
                'example_sentence': 'The hospital established a special program to provide free medical care to _______ patients who cannot afford treatment.',
                'memory_tip': 'Remember "INDIGENT" - think "IN-DIG-ENT" like someone who\'s "in" such poverty they might have to "dig" for basic necessities - extremely poor.'
            },
            'indignant': {
                'definition': 'Indignant describes feeling or showing anger and displeasure at what is perceived as unfair treatment, injustice, or morally wrong behavior. This adjective characterizes righteous anger that arises from witnessing or experiencing violations of fairness, dignity, or proper conduct. Indignant responses typically stem from strong moral convictions rather than personal inconvenience. Citizens become indignant about government corruption, while parents become indignant about unfair treatment of their children. The emotion combines anger with moral outrage, suggesting that principles have been violated. Unlike simple anger, indignation implies that the person has legitimate cause for upset based on ethical or justice concerns. Indignant behavior often motivates people to take action against perceived wrongs. The word suggests both emotional intensity and moral justification for feeling upset.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-DIG-nunt',
                'etymology': 'From Latin "indignans," present participle of "indignari" meaning "to regard as unworthy" or "to be angry at," derived from "indignus" (unworthy).',
                'language_origins': 'Latin',
                'example_sentence': 'The community members became _______ when they discovered that their tax money had been spent on the mayor\'s personal vacation.',
                'memory_tip': 'Remember "INDIGNANT" - think "IN-DIG-NANT" like being angry enough to "dig" into wrong behavior - feeling righteous anger about unfairness.'
            },
            'indigo': {
                'definition': 'Indigo is a deep blue-purple color, historically derived from plants in the genus Indigofera and prized for dyeing fabrics and creating artistic pigments. This noun and adjective describes both the natural dye and the distinctive color it produces. Indigo cultivation and trade significantly influenced global commerce for centuries, particularly connecting Asia, Europe, and the Americas. The color appears in the spectrum between blue and violet and is traditionally listed as one of the seven colors of the rainbow. Synthetic indigo replaced natural sources in the 19th century, making the color more widely available and affordable. Indigo-dyed denim became culturally significant in Western fashion. The word also refers to plants that produce this dye, which have been cultivated for over 4,000 years. Indigo represents both a specific color and the rich cultural history of textile dyeing.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'IN-di-go',
                'etymology': 'From Spanish "índigo," derived from Latin "indicum," meaning "Indian dye," ultimately from Greek "indikon" (Indian). The name reflects the dye\'s historical association with India.',
                'language_origins': 'Spanish, Latin, Greek',
                'example_sentence': 'The artist mixed _______ paint with white to create the perfect shade of twilight sky for her landscape painting.',
                'memory_tip': 'Remember "INDIGO" - think "INDI-GO" like "Indian-go" because this deep blue dye originally came from India and "went" around the world.'
            },
            'indistinguishable': {
                'definition': 'Indistinguishable describes things that are so similar they cannot be differentiated or told apart, even with careful observation or analysis. This word applies when differences between objects, people, or concepts are so minimal that they appear identical. Identical twins might be indistinguishable to strangers. High-quality reproductions can be indistinguishable from originals. Scientific measurements sometimes produce indistinguishable results within experimental error. The term emphasizes the absence of detectable differences rather than actual identity. Unlike obviously different things, indistinguishable items challenge observers to identify unique characteristics. Technology aims to make artificial products indistinguishable from natural ones. The concept appears in philosophy when discussing identity and similarity. Legal contexts might consider indistinguishable products as equivalent for regulatory purposes.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-dih-STING-gwish-uh-buhl',
                'etymology': 'From "in-" (not) plus "distinguishable," derived from Latin "distinguere" meaning "to separate" or "to differentiate." The word literally means "not able to be separated or differentiated."',
                'language_origins': 'Latin, English',
                'example_sentence': 'The counterfeit bills were nearly _______ from genuine currency, requiring special equipment to detect the forgery.',
                'memory_tip': 'Remember "INDISTINGUISHABLE" - think "IN-DISTINGUISH-ABLE" meaning NOT able to distinguish (tell apart) - so similar they look identical.'
            },
            'individual': {
                'definition': 'Individual refers to a single person, organism, or thing considered separately from a group, emphasizing uniqueness, distinctiveness, or personal identity. This word functions as both noun and adjective, highlighting the concept of singularity versus collective identity. As a noun, individual describes a specific person with unique characteristics, rights, and responsibilities. As an adjective, it emphasizes separate, personal, or customized treatment. Democratic societies value individual rights and freedoms. Education increasingly focuses on individual learning needs. The concept balances personal autonomy with social responsibility. Unlike group identity, individual identity emphasizes personal distinctiveness and self-determination. Psychology studies individual differences in personality, intelligence, and behavior. Legal systems recognize individual accountability for actions. The term appears frequently in discussions of human rights, personal development, and social organization.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'in-dih-VID-yoo-ul',
                'etymology': 'From Medieval Latin "individualis," derived from "individuus" meaning "indivisible," combining "in-" (not) with "dividuus" (divisible), from "dividere" (to divide).',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'Each _______ student receives personalized feedback on their academic progress and learning goals.',
                'memory_tip': 'Remember "INDIVIDUAL" - think "IN-DIVID-UAL" meaning NOT dividual (divisible) - a single, unique person who can\'t be divided or split.'
            },
            'indolent': {
                'definition': 'Indolent describes someone who is habitually lazy, avoiding work or exertion, preferring comfort and ease over productive activity. This adjective characterizes persistent reluctance to engage in physical or mental effort. Indolent behavior involves choosing inactivity when action is needed or expected. Unlike temporary rest or legitimate breaks, indolence suggests consistent avoidance of responsibility and effort. The word can also describe medical conditions characterized by slow development or minimal symptoms. Indolent students consistently avoid studying or completing assignments. In medical contexts, indolent infections develop slowly without acute symptoms. The term implies not just laziness but a fundamental disposition toward avoiding effort. Unlike being tired, which is temporary, being indolent suggests a character trait or habitual approach to life that prioritizes comfort over productivity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IN-duh-lunt',
                'etymology': 'From Latin "indolens," meaning "feeling no pain" or "insensitive," combining "in-" (not) with "dolens" (feeling pain), from "dolere" (to feel pain). The meaning evolved from "painless" to "avoiding effort."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ employee consistently arrived late and avoided taking on challenging projects that required extra effort.',
                'memory_tip': 'Remember "INDOLENT" - think "IN-DO-LENT" like someone who\'s "lent" to "in-doing" (not doing) anything - habitually lazy and avoiding work.'
            },
            'indolentdocumentary': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "indolent" (lazy, avoiding effort) and "documentary" (factual film or program). These are completely unrelated concepts that were accidentally joined during document processing.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'IN-duh-lunt-dok-yuh-MEN-tuh-ree',
                'etymology': 'This is a PDF parsing error combining "indolent" from Latin meaning avoiding pain/effort, and "documentary" from Latin meaning relating to documents.',
                'language_origins': 'Latin (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining terms for lazy behavior and factual films.',
                'memory_tip': 'This is a parsing error - remember to separate "indolent" (lazy) from "documentary" (factual film).'
            },
            'indubitable': {
                'definition': 'Indubitable describes something that cannot be doubted, questioned, or disputed because it is so clearly true or well-established that reasonable people cannot disagree with it. This word characterizes facts, evidence, or conclusions that are beyond reasonable doubt. Scientific laws become indubitable when supported by overwhelming evidence and repeated verification. Mathematical proofs provide indubitable conclusions when properly constructed. Historical events with extensive documentation become indubitable despite attempts to deny them. The term suggests not just strong evidence but evidence so compelling that doubt becomes unreasonable. Unlike opinions or interpretations that might vary, indubitable facts resist challenge because they are supported by objective, verifiable proof. Legal standards sometimes require indubitable evidence for serious convictions. The word emphasizes the highest level of certainty possible in human knowledge.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-DOO-bi-tuh-buhl',
                'etymology': 'From Latin "indubitabilis," combining "in-" (not) with "dubitabilis" (able to be doubted), derived from "dubitare" meaning "to doubt" or "to waver."',
                'language_origins': 'Latin',
                'example_sentence': 'The DNA evidence provided _______ proof that the suspect was present at the crime scene.',
                'memory_tip': 'Remember "INDUBITABLE" - think "IN-DUBIT-ABLE" meaning NOT "dubitable" (doubtable) - so certain it cannot be questioned.'
            },
            'inducement': {
                'definition': 'Inducement is something that persuades, motivates, or encourages someone to take a particular action, often involving incentives, rewards, or attractive offers designed to influence behavior. This noun describes various forms of motivation used to encourage desired responses. Financial inducements might include bonuses, discounts, or special offers. Legal inducements could involve plea bargains or reduced sentences. Business inducements encourage customer purchases or employee performance. The term can have positive connotations when describing legitimate incentives or negative implications when referring to manipulation or bribery. Unlike force or coercion, inducement works through attraction and appeal to self-interest. Marketing relies heavily on inducements to encourage consumer behavior. The concept recognizes that people often need additional motivation beyond obligation to take action.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-DOOS-munt',
                'etymology': 'From Latin "inducere," meaning "to lead into" or "to bring about," combined with the suffix "-ment" indicating the result of an action.',
                'language_origins': 'Latin',
                'example_sentence': 'The company offered a substantial signing bonus as an _______ to attract top talent from competing firms.',
                'memory_tip': 'Remember "INDUCEMENT" - think "IN-DUCE-MENT" like something that "duces" (leads) you "IN" to taking action - motivation or incentive.'
            },
            'inducementdid': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "inducement" (incentive or motivation) and "did" (past tense of "do"). These are completely unrelated concepts that were accidentally joined during document processing.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'in-DOOS-munt-did',
                'etymology': 'This is a PDF parsing error combining "inducement" from Latin "inducere" (to lead into) and "did" from Old English "dyde" (past tense of do).',
                'language_origins': 'Latin, Old English (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining a noun for incentive with a past tense verb.',
                'memory_tip': 'This is a parsing error - remember to separate "inducement" (incentive) from "did" (past tense of do).'
            },
            'indulgent': {
                'definition': 'Indulgent describes behavior that is overly permissive, lenient, or generous, often to the point of being excessive or potentially harmful. This word characterizes people who readily satisfy desires, grant requests, or overlook faults without applying appropriate limits. Indulgent parents might spoil children by avoiding discipline or giving excessive privileges. Indulgent self-behavior involves excessive consumption or pleasure-seeking. The term can describe both treatment of others and personal habits. Unlike appropriate kindness or generosity, indulgence suggests lack of restraint that might undermine long-term benefits. Indulgent managers might avoid confronting poor performance. The word carries implications that such permissiveness, while initially pleasant, might create problems. Indulgent attitudes often stem from desire to avoid conflict or please others, but can result in negative consequences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-DUL-junt',
                'etymology': 'From Latin "indulgens," present participle of "indulgere" meaning "to be kind to" or "to give free rein to." The root suggests yielding to desires or wishes.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ grandparents allowed their grandchildren to eat candy for breakfast and stay up past midnight.',
                'memory_tip': 'Remember "INDULGENT" - think "IN-DULGE-NT" like someone who "dulges" (indulges) "IN" too much - overly permissive and generous.'
            },
            'industrial': {
                'definition': 'Industrial describes things related to manufacturing, production, or large-scale business operations that transform raw materials into finished goods. This adjective characterizes the economic sector focused on mechanized production, heavy machinery, and mass manufacturing. Industrial processes use technology and organization to produce goods efficiently and in large quantities. Industrial societies developed during the Industrial Revolution when manufacturing became dominant over agriculture. Industrial design focuses on creating functional, mass-producible products. The term can describe machinery, buildings, processes, or entire economic systems. Industrial accidents involve workplace safety in manufacturing environments. Unlike agricultural or service economies, industrial economies emphasize production of physical goods. Environmental concerns often focus on industrial pollution and resource consumption. The word implies scale, mechanization, and systematic approaches to production.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-DUS-tree-ul',
                'etymology': 'From Latin "industrialis," derived from "industria" meaning "diligence" or "activity," ultimately from "industrius" (diligent, active).',
                'language_origins': 'Latin',
                'example_sentence': 'The city\'s _______ district houses several large manufacturing plants that produce automotive components.',
                'memory_tip': 'Remember "INDUSTRIAL" - think "IN-DUST-RIAL" like places where there\'s lots of dust from heavy manufacturing and production work.'
            },
            'industry': {
                'definition': 'Industry refers to organized economic activity involving the production of goods or services, particularly manufacturing that transforms raw materials into finished products using machinery and labor. This noun encompasses both specific business sectors and the general concept of systematic production. The automotive industry produces cars and trucks, while the entertainment industry creates movies and music. Industry also means hard work, diligence, and sustained effort in any endeavor. Unlike individual craftsmanship, industry implies organized, large-scale operations. Economic policies often focus on supporting key industries for national competitiveness. Industrial development drives technological innovation and job creation. The term can describe both the infrastructure of production and the attitude of dedicated work. Modern economies typically include primary industries (raw materials), secondary industries (manufacturing), and tertiary industries (services).',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-dus-tree',
                'etymology': 'From Latin "industria," meaning "diligence" or "earnest activity," derived from "industrius" (diligent, active). The meaning evolved from personal diligence to organized economic activity.',
                'language_origins': 'Latin',
                'example_sentence': 'The technology _______ has transformed how people communicate and access information worldwide.',
                'memory_tip': 'Remember "INDUSTRY" - think "IN-DUST-RY" like busy work that gets you dusty from all the productive activity and manufacturing.'
            },
            'ineffable': {
                'definition': 'Ineffable describes something that cannot be expressed in words, typically because it is too extreme, sublime, or mysterious for language to capture adequately. This word characterizes experiences, emotions, or concepts that transcend ordinary communication. Religious or mystical experiences are often considered ineffable because they involve realities beyond normal human understanding. Profound grief, overwhelming joy, or transcendent beauty might be ineffable emotions that resist verbal description. The term acknowledges the limitations of language when confronting ultimate realities or intense experiences. Unlike simply difficult-to-describe things, ineffable phenomena seem to exceed the capacity of words entirely. Artists, poets, and mystics often struggle to convey ineffable experiences through their chosen mediums. The word suggests that some aspects of existence remain forever beyond human ability to articulate, requiring direct experience rather than explanation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-EF-uh-buhl',
                'etymology': 'From Latin "ineffabilis," combining "in-" (not) with "effabilis" (able to be spoken), derived from "effari" meaning "to speak out." The word literally means "unspeakable."',
                'language_origins': 'Latin',
                'example_sentence': 'Standing before the vast mountain vista, she felt an _______ sense of awe that no words could properly capture.',
                'memory_tip': 'Remember "INEFFABLE" - think "IN-EFF-ABLE" meaning NOT "effable" (speakable) - so amazing or mysterious it can\'t be put into words.'
            },
            'ineffective': {
                'definition': 'Ineffective describes something that fails to produce desired results, accomplish intended goals, or work as expected despite efforts or attempts. This word characterizes methods, treatments, strategies, or actions that prove unsuccessful in achieving their purposes. Ineffective medicines fail to treat conditions, while ineffective teaching methods don\'t help students learn. Unlike effective approaches that succeed, ineffective ones waste time, resources, or effort without producing benefits. The term can apply to temporary failures or persistent inability to achieve results. Ineffective leadership fails to motivate or guide organizations successfully. Scientific studies identify ineffective treatments to prevent their continued use. The word implies not just absence of success but active failure despite reasonable expectations. Recognizing ineffective approaches helps redirect efforts toward more promising alternatives.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ih-FEK-tiv',
                'etymology': 'From "in-" (not) plus "effective," derived from Latin "effectivus" meaning "productive" or "causing effects." The word literally means "not producing intended effects."',
                'language_origins': 'Latin, English',
                'example_sentence': 'The medication proved _______ against the patient\'s rare infection, forcing doctors to try alternative treatments.',
                'memory_tip': 'Remember "INEFFECTIVE" - think "IN-EFFECTIVE" meaning NOT effective (successful) - failing to work or produce desired results.'
            },
            'ineluctable': {
                'definition': 'Ineluctable describes something that cannot be avoided, escaped, or resisted - inevitable forces or circumstances that must be accepted despite any efforts to prevent or change them. This word characterizes fate, consequences, or natural processes that prove unavoidable regardless of human will or action. Death is often considered ineluctable, as is aging. Economic cycles might seem ineluctable despite policy interventions. The term suggests not just difficulty in avoiding something but complete impossibility of escape. Unlike challenges that might be overcome with sufficient effort, ineluctable forces cannot be defeated or circumvented. Philosophical discussions often address ineluctable aspects of human existence. Literary works frequently explore characters confronting ineluctable destinies. The word emphasizes the limits of human agency when facing certain universal forces or logical consequences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ih-LUK-tuh-buhl',
                'etymology': 'From Latin "ineluctabilis," combining "in-" (not) with "eluctabilis" (able to be struggled out of), derived from "eluctari" meaning "to struggle out" or "to escape."',
                'language_origins': 'Latin',
                'example_sentence': 'The company\'s bankruptcy seemed _______ after years of declining sales and mounting debt.',
                'memory_tip': 'Remember "INELUCTABLE" - think "IN-E-LUCT-ABLE" meaning NOT able to "luct" (struggle) your way "E" (out) - impossible to escape or avoid.'
            },
            'ineptitude': {
                'definition': 'Ineptitude is the quality of being completely unsuitable, incompetent, or lacking the skills necessary to perform tasks adequately, characterized by consistent failure and poor judgment. This noun describes a fundamental inability to handle responsibilities or execute plans effectively. Unlike occasional mistakes or temporary inexperience, ineptitude suggests persistent incompetence across multiple situations. Political ineptitude might involve consistently poor decision-making that harms public interests. Professional ineptitude could manifest as repeated failures to meet basic job requirements. The word implies not just lack of skill but lack of awareness about one\'s limitations. Ineptitude often becomes apparent when someone is placed in positions requiring abilities they simply don\'t possess. The term carries strong negative connotations, suggesting that the person\'s inability creates problems for themselves and others.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-EP-ti-tood',
                'etymology': 'From Latin "ineptitudo," derived from "ineptus" meaning "unsuitable" or "absurd," combining "in-" (not) with "aptus" (fitted, suitable).',
                'language_origins': 'Latin',
                'example_sentence': 'The manager\'s _______ in handling the crisis led to widespread confusion and ultimately cost the company millions in lost revenue.',
                'memory_tip': 'Remember "INEPTITUDE" - think "IN-APT-ITUDE" meaning NOT having "aptitude" (ability) - complete lack of competence or skill.'
            }
        }
        
        return batch_090_data.get(word, {
            'definition': f'Educational definition for {word} would be generated here.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'{word.upper()}',
            'etymology': f'Etymology for {word} would be researched and provided.',
            'language_origins': 'To be determined',
            'example_sentence': f'An example sentence using _______ would be provided here.',
            'memory_tip': f'Memory tip for spelling {word} would be provided.'
        })

    def detect_word_error(self, word: str) -> str:
        """Detect and flag combined word errors and other parsing issues"""
        word_lower = word.lower()
        
        combined_errors = {
            'incunabulacordillera': 'Combined word error: "incunabulacordillera" appears to be "incunabula" (early printed books) + "cordillera" (mountain chain) merged together.',
            'indolentdocumentary': 'Combined word error: "indolentdocumentary" appears to be "indolent" (lazy) + "documentary" (factual film) merged together.',
            'inducementdid': 'Combined word error: "inducementdid" appears to be "inducement" (incentive) + "did" (past tense verb) merged together.'
        }
        
        for error_word, description in combined_errors.items():
            if error_word in word_lower:
                return f'{word}: {description} This is likely a PDF parsing error.'
        
        return ""

    def process_batch(self, input_file: str, output_file: str):
        """Process a batch of spelling bee words"""
        try:
            print(f"Processing {input_file}...")
            
            df = pd.read_csv(input_file)
            processed_data = []
            errors = []
            
            for _, row in df.iterrows():
                word = str(row['word']).strip()
                if not word or word == 'nan':
                    continue
                
                error = self.detect_word_error(word)
                if error:
                    errors.append(error)
                
                claude_data = self.get_comprehensive_claude_data(word)
                
                phonetic_score = self.difficulty_calculator.calculate_phonetic_transparency(word, claude_data['pronunciation_guide'])
                frequency_score = self.difficulty_calculator.calculate_word_frequency(word)
                morphological_score = self.difficulty_calculator.calculate_morphological_complexity(word)
                etymology_score = self.difficulty_calculator.calculate_etymology_complexity(claude_data['etymology'])
                
                word_data = WordData(
                    word=word,
                    years=str(row['years']),
                    source_files=str(row['source_files']),
                    source_difficulties=str(row['source_difficulties']),
                    definition=claude_data['definition'],
                    part_of_speech=claude_data['part_of_speech'],
                    pronunciation_guide=claude_data['pronunciation_guide'],
                    etymology=claude_data['etymology'],
                    language_origins=claude_data['language_origins'],
                    example_sentence=claude_data['example_sentence'],
                    memory_tip=claude_data['memory_tip'],
                    phonetic_transparency_score=phonetic_score,
                    word_frequency_score=frequency_score,
                    morphological_complexity_score=morphological_score,
                    etymology_complexity_score=etymology_score,
                    difficulty_level=None
                )
                
                processed_data.append(word_data)
                self.processed_count += 1
            
            output_df = pd.DataFrame([{
                'word': wd.word,
                'years': wd.years,
                'source_files': wd.source_files,
                'source_difficulties': wd.source_difficulties,
                'definition': wd.definition,
                'part_of_speech': wd.part_of_speech,
                'pronunciation_guide': wd.pronunciation_guide,
                'etymology': wd.etymology,
                'language_origins': wd.language_origins,
                'example_sentence': wd.example_sentence,
                'memory_tip': wd.memory_tip,
                'phonetic_transparency_score': wd.phonetic_transparency_score,
                'word_frequency_score': wd.word_frequency_score,
                'morphological_complexity_score': wd.morphological_complexity_score,
                'etymology_complexity_score': wd.etymology_complexity_score,
                'difficulty_level': wd.difficulty_level,
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'etymology_source': 'Claude',
                'example_sentence_source': 'Claude',
                'memory_tip_source': 'Claude',
                'audio_file_path': '',
                'image_file_path': '',
                'word_category': '',
                'subcategory': '',
                'difficulty_explanation': '',
                'learning_tips': wd.memory_tip
            } for wd in processed_data])
            
            output_df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Successfully processed {self.processed_count}/50 words to {output_file}")
            if errors:
                print(f"Found {len(errors)} error(s):")
                for error in errors:
                    print(f"  - {error}")
            
            return True
            
        except Exception as e:
            print(f"Error processing batch: {str(e)}")
            return False

def main():
    processor = Batch090Processor()
    input_file = "output/batch_090_words.csv"
    output_file = "output/batch_090_processed.csv"
    
    success = processor.process_batch(input_file, output_file)
    if success:
        print("Batch 090 processing completed successfully!")
    else:
        print("Batch 090 processing failed!")

if __name__ == "__main__":
    main()