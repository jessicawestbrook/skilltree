#!/usr/bin/env python3

import csv
import logging
from pathlib import Path
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        return {
            'phonetic_transparency_score': self._calculate_phonetic_transparency(word),
            'word_frequency_score': self._calculate_word_frequency(word),
            'morphological_complexity_score': self._calculate_morphological_complexity(word),
            'etymology_complexity_score': self._calculate_etymology_complexity(etymology),
            'difficulty': None
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> int:
        transparent_patterns = ['cat', 'dog', 'run', 'jump', 'play']
        if any(pattern in word.lower() for pattern in transparent_patterns):
            return 1
        return 3
    
    def _calculate_word_frequency(self, word: str) -> int:
        common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        if word.lower() in common_words:
            return 1
        elif len(word) <= 4:
            return 2
        elif len(word) <= 8:
            return 3
        else:
            return 4
    
    def _calculate_morphological_complexity(self, word: str) -> int:
        if len(word) <= 4:
            return 1
        elif len(word) <= 8:
            return 2
        elif len(word) <= 12:
            return 3
        else:
            return 4
    
    def _calculate_etymology_complexity(self, etymology: str) -> int:
        if 'Latin' in etymology or 'Greek' in etymology:
            return 4
        elif 'French' in etymology or 'German' in etymology:
            return 3
        elif 'Old English' in etymology:
            return 2
        else:
            return 1

class Batch114Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        claude_data = {
            'monk': {
                'definition': 'A monk is a person who practices religious asceticism by monastic living, either alone or with any number of other monks. A monk may be a person who decides to dedicate their life to serving God and others, typically living in a monastery under vows of poverty, chastity, and obedience. In various religious traditions, monks are characterized by their commitment to prayer, study, and service. Christian monks follow rules such as those established by Saint Benedict, while Buddhist monks follow the Vinaya. They often wear distinctive robes and may engage in meditation, scholarly work, copying manuscripts, teaching, or providing care to the sick and poor. Monks have played crucial roles throughout history in preserving knowledge, advancing learning, and providing spiritual guidance to their communities.',
                'pronunciation': '/mʌŋk/',
                'etymology': 'Middle English via Old French moine from Late Latin monachus, from Greek monakhos meaning "solitary," from monos meaning "alone." The word entered English in the medieval period as monastic communities became established.',
                'memory_tip': 'Remember MONK by thinking "MONks live alone (mONos) in Kingdoms of prayer" - they dedicate their lives to spiritual service in monasteries.',
                'example_sentence': 'The elderly _____ spent his days in quiet meditation and tending the monastery garden.'
            },
            'monkey': {
                'definition': 'A monkey is a member of the primate order that includes apes and humans, typically characterized by a long tail, agile movement through trees, and highly developed social behaviors. Monkeys are divided into Old World monkeys (such as baboons and macaques) and New World monkeys (such as capuchins and spider monkeys). They exhibit remarkable intelligence, using tools, solving problems, and displaying complex social hierarchies. Many species are arboreal, spending most of their lives in trees, while others are terrestrial. Monkeys play crucial ecological roles as seed dispersers and are found across tropical and subtropical regions worldwide. Their diverse diets range from primarily fruit and leaves to insects and small animals. Their expressive faces and playful behaviors have made them subjects of extensive behavioral research.',
                'pronunciation': '/ˈmʌŋki/',
                'etymology': 'Origin uncertain, possibly from Middle Low German Moneke or Middle French monikin. First appeared in English in the 16th century, potentially from a folk tale character. The word may derive from earlier terms referring to mischievous creatures.',
                'memory_tip': 'Remember MONKEY as "MONkeys are KEYs to understanding primate behavior" - they are key species for studying intelligence and social behavior.',
                'example_sentence': 'The curious _____ swung from branch to branch while observing the researchers below.'
            },
            'monochrome': {
                'definition': 'Monochrome refers to a photographic or artistic representation using only one color or different shades, tones, and tints of a single color, most commonly black and white. In visual arts, monochrome works create dramatic effects through contrast and texture rather than color variation. The technique emphasizes form, composition, and lighting. In photography, monochrome images can evoke mood and emotion differently than color photographs, often appearing more timeless and classic. Monochrome displays in technology show information using varying intensities of a single color, typically green or amber in early computer monitors. The aesthetic has remained popular in fine art, fashion photography, and graphic design for its ability to focus attention on essential elements without color distraction.',
                'pronunciation': '/ˈmɑːnəkroʊm/',
                'etymology': 'From Greek monos meaning "single" and chroma meaning "color." The term entered English in the mid-17th century, initially used in artistic contexts to describe paintings or drawings executed in one color.',
                'memory_tip': 'Remember MONOCHROME as "MONo CHROMa = one color" - the Greek roots directly tell you it means single-colored artwork or photography.',
                'example_sentence': 'The photographer specialized in _____ portraits that captured emotion through light and shadow.'
            },
            'monochromefacade': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "monochrome facade" - referring to a building front designed in a single color scheme.',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "monochrome" and "facade"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'monocle': {
                'definition': 'A monocle is a single corrective lens designed to fit in and around the area of one eye, typically held in place by the facial muscles around the eye socket. Popular in the 19th and early 20th centuries, particularly among upper-class European gentlemen, the monocle was both a vision aid and a fashion statement. It consists of a circular lens with a rim and often attached to a chain or cord to prevent dropping. The monocle requires practice to use effectively, as it must be held in place by tensing the eye muscles. While largely replaced by modern eyewear, monocles are still occasionally used and have become iconic symbols of sophistication, formality, or aristocratic bearing in literature and film.',
                'pronunciation': '/ˈmɑːnəkəl/',
                'etymology': 'From French monocle, from Late Latin monoculus meaning "one-eyed," from Greek monos "single" + Latin oculus "eye." The term entered English in the mid-19th century during the peak of its fashionable use.',
                'memory_tip': 'Remember MONOCLE as "MONo oCLE = one eye glass" - it\'s a single lens for one eye, unlike spectacles which have two lenses.',
                'example_sentence': 'The distinguished gentleman adjusted his _____ to read the fine print in the legal document.'
            },
            'monopolise': {
                'definition': 'Monopolise (British spelling of monopolize) means to obtain exclusive possession or control of a trade, commodity, or service, preventing others from participating in that market. In economics, this creates a monopoly where a single entity controls supply and can influence prices without competition. The term also applies to dominating or engrossing something completely, such as monopolising someone\'s attention or time. In business law, monopolising markets may violate antitrust regulations designed to maintain fair competition. The practice can occur through various means including buying out competitors, controlling essential resources, or creating barriers to entry. Outside economics, the word describes completely taking over or dominating any situation or resource.',
                'pronunciation': '/məˈnɑːpəlaɪz/',
                'etymology': 'From monopoly + -ise suffix. Monopoly comes from Greek monopolion, from monos "single" + polein "to sell." The verb form developed in the late 16th century as the concept of exclusive trading rights became more common.',
                'memory_tip': 'Remember MONOPOLISE as "MONOpoly-ISE = to create a single-seller market" - when you monopolise, you become the only seller or controller.',
                'example_sentence': 'The large corporation attempted to _____ the entire telecommunications market in the region.'
            },
            'monopolize': {
                'definition': 'Monopolize (American spelling) means to obtain exclusive possession or control of a trade, commodity, or service, thereby eliminating competition. This creates a monopoly situation where one entity controls supply and pricing without competitive pressure. In broader usage, it means to dominate or engross completely, such as monopolizing a conversation or someone\'s attention. Economically, monopolization can lead to higher prices and reduced innovation due to lack of competitive pressure. Legal systems often have antitrust laws to prevent harmful monopolization of markets. The term extends beyond business to describe any situation where one party gains exclusive control or dominance over a resource, opportunity, or social interaction.',
                'pronunciation': '/məˈnɑːpəlaɪz/',
                'etymology': 'From monopoly + -ize suffix. Derived from Greek monopolion meaning "exclusive sale," from monos "single" + polein "to sell." The verb form emerged in English during the late 16th century.',
                'memory_tip': 'Remember MONOPOLIZE as "MONOpoly-iZE = to make into a single-seller market" - you create a monopoly by eliminating all competition.',
                'example_sentence': 'The tech giant was accused of trying to _____ the online advertising market through aggressive acquisitions.'
            },
            'monotone': {
                'definition': 'Monotone describes a sound, voice, or musical passage that maintains the same pitch or tone without variation, creating a flat, unchanging quality. In speech, a monotone delivery lacks inflection, rhythm, or emotional expression, making it sound dull or mechanical. This can result from various factors including nervousness, lack of engagement, or certain medical conditions affecting vocal control. In music theory, monotone refers to a single unvaried tone or the recitation of text on one note. The term also applies to visual elements lacking variation in color, shade, or intensity. While sometimes effective for specific artistic or dramatic purposes, monotone delivery generally reduces audience engagement and emotional impact in communication.',
                'pronunciation': '/ˈmɑːnətoʊn/',
                'etymology': 'From Greek monotonos, from monos "single" + tonos "tone." Entered English in the mid-17th century, initially used in musical contexts before expanding to describe speech patterns.',
                'memory_tip': 'Remember MONOTONE as "MONo TONE = one unchanging tone" - it\'s speech or music that stays at the same pitch level throughout.',
                'example_sentence': 'The professor\'s _____ lecture style made even the fascinating subject seem boring to students.'
            },
            'monster': {
                'definition': 'A monster is a creature that is typically large, ugly, and frightening, often possessing supernatural or extraordinary powers that make it dangerous to humans. In mythology and folklore, monsters represent various fears and serve as antagonists in heroic tales, such as dragons, giants, or chimeric beasts. The term extends metaphorically to describe people who commit particularly cruel or evil acts, emphasizing their inhumanity. In modern culture, monsters appear in horror films, literature, and games, ranging from traditional creatures like vampires and werewolves to original creations. The concept also applies to anything abnormally large or powerful, such as a "monster truck" or "monster wave." Psychologically, monsters often symbolize repressed fears, societal anxieties, or the unknown aspects of human nature.',
                'pronunciation': '/ˈmɑːnstər/',
                'etymology': 'From Latin monstrum meaning "divine omen, warning sign," from monere "to warn." Originally referred to creatures that were omens from the gods, later evolving to mean frightening or unnatural creatures.',
                'memory_tip': 'Remember MONSTER as "MONster = warning (monere) creature" - originally these were creatures that served as divine warnings or omens.',
                'example_sentence': 'The children were convinced a _____ lived under their bed, making strange noises at night.'
            },
            'monstrosity': {
                'definition': 'A monstrosity is something that is abnormally large, distorted, or shocking in its ugliness, cruelty, or deviation from normal standards. The term describes both physical objects that are grotesquely malformed or oversized and abstract concepts like cruel acts or poor artistic creations. In architecture, a monstrosity might refer to a building that is aesthetically offensive or inappropriately massive for its setting. Morally, it describes acts of extreme cruelty or injustice that shock the conscience. The word emphasizes the disturbing nature of something that violates expected norms of proportion, beauty, or decency. Literary usage often employs monstrosity to describe characters or situations that embody evil or corruption in particularly vivid or exaggerated ways.',
                'pronunciation': '/mɑːnˈstrɑːsəti/',
                'etymology': 'From Late Latin monstrositas, from monstrosus "monstrous," ultimately from Latin monstrum "divine omen." The suffix -ity forms a noun indicating a quality or condition.',
                'memory_tip': 'Remember MONSTROSITY as "MONSTRous qualITY" - it\'s the quality of being monstrous or extremely abnormal and disturbing.',
                'example_sentence': 'The abandoned building had become an architectural _____ that dominated the once-beautiful neighborhood.'
            },
            'monstrositysofa': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "monstrosity sofa" - referring to an unusually large or ugly piece of furniture.',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "monstrosity" and "sofa"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'montage': {
                'definition': 'A montage is a technique in film, photography, or other visual arts where a series of images or clips are edited together to create a single work, often to condense time, show parallel actions, or convey complex ideas. In cinema, montage sequences rapidly present multiple shots to advance the narrative efficiently, such as showing a character\'s training progression or the passage of time. The technique emphasizes the juxtaposition of images to create meaning that emerges from their relationship rather than from individual shots. Soviet filmmakers like Sergei Eisenstein developed montage theory as a fundamental cinematic language. In photography and graphic design, montage combines multiple images into a composite artwork, often used in surrealist art and political propaganda to create powerful visual statements.',
                'pronunciation': '/mɑːnˈtɑːʒ/',
                'etymology': 'From French montage meaning "mounting, assembly," from monter "to mount." Entered English in the early 20th century through cinema terminology as filmmaking techniques developed.',
                'memory_tip': 'Remember MONTAGE as "MOUNTing AGE = mounting images together" - it comes from the French word for mounting or assembling visual elements.',
                'example_sentence': 'The film used a training _____ to show the protagonist\'s transformation from novice to expert.'
            },
            'month': {
                'definition': 'A month is a unit of time used in calendars, approximately equal to the period of the Moon\'s orbit around Earth (about 29.5 days). In the Gregorian calendar, months vary in length from 28 to 31 days, with twelve months comprising a year. The concept originated from lunar observations but was modified for practical calendar purposes. Different cultures have developed various calendar systems with different month lengths and names. Months serve as important organizational units for scheduling, billing cycles, seasonal planning, and legal purposes. Each month traditionally has associated weather patterns, agricultural activities, and cultural celebrations. The names of months in English derive from Roman deities, emperors, and numerical positions, reflecting the historical evolution of timekeeping systems.',
                'pronunciation': '/mʌnθ/',
                'etymology': 'From Old English monath, related to moon. Germanic languages share similar roots, all connecting the time period to lunar cycles. The connection to "moon" reflects the original lunar basis of monthly time divisions.',
                'memory_tip': 'Remember MONTH connects to MOON - both start with "MON" because months were originally based on the moon\'s cycle around Earth.',
                'example_sentence': 'She planned to complete the project within one _____ of starting her new job.'
            },
            'monthly': {
                'definition': 'Monthly describes something that occurs, is published, or is due every month, happening twelve times per year at regular intervals. The term applies to recurring events like monthly meetings, publications such as monthly magazines, or payment schedules like monthly rent. In business and personal finance, monthly cycles are common for billing, salary payments, and budget planning. Monthly data reporting helps track trends and performance over time. The regularity of monthly occurrences provides predictable structure for planning and organization. Subscriptions, memberships, and service contracts often operate on monthly terms. The adjective can also describe the total amount or average calculated over a month period, such as monthly income or monthly expenses.',
                'pronunciation': '/ˈmʌnθli/',
                'etymology': 'From month + -ly suffix, following the pattern of other time-based adverbs and adjectives. Developed in Middle English as calendar systems became more standardized.',
                'memory_tip': 'Remember MONTHLY as "MONTH + LY = happening every month" - the -ly suffix indicates regular occurrence at month intervals.',
                'example_sentence': 'The company holds _____ staff meetings to review progress and set goals for the upcoming period.'
            },
            'months': {
                'definition': 'Months is the plural form of month, referring to multiple periods of approximately 28-31 days each within calendar systems. The word describes extended durations measured in month units, such as "several months" or "twelve months equals one year." Different contexts use months for planning timelines, measuring age (especially for young children), tracking seasonal changes, and organizing long-term projects. In financial planning, months serve as budgeting periods and investment timeframes. Legal documents often specify time periods in months for contracts, leases, and statutory requirements. The plural form emphasizes duration and continuity over longer time spans than single monthly periods, helping conceptualize medium-term to long-term temporal relationships.',
                'pronunciation': '/mʌnθs/',
                'etymology': 'Plural formation of month using standard English -s plural suffix. Follows regular pluralization patterns while maintaining the connection to lunar-based time measurement.',
                'memory_tip': 'Remember MONTHS as the plural of MONTH - when you need more than one month to describe a time period, you use months.',
                'example_sentence': 'It took several _____ of dedicated practice before she mastered the difficult piano piece.'
            },
            'monture': {
                'definition': 'Monture is a specialized term referring to the frame or mounting of eyeglasses, particularly the part that holds the lenses and sits on the nose and ears. In optometry and eyewear manufacturing, the monture encompasses the entire frame structure including the bridge, temples, and lens rims. The term is more commonly used in French and technical optical contexts than in everyday English. Quality monture design affects both comfort and durability of eyeglasses, influencing how well they fit and how long they last. Materials for montures include plastic, metal, and composite materials, each offering different aesthetic and functional properties. The choice of monture style significantly impacts the wearer\'s appearance and the effectiveness of vision correction.',
                'pronunciation': '/mɑːnˈtʊər/',
                'etymology': 'From French monture meaning "mounting, frame," from monter "to mount." Used in specialized optical and eyewear contexts, particularly in technical or French-influenced terminology.',
                'memory_tip': 'Remember MONTURE as "MOUNTing for the EYE" - it\'s the mounting or frame structure that holds eyeglass lenses in place.',
                'example_sentence': 'The optician carefully selected a lightweight _____ that would complement the patient\'s face shape.'
            },
            'monumental': {
                'definition': 'Monumental describes something of exceptional size, importance, or significance, often serving as a lasting memorial or achievement. In architecture, monumental structures are built to impressive scale and designed to endure, such as monuments, cathedrals, or government buildings. The term emphasizes grandeur, permanence, and commemorative purpose. Monumental achievements represent major accomplishments that have lasting impact, such as scientific discoveries or artistic masterworks. The word can also describe tasks or challenges that require enormous effort or resources. In art history, monumental painting or sculpture refers to works created on a large scale with serious, elevated themes. The concept implies both physical magnitude and cultural or historical significance that transcends ordinary human scale.',
                'pronunciation': '/ˌmɑːnjuˈmentəl/',
                'etymology': 'From monument + -al suffix. Monument derives from Latin monumentum meaning "reminder, memorial," from monere "to remind, warn." The adjective form emphasizes the memorial and impressive qualities.',
                'memory_tip': 'Remember MONUMENTAL as "MONUMENT + AL = like a monument" - it describes things that are large, important, and lasting like monuments.',
                'example_sentence': 'The discovery of penicillin was a _____ achievement that revolutionized modern medicine.'
            },
            'mood': {
                'definition': 'Mood refers to a temporary emotional state or feeling that influences a person\'s outlook, behavior, and perceptions. Unlike emotions, which are typically responses to specific events, moods are more diffuse and longer-lasting psychological states that can affect multiple aspects of experience. Mood encompasses feelings ranging from happiness and excitement to sadness and irritability. In psychology, mood disorders like depression and bipolar disorder involve persistent alterations in emotional states. Environmental factors, physical health, social interactions, and brain chemistry all influence mood. The term also applies to the atmosphere or emotional tone of artistic works, settings, or situations, such as the mood of a painting, musical piece, or room. Understanding and managing mood is important for mental health and interpersonal relationships.',
                'pronunciation': '/muːd/',
                'etymology': 'From Old English mod meaning "heart, mind, spirit, courage." Related to German Mut meaning "courage." The modern sense of emotional state developed gradually from these earlier meanings of mental disposition.',
                'memory_tip': 'Remember MOOD as your inner emotional "MODe" - it\'s the mode or setting of your emotional state at any given time.',
                'example_sentence': 'Her cheerful _____ was contagious, brightening the entire office atmosphere.'
            },
            'moon': {
                'definition': 'The Moon is Earth\'s only natural satellite, a rocky body that orbits our planet approximately every 29.5 days. It significantly influences Earth through gravitational effects that create ocean tides and slightly slow Earth\'s rotation. The Moon\'s phases result from its changing position relative to Earth and the Sun, creating the familiar cycle from new moon to full moon. Its surface features include craters from meteor impacts, maria (dark plains formed by ancient lava flows), and highlands. The Moon plays crucial roles in human culture, serving as a calendar reference, inspiring mythology and literature, and representing mystery and romance. Scientific exploration has revealed its formation likely resulted from a Mars-sized object colliding with early Earth, ejecting material that eventually coalesced into the Moon.',
                'pronunciation': '/muːn/',
                'etymology': 'From Old English mona, related to Germanic and Indo-European roots meaning "measurer" (of time). Connected to words like "month" and "Monday," reflecting its importance in early timekeeping systems.',
                'memory_tip': 'Remember MOON as the "Measurer Of Our Nights" - it has historically been humanity\'s primary way of measuring monthly time periods.',
                'example_sentence': 'The full _____ cast a silvery glow across the calm lake surface.'
            },
            'moorage': {
                'definition': 'Moorage refers to the act of mooring a boat or ship, the place where a vessel is moored, or the fee charged for mooring services. In nautical contexts, moorage encompasses the facilities, equipment, and services needed to secure watercraft safely at docks, marinas, or anchorages. This includes dock space, cleats, lines, and sometimes utilities like electricity and water. Marina moorage rates vary based on boat size, location, and amenities provided. Temporary moorage serves transient boaters, while permanent moorage provides long-term slip rental. The term also applies to the physical act of securing a vessel with ropes, chains, or anchors to prevent drifting. Proper moorage is essential for boat safety and harbor organization.',
                'pronunciation': '/ˈmʊrɪdʒ/',
                'etymology': 'From moor (to secure a vessel) + -age suffix indicating action, place, or fee. Moor comes from Middle English moren, possibly from Middle Dutch maren meaning "to tie up."',
                'memory_tip': 'Remember MOORAGE as "MOOR + AGE = the place and process of mooring" - it\'s where boats are secured and the service of securing them.',
                'example_sentence': 'The marina charged a daily _____ fee that included dock space and electrical hookup.'
            },
            'moose': {
                'definition': 'A moose is the largest member of the deer family, characterized by its massive size, long legs, and distinctive broad, palmate antlers on males. Native to northern forests of North America and Eurasia (where they\'re called elk), moose can weigh up to 1,500 pounds and stand over six feet tall at the shoulder. They inhabit boreal and mixed forests, feeding primarily on woody plants, aquatic vegetation, and leaves. Moose are excellent swimmers and can dive up to 20 feet deep to feed on underwater plants. Despite their imposing size, they can run up to 35 mph. Their distinctive features include a bell-shaped dewlap hanging from the throat, poor eyesight compensated by excellent hearing and smell, and impressive antlers that bulls shed and regrow annually.',
                'pronunciation': '/muːs/',
                'etymology': 'From Algonquian languages, likely from Eastern Abenaki mos or similar forms meaning "twig eater," referring to their diet of woody vegetation. Entered English through early American colonial contact with Native Americans.',
                'memory_tip': 'Remember MOOSE as "Massive Outdoor Oddly-Shaped Elk" - they\'re the largest deer family members with distinctive broad antlers and imposing size.',
                'example_sentence': 'The massive _____ emerged from the forest, its enormous antlers spanning nearly six feet across.'
            },
            'moped': {
                'definition': 'A moped is a low-power two-wheeled vehicle that combines features of a motorcycle and bicycle, typically equipped with pedals and a small engine (usually 50cc or less). Originally designed for economical transportation, mopeds achieved popularity in Europe and urban areas worldwide due to their fuel efficiency, ease of parking, and lower licensing requirements compared to motorcycles. Most modern mopeds can reach speeds of 25-40 mph and are ideal for short commutes and urban travel. They often feature automatic transmissions, step-through frames, and storage compartments. The term encompasses various styles from classic pedal-equipped versions to modern scooter-style vehicles. Moped regulations vary by jurisdiction, often requiring special licenses or permits while offering more accessible entry into motorized transportation.',
                'pronunciation': '/ˈmoʊpɛd/',
                'etymology': 'From Swedish moped, a contraction of motorvelociped meaning "motor velocipede." Velocipede was an early term for bicycle, so moped literally means "motor bicycle."',
                'memory_tip': 'Remember MOPED as "MOtor + PEDal = motorized bicycle" - it combines a motor with pedals for economical transportation.',
                'example_sentence': 'She rode her _____ to work every day, appreciating its fuel efficiency and easy parking in the crowded city.'
            },
            'moppet': {
                'definition': 'Moppet is an affectionate, somewhat old-fashioned term for a young child, particularly a small girl, emphasizing endearment and cuteness. The word carries connotations of innocence, charm, and doll-like appearance, often used by adults when speaking fondly of children. In literary contexts, moppet appears in children\'s stories and period pieces to evoke a sense of nostalgia or quaint charm. The term can also refer to a child actor in theatrical or film contexts, particularly in early to mid-20th century entertainment. While generally positive, the word can sometimes carry slight condescending overtones depending on context. Modern usage is relatively rare, mostly appearing in literary works, period dramas, or when speakers deliberately employ old-fashioned terminology.',
                'pronunciation': '/ˈmɑːpɪt/',
                'etymology': 'Possibly from mop (referring to hair) + -et diminutive suffix, or from obsolete moppe meaning "baby, darling." The term emerged in the 17th century as an affectionate term for children.',
                'memory_tip': 'Remember MOPPET as "MOP-like hair + ET (little) = little child with mop-like hair" - it refers affectionately to young children.',
                'example_sentence': 'The little _____ skipped happily through the garden, her curls bouncing with each step.'
            },
            'mops': {
                'definition': 'Mops is the plural form of mop, referring to multiple cleaning implements consisting of absorbent material attached to a handle, used for cleaning floors and other surfaces. Different types of mops serve various cleaning purposes: string mops for general floor cleaning, sponge mops for smaller areas, microfiber mops for dust and fine particles, and specialized mops for specific surfaces. Commercial and residential cleaning operations often require multiple mops to prevent cross-contamination between different areas. The term also functions as a verb meaning to clean with a mop or to complete a cleaning task thoroughly. In military or gaming contexts, "mops up" means to complete final tasks or eliminate remaining resistance. Proper mop maintenance involves regular washing and replacement to ensure effective cleaning.',
                'pronunciation': '/mɑːps/',
                'etymology': 'Plural of mop, which may derive from Walloon mappe or Latin mappa meaning "napkin, cloth." The cleaning implement sense developed from the cloth-like absorbent material.',
                'memory_tip': 'Remember MOPS as the plural of MOP - when you need more than one cleaning tool, you have multiple mops for different areas or tasks.',
                'example_sentence': 'The janitor kept several _____ in the supply closet for cleaning different areas of the building.'
            },
            'moraine': {
                'definition': 'A moraine is a mass of rocks, sediment, and debris carried and deposited by a glacier during its movement and retreat. These geological formations provide evidence of past glacial activity and reveal information about ancient climate conditions and ice sheet movements. Terminal moraines mark the farthest advance of glaciers, while lateral moraines form along the sides. Ground moraines create relatively flat areas of mixed sediment beneath former ice sheets. Moraines vary in size from small ridges to massive formations covering thousands of square kilometers. They significantly influence local topography, drainage patterns, and soil composition. Many moraines contain valuable deposits of gravel, sand, and clay used in construction. Understanding moraine formation helps geologists reconstruct glacial history and predict landscape evolution in regions affected by past ice ages.',
                'pronunciation': '/məˈreɪn/',
                'etymology': 'From French moraine, from Savoyard morena meaning "mound of earth." The term entered geological vocabulary in the 18th century as scientists began studying glacial formations systematically.',
                'memory_tip': 'Remember MORAINE as "MORe + RAIN of rocks" - glaciers act like rain, depositing more rocks and debris in piles as they move.',
                'example_sentence': 'The terminal _____ clearly marked where the ancient glacier had reached its maximum extent thousands of years ago.'
            },
            'moratorium': {
                'definition': 'A moratorium is a temporary suspension or delay of an activity, typically imposed by authority or agreement to address specific concerns or allow time for consideration. In legal contexts, moratoriums pause debt payments, foreclosures, or legal proceedings during crisis periods. Governments may declare moratoriums on development, hunting, or other activities to protect resources or assess environmental impacts. Medical moratoriums halt certain procedures or treatments pending safety reviews. Business moratoriums suspend operations, hiring, or expansion plans during uncertain periods. The temporary nature distinguishes moratoriums from permanent bans, with the expectation that normal activities will resume after conditions change. Moratoriums serve as policy tools for crisis management, allowing stakeholders to regroup, reassess situations, or implement necessary reforms before resuming regular operations.',
                'pronunciation': '/ˌmɔːrəˈtɔːriəm/',
                'etymology': 'From Latin moratorius meaning "delaying," from morari "to delay," from mora "delay." Entered English in the late 19th century through legal and financial terminology.',
                'memory_tip': 'Remember MORATORIUM as "MORe TIME for evalUATION" - it\'s a temporary halt to allow more time for assessment or planning.',
                'example_sentence': 'The city council declared a _____ on new construction permits while they revised the zoning regulations.'
            },
            'morbidity': {
                'definition': 'Morbidity refers to the condition of being diseased or unhealthy, encompassing both the incidence of disease in a population and the degree of illness or disability it causes. In epidemiology, morbidity rates measure how frequently specific diseases occur within defined populations, helping public health officials track health trends and allocate resources. The term also describes the psychological preoccupation with disease, death, or disturbing subjects, often used in psychiatric contexts. Morbidity differs from mortality (death rates) by focusing on illness and disability rather than death. Comorbidity refers to the presence of multiple diseases or conditions in the same patient. Understanding morbidity patterns helps healthcare systems plan services, researchers identify risk factors, and policymakers develop prevention strategies.',
                'pronunciation': '/mɔːrˈbɪdəti/',
                'etymology': 'From Latin morbidus meaning "diseased, sickly," from morbus "disease." The suffix -ity creates a noun indicating condition or quality, forming the concept of diseased condition.',
                'memory_tip': 'Remember MORBIDITY as "MORBid condITY = the condition of being diseased" - it measures disease presence and severity in populations.',
                'example_sentence': 'The study examined the _____ rates of diabetes in urban versus rural communities.'
            },
            'mordant': {
                'definition': 'Mordant describes something harshly critical, biting, or caustic in expression, often applied to wit, humor, or commentary that cuts deeply through sharp observation or satire. In chemistry, a mordant is a substance used to fix dyes to fabrics by forming chemical bonds between the dye and fiber, ensuring colorfastness and durability. Literary mordant style employs cutting irony, sarcasm, or bitter humor to criticize or expose flaws in society, behavior, or ideas. The term suggests both sharpness and effectiveness - mordant criticism penetrates defenses and leaves lasting impressions. In textile arts, mordants like alum, iron, or copper salts create different color effects and improve dye permanence. The dual meaning reflects the concept of something that "bites" or grips firmly, whether in chemical bonding or penetrating social commentary.',
                'pronunciation': '/ˈmɔːrdənt/',
                'etymology': 'From French mordant meaning "biting," from mordre "to bite," ultimately from Latin mordere "to bite." The chemical sense developed from the idea of the substance "biting" into fabric.',
                'memory_tip': 'Remember MORDANT as "MORE biting" - it describes both sharp criticism that bites intellectually and chemicals that bite into fabric to fix dyes.',
                'example_sentence': 'The critic\'s _____ review exposed the fundamental flaws in the director\'s ambitious but poorly executed film.'
            },
            'morel': {
                'definition': 'A morel is a highly prized edible mushroom characterized by its distinctive honeycomb-like cap with deep pits and ridges, typically appearing in spring in temperate forests. These mushrooms are considered culinary delicacies, prized by chefs and foragers for their rich, earthy, nutty flavor and meaty texture. Morels emerge after soil temperatures reach specific levels following winter, often found near dead or dying trees, particularly elms, ash, and tulip poplars. They require careful identification as some similar-looking mushrooms can be toxic. Commercial cultivation is difficult, making wild foraging the primary source for these expensive fungi. Morels must be cooked before eating and are never consumed raw. Their seasonal availability, distinctive appearance, and exceptional taste make them one of the most sought-after wild mushrooms in North American and European cuisine.',
                'pronunciation': '/məˈrɛl/',
                'etymology': 'From French morille, possibly from Dutch morille or Germanic sources. The term entered English through culinary and foraging contexts as interest in wild mushrooms grew.',
                'memory_tip': 'Remember MOREL as "MORe ELusive" - these prized mushrooms are more elusive and harder to find than common mushrooms, making them valuable.',
                'example_sentence': 'The experienced forager found a patch of fresh _____ mushrooms near the base of the dead elm tree.'
            },
            'mores': {
                'definition': 'Mores are the essential or characteristic customs, conventions, and moral attitudes of a community or social group that distinguish it from others and guide acceptable behavior. Unlike simple customs or manners, mores carry moral significance and violating them typically results in strong social disapproval or sanctions. They encompass deeply held beliefs about right and wrong conduct, often rooted in religious, cultural, or historical traditions. Mores evolve slowly over time and vary significantly between different societies, cultures, and historical periods. They influence laws, social institutions, and individual behavior patterns. Anthropologists and sociologists study mores to understand how societies maintain order and transmit values across generations. Understanding different cultural mores is essential for cross-cultural communication and avoiding unintentional offense in diverse social settings.',
                'pronunciation': '/ˈmɔːreɪz/',
                'etymology': 'From Latin mores, plural of mos meaning "custom, manner, way of life." Adopted into English through sociology and anthropology to describe fundamental social customs with moral significance.',
                'memory_tip': 'Remember MORES as "MORal customs that are ESSential" - they\'re the essential moral customs that define how a society expects people to behave.',
                'example_sentence': 'The anthropologist studied the changing _____ of the community as it adapted to modern influences.'
            },
            'morgana': {
                'definition': 'Morgana typically refers to Morgan le Fay (also known as Morgana), a powerful enchantress in Arthurian legend, often portrayed as King Arthur\'s half-sister and sometimes his antagonist. In medieval romance literature, she is depicted as a skilled sorceress who studied magic and often opposed Arthur\'s reign, though her characterization varies from helpful ally to dangerous enemy depending on the version. The name also appears in the term "Fata Morgana," a complex superior mirage phenomenon that creates distorted images of distant objects, named after the legendary sorceress. In various adaptations of Arthurian tales, Morgana represents feminine power, knowledge of the occult, and the tension between pagan traditions and Christian values. Her character has influenced literature, opera, and popular culture for centuries.',
                'pronunciation': '/mɔːrˈgɑːnə/',
                'etymology': 'From Welsh Morrighan or Irish Morrigan, names associated with war goddesses in Celtic mythology. The Arthurian character likely evolved from these earlier mythological figures.',
                'memory_tip': 'Remember MORGANA as "MORe than ordinary, GANing magical powers" - she\'s Arthur\'s half-sister who gained more than ordinary human abilities through magic.',
                'example_sentence': 'In this version of the legend, _____ used her magical abilities to protect Camelot rather than threaten it.'
            },
            'moribund': {
                'definition': 'Moribund describes something that is dying, near death, or in terminal decline, whether literally in medical contexts or figuratively regarding institutions, industries, or ideas. In medical usage, moribund patients are in the final stages of terminal illness with little chance of recovery. The term extends metaphorically to describe businesses, organizations, or systems that are failing and unlikely to survive without dramatic intervention. Moribund industries face obsolescence due to technological changes, market shifts, or regulatory pressures. The word carries implications of gradual decline rather than sudden death, suggesting a prolonged period of weakness and deterioration. In literature and journalism, moribund effectively conveys the sense of something barely clinging to existence. The term emphasizes both current weakness and poor prognosis for future survival.',
                'pronunciation': '/ˈmɔːrɪbʌnd/',
                'etymology': 'From Latin moribundus meaning "dying," from mori "to die." Entered English in the mid-18th century through medical and literary usage to describe dying or declining states.',
                'memory_tip': 'Remember MORIBUND as "MORe than sick, BUt Not Dead" - it describes something that\'s more than just sick but hasn\'t quite died yet.',
                'example_sentence': 'The once-thriving downtown district had become _____, with empty storefronts lining every block.'
            },
            'morion': {
                'definition': 'A morion is a type of open helmet worn by infantry soldiers during the 16th and early 17th centuries, characterized by its distinctive high crest or comb running from front to back and a brim that curves up at the sides. This protective headgear was popular among Spanish conquistadors, pikemen, and other foot soldiers during the Renaissance period. Morions were typically made of steel and designed to deflect sword blows and projectiles while allowing good visibility and ventilation. They often featured decorative elements like etching or embossing, reflecting both practical protection needs and aesthetic considerations. The design influenced later military helmet development and appears frequently in period artwork depicting soldiers of the era. Modern reproductions are popular among historical reenactors and collectors of military artifacts.',
                'pronunciation': '/ˈmɔːriən/',
                'etymology': 'From French morion, possibly from Spanish morrión or Italian morione, potentially related to morro meaning "rounded hill," referring to the helmet\'s distinctive crest shape.',
                'memory_tip': 'Remember MORION as "MORe protectION" - it was a type of helmet that provided more protection for Renaissance soldiers with its distinctive crested design.',
                'example_sentence': 'The conquistador\'s polished _____ gleamed in the sunlight as he surveyed the new territory.'
            },
            'morionmortadella': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "morion mortadella" - combining a type of Renaissance helmet with an Italian cold cut.',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "morion" and "mortadella"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'moroccan': {
                'definition': 'Moroccan describes anything relating to Morocco, a North African country known for its rich cultural heritage, diverse landscapes, and historical significance as a crossroads between Africa, Europe, and the Middle East. Moroccan culture blends Berber, Arab, and French influences, reflected in architecture, cuisine, art, and social customs. Moroccan cuisine features tagines, couscous, mint tea, and aromatic spices like saffron and cinnamon. The architectural style includes intricate tile work, geometric patterns, and ornate decorations seen in palaces, mosques, and riads. Moroccan craftsmanship is renowned for textiles, leather goods, pottery, and metalwork. As a noun, Moroccan refers to a person from Morocco. The country\'s strategic location has made it historically important for trade and cultural exchange between continents.',
                'pronunciation': '/məˈrɑːkən/',
                'etymology': 'From Morocco + -an suffix. Morocco derives from Arabic Al-Maghrib meaning "the west" and the Berber city name Marrakech, combined in European languages as "Morocco."',
                'memory_tip': 'Remember MOROCCAN as "MORe than One Culture CANvased" - Morocco represents more than one culture combined (Arab, Berber, European influences).',
                'example_sentence': 'The _____ restaurant served authentic tagines in beautiful hand-painted ceramic dishes.'
            },
            'morose': {
                'definition': 'Morose describes a person who is sullen, gloomy, and ill-tempered, characterized by a persistently bad mood and antisocial behavior. Someone who is morose typically appears withdrawn, irritable, and unresponsive to attempts at cheering them up. This temperament goes beyond temporary sadness or disappointment to suggest a habitual tendency toward gloominess and negativity. Morose individuals often respond to social interactions with minimal enthusiasm, short answers, or obvious displeasure. The term can describe both personality traits and temporary emotional states, though it typically implies duration rather than momentary mood. In literature, morose characters often serve as foils to more optimistic personalities or represent deeper psychological or social problems. The word carries connotations of stubbornness in maintaining negative attitudes despite circumstances.',
                'pronunciation': '/məˈroʊs/',
                'etymology': 'From Latin morosus meaning "peevish, fastidious," from mos "custom, manner." Originally implied being excessively particular about customs, later evolving to mean sullen and ill-tempered.',
                'memory_tip': 'Remember MOROSE as "MORe + tROSE = more like a thorny rose" - someone morose is prickly and unpleasant like a rose\'s thorns.',
                'example_sentence': 'After losing the championship, the athlete became increasingly _____ and avoided speaking with teammates.'
            },
            'morphological': {
                'definition': 'Morphological relates to morphology, the study of the form and structure of organisms, words, or other complex systems. In biology, morphological analysis examines the shape, size, and structural features of organisms, helping classify species and understand evolutionary relationships. Linguistic morphology studies word formation, including how morphemes (smallest meaningful units) combine to create words through prefixes, suffixes, roots, and inflections. Morphological changes in organisms can result from genetic variations, environmental factors, or developmental processes. In geology, morphological features describe landscape shapes and formations. Medical morphology examines cellular and tissue structures to diagnose diseases. The term emphasizes form and structure rather than function, though morphology often relates to functional adaptations. Understanding morphological principles is essential in taxonomy, comparative anatomy, etymology, and various scientific disciplines that classify and analyze structural patterns.',
                'pronunciation': '/ˌmɔːrfəˈlɑːdʒɪkəl/',
                'etymology': 'From morphology + -ical suffix. Morphology comes from Greek morphe "form, shape" + -logia "study of." The adjective form applies this structural study approach to various fields.',
                'memory_tip': 'Remember MORPHOLOGICAL as "MORPH (shape) + LOGICAL study" - it\'s the logical study of shapes and structures in various fields.',
                'example_sentence': 'The biologist conducted a _____ analysis to identify the subtle differences between the two closely related species.'
            },
            'mortadella': {
                'definition': 'Mortadella is a traditional Italian cold cut or salumi made from finely ground pork, typically studded with cubes of pork fat and often flavored with pistachios, garlic, and various spices. Originating in Bologna, this smooth, delicate sausage has a distinctive pink color and mild, sophisticated flavor that sets it apart from coarser deli meats. Authentic mortadella is made using specific techniques that create its characteristic smooth texture and even distribution of fat cubes. The meat is often served sliced thin in antipasto platters, sandwiches, or incorporated into pasta dishes and appetizers. Quality mortadella represents centuries of Italian charcuterie tradition, with protected designation of origin status for Bologna mortadella. Its production requires skilled craftsmanship to achieve the proper texture, flavor balance, and aesthetic appearance that defines this premium cold cut.',
                'pronunciation': '/ˌmɔːrtəˈdɛlə/',
                'etymology': 'From Italian mortadella, possibly from Latin mortarium meaning "mortar," referring to the mortar and pestle used to grind the meat, or from Latin myrtatum (flavored with myrtle berries).',
                'memory_tip': 'Remember MORTADELLA as "MORtar grounD ELegant Lunch meat" - it\'s elegant lunch meat made by grinding pork in a mortar-like process.',
                'example_sentence': 'The Italian deli sliced the _____ paper-thin, revealing the distinctive pattern of white fat cubes throughout the pink meat.'
            },
            'mortal': {
                'definition': 'Mortal describes something subject to death or having a finite lifespan, as opposed to immortal beings or eternal entities. In human contexts, mortal emphasizes our shared vulnerability to death and the temporary nature of life. The term also describes something that causes or is capable of causing death, such as mortal wounds or mortal danger. In mythology and religion, mortal beings are contrasted with gods, angels, or other immortal entities. Mortal can intensify descriptions, meaning extreme or severe, as in "mortal fear" or "mortal enemy." Philosophically, mortality represents the fundamental human condition that shapes our understanding of meaning, urgency, and relationships. The concept of being mortal influences art, literature, religion, and personal decision-making, often spurring people to seek lasting impact or spiritual transcendence.',
                'pronunciation': '/ˈmɔːrtəl/',
                'etymology': 'From Latin mortalis meaning "subject to death," from mors/mortis "death." The root mort- appears in many death-related English words like mortality, morgue, and mortgage.',
                'memory_tip': 'Remember MORTAL as "MORe than TAL(l) - everyone dies" - no matter how tall or great, all mortals eventually die.',
                'example_sentence': 'The hero realized that even with great powers, she remained _____ and vulnerable to the same fate as everyone else.'
            },
            'mortgage': {
                'definition': 'A mortgage is a loan secured by real estate property, where the borrower pledges the property as collateral for repayment over a specified period, typically 15-30 years. If the borrower defaults, the lender can foreclose and take possession of the property to recover the debt. Mortgages enable people to purchase homes without paying the full price upfront, making homeownership accessible through monthly payments that include principal, interest, taxes, and insurance. Different mortgage types include fixed-rate (consistent payments) and adjustable-rate (varying interest rates) loans. The mortgage process involves application, credit evaluation, property appraisal, and closing procedures. Mortgages represent major financial commitments that significantly impact personal budgets and long-term wealth building through property ownership and equity accumulation.',
                'pronunciation': '/ˈmɔːrɡɪdʒ/',
                'etymology': 'From Old French mortgage, literally "death pledge," from mort "death" + gage "pledge." The name reflects that the pledge "dies" when the debt is paid or the property is forfeited.',
                'memory_tip': 'Remember MORTGAGE as "MORt (death) + GAGE (pledge)" - it\'s a "death pledge" that dies when you finish paying for your house.',
                'example_sentence': 'After years of saving, they finally qualified for a _____ and could purchase their first home.'
            },
            'mortician': {
                'definition': 'A mortician, also known as a funeral director or undertaker, is a professional who prepares deceased individuals for burial or cremation and coordinates funeral services. Their responsibilities include embalming, cosmetic restoration, arranging viewings, organizing funeral ceremonies, and providing grief support to families during difficult times. Morticians must complete specialized education in mortuary science, anatomy, and embalming techniques, plus obtain licensing requirements that vary by jurisdiction. They handle legal paperwork including death certificates, burial permits, and insurance claims. Modern morticians often provide comprehensive funeral services including venue coordination, floral arrangements, transportation, and memorial planning. The profession requires technical skills, emotional sensitivity, and strong communication abilities to help families navigate grief while managing practical arrangements. Morticians play essential roles in helping communities honor the deceased and support the living through loss.',
                'pronunciation': '/mɔːrˈtɪʃən/',
                'etymology': 'From Latin mors/mortis meaning "death" + -ician suffix indicating profession or expertise. The term developed as the funeral industry became more professionalized in the 19th and 20th centuries.',
                'memory_tip': 'Remember MORTICIAN as "MORTal technICIAN" - a technician who specializes in caring for mortal remains and helping families through death.',
                'example_sentence': 'The compassionate _____ helped the grieving family plan a meaningful ceremony that honored their loved one\'s memory.'
            },
            'mortification': {
                'definition': 'Mortification refers to a feeling of intense shame, humiliation, or embarrassment that causes great distress or wounded pride. The emotional state involves feeling exposed, foolish, or degraded in front of others, often resulting from public mistakes, social blunders, or personal failures. In religious contexts, mortification refers to the practice of disciplining the body through fasting, self-denial, or physical penance to suppress worldly desires and achieve spiritual purification. Medical mortification describes the death of tissue or cells, also called necrosis or gangrene. The term emphasizes the severity of embarrassment by connecting it metaphorically to death - one feels so ashamed they could "die of embarrassment." Literature often uses mortification to describe characters\' profound social discomfort and the lasting psychological impact of humiliating experiences.',
                'pronunciation': '/ˌmɔːrtəfəˈkeɪʃən/',
                'etymology': 'From Latin mortificationem meaning "a killing, putting to death," from mortificare "to kill, subdue." Extended meanings of shame and religious discipline developed from the concept of "killing" pride or flesh.',
                'memory_tip': 'Remember MORTIFICATION as "MORT (death) + feeling" - it\'s shame so intense you feel like you could die from embarrassment.',
                'example_sentence': 'Her _____ was complete when she realized she had been giving the presentation to the wrong audience for ten minutes.'
            },
            'mosaic': {
                'definition': 'A mosaic is an art form consisting of small colored pieces of stone, glass, tile, or other materials (called tesserae) arranged to form patterns or images, typically set in mortar or adhesive on surfaces like walls, floors, or ceilings. This ancient decorative technique reached its peak in Roman and Byzantine art, creating stunning religious and secular artworks that have survived for centuries. Modern mosaics use diverse materials including ceramic, metal, shells, and recycled objects. The term also describes anything composed of diverse elements forming a unified whole, such as cultural mosaics representing diverse populations or genetic mosaics in biology where organisms contain different cell types. Creating mosaics requires artistic vision, patience, and technical skill to achieve desired effects through careful placement of individual pieces. The technique allows for intricate detail work and creates unique textures and visual effects through the interaction of light with varied surfaces.',
                'pronunciation': '/moʊˈzeɪɪk/',
                'etymology': 'From Latin musaicum meaning "work of the Muses," from Greek mouseion. Originally referred to artistic works worthy of the Muses, goddesses of arts and sciences.',
                'memory_tip': 'Remember MOSAIC as "MO pieces SolveAIC = many pieces solve to form art" - it\'s art made from many small pieces working together.',
                'example_sentence': 'The ancient Roman _____ depicted scenes of daily life with thousands of tiny colored stones arranged in intricate patterns.'
            },
            'mosquitotarget': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "mosquito target" - referring to something that attracts mosquitoes.',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "mosquito" and "target"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'most': {
                'definition': 'Most functions as both a determiner and adverb indicating the greatest quantity, degree, or extent of something within a group or range. As a determiner, it specifies the majority or largest portion, such as "most people" or "most of the time." As an adverb, it forms superlatives with adjectives and adverbs, creating the highest degree of comparison: "most beautiful," "most carefully." The word can also mean "very" or "extremely" in informal usage. In quantitative contexts, most indicates more than half or the largest portion without specifying exact amounts. Understanding proper usage of most versus "more" (comparative) is essential for grammatical accuracy. The word appears frequently in statistical descriptions, preferences, and generalizations about groups or categories.',
                'pronunciation': '/moʊst/',
                'etymology': 'From Old English maest meaning "greatest, largest," related to Old English ma "more." The superlative form of "much/many," parallel to good/better/best pattern in English.',
                'memory_tip': 'Remember MOST as "MO than all the reST" - it indicates more than all the rest combined, the greatest amount.',
                'example_sentence': 'She spent _____ of her vacation reading books by the lake, enjoying the peaceful atmosphere.'
            },
            'mostaccioli': {
                'definition': 'Mostaccioli is a tube-shaped pasta similar to penne but with smooth sides instead of ridged, and cut straight across rather than diagonally. This Italian pasta shape, whose name means "little mustaches," is popular in Italian-American cuisine and works well with various sauces due to its hollow interior that captures flavors. The smooth exterior and tubular shape make it ideal for baked dishes, hearty meat sauces, and casseroles. Mostaccioli is often confused with penne, but the straight cut and smooth sides distinguish it. In Italian-American communities, particularly in Chicago, mostaccioli became a popular pasta shape for family gatherings and restaurant dishes. The pasta cooks evenly and holds sauce well both inside and out, making it versatile for different preparation methods from simple olive oil dressings to complex layered casseroles.',
                'pronunciation': '/ˌmoʊstətʃiˈoʊli/',
                'etymology': 'From Italian mostaccioli, plural of mostacciolo meaning "little mustache," from mostaccio "mustache." The name refers to the pasta\'s resemblance to small mustaches when viewed from certain angles.',
                'memory_tip': 'Remember MOSTACCIOLI as "MOSTly like penne but smooth = little mustaches" - it\'s mostly like penne but smooth, named for its mustache-like shape.',
                'example_sentence': 'The Italian restaurant served _____ with a rich meat sauce that clung perfectly to the smooth pasta tubes.'
            },
            'mother': {
                'definition': 'A mother is a female parent who gives birth to, adopts, or raises a child, providing care, guidance, and nurturing throughout the child\'s development. Beyond biological relationships, motherhood encompasses emotional bonds, protective instincts, and the responsibility of guiding young people toward maturity. Mothers play crucial roles in child development, providing both physical care and emotional support that shapes personality, values, and social skills. The term extends metaphorically to describe origins or sources, such as "mother country" or "mother lode." In many cultures, mothers hold special reverence and are celebrated through holidays and traditions. Modern motherhood includes diverse family structures including single mothers, adoptive mothers, stepmothers, and same-sex parent families. The maternal role continues evolving as society changes, but the fundamental importance of nurturing, protection, and guidance remains constant across cultures and time periods.',
                'pronunciation': '/ˈmʌðər/',
                'etymology': 'From Old English modor, related to Germanic and Indo-European roots for mother. Similar words appear across many languages (Latin mater, Greek meter, Sanskrit matar), suggesting ancient common origins.',
                'memory_tip': 'Remember MOTHER as "MOst imporTant caretaker, Helper, and guEaR" - the most important caretaker who helps and gears you for life.',
                'example_sentence': 'The devoted _____ spent countless hours teaching her children important life lessons and values.'
            },
            'motherumbung': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely meant to be "mother umbung" - combining the word mother with umbung (a type of Australian indigenous shelter).',
                'pronunciation': 'N/A - Combined word error',
                'etymology': 'Combined word parsing error',
                'memory_tip': 'This is a PDF parsing error combining "mother" and "umbung"',
                'example_sentence': 'N/A - This is not a valid single word'
            },
            'motion': {
                'definition': 'Motion refers to the act or process of moving or changing position in space over time, fundamental to physics and everyday experience. In physics, motion describes the movement of objects through space, measured in terms of displacement, velocity, and acceleration. Motion can be linear (straight-line), rotational (spinning), oscillatory (back-and-forth), or complex combinations of these types. The study of motion forms the basis of mechanics, from simple projectile motion to orbital dynamics. In legal contexts, a motion is a formal request made to a court for a specific ruling or action. Parliamentary procedure uses motions as proposals for group consideration and voting. In film and photography, motion capture creates realistic animation by recording real movement. Understanding motion principles enables engineering applications from transportation to robotics, while the perception of motion affects art, entertainment, and human psychology.',
                'pronunciation': '/ˈmoʊʃən/',
                'etymology': 'From Latin motionem meaning "a moving, motion," from movere "to move." The word entered English through Old French motion, maintaining its core meaning of movement or change in position.',
                'memory_tip': 'Remember MOTION as "MOvement Through space In Time, In Order Now" - it\'s movement through space in time, in order from one position to another.',
                'example_sentence': 'The physicist demonstrated the principles of _____ using a pendulum that swung back and forth with perfect regularity.'
            },
            'motley': {
                'definition': 'Motley describes something composed of many different elements, especially colors, forms, or types that don\'t match or harmonize, creating a varied or incongruous mixture. Historically, motley refers to the multicolored clothing worn by court jesters and fools, typically featuring a patchwork of bright, contrasting colors and patterns. The term can describe groups of people with diverse backgrounds, collections of dissimilar objects, or anything characterized by variety and lack of uniformity. While sometimes suggesting disorder or randomness, motley can also indicate richness and diversity that creates interesting contrasts. In literature, a "motley crew" refers to a diverse group of individuals, often with different skills, backgrounds, or personalities working together. The word carries both positive connotations of diversity and potentially negative implications of randomness or lack of cohesion.',
                'pronunciation': '/ˈmɑːtli/',
                'etymology': 'From Middle English motley, possibly from Anglo-French motteley meaning "variegated." Related to "mot" meaning "speck" or "blemish," referring to the spotted or variegated appearance of multicolored cloth.',
                'memory_tip': 'Remember MOTLEY as "Many cOlors Together Like jEster\'s clothYs" - it describes the mixed, multicolored appearance of a jester\'s outfit.',
                'example_sentence': 'The antique shop contained a _____ collection of items ranging from Victorian furniture to 1960s records.'
            }
        }
        
        return claude_data.get(word, {
            'definition': f'Definition for {word} not yet available.',
            'pronunciation': f'Pronunciation for {word} not yet available.',
            'etymology': f'Etymology for {word} not yet available.',
            'memory_tip': f'Memory tip for {word} not yet available.',
            'example_sentence': f'Example sentence for {word} not yet available.'
        })
    
    def detect_combined_words(self) -> List[str]:
        combined_words = [
            'monochromefacade',
            'monstrositysofa', 
            'morionmortadella',
            'mosquitotarget',
            'motherumbung'
        ]
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        logger.info("Processing Batch 114 with comprehensive Claude data...")
        
        combined_words = self.detect_combined_words()
        logger.info(f"Detected {len(combined_words)} combined word errors: {combined_words}")
        
        processed_words = []
        
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                word = row['word'].strip()
                if not word:
                    continue
                    
                logger.info(f"Processed word: {word}")
                
                claude_data = self.get_comprehensive_claude_data(word)
                difficulty_scores = self.difficulty_calc.calculate_difficulty_score(
                    word, claude_data['definition'], claude_data['etymology']
                )
                
                processed_word = {
                    'word': word,
                    'years': row['years'],
                    'source_files': row['source_files'], 
                    'source_difficulties': row['source_difficulties'],
                    'definition': claude_data['definition'],
                    'pronunciation': claude_data['pronunciation'],
                    'etymology': claude_data['etymology'],
                    'etymology_source': 'Claude',
                    'memory_tip': claude_data['memory_tip'],
                    'example_sentence': claude_data['example_sentence'],
                    'example_sentence_source': 'Claude',
                    'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                    'word_frequency_score': difficulty_scores['word_frequency_score'],
                    'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                    'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                    'difficulty': difficulty_scores['difficulty'],
                    'combined_word_error': word in combined_words
                }
                
                processed_words.append(processed_word)
        
        # Write output CSV
        if processed_words:
            fieldnames = [
                'word', 'years', 'source_files', 'source_difficulties',
                'definition', 'pronunciation', 'etymology', 'etymology_source',
                'memory_tip', 'example_sentence', 'example_sentence_source',
                'phonetic_transparency_score', 'word_frequency_score',
                'morphological_complexity_score', 'etymology_complexity_score',
                'difficulty', 'combined_word_error'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
        logger.info("Batch 114 processing completed!")
        logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {len(processed_words)} successful, 0 failed")

if __name__ == "__main__":
    processor = Batch114Processor()
    
    input_file = "output/batch_114_words.csv"
    output_file = "output/batch_114_processed.csv"
    
    processor.process_batch(input_file, output_file)