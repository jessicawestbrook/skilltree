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

class Batch070Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def detect_parsing_errors(self, word: str) -> Tuple[bool, bool, List[str]]:
        errors = []
        combined_detected = False
        incomplete_detected = False
        
        # Check for combined words (specific to this batch)
        combined_word_patterns = {
            'foleysyzygy': ['foley', 'syzygy'],
            'forgetrare': ['forget', 'rare']
        }
        
        # Check for incomplete words
        if word.lower() == 'forgetrare':
            incomplete_detected = True
            errors.append(f"Corrupted word: \"{word}\" appears to be malformed, possibly \"forget\" combined with \"rare\" or another corruption. This is likely a PDF parsing error.")
        elif word.lower() in combined_word_patterns:
            combined_detected = True
            errors.append(f"Combined word error: \"{word}\" appears to be {' + '.join(combined_word_patterns[word.lower()])} merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.")
        
        return combined_detected, incomplete_detected, errors
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge."""
        
        batch_070_data = {
            'focused': {
                'definition': 'Focused describes someone or something that is concentrated, directed, or centered on a particular objective, task, or area of attention. When someone is focused, they are able to direct their mental energy and attention toward specific goals without being easily distracted. This state involves mental clarity, purpose, and the ability to maintain concentration over time. Focused can also describe light, energy, or other phenomena that have been concentrated or directed toward a specific point or target.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'FOH-kust',
                'etymology': 'From "focus" (from Latin "focus" meaning "hearth" or "fireplace") plus the past participle ending "-ed."',
                'language_origins': 'Latin',
                'example_sentence': 'She remained _______ on her goals despite the many distractions around her.',
                'memory_tip': 'Remember "FOCUS-ed" - having achieved a state of FOCUS, concentrated and directed like light through a lens.'
            },
            'focuses': {
                'definition': 'Focuses can function as both a verb and noun, referring to the act of concentrating attention or effort on particular subjects, or to multiple centers of attention or activity. As a verb, focuses means to direct attention, adjust for clarity, or concentrate efforts. As a noun, focuses refers to multiple points of concentration or the central points of interest in various contexts. The word emphasizes concentration, clarity, and directed attention toward specific objectives.',
                'part_of_speech': 'verb, noun (plural)',
                'pronunciation_guide': 'FOH-kus-iz',
                'etymology': 'From "focus," plural form or third person singular present tense, from Latin "focus" meaning "hearth" or "central point."',
                'language_origins': 'Latin',
                'example_sentence': 'The research team _______ on three main areas of investigation this semester.',
                'memory_tip': 'Remember "FOCUS-es" - multiple points of FOCUS or the action of focusing, concentrating attention on specific areas.'
            },
            'fodder': {
                'definition': 'Fodder is coarse food, especially dried hay or feed, given to livestock such as cattle, horses, and sheep. The term can also refer metaphorically to raw material or people considered as readily available resources for a particular purpose, often with connotations of expendability. In military contexts, "cannon fodder" refers to soldiers viewed as expendable. The word emphasizes basic sustenance or material that serves a utilitarian purpose.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOD-er',
                'etymology': 'From Old English "fodor," meaning "food for cattle," related to "foda" meaning "food," ultimately from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The farmer stored bales of hay as winter _______ for the cattle.',
                'memory_tip': 'Remember "FODDER" - food for animals, or people treated like cattle, fed basic material to keep them going.'
            },
            'foible': {
                'definition': 'A foible is a minor weakness or failing in someone\'s character, particularly a small flaw or quirky trait that is relatively harmless but noticeable. Foibles are typically endearing or amusing personal characteristics that make people human and relatable, rather than serious character defects. These minor flaws often become part of what makes individuals unique and memorable. The word suggests tolerance and affection for human imperfections.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOY-bul',
                'etymology': 'From French "foible," meaning "weak," ultimately from Latin "flebilis" meaning "lamentable," related to "flere" (to weep).',
                'language_origins': 'French, Latin',
                'example_sentence': 'His habit of collecting vintage bottle caps was just one of his charming _______.',
                'memory_tip': 'Remember "FOIBLE" - a small FLAW that\'s quite WORKABLE, a minor weakness that\'s actually endearing.'
            },
            'foist': {
                'definition': 'Foist means to impose something unwanted or undesirable on someone through deception, persistence, or abuse of authority. When someone foists something upon another person, they force that person to accept, deal with, or take responsibility for something they didn\'t want or ask for. The word often implies trickery, manipulation, or taking advantage of someone\'s position or circumstances to make them accept an unwelcome burden or responsibility.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FOIST',
                'etymology': 'Possibly from Dutch "vuisten" meaning "to take in hand," or from obsolete "foist" meaning a dishonest person or cheat.',
                'language_origins': 'Dutch, English',
                'example_sentence': 'The unscrupulous contractor tried to _______ additional charges onto the unsuspecting homeowner.',
                'memory_tip': 'Remember "FOIST" - to force something unwanted on someone, like making them take a FIST full of problems.'
            },
            'folate': {
                'definition': 'Folate is a B-vitamin (specifically B9) that is essential for DNA synthesis, cell division, and proper brain function. This water-soluble vitamin is naturally found in leafy green vegetables, legumes, and fortified foods. Folate is particularly important during pregnancy for preventing birth defects, and deficiency can lead to anemia and other health problems. The synthetic form of folate, called folic acid, is commonly used in supplements and food fortification.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOH-layt',
                'etymology': 'From Latin "folium" meaning "leaf," because this vitamin was first isolated from spinach leaves.',
                'language_origins': 'Latin',
                'example_sentence': 'Pregnant women are advised to take _______ supplements to support healthy fetal development.',
                'memory_tip': 'Remember "FOL-ate" - a vitamin found in FOLiage (leafy greens) that you should folLOW for good health.'
            },
            'folded': {
                'definition': 'Folded describes something that has been bent, doubled over, or creased so that one part lies on another. When something is folded, it has been deliberately arranged to take up less space or to create a particular shape through bending or doubling. The word can apply to paper, fabric, body parts, or any flexible material that can be bent without breaking. Folded also suggests neatness, organization, and compact arrangement.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'FOHLD-id',
                'etymology': 'From "fold," from Old English "fealdan," meaning "to bend" or "to double over," related to similar words in Germanic languages.',
                'language_origins': 'Old English',
                'example_sentence': 'She placed the neatly _______ laundry in the dresser drawer.',
                'memory_tip': 'Remember "FOLD-ed" - something that has been bent and arranged, like papers that have been folded in half.'
            },
            'folding': {
                'definition': 'Folding refers to the action of bending or doubling something over so that one part lies against another, or describes something that can be bent or collapsed for storage or transport. Folding can describe the process of arranging clothes, creating origami, or the way certain furniture and equipment can be collapsed to save space. The word emphasizes flexibility, compactness, and the ability to change shape or size through bending.',
                'part_of_speech': 'verb (present participle), adjective, noun',
                'pronunciation_guide': 'FOHLD-ing',
                'etymology': 'From "fold" plus the present participle suffix "-ing," from Old English "fealdan" meaning "to bend."',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ table could be easily stored in the closet when not needed.',
                'memory_tip': 'Remember "FOLD-ing" - the ongoing action of bending things, or objects designed to fold for easy storage.'
            },
            'foley': {
                'definition': 'Foley refers to the reproduction of everyday sound effects that are added to films, videos, and other media in post-production to enhance audio quality. Named after sound-effects artist Jack Foley, this technique involves creating sounds like footsteps, door creaks, or rustling clothes in a recording studio to match the action on screen. Foley artists use various props and techniques to create realistic sounds that make scenes more immersive and believable.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOH-lee',
                'etymology': 'Named after Jack Foley (1891-1967), an American sound effects artist who developed many techniques for creating movie sound effects.',
                'language_origins': 'Proper name (American)',
                'example_sentence': 'The _______ artist created realistic footstep sounds by walking on different surfaces in the recording studio.',
                'memory_tip': 'Remember "FOLEY" - sound effects for films, named after Jack FOLEY who was FULLY committed to realistic movie sounds.'
            },
            'foliage': {
                'definition': 'Foliage refers collectively to the leaves of plants, trees, and shrubs, especially when viewed as a decorative or natural feature. This term encompasses the leafy growth that provides the green coverage of forests, gardens, and natural landscapes. Foliage can be described by its color, density, seasonal changes, or decorative qualities. The word is often used in gardening, landscaping, and nature description to emphasize the beauty and importance of plant leaves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOH-lee-ij',
                'etymology': 'From Old French "fueillage," from "feuille" meaning "leaf," ultimately from Latin "folium."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The autumn _______ created a spectacular display of red, orange, and yellow colors.',
                'memory_tip': 'Remember "FOLI-age" - the collective AGE of leaves (FOLI), all the leafy growth on trees and plants.'
            },
            'follicle': {
                'definition': 'A follicle is a small anatomical cavity or sac in the body, particularly the tiny structures in the skin from which hair grows, or the sacs in ovaries that contain developing eggs. Hair follicles are tube-like structures that surround hair roots and produce hair growth, while ovarian follicles release eggs during ovulation. Follicles are essential structures in both hair production and reproductive processes, representing important functional units in human biology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOL-i-kul',
                'etymology': 'From Latin "folliculus," diminutive of "follis" meaning "bag" or "sac," referring to the small sac-like structure.',
                'language_origins': 'Latin',
                'example_sentence': 'Each hair grows from its own _______ beneath the surface of the skin.',
                'memory_tip': 'Remember "FOLLI-cle" - small sacs where hair FOLLows its growth pattern, or eggs prepare to be FOLLowed by ovulation.'
            },
            'follow': {
                'definition': 'Follow means to go or come after someone or something in time, order, or position, or to pursue, chase, or accompany. The word can describe physical movement behind someone, adherence to rules or instructions, understanding of logic or reasoning, or showing interest in someone\'s activities or social media. Follow emphasizes sequence, pursuit, compliance, or the act of coming after something in various contexts.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FOL-oh',
                'etymology': 'From Old English "folgian," meaning "to pursue" or "to accompany," related to similar words in Germanic languages.',
                'language_origins': 'Old English',
                'example_sentence': 'Please _______ the marked trail to reach the summit safely.',
                'memory_tip': 'Remember "FOLLOW" - to go after someone or something, like following a FELLOW traveler on a path.'
            },
            'followed': {
                'definition': 'Followed is the past tense of follow, indicating that someone or something went after, pursued, or came after another person, thing, or event in time or sequence. When something followed, it occurred subsequently, adhered to instructions, or resulted from previous actions. The word can describe physical pursuit, chronological sequence, logical progression, or compliance with rules or directions that happened in the past.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'FOL-ohd',
                'etymology': 'Past tense of "follow," from Old English "folgian," meaning "to pursue" or "to accompany."',
                'language_origins': 'Old English',
                'example_sentence': 'The detective _______ the suspicious vehicle through the downtown area.',
                'memory_tip': 'Remember "FOLLOW-ed" - past tense of following, describing pursuit or sequence that already happened.'
            },
            'following': {
                'definition': 'Following can function as an adjective meaning "next" or "coming after," as a noun referring to a group of supporters or adherents, or as a preposition meaning "after" or "as a result of." When something is following, it comes next in sequence or time. As a noun, following describes people who support, admire, or regularly engage with someone or something, such as a social media following or a political following.',
                'part_of_speech': 'adjective, noun, preposition, verb (present participle)',
                'pronunciation_guide': 'FOL-oh-ing',
                'etymology': 'From "follow" plus the present participle suffix "-ing," creating multiple grammatical functions.',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ day brought clear skies and perfect weather for the outdoor concert.',
                'memory_tip': 'Remember "FOLLOW-ing" - what comes next after following, or the group of people who follow someone.'
            },
            'follows': {
                'definition': 'Follows is the third person singular present tense of follow, indicating that someone or something goes after, pursues, or comes after another person, thing, or event. When something follows, it occurs next in sequence, adheres to rules, results from previous actions, or physically pursues. The word can describe logical progression, physical movement, compliance, or chronological sequence happening in the present.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FOL-ohz',
                'etymology': 'Third person singular present form of "follow," from Old English "folgian."',
                'language_origins': 'Old English',
                'example_sentence': 'Success usually _______ hard work and dedication to one\'s goals.',
                'memory_tip': 'Remember "FOLLOW-s" - what someone or something does when they go after or come next, following a pattern.'
            },
            'folly': {
                'definition': 'Folly refers to foolishness, lack of good sense, or an act or idea that shows a lack of wisdom or judgment. When someone engages in folly, they demonstrate poor decision-making or pursue actions that are clearly unwise or impractical. Folly can also refer to a costly ornamental building with no practical purpose, often built as a whim or fancy. The word emphasizes foolishness, impracticality, and the waste that results from poor judgment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOL-ee',
                'etymology': 'From Old French "folie," from "fol" meaning "foolish," ultimately from Latin "follis" meaning "bellows" or "empty bag."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'Investing his entire savings in the risky venture proved to be an act of pure _______.',
                'memory_tip': 'Remember "FOLLY" - foolishness that makes you FOLLY (follow) bad decisions, showing lack of wisdom.'
            },
            'fomentation': {
                'definition': 'Fomentation refers to the action of instigating or stirring up trouble, unrest, or rebellion, particularly through deliberate agitation or inflammatory speech. In medical contexts, fomentation describes the application of warm, moist heat to treat pain or inflammation. The word can describe both the process of stirring up discord and the therapeutic application of heat. In both uses, fomentation involves applying pressure or heat to create a desired effect.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'foh-men-TAY-shun',
                'etymology': 'From Latin "fomentatio," from "fomentare" meaning "to warm" or "to cherish," from "fomes" (tinder, fuel).',
                'language_origins': 'Latin',
                'example_sentence': 'The political activist was accused of _______ of unrest through his inflammatory speeches.',
                'memory_tip': 'Remember "foment-ATION" - the ACTion of fomenting trouble, stirring up heat and agitation in situations.'
            },
            'fond': {
                'definition': 'Fond describes having a warm liking, affection, or tender feeling toward someone or something. When someone is fond of something, they have positive emotional attachment and enjoy or appreciate it. Fond can also describe memories, hopes, or beliefs that are cherished but may be unrealistic or overly optimistic. The word emphasizes gentle affection, pleasant attachment, and positive emotional connection.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FOND',
                'etymology': 'From Middle English, possibly from "fon" meaning "fool," originally meaning "foolishly tender," later developing positive connotations.',
                'language_origins': 'Middle English',
                'example_sentence': 'She had _______ memories of her grandmother\'s homemade apple pie.',
                'memory_tip': 'Remember "FOND" - having warm feelings for someone or something, like a loving BOND of affection.'
            },
            'fondant': {
                'definition': 'Fondant is a sweet, pliable sugar paste used in candy making and cake decorating, known for its smooth texture and ability to be rolled, molded, and shaped into decorative elements. This confection is made primarily from sugar, water, and often glucose or cream of tartar, creating a malleable substance that can cover cakes or be formed into intricate decorations. Fondant provides a professional, smooth finish to baked goods and allows for detailed decorative work.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FON-dant',
                'etymology': 'From French "fondant," literally meaning "melting," from "fondre" meaning "to melt," referring to its smooth, melt-in-the-mouth quality.',
                'language_origins': 'French',
                'example_sentence': 'The wedding cake was covered in white _______ and decorated with delicate sugar flowers.',
                'memory_tip': 'Remember "FOND-ant" - sweet sugar paste that\'s so smooth and pleasant you become FOND of using it for decorating.'
            },
            'fontina': {
                'definition': 'Fontina is a cow\'s milk cheese that originated in the Aosta Valley of Italy, characterized by a semi-soft texture and a mild, nutty flavor that becomes more complex with age. This versatile cheese has a natural rind and pale yellow interior, making it excellent for both eating and cooking. Fontina melts well, making it popular in fondues, gratins, and other cooked dishes. The cheese represents traditional Italian dairy craftsmanship and regional culinary heritage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fon-TEE-nah',
                'etymology': 'Named after Mount Fontin in the Aosta Valley of Italy, where this traditional cheese originated.',
                'language_origins': 'Italian',
                'example_sentence': 'The chef used aged _______ cheese in the risotto to add a rich, nutty flavor.',
                'memory_tip': 'Remember "fon-TINA" - Italian cheese from a mountain area, like a FOUNTAIN of creamy, nutty flavor.'
            },
            'food': {
                'definition': 'Food refers to any nutritious substance that people, animals, or plants consume to maintain life and growth. This essential requirement for survival includes natural products like fruits, vegetables, grains, and meat, as well as processed items created from these basic ingredients. Food provides the energy, nutrients, and building blocks necessary for biological functions. The concept encompasses both sustenance and cultural, social, and emotional aspects of eating and cuisine.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOOD',
                'etymology': 'From Old English "fōda," related to "feed" and similar words in Germanic languages meaning "nourishment."',
                'language_origins': 'Old English',
                'example_sentence': 'The community garden provided fresh, healthy _______ for local families.',
                'memory_tip': 'Remember "FOOD" - what we need for survival and GOOD health, nourishment that fuels our bodies and mood.'
            },
            'foods': {
                'definition': 'Foods is the plural form of food, referring to multiple types of nutritious substances consumed for nourishment and energy. This plural encompasses the variety of edible items available to humans and animals, including different categories like proteins, carbohydrates, fats, fruits, vegetables, and processed items. Foods represent the diversity of dietary options and the range of nutritious substances that support life and health across different cultures and cuisines.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FOODZ',
                'etymology': 'Plural form of "food," from Old English "fōda," representing multiple types of nourishment.',
                'language_origins': 'Old English',
                'example_sentence': 'The nutritionist recommended eating a variety of _______ from all major food groups.',
                'memory_tip': 'Remember "FOODS" - multiple types of nourishment, all the different edible things that are GOOD for our health and moods.'
            },
            'foolishness': {
                'definition': 'Foolishness is the quality of being unwise, imprudent, or lacking good judgment, characterized by actions or decisions that demonstrate poor thinking or disregard for consequences. This abstract noun describes behavior that shows lack of intelligence, common sense, or practical wisdom. Foolishness can manifest as reckless actions, poor decision-making, or failure to consider obvious risks or outcomes. The word emphasizes the absence of wisdom and the negative results that typically follow.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOOL-ish-nis',
                'etymology': 'From "foolish" (from "fool," ultimately from Latin "follis" meaning "bellows" or "empty bag") plus the suffix "-ness."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ of driving without insurance became apparent when he had the accident.',
                'memory_tip': 'Remember "FOOLISH-ness" - the quality of being a FOOL, showing lack of wisdom and making poor choices.'
            },
            'foosball': {
                'definition': 'Foosball is a table game simulating soccer, played with miniature figures attached to rotating rods that players manipulate to strike a ball toward goal areas. Also known as table soccer or table football in some regions, this game requires hand-eye coordination, quick reflexes, and strategic thinking. Foosball tables are common in game rooms, bars, and recreational facilities, providing entertainment and competitive play. The game combines skill, strategy, and social interaction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOOS-bawl',
                'etymology': 'From German "Fussball" meaning "football" (soccer), adapted for the table version of the game.',
                'language_origins': 'German',
                'example_sentence': 'The college students spent hours playing _______ in the dormitory game room.',
                'memory_tip': 'Remember "FOOS-ball" - table game that\'s a smaller version of FOOtball (soccer), played with spinning rods and tiny players.'
            },
            'foothills': {
                'definition': 'Foothills are low hills situated at the base of mountains or mountain ranges, forming the transitional zone between flat plains and higher mountain terrain. These gentle slopes and rolling hills typically mark the beginning of mountainous regions and often contain distinctive ecosystems and communities. Foothills provide scenic beauty, recreational opportunities, and often favorable conditions for agriculture and settlement. They represent the gradual rise from valley floors to mountain peaks.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FOOT-hilz',
                'etymology': 'Compound word combining "foot" (base or bottom) and "hills," referring to hills at the foot of mountains.',
                'language_origins': 'English',
                'example_sentence': 'The small town nestled in the _______ offered stunning views of the snow-capped mountains.',
                'memory_tip': 'Remember "FOOT-hills" - hills at the FOOT of mountains, the smaller slopes that lead up to bigger peaks.'
            },
            'foozle': {
                'definition': 'Foozle means to act clumsily or incompetently, particularly to bungle or botch something through careless or awkward handling. In golf, a foozle specifically refers to a mishit shot. The word describes actions that are poorly executed due to nervousness, lack of skill, or carelessness, resulting in disappointing or embarrassing outcomes. Foozle emphasizes the bumbling, awkward nature of failed attempts at tasks that should be straightforward.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FOO-zul',
                'etymology': 'Of uncertain origin, possibly imitative of clumsy action, first recorded in the late 19th century in golf contexts.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The nervous player managed to _______ his first shot, sending the ball into the rough.',
                'memory_tip': 'Remember "FOOZLE" - to fumble or bungle something, like when you FIZZLE out and make a clumsy mistake.'
            },
            'foppery': {
                'definition': 'Foppery refers to excessive attention to clothing, appearance, and mannerisms, particularly behavior characterized by vanity, affectation, and preoccupation with fashion and style. This noun describes the actions and attitudes of someone who is overly concerned with looking fashionable and sophisticated, often to the point of appearing ridiculous or superficial. Foppery suggests pretentious attention to appearance at the expense of substance or genuine character.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOP-er-ee',
                'etymology': 'From "fop" (a man excessively concerned with clothes and appearance) plus the suffix "-ery," from Middle English.',
                'language_origins': 'Middle English',
                'example_sentence': 'His constant _______ and obsession with designer clothes made him seem shallow to his colleagues.',
                'memory_tip': 'Remember "FOPP-ery" - the behavior of a fop who shops obsessively for fashion, caring more about appearance than substance.'
            },
            'forage': {
                'definition': 'Forage means to search for and gather food, especially in the wild, or refers to food for animals, particularly grass and other plants that livestock eat. As a verb, forage describes the act of seeking provisions by searching through available resources. As a noun, forage refers to the food itself, especially plant material consumed by grazing animals. The word emphasizes searching, gathering, and the natural process of finding sustenance in the environment.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FOR-ij',
                'etymology': 'From Old French "fourrage," from "fourrer" meaning "to fodder," related to "feurre" (straw).',
                'language_origins': 'Old French',
                'example_sentence': 'The deer would _______ in the meadow during the early morning hours.',
                'memory_tip': 'Remember "FORAGE" - to search FOR food in nature, like animals looking for AGE-old sources of nourishment.'
            },
            'forbid': {
                'definition': 'Forbid means to prohibit, ban, or refuse to allow something, typically by exercising authority or establishing rules. When someone forbids an action, they explicitly prevent it from happening through command, law, or strong disapproval. Forbidding implies the power to enforce prohibition and often carries consequences for disobedience. The word emphasizes authority, restriction, and the active prevention of unwanted actions or behaviors.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'fer-BID',
                'etymology': 'From Old English "forbeodan," combining "for-" (against) and "beodan" (to command), meaning "to command against."',
                'language_origins': 'Old English',
                'example_sentence': 'The school rules _______ students from using mobile phones during class time.',
                'memory_tip': 'Remember "for-BID" - to command against something, like making a BID for authority to stop unwanted actions.'
            },
            'forbidden': {
                'definition': 'Forbidden describes something that is prohibited, banned, or not allowed, typically by law, rule, or authority. When something is forbidden, it has been explicitly declared off-limits and engaging with it may result in punishment or consequences. Forbidden items, actions, or areas are those that people are specifically told to avoid or not access. The word carries connotations of transgression, danger, or moral boundaries that should not be crossed.',
                'part_of_speech': 'adjective, verb (past participle)',
                'pronunciation_guide': 'fer-BID-en',
                'etymology': 'Past participle of "forbid," from Old English "forbeodan," meaning "commanded against."',
                'language_origins': 'Old English',
                'example_sentence': 'Access to the _______ archive required special security clearance from the government.',
                'memory_tip': 'Remember "for-BIDD-en" - something that has been commanded against, HIDDEN away because it\'s not allowed.'
            },
            'forbivorous': {
                'definition': 'Forbivorous appears to be a rare or technical term that would describe organisms that feed on plants or plant material, similar to herbivorous but potentially with more specific botanical implications. This term might be used in scientific contexts to describe feeding behavior that focuses specifically on certain types of plant matter or plant structures. The word combines Latin roots related to plant feeding and consumption patterns.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'for-BIV-or-us',
                'etymology': 'Appears to combine Latin roots "forb-" (related to plants or herbs) and "-vorous" (feeding on), meaning "plant-eating."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ insects specialized in consuming the tender leaves of flowering plants.',
                'memory_tip': 'Remember "forb-VOROUS" - creatures that are voracious about eating FORBs (plants), specialized plant-eaters.'
            },
            'force': {
                'definition': 'Force can refer to physical strength, energy, or power used to cause motion or change, or to the act of compelling someone to do something against their will. In physics, force is any influence that causes an object to undergo acceleration, and is measured in units like newtons. Force can also describe military units, police departments, or any organized group with power. The word emphasizes strength, compulsion, influence, and the ability to cause change or movement.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FORS',
                'etymology': 'From Old French "force," from Latin "fortis" meaning "strong," emphasizing strength and power.',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The _______ of gravity pulls all objects toward the center of the Earth.',
                'memory_tip': 'Remember "FORCE" - power and strength that can change things, like a powerful source of energy and influence.'
            },
            'forcefully': {
                'definition': 'Forcefully means in a manner that shows strength, power, or intensity, or with vigorous and determined effort. When something is done forcefully, it is executed with considerable energy, conviction, or physical strength. The adverb can describe physical actions performed with power, or verbal expressions delivered with emphasis and determination. Forcefully suggests effectiveness through strength, intensity, and unwavering commitment.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FORS-ful-ee',
                'etymology': 'From "forceful" (combining "force" and the suffix "-ful") plus the adverb suffix "-ly."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'She argued _______ for the need to address climate change in the policy meeting.',
                'memory_tip': 'Remember "FORCE-fully" - doing something with full FORCE, using all your power and determination effectively.'
            },
            'forearm': {
                'definition': 'The forearm is the part of the human arm between the elbow and the wrist, containing two bones (the radius and ulna) and various muscles that control hand and finger movement. This anatomical region is essential for arm function, providing leverage for lifting and manipulating objects. The forearm contains muscles that control grip strength and fine motor movements of the hand. As a verb, forearm means to prepare or equip in advance for challenges or difficulties.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FOR-arm',
                'etymology': 'Compound word from "fore" (before, in front) and "arm," referring to the front part of the arm.',
                'language_origins': 'Old English',
                'example_sentence': 'The tennis player strengthened her _______ muscles to improve her backhand swing.',
                'memory_tip': 'Remember "FORE-arm" - the part of your arm that comes beFORE your hand, or to ARM yourself beFOREhand.'
            },
            'forearms': {
                'definition': 'Forearms is the plural form of forearm, referring to both the left and right parts of the arms between the elbows and wrists. These anatomical structures contain the muscles and bones necessary for complex hand and finger movements, grip strength, and arm rotation. Forearms are crucial for sports, manual labor, and daily activities requiring hand coordination. The word can also refer to multiple instances of preparing or equipping in advance.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'FOR-armz',
                'etymology': 'Plural form of "forearm," from "fore" (before) and "arm."',
                'language_origins': 'Old English',
                'example_sentence': 'The rock climber\'s _______ were muscular from years of gripping challenging holds.',
                'memory_tip': 'Remember "FORE-arms" - both arms from elbow to wrist, or arming yourself beforehand with multiple preparations.'
            },
            'forefend': {
                'definition': 'Forefend means to ward off, prevent, or protect against something undesirable or dangerous, typically used in the expression "God forefend" or "Heaven forefend" to express hope that something terrible won\'t happen. This somewhat archaic verb suggests active protection or the prevention of harm through divine intervention or careful precaution. Forefend emphasizes protection, prevention, and the turning away of potential threats or misfortunes.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'for-FEND',
                'etymology': 'From "fore-" (before, in advance) and "fend" (to defend), meaning "to defend in advance" or "to prevent."',
                'language_origins': 'English',
                'example_sentence': 'Heaven _______ that such a tragedy should befall their family again.',
                'memory_tip': 'Remember "fore-FEND" - to FEND off problems beFORE they happen, preventing harm through advance protection.'
            },
            'forensics': {
                'definition': 'Forensics refers to the scientific methods and techniques used to investigate crimes, analyze evidence, and solve legal cases. This field applies various scientific disciplines like biology, chemistry, physics, and computer science to examine physical evidence and determine facts in criminal and civil investigations. Forensics can also refer to the art of argumentation and debate, particularly in educational contexts. The work helps establish truth through scientific analysis and logical reasoning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fuh-REN-ziks',
                'etymology': 'From Latin "forensis" meaning "of or relating to the forum" (where legal cases were heard), from "forum" (public place).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ team analyzed DNA evidence to identify the suspect in the crime.',
                'memory_tip': 'Remember "fo-RENSICS" - science FOR legal cases, using scientific methods to uncover the truth in court.'
            },
            'foresight': {
                'definition': 'Foresight is the ability to predict or anticipate future events, consequences, or needs, and to plan accordingly. This valuable skill involves thinking ahead, considering potential outcomes, and making preparations based on likely scenarios. People with good foresight can avoid problems, take advantage of opportunities, and make better decisions by considering long-term implications. Foresight combines wisdom, planning ability, and the capacity to see beyond immediate circumstances.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOR-syt',
                'etymology': 'From "fore-" (before, in advance) and "sight," literally meaning "seeing beforehand."',
                'language_origins': 'English',
                'example_sentence': 'Her _______ in investing early in technology stocks paid off handsomely over the decades.',
                'memory_tip': 'Remember "FORE-sight" - the ability to see FORE (ahead) into the future, planning with advance vision.'
            },
            'forestallment': {
                'definition': 'Forestallment is the action of preventing, hindering, or thwarting something by taking advance action. This noun describes the process of getting ahead of potential problems, opponents, or events in order to prevent them from occurring or succeeding. Forestallment involves anticipatory action designed to block, delay, or redirect unwanted outcomes. The word emphasizes proactive measures taken to prevent undesirable developments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'for-STAWL-ment',
                'etymology': 'From "forestall" (from "fore-" meaning "before" and "stall" meaning "to stop") plus the suffix "-ment."',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ of the competitor\'s product launch gave the company time to improve their own offering.',
                'memory_tip': 'Remember "fore-STALL-ment" - the act of STALLing something beFORE it happens, preventing unwanted events.'
            },
            'foretell': {
                'definition': 'Foretell means to predict, prophesy, or announce what will happen in the future, typically through supernatural insight, careful observation, or analysis of current trends. When someone foretells events, they claim to know what will occur before it actually happens. This verb suggests both prediction and proclamation, often carrying connotations of prophecy, divination, or exceptional insight into future possibilities.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'for-TEL',
                'etymology': 'From "fore-" (before, in advance) and "tell," meaning "to tell beforehand" or "to predict."',
                'language_origins': 'Old English',
                'example_sentence': 'The ancient oracle claimed to _______ the outcome of the war through divine visions.',
                'memory_tip': 'Remember "fore-TELL" - to TELL about events beFORE they happen, predicting the future through insight.'
            },
            'forever': {
                'definition': 'Forever means for all future time, without end, or for an extremely long period that seems endless. This adverb expresses the concept of eternity, permanence, or duration that continues indefinitely into the future. Forever can describe lasting commitments, enduring love, permanent conditions, or situations that seem to last much longer than expected. The word emphasizes timelessness, infinity, and the absence of an ending point.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'fer-EV-er',
                'etymology': 'From "for" and "ever," literally meaning "for all time" or "for eternity."',
                'language_origins': 'Old English',
                'example_sentence': 'They promised to love each other _______ and sealed their vows with wedding rings.',
                'memory_tip': 'Remember "for-EVER" - FOR all time, EVER lasting, continuing without end into the future.'
            },
            'forfeit': {
                'definition': 'Forfeit means to give up or lose something as a penalty for wrongdoing, failure to meet obligations, or as a consequence of breaking rules. As a noun, forfeit refers to the thing that is given up or the penalty itself. When someone forfeits something, they surrender their right to keep it, usually because they have violated terms, failed to perform, or been found guilty of misconduct. The word emphasizes loss through rule-breaking or failure.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FOR-fit',
                'etymology': 'From Old French "forfet," meaning "transgression" or "penalty," from "forfaire" (to act beyond the law).',
                'language_origins': 'Old French',
                'example_sentence': 'The team had to _______ the game when they couldn\'t field enough players.',
                'memory_tip': 'Remember "FOR-feit" - to give up something because you\'re not FIT FOR keeping it, losing due to rule violations.'
            },
            'forfend': {
                'definition': 'Forfend is an alternative spelling of "forefend," meaning to ward off, prevent, or protect against something undesirable. This verb is often used in the expressions "God forfend" or "Heaven forfend" to express fervent hope that something bad won\'t happen. Forfend suggests active protection or divine intervention to prevent harm or misfortune. The word emphasizes prevention, protection, and the turning away of threats.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'for-FEND',
                'etymology': 'Alternative spelling of "forefend," from "for-" (away) and "fend" (to defend).',
                'language_origins': 'English',
                'example_sentence': 'God _______ that we should ever face such hardship again.',
                'memory_tip': 'Remember "for-FEND" - to FEND FOR protection against harm, defending against bad things happening.'
            },
            'forgeable': {
                'definition': 'Forgeable describes something that can be shaped, formed, or worked, particularly metals that can be hammered, bent, or molded when heated. In metallurgy, forgeable materials are those that can withstand the forging process without cracking or breaking. The word can also describe documents or signatures that are capable of being counterfeited or falsified. Forgeable emphasizes malleability, workability, and the capacity to be shaped or altered.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FOR-juh-bul',
                'etymology': 'From "forge" (from Latin "fabrica" meaning "workshop") plus the suffix "-able," meaning "capable of being forged."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ steel could be shaped into complex tools when heated to the proper temperature.',
                'memory_tip': 'Remember "FORGE-able" - able to be worked in a FORGE, metals that can be shaped and formed when heated.'
            },
            'forgive': {
                'definition': 'Forgive means to stop feeling angry or resentful toward someone who has done something wrong, or to cancel a debt or obligation. When someone forgives, they choose to let go of negative feelings and the desire for revenge or punishment. Forgiveness involves pardoning mistakes, showing mercy, and often rebuilding relationships after conflicts. The act emphasizes compassion, understanding, and the decision to move past hurt or wrongdoing.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'fer-GIV',
                'etymology': 'From Old English "forgiefan," combining "for-" (completely) and "giefan" (to give), meaning "to give completely."',
                'language_origins': 'Old English',
                'example_sentence': 'She decided to _______ her brother for breaking her favorite vase, knowing it was an accident.',
                'memory_tip': 'Remember "for-GIVE" - to completely GIVE up anger and resentment, offering mercy and understanding instead.'
            },
            'form': {
                'definition': 'Form can refer to the shape, structure, or appearance of something, or to the process of creating, shaping, or organizing. As a noun, form describes the visible shape or configuration of objects, the structure of organizations, or types of documents. As a verb, form means to create, establish, or give shape to something. The word emphasizes shape, structure, creation, and the process of bringing things into existence or organization.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FORM',
                'etymology': 'From Old French "forme," from Latin "forma" meaning "shape," "figure," or "appearance."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The clay began to take _______ as the potter shaped it on the spinning wheel.',
                'memory_tip': 'Remember "FORM" - the shape something takes, or the action of FORMing and creating structure from raw materials.'
            },
            'formalise': {
                'definition': 'Formalise is the British spelling of "formalize," meaning to make something official, systematic, or comply with established rules and procedures. When something is formalised, it is given official status, structured according to proper protocols, or made to conform to accepted standards. This process involves establishing clear procedures, documenting agreements, or creating official recognition for previously informal arrangements.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FOR-mul-yz',
                'etymology': 'British spelling of "formalize," from "formal" (from Latin "formalis") plus the suffix "-ise."',
                'language_origins': 'Latin',
                'example_sentence': 'The company decided to _______ the mentorship program with official guidelines and documentation.',
                'memory_tip': 'Remember "FORMAL-ise" - to make something FORMAL and official, following proper rules and procedures (British spelling).'
            },
            'formalize': {
                'definition': 'Formalize means to make something official, systematic, or give it a definite structure according to established rules and procedures. When something is formalized, it transitions from informal or unofficial status to being officially recognized, documented, and regulated. This process involves creating clear guidelines, establishing proper procedures, or gaining official approval for arrangements that were previously casual or unstructured.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FOR-mul-yz',
                'etymology': 'From "formal" (from Latin "formalis" meaning "relating to form") plus the suffix "-ize."',
                'language_origins': 'Latin',
                'example_sentence': 'The two countries agreed to _______ their trade relationship with a comprehensive agreement.',
                'memory_tip': 'Remember "FORMAL-ize" - to make something FORMAL and official, creating structure and rules (American spelling).'
            }
        }
        
        if word.lower() in batch_070_data:
            return batch_070_data[word.lower()]
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
        
        print("Batch 070 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch070Processor()
    
    input_file = "output/batch_070_words.csv"
    output_file = "output/batch_070_processed.csv"
    
    processor.process_batch(input_file, output_file)