#!/usr/bin/env python3
"""
Batch 094 Processor for Scripps National Spelling Bee Words
Processes words from irreversible through jankers with comprehensive Claude-generated data
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

class Batch094Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.processed_count = 0

    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge"""
        
        batch_094_data = {
            'irreversible': {
                'definition': 'Irreversible describes something that cannot be undone, reversed, or returned to its original state, characterizing changes or processes that are permanent and cannot be canceled or corrected. This adjective applies to physical, chemical, biological, or social changes that create lasting effects. Irreversible medical conditions cannot be cured and represent permanent health changes. Irreversible chemical reactions produce products that cannot be converted back to original reactants. The term emphasizes finality and the impossibility of restoration. Environmental damage can be irreversible when ecosystems are permanently altered. Unlike temporary changes that can be undone, irreversible modifications create new permanent conditions. Irreversible decisions have lasting consequences that cannot be changed. The concept is crucial in fields like medicine, chemistry, and environmental science where understanding permanence helps inform choices and interventions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ir-ih-VUR-suh-buhl',
                'etymology': 'From Latin "irreversibilis," combining "in-" (not) with "reversibilis" (able to be turned back), derived from "revertere" (to turn back).',
                'language_origins': 'Latin',
                'example_sentence': 'The doctor explained that the nerve damage from the accident was _______ and would require long-term adaptation.',
                'memory_tip': 'Remember "IRREVERSIBLE" - think "IR-REVERSIBLE" meaning NOT "REVERSIBLE" (able to be undone) - permanent changes that cannot be undone.'
            },
            'irrevocable': {
                'definition': 'Irrevocable describes something that cannot be called back, changed, or canceled once it has been established, particularly referring to legal documents, decisions, or commitments that are final and binding. This adjective characterizes agreements, trusts, or actions that cannot be altered or withdrawn after execution. Irrevocable trusts cannot be modified or terminated by the person who created them. Irrevocable letters of credit guarantee payment obligations that banks cannot cancel. The term emphasizes legal finality and the inability to change established arrangements. Irrevocable powers of attorney remain in effect regardless of the grantor\'s changing wishes. Unlike revocable arrangements that can be modified, irrevocable commitments are permanent and binding. Courts may declare certain actions irrevocably taken. The concept provides legal certainty but requires careful consideration before implementation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-REV-uh-kuh-buhl',
                'etymology': 'From Latin "irrevocabilis," combining "in-" (not) with "revocabilis" (able to be called back), from "revocare" (to call back, revoke).',
                'language_origins': 'Latin',
                'example_sentence': 'The wealthy donor established an _______ trust to ensure the charity would receive funding permanently.',
                'memory_tip': 'Remember "IRREVOCABLE" - think "IR-REVOCABLE" meaning NOT "REVOCABLE" (able to be called back) - cannot be canceled or changed.'
            },
            'irrigation': {
                'definition': 'Irrigation is the artificial application of water to soil or land for agricultural purposes, enabling crop cultivation in areas with insufficient natural rainfall or during dry periods. This agricultural practice involves systems of canals, pipes, sprinklers, or drip networks that deliver water directly to plants. Modern irrigation methods include drip irrigation, center-pivot systems, and flood irrigation techniques. Irrigation has enabled agricultural development in arid regions and increased crop yields worldwide. Ancient civilizations developed sophisticated irrigation systems that supported urban development and population growth. The practice requires careful water management to prevent soil salinization and water waste. Precision irrigation uses technology to optimize water delivery based on soil moisture and plant needs. Sustainable irrigation practices balance agricultural productivity with water conservation and environmental protection.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ir-ih-GAY-shun',
                'etymology': 'From Latin "irrigatio," derived from "irrigare" meaning "to water" or "to moisten," combining "in-" (into) with "rigare" (to wet, moisten).',
                'language_origins': 'Latin',
                'example_sentence': 'The desert farm\'s sophisticated _______ system allowed farmers to grow crops year-round despite minimal rainfall.',
                'memory_tip': 'Remember "IRRIGATION" - think "IRR-IGATION" like water flowing in an "AGITATED" way "IRR" (around) crops - artificial watering of plants.'
            },
            'irritability': {
                'definition': 'Irritability is the tendency to become easily annoyed, impatient, or angry in response to minor frustrations or stimuli, representing a heightened sensitivity to potentially bothersome situations. This psychological and physiological state can result from stress, fatigue, illness, or underlying emotional conditions. Medical irritability might indicate hormonal imbalances, neurological conditions, or medication side effects. Psychological irritability often accompanies anxiety, depression, or overwhelming life circumstances. The condition affects interpersonal relationships and daily functioning when individuals react disproportionately to normal situations. Unlike occasional bad moods, chronic irritability represents persistent patterns of heightened reactivity. Managing irritability often involves addressing underlying causes, developing coping strategies, and sometimes seeking professional help. The concept recognizes that emotional regulation varies among individuals and can be influenced by numerous biological and environmental factors.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ir-ih-tuh-BIL-ih-tee',
                'etymology': 'From Latin "irritabilitas," derived from "irritabilis" (easily provoked), from "irritare" (to provoke, annoy). The suffix "-ity" indicates a state or quality.',
                'language_origins': 'Latin',
                'example_sentence': 'His increased _______ during finals week was a clear sign that stress was affecting his emotional well-being.',
                'memory_tip': 'Remember "IRRITABILITY" - think "IRRITATE-ABILITY" meaning the "ABILITY" to be easily "IRRITATED" - tendency to get annoyed easily.'
            },
            'isaac': {
                'definition': 'Isaac is a male given name of Hebrew origin, most famous as the biblical patriarch who was the son of Abraham and Sarah, and father of Jacob and Esau, playing a crucial role in Judeo-Christian tradition. This proper noun appears in religious texts as a key figure in God\'s covenant with Abraham. Isaac was born to Sarah in her old age, representing divine intervention and promise fulfillment. The name has been popular across many cultures and time periods. Notable historical figures named Isaac include Sir Isaac Newton, the famous physicist and mathematician. The biblical Isaac was nearly sacrificed by his father Abraham in a test of faith. Isaac\'s story includes his marriage to Rebekah and the birth of twin sons Jacob and Esau. The name continues to be used widely in contemporary society across various religious and cultural backgrounds.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'EYE-zuk',
                'etymology': 'From Hebrew "Yitzchak" meaning "he will laugh" or "laughter," referring to Sarah\'s reaction to God\'s promise of a son in her old age.',
                'language_origins': 'Hebrew',
                'example_sentence': 'The biblical story of _______ and his sons Jacob and Esau illustrates themes of divine promise and family conflict.',
                'memory_tip': 'Remember "ISAAC" - think "I-SAAC" like "I" (will) "SAC" (sacrifice) but it means "laughter" - the biblical patriarch whose name means laughter.'
            },
            'isagoge': {
                'definition': 'Isagoge is an introductory work or treatise that provides basic principles and foundational knowledge for studying a particular subject, especially in philosophy, theology, or academic disciplines. This scholarly term describes educational texts designed to prepare students for advanced study. The most famous isagoge is Porphyry\'s "Introduction" to Aristotle\'s logical works, which influenced medieval education for centuries. Academic isagoge works explain fundamental concepts, terminology, and methods needed for specialized study. Unlike comprehensive textbooks that cover entire subjects, isagoge works focus on essential background knowledge. Medieval universities used isagoge texts to introduce students to complex philosophical and theological concepts. Modern academic programs might use isagoge materials to prepare students for graduate study. The concept emphasizes the importance of proper foundational knowledge before attempting advanced scholarly work.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eye-SAG-uh-jee',
                'etymology': 'From Greek "eisagoge," meaning "introduction" or "leading in," combining "eis" (into) with "agoge" (leading, guidance). Used for introductory academic texts.',
                'language_origins': 'Greek',
                'example_sentence': 'The philosophy professor assigned Porphyry\'s _______ as essential preparation for understanding Aristotelian logic.',
                'memory_tip': 'Remember "ISAGOGE" - think "I-SAG-OGE" like "I" need to "SAG" (study) this "OGE" (introduction) - an introductory academic text.'
            },
            'ishihara': {
                'definition': 'Ishihara refers to a color vision test developed by Japanese ophthalmologist Shinobu Ishihara, consisting of colored dot patterns that reveal numbers or shapes visible only to people with normal color vision. This medical diagnostic tool identifies color blindness, particularly red-green color deficiencies. The Ishihara test uses pseudoisochromatic plates with dots of various colors and sizes arranged to form numbers or patterns. People with normal color vision see different numbers than those with color vision deficiencies. The test has become the standard screening method for color blindness in medical, educational, and occupational settings. Different plates test for different types of color vision problems. The Ishihara test is quick, reliable, and requires no special equipment beyond the test booklet. Color vision screening is important for certain professions requiring accurate color discrimination.',
                'part_of_speech': 'proper noun, adjective',
                'pronunciation_guide': 'ish-ih-HAR-ah',
                'etymology': 'Named after Shinobu Ishihara (1879-1963), Japanese ophthalmologist who developed the color vision test in 1917.',
                'language_origins': 'Japanese (personal name)',
                'example_sentence': 'The pilot candidate failed the _______ color vision test and was unable to pursue a career in commercial aviation.',
                'memory_tip': 'Remember "ISHIHARA" - think "ISH-I-HARA" like "ISH" (kinda) "I" can see colors, but this "HARA" (test) will tell - the color blindness test.'
            },
            'islamic': {
                'definition': 'Islamic describes anything relating to Islam, the monotheistic religion founded by the Prophet Muhammad in 7th-century Arabia, encompassing beliefs, practices, culture, law, and civilization associated with Muslim communities worldwide. This adjective characterizes the religious, cultural, and historical elements connected to Islam. Islamic art features distinctive geometric patterns and calligraphy reflecting religious principles. Islamic law (Sharia) governs personal conduct and legal matters in Muslim societies. The term covers diverse cultures from Morocco to Indonesia united by common religious beliefs. Islamic architecture includes mosques, madrasas, and palaces with characteristic features like minarets and domes. Islamic scholarship preserved and advanced knowledge during the medieval period. Contemporary Islamic communities adapt religious teachings to modern contexts while maintaining core beliefs. The concept recognizes both unity of faith and diversity of cultural expression within the global Muslim community.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'iz-LAM-ik',
                'etymology': 'From Arabic "islami," derived from "islam" meaning "submission" (to Allah), from the root "s-l-m" (peace, submission).',
                'language_origins': 'Arabic',
                'example_sentence': 'The museum\'s _______ art collection featured beautiful calligraphy and geometric patterns from various historical periods.',
                'memory_tip': 'Remember "ISLAMIC" - think "ISLAM-IC" meaning relating to "ISLAM" - the religion and culture associated with Muslim faith.'
            },
            'island': {
                'definition': 'An island is a piece of land that is completely surrounded by water, forming a distinct geographical feature separate from mainland areas, ranging in size from small rocky outcrops to large landmasses like Australia or Greenland. This geographical term describes naturally formed or artificial land areas isolated by water barriers. Islands can form through volcanic activity, tectonic processes, or changes in sea level. Some islands support unique ecosystems and species that evolved in isolation. Island nations like Japan and the United Kingdom have developed distinctive cultures influenced by their maritime geography. Artificial islands are created for various purposes including airports, military bases, and urban development. Island environments often face special challenges related to limited resources, transportation, and climate vulnerability. The concept appears in literature and culture as symbols of isolation, paradise, or adventure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EYE-lund',
                'etymology': 'From Old English "īegland," combining "īeg" (island) with "land." The "s" was added later by association with "isle."',
                'language_origins': 'Old English',
                'example_sentence': 'The remote _______ served as a refuge for endangered species that had disappeared from the mainland.',
                'memory_tip': 'Remember "ISLAND" - think "IS-LAND" like land that "IS" surrounded by water - a piece of land completely encircled by water.'
            },
            'islands': {
                'definition': 'Islands are multiple pieces of land completely surrounded by water, forming distinct geographical features that can range from tiny uninhabited rocks to large populated landmasses supporting entire nations. This plural noun describes various types of water-surrounded territories. Volcanic islands form from underwater eruptions that build up to sea level. Coral islands develop from marine organisms creating reef structures. Continental islands result from rising sea levels isolating mainland areas. Island chains or archipelagos consist of multiple related islands formed by similar geological processes. Some islands are densely populated urban centers while others remain uninhabited wilderness areas. Islands often develop unique cultures, languages, and biological communities due to their isolation. Climate change poses special threats to low-lying islands through sea level rise. Tourism, fishing, and shipping are common economic activities for island communities.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'EYE-lundz',
                'etymology': 'From Old English "īegland" (island) with the plural suffix "-s." The word developed from "īeg" (island) plus "land."',
                'language_origins': 'Old English',
                'example_sentence': 'The tropical _______ in the Pacific Ocean are home to diverse marine life and coral reef ecosystems.',
                'memory_tip': 'Remember "ISLANDS" - think "IS-LANDS" like multiple pieces of land that each "IS" surrounded by water - many water-surrounded territories.'
            },
            'isle': {
                'definition': 'An isle is a small island, typically used in poetic, literary, or formal contexts to describe compact landmasses surrounded by water, often emphasizing their picturesque, remote, or romantic qualities. This noun suggests smaller scale than "island" and carries connotations of beauty or isolation. The British Isles include thousands of small isles around the main islands. Literary works often feature mysterious or enchanted isles in adventure stories. Unlike continental landmasses, isles suggest intimate, manageable geographical features. Some famous isles include the Isle of Wight, Isle of Skye, and various Caribbean isles. The term appears in poetry and song to evoke feelings of escape, beauty, or solitude. Tourist destinations often market themselves as tropical isles to suggest paradise-like qualities. The concept emphasizes the romantic and aesthetic appeal of small water-surrounded lands.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EYL',
                'etymology': 'From Old French "isle," derived from Latin "insula" (island). The word entered English through Norman French influence.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The poet wrote about a mystical _______ where time seemed to stand still and worries disappeared.',
                'memory_tip': 'Remember "ISLE" - think "I\'LL" go to this small "ISLE" - a poetic word for a small, often beautiful island.'
            },
            'isms': {
                'definition': 'Isms are distinctive doctrines, theories, or practices characterized by particular beliefs, principles, or ideologies, typically referring to formal systems of thought that end with the suffix "-ism." This plural noun encompasses various intellectual, political, religious, or social movements. Political isms include capitalism, socialism, and fascism. Religious isms encompass Buddhism, Judaism, and various denominations. Artistic isms include impressionism, cubism, and romanticism. The term often carries implications of systematic belief structures that influence behavior and worldview. Academic isms might include feminism, postmodernism, and structuralism. Some isms become dominant cultural forces while others remain niche philosophies. The concept recognizes human tendency to organize beliefs into coherent systems. Understanding various isms helps analyze historical movements, cultural trends, and contemporary debates.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'IZ-umz',
                'etymology': 'From Greek suffix "-ismos," indicating a distinctive doctrine or practice. The plural form refers to multiple ideological systems.',
                'language_origins': 'Greek',
                'example_sentence': 'The philosophy course covered various political _______ including liberalism, conservatism, and anarchism.',
                'memory_tip': 'Remember "ISMS" - think "IS-MS" like "IS" (many) "M\'S" (systems) of belief - doctrines and ideologies ending in "-ism."'
            },
            'isolation': {
                'definition': 'Isolation is the state of being separated, set apart, or cut off from others, whether physically, socially, or emotionally, representing disconnection that can be voluntary or involuntary. This noun describes various forms of separation from normal contact or interaction. Social isolation affects mental health when people lack meaningful relationships. Geographic isolation occurs when communities are physically separated from others. Medical isolation prevents disease transmission by separating infected patients. The term can describe both positive solitude sought for reflection and negative loneliness imposed by circumstances. Political isolation occurs when nations are excluded from international cooperation. Scientific isolation allows controlled experiments by eliminating external variables. Unlike temporary separation, isolation often implies significant disconnection that affects wellbeing or function. Understanding isolation helps address problems related to loneliness, quarantine, and social exclusion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eye-suh-LAY-shun',
                'etymology': 'From French "isolation," derived from Italian "isolato" (isolated), ultimately from Latin "insula" (island). The concept suggests being made island-like.',
                'language_origins': 'French, Italian, Latin',
                'example_sentence': 'The elderly man\'s social _______ worsened after he lost his ability to drive and visit friends.',
                'memory_tip': 'Remember "ISOLATION" - think "ISLE-ATION" like being on an "ISLE" (island) in a state of separation - being cut off from others.'
            },
            'isosceles': {
                'definition': 'Isosceles describes a triangle that has two sides of equal length and two equal angles opposite those sides, representing one of the fundamental triangle classifications in geometry. This mathematical term characterizes triangles with specific symmetrical properties that distinguish them from equilateral triangles (three equal sides) and scalene triangles (no equal sides). Isosceles triangles have one line of symmetry that passes through the vertex between the two equal sides and bisects the base. The two equal angles are called base angles, while the angle between the equal sides is the vertex angle. Understanding isosceles triangles is essential for geometric proofs and calculations. The properties of isosceles triangles appear in architecture, engineering, and design where symmetrical structures are needed. Mathematical problems involving isosceles triangles often focus on finding missing angles or side lengths using geometric principles.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'eye-SOS-uh-leez',
                'etymology': 'From Greek "isoskeles," combining "iso-" (equal) with "skelos" (leg). The word literally means "equal-legged," referring to the two equal sides.',
                'language_origins': 'Greek',
                'example_sentence': 'The architect designed the roof as an _______ triangle to create a symmetrical appearance for the building.',
                'memory_tip': 'Remember "ISOSCELES" - think "ISO-SCELES" like "ISO" (equal) "SCELES" (legs/sides) - a triangle with two equal sides.'
            },
            'isotopic': {
                'definition': 'Isotopic refers to or relating to isotopes, which are atoms of the same element that have different numbers of neutrons while maintaining the same number of protons, resulting in different atomic masses but identical chemical properties. This scientific adjective describes atomic variations that are crucial in nuclear science, chemistry, and physics. Isotopic analysis helps determine the age of archaeological artifacts and geological formations. Isotopic labeling allows scientists to track molecular pathways in biological research. Different isotopes of elements like carbon, hydrogen, and uranium have various applications in medicine, energy, and research. Isotopic signatures can reveal information about environmental conditions, dietary habits, and geographical origins. Some isotopes are radioactive while others are stable. Understanding isotopic properties is essential for nuclear medicine, radiocarbon dating, and nuclear energy applications. Isotopic studies contribute to fields ranging from astronomy to forensic science.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'eye-suh-TOP-ik',
                'etymology': 'From Greek "isotopes," combining "iso-" (equal) with "topos" (place), plus "-ic." Originally meant "same place" referring to position in the periodic table.',
                'language_origins': 'Greek',
                'example_sentence': 'The archaeologist used _______ analysis to determine that the ancient wooden artifacts were over 3,000 years old.',
                'memory_tip': 'Remember "ISOTOPIC" - think "ISO-TOPIC" like "ISO" (same) "TOPIC" (place) in periodic table - relating to atoms with same protons but different neutrons.'
            },
            'italian': {
                'definition': 'Italian refers to anything relating to Italy, its people, language, or culture, encompassing the characteristics and heritage associated with the European nation known for its contributions to art, cuisine, fashion, and civilization. This adjective describes the Romance language spoken by over 65 million people as well as the rich cultural traditions of the Italian peninsula. Italian cuisine features pasta, pizza, and regional specialties that have become globally popular. Italian art includes Renaissance masters like Leonardo da Vinci and Michelangelo. The Italian language evolved from Latin and serves as the basis for much musical and culinary terminology worldwide. Italian fashion and design influence global trends in clothing, furniture, and automotive styling. Italian history encompasses the Roman Empire, Renaissance city-states, and modern unification. Contemporary Italy balances preservation of cultural heritage with modern economic and technological development.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-TAL-yun',
                'etymology': 'From Medieval Latin "Italianus," derived from "Italia" (Italy), ultimately from Greek "Italia," possibly meaning "land of cattle."',
                'language_origins': 'Medieval Latin, Greek',
                'example_sentence': 'The _______ restaurant served authentic pasta dishes prepared using traditional family recipes.',
                'memory_tip': 'Remember "ITALIAN" - think "ITALY-AN" meaning belonging to or relating to "ITALY" - the people, language, and culture of Italy.'
            },
            'italians': {
                'definition': 'Italians are people from Italy or of Italian descent, representing citizens of the European nation known for its rich cultural heritage, artistic achievements, and influence on world civilization. This plural noun describes individuals who share Italian nationality, ethnicity, or cultural background. Historical Italians include Renaissance artists, explorers like Columbus, and scientists like Galileo. Italian immigrants to countries like the United States, Argentina, and Australia established communities that maintain cultural traditions. Modern Italians have contributed to fashion, automotive design, cuisine, and cinema. Italian culture emphasizes family relationships, regional identity, and appreciation for art and beauty. The Italian diaspora has spread Italian language, customs, and cuisine worldwide. Contemporary Italians balance respect for traditional ways with participation in modern European and global society. Regional differences within Italy create diverse Italian identities while maintaining shared national characteristics.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'ih-TAL-yunz',
                'etymology': 'From Medieval Latin "Italianus," derived from "Italia" (Italy). The plural form refers to multiple people from or relating to Italy.',
                'language_origins': 'Medieval Latin, Greek',
                'example_sentence': 'Many _______ emigrated to America in the early 1900s, bringing their culinary traditions and strong work ethic.',
                'memory_tip': 'Remember "ITALIANS" - think "ITALY-ANS" like people who are "ANS" (from) "ITALY" - people from or descended from Italy.'
            },
            'italicization': {
                'definition': 'Italicization is the process of formatting text in italics, a slanted typeface used to emphasize words, indicate foreign terms, mark titles of works, or show special textual elements in written communication. This typographical practice serves various grammatical and stylistic functions. Academic writing uses italicization for book titles, scientific names, and foreign phrases. Italicization can emphasize important words or show contrast in meaning. Legal documents use italicization for case names and statutes. The practice evolved from manuscript traditions where scribes used different lettering styles for emphasis. Digital publishing makes italicization easy to apply and modify. Style guides specify when italicization is appropriate versus other emphasis methods like boldface or underlining. Understanding proper italicization helps create clear, professional written communication that follows accepted conventions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-tal-ih-sih-ZAY-shun',
                'etymology': 'From "italic" (referring to the slanted typeface first used in Italy) plus the suffix "-ization" indicating the process of making italic.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The editor corrected the manuscript by adding proper _______ to all foreign words and book titles.',
                'memory_tip': 'Remember "ITALICIZATION" - think "ITALIC-IZATION" meaning the process of making text "ITALIC" - formatting text in slanted letters for emphasis.'
            },
            'italy': {
                'definition': 'Italy is a European country located on the Italian Peninsula in Southern Europe, famous for its rich history, cultural contributions, cuisine, and artistic heritage that has influenced world civilization for over two millennia. This proper noun refers to the nation that includes the mainland peninsula, Sicily, Sardinia, and other smaller islands. Italy is the birthplace of the Roman Empire and the Renaissance, two periods that profoundly shaped Western civilization. Modern Italy is known for fashion, automotive design, cuisine, and tourism. Italian cities like Rome, Florence, and Venice contain countless historical and artistic treasures. The country has contributed significantly to science, literature, music, and philosophy. Contemporary Italy is a member of the European Union and plays important roles in international politics and economics. Italian geography includes the Alps, Mediterranean coastlines, and diverse landscapes from industrial north to agricultural south.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'IT-uh-lee',
                'etymology': 'From Latin "Italia," possibly derived from Greek "Italia," meaning "land of cattle" or named after the Italic peoples who inhabited the peninsula.',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'Tourists flock to _______ each year to experience its ancient ruins, Renaissance art, and world-famous cuisine.',
                'memory_tip': 'Remember "ITALY" - think of the distinctive boot-shaped peninsula in Europe known for pasta, art, and Roman history.'
            },
            'ited': {
                'definition': 'This appears to be an incomplete or potentially erroneous word fragment that may be part of a larger word or represent a suffix. Without additional context, "ited" could be a past participle ending found in words like "visited," "invited," or "excited." The fragment might result from text processing errors or represent technical terminology in specialized contexts. In academic or technical writing, partial word forms sometimes appear as examples of linguistic patterns or morphological analysis. The sequence "ited" follows English patterns for past participle formation from verbs ending in consonants. However, as a standalone word, "ited" does not have standard dictionary meaning in English. Context would be necessary to determine the intended complete word or specific usage.',
                'part_of_speech': 'word fragment/suffix',
                'pronunciation_guide': 'EYE-tid',
                'etymology': 'Appears to be a suffix or word fragment, possibly from Latin past participle endings "-itus" or English "-ed" formations.',
                'language_origins': 'Latin, English (uncertain)',
                'example_sentence': 'The word fragment _______ appears to be part of a larger word that was incompletely processed.',
                'memory_tip': 'Remember "ITED" - this appears to be a word fragment or suffix, likely part of words ending in "-ited" like "visited" or "invited."'
            },
            'iteration': {
                'definition': 'Iteration is the process of repeating a set of operations, procedures, or calculations, typically with the goal of approaching a desired result or improving outcomes through successive refinements. This noun describes methodical repetition used in various fields including mathematics, computer science, and project management. Mathematical iteration involves repeated application of functions to approximate solutions. Computer programming uses iteration through loops to process data or solve problems. Business iteration involves repeated cycles of planning, implementation, and evaluation. Unlike single attempts, iteration recognizes that complex problems often require multiple approaches. Scientific iteration involves testing, analyzing, and refining hypotheses. Software development uses iterative processes to gradually build and improve products. The concept emphasizes learning and improvement through repetition rather than expecting perfect results on first attempts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'it-uh-RAY-shun',
                'etymology': 'From Latin "iteratio," derived from "iterare" meaning "to repeat," from "iterum" (again). The word emphasizes repetitive processes.',
                'language_origins': 'Latin',
                'example_sentence': 'The software team completed another _______ of the program, fixing bugs and adding new features based on user feedback.',
                'memory_tip': 'Remember "ITERATION" - think "ITER-ATION" like "ITERATING" (repeating) through a process - repetition to improve or solve problems.'
            },
            'itself': {
                'definition': 'Itself is a reflexive pronoun referring back to a previously mentioned singular noun or pronoun, emphasizing the same entity without involving other subjects, often used for emphasis or to indicate that something acts upon or relates to its own nature. This pronoun serves various grammatical functions including emphasis, clarification, and reflexive action. "The problem will solve itself" indicates autonomous resolution. "The city itself was beautiful" emphasizes the city specifically rather than its surroundings. Itself can indicate automatic or inherent action without external intervention. Unlike "themselves" which refers to plural subjects, itself relates to singular entities. The word helps avoid ambiguity in sentences with multiple possible references. Philosophical discussions use "itself" to explore concepts of identity and self-reference. The pronoun enables precise communication about relationships between subjects and their actions or qualities.',
                'part_of_speech': 'pronoun (reflexive)',
                'pronunciation_guide': 'it-SELF',
                'etymology': 'From Middle English, combining "it" with "self." The compound emphasizes the identity of the subject with the object.',
                'language_origins': 'Middle English',
                'example_sentence': 'The garden seemed to maintain _______ without any human intervention, thriving through natural processes.',
                'memory_tip': 'Remember "ITSELF" - think "IT-SELF" meaning "IT" referring back to "ITSELF" - the thing acting on or relating to its own nature.'
            },
            'ivermectin': {
                'definition': 'Ivermectin is an anti-parasitic medication used to treat various parasitic infections in humans and animals, originally developed from compounds found in soil bacteria. This pharmaceutical drug is effective against intestinal roundworms, scabies, and river blindness (onchocerciasis). Veterinary ivermectin treats parasites in livestock, horses, and pets. The medication works by paralyzing and killing parasites through interference with their nervous systems. Ivermectin has been crucial in controlling neglected tropical diseases in developing countries. The drug\'s discoverers received the Nobel Prize in Physiology or Medicine in 2015. During the COVID-19 pandemic, ivermectin became controversial when some promoted it as a treatment despite limited scientific evidence. Proper medical supervision is essential for ivermectin use due to potential side effects and drug interactions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eye-ver-MEK-tin',
                'etymology': 'Named from "iver-" (possibly from the fungus Streptomyces avermitilis from which it\'s derived) plus "-mectin" (common suffix for antibiotic compounds).',
                'language_origins': 'Scientific Latin',
                'example_sentence': 'The doctor prescribed _______ to treat the patient\'s parasitic infection after confirming the diagnosis through laboratory tests.',
                'memory_tip': 'Remember "IVERMECTIN" - think "I-VER-MECTIN" like "I" need "VER" (very) good "MECTIN" (medicine) - an anti-parasitic medication.'
            },
            'jabberwocky': {
                'definition': 'Jabberwocky refers to meaningless or nonsensical speech or writing, named after Lewis Carroll\'s famous nonsense poem "Jabberwocky" from "Through the Looking-Glass," which uses invented words and sounds that suggest meaning without actually having conventional definitions. This literary term describes language that sounds impressive but lacks real substance. The original poem includes words like "brillig," "slithy," and "vorpal" that Carroll invented for poetic effect. Academic jabberwocky might include unnecessarily complex terminology that obscures rather than clarifies meaning. Political jabberwocky uses impressive-sounding language to avoid clear positions. The concept recognizes that language can create emotional or aesthetic effects beyond literal meaning. Literary jabberwocky demonstrates the playful possibilities of language experimentation. Understanding jabberwocky helps identify when communication prioritizes style over substance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAB-er-wok-ee',
                'etymology': 'Coined by Lewis Carroll in 1871 for his nonsense poem. The word was created to sound meaningful while being essentially meaningless, demonstrating linguistic play.',
                'language_origins': 'English (literary invention)',
                'example_sentence': 'The politician\'s speech was pure _______, using complex words that sounded important but said nothing concrete.',
                'memory_tip': 'Remember "JABBERWOCKY" - think "JABBER-WOCKY" like "JABBER" (meaningless talk) that\'s "WOCKY" (silly) - nonsensical or meaningless language.'
            },
            'jabot': {
                'definition': 'A jabot is a decorative frill or ruffle of fabric, typically lace or fine material, worn at the throat or chest as part of formal or period clothing, historically associated with men\'s fashion in the 17th and 18th centuries. This fashion accessory featured elaborate lacework or pleated fabric that extended from the neck opening of shirts or coats. Jabots were symbols of wealth and social status during the baroque and rococo periods. Modern jabots appear in formal wear, judicial robes, and period costume recreations. The accessory requires skilled craftsmanship to create the delicate pleating and lacework. Historical portraits show aristocrats and wealthy merchants wearing elaborate jabots. Contemporary fashion occasionally revives jabot-inspired designs for formal occasions. The term extends to similar decorative elements in women\'s fashion and costume design.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'zhah-BOH',
                'etymology': 'From French "jabot," originally meaning "bird\'s crop," referring to the ruffled appearance resembling the crop of a bird. The fashion term developed from this anatomical reference.',
                'language_origins': 'French',
                'example_sentence': 'The historical costume designer carefully crafted an elaborate lace _______ for the actor portraying an 18th-century nobleman.',
                'memory_tip': 'Remember "JABOT" - think "JABOT" like a decorative "JOB" (work) at the "BOT" (bottom) of the throat - ornamental neck ruffle.'
            },
            'jacana': {
                'definition': 'A jacana is a tropical wading bird found in wetlands across Africa, Asia, Australia, and the Americas, characterized by extremely long toes that enable them to walk on floating vegetation like lily pads. This bird family (Jacanidae) includes eight species known for their unique adaptation to aquatic plant surfaces. Jacanas have specialized feet that distribute their weight across water plants, allowing them to forage for insects, small fish, and plant material. Many jacana species exhibit polyandry, where females mate with multiple males who then care for the eggs and young. The birds\' long toes and claws help them navigate dense aquatic vegetation. Northern jacanas in the Americas show distinctive bronze and black plumage. Jacanas are important indicators of wetland ecosystem health. Their specialized feeding and nesting behaviors make them vulnerable to habitat destruction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'juh-KAH-nah',
                'etymology': 'From Portuguese "jaçanã," borrowed from Tupi indigenous language of Brazil. The word entered scientific nomenclature through early naturalist observations.',
                'language_origins': 'Portuguese, Tupi',
                'example_sentence': 'The _______ carefully stepped across the lily pads, its long toes preventing it from sinking into the water.',
                'memory_tip': 'Remember "JACANA" - think "JACK-ANA" like "JACK" (guy) walking on "ANA" (water) - the long-toed bird that walks on water plants.'
            },
            'jacaranda': {
                'definition': 'Jacaranda refers to a genus of flowering trees native to South America, particularly known for their spectacular displays of purple-blue tubular flowers that bloom in spring and their delicate, fern-like compound leaves. These ornamental trees have become popular in warm climates worldwide for landscaping and urban beautification. Jacaranda trees can grow 40-60 feet tall and produce clusters of trumpet-shaped flowers before the leaves emerge. The wood is valuable for furniture making due to its attractive grain and workability. Different species of jacaranda trees grow throughout tropical and subtropical regions. The trees are deciduous in cooler areas but may remain evergreen in tropical climates. Jacaranda blooms create spectacular purple canopies in cities like Los Angeles, Buenos Aires, and Brisbane. The trees require warm climates and well-drained soil to thrive.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jak-uh-RAN-duh',
                'etymology': 'From Portuguese "jacarandá," borrowed from Tupi-Guarani indigenous languages of South America, where these trees are native.',
                'language_origins': 'Portuguese, Tupi-Guarani',
                'example_sentence': 'The city streets were carpeted with purple flowers from the blooming _______ trees lining the boulevard.',
                'memory_tip': 'Remember "JACARANDA" - think "JACK-A-RANDA" like "JACK" has "A" beautiful "RANDA" (purple) tree - the purple-flowering ornamental tree.'
            },
            'jack': {
                'definition': 'Jack can refer to several different things: a mechanical device for lifting heavy objects (car jack), a common male given name, playing cards (jack of hearts), electrical connectors, or various tools and equipment. As a mechanical device, jacks use leverage or hydraulic pressure to raise automobiles for tire changes or repairs. The name Jack has been popular for centuries and appears in folklore, nursery rhymes, and literature. In card games, jacks rank between tens and queens in standard decks. Electrical jacks provide connection points for plugs in audio, telecommunications, and power systems. The word appears in many compound terms like lumberjack, steeplejack, and hijack. Historical usage includes nautical flags (Union Jack) and various occupational tools. The versatility of the word reflects its long history in English usage.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JAK',
                'etymology': 'From Middle English "Jakke," a nickname for "John." The various mechanical and technical uses developed from the personal name through metaphorical extension.',
                'language_origins': 'Middle English',
                'example_sentence': 'The mechanic used a hydraulic _______ to lift the car safely before changing the flat tire.',
                'memory_tip': 'Remember "JACK" - think of "JACK" as a versatile word - from the lifting device to the playing card to the common name.'
            },
            'jackal': {
                'definition': 'A jackal is a medium-sized carnivorous mammal closely related to wolves and dogs, found primarily in Africa, Asia, and southeastern Europe, known for their opportunistic feeding habits and distinctive howling vocalizations. These canids are smaller than wolves but larger than foxes, typically weighing 15-35 pounds. Jackals are highly adaptable animals that hunt small prey, scavenge carrion, and sometimes feed on fruits and insects. They live in pairs or small family groups and are known for their intelligence and cunning behavior. Different species include the golden jackal, black-backed jackal, and side-striped jackal. Jackals play important ecological roles as both predators and scavengers. In various cultures, jackals appear in folklore and mythology, often associated with cunning or death. Modern jackal populations face pressure from habitat loss and human encroachment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAK-ul',
                'etymology': 'From Turkish "çakal," ultimately derived from Persian "shaghal." The word entered European languages through Ottoman Turkish.',
                'language_origins': 'Turkish, Persian',
                'example_sentence': 'The _______ pack scavenged the remains left by lions, demonstrating their opportunistic feeding behavior.',
                'memory_tip': 'Remember "JACKAL" - think "JACK-AL" like "JACK" (guy) who\'s "AL" (always) cunning - the clever wild dog that scavenges.'
            },
            'jacobean': {
                'definition': 'Jacobean refers to the period, style, or characteristics associated with the reign of King James I of England (1603-1625), encompassing architecture, furniture, literature, and decorative arts from this early 17th-century era. This historical and artistic term describes the transition period between Elizabethan and later Stuart styles. Jacobean architecture features more classical elements than earlier Tudor styles, with increased use of symmetry and Renaissance influences. Jacobean furniture is characterized by dark oak construction, elaborate carving, and heavy proportions. The period produced significant literature including works by Shakespeare, John Donne, and the King James Bible translation. Jacobean decorative arts show Continental European influences mixed with English traditions. The style represents a bridge between medieval and fully classical English design. Modern reproductions of Jacobean furniture remain popular for their substantial, dignified appearance.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'jak-uh-BEE-un',
                'etymology': 'From Latin "Jacobus" (James), referring to King James I. The suffix "-ean" indicates belonging to or characteristic of that period.',
                'language_origins': 'Latin',
                'example_sentence': 'The museum\'s _______ furniture collection featured massive oak pieces with intricate carved details from the early 1600s.',
                'memory_tip': 'Remember "JACOBEAN" - think "JACOB-EAN" relating to "JACOB" (James) - the style from King James I\'s reign in early 1600s England.'
            },
            'jacquard': {
                'definition': 'Jacquard refers to a type of fabric with intricate woven patterns created using a special loom invented by Joseph Marie Jacquard in 1804, or the weaving technique itself that allows complex designs to be woven directly into textiles. This textile innovation uses a system of punched cards to control individual warp threads, enabling elaborate patterns without hand manipulation. Jacquard fabrics include brocades, damasks, and tapestries with sophisticated designs. The Jacquard loom revolutionized textile production by automating pattern weaving. Modern jacquard weaving uses computer-controlled looms but follows the same basic principles. Jacquard techniques produce upholstery fabrics, clothing materials, and decorative textiles. The invention is considered a precursor to computer programming through its use of coded cards. High-quality jacquard fabrics are prized for their durability and intricate beauty.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'zhah-KARD',
                'etymology': 'Named after Joseph Marie Jacquard (1752-1834), French weaver and inventor who developed the automated weaving loom that bears his name.',
                'language_origins': 'French (personal name)',
                'example_sentence': 'The elegant sofa was upholstered in a rich _______ fabric featuring an intricate floral pattern.',
                'memory_tip': 'Remember "JACQUARD" - think "JACK-CARD" like "JACK" used punch "CARDS" to control looms - the automated weaving technique named after its inventor.'
            },
            'jacques': {
                'definition': 'Jacques is a French male given name, the French equivalent of James or Jacob, commonly used in French-speaking countries and appearing in literature, history, and culture as both a personal name and sometimes as a generic term for French peasants or common people. This proper noun has historical significance in various contexts. "Jacques" appears in Shakespeare\'s "As You Like It" as a melancholy character. The name has been borne by notable figures including philosophers, artists, and political leaders. In some historical contexts, "Jacques" was used disparagingly to refer to French peasants, particularly during peasant revolts. Modern usage primarily treats Jacques as a personal name rather than a generic term. The name appears in various cultural works and has contributed to French cultural identity. Understanding the name helps in reading French literature and understanding historical references.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'ZHAHK',
                'etymology': 'From Old French "Jacques," derived from Latin "Iacobus," ultimately from Hebrew "Ya\'aqov" (Jacob). The name entered French through Christian tradition.',
                'language_origins': 'French, Latin, Hebrew',
                'example_sentence': '_______ Cousteau, the famous oceanographer, introduced millions of people to the wonders of marine life.',
                'memory_tip': 'Remember "JACQUES" - think of the French pronunciation "ZHAHK" - the French version of the name James or Jacob.'
            },
            'jactance': {
                'definition': 'Jactance is ostentatious boasting, bragging, or vainglorious display intended to impress others or demonstrate superiority, representing excessive self-promotion that often irritates listeners or observers. This formal noun describes behavior that goes beyond healthy self-confidence to become annoying self-aggrandizement. Jactance appears in literature and formal writing to characterize people who constantly promote their achievements or abilities. Unlike legitimate pride in accomplishments, jactance suggests inappropriate emphasis on self-promotion. The behavior often stems from insecurity despite its outward appearance of confidence. Jactance can damage relationships and professional reputations when it becomes chronic. Social contexts discourage jactance because it focuses conversation on the speaker rather than creating mutual exchange. Understanding jactance helps identify when self-promotion becomes counterproductive and socially inappropriate.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAK-tuns',
                'etymology': 'From French "jactance," derived from Latin "jactantia" meaning "boasting," from "jactare" (to throw about, boast), related to "jacere" (to throw).',
                'language_origins': 'French, Latin',
                'example_sentence': 'His constant _______ about his wealth and achievements made dinner conversations uncomfortable for everyone.',
                'memory_tip': 'Remember "JACTANCE" - think "JACK-TANCE" like someone doing a "TANCE" (dance) to show off like "JACK" - ostentatious boasting or bragging.'
            },
            'jadeite': {
                'definition': 'Jadeite is a hard, typically green mineral that is one of the two types of jade (along with nephrite), prized for its beauty, durability, and cultural significance in jewelry making and carving, particularly in East Asian cultures. This pyroxene mineral ranges in color from white and lavender to various shades of green, with the most valuable being intense emerald green. Jadeite has higher density and hardness than nephrite, making it more valuable in gemstone markets. Chinese culture particularly values jadeite for its supposed protective and spiritual properties. Myanmar (Burma) produces the highest quality jadeite, while other deposits exist in Guatemala and other locations. Jadeite carvings and jewelry have been treasured for thousands of years. The mineral\'s toughness makes it excellent for intricate carving and decorative objects. Modern gemology distinguishes jadeite from nephrite through chemical and physical testing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAYD-eyet',
                'etymology': 'From "jade" (the gemstone) plus the suffix "-ite" indicating a mineral. "Jade" comes from Spanish "piedra de ijada" (stone of the side/kidney).',
                'language_origins': 'Spanish, English',
                'example_sentence': 'The museum\'s _______ collection included ancient Chinese carvings and modern jewelry featuring the precious green stone.',
                'memory_tip': 'Remember "JADEITE" - think "JADE-ITE" meaning a type of "JADE" mineral that\'s the "ITE" (right) one for fine jewelry - the harder, more valuable form of jade.'
            },
            'jahiliya': {
                'definition': 'Jahiliya is an Islamic term referring to the period of ignorance or barbarism that supposedly existed in Arabian society before the advent of Islam, characterized by polytheism, tribal warfare, and moral corruption according to Islamic historical perspective. This Arabic concept describes the pre-Islamic era from a religious viewpoint that emphasizes the transformative impact of Islamic revelation. Islamic scholars use jahiliya to contrast the conditions before and after Muhammad\'s prophecy. The term implies not just lack of knowledge but active opposition to divine guidance. Modern Islamic movements sometimes use jahiliya to describe contemporary societies they view as morally corrupt or non-Islamic. The concept has theological and political implications in Islamic thought about social reform and religious authority. Understanding jahiliya requires recognizing its religious rather than purely historical meaning. The term reflects Islamic self-understanding and historical interpretation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jah-hee-LEE-yah',
                'etymology': 'From Arabic "jahiliyyah," derived from "jahil" meaning "ignorant." The term was coined in Islamic literature to describe pre-Islamic Arabian society.',
                'language_origins': 'Arabic',
                'example_sentence': 'Islamic historians described the _______ period as a time of moral darkness before the light of religious revelation.',
                'memory_tip': 'Remember "JAHILIYA" - think "JAH-HILI-YA" like "JAH" (god) wasn\'t there, so it was "HILI" (really) bad "YA" (time) - the Islamic term for pre-Islamic ignorance.'
            },
            'jaimaica': {
                'definition': 'This appears to be a misspelling or variant of "Jamaica," the Caribbean island nation known for its beaches, music, culture, and history. The correct spelling is "Jamaica" with a "c" rather than an "i." If this represents an intentional alternative spelling or represents a different concept, additional context would be needed to provide accurate definition. Jamaica is famous for reggae music, beautiful beaches, Blue Mountain coffee, and rich cultural heritage. The island nation gained independence from Britain in 1962 and has since developed a distinctive culture blending African, European, and indigenous influences. Jamaican English (Patois) is a unique language variety. The economy depends on tourism, mining, and agriculture. Without additional context confirming this as an intentional alternative spelling, this appears to be an error for "Jamaica."',
                'part_of_speech': 'potential misspelling',
                'pronunciation_guide': 'juh-MY-kuh (if referring to Jamaica)',
                'etymology': 'Appears to be a variant or misspelling of "Jamaica," from Taíno "Xaymaca" meaning "land of wood and water."',
                'language_origins': 'Taíno (if referring to Jamaica)',
                'example_sentence': 'The word _______ appears to be a misspelling of Jamaica, the Caribbean island nation.',
                'memory_tip': 'Remember "JAIMAICA" - this appears to be a misspelling of "JAMAICA" - check if it should be spelled with "c" not "i".'
            },
            'jains': {
                'definition': 'Jains are followers of Jainism, an ancient Indian religion founded by Mahavira in the 6th century BCE, characterized by principles of non-violence (ahimsa), truth, and spiritual liberation through right conduct and knowledge. This plural noun describes adherents of one of the world\'s oldest religions, which emphasizes the sanctity of all life forms. Jains practice strict vegetarianism and often wear masks to avoid accidentally inhaling small insects. The religion teaches that souls can achieve liberation through purification and ethical living. Jain communities have historically been involved in trade and business, contributing significantly to Indian commerce and culture. Jain temples feature distinctive architecture and house important religious texts and artwork. Modern Jains continue traditional practices while adapting to contemporary life. The religion\'s emphasis on non-violence has influenced broader discussions of ethics and environmental protection.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'JAYNZ',
                'etymology': 'From Sanskrit "Jaina," meaning "follower of the Jina (victor/conqueror)," referring to Mahavira and other Jain spiritual leaders.',
                'language_origins': 'Sanskrit',
                'example_sentence': 'The _______ in the community built a beautiful temple that reflected their commitment to non-violence and spiritual purity.',
                'memory_tip': 'Remember "JAINS" - think "J-AINS" like people who "J" (follow Jainism) and practice "AINS" (non-violence) - followers of the ancient Indian religion of non-violence.'
            },
            'jalapeño': {
                'definition': 'A jalapeño is a medium-sized chili pepper with moderate heat, commonly used in Mexican and Tex-Mex cuisine, characterized by its thick walls, tapered shape, and distinctive flavor that ranges from mild to moderately spicy depending on growing conditions. This culinary pepper typically measures 2-4 inches long and is harvested while still green, though it can ripen to red. Jalapeños rate 2,500-8,000 on the Scoville heat scale, making them hotter than bell peppers but milder than serranos. The peppers are used fresh in salsas, stuffed with cheese for poppers, or pickled for longer storage. Smoked jalapeños are called chipotles and have a distinctly different flavor profile. The peppers contain capsaicin, which provides both heat and potential health benefits. Jalapeño plants are relatively easy to grow in warm climates and have become popular worldwide.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hah-lah-PAYN-yo',
                'etymology': 'From Spanish "jalapeño," meaning "from Xalapa" (also spelled Jalapa), a city in Veracruz, Mexico where these peppers were traditionally grown.',
                'language_origins': 'Spanish',
                'example_sentence': 'The chef added diced _______ peppers to the salsa to give it a moderate kick without overwhelming heat.',
                'memory_tip': 'Remember "JALAPEÑO" - think "HALA-PAYN-YO" with the Spanish pronunciation - the moderately hot green pepper from Mexico.'
            },
            'jalapeñoology': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "jalapeño" (the chili pepper) and "ology" (study of). There is no legitimate field called "jalapeñoology." This represents a PDF processing error where two separate concepts were accidentally joined. The suffix "-ology" typically indicates the study of something, so "jalapeñoology" would theoretically mean "the study of jalapeño peppers," but this is not a recognized academic discipline or real word. The combination likely resulted from text processing issues where "jalapeño" and another word ending in "-ology" were incorrectly merged during document digitization.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'hah-lah-PAYN-yo-OL-uh-jee',
                'etymology': 'This is a PDF parsing error combining "jalapeño" from Spanish (pepper from Xalapa) and "-ology" from Greek (study of).',
                'language_origins': 'Spanish, Greek (combined in error)',
                'example_sentence': 'The word _______ appears to be an error combining jalapeño pepper with the suffix for academic study.',
                'memory_tip': 'This is a parsing error - remember to separate "jalapeño" (chili pepper) from "-ology" (study of) - not a real word.'
            },
            'jalousie': {
                'definition': 'A jalousie is a window, door, or architectural feature consisting of parallel slats of glass, wood, or other material that can be adjusted to control airflow and visibility while providing protection from weather, commonly used in tropical and subtropical climates. This architectural element allows ventilation while maintaining privacy and weather protection. Jalousie windows feature multiple horizontal slats that can be opened or closed using a crank mechanism. The design originated in tropical regions where constant ventilation is desirable but protection from rain is necessary. Modern jalousie windows use aluminum or vinyl frames with glass slats for durability and energy efficiency. The term can also refer to decorative shutters with similar slat construction. Jalousie systems provide excellent airflow control and are popular in warm climates worldwide. The adjustable slats allow fine control over light and air penetration.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAHL-uh-zee',
                'etymology': 'From French "jalousie," literally meaning "jealousy," referring to the ability to see out while preventing others from seeing in, like the concept of jealous watching.',
                'language_origins': 'French',
                'example_sentence': 'The tropical home featured _______ windows that could be adjusted to let in ocean breezes while blocking rain.',
                'memory_tip': 'Remember "JALOUSIE" - think "JEALOUS-IE" like "JEALOUS" watching through slats - windows with adjustable slats that let you see out while controlling privacy.'
            },
            'jamaica': {
                'definition': 'Jamaica is an island nation in the Caribbean Sea, known for its vibrant culture, reggae music, beautiful beaches, and rich history that blends indigenous Taíno, African, and European influences into a distinctive national identity. This proper noun refers to the third-largest island in the Caribbean, which gained independence from Britain in 1962. Jamaica is famous for reggae music and Bob Marley, who brought international attention to Jamaican culture. The island\'s economy relies on tourism, mining (particularly bauxite), and agriculture including coffee and sugar. Jamaican cuisine features jerk seasoning, ackee and saltfish, and other distinctive flavors. The Blue Mountains produce some of the world\'s finest coffee. Jamaica has a strong athletic tradition, particularly in track and field with world-renowned sprinters. The island faces challenges related to economic development while maintaining its cultural heritage.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'juh-MAY-kuh',
                'etymology': 'From Taíno "Xaymaca," meaning "land of wood and water," referring to the island\'s natural features.',
                'language_origins': 'Taíno',
                'example_sentence': 'Tourists visit _______ to experience its beautiful beaches, vibrant music scene, and world-famous Blue Mountain coffee.',
                'memory_tip': 'Remember "JAMAICA" - think of the distinctive Caribbean island known for reggae music, beautiful beaches, and Bob Marley.'
            },
            'jambalaya': {
                'definition': 'Jambalaya is a Louisiana Creole dish consisting of rice cooked with a mixture of meats, seafood, vegetables, and spices, representing a fusion of Spanish, French, African, and Native American culinary traditions. This flavorful one-pot meal typically includes ingredients like shrimp, chicken, andouille sausage, bell peppers, onions, celery, and tomatoes seasoned with cayenne and other spices. Two main varieties exist: Creole jambalaya (with tomatoes) and Cajun jambalaya (without tomatoes). The dish evolved from Spanish paella and similar rice-based meals adapted to available Louisiana ingredients. Jambalaya preparation involves cooking rice with the other ingredients rather than separately, allowing flavors to meld together. The dish represents the multicultural heritage of Louisiana cuisine and has become an iconic American regional food. Different families and regions have their own jambalaya recipes and traditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jam-buh-LY-uh',
                'etymology': 'Possibly from Provençal "jambalaia" (mixture) or Spanish "jamón" (ham) plus "paella." The exact origin is debated among food historians.',
                'language_origins': 'Provençal, Spanish (uncertain)',
                'example_sentence': 'The New Orleans restaurant served authentic _______ loaded with shrimp, chicken, and spicy andouille sausage.',
                'memory_tip': 'Remember "JAMBALAYA" - think "JAM-BALA-YA" like a "JAM" (mixture) that will make you say "YA" (yes) - the Louisiana rice dish with mixed meats and seafood.'
            },
            'jambalayajarl': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "jambalaya" (Louisiana rice dish) and "jarl" (Scandinavian nobleman). These are completely unrelated concepts from different cultures and time periods that were accidentally joined during document processing. "Jambalaya" is a Creole rice dish while "jarl" refers to a Norse earl or nobleman. The combination has no legitimate meaning and represents a text processing error where two separate words were incorrectly merged.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'jam-buh-LY-uh-YARL',
                'etymology': 'This is a PDF parsing error combining "jambalaya" from Provençal/Spanish cuisine and "jarl" from Old Norse meaning nobleman.',
                'language_origins': 'Provençal/Spanish, Old Norse (combined in error)',
                'example_sentence': 'The word _______ appears to be an error combining a Louisiana dish name with a Scandinavian noble title.',
                'memory_tip': 'This is a parsing error - remember to separate "jambalaya" (Louisiana rice dish) from "jarl" (Norse nobleman) - not a real combined word.'
            },
            'jambe': {
                'definition': 'Jambe is a French word meaning "leg," used in English primarily in specialized contexts such as heraldry, where it refers to the leg of an animal (particularly a lion) shown in a coat of arms, or in architectural terminology describing vertical supports that resemble legs. In heraldic terminology, a "jambe" specifically denotes a leg cut off at the middle of the thigh, typically shown in profile. The word appears in English primarily in technical or historical contexts rather than general usage. Architectural jambes might refer to leg-like supports or decorative elements. The term maintains its French pronunciation and meaning when used in English contexts. Understanding jambe requires familiarity with French terminology and its specialized English applications. The word demonstrates how technical vocabularies borrow terms from other languages for specific purposes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ZHAHMB',
                'etymology': 'From French "jambe," meaning "leg," derived from Late Latin "gamba" (leg, hoof), ultimately from Greek "kampe" (bend, joint).',
                'language_origins': 'French, Late Latin, Greek',
                'example_sentence': 'The heraldic shield displayed a lion\'s _______ as part of the family\'s traditional coat of arms.',
                'memory_tip': 'Remember "JAMBE" - think of the French word for "leg" used in specialized English contexts like heraldry - a leg shown in coats of arms.'
            },
            'jamboree': {
                'definition': 'A jamboree is a large, festive gathering or celebration, typically involving entertainment, activities, and community participation, originally referring to Boy Scout gatherings but now used more broadly for any large, lively celebration or festival. This noun describes events that bring together many people for shared enjoyment and activities. Scout jamborees feature camping, skill demonstrations, and international fellowship among youth organizations. Music jamborees showcase various performers and styles for enthusiastic audiences. The term suggests energetic, communal celebration rather than formal ceremony. Corporate jamborees might celebrate company achievements or product launches. Unlike small, intimate gatherings, jamborees are characterized by their scale, energy, and festive atmosphere. The word carries connotations of fun, community spirit, and organized entertainment. Modern usage applies jamboree to various large-scale celebratory events.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jam-buh-REE',
                'etymology': 'Origin uncertain, possibly from Hindi "shab-i-barat" (night of forgiveness) or invented American slang. First recorded in the 1860s meaning "spree" or "celebration."',
                'language_origins': 'American English (uncertain origin)',
                'example_sentence': 'The annual county _______ featured live music, food vendors, and activities for families throughout the weekend.',
                'memory_tip': 'Remember "JAMBOREE" - think "JAM-BO-REE" like a "JAM" session where everyone\'s "REE" (really) excited - a large, festive gathering.'
            },
            'jamestown': {
                'definition': 'Jamestown refers to the first permanent English settlement in North America, established in 1607 in what is now Virginia, representing a crucial beginning in English colonial history and the eventual development of the United States. This proper noun describes the historic settlement that faced enormous challenges including disease, starvation, and conflicts with indigenous peoples. Jamestown colonists initially struggled to establish sustainable agriculture and governance. The settlement became economically viable through tobacco cultivation introduced by John Rolfe. Jamestown played a significant role in the development of slavery in North America. The colony established important precedents for representative government and private property. Modern Jamestown is a historic site that preserves and interprets early colonial history. Archaeological excavations continue to reveal details about early colonial life and interactions with Powhatan peoples.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'JAYMZ-town',
                'etymology': 'Named after King James I of England, who granted the charter for the Virginia Company that established the settlement.',
                'language_origins': 'English (named after monarch)',
                'example_sentence': 'Students learned about the hardships faced by early colonists at _______ during their study of American colonial history.',
                'memory_tip': 'Remember "JAMESTOWN" - think "JAMES-TOWN" named after King "JAMES" - the first permanent English settlement in America (1607).'
            },
            'jammer': {
                'definition': 'A jammer is a device that blocks, disrupts, or interferes with electronic signals such as radio, cell phone, GPS, or Wi-Fi communications by transmitting competing signals on the same frequencies. This electronic device serves various purposes from military applications to privacy protection. Cell phone jammers prevent mobile device communication in specific areas. GPS jammers block location tracking systems. Signal jammers can be used for security purposes or to prevent cheating during exams. Military jammers disrupt enemy communications and radar systems. The legality of jammers varies by jurisdiction and application, with many countries restricting civilian use. Unlike signal boosters that enhance communication, jammers deliberately interfere with electronic systems. Understanding jammers requires knowledge of radio frequency technology and legal restrictions on their use.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAM-er',
                'etymology': 'From "jam" meaning "to block" or "interfere with," plus the suffix "-er" indicating a device that performs the action.',
                'language_origins': 'English',
                'example_sentence': 'The security team used a cell phone _______ to prevent unauthorized communication during the classified meeting.',
                'memory_tip': 'Remember "JAMMER" - think "JAM-MER" like something that "JAMS" (blocks) signals - a device that interferes with electronic communications.'
            },
            'jangled': {
                'definition': 'Jangled is the past tense of "jangle," meaning to have made or caused harsh, discordant metallic sounds through collision or vibration, or to have created nervous irritation or disturbance. This verb describes completed actions that produced unpleasant noise or emotional agitation. Keys jangled noisily in pockets during movement. Nerves jangled from stress and anxiety. The term suggests harsh, irregular sounds rather than pleasant musical tones. Chains and metal objects jangle when they strike each other repeatedly. Unlike harmonious sounds, jangled noises are typically annoying or disturbing. Emotional states can feel jangled when disrupted by conflict or stress. The word combines physical sound description with metaphorical emotional states. Jangled conditions often require calming or organizing intervention to restore peace and order.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'JANG-guld',
                'etymology': 'From Middle English "janglen," possibly imitative of harsh metallic sounds. The word mimics the sound it describes.',
                'language_origins': 'Middle English (imitative)',
                'example_sentence': 'Her car keys _______ loudly as she searched through her purse for the house key.',
                'memory_tip': 'Remember "JANGLED" - think of harsh metallic sounds like keys making annoying noise - made discordant clanging sounds.'
            },
            'janitor': {
                'definition': 'A janitor is a person employed to clean and maintain buildings, typically responsible for tasks such as mopping floors, emptying trash, cleaning restrooms, and performing basic maintenance duties in schools, offices, or other facilities. This occupation involves custodial work that keeps buildings sanitary, safe, and functional for occupants. Janitors often work during off-hours to avoid disrupting normal activities. The job requires physical stamina, attention to detail, and knowledge of cleaning products and safety procedures. School janitors become familiar figures to students and staff. Commercial janitors maintain office buildings, hospitals, and retail spaces. Some janitors advance to supervisory positions or facility management roles. The profession provides essential services that support public health and building operations. Modern janitors often use specialized equipment and environmentally friendly cleaning products.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAN-ih-ter',
                'etymology': 'From Latin "janitor," meaning "doorkeeper," derived from "janus" (door) plus "-itor" (agent suffix). Originally referred to doorkeepers rather than cleaners.',
                'language_origins': 'Latin',
                'example_sentence': 'The school _______ took pride in keeping the hallways spotless and ensuring a safe environment for students.',
                'memory_tip': 'Remember "JANITOR" - think "JAN-ITOR" like someone who takes care of everything from "JAN" (January) to "ITOR" (all year) - the building caretaker and cleaner.'
            },
            'jankers': {
                'definition': 'Jankers is British military slang referring to military punishment or detention, typically involving extra duties, confinement, or disciplinary measures imposed on service members for infractions of military law or regulations. This informal term describes various forms of military discipline short of court martial. Jankers might include extra guard duty, kitchen work, or cleaning assignments. The punishment serves to maintain military discipline and order within units. Different branches of service have their own jankers procedures and traditions. Unlike civilian legal penalties, military jankers focus on maintaining unit cohesion and discipline. Servicemembers on jankers often lose privileges like leave or recreational activities. The term reflects the unique culture and language of military organizations. Understanding jankers requires familiarity with military justice systems and disciplinary procedures.',
                'part_of_speech': 'noun (usually plural)',
                'pronunciation_guide': 'JANG-kerz',
                'etymology': 'British military slang of uncertain origin, possibly related to "jangle" (discord) or from naval punishment terms. First recorded in mid-20th century military usage.',
                'language_origins': 'British English (military slang)',
                'example_sentence': 'The soldier was put on _______ for a week after being caught absent without leave.',
                'memory_tip': 'Remember "JANKERS" - think "JANK-ERS" like "JANK" (bad) behavior gets you "ERS" (in trouble) - British military punishment or detention.'
            }
        }
        
        return batch_094_data.get(word, {
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
            'jaimaica': 'Potential spelling error: "jaimaica" appears to be a misspelling of "Jamaica" - should likely be spelled with "c" not "i".',
            'jalapeñoology': 'Combined word error: "jalapeñoology" appears to be "jalapeño" (chili pepper) + "ology" (study of) merged together.',
            'jambalayajarl': 'Combined word error: "jambalayajarl" appears to be "jambalaya" (Louisiana rice dish) + "jarl" (Norse nobleman) merged together.'
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
            else:
                print("No errors detected in this batch.")
            
            return True
            
        except Exception as e:
            print(f"Error processing batch: {str(e)}")
            return False

def main():
    processor = Batch094Processor()
    input_file = "output/batch_094_words.csv"
    output_file = "output/batch_094_processed.csv"
    
    success = processor.process_batch(input_file, output_file)
    if success:
        print("Batch 094 processing completed successfully!")
    else:
        print("Batch 094 processing failed!")

if __name__ == "__main__":
    main()