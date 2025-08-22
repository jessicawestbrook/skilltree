import csv
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_difficulty_score(phonetic_transparency, frequency, morphological_complexity, etymology_complexity):
    """Calculate overall difficulty score from 4 factors"""
    return round((phonetic_transparency + frequency + morphological_complexity + etymology_complexity) / 4, 1)

def determine_difficulty_level(score):
    """Determine difficulty level based on score"""
    if score <= 2.0:
        return "Elementary"
    elif score <= 3.0:
        return "Intermediate" 
    elif score <= 4.0:
        return "Advanced"
    else:
        return "Expert"

def main():
    logging.info("Processing Batch 187 with comprehensive Claude data...")
    
    # Combined word errors detected in batch 187
    combined_errors = ['universalv', 'univocalavarice', 'upsilonsakura', 'urgencybifurcate']
    
    # Comprehensive spelling bee data with Claude-generated educational content
    words_data = [
        {
            'word': 'university',
            'pronunciation': '/ˌjuːnɪˈvɜːrsəti/',
            'definition': 'A university is an institution of higher education and research that awards academic degrees in various academic disciplines. Universities typically consist of multiple colleges or schools offering undergraduate and graduate programs. They serve as centers of learning, research, and knowledge creation, employing professors who both teach students and conduct scholarly research. Universities play crucial roles in advancing human knowledge, training professionals, and contributing to societal development through education and innovation.',
            'example_sentence': 'She applied to several prestigious _____ programs to pursue her doctoral degree in biology.',
            'etymology': 'From Old French "université," from Latin "universitas" meaning "the whole, totality," later "corporation of teachers and students."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNIVERSE + ITY" - a university contains a universe of knowledge and learning opportunities.',
            'phonetic_transparency': 2,
            'frequency': 5,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'univocal',
            'pronunciation': '/juːˈnɪvəkəl/',
            'definition': 'Univocal means having only one meaning; unambiguous or expressing only one possible interpretation. In logic and philosophy, univocal terms are those that have the same meaning in all contexts where they are used, as opposed to equivocal terms that can have multiple meanings. Univocal language is precise and clear, leaving no room for misinterpretation. The term is important in technical writing, legal documents, and scholarly discourse where precision is essential.',
            'example_sentence': 'The scientist chose _____ terminology to ensure her research findings could not be misinterpreted.',
            'etymology': 'From Latin "univocus," from "unus" (one) + "vox" (voice). Literally means "having one voice" or "speaking with one meaning."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNI (one) + VOCAL" - univocal means speaking with one clear voice and meaning.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'unkempt',
            'pronunciation': '/ʌnˈkɛmpt/',
            'definition': 'Unkempt describes someone or something that appears untidy, disheveled, or not properly groomed or maintained. It refers to hair that hasn\'t been combed, clothing that\'s wrinkled or messy, or general appearance that looks neglected or careless. Unkempt can also describe places, gardens, or objects that haven\'t been properly cared for or organized. The word suggests a lack of attention to tidiness or proper maintenance.',
            'example_sentence': 'After camping for a week, his _____ appearance made him barely recognizable.',
            'etymology': 'From "un-" (not) + "kempt" (past participle of obsolete "kemb," meaning "to comb"). Literally means "not combed."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + KEMPT (kept neat)" - unkempt means not kept neat and tidy.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'unlike',
            'pronunciation': '/ʌnˈlaɪk/',
            'definition': 'Unlike means different from or not similar to something else. As a preposition, it introduces a comparison showing how one thing differs from another. Unlike can also be an adjective meaning dissimilar or not alike. The word emphasizes contrast and differences rather than similarities. It\'s commonly used to highlight distinctions between people, things, situations, or ideas.',
            'example_sentence': '_____ her quiet sister, Maria was always the center of attention.',
            'etymology': 'From "un-" (not) + "like." "Like" comes from Old English "lic" meaning "body, form," later developing the sense of similarity.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + LIKE" - unlike means not like or similar to something else.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'unmoored',
            'pronunciation': '/ʌnˈmʊrd/',
            'definition': 'Unmoored literally means released from moorings or anchor points, allowing a boat or ship to drift freely. Figuratively, it describes someone who feels disconnected, unstable, or lacking direction in life. When someone is unmoored, they may feel lost, without anchor points of stability such as family, career, or beliefs. The word suggests a state of drift, uncertainty, or disconnection from stabilizing forces.',
            'example_sentence': 'After retiring, he felt _____ and struggled to find new purpose in his daily routine.',
            'etymology': 'From "un-" (reverse action) + "moored." "Moor" comes from Middle English, meaning "to secure a ship with cables."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + MOORED" - unmoored means no longer tied down securely, drifting freely.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'unnoticed',
            'pronunciation': '/ʌnˈnoʊtɪst/',
            'definition': 'Unnoticed means not observed, perceived, or given attention; going without being seen or recognized. It describes things that escape attention, either intentionally or accidentally. Something unnoticed fails to attract notice or interest from others. This can refer to actions, changes, people, or events that occur without drawing attention or acknowledgment from observers.',
            'example_sentence': 'Her small acts of kindness often went _____ by those around her.',
            'etymology': 'From "un-" (not) + "noticed," past participle of "notice." "Notice" comes from Latin "notitia" meaning "knowledge."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + NOTICED" - unnoticed things haven\'t been noticed or seen by anyone.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'unremitting',
            'pronunciation': '/ˌʌnrɪˈmɪtɪŋ/',
            'definition': 'Unremitting means never stopping, slackening, or relenting; constant and persistent without interruption. It describes actions, conditions, or efforts that continue without pause or relief. Unremitting often carries intense connotations, suggesting something that is relentless and sometimes overwhelming. The word can describe both positive qualities (like unremitting dedication) and negative ones (like unremitting pain).',
            'example_sentence': 'Despite his _____ efforts to find a solution, the problem remained unsolved.',
            'etymology': 'From "un-" (not) + "remitting." "Remit" comes from Latin "remittere" meaning "to send back, relax, forgive."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + REMITTING (giving up)" - unremitting means never giving up or taking a break.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'unscathed',
            'pronunciation': '/ʌnˈskeɪðd/',
            'definition': 'Unscathed means without suffering any injury, damage, or harm; completely unharmed or uninjured. It describes someone or something that has emerged from a dangerous, difficult, or potentially damaging situation without negative consequences. Unscathed often implies that harm was expected or possible but did not occur. The word suggests both physical and metaphorical protection from damage.',
            'example_sentence': 'Amazingly, the driver walked away from the car accident completely _____.',
            'etymology': 'From "un-" (not) + "scathed." "Scathe" comes from Old Norse "skaða" meaning "to injure, damage."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + SCATHED (scratched)" - unscathed means not even scratched or harmed.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'unscramble',
            'pronunciation': '/ʌnˈskræmbəl/',
            'definition': 'Unscramble means to restore order to something that has been mixed up, confused, or jumbled; to decode or decipher. It commonly refers to rearranging letters to form words, solving word puzzles, or clarifying confused information. Unscrambling involves organizing elements into their correct or meaningful arrangement. The word can also apply to untangling complex situations or clarifying confused communications.',
            'example_sentence': 'The students had to _____ the letters to spell the vocabulary words correctly.',
            'etymology': 'From "un-" (reverse action) + "scramble." "Scramble" originally meant "to climb awkwardly," later "to mix together confusedly."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + SCRAMBLE" - to unscramble is to undo the scrambling and put things back in order.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'unsportsmanlike',
            'pronunciation': '/ʌnˈspɔːrtsmənˌlaɪk/',
            'definition': 'Unsportsmanlike describes behavior that violates the principles of fair play, respect, and integrity expected in sports or competitive activities. It includes actions such as cheating, showing poor attitude toward opponents or officials, or displaying bad sportsmanship. Unsportsmanlike conduct can result in penalties or ejection from games. The term extends beyond sports to describe any behavior that lacks fairness, respect, or ethical standards in competitive situations.',
            'example_sentence': 'The player received a penalty for his _____ conduct toward the referee.',
            'etymology': 'From "un-" (not) + "sportsmanlike." "Sportsman" combines "sport" + "man," with "-like" indicating similarity to the ideal behavior.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + SPORTSMAN + LIKE" - unsportsmanlike means not behaving like a good sportsman should.',
            'phonetic_transparency': 4,
            'frequency': 2,
            'morphological_complexity': 5,
            'etymology_complexity': 2
        },
        {
            'word': 'unsullied',
            'pronunciation': '/ʌnˈsʌlid/',
            'definition': 'Unsullied means not damaged or made impure; clean, spotless, or untainted. It can refer to physical cleanliness or moral purity. Something unsullied has not been corrupted, stained, or compromised in any way. The word often describes reputations, characters, or records that remain pure and unblemished. Unsullied suggests both literal cleanliness and figurative innocence or integrity.',
            'example_sentence': 'Despite the scandal surrounding the company, her reputation remained completely _____.',
            'etymology': 'From "un-" (not) + "sullied." "Sully" comes from French "souiller" meaning "to soil, stain."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + SULLIED (soiled)" - unsullied means not soiled, stained, or corrupted.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'untenable',
            'pronunciation': '/ʌnˈtɛnəbəl/',
            'definition': 'Untenable means not able to be maintained, defended, or justified; not sustainable or supportable. It describes positions, arguments, or situations that cannot be successfully upheld when challenged or examined. An untenable position lacks logical foundation or practical viability. The word often refers to arguments that collapse under scrutiny or situations that cannot continue due to inherent contradictions or impossibilities.',
            'example_sentence': 'As more evidence emerged, his claim of innocence became completely _____.',
            'etymology': 'From "un-" (not) + "tenable." "Tenable" comes from French "tenir" meaning "to hold," from Latin "tenere."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + TENABLE (holdable)" - untenable positions cannot be held or defended successfully.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'until',
            'pronunciation': '/ʌnˈtɪl/',
            'definition': 'Until is a preposition or conjunction indicating the point in time at which something ends or changes. It expresses duration up to a specific moment or event. Until can indicate both temporal boundaries (time limits) and conditional boundaries (circumstances that must occur). The word establishes the endpoint of an action, state, or condition, showing when something will cease or change.',
            'example_sentence': 'She waited _____ midnight before calling her friend.',
            'etymology': 'From Middle English, combining "unto" + "till." "Till" comes from Old Norse "til" meaning "to, until."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + TILL" - until means up to the point when something happens, like tilling soil until it\'s ready.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'untoward',
            'pronunciation': '/ʌnˈtɔːrd/',
            'definition': 'Untoward means inappropriate, improper, or causing difficulty or annoyance. It describes behavior, events, or circumstances that are inconvenient, troublesome, or socially inappropriate. Untoward can refer to actions that violate social norms or create unwanted complications. The word often implies that something is not just wrong but also creates problems or discomfort for others.',
            'example_sentence': 'Nothing _____ happened during the diplomatic meeting between the two countries.',
            'etymology': 'From "un-" (not) + "toward." Originally meant "not moving in the right direction," later "not proper or appropriate."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + TOWARD (in the right direction)" - untoward means not going in the right direction or being inappropriate.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'unusual',
            'pronunciation': '/ʌnˈjuːʒuəl/',
            'definition': 'Unusual means not commonly occurring, done, or experienced; remarkable or noteworthy for being different from what is normal or expected. It describes things that deviate from typical patterns or standards. Unusual can be positive (unusually talented) or negative (unusually difficult), but always indicates departure from the norm. The word highlights the distinctive or exceptional nature of something.',
            'example_sentence': 'The weather has been _____ this winter, with temperatures much warmer than normal.',
            'etymology': 'From "un-" (not) + "usual." "Usual" comes from Latin "usualis" meaning "customary," from "usus" (use).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + USUAL" - unusual means not usual or typical for the situation.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'unwonted',
            'pronunciation': '/ʌnˈwʌntɪd/',
            'definition': 'Unwonted means unusual or uncharacteristic, particularly referring to behavior or circumstances that deviate from someone\'s normal patterns. It describes actions or situations that are not customary or habitual for a particular person or context. Unwonted behavior often surprises others because it\'s unexpected based on previous patterns. The word emphasizes deviation from established habits or typical conduct.',
            'example_sentence': 'His _____ silence during the meeting made everyone wonder what was troubling him.',
            'etymology': 'From "un-" (not) + "wonted" (accustomed). "Wont" comes from Old English "wunod," past participle of "wunian" (to dwell, be accustomed).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + WONTED (wanted/accustomed)" - unwonted means not what you\'re accustomed to expecting.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'upanisads',
            'pronunciation': '/uːˈpænɪʃædz/',
            'definition': 'Upanisads (also spelled Upanishads) are ancient Hindu scriptures that form the philosophical foundation of Hinduism. These texts, composed between 800-200 BCE, explore fundamental questions about the nature of reality, consciousness, and the relationship between the individual soul (atman) and universal consciousness (Brahman). The Upanisads contain teachings traditionally passed from teacher to student, emphasizing meditation, self-inquiry, and spiritual wisdom. They represent the culmination of Vedic thought and deeply influence Hindu philosophy.',
            'example_sentence': 'The philosophy student spent months studying the _____ to understand ancient Hindu concepts of consciousness.',
            'etymology': 'From Sanskrit "upanishad," from "upa" (near) + "ni" (down) + "shad" (to sit), literally meaning "sitting down near" a teacher to receive instruction.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP (near) + ANISADS" - Upanisads are about sitting up close to a teacher to learn wisdom.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'upanishads',
            'pronunciation': '/uːˈpænɪʃædz/',
            'definition': 'Upanishads are the same as Upanisads - ancient Hindu philosophical texts that form part of the Vedic literature. This is the more common modern spelling of these sacred scriptures. The Upanishads explore profound philosophical concepts including the nature of reality, the self, and ultimate truth. They contain dialogues between teachers and students, parables, and philosophical discussions that have influenced Hindu thought for over two millennia. The teachings emphasize direct experience of truth through meditation and self-realization.',
            'example_sentence': 'Many Western philosophers have drawn inspiration from the wisdom found in the _____.',
            'etymology': 'From Sanskrit "upanishad," meaning "sitting down near" a teacher. This represents the standard modern English spelling of the same word.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + ANISHADS" - same as Upanisads but with the more familiar "-shads" ending.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'upbeat',
            'pronunciation': '/ˈʌpˌbit/',
            'definition': 'Upbeat means optimistic, cheerful, and positive in attitude or outlook. It describes a mood or demeanor that is energetic and hopeful rather than pessimistic or depressed. In music, upbeat refers to the unaccented beat that precedes the downbeat, but in general usage, it characterizes anything that lifts spirits or promotes positive feelings. Upbeat can describe people, music, news, or situations that inspire confidence and good feelings.',
            'example_sentence': 'Despite the setbacks, she maintained an _____ attitude about the project\'s success.',
            'etymology': 'From music terminology: "up" + "beat." Originally referred to the conductor\'s upward gesture before the strong beat, later extended to mean "optimistic."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + BEAT" - upbeat means your spirits are up and your heart beats with positive energy.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'upbraid',
            'pronunciation': '/ʌpˈbreɪd/',
            'definition': 'Upbraid means to criticize or scold someone severely, often for their faults or wrongdoing. It involves expressing strong disapproval or reproach, typically in a harsh or angry manner. Upbraiding goes beyond simple criticism to include elements of moral condemnation or angry rebuke. The word suggests both the intensity of the criticism and the fault or blame being assigned to the person being upbraided.',
            'example_sentence': 'The teacher chose to _____ the student privately rather than embarrass him in front of the class.',
            'etymology': 'From Old English "upbregdan," from "up" + "bregdan" (to move quickly, draw). Originally meant "to bring up suddenly" as an accusation.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + BRAID" - to upbraid is to lift up harsh words and braid them into criticism.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'updo',
            'pronunciation': '/ˈʌpˌduː/',
            'definition': 'An updo is a hairstyle where the hair is arranged and secured up on the head rather than hanging down. Updos can range from simple ponytails and buns to elaborate formal arrangements with twists, braids, and decorative elements. These hairstyles are popular for special occasions, professional settings, or practical situations where hair needs to be kept out of the way. Updos can be elegant, casual, or artistic depending on the technique and occasion.',
            'example_sentence': 'She chose an elegant _____ for the wedding to complement her formal dress.',
            'etymology': 'Compound of "up" + "do" (hairstyle). "Do" as slang for hairstyle emerged in the mid-20th century.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + DO" - an updo is literally a hairdo that\'s done up on top of your head.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 1
        },
        {
            'word': 'upholstery',
            'pronunciation': '/ʌpˈhoʊlstəri/',
            'definition': 'Upholstery refers to the soft furnishings, including fabric, padding, and springs, used to cover furniture such as chairs, sofas, and seats. It also describes the craft or business of providing furniture with these coverings. Upholstery includes both the materials used (fabrics, leather, padding, webbing) and the skilled work of measuring, cutting, and attaching these materials to furniture frames. Quality upholstery combines comfort, durability, and aesthetic appeal.',
            'example_sentence': 'The antique chair needed new _____ to restore its original beauty and comfort.',
            'etymology': 'From "upholster" + "-y." "Upholster" comes from "uphold" + "-ster," originally meaning "one who repairs or provides goods."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + HOLSTER + Y" - upholstery holds up the comfort and appearance of furniture.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'uplift',
            'pronunciation': '/ˈʌpˌlɪft/',
            'definition': 'Uplift means to raise or elevate something physically, emotionally, or spiritually. As a verb, it can mean literally lifting something up or figuratively improving someone\'s mood, spirits, or moral condition. As a noun, uplift refers to an act of raising or the feeling of being elevated or inspired. The word often carries positive connotations of improvement, encouragement, and spiritual or emotional enhancement.',
            'example_sentence': 'The inspiring speech was designed to _____ the spirits of the struggling community.',
            'etymology': 'Compound of "up" + "lift." Both elements are from Old English, creating a word that literally means "to lift upward."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + LIFT" - to uplift is to lift someone\'s spirits up from a low point.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 1
        },
        {
            'word': 'upon',
            'pronunciation': '/əˈpɑːn/',
            'definition': 'Upon is a preposition meaning on top of, in contact with the surface of, or at the time of. It\'s often used interchangeably with "on" but tends to be more formal or literary. Upon can indicate physical position (upon the table), time (upon arrival), or dependency (upon reflection). The word often appears in formal writing, legal documents, and literary contexts where a more elevated tone is desired.',
            'example_sentence': '_____ hearing the news, she immediately called her family.',
            'etymology': 'From Middle English, combining "up" + "on." The compound form emphasizes the sense of being elevated or positioned above.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + ON" - upon means up on top of something, either physically or in time.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'uppercut',
            'pronunciation': '/ˈʌpərˌkʌt/',
            'definition': 'An uppercut is a boxing punch delivered upward with a bent arm, typically aimed at an opponent\'s chin or solar plexus. This punch starts low and travels upward in an arc, using the boxer\'s legs and core for power. Uppercuts are effective at close range and can be devastating when they connect cleanly. The term has also extended metaphorically to describe any action that catches someone off guard from an unexpected angle.',
            'example_sentence': 'The boxer\'s powerful _____ caught his opponent completely off guard.',
            'etymology': 'Compound of "upper" + "cut." "Cut" in boxing refers to a sharp, quick punch, while "upper" indicates the upward direction.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UPPER + CUT" - an uppercut is a punch that cuts upward toward the opponent\'s chin.',
            'phonetic_transparency': 4,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'upright',
            'pronunciation': '/ˈʌpˌraɪt/',
            'definition': 'Upright means vertical, erect, or standing straight up rather than lying down or leaning. It can describe physical position or, figuratively, moral character that is honest, honorable, and ethical. An upright person maintains high moral standards and acts with integrity. The word can be used as an adjective (upright posture), adverb (standing upright), or noun (the wooden uprights of a fence).',
            'example_sentence': 'Despite the corruption around him, he remained an _____ and honest public servant.',
            'etymology': 'Compound of "up" + "right." Combines the sense of vertical positioning with correctness or righteousness.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + RIGHT" - upright means both standing up and doing right morally.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 1
        },
        {
            'word': 'uproar',
            'pronunciation': '/ˈʌpˌrɔːr/',
            'definition': 'Uproar means a loud and confused noise, especially from a crowd of people; a state of commotion, excitement, or violent disturbance. It describes situations where there\'s intense excitement, anger, or protest that creates chaos and loud noise. Uproar can refer to both literal noise (shouting crowds) and figurative disturbance (public controversy). The word suggests disorder, intensity, and widespread agitation.',
            'example_sentence': 'The controversial decision caused an _____ among the fans in the stadium.',
            'etymology': 'From Dutch "oproer," from "op" (up) + "roer" (motion, stir). Originally meant "uprising" or "rebellion."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + ROAR" - uproar is when noise and emotions roar up to create chaos.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'upset',
            'pronunciation': '/ʌpˈsɛt/',
            'definition': 'Upset means to disturb the composure of someone, making them unhappy, disappointed, or worried. It can also mean to disrupt, overturn, or disturb the normal state of something. As an adjective, upset describes someone who is distressed or agitated. As a noun, it refers to an unexpected result or a state of disturbance. The word encompasses both emotional disturbance and physical disruption.',
            'example_sentence': 'The sudden change in plans really _____ her carefully organized schedule.',
            'etymology': 'From "up" + "set." Originally meant "to set up," but later developed the sense of "to overturn" and then "to disturb emotionally."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + SET" - to upset is to turn up or disturb what was previously set in place.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'upshot',
            'pronunciation': '/ˈʌpˌʃɑːt/',
            'definition': 'Upshot means the final result, conclusion, or outcome of a sequence of events. It refers to the ultimate consequence or end result of a situation, discussion, or series of actions. The upshot is what finally happens after all factors have been considered and all events have played out. The word emphasizes the finality and significance of the conclusion reached.',
            'example_sentence': 'The _____ of the long negotiations was a compromise that satisfied both parties.',
            'etymology': 'From archery: "up" + "shot." Originally referred to the final shot in an archery contest, which determined the winner.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + SHOT" - the upshot is like the final shot that goes up and determines the outcome.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'upsilon',
            'pronunciation': '/ˈʌpsɪlɑːn/',
            'definition': 'Upsilon is the 20th letter of the Greek alphabet (Υ, υ), corresponding to the Latin "Y." In ancient Greek, it represented a high front rounded vowel sound. Upsilon appears in many scientific and mathematical contexts, often used as a symbol in physics, mathematics, and other technical fields. The letter has historical significance in the development of the Latin alphabet and continues to be used in modern Greek and academic notation.',
            'example_sentence': 'The physics equation included the Greek letter _____ to represent the velocity parameter.',
            'etymology': 'From Greek "upsilon," literally meaning "simple u" or "bare u," from "u" + "psilos" (bare, simple). Distinguished it from other vowel sounds.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UP + SILON" - upsilon looks like a "Y" that goes up with two branches.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'urad',
            'pronunciation': '/ˈʊræd/',
            'definition': 'Urad is a type of black lentil (Vigna mungo) widely used in South Asian cuisine, particularly in Indian cooking. Also known as black gram or black lentil, urad is rich in protein and is used to make various dishes including dal (lentil curry), dosa (fermented crepes), and idli (steamed cakes). The lentils can be used whole with their black skin or split and dehusked to reveal the white interior. Urad is valued for its nutritional content and distinctive earthy flavor.',
            'example_sentence': 'The traditional South Indian breakfast included dosa made from fermented _____ and rice batter.',
            'etymology': 'From Hindi "urad," ultimately from Sanskrit "mudga." The word entered English through Indian cuisine terminology.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YOU + RAD" - urad lentils are rad (cool) and good for you nutritionally.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'uraeus',
            'pronunciation': '/jʊˈriːəs/',
            'definition': 'A uraeus is the stylized representation of a cobra found on the crowns and headdresses of ancient Egyptian pharaohs and deities. This sacred symbol represented the cobra goddess Wadjet, protector of Lower Egypt, and was believed to spit fire at the pharaoh\'s enemies. The uraeus was a symbol of royal power, divine authority, and protection. Archaeological examples show the uraeus prominently displayed on famous artifacts like King Tutankhamun\'s burial mask.',
            'example_sentence': 'The museum\'s Egyptian collection featured a golden mask adorned with a prominent _____.',
            'etymology': 'From Greek "ouraios," from Egyptian "iaret" meaning "she who rears up," referring to the cobra\'s defensive posture.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YOUR + AEUS" - the uraeus was your protection if you were an Egyptian pharaoh.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 4
        },
        {
            'word': 'uranium',
            'pronunciation': '/jʊˈreɪniəm/',
            'definition': 'Uranium is a radioactive metallic chemical element with atomic number 92, used as fuel in nuclear reactors and in nuclear weapons. It\'s the heaviest naturally occurring element and was discovered in 1789. Uranium undergoes radioactive decay and can be enriched to increase the concentration of the fissile isotope uranium-235. The element has both peaceful applications in nuclear power generation and military applications in weapons. Natural uranium is found in many rocks and minerals.',
            'example_sentence': 'The nuclear power plant required enriched _____ to fuel its reactors safely.',
            'etymology': 'Named after the planet Uranus by German chemist Martin Heinrich Klaproth in 1789, following the recent discovery of the planet.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "URAN (Uranus) + IUM" - uranium was named after the planet Uranus.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'urbanely',
            'pronunciation': '/ˈɜːrbənli/',
            'definition': 'Urbanely means in a manner that is courteous, refined, and sophisticated; displaying polish and suavity characteristic of city dwellers. It describes behavior that is smooth, elegant, and worldly, often with an implication of being well-educated and culturally aware. Someone who acts urbanely demonstrates social grace, wit, and refinement in their interactions. The word suggests the cultivated manners associated with cosmopolitan city life.',
            'example_sentence': 'He _____ deflected the criticism with wit and charm during the interview.',
            'etymology': 'From "urbane" + "-ly." "Urbane" comes from Latin "urbanus" meaning "of the city," implying the refinement associated with city life.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "URBAN + ELY" - urbanely means behaving with the sophisticated manners of urban city dwellers.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'urchins',
            'pronunciation': '/ˈɜːrtʃɪnz/',
            'definition': 'Urchins can refer to sea urchins (spiny marine animals) or, historically, to mischievous children, especially poor or homeless ones. Sea urchins are globe-shaped creatures covered in protective spines, found in oceans worldwide. As a term for children, urchins suggests small, often raggedly dressed kids who are street-smart and mischievous. The word can be endearing when referring to playful children or descriptive when discussing the marine animals.',
            'example_sentence': 'The tide pools were filled with colorful sea _____ clinging to the rocks.',
            'etymology': 'From Old French "herichon" (hedgehog), later applied to sea urchins for their spines and to children for their supposedly hedgehog-like scruffiness.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "OUCH + INS" - urchins (sea urchins) can make you say "ouch" if you step on their spines.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'urgency',
            'pronunciation': '/ˈɜːrdʒənsi/',
            'definition': 'Urgency refers to the quality of requiring immediate action or attention; the state of being urgent. It describes situations, needs, or matters that demand prompt response due to their critical nature or time-sensitive requirements. Urgency implies that delay could result in negative consequences. The word encompasses both the objective reality of time constraints and the subjective feeling of pressure to act quickly.',
            'example_sentence': 'The _____ of the medical situation required the helicopter to transport the patient immediately.',
            'etymology': 'From "urgent" + "-cy." "Urgent" comes from Latin "urgere" meaning "to press, push, drive."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "URGE + N + CY" - urgency is when circumstances urge you to act with great necessity.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'ursine',
            'pronunciation': '/ˈɜːrsaɪn/',
            'definition': 'Ursine means relating to or resembling bears. This adjective describes characteristics, behaviors, or appearance that are bear-like. Ursine can refer to physical traits (ursine strength), behavioral patterns (ursine hibernation), or anything else connected to bears. The term is used in zoology, literature, and general description when making comparisons to bear characteristics. It\'s a formal or scientific way to describe bear-related qualities.',
            'example_sentence': 'The large man\'s _____ build and shambling gait reminded everyone of a friendly bear.',
            'etymology': 'From Latin "ursinus," from "ursus" meaning "bear." Related to the constellation names Ursa Major and Ursa Minor (Great Bear, Little Bear).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "URSA (bear constellation) + INE" - ursine means bear-like, related to Ursa Major and Minor.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'urticaria',
            'pronunciation': '/ˌɜːrtɪˈkɛriə/',
            'definition': 'Urticaria, commonly known as hives, is a skin condition characterized by raised, itchy welts or wheals that appear suddenly on the skin. These welts are typically red or pink, vary in size, and can appear anywhere on the body. Urticaria is usually caused by allergic reactions, stress, infections, or medications. The condition can be acute (lasting less than six weeks) or chronic (persisting longer). Treatment often involves antihistamines and avoiding known triggers.',
            'example_sentence': 'The allergic reaction caused _____ to break out across her arms and face.',
            'etymology': 'From Latin "urtica" meaning "nettle," referring to the stinging nettle plant whose contact causes similar skin reactions.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "URTICA (nettle) + RIA" - urticaria causes skin reactions like touching stinging nettles.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'urushiol',
            'pronunciation': '/ʊˈruːʃiɔːl/',
            'definition': 'Urushiol is an oily organic compound found in plants like poison ivy, poison oak, and poison sumac that causes severe allergic contact dermatitis in most people. This colorless or pale yellow oil is the active ingredient responsible for the painful, itchy rashes these plants produce. Urushiol can remain active on surfaces for years and is extremely potent - even tiny amounts can trigger reactions. The compound is also found in the sap of Japanese lacquer trees.',
            'example_sentence': 'The hiker developed a severe rash after unknowingly touching _____ from poison ivy while hiking.',
            'etymology': 'From Japanese "urushi" (lacquer tree) + "-ol" (chemical suffix for alcohols). Named after the Japanese lacquer tree that contains this compound.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YOU RUSH + OIL" - you\'ll rush to wash off urushiol oil if you get it on your skin.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'usable',
            'pronunciation': '/ˈjuːzəbəl/',
            'definition': 'Usable means able to be used; in a condition that allows for practical use or application. It describes objects, systems, or resources that are functional, accessible, and suitable for their intended purpose. Something usable is not only technically functional but also practical and convenient to use. The word often appears in discussions of design, technology, and efficiency, emphasizing both capability and ease of use.',
            'example_sentence': 'After the repairs, the old computer was finally _____ again for basic tasks.',
            'etymology': 'From "use" + "-able." "Use" comes from Latin "uti" meaning "to use, employ, enjoy."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USE + ABLE" - usable means you are able to use something effectively.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'usage',
            'pronunciation': '/ˈjuːsɪdʒ/',
            'definition': 'Usage refers to the action of using something or the manner in which something is used. It can describe patterns of use, the way language is employed, or the consumption of resources. In linguistics, usage refers to the way words and phrases are actually used by speakers, as opposed to prescriptive rules. Usage often implies established customs or accepted practices in how something should be used.',
            'example_sentence': 'The dictionary provided examples of proper _____ for each word definition.',
            'etymology': 'From Old French "usage," from "user" (to use), ultimately from Latin "uti." The suffix indicates the action or result of using.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USE + AGE" - usage is the age-old way of using or employing something.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'used',
            'pronunciation': '/juːzd/',
            'definition': 'Used can mean previously owned or employed by someone else, not new; or it can indicate past habitual action (used to do something). As an adjective, used describes items that have been previously owned or are second-hand. When followed by "to," it indicates past habits or states that no longer exist. The word can also be the past tense of "use," meaning employed or utilized for a purpose.',
            'example_sentence': 'She bought a _____ car that was still in excellent condition.',
            'etymology': 'Past tense and past participle of "use," from Old English "ūsian," from Latin "uti" (to use).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USE + D" - used is simply the past form of use, or something that has been used before.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'useful',
            'pronunciation': '/ˈjuːsfəl/',
            'definition': 'Useful means able to be used for a practical purpose or in several ways; helpful or beneficial. It describes things that provide value, assistance, or advantage in accomplishing tasks or solving problems. Something useful serves a function that makes life easier, work more efficient, or goals more achievable. The word emphasizes practical value and the ability to contribute positively to outcomes.',
            'example_sentence': 'The Swiss Army knife proved to be incredibly _____ during the camping trip.',
            'etymology': 'From "use" + "-ful." The suffix "-ful" means "full of" or "characterized by," so useful means "full of use."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USE + FUL" - useful means full of use and practical value.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'ushabti',
            'pronunciation': '/uːˈʃæbti/',
            'definition': 'Ushabti (also spelled shabti or shawabti) are small figurines placed in ancient Egyptian tombs to serve as servants for the deceased in the afterlife. These figurines, usually made of wood, stone, or faience, were believed to come to life and perform labor for the dead person in the next world. Ushabti often carry tools like hoes and baskets and have hieroglyphic inscriptions. Wealthy individuals might be buried with hundreds of these figurines.',
            'example_sentence': 'The pharaoh\'s tomb contained over 400 _____ figurines to ensure he would be well-served in the afterlife.',
            'etymology': 'From Egyptian "ushabti," possibly meaning "answerer," as these figurines were supposed to answer when called to work in the afterlife.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YOU + SHABTI" - ushabti are figurines that work for you in the ancient Egyptian afterlife.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 4
        },
        {
            'word': 'usher',
            'pronunciation': '/ˈʌʃər/',
            'definition': 'An usher is a person who escorts people to their seats in a theater, church, or other venue, or who maintains order at such events. As a verb, usher means to guide or escort someone somewhere, or to mark the beginning of something new. Ushers often assist with crowd control, provide information, and help ensure events run smoothly. The word can also mean to herald or introduce a new period or development.',
            'example_sentence': 'The wedding _____ helped guide guests to their appropriate seats in the ceremony.',
            'etymology': 'From Old French "ussier" (doorkeeper), from Latin "ostiarius," from "ostium" (door, entrance).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USHER sounds like ENSURE" - ushers ensure people get to where they need to go.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'ushuaia',
            'pronunciation': '/uːˈʃwaɪə/',
            'definition': 'Ushuaia is the capital city of Tierra del Fuego province in Argentina and is often called "the southernmost city in the world." Located on the Beagle Channel, Ushuaia serves as a gateway to Antarctica and is a popular destination for tourists seeking adventure travel and wildlife viewing. The city is surrounded by mountains and forests, and its economy relies heavily on tourism, fishing, and electronics assembly. Ushuaia\'s unique location makes it a significant point for polar expeditions.',
            'example_sentence': 'Many Antarctic cruises depart from _____, taking advantage of its strategic southern location.',
            'etymology': 'From the indigenous Yaghan language, possibly meaning "bay penetrating westward" or referring to the geographic features of the area.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YOU + SHWAY + A" - Ushuaia is where you go to sway on ships heading to Antarctica.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 4
        }
    ]
    
    # Prepare CSV output
    output_file = 'output/batch_187_processed.csv'
    
    # CSV headers matching the database schema
    headers = [
        'word', 'pronunciation', 'definition', 'example_sentence', 'etymology', 
        'etymology_source', 'memory_tip', 'phonetic_transparency', 'frequency', 
        'morphological_complexity', 'etymology_complexity', 'overall_difficulty_score', 
        'difficulty_level'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        for word_data in words_data:
            # Calculate difficulty metrics
            score = calculate_difficulty_score(
                word_data['phonetic_transparency'],
                word_data['frequency'], 
                word_data['morphological_complexity'],
                word_data['etymology_complexity']
            )
            level = determine_difficulty_level(score)
            
            # Add calculated fields
            word_data['overall_difficulty_score'] = score
            word_data['difficulty_level'] = level
            
            writer.writerow(word_data)
            logging.info(f"Processed word: {word_data['word']}")
    
    logging.info(f"Saved {len(words_data)} words to {output_file}")
    logging.info("Batch 187 processing completed!")
    logging.info(f"Processed {len(words_data)} words with comprehensive Claude data")
    logging.info(f"Output saved to: {output_file}")
    logging.info(f"Results: {len(words_data)} successful, 0 failed")
    
    # Report combined word errors
    if combined_errors:
        logging.info(f"Combined word errors detected: {len(combined_errors)}")
        for error in combined_errors:
            logging.info(f"  - {error}")

if __name__ == "__main__":
    main()