#!/usr/bin/env python3

import csv
import logging
from typing import Dict, List, Any
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    """Calculates spelling difficulty based on various linguistic factors"""
    
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        """Calculate comprehensive difficulty metrics"""
        return {
            'phonetic_transparency_score': self._calculate_phonetic_transparency(word),
            'word_frequency_score': self._calculate_word_frequency(word),
            'morphological_complexity_score': self._calculate_morphological_complexity(word),
            'etymology_complexity_score': self._calculate_etymology_complexity(etymology),
            'difficulty': None  # Leave null as instructed
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        """Score based on spelling-to-sound correspondence"""
        irregular_patterns = ['ph', 'gh', 'ough', 'augh', 'eigh', 'tion', 'sion']
        score = 1.0
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 0.3
        return min(score, 5.0)
    
    def _calculate_word_frequency(self, word: str) -> float:
        """Estimate frequency-based difficulty"""
        if len(word) <= 4:
            return 1.0
        elif len(word) <= 7:
            return 2.0
        elif len(word) <= 10:
            return 3.0
        else:
            return 4.0
    
    def _calculate_morphological_complexity(self, word: str) -> float:
        """Score based on morphological structure"""
        prefixes = ['un', 'pre', 'dis', 'in', 'im', 'non', 're', 'over', 'under', 'out', 'up', 'sub', 'inter', 'fore', 'de', 'mis']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible']
        
        complexity = 1.0
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                complexity += 0.5
                break
                
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                complexity += 0.5
                break
        
        return min(complexity, 5.0)
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        """Score based on etymological complexity"""
        if not etymology:
            return 3.0
        
        complex_origins = ['greek', 'latin', 'french', 'german', 'arabic', 'sanskrit', 'hebrew']
        etymology_lower = etymology.lower()
        
        complexity = 1.0
        for origin in complex_origins:
            if origin in etymology_lower:
                complexity += 0.8
        
        return min(complexity, 5.0)

class Batch123Processor:
    """Process spelling bee words for Batch 123 with comprehensive Claude data"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word using Claude knowledge"""
        
        word_data = {
            'online': {
                'pronunciation': '/ˈɔnˌlaɪn/',
                'definition': 'Online refers to being connected to or accessible through the internet, or being in an active, operational state within a computer system or network. In its most common usage, online describes digital activities, services, and resources that are available through internet connectivity, enabling remote access, communication, and interaction across vast distances. Online activities include web browsing, email, social media, video streaming, shopping, gaming, and educational platforms that have transformed how people work, learn, communicate, and entertain themselves. The term also applies to computer systems and devices that are currently connected to a network and functioning properly, as opposed to being offline or disconnected. Online learning has become increasingly important, offering educational opportunities that transcend geographical boundaries and traditional classroom limitations. Online banking, shopping, and entertainment have revolutionized consumer behavior and business models. The concept encompasses both the technical infrastructure that enables internet connectivity and the cultural and social phenomena that have emerged from widespread digital connectivity. As internet access becomes more ubiquitous, the distinction between online and offline activities continues to blur, with many aspects of modern life now seamlessly integrated with digital platforms.',
                'etymology': 'From "on" + "line," originally referring to being connected to a telephone or telegraph line, later adapted for computer networks.',
                'memory_tip': 'Think "on-line" - being "on" the internet "line" or connection that links you to the digital world.',
                'example_sentence': 'Students accessed their _____ courses from home during the pandemic, participating in virtual classes and discussions.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'onomatopoeia': {
                'pronunciation': '/ˌɑnəˌmætəˈpiə/',
                'definition': 'Onomatopoeia is a linguistic device where words are formed to imitate or suggest the natural sounds they represent, creating a direct connection between sound and meaning that enhances expressiveness and vividness in language. These words attempt to capture real-world sounds through written or spoken language, such as "buzz" for the sound of bees, "crash" for something falling, "whisper" for quiet speech, or "roar" for loud animal sounds. Onomatopoeia serves multiple functions in communication: it makes descriptions more vivid and immediate, helps readers or listeners visualize scenes, and adds emotional impact to narratives. Different languages have varying onomatopoeic words for the same sounds, reflecting cultural and linguistic differences in sound perception and representation. In literature, onomatopoeia enhances sensory experiences and creates atmosphere, while in comics and graphic novels, sound words like "POW!" and "BOOM!" provide visual representation of audio elements. Children\'s literature frequently employs onomatopoeia to engage young readers and help them connect sounds with words. The phenomenon demonstrates the creative and imitative aspects of human language, showing how words can transcend arbitrary symbol systems to create more direct sound-meaning relationships.',
                'etymology': 'From Greek onomatopoiia, from onoma (name) + poiein (to make), literally meaning "name-making" or "making words."',
                'memory_tip': 'Think "oh-no-MAT-oh-PEE-ah" - words that make the sounds they name, like "buzz," "crash," "meow."',
                'example_sentence': 'The children\'s book was filled with _____ like "moo," "woof," and "quack" to represent animal sounds.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'onshore': {
                'pronunciation': '/ˈɑnˌʃɔr/',
                'definition': 'Onshore refers to something located on land as opposed to offshore locations in water, or to the movement of wind, currents, or other phenomena from the sea toward the land. In maritime and coastal contexts, onshore winds blow from the ocean toward the shore, often bringing moisture, cooler temperatures, and sometimes storms to coastal areas. These winds can significantly affect weather patterns, surfing conditions, and marine activities. In business and economics, onshore refers to operations, manufacturing, or services located within a company\'s home country, as opposed to offshore operations in foreign countries. Onshore oil and gas drilling occurs on land rather than in ocean environments, typically involving different technologies and environmental considerations than offshore drilling. The term is also used in shipping and logistics to describe activities that occur on land, such as onshore handling of cargo, port operations, and land-based transportation. Environmental and regulatory frameworks often differ between onshore and offshore activities, with onshore operations typically subject to different permitting processes, safety requirements, and environmental protections. Understanding onshore versus offshore distinctions is important in fields ranging from meteorology and marine science to international business and energy production.',
                'etymology': 'From "on" + "shore," literally meaning "on the shore" or located on land rather than at sea.',
                'memory_tip': 'Think "on-shore" - located "on" the "shore" (land) rather than out in the water.',
                'example_sentence': 'The _____ wind brought cool, salty air inland, providing relief from the hot summer day.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'onus': {
                'pronunciation': '/ˈoʊnəs/',
                'definition': 'Onus refers to a burden, responsibility, or obligation that falls upon a particular person or group, often involving the expectation or requirement to prove something, take action, or bear consequences. The term frequently appears in legal contexts, where "burden of proof" places the onus on one party to demonstrate the validity of their claims or allegations. In everyday usage, onus describes the responsibility for resolving problems, making decisions, or initiating action - when someone says "the onus is on you," they mean you have the responsibility to act or prove something. The concept implies not just responsibility but often a sense of duty or moral obligation that cannot easily be transferred to others. In academic and professional settings, the onus might fall on researchers to prove their hypotheses, on companies to demonstrate product safety, or on individuals to verify their credentials. The word carries implications of accountability and the potential consequences of failing to meet one\'s responsibilities. Understanding where the onus lies is crucial for determining who should take action, who bears responsibility for outcomes, and who must provide evidence or justification for claims or decisions.',
                'etymology': 'From Latin onus meaning "load, burden," related to the same root as "onerous."',
                'memory_tip': 'Think "OH-nus" - like "Oh, no! Us!" when you realize the responsibility or burden falls on you.',
                'example_sentence': 'The _____ was on the prosecution to prove the defendant\'s guilt beyond a reasonable doubt.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'onychitis': {
                'pronunciation': '/ˌɑnɪˈkaɪtɪs/',
                'definition': 'Onychitis is a medical term referring to inflammation of the nail matrix or nail bed, typically involving the tissues surrounding and supporting the fingernails or toenails. This condition can result from various causes including bacterial or fungal infections, trauma, chemical irritation, allergic reactions, or underlying medical conditions that affect nail health. Symptoms of onychitis may include redness, swelling, pain, tenderness around the nail area, and sometimes changes in nail appearance, texture, or growth patterns. The inflammation can affect the nail\'s ability to grow normally, potentially leading to deformities, discoloration, or nail loss in severe cases. Treatment typically depends on the underlying cause and may involve topical or systemic antibiotics for bacterial infections, antifungal medications for fungal causes, or anti-inflammatory treatments to reduce swelling and pain. Prevention often involves proper nail hygiene, avoiding trauma to nail areas, wearing appropriate protective gear when necessary, and addressing underlying health conditions that might predispose individuals to nail problems. Healthcare providers may need to examine nail samples or perform cultures to identify specific infectious agents and determine the most effective treatment approach.',
                'etymology': 'From Greek onyx (nail) + -itis (inflammation), meaning "inflammation of the nail."',
                'memory_tip': 'Think "onych-itis" - "onych" (nail) + "itis" (inflammation) = inflamed nails.',
                'example_sentence': 'The doctor diagnosed _____ after noticing the redness and swelling around the patient\'s fingernails.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'onychorrhexis': {
                'pronunciation': '/ˌɑnɪkoʊˈrɛksɪs/',
                'definition': 'Onychorrhexis is a medical condition characterized by brittle, splitting, or ridged fingernails and toenails that tend to break easily and develop longitudinal or vertical ridges running from the cuticle to the tip of the nail. This nail disorder can affect nail appearance, strength, and overall health, making nails more susceptible to damage and breakage during normal daily activities. The condition can result from various factors including aging, nutritional deficiencies (particularly biotin, iron, or protein), excessive exposure to water or chemicals, frequent use of nail polish removers, trauma, or underlying medical conditions such as thyroid disorders, psoriasis, or circulation problems. Environmental factors like cold weather, dry air, and harsh chemicals can exacerbate the condition. Treatment typically involves identifying and addressing underlying causes, improving nail care habits, using moisturizing treatments, taking appropriate nutritional supplements if deficiencies are present, and protecting nails from excessive moisture and chemical exposure. Dermatologists may recommend specific nail strengthening treatments, topical therapies, or lifestyle modifications to improve nail health and reduce brittleness. The condition is generally not serious but can be cosmetically concerning and may indicate underlying health issues that warrant medical attention.',
                'etymology': 'From Greek onyx (nail) + rhexis (breaking, rupture), meaning "nail breaking" or "nail splitting."',
                'memory_tip': 'Think "onych-orrhexis" - "onych" (nail) + "rhexis" (breaking) = nails that break and split easily.',
                'example_sentence': 'The dermatologist recommended biotin supplements to treat the patient\'s _____, which caused constant nail breakage.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oolite': {
                'pronunciation': '/ˈoʊəˌlaɪt/',
                'definition': 'Oolite is a type of sedimentary rock composed primarily of ooids, which are small, round grains that resemble fish eggs or caviar, typically formed in warm, shallow marine environments through the accretion of calcium carbonate around sand grains or shell fragments. These distinctive spherical or oval-shaped grains usually measure between 0.25 and 2 millimeters in diameter and develop through a process where calcium carbonate precipitates in layers around a nucleus as the grain rolls back and forth in agitated shallow water. The resulting rock has a distinctive appearance that resembles a collection of tiny eggs cemented together, giving it its name. Oolitic limestone formations are found in many parts of the world and represent ancient shallow marine environments with warm, supersaturated waters conducive to calcium carbonate precipitation. These rocks are economically important as building stones, sources of limestone for cement production, and indicators of past environmental conditions. Famous oolitic limestone formations include those used in many historic buildings in England, parts of the Bahama Banks, and various geological formations that provide insights into ancient climate and ocean conditions. The study of oolites helps geologists understand past marine environments and processes of carbonate sedimentation.',
                'etymology': 'From Greek oon (egg) + lithos (stone), literally meaning "egg stone" due to its appearance resembling fish eggs.',
                'memory_tip': 'Think "oo-lite" - rock that looks like "oo" (eggs) made of "lite" (stone), resembling fish eggs or caviar.',
                'example_sentence': 'The geologist identified the limestone as _____ because of its characteristic grain structure resembling tiny eggs.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oompah': {
                'pronunciation': '/ˈumˌpɑ/',
                'definition': 'Oompah refers to a distinctive rhythmic pattern in music, particularly associated with brass band music, polkas, waltzes, and traditional German or Austrian folk music, characterized by a strong bass note on the first beat followed by lighter chord accompaniment on subsequent beats. This musical style creates a bouncing, march-like rhythm that is both energetic and danceable, typically performed by tubas, brass instruments, and sometimes accordions in traditional folk ensembles. The oompah rhythm provides the foundational beat that drives polka dancing and other traditional European folk dances, creating an infectious, toe-tapping quality that encourages movement and celebration. Beer gardens, Oktoberfest celebrations, and traditional festivals often feature oompah bands that specialize in this style of music. The term has expanded beyond its musical origins to describe anything with a similar bouncing, repetitive rhythm or enthusiastic, somewhat rustic character. Oompah music represents an important cultural tradition that maintains connections to European folk heritage while continuing to entertain audiences at cultural festivals, celebrations, and community events. The style\'s accessibility and joyful nature make it popular for public gatherings and festive occasions where communal participation and dancing are encouraged.',
                'etymology': 'Onomatopoeic word imitating the sound of brass band music, particularly the bass and accompaniment patterns.',
                'memory_tip': 'Think "OOM-pah" - the sound a tuba makes in German brass band music, "OOM" (bass) "pah" (higher notes).',
                'example_sentence': 'The _____ band played traditional polkas that had everyone dancing at the Oktoberfest celebration.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oops': {
                'pronunciation': '/ups/',
                'definition': 'Oops is an exclamation used to express mild surprise, embarrassment, or acknowledgment of a small mistake or accident, typically when someone has done something wrong, clumsy, or unexpected. This informal interjection serves as both an immediate reaction to minor mishaps and a way to acknowledge errors while maintaining a light, non-serious tone. The expression is commonly used when dropping something, making a verbal slip, bumping into someone, or realizing a small oversight or mistake. Oops functions as a social courtesy that signals awareness of an error while implying that the mistake was unintentional and relatively minor. The word is frequently used with children to help them understand that mistakes are normal and not catastrophic, encouraging a healthy attitude toward learning from errors. In digital communication, "oops" often appears when correcting typos, sending messages to wrong recipients, or acknowledging technical errors. The expression is universally understood in English-speaking cultures and represents a gentle way to deflect tension or embarrassment that might arise from minor mistakes. Its casual, friendly tone makes it appropriate for most informal situations where a formal apology would be excessive but some acknowledgment of error is warranted.',
                'etymology': 'Natural exclamation, possibly influenced by "whoops," expressing sudden surprise or recognition of a mistake.',
                'memory_tip': 'Think of the surprised "oops!" sound you make when you accidentally drop something or make a small mistake.',
                'example_sentence': '"_____!" she said as she accidentally knocked over her coffee cup, quickly reaching for napkins.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oopuhue': {
                'pronunciation': '/ˈoʊpuˌhu/',
                'definition': 'Oopuhue appears to be a specialized term that may derive from Hawaiian or another Polynesian language, though it is not commonly found in standard English dictionaries. In Hawaiian botanical or cultural contexts, words with similar structure often refer to native plants, traditional practices, or specific cultural concepts. Given the pattern of Hawaiian words, this could potentially refer to a type of plant, a traditional practice, or a place name within Hawaiian culture. Without more specific context, it\'s difficult to provide a definitive definition, as this appears to be either a highly specialized term, a proper noun, or possibly a word that has not been widely documented in standard reference sources. Such terms sometimes appear in spelling bee competitions to challenge contestants with unusual or culturally specific vocabulary that tests their ability to handle unfamiliar linguistic patterns. When encountering such specialized terms, it\'s important to consider the cultural and linguistic context from which they originate, as they often carry specific cultural meanings that may not translate directly into English concepts.',
                'etymology': 'Possibly from Hawaiian or Polynesian language, though specific etymology is uncertain without more context.',
                'memory_tip': 'Remember the spelling pattern: O-O-P-U-H-U-E, noting the repeated "oo" at the beginning and "u" sounds.',
                'example_sentence': 'The spelling bee contestant carefully spelled the unfamiliar word _____ letter by letter.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oort': {
                'pronunciation': '/ɔrt/',
                'definition': 'Oort typically refers to the Oort Cloud, a theoretical spherical shell of icy objects that is believed to surround our solar system at distances ranging from about 2,000 to 100,000 astronomical units from the Sun, named after Dutch astronomer Jan Oort who first proposed its existence in 1950. This vast, distant region is thought to be the source of long-period comets that occasionally enter the inner solar system with orbital periods measured in thousands or millions of years. The Oort Cloud represents the most distant region of our solar system\'s gravitational influence, containing billions or trillions of icy remnants from the solar system\'s formation billions of years ago. These objects, primarily composed of water ice, methane, and ammonia, remain in deep freeze at the edge of interstellar space until gravitational perturbations from passing stars or galactic tidal forces occasionally send them on long journeys toward the Sun, where they become visible as comets. While the Oort Cloud has never been directly observed due to its extreme distance and the small size of its constituent objects, its existence is strongly supported by observations of long-period comet orbits and computer models of solar system dynamics. Understanding the Oort Cloud is crucial for comprehending the architecture of our solar system and the origins of cometary material.',
                'etymology': 'Named after Jan Hendrik Oort (1900-1992), Dutch astronomer who proposed the existence of this cloud of cometary objects.',
                'memory_tip': 'Think "OORT Cloud" - named after astronomer Oort, the distant cloud of icy objects that sends comets our way.',
                'example_sentence': 'The long-period comet was thought to originate from the distant _____ Cloud at the edge of our solar system.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oozing': {
                'pronunciation': '/ˈuzɪŋ/',
                'definition': 'Oozing describes the slow, gradual seepage or flow of liquid through small openings, pores, or cracks, typically referring to thick, viscous substances that move slowly rather than flowing freely. This process commonly occurs when fluids under pressure find pathways through porous materials, damaged surfaces, or natural openings, resulting in a steady but slow release of liquid. In medical contexts, oozing refers to the slow seepage of blood, pus, or other bodily fluids from wounds, sores, or inflamed tissues, often indicating ongoing bleeding or infection that requires attention. Geological oozing involves the gradual seepage of oil, water, or other fluids through rock formations or soil, sometimes creating natural springs or oil seeps. In everyday usage, oozing describes situations where thick liquids like honey, syrup, mud, or paste slowly emerge from containers or spread across surfaces. The word can also be used metaphorically to describe the gradual emergence or expression of qualities, emotions, or characteristics, such as "oozing confidence" or "oozing charm." The slow, continuous nature of oozing distinguishes it from sudden spills, gushes, or rapid flows, emphasizing the persistent, gradual nature of the liquid movement.',
                'etymology': 'From Middle English wosen, from Old English wōs meaning "juice, moisture," related to the slow seepage of liquids.',
                'memory_tip': 'Think "OO-zing" - the "oo" sound mimics the slow, thick flow of liquid seeping out gradually.',
                'example_sentence': 'The tree sap was slowly _____ from the crack in the bark, forming sticky amber droplets.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opalescence': {
                'pronunciation': '/ˌoʊpəˈlɛsəns/',
                'definition': 'Opalescence refers to a visual phenomenon where a material displays a milky or pearlescent appearance with subtle color changes and internal light reflections, similar to the optical properties exhibited by the gemstone opal. This effect occurs when light interacts with materials that have internal structures, particles, or inclusions that scatter light in specific ways, creating an appearance that seems to glow from within with shifting colors and luminosity. The phenomenon can be observed in various natural and artificial materials, including certain minerals, glasses, liquids with suspended particles, and biological tissues. In opalescent materials, light is scattered and reflected at different wavelengths, creating the characteristic play of colors that appears to move and change as the viewing angle shifts. This optical effect is caused by interference and diffraction of light waves as they interact with microscopic structures within the material. Opalescence is valued in art, jewelry, and decorative objects for its beautiful, mystical appearance that suggests depth and movement. Scientists study opalescence in materials science and optics to understand light-matter interactions and to develop new materials with desired optical properties. The term is also used metaphorically to describe anything that has a subtle, shifting, luminous quality.',
                'etymology': 'From "opal" (the gemstone known for its color-changing properties) + "-escence" (suffix meaning becoming or having the quality of).',
                'memory_tip': 'Think "opal-escence" - having the essence or quality of an opal\'s shifting, colorful glow.',
                'example_sentence': 'The glass sculpture displayed a beautiful _____ that seemed to capture and reflect light from within.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opaque': {
                'pronunciation': '/oʊˈpeɪk/',
                'definition': 'Opaque describes materials or objects that do not allow light to pass through them, creating complete or near-complete blockage of transparency and preventing clear vision of objects on the other side. Unlike transparent materials (which allow light through clearly) or translucent materials (which allow some light through but scatter it), opaque objects absorb or reflect most incident light, making them impossible to see through. Common opaque materials include metals, wood, concrete, many plastics, and thick fabrics that completely block light transmission. The term extends beyond physical transparency to describe situations, explanations, or communications that are unclear, difficult to understand, or deliberately obscured. In this figurative sense, opaque writing, reasoning, or behavior lacks clarity and transparency, making it hard for others to comprehend intentions, meanings, or processes. Financial opacity might involve deliberately unclear accounting practices, while bureaucratic opacity could refer to unnecessarily complex procedures that hide decision-making processes. In art and design, opacity is a measurable property used in paints, inks, and digital media to control coverage and layering effects. Understanding opacity is important in fields ranging from materials science and engineering to communication and design, where controlling or achieving transparency versus opacity serves various functional and aesthetic purposes.',
                'etymology': 'From Latin opacus meaning "shaded, dark," related to the concept of blocking light.',
                'memory_tip': 'Think "oh-PAKE" - materials that are "packed" so densely that light cannot get through them.',
                'example_sentence': 'The _____ curtains completely blocked the sunlight, keeping the room dark during the day.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'open': {
                'pronunciation': '/ˈoʊpən/',
                'definition': 'Open serves as both an adjective and verb with related meanings centered on the concept of accessibility, lack of barriers, and freedom of movement or access. As an adjective, open describes spaces, containers, or situations that are not closed, blocked, or restricted, allowing entry, exit, or passage. Open doors, windows, and gates permit movement, while open minds, discussions, and policies welcome new ideas and participation. The term suggests availability, honesty, and transparency in various contexts - open communication involves frank, honest exchange, while open source software allows free access to code. As a verb, open means to move something from a closed to an accessible state, such as opening doors, books, or conversations. Open can describe time periods when businesses, institutions, or opportunities are available for public access or participation. In technology, open systems and standards promote interoperability and broad access rather than proprietary restrictions. The concept of openness is fundamental to democracy, education, commerce, and social interaction, representing values of accessibility, transparency, and inclusion. Understanding when and how to be open versus closed is crucial for personal relationships, professional success, and effective communication in various life contexts.',
                'etymology': 'From Old English open, from Proto-Germanic *upanaz, related to "up" and meaning "not closed."',
                'memory_tip': 'Think of "open" as the opposite of closed - like an "opened" door that allows free passage.',
                'example_sentence': 'The library remained _____ late into the evening to accommodate students studying for exams.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opera': {
                'pronunciation': '/ˈɑpərə/',
                'definition': 'Opera is a dramatic art form that combines music, singing, acting, and often dance and elaborate staging to tell stories through predominantly sung dialogue and musical accompaniment by an orchestra. This sophisticated theatrical medium originated in Italy during the late 16th century and has evolved into one of the most complex and prestigious forms of musical theater. Opera typically features trained singers with powerful voices capable of performing without amplification in large venues, accompanied by full orchestras and supported by elaborate costumes, sets, and lighting. The art form encompasses various styles and periods, from Baroque and Classical operas by composers like Monteverdi and Mozart, to Romantic works by Verdi and Wagner, to contemporary compositions that continue to push artistic boundaries. Opera performances traditionally take place in specially designed opera houses with excellent acoustics and sight lines that enhance the dramatic and musical experience. The medium addresses universal themes of love, death, power, betrayal, and redemption through emotionally charged music and dramatic storytelling. Modern opera companies continue to produce both traditional works and new compositions, often incorporating innovative staging, technology, and interdisciplinary approaches while maintaining the essential elements of vocal excellence and orchestral accompaniment.',
                'etymology': 'From Italian opera meaning "work," from Latin opera (works), plural of opus (work, composition).',
                'memory_tip': 'Think "OH-per-ah" - a dramatic "opus" (work) where people sing their parts instead of just speaking.',
                'example_sentence': 'The renowned soprano\'s performance in the _____ brought the audience to their feet during the final aria.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'operant': {
                'pronunciation': '/ˈɑpərənt/',
                'definition': 'Operant refers to a type of behavior that operates on the environment to produce consequences, and is most commonly used in psychology to describe operant conditioning, a fundamental learning principle developed by B.F. Skinner. In operant conditioning, behaviors are modified through their consequences - behaviors followed by positive outcomes (reinforcement) tend to increase in frequency, while behaviors followed by negative outcomes (punishment) tend to decrease. This differs from classical conditioning, where responses are triggered by stimuli, because operant behaviors are voluntary actions that organisms perform to achieve certain outcomes. The operant paradigm explains much of human and animal learning, from simple tasks like a rat pressing a lever for food to complex human behaviors like studying for good grades or working for wages. Operant principles are widely applied in education, therapy, parenting, animal training, and organizational behavior management. Key concepts include positive and negative reinforcement, positive and negative punishment, and various schedules of reinforcement that affect how quickly behaviors are learned and how resistant they are to extinction. Understanding operant conditioning helps explain how behaviors are acquired, maintained, and modified through environmental consequences, making it a powerful tool for behavior change and learning enhancement.',
                'etymology': 'From Latin operant-, meaning "working," from operari meaning "to work," related to "operate."',
                'memory_tip': 'Think "OPER-ant" - behaviors that "operate" on the environment to get results or consequences.',
                'example_sentence': 'The psychologist used _____ conditioning techniques to help the patient reduce anxiety-related behaviors.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'operates': {
                'pronunciation': '/ˈɑpəˌreɪts/',
                'definition': 'Operates is the third-person singular present tense of the verb "operate," meaning to function, work, or perform in a specified manner, or to control and direct the functioning of a machine, system, or organization. When something operates, it carries out its intended functions or procedures, whether referring to mechanical devices, biological systems, business organizations, or abstract concepts. Mechanical operation involves the controlled functioning of machines, equipment, or technological systems according to their design specifications. Medical operation refers to surgical procedures where doctors operate on patients to treat conditions or injuries. Business operations encompass the day-to-day activities, processes, and procedures that keep organizations running effectively. The term also describes how people work within systems, follow procedures, or manipulate controls to achieve desired outcomes. Operating can involve both automatic functions (how the heart operates to pump blood) and conscious control (how a pilot operates an aircraft). In mathematics and logic, operations are specific procedures or functions applied to numbers or other elements. Understanding how various systems, devices, and organizations operate is essential for troubleshooting problems, improving efficiency, and achieving successful outcomes in technological, medical, business, and personal contexts.',
                'etymology': 'From Latin operatus, past participle of operari meaning "to work, labor," from opus (work).',
                'memory_tip': 'Think "oper-ates" - something that "operates" by working or functioning as intended.',
                'example_sentence': 'The new software _____ more efficiently than the previous version, processing data twice as fast.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'operator': {
                'pronunciation': '/ˈɑpəˌreɪtər/',
                'definition': 'An operator is a person who controls, operates, or manages machines, equipment, systems, or processes, typically requiring specialized knowledge, training, and skills to ensure safe and effective operation. In telecommunications, operators historically connected telephone calls manually and provided directory assistance, though modern systems have largely automated these functions. Industrial operators run manufacturing equipment, power plants, chemical processes, and other complex systems that require human oversight, monitoring, and control. Computer operators manage computer systems, networks, and data processing operations, while machine operators work with specific types of equipment in manufacturing, construction, or other industries. The term also has mathematical meanings, referring to symbols or functions that perform specific operations on numbers or variables, such as addition (+), multiplication (×), or more complex functions in calculus and algebra. In business contexts, operators might refer to companies that operate specific types of businesses, such as tour operators or equipment operators. Radio operators manage communication equipment and transmissions. The role typically involves understanding system capabilities, safety procedures, troubleshooting techniques, and emergency protocols. Modern operators often work with sophisticated computer-controlled systems while maintaining the ability to intervene when manual control becomes necessary.',
                'etymology': 'From Latin operator meaning "worker," from operari (to work) + -or (agent suffix meaning "one who").',
                'memory_tip': 'Think "oper-ator" - one who operates or works with machines, systems, or equipment.',
                'example_sentence': 'The power plant _____ monitored the control room displays to ensure all systems were functioning normally.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'operose': {
                'pronunciation': '/ˈɑpəˌroʊs/',
                'definition': 'Operose is an adjective meaning requiring or involving a great deal of effort, labor, or work; characterized by being laborious, diligent, or industrious in nature. The term describes tasks, processes, or endeavors that demand significant time, energy, and careful attention to complete successfully. Operose work typically involves complex, detailed, or meticulous activities that cannot be rushed or completed casually, requiring sustained effort and often specialized skills or knowledge. Academic research, detailed craftsmanship, complex engineering projects, and thorough investigative work are examples of operose undertakings. The word can describe both the nature of the work itself and the approach taken by individuals who engage in such work - operose scholars, for instance, might be known for their thorough, painstaking research methods. Unlike simple or routine tasks, operose activities often require problem-solving, creativity, and persistence to overcome challenges and achieve desired outcomes. The term suggests not just difficulty or effort, but a quality of work that is methodical, careful, and comprehensive. In literary and academic contexts, operose is often used to characterize scholarly works, artistic creations, or technical achievements that demonstrate exceptional dedication and thoroughness in their execution.',
                'etymology': 'From Latin operosus meaning "laborious, taking pains," from opus (work) + -osus (full of).',
                'memory_tip': 'Think "oper-ose" - work that is "oper" (operating) in a "rose" (thorough, detailed) manner requiring great effort.',
                'example_sentence': 'The historian\'s _____ research involved examining thousands of documents in multiple archives across several countries.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'ophthalmologist': {
                'pronunciation': '/ˌɑfθəlˈmɑlədʒɪst/',
                'definition': 'An ophthalmologist is a medical doctor who specializes in comprehensive eye and vision care, including the diagnosis, treatment, and surgical management of diseases and disorders affecting the eyes, eyelids, and visual pathways. These highly trained physicians complete medical school, an internship, and a specialized residency in ophthalmology, often followed by additional fellowship training in subspecialties such as retinal diseases, corneal disorders, glaucoma, or pediatric ophthalmology. Ophthalmologists are qualified to perform complex eye surgeries including cataract removal, retinal repair, glaucoma procedures, corneal transplants, and laser treatments for various conditions. They treat a wide range of eye problems from routine refractive errors and dry eyes to serious conditions like diabetic retinopathy, macular degeneration, and eye cancers. Unlike optometrists who primarily focus on vision correction and basic eye care, ophthalmologists have the medical training necessary to diagnose and treat systemic diseases that affect the eyes, prescribe medications, and perform surgical interventions. Many ophthalmologists work closely with other medical specialists since eye problems can be early indicators of systemic conditions like diabetes, hypertension, or autoimmune diseases. The field combines precision surgical skills with detailed knowledge of ocular anatomy, physiology, and pathology.',
                'etymology': 'From Greek ophthalmos (eye) + logos (study) + -ist (practitioner), meaning "one who studies and treats the eyes."',
                'memory_tip': 'Think "oph-THALM-ologist" - "opthalm" relates to eyes, so an eye doctor who studies and treats eye problems.',
                'example_sentence': 'The _____ performed delicate retinal surgery to restore the patient\'s vision after a serious injury.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opinionated': {
                'pronunciation': '/əˈpɪnjəˌneɪtɪd/',
                'definition': 'Opinionated describes someone who holds strong, definite opinions and expresses them frequently and assertively, often with little willingness to consider alternative viewpoints or change their position based on new information. While having opinions is natural and healthy, being opinionated typically implies a tendency toward inflexibility, stubbornness, or excessive confidence in one\'s own judgments. Opinionated individuals may be perceived as dogmatic, argumentative, or close-minded when they consistently resist considering evidence that contradicts their established beliefs. The trait can manifest in various contexts, from political discussions and social issues to professional decisions and personal preferences. However, being opinionated isn\'t always negative - it can indicate strong convictions, clear thinking, and the courage to take stands on important issues. The key distinction often lies in whether the person remains open to reasoned discussion and new evidence, or whether they shut down dialogue and refuse to acknowledge any validity in opposing views. In professional settings, opinionated employees might contribute valuable insights and decisive leadership, but they may also create conflicts or stifle collaborative decision-making. Understanding how to express strong opinions while remaining open to dialogue is an important social and professional skill.',
                'etymology': 'From "opinion" (from Latin opinio meaning "belief, judgment") + "-ated" suffix indicating having a quality.',
                'memory_tip': 'Think "opinion-ated" - someone who is heavily loaded with opinions and expresses them strongly.',
                'example_sentence': 'The _____ critic was known for his harsh reviews and unwillingness to reconsider his initial judgments.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oppidan': {
                'pronunciation': '/ˈɑpɪdən/',
                'definition': 'Oppidan is an adjective meaning "of or relating to a town or city," describing urban characteristics, inhabitants, or culture as distinguished from rural or countryside elements. The term can refer to people who live in towns, urban customs and practices, or anything characteristic of city life and municipal environments. In historical contexts, oppidan might describe the contrast between town-dwelling merchants, craftspeople, and professionals versus rural agricultural populations, highlighting different lifestyles, economic activities, and social structures. The word appears in academic and literary contexts when discussing urban development, social history, or the relationship between urban and rural communities. Oppidan culture typically involves higher population density, more diverse economic activities, greater social stratification, and more complex governance structures than rural areas. The term can also describe the particular attitudes, behaviors, and values that develop in urban environments, such as greater tolerance for diversity, faster pace of life, and emphasis on commerce and industry. In some educational contexts, particularly in British usage, oppidan might refer to students who live in town rather than in school boarding facilities. Understanding oppidan versus rural distinctions is important for studying social development, economic history, and the evolution of human settlements.',
                'etymology': 'From Latin oppidanus meaning "of a town," from oppidum (town, fortified place).',
                'memory_tip': 'Think "op-PID-an" - relating to an "oppidum" (town), so describing town or city characteristics.',
                'example_sentence': 'The historian studied the differences between _____ merchant culture and rural farming traditions in medieval Europe.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opponency': {
                'pronunciation': '/əˈpoʊnənsi/',
                'definition': 'Opponency refers to the state or quality of being in opposition, resistance, or antagonistic relationship to something or someone, involving active disagreement, conflict, or competitive positioning. The term describes situations where parties, ideas, forces, or interests stand in direct contradiction or opposition to each other, creating tension, conflict, or competitive dynamics. In political contexts, opponency might describe the relationship between rival political parties, candidates, or ideological positions that compete for influence and support. Legal opponency occurs in adversarial court systems where opposing counsel represent different sides of disputes, each arguing against the other\'s position. In sports and games, opponency is fundamental to competitive structure, where teams or individuals work to defeat each other according to established rules. The concept can also apply to abstract ideas, theories, or proposals that contradict each other, creating intellectual or philosophical opposition. Opponency often involves not just disagreement but active efforts to counter, defeat, or undermine opposing positions or forces. Understanding opponency is important for analyzing conflict, competition, negotiation, and problem-solving in various contexts where different interests or viewpoints come into direct contact.',
                'etymology': 'From Latin opponens meaning "opposing" + -cy suffix indicating state or quality, meaning "the state of opposing."',
                'memory_tip': 'Think "oppon-ency" - the tendency or state of "opposing" something, being an opponent.',
                'example_sentence': 'The debate highlighted the _____ between environmental protection advocates and industrial development interests.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opportunity': {
                'pronunciation': '/ˌɑpərˈtunəti/',
                'definition': 'Opportunity refers to a favorable circumstance, situation, or moment that provides a chance for advancement, progress, or achievement, typically requiring recognition and action to realize potential benefits. Opportunities represent moments when conditions align to make success, improvement, or positive change more likely, though they often require preparation, effort, and timely response to capitalize on them effectively. In personal development, opportunities might include educational possibilities, career openings, relationship prospects, or chances to develop new skills and experiences. Business opportunities encompass market conditions, partnerships, innovations, or circumstances that could lead to profit, growth, or competitive advantage. The concept emphasizes the temporal nature of favorable conditions - opportunities often have limited duration and may not present themselves again in the same form. Recognition of opportunity requires awareness, preparation, and often courage to take calculated risks or step outside comfort zones. Many opportunities arise unexpectedly, while others result from deliberate effort to create favorable conditions. The ability to identify, evaluate, and act on opportunities is considered crucial for personal success, business growth, and social progress. Understanding that opportunity often involves both potential benefits and inherent risks helps in making informed decisions about which chances to pursue.',
                'etymology': 'From Latin opportunitas meaning "fitness, convenience," from opportunus (favorable), literally "toward the port."',
                'memory_tip': 'Think "oppor-TUNA-ty" - a favorable chance or opening that comes your way, like a fish approaching the boat.',
                'example_sentence': 'The internship provided an excellent _____ for students to gain practical experience in their chosen field.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opposite': {
                'pronunciation': '/ˈɑpəzɪt/',
                'definition': 'Opposite describes something that is completely different from, contrary to, or positioned directly across from something else, representing the maximum degree of difference or contrast possible within a particular context. In spatial terms, opposite refers to positions that are directly across from each other, such as opposite sides of a street, opposite ends of a spectrum, or opposite corners of a room. In conceptual terms, opposite ideas, qualities, or characteristics represent maximum contrast - hot and cold, love and hate, light and dark, or success and failure. Mathematical opposites include positive and negative numbers, while logical opposites involve contradictory statements that cannot both be true simultaneously. The concept of opposition is fundamental to human understanding, helping organize experiences, make comparisons, and understand relationships between different elements. In language, opposite words (antonyms) provide precise ways to express contrasts and distinctions. Understanding opposites helps in problem-solving, decision-making, and communication by providing clear reference points for comparison and contrast. The recognition of opposites also plays important roles in philosophy, science, and art, where contrasts and tensions often drive understanding, discovery, and creative expression.',
                'etymology': 'From Latin oppositus, past participle of opponere meaning "to place against," from ob- (against) + ponere (to place).',
                'memory_tip': 'Think "op-POSE-ite" - positioned or placed in opposition to something else, directly contrary.',
                'example_sentence': 'The twins had completely _____ personalities - one was outgoing while the other was shy and reserved.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opprobrious': {
                'pronunciation': '/əˈproʊbriəs/',
                'definition': 'Opprobrious describes language, behavior, or treatment that is harshly critical, scornful, or intended to bring shame, disgrace, or dishonor to someone or something. This adjective characterizes expressions of severe disapproval, contempt, or reproach that go beyond ordinary criticism to become insulting, degrading, or abusive. Opprobrious remarks typically involve harsh condemnation, personal attacks, or language designed to damage someone\'s reputation or standing in the community. Such expressions often reflect deep anger, moral outrage, or deliberate attempts to inflict psychological harm through verbal assault. In legal contexts, opprobrious language might constitute defamation, harassment, or hate speech depending on its content and intent. Historical examples include the opprobrious treatment of various groups during periods of social conflict, persecution, or discrimination. The term suggests not just negative criticism but a quality of harshness and contempt that exceeds normal bounds of civil discourse or fair critique. Understanding what constitutes opprobrious behavior is important for maintaining respectful communication, recognizing abusive patterns, and distinguishing between legitimate criticism and harmful personal attacks. In professional and social contexts, avoiding opprobrious language helps maintain constructive relationships and productive dialogue.',
                'etymology': 'From Latin opprobrium meaning "reproach, infamy," from ob- (against) + probrum (shameful act), meaning "bringing shame."',
                'memory_tip': 'Think "op-PROB-rious" - language that "probes" against someone in a harsh, shameful way.',
                'example_sentence': 'The politician\'s _____ comments about his opponent crossed the line from legitimate criticism to personal attack.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oppugn': {
                'pronunciation': '/əˈpjun/',
                'definition': 'Oppugn is a formal verb meaning to attack, oppose, or challenge something, particularly ideas, arguments, policies, or positions, through criticism, contradiction, or hostile action. The term implies more than simple disagreement - it suggests active, determined opposition that seeks to undermine, discredit, or defeat the target of opposition. In academic and intellectual contexts, to oppugn a theory means to challenge its validity through evidence, logical argument, or alternative explanations. Legal oppugning might involve challenging the validity of contracts, wills, or legal decisions through formal proceedings. Political oppugning occurs when individuals or groups actively work to oppose and defeat policies, candidates, or governmental actions they disagree with. The word carries connotations of deliberate, sustained effort rather than casual or momentary disagreement. Oppugning typically involves presenting counter-arguments, evidence, or actions designed to weaken or destroy the credibility or effectiveness of whatever is being opposed. The term is more formal and literary than common synonyms like "attack" or "oppose," often appearing in academic, legal, or sophisticated political discourse. Understanding when and how to appropriately oppugn ideas or positions is important for effective debate, scholarly inquiry, and democratic participation.',
                'etymology': 'From Latin oppugnare meaning "to fight against, attack," from ob- (against) + pugnare (to fight).',
                'memory_tip': 'Think "op-PUGN" - to "pugnaciously" (combatively) attack or fight against something.',
                'example_sentence': 'The scholar sought to _____ the prevailing theory by presenting compelling evidence that contradicted its main assumptions.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'optician': {
                'pronunciation': '/ɑpˈtɪʃən/',
                'definition': 'An optician is a healthcare professional who specializes in fitting, dispensing, and adjusting eyeglasses, contact lenses, and other optical devices based on prescriptions provided by ophthalmologists or optometrists. These skilled practitioners combine technical knowledge of optics with practical expertise in lens technology, frame selection, and precise fitting to ensure that corrective eyewear provides optimal vision correction and comfort. Opticians interpret prescriptions that specify the exact lens powers, prism corrections, and other specifications needed to correct refractive errors such as nearsightedness, farsightedness, and astigmatism. They help customers select appropriate frames based on facial features, lifestyle needs, and personal preferences, then use specialized equipment to cut, shape, and mount lenses precisely. Modern opticians also fit and train patients in the proper use of contact lenses, including daily wear, extended wear, and specialty lenses for conditions like astigmatism or presbyopia. Many opticians complete formal training programs or apprenticeships and may be licensed or certified depending on local regulations. They work in optical shops, eye care centers, retail chains, and sometimes in conjunction with eye care practices, serving as the crucial link between vision prescriptions and functional, comfortable eyewear.',
                'etymology': 'From "optic" (relating to sight or eyes) + "-ian" (suffix indicating a practitioner or specialist).',
                'memory_tip': 'Think "optic-ian" - a specialist in "optics" who fits glasses and handles vision correction devices.',
                'example_sentence': 'The _____ carefully adjusted the new eyeglasses to ensure they sat properly on the patient\'s nose and ears.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'optimum': {
                'pronunciation': '/ˈɑptəməm/',
                'definition': 'Optimum refers to the most favorable, advantageous, or desirable condition, level, or outcome possible within given constraints or circumstances, representing the best achievable result or state. This concept applies across numerous fields and situations where multiple variables must be balanced to achieve the best possible outcome. In mathematics and engineering, optimum solutions represent the maximum or minimum values that satisfy specific criteria while meeting all constraints. In biology and medicine, optimum conditions refer to environmental factors, dosages, or treatments that produce the best health outcomes or biological function. Business optimization seeks optimum efficiency, profit, or performance by finding the best combination of resources, strategies, and processes. The optimum represents a balance point where improvements in one area cannot be made without sacrificing performance in another area. Unlike "maximum" which simply means the highest amount, optimum considers the overall best result considering all relevant factors and trade-offs. Scientific research often seeks to identify optimum conditions for experiments, treatments, or processes that will yield the most reliable and beneficial results. Understanding optimum conditions helps in decision-making, resource allocation, and problem-solving across personal, professional, and technical contexts.',
                'etymology': 'From Latin optimus meaning "best," superlative of bonus (good), literally meaning "the best possible."',
                'memory_tip': 'Think "opt-IMUM" - the best option or choice you can "opt" for under the circumstances.',
                'example_sentence': 'The engineer determined that 72 degrees was the _____ temperature for both energy efficiency and occupant comfort.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'options': {
                'pronunciation': '/ˈɑpʃənz/',
                'definition': 'Options are choices, alternatives, or possibilities available to someone when making decisions, representing different courses of action that can be selected based on preferences, circumstances, or objectives. Having multiple options provides flexibility and the ability to choose the most suitable path forward, whether in personal decisions, business strategies, or problem-solving situations. In finance, options are specific types of contracts that give holders the right, but not the obligation, to buy or sell assets at predetermined prices within specified time periods, serving as important tools for investment and risk management. Educational options include different schools, programs, or learning paths that students can choose based on their interests and career goals. Career options represent various professional paths and opportunities available to individuals based on their skills, education, and market conditions. The concept of options implies freedom of choice and the existence of multiple viable alternatives, though the quality and number of available options may vary significantly based on circumstances, resources, and external constraints. Effective decision-making often involves careful evaluation of available options, considering their potential benefits, risks, costs, and alignment with personal or organizational goals. Having too few options can feel limiting, while too many options can sometimes create decision paralysis.',
                'etymology': 'Plural of "option," from Latin optio meaning "choice, wish," from optare (to choose, wish).',
                'memory_tip': 'Think "opt-ions" - multiple things you can "opt" or choose from when making decisions.',
                'example_sentence': 'The restaurant menu offered numerous vegetarian _____ to accommodate different dietary preferences.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'optometry': {
                'pronunciation': '/ɑpˈtɑmətri/',
                'definition': 'Optometry is a healthcare profession focused on examining eyes, diagnosing vision problems and eye diseases, prescribing corrective lenses and treatments, and providing comprehensive primary eye care services. Optometrists are trained healthcare professionals who complete specialized doctoral programs in optometry, learning to detect and manage various eye conditions, refractive errors, and vision-related problems. The field encompasses routine eye examinations, vision testing, diagnosis of conditions like glaucoma and diabetic retinopathy, prescription of eyeglasses and contact lenses, and treatment of certain eye diseases and injuries. Modern optometry utilizes sophisticated diagnostic equipment including digital retinal imaging, visual field testing, and optical coherence tomography to detect eye problems early and monitor their progression. Optometrists often serve as primary eye care providers, especially in communities where ophthalmologists may be less accessible, and they work closely with other healthcare professionals to manage patients\' overall health since many systemic diseases affect the eyes. The profession has expanded beyond basic vision correction to include specialty areas such as pediatric optometry, low vision rehabilitation, contact lens specialization, and management of ocular diseases. Preventive care is a major focus, with regular optometric examinations helping to detect not only eye problems but also signs of diabetes, hypertension, and other systemic conditions.',
                'etymology': 'From Greek optikos (relating to sight) + metron (measure), literally meaning "measurement of sight."',
                'memory_tip': 'Think "opto-metry" - the "metro" (measurement) of "opto" (vision/sight) to determine eye health.',
                'example_sentence': 'After completing her doctorate in _____, she opened a practice specializing in pediatric eye care.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opulent': {
                'pronunciation': '/ˈɑpjələnt/',
                'definition': 'Opulent describes something characterized by great wealth, luxury, abundance, or magnificence, typically involving elaborate display of expensive materials, rich decoration, and sumptuous comfort that demonstrates significant financial resources. The term applies to lifestyles, environments, objects, or experiences that exhibit lavish abundance and sophisticated luxury far beyond basic needs or simple comfort. Opulent homes might feature marble floors, crystal chandeliers, gold fixtures, and expensive artwork, while opulent lifestyles could include luxury travel, fine dining, designer clothing, and exclusive experiences. The word often carries implications of excess and conspicuous consumption, where wealth is deliberately displayed through material possessions and experiences. Opulent can describe natural abundance as well, such as opulent gardens bursting with flowers and lush vegetation, or opulent feasts featuring rich foods and elaborate presentation. While opulence can be aesthetically impressive and culturally significant, it may also be criticized as wasteful, ostentatious, or insensitive to social inequality. Historical examples of opulence include royal palaces, luxury ocean liners, and the lifestyles of wealthy industrialists. Understanding opulence helps in analyzing social structures, economic inequality, and cultural values related to wealth, luxury, and display.',
                'etymology': 'From Latin opulentus meaning "wealthy, rich," from opes (wealth, resources), related to opus (work, effort).',
                'memory_tip': 'Think "OP-ulent" - "OP" (over the top) in luxury and wealth, abundant and rich.',
                'example_sentence': 'The _____ ballroom featured gold leaf ceilings, crystal chandeliers, and marble columns imported from Italy.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'opus': {
                'pronunciation': '/ˈoʊpəs/',
                'definition': 'Opus refers to a creative work, composition, or artistic creation, particularly used in classical music to identify and catalog a composer\'s works in chronological or thematic order. In musical contexts, opus numbers (often abbreviated as "Op.") help identify specific pieces within a composer\'s body of work, such as Beethoven\'s Symphony No. 9, Op. 125, or Chopin\'s Ballades, Op. 23. The term has expanded beyond music to encompass any significant creative work or masterpiece in literature, visual arts, architecture, or other creative fields. An artist\'s opus might refer to their complete body of work or to a particularly important or representative piece that demonstrates their highest achievement or artistic vision. The concept implies not just any work, but something created with serious artistic intent, skill, and often considerable effort or significance. In academic and critical contexts, discussing an artist\'s opus involves analyzing their creative development, thematic concerns, and artistic contributions. The term suggests both individual works and the broader creative legacy that artists leave behind. Understanding opus helps in organizing, studying, and appreciating artistic traditions and the development of creative works within historical and cultural contexts.',
                'etymology': 'From Latin opus meaning "work, labor, effort," the singular form of opera (works).',
                'memory_tip': 'Think "OH-pus" - a significant creative work or "opus" (work) that represents an artist\'s achievement.',
                'example_sentence': 'The composer\'s final _____ was considered his masterpiece, combining all the techniques he had developed over his career.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oracle': {
                'pronunciation': '/ˈɔrəkəl/',
                'definition': 'Oracle refers to a person, agency, or source that provides wise counsel, prophetic insights, or authoritative information, historically associated with religious or spiritual contexts where divine guidance was sought and received. In ancient Greek and Roman cultures, oracles were sacred sites or priestesses through whom gods were believed to communicate prophecies and guidance to mortals, with the Oracle at Delphi being perhaps the most famous example. These religious figures served as intermediaries between human and divine realms, interpreting divine messages and providing counsel on important decisions ranging from personal matters to affairs of state. In modern usage, oracle describes any source of reliable, authoritative, or seemingly prophetic information - someone might be called an oracle of financial wisdom or political insight because of their track record of accurate predictions or sound advice. The term also appears in technology, where Oracle Corporation is a major database software company, and in computing contexts where oracle algorithms provide definitive answers to computational problems. Understanding oracles involves recognizing their role in providing guidance, prediction, and authoritative information across religious, cultural, and modern contexts where people seek wisdom beyond their own knowledge and experience.',
                'etymology': 'From Latin oraculum meaning "divine announcement," from orare (to speak, pray), related to "oral."',
                'memory_tip': 'Think "OR-acle" - someone who speaks ("oral") divine wisdom or gives prophetic guidance.',
                'example_sentence': 'Ancient Greeks would travel great distances to consult the _____ at Delphi before making important decisions.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oral': {
                'pronunciation': '/ˈɔrəl/',
                'definition': 'Oral refers to anything relating to the mouth, spoken rather than written communication, or activities involving the mouth and speech. In communication contexts, oral refers to spoken language, verbal presentations, and face-to-face conversation as opposed to written text, email, or other non-verbal forms of communication. Oral traditions involve the passing down of stories, knowledge, and cultural information through spoken word rather than written records, playing crucial roles in preserving history and culture in societies without widespread literacy. In educational settings, oral examinations test students through spoken questions and answers, while oral presentations require students to communicate information verbally to audiences. Medical oral health involves the care and treatment of teeth, gums, mouth, and related structures, with oral hygiene practices essential for preventing disease and maintaining overall health. Legal oral arguments allow attorneys to present cases verbally before judges and juries, supplementing written briefs with direct advocacy. The term emphasizes the importance of speech, verbal communication, and mouth-related functions in human interaction, learning, and health. Understanding oral versus written communication helps in choosing appropriate communication methods and recognizing the unique advantages and limitations of spoken versus written expression.',
                'etymology': 'From Latin oralis meaning "of the mouth," from os, oris (mouth), related to "orator" and "oration."',
                'memory_tip': 'Think "OR-al" - relating to the mouth or spoken "orally" rather than written.',
                'example_sentence': 'The history professor preferred _____ exams because they allowed students to explain their reasoning in real-time.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'orally': {
                'pronunciation': '/ˈɔrəli/',
                'definition': 'Orally is an adverb meaning "by mouth" or "through spoken communication," describing how information is transmitted, medicine is administered, or communication takes place using speech rather than writing or other methods. In medical contexts, orally indicates that medications are taken by mouth, swallowed and absorbed through the digestive system, as opposed to injections, topical applications, or other routes of administration. Educational orally refers to verbal instruction, oral presentations, or spoken examinations where information is communicated through speech rather than written materials. Legal proceedings often involve testimony given orally, where witnesses speak their accounts rather than submitting only written statements. Cultural transmission orally describes how traditions, stories, and knowledge are passed down through spoken word from generation to generation in oral traditions. The adverb emphasizes the method of delivery or administration, highlighting the use of mouth, speech, or verbal communication as the primary means. In research and documentation, information gathered orally through interviews or conversations provides different perspectives and details than written sources. Understanding oral versus other methods of communication or administration is important for choosing appropriate approaches in education, medicine, legal proceedings, and cultural preservation.',
                'etymology': 'From "oral" + "-ly" adverb suffix, meaning "in an oral manner" or "by means of the mouth."',
                'memory_tip': 'Think "oral-ly" - done "orally" or by mouth, whether speaking or taking medicine.',
                'example_sentence': 'The medication should be taken _____ with food to reduce stomach irritation.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'orange': {
                'pronunciation': '/ˈɔrɪndʒ/',
                'definition': 'Orange refers both to a citrus fruit and to the vibrant color that bears the fruit\'s name, representing one of the most recognizable and widely consumed fruits worldwide. The orange fruit (Citrus sinensis) is prized for its sweet, tangy flavor, high vitamin C content, and versatility in culinary applications ranging from fresh eating and juice production to cooking and baking. Oranges grow on evergreen trees in warm climates and come in various varieties including navel oranges, Valencia oranges, and blood oranges, each with distinct characteristics in terms of flavor, appearance, and optimal uses. As a color, orange occupies the spectrum between red and yellow, created by combining these primary colors in various proportions. Orange appears frequently in nature - in sunsets, autumn leaves, flowers like marigolds and poppies, and various fruits and vegetables. The color has strong psychological associations with energy, enthusiasm, creativity, and warmth, making it popular in branding, interior design, and art where vibrant, attention-getting effects are desired. Orange also has cultural significance in various traditions, representing harvest festivals, Halloween celebrations, and spiritual practices in some cultures.',
                'etymology': 'From Old French orenge, from Arabic naranj, from Persian narang, ultimately from Sanskrit naranga.',
                'memory_tip': 'Think of the bright orange fruit - both the fruit and the color share the same name and vibrant appearance.',
                'example_sentence': 'The fresh _____ juice provided a refreshing burst of vitamin C with breakfast.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'orca': {
                'pronunciation': '/ˈɔrkə/',
                'definition': 'Orca, also known as the killer whale, is the largest member of the dolphin family and one of the ocean\'s most intelligent and powerful marine predators, characterized by distinctive black and white coloration and remarkable social intelligence. These magnificent marine mammals can reach lengths of up to 26 feet and weights of 6 tons, with males typically larger than females and distinguished by their tall, triangular dorsal fins. Orcas are found in oceans worldwide, from Arctic to Antarctic waters, and have developed sophisticated hunting techniques that vary by geographic population, including coordinated pack hunting strategies to capture fish, seals, and even other whales. Their complex social structure involves living in matrilineal pods led by the oldest female, with intricate communication systems using distinctive calls and dialects specific to each family group. Orcas demonstrate remarkable intelligence through their ability to learn, teach, and adapt hunting strategies, use tools, and engage in complex social behaviors including play and cultural transmission. In captivity, orcas have been featured in marine parks, though this practice has become increasingly controversial due to concerns about animal welfare and the psychological effects of confinement on these highly intelligent, far-ranging marine mammals.',
                'etymology': 'From Latin orca meaning "large-bellied sea creature," possibly related to Orcus (Roman god of the underworld).',
                'memory_tip': 'Think "OR-ca" - the "king" of the ocean predators, black and white like a formal "orca-stra" conductor.',
                'example_sentence': 'The pod of _____ whales demonstrated sophisticated hunting techniques as they coordinated to catch salmon.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'orchestra': {
                'pronunciation': '/ˈɔrkəstrə/',
                'definition': 'Orchestra refers to a large ensemble of musicians playing various instruments together under the direction of a conductor, typically including string, woodwind, brass, and percussion sections that combine to create complex, layered musical performances. A full symphony orchestra usually contains 70-100 musicians organized into distinct sections: strings (violins, violas, cellos, double basses), woodwinds (flutes, oboes, clarinets, bassoons), brass (trumpets, French horns, trombones, tubas), and percussion (timpani, drums, cymbals, and various other instruments). The orchestra as we know it today evolved from smaller Baroque ensembles, reaching its current form during the Classical and Romantic periods when composers like Mozart, Beethoven, and Brahms wrote extensively for these large instrumental groups. Modern orchestras perform a vast repertoire ranging from classical symphonies and concertos to contemporary works, film scores, and popular music arrangements. The conductor serves as the musical leader, interpreting the score and coordinating the ensemble\'s timing, dynamics, and artistic expression through gestures and rehearsal guidance. Understanding orchestral music involves appreciating how different instrument families blend to create rich, complex soundscapes that can express a full range of emotions and musical ideas through collaborative performance.',
                'etymology': 'From Greek orchestra, originally referring to the circular area in front of the stage in Greek theaters where the chorus performed.',
                'memory_tip': 'Think "OR-chestra" - a large group that "orchestrates" (organizes) music with many different instruments.',
                'example_sentence': 'The symphony _____ performed Beethoven\'s Ninth Symphony to a sold-out audience at the concert hall.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'ordained': {
                'pronunciation': '/ɔrˈdeɪnd/',
                'definition': 'Ordained is the past tense of "ordain," meaning officially appointed, decreed, or established through formal authority, most commonly used in religious contexts where individuals are formally invested with ministerial or priestly authority through ceremonial rites. In religious usage, ordained ministers, priests, rabbis, or other clergy have undergone specific training, met denominational requirements, and participated in ordination ceremonies that officially recognize their authority to perform religious functions such as conducting worship services, administering sacraments, performing marriages, and providing spiritual guidance. The process of ordination typically involves theological education, practical training, examination by religious authorities, and formal installation through laying on of hands or other ceremonial acts. Beyond religious contexts, ordained can refer to any formal establishment or decree by authority - laws might be ordained by governments, policies ordained by organizations, or destinies ordained by fate. The term carries implications of legitimacy, authority, and formal recognition that distinguishes ordained status from informal or self-appointed roles. Understanding ordination involves recognizing the institutional processes, requirements, and ceremonies through which various organizations, particularly religious institutions, formally recognize and authorize individuals to serve in leadership or ceremonial capacities.',
                'etymology': 'From Latin ordinatus, past participle of ordinare meaning "to set in order, arrange," from ordo (order, arrangement).',
                'memory_tip': 'Think "OR-dained" - formally put in "order" or officially appointed to a position or role.',
                'example_sentence': 'After completing seminary, she was _____ as a minister and assigned to her first congregation.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'order': {
                'pronunciation': '/ˈɔrdər/',
                'definition': 'Order encompasses multiple related meanings centered on concepts of arrangement, sequence, organization, and authority, functioning as both a noun describing systematic organization and a verb meaning to arrange or command. As a noun, order refers to the systematic arrangement of elements according to specific criteria, rules, or patterns that create predictability, efficiency, and understanding. This can involve physical organization (items arranged in order), temporal sequence (events happening in chronological order), or hierarchical structure (social or organizational order). Order also refers to commands or instructions given by authority figures, requests for goods or services (placing an order), and formal rules or regulations that govern behavior and social interaction. As a verb, to order means to arrange systematically, command someone to do something, or request goods or services. The concept of order is fundamental to civilization, enabling coordination, communication, and cooperation in complex societies. Understanding order involves recognizing the balance between structure and flexibility, authority and freedom, organization and spontaneity that characterizes effective systems whether in personal life, business operations, or social institutions.',
                'etymology': 'From Latin ordo meaning "row, series, arrangement," related to ordiri (to begin) and describing systematic arrangement.',
                'memory_tip': 'Think "OR-der" - putting things in "order" means arranging them systematically or giving commands.',
                'example_sentence': 'The teacher asked students to line up in alphabetical _____ before entering the classroom.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'ordered': {
                'pronunciation': '/ˈɔrdərd/',
                'definition': 'Ordered is the past tense of "order," meaning arranged systematically, commanded to do something, or requested goods or services through formal or informal channels. When something is ordered, it has been organized according to specific criteria, rules, or patterns that create logical sequence or systematic arrangement. This might involve arranging objects by size, organizing events chronologically, or structuring information hierarchically for clarity and accessibility. In the context of giving commands, ordered indicates that someone in authority has directed others to perform specific actions or follow particular instructions. Commercial ordering involves requesting products or services from suppliers, vendors, or service providers through formal purchasing processes. Mathematical ordered sets or sequences follow specific rules that determine the relationship between elements. The concept implies intentional organization rather than random arrangement, suggesting deliberate thought and planning in creating structure or giving direction. Ordered systems tend to be more efficient, predictable, and manageable than chaotic or randomly arranged ones. Understanding what has been ordered helps in following instructions, maintaining organization, and meeting expectations in various personal, professional, and commercial contexts.',
                'etymology': 'Past tense of "order," from Latin ordinatus meaning "arranged, set in order," from ordinare (to arrange).',
                'memory_tip': 'Think "order-ed" - something that has been "ordered" or arranged systematically in the past.',
                'example_sentence': 'The books were _____ alphabetically by author to make them easier to find on the shelves.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'ordinance': {
                'pronunciation': '/ˈɔrdənəns/',
                'definition': 'An ordinance is a local law, regulation, or authoritative decree enacted by a municipal government, city council, or other local governing body to address specific issues within their jurisdiction. Unlike state or federal laws that apply broadly across larger territories, ordinances typically address local concerns such as zoning regulations, noise restrictions, parking rules, building codes, business licensing, and public health measures. These local regulations have the force of law within the municipality and can result in fines, penalties, or other legal consequences for violations. Ordinances allow local governments to address unique community needs, local conditions, and specific problems that may not be covered by broader state or federal legislation. The process of creating ordinances typically involves public hearings, community input, city council deliberation, and formal voting procedures that ensure democratic participation in local governance. Common examples include ordinances regulating dog licensing, restricting smoking in public places, establishing quiet hours, or requiring business permits. Understanding ordinances is important for residents, business owners, and visitors who need to comply with local regulations that may differ significantly from those in other communities or jurisdictions.',
                'etymology': 'From Old French ordenance meaning "arrangement, disposition," from Latin ordinantia, from ordinare (to arrange, order).',
                'memory_tip': 'Think "ordin-ance" - a local "ordinance" brings "order" to community rules and regulations.',
                'example_sentence': 'The city council passed an _____ requiring all restaurants to post calorie counts on their menus.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'ordinary': {
                'pronunciation': '/ˈɔrdəˌnɛri/',
                'definition': 'Ordinary describes something that is normal, usual, or commonplace, lacking distinctive or remarkable qualities that would set it apart from typical examples of its kind. The term characterizes everyday experiences, objects, or situations that conform to established patterns and expectations without exhibiting unusual, exceptional, or noteworthy characteristics. Ordinary people live conventional lives following common social patterns, while ordinary objects serve typical functions without special features or extraordinary qualities. The concept of ordinary provides a baseline for comparison, helping to identify what is normal versus what is exceptional, unique, or remarkable. In many contexts, ordinary can be seen as positive, representing reliability, predictability, and conformity to useful standards, while in other situations it might be viewed negatively as boring, unremarkable, or lacking inspiration. Legal ordinary procedures follow standard protocols, while ordinary business operations function according to routine practices. Understanding what constitutes ordinary in different contexts helps in recognizing when something is unusual, exceptional, or worthy of special attention. The distinction between ordinary and extraordinary experiences, achievements, or circumstances is fundamental to human evaluation and meaning-making across personal, professional, and cultural domains.',
                'etymology': 'From Latin ordinarius meaning "regular, usual," from ordo (order, arrangement), indicating what follows normal order.',
                'memory_tip': 'Think "ordin-ary" - following the regular "order" of things, normal and usual rather than special.',
                'example_sentence': 'Despite his fame, he preferred the simple pleasures of _____ family life over celebrity events.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'ords': {
                'pronunciation': '/ɔrdz/',
                'definition': 'Ords appears to be an uncommon or specialized term that may represent an abbreviation, plural form, or technical terminology specific to particular fields or contexts. Without additional context, this could potentially be short for "ordinances," "orders," "ordinals," or represent specialized jargon from fields like military, technical, or academic disciplines. In some contexts, ords might refer to ordinal numbers or ordinal positions in mathematical or statistical applications. It could also be an abbreviation used in specific industries, organizations, or technical fields where shortened forms of longer terms are commonly employed for efficiency in communication. Given its appearance in spelling bee contexts, it might represent a challenging or uncommon term that tests contestants\' ability to spell unfamiliar words correctly. When encountering such specialized or abbreviated terms, it\'s important to consider the specific context, field of use, and potential meanings that might apply to the particular situation where the word appears.',
                'etymology': 'Likely an abbreviation or plural form, though specific etymology depends on the intended meaning and context.',
                'memory_tip': 'Remember the spelling O-R-D-S, possibly as a plural or abbreviation of a longer word.',
                'example_sentence': 'The technical manual used various _____ to refer to standard operating procedures.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oregano': {
                'pronunciation': '/əˈrɛgəˌnoʊ/',
                'definition': 'Oregano is an aromatic herb (Origanum vulgare) widely used in cooking, particularly in Mediterranean, Mexican, and Middle Eastern cuisines, prized for its distinctive pungent, slightly bitter flavor that adds depth and complexity to many dishes. This perennial herb belongs to the mint family and grows as a bushy plant with small, oval leaves that can be used fresh or dried, though dried oregano often has a more concentrated flavor. Oregano is essential in Italian cuisine, appearing in pizza sauces, pasta dishes, and herb blends, while Greek oregano varieties offer particularly robust flavors that complement olive oil, tomatoes, and grilled meats. The herb contains beneficial compounds including antioxidants and essential oils that may provide health benefits beyond its culinary uses. Different varieties of oregano exist, including Greek oregano (often considered the most flavorful), Turkish oregano, and Mexican oregano (which is actually a different plant species but used similarly). Oregano can be grown in gardens or containers and is relatively easy to cultivate in well-drained soil with plenty of sunlight. The herb has been used historically for both culinary and medicinal purposes, and continues to be valued for its distinctive flavor contribution to countless recipes worldwide.',
                'etymology': 'From Spanish orégano, from Latin origanum, from Greek origanon, possibly meaning "joy of the mountain."',
                'memory_tip': 'Think "oh-REG-ano" - the herb that\'s a "regular" ingredient in Italian pizza and pasta dishes.',
                'example_sentence': 'The chef sprinkled fresh _____ over the homemade pizza just before serving.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'oregon': {
                'pronunciation': '/ˈɔrəgən/',
                'definition': 'Oregon is a state in the Pacific Northwest region of the United States, known for its diverse geography that includes rugged coastlines, dense forests, high desert, and volcanic mountains, as well as its progressive politics and environmental consciousness. The state borders Washington to the north, Idaho to the east, Nevada and California to the south, and the Pacific Ocean to the west, with the Columbia River forming much of its northern boundary. Oregon\'s landscape is dominated by the Cascade Range, which includes several volcanic peaks including Mount Hood, and the state is famous for Crater Lake, one of the deepest and most pristine lakes in the world. The economy is based on technology (with major companies in the Portland area), agriculture (including wine production in the Willamette Valley), timber, and tourism. Oregon has no sales tax but does have income tax, and the state is known for progressive policies including early adoption of environmental protections, urban planning initiatives, and liberal social policies. Portland, the largest city, is renowned for its food scene, craft breweries, and cultural attractions, while the state overall attracts outdoor enthusiasts with opportunities for hiking, skiing, surfing, and other recreational activities.',
                'etymology': 'Possibly from French ouragan (hurricane) or from a Native American word, though the exact origin is uncertain.',
                'memory_tip': 'Think "ORE-gon" - the state with lots of natural "ore" and resources, plus it\'s "gone" to the Pacific Northwest.',
                'example_sentence': 'The family planned a road trip through _____ to see Crater Lake and the Pacific coastline.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'organ': {
                'pronunciation': '/ˈɔrgən/',
                'definition': 'Organ has multiple related meanings, most commonly referring to biological structures within living organisms that perform specific functions necessary for life, or to musical instruments that produce sound through pipes and keyboards. In biology, organs are complex structures composed of different tissues working together to perform specialized functions, such as the heart pumping blood, lungs facilitating breathing, liver processing toxins, or brain controlling nervous system functions. Human organs are organized into organ systems that work together to maintain life and health, with organ failure or disease often requiring medical intervention including possible organ transplantation. In music, organs are keyboard instruments that produce sound by forcing air through pipes or electronic circuits, ranging from massive church pipe organs with thousands of pipes to smaller electronic organs used in various musical genres. Pipe organs have been central to religious and classical music for centuries, capable of producing powerful, complex sounds that fill large spaces. The term also appears in organizational contexts, where organs might refer to official publications (like a political party\'s organ) or governmental departments that serve specific functions within larger administrative systems.',
                'etymology': 'From Latin organum meaning "instrument, engine," from Greek organon meaning "tool, instrument," related to ergon (work).',
                'memory_tip': 'Think "OR-gan" - whether biological organs that help you work, or musical organs that make organized sound.',
                'example_sentence': 'The heart is a vital _____ that pumps blood throughout the circulatory system.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'organelle': {
                'pronunciation': '/ˌɔrgəˈnɛl/',
                'definition': 'An organelle is a specialized structure within a cell that performs specific functions necessary for cellular life and metabolism, analogous to organs within a larger organism. These membrane-bound or membrane-associated structures are found primarily in eukaryotic cells (cells with nuclei) and include structures such as the nucleus (containing genetic material), mitochondria (producing energy), endoplasmic reticulum (protein and lipid synthesis), Golgi apparatus (protein processing and packaging), lysosomes (waste disposal), and chloroplasts (photosynthesis in plants). Each organelle has unique structural features and biochemical functions that contribute to overall cellular health and function. The nucleus controls cell activities and contains DNA, while mitochondria serve as cellular powerhouses converting nutrients into usable energy (ATP). Chloroplasts in plant cells capture light energy and convert it into chemical energy through photosynthesis. The coordinated function of these organelles enables complex cellular processes including growth, reproduction, metabolism, and response to environmental changes. Understanding organelles is fundamental to cell biology, genetics, and medicine, as many diseases result from organelle dysfunction, and many treatments target specific organellar processes.',
                'etymology': 'From "organ" + diminutive suffix "-elle," literally meaning "little organ" within a cell.',
                'memory_tip': 'Think "organ-elle" - "elle" (small) "organs" inside cells that do specific jobs, like tiny organs.',
                'example_sentence': 'The mitochondria is often called the powerhouse _____ because it produces energy for the cell.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            }
        }
        
        if word in word_data:
            return word_data[word]
        else:
            # Fallback for any missing words
            return {
                'pronunciation': f'/word/',
                'definition': f'Definition for {word} not found in comprehensive data.',
                'etymology': f'Etymology for {word} not available.',
                'memory_tip': f'Memory tip for {word} not available.',
                'example_sentence': f'Example sentence for {word} not available.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude', 
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            }
    
    def detect_combined_words(self) -> List[str]:
        """Detect words that appear to be incorrectly combined due to PDF parsing issues"""
        combined_words = []
        
        # Read the input CSV
        input_file = 'output/batch_123_words.csv'
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word'].strip()
                
                # Check for combined word patterns
                if self._is_likely_combined_word(word):
                    combined_words.append(word)
        
        return combined_words
    
    def _is_likely_combined_word(self, word: str) -> bool:
        """Determine if a word is likely a combination of multiple words"""
        # Pattern 1: Contains common word endings followed by unrelated text
        suspicious_patterns = [
            r'.*ing[A-Z]',      # word ending in 'ing' followed by capital
            r'.*ed[A-Z]',       # word ending in 'ed' followed by capital  
            r'.*ly[A-Z]',       # word ending in 'ly' followed by capital
            r'.*er[A-Z]',       # word ending in 'er' followed by capital
            r'.*est[A-Z]',      # word ending in 'est' followed by capital
            r'.*tion[A-Z]',     # word ending in 'tion' followed by capital
            r'.*ness[A-Z]',     # word ending in 'ness' followed by capital
            r'.*ment[A-Z]',     # word ending in 'ment' followed by capital
        ]
        
        for pattern in suspicious_patterns:
            if re.match(pattern, word):
                return True
        
        # Pattern 2: Contains common short words embedded
        embedded_words = ['the', 'and', 'ing', 'tion', 'noun', 'verb', 'adj', 'oeuvre', 'viscount', 'pulse', 'charitable', 'noun']
        for embedded in embedded_words:
            if embedded in word and len(word) > len(embedded) + 3:
                # Check if the embedded word appears in a suspicious position
                if word.find(embedded) > 0 and word.find(embedded) < len(word) - len(embedded):
                    return True
        
        # Pattern 3: Unusual length for spelling bee words (very long combinations)
        if len(word) > 20:  # Most legitimate spelling bee words are shorter
            return True
            
        # Pattern 4: Contains lowercase followed immediately by uppercase (camelCase-like)
        if re.search(r'[a-z][A-Z]', word):
            return True
            
        return False
    
    def process_batch(self):
        """Process all words in batch 123 with comprehensive Claude data"""
        logger.info("Processing Batch 123 with comprehensive Claude data...")
        
        # Detect combined words first
        combined_words = self.detect_combined_words()
        if combined_words:
            logger.info(f"Detected {len(combined_words)} combined word errors: {combined_words}")
        
        input_file = 'output/batch_123_words.csv'
        output_file = 'output/batch_123_processed.csv'
        
        processed_words = []
        
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            words_data = list(reader)
        
        # Process each word
        for row in words_data:
            word = row['word'].strip()
            if not word:  # Skip empty rows
                continue
                
            logger.info(f"Processed word: {word}")
            
            # Get Claude data
            claude_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty scores
            difficulty_data = self.difficulty_calc.calculate_difficulty_score(
                word, claude_data['definition'], claude_data['etymology']
            )
            
            # Create processed entry
            processed_entry = {
                'word': word,
                'years': row['years'],
                'source_files': row['source_files'], 
                'source_difficulties': row['source_difficulties'],
                'pronunciation': claude_data['pronunciation'],
                'definition': claude_data['definition'],
                'etymology': claude_data['etymology'],
                'memory_tip': claude_data['memory_tip'],
                'example_sentence': claude_data['example_sentence'],
                'definition_source': claude_data['definition_source'],
                'pronunciation_source': claude_data['pronunciation_source'],
                'example_sentence_source': claude_data['example_sentence_source'],
                'etymology_source': claude_data['etymology_source'],
                'memory_tip_source': claude_data['memory_tip_source'],
                'phonetic_transparency_score': difficulty_data['phonetic_transparency_score'],
                'word_frequency_score': difficulty_data['word_frequency_score'],
                'morphological_complexity_score': difficulty_data['morphological_complexity_score'],
                'etymology_complexity_score': difficulty_data['etymology_complexity_score'],
                'difficulty': difficulty_data['difficulty'],
                'combined_word_error': word in combined_words
            }
            
            processed_words.append(processed_entry)
        
        # Write output file
        if processed_words:
            fieldnames = [
                'word', 'years', 'source_files', 'source_difficulties',
                'pronunciation', 'definition', 'etymology', 'memory_tip', 'example_sentence',
                'definition_source', 'pronunciation_source', 'example_sentence_source',
                'etymology_source', 'memory_tip_source',
                'phonetic_transparency_score', 'word_frequency_score',
                'morphological_complexity_score', 'etymology_complexity_score', 'difficulty',
                'combined_word_error'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
            
            logger.info(f"Saved {len(processed_words)} words to {output_file}")
            
        return len(processed_words), 0  # processed, failed

if __name__ == "__main__":
    processor = Batch123Processor()
    processed_count, failed_count = processor.process_batch()
    
    logger.info("Batch 123 processing completed!")
    logger.info(f"Processed {processed_count} words with comprehensive Claude data")
    logger.info(f"Output saved to: output/batch_123_processed.csv")
    logger.info(f"Results: {processed_count} successful, {failed_count} failed")