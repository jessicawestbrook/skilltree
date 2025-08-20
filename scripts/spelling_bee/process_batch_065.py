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

class Batch065Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def detect_parsing_errors(self, word: str) -> Tuple[bool, bool, List[str]]:
        errors = []
        combined_detected = False
        incomplete_detected = False
        
        # Check for combined words (specific to this batch)
        combined_word_patterns = {
            'facebook': ['This appears to be the brand name rather than a combined word error'],
            'fadeawayfallacy': ['fadeaway', 'fallacy'],
            'fairesbrinz': ['corrupted word, possibly "fairness" or similar'],
            'faminelinoleum': ['famine', 'linoleum']
        }
        
        if word.lower() in combined_word_patterns:
            if word.lower() != 'facebook':  # Facebook is a legitimate brand name
                combined_detected = True
                if word.lower() == 'fairesbrinz':
                    errors.append(f"Corrupted word: \"{word}\" appears to be corrupted or malformed. This is likely a PDF parsing error.")
                else:
                    errors.append(f"Combined word error: \"{word}\" appears to be {' + '.join(combined_word_patterns[word.lower()])} merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.")
        
        return combined_detected, incomplete_detected, errors
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge."""
        
        batch_065_data = {
            'fabric': {
                'definition': 'Fabric is a material made by weaving, knitting, crocheting, or bonding fibers together to create a flexible sheet or textile. Fabrics can be made from natural fibers such as cotton, wool, silk, or linen, or from synthetic materials like polyester, nylon, or rayon. The term can also refer metaphorically to the fundamental structure or framework of something, such as "the fabric of society." In construction, fabric can describe the physical structure of a building. The word encompasses both the material itself and the process of its creation, representing one of humanity\'s most important technological achievements.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAB-rik',
                'etymology': 'From Latin "fabrica," meaning "workshop" or "trade," derived from "faber" meaning "craftsman" or "smith." Originally referred to the place where things were made.',
                'language_origins': 'Latin',
                'example_sentence': 'The quilter carefully selected a soft cotton _______ with tiny floral patterns for the baby blanket.',
                'memory_tip': 'Remember "FAB-ric" - think of FABulous craftsmen creating RIch textiles in their workshops.'
            },
            'fabulist': {
                'definition': 'A fabulist is a person who creates, tells, or collects fables, which are short stories that typically feature animals or inanimate objects as characters and convey moral lessons. Fabulists craft narratives that use allegory and symbolism to teach ethical principles or life lessons in an engaging, memorable way. The term can also refer to someone who tells elaborate lies or fabricated stories, though this usage is less common. Famous fabulists include Aesop, whose animal fables have been told for centuries, and Jean de La Fontaine, who adapted and expanded upon classical fables.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAB-yuh-list',
                'etymology': 'From Latin "fabula" meaning "story" or "tale," combined with the suffix "-ist" meaning "one who practices." Related to "fable."',
                'language_origins': 'Latin',
                'example_sentence': 'The renowned _______ spent years collecting folk tales from different cultures to create a comprehensive book of moral stories.',
                'memory_tip': 'Remember "FABU-list" - someone who makes a LIST of FABUlous fables and stories.'
            },
            'facade': {
                'definition': 'A facade is the front face or exterior wall of a building, especially the principal front face that serves as the main architectural feature. In a broader sense, facade refers to any superficial appearance or false front that conceals the true nature of something underneath. When used metaphorically, it describes a deceptive outward appearance that masks reality, such as maintaining a facade of happiness while feeling sad inside. Architectural facades are often designed to be decorative and impressive, representing the building\'s most important visual element to the public.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fuh-SAHD',
                'etymology': 'From French "façade," ultimately from Italian "facciata," meaning "face of a building," derived from Latin "facies" meaning "face."',
                'language_origins': 'French, Italian, Latin',
                'example_sentence': 'Behind the cheerful _______ she presented at work, Sarah was struggling with personal difficulties.',
                'memory_tip': 'Remember "fa-CADE" - think of the FACE of a building, or someone putting on a fake FACE to hide their true feelings.'
            },
            'face': {
                'definition': 'Face refers to the front part of the human head, containing the eyes, nose, mouth, and other features that form a person\'s distinctive appearance. As a verb, face means to confront, deal with, or turn toward something. The word has numerous idiomatic uses: losing face means losing dignity or respect, while saving face means preserving one\'s reputation. Face can also refer to the surface of objects, such as the face of a clock or the face of a mountain. In various contexts, it represents confrontation, appearance, or the act of addressing challenges directly.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FAYS',
                'etymology': 'From Old French "face," from Latin "facies" meaning "form," "figure," or "appearance." Related to "facere" meaning "to make."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'She took a deep breath and decided to _______ her fears by signing up for the public speaking class.',
                'memory_tip': 'Remember "FACE" - we show our FACE when we FACE challenges head-on, confronting them directly.'
            },
            'facebook': {
                'definition': 'Facebook is a social networking platform and technology company founded by Mark Zuckerberg in 2004. Originally created for college students, it expanded to become one of the world\'s largest social media platforms, allowing users to connect with friends, share content, and communicate online. The platform enables users to create profiles, post updates, share photos and videos, and interact with content from others in their network. Facebook has fundamentally changed how people communicate and share information globally, though it has also faced scrutiny regarding privacy and misinformation.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'FAYS-book',
                'etymology': 'Compound word combining "face" (referring to a person\'s appearance or identity) and "book" (referring to a directory or record), originally inspired by physical directories of student photos at universities.',
                'language_origins': 'English',
                'example_sentence': 'Many people use _______ to stay connected with family members who live far away.',
                'memory_tip': 'Remember "FACE-book" - like a book full of people\'s FACES, connecting them in a social network.'
            },
            'faced': {
                'definition': 'Faced is the past tense of the verb "face," meaning to have confronted, encountered, or dealt with something directly. When someone has faced a challenge, they have met it head-on rather than avoiding it. The word can also describe physical positioning, such as having turned toward or looked in a particular direction. In construction or manufacturing, faced can refer to having applied a surface layer or covering to something. The term implies direct engagement rather than avoidance or postponement.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'FAYST',
                'etymology': 'Past tense of "face," from Old French "face," from Latin "facies." The past tense ending follows standard English verb conjugation patterns.',
                'language_origins': 'Latin, Old French, English',
                'example_sentence': 'After months of preparation, the team finally _______ their biggest challenge when they presented to the board of directors.',
                'memory_tip': 'Remember "FACED" - like someone who has FACED their problems with their FACE forward, not running away.'
            },
            'facetious': {
                'definition': 'Facetious describes someone who treats serious or sensitive matters with inappropriate humor, flippancy, or lack of respect. When someone is being facetious, they are making light of situations that deserve more serious attention, often through sarcasm, jokes, or dismissive comments. This behavior can be annoying or hurtful to others, especially when dealing with important or emotional topics. Facetious remarks are characterized by their inappropriate timing and tendency to minimize the significance of serious matters.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fuh-SEE-shus',
                'etymology': 'From Latin "facetiosus," meaning "witty" or "humorous," derived from "facetia" meaning "jest" or "witticism." Originally had a more positive connotation.',
                'language_origins': 'Latin',
                'example_sentence': 'His _______ comments during the serious discussion about budget cuts showed poor judgment and upset his colleagues.',
                'memory_tip': 'Remember "fa-CEE-tious" - someone who thinks they\'re being witty but others CEE them as inappropriate and annoying.'
            },
            'facile': {
                'definition': 'Facile describes something that is achieved with ease but often lacks depth, substance, or careful consideration. When something is facile, it appears simple on the surface but may be overly simplistic or superficial. The word can describe solutions, explanations, or responses that seem easy but fail to address the complexity of a situation. While facile can sometimes simply mean "easy to do," it often carries a negative connotation, suggesting that something is too easy or lacks the thoroughness required for a proper solution.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAS-ahyl',
                'etymology': 'From Latin "facilis," meaning "easy to do," derived from "facere" meaning "to do" or "to make." Related to "facility" and "facilitate."',
                'language_origins': 'Latin',
                'example_sentence': 'The politician\'s _______ answers to complex economic questions failed to convince the experienced journalists.',
                'memory_tip': 'Remember "FACILE" - sounds like "FACILE" (easy), but often means TOO easy, lacking depth like a superficial FOSSIL.'
            },
            'facsimile': {
                'definition': 'A facsimile is an exact copy or reproduction of something, particularly documents, manuscripts, or artworks. The term is most commonly associated with fax machines, which transmit facsimile copies of documents over telephone lines. In broader usage, facsimile refers to any precise reproduction that maintains the appearance and details of the original. Museums often display facsimiles of fragile historical documents to allow public viewing while preserving the originals. The word emphasizes accuracy and fidelity to the source material.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fak-SIM-uh-lee',
                'etymology': 'From Latin "fac simile," literally meaning "make similar" or "make alike." "Fac" is from "facere" (to make) and "simile" means "similar."',
                'language_origins': 'Latin',
                'example_sentence': 'The museum displayed a _______ of the ancient manuscript so visitors could examine the text without damaging the original.',
                'memory_tip': 'Remember "fac-SIMILE" - FAC (make) it look exactly SIMILAR to the original, an exact copy.'
            },
            'fact': {
                'definition': 'A fact is a piece of information that is objectively true and can be verified through observation, measurement, or documentation. Facts are distinguished from opinions, beliefs, or interpretations because they represent reality as it exists, regardless of personal views or feelings. In academic and scientific contexts, facts form the foundation for knowledge, research, and decision-making. Legal proceedings rely heavily on establishing facts to determine truth. The word emphasizes objectivity, verifiability, and the distinction between what is real and what is subjective.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAKT',
                'etymology': 'From Latin "factum," meaning "something done" or "deed," past participle of "facere" meaning "to do" or "to make."',
                'language_origins': 'Latin',
                'example_sentence': 'It is a scientific _______ that water boils at 100 degrees Celsius at standard atmospheric pressure.',
                'memory_tip': 'Remember "FACT" - something that has been done or made real, not just an opinion but actual truth.'
            },
            'factitious': {
                'definition': 'Factitious describes something that is artificially created, contrived, or not genuine in nature. When something is factitious, it has been deliberately manufactured or constructed rather than occurring naturally or spontaneously. In psychology, factitious disorders involve the intentional production of symptoms. In general usage, factitious can describe artificial situations, forced emotions, or contrived circumstances that lack authenticity. The word emphasizes the deliberate, artificial nature of something that might otherwise appear natural or genuine.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fak-TISH-us',
                'etymology': 'From Latin "facticius," meaning "made by art" or "artificial," derived from "facere" meaning "to make." Related to "faction" and "factory."',
                'language_origins': 'Latin',
                'example_sentence': 'The diplomat\'s _______ smile during the tense negotiations fooled no one in the room.',
                'memory_tip': 'Remember "fact-ITIOUS" - not based on real FACTS but artificially made, like nutritious food that\'s fake.'
            },
            'facto': {
                'definition': 'Facto is a Latin term meaning "in fact" or "by the deed," commonly used in legal and formal contexts as part of the phrase "de facto," which means "in reality" or "in practice." While not typically used as a standalone English word, facto appears in various Latin legal phrases that have been adopted into English usage. It emphasizes the actual state of affairs rather than what is officially or theoretically supposed to be the case. The term is fundamental to distinguishing between legal theory and practical reality.',
                'part_of_speech': 'Latin term used in English legal contexts',
                'pronunciation_guide': 'FAK-toh',
                'etymology': 'From Latin "facto," ablative case of "factum" meaning "deed" or "fact," derived from "facere" meaning "to do" or "to make."',
                'language_origins': 'Latin',
                'example_sentence': 'The company became the de _______ leader in the industry through aggressive expansion, even without official recognition.',
                'memory_tip': 'Remember "FACTO" - from Latin meaning by the FACT or deed, what actually happens in practice.'
            },
            'factoid': {
                'definition': 'A factoid is a brief, interesting piece of information that is presented as fact but may be of questionable accuracy or significance. Originally coined to mean false or unverified information presented as fact, the term has evolved to also describe trivial but true facts, often used in media or casual conversation. Factoids are typically attention-grabbing snippets of information that are easy to remember and share but may lack proper context or verification. They often appear in trivia, social media posts, or casual discussions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAK-toid',
                'etymology': 'Coined in 1973 by author Norman Mailer, combining "fact" with the suffix "-oid" meaning "resembling" or "like," literally meaning "fact-like."',
                'language_origins': 'English (neologism)',
                'example_sentence': 'The magazine was full of interesting _______ about celebrities, though readers questioned the accuracy of some claims.',
                'memory_tip': 'Remember "FACT-oid" - something that looks like a FACT but might be as fake as an android, not quite real.'
            },
            'factorial': {
                'definition': 'Factorial is a mathematical concept representing the product of all positive integers from 1 up to a given number. Denoted by an exclamation mark (!), the factorial of n (written as n!) equals n × (n-1) × (n-2) × ... × 2 × 1. For example, 5! = 5 × 4 × 3 × 2 × 1 = 120. Factorials are fundamental in combinatorics, probability theory, and various mathematical calculations involving permutations and combinations. They grow extremely rapidly, making them useful for calculating the number of possible arrangements or selections.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'fak-TOR-ee-ul',
                'etymology': 'From "factor" (from Latin "factor" meaning "maker" or "doer") plus the suffix "-ial." The mathematical usage developed in the 19th century.',
                'language_origins': 'Latin, English',
                'example_sentence': 'To calculate the number of ways to arrange five books on a shelf, you need to compute five _______.',
                'memory_tip': 'Remember "FACTOR-ial" - you FACTOR in every number by multiplying them all together, creating a factorial.'
            },
            'faculty': {
                'definition': 'Faculty refers to the teaching staff of a university, college, or school, collectively representing the academic professionals responsible for instruction and research. The term can also describe a particular department or division within an educational institution, such as the faculty of medicine or faculty of arts. More broadly, faculty means an inherent ability, power, or capacity that someone possesses, such as mental faculties or the faculty of speech. In this sense, it refers to natural or developed capabilities that enable specific functions or activities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAK-ul-tee',
                'etymology': 'From Latin "facultas," meaning "capability," "power," or "opportunity," derived from "facilis" meaning "easy" and ultimately from "facere" meaning "to do."',
                'language_origins': 'Latin',
                'example_sentence': 'The university\'s _______ voted unanimously to implement the new curriculum changes proposed by the academic committee.',
                'memory_tip': 'Remember "FACUL-ty" - the FACULty has the ability and power to teach, like having multiple FACULties or capabilities.'
            },
            'facundity': {
                'definition': 'Facundity is the quality of being eloquent, fluent, or skilled in speaking or writing. Someone who possesses facundity demonstrates exceptional ability to express ideas clearly, persuasively, and with considerable verbal dexterity. The term suggests not just fluency but also sophistication and effectiveness in communication. Facundity implies both natural talent and cultivated skill in the use of language, enabling someone to communicate complex ideas in compelling and articulate ways. It is often associated with orators, writers, and other professionals who rely on exceptional communication skills.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fuh-KUN-di-tee',
                'etymology': 'From Latin "facunditas," meaning "eloquence" or "fluency," derived from "facundus" meaning "eloquent," related to "fari" meaning "to speak."',
                'language_origins': 'Latin',
                'example_sentence': 'The lawyer\'s remarkable _______ in the courtroom helped her win several high-profile cases through persuasive arguments.',
                'memory_tip': 'Remember "fa-CUNDity" - someone with great speaking ability, so CUNNING with words that they have exceptional verbal facility.'
            },
            'fadeaway': {
                'definition': 'Fadeaway refers to a basketball shooting technique where the player leans backward while shooting to create space from the defender, making the shot more difficult to block. This move involves jumping and simultaneously leaning away from the basket, requiring exceptional balance and skill. The term can also describe anything that gradually diminishes or disappears, such as a fadeaway jump shot in basketball or a fadeaway effect in music. In broader usage, fadeaway suggests a gradual decline or reduction rather than an abrupt ending.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAYD-uh-way',
                'etymology': 'Compound word combining "fade" (to gradually disappear) and "away" (indicating direction or removal), reflecting the backward motion of the basketball shot.',
                'language_origins': 'English',
                'example_sentence': 'Michael Jordan\'s signature _______ jump shot was nearly impossible for defenders to block due to his backward lean.',
                'memory_tip': 'Remember "FADE-away" - the player FADES backward and shoots AWAY from the defender, creating space.'
            },
            'fado': {
                'definition': 'Fado is a traditional Portuguese music genre characterized by mournful melodies and lyrics that often express themes of longing, loss, and nostalgia. Typically performed by a single vocalist accompanied by classical and Portuguese guitars, fado is known for its emotional intensity and melancholic atmosphere. The music often reflects the Portuguese concept of "saudade," a deep emotional state of longing for something absent. Fado has been recognized by UNESCO as an Intangible Cultural Heritage of Humanity, highlighting its cultural significance to Portuguese identity and heritage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAH-doo',
                'etymology': 'From Portuguese "fado," meaning "fate" or "destiny," derived from Latin "fatum." The music expresses the acceptance of fate and life\'s sorrows.',
                'language_origins': 'Portuguese, Latin',
                'example_sentence': 'The haunting _______ performance in the small Lisbon tavern moved the audience to tears with its raw emotion.',
                'memory_tip': 'Remember "FADO" - FAtal DOleful music that expresses fate and destiny through sad, beautiful Portuguese songs.'
            },
            'failure': {
                'definition': 'Failure is the lack of success in achieving a desired goal, outcome, or standard. It represents the state of not meeting expectations, requirements, or intended results despite effort or attempt. Failure can occur in various contexts, including academic, professional, personal, or mechanical situations. While often viewed negatively, failure can also be a valuable learning experience that provides insights and motivation for improvement. The concept encompasses both the act of failing and the resulting condition or consequence of unsuccessful attempts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAYL-yer',
                'etymology': 'From Old French "faillir" meaning "to fail" or "to be lacking," ultimately from Latin "fallere" meaning "to deceive" or "to be false."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'Despite the initial _______ of her first business venture, she learned valuable lessons that led to future success.',
                'memory_tip': 'Remember "FAIL-ure" - when you FAIL to reach your goal, it results in failure, but you can learn from it.'
            },
            'faint': {
                'definition': 'Faint can describe something that is weak, dim, or barely perceptible, such as a faint sound, light, or smell. As a verb, faint means to lose consciousness temporarily, usually due to insufficient blood flow to the brain. When describing qualities or sensations, faint suggests something that is present but very subtle or difficult to detect. The word can also describe someone who is weak, timid, or lacking in courage, as in "faint of heart." In all uses, faint implies a lack of strength, intensity, or clarity.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'FAYNT',
                'etymology': 'From Old French "feint," past participle of "feindre" meaning "to feign" or "to pretend," from Latin "fingere" meaning "to shape" or "to pretend."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'She heard a _______ whisper coming from the next room, barely audible through the thick walls.',
                'memory_tip': 'Remember "FAINT" - when something is FAINT, it\'s so weak you might need to FEINT (pretend) to see or hear it clearly.'
            },
            'faipule': {
                'definition': 'Faipule is a Samoan term referring to a member of the Samoan Parliament or Legislative Assembly. In the traditional Samoan political system, faipule are elected representatives who serve in the national legislature. The position combines traditional Samoan leadership concepts with modern parliamentary democracy. Faipule are typically chosen from among matai (traditional chiefs) and are responsible for representing their constituencies in national government decisions. The term reflects the unique blend of traditional Samoan culture and contemporary democratic governance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fahy-POO-lay',
                'etymology': 'From Samoan "faipule," combining "fai" meaning "to do" or "to make" and "pule" meaning "authority" or "power."',
                'language_origins': 'Samoan',
                'example_sentence': 'The _______ addressed the assembly about important legislation affecting rural communities in Samoa.',
                'memory_tip': 'Remember "fai-PULE" - someone who FAI (does/makes) decisions with PULE (power/authority) in Samoan government.'
            },
            'fair': {
                'definition': 'Fair has multiple meanings depending on context. As an adjective, it means just, equitable, or reasonable, treating people without favoritism or discrimination. Fair can also describe something that is satisfactory but not excellent, or weather that is pleasant and clear. When referring to appearance, fair means light in color, particularly skin or hair. As a noun, fair refers to a public event featuring entertainment, food, and often commercial exhibitions. The word emphasizes concepts of justice, equality, and reasonableness.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FAIR',
                'etymology': 'From Old English "fæger" meaning "beautiful" or "pleasant," related to Old Norse "fagr." The "just/equitable" meaning developed in Middle English.',
                'language_origins': 'Old English, Old Norse',
                'example_sentence': 'The judge made a _______ decision that satisfied both parties in the dispute.',
                'memory_tip': 'Remember "FAIR" - it\'s FAIR to treat everyone equally, and fair weather is pleasant and clear.'
            },
            'faire': {
                'definition': 'Faire is a French word meaning "to do" or "to make," commonly encountered in English in phrases borrowed from French. In historical contexts, it appears in terms like "laissez-faire," meaning "let do" or "let it be," referring to a hands-off approach, particularly in economics. Faire can also refer to a Renaissance faire, a themed entertainment event recreating medieval or Renaissance periods. In these contexts, the French spelling is retained to maintain the cultural or historical flavor of the expression.',
                'part_of_speech': 'French verb used in English contexts',
                'pronunciation_guide': 'FAIR',
                'etymology': 'From Old French "faire," from Latin "facere" meaning "to do" or "to make." Related to English words like "fact" and "factory."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The economic policy followed a laissez-_______ approach, allowing markets to operate without government interference.',
                'memory_tip': 'Remember "FAIRE" - the French word for "to do," sounds like FAIR but means making or doing something.'
            },
            'fait': {
                'definition': 'Fait is a French word meaning "fact" or "deed," most commonly encountered in English in the phrase "fait accompli," which means "accomplished fact" or something that has already been done and cannot be changed. When something is described as a fait accompli, it refers to an irreversible action or decision that others must accept, regardless of their preferences. The term is often used in diplomatic, political, or business contexts to describe situations where decisions have been made unilaterally, presenting others with completed actions rather than opportunities for input.',
                'part_of_speech': 'French noun used in English contexts',
                'pronunciation_guide': 'FAY',
                'etymology': 'From Old French "fait," from Latin "factum" meaning "something done" or "deed," past participle of "facere" meaning "to do."',
                'language_origins': 'French, Latin',
                'example_sentence': 'By the time the committee met, the CEO had already signed the contract, presenting them with a _______ accompli.',
                'memory_tip': 'Remember "FAIT" - sounds like FATE, representing a FACT or deed that\'s already been done and can\'t be changed.'
            },
            'faith': {
                'definition': 'Faith is a strong belief, trust, or confidence in someone or something, often without requiring complete proof or evidence. In religious contexts, faith represents belief in divine beings, spiritual principles, or religious teachings. More broadly, faith describes trust or reliance on people, institutions, or concepts. It can mean loyalty, fidelity, or steadfast commitment to principles or relationships. Faith often involves acceptance of things that cannot be empirically proven but are held to be true through personal conviction, tradition, or spiritual experience.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAYTH',
                'etymology': 'From Old French "feid," from Latin "fides" meaning "trust," "belief," or "confidence." Related to "fidelity" and "confide."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'Despite the challenges, she maintained her _______ that the team would successfully complete the project.',
                'memory_tip': 'Remember "FAITH" - you have FAITH when you believe something will work out, trusting even without complete proof.'
            },
            'fajitas': {
                'definition': 'Fajitas are a Tex-Mex dish consisting of grilled meat, typically beef or chicken, served with sautéed onions and bell peppers, accompanied by tortillas and various toppings such as salsa, guacamole, sour cream, and cheese. Diners typically assemble their own tacos by placing the meat and vegetables in tortillas and adding desired toppings. The dish originated in the ranch lands of South and West Texas and has become popular throughout North America. Fajitas are often served on a sizzling cast-iron plate, creating an dramatic presentation.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'fuh-HEE-tahs',
                'etymology': 'From Mexican Spanish "fajita," diminutive of "faja" meaning "belt" or "sash," referring to the cut of meat from the skirt steak area.',
                'language_origins': 'Spanish',
                'example_sentence': 'The restaurant\'s sizzling chicken _______ arrived at our table with warm tortillas and fresh guacamole.',
                'memory_tip': 'Remember "fa-HEE-tas" - the sizzling sound "HEE" when the hot _______ are served on the iron plate.'
            },
            'fallacy': {
                'definition': 'A fallacy is a mistaken belief, flawed reasoning, or error in logic that undermines the validity of an argument or conclusion. Fallacies can be formal, involving structural problems in logical reasoning, or informal, involving problems with content or context. Common fallacies include ad hominem attacks, straw man arguments, and false dichotomies. Understanding fallacies is crucial for critical thinking, as they often appear in debates, advertising, and everyday discussions. Recognizing fallacies helps people evaluate arguments more effectively and avoid being misled by faulty reasoning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAL-uh-see',
                'etymology': 'From Latin "fallacia," meaning "deceptive appearance" or "deceit," derived from "fallax" meaning "deceptive," related to "fallere" meaning "to deceive."',
                'language_origins': 'Latin',
                'example_sentence': 'The politician\'s argument contained a logical _______ that made his conclusion invalid despite sounding convincing.',
                'memory_tip': 'Remember "FALL-acy" - a logical error that makes an argument FALL apart, like falling for deceptive reasoning.'
            },
            'fallow': {
                'definition': 'Fallow describes farmland that is left unplanted during a growing season to allow the soil to rest and recover its fertility. This agricultural practice helps restore nutrients to the soil and can help control weeds and pests. Figuratively, fallow can describe any period of inactivity or rest that allows for restoration or preparation for future productivity. As a color, fallow refers to a pale yellowish-brown shade, similar to the color of unplanted earth. The concept emphasizes the value of rest and renewal in maintaining long-term productivity.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FAL-oh',
                'etymology': 'From Old English "fealgian" meaning "to break up land for sowing," related to Old English "fealh" meaning "harrow." The agricultural term has ancient roots.',
                'language_origins': 'Old English',
                'example_sentence': 'The farmer decided to leave the north field _______ this year to restore its nutrients for next season\'s crop.',
                'memory_tip': 'Remember "FALLOW" - farmland that FAllows (rests) to be empty, allowing soil to recover and become more productive.'
            },
            'faltered': {
                'definition': 'Faltered is the past tense of "falter," meaning to hesitate, waver, or lose strength, confidence, or momentum. When someone has faltered, they have experienced a moment of weakness, uncertainty, or stumbling, either literally or figuratively. This can apply to physical movement, such as stumbling while walking, or to abstract concepts like speech, confidence, or progress toward goals. Faltering suggests a temporary loss of steadiness or determination rather than complete failure, often implying the possibility of recovery.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'FAWL-terd',
                'etymology': 'From Middle English "falteren," possibly related to "fold" or from Old Norse "faltrask" meaning "to be encumbered." The exact origin is uncertain.',
                'language_origins': 'Middle English, possibly Old Norse',
                'example_sentence': 'Her voice _______ with emotion as she tried to deliver the difficult news to her family.',
                'memory_tip': 'Remember "FALTER-ed" - someone who FALLs short or stumbles, their strength or confidence has FAltered (weakened).'
            },
            'famed': {
                'definition': 'Famed means well-known, celebrated, or famous for particular qualities, achievements, or characteristics. When someone or something is famed, they have acquired a reputation that extends beyond their immediate surroundings, often for excellence, skill, or notable accomplishments. The word suggests a positive reputation based on merit or achievement rather than notoriety. Famed implies widespread recognition and respect, often built over time through consistent performance or significant contributions to a field or community.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAYMD',
                'etymology': 'Past participle of "fame" used as an adjective, from Latin "fama" meaning "report," "rumor," or "reputation," related to "fari" meaning "to speak."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ chef opened a new restaurant that attracted food critics from across the country.',
                'memory_tip': 'Remember "FAMED" - someone who has earned their FAME through skill or achievement, making them well-known and respected.'
            },
            'family': {
                'definition': 'Family refers to a group of people related by blood, marriage, adoption, or strong emotional bonds who typically live together or maintain close relationships. In biological terms, family is also a taxonomic classification above genus and below order. The concept of family varies across cultures and can include nuclear families (parents and children), extended families (including grandparents, aunts, uncles, cousins), or chosen families (close friends considered family). Family represents fundamental social bonds and support systems that provide care, identity, and belonging.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAM-uh-lee',
                'etymology': 'From Latin "familia," meaning "household," including servants and slaves, derived from "famulus" meaning "servant." The modern meaning of blood relatives developed later.',
                'language_origins': 'Latin',
                'example_sentence': 'The annual _______ reunion brought together relatives from across the country to celebrate their shared heritage.',
                'memory_tip': 'Remember "FAM-ily" - your FAMiliar people who are close to you, the group you\'re most familiar and comfortable with.'
            },
            'famished': {
                'definition': 'Famished means extremely hungry, starving, or having an intense craving for food. When someone is famished, they have gone without food long enough to feel significant discomfort and urgency about eating. The word expresses a more extreme state than simply being hungry, suggesting a level of hunger that demands immediate attention. Famished can also be used somewhat hyperbolically in casual conversation to emphasize strong hunger, even when the person is not literally starving.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAM-isht',
                'etymology': 'From "famish," derived from Middle English "famen" meaning "to starve," ultimately from Latin "fames" meaning "hunger."',
                'language_origins': 'Latin, Middle English',
                'example_sentence': 'After hiking for eight hours without stopping for lunch, the entire group was absolutely _______.',
                'memory_tip': 'Remember "FAM-ished" - so hungry you\'re FAMous for being starved, or your FAMily is worried about your hunger.'
            },
            'famous': {
                'definition': 'Famous means widely known and recognized by many people, typically due to notable achievements, talents, or significant events. When someone or something is famous, they have achieved widespread recognition and are easily identifiable to the general public. Fame can result from positive accomplishments like artistic talent, scientific discoveries, or athletic achievements, or from negative notoriety. The state of being famous often involves media attention and public interest, and can significantly impact a person\'s life and opportunities.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAY-mus',
                'etymology': 'From Latin "famosus," meaning "much talked about" or "renowned," derived from "fama" meaning "report," "rumor," or "reputation."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ actor donated millions of dollars to charity, using his celebrity status to support important causes.',
                'memory_tip': 'Remember "FAMOUS" - someone whose FAME is so great that they\'re known by Almost everyone, FAMously recognized.'
            },
            'fanatic': {
                'definition': 'A fanatic is a person who holds extreme, often irrational beliefs or opinions about something and pursues them with excessive zeal or intensity. Fanatics are characterized by their unwillingness to consider alternative viewpoints and their tendency to take their beliefs to unhealthy or dangerous extremes. The term can apply to various contexts, including religion, politics, sports, or personal interests. While passion for a subject can be positive, fanaticism involves a loss of perspective and balance that can lead to harmful or destructive behavior.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fuh-NAT-ik',
                'etymology': 'From Latin "fanaticus," meaning "inspired by a deity" or "frenzied," derived from "fanum" meaning "temple." Originally referred to religious enthusiasm.',
                'language_origins': 'Latin',
                'example_sentence': 'The sports _______ painted his entire house in team colors and attended every game for twenty consecutive seasons.',
                'memory_tip': 'Remember "fan-ATIC" - an extreme FAN whose enthusiasm becomes ATTIC-level (over the top) obsessive behavior.'
            },
            'fandango': {
                'definition': 'Fandango is a lively Spanish dance performed by a couple, characterized by quick, intricate footwork and the use of castanets. The dance is traditionally accompanied by guitar music and features dramatic poses, spins, and rhythmic stamping. Fandango music is typically written in triple meter with a moderate to fast tempo. The dance and its music became popular throughout Europe in the 18th century and remain an important part of Spanish cultural heritage. The term can also refer more generally to any elaborate or showy performance or celebration.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fan-DANG-goh',
                'etymology': 'From Spanish "fandango," of uncertain origin, possibly from Portuguese "fado" or from an African language. The dance emerged in 18th-century Spain.',
                'language_origins': 'Spanish',
                'example_sentence': 'The flamenco troupe\'s passionate _______ performance captivated the audience with its fiery energy and precise footwork.',
                'memory_tip': 'Remember "fan-DANGO" - a dance where fans go crazy for the DANG good performance with quick footwork.'
            },
            'fanfaronade': {
                'definition': 'Fanfaronade is boastful or bragging talk, especially empty boasting that lacks substance or truth. The word describes ostentatious display of superiority or achievement that is designed to impress others but may be exaggerated or false. Fanfaronade often involves loud, showy declarations about one\'s abilities, accomplishments, or importance. The term suggests theatrical, over-the-top behavior that prioritizes appearance over substance. It implies a kind of verbal strutting or peacocking that others may find annoying or transparently fake.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fan-far-uh-NAYD',
                'etymology': 'From French "fanfaronnade," derived from "fanfaron" meaning "braggart," ultimately from Spanish "fanfarrón." Related to "fanfare."',
                'language_origins': 'French, Spanish',
                'example_sentence': 'The politician\'s speech was pure _______, full of empty promises and exaggerated claims about his achievements.',
                'memory_tip': 'Remember "fanfare-ONADE" - like a loud FANFARE but it\'s just empty boasting and showing off, a parade of bragging.'
            },
            'fanged': {
                'definition': 'Fanged describes something that has fangs, which are long, sharp teeth typically found in carnivorous animals, snakes, or mythical creatures. Fangs are specialized for gripping, tearing, or injecting venom. When something is described as fanged, it emphasizes the presence of these prominent, threatening teeth. The term is often used to describe predatory animals like wolves, snakes, or vampires in literature and folklore. Fanged creatures are typically portrayed as dangerous or aggressive due to their prominent dental weaponry.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FANGD',
                'etymology': 'From "fang" (from Old English "fang" meaning "capture" or "grasp") plus the past participle ending "-ed" used as an adjective.',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ serpent in the ancient myth was said to guard the treasure with deadly precision.',
                'memory_tip': 'Remember "FANGED" - having sharp FANGs that can GRAB and pierce, like a dangerous predator.'
            },
            'fans': {
                'definition': 'Fans can refer to multiple meanings depending on context. As a plural noun, fans are people who have a strong interest in or admiration for a particular person, team, activity, or form of entertainment. They demonstrate enthusiasm and loyalty through support, attendance, or following. Fans can also be the plural of fan, the mechanical device that creates airflow for cooling or ventilation by rotating blades. In both uses, the concept involves movement - either emotional enthusiasm or physical air movement.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FANZ',
                'etymology': 'For enthusiasts: shortened from "fanatic." For devices: from Latin "vannus" meaning "winnowing basket," referring to tools for separating grain.',
                'language_origins': 'Latin, English',
                'example_sentence': 'Thousands of _______ gathered outside the stadium hours before the championship game began.',
                'memory_tip': 'Remember "FANS" - people who are FANatically enthusiastic, or devices that create a breeze by FANning the air.'
            },
            'fantastically': {
                'definition': 'Fantastically is an adverb meaning in an extraordinary, remarkable, or excellent manner. When something is done fantastically, it is performed with exceptional skill, success, or impressiveness that exceeds normal expectations. The word can also mean in a way that seems unreal, imaginary, or too extraordinary to believe. Fantastically emphasizes the exceptional nature of something, whether referring to quality of performance, degree of success, or the seemingly impossible nature of an occurrence.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'fan-TAS-ti-klee',
                'etymology': 'From "fantastic" (from Greek "phantastikos" meaning "able to present to the mind") plus the adverb suffix "-ally."',
                'language_origins': 'Greek',
                'example_sentence': 'The new restaurant\'s opening night went _______, with every table filled and customers raving about the food.',
                'memory_tip': 'Remember "fanTAS-tically" - done so well it\'s like a FANTASTic performance that TAStes amazing, extraordinarily good.'
            },
            'farcical': {
                'definition': 'Farcical describes something that is absurd, ridiculous, or resembling a farce - a dramatic work characterized by exaggerated, improbable situations and characters. When a situation is farcical, it is so unreasonable, illogical, or poorly managed that it becomes laughable or mockable. The word often applies to situations that are meant to be serious but have become so dysfunctional or absurd that they resemble comedy. Farcical implies a level of dysfunction that undermines credibility and invites ridicule rather than respect.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAR-si-kul',
                'etymology': 'From "farce" (from Latin "farcire" meaning "to stuff," referring to comic interludes "stuffed" into serious plays) plus the suffix "-ical."',
                'language_origins': 'Latin',
                'example_sentence': 'The committee meeting became _______ when members spent three hours debating the color of paper clips.',
                'memory_tip': 'Remember "FARCE-ical" - so ridiculous it\'s like a FARCE, a comedy where everything goes absurdly wrong.'
            },
            'fardel': {
                'definition': 'Fardel is an archaic term meaning a bundle, pack, or burden, particularly one carried by a traveler or peddler. The word can refer to both physical bundles of goods or belongings and metaphorical burdens such as responsibilities, troubles, or hardships. Fardel appears in Shakespeare\'s "Hamlet" in the famous "To be or not to be" soliloquy, where Hamlet speaks of bearing "fardels" (burdens) of life. While rarely used in modern English, the term occasionally appears in literary contexts to evoke historical or poetic atmosphere.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAR-dul',
                'etymology': 'From Old French "fardel," meaning "little bundle," derived from Arabic "fardah" meaning "package." The word traveled through multiple languages.',
                'language_origins': 'Arabic, Old French',
                'example_sentence': 'The weary traveler carried his _______ of worldly possessions on his back as he walked the dusty road.',
                'memory_tip': 'Remember "FAR-del" - a bundle you carry FAR when you travel, or burdens that feel FAR too heavy to bear.'
            },
            'farewell': {
                'definition': 'Farewell is an expression used when parting from someone, wishing them well in their future endeavors. As a noun, farewell refers to the act of saying goodbye or a ceremony marking someone\'s departure. The word carries connotations of finality and good wishes, often used when separations are expected to be lengthy or permanent. Farewells can be formal or informal, depending on the relationship and circumstances. The term combines wishes for the person\'s well-being with acknowledgment that separation is occurring.',
                'part_of_speech': 'interjection, noun',
                'pronunciation_guide': 'fair-WEL',
                'etymology': 'Middle English compound of "fare" (meaning "to go" or "to travel") and "well" (meaning "in a good manner"), literally meaning "travel well."',
                'language_origins': 'Middle English',
                'example_sentence': 'At the retirement party, colleagues gathered to bid _______ to their longtime manager and wish him happiness.',
                'memory_tip': 'Remember "FARE-well" - wishing someone will FARE WELL as they travel on their journey away from you.'
            },
            'farfalle': {
                'definition': 'Farfalle is a type of pasta shaped like bow ties or butterflies, characterized by its pinched center and flared edges. The pasta is made from durum wheat and eggs, and its unique shape helps it hold sauces effectively in its folds and crevices. Farfalle originated in Northern Italy and is popular in various dishes, from light olive oil preparations to creamy sauces. The distinctive butterfly shape not only serves practical purposes for sauce retention but also makes dishes visually appealing and interesting.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'far-FAL-lay',
                'etymology': 'From Italian "farfalle," literally meaning "butterflies," derived from "farfalla" (butterfly), ultimately from Latin "papilio."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The chef prepared a delicious _______ salad with cherry tomatoes, fresh basil, and mozzarella cheese.',
                'memory_tip': 'Remember "far-FALL-e" - pasta that looks like butterflies that might FLY FAR, or bow ties that have FALLen into butterfly shapes.'
            },
            'farfetched': {
                'definition': 'Farfetched describes something that is unlikely, improbable, or difficult to believe due to being remote from reality or common sense. When an idea, story, or explanation is farfetched, it seems to require too great a stretch of imagination or too many unlikely coincidences to be credible. The term suggests that something has been "fetched from far away" in terms of logic or probability. Farfetched ideas often lack supporting evidence or depend on implausible circumstances.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAR-fecht',
                'etymology': 'Compound word meaning "fetched from far," implying something so unlikely it seems to come from a distant, improbable source.',
                'language_origins': 'English',
                'example_sentence': 'His excuse for being three hours late seemed _______ and didn\'t match the evidence his colleagues had observed.',
                'memory_tip': 'Remember "FAR-fetched" - an idea so unlikely it seems FETCHED from FAR away, pulled from somewhere distant and improbable.'
            },
            'farina': {
                'definition': 'Farina is a fine flour or meal made from grains, seeds, or roots, most commonly referring to a wheat-based cereal similar to cream of wheat. The term can describe various types of ground grain products used for making porridge, pasta, or baked goods. Farina is typically smoother and finer in texture than regular flour and is often used to make hot breakfast cereals. In some regions, farina refers to cassava flour or other starchy, ground food products used as dietary staples.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fuh-REE-nuh',
                'etymology': 'From Latin "farina" meaning "flour" or "meal," derived from "far" meaning "grain" or "spelt wheat."',
                'language_origins': 'Latin',
                'example_sentence': 'For breakfast, grandmother prepared a warm bowl of _______ topped with butter and brown sugar.',
                'memory_tip': 'Remember "fa-RINA" - a FINE flour that\'s as smooth as a balleRINA, ground very finely from grains.'
            },
            'farkleberry': {
                'definition': 'Farkleberry is a small shrub or tree native to the southeastern United States, scientifically known as Vaccinium arboreum. It belongs to the blueberry family and produces small, dark berries that are edible but somewhat tart and seedy. The plant typically grows in sandy soils and pine forests, reaching heights of 6-10 feet. Farkleberries are sometimes called tree huckleberries or sparkleberries. While the berries can be eaten fresh, they are often used in jams, jellies, or baked goods, and they provide food for wildlife.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAR-kul-ber-ee',
                'etymology': 'American English, possibly a folk etymology or dialectal variation related to "sparkleberry," another name for the same plant.',
                'language_origins': 'American English',
                'example_sentence': 'The hikers discovered a patch of _______ bushes and carefully harvested some of the tart berries for their evening meal.',
                'memory_tip': 'Remember "FARKLE-berry" - berries that make you pucker like you\'re playing the dice game Farkle, tart and seedy.'
            },
            'farmyard': {
                'definition': 'A farmyard is the enclosed area immediately surrounding farm buildings, typically including the barn, stable, chicken coop, and farmer\'s house. This central area serves as the hub of farm activity, where animals are fed, equipment is stored, and daily farm operations are conducted. Farmyards are usually enclosed by fences or buildings to contain livestock and organize the various functions of the farm. The farmyard represents the domestic, organized center of agricultural life, distinct from the fields where crops are grown.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FARM-yahrd',
                'etymology': 'Compound word combining "farm" (from Old English "feorm" meaning "provision" or "feast") and "yard" (from Old English "geard" meaning "enclosure").',
                'language_origins': 'Old English',
                'example_sentence': 'The children loved visiting their grandfather\'s farm and playing with the chickens that roamed freely around the _______.',
                'memory_tip': 'Remember "FARM-yard" - the YARD where all the FARM animals gather around the barn, the central courtyard of farm life.'
            }
        }
        
        if word.lower() in batch_065_data:
            return batch_065_data[word.lower()]
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
        
        print("Batch 065 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch065Processor()
    
    input_file = "output/batch_065_words.csv"
    output_file = "output/batch_065_processed.csv"
    
    processor.process_batch(input_file, output_file)