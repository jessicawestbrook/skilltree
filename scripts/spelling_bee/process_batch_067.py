import pandas as pd
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math

@dataclass
class WordData:
    word: str
    definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    language_origins: str = ""
    definition_source: str = "Claude"
    pronunciation_source: str = "Claude"
    etymology_source: str = "Claude"
    example_sentence: str = ""
    example_sentence_source: str = "Claude"
    memory_tip: str = ""
    memory_tip_source: str = "Claude"
    difficulty_phonetic: Optional[int] = None
    difficulty_semantic: Optional[int] = None
    difficulty_morphological: Optional[int] = None
    difficulty_etymological: Optional[int] = None
    combined_words_detected: bool = False
    incomplete_word_detected: bool = False
    parsing_errors: List[str] = field(default_factory=list)
    years: str = ""
    source_files: str = ""
    source_difficulties: str = ""

class DifficultyCalculator:
    def calculate_phonetic_score(self, word: str, pronunciation: str) -> int:
        irregular_patterns = ['ough', 'augh', 'eigh', 'ough', 'ph', 'gh', 'ch', 'sh', 'th']
        score = 1
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 1
        return min(score, 5)
    
    def calculate_semantic_score(self, definition: str, word: str) -> int:
        if len(definition) > 300:
            return 4
        elif len(definition) > 200:
            return 3
        elif len(definition) > 100:
            return 2
        return 1
    
    def calculate_morphological_score(self, word: str) -> int:
        prefixes = ['un', 'pre', 'dis', 'in', 'im', 'ir', 'ex', 'sub', 'super', 'anti', 'auto']
        suffixes = ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ous', 'eous', 'ious']
        score = 1
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 1
                break
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 1
                break
        if len(word) > 10:
            score += 1
        return min(score, 5)
    
    def calculate_etymological_score(self, etymology: str, language_origins: str) -> int:
        complex_origins = ['Greek', 'Latin', 'Sanskrit', 'Hebrew', 'Arabic']
        if any(origin in language_origins for origin in complex_origins):
            return 3
        elif 'French' in language_origins or 'German' in language_origins:
            return 2
        return 1

class Batch067Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def detect_parsing_errors(self, word: str) -> Tuple[bool, bool, List[str]]:
        errors = []
        combined_detected = False
        incomplete_detected = False
        
        # Check for combined words (specific to this batch)
        combined_word_patterns = {
            'fensterfiat': ['fenster', 'fiat'],
            'ficusagelicism': ['ficus', 'angelicism'],
            'fiduciaryadjective': ['fiduciary', 'adjective']
        }
        
        if word.lower() in combined_word_patterns:
            combined_detected = True
            errors.append(f"Combined word error: \"{word}\" appears to be {' + '.join(combined_word_patterns[word.lower()])} merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.")
        
        return combined_detected, incomplete_detected, errors
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge."""
        
        batch_067_data = {
            'female': {
                'definition': 'Female refers to the sex of an organism that typically produces eggs or bears offspring, or to characteristics associated with this sex. In biology, females are distinguished by their reproductive role and often by secondary sexual characteristics. The term can also describe objects, connectors, or parts that are designed to receive rather than insert, such as female electrical plugs. In social contexts, female can refer to gender identity and expression. The word encompasses both biological and social aspects of femininity.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FEE-mayl',
                'etymology': 'From Old French "femelle," from Latin "femella," diminutive of "femina" meaning "woman."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The _______ cardinal is brown and tan, while the male has bright red plumage.',
                'memory_tip': 'Remember "FE-male" - the FE-minine gender that complements male, from the Latin word for woman.'
            },
            'fend': {
                'definition': 'Fend means to defend oneself or to manage independently, often in difficult circumstances. The word commonly appears in phrases like "fend for oneself," meaning to take care of one\'s own needs without help from others. Fend can also mean to ward off or repel something unwanted, such as fending off attackers or fending off criticism. The word implies self-reliance, independence, and the ability to handle challenges through one\'s own efforts and resources.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FEND',
                'etymology': 'From Middle English "fenden," shortened from "defenden," ultimately from Latin "defendere" meaning "to defend."',
                'language_origins': 'Latin, Middle English',
                'example_sentence': 'After losing his job, he had to _______ for himself and his family without any financial support.',
                'memory_tip': 'Remember "FEND" - like a defensive FENCE, you protect yourself and FEND off problems or dangers.'
            },
            'fenestrated': {
                'definition': 'Fenestrated describes something that has windows, openings, or perforations, particularly in architecture, medicine, or biology. In architecture, fenestrated refers to buildings with windows or window-like openings. In medicine, it describes structures with natural or surgical openings, such as fenestrated blood vessels or surgical instruments with holes. In biology, fenestrated membranes have pores or gaps. The term emphasizes the presence of openings that allow passage of light, air, substances, or access.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FEN-uh-stray-tid',
                'etymology': 'From Latin "fenestratus," from "fenestra" meaning "window." Related to "defenestration" (throwing out of windows).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ wall of the cathedral allowed streams of colored light to filter through the stained glass windows.',
                'memory_tip': 'Remember "FENESTR-ated" - having windows or openings, like FENSTER (German for window) that have been created.'
            },
            'fens': {
                'definition': 'Fens are low-lying wetlands with alkaline water, characterized by soft, muddy ground and often covered with water. These marshy areas are typically fed by groundwater and surface water, creating unique ecosystems that support specialized plants and wildlife. Fens differ from bogs in their mineral content and water chemistry. The term is also used in proper names, such as the Fens in eastern England, a region known for its extensive fenland that has been largely drained for agriculture.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FENZ',
                'etymology': 'From Old English "fen" meaning "marsh" or "bog," related to similar words in other Germanic languages.',
                'language_origins': 'Old English',
                'example_sentence': 'The nature preserve protects several rare bird species that nest in the protected _______.',
                'memory_tip': 'Remember "FENS" - marshy wetlands where you need a FENCE to mark safe paths through the boggy ground.'
            },
            'fenster': {
                'definition': 'Fenster is the German word for "window," sometimes used in English in architectural, geological, or technical contexts. In geology, a fenster (also called a tectonic window) is an area where erosion has removed upper rock layers, exposing older rocks beneath. In architecture, the term might be used to describe window-like openings or features. The word emphasizes the concept of an opening that provides view or access to something beyond.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEN-ster',
                'etymology': 'From German "Fenster" meaning "window," ultimately from Latin "fenestra."',
                'language_origins': 'German, Latin',
                'example_sentence': 'The geological survey identified a _______ in the mountain range where ancient rock formations were visible.',
                'memory_tip': 'Remember "FENSTER" - the German word for window, like a FENCE with a opening to see through.'
            },
            'fermat': {
                'definition': 'Fermat typically refers to Pierre de Fermat (1601-1665), a French mathematician known for his contributions to number theory, probability theory, and analytic geometry. Fermat is famous for Fermat\'s Last Theorem, which states that no three positive integers can satisfy the equation a^n + b^n = c^n for any integer value of n greater than 2. This theorem remained unproven for over 350 years until Andrew Wiles proved it in 1995. Fermat\'s work laid foundations for modern mathematics.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'fer-MAH',
                'etymology': 'French surname, possibly from a place name or occupational term related to farming or land management.',
                'language_origins': 'French',
                'example_sentence': 'Students studying number theory often encounter _______ primes and other concepts named after the famous mathematician.',
                'memory_tip': 'Remember "FER-MAT" - a mathematician whose theorems were so complex they seemed FAR from being solved on a MATH test.'
            },
            'ferocious': {
                'definition': 'Ferocious describes something that is extremely fierce, violent, or intense in a savage or brutal way. When applied to animals, ferocious suggests predatory behavior characterized by aggressive attacks and lack of mercy. The word can also describe weather conditions, competition, or human behavior that is marked by extreme intensity or violence. Ferocious implies a level of wildness and aggression that is both frightening and potentially dangerous to encounter.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fuh-ROH-shus',
                'etymology': 'From Latin "ferocious," from "ferox" meaning "fierce" or "wild," related to "ferus" meaning "wild animal."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ storm brought destructive winds and torrential rain that lasted for hours.',
                'memory_tip': 'Remember "fe-ROCIOUS" - so fierce it\'s like a wild animal that ROCKS with violent intensity.'
            },
            'ferret': {
                'definition': 'A ferret is a domesticated carnivorous mammal related to weasels, traditionally used for hunting rabbits and rodents. Ferrets are elongated animals with short legs, known for their curiosity, playfulness, and ability to squeeze through small spaces. As a verb, ferret means to search persistently for something, often in a thorough or tenacious manner, similar to how the animal hunts. Modern ferrets are popular as pets due to their social nature and entertaining behaviors.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FAIR-it',
                'etymology': 'From Old French "furet," ultimately from Latin "fur" meaning "thief," referring to the animal\'s hunting behavior.',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The detective managed to _______ out the truth about the missing documents after hours of investigation.',
                'memory_tip': 'Remember "FERRET" - an animal that FERrets around to find things, like a furry detective searching everywhere.'
            },
            'ferruginous': {
                'definition': 'Ferruginous describes something that contains iron or has the rusty reddish-brown color of iron oxide. The term is commonly used in geology to describe rocks, soils, or minerals with high iron content, and in biology to describe organisms or structures with iron-rich coloration. Ferruginous materials often develop the characteristic rust color when iron compounds are exposed to oxygen and moisture. The word emphasizes both the chemical composition and the distinctive coloration associated with iron.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fuh-ROO-ji-nus',
                'etymology': 'From Latin "ferruginosus," from "ferrugo" meaning "rust" or "iron rust," derived from "ferrum" meaning "iron."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ soil in the region gave the landscape a distinctive reddish hue from its high iron content.',
                'memory_tip': 'Remember "ferr-UGINOUS" - containing FERR (iron) that makes things look rusty and UGLY with reddish-brown color.'
            },
            'fervently': {
                'definition': 'Fervently means with great intensity, passion, or enthusiasm, displaying deep feeling or ardent devotion to something. When someone acts fervently, they demonstrate strong emotional commitment and earnest dedication to their beliefs, causes, or activities. The word suggests not just enthusiasm but a kind of burning intensity that drives persistent effort and unwavering commitment. Fervent behavior often involves both emotional and physical expressions of dedication.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FUR-vunt-lee',
                'etymology': 'From "fervent" (from Latin "fervens," meaning "boiling" or "burning") plus the adverb suffix "-ly."',
                'language_origins': 'Latin',
                'example_sentence': 'She prayed _______ for her family\'s safety during the dangerous storm.',
                'memory_tip': 'Remember "FERVENT-ly" - with burning passion, like a FERVENT flame that burns intensely and constantly.'
            },
            'fervorous': {
                'definition': 'Fervorous describes something characterized by intense heat, burning passion, or fervent enthusiasm. The word suggests a quality of burning intensity or zealous devotion that is almost fever-like in its ardor. When something is fervorous, it embodies passionate intensity that can be both inspiring and overwhelming. The term is less commonly used than "fervent" but carries similar meanings of intense emotional heat and passionate dedication to causes or beliefs.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FUR-vor-us',
                'etymology': 'From Latin "fervor" meaning "burning heat" or "passion," plus the suffix "-ous" meaning "characterized by."',
                'language_origins': 'Latin',
                'example_sentence': 'His _______ dedication to social justice inspired others to join the movement for equality.',
                'memory_tip': 'Remember "FERVOR-ous" - full of FERVOR, burning with passionate intensity like a blazing furnace.'
            },
            'fester': {
                'definition': 'Fester means to become infected and form pus, or to deteriorate and become increasingly worse over time. When wounds fester, they fail to heal properly and become infected, often causing pain and complications. Figuratively, fester describes problems, grievances, or negative emotions that worsen when left unaddressed, growing more serious and potentially harmful over time. The word emphasizes the progressive deterioration that occurs without proper treatment or attention.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FES-ter',
                'etymology': 'From Old French "festre," ultimately from Latin "fistula" meaning "pipe" or "ulcer."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'If left untreated, the small disagreement between the neighbors will _______ into a major conflict.',
                'memory_tip': 'Remember "FESTER" - like a wound that gets worse FASTER when not properly treated, becoming infected and painful.'
            },
            'festival': {
                'definition': 'A festival is a celebration or series of events, typically involving music, food, entertainment, and cultural activities, held to commemorate special occasions, traditions, or themes. Festivals can be religious, cultural, artistic, seasonal, or commercial in nature, bringing communities together for shared experiences and enjoyment. They often feature performances, exhibitions, competitions, and social gatherings that celebrate particular aspects of culture, history, or achievement. Festivals serve important social functions in preserving traditions and building community bonds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FES-ti-vul',
                'etymology': 'From Old French "festival," from Latin "festivus" meaning "festive," related to "festum" meaning "feast" or "holiday."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The annual music _______ attracts thousands of visitors to the small town each summer.',
                'memory_tip': 'Remember "FEST-ival" - a FEAST-like celebration where people come together for festive activities and fun.'
            },
            'festooned': {
                'definition': 'Festooned describes something that is decorated or adorned with chains, garlands, ribbons, or other ornamental items hung in curves or loops. When something is festooned, it has been embellished with decorative elements that create a celebratory or ornate appearance. The decorations typically hang in graceful curves, creating patterns that are both decorative and festive. Festooning is common for celebrations, holidays, and special events where visual appeal and festivity are desired.',
                'part_of_speech': 'adjective (past participle)',
                'pronunciation_guide': 'fes-TOOND',
                'etymology': 'From "festoon," from French "feston," ultimately from Italian "festone" meaning "festive ornament."',
                'language_origins': 'Italian, French',
                'example_sentence': 'The wedding venue was _______ with white roses and twinkling lights that created a magical atmosphere.',
                'memory_tip': 'Remember "fest-OONED" - decorated for a FEST (celebration), with ornaments draped like a festive SWOON of decorations.'
            },
            'feta': {
                'definition': 'Feta is a traditional Greek cheese made from sheep\'s milk or a mixture of sheep and goat milk, characterized by its white color, crumbly texture, and tangy, salty flavor. The cheese is typically aged in brine, which gives it its distinctive taste and helps preserve it. Feta is a staple ingredient in Greek cuisine, commonly used in salads, pastries, and various Mediterranean dishes. The cheese has protected designation of origin status in the European Union, meaning authentic feta must be produced in specific regions of Greece.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FET-uh',
                'etymology': 'From modern Greek "feta," meaning "slice," referring to how the cheese is cut into slices before being placed in brine.',
                'language_origins': 'Greek',
                'example_sentence': 'The Greek salad was topped with crumbled _______ cheese and drizzled with olive oil.',
                'memory_tip': 'Remember "FETA" - a Greek cheese that\'s better than BETA, the creamy white cheese that FETs (fits) perfectly in salads.'
            },
            'fetlocks': {
                'definition': 'Fetlocks are the joints on horses\' legs located between the cannon bone and the pastern, corresponding roughly to the human ankle. These joints are visible as the "ankle" area on each of the horse\'s four legs and are important for the animal\'s movement and shock absorption. The term can also refer to the tuft of hair that grows behind these joints on some horse breeds. Fetlocks are crucial anatomical features that veterinarians and horse owners monitor for injuries or abnormalities.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FET-loks',
                'etymology': 'From Middle English, possibly related to "foot" and "lock" (tuft of hair), referring to the joint and hair in that area.',
                'language_origins': 'Middle English',
                'example_sentence': 'The veterinarian examined the horse\'s _______ for signs of swelling or injury after the race.',
                'memory_tip': 'Remember "FET-locks" - the joints where horses\' FEET are LOCKED to their legs, like ankle joints with tufts of hair.'
            },
            'fetticus': {
                'definition': 'Fetticus appears to be a rare or archaic term that may relate to legal or formal contexts, possibly referring to something made, fashioned, or artificial. The word may be related to Latin legal terminology or historical usage in formal documents. Without extensive historical context, the exact meaning and usage of this term are unclear, and it may represent a specialized or obsolete word that was used in specific legal, academic, or technical contexts in earlier periods.',
                'part_of_speech': 'adjective (uncertain)',
                'pronunciation_guide': 'FET-i-kus',
                'etymology': 'Possibly from Latin roots related to "facere" (to make) or legal terminology, though exact origin is uncertain.',
                'language_origins': 'Latin (uncertain)',
                'example_sentence': 'The ancient legal document contained several _______ clauses that modern scholars struggle to interpret.',
                'memory_tip': 'Remember "FETT-icus" - sounds like something FETCHED from old Latin texts, artificial or made up for legal purposes.'
            },
            'feudalism': {
                'definition': 'Feudalism is a medieval European social and economic system based on the holding of land in exchange for service and loyalty. Under feudalism, land was owned by kings and nobles who granted portions to vassals in return for military service, labor, or other obligations. The system created a hierarchical structure of lords and vassals, with peasants (serfs) working the land at the bottom of the social order. Feudalism dominated European society from roughly the 9th to 15th centuries and shaped political, economic, and social relationships throughout the medieval period.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYOOD-l-izm',
                'etymology': 'From "feudal" (from Medieval Latin "feudalis," related to "feudum" meaning "fief") plus the suffix "-ism."',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'The decline of _______ in Western Europe coincided with the rise of stronger centralized monarchies and urban commerce.',
                'memory_tip': 'Remember "FEUD-alism" - a system based on land FEUDS and loyalty, where everyone had their place in the social hierarchy.'
            },
            'fiat': {
                'definition': 'Fiat refers to an authoritative decree, order, or decision, especially one issued by someone in authority without the need for approval from others. The word comes from Latin meaning "let it be done" and implies the power to make something happen through declaration alone. In economics, fiat money is currency that has value because the government declares it legal tender, not because it\'s backed by physical commodities like gold. Fiat emphasizes the power of official proclamation or command.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEE-aht',
                'etymology': 'From Latin "fiat," meaning "let it be done" or "let it happen," third person singular present subjunctive of "fieri" (to become).',
                'language_origins': 'Latin',
                'example_sentence': 'The king issued a _______ declaring that all citizens must pay the new tax immediately.',
                'memory_tip': 'Remember "FIAT" - an order that\'s FLAT out final, decreed by authority with no discussion needed.'
            },
            'fibromyalgia': {
                'definition': 'Fibromyalgia is a chronic medical condition characterized by widespread musculoskeletal pain, fatigue, sleep disturbances, and often cognitive difficulties sometimes called "fibro fog." The condition affects the way the brain processes pain signals, amplifying painful sensations throughout the body. People with fibromyalgia may experience tender points in specific areas, along with other symptoms like headaches, depression, and anxiety. While the exact cause is unknown, the condition is recognized as a legitimate medical disorder that requires comprehensive management approaches.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fahy-broh-mahy-AL-juh',
                'etymology': 'From Latin "fibra" (fiber), Greek "myo" (muscle), and Greek "algia" (pain), literally meaning "fiber muscle pain."',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'After years of unexplained pain and fatigue, she was finally diagnosed with _______ and began appropriate treatment.',
                'memory_tip': 'Remember "FIBRO-MY-ALGIA" - pain in FIBers and MYscles, causing widespread ALGIA (pain) throughout the body.'
            },
            'fibula': {
                'definition': 'The fibula is the smaller of the two bones in the lower leg, running parallel to the tibia (shinbone) on the outer side of the leg. This slender bone extends from just below the knee to the ankle and plays important roles in muscle attachment and ankle stability. While the fibula doesn\'t bear as much weight as the tibia, it\'s crucial for proper leg function and movement. The term is also used in archaeology to describe ancient brooches or pins that resembled the bone in shape.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIB-yuh-luh',
                'etymology': 'From Latin "fibula" meaning "clasp" or "brooch," from "figere" meaning "to fix" or "to fasten."',
                'language_origins': 'Latin',
                'example_sentence': 'The X-ray showed a fracture in her _______ that would require several weeks to heal properly.',
                'memory_tip': 'Remember "FIB-ula" - the smaller leg bone that\'s like a FIB compared to the bigger tibia, thin and slender.'
            },
            'fictile': {
                'definition': 'Fictile describes something that is made of clay or earth, or something that can be molded or shaped, particularly referring to pottery and ceramic arts. The word emphasizes the malleable quality of clay and other materials that can be formed into desired shapes through human craftsmanship. Fictile objects are those created through the potter\'s art, including vessels, sculptures, and decorative items. The term can also refer more broadly to anything that is capable of being molded or fashioned.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FIK-tahyl',
                'etymology': 'From Latin "fictilis" meaning "made of clay" or "molded," from "fingere" meaning "to shape" or "to mold."',
                'language_origins': 'Latin',
                'example_sentence': 'The museum\'s collection of _______ artifacts included beautiful pottery from ancient civilizations.',
                'memory_tip': 'Remember "FICT-ile" - clay objects that are FICTioned (shaped) into useful and beautiful forms.'
            },
            'fiction': {
                'definition': 'Fiction is literature or other creative work that describes imaginary events, characters, and settings rather than real facts or actual occurrences. Fiction includes novels, short stories, plays, and other narrative forms that are products of imagination rather than historical record. The genre allows authors to explore themes, emotions, and ideas through invented scenarios and characters. While fiction may incorporate elements of reality or be inspired by real events, its primary characteristic is its imaginative rather than factual nature.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIK-shun',
                'etymology': 'From Latin "fictio" meaning "a fashioning" or "a feigning," from "fingere" meaning "to shape" or "to invent."',
                'language_origins': 'Latin',
                'example_sentence': 'She preferred reading _______ over biographies because she enjoyed escaping into imaginary worlds.',
                'memory_tip': 'Remember "FICTION" - stories that are FIXED up from imagination, not real facts but created narratives.'
            },
            'ficus': {
                'definition': 'Ficus is a genus of trees and shrubs in the mulberry family, including the common fig tree and many popular houseplants such as the rubber tree and weeping fig. These plants are characterized by their broad leaves, aerial roots, and often their ability to thrive in indoor environments. Many ficus species produce edible fruits, with the common fig being the most well-known. Ficus plants are native to tropical and subtropical regions and are widely cultivated for both ornamental and food purposes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FY-kus',
                'etymology': 'From Latin "ficus" meaning "fig tree," the ancient name for the fig and related plants.',
                'language_origins': 'Latin',
                'example_sentence': 'The large _______ tree in the office lobby required regular pruning to maintain its shape.',
                'memory_tip': 'Remember "FICUS" - sounds like FOCUS, these plants help you FOCUS on green beauty, especially the fig tree.'
            },
            'fiddlehead': {
                'definition': 'A fiddlehead is the young, coiled frond of a fern before it unfurls, resembling the scroll at the head of a violin or fiddle. These tightly curled structures are considered a delicacy in many cuisines and are harvested in spring when they emerge from the ground. Fiddleheads must be properly prepared before eating, as some species can be toxic if consumed raw. The term also refers to decorative architectural or nautical elements that resemble this distinctive spiral shape.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FID-l-hed',
                'etymology': 'Compound word combining "fiddle" and "head," referring to the resemblance to the decorative scroll at the head of a violin.',
                'language_origins': 'English',
                'example_sentence': 'The chef prepared the _______ ferns by sautéing them with garlic and butter as a seasonal specialty.',
                'memory_tip': 'Remember "FIDDLE-head" - young fern fronds that look like the curled HEAD of a FIDDLE before they unfurl.'
            },
            'fide': {
                'definition': 'Fide is a Latin word meaning "faith" or "trust," commonly encountered in English in legal and formal phrases such as "bona fide" (in good faith) and "mala fide" (in bad faith). The word represents concepts of reliability, trustworthiness, and honest intention in various contexts. In legal terminology, fide appears in expressions that describe the manner or spirit in which actions are taken, emphasizing the importance of sincere and honest conduct in formal proceedings and agreements.',
                'part_of_speech': 'Latin noun used in English contexts',
                'pronunciation_guide': 'FY-day',
                'etymology': 'From Latin "fides" meaning "faith," "trust," or "confidence," related to "fidere" meaning "to trust."',
                'language_origins': 'Latin',
                'example_sentence': 'The court determined that the buyer had acted in good _______ when making the purchase.',
                'memory_tip': 'Remember "FIDE" - from Latin meaning faith, like having FAITH that you can CONFIDE in someone trustworthy.'
            },
            'fidgeting': {
                'definition': 'Fidgeting is the act of making small, restless movements due to nervousness, impatience, or inability to remain still. When someone is fidgeting, they engage in repetitive motions such as tapping fingers, shifting position, playing with objects, or other minor movements that help release nervous energy. Fidgeting can be a natural response to stress, boredom, or anxiety, and while sometimes distracting to others, it often helps the fidgeter concentrate or manage emotional states.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'FIJ-it-ing',
                'etymology': 'From "fidget," possibly from earlier "fidge," of uncertain origin, possibly related to "fitch" meaning "to move restlessly."',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'His constant _______ during the long meeting showed how anxious he was about the presentation.',
                'memory_tip': 'Remember "FIDGET-ing" - making restless movements when you can\'t sit still, like a nervous FIDGETY habit.'
            },
            'fidgety': {
                'definition': 'Fidgety describes someone who is restless, unable to sit still, or inclined to make small, nervous movements. A fidgety person has difficulty remaining calm and stationary, often displaying anxiety, impatience, or excess energy through constant minor movements. This adjective characterizes both the behavior and the person who exhibits such restless tendencies. Fidgety behavior is common in situations involving stress, boredom, or anticipation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FIJ-it-ee',
                'etymology': 'From "fidget" plus the suffix "-y," describing the quality of being restless or unable to sit still.',
                'language_origins': 'English',
                'example_sentence': 'The _______ child couldn\'t sit through the entire concert without constantly shifting in her seat.',
                'memory_tip': 'Remember "FIDGET-y" - having a tendency to FIDGET, restless like someone who\'s itchy and can\'t sit still.'
            },
            'fido': {
                'definition': 'Fido is a common name for dogs, particularly in American culture, often used as a generic or stereotypical dog name in stories, jokes, and examples. The name comes from the Latin word "fidelis" meaning "faithful," reflecting the loyal nature associated with dogs. Historically, Fido was the name of Abraham Lincoln\'s dog, which helped popularize it. The name represents the archetypal faithful companion dog and is often used when referring to dogs in general rather than specific pets.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'FY-doh',
                'etymology': 'From Latin "fidelis" meaning "faithful" or "loyal," reflecting the characteristic loyalty of dogs.',
                'language_origins': 'Latin',
                'example_sentence': 'When giving examples in his speech, the professor always referred to the hypothetical family dog as _______.',
                'memory_tip': 'Remember "FIDO" - the faithful dog name from FIDel (faithful), representing loyal canine companions.'
            },
            'fiduciary': {
                'definition': 'Fiduciary refers to a relationship of trust where one party has a legal obligation to act in the best interest of another party. This term is commonly used in finance, law, and business to describe professionals who manage money, property, or other assets on behalf of clients. Fiduciaries must avoid conflicts of interest and prioritize their clients\' welfare over their own. Examples include financial advisors, trustees, and attorneys who have fiduciary duties to their clients or beneficiaries.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'fi-DOO-shee-er-ee',
                'etymology': 'From Latin "fiduciarius," from "fiducia" meaning "trust" or "confidence," related to "fides" meaning "faith."',
                'language_origins': 'Latin',
                'example_sentence': 'As a _______ advisor, she was legally required to recommend investments that were in her client\'s best interest.',
                'memory_tip': 'Remember "fi-DUCIARY" - like a financial DUCTILE relationship built on trust, where you CONFIDE in someone to manage your money.'
            },
            'field': {
                'definition': 'Field has multiple meanings depending on context. It can refer to an open area of land, especially one used for agriculture or sports. In academic contexts, field refers to a particular area of study or professional activity, such as the field of medicine. Field can also mean the area where practical work or research is conducted, as opposed to theoretical study. In various technical contexts, field describes areas of influence or activity, such as magnetic fields or visual fields.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FEELD',
                'etymology': 'From Old English "feld" meaning "open land" or "plain," related to similar words in other Germanic languages.',
                'language_origins': 'Old English',
                'example_sentence': 'The researcher spent months in the _______ collecting data on wildlife behavior patterns.',
                'memory_tip': 'Remember "FIELD" - an open area where you can FEEL free to work, play, or study in your area of expertise.'
            },
            'fiendishly': {
                'definition': 'Fiendishly means in an extremely wicked, cruel, or diabolical manner, or with devilish cleverness and cunning. The word can describe actions that are deliberately harmful or malicious, or it can describe something that is extremely difficult or challenging in a cleverly constructed way. Fiendishly often implies a kind of intelligent evil or sophisticated cruelty that makes situations particularly troublesome or complex. The adverb emphasizes the deliberate and calculated nature of the difficulty or wickedness.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FEEN-dish-lee',
                'etymology': 'From "fiendish" (from "fiend," from Old English "fēond" meaning "enemy" or "devil") plus the adverb suffix "-ly."',
                'language_origins': 'Old English',
                'example_sentence': 'The puzzle was _______ difficult, designed to challenge even the most experienced solvers.',
                'memory_tip': 'Remember "FIEND-ishly" - done in a devilish way, like a FIEND who acts wickedly or makes things extremely challenging.'
            },
            'fiercest': {
                'definition': 'Fiercest is the superlative form of fierce, describing something that displays the most intense degree of aggression, intensity, or strength. When something is the fiercest, it surpasses all others in terms of wild, savage, or passionate behavior. The word can apply to animals, competition, weather, or any situation characterized by extreme intensity. Fiercest implies not just strength but also a kind of wild, untamed quality that makes something particularly formidable or impressive.',
                'part_of_speech': 'adjective (superlative)',
                'pronunciation_guide': 'FEER-sist',
                'etymology': 'Superlative form of "fierce," from Old French "fiers," ultimately from Latin "ferus" meaning "wild."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The lioness was known as the _______ hunter in the pride, feared by all prey animals.',
                'memory_tip': 'Remember "FIERCE-st" - the most FIERCE of all, showing the greatest intensity and wild strength.'
            },
            'fifth': {
                'definition': 'Fifth refers to the number five in a sequence or series, representing the ordinal position that comes after fourth and before sixth. As a noun, fifth can refer to one of five equal parts of something, or to a specific quantity, such as a fifth of a gallon (in liquid measurement). In music, fifth refers to an interval of five notes. The word is used in various contexts to indicate position, proportion, or quantity related to the number five.',
                'part_of_speech': 'ordinal number, noun',
                'pronunciation_guide': 'FIFTH',
                'etymology': 'From Old English "fīfta," related to "fīf" (five), following the pattern of other ordinal numbers.',
                'language_origins': 'Old English',
                'example_sentence': 'She finished in _______ place in the marathon, achieving her personal best time.',
                'memory_tip': 'Remember "FIFTH" - the FIFth position, coming after four others, related to FIVE.'
            },
            'fifty': {
                'definition': 'Fifty is the cardinal number equal to five times ten, written as 50 in numerals. This number represents a significant milestone in many contexts, such as the fiftieth birthday being a major celebration, or fifty percent representing half of something. Fifty is often used as a round number in estimates, measurements, and various calculations. The number has cultural significance in phrases like "fifty-fifty" (equal chances) and represents a substantial quantity in most counting contexts.',
                'part_of_speech': 'cardinal number, noun',
                'pronunciation_guide': 'FIF-tee',
                'etymology': 'From Old English "fīftig," combining "fīf" (five) and "tig" (group of ten), literally meaning "five tens."',
                'language_origins': 'Old English',
                'example_sentence': 'The small town had a population of exactly _______ residents according to the latest census.',
                'memory_tip': 'Remember "FIF-ty" - FIFe (five) groups of ten, halfway to one hundred.'
            },
            'fights': {
                'definition': 'Fights can function as both a noun and verb, referring to physical or verbal conflicts between people or animals. As a verb, fights means to engage in battle, to struggle against something, or to work hard to achieve or resist something. As a noun, fights are instances of combat, arguments, or struggles. The word can apply to literal physical altercations, competitive contests, or metaphorical battles against diseases, injustice, or other challenges that require sustained effort to overcome.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'FYTS',
                'etymology': 'From Old English "feohtan" meaning "to combat" or "to struggle," related to similar words in other Germanic languages.',
                'language_origins': 'Old English',
                'example_sentence': 'The boxer _______ professionally and donates part of his earnings to charity.',
                'memory_tip': 'Remember "FIGHTS" - conflicts where people might FIGHT with their FISTS or struggle against challenges.'
            },
            'figurative': {
                'definition': 'Figurative describes language, art, or expression that uses figures of speech, symbols, or metaphors rather than literal, straightforward meaning. Figurative language includes metaphors, similes, personification, and other literary devices that create meaning through comparison or symbolic representation. In art, figurative refers to works that represent recognizable objects, people, or scenes rather than abstract forms. Figurative expression enriches communication by adding layers of meaning and emotional resonance beyond literal statements.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FIG-yur-uh-tiv',
                'etymology': 'From Latin "figurativus," from "figurare" meaning "to shape" or "to form," related to "figura" meaning "shape."',
                'language_origins': 'Latin',
                'example_sentence': 'The poet\'s _______ language painted vivid mental images through creative metaphors and similes.',
                'memory_tip': 'Remember "FIGUR-ative" - using FIGUREs of speech that aren\'t literal, like drawing word pictures with language.'
            },
            'filagree': {
                'definition': 'Filagree (also spelled filigree) is delicate ornamental work made from fine wire, typically gold or silver, twisted and soldered together to create intricate decorative patterns. This ancient metalworking technique produces lace-like designs that are both beautiful and technically challenging to create. Filagree work is often used in jewelry, decorative objects, and architectural details. The term can also describe anything that resembles this delicate, intricate wirework, emphasizing fine detail and ornate craftsmanship.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIL-uh-gree',
                'etymology': 'From French "filigrane," from Italian "filigrana," from Latin "filum" (thread) and "granum" (grain), referring to the thread-like appearance.',
                'language_origins': 'Latin, Italian, French',
                'example_sentence': 'The antique brooch featured intricate _______ work that demonstrated the jeweler\'s exceptional skill.',
                'memory_tip': 'Remember "FIL-agree" - decorative work made from FILaments (fine wires) that people aGREE looks beautiful and delicate.'
            },
            'filar': {
                'definition': 'Filar refers to something relating to or resembling a thread or having a thread-like structure. In technical and scientific contexts, filar describes instruments, measurements, or structures that use fine threads, wires, or thread-like components. For example, filar micrometers use fine threads or wires as measuring references. The term emphasizes the thin, thread-like quality of objects or the use of thread-like elements in precision instruments and measurements.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FY-lar',
                'etymology': 'From Latin "filaris," from "filum" meaning "thread," emphasizing thread-like characteristics.',
                'language_origins': 'Latin',
                'example_sentence': 'The astronomer used a _______ micrometer to make precise measurements of stellar positions.',
                'memory_tip': 'Remember "FIL-ar" - relating to FILaments or threads, like hair that\'s as thin as thread.'
            },
            'filbert': {
                'definition': 'A filbert is a type of hazelnut, specifically the cultivated variety of the hazel tree that produces edible nuts. Filberts are oval-shaped nuts with a sweet, rich flavor commonly used in cooking, baking, and confections. The nuts are harvested in autumn and can be eaten fresh or used in various culinary applications, from chocolates and pastries to savory dishes. Filbert trees are also grown ornamentally and are important in commercial nut production, particularly in regions with temperate climates.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIL-bert',
                'etymology': 'From Old French "noix de Philibert," named after St. Philibert, whose feast day falls during the nut harvest season.',
                'language_origins': 'Old French',
                'example_sentence': 'The baker added chopped _______ nuts to the coffee cake for extra flavor and texture.',
                'memory_tip': 'Remember "FIL-bert" - a nut named after Saint Philibert, like PHIL who likes BERT-sized nuts (hazelnuts).'
            },
            'files': {
                'definition': 'Files can refer to collections of papers, documents, or digital information organized for storage and reference, or to tools used for smoothing or shaping surfaces through abrasion. In office contexts, files are organized records kept for future reference. In computing, files are units of data stored on computers. As a verb, files means to organize documents systematically or to smooth surfaces with an abrasive tool. The word emphasizes organization, storage, and systematic arrangement of information or materials.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'FYLZ',
                'etymology': 'From Old French "filer" meaning "to string documents on a thread," from Latin "filum" meaning "thread."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'She organized all the legal _______ alphabetically for easy reference during the trial preparation.',
                'memory_tip': 'Remember "FILES" - documents strung together in order like beads on a string, or tools that make surfaces smoother.'
            },
            'filial': {
                'definition': 'Filial describes the relationship, feelings, or duties of a child toward their parents, emphasizing respect, obedience, and care. This adjective relates to the bond between offspring and their parents, particularly focusing on the responsibilities and emotional connections that children have toward those who raised them. Filial concepts are important in many cultures and legal systems, where filial duties may include caring for aging parents. The term emphasizes family relationships and intergenerational obligations.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FIL-ee-ul',
                'etymology': 'From Latin "filialis," from "filius" (son) and "filia" (daughter), relating to children\'s relationships with parents.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ devotion to her elderly mother was evident in the daily care and attention she provided.',
                'memory_tip': 'Remember "FIL-ial" - the relationship between children and parents, like how children should FILL their role as loving offspring.'
            },
            'filigree': {
                'definition': 'Filigree is an intricate ornamental technique using fine wire, typically gold or silver, twisted and soldered together to create delicate, lace-like patterns. This ancient decorative art form produces jewelry, boxes, and ornamental objects with elaborate openwork designs that appear almost ethereal in their delicacy. Filigree requires exceptional skill and patience, as artisans must manipulate extremely fine wires into complex patterns. The technique has been practiced for centuries across many cultures and represents some of the finest examples of metalworking artistry.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FIL-i-gree',
                'etymology': 'From French "filigrane," from Italian "filigrana," combining Latin "filum" (thread) and "granum" (grain).',
                'language_origins': 'Latin, Italian, French',
                'example_sentence': 'The museum displayed exquisite _______ jewelry from the 18th century, showcasing incredibly detailed wirework.',
                'memory_tip': 'Remember "FILI-gree" - ornate jewelry made from fine FILaments that people aGREE is beautifully intricate.'
            },
            'fillings': {
                'definition': 'Fillings are materials used to fill spaces, cavities, or containers, such as dental fillings that repair tooth decay, food fillings that go inside pastries or sandwiches, or substances used to fill gaps in construction. In dentistry, fillings restore damaged teeth using materials like amalgam or composite resin. In cooking, fillings are ingredients placed inside pastries, dumplings, or other foods. The word emphasizes the function of filling empty spaces or adding substance to hollow areas.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FIL-ingz',
                'etymology': 'From "fill" (from Old English "fyllan") plus the suffix "-ing," referring to materials that fill spaces.',
                'language_origins': 'Old English',
                'example_sentence': 'The dentist recommended composite _______ for the cavities because they match the natural tooth color.',
                'memory_tip': 'Remember "FILL-ings" - materials that FILL empty spaces, whether in teeth, food, or other objects.'
            },
            'film': {
                'definition': 'Film has multiple meanings, most commonly referring to a thin layer of material or a motion picture. As a thin layer, film can describe coatings, membranes, or surface coverings that are very thin. In photography and cinema, film refers to the medium used to capture images, or to motion pictures themselves. Film can also be a verb meaning to record moving images with a camera. The word emphasizes both thinness and the recording or covering function.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FILM',
                'etymology': 'From Old English "filmen" meaning "membrane" or "thin skin," related to "fell" meaning "hide" or "skin."',
                'language_origins': 'Old English',
                'example_sentence': 'The director decided to _______ the documentary in black and white to create a timeless artistic effect.',
                'memory_tip': 'Remember "FILM" - a thin layer like skin, or movies that capture images on thin strips of material.'
            },
            'final': {
                'definition': 'Final describes something that comes at the end, represents the last in a series, or is conclusive and unchangeable. When something is final, it represents the ultimate conclusion, decision, or result that cannot be altered or appealed. Final can apply to examinations, decisions, products, or any situation where no further changes are expected or possible. The word emphasizes completeness, conclusion, and the definitive nature of whatever is being described.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FY-nul',
                'etymology': 'From Latin "finalis," from "finis" meaning "end" or "boundary," emphasizing conclusion or completion.',
                'language_origins': 'Latin',
                'example_sentence': 'The judge\'s _______ ruling ended the lengthy legal battle between the two companies.',
                'memory_tip': 'Remember "FIN-al" - the FINish or end, the last and conclusive point that FINalizes everything.'
            },
            'finally': {
                'definition': 'Finally is an adverb meaning at last, after a long wait or delay, or as the final point in a sequence or argument. When something happens finally, it occurs after previous attempts, extended time, or as the conclusion to a series of events. The word can express relief, completion, or the resolution of something that has been anticipated or worked toward. Finally emphasizes the conclusion of a process and often implies that the wait or effort has been worthwhile.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FY-nul-ee',
                'etymology': 'From "final" (from Latin "finalis") plus the adverb suffix "-ly," meaning "in a final manner."',
                'language_origins': 'Latin',
                'example_sentence': 'After months of hard work and preparation, she _______ received her college acceptance letter.',
                'memory_tip': 'Remember "FIN-ally" - at last reaching the FINish line, the conclusion everyone has been waiting for.'
            }
        }
        
        if word.lower() in batch_067_data:
            return batch_067_data[word.lower()]
        else:
            # For any words not in our comprehensive data, return basic structure
            return {
                'definition': f'[Definition for {word} not available in batch data]',
                'part_of_speech': 'unknown',
                'pronunciation_guide': f'[Pronunciation for {word} not available]',
                'etymology': f'[Etymology for {word} not available]',
                'language_origins': 'unknown',
                'example_sentence': f'[Example sentence for {word} not available]',
                'memory_tip': f'[Memory tip for {word} not available]'
            }
    
    def process_batch(self, input_file: str, output_file: str):
        """Process a batch of spelling bee words with comprehensive Claude data."""
        print(f"Processing {input_file}...")
        
        # Read the input CSV
        df = pd.read_csv(input_file)
        
        processed_words = []
        error_count = 0
        
        for _, row in df.iterrows():
            word = str(row['word']).strip()
            
            # Skip empty rows
            if not word or word.lower() == 'nan':
                continue
            
            # Detect parsing errors
            combined_detected, incomplete_detected, errors = self.detect_parsing_errors(word)
            if errors:
                error_count += len(errors)
            
            # Get comprehensive data for this word
            word_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty scores (leaving final difficulty as null for now)
            phonetic_score = self.difficulty_calculator.calculate_phonetic_score(word, word_data['pronunciation_guide'])
            semantic_score = self.difficulty_calculator.calculate_semantic_score(word_data['definition'], word)
            morphological_score = self.difficulty_calculator.calculate_morphological_score(word)
            etymological_score = self.difficulty_calculator.calculate_etymological_score(word_data['etymology'], word_data['language_origins'])
            
            # Create WordData object
            processed_word = WordData(
                word=word,
                definition=word_data['definition'],
                part_of_speech=word_data['part_of_speech'],
                pronunciation_guide=word_data['pronunciation_guide'],
                etymology=word_data['etymology'],
                language_origins=word_data['language_origins'],
                example_sentence=word_data['example_sentence'],
                memory_tip=word_data['memory_tip'],
                difficulty_phonetic=phonetic_score,
                difficulty_semantic=semantic_score,
                difficulty_morphological=morphological_score,
                difficulty_etymological=etymological_score,
                combined_words_detected=combined_detected,
                incomplete_word_detected=incomplete_detected,
                parsing_errors=errors,
                years=str(row['years']) if 'years' in row else '',
                source_files=str(row['source_files']) if 'source_files' in row else '',
                source_difficulties=str(row['source_difficulties']) if 'source_difficulties' in row else ''
            )
            
            processed_words.append(processed_word)
        
        # Convert to DataFrame
        output_data = []
        for word_obj in processed_words:
            output_data.append({
                'word': word_obj.word,
                'definition': word_obj.definition,
                'part_of_speech': word_obj.part_of_speech,
                'pronunciation_guide': word_obj.pronunciation_guide,
                'etymology': word_obj.etymology,
                'language_origins': word_obj.language_origins,
                'definition_source': word_obj.definition_source,
                'pronunciation_source': word_obj.pronunciation_source,
                'etymology_source': word_obj.etymology_source,
                'example_sentence': word_obj.example_sentence,
                'example_sentence_source': word_obj.example_sentence_source,
                'memory_tip': word_obj.memory_tip,
                'memory_tip_source': word_obj.memory_tip_source,
                'difficulty_phonetic': word_obj.difficulty_phonetic,
                'difficulty_semantic': word_obj.difficulty_semantic,
                'difficulty_morphological': word_obj.difficulty_morphological,
                'difficulty_etymological': word_obj.difficulty_etymological,
                'difficulty': None,  # Leave null for now
                'years': word_obj.years,
                'source_files': word_obj.source_files,
                'source_difficulties': word_obj.source_difficulties,
                'combined_words_detected': word_obj.combined_words_detected,
                'incomplete_word_detected': word_obj.incomplete_word_detected,
                'parsing_errors': '; '.join(word_obj.parsing_errors) if word_obj.parsing_errors else ''
            })
        
        # Save to CSV
        output_df = pd.DataFrame(output_data)
        output_df.to_csv(output_file, index=False, quoting=1)  # quoting=1 ensures text fields are quoted
        
        # Print results
        print(f"Successfully processed {len(processed_words)}/50 words to {output_file}")
        if error_count > 0:
            print(f"Found {error_count} error(s):")
            for word_obj in processed_words:
                if word_obj.parsing_errors:
                    for error in word_obj.parsing_errors:
                        print(f"  - {word_obj.word}: {error}")
        
        print("Batch 067 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch067Processor()
    
    input_file = "output/batch_067_words.csv"
    output_file = "output/batch_067_processed.csv"
    
    processor.process_batch(input_file, output_file)