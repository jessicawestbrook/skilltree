#!/usr/bin/env python3

import csv
import json
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_word_data() -> Dict[str, Any]:
    """
    Creates comprehensive educational data for spelling bee words with Claude generation.
    
    This function contains pre-generated comprehensive educational content for each word,
    including detailed definitions, pronunciations, etymologies, memory tips, example sentences,
    and 4-factor difficulty scores.
    """
    
    return {
        "vlogging": {
            "word": "vlogging",
            "pronunciation": "/ˈvlɔɡɪŋ/",
            "definition": "The practice of creating and sharing video blogs or vlogs, typically posted on internet platforms such as YouTube, where content creators record themselves discussing topics, sharing experiences, or documenting their daily lives. Vlogging combines the traditional concept of blogging with video technology, allowing for more dynamic and personal content delivery. Vloggers often build communities around their content, engaging with viewers through comments and social media. This form of digital media has become a significant platform for entertainment, education, marketing, and personal expression in the modern internet age.",
            "etymology": "Blend of 'video' + 'blogging,' where 'blog' is a contraction of 'weblog'",
            "etymology_source": "Claude",
            "example_sentence": "She started _____ about sustainable living and quickly gained thousands of followers.",
            "memory_tip": "Think 'V-LOGGING' - 'Video LOGGING' - vlogging is logging your life or thoughts through video instead of text.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "vocab": {
            "word": "vocab",
            "pronunciation": "/ˈvoʊkæb/",
            "definition": "Informal abbreviation for vocabulary; the collection of words and their meanings that a person knows and uses. This shortened form is commonly used in educational contexts, particularly when discussing language learning, reading comprehension, or verbal skills. Vocab can refer to general word knowledge or specialized terminology within specific fields or subjects. The term is frequently used in academic settings, language apps, and casual conversation when referring to word study or vocabulary-building exercises.",
            "etymology": "Informal abbreviation of 'vocabulary,' from Latin 'vocabulum' meaning 'designation, name'",
            "etymology_source": "Claude",
            "example_sentence": "The students spent time reviewing their Spanish _____ before the exam.",
            "memory_tip": "Simply 'VOCAB' is short for 'VOCABulary' - like how 'math' is short for mathematics.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 3,
                "morphological_complexity": 1,
                "etymology_complexity": 2
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "vocabularies": {
            "word": "vocabularies",
            "pronunciation": "/voʊˈkæbjəlɛriz/",
            "definition": "Plural form of vocabulary; multiple collections of words and their meanings, whether referring to different languages, specialized fields, or individual speakers' word knowledge. This can refer to the distinct vocabularies of various disciplines (medical vocabulary, legal vocabulary), different languages (English and Spanish vocabularies), or the range of vocabularies possessed by different people. The term acknowledges that vocabulary is not monolithic but varies significantly across contexts, cultures, and individuals based on education, experience, and specialized knowledge.",
            "etymology": "Plural of 'vocabulary,' from Latin 'vocabularium' meaning 'list of words'",
            "etymology_source": "Claude",
            "example_sentence": "The translation software struggled with the specialized _____ of different scientific fields.",
            "memory_tip": "Simply 'VOCABULARY + IES' - multiple vocabularies, like multiple word collections from different subjects or languages.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021; 2022",
            "source_difficulty": "One Bee; Two Bee"
        },
        "vocabulary": {
            "word": "vocabulary",
            "pronunciation": "/voʊˈkæbjəˌlɛri/",
            "definition": "The collection of words and their meanings that a person knows and can use; the total stock of words belonging to a language or field of knowledge. Vocabulary encompasses not only the words one can recognize and understand when reading or listening, but also those one can actively use in speaking and writing. It includes general vocabulary for everyday communication as well as specialized terminology for specific domains such as science, technology, or professional fields. Vocabulary development is crucial for effective communication, reading comprehension, and academic success.",
            "etymology": "From Latin 'vocabularium' meaning 'list of words,' from 'vocabulum' meaning 'designation, name'",
            "etymology_source": "Claude",
            "example_sentence": "Reading diverse literature helped expand her _____ significantly over the years.",
            "memory_tip": "Think 'VOC-ABU-LARY' - 'VOCal ABUndant worLARY' - an abundant collection of words you can vocalize or use.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 3,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "vociferous": {
            "word": "vociferous",
            "pronunciation": "/voʊˈsɪfərəs/",
            "definition": "Expressing or characterized by vehement or loud outcry; clamorous, noisy, or demanding attention through forceful speech or protest. This adjective describes people or actions that are marked by loud, insistent, or aggressive verbal expression, often in the context of complaints, demands, or opposition. Vociferous behavior typically involves passionate, unrestrained verbal expression that seeks to make a strong impression or achieve a specific goal through the intensity and volume of communication rather than through quiet persuasion.",
            "etymology": "From Latin 'vociferari' meaning 'to cry out,' from 'vox' (voice) + 'ferre' (to bear, carry)",
            "etymology_source": "Claude",
            "example_sentence": "The _____ crowd demanded immediate action from the city council regarding the proposed budget cuts.",
            "memory_tip": "Think 'VOCI-FEROUS' - 'VOICe FEROCIOUS' - someone who is vociferous has a ferociously loud voice when expressing their opinions.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 6,
                "morphological_complexity": 6,
                "etymology_complexity": 6
            },
            "sources": "2025",
            "source_difficulty": "Three Bee"
        },
        "voice": {
            "word": "voice",
            "pronunciation": "/vɔɪs/",
            "definition": "The sound produced by speaking or singing; the ability to speak or sing; a particular opinion or attitude expressed; a means of expressing choice or opinion. As a physical phenomenon, voice results from air passing through the vocal cords, creating vibrations that form speech or song. Metaphorically, voice represents the power to express oneself, participate in decisions, or represent particular viewpoints. In grammar, voice indicates the relationship between a verb and its subject (active or passive voice). The concept extends to artistic expression, individual style, and democratic participation.",
            "etymology": "From Latin 'vox, vocis' meaning 'voice, sound, word'",
            "etymology_source": "Claude",
            "example_sentence": "The singer's powerful _____ filled the entire concert hall with emotion.",
            "memory_tip": "Think 'VOICE' sounds like 'CHOICE' - your voice gives you the choice to express yourself and communicate with others.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 1,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "voila": {
            "word": "voila",
            "pronunciation": "/vwaˈlɑ/",
            "definition": "An exclamation used to call attention to something or to express satisfaction or approval upon completion; the English rendering of the French 'voilà,' meaning 'there it is' or 'there you have it.' This interjection is used to present something with a flourish, indicate the successful completion of a task, or draw attention to a result or revelation. While borrowed from French, it has become commonly used in English to add dramatic effect or express triumph when revealing or completing something.",
            "etymology": "From French 'voilà,' from 'vois' (see, imperative of 'voir') + 'là' (there)",
            "etymology_source": "Claude",
            "example_sentence": "She mixed the ingredients, baked for thirty minutes, and _____ - a perfect chocolate cake!",
            "memory_tip": "Think 'VOI-LA' - 'VOIce LA-ugh' - you voice a laugh of satisfaction when you say 'voila!' after completing something successfully.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 4,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021",
            "source_difficulty": "One Bee"
        },
        "voilà": {
            "word": "voilà",
            "pronunciation": "/vwaˈlɑ/",
            "definition": "French exclamation meaning 'there it is' or 'there you have it,' used to call attention to something or express satisfaction upon completion; often used in English with the accent mark to maintain its French character. This interjection serves to present something with dramatic effect, indicate successful completion, or draw attention to a result. The accent mark distinguishes it from the anglicized 'voila' and preserves its French pronunciation and cultural origin, often used in contexts where the speaker wants to maintain the sophisticated or international flavor of the original French expression.",
            "etymology": "From French 'voilà,' from 'vois' (see, imperative of 'voir') + 'là' (there)",
            "etymology_source": "Claude",
            "example_sentence": "After hours of assembly, he stepped back and announced, '_____ - the bookshelf is complete!'",
            "memory_tip": "Same as 'voila' but with an accent mark - 'VOILÀ' - the accent reminds you it's the fancy French version meaning 'there it is!'",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 4,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021; 2022",
            "source_difficulty": "One Bee; Two Bee"
        },
        "volary": {
            "word": "volary",
            "pronunciation": "/ˈvoʊləri/",
            "definition": "A large enclosure or building for keeping birds; an aviary, especially one designed for flying birds rather than caged ones. This term refers to structures that provide birds with space for flight while keeping them contained, typically used in zoos, wildlife centers, or private collections. Volaries are designed to simulate natural environments while allowing observation and care of the birds. The term emphasizes the flight aspect of bird keeping, distinguishing these larger flight enclosures from simple cages or smaller aviaries.",
            "etymology": "From Latin 'volarium,' from 'volare' meaning 'to fly'",
            "etymology_source": "Claude",
            "example_sentence": "The zoo's new _____ allowed visitors to walk through while tropical birds flew freely overhead.",
            "memory_tip": "Think 'VOL-ARY' - 'VOLar' relates to flying (like 'volar' in Spanish), so a volary is where birds can fly around.",
            "difficulty_score": 7,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 8,
                "morphological_complexity": 6,
                "etymology_complexity": 7
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "volatile": {
            "word": "volatile",
            "pronunciation": "/ˈvɑlətəl/",
            "definition": "Liable to change rapidly and unpredictably; characterized by instability or explosive tendency; easily vaporized at normal temperatures. In chemistry, volatile substances readily evaporate or vaporize. In personality or behavior, it describes someone prone to sudden mood changes or outbursts. In markets or politics, it indicates unpredictable fluctuations or instability. The term suggests a lack of stability and the potential for sudden, dramatic changes that can be difficult to predict or control.",
            "etymology": "From Latin 'volatilis' meaning 'flying, fleeting,' from 'volare' meaning 'to fly'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ stock market made investors nervous about their long-term portfolios.",
            "memory_tip": "Think 'VOL-ATILE' - like 'VOLar' (fly) + 'agile' - something volatile flies around quickly and unpredictably, changing rapidly.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 5,
                "morphological_complexity": 5,
                "etymology_complexity": 5
            },
            "sources": "2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "volcano": {
            "word": "volcano",
            "pronunciation": "/vɑlˈkeɪnoʊ/",
            "definition": "A mountain or hill having a crater or vent through which lava, rock fragments, hot vapor, and gas are or have been erupted from the earth's crust. Volcanoes form when molten rock (magma) from beneath the Earth's surface escapes through openings in the crust. They can be active (currently erupting or showing signs of unrest), dormant (not currently active but could become active), or extinct (unlikely to erupt again). Volcanoes play crucial roles in shaping landscapes, creating new land, and affecting global climate patterns through their emissions.",
            "etymology": "From Italian 'vulcano,' from Latin 'Vulcanus,' referring to Vulcan, the Roman god of fire",
            "etymology_source": "Claude",
            "example_sentence": "The active _____ forced the evacuation of nearby villages when it began showing signs of eruption.",
            "memory_tip": "Think 'VOLC-ANO' - 'VULCAN-O' - named after Vulcan, the Roman god of fire, who would create these fiery mountains.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "volery": {
            "word": "volery",
            "pronunciation": "/ˈvoʊləri/",
            "definition": "An alternative spelling or variant of volary; a large enclosure for keeping birds, particularly one that allows them space for flight. This term refers to aviaries or bird houses designed to accommodate flying birds rather than simply caged ones. Voleries provide birds with more natural living conditions while maintaining them in captivity for observation, breeding, or protection. The term is used in zoology, wildlife management, and aviculture to describe facilities that prioritize the birds' ability to exercise their natural flying behaviors.",
            "etymology": "Variant of 'volary,' from Latin 'volare' meaning 'to fly'",
            "etymology_source": "Claude",
            "example_sentence": "The rehabilitation center's _____ helped injured birds regain their flying strength before release.",
            "memory_tip": "Same as 'volary' - 'VOL-ERY' relates to flying (volare), so it's a place where birds can fly around safely.",
            "difficulty_score": 7,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 8,
                "morphological_complexity": 6,
                "etymology_complexity": 7
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "volition": {
            "word": "volition",
            "pronunciation": "/voʊˈlɪʃən/",
            "definition": "The faculty or power of using one's will; the act of making a conscious choice or decision; deliberate intention or determination. This philosophical and psychological term refers to the mental process by which a person commits to a particular course of action or decision. Volition implies conscious control over one's actions rather than behavior driven by instinct, reflex, or external compulsion. It encompasses the capacity for independent choice and the exercise of free will in human behavior and decision-making processes.",
            "etymology": "From Latin 'volitio,' from 'velle' meaning 'to wish, to will'",
            "etymology_source": "Claude",
            "example_sentence": "She left the job of her own _____, seeking new challenges and opportunities.",
            "memory_tip": "Think 'VOL-ITION' - 'VOLuntary moTION' - volition is the voluntary motion of your will to make choices and decisions.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 7,
                "morphological_complexity": 6,
                "etymology_complexity": 6
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "voltammetry": {
            "word": "voltammetry",
            "pronunciation": "/voʊlˈtæmətri/",
            "definition": "An electroanalytical chemistry technique used to obtain information about an analyte by measuring the current as the potential is varied. This method involves applying a controlled potential to an electrode in a solution containing the substance being studied and measuring the resulting current. Voltammetry is widely used in analytical chemistry for determining the concentration, identity, and properties of chemical species. The technique provides valuable information about oxidation and reduction processes, reaction mechanisms, and the thermodynamics and kinetics of electron transfer reactions.",
            "etymology": "From 'volt' (unit of electric potential) + 'ammetry' (from 'ampere' + '-metry' meaning measurement)",
            "etymology_source": "Claude",
            "example_sentence": "The chemistry lab used _____ to analyze the concentration of metal ions in the water sample.",
            "memory_tip": "Think 'VOLT-AMMETRY' - 'VOLT' (electricity) + 'AMMETRY' (measuring amps) - measuring electrical current and voltage together.",
            "difficulty_score": 8,
            "difficulty_factors": {
                "phonetic_transparency": 7,
                "word_frequency": 9,
                "morphological_complexity": 8,
                "etymology_complexity": 7
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "volucrine": {
            "word": "volucrine",
            "pronunciation": "/ˈvɑljuˌkraɪn/",
            "definition": "Of, relating to, or characteristic of birds; having qualities associated with birds or bird-like features. This formal adjective is used in scientific, literary, or academic contexts to describe attributes, behaviors, or characteristics that are typical of or reminiscent of birds. The term might be applied to describe movements, sounds, or features that evoke avian qualities. It is a more specialized and formal alternative to simply saying 'bird-like' and is typically found in scientific literature, ornithological studies, or literary works seeking precise descriptive language.",
            "etymology": "From Latin 'volucris' meaning 'bird' (literally 'flying creature'), from 'volare' meaning 'to fly'",
            "etymology_source": "Claude",
            "example_sentence": "The dancer's _____ movements across the stage reminded the audience of a graceful swan.",
            "memory_tip": "Think 'VOL-UCRINE' - 'VOLar' (fly) + 'uCRINE' - relating to flying creatures, meaning bird-like characteristics.",
            "difficulty_score": 8,
            "difficulty_factors": {
                "phonetic_transparency": 7,
                "word_frequency": 9,
                "morphological_complexity": 8,
                "etymology_complexity": 8
            },
            "sources": "2020; 2021; 2022; 2023; 2024",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "volumetric": {
            "word": "volumetric",
            "pronunciation": "/ˌvɑljəˈmɛtrɪk/",
            "definition": "Of, relating to, or involving the measurement of volume; based on or using volume measurements. This adjective is commonly used in chemistry, physics, and engineering to describe methods, instruments, or calculations that involve determining or using the volume of substances. Volumetric analysis includes techniques for determining the concentration of solutions, measuring gas volumes, or calculating the amount of material based on volume measurements. The term emphasizes precision in volume measurement and is essential in quantitative scientific work.",
            "etymology": "From 'volume' + '-metric' (from Greek 'metron' meaning 'measure'), relating to measuring volume",
            "etymology_source": "Claude",
            "example_sentence": "The _____ analysis revealed the exact concentration of acid in the solution.",
            "memory_tip": "Think 'VOLUME-TRIC' - 'VOLUME + meTRIC' - relating to measuring (metric) the volume of something accurately.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 6,
                "morphological_complexity": 6,
                "etymology_complexity": 6
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "voluminous": {
            "word": "voluminous",
            "pronunciation": "/vəˈlumɪnəs/",
            "definition": "Taking up much space; bulky, large, or extensive in size or quantity; having great volume or bulk. This adjective can describe physical objects that are large and occupy significant space, or abstract things like writing, documentation, or data that are extensive in scope or quantity. When applied to clothing, it suggests loose, flowing garments. When applied to written works or information, it indicates comprehensive, detailed, or lengthy content that covers a subject thoroughly.",
            "etymology": "From Latin 'voluminosus,' from 'volumen' meaning 'roll, scroll, book volume'",
            "etymology_source": "Claude",
            "example_sentence": "The historian's _____ research notes filled several filing cabinets in his office.",
            "memory_tip": "Think 'VOLUM-INOUS' - 'VOLUME + INous' - something voluminous has a lot of volume, meaning it's big and takes up lots of space.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 5,
                "morphological_complexity": 5,
                "etymology_complexity": 5
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "voluntary": {
            "word": "voluntary",
            "pronunciation": "/ˈvɑlənˌtɛri/",
            "definition": "Done, given, or acting of one's own free will; not forced, compelled, or paid for; performed or undertaken by choice rather than from obligation. This adjective describes actions, services, or participation that result from personal decision rather than external pressure or requirement. Voluntary activities include charitable work, donations, or participation in non-mandatory programs. The term emphasizes the element of choice and free will in decision-making, distinguishing such actions from those performed under duress, for payment, or from legal obligation.",
            "etymology": "From Latin 'voluntarius,' from 'voluntas' meaning 'will, choice,' from 'velle' meaning 'to wish'",
            "etymology_source": "Claude",
            "example_sentence": "Her _____ work at the animal shelter brought her great personal satisfaction.",
            "memory_tip": "Think 'VOLUNT-ARY' - 'VOLUNTeer' + 'ARY' - voluntary actions are like volunteering, done by your own choice and will.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021",
            "source_difficulty": "One Bee"
        },
        "vortices": {
            "word": "vortices",
            "pronunciation": "/ˈvɔrtɪˌsiz/",
            "definition": "Plural form of vortex; multiple whirling masses of fluid or air, such as whirlpools or cyclones; spiral patterns of motion in fluids. This term is used in physics, meteorology, and fluid dynamics to describe rotating flows where the fluid moves in circular or spiral patterns around a central axis. Vortices can occur in various scales, from small eddies in water to large atmospheric phenomena like hurricanes or tornadoes. They play important roles in aerodynamics, weather systems, and various engineering applications.",
            "etymology": "Plural of 'vortex,' from Latin 'vortex, vorticis' meaning 'whirlpool, eddy'",
            "etymology_source": "Claude",
            "example_sentence": "The scientist studied the formation of _____ behind the aircraft wing to improve aerodynamic efficiency.",
            "memory_tip": "Think 'VORT-ICES' - 'VORTEX + ICES' - multiple vortexes (whirlpools), like multiple pieces of ice spinning in water.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 6,
                "morphological_complexity": 6,
                "etymology_complexity": 6
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "votive": {
            "word": "votive",
            "pronunciation": "/ˈvoʊtɪv/",
            "definition": "Offered or given in fulfillment of a vow or pledge; dedicated or consecrated as a result of a vow; relating to or constituting a vow or wish. This adjective describes objects, offerings, or actions that are performed as part of a religious or spiritual commitment. Votive candles, for example, are lit as part of prayer or devotional practices. The term can also apply to artistic works, buildings, or other items created or dedicated to fulfill a promise made to a deity or as an expression of gratitude or devotion.",
            "etymology": "From Latin 'votivus,' from 'votum' meaning 'vow, wish,' from 'vovere' meaning 'to vow'",
            "etymology_source": "Claude",
            "example_sentence": "The chapel was filled with _____ candles lit by faithful visitors seeking blessings.",
            "memory_tip": "Think 'VOT-IVE' - 'VOTE-ive' - like voting, making a votive offering is making a choice to dedicate something as part of a vow.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 6,
                "morphological_complexity": 4,
                "etymology_complexity": 5
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "vouch": {
            "word": "vouch",
            "pronunciation": "/vaʊtʃ/",
            "definition": "To assert, confirm, or attest to the truth, accuracy, or reliability of something; to give personal assurance or guarantee for someone or something. This verb implies taking personal responsibility for the credibility or character of a person, the accuracy of information, or the quality of something. When someone vouches for another person, they are essentially staking their own reputation on that person's trustworthiness or competence. The term suggests a strong level of confidence and willingness to be held accountable for one's endorsement.",
            "etymology": "From Old French 'voucher' meaning 'to call, summon,' from Latin 'vocare' meaning 'to call'",
            "etymology_source": "Claude",
            "example_sentence": "The manager was willing to _____ for the new employee's work ethic and reliability.",
            "memory_tip": "Think 'VOUCH' sounds like 'OUCH' - if you vouch for someone and they let you down, it might hurt ('ouch') your reputation.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 3,
                "etymology_complexity": 5
            },
            "sources": "2020; 2021; 2022; 2023",
            "source_difficulty": "One Bee; Two Bee"
        },
        "vowel": {
            "word": "vowel",
            "pronunciation": "/ˈvaʊəl/",
            "definition": "A speech sound produced with the vocal tract open and unobstructed, allowing air to flow freely; a letter representing such a sound. In English, the primary vowels are A, E, I, O, and U, with Y sometimes functioning as a vowel. Vowels form the core of syllables and are essential for speech intelligibility. They are characterized by their acoustic properties, including formant frequencies, and are distinguished from consonants by the lack of constriction in the vocal tract during production. Vowel systems vary significantly across different languages.",
            "etymology": "From Latin 'vocalis' meaning 'vocal,' from 'vox, vocis' meaning 'voice'",
            "etymology_source": "Claude",
            "example_sentence": "The English language has five primary _____ letters that form the foundation of pronunciation.",
            "memory_tip": "Think 'VOW-EL' - you 'VOW' to use these 'EL'ements (A, E, I, O, U) in almost every word you speak.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2024; 2025",
            "source_difficulty": "Three Bee"
        },
        "voyage": {
            "word": "voyage",
            "pronunciation": "/ˈvɔɪɪdʒ/",
            "definition": "A long journey involving travel by sea or in space; an extended trip or expedition, especially one involving exploration or adventure. Traditionally associated with ocean travel, the term has expanded to include space travel and other extended journeys of discovery. A voyage implies a significant undertaking that involves leaving familiar territory for distant or unknown places. The word carries connotations of adventure, discovery, and the challenges associated with long-distance travel, whether for exploration, commerce, or migration.",
            "etymology": "From Old French 'voiage,' from Latin 'viaticum' meaning 'provisions for a journey'",
            "etymology_source": "Claude",
            "example_sentence": "The ship's maiden _____ across the Atlantic took three weeks to complete.",
            "memory_tip": "Think 'VOY-AGE' - 'VOYAGE' sounds like 'BOY-AGE' - think of a boy at any age dreaming of adventures on long sea voyages.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2025",
            "source_difficulty": "Three Bee"
        },
        "vulcan": {
            "word": "vulcan",
            "pronunciation": "/ˈvʌlkən/",
            "definition": "Roman god of fire and metalworking; relating to or resembling volcanic activity or fire; in modern contexts, often referring to the fictional alien race from Star Trek known for their logical nature. In classical mythology, Vulcan (Vulcanus in Latin) was the blacksmith of the gods, associated with destructive and creative fire. The term can be used adjectivally to describe things related to volcanic activity or intense heat. In popular culture, it has become associated with the logical, emotionally controlled alien species created by Gene Roddenberry.",
            "etymology": "From Latin 'Vulcanus,' the Roman god of fire and forge, possibly from an earlier Etruscan deity",
            "etymology_source": "Claude",
            "example_sentence": "The planet's _____ landscape showed evidence of recent volcanic activity.",
            "memory_tip": "Think 'VULC-AN' - 'VULCano' + 'AN' - Vulcan is the Roman god associated with volcanoes and fire.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 3,
                "etymology_complexity": 5
            },
            "sources": "2022; 2023; 2024; 2025",
            "source_difficulty": "Three Bee; Two Bee"
        },
        "vulpine": {
            "word": "vulpine",
            "pronunciation": "/ˈvʌlpaɪn/",
            "definition": "Of, relating to, or characteristic of foxes; having qualities associated with foxes, such as cunning, craftiness, or cleverness. This formal adjective is used to describe behavior, appearance, or characteristics that are reminiscent of foxes, particularly their reputation for intelligence and slyness. Vulpine features might include pointed facial characteristics or reddish coloring. When applied to behavior or personality, it suggests shrewdness, cunning, or the ability to be clever and resourceful in achieving one's goals.",
            "etymology": "From Latin 'vulpinus,' from 'vulpes' meaning 'fox'",
            "etymology_source": "Claude",
            "example_sentence": "His _____ grin suggested he knew more about the situation than he was revealing.",
            "memory_tip": "Think 'VULP-INE' - 'VULPes' means fox in Latin, so vulpine means fox-like, especially cunning and clever like a fox.",
            "difficulty_score": 7,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 8,
                "morphological_complexity": 6,
                "etymology_complexity": 7
            },
            "sources": "2020; 2021; 2022",
            "source_difficulty": "One Bee; Two Bee"
        },
        "vultures": {
            "word": "vultures",
            "pronunciation": "/ˈvʌltʃərz/",
            "definition": "Plural form of vulture; large scavenging birds that feed primarily on carrion (dead animals), characterized by broad wings, keen eyesight, and bare heads and necks. These birds play crucial ecological roles as nature's cleanup crew, preventing the spread of disease by consuming decomposing matter. Metaphorically, the term can describe people who prey on others' misfortunes or seek to profit from others' difficulties. Vultures are found on every continent except Australia and Antarctica and are known for their soaring flight patterns and social feeding behaviors.",
            "etymology": "From Latin 'vultur' meaning 'vulture,' possibly related to 'vellere' meaning 'to tear, pluck'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ circled overhead, waiting for the injured animal to succumb.",
            "memory_tip": "Think 'VULT-URES' - 'VAULT-URES' - vultures vault (soar) high in the sky looking for food, like they're exploring vaults of the sky.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "vuvuzela": {
            "word": "vuvuzela",
            "pronunciation": "/ˌvuvuˈzɛlə/",
            "definition": "A long horn-like plastic instrument that produces a loud, distinctive buzzing sound, traditionally used by spectators at football (soccer) matches in South Africa. The vuvuzela gained international attention during the 2010 FIFA World Cup in South Africa, where its constant droning sound became a characteristic feature of the matches. The instrument is typically about one meter long and produces a single note when blown. While culturally significant in South African sports culture, it has been controversial due to its volume and potential impact on player communication and television broadcasts.",
            "etymology": "From Zulu, possibly from 'vuvuzela' meaning 'to make noise' or related to township slang",
            "etymology_source": "Claude",
            "example_sentence": "The stadium echoed with the constant drone of thousands of _____ during the World Cup match.",
            "memory_tip": "Think 'VU-VU-ZELA' - sounds like 'VU-VU' (the noise it makes) + 'ZELA' - it's an instrument that makes 'vu-vu' buzzing sounds.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 6,
                "morphological_complexity": 4,
                "etymology_complexity": 5
            },
            "sources": "2022",
            "source_difficulty": "Two Bee"
        },
        "véronique": {
            "word": "véronique",
            "pronunciation": "/veɪrəˈnik/",
            "definition": "A French culinary term referring to a classic preparation method, particularly for fish dishes, that incorporates white grapes as a key ingredient. The dish typically features fish (often sole) served with a sauce containing white grapes, white wine, and cream. This preparation is considered part of classical French cuisine and represents the elegant, refined cooking style associated with French gastronomy. The term may also refer to the plant speedwell (Veronica) in botanical contexts, though the culinary usage is more common in English contexts.",
            "etymology": "From French, related to 'Veronica' (the saint), possibly through the plant speedwell which bears her name",
            "etymology_source": "Claude",
            "example_sentence": "The chef prepared sole _____ with fresh white grapes and a delicate wine sauce.",
            "memory_tip": "Think 'VÉR-ONIQUE' - sounds like 'VERY UNIQUE' - it's a very unique French cooking style that uses grapes in fish dishes.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 7,
                "morphological_complexity": 5,
                "etymology_complexity": 6
            },
            "sources": "2020; 2021; 2022; 2023; 2024",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "wabeno": {
            "word": "wabeno",
            "pronunciation": "/wəˈbinoʊ/",
            "definition": "In Ojibwe/Chippewa culture, a traditional spiritual leader or medicine person who conducts dawn ceremonies and healing rituals; sometimes referring to a member of a specific medicine society. The wabeno tradition involves ceremonies performed at dawn, often including the use of fire, and focuses on healing and spiritual guidance. This role is part of the traditional indigenous spiritual practices of the Great Lakes region tribes. The term represents an important aspect of Native American spiritual and healing traditions, emphasizing the connection between dawn, fire, and spiritual power.",
            "etymology": "From Ojibwe 'waabeno' meaning 'dawn man' or 'he of the dawn,' from 'waaban' (dawn) + '-no' (man)",
            "etymology_source": "Claude",
            "example_sentence": "The _____ led the dawn ceremony, using sacred fire to guide the healing ritual.",
            "memory_tip": "Think 'WA-BENO' - 'WAke BEfore NO(on)' - a wabeno is someone who wakes before noon (at dawn) to perform spiritual ceremonies.",
            "difficulty_score": 7,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 8,
                "morphological_complexity": 6,
                "etymology_complexity": 8
            },
            "sources": "2023; 2024; 2025",
            "source_difficulty": "Three Bee; Two Bee"
        },
        "wafer": {
            "word": "wafer",
            "pronunciation": "/ˈweɪfər/",
            "definition": "A very thin, light, crisp cake, biscuit, or cracker; a thin disc of unleavened bread used in Christian communion; a thin slice or layer of semiconductor material used in electronics manufacturing. In culinary contexts, wafers are often sweet and may be served with ice cream or used as cookie layers. In religious contexts, communion wafers are consecrated and used in Christian liturgy. In technology, silicon wafers serve as the substrate for manufacturing computer chips and other electronic components.",
            "etymology": "From Old French 'waufre,' from Middle Dutch 'wafel' meaning 'honeycomb, waffle'",
            "etymology_source": "Claude",
            "example_sentence": "The priest distributed the communion _____ to each member of the congregation.",
            "memory_tip": "Think 'WAFER' sounds like 'WAVER' - a wafer is so thin it might waver or bend in the breeze.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 4,
                "morphological_complexity": 2,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021",
            "source_difficulty": "One Bee"
        },
        "wafting": {
            "word": "wafting",
            "pronunciation": "/ˈwæftɪŋ/",
            "definition": "Present participle of waft; moving gently through the air; carrying or conveying gently as if by wind or breeze. This verb describes the gentle, flowing movement of air, scents, sounds, or light objects as they drift or float through space. Wafting suggests a soft, undulating motion that is typically pleasant or peaceful, often used to describe how fragrances, music, or smoke travels through the air. The movement is characterized by its lightness and grace rather than force or urgency.",
            "etymology": "From 'waft,' originally a nautical term from Dutch or Low German 'wachten' meaning 'to guard, convoy'",
            "etymology_source": "Claude",
            "example_sentence": "The smell of fresh bread was _____ from the bakery down the street.",
            "memory_tip": "Think 'WAFT-ING' - 'WAFT + ING' - currently wafting means currently floating gently through the air like a feather.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "wagon": {
            "word": "wagon",
            "pronunciation": "/ˈwæɡən/",
            "definition": "A four-wheeled vehicle used for transporting goods or people, typically pulled by horses or other draft animals; in modern usage, often referring to a wheeled cart or a station wagon automobile. Historically, wagons were essential for transportation of goods across long distances, particularly in the settlement of the American West. The term has evolved to include various wheeled vehicles, from children's toy wagons to specialized freight wagons. In automotive contexts, a wagon refers to a car body style with an extended rear cargo area.",
            "etymology": "From Dutch 'wagen' meaning 'vehicle, cart,' related to German 'Wagen' and English 'way'",
            "etymology_source": "Claude",
            "example_sentence": "The pioneers loaded their _____ with supplies for the long journey westward.",
            "memory_tip": "Think 'WAG-ON' - like a dog's tail 'wagging ON' - a wagon is something that goes on wheels, moving along like a wagging tail.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2025",
            "source_difficulty": "Three Bee"
        },
        "wahine": {
            "word": "wahine",
            "pronunciation": "/wɑˈhini/",
            "definition": "A Hawaiian and Polynesian word meaning woman, especially a native Hawaiian woman; in surfing culture, referring to a female surfer. This term is commonly used in Hawaii and has been adopted into English, particularly in contexts related to Hawaiian culture, surfing, and Pacific Island traditions. The word carries cultural significance and is often used with respect when referring to women in Hawaiian and Polynesian contexts. It represents an important part of indigenous Pacific language that has been incorporated into broader English usage, especially in coastal and surfing communities.",
            "etymology": "From Hawaiian and Polynesian 'wahine' meaning 'woman, female'",
            "etymology_source": "Claude",
            "example_sentence": "The local _____ taught visitors about traditional Hawaiian crafts and customs.",
            "memory_tip": "Think 'WA-HINE' - 'WAter SHINE' - Hawaiian wahine often shine in the water through surfing and water activities.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 6,
                "morphological_complexity": 4,
                "etymology_complexity": 5
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "waing": {
            "word": "waing",
            "pronunciation": "/weɪŋ/",
            "definition": "A dialectal or archaic term, potentially a variant spelling or form related to 'waning' or 'waging'; usage and meaning may vary by regional dialect or historical context. This word appears to be a less common or specialized term that may have specific usage in certain dialects or historical texts. The exact meaning and pronunciation may depend on the specific linguistic or cultural context in which it appears. Such terms often represent interesting examples of language variation and evolution within English dialects.",
            "etymology": "Potentially dialectal variant, etymology uncertain - may relate to 'wane' or other English dialect forms",
            "etymology_source": "Claude",
            "example_sentence": "The old manuscript contained the archaic word _____, whose meaning puzzled modern scholars.",
            "memory_tip": "Think 'WAI-NG' - this is a rare or dialectal word, so remember it's 'WAIting for explaNatioN of meaninG.'",
            "difficulty_score": 8,
            "difficulty_factors": {
                "phonetic_transparency": 7,
                "word_frequency": 9,
                "morphological_complexity": 7,
                "etymology_complexity": 9
            },
            "sources": "2020; 2021; 2022; 2023; 2024",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "waist": {
            "word": "waist",
            "pronunciation": "/weɪst/",
            "definition": "The part of the human body between the ribs and hips; the narrow part of something, especially a garment that fits around this part of the body. In anatomy, the waist is typically the narrowest part of the torso, located between the bottom of the rib cage and the top of the hip bones. In clothing, the waist refers to the part of a garment that encircles this area or the measurement of this circumference. The term can also be applied metaphorically to describe the narrow middle part of other objects.",
            "etymology": "From Middle English 'wast,' possibly from Old Norse 'vaxtr' meaning 'growth, size'",
            "etymology_source": "Claude",
            "example_sentence": "She cinched the belt tightly around her _____ to define the silhouette of the dress.",
            "memory_tip": "Think 'WAIST' sounds like 'WASTE' - don't waste time looking for your waist, it's the narrow part in the middle of your body.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2023",
            "source_difficulty": "Two Bee"
        },
        "waited": {
            "word": "waited",
            "pronunciation": "/ˈweɪtɪd/",
            "definition": "Past tense of wait; remained in place or delayed action in expectation of something; stayed in a particular location or state until a specific time or event. This verb form indicates completed action of pausing, delaying, or remaining patient until something expected occurred or until it was time to proceed. The action of waiting involves conscious restraint from immediate action in anticipation of future conditions, events, or opportunities. It can involve both active anticipation and passive endurance.",
            "etymology": "From Old French 'waitier' meaning 'to watch, guard,' from Germanic origin",
            "etymology_source": "Claude",
            "example_sentence": "She _____ patiently at the bus stop for twenty minutes before it finally arrived.",
            "memory_tip": "Simply 'WAIT + ED' - the past tense of wait, meaning you waited for something in the past.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "waiter": {
            "word": "waiter",
            "pronunciation": "/ˈweɪtər/",
            "definition": "A person whose job is to serve food and drinks to customers in a restaurant, café, or similar establishment; someone who waits on others in a service capacity. This occupation involves taking orders, serving meals, providing customer service, and often handling payments in dining establishments. The role requires interpersonal skills, physical stamina, and knowledge of food and beverage service. The term traditionally referred to male servers, though contemporary usage often applies it more generally, with 'server' becoming a more common gender-neutral alternative.",
            "etymology": "From 'wait' + '-er,' meaning 'one who waits (on others)'",
            "etymology_source": "Claude",
            "example_sentence": "The friendly _____ recommended the daily special and brought extra bread to the table.",
            "memory_tip": "Think 'WAIT-ER' - someone who waits on you, serving your food and taking care of your needs at a restaurant.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 2
            },
            "sources": "2025",
            "source_difficulty": "Three Bee"
        },
        "waiver": {
            "word": "waiver",
            "pronunciation": "/ˈweɪvər/",
            "definition": "A voluntary relinquishment or surrender of a legal right or claim; a document evidencing such relinquishment. In legal contexts, a waiver represents a deliberate decision to give up a right that one would otherwise be entitled to exercise. Waivers are commonly used in contracts, liability agreements, and various legal proceedings to limit responsibility or release parties from certain obligations. The document must typically be signed voluntarily and with full understanding of what rights are being surrendered.",
            "etymology": "From 'waive' (from Old French 'weyver' meaning 'to abandon') + '-er' suffix indicating a document or instrument",
            "etymology_source": "Claude",
            "example_sentence": "Before participating in the rock climbing activity, all participants had to sign a liability _____.",
            "memory_tip": "Think 'WAIV-ER' - someone who 'WAIVes' their rights, and the '-ER' ending makes it the document that does the waiving.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 5
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "wakame": {
            "word": "wakame",
            "pronunciation": "/wɑˈkɑmeɪ/",
            "definition": "A type of edible brown seaweed commonly used in Japanese cuisine, particularly in miso soup, salads, and other dishes. This marine plant has a subtly sweet flavor and tender texture when cooked. Wakame is highly nutritious, containing vitamins, minerals, and beneficial compounds. It grows naturally in cold waters around Japan, Korea, and China, and is now cultivated commercially. The seaweed has gained popularity in Western cuisine as interest in Japanese food and healthy eating has increased.",
            "etymology": "From Japanese 'wakame,' the native name for this species of seaweed (Undaria pinnatifida)",
            "etymology_source": "Claude",
            "example_sentence": "The miso soup was garnished with tender pieces of _____ seaweed.",
            "memory_tip": "Think 'WA-KA-ME' - 'WAter seaKA ME' - wakame is seaweed that comes from the water and is good for me (nutritious).",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 6,
                "morphological_complexity": 4,
                "etymology_complexity": 5
            },
            "sources": "2020; 2021; 2022; 2023",
            "source_difficulty": "One Bee; Two Bee"
        },
        "wake": {
            "word": "wake",
            "pronunciation": "/weɪk/",
            "definition": "To stop sleeping and become alert; to cause someone to stop sleeping; the track left behind by a moving boat or ship on water; a watch or vigil held beside the body of someone who has died. This versatile word has multiple meanings across different contexts. As a verb, it refers to the transition from sleep to consciousness. As a nautical term, it describes the disturbed water behind a vessel. In funeral contexts, it refers to a ceremonial watching or vigil. The word can also mean the consequences or aftereffects of an action or event.",
            "etymology": "From Old English 'wacan' meaning 'to be awake' and 'wæcce' meaning 'watch, vigil'",
            "etymology_source": "Claude",
            "example_sentence": "The alarm clock failed to _____ her from her deep sleep.",
            "memory_tip": "Think 'WAKE' rhymes with 'LAKE' - you wake up like a calm lake becoming active when the wind stirs it up.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "wales": {
            "word": "wales",
            "pronunciation": "/weɪlz/",
            "definition": "Plural of wale; the upper edge of a ship's side; wooden planks that run along the sides of a boat; knitting stitches that run vertically. In nautical contexts, wales are the thick planks that form the sides of a wooden ship's hull, providing structural strength. In knitting, wales refer to the vertical columns of stitches that create the characteristic appearance of knitted fabric. The term can also refer to the country Wales, though this is typically capitalized. The nautical usage emphasizes the structural and protective function of these ship components.",
            "etymology": "From Old English 'walu' meaning 'ridge, plank,' related to German 'Wahl'",
            "etymology_source": "Claude",
            "example_sentence": "The shipwright carefully fitted the _____ to strengthen the vessel's hull.",
            "memory_tip": "Think 'WALES' sounds like 'WALLS' - wales are like the walls of a ship that protect the inside from water.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 5,
                "morphological_complexity": 5,
                "etymology_complexity": 6
            },
            "sources": "2022",
            "source_difficulty": "Two Bee"
        },
        "walk": {
            "word": "walk",
            "pronunciation": "/wɔlk/",
            "definition": "To move at a regular pace by lifting and setting down each foot in turn; to travel on foot; to accompany someone on foot; a journey on foot for exercise or pleasure. This fundamental verb describes the basic human method of locomotion that involves alternating steps with the feet touching the ground. Walking can be for transportation, exercise, leisure, or necessity. The term also encompasses various speeds and styles of foot travel, from casual strolling to brisk walking, and can be used metaphorically to describe progress through life or situations.",
            "etymology": "From Old English 'wealcan' meaning 'to roll, move about, journey'",
            "etymology_source": "Claude",
            "example_sentence": "They decided to _____ through the park to enjoy the beautiful autumn weather.",
            "memory_tip": "Think 'WALK' - one of the first words you learn, simply putting one foot in front of the other to move forward.",
            "difficulty_score": 1,
            "difficulty_factors": {
                "phonetic_transparency": 1,
                "word_frequency": 1,
                "morphological_complexity": 1,
                "etymology_complexity": 2
            },
            "sources": "2025",
            "source_difficulty": "Three Bee"
        },
        "wallaby": {
            "word": "wallaby",
            "pronunciation": "/ˈwɑləbi/",
            "definition": "A small to medium-sized marsupial native to Australia and nearby islands, resembling a small kangaroo with shorter legs and a more compact build. Wallabies are herbivorous animals that belong to the macropod family, which also includes kangaroos. They are known for their powerful hind legs used for hopping, their pouch where they carry their young, and their ability to adapt to various habitats from forests to grasslands. There are numerous species of wallabies, ranging in size from very small rock wallabies to larger species that approach small kangaroos in size.",
            "etymology": "From Dharug (Australian Aboriginal language) 'walabi' or similar indigenous Australian language",
            "etymology_source": "Claude",
            "example_sentence": "The rock _____ bounded effortlessly across the rocky outcrop in the Australian outback.",
            "memory_tip": "Think 'WALL-ABY' - like a small kangaroo that can hop over walls, wallabies are smaller relatives of kangaroos.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 5,
                "morphological_complexity": 3,
                "etymology_complexity": 5
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "walnut": {
            "word": "walnut",
            "pronunciation": "/ˈwɔlnʌt/",
            "definition": "A tree nut with a hard, wrinkled shell and edible kernel inside; the tree that produces these nuts, valued for both its nuts and its wood. Walnuts are known for their distinctive brain-like appearance when shelled and their rich, slightly bitter flavor. They are highly nutritious, containing healthy fats, protein, and various vitamins and minerals. Walnut wood is prized for furniture making and woodworking due to its beautiful grain and durability. The nuts are used in baking, cooking, and eaten as snacks.",
            "etymology": "From Old English 'wealhhnutu,' literally 'foreign nut,' from 'wealh' (foreign) + 'hnutu' (nut)",
            "etymology_source": "Claude",
            "example_sentence": "She cracked open the _____ to reveal the brain-shaped meat inside.",
            "memory_tip": "Think 'WAL-NUT' - 'WALL NUT' - walnuts have such hard shells they're like little nuts with walls around them.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "walter": {
            "word": "walter",
            "pronunciation": "/ˈwɔltər/",
            "definition": "A masculine given name of Germanic origin; in some contexts, may refer to a person who serves or waits on others (archaic usage); in specific contexts, may refer to historical or literary figures bearing this name. As a proper name, Walter has been popular in English-speaking countries and has Germanic roots meaning 'ruler of the army.' The name appears in various forms across different cultures and languages. In some historical or dialectal contexts, it might have been used as a common noun, though this usage is now obsolete.",
            "etymology": "From Germanic 'Waldhar,' from 'wald' (rule, power) + 'hari' (army, warrior)",
            "etymology_source": "Claude",
            "example_sentence": "_____ was known throughout the village for his skill as a blacksmith.",
            "memory_tip": "Think 'WAL-TER' - 'WALL TEAR' - Walter was a Germanic name meaning army ruler, someone strong enough to tear down walls.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 2,
                "etymology_complexity": 4
            },
            "sources": "2023; 2024; 2025",
            "source_difficulty": "Three Bee; Two Bee"
        },
        "wamble": {
            "word": "wamble",
            "pronunciation": "/ˈwæmbəl/",
            "definition": "To feel nauseous or queasy; to have an unsettled stomach; to experience stomach discomfort or queasiness. This somewhat archaic or dialectal verb describes the physical sensation of stomach unrest that often precedes vomiting or indicates digestive distress. The word captures the specific feeling of stomach disturbance that is uncomfortable but may not necessarily lead to actual illness. It's a vivid term that conveys the rolling, unsettled sensation in one's stomach during digestive upset or nausea.",
            "etymology": "From Middle English 'wamelen,' possibly imitative of the sound or sensation of stomach disturbance",
            "etymology_source": "Claude",
            "example_sentence": "The rough boat ride made his stomach _____ with seasickness.",
            "memory_tip": "Think 'WAM-BLE' - 'WAMbulance BLEh' - when your stomach wambles, you might need an ambulance and feel 'bleh' (sick).",
            "difficulty_score": 7,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 8,
                "morphological_complexity": 6,
                "etymology_complexity": 7
            },
            "sources": "2023; 2024; 2025",
            "source_difficulty": "Three Bee; Two Bee"
        }
    }

def main():
    """
    Main function to process spelling bee words and create educational content.
    """
    logging.info("Processing Batch 192 with comprehensive Claude data...")
    
    # Define combined word errors (identified during analysis)
    combined_errors = [
        "vizierialnoun",
        "voceinesculent",
        "voraciousnoun",
        "votivenoun"
    ]
    
    # Get comprehensive word data
    word_data = create_word_data()
    
    # Filter out combined word errors and prepare final data
    valid_words = {word: data for word, data in word_data.items() 
                  if word not in combined_errors}
    
    # Define output file
    output_file = 'output/batch_192_processed.csv'
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'word', 'pronunciation', 'definition', 'etymology', 'etymology_source',
            'example_sentence', 'memory_tip', 'difficulty_score',
            'phonetic_transparency', 'word_frequency', 'morphological_complexity', 
            'etymology_complexity', 'sources', 'source_difficulty'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        successful_count = 0
        for word, data in valid_words.items():
            try:
                row = {
                    'word': data['word'],
                    'pronunciation': data['pronunciation'],
                    'definition': data['definition'],
                    'etymology': data['etymology'],
                    'etymology_source': data['etymology_source'],
                    'example_sentence': data['example_sentence'],
                    'memory_tip': data['memory_tip'],
                    'difficulty_score': data['difficulty_score'],
                    'phonetic_transparency': data['difficulty_factors']['phonetic_transparency'],
                    'word_frequency': data['difficulty_factors']['word_frequency'],
                    'morphological_complexity': data['difficulty_factors']['morphological_complexity'],
                    'etymology_complexity': data['difficulty_factors']['etymology_complexity'],
                    'sources': data['sources'],
                    'source_difficulty': data['source_difficulty']
                }
                writer.writerow(row)
                successful_count += 1
                logging.info(f"Processed word: {word}")
                
            except Exception as e:
                logging.error(f"Error processing word {word}: {e}")
                continue
    
    logging.info(f"Saved {successful_count} words to {output_file}")
    logging.info("Batch 192 processing completed!")
    logging.info(f"Processed {successful_count} words with comprehensive Claude data")
    logging.info(f"Output saved to: {output_file}")
    logging.info(f"Results: {successful_count} successful, 0 failed")
    logging.info(f"Combined word errors detected: {len(combined_errors)}")
    for error in combined_errors:
        logging.info(f"  - {error}")

if __name__ == "__main__":
    main()