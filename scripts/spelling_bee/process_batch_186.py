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
    logging.info("Processing Batch 186 with comprehensive Claude data...")
    
    # Combined word errors detected in batch 186
    combined_errors = ['ufologycholera', 'uglinessquack', 'undergirdnoun', 'unfurldifficulty']
    
    # Comprehensive spelling bee data with Claude-generated educational content
    words_data = [
        {
            'word': 'ugliness',
            'pronunciation': '/ˈʌɡlinəs/',
            'definition': 'Ugliness refers to the quality or state of being unpleasant or repulsive to look at, lacking beauty or aesthetic appeal. It can describe physical appearance, behavior, or situations that are morally offensive or disagreeable. Ugliness is often subjective, varying across cultures and personal preferences, though some aspects may be more universally perceived. The concept extends beyond visual appearance to include ugly behavior, ugly situations, or ugly truths that are unpleasant to confront.',
            'example_sentence': 'The _____ of the abandoned building contrasted sharply with the beautiful park next to it.',
            'etymology': 'From "ugly" + "-ness." "Ugly" comes from Old Norse "uggligr" meaning "fearful, dreadful," related to "ugga" (to fear). The -ness suffix creates the noun form.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UGLY + NESS" - ugliness is simply the state or quality of being ugly.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'ukrainian',
            'pronunciation': '/juːˈkreɪniən/',
            'definition': 'Ukrainian refers to anything relating to Ukraine, its people, language, or culture. As a noun, it describes a person from Ukraine or the East Slavic language spoken there. Ukrainian is the official language of Ukraine and is spoken by about 45 million people worldwide. The language uses the Cyrillic alphabet and has distinctive features that differentiate it from Russian and other Slavic languages. Ukrainian culture has rich traditions in literature, music, folk art, and cuisine.',
            'example_sentence': 'She learned to cook traditional _____ dishes from her grandmother\'s recipes.',
            'etymology': 'From "Ukraine" + "-ian." "Ukraine" comes from Ukrainian "Україна" meaning "borderland" or "frontier," from "u" (at) + "krai" (edge, border).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UKRAINE + IAN" - Ukrainian describes people or things from Ukraine, like "American" for America.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'ullage',
            'pronunciation': '/ˈʌlɪdʒ/',
            'definition': 'Ullage is the amount by which a container, particularly a wine bottle or barrel, falls short of being completely full. This space allows for thermal expansion of the liquid and is normal in wine storage. In wine aging, some ullage occurs naturally through evaporation and absorption into the wood of barrels. Excessive ullage can indicate spoilage or improper storage. The term is also used in other industries dealing with liquid storage and transportation.',
            'example_sentence': 'The wine collector noted the _____ in the vintage bottle, which indicated its age and proper storage.',
            'etymology': 'From Anglo-French "ullage," from "ouiller" meaning "to fill up," from "ueil" (eye), referring to the bung-hole of a barrel that resembles an eye.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "FULL + AGE" but backwards - ullage is the empty space that comes with age in wine containers.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 4
        },
        {
            'word': 'ulna',
            'pronunciation': '/ˈʌlnə/',
            'definition': 'The ulna is one of the two bones in the human forearm, located on the pinky finger side (medial side) when the palm faces forward. It\'s the longer of the two forearm bones, extending from the elbow to the wrist. The ulna forms the primary articulation with the humerus at the elbow joint and provides attachment points for many muscles that control hand and wrist movement. It works together with the radius bone to allow rotation of the forearm.',
            'example_sentence': 'The X-ray revealed a hairline fracture in her _____ bone near the wrist.',
            'etymology': 'From Latin "ulna" meaning "elbow" or "forearm," related to Greek "olene" (elbow). The anatomical term has been used since ancient times.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "ULNA sounds like ELBOW-na" - it\'s the forearm bone that connects to your elbow.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'ulterior',
            'pronunciation': '/ʌlˈtɪriər/',
            'definition': 'Ulterior means existing beyond what is obvious or admitted, typically referring to hidden motives or purposes. It describes intentions that are concealed or not immediately apparent, often implying that someone has secret reasons for their actions. The word frequently appears in the phrase "ulterior motive," suggesting that someone\'s stated reason for doing something is not their real reason. Ulterior can also mean further, more remote, or lying beyond.',
            'example_sentence': 'She suspected he had an _____ motive for offering to help with her project.',
            'etymology': 'From Latin "ulterior," comparative of "ulter" meaning "beyond, farther." Related to "ultra" (beyond). The word suggests something lying beyond what is immediately visible.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "ULTRA + INTERIOR" - ulterior motives are ultra-hidden in the interior of someone\'s mind.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'ultimate',
            'pronunciation': '/ˈʌltɪmət/',
            'definition': 'Ultimate means final, last, or concluding in a series or process. It can also mean the best, most extreme, or most significant of its kind. Ultimate suggests the highest degree of something or the final stage that cannot be surpassed or exceeded. In philosophy, ultimate refers to fundamental or basic principles. The word implies both finality and supremacy, representing the end point or peak of achievement.',
            'example_sentence': 'Winning the championship was the _____ goal of their training season.',
            'etymology': 'From Latin "ultimus" meaning "last, final," superlative of "ulter" (beyond). The word has maintained its sense of finality and extremity.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "ULTRA + MATE" - ultimate is like the ultra version, the best mate or final answer.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'ultimatum',
            'pronunciation': '/ˌʌltɪˈmeɪtəm/',
            'definition': 'An ultimatum is a final demand or proposal, especially one whose rejection will result in the end of negotiations and possibly lead to hostile action. It represents a last resort in negotiations, where one party presents non-negotiable terms that must be accepted or rejected. Ultimatums are often used in diplomacy, business negotiations, and personal relationships when other forms of persuasion have failed. The word implies urgency and serious consequences for non-compliance.',
            'example_sentence': 'The union issued an _____ to management: improve working conditions or face a strike.',
            'etymology': 'From Latin "ultimatum," neuter of "ultimatus" (final), from "ultimus" (last). Originally a diplomatic term meaning "the final proposition."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "ULTIMATE + TUM (tummy)" - an ultimatum makes your tummy nervous because it\'s the ultimate, final demand.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'ultradian',
            'pronunciation': '/ʌlˈtreɪdiən/',
            'definition': 'Ultradian refers to biological rhythms or cycles that occur with a frequency higher than circadian rhythms, typically multiple times within a 24-hour period. These rhythms have periods shorter than 20 hours and include patterns like REM sleep cycles (90-120 minutes), hormone fluctuations, and feeding patterns. Ultradian rhythms are important in understanding human physiology, sleep architecture, and optimal timing for various activities. They contrast with circadian (daily) and infradian (longer than daily) rhythms.',
            'example_sentence': 'Researchers studied the _____ patterns of hormone release throughout the day.',
            'etymology': 'From Latin "ultra" (beyond) + "dies" (day) + "-ian." Coined in chronobiology to describe rhythms that cycle more frequently than once per day.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "ULTRA + DAY + IAN" - ultradian rhythms happen ultra-frequently, more than once per day.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'ululate',
            'pronunciation': '/ˈʌljəˌleɪt/',
            'definition': 'To ululate means to howl or wail in a prolonged, typically high-pitched manner, often as an expression of grief, joy, or celebration. This vocalization is characterized by a distinctive warbling or trilling sound, commonly produced by rapidly moving the tongue or by rapid changes in pitch. Ululation is found in many cultures as part of traditional celebrations, mourning rituals, or expressions of excitement. The sound is also naturally produced by wolves, coyotes, and other animals.',
            'example_sentence': 'The women began to _____ in celebration of the successful harvest.',
            'etymology': 'From Latin "ululatus," past participle of "ululare" meaning "to howl" or "to cry out." The word imitates the sound it describes.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "OOL (howl) + LATE" - to ululate is to make howling sounds, often late into the night.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'umami',
            'pronunciation': '/uːˈmɑːmi/',
            'definition': 'Umami is one of the five basic tastes, along with sweet, sour, bitter, and salty. It\'s characterized by a savory, meaty, or brothy flavor that enhances the overall taste of food. Umami taste is triggered by glutamates, particularly monosodium glutamate (MSG), and is found naturally in foods like mushrooms, aged cheeses, tomatoes, soy sauce, and fish sauce. The discovery and recognition of umami as a distinct taste has revolutionized understanding of flavor and cooking techniques.',
            'example_sentence': 'The chef added mushrooms and parmesan to enhance the _____ flavor of the dish.',
            'etymology': 'From Japanese "umami" (うま味), from "umai" (delicious) + "mi" (taste). The term was coined by Japanese chemist Kikunae Ikeda in 1908.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YUM + AMI (friend)" - umami makes food yummy, like a friend to your taste buds.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'umbelliferous',
            'pronunciation': '/ʌmˌbɛlɪˈfɛrəs/',
            'definition': 'Umbelliferous describes plants belonging to the Umbelliferae family (now called Apiaceae), characterized by flowers arranged in umbrella-like clusters called umbels. These plants include carrots, parsley, fennel, dill, celery, and cilantro. The family is known for its distinctive flower arrangement where individual flower stalks radiate from a common point, resembling the spokes of an umbrella. Many umbelliferous plants are economically important as food crops, spices, or medicinal herbs.',
            'example_sentence': 'The botanist identified the plant as _____ based on its characteristic umbrella-shaped flower clusters.',
            'etymology': 'From Latin "umbella" (little shade, umbrella) + "-ferous" (bearing). Literally means "bearing umbels" or "umbrella-bearing."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UMBRELLA + FEROUS (bearing)" - umbelliferous plants bear umbrella-shaped flower clusters.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 5,
            'etymology_complexity': 4
        },
        {
            'word': 'umbilical',
            'pronunciation': '/ʌmˈbɪlɪkəl/',
            'definition': 'Umbilical relates to the umbilicus (navel) or umbilical cord, the flexible tube-like structure that connects a developing fetus to the placenta during pregnancy. The umbilical cord carries nutrients and oxygen from the mother to the baby and removes waste products. After birth, the cord is cut, leaving the navel as a permanent reminder of this vital connection. Metaphorically, umbilical can describe any vital connection or link between entities.',
            'example_sentence': 'The astronaut\'s _____ cord provided life support during the spacewalk.',
            'etymology': 'From Latin "umbilicus" meaning "navel," related to "umbo" (boss of a shield, something that projects). The anatomical term has ancient origins.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UMBILICAL sounds like NAVEL-ical" - it relates to the navel and the cord that was once there.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'umbrage',
            'pronunciation': '/ˈʌmbrɪdʒ/',
            'definition': 'Umbrage means offense or resentment, particularly when someone feels their pride has been wounded or they\'ve been slighted. It describes the feeling of being insulted or having one\'s dignity compromised, often over something relatively minor. The phrase "take umbrage" is commonly used to mean becoming offended or feeling insulted by someone\'s words or actions. Umbrage implies a sense of injured pride or wounded feelings.',
            'example_sentence': 'She took _____ at his suggestion that she wasn\'t qualified for the position.',
            'etymology': 'From Latin "umbra" meaning "shadow" or "shade." Originally meant shade or shadow, then came to mean suspicion, and finally offense (being in someone\'s shadow).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDER + RAGE" - umbrage is like being under a shadow of rage when someone offends you.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 4
        },
        {
            'word': 'umbrella',
            'pronunciation': '/ʌmˈbrɛlə/',
            'definition': 'An umbrella is a collapsible canopy designed to protect against rain or sun, consisting of a circular fabric cover stretched over hinged ribs that radiate from a central pole. Umbrellas can be handheld (parasols) or larger patio versions for outdoor shade. The word also refers metaphorically to anything that covers or protects, such as an "umbrella organization" that encompasses smaller groups, or "umbrella insurance" that provides broad coverage.',
            'example_sentence': 'She grabbed her _____ before stepping out into the pouring rain.',
            'etymology': 'From Italian "ombrella," diminutive of "ombra" (shade), from Latin "umbra" (shadow). Originally referred to a sunshade rather than rain protection.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDER + BELLA (beautiful)" - an umbrella keeps you beautifully dry under its protection.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'umpirage',
            'pronunciation': '/ˈʌmpaɪrɪdʒ/',
            'definition': 'Umpirage refers to the act, process, or period of serving as an umpire, particularly in sports or disputes. It encompasses the duties, decisions, and authority exercised by an umpire during a game or arbitration process. Umpirage involves making impartial judgments, enforcing rules, and resolving conflicts between competing parties. The term emphasizes the official capacity and responsibility inherent in the umpire\'s role.',
            'example_sentence': 'His fair and decisive _____ earned him respect from players and coaches alike.',
            'etymology': 'From "umpire" + "-age." "Umpire" comes from Old French "nonper" meaning "not equal, odd number," referring to a third party who breaks ties.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UMPIRE + AGE" - umpirage is the act or period of being an umpire, like "coverage" or "storage."',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'unabridged',
            'pronunciation': '/ˌʌnəˈbrɪdʒd/',
            'definition': 'Unabridged means complete and not shortened, condensed, or reduced from the original version. This term is most commonly applied to books, particularly dictionaries, novels, and reference works that contain the full, original text without cuts or modifications. An unabridged work preserves all the author\'s original content, providing readers with the complete intended experience. This contrasts with abridged versions that are shortened for convenience or specific audiences.',
            'example_sentence': 'She preferred to read the _____ version of the classic novel to experience the author\'s complete vision.',
            'etymology': 'From "un-" (not) + "abridged." "Abridge" comes from Old French "abregier," from Latin "abbreviare" (to shorten).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + BRIDGE" - unabridged works don\'t bridge (skip over) any content, they include everything.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'unacknowledged',
            'pronunciation': '/ˌʌnəkˈnɑːlɪdʒd/',
            'definition': 'Unacknowledged means not recognized, admitted, or given credit for something. It describes contributions, achievements, feelings, or facts that have not been formally recognized or accepted. This can apply to people whose work goes unnoticed, emotions that aren\'t expressed or validated, or truths that society chooses to ignore. Unacknowledged often carries a sense of injustice or oversight, suggesting that recognition is deserved but withheld.',
            'example_sentence': 'Her groundbreaking research remained _____ by the scientific community for decades.',
            'etymology': 'From "un-" (not) + "acknowledged." "Acknowledge" comes from "a-" (intensive) + "knowledge," meaning to admit knowledge of something.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + ACKNOWLEDGE" - something unacknowledged hasn\'t been given the recognition it deserves.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 2
        },
        {
            'word': 'unakite',
            'pronunciation': '/ˈjuːnəkaɪt/',
            'definition': 'Unakite is a distinctive metamorphic rock composed primarily of pink orthoclase feldspar, green epidote, and clear quartz. Named after the Unaka Mountains where it was first found, this rock is prized for its attractive mottled green and pink appearance. Unakite is popular in jewelry making, decorative objects, and lapidary work. In crystal healing practices, it\'s believed to promote emotional balance and spiritual growth, though these claims lack scientific support.',
            'example_sentence': 'The jewelry maker chose _____ for its beautiful combination of green and pink coloring.',
            'etymology': 'Named after the Unaka Mountains on the Tennessee-North Carolina border where this rock type was first identified and described.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNA (one) + KITE" - unakite looks like one colorful kite with green and pink patches flying together.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'unanimous',
            'pronunciation': '/juːˈnænɪməs/',
            'definition': 'Unanimous means fully in agreement, with all people involved sharing the same opinion or reaching the same decision. It describes a situation where there is complete accord among all parties, with no dissenting voices or opposing votes. Unanimous decisions carry special weight because they demonstrate total consensus. The term is commonly used in voting contexts, jury verdicts, and group decisions where unity of opinion is significant.',
            'example_sentence': 'The jury reached a _____ verdict after deliberating for only two hours.',
            'etymology': 'From Latin "unanimus," from "unus" (one) + "animus" (mind, spirit). Literally means "of one mind."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNI (one) + ANIMUS (mind)" - unanimous means everyone has one unified mind on the issue.',
            'phonetic_transparency': 2,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'unassuming',
            'pronunciation': '/ˌʌnəˈsuːmɪŋ/',
            'definition': 'Unassuming describes someone who is modest, humble, and not pretentious or arrogant. An unassuming person doesn\'t draw attention to themselves, show off, or act superior to others. This quality is often admired as it demonstrates genuine humility and lack of ego. Unassuming can also describe things that are simple, unpretentious, or not designed to impress, such as an unassuming building or meal that turns out to be exceptional.',
            'example_sentence': 'Despite his great wealth, he remained _____ and approachable to everyone he met.',
            'etymology': 'From "un-" (not) + "assuming." "Assume" comes from Latin "assumere" meaning "to take up," but "assuming" here means "pretentious."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + ASSUMING" - unassuming people don\'t assume they\'re better than others; they\'re humble.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'unbeknownst',
            'pronunciation': '/ˌʌnbɪˈnoʊnst/',
            'definition': 'Unbeknownst means without the knowledge of someone; unknown or unnoticed by a particular person. It describes situations where something happens or exists without someone being aware of it. The word often introduces information that reveals hidden or secret circumstances that the subject was unaware of. It\'s typically followed by "to" and indicates that important events or facts were occurring outside someone\'s awareness.',
            'example_sentence': '_____ to her parents, she had been secretly taking art classes after school.',
            'etymology': 'From "un-" (not) + "beknown" (archaic past participle of "know") + "-st" (archaic suffix). An older form meaning "unknown."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + BE + KNOWN + ST" - something unbeknownst wasn\'t known to exist or happen.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'uncanny',
            'pronunciation': '/ʌnˈkæni/',
            'definition': 'Uncanny describes something strange, mysterious, or unsettling in a way that seems supernatural or beyond normal explanation. It refers to phenomena that are eerily strange or remarkably accurate in a way that seems almost impossible. Uncanny can describe coincidences, resemblances, abilities, or situations that are so unusual they create an uncomfortable or eerie feeling. The word suggests something that transcends ordinary understanding or expectation.',
            'example_sentence': 'She had an _____ ability to predict exactly what people were thinking.',
            'etymology': 'From Scots "uncanny," from "un-" (not) + "canny" (knowing, skillful). Originally meant "dangerous because of supernatural powers."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + CANNY (able)" - uncanny things are so strange they seem beyond human ability to explain.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'unchristened',
            'pronunciation': '/ʌnˈkrɪsənd/',
            'definition': 'Unchristened means not having received the Christian sacrament of baptism or christening. In traditional Christian practice, christening involves the ceremonial naming and blessing of a person, usually an infant, through baptism. An unchristened person has not undergone this religious ritual. The word can also be used metaphorically to describe something that hasn\'t been formally named, dedicated, or inaugurated.',
            'example_sentence': 'The old church records showed several _____ children from families who lived far from town.',
            'etymology': 'From "un-" (not) + "christened." "Christen" comes from "Christ" + "-en," meaning to make Christian through baptism.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + CHRISTENED" - unchristened people haven\'t been formally named and blessed in a Christian ceremony.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'uncle',
            'pronunciation': '/ˈʌŋkəl/',
            'definition': 'An uncle is the brother of one\'s father or mother, or the husband of one\'s aunt. This family relationship represents a specific kinship role in family structures across cultures. Uncles often play important roles in extended families, sometimes serving as mentors, father figures, or close family friends. The term can also be used as a title of respect for older men who aren\'t biological relatives, and appears in various cultural expressions and idioms.',
            'example_sentence': 'Her _____ taught her how to fish during their summer vacation at the lake.',
            'etymology': 'From Old French "oncle," from Latin "avunculus" meaning "mother\'s brother," diminutive of "avus" (grandfather). The term originally distinguished maternal uncles.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNCLE sounds like ANKLE" - both are parts of your family body, with uncle being family and ankle being body.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'unconscionable',
            'pronunciation': '/ʌnˈkɑːnʃənəbəl/',
            'definition': 'Unconscionable means not guided by conscience; unreasonably excessive or shocking. It describes actions, demands, or behavior that are so unfair, unethical, or extreme that they shock the moral sense. In legal contexts, unconscionable contracts are those so one-sided or unfair that no reasonable person would agree to them. The word implies a complete lack of moral restraint or consideration for others.',
            'example_sentence': 'The landlord\'s demand for a 300% rent increase was deemed _____ by the housing court.',
            'etymology': 'From "un-" (not) + "conscionable" (guided by conscience). "Conscience" comes from Latin "conscientia" meaning "knowledge within oneself."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + CONSCIENCE + ABLE" - unconscionable acts are not able to be guided by conscience.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 5,
            'etymology_complexity': 3
        },
        {
            'word': 'uncouth',
            'pronunciation': '/ʌnˈkuːθ/',
            'definition': 'Uncouth describes behavior that is lacking in good manners, refinement, or grace; crude or awkward in behavior or appearance. It characterizes people or actions that seem uncivilized, rough, or socially inappropriate. Uncouth behavior violates social norms and expectations of politeness or sophistication. The word suggests a lack of cultural refinement or education in proper social conduct.',
            'example_sentence': 'His _____ table manners embarrassed his family at the formal dinner.',
            'etymology': 'From Old English "uncūth" meaning "unknown, strange," from "un-" (not) + "cūth" (known, familiar). Originally meant "unfamiliar" but evolved to mean "unrefined."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + COUTH (smooth)" - uncouth people aren\'t smooth or refined in their behavior.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 4
        },
        {
            'word': 'unctuous',
            'pronunciation': '/ˈʌŋktʃuəs/',
            'definition': 'Unctuous primarily means excessively flattering or ingratiating in a way that seems insincere or oily. It describes behavior that is overly smooth, suave, or fawning, often with the intent to manipulate or gain favor. In its literal sense, unctuous means having an oily or greasy texture. The word carries negative connotations when applied to personality, suggesting false charm or sycophantic behavior.',
            'example_sentence': 'The salesman\'s _____ manner made customers suspicious of his true intentions.',
            'etymology': 'From Latin "unctuosus" meaning "oily, greasy," from "unctus" (anointed), from "ungere" (to anoint). The figurative meaning developed from the idea of being "slippery."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "OILY + UNCTUOUS" - unctuous people are oily and slippery in their overly smooth behavior.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'undaunted',
            'pronunciation': '/ʌnˈdɔːntɪd/',
            'definition': 'Undaunted means not intimidated or discouraged by difficulty, danger, or disappointment. It describes someone who perseveres with courage and determination despite obstacles, setbacks, or fears. An undaunted person maintains their resolve and continues forward even when facing significant challenges. The word implies both bravery and persistence in the face of adversity.',
            'example_sentence': 'Though her first business failed, she remained _____ and started planning her next venture.',
            'etymology': 'From "un-" (not) + "daunted." "Daunt" comes from Old French "danter," from Latin "domitare" meaning "to tame."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + DAUNTED" - undaunted people can\'t be tamed or discouraged by challenges.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'undercroft',
            'pronunciation': '/ˈʌndərˌkrɔːft/',
            'definition': 'An undercroft is a vaulted chamber or basement beneath the main floor of a church, castle, or other large building, typically used for storage or as a foundation space. These underground rooms were common in medieval architecture, often featuring stone vaulting and serving various practical purposes. In churches, undercrofts sometimes housed crypts or burial chambers. The architectural feature provided both structural support and useful space.',
            'example_sentence': 'The medieval cathedral\'s _____ housed ancient artifacts and served as a museum.',
            'etymology': 'From "under" + "croft." "Croft" comes from Old English, meaning a small enclosed field or chamber, related to "craft."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDER + CROFT (craft room)" - an undercroft is like a craft room under the main building.',
            'phonetic_transparency': 4,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'undergird',
            'pronunciation': '/ˌʌndərˈɡɜːrd/',
            'definition': 'To undergird means to strengthen or support from underneath, either literally or figuratively. It can describe providing physical support through structural reinforcement, or metaphorically supporting ideas, arguments, or institutions with strong foundations. Undergirding involves creating a solid base or framework that supports something more complex built upon it. The word emphasizes the foundational nature of the support provided.',
            'example_sentence': 'Strong ethical principles _____ all of the company\'s business decisions.',
            'etymology': 'From "under" + "gird." "Gird" comes from Old English "gyrdan" meaning "to encircle, prepare." Originally referred to fastening a belt or rope around something.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDER + GIRD (belt)" - to undergird is to put a strong belt of support under something.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'understand',
            'pronunciation': '/ˌʌndərˈstænd/',
            'definition': 'Understand means to perceive the meaning, nature, or importance of something; to grasp mentally or emotionally. It involves comprehending information, concepts, situations, or people\'s feelings and motivations. Understanding can be intellectual (grasping facts or ideas), emotional (empathizing with feelings), or practical (knowing how to do something). The word implies not just awareness but genuine comprehension.',
            'example_sentence': 'It took her years to fully _____ the complex mathematical concepts.',
            'etymology': 'From Old English "understandan," literally "to stand under" or "stand among." The metaphor suggests standing close enough to get the full meaning.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDER + STAND" - to understand, you need to stand under or close to something to really get it.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'understanding',
            'pronunciation': '/ˌʌndərˈstændɪŋ/',
            'definition': 'Understanding can be a noun meaning comprehension, insight, or sympathetic awareness of others\' feelings or situations. As an adjective, it describes someone who is compassionate, tolerant, and patient with others\' difficulties or mistakes. Understanding involves both intellectual grasp and emotional empathy. It can also refer to an informal agreement or arrangement between parties.',
            'example_sentence': 'Her _____ of the situation helped calm everyone\'s concerns.',
            'etymology': 'From "understand" + "-ing." The gerund form can function as both a noun (the act of understanding) and an adjective (showing understanding).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDERSTAND + ING" - understanding is the ongoing process or quality of being able to understand.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'undertake',
            'pronunciation': '/ˌʌndərˈteɪk/',
            'definition': 'Undertake means to commit oneself to begin and carry out a task, project, or responsibility. It implies accepting the obligation to complete something, often something challenging or significant. Undertaking involves both the decision to begin and the commitment to see it through. The word suggests a serious commitment rather than a casual attempt.',
            'example_sentence': 'The research team decided to _____ a comprehensive study of climate change effects.',
            'etymology': 'From "under" + "take." Originally meant "to take in hand" or "to catch." The sense of "accept responsibility" developed in Middle English.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDER + TAKE" - to undertake is to take something under your responsibility and control.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'undertaken',
            'pronunciation': '/ˌʌndərˈteɪkən/',
            'definition': 'Undertaken is the past participle of undertake, meaning something has been committed to, begun, or accepted as a responsibility. It describes tasks, projects, or obligations that someone has formally agreed to carry out. The word implies that the commitment has been made and the work has commenced, though it may not yet be completed.',
            'example_sentence': 'The renovation project was _____ by the city\'s most experienced construction crew.',
            'etymology': 'Past participle of "undertake," from "under" + "take" + "-en" (past participle ending). Shows completed action of accepting responsibility.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDERTAKE + EN" - undertaken means someone has already taken on the responsibility.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'undine',
            'pronunciation': '/ˈʌndiːn/',
            'definition': 'An undine is a water spirit or nymph in European folklore, particularly Germanic and medieval traditions. These supernatural beings were believed to inhabit rivers, lakes, and other bodies of water. According to legend, undines could gain a soul by marrying a human, but would return to the water if betrayed. The concept appears in various literary works and represents the connection between the human and natural worlds.',
            'example_sentence': 'The romantic novel featured an _____ who fell in love with a mortal fisherman.',
            'etymology': 'From Latin "unda" meaning "wave." Coined by the medieval writer Paracelsus to describe water elementals, later popularized in literature.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDINE sounds like UNDER WATER" - undines are water spirits that live under the waves.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'undulating',
            'pronunciation': '/ˈʌndʒəˌleɪtɪŋ/',
            'definition': 'Undulating describes something that moves with a smooth, wavelike motion or has a wavy form. It can refer to physical movement like the undulating motion of a snake, or to landscape features like rolling hills. The word suggests a continuous, flowing movement that rises and falls in a regular pattern, similar to ocean waves. Undulating implies grace and fluidity in motion or form.',
            'example_sentence': 'The _____ hills stretched as far as the eye could see.',
            'etymology': 'From Latin "undulatus," from "undula" (little wave), diminutive of "unda" (wave). The word preserves the wave-like imagery in its meaning.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNDO + LATE + ING" - undulating motion seems to undo straight lines, making them wavy.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'uneasy',
            'pronunciation': '/ʌnˈiːzi/',
            'definition': 'Uneasy describes a feeling of discomfort, anxiety, or apprehension about something. It can refer to both physical and mental discomfort - being physically uncomfortable or emotionally troubled by uncertainty or worry. Uneasy suggests a state of restlessness or concern that prevents complete relaxation or peace of mind. The word implies that something isn\'t quite right, even if the exact problem can\'t be identified.',
            'example_sentence': 'She felt _____ about leaving her children with a babysitter she had just met.',
            'etymology': 'From "un-" (not) + "easy." "Easy" comes from Old French "aisie," meaning "comfortable, at ease."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + EASY" - uneasy is simply not feeling easy, comfortable, or relaxed.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'unexpectedly',
            'pronunciation': '/ˌʌnɪkˈspɛktɪdli/',
            'definition': 'Unexpectedly means in a way that is not expected or anticipated; suddenly and without warning. It describes events, actions, or outcomes that occur without prior indication or preparation. Something happening unexpectedly catches people by surprise because it wasn\'t predicted or planned for. The word emphasizes the element of surprise and the absence of advance notice.',
            'example_sentence': 'The shy student _____ volunteered to give the presentation.',
            'etymology': 'From "unexpected" + "-ly." "Unexpected" comes from "un-" (not) + "expected," from Latin "expectare" (to look out for).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + EXPECTED + LY" - unexpectedly means something happened in a way that wasn\'t expected.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 4,
            'etymology_complexity': 2
        },
        {
            'word': 'unfazed',
            'pronunciation': '/ʌnˈfeɪzd/',
            'definition': 'Unfazed means not disturbed, perturbed, or affected by something that might typically cause concern, surprise, or upset. It describes someone who remains calm and composed in the face of difficulties, criticism, or unexpected events. An unfazed person shows remarkable composure and doesn\'t let external circumstances affect their emotional state or determination.',
            'example_sentence': 'Despite the harsh criticism, she remained completely _____ and continued with her presentation.',
            'etymology': 'From "un-" (not) + "fazed." "Faze" is a variant of "feeze," meaning "to worry, disturb," from Old English "fēsian" (to drive away).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + FAZED (phased)" - unfazed people aren\'t phased or bothered by what happens around them.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'unfurl',
            'pronunciation': '/ʌnˈfɜːrl/',
            'definition': 'Unfurl means to open or spread out from a rolled or folded state, particularly used with flags, sails, banners, or similar items. The action involves unrolling or unfolding something that was previously compact or furled. Unfurl can also be used metaphorically to describe the gradual revelation or development of ideas, plans, or events. The word suggests a smooth, deliberate opening process.',
            'example_sentence': 'The soldiers watched the flag slowly _____ in the morning breeze.',
            'etymology': 'From "un-" (reverse action) + "furl." "Furl" comes from French "ferler," meaning "to bind firmly," originally a nautical term for securing sails.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + FURL" - to unfurl is to undo the furling (rolling up) of flags or sails.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'ungetatable',
            'pronunciation': '/ʌnˈɡɛtətəbəl/',
            'definition': 'Ungetatable means impossible to obtain, reach, or achieve; inaccessible or unattainable. This somewhat informal word describes something that cannot be acquired despite efforts to get it. It can refer to physical objects that are out of reach, abstract goals that are unrealistic, or people who are unavailable or difficult to contact. The word emphasizes the frustrating impossibility of obtaining something desired.',
            'example_sentence': 'The rare book was completely _____ due to its astronomical price.',
            'etymology': 'From "un-" (not) + "get" + "-at" (indicating possibility) + "-able" (capable of). A compound formation meaning "not able to be gotten at."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN + GET + AT + ABLE" - ungetatable things can\'t be gotten at or reached.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 2
        },
        {
            'word': 'unguiculate',
            'pronunciation': '/ʌnˈɡwɪkjələt/',
            'definition': 'Unguiculate describes animals that have claws or nails, as opposed to hooves. This zoological term distinguishes mammals with claws (like cats, dogs, and bears) from ungulates (hoofed animals like horses and cattle). Unguiculate animals use their claws for various purposes including climbing, digging, hunting, and defense. The term is used in scientific classification and anatomical studies.',
            'example_sentence': 'The biologist studied the hunting behaviors of various _____ predators.',
            'etymology': 'From Latin "unguiculus," diminutive of "unguis" meaning "nail, claw." The suffix "-ate" indicates possession of the characteristic.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UN (nail) + GUICULATE" - unguiculate animals have nails or claws rather than hooves.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 4
        },
        {
            'word': 'unilaterally',
            'pronunciation': '/ˌjuːnɪˈlætərəli/',
            'definition': 'Unilaterally means done by one side or party alone, without agreement or consultation with others involved. It describes actions taken independently, often in situations where cooperation or mutual agreement would be expected or preferred. Unilateral decisions can be seen as either decisive leadership or inconsiderate disregard for others\' input, depending on the context and consequences.',
            'example_sentence': 'The country decided to _____ withdraw from the international trade agreement.',
            'etymology': 'From "unilateral" + "-ly." "Unilateral" comes from Latin "unus" (one) + "lateralis" (of the side), meaning "one-sided."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNI (one) + LATERAL (side) + LY" - unilaterally means acting from one side only.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 5,
            'etymology_complexity': 3
        },
        {
            'word': 'unit',
            'pronunciation': '/ˈjuːnɪt/',
            'definition': 'A unit is a single thing or person regarded as separate and complete, or a standard measurement used to express quantities. In mathematics and science, units provide the basis for measurement systems (like meters, seconds, or grams). Units can also refer to organizational divisions, housing accommodations, or individual components of larger systems. The concept emphasizes both individuality and standardization.',
            'example_sentence': 'Each _____ in the apartment complex has its own private entrance.',
            'etymology': 'From Latin "unus" meaning "one." The word entered English through Middle French "unité," emphasizing the concept of oneness or singularity.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNI (one) + T" - a unit is one single thing, unified and complete.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'united',
            'pronunciation': '/juːˈnaɪtɪd/',
            'definition': 'United means joined together for a common purpose or by common feelings; in agreement or harmony. It describes people, groups, or things that have come together or been brought together to form a single entity or to work toward shared goals. United implies cooperation, solidarity, and the setting aside of differences for mutual benefit. The word emphasizes both the act of joining and the resulting state of togetherness.',
            'example_sentence': 'The community remained _____ in their effort to rebuild after the natural disaster.',
            'etymology': 'Past participle of "unite," from Latin "unitus," from "unus" (one). The word emphasizes the action of becoming one or joining together.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNI (one) + TED" - united people have become one group working together.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'universal',
            'pronunciation': '/ˌjuːnɪˈvɜːrsəl/',
            'definition': 'Universal means applicable to all cases, situations, or people; existing everywhere or affecting everyone. It describes principles, truths, laws, or phenomena that are consistent across all contexts without exception. Universal can refer to shared human experiences, scientific laws that apply throughout the universe, or values that transcend cultural boundaries. The word emphasizes comprehensiveness and inclusivity.',
            'example_sentence': 'The desire for happiness appears to be a _____ human trait.',
            'etymology': 'From Latin "universalis," from "universus" meaning "whole, entire," from "unus" (one) + "versus" (turned). Originally meant "turned into one."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UNI (one) + VERSAL (version)" - universal means one version that applies to everyone and everything.',
            'phonetic_transparency': 2,
            'frequency': 4,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        }
    ]
    
    # Prepare CSV output
    output_file = 'output/batch_186_processed.csv'
    
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
    logging.info("Batch 186 processing completed!")
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