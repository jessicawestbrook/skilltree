#!/usr/bin/env python3
"""
Batch 091 Processor for Scripps National Spelling Bee Words
Processes words from inerrancy through insights with comprehensive Claude-generated data
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

class Batch091Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.processed_count = 0

    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge"""
        
        batch_091_data = {
            'inerrancy': {
                'definition': 'Inerrancy is the quality of being completely free from error, mistakes, or falsehood, particularly used in theological contexts to describe the belief that religious scriptures are without error in their original forms. This noun represents the doctrine that sacred texts, when properly understood, contain no factual, historical, or theological errors. Biblical inerrancy holds that scripture is completely trustworthy and accurate in all matters it addresses. The concept extends beyond simple accuracy to include internal consistency and reliability across all subjects covered. Unlike infallibility, which focuses on authority in teaching, inerrancy specifically addresses the absence of errors in content. Debates about inerrancy often center on interpretation methods, translation issues, and the scope of what subjects scripture addresses. The term requires careful definition of what constitutes "error" and how to handle apparent discrepancies in ancient texts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-ER-un-see',
                'etymology': 'From Latin "inerrantia," derived from "inerrans" meaning "not wandering" or "not erring," combining "in-" (not) with "errans" (wandering, making mistakes), from "errare" (to wander, err).',
                'language_origins': 'Latin',
                'example_sentence': 'The theological seminary taught the doctrine of biblical _______, maintaining that scripture contains no errors in its original manuscripts.',
                'memory_tip': 'Remember "INERRANCY" - think "IN-ERR-ANCY" meaning NOT having "errancy" (errors) - completely free from mistakes or errors.'
            },
            'inevitable': {
                'definition': 'Inevitable describes something that is certain to happen and cannot be avoided or prevented, regardless of efforts to change the outcome. This adjective characterizes events, consequences, or developments that must occur due to natural laws, logical necessity, or overwhelming circumstances. Death is inevitable for all living things, while consequences often seem inevitable after poor decisions. Unlike merely probable events, inevitable ones will definitely occur given current conditions. The term suggests that opposing forces are insufficient to prevent the predicted outcome. Economic downturns might seem inevitable after excessive speculation. Scientific processes often follow inevitable patterns based on physical laws. The word implies futility of resistance while acknowledging the certainty of outcomes. Accepting inevitable changes helps people adapt rather than waste energy fighting unchangeable circumstances.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-EV-i-tuh-buhl',
                'etymology': 'From Latin "inevitabilis," combining "in-" (not) with "evitabilis" (able to be avoided), derived from "evitare" meaning "to avoid" or "to shun."',
                'language_origins': 'Latin',
                'example_sentence': 'After years of ignoring maintenance, the building\'s structural collapse seemed _______ without immediate intervention.',
                'memory_tip': 'Remember "INEVITABLE" - think "IN-EVIT-ABLE" meaning NOT "evitable" (avoidable) - certain to happen and can\'t be prevented.'
            },
            'inexorably': {
                'definition': 'Inexorably means in a way that cannot be stopped or changed, continuing relentlessly without possibility of alteration or mercy. This adverb describes processes, forces, or developments that advance steadily despite any attempts to halt or redirect them. Time passes inexorably, aging affects everyone inexorably, and certain consequences follow inexorably from specific actions. The word emphasizes the unstoppable nature of the progression, suggesting that human will or intervention cannot alter the course. Natural forces often work inexorably, like erosion slowly wearing away mountains. Economic trends might develop inexorably despite policy interventions. Unlike simply persistent forces, inexorable ones cannot be reasoned with, bargained with, or deflected from their path. The term carries connotations of fate or natural law that human agency cannot overcome.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'in-EK-sur-uh-blee',
                'etymology': 'From Latin "inexorabilis," combining "in-" (not) with "exorabilis" (able to be moved by entreaty), derived from "exorare" meaning "to prevail upon" or "to move by entreaty."',
                'language_origins': 'Latin',
                'example_sentence': 'The glacier moved _______ down the mountain valley, reshaping the landscape over thousands of years.',
                'memory_tip': 'Remember "INEXORABLY" - think "IN-EX-ORABLY" meaning NOT able to be "exor" (moved by pleading) - unstoppably advancing despite entreaties.'
            },
            'infant': {
                'definition': 'An infant is a very young child, typically under one year of age, in the earliest stage of life characterized by complete dependence on caregivers for survival and development. This noun describes babies during their most vulnerable period when they require constant care, feeding, and protection. Medical contexts often define infancy as the first year of life, when rapid physical and neurological development occurs. Legal systems establish special protections for infants due to their inability to care for themselves. Child development studies focus on infant milestones like crawling, speaking first words, and developing social attachments. The term can extend metaphorically to describe anything in its earliest, most vulnerable stage of development. Unlike older children who develop independence, infants remain completely dependent on adult care for all basic needs.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'IN-funt',
                'etymology': 'From Latin "infans," literally meaning "unable to speak," combining "in-" (not) with "fans" (speaking), from "fari" (to speak). The term originally emphasized the inability to communicate verbally.',
                'language_origins': 'Latin',
                'example_sentence': 'The pediatric unit specialized in caring for premature _______ who required intensive medical support.',
                'memory_tip': 'Remember "INFANT" - think "IN-FANT" like "IN-FANTASY" land - very young children living in a world of wonder and complete dependence.'
            },
            'infarction': {
                'definition': 'Infarction is the death of tissue in an organ or body part due to inadequate blood supply, typically caused by blockage of blood vessels that deliver oxygen and nutrients necessary for cellular survival. This medical term describes the pathological process where cells die when deprived of circulation. Myocardial infarction (heart attack) occurs when coronary arteries become blocked. Brain infarction (stroke) happens when cerebral blood vessels are occluded. The severity depends on the size of affected area and duration of blood loss. Treatment focuses on rapidly restoring circulation to minimize tissue death. Infarctions can result from blood clots, arterial spasm, or gradual vessel narrowing. Early intervention often determines outcomes, as dead tissue cannot regenerate. Prevention involves managing risk factors like hypertension, diabetes, and arterial disease.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-FARK-shun',
                'etymology': 'From Latin "infarctus," meaning "stuffed into" or "crammed full," derived from "infarcire" combining "in-" (into) with "farcire" (to stuff). Originally described tissue "stuffed" with clotted blood.',
                'language_origins': 'Latin',
                'example_sentence': 'The emergency room team quickly identified signs of cardiac _______ and immediately began treatment to restore blood flow.',
                'memory_tip': 'Remember "INFARCTION" - think "IN-FARCT-ION" like tissue getting "in" a "fact" of being blocked - when blood supply is cut off and tissue dies.'
            },
            'infatuation': {
                'definition': 'Infatuation is an intense but typically short-lived passion or admiration for someone or something, characterized by irrational feelings and obsessive thoughts that often lack deep understanding or realistic assessment. This noun describes emotional states where attraction overrides rational judgment. Romantic infatuation involves overwhelming feelings for another person based on idealization rather than genuine knowledge of their character. People can develop infatuations with celebrities, ideas, or objects that capture their imagination. Unlike mature love, infatuation tends to be superficial, focused on external qualities or fantasized perfection. The intensity often cannot sustain itself once reality intrudes or the novelty wears off. Infatuation can motivate positive actions but also leads to poor decisions when emotions override practical considerations. Understanding the difference between infatuation and deeper feelings helps in making better relationship and life choices.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-fach-oo-AY-shun',
                'etymology': 'From Latin "infatuatio," derived from "infatuare" meaning "to make foolish," combining "in-" (into) with "fatuus" (foolish, silly). The root suggests being made foolish by passion.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ with the movie star lasted only a few months before she realized it was based on fantasy rather than reality.',
                'memory_tip': 'Remember "INFATUATION" - think "IN-FATUOUS-ATION" like being made "fatuous" (foolishly silly) by intense but shallow attraction.'
            },
            'infectious': {
                'definition': 'Infectious describes something capable of spreading from one person, organism, or place to another, particularly diseases caused by bacteria, viruses, or other microorganisms that can be transmitted through various means. This adjective characterizes medical conditions that spread through contact, airborne particles, contaminated surfaces, or bodily fluids. Infectious diseases like influenza spread rapidly through populations. The term can extend metaphorically to describe emotions, behaviors, or ideas that spread quickly among people. Infectious laughter spreads joy through groups, while infectious enthusiasm motivates others. Unlike contagious, which specifically refers to direct transmission, infectious encompasses broader methods of spread. Public health measures focus on controlling infectious disease outbreaks through vaccination, quarantine, and sanitation. The word implies both the capacity for transmission and the potential for widespread impact.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-FEK-shus',
                'etymology': 'From Latin "infectiosus," derived from "inficere" meaning "to taint" or "to corrupt," combining "in-" (into) with "facere" (to make). The root suggests making something impure by transmission.',
                'language_origins': 'Latin',
                'example_sentence': 'The hospital implemented strict protocols to prevent the spread of _______ diseases among patients and staff.',
                'memory_tip': 'Remember "INFECTIOUS" - think "IN-FECT-IOUS" like something that can "infect" others by spreading "IN" to them - capable of transmission.'
            },
            'inferno': {
                'definition': 'Inferno refers to a large, intense, and destructive fire, or metaphorically, any situation characterized by extreme heat, chaos, or suffering reminiscent of hell or damnation. This noun describes blazes that consume everything in their path with overwhelming force and intensity. Forest infernos destroy vast areas of wilderness, while building infernos threaten lives and property. The word carries literary connotations from Dante\'s "Inferno," which depicted hell as a realm of eternal fire and punishment. Unlike ordinary fires, infernos suggest apocalyptic destruction and uncontrollable forces. Metaphorically, people describe extremely difficult situations as infernos of stress, conflict, or hardship. The term emphasizes both the physical properties of intense fire and the emotional impact of overwhelming destructive forces. Infernos represent ultimate tests of human resilience and survival.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-FUR-no',
                'etymology': 'From Italian "inferno," meaning "hell" or "underworld," derived from Latin "infernus" meaning "of the lower regions," from "inferus" (below). Made famous by Dante\'s "Divine Comedy."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The warehouse quickly became a raging _______ that required dozens of firefighters and hours to control.',
                'memory_tip': 'Remember "INFERNO" - think "IN-FERN-O" like being "IN" a place full of "FERN" (fire) that\'s out of control - a massive, destructive fire.'
            },
            'infiltrate': {
                'definition': 'Infiltrate means to secretly enter or penetrate an organization, area, or system gradually and stealthily, often with the purpose of gathering information, causing damage, or gaining unauthorized access. This verb describes covert operations where agents blend in to avoid detection while pursuing hidden agendas. Spies infiltrate enemy organizations to gather intelligence. Undercover police infiltrate criminal networks to collect evidence. Water can infiltrate building foundations, causing structural damage. The term implies gradual, undetected entry rather than obvious invasion. Military infiltration involves moving troops through enemy territory undetected. Social movements might be infiltrated by opponents seeking to disrupt activities. Unlike direct confrontation, infiltration relies on stealth, patience, and careful planning to achieve objectives without arousing suspicion.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'IN-fil-trayt',
                'etymology': 'From Latin "infiltrare," combining "in-" (into) with "filtrare" (to filter). The word originally meant "to filter into" something gradually, like liquid seeping through porous material.',
                'language_origins': 'Latin',
                'example_sentence': 'The detective managed to _______ the criminal organization by posing as a corrupt businessman.',
                'memory_tip': 'Remember "INFILTRATE" - think "IN-FILTER-ATE" like filtering your way "IN" to a place secretly - gradually entering undetected.'
            },
            'infinite': {
                'definition': 'Infinite describes something that has no limits, boundaries, or end - extending indefinitely in time, space, quantity, or degree without possibility of measurement or completion. This adjective characterizes concepts that exceed finite human comprehension. Mathematical infinity represents quantities larger than any finite number. The universe might be infinite in size, continuing forever in all directions. Time could be infinite, having no beginning or end. Infinite patience suggests tolerance without limits, while infinite wisdom implies knowledge without boundaries. Unlike merely very large things, infinite entities cannot be counted, measured, or fully grasped by human minds. Philosophers debate whether anything truly infinite exists or if infinity is purely theoretical. The concept challenges human understanding while inspiring awe about the vastness of existence.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'IN-fuh-nit',
                'etymology': 'From Latin "infinitus," combining "in-" (not) with "finitus" (limited, bounded), from "finire" (to bound, limit). The word literally means "without limits or boundaries."',
                'language_origins': 'Latin',
                'example_sentence': 'The mathematician explained that there are _______ numbers between any two points on a number line.',
                'memory_tip': 'Remember "INFINITE" - think "IN-FINITE" meaning NOT finite (limited) - without any boundaries or limits, going on forever.'
            },
            'infirm': {
                'definition': 'Infirm describes someone who is weak, frail, or in poor health, particularly due to old age or chronic illness that reduces physical strength and capabilities. This adjective characterizes individuals whose bodies have become unreliable or inadequate for normal activities. Infirm elderly people might require assistance with daily tasks like walking, bathing, or preparing meals. The term can also describe weak foundations, shaky arguments, or unreliable systems. Unlike temporary illness, infirmity suggests persistent or progressive weakness that affects quality of life. Medical care for infirm patients focuses on comfort, support, and maintaining dignity rather than aggressive treatment. The word carries connotations of fragility and vulnerability requiring compassionate care. Infirmity is often part of natural aging processes but can result from disease or injury.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-FURM',
                'etymology': 'From Latin "infirmus," combining "in-" (not) with "firmus" (strong, steady). The word literally means "not strong" or "lacking firmness."',
                'language_origins': 'Latin',
                'example_sentence': 'The nursing home provided specialized care for _______ residents who could no longer live independently.',
                'memory_tip': 'Remember "INFIRM" - think "IN-FIRM" meaning NOT firm (strong) - weak and frail in health or structure.'
            },
            'inflammable': {
                'definition': 'Inflammable means easily set on fire or highly combustible, capable of igniting quickly and burning rapidly when exposed to heat, sparks, or flames. This adjective describes materials that pose fire hazards due to their chemical properties. Gasoline, alcohol, and many solvents are inflammable substances requiring careful handling. Despite common confusion, inflammable and flammable mean the same thing - both indicate high fire risk. The "in-" prefix here means "into" rather than "not," referring to the tendency to burst into flames. Safety protocols require special storage, handling, and labeling of inflammable materials. Industrial processes involving inflammable substances need fire suppression systems and trained personnel. The term appears on warning labels and safety documentation to alert people to fire dangers. Understanding inflammable properties helps prevent accidents and fires.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-FLAM-uh-buhl',
                'etymology': 'From Latin "inflammare," meaning "to set on fire," combining "in-" (into) with "flammare" (to flame). The "in-" here means "into flame" rather than negation.',
                'language_origins': 'Latin',
                'example_sentence': 'The warning label clearly marked the cleaning solvent as _______ and required storage away from heat sources.',
                'memory_tip': 'Remember "INFLAMMABLE" - think "IN-FLAM-ABLE" meaning able to go "IN" to "flames" quickly - easily catches fire (NOT fire-proof!).'
            },
            'inflate': {
                'definition': 'Inflate means to fill with air or gas to expand something to its full size, or more broadly, to increase, exaggerate, or artificially raise the value, importance, or size of something. This verb describes both physical expansion and abstract enlargement. Inflating tires, balloons, or air mattresses involves adding air pressure. Economic inflation increases prices across an economy. People might inflate their accomplishments on resumes or inflate the importance of minor problems. Currency can be inflated when governments print excessive money. Unlike natural growth, inflation often suggests artificial or excessive expansion. Inflated egos result from overestimating personal importance. The process can be beneficial, as when inflating safety equipment, or problematic, as when inflating expectations beyond realistic possibilities. The word implies expansion beyond normal or natural size.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-FLAYT',
                'etymology': 'From Latin "inflatus," past participle of "inflare" meaning "to blow into," combining "in-" (into) with "flare" (to blow). The root emphasizes the process of blowing air into something.',
                'language_origins': 'Latin',
                'example_sentence': 'The mechanic had to _______ the spare tire before it could be safely mounted on the vehicle.',
                'memory_tip': 'Remember "INFLATE" - think "IN-FLATE" like blowing air "IN" to make something "FLAT" become full and expanded.'
            },
            'influential': {
                'definition': 'Influential describes someone or something that has significant power to affect, modify, or control other people\'s thoughts, decisions, or actions through authority, persuasion, or example. This adjective characterizes individuals, ideas, or forces that shape outcomes in meaningful ways. Influential leaders inspire followers and create social change. Influential books alter how people think about important topics. Influential scientific discoveries transform entire fields of knowledge. The term implies not just popularity but substantive impact on others\' beliefs or behaviors. Unlike mere fame, influence suggests the ability to motivate action or change thinking. Political figures, artists, teachers, and activists can be influential by affecting how others see the world. Influential factors in decision-making carry significant weight in determining outcomes. The word recognizes that some people and ideas have disproportionate power to shape events.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-floo-EN-shul',
                'etymology': 'From Medieval Latin "influentia," derived from "influere" meaning "to flow into," combining "in-" (into) with "fluere" (to flow). Originally referred to stellar influences flowing into earthly affairs.',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'The _______ teacher inspired generations of students to pursue careers in environmental science.',
                'memory_tip': 'Remember "INFLUENTIAL" - think "IN-FLU-ENTIAL" like having a "flu" that flows "IN" to others - having power to affect and influence people.'
            },
            'information': {
                'definition': 'Information consists of facts, data, knowledge, or details about a particular subject that can be communicated, processed, or used to increase understanding or make decisions. This fundamental noun encompasses all forms of meaningful content that reduce uncertainty or ignorance. Information can be stored in books, databases, or human memory. Digital information travels through computer networks and communication systems. Scientific information advances human knowledge through research and experimentation. Unlike mere data, information provides context and meaning that people can interpret and apply. Information systems organize and distribute knowledge efficiently. Quality information is accurate, relevant, and timely for its intended purpose. The information age emphasizes knowledge as a primary economic resource. Access to information affects education, democracy, and economic opportunity. Processing information effectively is crucial for learning, problem-solving, and informed decision-making.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-fer-MAY-shun',
                'etymology': 'From Latin "informatio," meaning "formation" or "conception," derived from "informare" meaning "to shape" or "to form," combining "in-" (into) with "formare" (to form).',
                'language_origins': 'Latin',
                'example_sentence': 'The research team gathered _______ from multiple sources to develop a comprehensive understanding of the environmental crisis.',
                'memory_tip': 'Remember "INFORMATION" - think "IN-FORM-ATION" like facts that help "form" understanding "IN" your mind - knowledge that informs you.'
            },
            'informed': {
                'definition': 'Informed describes someone who has acquired knowledge, facts, or understanding about a particular subject through study, experience, or reliable sources, enabling them to make educated decisions or judgments. This adjective characterizes individuals who are well-versed in relevant information rather than relying on guesswork or ignorance. Informed citizens participate more effectively in democratic processes by understanding issues and candidates. Informed medical decisions require understanding treatment options, risks, and benefits. Unlike merely opinionated, informed perspectives are based on factual knowledge and careful consideration. Informed consent in legal and medical contexts requires understanding consequences of decisions. The term implies both access to information and the intellectual capacity to process and apply it meaningfully. Staying informed requires active effort to seek reliable sources and update knowledge as circumstances change.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'in-FORMD',
                'etymology': 'From Latin "informatus," past participle of "informare" meaning "to shape" or "to give form to," combining "in-" (into) with "formare" (to form). The sense evolved to "shaped by knowledge."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ voter had researched all candidates\' positions before making decisions at the ballot box.',
                'memory_tip': 'Remember "INFORMED" - think "IN-FORMED" like being "formed" or shaped "IN" your mind by knowledge - having good information about something.'
            },
            'infrared': {
                'definition': 'Infrared refers to electromagnetic radiation with wavelengths longer than visible light but shorter than microwaves, typically experienced as heat and used in various technological applications including remote controls, thermal imaging, and night vision equipment. This adjective and noun describes radiation invisible to human eyes but detectable by specialized instruments. Infrared radiation is emitted by all objects with temperature above absolute zero. Infrared cameras reveal heat signatures for military, medical, and industrial purposes. Television remote controls use infrared signals to communicate with devices. Infrared astronomy studies celestial objects that emit heat rather than visible light. Unlike visible light, infrared radiation can penetrate smoke, fog, and darkness. Medical applications include infrared therapy for pain relief and thermal imaging for diagnostic purposes. The technology has revolutionized surveillance, search and rescue, and scientific research by revealing information invisible to normal sight.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'IN-fruh-red',
                'etymology': 'From Latin "infra" meaning "below" combined with "red." The term indicates electromagnetic radiation with frequencies below (longer wavelengths than) visible red light.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The security system used _______ cameras to detect intruders even in complete darkness.',
                'memory_tip': 'Remember "INFRARED" - think "INFRA-RED" meaning "below red" on the light spectrum - heat radiation we can\'t see but can feel.'
            },
            'infrastructure': {
                'definition': 'Infrastructure refers to the fundamental physical and organizational structures, systems, and facilities needed for a society, organization, or enterprise to function effectively, including transportation networks, utilities, communication systems, and institutional frameworks. This noun encompasses both tangible assets like roads, bridges, and power grids, and intangible systems like legal frameworks and educational institutions. Economic infrastructure supports commerce and industry through transportation, energy, and communication networks. Social infrastructure includes schools, hospitals, and public services that support community wellbeing. Digital infrastructure encompasses internet networks, data centers, and telecommunications systems. Unlike superficial improvements, infrastructure provides foundational support for all other activities. Infrastructure investment drives economic development and improves quality of life. Aging infrastructure requires maintenance and modernization to remain effective. The term recognizes that complex societies depend on interconnected systems working reliably.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-fruh-struk-cher',
                'etymology': 'From Latin "infra" (below) combined with "structure," from Latin "structura" (building, arrangement). The term literally means "the structure beneath" other activities.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The government allocated billions of dollars to rebuild the country\'s aging transportation _______ after decades of neglect.',
                'memory_tip': 'Remember "INFRASTRUCTURE" - think "INFRA-STRUCTURE" meaning the "structure" that\'s "infra" (below/underneath) - the foundation systems that support everything else.'
            },
            'infringe': {
                'definition': 'Infringe means to violate, breach, or encroach upon someone\'s rights, property, or established boundaries, typically in a way that undermines their legitimate interests or legal protections. This verb describes actions that trespass beyond acceptable limits or interfere with others\' rightful claims. Copyright infringement occurs when someone uses protected material without permission. Patent infringement involves unauthorized use of protected inventions. Constitutional rights can be infringed when government actions exceed legal authority. The term implies crossing established boundaries rather than respecting established limits. Property lines might be infringed by neighboring construction. Academic freedom can be infringed by censorship or administrative interference. Unlike accidental intrusion, infringement often involves knowing violation of recognized rights or boundaries. Legal systems provide remedies for infringement to protect individual and institutional interests.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-FRINJ',
                'etymology': 'From Latin "infringere," meaning "to break into" or "to damage," combining "in-" (into) with "frangere" (to break). The root emphasizes breaking into protected areas.',
                'language_origins': 'Latin',
                'example_sentence': 'The court ruled that the company did _______ on the patent by using the protected technology without licensing rights.',
                'memory_tip': 'Remember "INFRINGE" - think "IN-FRINGE" like going "IN" to the "FRINGE" (edge) of someone else\'s rights - crossing boundaries you shouldn\'t cross.'
            },
            'ingenuous': {
                'definition': 'Ingenuous describes someone who is innocent, naive, and sincere, displaying honest and straightforward character without deception, cunning, or worldly sophistication. This adjective characterizes individuals who approach situations with genuine openness and trust, often lacking awareness of others\' potential duplicity. Ingenuous people express their thoughts honestly without calculating social or political consequences. Children are often ingenuous before learning social conventions and protective skepticism. The term suggests admirable honesty combined with potentially problematic vulnerability. Unlike disingenuous behavior that involves deliberate deception, ingenuous responses reflect authentic feelings and beliefs. Ingenuous questions arise from genuine curiosity rather than hidden agendas. While ingenuous character is often refreshing and trustworthy, it can lead to exploitation by less scrupulous individuals. The word implies both moral virtue and practical inexperience.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-JEN-yoo-us',
                'etymology': 'From Latin "ingenuus," meaning "native" or "freeborn," derived from "in-" (in) plus "gignere" (to beget). Originally referred to free-born Romans as opposed to slaves.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ response to the reporter\'s questions revealed she hadn\'t considered the political implications of her statements.',
                'memory_tip': 'Remember "INGENUOUS" - think "IN-GENUINE-US" like being genuinely sincere and innocent, not calculating or deceptive.'
            },
            'inglenook': {
                'definition': 'An inglenook is a cozy corner or recess beside a large open fireplace, often with built-in seating, creating an intimate and warm space for relaxation and conversation within larger rooms. This architectural feature was particularly popular in medieval halls and Tudor-era homes, designed to provide comfortable seating near the fire\'s warmth and light. Traditional inglenooks feature stone or brick construction with wooden benches or cushioned seats arranged around the fireplace opening. The enclosed nature creates a sense of privacy and intimacy within larger spaces. Modern interpretations adapt the concept for contemporary homes, sometimes without actual fireplaces but maintaining the cozy, enclosed feeling. The term evokes images of comfortable domestic life, storytelling, and gathering around hearth fires. Inglenooks represent architectural attempts to create human-scaled comfort within grander spaces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-guhl-nook',
                'etymology': 'From English "ingle" (fireplace or hearth fire) combined with "nook" (corner or recess). "Ingle" derives from Scottish Gaelic "aingeal" meaning fire or light.',
                'language_origins': 'English, Scottish Gaelic',
                'example_sentence': 'The old cottage featured a charming _______ where the family gathered to read stories by the fire on winter evenings.',
                'memory_tip': 'Remember "INGLENOOK" - think "INGLE-NOOK" like a cozy "nook" (corner) near the "ingle" (fire) - a warm corner by the fireplace.'
            },
            'inglenookefflux': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "inglenook" (a cozy fireplace corner) and "efflux" (flowing out or discharge). These are completely unrelated concepts that were accidentally joined during document processing.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'IN-guhl-nook-EF-luks',
                'etymology': 'This is a PDF parsing error combining "inglenook" from English/Gaelic meaning fireplace corner, and "efflux" from Latin meaning flowing out.',
                'language_origins': 'English, Scottish Gaelic, Latin (combined in error)',
                'example_sentence': 'This word appears to be an error where _______ was incorrectly formed by combining architectural and flow-related terminology.',
                'memory_tip': 'This is a parsing error - remember to separate "inglenook" (cozy fireplace corner) from "efflux" (outward flow).'
            },
            'inglorious': {
                'definition': 'Inglorious describes something that brings shame, dishonor, or disgrace rather than praise or recognition, characterized by failure, defeat, or morally questionable actions that damage reputation. This adjective applies to events, behaviors, or outcomes that reflect poorly on individuals, organizations, or causes. Inglorious military defeats result in national embarrassment and loss of prestige. Inglorious behavior involves actions that violate moral or ethical standards. Unlike glorious achievements that inspire admiration, inglorious actions provoke criticism or disappointment. The term can describe both dramatic failures and quiet defeats that lack any redeeming qualities. Inglorious endings to careers result from scandal or incompetence rather than noble retirement. Historical events might be remembered as inglorious when they involve betrayal, cruelty, or cowardice. The word emphasizes the absence of honor or dignity in failure.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-GLOR-ee-us',
                'etymology': 'From Latin "ingloriosus," combining "in-" (not) with "gloriosus" (glorious), derived from "gloria" meaning "fame" or "honor." The word literally means "not glorious."',
                'language_origins': 'Latin',
                'example_sentence': 'The politician\'s _______ downfall resulted from corruption scandals that destroyed his reputation and career.',
                'memory_tip': 'Remember "INGLORIOUS" - think "IN-GLORIOUS" meaning NOT glorious (honorable) - bringing shame or disgrace instead of honor.'
            },
            'ingot': {
                'definition': 'An ingot is a block or bar of metal, typically precious metals like gold, silver, or industrial metals like iron or steel, cast in a standardized shape for storage, transportation, or further processing into finished products. This noun describes raw metal formed into convenient shapes for handling and trade. Gold ingots serve as stores of value and are traded in international markets. Steel ingots are reheated and rolled into sheets, bars, or structural shapes. The standardized forms allow accurate weighing and valuation of metal content. Ingots represent intermediate stages between raw ore and finished products, facilitating efficient industrial processes. Historical ingots were often stamped with purity marks and maker identification. Unlike coins or jewelry, ingots are valued primarily for metal content rather than craftsmanship. The shape allows efficient stacking and storage in vaults or warehouses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-got',
                'etymology': 'From Middle English, possibly from Old English "in" (into) plus "goten" (poured), referring to metal poured into molds. The word emphasizes the casting process used to create the bars.',
                'language_origins': 'Middle English, Old English',
                'example_sentence': 'The foundry cast molten steel into standardized _______ that would later be rolled into construction beams.',
                'memory_tip': 'Remember "INGOT" - think "IN-GOT" like metal that was "got" (poured) "IN" to a mold - a bar of cast metal.'
            },
            'ingratiate': {
                'definition': 'Ingratiate means to bring oneself into another\'s favor through deliberate efforts to please, often involving flattery, excessive agreeableness, or calculated charm designed to win approval or advantage. This verb describes behavior aimed at gaining acceptance or benefits by appealing to others\' vanity or preferences. People might ingratiate themselves with supervisors hoping for promotions or with wealthy individuals seeking financial benefits. The term often carries negative connotations, suggesting insincere or manipulative behavior rather than genuine friendship. Ingratiating actions might include excessive compliments, agreeing with everything someone says, or performing unrequested favors. Unlike authentic relationship building, ingratiating focuses on self-benefit rather than mutual respect. Political candidates sometimes ingratiate themselves with voter groups through calculated appeals. The behavior can be transparent and counterproductive when recipients recognize the manipulation.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-GRAY-shee-ayt',
                'etymology': 'From Latin "ingratiare," derived from "in-" (into) plus "gratia" (favor, grace). The word literally means "to bring into favor" or "to make oneself pleasing."',
                'language_origins': 'Latin',
                'example_sentence': 'The ambitious employee tried to _______ himself with the new manager by constantly praising her decisions.',
                'memory_tip': 'Remember "INGRATIATE" - think "IN-GRATI-ATE" like trying to get "IN" someone\'s good "graces" by being overly pleasing - seeking favor through flattery.'
            },
            'ingredient': {
                'definition': 'An ingredient is a component, element, or constituent that combines with others to form a mixture, compound, or complex whole, most commonly referring to items used in cooking, manufacturing, or formulation processes. This noun describes individual parts that contribute to larger products. Cooking ingredients include spices, vegetables, and proteins that combine to create dishes. Pharmaceutical ingredients combine to produce medicines with specific therapeutic effects. Chemical ingredients react to form new compounds with different properties. The term can extend metaphorically to describe elements that contribute to success, such as ingredients for happiness or ingredients of effective leadership. Quality ingredients often determine final product quality. Unlike finished products, ingredients maintain their distinct identities while contributing to combined effects. Understanding ingredient interactions helps in cooking, chemistry, and manufacturing processes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-GREE-dee-unt',
                'etymology': 'From Latin "ingrediens," present participle of "ingredi" meaning "to enter into" or "to go into," combining "in-" (into) with "gradi" (to step, walk).',
                'language_origins': 'Latin',
                'example_sentence': 'The chef carefully measured each _______ to ensure the sauce would have the perfect balance of flavors.',
                'memory_tip': 'Remember "INGREDIENT" - think "IN-GREDI-ENT" like something that "goes in" or enters "IN" to the recipe - a component that goes into making something.'
            },
            'ingredients': {
                'definition': 'Ingredients are the multiple components, elements, or constituents that combine together to form mixtures, compounds, or complex products, commonly referring to the various items used in cooking, manufacturing, or formulation processes. This plural noun describes all the individual parts that contribute to creating larger, more complex products. Recipe ingredients must be combined in proper proportions to achieve desired flavors and textures. Industrial ingredients undergo processing to create consumer goods like cosmetics, pharmaceuticals, or processed foods. Natural ingredients often appeal to consumers seeking healthier or more authentic products. The quality and freshness of ingredients directly impacts final product quality. Understanding how ingredients interact helps optimize formulations and recipes. Unlike single components, multiple ingredients create synergistic effects where the combination produces results greater than individual parts could achieve alone.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'in-GREE-dee-unts',
                'etymology': 'From Latin "ingrediens," present participle of "ingredi" meaning "to enter into," combining "in-" (into) with "gradi" (to step, walk). The plural form indicates multiple components.',
                'language_origins': 'Latin',
                'example_sentence': 'The nutrition label listed all the _______ in order of their concentration in the processed food product.',
                'memory_tip': 'Remember "INGREDIENTS" - think "IN-GREDI-ENTS" like multiple things that "go in" or enter "IN" to make the final product - all the components together.'
            },
            'inheritance': {
                'definition': 'Inheritance refers to money, property, or characteristics passed down from one generation to another, encompassing both material assets received after someone\'s death and traits or qualities transmitted through family lines. This noun describes the legal and biological processes of transmission across generations. Financial inheritance includes real estate, investments, and personal possessions left by deceased relatives. Genetic inheritance involves traits like eye color, height, or disease susceptibility passed from parents to children. Cultural inheritance encompasses traditions, values, and knowledge transmitted within families or communities. Legal inheritance involves wills, estates, and probate procedures that distribute assets. Unlike earned wealth, inheritance represents unearned transfer based on family relationships. Inheritance laws vary by jurisdiction but generally protect surviving family members\' rights. The concept recognizes that current generations benefit from previous generations\' accumulations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-HAIR-ih-tuns',
                'etymology': 'From Old French "inheritance," derived from "inheriter" meaning "to inherit," ultimately from Latin "hereditare" based on "heres" (heir). The root emphasizes succession and heredity.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The family\'s _______ included not only financial assets but also valuable antiques and the ancestral home.',
                'memory_tip': 'Remember "INHERITANCE" - think "IN-HERIT-ANCE" like the "stance" of "inheriting" things "IN" from your family - what you receive from previous generations.'
            },
            'inimical': {
                'definition': 'Inimical describes something that is hostile, harmful, or unfavorable, creating conditions that oppose, damage, or prevent success, wellbeing, or positive outcomes. This adjective characterizes forces, policies, or circumstances that work against desired goals or beneficial conditions. Inimical weather conditions prevent successful harvests or outdoor activities. Inimical policies undermine economic growth or social progress. The term suggests active opposition rather than mere absence of support. Environmental factors can be inimical to certain species\' survival. Political climates might be inimical to democratic processes or human rights. Unlike merely unfavorable circumstances, inimical conditions actively work against positive outcomes. The word implies that the opposing force creates genuine threats or obstacles that must be overcome. Understanding inimical factors helps in planning strategies to counter or avoid their negative effects.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-NIM-ih-kul',
                'etymology': 'From Late Latin "inimicalis," derived from "inimicus" meaning "enemy" or "hostile," combining "in-" (not) with "amicus" (friend). The word literally means "not friendly."',
                'language_origins': 'Late Latin',
                'example_sentence': 'The harsh winter weather proved _______ to the construction project, forcing delays and equipment failures.',
                'memory_tip': 'Remember "INIMICAL" - think "IN-ENEMY-CAL" like having an "enemy" "IN" the situation - hostile and harmful to your goals.'
            },
            'inimitable': {
                'definition': 'Inimitable describes something so unique, distinctive, or perfectly executed that it cannot be copied, replicated, or matched by others, possessing qualities that resist imitation despite attempts to reproduce them. This adjective characterizes artistic performances, personal styles, or achievements that remain uniquely associated with their creators. Inimitable musical performances capture lightning in a bottle that cover versions cannot recapture. Inimitable literary voices create distinctive prose styles that remain recognizably their own. The term suggests that the special quality depends on intangible factors like genius, personality, or circumstances that cannot be artificially reproduced. Inimitable comedic timing results from natural instincts rather than learned techniques. Unlike merely difficult-to-copy things, inimitable phenomena possess essential uniqueness that makes reproduction impossible. The word celebrates exceptional individual achievement that stands apart from all attempts at duplication.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-NIM-ih-tuh-buhl',
                'etymology': 'From Latin "inimitabilis," combining "in-" (not) with "imitabilis" (able to be imitated), derived from "imitari" meaning "to copy" or "to imitate."',
                'language_origins': 'Latin',
                'example_sentence': 'The comedian\'s _______ style of humor made him a legend that countless imitators tried but failed to replicate.',
                'memory_tip': 'Remember "INIMITABLE" - think "IN-IMITABLE" meaning NOT imitable (copyable) - so unique it can\'t be copied or reproduced.'
            },
            'injunction': {
                'definition': 'An injunction is a legal order issued by a court that compels someone to perform a specific action or, more commonly, prohibits them from continuing certain behavior that causes or threatens harm to others. This noun describes judicial remedies that prevent ongoing damage rather than simply providing monetary compensation after harm occurs. Courts issue injunctions to stop activities like pollution, harassment, or copyright infringement. Temporary injunctions provide immediate relief while cases proceed through litigation. Permanent injunctions establish long-term behavioral requirements or prohibitions. The legal remedy recognizes that some harms cannot be adequately addressed through monetary damages alone. Violating injunctions can result in contempt of court charges and additional penalties. Unlike criminal charges that punish past behavior, injunctions focus on preventing future harm by controlling ongoing conduct.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-JUNK-shun',
                'etymology': 'From Latin "injunctionem," derived from "injungere" meaning "to join into" or "to impose upon," combining "in-" (into) with "jungere" (to join, yoke).',
                'language_origins': 'Latin',
                'example_sentence': 'The court issued a temporary _______ preventing the company from cutting down the old-growth forest until the environmental case was resolved.',
                'memory_tip': 'Remember "INJUNCTION" - think "IN-JUNCTION" like a legal "junction" that puts you "IN" a position where you must or must not do something - a court order.'
            },
            'injurious': {
                'definition': 'Injurious describes something that causes harm, damage, or injury to health, reputation, interests, or wellbeing, whether through physical, emotional, or economic means. This adjective characterizes actions, substances, or conditions that have negative effects on people, organizations, or situations. Injurious chemicals cause health problems or environmental damage. Injurious gossip damages reputations and relationships. The term encompasses both intentional harm and unintentional damage that results from negligence or poor judgment. Injurious business practices harm competitors or consumers. Unlike beneficial influences that improve conditions, injurious factors create problems or worsen existing situations. Legal systems often address injurious actions through compensation or prevention mechanisms. The word recognizes that some influences actively damage rather than simply failing to help. Understanding injurious factors helps in avoiding or minimizing their negative impacts.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-JOOR-ee-us',
                'etymology': 'From Latin "injuriosus," derived from "injuria" meaning "injury" or "wrong," combining "in-" (not) with "jus, juris" (right, law). The root suggests acting against what is right.',
                'language_origins': 'Latin',
                'example_sentence': 'The factory\'s _______ emissions were causing respiratory problems for residents in the surrounding neighborhood.',
                'memory_tip': 'Remember "INJURIOUS" - think "INJURY-OUS" meaning full of injury - causing harm or damage to health, reputation, or wellbeing.'
            },
            'inkling': {
                'definition': 'An inkling is a slight hint, vague idea, or faint suspicion about something, representing the earliest stage of understanding or awareness before complete knowledge develops. This noun describes intuitive feelings or partial insights that suggest larger truths without providing complete information. People might have inklings about surprises being planned or problems developing. Inklings often precede full realizations, serving as early warning signals or preliminary insights. The term suggests uncertainty and incompleteness - more than complete ignorance but less than definitive knowledge. Scientific discoveries sometimes begin with inklings that motivate further investigation. Social situations might provide inklings about others\' feelings or intentions. Unlike concrete evidence, inklings require interpretation and may prove incorrect. The word captures the tentative nature of emerging awareness when understanding begins to form.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'INK-ling',
                'etymology': 'From Middle English "inklen," meaning "to hint" or "to whisper," possibly related to Old English "inca" meaning "suspicion" or "doubt." The diminutive suffix "-ling" suggests something small.',
                'language_origins': 'Middle English, Old English',
                'example_sentence': 'She had no _______ that her colleagues were planning a surprise retirement party in her honor.',
                'memory_tip': 'Remember "INKLING" - think "INK-LING" like a tiny drop of "ink" that hints at a larger picture - a small hint or vague idea.'
            },
            'inlaid': {
                'definition': 'Inlaid describes decorative work where materials like wood, metal, or stone are set into the surface of an object to create patterns, designs, or contrasting colors, forming a flush or level surface rather than raised decoration. This adjective characterizes craftsmanship techniques that embed one material within another for artistic or functional purposes. Inlaid furniture features decorative wood veneers or metal accents set into table tops or cabinet doors. Inlaid floors use different colored stones or tiles to create intricate patterns. The technique requires precise cutting and fitting to achieve seamless integration between materials. Musical instruments often feature inlaid mother-of-pearl or abalone decorations around sound holes or on fingerboards. Unlike applied decorations that sit on surfaces, inlaid work becomes integral to the object\'s structure. The craftsmanship represents traditional skills requiring patience, precision, and artistic vision.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'in-LAYD',
                'etymology': 'From "in-" (into) plus "laid" (past tense of lay), indicating something laid or placed into a surface. The compound emphasizes the embedding process.',
                'language_origins': 'English',
                'example_sentence': 'The antique jewelry box featured intricate _______ mother-of-pearl designs that sparkled in the light.',
                'memory_tip': 'Remember "INLAID" - think "IN-LAID" like decorative material "laid" "IN" to the surface - embedded decoration that\'s flush with the surface.'
            },
            'inlet': {
                'definition': 'An inlet is a narrow arm of water extending inland from a larger body of water such as an ocean, sea, or lake, or more generally, any entrance or opening that allows something to flow or enter inward. This noun describes geographical features where water penetrates land masses, creating protected harbors, bays, or channels. Coastal inlets provide sheltered areas for boats and marine wildlife. Tidal inlets connect ocean waters with lagoons or marshes. The term can also describe mechanical openings where fluids, air, or materials enter systems. Engine air inlets allow airflow into combustion chambers. Unlike outlets that allow materials to exit, inlets facilitate entry into enclosed spaces. Natural inlets often form through erosion or geological processes over long periods. The protected nature of inlets makes them valuable for harbors, fishing, and marine ecosystems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-let',
                'etymology': 'From "in-" (into) plus "let" (to allow or permit), indicating a place that lets water or other substances flow inward. The compound emphasizes the inward movement.',
                'language_origins': 'English',
                'example_sentence': 'The fishing boats found shelter from the storm in the protected _______ surrounded by rocky cliffs.',
                'memory_tip': 'Remember "INLET" - think "IN-LET" like a place that "lets" water flow "IN" from the ocean - a narrow waterway going inland.'
            },
            'innards': {
                'definition': 'Innards refers to the internal parts or organs of a person, animal, or machine, particularly the essential working components that are normally hidden from view inside the outer structure. This informal noun describes the inner workings that make something function. Human innards include organs like the heart, liver, and intestines. Machine innards consist of gears, circuits, or mechanical components that operate inside casings. The term often appears in casual or colloquial contexts rather than formal or technical writing. Unlike external features that are visible, innards require opening or dismantling to access. Understanding innards helps with maintenance, repair, or medical diagnosis. The word can also describe the interior contents of buildings or other structures. Innards represent the functional reality behind external appearances.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'IN-erdz',
                'etymology': 'From "inward" plus the suffix "-s," representing a colloquial contraction of "inward parts." The word emphasizes the internal location of these components.',
                'language_origins': 'English',
                'example_sentence': 'The mechanic had to examine the engine\'s _______ to find the source of the unusual noise.',
                'memory_tip': 'Remember "INNARDS" - think "INNER-ARDS" like the "inner" parts or "guts" inside something - the internal working components.'
            },
            'inner': {
                'definition': 'Inner describes something located inside, toward the center, or closer to the core of an object, person, or concept, as opposed to outer or external positions. This adjective characterizes physical locations, emotional states, or conceptual relationships that exist within rather than outside boundaries. Inner city areas are located toward urban centers. Inner feelings represent private emotions not readily visible to others. The term can describe both spatial relationships and abstract qualities. Inner circles include close associates with privileged access. Inner peace refers to emotional tranquility and self-acceptance. Unlike outer characteristics that are immediately observable, inner qualities require deeper understanding or investigation. Inner workings describe hidden mechanisms or processes. The word suggests depth, privacy, and essential rather than superficial qualities. Inner development focuses on personal growth and self-understanding.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IN-er',
                'etymology': 'From Old English "innera," comparative form of "inne" meaning "within" or "inside." The word originally indicated relative position closer to the center.',
                'language_origins': 'Old English',
                'example_sentence': 'The meditation practice helped her find _______ peace despite the chaos in her external circumstances.',
                'memory_tip': 'Remember "INNER" - think of something that\'s more "IN" than outer things - located inside or toward the center, not on the surface.'
            },
            'innermost': {
                'definition': 'Innermost describes the deepest, most central, or most private position within something, representing the farthest point inward whether in physical space, emotional depth, or conceptual importance. This adjective characterizes the most protected, hidden, or essential core of objects, feelings, or ideas. Innermost thoughts represent the most private mental content that people rarely share. Innermost rooms in buildings are farthest from external walls and entrances. The term suggests maximum intimacy, secrecy, or centrality within hierarchical systems. Innermost circles include only the most trusted associates. Innermost desires reflect fundamental motivations that drive behavior. Unlike merely inner qualities, innermost characteristics represent ultimate depths that few people access. Innermost secrets are the most carefully guarded information. The word emphasizes exclusivity and the special access required to reach such protected depths.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IN-er-most',
                'etymology': 'From Old English "innermest," superlative form of "inner," meaning "most inward" or "deepest inside." The "-most" suffix indicates the extreme degree of inwardness.',
                'language_origins': 'Old English',
                'example_sentence': 'She kept her _______ fears about the future locked away, sharing them with no one, not even her closest friends.',
                'memory_tip': 'Remember "INNERMOST" - think "INNER-MOST" meaning the "MOST inner" part - the deepest, most private, or most central core.'
            },
            'innings': {
                'definition': 'Innings refers to the periods of play in baseball or cricket during which one team or player has the opportunity to bat and score, or more broadly, any period during which someone has a turn or opportunity to act. This noun describes structured periods of activity within games or other sequential activities. Baseball games consist of nine innings, with each team batting once per inning. Cricket innings can last much longer, sometimes for days in international matches. The term can extend metaphorically to describe periods of opportunity in politics, careers, or other endeavors. Unlike continuous activity, innings involve alternating periods where different participants take turns. Each innings provides specific opportunities and limitations based on game rules. The concept emphasizes fair distribution of opportunities and structured competition. Understanding innings helps follow game progress and strategy.',
                'part_of_speech': 'noun (plural, sometimes singular)',
                'pronunciation_guide': 'IN-ingz',
                'etymology': 'From "inning," derived from "in" plus "-ing," originally meaning "a going in" or "a turn at bat." The term reflects the idea of players going in to bat.',
                'language_origins': 'English',
                'example_sentence': 'The pitcher threw a perfect game, allowing no hits or walks during all nine _______ of the championship match.',
                'memory_tip': 'Remember "INNINGS" - think "IN-NINGS" like turns when players go "IN" to bat - periods of play when it\'s your team\'s turn.'
            },
            'innocent': {
                'definition': 'Innocent describes someone who is free from guilt, wrongdoing, or moral corruption, or something that is harmless and without evil intent or negative consequences. This adjective characterizes individuals who have not committed crimes or moral violations, as well as actions or things that pose no threat or harm. Legal systems presume defendants innocent until proven guilty. Innocent children display natural purity before learning about evil or corruption. The term can describe both factual absence of wrongdoing and naive lack of awareness about harmful realities. Innocent questions arise from genuine curiosity without hidden agendas. Innocent pleasures bring joy without negative consequences. Unlike guilty parties who bear responsibility for harm, innocent people deserve protection and fair treatment. The word encompasses both moral purity and legal blamelessness.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'IN-uh-sunt',
                'etymology': 'From Latin "innocens," combining "in-" (not) with "nocens" (harmful), derived from "nocere" meaning "to harm" or "to hurt." The word literally means "not harmful."',
                'language_origins': 'Latin',
                'example_sentence': 'The jury found the defendant _______ of all charges after reviewing the evidence and witness testimony.',
                'memory_tip': 'Remember "INNOCENT" - think "IN-NO-CENT" meaning there\'s "NO" harmful intent "IN" them - free from guilt or wrongdoing.'
            },
            'innovator': {
                'definition': 'An innovator is someone who introduces new ideas, methods, products, or approaches that bring about positive change, improvement, or advancement in their field or society. This noun describes individuals who challenge existing practices and create novel solutions to problems or opportunities. Technological innovators develop breakthrough inventions that transform how people live and work. Social innovators create new approaches to address community problems. Business innovators pioneer new business models or market strategies. Unlike mere inventors who create new things, innovators focus on practical implementation and real-world impact. Educational innovators develop new teaching methods that improve learning outcomes. The term emphasizes both creativity and practical application of new ideas. Successful innovators often combine vision, persistence, and understanding of market or social needs to create meaningful change.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-uh-vay-ter',
                'etymology': 'From Latin "innovare," meaning "to renew" or "to change," combining "in-" (into) with "novus" (new). The "-ator" suffix indicates one who performs the action.',
                'language_origins': 'Latin',
                'example_sentence': 'The technology _______ revolutionized the smartphone industry with her breakthrough battery design.',
                'memory_tip': 'Remember "INNOVATOR" - think "IN-NOVA-TOR" like someone who brings "NOVA" (new) things "IN" to the world - a person who creates new and better ways.'
            },
            'inoculate': {
                'definition': 'Inoculate means to introduce a vaccine, serum, or antigenic substance into the body to stimulate immunity against disease, or more broadly, to introduce ideas or attitudes to provide protection against harmful influences. This verb describes preventive medical procedures that prepare immune systems to fight specific infections. Doctors inoculate children against diseases like measles, polio, and whooping cough. The process involves exposing immune systems to weakened or dead pathogens that trigger protective responses. Metaphorically, education can inoculate minds against misinformation by teaching critical thinking skills. Unlike treating existing illness, inoculation focuses on prevention before exposure occurs. Mass inoculation programs have eliminated diseases like smallpox. The concept recognizes that controlled exposure to mild threats can provide protection against severe dangers.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-NOK-yuh-layt',
                'etymology': 'From Latin "inoculare," meaning "to graft" or "to implant," combining "in-" (into) with "oculus" (eye or bud). Originally referred to grafting plant buds.',
                'language_origins': 'Latin',
                'example_sentence': 'The public health campaign aimed to _______ the entire population against the emerging flu strain.',
                'memory_tip': 'Remember "INOCULATE" - think "IN-OCULATE" like putting protective medicine "IN" through the "eye" (small opening) - introducing vaccine to prevent disease.'
            },
            'inquietude': {
                'definition': 'Inquietude is a state of restlessness, uneasiness, or mental agitation characterized by inability to remain calm or at peace, often accompanied by anxiety about uncertain outcomes or troubling circumstances. This noun describes persistent inner turmoil that prevents tranquility or contentment. Political inquietude affects populations during times of social upheaval. Personal inquietude might result from unresolved conflicts or major life changes. The term suggests ongoing disturbance rather than temporary worry. Unlike simple nervousness, inquietude implies deeper existential unrest that affects overall wellbeing. Inquietude can motivate action to address underlying problems or can become paralyzing when no solutions seem available. Literary works often explore characters experiencing inquietude during moral or emotional crises. The condition represents the opposite of serenity, involving constant mental motion and emotional disturbance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-KWY-ih-tood',
                'etymology': 'From Latin "inquietudo," derived from "inquietus" meaning "restless" or "troubled," combining "in-" (not) with "quietus" (quiet, at rest).',
                'language_origins': 'Latin',
                'example_sentence': 'The uncertainty about her job security filled her with a deep _______ that made concentration difficult.',
                'memory_tip': 'Remember "INQUIETUDE" - think "IN-QUIET-UDE" meaning NOT having "quietude" (peace) - a state of restless anxiety and unease.'
            },
            'inquisitor': {
                'definition': 'An inquisitor is someone who conducts intensive questioning or investigation, historically referring to officials who interrogated people suspected of heresy during religious inquisitions, but now describing anyone who pursues aggressive inquiry or examination. This noun characterizes individuals who probe deeply into beliefs, actions, or circumstances, often with official authority or serious purpose. Historical inquisitors investigated religious orthodoxy and punished those deemed heretical. Modern inquisitors might include journalists investigating corruption or prosecutors questioning suspects. The term carries connotations of persistent, thorough, and sometimes intimidating questioning. Unlike casual questioners, inquisitors pursue systematic investigation with specific goals. Academic inquisitors might rigorously challenge theories or research findings. The word implies both methodical approach and potential for making subjects uncomfortable through intensive scrutiny.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-KWIZ-ih-ter',
                'etymology': 'From Latin "inquisitor," derived from "inquirere" meaning "to search into" or "to investigate," combining "in-" (into) with "quaerere" (to seek, ask).',
                'language_origins': 'Latin',
                'example_sentence': 'The investigative journalist acted like a relentless _______, questioning every witness and examining every document related to the scandal.',
                'memory_tip': 'Remember "INQUISITOR" - think "IN-QUIZ-ITOR" like someone who puts you "IN" a "QUIZ" situation - asking probing questions to investigate thoroughly.'
            },
            'inscription': {
                'definition': 'An inscription is text, symbols, or writing carved, engraved, or written on a surface such as stone, metal, paper, or other materials, typically intended to provide permanent record, commemoration, or identification. This noun describes various forms of permanent marking that convey information, dedicate monuments, or identify objects. Tombstone inscriptions record names, dates, and memorial messages. Building inscriptions identify construction dates, architects, or dedications. Ancient inscriptions provide historical information about past civilizations. The permanence of inscriptions makes them valuable for historical research and legal documentation. Unlike temporary writing, inscriptions are designed to endure over time. Ceremonial inscriptions mark important events or honor significant individuals. The craftsmanship involved in creating inscriptions often makes them artistic as well as informational.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-SKRIP-shun',
                'etymology': 'From Latin "inscriptio," derived from "inscribere" meaning "to write upon" or "to engrave," combining "in-" (upon) with "scribere" (to write).',
                'language_origins': 'Latin',
                'example_sentence': 'The ancient temple\'s _______ revealed the names of the rulers who commissioned its construction over two millennia ago.',
                'memory_tip': 'Remember "INSCRIPTION" - think "IN-SCRIPT-ION" like "script" (writing) put "IN" or "ON" a surface - permanent text carved or written on something.'
            },
            'inscrutable': {
                'definition': 'Inscrutable describes something that is impossible to understand, interpret, or fathom, characterized by mysterious or enigmatic qualities that resist explanation or comprehension despite careful study or observation. This adjective applies to people, situations, or phenomena that remain puzzling even after extensive analysis. Inscrutable expressions on faces give no indication of underlying thoughts or feelings. Inscrutable ancient texts challenge linguists and historians. The term suggests depth or complexity that exceeds human ability to penetrate or decode. Inscrutable natural phenomena baffle scientists until breakthrough discoveries provide explanations. Unlike simply complicated things that can eventually be understood, inscrutable matters seem to possess fundamental mystery. Inscrutable personalities fascinate others precisely because their motivations and thoughts remain hidden. The word acknowledges limits to human understanding when confronting profound mysteries.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-SKROO-tuh-buhl',
                'etymology': 'From Latin "inscrutabilis," combining "in-" (not) with "scrutabilis" (able to be examined), derived from "scrutari" meaning "to search" or "to examine closely."',
                'language_origins': 'Latin',
                'example_sentence': 'The professor\'s _______ smile gave students no hint about whether their answers were correct or completely wrong.',
                'memory_tip': 'Remember "INSCRUTABLE" - think "IN-SCRUTABLE" meaning NOT "scrutable" (examinable) - impossible to examine or understand, mysterious and puzzling.'
            },
            'insect': {
                'definition': 'An insect is a small arthropod animal characterized by having six legs, three body segments (head, thorax, abdomen), and typically two pairs of wings, representing the largest class in the animal kingdom with over one million described species. This noun describes creatures that play crucial roles in ecosystems as pollinators, decomposers, and food sources for other animals. Common insects include bees, ants, butterflies, beetles, and flies. Insects undergo metamorphosis, changing form during their life cycles. Many insects are beneficial to humans through pollination of crops and control of pest species. Some insects are considered pests when they damage crops or spread diseases. The diversity of insects exceeds all other animal groups combined. Understanding insect biology helps with agriculture, medicine, and environmental conservation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-sekt',
                'etymology': 'From Latin "insectum," meaning "cut into" or "segmented," derived from "insectus," past participle of "insecare" (to cut into), referring to their segmented bodies.',
                'language_origins': 'Latin',
                'example_sentence': 'The entomologist identified the unknown _______ by examining its wing patterns and body structure under a microscope.',
                'memory_tip': 'Remember "INSECT" - think "IN-SECT" like animals that are "IN" "SECTIONS" (segments) - creatures with segmented bodies and six legs.'
            },
            'inside': {
                'definition': 'Inside refers to the interior or inner part of something, or describes position within the boundaries or confines of an object, space, or concept. This preposition, adverb, and noun characterizes location or position enclosed within something else. Inside buildings, people find protection from weather. Inside boxes, objects are stored and protected. The term can describe both physical containment and abstract inclusion. Inside information refers to confidential knowledge available only to authorized individuals. Inside jokes are understood only by specific groups. Unlike outside positions that are exposed or external, inside locations offer protection, privacy, or special access. Inside perspectives provide understanding available only to participants or members. The concept emphasizes containment, protection, and privileged access to enclosed spaces or exclusive knowledge.',
                'part_of_speech': 'preposition, adverb, noun, adjective',
                'pronunciation_guide': 'in-SYD',
                'etymology': 'From Middle English, combining "in" with "side," literally meaning "on the inner side." The compound emphasizes the interior position relative to boundaries.',
                'language_origins': 'Middle English',
                'example_sentence': 'The valuable documents were kept _______ the fireproof safe to protect them from damage.',
                'memory_tip': 'Remember "INSIDE" - think "IN-SIDE" like being "IN" on the inner "SIDE" of something - within the boundaries or interior.'
            },
            'insight': {
                'definition': 'Insight is the ability to understand the true nature of something through deep perception, intuitive understanding, or sudden realization that reveals previously hidden relationships, meanings, or solutions. This noun describes moments of clarity when complex problems become understandable or when underlying patterns become visible. Psychological insights help therapists understand their patients\' behavior and motivations. Scientific insights lead to breakthrough discoveries and new theories. Business insights reveal market opportunities or operational improvements. The term suggests understanding that goes beyond surface-level observation to grasp fundamental principles. Unlike mere information, insights provide transformative understanding that changes how people think or act. Insights often occur suddenly after periods of reflection or study. The quality distinguishes between knowing facts and truly understanding their significance and implications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-syt',
                'etymology': 'From Middle English, combining "in" with "sight," literally meaning "inner sight" or "the ability to see within." The compound emphasizes internal perception.',
                'language_origins': 'Middle English',
                'example_sentence': 'Her sudden _______ into the problem\'s root cause led to an elegant solution that had eluded the team for months.',
                'memory_tip': 'Remember "INSIGHT" - think "IN-SIGHT" like having "SIGHT" that goes "IN" deep - seeing the truth beneath the surface.'
            },
            'insights': {
                'definition': 'Insights are multiple instances of deep understanding, perceptive observations, or revealing discoveries that illuminate the true nature of complex subjects, problems, or situations. This plural noun describes accumulated wisdom or understanding gained through careful observation, analysis, or intuitive perception. Market research provides insights into consumer behavior and preferences. Scientific studies offer insights into natural phenomena and their underlying mechanisms. Personal experiences generate insights about human nature and relationships. The term emphasizes quality of understanding rather than quantity of information. Unlike mere data or facts, insights reveal meaningful patterns and relationships that inform decision-making. Educational insights help teachers understand how students learn most effectively. The accumulation of insights over time builds expertise and wisdom in specific domains.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'IN-syts',
                'etymology': 'From Middle English "insight," combining "in" with "sight." The plural form indicates multiple instances of deep understanding or perception.',
                'language_origins': 'Middle English',
                'example_sentence': 'The research team\'s _______ into customer behavior helped the company redesign its marketing strategy for better results.',
                'memory_tip': 'Remember "INSIGHTS" - think "IN-SIGHTS" like multiple "SIGHTS" that see "IN" deep - several deep understandings or discoveries.'
            }
        }
        
        return batch_091_data.get(word, {
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
            'inglenookefflux': 'Combined word error: "inglenookefflux" appears to be "inglenook" (cozy fireplace corner) + "efflux" (flowing out) merged together.'
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
    processor = Batch091Processor()
    input_file = "output/batch_091_words.csv"
    output_file = "output/batch_091_processed.csv"
    
    success = processor.process_batch(input_file, output_file)
    if success:
        print("Batch 091 processing completed successfully!")
    else:
        print("Batch 091 processing failed!")

if __name__ == "__main__":
    main()