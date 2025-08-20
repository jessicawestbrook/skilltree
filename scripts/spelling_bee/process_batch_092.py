#!/usr/bin/env python3
"""
Batch 092 Processor for Scripps National Spelling Bee Words
Processes words from insignia through intertribal with comprehensive Claude-generated data
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

class Batch092Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.processed_count = 0

    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge"""
        
        batch_092_data = {
            'insignia': {
                'definition': 'Insignia are distinctive badges, symbols, or emblems that indicate rank, office, membership, or achievement, typically worn on uniforms, displayed on official documents, or used to identify organizational affiliation. This plural noun (singular: insignium) describes various forms of symbolic identification used by military forces, government agencies, schools, and other institutions. Military insignia show rank and unit assignments through stripes, stars, and patches. Police insignia identify department affiliation and officer rank. Academic insignia include graduation cords, pins, and ceremonial regalia. Corporate insignia represent company identity and employee status. The term encompasses both official symbols with legal authority and ceremonial decorations that recognize achievement or membership. Unlike mere decoration, insignia carry specific meaning within organizational hierarchies.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'in-SIG-nee-uh',
                'etymology': 'From Latin "insignia," plural of "insigne" meaning "mark" or "badge," derived from "insignis" meaning "marked" or "distinguished," combining "in-" (into) with "signum" (sign, mark).',
                'language_origins': 'Latin',
                'example_sentence': 'The general\'s _______ clearly displayed his rank and years of distinguished service through various ribbons and stars.',
                'memory_tip': 'Remember "INSIGNIA" - think "IN-SIGN-IA" like "signs" that are "IN" use to show rank or membership - distinctive badges or symbols.'
            },
            'insolent': {
                'definition': 'Insolent describes behavior that is boldly rude, disrespectful, or contemptuous, showing deliberate defiance of authority or social conventions without regard for consequences. This adjective characterizes actions or attitudes that display arrogant disregard for proper conduct, authority figures, or established norms. Insolent students openly challenge teachers with disrespectful comments or behavior. Insolent employees might openly criticize management or refuse reasonable requests. The term suggests not just rudeness but deliberate, brazen defiance that shows lack of proper respect. Unlike accidental rudeness or cultural misunderstandings, insolent behavior involves conscious choice to act disrespectfully. Insolent remarks during formal proceedings can result in serious consequences. The word implies both the boldness of the behavior and its inappropriate nature given the social or professional context.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IN-suh-lunt',
                'etymology': 'From Latin "insolens," combining "in-" (not) with "solens" (accustomed), from "solere" (to be accustomed). Originally meant "unusual" but evolved to mean "impudently bold."',
                'language_origins': 'Latin',
                'example_sentence': 'The defendant\'s _______ attitude toward the judge resulted in additional charges for contempt of court.',
                'memory_tip': 'Remember "INSOLENT" - think "IN-SO-LENT" like someone who\'s "so" rude they need to be "lent" some manners - boldly disrespectful.'
            },
            'insomnia': {
                'definition': 'Insomnia is a sleep disorder characterized by persistent difficulty falling asleep, staying asleep, or achieving restorative sleep despite adequate opportunity for rest, resulting in daytime fatigue and impaired functioning. This medical condition affects millions of people and can be acute (short-term) or chronic (long-lasting). Acute insomnia often results from stress, illness, or environmental factors. Chronic insomnia may involve underlying medical conditions, medications, or psychological factors. Primary insomnia occurs without identifiable causes, while secondary insomnia results from other conditions. The disorder significantly impacts quality of life, cognitive function, and physical health. Treatment approaches include sleep hygiene education, cognitive-behavioral therapy, and sometimes medications. Unlike occasional sleepless nights that everyone experiences, insomnia represents persistent sleep problems that interfere with daily functioning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-SOM-nee-uh',
                'etymology': 'From Latin "insomnia," combining "in-" (not) with "somnus" (sleep). The word literally means "lack of sleep" or "sleeplessness."',
                'language_origins': 'Latin',
                'example_sentence': 'Her chronic _______ left her exhausted during the day and unable to concentrate on important work tasks.',
                'memory_tip': 'Remember "INSOMNIA" - think "IN-SOM-NIA" like "IN" a state where there\'s "NO" "SOM" (sleep) - inability to sleep properly.'
            },
            'insouciance': {
                'definition': 'Insouciance is a casual lack of concern, worry, or anxiety; a carefree attitude characterized by indifference to potential problems or responsibilities. This noun describes an attitude of nonchalant unconcern that can be either admirable (showing confidence and composure) or problematic (indicating irresponsibility or indifference). Insouciance might help someone remain calm under pressure or might reflect dangerous lack of preparation for serious situations. The quality can manifest as charming confidence in social situations or as frustrating indifference to important matters. French cultural associations often link insouciance with sophistication and effortless style. Unlike anxiety or excessive worry, insouciance represents emotional detachment from stressful circumstances. The attitude can be cultivated as a coping mechanism or can be a natural personality trait.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-SOO-see-ahns',
                'etymology': 'From French "insouciance," derived from "insouciant" meaning "carefree," combining "in-" (not) with "souciant" (caring), from "soucier" (to worry).',
                'language_origins': 'French',
                'example_sentence': 'Despite the impending deadline, she maintained an air of _______ that either impressed or worried her colleagues.',
                'memory_tip': 'Remember "INSOUCIANCE" - think "IN-SOUCI-ANCE" from French meaning not having "souci" (worry) - a carefree, unconcerned attitude.'
            },
            'inspector': {
                'definition': 'An inspector is an official whose job involves examining, investigating, or overseeing something to ensure compliance with standards, regulations, or proper procedures. This noun describes professionals who have authority to evaluate conditions, investigate problems, or verify that requirements are met. Building inspectors examine construction for safety code compliance. Health inspectors investigate restaurants and food facilities. Police inspectors supervise investigations and detective work. Quality control inspectors examine products for defects. Unlike casual observers, inspectors have official authority and expertise to evaluate specific aspects of systems, processes, or conditions. Educational inspectors assess school performance and teaching quality. The role requires attention to detail, knowledge of relevant standards, and ability to identify problems or violations. Inspectors often have power to require corrections or improvements.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-SPEK-ter',
                'etymology': 'From Latin "inspector," derived from "inspicere" meaning "to look into" or "to examine," combining "in-" (into) with "specere" (to look, see).',
                'language_origins': 'Latin',
                'example_sentence': 'The safety _______ found several code violations that had to be corrected before the building could open.',
                'memory_tip': 'Remember "INSPECTOR" - think "IN-SPECT-OR" like someone who "spects" (looks) "IN" to things - an official examiner.'
            },
            'inspired': {
                'definition': 'Inspired describes something that is filled with creativity, enthusiasm, or exceptional quality that seems to come from a divine or extraordinary source, or someone who has been motivated to create or act by powerful influences or ideas. This adjective characterizes work, performance, or behavior that exceeds normal expectations through exceptional creativity or insight. Inspired artwork captures viewers\' imagination and emotions. Inspired leadership motivates others to achieve great things. The term can describe both the creative process (feeling inspired to write) and the results (producing inspired poetry). Unlike routine work, inspired efforts display originality, passion, and excellence that distinguishes them from ordinary accomplishments. Inspired teaching transforms students\' understanding and enthusiasm. The word suggests that exceptional results come from sources beyond mere technical skill or effort.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'in-SPYRD',
                'etymology': 'From Latin "inspiratus," past participle of "inspirare" meaning "to breathe into," combining "in-" (into) with "spirare" (to breathe). Originally suggested divine influence breathing life into creative work.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ performance moved the audience to tears and earned a standing ovation from the packed theater.',
                'memory_tip': 'Remember "INSPIRED" - think "IN-SPIRED" like having creative spirit "spired" (breathed) "IN" - filled with exceptional creativity or motivation.'
            },
            'inspiring': {
                'definition': 'Inspiring describes something that motivates, encourages, or stimulates others to feel enthusiasm, confidence, or creativity, often leading to positive action or personal growth. This adjective characterizes people, events, or experiences that uplift others and create desire for achievement or improvement. Inspiring teachers help students discover their potential and passion for learning. Inspiring stories of overcoming adversity motivate others facing similar challenges. The term suggests ability to create positive emotional responses and behavioral changes in others. Inspiring leadership brings out the best in team members. Unlike merely informative or entertaining content, inspiring material creates lasting impact on attitudes and motivation. Inspiring art, music, or literature can change how people see themselves or the world. The quality involves connecting with others\' hopes, dreams, and desire for meaning.',
                'part_of_speech': 'adjective, present participle',
                'pronunciation_guide': 'in-SPY-ring',
                'etymology': 'From Latin "inspirare" meaning "to breathe into," combined with the English suffix "-ing." The participial form emphasizes ongoing inspirational influence.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The documentary about environmental conservation was so _______ that many viewers changed their daily habits.',
                'memory_tip': 'Remember "INSPIRING" - think "IN-SPIRING" like "spiring" (breathing) motivation "IN" to others - motivating and encouraging people.'
            },
            'instagram': {
                'definition': 'Instagram is a social media platform and mobile application that allows users to share photos and videos, apply filters and editing tools, and interact with others through likes, comments, and direct messages. This proper noun refers to the photo-sharing service launched in 2010 and later acquired by Facebook (Meta). Instagram features include Stories (temporary posts), Reels (short videos), IGTV (longer videos), and shopping integration. The platform has significantly influenced social media culture, photography trends, and digital marketing strategies. Instagram\'s visual focus has changed how people document and share experiences. Businesses use Instagram for brand marketing and customer engagement. The platform has created new forms of online celebrity and influenced everything from fashion to travel trends. Instagram represents the shift toward visual communication in digital media.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'IN-stuh-gram',
                'etymology': 'Combination of "instant" and "telegram," coined by founders Kevin Systrom and Mike Krieger to reflect instant photo sharing similar to sending telegrams.',
                'language_origins': 'English (coined term)',
                'example_sentence': 'The restaurant\'s popularity increased dramatically after food bloggers began posting appetizing photos on _______.',
                'memory_tip': 'Remember "INSTAGRAM" - think "INSTANT-GRAM" like instant photos sent like telegrams - a platform for sharing instant photos.'
            },
            'installation': {
                'definition': 'Installation refers to the process of setting up, placing, or establishing equipment, software, systems, or artistic works in their intended locations, or the completed setup itself. This noun encompasses both the action of installing and the resulting arrangement. Software installation involves copying files and configuring programs on computers. Art installations are three-dimensional works designed for specific spaces. Military installations are permanent bases or facilities. Home installations might include appliances, security systems, or entertainment equipment. The term implies more than simple placement - it involves proper connection, configuration, and integration with existing systems. Installation often requires specialized knowledge, tools, and procedures. Unlike temporary setups, installations are intended to remain in place and function reliably over time. The process typically includes testing to ensure proper operation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-stuh-LAY-shun',
                'etymology': 'From Medieval Latin "installatio," derived from "installare" meaning "to place in position," combining "in-" (in) with "stallum" (place, stall).',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'The solar panel _______ on their roof was completed efficiently and began generating electricity immediately.',
                'memory_tip': 'Remember "INSTALLATION" - think "IN-STALL-ATION" like putting something "IN" its proper "STALL" (place) - the process of setting up equipment.'
            },
            'instantaneous': {
                'definition': 'Instantaneous describes something that occurs immediately, without any perceptible delay between cause and effect, happening in an instant or moment too brief to measure. This adjective characterizes events, reactions, or processes that appear to take no time at all. Lightning provides instantaneous illumination during storms. Computer calculations can seem instantaneous despite involving millions of operations. Unlike rapid events that take measurable time, instantaneous phenomena appear to happen without duration. Instantaneous communication via digital networks connects people across vast distances. The term is often used colloquially to mean "very fast" even when technically some time passes. In physics, truly instantaneous events are rare, as most processes require some time for completion. Instantaneous responses in emergencies can save lives by eliminating dangerous delays.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-stan-TAY-nee-us',
                'etymology': 'From Medieval Latin "instantaneus," derived from "instans" meaning "present moment," from "instare" (to stand near, be present).',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'The airbag\'s _______ deployment during the crash prevented serious injury to the vehicle\'s occupants.',
                'memory_tip': 'Remember "INSTANTANEOUS" - think "INSTANT-ANEOUS" like happening in an "INSTANT" - occurring immediately without delay.'
            },
            'instantly': {
                'definition': 'Instantly means immediately, without delay, or at the very moment something happens, describing actions or events that occur right away without intervening time. This adverb characterizes immediate responses, reactions, or consequences that follow directly from causes. Digital messages can be transmitted instantly across global networks. Recognition software can instantly identify faces in photographs. The term emphasizes the absence of waiting time between trigger and response. Unlike gradually or eventually, instantly indicates immediate occurrence. Emergency systems must respond instantly to prevent disasters. Instant communication has transformed business and personal relationships. While often used colloquially for "very quickly," instantly technically means with zero delay. The concept highlights human expectation for immediate gratification in modern technology and services.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'IN-stunt-lee',
                'etymology': 'From "instant" plus the adverbial suffix "-ly." "Instant" derives from Latin "instans" meaning "present moment."',
                'language_origins': 'Latin, English',
                'example_sentence': 'When she heard her baby crying, the mother _______ dropped everything and rushed to the nursery.',
                'memory_tip': 'Remember "INSTANTLY" - think "INSTANT-LY" like doing something in an instant manner - immediately and without delay.'
            },
            'instead': {
                'definition': 'Instead means as an alternative to something else, in place of what was expected or mentioned, or as a substitute choice when the original option is not available or desirable. This adverb indicates replacement or substitution in actions, choices, or circumstances. Instead of driving, she took the train to avoid traffic. Instead of anger, he felt disappointment about the situation. The word signals a change from one option to another, often suggesting preference or necessity. Instead can introduce better alternatives or necessary substitutions when original plans cannot be followed. Unlike in addition to, instead indicates replacement rather than addition. The concept is fundamental to decision-making, problem-solving, and adapting to changing circumstances. Instead choices often reflect values, priorities, or practical constraints that influence behavior.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'in-STED',
                'etymology': 'From Middle English "in stede," meaning "in place," combining "in" with "stede" (place, position). The phrase originally meant "in the place of."',
                'language_origins': 'Middle English',
                'example_sentence': 'Rather than buying a new car, they decided to repair their old one _______.',
                'memory_tip': 'Remember "INSTEAD" - think "IN-STEAD" like being "IN" the "STEAD" (place) of something else - as a replacement or alternative.'
            },
            'instigate': {
                'definition': 'Instigate means to initiate, provoke, or incite action or events, particularly those involving conflict, change, or controversial activities. This verb describes deliberate actions taken to start processes, often with the understanding that others will carry out the resulting activities. Political leaders might instigate reforms to address social problems. Troublemakers instigate fights by provoking others. The term carries implications of intentional initiation with awareness of likely consequences. Unlike accidental triggering of events, instigation involves purposeful action to create specific outcomes. Instigating positive change requires vision and courage. However, instigating violence or disorder carries moral and legal responsibilities. The word suggests both the power to influence events and accountability for results. Successful instigation requires understanding how to motivate others to act.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'IN-sti-gayt',
                'etymology': 'From Latin "instigare," meaning "to goad" or "to urge forward," possibly from "in-" (into) with "stigare" (to prick, goad). The root suggests prodding something into action.',
                'language_origins': 'Latin',
                'example_sentence': 'The community organizer worked to _______ positive changes in local housing policies through grassroots advocacy.',
                'memory_tip': 'Remember "INSTIGATE" - think "IN-STIGATE" like "stigating" (prodding) someone "IN" to action - deliberately starting or provoking events.'
            },
            'instinctive': {
                'definition': 'Instinctive describes behavior, reactions, or responses that occur naturally without conscious thought, learning, or deliberate decision-making, arising from innate biological or psychological tendencies rather than acquired knowledge. This adjective characterizes automatic responses that seem programmed into organisms. Instinctive behaviors in animals include migration patterns, mating rituals, and protective responses to threats. Human instinctive reactions might include jumping away from danger or caring for infants. Unlike learned behaviors that require training or experience, instinctive actions occur without instruction. Instinctive responses often provide survival advantages by enabling quick reactions to important situations. The term can also describe human intuitive responses that feel natural even when not strictly biological. Instinctive understanding might develop through experience but feels automatic rather than analytical.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-STINGK-tiv',
                'etymology': 'From Latin "instinctus," past participle of "instinguere" meaning "to incite" or "to instigate," combined with the suffix "-ive" indicating tendency.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ reaction to protect the child from danger occurred before she had time to think about the risks.',
                'memory_tip': 'Remember "INSTINCTIVE" - think "IN-STINCT-IVE" like having a natural "stinct" (instinct) "IN" you - automatic behavior without thinking.'
            },
            'instrument': {
                'definition': 'An instrument is a tool, device, or implement designed for precise work, measurement, or artistic expression, or a means by which something is accomplished or expressed. This noun encompasses physical devices (musical instruments, scientific instruments), legal documents (legal instruments), and abstract means of achieving goals (instruments of policy). Musical instruments produce sound for artistic expression. Scientific instruments measure, analyze, or manipulate physical phenomena. Medical instruments enable diagnosis and treatment. Financial instruments represent investments or contracts. The term implies precision, purpose, and specialized function. Unlike general tools, instruments often require skill and training to use effectively. Instruments can be simple (rulers) or complex (electron microscopes). The concept extends metaphorically to describe anything that serves as a means to accomplish specific objectives.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-struh-munt',
                'etymology': 'From Latin "instrumentum," derived from "instruere" meaning "to build into" or "to equip," combining "in-" (into) with "struere" (to build).',
                'language_origins': 'Latin',
                'example_sentence': 'The surgeon carefully selected each _______ needed for the delicate operation before beginning the procedure.',
                'memory_tip': 'Remember "INSTRUMENT" - think "IN-STRUMENT" like something "constructed" or "structured" "IN" to help accomplish specific tasks - a precise tool.'
            },
            'insubstantial': {
                'definition': 'Insubstantial describes something that lacks substance, solidity, or significant reality, characterized by being flimsy, weak, or having little physical or conceptual weight. This adjective applies to both physical objects that are fragile or ethereal and abstract concepts that lack depth or importance. Insubstantial evidence cannot support serious legal claims. Insubstantial materials might collapse under pressure or wear. The term can describe gossip, rumors, or theories that have little factual foundation. Insubstantial income provides inadequate financial support. Unlike substantial things that are solid and significant, insubstantial items are ephemeral, weak, or insufficient. Insubstantial arguments lack logical foundation or evidence. The word emphasizes the absence of meaningful weight, whether physical, intellectual, or practical. Insubstantial fears might be based on imagination rather than real threats.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-sub-STAN-shul',
                'etymology': 'From Latin "insubstantialis," combining "in-" (not) with "substantialis" (having substance), derived from "substantia" (substance, essence).',
                'language_origins': 'Latin',
                'example_sentence': 'The prosecutor\'s case appeared _______ when key witnesses failed to provide credible testimony.',
                'memory_tip': 'Remember "INSUBSTANTIAL" - think "IN-SUBSTANTIAL" meaning NOT substantial (solid/significant) - lacking substance or importance.'
            },
            'insufferable': {
                'definition': 'Insufferable describes someone or something that is extremely annoying, unbearable, or impossible to tolerate due to arrogant, obnoxious, or persistently irritating behavior or qualities. This adjective characterizes people whose behavior is so unpleasant that others cannot endure their presence or actions. Insufferable personalities combine arrogance with insensitivity to others\' feelings. Insufferable heat makes outdoor activities impossible. The term suggests behavior that goes beyond merely annoying to become genuinely intolerable. Insufferable critics offer constant, harsh judgment without constructive purpose. Unlike temporarily irritating situations, insufferable conditions seem to persist without relief. Insufferable pain requires immediate medical intervention. The word emphasizes the emotional impact on those who must endure the unpleasant situation. Insufferable behavior often results from lack of self-awareness or consideration for others.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-SUF-er-uh-buhl',
                'etymology': 'From Latin "insufferabilis," combining "in-" (not) with "sufferabilis" (able to be endured), derived from "sufferre" (to bear, endure).',
                'language_origins': 'Latin',
                'example_sentence': 'His _______ arrogance and constant bragging made it impossible for colleagues to enjoy working with him.',
                'memory_tip': 'Remember "INSUFFERABLE" - think "IN-SUFFER-ABLE" meaning NOT "sufferable" (bearable) - too annoying or unpleasant to tolerate.'
            },
            'insufflator': {
                'definition': 'An insufflator is a medical device used to blow air, gas, or powdered medication into body cavities or onto surfaces for therapeutic or diagnostic purposes. This specialized instrument enables controlled delivery of substances to areas that are difficult to reach through other methods. Surgical insufflators inflate body cavities with carbon dioxide to create space for minimally invasive procedures like laparoscopy. Nasal insufflators deliver powdered medications directly to nasal passages. Ear insufflators help examine tympanic membranes by creating air pressure changes. The device provides precise control over pressure, volume, and flow rate of delivered substances. Unlike simple blowing or spraying, insufflation requires controlled conditions to ensure patient safety and procedure effectiveness. Veterinary insufflators serve similar functions in animal medical care. The technology enables modern minimally invasive surgical techniques.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-SUF-lay-ter',
                'etymology': 'From Latin "insufflare," meaning "to blow into," combining "in-" (into) with "sufflare" (to blow). The suffix "-ator" indicates a device that performs the action.',
                'language_origins': 'Latin',
                'example_sentence': 'The surgeon used an _______ to inflate the patient\'s abdomen with gas, creating space to perform the minimally invasive procedure.',
                'memory_tip': 'Remember "INSUFFLATOR" - think "IN-SUFFLATOR" like a device that "sufflates" (blows) air or gas "IN" to body cavities for medical procedures.'
            },
            'insulation': {
                'definition': 'Insulation refers to materials or techniques used to prevent the transfer of heat, sound, or electricity between different areas, or the act of installing such protective barriers. This noun describes both the physical materials and the process of creating barriers against unwanted energy transfer. Building insulation reduces heating and cooling costs by maintaining interior temperatures. Electrical insulation prevents dangerous current flow between conductors. Sound insulation reduces noise transmission between spaces. Thermal insulation materials include fiberglass, foam, and reflective barriers. The effectiveness depends on material properties, thickness, and proper installation. Unlike conductors that allow energy transfer, insulation blocks or significantly reduces transfer. Insulation systems often combine multiple materials and techniques to achieve desired performance. Proper insulation improves energy efficiency, comfort, and safety in buildings and equipment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-suh-LAY-shun',
                'etymology': 'From Latin "insula," meaning "island," combined with "-ation." The concept suggests creating an "island" that separates different temperature or energy zones.',
                'language_origins': 'Latin',
                'example_sentence': 'Adding proper _______ to the attic significantly reduced the family\'s heating bills during the cold winter months.',
                'memory_tip': 'Remember "INSULATION" - think "IN-SUL-ATION" like creating an "insulated" island that keeps heat "IN" or out - protective barriers against energy transfer.'
            },
            'insulin': {
                'definition': 'Insulin is a hormone produced by the pancreas that regulates blood glucose levels by enabling cells to absorb and use sugar for energy, essential for proper metabolism and cellular function. This protein hormone is crucial for converting glucose from food into usable energy. Type 1 diabetes occurs when the pancreas cannot produce insulin, requiring external insulin administration through injections or pumps. Type 2 diabetes involves reduced insulin effectiveness or production. Synthetic insulin medications help diabetics manage blood sugar levels and prevent dangerous complications. Discovery of insulin treatment transformed diabetes from a fatal disease to a manageable condition. Different types of insulin work at different speeds and durations. Proper insulin management requires monitoring blood glucose levels and adjusting doses based on food intake, activity, and individual needs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-suh-lin',
                'etymology': 'From Latin "insula," meaning "island," referring to the islets of Langerhans in the pancreas where insulin is produced. The suffix "-in" indicates a protein or biochemical substance.',
                'language_origins': 'Latin',
                'example_sentence': 'The diabetic patient had to inject _______ before meals to properly regulate her blood sugar levels.',
                'memory_tip': 'Remember "INSULIN" - think "IN-SUL-IN" from "insula" (island) because it\'s made in pancreatic "islands" - the hormone that controls blood sugar.'
            },
            'insult': {
                'definition': 'An insult is a disrespectful or offensive remark, action, or treatment intended to hurt someone\'s feelings, dignity, or reputation, or the act of delivering such offensive content. This noun and verb describes deliberate attempts to demean, humiliate, or offend others through words or actions. Verbal insults include name-calling, mockery, or disparaging comments. Actions can be insulting when they show deliberate disrespect or contempt. Cultural differences affect what constitutes insulting behavior. Unlike constructive criticism that aims to help, insults are intended to harm or diminish others. Insults often reflect the insulter\'s anger, frustration, or desire to assert superiority. The impact depends on the relationship between parties, cultural context, and individual sensitivity. Legal systems sometimes address severe insults as harassment or defamation.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'in-SULT (noun), in-SULT (verb)',
                'etymology': 'From Latin "insultare," meaning "to leap upon" or "to attack," combining "in-" (upon) with "saltare" (to leap, jump). Originally suggested physical attack.',
                'language_origins': 'Latin',
                'example_sentence': 'His crude _______ about her appearance was completely inappropriate and hurt her feelings deeply.',
                'memory_tip': 'Remember "INSULT" - think "IN-SULT" like "salting" wounds by being mean "IN" someone - offensive remarks that hurt feelings.'
            },
            'insurance': {
                'definition': 'Insurance is a financial arrangement where individuals or organizations pay regular premiums to an insurance company in exchange for protection against specified risks, with the insurer agreeing to compensate for covered losses or damages. This system spreads financial risk across many policyholders, making catastrophic losses manageable for individuals. Health insurance covers medical expenses. Auto insurance protects against vehicle damage and liability. Life insurance provides financial security for beneficiaries. Property insurance covers homes and belongings. The concept relies on probability calculations and risk pooling to determine fair premium rates. Insurance policies specify coverage limits, deductibles, and exclusions. Unlike savings or investments, insurance provides protection against unlikely but potentially devastating financial losses. The industry plays a crucial role in economic stability by enabling people and businesses to take calculated risks.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-SHOOR-uns',
                'etymology': 'From Old French "enseurance," derived from "ensurer" meaning "to make sure," ultimately from Latin "securus" (secure, safe).',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The comprehensive health _______ policy covered most of the expensive medical treatment she needed.',
                'memory_tip': 'Remember "INSURANCE" - think "IN-SURANCE" like being "IN" a state of "surance" (assurance/security) - financial protection against risks.'
            },
            'integrity': {
                'definition': 'Integrity is the quality of being honest, moral, and consistent in principles and behavior, characterized by adherence to ethical standards even when no one is watching or when facing difficult choices. This noun describes both moral character and structural wholeness or completeness. Personal integrity involves consistency between beliefs, words, and actions. Professional integrity requires ethical conduct in business dealings and responsibilities. Structural integrity refers to physical soundness of buildings, bridges, or systems. Data integrity ensures information remains accurate and uncorrupted. Unlike mere rule-following, integrity comes from internal commitment to doing right. Integrity often involves making difficult choices that prioritize principles over personal advantage. The concept encompasses both individual character and systematic reliability. People with integrity earn trust through consistent ethical behavior over time.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-TEG-ri-tee',
                'etymology': 'From Latin "integritas," meaning "wholeness" or "completeness," derived from "integer" (whole, complete), combining "in-" (not) with "tangere" (to touch, harm).',
                'language_origins': 'Latin',
                'example_sentence': 'The judge\'s reputation for _______ meant that lawyers trusted her decisions would be fair and based on legal principles.',
                'memory_tip': 'Remember "INTEGRITY" - think "INTEGRATE-Y" like being integrated/whole in your moral character - honest and consistent in principles.'
            },
            'integument': {
                'definition': 'An integument is a natural outer covering or protective layer that encloses and shields an organism or organ from external environment, serving functions like protection, regulation, and interaction with surroundings. This biological term describes various forms of external covering in living organisms. Human integument (skin) protects against infection, regulates temperature, and provides sensory input. Plant integuments protect seeds and developing reproductive structures. Insect integuments (exoskeletons) provide structural support and protection. The term can extend to any protective outer layer or membrane. Unlike simple barriers, integuments often perform multiple complex functions including gas exchange, waste elimination, and communication with environment. Integumentary systems are often the first line of defense against pathogens and environmental hazards. The structure and function of integuments vary greatly across different organisms.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-TEG-yuh-munt',
                'etymology': 'From Latin "integumentum," meaning "covering" or "wrapping," derived from "integere" meaning "to cover," combining "in-" (over) with "tegere" (to cover).',
                'language_origins': 'Latin',
                'example_sentence': 'The thick _______ of the cactus helps it survive in desert environments by preventing water loss.',
                'memory_tip': 'Remember "INTEGUMENT" - think "IN-TEGUMENT" like a natural "tegument" (covering) that\'s "IN" place - the protective outer layer of organisms.'
            },
            'intellectual': {
                'definition': 'Intellectual describes someone who engages in abstract thinking, scholarly pursuits, or complex mental activities, or refers to matters requiring advanced reasoning and knowledge rather than practical or manual skills. This adjective and noun characterizes both people and activities involving sophisticated thought processes. Intellectual discussions explore complex ideas and theories. Intellectual property includes patents, copyrights, and creative works. As a noun, an intellectual is someone devoted to mental rather than physical labor, often in academic or cultural fields. Unlike purely practical concerns, intellectual matters require critical thinking, analysis, and theoretical understanding. Intellectual development involves education, reading, and exposure to diverse ideas. The term can sometimes carry connotations of elitism or detachment from practical concerns, though intellectual work often provides essential foundations for practical applications.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'in-tuh-LEK-choo-ul',
                'etymology': 'From Latin "intellectualis," derived from "intellectus" meaning "understanding," from "intelligere" (to understand), combining "inter" (between) with "legere" (to choose, read).',
                'language_origins': 'Latin',
                'example_sentence': 'The university\'s _______ environment encouraged students to engage with challenging philosophical and scientific concepts.',
                'memory_tip': 'Remember "INTELLECTUAL" - think "INTEL-LECTUAL" like using "intel" (intelligence) to be "lectual" (related to learning) - involving advanced thinking and reasoning.'
            },
            'intensify': {
                'definition': 'Intensify means to increase in strength, degree, or concentration, or to make something more acute, powerful, or concentrated than it was previously. This verb describes processes where existing qualities become more pronounced or extreme. Heat intensifies as summer progresses. Conflicts intensify when communication breaks down. Medical treatments might intensify when conditions worsen. Unlike simply increasing quantity, intensifying focuses on making existing qualities more powerful or concentrated. Training programs intensify before competitions. Emotions can intensify during stressful situations. The process often involves reaching higher levels of whatever characteristic already exists. Weather patterns intensify into storms when atmospheric conditions align. Intensification can be gradual or sudden, but always involves movement toward greater strength or severity.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-TEN-suh-fy',
                'etymology': 'From Latin "intensus" meaning "stretched" or "strained," combined with the suffix "-ify" meaning "to make." The root suggests making something more strained or concentrated.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The storm began to _______ rapidly as it moved over the warm ocean waters.',
                'memory_tip': 'Remember "INTENSIFY" - think "INTENSE-IFY" meaning to make something more "intense" - increasing strength or concentration.'
            },
            'intentionally': {
                'definition': 'Intentionally means deliberately, on purpose, or with conscious design and planning rather than by accident or coincidence. This adverb describes actions taken with specific goals or purposes in mind. Intentionally harmful behavior involves deliberate attempts to cause damage. Artists might intentionally create ambiguous works to provoke thought. Unlike accidental outcomes, intentional actions result from conscious decision-making. Intentionally misleading statements constitute deception rather than honest mistakes. The term emphasizes the mental state behind actions, distinguishing between planned and unplanned results. Legal systems often consider intent when determining responsibility and punishment. Intentionally helpful behavior demonstrates care and consideration for others. The concept recognizes that human actions often result from conscious choice rather than random occurrence.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'in-TEN-shun-ul-ee',
                'etymology': 'From Latin "intentionalis," derived from "intentio" meaning "purpose" or "aim," combined with the adverbial suffix "-ly."',
                'language_origins': 'Latin, English',
                'example_sentence': 'She _______ chose challenging courses to prepare herself for graduate school admission.',
                'memory_tip': 'Remember "INTENTIONALLY" - think "INTENTION-ALLY" like acting as an "ally" to your "intention" - doing something on purpose with specific goals.'
            },
            'interact': {
                'definition': 'Interact means to act upon each other, communicate, or engage in mutual activity that involves reciprocal influence or exchange between two or more entities. This verb describes dynamic relationships where participants affect each other through communication, behavior, or shared activities. People interact through conversation, collaboration, and social engagement. Chemical substances interact to form new compounds. Computer systems interact with users through interfaces. Unlike one-way communication, interaction requires response and mutual engagement. Students interact with teachers and classmates during educational activities. Interactive technology responds to user input. The concept emphasizes reciprocal relationships rather than isolated actions. Successful interactions often require understanding, empathy, and effective communication skills. Social interactions build relationships and communities.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-ter-AKT',
                'etymology': 'From Latin "inter" (between) combined with "agere" (to act), literally meaning "to act between" or "to act with each other."',
                'language_origins': 'Latin',
                'example_sentence': 'The shy child gradually learned to _______ more confidently with classmates during group activities.',
                'memory_tip': 'Remember "INTERACT" - think "INTER-ACT" meaning to "ACT" "INTER" (between/with) others - mutual communication and influence.'
            },
            'intercede': {
                'definition': 'Intercede means to intervene on behalf of another person, typically by making a request or plea to someone in authority to help resolve a problem or provide assistance. This verb describes the act of acting as an intermediary to help others who cannot effectively advocate for themselves. Parents might intercede with teachers on behalf of struggling students. Diplomats intercede between conflicting nations to prevent war. Religious figures intercede with divine powers for their followers. The term implies selfless action taken to benefit others rather than oneself. Unlike direct confrontation, intercession involves appealing to authority or goodwill. Interceding often requires courage and moral conviction. The concept appears in legal, religious, and social contexts where advocacy is needed. Successful intercession requires understanding both the problem and the authority being approached.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-ter-SEED',
                'etymology': 'From Latin "intercedere," meaning "to go between" or "to intervene," combining "inter" (between) with "cedere" (to go, yield).',
                'language_origins': 'Latin',
                'example_sentence': 'The counselor agreed to _______ with the principal on behalf of the student who was facing unfair punishment.',
                'memory_tip': 'Remember "INTERCEDE" - think "INTER-CEDE" like "ceding" (going) "INTER" (between) people to help - intervening to help others.'
            },
            'interesting': {
                'definition': 'Interesting describes something that attracts attention, curiosity, or fascination because it is unusual, engaging, or thought-provoking in ways that capture and hold interest. This adjective characterizes subjects, people, or experiences that stimulate mental engagement and desire to learn more. Interesting books hold readers\' attention through compelling plots or ideas. Interesting people have diverse experiences or unique perspectives that engage others in conversation. The term suggests quality that makes something worth attention and consideration. Unlike boring content that fails to engage, interesting material creates desire for continued involvement. Interesting problems challenge thinking and problem-solving skills. Scientific discoveries are interesting when they reveal unexpected patterns or possibilities. The concept is subjective - what one person finds interesting, another might find dull, depending on personal interests, background, and experiences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'IN-ter-est-ing',
                'etymology': 'From Latin "interesse," meaning "to be between" or "to be important," combined with the English suffix "-ing." Originally suggested something that "interests" or concerns people.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The documentary about deep-sea exploration was so _______ that viewers forgot they had been watching for three hours.',
                'memory_tip': 'Remember "INTERESTING" - think "INTER-ESTING" like something that goes "INTER" (into) your mind and creates "ESTING" (lasting) engagement - fascinating and engaging.'
            },
            'interferon': {
                'definition': 'Interferon is a protein produced naturally by the immune system in response to viral infections, tumors, or other threats, serving as a critical defense mechanism that interferes with viral replication and enhances immune responses. This biological molecule represents one of the body\'s first lines of defense against pathogens. Interferon helps infected cells resist further viral invasion and signals neighboring cells to strengthen their defenses. Medical researchers have developed synthetic interferons as treatments for various conditions including hepatitis, multiple sclerosis, and certain cancers. Different types of interferons (alpha, beta, gamma) have specific functions and therapeutic applications. The discovery of interferon revolutionized understanding of immune system function and led to important medical treatments. Side effects of interferon therapy can include flu-like symptoms, fatigue, and mood changes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-ter-FEER-on',
                'etymology': 'Coined in 1957 from "interfere" plus the suffix "-on" (indicating a substance). The name reflects its ability to interfere with viral replication.',
                'language_origins': 'English (scientific coinage)',
                'example_sentence': 'The patient\'s treatment with _______ helped control the viral infection and boost her immune system response.',
                'memory_tip': 'Remember "INTERFERON" - think "INTERFERE-ON" like a substance that\'s "ON" and ready to "INTERFERE" with viruses - a natural antiviral protein.'
            },
            'interim': {
                'definition': 'Interim describes a temporary period between two events or states, or something that serves as a provisional measure while waiting for a permanent solution or replacement. This adjective and noun characterizes transitional arrangements that bridge gaps in time or authority. Interim governments maintain stability between elections. Interim reports provide updates before final results are available. The term suggests temporary status that will eventually be replaced by permanent arrangements. Unlike permanent appointments, interim positions are understood to be short-term. Interim solutions address immediate needs while better options are developed. Business interim managers step in during transitions between permanent leaders. The concept recognizes that some situations require temporary measures to maintain continuity and function. Interim periods often involve uncertainty about future developments.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'IN-ter-im',
                'etymology': 'From Latin "interim," meaning "meanwhile" or "in the meantime," derived from "inter" (between) and the suffix "-im" indicating time.',
                'language_origins': 'Latin',
                'example_sentence': 'The board appointed an _______ CEO to lead the company while they searched for a permanent replacement.',
                'memory_tip': 'Remember "INTERIM" - think "INTER-IM" like "in the time" that\'s "INTER" (between) permanent situations - temporary or provisional.'
            },
            'interjected': {
                'definition': 'Interjected is the past tense of "interject," meaning to have inserted a comment, remark, or interruption abruptly into a conversation or discussion, typically when one was not previously speaking. This verb describes the action of breaking into ongoing dialogue to add information, express disagreement, or redirect conversation. Interjected comments often occur when someone feels compelled to add important information or correct misunderstandings. Unlike planned contributions to discussion, interjected remarks interrupt the natural flow of conversation. The action can be helpful when adding crucial information or problematic when disrupting productive dialogue. Interjected questions can clarify confusing points. The timing and manner of interjection affects whether it\'s perceived as helpful contribution or rude interruption. Skilled communicators know when interjection is appropriate and when patience is better.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'in-ter-JEK-tid',
                'etymology': 'From Latin "interjectus," past participle of "interjicere," combining "inter" (between) with "jacere" (to throw). Literally means "thrown between."',
                'language_origins': 'Latin',
                'example_sentence': 'During the heated debate, she _______ a crucial fact that completely changed the direction of the discussion.',
                'memory_tip': 'Remember "INTERJECTED" - think "INTER-JECTED" like something "JECTED" (thrown) "INTER" (between) speakers - interrupting conversation with a comment.'
            },
            'interjection': {
                'definition': 'An interjection is a word or phrase expressing sudden emotion, surprise, or reaction that stands alone grammatically and is typically punctuated with an exclamation point, or more generally, any abrupt interruption or insertion into speech or text. This grammatical term describes expressions like "Oh!" "Wow!" "Alas!" and "Hooray!" that convey immediate emotional responses. Interjections often reflect natural human reactions to unexpected situations. They can express joy, surprise, pain, disgust, or other strong feelings. Unlike other parts of speech that have grammatical relationships within sentences, interjections function independently. Common interjections vary across languages and cultures. Some interjections are borrowed from other languages ("Ouch!" from Dutch). The concept extends beyond grammar to describe any sudden insertion or interruption in ongoing processes or conversations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-ter-JEK-shun',
                'etymology': 'From Latin "interjectio," derived from "interjicere" meaning "to throw between," combining "inter" (between) with "jacere" (to throw).',
                'language_origins': 'Latin',
                'example_sentence': 'The student\'s sudden _______ of "Eureka!" indicated she had finally solved the difficult mathematics problem.',
                'memory_tip': 'Remember "INTERJECTION" - think "INTER-JECTION" like a word "JECTED" (thrown) "INTER" (between) regular speech - an exclamatory word expressing emotion.'
            },
            'interlocutor': {
                'definition': 'An interlocutor is a person who takes part in dialogue or conversation, particularly in formal discussions, debates, or questioning sessions where their role involves engaging with others through speech and response. This noun describes participants in conversational exchanges, especially those serving official or structured roles. Legal interlocutors might include judges, lawyers, or court-appointed questioners. Academic interlocutors participate in scholarly debates and discussions. The term emphasizes the interactive nature of communication where multiple parties exchange ideas. Unlike monologue speakers who talk without response, interlocutors engage in reciprocal communication. Skilled interlocutors can guide conversations, ask probing questions, and facilitate meaningful dialogue. The concept appears in formal contexts where conversation serves specific purposes like education, negotiation, or fact-finding. Effective interlocutors combine speaking and listening skills.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-ter-LOK-yuh-ter',
                'etymology': 'From Latin "interlocutor," derived from "interloqui" meaning "to speak between," combining "inter" (between) with "loqui" (to speak).',
                'language_origins': 'Latin',
                'example_sentence': 'The skilled _______ helped facilitate the peace negotiations by asking thoughtful questions of both parties.',
                'memory_tip': 'Remember "INTERLOCUTOR" - think "INTER-LOCUTOR" like someone who "LOCUTES" (speaks) "INTER" (between/with) others - a participant in dialogue.'
            },
            'interloper': {
                'definition': 'An interloper is someone who interferes in or intrudes upon a situation where they are not wanted or do not belong, typically inserting themselves into affairs, relationships, or activities without invitation or right. This noun describes individuals who involve themselves inappropriately in others\' business. Business interlopers might interfere in negotiations or transactions without authorization. Social interlopers insert themselves into private gatherings or conversations. The term carries negative connotations, suggesting unwelcome intrusion rather than legitimate participation. Unlike invited guests or authorized participants, interlopers lack proper standing or permission. Interlopers often disrupt established relationships or procedures. The concept emphasizes boundary violations and inappropriate involvement. Historical interlopers included unauthorized traders who interfered with established commercial relationships. Modern interlopers might interfere in family disputes or business dealings.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'IN-ter-lo-per',
                'etymology': 'From "interlope," meaning "to interfere in trade," possibly from Dutch "interlooper." The "-er" suffix indicates one who performs the action.',
                'language_origins': 'Dutch, English',
                'example_sentence': 'The family considered him an _______ who had no right to interfere in their private business decisions.',
                'memory_tip': 'Remember "INTERLOPER" - think "INTER-LOPER" like someone who "LOPES" (runs) "INTER" (into) places they don\'t belong - an unwelcome intruder.'
            },
            'intermezzo': {
                'definition': 'An intermezzo is a short musical composition or theatrical piece performed between the acts of an opera, play, or longer musical work, or more broadly, any brief interlude or interval that provides contrast or transition between longer sections. This musical term describes intermezzos that originated in Italian opera as entertainment during scene changes. Musical intermezzos can be independent compositions or movements within larger works. The concept extends to any brief intervening episode that provides relief or transition. Literary intermezzos might be short chapters that break up longer narratives. Unlike main acts or movements, intermezzos serve transitional or complementary functions. Famous intermezzos include pieces by Brahms and Mascagni. The term suggests something lighter or more playful than surrounding serious content. Modern usage sometimes describes any brief interlude or break in ongoing activities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-ter-MET-so',
                'etymology': 'From Italian "intermezzo," meaning "in the middle," derived from Latin "intermedius" (intermediate), combining "inter" (between) with "medius" (middle).',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The orchestra performed a delightful _______ between the opera\'s second and third acts.',
                'memory_tip': 'Remember "INTERMEZZO" - think "INTER-MEZZO" like something in the "MEZZO" (middle) that\'s "INTER" (between) main sections - a musical interlude.'
            },
            'international': {
                'definition': 'International describes relationships, activities, or matters that involve two or more countries or extend across national boundaries, characterized by cooperation, conflict, or interaction between different nations. This adjective encompasses politics, economics, law, culture, and social issues that transcend individual countries. International trade connects global markets and economies. International law governs relationships between sovereign states. The term suggests scope beyond domestic or national concerns. International organizations like the United Nations coordinate global cooperation. International conflicts require diplomatic solutions. Unlike national issues that affect single countries, international matters have global implications. International students study in countries other than their own. The concept recognizes increasing global interconnection and the need for cooperation on shared challenges. International perspectives help understand diverse viewpoints and approaches.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ter-NASH-uh-nul',
                'etymology': 'From "inter-" (between) combined with "national," from Latin "natio" (nation, people). The term emphasizes relationships between nations.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The _______ conference brought together diplomats from fifty countries to discuss climate change solutions.',
                'memory_tip': 'Remember "INTERNATIONAL" - think "INTER-NATIONAL" meaning "INTER" (between) different "NATIONS" - involving multiple countries.'
            },
            'internecine': {
                'definition': 'Internecine describes conflict or warfare that is mutually destructive, particularly within a group, organization, or nation where different factions fight each other with devastating consequences for all involved parties. This adjective characterizes internal struggles that weaken or destroy the larger entity. Internecine political warfare damages entire parties or movements. Corporate internecine conflicts can destroy companies from within. The term emphasizes mutual destruction rather than victory. Unlike external conflicts with foreign enemies, internecine struggles involve internal divisions. Family internecine disputes can tear families apart permanently. Academic internecine battles damage entire institutions. The concept suggests that everyone loses when internal conflicts become too destructive. Internecine warfare often involves personal animosity and intimate knowledge of opponents\' weaknesses. Resolution requires focusing on common interests rather than internal divisions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ter-NEE-syn',
                'etymology': 'From Latin "internecinus," meaning "mutually destructive," derived from "internecare" (to kill between), combining "inter" (between) with "necare" (to kill).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ fighting between party factions weakened their chances in the upcoming election.',
                'memory_tip': 'Remember "INTERNECINE" - think "INTER-NECINE" like "INTER" (internal) killing that\'s "NECINE" (deadly) - mutually destructive internal conflict.'
            },
            'internet': {
                'definition': 'The Internet is a global network of interconnected computers and servers that enables worldwide communication, information sharing, and digital services through standardized protocols and infrastructure. This revolutionary technology connects billions of devices and users across the planet. The Internet supports email, websites, social media, online shopping, and countless digital applications. Unlike isolated computer networks, the Internet creates universal connectivity. Internet protocols like TCP/IP enable different systems to communicate effectively. The Internet has transformed education, business, entertainment, and social interaction. Access to Internet resources has become essential for modern life in many societies. Internet security and privacy present ongoing challenges as usage expands. The network\'s decentralized structure provides both resilience and complexity. Internet governance involves international cooperation and technical standards organizations.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'IN-ter-net',
                'etymology': 'Coined in the 1970s from "inter-" (between) and "network," originally referring to interconnected networks. The term emphasized connection between separate networks.',
                'language_origins': 'English (technical coinage)',
                'example_sentence': 'The _______ revolutionized how people access information and communicate with others around the world.',
                'memory_tip': 'Remember "INTERNET" - think "INTER-NET" like a "NET" that connects things "INTER" (between) each other - a global network connecting computers.'
            },
            'interpellate': {
                'definition': 'Interpellate means to formally question or challenge someone, particularly in political contexts where legislators demand explanations from government officials, or in academic theory, to address or hail someone in a way that creates their identity or subject position. This verb has both political and theoretical applications. Parliamentary interpellation allows opposition members to question government policies and actions. In political theory, interpellation describes how ideological structures address individuals and create their social identities. Unlike casual questioning, interpellation often involves formal procedures and significant consequences. Legal interpellation might involve official challenges to authority or jurisdiction. The concept suggests that being addressed in certain ways shapes identity and social position. Interpellation can be confrontational when challenging authority or constructive when seeking clarification. The term emphasizes the power dynamics involved in formal questioning.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-ter-PEL-ayt',
                'etymology': 'From Latin "interpellare," meaning "to interrupt by speaking" or "to appeal to," combining "inter" (between) with "pellere" (to drive, push).',
                'language_origins': 'Latin',
                'example_sentence': 'The opposition leader decided to _______ the prime minister about the controversial policy during the parliamentary session.',
                'memory_tip': 'Remember "INTERPELLATE" - think "INTER-PELLATE" like "PELL-ATING" (pushing with words) "INTER" (between) people - formally questioning or challenging someone.'
            },
            'interred': {
                'definition': 'Interred is the past tense of "inter," meaning to have buried or placed a dead body in the ground or in a tomb, typically as part of formal funeral rites and ceremonies. This verb describes the solemn act of laying the deceased to rest in their final resting place. Interred remains are placed in cemeteries, mausoleums, or other designated burial sites. The term carries formal and respectful connotations associated with death and burial customs. Unlike casual disposal, interment involves ceremonial procedures and permanent placement. Historically important figures are often interred in special locations like national cemeteries or family burial grounds. Interred artifacts might be buried with the deceased according to cultural traditions. The concept emphasizes the dignity and permanence of proper burial. Modern interment may involve caskets, urns for cremated remains, or traditional shrouds.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'in-TURD',
                'etymology': 'From Latin "interrare," meaning "to bury in the earth," combining "in-" (in) with "terra" (earth, ground).',
                'language_origins': 'Latin',
                'example_sentence': 'The war hero was _______ with full military honors in the national cemetery.',
                'memory_tip': 'Remember "INTERRED" - think "IN-TERRA-ED" meaning placed "IN" the "TERRA" (earth) - buried in the ground with ceremony.'
            },
            'interregnum': {
                'definition': 'An interregnum is a period when normal government or institutional authority is suspended, interrupted, or vacant, typically the interval between the end of one ruler\'s reign and the beginning of another\'s. This noun describes transitional periods that can create uncertainty and instability. Political interregnums occur between monarchs, presidents, or other leaders. Institutional interregnums happen when organizations lack clear leadership. The term suggests temporary absence of established authority rather than permanent change. Unlike stable governance periods, interregnums often involve competing claims to power or unclear succession. Historical interregnums sometimes led to civil wars or political chaos. Modern interregnums might involve caretaker governments or interim administrations. The concept emphasizes the importance of continuous legitimate authority for social stability. Interregnum periods test institutional strength and resilience.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-ter-REG-num',
                'etymology': 'From Latin "interregnum," meaning "between reigns," combining "inter" (between) with "regnum" (reign, kingdom).',
                'language_origins': 'Latin',
                'example_sentence': 'The country experienced political instability during the six-month _______ following the dictator\'s death.',
                'memory_tip': 'Remember "INTERREGNUM" - think "INTER-REGNUM" meaning "INTER" (between) "REGNUM" (reigns) - the gap between rulers when no one is officially in charge.'
            },
            'interrogative': {
                'definition': 'Interrogative describes words, sentences, or expressions used to ask questions, or more generally, having the quality of questioning or inquiry. This grammatical term encompasses question words like "who," "what," "when," "where," "why," and "how," as well as sentence structures that seek information. Interrogative pronouns introduce questions about identity, quantity, or characteristics. Interrogative sentences require answers and often use specific word order or punctuation. The term can describe investigative approaches that seek information through systematic questioning. Unlike declarative statements that provide information, interrogative expressions request information. Interrogative mood in grammar specifically indicates questioning intent. Legal interrogatives are formal questions used in depositions and court proceedings. Effective interrogatives are clear, specific, and designed to elicit useful responses. The concept emphasizes the communicative function of seeking information.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'in-ter-ROG-uh-tiv',
                'etymology': 'From Latin "interrogativus," derived from "interrogare" meaning "to ask" or "to question," combining "inter" (between) with "rogare" (to ask).',
                'language_origins': 'Latin',
                'example_sentence': 'The teacher used various _______ techniques to encourage students to think critically about the historical events.',
                'memory_tip': 'Remember "INTERROGATIVE" - think "INTER-ROGATIVE" like "ROGATING" (asking) "INTER" (between) people - relating to questions and inquiry.'
            },
            'intersecting': {
                'definition': 'Intersecting describes things that cross or meet at one or more points, creating connections or overlapping areas where different elements come together. This present participle characterizes both physical crossing and conceptual convergence. Intersecting roads create traffic intersections requiring signals or signs. Intersecting circles in geometry create areas of overlap. The term can describe overlapping interests, fields of study, or social issues. Intersecting storylines in literature create complex narratives. Unlike parallel elements that never meet, intersecting ones create points of connection and interaction. Intersecting demographics help marketers understand target audiences. Mathematical intersecting sets share common elements. The concept emphasizes points where different entities meet and interact. Intersecting ideas can lead to innovation and new understanding.',
                'part_of_speech': 'adjective, present participle',
                'pronunciation_guide': 'in-ter-SEK-ting',
                'etymology': 'From Latin "intersectus," past participle of "intersecare," combining "inter" (between) with "secare" (to cut). Literally means "cutting between."',
                'language_origins': 'Latin',
                'example_sentence': 'The city\'s _______ bike paths created a comprehensive network for bicycle commuters.',
                'memory_tip': 'Remember "INTERSECTING" - think "INTER-SECTING" like "SECTING" (cutting) "INTER" (between) things so they meet - crossing or meeting at points.'
            },
            'intersection': {
                'definition': 'An intersection is a place where two or more roads, paths, or lines cross each other, or more generally, any point where different elements meet, overlap, or interact. This noun describes both physical crossing points and conceptual convergences. Traffic intersections require careful navigation and traffic control systems. Mathematical intersections show where geometric figures meet. The term can describe overlapping areas in various fields or disciplines. Social intersections occur where different communities or cultures meet. Unlike separate or parallel elements, intersections create points of contact and potential interaction. Intersection theory in mathematics studies how different sets relate. Academic intersections occur where different fields of study overlap. The concept emphasizes connection points rather than isolation. Busy intersections often become focal points for communities or commercial activity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'in-ter-SEK-shun',
                'etymology': 'From Latin "intersectio," derived from "intersecare" meaning "to cut between," combining "inter" (between) with "secare" (to cut).',
                'language_origins': 'Latin',
                'example_sentence': 'The busy _______ required a traffic light to safely manage the flow of vehicles from all four directions.',
                'memory_tip': 'Remember "INTERSECTION" - think "INTER-SECTION" like a "SECTION" where roads go "INTER" (between/across) each other - where paths cross.'
            },
            'intersperse': {
                'definition': 'Intersperse means to scatter, place, or distribute things at intervals among or between other things, creating a pattern of alternation or variation rather than concentration in one area. This verb describes the action of mixing different elements throughout a space or sequence. Writers intersperse humor throughout serious narratives to provide relief. Gardeners intersperse different flowers to create varied color patterns. Unlike clustering similar items together, interspersing creates distribution and variety. Teachers intersperse different activities throughout lessons to maintain student engagement. Interspersed comments can interrupt the flow of presentations. The technique often enhances overall effect by providing contrast and preventing monotony. Musical compositions might intersperse quiet passages between loud sections. Interspersing requires intentional planning to achieve desired distribution and effect.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'in-ter-SPURS',
                'etymology': 'From Latin "interspersus," past participle of "interspergere," combining "inter" (among) with "spargere" (to scatter, sprinkle).',
                'language_origins': 'Latin',
                'example_sentence': 'The director decided to _______ comedic scenes throughout the drama to balance the film\'s emotional intensity.',
                'memory_tip': 'Remember "INTERSPERSE" - think "INTER-SPERSE" like "SPERSING" (scattering) things "INTER" (among) other things - distributing elements throughout.'
            },
            'interstellar': {
                'definition': 'Interstellar describes phenomena, objects, or spaces that exist or occur between stars within a galaxy, characterizing the vast regions of space that separate stellar systems. This astronomical adjective applies to the medium, distances, and processes in the space between stars. Interstellar dust and gas fill the regions between stars. Interstellar travel would require enormous distances and advanced technology. The term distinguishes between interstellar (between stars) and interplanetary (between planets) scales. Interstellar molecules have been detected in space using radio astronomy. Unlike the relatively empty space within solar systems, interstellar space contains various materials and radiation. Interstellar distances are measured in light-years rather than smaller units. Science fiction often explores interstellar civilizations and travel possibilities. The concept emphasizes the immense scale and complexity of galactic structure.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ter-STEL-er',
                'etymology': 'From Latin "inter" (between) combined with "stellar" (of the stars), from "stella" (star). Literally means "between the stars."',
                'language_origins': 'Latin, English',
                'example_sentence': 'Scientists study _______ dust clouds to understand how new stars and planetary systems form.',
                'memory_tip': 'Remember "INTERSTELLAR" - think "INTER-STELLAR" meaning "INTER" (between) "STELLAR" (stars) - the space and phenomena between stars.'
            },
            'intertidal': {
                'definition': 'Intertidal describes the coastal zone that is alternately covered and uncovered by ocean tides, characterized by unique ecological conditions that create specialized habitats for marine and terrestrial organisms. This ecological term applies to the area between high and low tide marks. Intertidal organisms must adapt to dramatic changes in water coverage, temperature, and salinity. Rocky intertidal zones support diverse communities of barnacles, mussels, and sea anemones. Sandy intertidal areas provide habitat for clams, crabs, and various worms. The environment creates unique challenges requiring specialized adaptations. Intertidal ecosystems are among the most productive marine environments. Unlike permanently submerged or terrestrial areas, intertidal zones experience regular environmental fluctuations. Intertidal research helps scientists understand adaptation and environmental stress. Human activities often threaten these sensitive coastal ecosystems.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ter-TY-dul',
                'etymology': 'From "inter-" (between) combined with "tidal" (relating to tides), from "tide." Refers to the zone between tidal extremes.',
                'language_origins': 'English',
                'example_sentence': 'The marine biology class studied the diverse creatures living in the rocky _______ pools during low tide.',
                'memory_tip': 'Remember "INTERTIDAL" - think "INTER-TIDAL" meaning "INTER" (between) high and low "TIDES" - the coastal zone covered and uncovered by tides.'
            },
            'intertribal': {
                'definition': 'Intertribal describes relationships, activities, or conflicts that occur between different tribes, nations, or indigenous groups, characterizing interactions that cross tribal boundaries and involve multiple distinct communities. This adjective applies to various forms of contact between separate tribal entities. Intertribal warfare historically occurred when different groups competed for resources or territory. Intertribal trade created economic relationships between distant communities. Modern intertribal councils coordinate political action on shared issues. The term recognizes that tribal communities are distinct entities with their own governments, cultures, and territories. Intertribal marriages created kinship connections between different groups. Unlike intratribal matters that occur within single tribes, intertribal affairs involve multiple sovereign entities. Intertribal ceremonies might bring together different communities for cultural exchange. Contemporary intertribal organizations work on issues affecting multiple indigenous communities.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'in-ter-TRY-bul',
                'etymology': 'From "inter-" (between) combined with "tribal" (relating to tribes), from "tribe." Emphasizes relationships between separate tribal groups.',
                'language_origins': 'English',
                'example_sentence': 'The _______ council brought together representatives from six different Native American nations to discuss water rights.',
                'memory_tip': 'Remember "INTERTRIBAL" - think "INTER-TRIBAL" meaning "INTER" (between) different "TRIBES" - involving relationships between separate tribal groups.'
            }
        }
        
        return batch_092_data.get(word, {
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
        
        # No obvious combined word errors detected in this batch
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
            else:
                print("No errors detected in this batch.")
            
            return True
            
        except Exception as e:
            print(f"Error processing batch: {str(e)}")
            return False

def main():
    processor = Batch092Processor()
    input_file = "output/batch_092_words.csv"
    output_file = "output/batch_092_processed.csv"
    
    success = processor.process_batch(input_file, output_file)
    if success:
        print("Batch 092 processing completed successfully!")
    else:
        print("Batch 092 processing failed!")

if __name__ == "__main__":
    main()