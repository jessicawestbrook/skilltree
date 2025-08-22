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
    logging.info("Processing Batch 188 with comprehensive Claude data...")
    
    # Combined word errors detected in batch 188
    combined_errors = ['usurpernoun', 'uvulaenumerated', 'vandalizechancellor', 'varicosedifficulty']
    
    # Comprehensive spelling bee data with Claude-generated educational content
    words_data = [
        {
            'word': 'using',
            'pronunciation': '/ˈjuːzɪŋ/',
            'definition': 'Using is the present participle of "use," meaning employing something for a particular purpose or taking advantage of something. It describes the action of making use of tools, methods, resources, or opportunities to accomplish a goal. Using can refer to physical utilization of objects, application of techniques or skills, or consumption of materials. The word indicates active employment of something available to achieve a desired outcome.',
            'example_sentence': 'She solved the complex problem by _____ a combination of traditional methods and modern technology.',
            'etymology': 'Present participle of "use," from Old English "ūsian," ultimately from Latin "uti" meaning "to use, employ, enjoy."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USE + ING" - using is simply the action of use happening right now.',
            'phonetic_transparency': 4,
            'frequency': 5,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'ustion',
            'pronunciation': '/ˈʌstʃən/',
            'definition': 'Ustion is the act of burning or the state of being burned; the medical or therapeutic application of heat or burning to tissue. In medical contexts, ustion refers to procedures involving controlled burning or heating for therapeutic purposes. The term is rarely used in modern medicine but appears in historical medical texts describing treatments involving cauterization or similar procedures. It can also refer to any process involving burning or combustion.',
            'example_sentence': 'The ancient medical text described various forms of _____ used to treat certain skin conditions.',
            'etymology': 'From Latin "ustio," from "ustus," past participle of "urere" meaning "to burn." Related to "combust" and "combustion."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UST (bust) + ION" - ustion busts things by burning them, like combustion.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 4
        },
        {
            'word': 'usual',
            'pronunciation': '/ˈjuːʒuəl/',
            'definition': 'Usual means happening or done most of the time; typical, normal, or customary. It describes what occurs regularly or what is expected under normal circumstances. Something usual follows established patterns or conforms to standard practices. The word indicates conformity with regular habits, common practices, or typical conditions. Usual suggests predictability and adherence to established norms.',
            'example_sentence': 'Despite the holiday, she followed her _____ morning routine of exercise and breakfast.',
            'etymology': 'From Latin "usualis" meaning "customary," from "usus" (use, custom). The word emphasizes what is commonly practiced or experienced.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USE + UAL" - usual things are what you usually use or do regularly.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'usually',
            'pronunciation': '/ˈjuːʒuəli/',
            'definition': 'Usually means in the way that is typical or normal; most of the time or under normal circumstances. It indicates that something happens frequently or regularly, though not necessarily always. Usually suggests a pattern of behavior or occurrence that can be expected but allows for occasional exceptions. The word describes the most common or standard way things happen.',
            'example_sentence': 'She _____ arrives at work by 8:00 AM, but today she was delayed by traffic.',
            'etymology': 'From "usual" + "-ly." Derives from Latin "usualis" meaning "customary," with the adverbial suffix indicating manner.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USUAL + LY" - usually describes how things usual-ly happen most of the time.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'usufruct',
            'pronunciation': '/ˈjuːzʊfrʌkt/',
            'definition': 'Usufruct is a legal term referring to the right to use and enjoy the benefits of someone else\'s property without owning it, as long as the property is not damaged or destroyed. This concept appears in Roman law and civil law systems, allowing someone to use property (like land or buildings) and collect its profits while the actual owner retains ownership. Usufruct often applies to agricultural land, rental properties, or natural resources.',
            'example_sentence': 'The heir received _____ of the estate, allowing him to live there and collect rent while his aunt retained ownership.',
            'etymology': 'From Latin "usufructus," from "usus" (use) + "fructus" (fruit, enjoyment). Literally means "use and enjoyment."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USE + FRUIT" - usufruct lets you use something and enjoy its fruits without owning it.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'usurper',
            'pronunciation': '/juːˈzɜːrpər/',
            'definition': 'A usurper is someone who takes another person\'s position of power illegally or by force, especially in reference to thrones, leadership roles, or authority. Usurpers seize power without legal right, often through violence, deception, or political maneuvering. The term is commonly used in historical contexts to describe those who overthrew legitimate rulers. Usurpation violates established succession or appointment processes.',
            'example_sentence': 'The rightful king was overthrown by a _____ who seized the throne through military force.',
            'etymology': 'From Old French "usurpeur," from Latin "usurpare" meaning "to take into use, occupy, enjoy." Originally neutral, later acquired negative connotations.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "USER + PER" - a usurper is someone who uses power per their own illegal taking of it.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'utilitarian',
            'pronunciation': '/ˌjuːtɪlɪˈtɛriən/',
            'definition': 'Utilitarian describes a philosophy that judges actions by their usefulness and practical results rather than by moral principles alone. In ethics, utilitarianism holds that the best action is the one that produces the greatest good for the greatest number of people. As an adjective, utilitarian can describe objects or designs that prioritize function over form, focusing on practical use rather than aesthetic appeal. The term emphasizes practical benefit and efficiency.',
            'example_sentence': 'The architect chose a _____ design that maximized functionality over decorative elements.',
            'etymology': 'From "utility" + "-arian." "Utility" comes from Latin "utilitas" meaning "usefulness," from "uti" (to use).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UTILITY + ARIAN" - utilitarians believe in the utility (usefulness) of actions for the greatest good.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 5,
            'etymology_complexity': 3
        },
        {
            'word': 'utterable',
            'pronunciation': '/ˈʌtərəbəl/',
            'definition': 'Utterable means capable of being spoken, expressed, or pronounced; able to be put into words. It describes thoughts, feelings, or concepts that can be articulated verbally or vocally expressed. Something utterable can be communicated through speech, as opposed to things that are too complex, profound, or indescribable to express in words. The word emphasizes the possibility of vocal or verbal expression.',
            'example_sentence': 'His grief was so profound that it seemed barely _____ in any human language.',
            'etymology': 'From "utter" + "-able." "Utter" comes from Old English "ūterra" meaning "outer," later developing the sense of "to speak out."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UTTER + ABLE" - utterable means you are able to utter or speak something aloud.',
            'phonetic_transparency': 4,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'uveal',
            'pronunciation': '/ˈjuːviəl/',
            'definition': 'Uveal refers to the uvea, the vascular middle layer of the eye that includes the iris, ciliary body, and choroid. This anatomical term describes structures or conditions related to this part of the eye. The uvea is responsible for much of the eye\'s blood supply and contains melanin that gives eyes their color. Uveal conditions can include inflammation (uveitis), melanoma, or other disorders affecting this crucial eye structure.',
            'example_sentence': 'The ophthalmologist diagnosed the patient with _____ melanoma, a serious form of eye cancer.',
            'etymology': 'From Latin "uvea," from "uva" meaning "grape," because the eye\'s uveal layer resembles a peeled grape in shape and color.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "UVE (grape) + AL" - uveal relates to the grape-like uvea layer of the eye.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'uvula',
            'pronunciation': '/ˈjuːvjələ/',
            'definition': 'The uvula is the small, teardrop-shaped piece of soft tissue that hangs from the back of the soft palate in the mouth. This anatomical structure helps with speech articulation and swallowing by directing food and liquid toward the throat. The uvula also plays a role in producing certain sounds in speech and helps prevent food from entering the nasal cavity during swallowing. In some people, the uvula can become elongated or inflamed.',
            'example_sentence': 'The doctor examined her throat and noted that her _____ was slightly swollen from the infection.',
            'etymology': 'From Latin "uvula," diminutive of "uva" meaning "grape," referring to its grape-like shape hanging in the throat.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "YOU + VULA" - your uvula is the little grape-shaped thing you can see hanging in your throat.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'vacancy',
            'pronunciation': '/ˈveɪkənsi/',
            'definition': 'Vacancy refers to an unoccupied position, job opening, or empty space available for occupation. It can describe employment opportunities, empty rooms in hotels, vacant apartments for rent, or unfilled positions in organizations. Vacancy implies that something is available and waiting to be filled or occupied. The word can also refer to emptiness or absence of thought, as in "mental vacancy."',
            'example_sentence': 'The company posted a _____ for a software engineer with five years of experience.',
            'etymology': 'From Latin "vacantia," from "vacans" (being empty), from "vacare" meaning "to be empty, free, or unoccupied."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VACANT + CY" - vacancy is the state or condition of being vacant or empty.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vacation',
            'pronunciation': '/vəˈkeɪʃən/',
            'definition': 'A vacation is a period of time spent away from work or daily routines, typically for rest, recreation, or travel. Vacations provide opportunities to relax, explore new places, spend time with family, or pursue leisure activities. The term can refer to both the time off from work and the trip or activities undertaken during that time. Vacations are important for mental health, stress relief, and work-life balance.',
            'example_sentence': 'They planned a two-week _____ to explore the national parks of the American Southwest.',
            'etymology': 'From Latin "vacatio," from "vacare" meaning "to be empty, free." Originally meant "freedom from occupation" or "leisure."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VACATE + ION" - vacation is when you vacate your work responsibilities for leisure time.',
            'phonetic_transparency': 3,
            'frequency': 5,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vaccary',
            'pronunciation': '/ˈvækəri/',
            'definition': 'A vaccary is a dairy farm or cow pasture; a place where cattle are kept for milk production. This somewhat archaic term refers specifically to establishments focused on dairy cattle and milk production rather than beef cattle. Vaccaries were important agricultural enterprises in medieval and early modern periods. The word emphasizes the connection between cattle keeping and dairy production.',
            'example_sentence': 'The medieval manor included a large _____ that supplied milk and cheese to the surrounding village.',
            'etymology': 'From Latin "vaccaria," from "vacca" meaning "cow." The suffix "-ary" indicates a place associated with the root word.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VACCA (cow) + RY" - a vaccary is where cows are kept for dairy production.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vaccination',
            'pronunciation': '/ˌvæksɪˈneɪʃən/',
            'definition': 'Vaccination is the administration of a vaccine to help the immune system develop protection against a disease. This medical procedure involves introducing antigens or weakened pathogens to stimulate the body\'s immune response and create immunity. Vaccination has been crucial in preventing many serious diseases like polio, measles, and smallpox. The process trains the immune system to recognize and fight specific diseases without causing the actual illness.',
            'example_sentence': 'The child received her routine _____ against measles, mumps, and rubella.',
            'etymology': 'From "vaccine" + "-ation." "Vaccine" comes from Latin "vaccinus" meaning "of cows," as the first vaccine used cowpox to prevent smallpox.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VACCINE + ATION" - vaccination is the action of giving vaccines for disease prevention.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'vacillate',
            'pronunciation': '/ˈvæsəˌleɪt/',
            'definition': 'Vacillate means to waver between different opinions, decisions, or courses of action; to be indecisive or changeable. It describes the behavior of someone who cannot make up their mind and keeps changing their position on issues. Vacillating involves moving back and forth between alternatives without settling on one choice. The word suggests uncertainty, hesitation, and lack of firm commitment.',
            'example_sentence': 'She continued to _____ between accepting the job offer and staying at her current position.',
            'etymology': 'From Latin "vacillare" meaning "to sway, waver, hesitate." Related to the physical motion of swaying back and forth.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VACILL (swivel) + ATE" - to vacillate is to swivel back and forth between decisions.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vacuousness',
            'pronunciation': '/ˈvækjuəsnəs/',
            'definition': 'Vacuousness refers to the quality of being empty of substance, meaning, or intelligence; lacking in ideas or content. It describes speech, writing, or thinking that appears to have no real substance despite seeming meaningful on the surface. Vacuousness can characterize empty rhetoric, meaningless statements, or superficial thinking that lacks depth or genuine insight. The word suggests an absence of meaningful content.',
            'example_sentence': 'The politician\'s speech was criticized for its _____ despite lasting over an hour.',
            'etymology': 'From "vacuous" + "-ness." "Vacuous" comes from Latin "vacuus" meaning "empty, void." The suffix creates the noun form.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VACUUM + OUSNESS" - vacuousness is the quality of being as empty as a vacuum.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'vacuum',
            'pronunciation': '/ˈvækjuəm/',
            'definition': 'A vacuum is a space entirely devoid of matter, or a space with air or gas removed to create suction. In physics, a perfect vacuum contains no particles, though this is theoretical since even outer space contains some matter. Practically, vacuum refers to enclosed spaces with significantly reduced air pressure. Vacuum cleaners use this principle to create suction for cleaning. The concept is important in physics, engineering, and technology.',
            'example_sentence': 'The scientist created a partial _____ in the chamber to conduct the experiment.',
            'etymology': 'From Latin "vacuum," neuter of "vacuus" meaning "empty, free, unoccupied." Originally used in the phrase "vacuum space."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAC (empty) + UUM" - a vacuum is completely empty space with no matter.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'vagabonds',
            'pronunciation': '/ˈvæɡəbɑːndz/',
            'definition': 'Vagabonds are people who wander from place to place without a permanent home or regular employment; nomads or wanderers. Historically, the term often carried negative connotations, referring to homeless people or those seen as undesirable by settled communities. However, vagabonds can also be viewed as free spirits who choose a lifestyle of travel and adventure over conventional stability. The word encompasses both voluntary and involuntary homelessness.',
            'example_sentence': 'The old tales spoke of _____ who traveled the countryside, sharing stories and songs.',
            'etymology': 'From Old French "vagabond," from Latin "vagabundus," from "vagari" meaning "to wander." Related to "vagrant" and "vague."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAGUE + BONDS" - vagabonds have vague bonds to any particular place, always wandering.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vagary',
            'pronunciation': '/ˈveɪɡəri/',
            'definition': 'A vagary is an unpredictable or erratic action, occurrence, or notion; a whimsical or capricious idea or change. Vagaries are unexpected developments that seem to follow no logical pattern or predictable sequence. The word often describes the unpredictable nature of weather, human behavior, fate, or circumstances that change suddenly and inexplicably. Vagaries suggest randomness and unpredictability.',
            'example_sentence': 'The _____ of weather in the mountains made it impossible to predict conditions for hiking.',
            'etymology': 'From Latin "vagari" meaning "to wander, roam." Originally referred to wandering of the mind or thoughts.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAGUE + ARY" - a vagary is a vague, unpredictable wandering of events or thoughts.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vague',
            'pronunciation': '/veɪɡ/',
            'definition': 'Vague means unclear, imprecise, or lacking definite form or limits; not clearly expressed or understood. Something vague is ambiguous, indefinite, or uncertain, making it difficult to grasp the exact meaning or details. Vague can describe statements, memories, impressions, or concepts that lack clarity or specificity. The word suggests haziness, indistinctness, or lack of clear definition.',
            'example_sentence': 'Her instructions were so _____ that nobody knew exactly what they were supposed to do.',
            'etymology': 'From Latin "vagus" meaning "wandering, uncertain, indefinite." Related to "vagrant" and "vagabond."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAGUE rhymes with PLAGUE" - vague instructions are a plague because they\'re unclear.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'vainglorious',
            'pronunciation': '/ˌveɪnˈɡlɔːriəs/',
            'definition': 'Vainglorious means excessively proud of one\'s achievements or abilities; boastful and conceited about one\'s own accomplishments. It describes someone who displays their pride in an ostentatious or arrogant manner, often seeking admiration from others. Vainglorious behavior involves showing off, bragging, or drawing attention to one\'s successes in ways that others find annoying or offensive. The word combines vanity with an excessive desire for glory.',
            'example_sentence': 'His _____ speech about his business success alienated many of his former colleagues.',
            'etymology': 'From "vain" + "glorious." "Vain" comes from Latin "vanus" (empty), and "glorious" from Latin "gloriosus" (full of glory).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAIN + GLORIOUS" - vainglorious people are vainly seeking glory and recognition.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'valedictorian',
            'pronunciation': '/ˌvæləˌdɪkˈtɔːriən/',
            'definition': 'A valedictorian is the student with the highest academic rank in a graduating class, typically chosen to deliver the farewell speech at graduation. This honor recognizes academic excellence, usually based on grade point average or overall academic performance throughout the student\'s time at the institution. The valedictorian represents the academic achievements of the entire graduating class and traditionally speaks about shared experiences and future aspirations.',
            'example_sentence': 'As _____, she delivered an inspiring speech about perseverance and the pursuit of knowledge.',
            'etymology': 'From Latin "valedicere" meaning "to say farewell," from "vale" (farewell) + "dicere" (to say). The "-ian" suffix indicates a person.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALE (farewell) + DICTATOR + IAN" - the valedictorian is the person who dictates the farewell speech.',
            'phonetic_transparency': 2,
            'frequency': 2,
            'morphological_complexity': 5,
            'etymology_complexity': 3
        },
        {
            'word': 'valerian',
            'pronunciation': '/vəˈlɪriən/',
            'definition': 'Valerian is a perennial flowering plant used in herbal medicine for its sedative and calming properties. The root of the valerian plant contains compounds that may help with sleep disorders, anxiety, and nervousness. Valerian has been used medicinally for centuries and is available as teas, tinctures, and supplements. The plant has a distinctive, somewhat unpleasant smell that many describe as similar to dirty socks.',
            'example_sentence': 'She brewed _____ tea before bedtime to help with her insomnia.',
            'etymology': 'From Latin "valeriana," possibly from "valere" meaning "to be strong" or named after the Roman province Valeria.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALOR + IAN" - valerian gives you the valor (strength) to fight insomnia.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'valetudinary',
            'pronunciation': '/ˌvæləˈtuːdɪˌnɛri/',
            'definition': 'Valetudinary describes someone who is chronically concerned about their health; a person who is sickly or constantly worried about illness. A valetudinary individual is often preoccupied with their physical condition and may be hypochondriacal or excessively focused on real or imagined health problems. The word can describe both genuinely frail individuals and those who are overly anxious about their health.',
            'example_sentence': 'The _____ old man spent most of his time reading medical journals and visiting doctors.',
            'etymology': 'From Latin "valetudinarius," from "valetudo" meaning "health, state of health," from "valere" (to be strong, healthy).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALUE + TUDIN + ARY" - valetudinary people place high value on monitoring their health condition.',
            'phonetic_transparency': 2,
            'frequency': 1,
            'morphological_complexity': 5,
            'etymology_complexity': 4
        },
        {
            'word': 'valiant',
            'pronunciation': '/ˈvæljənt/',
            'definition': 'Valiant means showing courage or determination; brave and heroic in the face of danger or difficulty. It describes actions, people, or efforts that demonstrate boldness and fearlessness when confronting challenges. Valiant behavior involves taking risks or making sacrifices for noble causes or to help others. The word suggests both physical bravery and moral courage in standing up for what is right.',
            'example_sentence': 'The firefighter made a _____ effort to rescue the family trapped in the burning building.',
            'etymology': 'From Old French "vaillant," from Latin "valere" meaning "to be strong." The word emphasizes strength and courage.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALID + ANT" - a valiant person is a valid ant who works courageously for the colony.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'valkyrian',
            'pronunciation': '/vælˈkɪriən/',
            'definition': 'Valkyrian relates to or resembles the Valkyries, the warrior maidens in Norse mythology who chose which soldiers would die in battle and escorted the souls of heroes to Valhalla. Something valkyrian embodies the fierce, noble, and supernatural qualities associated with these mythological figures. The word can describe warrior-like women, heroic behavior, or anything that evokes the powerful, otherworldly nature of the Valkyries.',
            'example_sentence': 'Her _____ presence on the battlefield inspired the soldiers to fight with renewed courage.',
            'etymology': 'From "Valkyrie" + "-ian." "Valkyrie" comes from Old Norse "valkyrja," from "valr" (slain warriors) + "kyrja" (chooser).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAL (valley) + KYRIE + AN" - valkyrian warriors soar over valleys like the mythical Valkyries.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 4
        },
        {
            'word': 'valley',
            'pronunciation': '/ˈvæli/',
            'definition': 'A valley is a low-lying area of land between hills or mountains, typically with a river or stream running through it. Valleys are formed through geological processes like erosion by water or glacial activity over long periods. They often contain fertile soil and are important for agriculture, settlements, and transportation routes. Valleys can vary greatly in size, from small dales to vast river basins.',
            'example_sentence': 'The peaceful _____ was dotted with farms and small villages along the winding river.',
            'etymology': 'From Old French "valee," from Latin "vallis" meaning "valley." The word has maintained its basic meaning throughout history.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAL (low) + LEY" - a valley is a low place where water leys (lies) between mountains.',
            'phonetic_transparency': 4,
            'frequency': 4,
            'morphological_complexity': 2,
            'etymology_complexity': 2
        },
        {
            'word': 'valorous',
            'pronunciation': '/ˈvælərəs/',
            'definition': 'Valorous means showing great courage, especially in battle; brave and heroic. It describes actions or people that demonstrate exceptional bravery and fearlessness in dangerous situations. Valorous behavior involves facing threats or challenges with determination and honor. The word is often used in literary or formal contexts to describe heroic deeds or courageous individuals.',
            'example_sentence': 'The _____ knight defended the village against overwhelming odds.',
            'etymology': 'From "valor" + "-ous." "Valor" comes from Latin "valor," from "valere" meaning "to be strong, be worth."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALOR + OUS" - valorous people are full of valor and courage.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'valourous',
            'pronunciation': '/ˈvælərəs/',
            'definition': 'Valourous is the British English spelling of "valorous," meaning showing great courage and bravery, especially in battle or dangerous situations. This spelling follows British conventions with the "ou" combination rather than just "o." The meaning is identical to "valorous" - describing heroic actions, brave individuals, or courageous behavior in the face of danger or adversity.',
            'example_sentence': 'The _____ actions of the rescue team saved dozens of lives during the disaster.',
            'etymology': 'British spelling of "valorous," from "valour" + "-ous." "Valour" is the British form of "valor," from Latin "valor."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALOUR + OUS" - valourous is the British way to spell valorous, full of valour.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'valuator',
            'pronunciation': '/ˈvæljuˌeɪtər/',
            'definition': 'A valuator is a professional who determines the worth or value of property, assets, businesses, or other items for various purposes such as sales, insurance, taxation, or legal proceedings. Valuators use their expertise to assess market value, replacement cost, or other relevant measures of worth. They must understand market conditions, comparable sales, and various valuation methodologies. Different types of valuators specialize in real estate, art, jewelry, businesses, or other specific assets.',
            'example_sentence': 'The insurance company hired a professional _____ to assess the damage to the antique collection.',
            'etymology': 'From "valuate" + "-or." "Valuate" comes from "value," ultimately from Latin "valere" meaning "to be worth."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALUE + ATOR" - a valuator is someone who evaluates the value of things.',
            'phonetic_transparency': 4,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'valvata',
            'pronunciation': '/vælˈveɪtə/',
            'definition': 'Valvata refers to a genus of small freshwater snails found in lakes and slow-moving streams. These gastropod mollusks have spiral shells and are commonly found in temperate regions. Valvata snails are herbivorous, feeding on algae and organic matter in aquatic environments. They play important ecological roles in freshwater ecosystems and are sometimes used as indicators of water quality. The name refers to the valve-like structure of their shells.',
            'example_sentence': 'The biologist collected samples of _____ snails to study the health of the lake ecosystem.',
            'etymology': 'From Latin "valvata," feminine of "valvatus" meaning "having valves," from "valva" (valve, door leaf).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VALVE + ATA" - valvata snails have shells with valve-like structures.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vambrace',
            'pronunciation': '/ˈvæmbreɪs/',
            'definition': 'A vambrace is a piece of armor designed to protect the forearm, particularly the area from the wrist to the elbow. Vambraces were commonly worn by medieval knights and soldiers as part of their armor. They could be made of metal, leather, or other protective materials and were often articulated to allow arm movement while fighting. Modern vambraces are sometimes worn for historical reenactment, fantasy costumes, or certain sports.',
            'example_sentence': 'The medieval knight\'s _____ protected his forearms from sword strikes during combat.',
            'etymology': 'From Old French "avant-bras," meaning "forearm," from "avant" (before) + "bras" (arm). The spelling evolved through Middle English.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAM (arm) + BRACE" - a vambrace is a brace that protects your arm.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'vancouver',
            'pronunciation': '/vænˈkuːvər/',
            'definition': 'Vancouver refers to a major coastal city in British Columbia, Canada, known for its natural beauty, diverse population, and economic importance. The city is a major Pacific port and serves as a gateway between Canada and Asia. Vancouver is famous for its mountains, ocean, parks, and cultural attractions. The name also refers to Vancouver Island and honors British explorer Captain George Vancouver who explored the Pacific Northwest coast.',
            'example_sentence': 'The 2010 Winter Olympics were held in _____, showcasing the city\'s stunning mountain and ocean scenery.',
            'etymology': 'Named after Captain George Vancouver (1757-1798), British Royal Navy officer who explored and surveyed the Pacific Northwest coast.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAN + COUVER" - like a van that covers a lot of territory, Vancouver covers a large coastal area.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vandalize',
            'pronunciation': '/ˈvændəlaɪz/',
            'definition': 'Vandalize means to deliberately damage or destroy public or private property, typically in a mindless or malicious manner. Vandalism includes activities like graffiti, breaking windows, damaging park equipment, or defacing buildings. This antisocial behavior often involves destruction that serves no purpose other than causing damage or expressing anger. Vandalism is illegal and can result in fines, community service, or other legal consequences.',
            'example_sentence': 'Unknown individuals attempted to _____ the historic monument with spray paint.',
            'etymology': 'From "vandal" + "-ize." "Vandal" comes from the Germanic tribe that sacked Rome, later meaning "one who destroys."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VANDAL + IZE" - to vandalize is to act like a vandal and destroy things.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vane',
            'pronunciation': '/veɪn/',
            'definition': 'A vane is a device that shows wind direction, typically mounted on top of buildings, poles, or weathercocks. Weather vanes are designed to rotate freely and point in the direction from which the wind is blowing. Vanes can also refer to the flat surfaces on windmill blades, propellers, or turbines that catch the wind or air flow. The word can also describe any thin, flat piece that moves in response to air current.',
            'example_sentence': 'The rooster-shaped weather _____ on the barn roof indicated that the wind was coming from the north.',
            'etymology': 'From Old English "fana" meaning "banner, flag." Related to "fane" (temple) and ultimately to showing or displaying direction.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VANE sounds like MAIN" - the main function of a vane is to show wind direction.',
            'phonetic_transparency': 4,
            'frequency': 2,
            'morphological_complexity': 1,
            'etymology_complexity': 3
        },
        {
            'word': 'vanguard',
            'pronunciation': '/ˈvænɡɑːrd/',
            'definition': 'Vanguard refers to the foremost part of an advancing army or the leaders of a movement or trend. In military contexts, the vanguard is the advance guard that goes ahead of the main force. Figuratively, vanguard describes people or groups that are at the forefront of new developments, innovations, or social movements. Being in the vanguard means being among the first to adopt or promote new ideas.',
            'example_sentence': 'The company has always been in the _____ of technological innovation in the industry.',
            'etymology': 'From Old French "avant-garde," meaning "advance guard," from "avant" (before) + "garde" (guard).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAN + GUARD" - the vanguard is like the guard riding in the van (front) of an army.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'vanity',
            'pronunciation': '/ˈvænəti/',
            'definition': 'Vanity is excessive pride in one\'s appearance, achievements, or abilities; the quality of being vain or conceited. It involves preoccupation with one\'s looks, status, or accomplishments to a degree that others find annoying or shallow. Vanity can also refer to the futility or worthlessness of earthly pursuits. As a noun, vanity sometimes refers to a dressing table with mirrors, emphasizing the connection to personal appearance.',
            'example_sentence': 'His _____ led him to spend hours each morning perfecting his appearance.',
            'etymology': 'From Old French "vanité," from Latin "vanitas" meaning "emptiness, futility," from "vanus" (empty, vain).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAIN + ITY" - vanity is the quality of being vain about your appearance.',
            'phonetic_transparency': 4,
            'frequency': 3,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vanquish',
            'pronunciation': '/ˈvæŋkwɪʃ/',
            'definition': 'Vanquish means to defeat thoroughly in a battle, competition, or conflict; to overcome completely. The word implies not just winning but achieving a decisive, overwhelming victory that leaves the opponent powerless to continue fighting. Vanquishing involves dominating an enemy or overcoming an obstacle so completely that resistance becomes impossible. The term is often used in heroic or dramatic contexts.',
            'example_sentence': 'The hero set out to _____ the dragon that had been terrorizing the village.',
            'etymology': 'From Old French "vainquir," from Latin "vincere" meaning "to conquer, defeat." Related to "victory" and "convince."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAN + QUISH" - to vanquish is to quash (crush) your enemies like a van rolling over them.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'vantage',
            'pronunciation': '/ˈvæntɪdʒ/',
            'definition': 'Vantage refers to a position or place that provides a good view or strategic advantage; a superior or commanding position. A vantage point offers clear visibility of the surrounding area or a better perspective on a situation. Vantage can also mean any advantage or benefit that gives someone a superior position in competition or conflict. The word emphasizes the value of position and perspective.',
            'example_sentence': 'From their _____ point on the hilltop, they could see the entire valley below.',
            'etymology': 'From Old French "avantage," meaning "advantage," from "avant" (before). The initial "a" was dropped in English.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAN + TAGE" - a vantage point is like having a van on a stage where you can see everything.',
            'phonetic_transparency': 3,
            'frequency': 3,
            'morphological_complexity': 2,
            'etymology_complexity': 3
        },
        {
            'word': 'vanuatu',
            'pronunciation': '/ˌvɑːnuˈɑːtuː/',
            'definition': 'Vanuatu is an island nation in the South Pacific Ocean, consisting of about 80 islands. Located east of Australia and northeast of New Zealand, Vanuatu is known for its volcanic landscapes, coral reefs, and diverse cultures. The country gained independence from joint British and French colonial rule in 1980. Vanuatu\'s economy relies on agriculture, tourism, and offshore financial services. The nation is frequently ranked as one of the happiest countries in the world.',
            'example_sentence': 'The tropical paradise of _____ attracts visitors with its pristine beaches and active volcanoes.',
            'etymology': 'From Bislama (local language) "Vanuatu," meaning "land eternal" or "land that stands," from "vanua" (land) + "tu" (stand).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAN + YOU + ATU" - Vanuatu is where you can take a van to see the beautiful atu (islands).',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'vaporetto',
            'pronunciation': '/ˌvæpəˈrɛtoʊ/',
            'definition': 'A vaporetto is a waterbus or water taxi that operates on the canals and lagoon of Venice, Italy. These boats serve as public transportation, carrying passengers between different parts of the city and to nearby islands. Vaporettos are essential to Venice\'s transportation system since the city has no roads for cars. The boats run on scheduled routes and are used by both locals and tourists to navigate the unique canal system.',
            'example_sentence': 'They took the _____ from St. Mark\'s Square to reach the island of Murano.',
            'etymology': 'From Italian "vaporetto," diminutive of "vapore" (steam), originally referring to small steam boats that operated in Venice.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VAPOR + ETTO (little)" - a vaporetto is like a little vapor (steam) boat in Venice.',
            'phonetic_transparency': 3,
            'frequency': 1,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'varicella',
            'pronunciation': '/ˌværɪˈsɛlə/',
            'definition': 'Varicella is the medical term for chickenpox, a highly contagious viral infection caused by the varicella-zoster virus. The disease typically affects children and is characterized by itchy, fluid-filled blisters that appear all over the body. Varicella usually causes fever and discomfort but is generally mild in healthy children. The same virus that causes varicella can later reactivate to cause shingles (herpes zoster) in adults.',
            'example_sentence': 'The pediatrician diagnosed the child with _____ and recommended rest and calamine lotion for the itchy rash.',
            'etymology': 'From Latin "varicella," diminutive of "variola" (smallpox), from "varius" meaning "spotted, varied," referring to the spotted rash.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VARI (varied) + CELLA (cells)" - varicella creates varied spots on skin cells.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 4
        },
        {
            'word': 'varicose',
            'pronunciation': '/ˈværəˌkoʊs/',
            'definition': 'Varicose describes veins that have become abnormally swollen, twisted, and enlarged, typically in the legs. Varicose veins occur when valves in the veins become weak or damaged, causing blood to pool and the veins to stretch. This condition can cause pain, aching, and cosmetic concerns. Varicose veins are more common in women and people who stand for long periods. Treatment options include lifestyle changes, compression stockings, and medical procedures.',
            'example_sentence': 'After years of standing at work, she developed _____ veins that required medical treatment.',
            'etymology': 'From Latin "varicosus," from "varix" meaning "dilated vein." Related to "various" through the idea of irregularity.',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VARI (varied) + COSE" - varicose veins vary from normal by being swollen and twisted.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'variegated',
            'pronunciation': '/ˈvɛriəˌɡeɪtɪd/',
            'definition': 'Variegated means marked with patches or streaks of different colors; having variety in appearance, especially in coloring. This term is commonly used to describe plants with leaves that have multiple colors, such as green with white or yellow markings. Variegated can also describe anything that shows diversity or variety in appearance, pattern, or character. The word emphasizes the attractive diversity created by multiple colors or patterns.',
            'example_sentence': 'The _____ leaves of the hosta plant added beautiful color contrast to the garden.',
            'etymology': 'From Latin "variegatus," past participle of "variegare" meaning "to make varied in color," from "varius" (varied) + "agere" (to make).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VARIED + GATED" - variegated things have varied colors gated (contained) in patterns.',
            'phonetic_transparency': 3,
            'frequency': 2,
            'morphological_complexity': 4,
            'etymology_complexity': 3
        },
        {
            'word': 'varieties',
            'pronunciation': '/vəˈraɪətiz/',
            'definition': 'Varieties are different types, forms, or kinds within the same general category; diverse manifestations of something. The word can refer to different breeds of animals, cultivars of plants, styles of products, or any collection of things that share basic characteristics but differ in specific details. Varieties provide options and diversity within a broader classification. The term emphasizes both similarity and difference.',
            'example_sentence': 'The farmers\' market offered many _____ of tomatoes, from cherry to heirloom types.',
            'etymology': 'Plural of "variety," from Latin "varietas" meaning "difference, diversity," from "varius" (varied, different).',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VARY + ETIES" - varieties are different entities that vary from each other.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        },
        {
            'word': 'variety',
            'pronunciation': '/vəˈraɪəti/',
            'definition': 'Variety refers to the quality of being different or diverse; a range of different things of the same general type. It can describe diversity within a collection, the state of having many different forms or types, or a particular type within a broader category. Variety adds interest and prevents monotony. The word can also refer to a subspecies or cultivar of a plant or animal.',
            'example_sentence': 'The spice of life is _____, and she enjoyed trying foods from different cultures.',
            'etymology': 'From Latin "varietas" meaning "difference, diversity," from "varius" meaning "varied, different, changing."',
            'etymology_source': 'Claude',
            'memory_tip': 'Think "VARY + ETY" - variety is the quality that makes things vary from each other.',
            'phonetic_transparency': 3,
            'frequency': 4,
            'morphological_complexity': 3,
            'etymology_complexity': 3
        }
    ]
    
    # Prepare CSV output
    output_file = 'output/batch_188_processed.csv'
    
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
    logging.info("Batch 188 processing completed!")
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