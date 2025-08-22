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
    logging.info("Processing Batch 185 with comprehensive Claude data...")
    
    # Combined word errors detected in batch 185
    combined_errors = ['turkenriddance', 'tweeholiday', 'twinklesnicker', 'tympanumfisticuffs']
    
    # Comprehensive spelling bee data with Claude-generated educational content
    words_data = [
        {
            'word': 'turgor',
            'pronunciation': '/ˈtɜːrɡər/',
            'definition': 'Turgor is the pressure of cell contents against the cell wall in plant cells, bacteria, and fungi. This hydrostatic pressure is crucial for maintaining cell shape and providing structural support to plant tissues. When plants have adequate water, turgor pressure keeps leaves rigid and stems upright. During drought conditions, reduced turgor pressure causes wilting as cells lose their firmness. The process involves osmotic movement of water into cells, creating internal pressure that pushes against the cell wall.',
            'example_sentence': 'The botanist explained how _____ pressure keeps the flower petals firm and upright.',
            'etymology': 'From Latin "turgere" meaning "to swell" or "to be inflated," related to "turgidus" (swollen). The term entered English through scientific Latin in the 19th century as botanists developed understanding of plant physiology.',
            'etymology_source': 'Claude',
            'memory_tip': 'Remember "turgor" by thinking "TURn GORgeous" - when plants have proper turgor pressure, they turn gorgeous and upright, but without it they wilt.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'turken',
            'pronunciation': '/ˈtɜːrkən/',
            'definition': 'A turken is a hybrid bird created by crossing a turkey with a chicken, though such crosses are extremely rare and difficult to achieve due to genetic incompatibility. More commonly, the term refers to a breed of chicken called the Naked Neck or Transylvanian Naked Neck, which has a featherless neck resembling a turkey. These chickens originated in Transylvania and are known for their unusual appearance and heat tolerance. The naked neck trait is controlled by a dominant gene.',
            'example_sentence': 'The farmer was surprised to see a _____ strutting around the barnyard with its distinctive featherless neck.',
            'etymology': 'Blend of "turkey" + "chicken," created in English to describe this unusual hybrid or chicken breed. The term gained popularity in the 20th century among poultry enthusiasts.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TURKey chicKEN" - it\'s literally a combination of the two bird names, describing something that looks like both.',
            'phonetic_transparency': 4,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'turmeric',
            'pronunciation': '/ˈtɜːrmərɪk/',
            'definition': 'Turmeric is a golden-yellow spice derived from the rhizome of Curcuma longa, a plant in the ginger family. Native to Southeast Asia, turmeric has been used for thousands of years in cooking, traditional medicine, and as a dye. The active compound curcumin gives turmeric its distinctive color and potential anti-inflammatory properties. In cuisine, it\'s essential in curry powders and many Indian, Thai, and Middle Eastern dishes, providing both flavor and vibrant color.',
            'example_sentence': 'The chef added a pinch of _____ to the rice, turning it a beautiful golden color.',
            'etymology': 'From Middle English via Old French "terre merite" meaning "deserving earth," possibly influenced by Latin "terra merita." The word evolved through various European languages before reaching its modern English form.',
            'etymology_source': 'Claude',
            'memory_tip': 'Remember "TURn MERRY" + "IC" - turmeric turns food merry and golden, and it\'s terrific for health.',
            'phonetic_transparency': 2,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'turn',
            'pronunciation': '/tɜːrn/',
            'definition': 'Turn means to move in a circular direction wholly or partly around an axis or point, or to change direction or position. It can also mean to change in nature, state, form, or condition. As a noun, it refers to an act of moving something in a circular direction, a change of direction, or one\'s chance or opportunity to do something. The word has numerous applications from physical rotation to metaphorical changes in circumstances or fortune.',
            'example_sentence': 'Please _____ the page to continue reading the story.',
            'etymology': 'From Old English "turnian," from Latin "tornare" meaning "to turn on a lathe," from "tornus" (lathe), from Greek "tornos" (tool for drawing circles). The word has maintained its core meaning throughout centuries.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think of a "TURN table" - it literally turns around, just like the action the word describes.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'turning',
            'pronunciation': '/ˈtɜːrnɪŋ/',
            'definition': 'Turning refers to the action of moving something in a circular direction or changing direction. It can describe physical rotation, directional changes, or the process of transformation from one state to another. In manufacturing, turning is a machining process where a cutting tool removes material from a rotating workpiece. As a gerund, it often describes ongoing rotational motion or the act of changing course or direction.',
            'example_sentence': 'The car was _____ the corner when the traffic light changed to red.',
            'etymology': 'Present participle of "turn," from Old English "turnian," ultimately from Latin "tornare" meaning "to turn on a lathe." The -ing suffix creates the continuous action form.',
            'etymology_source': 'Claude',
            'memory_tip': 'Remember "TURN + ING" - it\'s simply the action of turn happening right now or continuously.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'turnip',
            'pronunciation': '/ˈtɜːrnɪp/',
            'definition': 'A turnip is a round, white-fleshed root vegetable with a purple or reddish top, belonging to the Brassica family along with cabbage and broccoli. Turnips have been cultivated for over 4,000 years and are grown worldwide as both human food and livestock feed. The entire plant is edible - the root can be eaten raw or cooked, while the leaves (turnip greens) are nutritious leafy vegetables. Turnips have a slightly peppery flavor when raw and become sweeter when cooked.',
            'example_sentence': 'The farmer harvested the _____ from the garden, noting their perfect purple and white coloring.',
            'etymology': 'From "turn" + "neep" (from Old English "næp," meaning turnip), referring to the rounded, turned shape of the vegetable. The word evolved in Middle English as farming terminology developed.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TURN + NIP" - the turnip has a rounded, turned shape and might give a little nip of peppery flavor.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'turns',
            'pronunciation': '/tɜːrnz/',
            'definition': 'Turns is the plural of turn, referring to multiple rotations, changes of direction, or opportunities. It can describe sequential rotations, alternating opportunities (as in "taking turns"), or multiple changes in direction or circumstances. In games and activities, turns represent each person\'s opportunity to participate. The word also describes multiple instances of circular motion or directional changes.',
            'example_sentence': 'The children were taking _____ on the playground swing.',
            'etymology': 'Plural form of "turn," from Old English "turnian," with the standard English plural suffix -s added to indicate multiple instances.',
            'etymology_source': 'Claude',
            'memory_tip': 'Simply "TURN" + "S" for plural - multiple turns or rotations happening.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 1
        },
        {
            'word': 'turophile',
            'pronunciation': '/ˈtʊrəfaɪl/',
            'definition': 'A turophile is a person who loves or has a great appreciation for cheese. This term describes cheese enthusiasts, connoisseurs, or collectors who have extensive knowledge about different varieties, production methods, aging processes, and flavor profiles of cheeses. Turophiles often seek out rare or artisanal cheeses, visit cheese shops and dairy farms, and can distinguish subtle differences between cheese types. The term encompasses both casual cheese lovers and serious cheese professionals.',
            'example_sentence': 'As a dedicated _____, she could identify the region and aging process of any cheese by taste alone.',
            'etymology': 'From Greek "turos" meaning "cheese" + "-phile" meaning "lover of." The term was coined in English to describe cheese enthusiasts, following the pattern of other -phile words.',
            'etymology_source': 'Claude',
            'memory_tip': 'Remember "TYRO (beginner) + PHILE (lover)" - but actually "TURO (cheese) + PHILE" - a cheese lover who started as a tyro but became expert.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'turpentine',
            'pronunciation': '/ˈtɜːrpənˌtaɪn/',
            'definition': 'Turpentine is a volatile essential oil obtained from the resin of pine trees, particularly longleaf pine, loblolly pine, and slash pine. It has been used for centuries as a solvent for paints and varnishes, in medicine, and as a cleaning agent. The production involves distilling pine resin to separate the volatile turpentine oil from the non-volatile rosin. Turpentine has a characteristic sharp, pine-like odor and is flammable. In art, it\'s commonly used to thin oil paints and clean brushes.',
            'example_sentence': 'The artist used _____ to thin the oil paint and achieve the desired consistency.',
            'etymology': 'From Old French "terebentine," from Latin "terebinthina," from Greek "terebinthos" (turpentine tree). The word evolved through various European languages as trade in this valuable substance spread.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TURbo PENTagon + INE" - turpentine cleans so fast it\'s like turbo speed, and it\'s made from pine trees.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'turpitude',
            'pronunciation': '/ˈtɜːrpɪˌtuːd/',
            'definition': 'Turpitude refers to depravity, wickedness, or moral corruption. It describes behavior that is fundamentally wrong, evil, or corrupt, often in a legal or ethical context. The term is frequently used in legal proceedings when describing crimes that involve moral depravity or dishonesty. Turpitude suggests not just wrongdoing, but actions that demonstrate a corrupt or depraved character. It\'s often seen in the phrase "moral turpitude," referring to conduct contrary to community standards of justice, honesty, or good morals.',
            'example_sentence': 'The judge considered the defendant\'s history of moral _____ when determining the sentence.',
            'etymology': 'From Latin "turpitudo" meaning "baseness, ugliness," from "turpis" (ugly, base, shameful). The word entered English through legal and scholarly Latin in the 15th century.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TURP (ugly) + ATTITUDE" - turpitude is having an ugly, morally corrupt attitude or behavior.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'turquois',
            'pronunciation': '/ˈtɜːrkɔɪz/',
            'definition': 'Turquois is an alternative spelling of turquoise, referring to a blue-green mineral used as a gemstone and ornamental stone. This copper aluminum phosphate mineral forms in arid regions and has been prized for jewelry and decoration for thousands of years. The stone ranges from sky blue to green, with the most valuable specimens showing a pure, intense blue color. Turquoise has significant cultural importance in many Native American traditions and was also valued by ancient Egyptians and Persians.',
            'example_sentence': 'The antique jewelry featured a beautiful _____ stone set in silver.',
            'etymology': 'Alternative spelling of "turquoise," from Old French "turqueise," meaning "Turkish stone," as it was originally imported to Europe through Turkey. The simpler spelling reflects phonetic preference.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TURK + QUOIS" - the Turkish stone with a distinctive blue-green color, spelled without the final -e.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'turquoise',
            'pronunciation': '/ˈtɜːrkɔɪz/',
            'definition': 'Turquoise is a blue-green mineral composed of copper aluminum phosphate, highly valued as a gemstone and ornamental material. Found primarily in arid regions, turquoise forms when copper-rich groundwater percolates through aluminum-rich rock. The stone has been treasured across cultures for over 7,000 years, from ancient Egyptian pharaohs to Native American tribes. Its color ranges from sky blue to apple green, with the finest specimens showing an intense, uniform blue. Beyond jewelry, turquoise is used in art, decoration, and has spiritual significance in many cultures.',
            'example_sentence': 'The Southwest landscape was perfectly complemented by her _____ and silver bracelet.',
            'etymology': 'From Old French "turqueise" meaning "Turkish stone," as Europeans first encountered this mineral through Turkish merchants. The stone actually originated from Persia and Central Asia.',
            'etymology_source': 'Claude',
            'memory_tip': 'Remember "TURK (Turkish) + QUOISE (noise)" - the Turkish traders made noise about this beautiful blue-green stone.',
            'phonetic_transparency': 2,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'turret',
            'pronunciation': '/ˈtɜːrɪt/',
            'definition': 'A turret is a small tower, typically forming part of a larger structure such as a castle, church, or modern building. In military architecture, turrets provided defensive positions and commanding views of surrounding areas. They can be round, square, or polygonal and may project from the wall or rise from within it. In naval and military contexts, a turret refers to a rotating armored structure containing guns. Modern buildings may feature decorative turrets as architectural elements.',
            'example_sentence': 'The medieval castle\'s _____ provided an excellent vantage point for spotting approaching enemies.',
            'etymology': 'From Old French "tourette," diminutive of "tour" (tower), from Latin "turris." The -et suffix indicates a smaller version of a tower.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TOUR + ET" - a turret is like a small tour (tower) where you can get a commanding view.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'turtle',
            'pronunciation': '/ˈtɜːrtəl/',
            'definition': 'A turtle is a reptile with a hard, protective shell covering its body, belonging to the order Testudines. Turtles have existed for over 200 million years, making them one of the oldest reptile groups. They are found in various environments including oceans, rivers, ponds, and land. Sea turtles migrate vast distances, while land turtles (tortoises) are adapted for terrestrial life. Their shells consist of a carapace (top) and plastron (bottom), and they can retract their heads and limbs for protection.',
            'example_sentence': 'The ancient _____ slowly made its way across the garden path.',
            'etymology': 'From Old English "turtle," possibly from Latin "tortuca," related to "tortus" (twisted), referring to the turtle\'s feet. The word has maintained its form across centuries.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TUR + TLE" - turtles turn slowly and have a shell that looks like a little bowl or tile.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'tusche',
            'pronunciation': '/ˈtʊʃə/',
            'definition': 'Tusche is a greasy liquid or solid drawing material used in lithography to create images on limestone or metal plates. This substance, containing grease or wax, is applied to the printing surface where ink is intended to adhere during the printing process. In lithographic printing, tusche works on the principle that oil and water repel each other. Artists use tusche to draw directly on the lithographic stone, and areas treated with tusche will accept ink while untreated areas will repel it, allowing for detailed printed reproductions.',
            'example_sentence': 'The printmaker carefully applied _____ to the lithographic stone to create the dark areas of the image.',
            'etymology': 'From German "Tusche" meaning "India ink" or "drawing ink," from French "touche." The word entered English through printmaking terminology in the 19th century.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TOUCH + E" - tusche is what you touch to the stone to make marks in lithography.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'tuschet',
            'pronunciation': '/ˈtʊʃɪt/',
            'definition': 'Tuschet is a variant or alternate form of tusche, referring to the same greasy drawing material used in lithography. Like tusche, tuschet is applied to lithographic stones or plates to create areas that will accept ink during the printing process. This material allows artists to draw directly on the printing surface, with the tuschet-treated areas becoming the printed image. The term may represent a regional or historical variation in printmaking terminology.',
            'example_sentence': 'The experienced lithographer preferred using _____ for its smooth application on the stone surface.',
            'etymology': 'Variant of "tusche," from German "Tusche" meaning India ink, possibly influenced by French pronunciation or regional dialect variations in printmaking communities.',
            'etymology_source': 'Claude',
            'memory_tip': 'Remember "TOUCH + ET" - similar to tusche, it\'s what you touch to the printing surface, with a slightly different ending.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'tussle',
            'pronunciation': '/ˈtʌsəl/',
            'definition': 'A tussle is a vigorous struggle or scuffle, typically involving physical contact but not necessarily violent. It can describe a brief fight, wrestling match, or energetic struggle between people or animals. Tussles are usually less serious than full fights, often involving pushing, grabbing, or wrestling rather than punching or serious violence. The word can also be used metaphorically to describe intense struggles or conflicts that don\'t involve physical contact, such as political or intellectual disputes.',
            'example_sentence': 'The two puppies had a playful _____ over the squeaky toy.',
            'etymology': 'Possibly from Middle English "tusshen," of uncertain origin, perhaps related to "tousle." The word appeared in English around the 15th century to describe physical struggles.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TOSS + EL" - in a tussle, people might toss each other around in a struggle.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'tussock',
            'pronunciation': '/ˈtʌsək/',
            'definition': 'A tussock is a dense clump or tuft of grass or other vegetation that grows in a compact, mounded form. These grass clumps are characteristic of certain ecosystems, particularly wetlands, prairies, and moorlands. Tussocks form when perennial grasses grow outward from a central point, creating distinctive mounds that can be several feet across. They provide important habitat for wildlife and help prevent soil erosion. The term also refers to specific grass species known for this growth pattern.',
            'example_sentence': 'The hiker carefully stepped from one grassy _____ to another while crossing the marsh.',
            'etymology': 'Of uncertain origin, possibly from Old English or Celtic roots. The word has been used in English since the 16th century to describe clumps of grass or vegetation.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TUSK + SOCK" - a tussock looks like a grass tuft that could hide a tusk, all bundled up like a sock.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'tutelage',
            'pronunciation': '/ˈtuːtəlɪdʒ/',
            'definition': 'Tutelage refers to protection, guidance, or instruction provided by a teacher, guardian, or mentor. It encompasses both the act of teaching and the state of being under someone\'s care or instruction. Tutelage implies a relationship where an experienced person guides a less experienced one, providing knowledge, skills, and wisdom. The term can apply to formal education, apprenticeships, mentoring relationships, or any situation where one person is learning under another\'s guidance and protection.',
            'example_sentence': 'Under her grandmother\'s _____, she learned the traditional art of quilting.',
            'etymology': 'From Latin "tutela" meaning "protection, guardianship," from "tutus" (safe, protected). The word entered English through French, maintaining its sense of protective guidance.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TUTOR + AGE" - tutelage is the age or period when you have a tutor guiding and protecting your learning.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'tutti',
            'pronunciation': '/ˈtuːti/',
            'definition': 'Tutti is a musical term meaning "all" or "everyone," indicating that all performers should play or sing together. In orchestral and choral music, tutti passages involve the full ensemble rather than solo sections or smaller groups. The term contrasts with solo passages where individual instruments or voices are featured. Tutti sections often provide climactic moments in compositions, showcasing the full power and range of the complete ensemble. The word appears in musical scores to guide conductors and performers.',
            'example_sentence': 'The symphony reached its climax during the powerful _____ section where all instruments played together.',
            'etymology': 'From Italian "tutti," plural of "tutto" meaning "all," from Latin "totus" (whole, entire). The term entered musical terminology directly from Italian.',
            'etymology_source': 'Claude',
            'memory_tip': 'Remember "TOOT + I" - when it\'s tutti, everyone toots their instruments, and "I" join in too.',
            'phonetic_transparency': 4,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'tuxedo',
            'pronunciation': '/tʌkˈsiːdoʊ/',
            'definition': 'A tuxedo is a formal evening suit for men, consisting of a black jacket with satin or grosgrain lapels, matching trousers with a satin stripe, and traditionally worn with a bow tie and cummerbund or vest. Also called a dinner jacket in British English, the tuxedo is appropriate for formal evening events, galas, and black-tie occasions. The style evolved from the tailcoat but is less formal, featuring a shorter jacket that doesn\'t have tails.',
            'example_sentence': 'He looked elegant in his black _____ as he prepared for the formal dinner.',
            'etymology': 'Named after Tuxedo Park, a resort community in New York where this style of formal wear was popularized in the 1880s by American socialites who adopted the British dinner jacket.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TUX + EDO" - tux is short for tuxedo, and "edo" sounds like "do" - what you do when you want to look formal.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'twain',
            'pronunciation': '/tweɪn/',
            'definition': 'Twain is an archaic or poetic word meaning "two" or "a pair." It\'s most commonly encountered in literature and traditional phrases, such as "never the twain shall meet," meaning two things will never come together or agree. The word has largely been replaced by "two" in modern usage but persists in certain expressions and literary contexts. Mark Twain famously used this word as his pen name, and it appears in various traditional sayings and proverbs.',
            'example_sentence': 'The old saying warns that never the _____ shall meet when describing two incompatible ideas.',
            'etymology': 'From Old English "twegen," the masculine form of "two." Related to Old Norse "tveir" and German "zwei," all from the same Indo-European root meaning "two."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWICE + MAIN" simplified to "TWAIN" - it means two, like twice, and it\'s the main old word for "two."',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'twang',
            'pronunciation': '/twæŋ/',
            'definition': 'Twang refers to a sharp, vibrating sound, often produced by plucking a taut string or similar object. It can describe the sound of a guitar string, bowstring, or rubber band when released. Twang also refers to a distinctive accent or manner of speaking, particularly associated with certain regional dialects that have a nasal quality. In music, twang characterizes the sound of certain instruments like banjos or the vocal style in country music.',
            'example_sentence': 'The guitar string made a sharp _____ when he plucked it too hard.',
            'etymology': 'Imitative word (onomatopoeia) representing the sound of a vibrating string or similar sharp, resonant noise. The word appeared in English around the 16th century.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think of the sound "TWANG" - it sounds exactly like what it describes, the sharp sound of a plucked string.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'twee',
            'pronunciation': '/twiː/',
            'definition': 'Twee describes something excessively sweet, quaint, or cute in a way that seems affected or overly sentimental. Originally British slang, the term often carries a slightly negative connotation, suggesting that something is trying too hard to be charming or is cute to an annoying degree. Twee can describe decorative styles, behavior, entertainment, or artistic works that are perceived as saccharine or overly precious. The word is commonly used in cultural criticism.',
            'example_sentence': 'The cottage\'s overly cute decorations struck her as rather _____.',
            'etymology': 'British baby-talk alteration of "sweet," representing the childish pronunciation. The word gained popularity in the mid-20th century as a way to describe excessive cuteness.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TOO WEE" - when something is too small, cute, and sweet, it becomes twee.',
            'phonetic_transparency': 4,
            'frequency': 2,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'twelve',
            'pronunciation': '/twɛlv/',
            'definition': 'Twelve is the number 12, representing the quantity that comes after eleven and before thirteen. It\'s significant in many cultural and mathematical contexts: there are twelve months in a year, twelve hours on a clock face, twelve apostles in Christian tradition, and twelve signs of the zodiac. Mathematically, twelve is highly composite, meaning it has more divisors than any smaller positive integer, making it useful for division and measurement systems.',
            'example_sentence': 'The clock struck _____ as midnight arrived.',
            'etymology': 'From Old English "twelf," related to Old Norse "tólf" and German "zwölf." The word literally means "two left" (over ten), from "twa" (two) + "lif" (left).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWO + ELVE" - it\'s two more than ten, or you can remember it\'s "twelve elves" in many fairy tales.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'twice',
            'pronunciation': '/twaɪs/',
            'definition': 'Twice means two times or on two occasions. It indicates that something happens, is done, or exists two times. The word can refer to frequency (how often something occurs), multiplication (two times a quantity), or repetition (doing something again). Twice is commonly used in mathematics, everyday speech, and instructions to specify that an action should be performed two times or that something occurs with a frequency of two.',
            'example_sentence': 'She checked her work _____ before submitting the important report.',
            'etymology': 'From Middle English "twies," from Old English "twiwa," meaning "two times." Related to "two" with the Old English suffix "-wa" indicating "times" or "ways."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWO + ICE" - if you want two ice cubes, you ask for them twice as much as one.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'twilight',
            'pronunciation': '/ˈtwaɪlaɪt/',
            'definition': 'Twilight is the soft, diffused light that occurs when the sun is below the horizon but its rays still illuminate the sky, creating the periods between day and night. There are three types: civil twilight (sun 0-6 degrees below horizon), nautical twilight (6-12 degrees), and astronomical twilight (12-18 degrees). Twilight occurs twice daily - evening twilight after sunset and morning twilight before sunrise. The word also metaphorically describes any period of decline or approaching end.',
            'example_sentence': 'They enjoyed their evening walk during the peaceful _____ hours.',
            'etymology': 'From Old English "twi-" (two, double) + "light," literally meaning "two lights" or the time between day and night when both light and darkness are present.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWI (two) + LIGHT" - twilight is when you have two kinds of light: the fading daylight and the emerging night.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'twinge',
            'pronunciation': '/twɪndʒ/',
            'definition': 'A twinge is a sudden, sharp, but usually brief pain or uncomfortable sensation. It often describes localized pain that comes and goes quickly, such as a muscle cramp, joint pain, or nerve irritation. Twinge can also refer to a sudden, brief feeling of emotion, such as guilt, regret, or anxiety. The word implies something that\'s temporary and acute rather than chronic or dull.',
            'example_sentence': 'She felt a sharp _____ in her back when she bent over to pick up the heavy box.',
            'etymology': 'From Old English "twengan" meaning "to pinch" or "to torment." The word evolved to describe sudden, sharp sensations, both physical and emotional.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWIN + GE" - a twinge is like a twin sensation that comes and goes quickly, giving you a brief "ge" (ouch).',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'twirled',
            'pronunciation': '/twɜːrld/',
            'definition': 'Twirled is the past tense of twirl, meaning to spin rapidly or rotate in a quick, spinning motion. It describes the action of turning something or someone around quickly, often in a graceful or playful manner. Twirling can involve rotating objects like batons, spinning around while dancing, or turning something between one\'s fingers. The movement is typically characterized by its circular, revolving nature and often has a lighthearted or artistic quality.',
            'example_sentence': 'The dancer _____ gracefully across the stage, her dress flowing with each spin.',
            'etymology': 'Past tense of "twirl," which is possibly a variant of "tirl" (to turn), related to words meaning "to turn" or "to rotate." The word emphasizes rapid, spinning motion.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWIRL + ED" - someone twirled (spun around) in the past, and "ED" marks it as completed action.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'twisting',
            'pronunciation': '/ˈtwɪstɪŋ/',
            'definition': 'Twisting refers to the action of turning or rotating something by applying force in opposite directions to different parts, creating a spiral or helical motion. It can describe physical actions like wringing out a cloth, turning a bottle cap, or the motion of roads and paths that curve and turn. Twisting can also refer to distorting facts or meanings, as in "twisting someone\'s words." The action often involves a combination of rotation and torque.',
            'example_sentence': 'The mountain road was _____ and turning through the scenic valley.',
            'etymology': 'Present participle of "twist," from Old English "twist" meaning "rope" or "divided thing," related to "twi-" (two). The verb developed from the idea of combining two strands.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWIST + ING" - something is currently being twisted or turned in a spiral motion.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'twisty',
            'pronunciation': '/ˈtwɪsti/',
            'definition': 'Twisty describes something that has many twists, turns, or curves. It characterizes roads, paths, or routes that wind and curve frequently rather than going straight. Twisty can also describe objects that are bent, coiled, or spiral in shape. Figuratively, it can refer to complex situations, stories, or problems that have many complications or unexpected developments, like a "twisty plot" in a mystery novel.',
            'example_sentence': 'The _____ mountain road required careful driving due to its many sharp curves.',
            'etymology': 'Adjective form of "twist" with the suffix "-y," meaning "characterized by twisting" or "having the quality of being twisted."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWIST + Y" - something that is twisty has the quality of being full of twists and turns.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'twitchy',
            'pronunciation': '/ˈtwɪtʃi/',
            'definition': 'Twitchy describes someone or something that exhibits sudden, involuntary movements or jerks. It can refer to physical conditions causing muscle spasms or nervous tics, or to behavioral patterns characterized by nervous, restless, or jumpy movements. Twitchy can also describe a nervous, anxious, or easily startled temperament. In informal usage, it might describe someone who is irritable, on edge, or hyperactive.',
            'example_sentence': 'The cat became _____ and restless before the thunderstorm arrived.',
            'etymology': 'Adjective form of "twitch" with the suffix "-y." "Twitch" comes from Old English "twiccian" meaning "to pluck" or "to pull," describing sudden, quick movements.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TWITCH + Y" - someone who is twitchy has the quality of making frequent twitching movements.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'twitter',
            'pronunciation': '/ˈtwɪtər/',
            'definition': 'Twitter originally means a series of light, high-pitched sounds made by birds, characterized by rapid, musical chirping. The word describes the characteristic sound of small birds communicating, especially during dawn and dusk. By extension, twitter can refer to excited chatter or rapid, light conversation among people. The term gained modern prominence as the name of the social media platform, chosen to evoke the idea of short, frequent communications resembling bird songs.',
            'example_sentence': 'The morning air was filled with the gentle _____ of birds in the garden.',
            'etymology': 'Imitative word (onomatopoeia) representing the sound of bird calls. The word appeared in English in the 14th century, mimicking the light, rapid sounds birds make.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think of the sound "TWITTER" - it mimics the light, rapid chirping sounds that birds make.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'tympanum',
            'pronunciation': '/ˈtɪmpənəm/',
            'definition': 'A tympanum has multiple meanings across different fields. In anatomy, it refers to the eardrum or middle ear cavity. In architecture, it\'s the triangular or semicircular decorative wall surface over an entrance, often found above doors in classical and medieval buildings. In ancient Greece and Rome, a tympanum was also a type of frame drum used in religious ceremonies. The architectural tympanum often features sculptural reliefs, paintings, or inscriptions and serves both decorative and symbolic purposes.',
            'example_sentence': 'The cathedral\'s ornate _____ above the main entrance depicted scenes from biblical stories.',
            'etymology': 'From Latin "tympanum," from Greek "tympanon" meaning "drum," from "typtein" (to strike). The word reflects the drum-like shape of both the eardrum and architectural feature.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYM (time) + PANUM (panel)" - the tympanum is like a time panel that shows historical or religious scenes above doorways.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'type',
            'pronunciation': '/taɪp/',
            'definition': 'Type refers to a category of things having common characteristics, or a particular kind or variety within a larger group. In printing, type refers to the characters or letters used for printing text. As a verb, type means to write using a typewriter or keyboard. The word encompasses the concept of classification, categorization, and standardized forms. Type can also refer to a person or thing that exemplifies particular characteristics of a group.',
            'example_sentence': 'What _____ of music do you prefer to listen to while studying?',
            'etymology': 'From Latin "typus," from Greek "typos" meaning "impression, figure, model," from "typtein" (to strike). Originally referred to impressions made by striking or stamping.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TY (tie) + PE (people)" - type helps tie people or things together into similar groups.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'typewriter',
            'pronunciation': '/ˈtaɪpˌraɪtər/',
            'definition': 'A typewriter is a mechanical or electromechanical machine for writing characters similar to those produced by printer\'s type. Invented in the 19th century, typewriters were the primary tool for creating documents before computers and word processors. They work by striking inked ribbons against paper through mechanical keys, each representing a different character. Typewriters revolutionized office work and writing, enabling faster and more legible document creation than handwriting.',
            'example_sentence': 'The vintage _____ sat on the desk, a reminder of how documents were created before computers.',
            'etymology': 'Compound word from "type" + "writer," literally meaning "a machine that writes type." Coined in the 19th century when these machines were invented.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYPE + WRITER" - it\'s literally a machine that writes by typing letters and characters.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        },
        {
            'word': 'typhlology',
            'pronunciation': '/tɪˈflɒlədʒi/',
            'definition': 'Typhlology is the scientific study of blindness and the methods, techniques, and systems used to assist blind individuals. This field encompasses research into the causes and treatment of blindness, development of assistive technologies, educational methods for the visually impaired, and rehabilitation techniques. Typhlology includes the study of Braille systems, mobility training, adaptive technologies, and psychological aspects of visual impairment. It\'s an interdisciplinary field combining medicine, education, psychology, and technology.',
            'example_sentence': 'Her graduate research in _____ focused on developing new technologies to help blind students navigate college campuses.',
            'etymology': 'From Greek "typhlos" meaning "blind" + "-logy" meaning "study of." The term was coined in the 19th century as formal study of blindness developed.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYPH (tough) + LOLOGY (study)" - typhlology is the tough study of helping people who can\'t see.',
            'phonetic_transparency': 1,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 4
        },
        {
            'word': 'typhoean',
            'pronunciation': '/taɪˈfoʊiən/',
            'definition': 'Typhoean refers to something characteristic of or relating to Typhon, a monstrous giant in Greek mythology known for his incredible size and destructive power. Typhon was considered the most deadly creature in Greek mythology, with a hundred dragon heads and was associated with storms, volcanoes, and natural disasters. By extension, typhoean describes anything of enormous, destructive, or tempestuous nature, particularly forces or events that seem overwhelmingly powerful and chaotic.',
            'example_sentence': 'The hurricane\'s _____ fury reminded observers of the ancient myths of unstoppable destructive forces.',
            'etymology': 'From Greek "Typhoeus" or "Typhon," the name of the mythological giant, possibly related to "typhon" (whirlwind). The adjective form describes qualities associated with this destructive figure.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYPHOON + EAN" - typhoean describes forces as powerful and destructive as a typhoon, like the mythical giant Typhon.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'typhoeanu',
            'pronunciation': '/taɪˈfoʊiənu/',
            'definition': 'Typhoeanu appears to be a variant or extended form of typhoean, maintaining the same reference to the mythological giant Typhon and describing characteristics of enormous destructive power. Like typhoean, it relates to forces or phenomena that exhibit the overwhelming, chaotic, and destructive qualities associated with the Greek mythological figure. This form may represent a regional variation or specialized usage in certain contexts, particularly in literary or academic discussions of mythology.',
            'example_sentence': 'The volcano\'s _____ eruption devastated the entire region with its mythological fury.',
            'etymology': 'Extended variant of "typhoean," from Greek "Typhoeus/Typhon," with an additional suffix. The etymology follows the same mythological reference to the destructive giant.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYPHOON + EANU" - like typhoean but with extra syllables, describing the same mythologically powerful and destructive forces.',
            'phonetic_transparency': 1,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 4
        },
        {
            'word': 'typically',
            'pronunciation': '/ˈtɪpɪkəli/',
            'definition': 'Typically means in a way that is characteristic or representative of a particular type, group, or situation. It indicates what usually happens, what is normal or expected, or what serves as a standard example. The word describes patterns, behaviors, or characteristics that are common or standard within a given context. Typically is often used to set expectations or describe general tendencies while acknowledging that exceptions may exist.',
            'example_sentence': 'Students _____ need several hours to complete their homework assignments.',
            'etymology': 'From "typical" + "-ly." "Typical" comes from Latin "typicus," from Greek "typikos" meaning "serving as a type or model," ultimately from "typos" (impression, model).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYPICAL + LY" - it describes how things typically or usually happen in a standard way.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'typing',
            'pronunciation': '/ˈtaɪpɪŋ/',
            'definition': 'Typing is the process of writing or inputting text by pressing keys on a typewriter, computer keyboard, or similar device. It involves the skill of using fingers to press keys corresponding to letters, numbers, and symbols to create written text. Modern typing includes touch typing (typing without looking at keys), hunt-and-peck methods, and various keyboard layouts. Typing speed and accuracy are important skills in many professions and educational settings.',
            'example_sentence': 'Her fast _____ skills made her highly efficient at data entry work.',
            'etymology': 'Present participle of "type," from the verb meaning "to write with a typewriter or keyboard." The -ing form indicates the ongoing action of typing.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYPE + ING" - the action of typing is currently happening or ongoing.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'tyrannical',
            'pronunciation': '/tɪˈrænɪkəl/',
            'definition': 'Tyrannical describes behavior, rule, or authority that is oppressive, cruel, and unreasonably harsh. It characterizes actions or systems that exercise power in an arbitrary, despotic manner without regard for justice or the rights of others. A tyrannical ruler or system suppresses freedom, ignores laws or constitutions, and often uses force or intimidation to maintain control. The word can apply to governments, leaders, or anyone who exercises authority in an oppressive, domineering manner.',
            'example_sentence': 'The citizens rebelled against their _____ ruler who had stripped away all their basic freedoms.',
            'etymology': 'From "tyrant" + "-ical." "Tyrant" comes from Greek "tyrannos," originally meaning "ruler" but later acquiring negative connotations of oppressive rule.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "TYRANT + ICAL" - tyrannical describes someone who acts like a tyrant in a systematic, oppressive way.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'ubiquinone',
            'pronunciation': '/ˌjuːbɪˈkwɪnoʊn/',
            'definition': 'Ubiquinone, also known as Coenzyme Q10 (CoQ10), is a crucial compound found in the mitochondria of cells throughout the human body. It plays an essential role in the electron transport chain, helping to produce ATP (cellular energy). Ubiquinone also functions as a powerful antioxidant, protecting cells from oxidative damage. As people age, natural ubiquinone levels decline, leading to its use as a dietary supplement. It\'s particularly concentrated in organs with high energy demands like the heart, liver, and kidneys.',
            'example_sentence': 'The cardiologist recommended _____ supplements to support her patient\'s heart health and cellular energy production.',
            'etymology': 'From Latin "ubique" meaning "everywhere" + "quinone" (a type of organic compound). Named because it\'s ubiquitous (found everywhere) in living cells.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UBI (everywhere) + QUINONE" - ubiquinone is found everywhere in your cells, giving them energy.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'ubiquity',
            'pronunciation': '/juːˈbɪkwɪti/',
            'definition': 'Ubiquity refers to the state of being everywhere at once or existing in all places simultaneously. It describes the quality of being omnipresent or universally present. In modern usage, ubiquity often refers to the widespread presence of something, such as technology, brands, or cultural phenomena that seem to be found everywhere. The concept implies not just widespread distribution, but a sense of inescapable presence across multiple locations or contexts.',
            'example_sentence': 'The _____ of smartphones has transformed how people communicate and access information.',
            'etymology': 'From Latin "ubiquitas," from "ubique" meaning "everywhere," from "ubi" (where) + "que" (and). The word entered English through scholarly Latin in the 17th century.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UBI (Uber everywhere) + QUITY (quality)" - ubiquity is the quality of being everywhere, like Uber trying to be in every city.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'udon',
            'pronunciation': '/ˈuːdɒn/',
            'definition': 'Udon is a type of thick, chewy Japanese wheat flour noodle, typically served in a hot broth as a soup. These noodles are characterized by their substantial thickness and smooth, elastic texture. Udon can be served in various ways: in hot broth with toppings like tempura, green onions, or kamaboko (fish cake), or cold with dipping sauce. The dish is a staple of Japanese cuisine and is popular for its comforting, hearty qualities and versatility in preparation.',
            'example_sentence': 'The restaurant served steaming bowls of _____ in rich, savory broth topped with green onions.',
            'etymology': 'From Japanese "udon" (うどん), which may have origins in Chinese noodle-making traditions. The word entered English directly from Japanese as Japanese cuisine gained international popularity.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YOU + DON" - when you don\'t know what noodles to order, you don udon because they\'re thick and satisfying.',
            'phonetic_transparency': 4,
            'frequency': 2,
            'morphological_complexity': 1,
            'etymology_complexity': 2
        },
        {
            'word': 'ufology',
            'pronunciation': '/juːˈfɒlədʒi/',
            'definition': 'Ufology is the study of unidentified flying objects (UFOs) and related phenomena. This field involves the investigation, analysis, and documentation of UFO sightings, alleged alien encounters, and unexplained aerial phenomena. Ufologists collect eyewitness accounts, analyze photographs and videos, and attempt to apply scientific methods to understand these mysterious occurrences. While not considered a mainstream science, ufology has developed its own methodologies, terminology, and research communities dedicated to exploring the possibility of extraterrestrial visitation.',
            'example_sentence': 'Her interest in _____ led her to investigate numerous reports of strange lights in the night sky.',
            'etymology': 'From "UFO" (Unidentified Flying Object) + "-logy" (study of). The term was coined in the 1950s as public interest in UFO phenomena grew.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UFO + LOGY" - ufology is literally the study (logy) of UFOs and alien phenomena.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 2
        }
    ]
    
    # Prepare CSV output
    output_file = 'output/batch_185_processed.csv'
    
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
    logging.info("Batch 185 processing completed!")
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