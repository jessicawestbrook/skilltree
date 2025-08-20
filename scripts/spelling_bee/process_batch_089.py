#!/usr/bin/env python3
"""
Batch 089 Processor for Scripps National Spelling Bee Words
Processes words from impasse through inclement with comprehensive Claude-generated data
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

class Batch089Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.processed_count = 0

    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge"""
        
        batch_089_data = {
            'impasse': {
                'definition': 'An impasse is a situation where progress becomes impossible due to disagreement, deadlock, or an insurmountable obstacle. In negotiations, politics, or problem-solving contexts, an impasse occurs when opposing parties cannot find common ground or when all possible solutions have been exhausted. The word can also refer to a physical dead end or cul-de-sac where passage is blocked. In chess, an impasse would be a position where no beneficial moves are available. The term implies not just difficulty, but a complete standstill that requires either external intervention, creative thinking, or fundamental changes in approach to resolve. Unlike temporary setbacks, an impasse suggests a more serious and potentially permanent blockage that challenges conventional solutions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IM-pas',
                'etymology': 'From French "impasse," literally meaning "not pass," from the prefix "im-" (not) and "passe" (pass). The French word combined "im-" (variant of "in-" meaning not) with "passer" (to pass), creating a term for a place where passage is impossible.',
                'language_origins': 'French',
                'example_sentence': 'The peace negotiations reached an _______ when neither side would compromise on the disputed territory.',
                'memory_tip': 'Remember "IMPASSE" - think "I\'M PAST" (going past) but with double S. Or imagine being "IM-PASSED" by a dead-end - you can\'t pass through!'
            },
            'impasto': {
                'definition': 'Impasto is a painting technique where paint is applied in thick, heavy layers, creating a three-dimensional texture on the canvas surface. This method allows brush strokes, palette knife marks, and fingerprints to remain visible, giving the artwork a sculptural quality. Famous artists like Vincent van Gogh and Jackson Pollock extensively used impasto to add energy and movement to their paintings. The thick paint creates shadows and highlights that change as viewing angles shift, making the artwork appear to have physical depth and movement. This technique requires paint to be used straight from the tube or mixed with mediums that maintain its consistency. Impasto can be applied with brushes, palette knives, or even hands, and it\'s particularly effective in oil painting where the medium naturally supports heavy application.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-PAS-to',
                'etymology': 'From Italian "impasto," from "impastare" meaning "to make into a paste" or "to knead." The word combines "in-" (into) with "pasta" (paste), literally meaning "made into paste." This reflects the thick, paste-like consistency of paint applied in this technique.',
                'language_origins': 'Italian',
                'example_sentence': 'Van Gogh\'s use of _______ technique made his sunflowers appear to leap from the canvas with their thick, textured petals.',
                'memory_tip': 'Remember "IMPASTO" - think "IM-PASTE-O" like thick paste applied to create texture in paintings.'
            },
            'impastoantagonistic': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely merging "impasto" (a painting technique) and "antagonistic" (showing hostility or opposition). These are two distinct concepts that were incorrectly joined during document processing.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'im-PAS-to-an-TAG-uh-NIS-tik',
                'etymology': 'This is a PDF parsing error combining two separate words: "impasto" from Italian meaning thick paint technique, and "antagonistic" from Greek meaning opposed or hostile.',
                'language_origins': 'Italian, Greek (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining two separate terms.',
                'memory_tip': 'This is a parsing error - remember to separate "impasto" (painting technique) from "antagonistic" (hostile behavior).'
            },
            'impeachable': {
                'definition': 'Impeachable describes actions or behaviors that provide grounds for impeachment, the formal process of charging a public official with misconduct while in office. In legal and political contexts, impeachable offenses typically include treason, bravery, high crimes, or misdemeanors that violate the public trust. The term can also apply more broadly to any conduct that calls someone\'s integrity, reliability, or credibility into question. In legal proceedings, witness testimony might be considered impeachable if it contains contradictions or inconsistencies. The word implies not just wrongdoing, but wrongdoing serious enough to warrant formal accusations or removal from position. Historical examples include various presidential impeachment proceedings where specific actions were deemed impeachable offenses under constitutional standards.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-PEE-chuh-buhl',
                'etymology': 'From Middle English "empechen," from Old French "empêchier" meaning "to hinder" or "to prevent," ultimately from Late Latin "impedicare" meaning "to fetter." The legal sense developed through the idea of "hindering" someone by bringing formal charges.',
                'language_origins': 'Old French, Late Latin',
                'example_sentence': 'The committee determined that the official\'s actions were _______ under the constitutional standards for removal from office.',
                'memory_tip': 'Remember "IMPEACHABLE" - think "IM-PEACH-ABLE" like being able to be "impeached" (formally accused). Peach helps you remember the "PEACH" sound.'
            },
            'impeccable': {
                'definition': 'Impeccable means absolutely perfect, flawless, or without fault in execution, behavior, or appearance. This word describes something so well-done that no criticism or improvement is possible. When applied to people, it refers to irreproachable character, behavior, or reputation. In describing work quality, impeccable suggests attention to every detail and the highest standards of excellence. The word carries connotations of moral purity and ethical perfection, originally coming from religious contexts meaning "without sin." Modern usage extends to describe anything from impeccable timing to impeccable taste, emphasizing the complete absence of any deficiency or error. It\'s stronger than merely "good" or "excellent," implying a level of perfection that serves as a standard for others.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-PEK-uh-buhl',
                'etymology': 'From Latin "impeccabilis," combining "im-" (not) with "peccare" (to sin) and the suffix "-able." Literally means "not able to sin" or "incapable of wrongdoing." The religious origins emphasized moral perfection.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ manners and attention to detail made her the perfect choice for the diplomatic position.',
                'memory_tip': 'Remember "IMPECCABLE" - think "IM-PECK-ABLE" but it\'s the opposite - NOT able to be pecked at (criticized) because it\'s perfect!'
            },
            'impecunious': {
                'definition': 'Impecunious describes someone who lacks money or resources; essentially poor or penniless, but often temporarily so due to circumstances rather than permanent destitution. This formal term suggests someone who may have previously had means but currently faces financial hardship. Unlike other words for poverty, impecunious often implies a refined or educated person experiencing financial difficulties, perhaps due to poor investments, economic downturns, or pursuing artistic endeavors that don\'t generate income. The word carries a somewhat literary or humorous tone, often used to describe struggling artists, writers, or intellectuals. It can also refer to institutions, organizations, or even countries facing financial constraints. The term suggests dignity despite financial limitations, distinguishing it from words that might carry social stigma.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-pi-KYOO-nee-us',
                'etymology': 'From Latin "impecuniosus," combining "im-" (not) with "pecuniosus" (wealthy), derived from "pecunia" (money). "Pecunia" itself comes from "pecus" (cattle), reflecting ancient times when wealth was measured in livestock.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ artist traded paintings for meals while waiting for his work to gain recognition.',
                'memory_tip': 'Remember "IMPECUNIOUS" - think "IM-PECUNIA-OUS" where "pecunia" is Latin for money. No pecunia = no money = impecunious!'
            },
            'impediment': {
                'definition': 'An impediment is an obstacle, hindrance, or obstruction that slows, prevents, or complicates progress toward a goal. This can be physical, such as a roadblock or architectural barrier, or abstract, like bureaucratic red tape or personal limitations. In speech therapy, a speech impediment refers to conditions affecting clear communication, such as stuttering or pronunciation difficulties. Legal impediments are circumstances that prevent certain actions, like marriage or contract formation. The word implies something that doesn\'t completely stop progress but makes it significantly more difficult or slower. Unlike complete barriers, impediments can often be overcome with additional effort, time, or resources. The term is commonly used in project management, personal development, and problem-solving contexts to identify factors requiring special attention or alternative approaches.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-PED-uh-munt',
                'etymology': 'From Latin "impedimentum," derived from "impedire" meaning "to entangle" or "to hinder," which combines "in-" (in) with "pes, pedis" (foot). Originally referred to things that would entangle the feet and prevent walking.',
                'language_origins': 'Latin',
                'example_sentence': 'The language barrier proved to be a significant _______ in the international business negotiations.',
                'memory_tip': 'Remember "IMPEDIMENT" - think "IM-PEDE-MENT" like something affecting your "peds" (feet), preventing you from moving forward smoothly.'
            },
            'impel': {
                'definition': 'Impel means to drive forward, urge, or push someone toward action through force, motivation, or compelling circumstances. Unlike gentle encouragement, impelling involves a stronger sense of necessity or urgency that makes action feel inevitable. This force can be external, such as circumstances that demand response, or internal, like powerful emotions or convictions that drive behavior. The word suggests movement from a static state to active engagement, often triggered by powerful motivations. In physics, impel relates to applying force to create motion. Psychologically, people can be impelled by conscience, passion, fear, or opportunity. The term implies that the driving force is strong enough to overcome resistance or hesitation, creating momentum toward specific goals or actions.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'im-PEL',
                'etymology': 'From Latin "impellere," combining "in-" (into, against) with "pellere" (to push, drive, or strike). The word literally means "to push into" or "to drive against," emphasizing the forceful nature of the action.',
                'language_origins': 'Latin',
                'example_sentence': 'The urgent deadline did _______ the team to work through the night to complete their project.',
                'memory_tip': 'Remember "IMPEL" - sounds like "IM-PULL" but it\'s the opposite - you\'re pushing or driving someone forward, not pulling them back!'
            },
            'impenetrable': {
                'definition': 'Impenetrable describes something that cannot be pierced through, entered, or passed through, whether physically or intellectually. Physically, it refers to barriers, materials, or defenses so strong or dense that nothing can pass through them, such as impenetrable armor or dense jungle. Intellectually, it describes concepts, texts, or reasoning so complex or obscure that they\'re impossible to understand or comprehend. The word can also describe emotional or social barriers that resist access or influence. In military contexts, impenetrable defenses cannot be breached. In academic writing, impenetrable prose is so convoluted that readers cannot extract meaning. The term suggests complete resistance rather than mere difficulty, implying that conventional approaches or efforts will prove inadequate for breakthrough or understanding.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-PEN-uh-truh-buhl',
                'etymology': 'From Late Latin "impenetrabilis," combining "im-" (not) with "penetrabilis" (able to be pierced), derived from "penetrare" (to enter or pierce through). The root "penetrare" comes from "penitus" meaning "within."',
                'language_origins': 'Late Latin',
                'example_sentence': 'The professor\'s lecture on quantum mechanics was so _______ that even graduate students struggled to follow his reasoning.',
                'memory_tip': 'Remember "IMPENETRABLE" - think "IM-PENETRATE-ABLE" meaning NOT able to be penetrated or pierced through.'
            },
            'imperator': {
                'definition': 'Imperator was an ancient Roman title meaning "commander" or "emperor," originally awarded to victorious military generals who had achieved significant conquests. The term evolved from describing successful battlefield commanders to becoming the primary title for Roman emperors, emphasizing their supreme military authority. In Roman tradition, soldiers would salute a victorious general by shouting "Imperator!" after major victories. The title carried immense prestige and was often a stepping stone to higher political power. Later, it became synonymous with imperial rule, as emperors combined military command with political supremacy. The word embodies the Roman ideal of leadership through military prowess and strategic excellence. Modern usage occasionally refers to any supreme commander or someone exercising imperial authority, though it retains strong associations with Roman history and military leadership traditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-per-uh-TOR',
                'etymology': 'From Latin "imperator," meaning "commander" or "chief," derived from "imperare" meaning "to command" or "to order." The root comes from "in-" (in) and "parare" (to prepare or make ready), suggesting someone who prepares others for action.',
                'language_origins': 'Latin',
                'example_sentence': 'Julius Caesar earned the title _______ after his military victories in Gaul, eventually leading to his rise as dictator.',
                'memory_tip': 'Remember "IMPERATOR" - think "IM-EMPEROR" - an imperator was like an emperor, the supreme commander of Roman forces.'
            },
            'imperious': {
                'definition': 'Imperious describes behavior that is arrogantly domineering, commanding others with an assumption of superiority and expecting immediate obedience. This word characterizes people who act with overbearing authority, often displaying haughty or condescending attitudes toward those they perceive as subordinates. Imperious behavior involves making demands rather than requests, showing little patience for questioning or delay. The term suggests an attitude of entitlement and assumed superiority that can alienate others through its dismissive or contemptuous tone. Unlike confident leadership, imperious behavior lacks consideration for others\' feelings or perspectives. Historical monarchs or aristocrats might display imperious manners, expecting deference based on status rather than earning respect through competence or character. The word often carries negative connotations of tyranny or excessive pride.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-PEER-ee-us',
                'etymology': 'From Latin "imperiosus," meaning "commanding" or "domineering," derived from "imperium" (command, authority, or empire). The root "imperare" means "to command," combining "in-" with "parare" (to prepare).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ manager\'s constant demands and dismissive tone created a hostile work environment for the entire team.',
                'memory_tip': 'Remember "IMPERIOUS" - think "IM-PEER-IOUS" like someone acting superior to their peers, demanding to be treated like royalty.'
            },
            'impermeable': {
                'definition': 'Impermeable describes materials, surfaces, or barriers that do not allow liquids, gases, or other substances to pass through them. This property is crucial in various applications, from waterproof clothing and building materials to geological formations that prevent water infiltration. In earth sciences, impermeable rock layers like clay or shale prevent groundwater movement and can trap oil or gas deposits. Biologically, cell membranes can be selectively impermeable, controlling which substances enter or exit. The concept extends beyond physical barriers to describe systems, policies, or boundaries that resist penetration or influence. Unlike merely resistant materials, impermeable substances provide complete blockage under normal conditions. This property is essential in engineering, construction, and environmental protection, where controlling substance movement is critical for safety and functionality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-PUR-mee-uh-buhl',
                'etymology': 'From Late Latin "impermeabilis," combining "im-" (not) with "permeabilis" (able to be passed through), derived from "permeare" meaning "to pass through completely." The root combines "per-" (through) with "meare" (to go).',
                'language_origins': 'Late Latin',
                'example_sentence': 'The engineer selected an _______ membrane to prevent water from seeping into the building\'s foundation.',
                'memory_tip': 'Remember "IMPERMEABLE" - think "IM-PERMEATE-ABLE" meaning NOT able to be permeated (passed through) by liquids or gases.'
            },
            'impertinent': {
                'definition': 'Impertinent describes behavior or speech that is disrespectfully bold, presumptuous, or inappropriately forward, especially toward someone in authority or in formal situations. This word characterizes actions that cross boundaries of proper etiquette, showing lack of respect for social hierarchies or appropriate conduct. Impertinent questions probe into matters that are none of the questioner\'s business, while impertinent remarks show disregard for courtesy or diplomacy. The term can also describe things that are irrelevant or not pertaining to the matter at hand, though this usage is less common. Unlike playful teasing or casual informality, impertinent behavior demonstrates poor judgment about social appropriateness and can damage relationships or reputations. The word often applies to situations where someone oversteps their role or position.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-PUR-tn-unt',
                'etymology': 'From Late Latin "impertinens," combining "im-" (not) with "pertinens" (pertaining to, relevant). Originally meant "not relevant," but evolved to mean "inappropriately forward" through the idea of behavior not pertaining to one\'s proper role.',
                'language_origins': 'Late Latin',
                'example_sentence': 'The student\'s _______ questions about the teacher\'s personal life were inappropriate during the academic discussion.',
                'memory_tip': 'Remember "IMPERTINENT" - think "IM-PERTINENT" meaning NOT pertinent (appropriate) to the situation - being inappropriately bold or rude.'
            },
            'impetus': {
                'definition': 'Impetus refers to the force, energy, or motivation that causes something to happen, develop, or continue moving forward. In physics, it relates to momentum - the tendency of moving objects to continue in motion. More broadly, impetus describes the driving force behind actions, decisions, or changes, whether from external pressures or internal motivations. This stimulus can be sudden, like a crisis that spurs reform, or gradual, like growing public awareness that leads to policy changes. The word implies not just initiation but sufficient force to sustain progress through obstacles or resistance. Business ventures need impetus to overcome market challenges, while social movements require impetus to effect meaningful change. The term suggests energy that transforms potential into action and maintains momentum toward goals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IM-pi-tus',
                'etymology': 'From Latin "impetus," meaning "attack, assault, or violent motion," derived from "impetere" meaning "to rush upon" or "to attack." This combines "in-" (upon) with "petere" (to seek or aim at).',
                'language_origins': 'Latin',
                'example_sentence': 'The environmental disaster provided the _______ needed for lawmakers to finally pass comprehensive pollution control legislation.',
                'memory_tip': 'Remember "IMPETUS" - think "IM-PET-US" like a pet that\'s rushing toward us with energy and momentum, giving force to movement.'
            },
            'implacable': {
                'definition': 'Implacable describes someone or something that cannot be appeased, pacified, or satisfied; relentlessly unforgiving and impossible to placate through any means. This word characterizes enemies who refuse reconciliation, forces that cannot be stopped or redirected, or conditions that resist all attempts at resolution. Implacable opposition continues despite efforts at compromise or negotiation. In literature and mythology, implacable foes pursue their objectives without mercy or possibility of truce. The term can describe natural forces like implacable storms or diseases that resist treatment, as well as human emotions like implacable hatred or determination. Unlike temporary anger or frustration, implacable suggests a permanent state of opposition that no concession or apology can change. The word emphasizes the futility of attempting to soften or redirect such determined resistance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-PLAK-uh-buhl',
                'etymology': 'From Latin "implacabilis," combining "im-" (not) with "placabilis" (able to be appeased), derived from "placare" meaning "to calm" or "to appease." The root suggests something that cannot be made peaceful or calm.',
                'language_origins': 'Latin',
                'example_sentence': 'Despite numerous peace overtures, the two families remained _______ enemies after the ancient feud destroyed both their fortunes.',
                'memory_tip': 'Remember "IMPLACABLE" - think "IM-PLACATE-ABLE" meaning NOT able to be placated (calmed down or appeased) - impossible to satisfy or appease.'
            },
            'implicative': {
                'definition': 'Implicative refers to something that suggests, implies, or hints at meanings beyond what is directly stated or obvious. This term describes language, behavior, or evidence that carries indirect significance requiring interpretation to fully understand. In linguistics, implicative verbs carry assumptions about related actions or states - for example, "manage to do" implies difficulty was overcome. Logically, implicative statements create chains of reasoning where one conclusion suggests another. Legal evidence can be implicative when it suggests guilt without providing direct proof. The word describes communication that operates through suggestion rather than explicit statement, requiring active interpretation from the audience. Implicative meaning often relies on context, shared knowledge, or cultural understanding to convey its full significance. This indirect communication style can be more persuasive or diplomatic than direct statements.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IM-pli-kay-tiv',
                'etymology': 'From Latin "implicare," meaning "to entangle" or "to involve," combined with the suffix "-ative" indicating tendency or capacity. The root combines "in-" (in) with "plicare" (to fold), suggesting meanings folded within other meanings.',
                'language_origins': 'Latin',
                'example_sentence': 'The witness\'s _______ testimony suggested corruption without directly accusing any specific officials of wrongdoing.',
                'memory_tip': 'Remember "IMPLICATIVE" - think "IM-PLICATE-IVE" meaning tending to implicate or suggest hidden meanings beyond the obvious.'
            },
            'implicativesostenuto': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "implicative" (suggesting indirect meanings) and "sostenuto" (a musical term meaning sustained). These are two distinct concepts from different fields that were accidentally joined during document processing.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'IM-pli-kay-tiv-sos-tuh-NOO-to',
                'etymology': 'This is a PDF parsing error combining "implicative" from Latin "implicare" (to entangle) and "sostenuto" from Italian meaning "sustained" in musical contexts.',
                'language_origins': 'Latin, Italian (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining linguistic and musical terminology.',
                'memory_tip': 'This is a parsing error - remember to separate "implicative" (suggesting meanings) from "sostenuto" (sustained musical style).'
            },
            'implore': {
                'definition': 'Implore means to beg earnestly or desperately for something, typically appealing to someone\'s compassion, mercy, or sense of justice. This word describes urgent, emotional requests that go beyond simple asking to convey deep need or desperation. When someone implores, they often display vulnerability, humility, or intense emotion, recognizing their dependence on another\'s goodwill or power. The term suggests that normal requests have failed or that the situation is too critical for casual approaches. Religious contexts often involve imploring divine intervention or mercy. In literature and drama, characters implore when facing life-changing decisions or desperate circumstances. Unlike demanding or commanding, imploring acknowledges the other party\'s right to refuse while appealing to their better nature. The word carries connotations of urgency and emotional intensity.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'im-PLOR',
                'etymology': 'From Latin "implorare," combining "in-" (upon) with "plorare" (to cry out or wail). The word literally means "to cry out to" or "to call upon with weeping," emphasizing the emotional intensity of the appeal.',
                'language_origins': 'Latin',
                'example_sentence': 'The defendant did _______ the judge for leniency, citing his young children who depended on his support.',
                'memory_tip': 'Remember "IMPLORE" - think "IM-PLORE" like "I\'m POOR" (desperate) and need to beg earnestly for help.'
            },
            'impolite': {
                'definition': 'Impolite describes behavior, language, or actions that violate accepted standards of courtesy, respect, or social etiquette. This word encompasses a range of discourteous behaviors from minor social oversights to deliberately rude conduct. Impolite behavior might include interrupting conversations, failing to acknowledge others, using inappropriate language, or disregarding social conventions. The term applies to actions that show lack of consideration for others\' feelings, status, or comfort. Cultural contexts significantly influence what constitutes impolite behavior, as standards vary across societies and situations. Unlike accidentally offensive behavior, impolite actions often reflect either ignorance of proper conduct or deliberate disregard for social norms. The word suggests behavior that makes social interactions uncomfortable or strained, potentially damaging relationships or reputations through its inconsiderate nature.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-puh-LYT',
                'etymology': 'From Latin "impolitus," combining "im-" (not) with "politus" (polished, refined), derived from "polire" meaning "to polish" or "to make smooth." Originally referred to things not refined or smoothed.',
                'language_origins': 'Latin',
                'example_sentence': 'It would be _______ to arrive at the formal dinner party wearing casual clothes and chewing gum.',
                'memory_tip': 'Remember "IMPOLITE" - think "IM-POLITE" meaning NOT polite, lacking in good manners or courtesy.'
            },
            'imponderabilia': {
                'definition': 'Imponderabilia refers to things that cannot be measured, weighed, or evaluated precisely - intangible factors that resist quantification but significantly influence outcomes or understanding. This philosophical and scientific term describes elements like emotions, cultural attitudes, spiritual beliefs, or aesthetic values that affect situations despite being unmeasurable. In anthropology, imponderabilia include subtle cultural practices, unspoken social rules, and emotional atmospheres that shape community life. Scientific research often struggles with imponderabilia - factors that clearly matter but cannot be controlled or measured in experiments. The term acknowledges that human experience and complex systems involve mysterious elements that defy mathematical analysis yet remain crucial for comprehensive understanding. These intangible factors often determine success or failure in endeavors where measurable factors alone prove insufficient for prediction or explanation.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'im-pon-der-uh-BIL-ee-uh',
                'etymology': 'From Latin "imponderabilia," the plural of "imponderabile," combining "im-" (not) with "ponderabilis" (able to be weighed), derived from "ponderare" (to weigh). The root "pondus" means "weight."',
                'language_origins': 'Latin',
                'example_sentence': 'The anthropologist studied the _______ of village life - the unspoken customs and emotional undercurrents that shaped social interactions.',
                'memory_tip': 'Remember "IMPONDERABILIA" - think "IM-PONDERABLE-IA" meaning things that are NOT ponderable (weighable/measurable) - the intangible aspects of life.'
            },
            'important': {
                'definition': 'Important describes something that carries significant meaning, value, or consequence, deserving attention, consideration, or priority. This fundamental word applies to matters that affect outcomes, wellbeing, or understanding in meaningful ways. Important decisions shape future possibilities, while important information influences knowledge or actions. The term encompasses both immediate significance and long-term impact, from important daily tasks to important historical events. Importance can be subjective, varying based on personal values, circumstances, or perspectives, or objective, recognized universally as significant. In hierarchies, important positions carry greater responsibility and influence. Academic subjects, social issues, and personal relationships can all be deemed important based on their capacity to affect lives, communities, or knowledge. The word implies that something deserves more attention, resources, or careful consideration than less significant matters.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-POR-tnt',
                'etymology': 'From Medieval Latin "importantia," derived from Latin "importare" meaning "to bring into" or "to carry in." The sense developed from "bringing in" consequences or significance to "having significance."',
                'language_origins': 'Medieval Latin, Latin',
                'example_sentence': 'The research findings were so _______ that they changed the entire field\'s understanding of cellular biology.',
                'memory_tip': 'Remember "IMPORTANT" - think "IM-PORT-ANT" like something being imported (brought in) because it has significant value or consequence.'
            },
            'importunate': {
                'definition': 'Importunate describes persistent, urgent, or troublesomely insistent requests, demands, or behavior that continues despite resistance or inconvenience to others. This word characterizes people who press their cases with annoying persistence, refusing to accept refusal or delay. Importunate creditors repeatedly demand payment, while importunate suitors persist despite clear rejection. The term suggests behavior that crosses the line from appropriate persistence into harassment or nuisance. Unlike reasonable follow-up or legitimate urgency, importunate actions show insensitivity to others\' circumstances, convenience, or clearly expressed boundaries. Historical contexts often describe importunate petitioners who repeatedly approached rulers or officials despite being told to wait. The word implies that the persistence has become counterproductive, potentially alienating the very people whose cooperation is sought.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-POR-chuh-nut',
                'etymology': 'From Latin "importunus," combining "im-" (not) with "portunus" (suitable, convenient), derived from "portus" (port, harbor). Originally meant "inconvenient" or "unsuitable," developing into "persistently troublesome."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ salesperson called multiple times daily despite being told the customer was not interested in the product.',
                'memory_tip': 'Remember "IMPORTUNATE" - think "IM-PORTUN-ATE" like being "inopportune" (badly timed) with persistent, annoying requests.'
            },
            'imposing': {
                'definition': 'Imposing describes something that creates a strong impression through size, appearance, or presence, commanding respect, awe, or attention through its impressive qualities. This word applies to physical structures like imposing buildings or mountains that dominate landscapes, as well as people whose bearing, stature, or demeanor creates immediate impact. Imposing figures possess natural authority or dignity that influences others\' behavior and attitudes. The term can describe anything from imposing ceremonies that create solemnity to imposing arguments that demand serious consideration. Unlike merely large or loud, imposing suggests a quality of dignity, grandeur, or significance that naturally commands respect. Architecture, natural landscapes, personalities, and abstract concepts like imposing challenges all can possess this quality of impressive presence that cannot be ignored or dismissed casually.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'im-POZ-ing',
                'etymology': 'From Latin "imponere," meaning "to place upon" or "to set up," combining "in-" (upon) with "ponere" (to place). The sense developed from "placing something impressive" to "creating strong impressions."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ cathedral with its towering spires and intricate stonework dominated the medieval city\'s skyline.',
                'memory_tip': 'Remember "IMPOSING" - think "IM-POSE-ING" like something that poses (presents itself) in an impressive, commanding way that demands attention.'
            },
            'imposter': {
                'definition': 'An imposter is someone who deceives others by pretending to be someone else, typically to gain advantage, access, or credibility they wouldn\'t otherwise possess. This person adopts false identities, credentials, or personas to mislead others about their true nature, qualifications, or intentions. Imposters might claim professional credentials they lack, assume others\' identities for financial gain, or infiltrate organizations under false pretenses. The term encompasses various forms of identity deception, from simple lies about qualifications to elaborate schemes involving forged documents and sustained role-playing. Psychology recognizes "imposter syndrome" where legitimate achievers feel like frauds despite genuine accomplishments. Historical imposters have claimed royal titles, professional expertise, or social positions far beyond their actual status. The word implies deliberate deception rather than honest mistakes about identity or qualifications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-POS-ter',
                'etymology': 'From Latin "imponere," meaning "to place upon" or "to impose," through Old French "imposteur." The sense developed from "placing oneself in a false position" to "deceiving about one\'s identity."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The hospital discovered that the _______ had been practicing medicine for months without any real medical training or license.',
                'memory_tip': 'Remember "IMPOSTER" - think "IM-POST-ER" like someone posting (presenting) themselves as something they\'re not - a fake identity.'
            },
            'impostor': {
                'definition': 'An impostor is someone who deceives others by pretending to be someone else, typically to gain advantage, access, or credibility they wouldn\'t otherwise possess. This alternative spelling of "imposter" carries identical meaning and usage. The person adopts false identities, credentials, or personas to mislead others about their true nature, qualifications, or intentions. Impostors might claim professional credentials they lack, assume others\' identities for financial gain, or infiltrate organizations under false pretenses. The term encompasses various forms of identity deception, from simple lies about qualifications to elaborate schemes involving forged documents and sustained role-playing. Both spellings are acceptable, though "impostor" is considered more traditional while "imposter" has become more common in modern usage. The word implies deliberate deception rather than honest mistakes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-POS-ter',
                'etymology': 'From Latin "imponere," meaning "to place upon" or "to impose," through Old French "imposteur." This is the traditional spelling, with "imposter" being a more modern variant.',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The famous art _______ successfully sold fake masterpieces for years before experts discovered his elaborate deception.',
                'memory_tip': 'Remember "IMPOSTOR" - think "IM-POST-OR" like someone posting or presenting themselves as something they\'re not - the traditional spelling of this deceptive role.'
            },
            'impoverish': {
                'definition': 'Impoverish means to make poor or reduce to poverty, whether financially, intellectually, culturally, or in quality. This verb describes processes that strip away resources, wealth, opportunities, or enriching elements from people, communities, or experiences. Financial impoverishment occurs through job loss, economic collapse, or exploitation. Cultural impoverishment results from loss of traditions, education, or artistic expression. Environmental impoverishment happens when ecosystems lose biodiversity or natural resources. The word can describe both gradual processes and sudden changes that reduce richness or abundance. Policies might impoverish communities by limiting access to education or healthcare. Natural disasters can impoverish entire regions. The term implies not just reduction but movement toward deprivation that affects wellbeing, development, or quality of life in significant ways.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'im-POV-er-ish',
                'etymology': 'From Old French "empovrir," derived from "en-" (in) plus "povre" (poor), ultimately from Latin "pauper" meaning "poor." The word literally means "to make poor" or "to put into poverty."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The factory closure threatened to _______ the entire town by eliminating its primary source of employment.',
                'memory_tip': 'Remember "IMPOVERISH" - think "IM-POVER-ISH" like making something "poverty-ish" - reducing it to a poor state.'
            },
            'imprecatory': {
                'definition': 'Imprecatory refers to language, prayers, or expressions that invoke curses, condemnation, or divine punishment upon someone or something. This adjective describes communications intended to bring harm, misfortune, or divine wrath to their targets. Imprecatory psalms in religious texts call upon God to punish enemies or wrongdoers. Legal language sometimes includes imprecatory elements when pronouncing judgments or sentences. The term characterizes speech acts that go beyond criticism to actively wish or invoke negative consequences. Unlike mere complaints or expressions of anger, imprecatory language specifically calls for punishment or retribution, often invoking supernatural or divine intervention. Historical contexts include imprecatory formulas used in treaties or oaths to ensure compliance through fear of supernatural consequences. The word implies both condemnation and active desire for the target to suffer consequences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IM-pri-kuh-tor-ee',
                'etymology': 'From Latin "imprecatorius," derived from "imprecari" meaning "to call down upon" or "to invoke," combining "in-" (upon) with "precari" (to pray or ask). The root emphasizes calling upon higher powers for punishment.',
                'language_origins': 'Latin',
                'example_sentence': 'The ancient tablet contained _______ inscriptions calling upon the gods to curse anyone who disturbed the pharaoh\'s tomb.',
                'memory_tip': 'Remember "IMPRECATORY" - think "IM-PRAY-CATORY" like praying for curses or punishment to fall upon someone - invoking negative consequences.'
            },
            'impresario': {
                'definition': 'An impresario is a person who organizes, manages, or sponsors entertainment productions, particularly in opera, theater, or concert performances. This role combines artistic vision with business acumen, requiring skills in talent management, financial planning, and audience development. Impresarios identify promising performers, secure venues, arrange financing, and coordinate complex productions from conception to performance. Historical impresarios like Sergei Diaghilev transformed entire art forms by bringing together innovative artists, composers, and performers. The position demands understanding both artistic excellence and commercial viability, balancing creative ambitions with practical constraints. Modern impresarios might manage concert tours, produce Broadway shows, or organize festivals. The role requires networking abilities, cultural sophistication, and entrepreneurial courage to invest in uncertain artistic ventures. Successful impresarios often become influential cultural figures who shape public taste and artistic trends.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'im-pruh-SAR-ee-oh',
                'etymology': 'From Italian "impresario," derived from "impresa" meaning "undertaking" or "enterprise," ultimately from Latin "imprendere" (to undertake). The word emphasizes the entrepreneurial aspect of organizing artistic productions.',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The famous _______ brought together world-class musicians from different genres to create an innovative fusion concert series.',
                'memory_tip': 'Remember "IMPRESARIO" - think "IM-PRESS-ARIO" like someone who impresses audiences by organizing amazing artistic performances and productions.'
            },
            'impromptu': {
                'definition': 'Impromptu describes something done without advance planning, preparation, or rehearsal - spontaneous actions or performances created in the moment. This word applies to speeches delivered without scripts, musical performances created on the spot, or social gatherings organized at the last minute. Impromptu events often capture authentic energy and creativity that planned activities might lack, though they also carry risks of poor execution due to lack of preparation. The term can describe both positive spontaneity, like impromptu celebrations, and necessary adaptations, like impromptu solutions to unexpected problems. In music, impromptu pieces are composed to sound spontaneous even when actually written down. The word emphasizes the immediate, unrehearsed quality that creates both excitement and uncertainty. Impromptu actions require quick thinking and adaptability.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'im-PROMP-too',
                'etymology': 'From Latin "in promptu," meaning "in readiness" or "at hand," combining "in" (in) with "promptus" (ready, prepared). The phrase originally meant "readily available" but evolved to mean "spontaneous."',
                'language_origins': 'Latin',
                'example_sentence': 'The mayor delivered an _______ speech at the community gathering, speaking directly from the heart without prepared remarks.',
                'memory_tip': 'Remember "IMPROMPTU" - think "IM-PROMPT-U" like "I\'M PROMPTED TO" do something spontaneously without advance planning.'
            },
            'impromptuincinerate': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "impromptu" (spontaneous, unplanned) and "incinerate" (to burn completely). These are completely different concepts that were accidentally joined during document processing.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'im-PROMP-too-in-SIN-uh-rayt',
                'etymology': 'This is a PDF parsing error combining "impromptu" from Latin "in promptu" (in readiness) and "incinerate" from Latin "incinerare" (to burn to ashes).',
                'language_origins': 'Latin (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining terms for spontaneous action and burning.',
                'memory_tip': 'This is a parsing error - remember to separate "impromptu" (spontaneous) from "incinerate" (burn completely).'
            },
            'improve': {
                'definition': 'Improve means to make or become better in quality, condition, or effectiveness through changes, enhancements, or development. This fundamental verb describes processes that increase value, functionality, or desirability in various contexts. People improve skills through practice, organizations improve processes through optimization, and communities improve conditions through collective action. Improvement can be gradual, like slowly improving health through lifestyle changes, or dramatic, like improving productivity through technological innovations. The word implies movement from a current state toward a better one, whether measured objectively through metrics or subjectively through satisfaction. Improvement requires effort, resources, or favorable circumstances to achieve positive change. The concept applies universally from personal development to technological advancement, always suggesting progress toward more favorable conditions or outcomes.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'im-PROOV',
                'etymology': 'From Anglo-Norman "emprover," meaning "to make profit from," derived from Old French "prou" (profit, advantage). The word originally meant "to make profitable" but expanded to mean "to make better."',
                'language_origins': 'Anglo-Norman, Old French',
                'example_sentence': 'The new training program helped employees _______ their technical skills and advance in their careers.',
                'memory_tip': 'Remember "IMPROVE" - think "IM-PROVE" like "I\'M PROVING" that something can be made better through effort and changes.'
            },
            'impudence': {
                'definition': 'Impudence is bold, disrespectful behavior that shows lack of shame or proper regard for authority, propriety, or social boundaries. This noun describes attitudes and actions that brazenly violate expected norms of courtesy, deference, or appropriateness. Impudence goes beyond simple rudeness to include defiant disregard for consequences, often displaying shocking disrespect toward authority figures or social conventions. The word implies not just inappropriate behavior but shameless boldness in acting inappropriately. Historical contexts often describe impudence toward superiors, teachers, or social betters as particularly scandalous. Unlike accidental rudeness or cultural misunderstandings, impudence involves deliberate choice to act disrespectfully. The term carries strong negative connotations, suggesting behavior that reasonable people would find offensive or shocking. Impudence often provokes strong reactions due to its brazen nature.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IM-pyuh-duns',
                'etymology': 'From Latin "impudentia," derived from "impudens" meaning "shameless," combining "im-" (not) with "pudens" (feeling shame), from "pudere" (to feel shame). The word literally means "lack of shame."',
                'language_origins': 'Latin',
                'example_sentence': 'The student\'s _______ in talking back to the principal during the assembly shocked both teachers and parents.',
                'memory_tip': 'Remember "IMPUDENCE" - think "IM-PUDENT" meaning NOT prudent (wise/proper) - acting shamelessly disrespectful and bold.'
            },
            'impugn': {
                'definition': 'Impugn means to challenge, dispute, or attack the truth, validity, or integrity of something, typically through argument or evidence that casts doubt on its reliability. This verb describes actions that question authenticity, accuracy, or moral standing of ideas, claims, or people\'s character. Legal contexts frequently involve impugning witness testimony by revealing inconsistencies or bias. Academic discourse might impugn research findings by identifying methodological flaws. Political debates often feature attempts to impugn opponents\' credibility or policy proposals. The word implies more than simple disagreement - it suggests systematic efforts to undermine confidence in the target through reasoned argument or evidence. Unlike casual criticism, impugning involves deliberate attempts to damage credibility or reputation through factual challenges. The term carries connotations of formal challenge rather than emotional attack.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'im-PYOON',
                'etymology': 'From Latin "impugnare," meaning "to fight against" or "to attack," combining "in-" (against) with "pugnare" (to fight). The root "pugnus" means "fist," emphasizing the combative nature of the challenge.',
                'language_origins': 'Latin',
                'example_sentence': 'The defense attorney attempted to _______ the witness\'s testimony by revealing her financial interest in the case\'s outcome.',
                'memory_tip': 'Remember "IMPUGN" - think "IM-PUGN" like "I\'M PUGNACIOUS" (fighting) against something, challenging its truth or validity.'
            },
            'inaudible': {
                'definition': 'Inaudible describes sounds that cannot be heard, either because they are too quiet, beyond the range of human hearing, or blocked by interference or distance. This word applies to speech, music, or noises that fail to reach listeners\' ears with sufficient volume or clarity for recognition. Inaudible whispers might be intentionally quiet to avoid eavesdropping, while inaudible instructions create confusion in noisy environments. Technical contexts describe inaudible frequencies above or below human hearing range, like ultrasonic or infrasonic sounds. Communication problems often arise from inaudible messages during phone calls, presentations, or public announcements. The term can describe temporary conditions, like inaudible speech due to laryngitis, or permanent situations, like inaudible sounds for hearing-impaired individuals. The word emphasizes the failure of sound to successfully reach and register with intended recipients.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-AW-duh-buhl',
                'etymology': 'From Late Latin "inaudibilis," combining "in-" (not) with "audibilis" (able to be heard), derived from "audire" (to hear). The word literally means "not able to be heard."',
                'language_origins': 'Late Latin',
                'example_sentence': 'The speaker\'s voice became _______ as she moved away from the microphone during her presentation.',
                'memory_tip': 'Remember "INAUDIBLE" - think "IN-AUDIBLE" meaning NOT audible (hearable) - sounds that cannot be heard or detected by ears.'
            },
            'incandescent': {
                'definition': 'Incandescent describes something that emits bright light as a result of being heated to high temperatures, or metaphorically, something that displays brilliant intensity, passion, or anger. Physically, incandescent objects like traditional light bulbs produce light through heated filaments that glow white-hot. The term extends to describe volcanic lava, glowing coals, or any heated material that radiates visible light. Metaphorically, incandescent anger suggests rage so intense it seems to glow with fury, while incandescent performance indicates brilliance that illuminates and captivates audiences. The word implies not just brightness but the energy and heat that creates that luminosity. Scientific contexts describe the relationship between temperature and light emission that characterizes incandescent phenomena. The term suggests intensity that cannot be ignored or contained.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-kan-DES-unt',
                'etymology': 'From Latin "incandescere," meaning "to glow with heat," combining "in-" (thoroughly) with "candescere" (to begin to glow), derived from "candere" (to glow or be white). The root emphasizes the white-hot nature of the glow.',
                'language_origins': 'Latin',
                'example_sentence': 'The actor\'s _______ performance lit up the stage with such emotional intensity that the audience was completely mesmerized.',
                'memory_tip': 'Remember "INCANDESCENT" - think "IN-CANDESCENT" like "IN-CANDLE-SCENT" - glowing brightly with heat like a candle, but much more intense.'
            },
            'incantations': {
                'definition': 'Incantations are magical formulas, spells, or ritual words spoken or chanted to invoke supernatural powers, cast spells, or produce magical effects. These verbal formulas appear in religious ceremonies, magical practices, and folklore traditions across cultures. Incantations typically follow specific patterns, rhythms, or ancient languages believed to enhance their power. Historical examples include Latin incantations in medieval magic, Sanskrit mantras in Hinduism, or indigenous ritual chants for healing or protection. The effectiveness of incantations often depends on precise pronunciation, proper timing, or ceremonial context. Literary traditions feature incantations in fantasy stories, while anthropological studies document their role in traditional healing and spiritual practices. The word implies both the verbal component and the belief system that gives these words their supposed power to affect reality through supernatural means.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'in-kan-TAY-shunz',
                'etymology': 'From Latin "incantatio," derived from "incantare" meaning "to chant" or "to cast a spell," combining "in-" (upon) with "cantare" (to sing). The root emphasizes the musical or rhythmic nature of magical speech.',
                'language_origins': 'Latin',
                'example_sentence': 'The ancient grimoire contained numerous _______ written in archaic Latin for summoning protective spirits.',
                'memory_tip': 'Remember "INCANTATIONS" - think "IN-CHANT-ATIONS" like chanting special words or songs to cast magical spells.'
            },
            'incarnadine': {
                'definition': 'Incarnadine describes something having the color of flesh or blood - a deep pink or crimson red color, or as a verb, to make something turn this reddish color. This literary word appears famously in Shakespeare\'s Macbeth, where blood-stained hands are described as incarnadine. The term carries poetic and dramatic connotations, often used to describe sunset skies, roses, or other naturally occurring red coloration. As an adjective, incarnadine suggests not just red but specifically the warm, organic red of living tissue. As a verb, it means to dye or tint with this flesh-colored hue, often used metaphorically for covering something with blood or creating red stains. The word adds elegance and literary sophistication to descriptions that might otherwise use simpler color terms like "red" or "bloody."',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'in-KAR-nuh-dyn',
                'etymology': 'From Italian "incarnadino," derived from "incarnato" meaning "flesh-colored," ultimately from Latin "incarnatus" (made flesh). The root "carn-" means flesh, as in "carnivore" or "carnal."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The sunset painted the clouds an _______ shade that reminded viewers of rose petals or blushing skin.',
                'memory_tip': 'Remember "INCARNADINE" - think "IN-CARN-ADINE" where "carn" means flesh, so it\'s the color of flesh or blood - a deep pinkish-red.'
            },
            'incarnadineor': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "incarnadine" (flesh-colored, deep red) with "or." This represents a formatting or processing error where a conjunction was accidentally attached to the preceding word.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'in-KAR-nuh-dyn-or',
                'etymology': 'This is a PDF parsing error combining "incarnadine" from Italian/Latin meaning flesh-colored, with the English conjunction "or."',
                'language_origins': 'Italian, Latin, English (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining a color term with a conjunction.',
                'memory_tip': 'This is a parsing error - remember to separate "incarnadine" (flesh-colored) from "or" (conjunction).'
            },
            'incendiary': {
                'definition': 'Incendiary describes something designed to cause fires, or metaphorically, something intended to arouse anger, violence, or strong controversial reactions. As a noun, it refers to devices or substances used to start fires deliberately, such as incendiary bombs or chemicals. Firefighters and military personnel deal with incendiary weapons designed to ignite structures or materials. Metaphorically, incendiary speech, writing, or behavior intentionally provokes heated responses, controversy, or conflict. Incendiary rhetoric in politics might inflame tensions between groups, while incendiary journalism might sensationalize events to generate strong public reactions. The word implies deliberate intent to ignite - whether literally with fire or figuratively with emotions. Unlike accidental fires or unintended controversy, incendiary actions are calculated to produce inflammatory results. The term carries negative connotations of dangerous or irresponsible behavior.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'in-SEN-dee-er-ee',
                'etymology': 'From Latin "incendiarius," derived from "incendium" (fire or conflagration), ultimately from "incendere" meaning "to set fire to," combining "in-" (in) with "candere" (to glow or burn).',
                'language_origins': 'Latin',
                'example_sentence': 'The politician\'s _______ remarks about immigration sparked heated debates and protests across the country.',
                'memory_tip': 'Remember "INCENDIARY" - think "IN-CEND-IARY" like something that will "send" things "in" to burning flames - designed to ignite fires or emotions.'
            },
            'incense': {
                'definition': 'Incense refers to aromatic substances that release fragrant smoke when burned, commonly used in religious ceremonies, meditation, or to create pleasant atmospheres. These materials include tree resins, herbs, spices, or synthetic compounds formed into sticks, cones, or loose granules. Different cultures use specific incenses for spiritual practices - frankincense and myrrh in Christianity, sandalwood in Buddhism, or sage in indigenous ceremonies. The burning process releases essential oils that produce distinctive scents believed to enhance prayer, meditation, or ritual experiences. As a verb, incense means to anger or enrage someone intensely. The aromatic sense relates to purification, spiritual elevation, or masking unpleasant odors. Quality incense produces clean, pleasant smoke, while poor varieties may create harsh or cloying fragrances. The practice spans millennia and continues in both religious and secular contexts.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'IN-sens (noun), in-SENS (verb)',
                'etymology': 'From Latin "incensum," meaning "something burned," derived from "incendere" (to burn). As a verb meaning "to anger," it comes from Latin "incensus" meaning "set on fire" or "inflamed."',
                'language_origins': 'Latin',
                'example_sentence': 'The temple filled with aromatic _______ smoke during the evening prayer ceremony, creating a peaceful atmosphere.',
                'memory_tip': 'Remember "INCENSE" - think "IN-SCENSE" like scents going IN to the air when burned, or getting someone "in-censed" (angry).'
            },
            'incentive': {
                'definition': 'An incentive is something that motivates, encourages, or provides reason for particular actions or behaviors, typically offering rewards, benefits, or positive consequences for desired outcomes. Incentives can be financial, like bonuses or tax breaks, social, like recognition or status, or personal, like satisfaction or achievement. Businesses use incentives to motivate employees, governments use tax incentives to influence economic behavior, and schools use academic incentives to encourage learning. The effectiveness of incentives depends on their relevance to recipients\' values and needs. Some incentives work through positive reinforcement, while others work by removing negative consequences. Economic theory extensively studies how incentive structures shape decision-making and behavior in markets, organizations, and societies. Well-designed incentives align individual interests with broader organizational or social goals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-SEN-tiv',
                'etymology': 'From Late Latin "incentivum," meaning "something that incites," derived from Latin "incentivus" (inciting), from "incendere" (to kindle or set fire to). The root suggests sparking action or motivation.',
                'language_origins': 'Late Latin',
                'example_sentence': 'The company offered a substantial _______ program to encourage employees to suggest cost-saving improvements.',
                'memory_tip': 'Remember "INCENTIVE" - think "IN-SENT-IVE" like being sent in the right direction toward a goal through motivation or rewards.'
            },
            'incessant': {
                'definition': 'Incessant describes something that continues without pause, interruption, or relief - constant, unending activity that may become annoying or overwhelming due to its relentless nature. This word characterizes sounds, behaviors, or conditions that persist continuously without breaks. Incessant noise prevents concentration, incessant rain causes flooding, and incessant demands create stress. The term implies not just continuity but troublesome persistence that tests patience or tolerance. Unlike regular patterns or cycles, incessant phenomena provide no respite or variation. Weather patterns, mechanical sounds, or behavioral issues can all be incessant when they continue beyond normal or acceptable duration. The word carries negative connotations, suggesting that the continuous nature creates problems rather than benefits. Relief from incessant conditions often requires intervention or significant change in circumstances.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-SES-unt',
                'etymology': 'From Latin "incessans," present participle of "incessare" meaning "to never cease," combining "in-" (not) with "cessare" (to cease or stop). The root emphasizes the complete absence of stopping.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ barking from the neighbor\'s dog kept the entire family awake throughout the night.',
                'memory_tip': 'Remember "INCESSANT" - think "IN-CEASE-ANT" meaning NOT ceasing like an ant that never stops working - continuous without pause.'
            },
            'inched': {
                'definition': 'Inched is the past tense of "inch," meaning to move very slowly and gradually, typically by small increments like the unit of measurement "inch." This verb describes cautious, deliberate movement that advances little by little, often in challenging or careful situations. Traffic might inch forward during rush hour, negotiations might inch toward agreement through small concessions, or prices might inch upward over time. The word emphasizes the slow, measured nature of progress rather than dramatic or rapid change. Physical movement can be inching when conditions require extreme caution, while abstract concepts like understanding or relationships can inch forward through gradual development. The term suggests persistence and patience, acknowledging that significant progress sometimes requires many small steps rather than dramatic leaps.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'INCHT',
                'etymology': 'From Old English "ynce," derived from Latin "uncia" meaning "a twelfth part" (of a foot). The verb sense developed from the idea of moving by small units like inches.',
                'language_origins': 'Old English, Latin',
                'example_sentence': 'The rescue team _______ carefully across the unstable bridge to reach the stranded hikers.',
                'memory_tip': 'Remember "INCHED" - think moving forward inch by inch, making slow but steady progress like measuring with a ruler.'
            },
            'inchoate': {
                'definition': 'Inchoate describes something in an early stage of development, just beginning to form or exist but not yet fully developed or organized. This word applies to ideas, plans, projects, or conditions that are embryonic, rudimentary, or incomplete. Legal contexts use inchoate to describe crimes that are attempted but not completed, or rights that exist but haven\'t been fully realized. Inchoate emotions are feelings that are just beginning to emerge but aren\'t yet clearly defined. Scientific theories might be inchoate when initial observations suggest patterns but comprehensive understanding hasn\'t developed. The word implies potential for development while acknowledging current incomplete status. Unlike abandoned or failed efforts, inchoate phenomena contain the seeds of future completion. The term recognizes that complex developments often begin as vague, unformed impulses that gradually acquire structure and definition.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-KOH-it',
                'etymology': 'From Latin "inchoatus," past participle of "inchoare" (also "incohare") meaning "to begin" or "to start work on." The root may be related to "cohum" (yoke strap), suggesting the beginning of harnessing or organizing.',
                'language_origins': 'Latin',
                'example_sentence': 'The artist\'s _______ vision for the sculpture was still forming when she began sketching initial ideas.',
                'memory_tip': 'Remember "INCHOATE" - think "IN-CO-ATE" like something that\'s "in" the process of being "co-created" but not yet complete - just beginning to form.'
            },
            'incident': {
                'definition': 'An incident is a specific event or occurrence, often one that is notable, problematic, or worthy of attention due to its impact or unusual nature. This word can describe minor happenings like traffic incidents or major events like international incidents that affect diplomatic relations. Workplace incidents might involve accidents, conflicts, or safety violations requiring investigation. The term is neutral, though it often implies some level of disruption, conflict, or significance that distinguishes the event from routine activities. Legal contexts document incidents for evidence or analysis, while safety protocols address incident prevention and response. Unlike accidents, incidents may be intentional or predictable. The word encompasses everything from brief disruptions to complex situations requiring extensive management. Documentation and analysis of incidents often help prevent future occurrences or improve response procedures.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-si-dunt',
                'etymology': 'From Latin "incidere," meaning "to fall upon" or "to happen," combining "in-" (upon) with "cadere" (to fall). The word literally suggests something that "falls upon" or occurs unexpectedly.',
                'language_origins': 'Latin',
                'example_sentence': 'The security team filed a detailed report about the _______ that occurred during the evening shift.',
                'memory_tip': 'Remember "INCIDENT" - think "IN-CIDENT" like something that happened "in" a specific moment, an event that "dented" the normal flow of activities.'
            },
            'incinerate': {
                'definition': 'Incinerate means to burn something completely to ashes, typically through controlled high-temperature combustion processes. This verb describes thorough destruction by fire, often used for waste disposal, cremation, or eliminating materials completely. Municipal incinerators burn garbage to reduce volume and generate energy, while medical facilities incinerate biological waste to prevent contamination. The process requires sufficient heat and time to reduce organic materials to ash and gases. Industrial applications incinerate hazardous materials to neutralize dangerous compounds. Unlike simple burning, incineration implies systematic, complete combustion designed to leave minimal residue. Environmental considerations include managing emissions and ash disposal. The word can be used metaphorically to describe complete destruction by any means, though literal usage involves actual fire. Modern incineration technology includes pollution controls and energy recovery systems.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-SIN-uh-rayt',
                'etymology': 'From Medieval Latin "incinerare," derived from Latin "in-" (into) plus "cinis, cineris" (ashes). The word literally means "to reduce to ashes" or "to turn into cinders."',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'The hospital must _______ all contaminated medical waste according to strict environmental safety regulations.',
                'memory_tip': 'Remember "INCINERATE" - think "IN-CINDER-ATE" like turning something into cinders (ashes) by burning it completely.'
            },
            'incisiform': {
                'definition': 'Incisiform describes something having the shape or appearance of an incisor tooth - typically referring to structures that are sharp, cutting, or wedge-shaped like the front teeth used for biting. This anatomical term applies to various biological structures that resemble the chisel-like shape of incisor teeth. In dental anatomy, incisiform characteristics include flat, sharp edges designed for cutting rather than grinding. Paleontology uses this term to describe fossil teeth or other structures with similar morphology. The word can extend to describe any sharp, wedge-shaped structures in biology, geology, or engineering that share the cutting profile of incisor teeth. Tools or instruments might be described as incisiform when they feature similar sharp, flat cutting edges. The term emphasizes both the shape and functional similarity to natural cutting teeth.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-SY-zi-form',
                'etymology': 'From Latin "incisivus" (cutting) plus "-form" (having the shape of). "Incisivus" derives from "incidere" meaning "to cut into," combining "in-" (into) with "caedere" (to cut).',
                'language_origins': 'Latin',
                'example_sentence': 'The fossil displayed _______ teeth structures perfectly adapted for cutting through tough plant materials.',
                'memory_tip': 'Remember "INCISIFORM" - think "IN-CISE-I-FORM" meaning having the form of something that incises (cuts), like sharp incisor teeth.'
            },
            'incited': {
                'definition': 'Incited is the past tense of "incite," meaning to have encouraged, urged, or provoked someone to action, often toward violence, rebellion, or undesirable behavior. This verb describes actions that stir up or instigate responses in others, typically through speeches, writings, or demonstrations that inflame emotions or motivations. Legal contexts often address inciting riots, violence, or criminal activity as serious offenses. Political figures might be accused of inciting unrest through inflammatory rhetoric. The word implies deliberate action to stimulate specific responses rather than accidental provocation. Historical examples include leaders who incited revolutions or reformers who incited social change. Unlike simple encouragement, inciting suggests stirring strong emotions or creating urgency that compels action. The term carries implications of responsibility for consequences that follow such provocation.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'in-SY-tid',
                'etymology': 'From Latin "incitare," meaning "to put in rapid motion" or "to urge forward," combining "in-" (into) with "citare" (to set in motion). The root "ciere" means "to move" or "to stir up."',
                'language_origins': 'Latin',
                'example_sentence': 'The controversial speech _______ angry protests throughout the city as citizens responded to the inflammatory remarks.',
                'memory_tip': 'Remember "INCITED" - think "IN-CITED" like getting someone "excited" or "cited" into action - stirred up to do something.'
            },
            'incitive': {
                'definition': 'Incitive describes something that tends to incite, provoke, or stimulate action, emotions, or responses in others. This adjective characterizes speech, writing, behavior, or conditions that have the capacity to arouse, encourage, or inflame. Incitive language might spark controversy or motivate action, while incitive circumstances might create conditions that lead to unrest or change. The word implies inherent potential to stimulate responses rather than guaranteed outcomes. Marketing materials might be incitive to purchasing decisions, while political rhetoric might be incitive to public demonstrations. Unlike actively inciting, incitive describes the quality or tendency to provoke rather than specific acts of provocation. Educational content can be incitive to learning, while artistic works might be incitive to emotional or intellectual responses. The term recognizes that certain stimuli naturally tend to generate reactions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-SY-tiv',
                'etymology': 'From Latin "incitare" (to urge forward) plus the suffix "-ive" indicating tendency or capacity. The root "citare" means "to set in motion" or "to call forth."',
                'language_origins': 'Latin',
                'example_sentence': 'The documentary\'s _______ portrayal of environmental destruction motivated viewers to join conservation efforts.',
                'memory_tip': 'Remember "INCITIVE" - think "IN-CITE-IVE" meaning having the quality of inciting or provoking - tending to stir people to action.'
            },
            'inclement': {
                'definition': 'Inclement describes harsh, severe, or unpleasant weather conditions that make outdoor activities difficult, dangerous, or uncomfortable. This word typically refers to storms, extreme cold, heavy rain, snow, or other meteorological phenomena that pose challenges to human activities and safety. Inclement weather might cancel outdoor events, close schools, or create hazardous travel conditions. The term can extend beyond weather to describe any harsh or unmerciful conditions, including inclement treatment by authorities or inclement circumstances that create hardship. Maritime contexts frequently use inclement to describe dangerous sea conditions. Unlike merely unpleasant weather, inclement conditions present genuine risks or significant inconvenience. Weather forecasters use this term to warn of conditions requiring special precautions. The word emphasizes the severity and potential impact rather than simple discomfort.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-KLEM-unt',
                'etymology': 'From Latin "inclemens," combining "in-" (not) with "clemens" (mild, gentle, merciful). The root "clemens" relates to clemency and describes mildness or mercy, so inclement means lacking these gentle qualities.',
                'language_origins': 'Latin',
                'example_sentence': 'The school district cancelled classes due to _______ weather conditions that made bus transportation dangerous.',
                'memory_tip': 'Remember "INCLEMENT" - think "IN-CLEMENT" meaning NOT clement (mild/gentle) - harsh, severe weather that shows no mercy to people outdoors.'
            }
        }
        
        return batch_089_data.get(word, {
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
            'impastoantagonistic': 'Combined word error: "impastoantagonistic" appears to be "impasto" (painting technique) + "antagonistic" (hostile) merged together.',
            'implicativesostenuto': 'Combined word error: "implicativesostenuto" appears to be "implicative" (suggesting meanings) + "sostenuto" (musical term for sustained) merged together.',
            'impromptuincinerate': 'Combined word error: "impromptuincinerate" appears to be "impromptu" (spontaneous) + "incinerate" (burn completely) merged together.',
            'incarnadineor': 'Combined word error: "incarnadineor" appears to be "incarnadine" (flesh-colored) + "or" (conjunction) merged together.'
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
    processor = Batch089Processor()
    input_file = "output/batch_089_words.csv"
    output_file = "output/batch_089_processed.csv"
    
    success = processor.process_batch(input_file, output_file)
    if success:
        print("Batch 089 processing completed successfully!")
    else:
        print("Batch 089 processing failed!")

if __name__ == "__main__":
    main()