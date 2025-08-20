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

class Batch120Processor:
    """Process spelling bee words for Batch 120 with comprehensive Claude data"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word using Claude knowledge"""
        
        word_data = {
            'norovirus': {
                'pronunciation': '/ˈnɔroʊˌvaɪrəs/',
                'definition': 'Norovirus is a highly contagious virus that causes gastroenteritis, commonly known as the stomach flu or winter vomiting bug. It is the most common cause of viral gastroenteritis worldwide, responsible for millions of cases of food poisoning annually. The virus belongs to the family Caliciviridae and was first identified in 1972 following an outbreak in Norwalk, Ohio. Norovirus infections are characterized by sudden onset of nausea, vomiting, diarrhea, and stomach cramps. The virus is extremely resilient, surviving on surfaces for days and requiring only a tiny amount to cause infection. It spreads rapidly in closed environments like cruise ships, nursing homes, schools, and hospitals. Unlike bacterial food poisoning, norovirus cannot be treated with antibiotics and typically resolves on its own within 24-72 hours. Prevention relies heavily on proper hand hygiene, surface disinfection, and food safety practices. The virus has multiple strains and constantly mutates, making it difficult for the human immune system to develop long-lasting protection.',
                'etymology': 'Named after Norwalk, Ohio, where the first outbreak was identified in 1972. The suffix "-virus" comes from Latin virus meaning "poison" or "slimy liquid."',
                'memory_tip': 'Remember "Norwalk virus" - the original name from the city where it was first discovered. Think "Nor-walk" because you might not want to walk much when you have this stomach bug.',
                'example_sentence': 'The cruise ship was quarantined after a _____ outbreak affected over 200 passengers with severe gastrointestinal symptoms.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'north': {
                'pronunciation': '/nɔrθ/',
                'definition': 'North refers to the cardinal direction that is opposite to south and is typically oriented toward the top of maps. In geography and navigation, north is defined as the direction toward the Earth\'s North Pole, which is located at the northern end of the planet\'s rotational axis. The concept of north has been fundamental to human navigation for millennia, with various cultures developing methods to determine this direction using celestial bodies, particularly the North Star (Polaris) in the Northern Hemisphere. Magnetic north, indicated by compass needles, differs slightly from true north due to the Earth\'s magnetic field variations. The word is also used metaphorically to represent upward direction, progress, or positive movement, as in "heading north" to mean improving or increasing. In cultural contexts, "the North" often refers to regions in the northern part of a country or continent, such as Northern England, the American North during the Civil War, or the Arctic regions. The direction north has symbolic associations with coldness, winter, darkness (in the Northern Hemisphere), and in some traditions, wisdom or spiritual enlightenment.',
                'etymology': 'From Old English norþ, from Proto-Germanic *nurþraz, related to Dutch noord and German nord. The root may be related to "nether" meaning "below" or "under."',
                'memory_tip': 'Think of the North Star - the bright star that has guided travelers north for centuries. "North" sounds like "worth" - worth knowing for navigation.',
                'example_sentence': 'The explorer used his compass to determine which direction was _____ before setting up camp.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'northern': {
                'pronunciation': '/ˈnɔrðərn/',
                'definition': 'Northern is an adjective describing something situated in, directed toward, or characteristic of the north or the northern part of a region, country, or hemisphere. When applied to geography, it designates areas located in the upper portions of maps or closer to the North Pole. The term carries various cultural, climatic, and biological associations depending on context. In climatology, northern regions typically experience cooler temperatures, distinct seasonal patterns, and in extreme cases, polar conditions with extended periods of darkness or daylight. Northern ecosystems often feature coniferous forests, tundra, and specialized wildlife adapted to colder climates. Culturally, "Northern" can refer to distinct regional identities, dialects, cuisines, and traditions that have developed in response to geographic and climatic conditions. In historical contexts, particularly in American history, "Northern" refers to the states that opposed slavery and formed the Union during the Civil War. The term is also used in politics, economics, and social sciences to describe characteristics, policies, or phenomena associated with northern regions, such as Northern European social democracy or Northern industrial economies.',
                'etymology': 'From Old English norþerne, combining norþ (north) with the suffix -erne indicating direction or origin, similar to "southern," "eastern," and "western."',
                'memory_tip': 'Add "-ern" to north to make it an adjective. Think of "Northern Lights" - the beautiful aurora visible in northern regions.',
                'example_sentence': 'The _____ territories of Canada experience extreme cold temperatures during the winter months.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nose': {
                'pronunciation': '/noʊz/',
                'definition': 'The nose is a prominent facial organ that serves as the primary entrance to the respiratory system and houses the sense of smell. Anatomically, it consists of external and internal structures, including the nasal bones, cartilage, nostrils (nares), nasal cavity, and olfactory epithelium. The nose performs several vital functions: it filters, warms, and humidifies incoming air; it contains specialized cells that detect odors and transmit information to the brain for smell recognition; and it plays a role in speech resonance and voice quality. The external nose shape varies significantly among individuals and populations, influenced by genetic, environmental, and evolutionary factors. Beyond its biological functions, the nose holds cultural significance in many societies, appearing in idioms ("nose for business," "right under your nose"), literature, and art. In medicine, the nose is subject to various conditions including allergies, infections, structural abnormalities, and injuries. The phrase "nose" is also used metaphorically to describe the front or projecting part of objects, such as the nose of an airplane or ship.',
                'etymology': 'From Old English nosu, from Proto-Germanic *nusō, related to Dutch neus and German Nase. Connected to Latin nasus and Sanskrit nasa.',
                'memory_tip': 'Think of how your nose "knows" smells - both words start with "no" and relate to sensing and awareness.',
                'example_sentence': 'The bloodhound used its powerful _____ to track the scent through the dense forest.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nosh': {
                'pronunciation': '/nɑʃ/',
                'definition': 'Nosh is a Yiddish-derived word that means to eat snacks or light food between meals, or to nibble continuously throughout the day rather than eating formal meals. As a verb, it describes the act of casual, informal eating, often of small portions or appetizers. As a noun, it refers to the snack food itself or a light meal. The word carries connotations of leisurely, social eating and is often associated with Jewish-American culture and delicatessen traditions. In modern usage, noshing implies a relaxed, social atmosphere where people graze on various small foods, such as at parties, gatherings, or while socializing. The term has expanded beyond its cultural origins and is now commonly used in American English to describe any casual snacking behavior. Noshing often involves foods that can be eaten by hand, such as nuts, crackers, chips, small sandwiches, or appetizers. The concept emphasizes the social and pleasurable aspects of eating rather than eating for purely nutritional purposes.',
                'etymology': 'From Yiddish nashn, meaning "to eat sweets" or "to snack," which comes from Middle High German naschen meaning "to nibble" or "to eat secretly."',
                'memory_tip': 'Think "nibble nosh" - both start with "n" and relate to small, casual eating. The "sh" sound mimics the munching sound of snacking.',
                'example_sentence': 'At the party, guests were invited to _____ on a variety of appetizers and finger foods throughout the evening.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nostalgia': {
                'pronunciation': '/nɑˈstældʒə/',
                'definition': 'Nostalgia is a complex emotional state characterized by a wistful or sentimental longing for a period in the past, typically for a time or place associated with happy personal memories or perceived as better than the present. Originally coined as a medical term to describe severe homesickness, nostalgia is now understood as a normal psychological phenomenon that serves important emotional and social functions. It often involves idealized memories that may not accurately reflect past reality, as people tend to remember positive aspects while forgetting negative ones. Nostalgia can be triggered by sensory experiences like music, smells, or visual cues, and it serves to enhance mood, increase self-esteem, foster social connections, and provide meaning and continuity in life. The emotion is universal across cultures, though the specific triggers and objects of nostalgic feelings vary widely. In consumer culture, nostalgia is frequently exploited in marketing through "retro" products, remakes, and appeals to "the good old days." Psychologically, nostalgia helps people cope with stress, loneliness, and uncertainty by connecting them to positive memories and reinforcing their sense of identity and belonging.',
                'etymology': 'Coined in 1688 by Swiss physician Johannes Hofer from Greek nostos (homecoming) + algos (pain, grief), literally meaning "the pain of homecoming" or homesickness.',
                'memory_tip': 'Break it down: "nost-" sounds like "lost" and "-algia" means pain (like neuralgia). So nostalgia is the pleasant pain of things lost to time.',
                'example_sentence': 'Looking through old photo albums filled her with _____ for her childhood summers at her grandmother\'s house.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nostradame': {
                'pronunciation': '/ˌnoʊstrəˈdɑm/',
                'definition': 'Nostradame is likely a variant spelling or alternate form of Nostradamus, referring to Michel de Nostredame (1503-1566), the famous French physician, astrologer, and reputed prophet. He is best known for his book "Les Prophéties," a collection of 942 poetic quatrains that many believe contain predictions about future events. Born in southeastern France, he initially worked as a physician treating plague victims before turning to astrology and divination. His prophecies, written in a mixture of French, Latin, Greek, and Occitan, are intentionally cryptic and ambiguous, allowing for multiple interpretations. Throughout history, people have claimed that Nostradamus predicted major events such as the Great Fire of London, the French Revolution, the rise of Napoleon and Hitler, and various natural disasters. However, scholars and skeptics argue that these connections are often made retroactively and that the vague language of his quatrains can be interpreted to fit almost any significant event. Regardless of their prophetic accuracy, Nostradamus\'s writings have had a lasting cultural impact and continue to fascinate people interested in prophecy and the supernatural.',
                'etymology': 'Variant of Nostradamus, from the Latinized form of Michel de Nostredame\'s surname. "Nostredame" means "Our Lady" in Old French, referring to the Virgin Mary.',
                'memory_tip': 'Think of "Notre Dame" (Our Lady) - Nostradame/Nostradamus comes from a similar French origin meaning "Our Lady."',
                'example_sentence': 'The documentary explored various interpretations of _____ prophecies and their alleged connections to historical events.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nostradamus': {
                'pronunciation': '/ˌnoʊstrəˈdɑməs/',
                'definition': 'Nostradamus is the Latinized name of Michel de Nostredame (1503-1566), a French physician, astrologer, and renowned prophet whose cryptic predictions have fascinated and puzzled people for centuries. Born during the Renaissance in Saint-Rémy-de-Provence, he initially pursued medicine, becoming a respected physician who treated plague victims with innovative methods. However, he gained lasting fame for his prophetic writings, particularly "Les Prophéties" (The Prophecies), published in 1555. This work contains 942 poetic quatrains written in a deliberately obscure style, mixing French with Latin, Greek, and Occitan words. His predictions allegedly foretold major historical events including the Great Fire of London (1666), the French Revolution, the rise and fall of Napoleon, World War II, and the September 11 attacks. The ambiguous nature of his writings allows for multiple interpretations, leading to ongoing debates about their accuracy. Skeptics argue that the prophecies are too vague to constitute genuine predictions and that supposed connections to historical events are often made retroactively. Despite scholarly criticism, Nostradamus remains a popular figure in popular culture, with his name synonymous with prophecy and future prediction.',
                'etymology': 'Latinized form of Michel de Nostredame, from Old French "nostre dame" meaning "our lady," referring to the Virgin Mary.',
                'memory_tip': 'Think "nos-tra-DAM-us" - "nos" (us) + "tra" (see) + "dam" (stop/block) + "us" - he tried to help us see what would block or challenge us in the future.',
                'example_sentence': 'Many people still study the cryptic quatrains of _____ hoping to decode predictions about future world events.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nostrilsthe': {
                'pronunciation': 'Not applicable - combined word error',
                'definition': 'This appears to be a combined word error resulting from PDF parsing issues. It likely represents "nostrils" combined with "the" or another word fragment.',
                'etymology': 'Combined word error - not a legitimate word.',
                'memory_tip': 'This is an error from PDF processing - "nostrils" and another word were incorrectly joined together.',
                'example_sentence': 'Not applicable - this is an error in data processing.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'notable': {
                'pronunciation': '/ˈnoʊtəbəl/',
                'definition': 'Notable is an adjective meaning worthy of attention, remarkable, or significant due to distinctive qualities or achievements that set someone or something apart from the ordinary. When describing people, notable individuals are those who have achieved recognition, distinction, or fame in their fields, whether in arts, sciences, politics, business, or other areas of human endeavor. For events, discoveries, or phenomena, notable refers to those that have particular importance, influence, or memorable characteristics that make them stand out in history or current affairs. The word implies a level of prominence that merits recognition, discussion, or remembrance. As a noun, "notables" refers to prominent or distinguished people within a community or society. Notable achievements often contribute to progress, culture, or understanding in significant ways. The term suggests that something or someone has qualities that deserve to be "noted" or recorded for their importance, influence, or exceptional nature. In academic and professional contexts, notable work represents contributions that advance knowledge, technique, or understanding beyond routine accomplishments.',
                'etymology': 'From Latin notabilis, from notare meaning "to mark" or "to note," which comes from nota meaning "mark" or "sign."',
                'memory_tip': 'Think "note-able" - something so important that it\'s able to be noted or worth writing down and remembering.',
                'example_sentence': 'The scientist\'s _____ discovery about gene therapy earned her recognition from the international medical community.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'notebook': {
                'pronunciation': '/ˈnoʊtˌbʊk/',
                'definition': 'A notebook is a portable book or collection of blank or lined pages bound together for the purpose of writing notes, recording information, making lists, sketching, or keeping records. Traditionally made of paper with various binding methods such as spiral coils, stitching, or perfect binding, notebooks serve as essential tools for students, professionals, writers, artists, and anyone who needs to capture thoughts or information on paper. They come in various sizes from pocket-sized memo pads to large format journals, with different page styles including lined, blank, grid, or dot patterns to suit different uses. The term has evolved with technology to also refer to laptop computers, specifically "notebook computers," which are portable personal computers designed for mobile use. In the digital age, electronic notebooks and note-taking applications have emerged as alternatives to traditional paper notebooks, offering features like searchability, cloud synchronization, and multimedia integration. Whether physical or digital, notebooks remain fundamental tools for learning, creativity, organization, and communication, serving as external memory aids that help people process, organize, and retain information.',
                'etymology': 'Compound word from "note" (from Latin nota meaning "mark") and "book" (from Old English bōc), literally meaning "a book for notes."',
                'memory_tip': 'Simple compound: "note" + "book" = a book where you write notes. Easy to remember because it describes exactly what it is.',
                'example_sentence': 'She carried her _____ everywhere, jotting down ideas for her novel whenever inspiration struck.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'notes': {
                'pronunciation': '/noʊts/',
                'definition': 'Notes are brief written records, observations, or reminders that capture important information, ideas, or instructions for future reference. They serve as external memory aids that help people remember, organize, and process information from various sources such as lectures, meetings, books, research, or personal thoughts. Notes can take many forms, from quick jottings and bullet points to detailed outlines and comprehensive summaries, depending on their purpose and the note-taker\'s preferences. In academic contexts, effective note-taking is a crucial skill that enhances learning, comprehension, and retention of material. Professional notes might include meeting minutes, project updates, or strategic planning documents. Personal notes can range from shopping lists and reminders to journal entries and creative ideas. The word also refers to musical notes, which are symbols representing sounds in musical notation, and to short written communications or messages. In finance, notes can refer to promissory notes or other debt instruments. Digital note-taking has become increasingly popular, with applications offering features like search functionality, multimedia integration, and cloud synchronization across devices.',
                'etymology': 'From Latin nota meaning "mark," "sign," or "character," originally referring to shorthand characters used by Roman scribes.',
                'memory_tip': 'Think of musical notes on a staff - both written notes and musical notes are symbols that help us remember and record information.',
                'example_sentence': 'The student\'s detailed _____ from the lecture helped her prepare effectively for the upcoming exam.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'notification': {
                'pronunciation': '/ˌnoʊtəfəˈkeɪʃən/',
                'definition': 'A notification is a formal or informal message that informs someone about an event, change, requirement, or piece of information that requires their attention or awareness. In traditional contexts, notifications include official documents, announcements, warnings, or alerts delivered through various channels such as mail, telephone, or in-person communication. The purpose is to ensure that relevant parties are made aware of important information in a timely manner. In the digital age, notifications have become ubiquitous features of electronic devices and software applications, appearing as pop-ups, badges, sounds, or vibrations that alert users to new messages, updates, reminders, or system events. These digital notifications can range from social media updates and email alerts to system warnings and calendar reminders. While notifications serve important functions in keeping people informed and connected, they can also contribute to information overload and distraction. Modern devices often include notification management settings that allow users to customize, prioritize, or silence various types of alerts to balance staying informed with maintaining focus and productivity.',
                'etymology': 'From Latin notificare, meaning "to make known," composed of notus (known) + facere (to make), through Old French notification.',
                'memory_tip': 'Break it down: "noti-fi-cation" - "notify" (to inform) + "-cation" (action) = the action of informing someone.',
                'example_sentence': 'She received a _____ on her phone reminding her about the important meeting scheduled for that afternoon.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'notoriety': {
                'pronunciation': '/ˌnoʊtəˈraɪəti/',
                'definition': 'Notoriety refers to the state of being famous or well-known for something negative, scandalous, or morally questionable. Unlike positive fame or celebrity, notoriety carries distinctly negative connotations and is associated with infamy, disrepute, or public disapproval. A person, event, or thing gains notoriety when it becomes widely known due to controversial, criminal, unethical, or socially unacceptable behavior or characteristics. Historical figures who have achieved notoriety include criminals, corrupt politicians, and individuals involved in major scandals. The concept implies that while the subject has achieved widespread recognition, this recognition comes at the cost of reputation and social standing. Notoriety can be temporary, arising from a specific incident, or it can be long-lasting, defining how someone or something is remembered by history. The media often plays a significant role in creating notoriety by extensively covering controversial subjects. While some individuals may actively seek notoriety as a form of attention, most people who achieve it do so inadvertently as a consequence of their actions or associations.',
                'etymology': 'From Medieval Latin notorius meaning "well-known," from Latin notus meaning "known," with the suffix -ity indicating a state or condition.',
                'memory_tip': 'Think "notorious" + "-ity" = the state of being notorious (badly famous). Remember it\'s negative fame - "noted for the wrong reasons."',
                'example_sentence': 'The politician\'s involvement in the corruption scandal brought him unwanted _____ that ended his career.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'notturno': {
                'pronunciation': '/noʊˈtʊrnoʊ/',
                'definition': 'Notturno is an Italian musical term meaning "nocturne" or "night piece," referring to a musical composition that evokes the atmosphere, mood, or imagery of nighttime. In classical music, a notturno is typically a lyrical, dreamy piece characterized by flowing melodies, gentle rhythms, and often melancholic or romantic expressions that capture the serene, mysterious, or contemplative qualities associated with night. The form became particularly popular during the Romantic era, with composers like John Field and Frédéric Chopin creating numerous examples that emphasized expressive melody over technical virtuosity. These pieces often feature singing melodic lines accompanied by simple, repetitive harmonies that create a sense of peaceful introspection. The notturno can be written for various instruments, though piano nocturnes are most common, but examples exist for orchestra, chamber ensembles, and solo instruments. The Italian term reflects the international nature of classical music terminology, where Italian words became standard across different musical cultures. Beyond classical music, the concept has influenced other genres, with jazz and popular music adopting similar nocturnal themes and atmospheric qualities.',
                'etymology': 'Italian word meaning "nocturnal" or "of the night," from Latin nocturnus, related to nox (night).',
                'memory_tip': 'Think "nocturnal" with Italian flair - "notturno" is the Italian way of saying a nighttime musical piece.',
                'example_sentence': 'The pianist\'s performance of Chopin\'s _____ filled the concert hall with the peaceful, dreamy atmosphere of a moonlit evening.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'noumenon': {
                'pronunciation': '/ˈnumənɑn/',
                'definition': 'Noumenon is a philosophical term introduced by Immanuel Kant to describe the "thing-in-itself," or reality as it exists independently of human perception and understanding. In Kant\'s critical philosophy, the noumenon represents the unknowable aspect of objects that exists beyond the realm of sensory experience and conceptual knowledge. According to Kant, humans can only access phenomena (things as they appear to us through our senses and cognitive structures), but never the noumenon (things as they truly are in themselves). This distinction forms a central part of Kant\'s epistemology and his solution to philosophical problems about the relationship between appearance and reality. The noumenal realm is populated by things that may exist but cannot be directly experienced or fully comprehended by human consciousness, which is limited by the forms of space and time and the categories of understanding. While we can think about noumena, we cannot have knowledge of them in the strict sense. This concept has been influential in subsequent philosophy, theology, and metaphysics, though it has also been subject to extensive criticism and reinterpretation by later philosophers who questioned the coherence or necessity of the noumenal/phenomenal distinction.',
                'etymology': 'From Greek noumenon, meaning "that which is thought," from Greek nous (mind) + the passive participle ending -menon.',
                'memory_tip': 'Think "NEW-men-on" - it\'s the new dimension of reality that\'s on (exists) but can\'t be directly known by the human mind.',
                'example_sentence': 'According to Kant\'s philosophy, we can never directly perceive the _____ but only experience phenomena filtered through our cognitive structures.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'noun': {
                'pronunciation': '/naʊn/',
                'definition': 'A noun is a fundamental part of speech in grammar that serves to name and identify people, places, things, ideas, concepts, qualities, or actions. Nouns function as the subjects and objects of sentences, providing the essential building blocks around which other grammatical elements are organized. They can be classified in several ways: common nouns refer to general categories (dog, city, love), while proper nouns name specific entities (Rover, Paris, Christianity); concrete nouns denote physical objects that can be perceived through the senses (table, apple, music), while abstract nouns represent concepts, emotions, or qualities that cannot be physically touched (freedom, happiness, justice); count nouns can be enumerated (books, cars), while mass nouns represent substances or concepts that cannot be easily counted (water, sand, information). Nouns also vary in number (singular/plural) and in many languages, including English, can show possession through possessive forms. In sentence structure, nouns can serve as subjects performing actions, direct objects receiving actions, indirect objects, or objects of prepositions. Understanding nouns is essential for mastering grammar, vocabulary development, and effective communication.',
                'etymology': 'From Old French non, from Latin nomen meaning "name," from the same root as "nomenclature" and "nominal."',
                'memory_tip': 'Remember "noun = name" - both start with "n" and nouns are words that name people, places, things, or ideas.',
                'example_sentence': 'In the sentence "The dog chased the ball," both "dog" and "ball" are examples of a _____.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nouns': {
                'pronunciation': '/naʊnz/',
                'definition': 'Nouns is the plural form of noun, referring to multiple words that function as names for people, places, things, ideas, or concepts in language. As a category, nouns represent one of the primary parts of speech in virtually all languages, serving as the foundation for communication by providing labels for everything we wish to discuss or describe. The study of nouns encompasses their various types, functions, and grammatical behaviors within sentences. Different languages handle nouns differently - some have complex case systems that change noun endings based on their grammatical role, while others like English rely more heavily on word order. Nouns can be modified by adjectives, determined by articles, and connected by conjunctions to create complex noun phrases. In language learning and grammar instruction, understanding how nouns work is fundamental because they anchor meaning in sentences and provide reference points for other grammatical elements. The collection of nouns in a language represents its vocabulary\'s naming capacity, reflecting the culture, environment, and concepts important to its speakers. Mastery of nouns and their proper usage is essential for effective communication, reading comprehension, and writing skills.',
                'etymology': 'Plural form of noun, from Old French non, from Latin nomen meaning "name."',
                'memory_tip': 'Simply "noun" + "s" = multiple naming words. Think of collecting names for everything around you.',
                'example_sentence': 'Students learning English grammar must understand how _____ function as subjects and objects in sentences.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nourish': {
                'pronunciation': '/ˈnʌrɪʃ/',
                'definition': 'Nourish means to provide with the substances necessary for growth, health, and good condition, particularly through food and nutrition, but extending metaphorically to emotional, intellectual, and spiritual sustenance. In its primary biological sense, nourishing involves supplying the essential nutrients, vitamins, minerals, and calories that organisms need to maintain life processes, support growth and development, repair tissues, and maintain optimal health. Good nutrition nourishes the body by providing balanced macronutrients (proteins, carbohydrates, fats) and micronutrients (vitamins, minerals) in appropriate quantities. Beyond physical nourishment, the term applies to fostering and supporting development in broader contexts: parents nourish their children\'s emotional growth through love and attention; teachers nourish students\' intellectual development through quality education; communities nourish cultural traditions through practice and transmission; individuals nourish their creativity through exposure to art and new experiences. The concept implies ongoing care, attention, and provision of what is needed for healthy development and flourishing, whether applied to plants, animals, people, relationships, ideas, or institutions.',
                'etymology': 'From Old French norir, from Latin nutrire meaning "to feed, nurse, foster, support," related to "nutrition" and "nutrient."',
                'memory_tip': 'Think "nourish = nour-ish" where "nour" sounds like "nurture" - both mean to feed and care for something to help it grow.',
                'example_sentence': 'The rich soil and careful attention helped to _____ the young plants throughout their first growing season.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nouveau': {
                'pronunciation': '/nuˈvoʊ/',
                'definition': 'Nouveau is a French adjective meaning "new" or "newly arrived," commonly used in English in various compound terms and phrases to denote something recently created, recently acquired, or representing a new style or approach. The word often carries connotations of innovation, freshness, or departure from traditional forms, though it can sometimes imply superficiality or lack of authenticity when applied to social status. One of the most common uses is "nouveau riche," referring to people who have recently acquired wealth but may lack the social refinement traditionally associated with established wealthy families. In art and design, "Art Nouveau" describes the decorative art movement of the late 19th and early 20th centuries characterized by intricate patterns inspired by natural forms. "Beaujolais Nouveau" refers to young wine released shortly after harvest. In cuisine, "nouvelle cuisine" describes a style of cooking that emphasizes fresh ingredients, lighter preparations, and artistic presentation. The word adds a French sophistication to English usage while highlighting the concept of newness, whether in terms of time, style, status, or approach.',
                'etymology': 'French word meaning "new," from Latin novus meaning "new, fresh, young," related to English "novel" and "innovation."',
                'memory_tip': 'Think "new-vo" - sounds like "new" with a French accent. Often seen in "nouveau riche" (newly rich).',
                'example_sentence': 'The _____ riche family struggled to gain acceptance in the established social circles despite their newfound wealth.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nova': {
                'pronunciation': '/ˈnoʊvə/',
                'definition': 'Nova is an astronomical term describing a stellar explosion that causes a dramatic and temporary increase in a star\'s brightness, making it appear as a "new star" in the sky. This phenomenon occurs in binary star systems where a white dwarf star accumulates material from a companion star until conditions trigger a thermonuclear explosion on the white dwarf\'s surface. Unlike supernovae, which destroy the star entirely, a nova explosion allows the white dwarf to survive and potentially repeat the process. The brightness increase can be enormous, sometimes making the star tens of thousands of times brighter than normal, visible to the naked eye even during daylight in some cases. After reaching peak brightness, a nova gradually fades over weeks, months, or years as the explosion\'s effects diminish. Historically, astronomers named these events "novae" (plural of nova) because they appeared to be new stars suddenly appearing in the sky, though they are actually existing stars undergoing explosive episodes. The term has been adopted metaphorically to describe anything that suddenly appears or becomes prominent, and it\'s also used as a proper name for cars, television shows, and other products suggesting innovation or brilliance.',
                'etymology': 'From Latin nova (stella) meaning "new (star)," from Latin novus meaning "new."',
                'memory_tip': 'Think "new star" - nova comes from Latin "new" because these stellar explosions make stars appear suddenly bright like new stars.',
                'example_sentence': 'Astronomers observed the _____ reaching peak brightness before gradually fading over several months.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'novanglian': {
                'pronunciation': '/noʊˈvæŋgliən/',
                'definition': 'Novanglian is a term referring to something or someone from or relating to New England, the northeastern region of the United States comprising six states: Maine, New Hampshire, Vermont, Massachusetts, Rhode Island, and Connecticut. The word serves as an adjective describing the distinctive cultural, linguistic, historical, or geographical characteristics associated with this region. New England, known for its rich colonial history, distinctive architecture, autumn foliage, maritime traditions, and educational institutions like Harvard and Yale, has developed unique cultural identity over centuries. Novanglian characteristics might include particular dialects or accents, culinary traditions like clam chowder and maple syrup, architectural styles such as colonial and Victorian homes, and cultural values often associated with Puritan heritage including education, self-reliance, and civic responsibility. The region\'s economy historically based on fishing, shipping, manufacturing, and later technology and education, has created distinctive economic and social patterns. Novanglian literature, from authors like Nathaniel Hawthorne, Emily Dickinson, and Robert Frost, reflects the region\'s landscape, history, and cultural sensibilities.',
                'etymology': 'From Latin "Novanglia" meaning "New England," combining "nov-" (new) + "Anglia" (England).',
                'memory_tip': 'Break it down: "Nov-anglian" = "New-English" = relating to New England, the region settled by English colonists.',
                'example_sentence': 'The author\'s _____ heritage was evident in her stories about small coastal towns and harsh winters.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'novelist': {
                'pronunciation': '/ˈnɑvəlɪst/',
                'definition': 'A novelist is a writer who specializes in creating novels, which are extended fictional narratives typically featuring complex characters, intricate plots, and detailed settings that explore themes of human experience, society, relationships, and the human condition. Novelists combine artistic creativity with technical writing skills to craft lengthy prose works that entertain, inform, challenge, or inspire readers through storytelling. The craft requires mastery of various literary elements including character development, plot structure, dialogue, setting, point of view, theme, and narrative voice. Successful novelists must sustain reader interest across hundreds of pages while maintaining consistency in style, character, and story logic. Many novelists specialize in particular genres such as literary fiction, mystery, romance, science fiction, fantasy, historical fiction, or contemporary fiction, though some write across multiple genres. The profession can range from full-time career authors who make their living through writing and publishing to part-time writers who combine novel writing with other occupations. Famous novelists throughout history have shaped literature, culture, and social consciousness through their works, with many novels becoming classics that continue to influence readers and writers across generations.',
                'etymology': 'From "novel" (from Italian novella meaning "new story") + "-ist" (suffix meaning "one who practices or specializes in").',
                'memory_tip': 'Think "novel" + "-ist" = a person who writes novels, just like "piano" + "-ist" = pianist.',
                'example_sentence': 'The celebrated _____ spent five years researching historical details for her latest work set during the Civil War.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'novemdecillion': {
                'pronunciation': '/noʊˌvɛmdɪˈsɪljən/',
                'definition': 'Novemdecillion is an extremely large number in the American numbering system, equal to 10 raised to the 60th power, or 1 followed by 60 zeros. In the short scale system used in the United States and other English-speaking countries, this represents one thousand vigintillion or one million octodecillion. To put this astronomical number in perspective, it is far larger than the estimated number of atoms in the observable universe, which is approximately 10^80. The word follows the standard pattern for naming large numbers, where Latin prefixes indicate the power of 1000 being multiplied. Numbers of this magnitude exist primarily in theoretical mathematics, cosmology, and physics, rather than in practical everyday applications. They might appear in calculations involving quantum mechanics, statistical mechanics, or theoretical scenarios involving vast quantities of particles or possibilities. The concept of novemdecillion illustrates the infinite nature of mathematics and the human ability to conceive and name quantities far beyond physical reality. While such numbers have little practical application in daily life, they are essential for advanced mathematical and scientific calculations that push the boundaries of human understanding.',
                'etymology': 'From Latin "novem" (nine) + "decem" (ten) + "-illion," indicating 19 groups of three zeros after the first thousand in the short scale system.',
                'memory_tip': 'Break it down: "novem" (9) + "dec" (10) = 19, so it\'s the 19th "-illion" number (19 × 3 = 57 zeros after the first 3 = 60 total zeros).',
                'example_sentence': 'The theoretical physicist calculated that the probability of that specific quantum event was approximately one in a _____.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'novice': {
                'pronunciation': '/ˈnɑvɪs/',
                'definition': 'A novice is a beginner or someone new to a particular activity, skill, profession, or area of knowledge who is in the early stages of learning and development. The term implies inexperience and the need for instruction, guidance, and practice to develop competency. Novices typically rely heavily on rules, procedures, and external guidance because they lack the intuitive understanding and pattern recognition that comes with experience. In many fields, being a novice is a recognized stage of development with specific expectations, requirements, and learning objectives. The novice phase is characterized by careful attention to explicit rules and procedures, limited ability to adapt to unusual situations, and dependence on mentors or instructional materials. In religious contexts, a novice is someone who has begun training for membership in a religious order but has not yet taken final vows. The term can apply to any domain of human activity, from novice drivers learning traffic rules to novice chess players memorizing opening moves to novice cooks following recipes exactly. Everyone begins as a novice when approaching new challenges, and the novice stage is essential for building the foundation of knowledge and skills necessary for eventual expertise.',
                'etymology': 'From Old French novice, from Latin novicius meaning "newly imported, newly arrived," from novus meaning "new."',
                'memory_tip': 'Think "new-vice" - a novice is someone new to something, still developing their "vice" or skill in that area.',
                'example_sentence': 'As a _____ photographer, she carefully studied the camera manual before attempting to capture her first professional portraits.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'noxious': {
                'pronunciation': '/ˈnɑkʃəs/',
                'definition': 'Noxious describes something harmful, poisonous, or extremely unpleasant, particularly in terms of health, well-being, or environmental impact. The term most commonly applies to substances, fumes, or conditions that can cause physical harm, illness, or significant discomfort when encountered. Noxious gases, for example, can be toxic or irritating to breathe, while noxious chemicals can cause burns, poisoning, or other health problems. Beyond physical harm, noxious can describe anything that is morally corrupting, socially destructive, or intellectually harmful, such as noxious ideas that promote hatred or violence. The word implies an active quality of harm rather than mere unpleasantness - something noxious doesn\'t just smell bad or look unappealing, but actively threatens health or well-being. In environmental science, noxious weeds are invasive plants that damage ecosystems and agricultural lands. In legal contexts, noxious activities might be those that constitute public nuisances or violations of health and safety regulations. The term conveys a sense of serious concern and the need for avoidance, protection, or remediation when dealing with noxious substances or conditions.',
                'etymology': 'From Latin noxius meaning "harmful, injurious," from noxa meaning "damage, injury, harm," related to nocere meaning "to harm."',
                'memory_tip': 'Think "nox-ious" sounds like "knock-shus" - something that will "knock you out" or harm you with its toxic effects.',
                'example_sentence': 'Workers in the factory were required to wear protective masks to avoid inhaling the _____ fumes from the chemical processing.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nozzles': {
                'pronunciation': '/ˈnɑzəlz/',
                'definition': 'Nozzles are mechanical devices designed to control the direction, pressure, and flow characteristics of a fluid (liquid or gas) as it exits a container, pipe, or system. They are essential components in countless applications ranging from garden hoses and fire hydrants to rocket engines and fuel injectors. The basic principle of nozzle operation involves changing the cross-sectional area through which fluid flows, which according to fluid dynamics principles, affects pressure and velocity. Convergent nozzles accelerate subsonic flow by decreasing area, while divergent nozzles can decelerate flow or accelerate supersonic flow. Nozzles come in various designs optimized for specific purposes: spray nozzles create fine mists for painting or irrigation; jet nozzles produce focused streams for cleaning or propulsion; adjustable nozzles allow users to vary spray patterns; and specialized nozzles handle specific fluids or operating conditions. In engineering, nozzle design considers factors like flow rate, pressure drop, material compatibility, wear resistance, and desired spray characteristics. Quality nozzles are precisely manufactured to ensure consistent performance, proper flow patterns, and durability under operating conditions.',
                'etymology': 'Plural of nozzle, which comes from "nose" + diminutive suffix "-le," literally meaning "little nose," referring to a protruding spout.',
                'memory_tip': 'Think of a "nose" that squirts - nozzles are like little noses (spouts) that control how liquids come out.',
                'example_sentence': 'The irrigation system used multiple adjustable _____ to ensure even water distribution across the entire garden.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nuance': {
                'pronunciation': '/ˈnuɑns/',
                'definition': 'Nuance refers to subtle differences, variations, or distinctions in expression, meaning, response, or perception that require careful attention and sensitivity to detect and understand. It represents the fine gradations between obvious differences, the delicate shades of meaning that exist between clear-cut categories, and the sophisticated understanding that comes from recognizing complexity rather than seeing things in simple terms. In communication, nuance involves the subtle ways that tone, context, word choice, and timing can alter meaning beyond the literal content of words. In art, literature, and music, nuance encompasses the subtle techniques and expressions that create depth, emotion, and sophistication. Social and cultural nuance involves understanding the unspoken rules, implications, and sensitivities that govern human interactions within specific contexts. Political and ethical nuance requires recognizing that most issues exist on spectrums rather than as simple either/or choices. The appreciation of nuance is often considered a mark of intelligence, wisdom, and cultural sophistication, as it requires the ability to hold multiple perspectives simultaneously and to recognize that reality is typically more complex than it initially appears.',
                'etymology': 'From French nuance meaning "shade, slight difference," from nuer meaning "to shade," ultimately from Latin nubes meaning "cloud."',
                'memory_tip': 'Think "new-ance" - nuance is the "new" or subtle difference in stance that sophisticated understanding brings.',
                'example_sentence': 'The diplomat\'s speech was full of _____ that conveyed different messages to different audiences without explicitly stating controversial positions.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nubilous': {
                'pronunciation': '/ˈnubɪləs/',
                'definition': 'Nubilous is an adjective meaning cloudy, foggy, or obscured by clouds, typically used in poetic or literary contexts to describe atmospheric conditions or metaphorically to suggest vagueness, confusion, or lack of clarity. In its literal sense, nubilous describes weather or sky conditions characterized by the presence of clouds that may obscure visibility or create dim, overcast conditions. The word evokes imagery of mist-shrouded landscapes, fog-covered mountains, or overcast skies that create mysterious or melancholic atmospheres. Figuratively, nubilous can describe mental states, ideas, or situations that are unclear, confused, or difficult to understand, much like how clouds can obscure our view of the sky. In literature, authors might use "nubilous" to create atmospheric descriptions or to suggest psychological states of uncertainty or confusion. The term is relatively rare in contemporary usage, appearing more often in historical texts, poetry, or formal writing where a more elevated or archaic style is desired. It belongs to a family of weather-related words that have acquired metaphorical meanings related to clarity and understanding.',
                'etymology': 'From Latin nubilosus meaning "cloudy," from nubes meaning "cloud," related to "nebula" and "nebulous."',
                'memory_tip': 'Think "nubilous = nebulous" - both mean cloudy or unclear, both starting with "nu-" and relating to clouds.',
                'example_sentence': 'The mountain peak remained hidden in the _____ atmosphere, shrouded by thick clouds that refused to lift.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nubuck': {
                'pronunciation': '/ˈnubʌk/',
                'definition': 'Nubuck is a type of leather that has been processed to create a soft, velvety texture on the outer surface through buffing or sanding the top grain. This process, called napping, creates a slight nap or fuzzy texture that gives nubuck its distinctive feel and appearance. Unlike suede, which is made from the inner split of leather and has a more pronounced fuzzy texture, nubuck is made from the outer layer of the hide, making it more durable while maintaining a luxurious, soft feel. The leather starts as full-grain leather and is then carefully buffed to achieve the desired texture without compromising its strength. Nubuck is commonly used in high-quality footwear, furniture upholstery, handbags, and clothing because it combines durability with an attractive appearance and tactile appeal. However, nubuck requires special care as it can be more susceptible to staining and water damage than smooth leather surfaces. The material can be treated with protective sprays and requires specific cleaning methods to maintain its appearance. Nubuck leather is prized for its combination of luxury feel, durability, and distinctive appearance that develops character with age and wear.',
                'etymology': 'Possibly a combination of "nub" (referring to the napped surface texture) and "buck" (from buckskin leather), though the exact origin is uncertain.',
                'memory_tip': 'Think "nub-uck" - the "nub" refers to the nubby, textured surface created by buffing the leather.',
                'example_sentence': 'The hiking boots were made from high-quality _____ leather that provided both durability and comfort.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nuce': {
                'pronunciation': '/nus/',
                'definition': 'Nuce is a rare or archaic term that can refer to a nut or the kernel of a nut, though it is not commonly used in modern English. In some contexts, it may appear in botanical or historical texts when discussing nuts, seeds, or similar small, hard-shelled fruits or their contents. The word might also appear in specialized academic or scientific literature when discussing plant anatomy or in translations of older texts where more archaic terminology is preserved. Due to its rarity in contemporary usage, nuce is more likely to be encountered in specialized dictionaries, etymology studies, or historical documents rather than in everyday conversation or modern writing. The term represents one of many words that have fallen out of common usage as language evolves and more familiar terms like "nut," "kernel," or "seed" have become standard. In some cases, such rare words are maintained in specific technical vocabularies or appear in crossword puzzles and word games that challenge participants with unusual or archaic terms.',
                'etymology': 'From Latin nux, nucis meaning "nut," related to nucleus and other nut-related terms.',
                'memory_tip': 'Think of "nucleus" - both "nuce" and "nucleus" come from the Latin word for nut, referring to the hard center.',
                'example_sentence': 'The medieval botanical text described the _____ as the valuable inner part of the walnut.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nuciform': {
                'pronunciation': '/ˈnusɪˌfɔrm/',
                'definition': 'Nuciform is an adjective meaning "nut-shaped" or "having the form of a nut," used primarily in botanical, anatomical, and scientific contexts to describe objects, structures, or organisms that resemble nuts in their shape or form. The term is particularly useful in biological classification and description, where precise morphological terminology is essential for accurate identification and communication among scientists. In botany, nuciform might describe seeds, fruits, or other plant structures that have the characteristic hard, compact, rounded, or oval shape typical of nuts. In anatomy or medicine, the term could apply to organs, growths, or structures that exhibit similar morphological characteristics. The word represents the systematic approach to scientific nomenclature, where Latin and Greek roots are combined to create precise descriptive terms that can be understood across different languages and cultures. Such morphological terms are crucial in taxonomy, comparative anatomy, and descriptive sciences where accurate shape description is fundamental to classification and understanding. While not commonly used in everyday language, nuciform exemplifies the rich vocabulary available for precise scientific description.',
                'etymology': 'From Latin nucis (nut, genitive of nux) + -form (having the shape of), literally meaning "having the shape of a nut."',
                'memory_tip': 'Break it down: "nuci-" (nut) + "-form" (shaped) = nut-shaped. Like "uniform" but for nut shape.',
                'example_sentence': 'The botanist noted that the seed had a distinctly _____ appearance, closely resembling a small walnut.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nucleated': {
                'pronunciation': '/ˈnukliˌeɪtɪd/',
                'definition': 'Nucleated is an adjective describing cells, structures, or processes that possess or are characterized by the presence of a nucleus. In biology, nucleated cells (eukaryotic cells) are distinguished from non-nucleated cells (prokaryotic cells) by having their genetic material enclosed within a membrane-bound nucleus, which is one of the fundamental distinctions in cellular organization. All complex multicellular organisms, including plants, animals, and fungi, are composed of nucleated cells, while bacteria and archaea are non-nucleated. The term can also refer to the process of nucleation in physics and chemistry, where nucleated describes the formation of crystal or phase structures around central nuclei or seed points. In crystallography, nucleated growth occurs when crystals form around specific nucleation sites. In meteorology, nucleated particles serve as condensation centers for cloud formation. In materials science, nucleated plastics contain added agents that promote uniform crystal formation. The concept of nucleation is fundamental to understanding many physical and biological processes, from cell division and reproduction to crystal formation and phase transitions in materials.',
                'etymology': 'From Latin nucleus (kernel, core) + -ated (having, characterized by), meaning "having a nucleus."',
                'memory_tip': 'Think "nucleus-ated" - having a nucleus, like how "decorated" means having decorations.',
                'example_sentence': 'Under the microscope, the biologist could clearly distinguish between the _____ plant cells and the bacterial cells without nuclei.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nudged': {
                'pronunciation': '/nʌdʒd/',
                'definition': 'Nudged is the past tense of the verb "nudge," meaning to push or poke gently, typically with the elbow, to get someone\'s attention or encourage them to take action. The action implies a gentle, subtle form of physical contact intended to communicate something without words or to prompt a response without being forceful or demanding. Nudging can serve various purposes: getting someone\'s attention discreetly, encouraging someone to notice something, suggesting they should move or act, or expressing solidarity or complicity in a shared understanding. Beyond the literal physical meaning, "nudged" is frequently used metaphorically to describe gentle encouragement, subtle influence, or gradual persuasion. In behavioral economics and psychology, "nudging" refers to techniques that influence people\'s behavior and decisions through gentle guidance rather than mandates or restrictions. For example, placing healthier food options at eye level nudges people toward better dietary choices. The concept of nudging recognizes that small, thoughtful changes in how choices are presented can significantly influence outcomes while preserving individual freedom of choice. The gentle nature of nudging makes it an effective tool for positive influence in various contexts.',
                'etymology': 'Past tense of "nudge," which may be related to Norwegian nugga meaning "to rub" or "to push," suggesting gentle physical contact.',
                'memory_tip': 'Think of gently pushing someone with your elbow to get their attention - that\'s a nudge. "Nudged" is just the past tense.',
                'example_sentence': 'She gently _____ her friend when the teacher asked a question, encouraging her to raise her hand.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nudibranch': {
                'pronunciation': '/ˈnudɪˌbræŋk/',
                'definition': 'Nudibranch is a group of soft-bodied, marine gastropod mollusks that are among the most visually spectacular creatures in the ocean, known for their extraordinary diversity of colors, shapes, and ornate appendages. These sea slugs belong to the order Nudibranchia and are characterized by their external gills (cerata) and lack of shells, which distinguishes them from other gastropods. The name literally means "naked gills," referring to their exposed respiratory structures that often create beautiful, branching patterns on their backs. Nudibranchs are found in oceans worldwide, from shallow tidal pools to deep ocean waters, with over 3,000 known species displaying an incredible array of forms and colors. Many species are highly specialized feeders, with some consuming sponges, hydroids, barnacles, or other specific prey, often incorporating toxins or stinging cells from their food for defense. Their striking appearances serve various functions including camouflage, warning coloration, and species recognition. Nudibranchs are popular subjects for underwater photographers and marine biologists due to their beauty and the diversity of ecological adaptations they represent. Their life cycles typically involve planktonic larval stages and complex reproductive behaviors.',
                'etymology': 'From Latin nudus (naked) + Greek branchia (gills), literally meaning "naked gills," referring to their external respiratory structures.',
                'memory_tip': 'Break it down: "nudi-" (naked) + "branch" (like tree branches) - they have naked gill branches on their backs.',
                'example_sentence': 'The scuba diver was thrilled to photograph a colorful _____ feeding on coral polyps during the night dive.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nugatory': {
                'pronunciation': '/ˈnugəˌtɔri/',
                'definition': 'Nugatory is an adjective meaning worthless, futile, or having no value or importance. It describes things that are ineffective, trivial, or so insignificant as to be essentially useless or meaningless. The term is often used in formal or legal contexts to characterize arguments, efforts, proposals, or actions that lack substance, merit, or practical effect. Something nugatory fails to achieve its intended purpose or has such minimal impact that it might as well not exist. In legal discourse, nugatory might describe contracts, clauses, or precedents that have no binding force or practical application. In academic or philosophical contexts, it can refer to arguments or theories that lack logical foundation or empirical support. The word carries a stronger connotation than simply "ineffective" – it suggests something that is fundamentally without worth or substance. Unlike terms that describe temporary failure or partial success, nugatory implies an inherent lack of value or purpose. The term is relatively formal and literary, appearing more often in scholarly writing, legal documents, or elevated discourse than in casual conversation, where simpler terms like "worthless" or "pointless" might be preferred.',
                'etymology': 'From Latin nugatorius meaning "trifling, worthless," from nugari meaning "to trifle," related to nugae meaning "trifles, nonsense."',
                'memory_tip': 'Think "nug-a-tory" sounds like "nugget-ory" - but instead of valuable nuggets, these are worthless nuggets of nothing.',
                'example_sentence': 'The committee dismissed the proposal as _____, arguing that it would accomplish nothing while wasting valuable resources.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nuggets': {
                'pronunciation': '/ˈnʌgɪts/',
                'definition': 'Nuggets are small, irregular lumps or chunks of valuable material, most commonly referring to gold nuggets - naturally occurring pieces of native gold found in placer deposits, rivers, or mines. These gold nuggets have been highly prized throughout history as symbols of wealth and fortune, often triggering gold rushes when discovered in significant quantities. Beyond precious metals, the term applies to any small, concentrated pieces of valuable or useful material. In the culinary world, chicken nuggets are small, bite-sized pieces of processed chicken that have become popular fast food items. The word has also taken on metaphorical meanings, referring to small pieces of valuable information, wisdom, or insight - "nuggets of wisdom" or "information nuggets" that are particularly useful or illuminating. In digital contexts, content nuggets refer to small, digestible pieces of information designed for easy consumption. The concept of nuggets implies both small size and concentrated value - something that may be little but packs significant worth or utility. The term suggests something precious found among less valuable material, whether literal gold in sediment or figurative wisdom in conversation.',
                'etymology': 'Diminutive form of "nug," possibly from "lump" or "chunk," first applied to small lumps of precious metals, especially gold.',
                'memory_tip': 'Think of gold nuggets - small but valuable chunks. Whether gold, chicken, or information, nuggets are small pieces of something good.',
                'example_sentence': 'The prospector was excited to find several small gold _____ while panning in the mountain stream.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nuisance': {
                'pronunciation': '/ˈnusəns/',
                'definition': 'A nuisance is something or someone that causes inconvenience, annoyance, or minor trouble, interfering with comfort, peace, or normal activities without necessarily causing serious harm. The term encompasses a wide range of bothersome situations, from noisy neighbors and persistent telemarketers to broken equipment and bureaucratic delays. Nuisances are typically characterized by their persistence, their ability to disrupt daily routines, and their tendency to require attention or action to resolve. In legal contexts, nuisance has specific meanings related to activities or conditions that interfere with the use and enjoyment of property or that affect public health, safety, or welfare. Public nuisances affect the community at large, while private nuisances specifically interfere with an individual\'s use of their property. Common examples include excessive noise, unpleasant odors, blocked access, or activities that disturb the peace. The concept recognizes that while some disruptions may not cause serious damage, they can significantly impact quality of life and warrant attention or resolution. Dealing with nuisances often requires patience, communication, and sometimes legal intervention to restore normal conditions.',
                'etymology': 'From Old French nusance meaning "harm," from Latin nocere meaning "to harm" + suffix -ance, originally meaning "harm" but evolved to mean "annoyance."',
                'memory_tip': 'Think "new-sance" - a new annoyance that keeps bothering you. The "nui" sounds like "annoying."',
                'example_sentence': 'The construction work next door had become a constant _____, disrupting sleep and making it difficult to concentrate.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nullius': {
                'pronunciation': '/ˈnʌliəs/',
                'definition': 'Nullius is a Latin word meaning "of no one" or "belonging to no one," most commonly encountered in the legal phrase "terra nullius," which refers to land that belongs to no one or is not under the sovereignty of any state. This concept has significant historical importance in international law, colonial expansion, and indigenous rights discussions. Terra nullius was used to justify European colonization of territories that were inhabited by indigenous peoples who did not have recognized European-style land ownership or governmental systems. The doctrine allowed colonizers to claim that lands were empty or unoccupied, even when they were inhabited, because the inhabitants did not have what Europeans considered legitimate sovereignty or property rights. This legal fiction has been widely criticized and largely abandoned in modern international law, as it ignored indigenous peoples\' existing relationships to their lands and their sophisticated governance systems. The concept of nullius also appears in other legal contexts related to ownerless property, abandoned goods, or unclaimed territories. Understanding this term is crucial for comprehending the legal foundations of colonialism and the ongoing struggles for indigenous rights and land acknowledgment.',
                'etymology': 'Latin genitive singular of nullus meaning "none, not any," used in legal phrases to indicate "of no one" or "belonging to no one."',
                'memory_tip': 'Think "null-ius" - "null" (nothing/no one) + Latin ending - meaning "belonging to no one."',
                'example_sentence': 'The court rejected the colonial-era claim that the land was terra _____, recognizing the indigenous people\'s prior occupation and rights.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nulliusnoun': {
                'pronunciation': 'Not applicable - combined word error',
                'definition': 'This appears to be a combined word error resulting from PDF parsing issues. It likely represents "nullius" combined with "noun" or another word fragment.',
                'etymology': 'Combined word error - not a legitimate word.',
                'memory_tip': 'This is an error from PDF processing - "nullius" and another word were incorrectly joined together.',
                'example_sentence': 'Not applicable - this is an error in data processing.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'number': {
                'pronunciation': '/ˈnʌmbər/',
                'definition': 'A number is a mathematical object used to count, measure, and label, representing quantity, position, or value in various numerical systems. Numbers form the foundation of mathematics, science, economics, and countless aspects of daily life, from telling time and measuring distances to calculating costs and analyzing data. The concept of number has evolved throughout human history, beginning with natural numbers (1, 2, 3...) used for counting, expanding to include zero, negative numbers, fractions, decimals, and complex numbers as mathematical understanding advanced. Numbers can be classified in various ways: natural numbers, whole numbers, integers, rational numbers, irrational numbers, real numbers, and complex numbers, each serving different mathematical purposes. Beyond pure mathematics, numbers serve as labels (phone numbers, identification numbers), codes (ZIP codes, ISBN numbers), and measurements (temperatures, speeds, weights). In grammar, number refers to the distinction between singular and plural forms of words. The human ability to understand and manipulate numbers is considered fundamental to cognitive development and is essential for functioning in modern society.',
                'etymology': 'From Old French nombre, from Latin numerus meaning "number, quantity," related to Greek nemein meaning "to distribute" or "to deal out."',
                'memory_tip': 'Think of "numerous" - both words come from the same root and relate to counting and quantity.',
                'example_sentence': 'The mathematician explained that every _____ greater than 2 that is prime must be odd.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'numerical': {
                'pronunciation': '/nəˈmɛrɪkəl/',
                'definition': 'Numerical is an adjective relating to, expressed by, or involving numbers and numerical calculation. It describes anything that deals with numbers as opposed to qualitative descriptions, emphasizing quantitative measurement, mathematical relationships, and precise numerical values. In mathematics and science, numerical methods involve using numbers and mathematical computation to solve problems, analyze data, or model phenomena. Numerical data consists of measurements that can be expressed as numbers, such as height, weight, temperature, or speed, as distinct from categorical data like colors or names. Numerical analysis is a branch of mathematics that develops algorithms for solving mathematical problems using numerical approximation. In computing, numerical processing involves mathematical operations on numerical data, while numerical codes use numbers to represent information. The term emphasizes precision, measurement, and mathematical rigor, distinguishing quantitative approaches from qualitative ones. Numerical literacy - the ability to understand and work with numbers - is considered essential for success in modern education and professional life, particularly in science, technology, engineering, mathematics, finance, and data analysis fields.',
                'etymology': 'From Latin numerus (number) + -ical (suffix meaning "relating to"), meaning "relating to numbers."',
                'memory_tip': 'Think "number-ical" - relating to numbers, just like "historical" relates to history.',
                'example_sentence': 'The researcher preferred _____ data over subjective opinions because numbers provided more reliable evidence.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'numerology': {
                'pronunciation': '/ˌnuməˈrɑlədʒi/',
                'definition': 'Numerology is a belief system and practice that attributes mystical, spiritual, or divinatory significance to numbers and their relationships to human life, personality, and events. Practitioners of numerology believe that numbers have inherent meanings and influences that can provide insight into a person\'s character, predict future events, or guide important life decisions. Common numerological practices include analyzing birth dates, names converted to numerical values, and significant life numbers to reveal supposed hidden meanings about personality traits, compatibility with others, favorable dates for important events, and life purposes or destinies. Different numerological systems exist, including Pythagorean numerology (based on the ancient Greek mathematician\'s teachings), Chaldean numerology (derived from ancient Babylonian practices), and Kabbalistic numerology (rooted in Jewish mystical traditions). While numerology lacks scientific evidence and is considered a pseudoscience by mainstream academia, it remains popular in various cultural contexts and is often used alongside astrology, tarot reading, and other divinatory practices. The appeal of numerology lies in its promise to provide meaning, guidance, and understanding through the universal language of numbers.',
                'etymology': 'From Latin numerus (number) + Greek logos (study), literally meaning "the study of numbers," though specifically referring to mystical number meanings.',
                'memory_tip': 'Think "numero-logy" - the study (-logy) of numbers (numero) and their supposed mystical meanings.',
                'example_sentence': 'She consulted a _____ expert who claimed that her birth date revealed important insights about her life path.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nunchaku': {
                'pronunciation': '/nʌnˈʧɑku/',
                'definition': 'Nunchaku, also known as nunchucks or nunchuks, is a traditional martial arts weapon consisting of two wooden, metal, or plastic sticks connected by a short chain or rope. Originally developed in Okinawa, Japan, the weapon is believed to have evolved from a farming tool used for threshing grain, though its exact origins are debated among historians. In martial arts, particularly in karate, kobudo (traditional weapons training), and various fighting systems, nunchaku are used for striking, blocking, and trapping techniques that require significant skill, coordination, and practice to master safely. The weapon\'s flexible connection allows for rapid, flowing movements and unpredictable attack patterns, but this same flexibility makes it challenging to control and potentially dangerous to inexperienced users. Nunchaku gained widespread recognition in popular culture through martial arts films, particularly those featuring Bruce Lee, leading to their adoption in various martial arts schools worldwide. However, their association with violence and their potential for causing injury has led to legal restrictions in many jurisdictions, where they are classified as prohibited weapons or require special permits for ownership and training.',
                'etymology': 'From Japanese ヌンチャク (nunchaku), possibly derived from the Okinawan word "nunchaku" referring to the original farming tool.',
                'memory_tip': 'Think of Bruce Lee spinning the "nun-chuck-u" - two sticks connected by a chain that martial artists chuck around.',
                'example_sentence': 'The martial arts student spent months learning basic _____ techniques before attempting advanced spinning movements.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nurture': {
                'pronunciation': '/ˈnɜrtʃər/',
                'definition': 'Nurture encompasses the care, attention, support, and environmental influences that promote growth, development, and well-being in living beings, particularly in the context of raising children, tending plants, or fostering relationships and ideas. As a verb, to nurture means to provide the conditions necessary for healthy development, including physical needs like food, shelter, and safety, as well as emotional needs like love, encouragement, and guidance. The concept extends beyond basic survival to include enriching experiences that help individuals reach their full potential. In child development, nurturing involves responsive caregiving, emotional attunement, and creating secure attachments that support psychological and social development. In the famous "nature versus nurture" debate, nurture represents environmental factors - parenting styles, education, social experiences, and cultural influences - that shape personality and behavior, as opposed to genetic inheritance. Nurturing can apply to creative projects, business ventures, relationships, skills, and talents, all requiring patience, dedication, and appropriate support. The quality of nurturing received, particularly in early life, is believed to have lasting impacts on mental health, resilience, and overall life outcomes.',
                'etymology': 'From Old French norreture meaning "food, nourishment," from Latin nutritus, past participle of nutrire meaning "to feed, nurse, tend."',
                'memory_tip': 'Think "nurse-ture" - like how a nurse tends to and cares for someone, nurture means to care for and help grow.',
                'example_sentence': 'The teacher worked to _____ each student\'s unique talents through individualized attention and encouragement.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nutation': {
                'pronunciation': '/nuˈteɪʃən/',
                'definition': 'Nutation is a small, periodic oscillation or wobbling motion superimposed on the primary rotational movement of a rotating body, most commonly observed in astronomy and physics. In astronomical contexts, nutation refers to the slight irregularities in the Earth\'s rotational axis caused by gravitational forces from the Moon and Sun, which create small oscillations in the planet\'s precession (the slow circular motion of the axis itself). These nutational movements are relatively small - typically measured in arcseconds - but are significant enough to affect precise astronomical observations and calculations. The term also applies to similar wobbling motions in other celestial bodies, spinning tops, gyroscopes, and rotating machinery where the rotation axis itself oscillates around its mean position. In plant biology, nutation describes the circular or spiral growth movements of plant parts, particularly growing tips of stems and roots that exhibit circumnutation - a helical growth pattern that helps plants explore their environment and find optimal growing conditions. Understanding nutation is crucial for precision in astronomical observations, navigation systems, and the design of rotating mechanical systems where stability and predictable motion are important.',
                'etymology': 'From Latin nutare meaning "to nod" or "to sway," referring to the nodding or wobbling motion of rotating objects.',
                'memory_tip': 'Think "nod-tation" - nutation is like a nodding motion, a small wobble superimposed on the main rotation.',
                'example_sentence': 'Astronomers must account for Earth\'s _____ when making precise measurements of star positions.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nutria': {
                'pronunciation': '/ˈnutriə/',
                'definition': 'Nutria, also known as coypu or river rats, are large, semi-aquatic rodents native to South America that have become significant invasive species in many parts of North America, Europe, and Asia. These robust animals, scientifically named Myocastor coypus, are characterized by their dense brown fur, webbed hind feet, large orange-yellow incisors, and rat-like tails. Adult nutria typically weigh 15-20 pounds and can grow up to two feet long, making them one of the largest rodents in many ecosystems where they\'ve been introduced. Originally raised for their fur in the early-to-mid 20th century, many nutria escaped or were released from fur farms, establishing wild populations that have caused significant ecological and economic damage. These prolific breeders consume large quantities of vegetation, destroying wetland habitats, undermining levees and riverbanks, and competing with native wildlife. Their feeding behavior involves consuming plant roots, which kills entire plants and contributes to coastal erosion and habitat loss. Management efforts include trapping programs, hunting initiatives, and research into biological control methods, as nutria populations have proven difficult to control once established.',
                'etymology': 'From Spanish nutria meaning "otter," from Latin lutra meaning "otter," though nutria are actually large rodents, not otters.',
                'memory_tip': 'Think "nutr-ia" sounds like "nutrition" - these large rodents consume lots of vegetation, sometimes too much in invaded habitats.',
                'example_sentence': 'Wildlife officials implemented a trapping program to control the invasive _____ population that was destroying the wetland vegetation.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nutrients': {
                'pronunciation': '/ˈnutriənts/',
                'definition': 'Nutrients are chemical substances found in food that are essential for the growth, maintenance, and functioning of living organisms. These vital compounds provide energy, support bodily functions, and serve as building blocks for tissues and organs. Nutrients are broadly classified into macronutrients and micronutrients based on the quantities needed by the body. Macronutrients include carbohydrates (primary energy source), proteins (building blocks for muscles and tissues), and fats (energy storage and cell membrane components), which are needed in relatively large amounts. Micronutrients include vitamins and minerals that are required in smaller quantities but are equally crucial for health, supporting functions like immune system operation, bone health, blood clotting, and energy metabolism. Essential nutrients cannot be produced by the body in sufficient quantities and must be obtained through diet, while non-essential nutrients can be synthesized by the body. The study of how nutrients interact with the body forms the foundation of nutrition science, dietetics, and food science. Proper nutrient intake through a balanced diet is fundamental to preventing deficiency diseases, maintaining optimal health, and supporting growth and development throughout life.',
                'etymology': 'From Latin nutrire meaning "to feed, nourish" + -ent suffix, meaning "substances that nourish."',
                'memory_tip': 'Think "nutri-ents" - substances that provide nutrition and nourishment to keep the body healthy.',
                'example_sentence': 'The dietitian explained that fresh fruits and vegetables provide essential _____ needed for optimal health.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nuzzer': {
                'pronunciation': '/ˈnʌzər/',
                'definition': 'Nuzzer appears to be an uncommon or colloquial term that may refer to someone who nuzzles - that is, someone who rubs or pushes gently with the nose, snout, or face, typically in an affectionate manner. The word would be derived from the verb "nuzzle," which describes the gentle, affectionate behavior often seen between animals and their offspring, between romantic partners, or between pets and their owners. If "nuzzer" is indeed a variant or informal form, it would describe a person or animal that frequently engages in nuzzling behavior. However, this particular spelling and usage is not standard in most dictionaries and may represent regional dialect, colloquial usage, or a specialized term within certain communities. The behavior of nuzzling itself is associated with comfort, affection, bonding, and intimacy across many species, serving important social and emotional functions in relationships. Without more context, it\'s possible this could also be a proper noun, nickname, or specialized term with meanings specific to particular groups or regions.',
                'etymology': 'Possibly derived from "nuzzle" + "-er" suffix, meaning "one who nuzzles," though this specific form is not standard.',
                'memory_tip': 'Think of someone who "nuzzles" - a "nuzzer" would be someone who likes to nuzzle or rub gently with their nose.',
                'example_sentence': 'The affectionate dog was such a _____, always pushing his nose against his owner\'s hand for attention.',
                'definition_source': 'Claude',
                'pronunciation_source': 'Claude',
                'example_sentence_source': 'Claude',
                'etymology_source': 'Claude',
                'memory_tip_source': 'Claude'
            },
            'nyctinasty': {
                'pronunciation': '/ˈnɪktɪˌnæsti/',
                'definition': 'Nyctinasty is a biological phenomenon in plants where leaves, flowers, or other plant parts exhibit rhythmic movements in response to daily cycles of light and darkness, independent of the direction of the light source. This type of plant movement, also called "sleep movements," involves the opening and closing or folding and unfolding of plant structures following circadian rhythms. Common examples include flowers that close at night and reopen in the morning, such as morning glories and tulips, and leaves that fold up during darkness, like those of prayer plants, beans, and clover. Unlike phototropism, which is directional growth toward or away from light, nyctinasty is a non-directional response controlled by internal biological clocks and triggered by changes in light intensity rather than light direction. The movements are typically caused by changes in cell turgor pressure in specialized motor cells located in structures called pulvini. This adaptation helps plants protect delicate reproductive organs from cool nighttime temperatures, reduce water loss through transpiration, and optimize their exposure to pollinators during appropriate times. Nyctinasty demonstrates the sophisticated ways plants have evolved to respond to environmental rhythms.',
                'etymology': 'From Greek nyktos (night) + nastos (pressed close), literally meaning "night pressing" or "night closing movements."',
                'memory_tip': 'Break it down: "nycti-" (night) + "nasty" (pressed) = plants that press their parts closed at night.',
                'example_sentence': 'The botanist studied _____ in prayer plants, observing how their leaves folded upward each evening as darkness approached.',
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
        input_file = 'output/batch_120_words.csv'
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
        embedded_words = ['the', 'and', 'ing', 'tion', 'noun', 'verb', 'adj']
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
        """Process all words in batch 120 with comprehensive Claude data"""
        logger.info("Processing Batch 120 with comprehensive Claude data...")
        
        # Detect combined words first
        combined_words = self.detect_combined_words()
        if combined_words:
            logger.info(f"Detected {len(combined_words)} combined word errors: {combined_words}")
        
        input_file = 'output/batch_120_words.csv'
        output_file = 'output/batch_120_processed.csv'
        
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
    processor = Batch120Processor()
    processed_count, failed_count = processor.process_batch()
    
    logger.info("Batch 120 processing completed!")
    logger.info(f"Processed {processed_count} words with comprehensive Claude data")
    logger.info(f"Output saved to: output/batch_120_processed.csv")
    logger.info(f"Results: {processed_count} successful, {failed_count} failed")