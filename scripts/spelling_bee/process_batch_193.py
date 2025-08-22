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
        "wampanoag": {
            "word": "wampanoag",
            "pronunciation": "/ˌwæmpəˈnoʊæɡ/",
            "definition": "A member of a Native American confederacy of southeastern Massachusetts and Rhode Island; relating to this people or their language. The Wampanoag were among the first Native Americans to encounter European colonists, including the Pilgrims at Plymouth in 1620. They played a crucial role in the survival of the early Plymouth Colony, with leaders like Massasoit establishing peaceful relations and trade agreements. The Wampanoag people have a rich cultural heritage including traditional crafts, agriculture (particularly the 'Three Sisters' crops of corn, beans, and squash), and oral traditions that continue to this day.",
            "etymology": "From Narragansett 'wampanooag,' meaning 'eastern people' or 'people of the dawn land'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ tribe taught the Plymouth colonists essential farming techniques for survival.",
            "memory_tip": "Think 'WAM-PAN-O-AG' - 'WAMpum PAN O AGriculture' - the Wampanoag people were known for wampum beads and shared agricultural knowledge.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 6,
                "word_frequency": 6,
                "morphological_complexity": 6,
                "etymology_complexity": 6
            },
            "sources": "2024; 2025",
            "source_difficulty": "Three Bee"
        },
        "wand": {
            "word": "wand",
            "pronunciation": "/wænd/",
            "definition": "A thin rod or stick, especially one used by a magician, fairy, or conductor; a staff carried as a symbol of office or authority; a handheld electronic device used for scanning or pointing. In fantasy and magic contexts, wands are portrayed as tools for casting spells or channeling magical power. In music, a conductor's wand (baton) is used to direct orchestral performances. In technology, wands can refer to barcode scanners or remote pointing devices. The term suggests precision, control, and the ability to direct or influence from a distance.",
            "etymology": "From Old Norse 'vöndr' meaning 'rod, stick,' related to 'vind' meaning 'to wind'",
            "etymology_source": "Claude",
            "example_sentence": "The conductor raised his _____ to signal the beginning of the symphony.",
            "memory_tip": "Think 'WAND' rhymes with 'HAND' - a wand is held in your hand to direct or control things, like magic or music.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 3,
                "morphological_complexity": 1,
                "etymology_complexity": 3
            },
            "sources": "2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "want": {
            "word": "want",
            "pronunciation": "/wænt/",
            "definition": "To have a desire to possess or do something; to wish for; to lack or be without something necessary; to be deficient in. As a verb, it expresses desire, need, or intention. As a noun, it refers to a lack or deficiency of something essential, or a desire for something. The word encompasses both emotional desires (wanting happiness) and practical needs (wanting food). It can indicate everything from casual preferences to urgent necessities, making it one of the most fundamental expressions of human motivation and need.",
            "etymology": "From Old Norse 'vanta' meaning 'to lack, be wanting'",
            "etymology_source": "Claude",
            "example_sentence": "Children often _____ what they cannot have more than what they already possess.",
            "memory_tip": "Think 'WANT' - one of the most basic words expressing human desire and need, fundamental to communication.",
            "difficulty_score": 1,
            "difficulty_factors": {
                "phonetic_transparency": 1,
                "word_frequency": 1,
                "morphological_complexity": 1,
                "etymology_complexity": 2
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "wapiti": {
            "word": "wapiti",
            "pronunciation": "/ˈwæpɪti/",
            "definition": "The North American elk, a large deer species native to North America and eastern Asia; one of the largest species in the deer family. Wapiti are characterized by their impressive antlers (in males), light-colored rump patch, and distinctive bugling call during mating season. These animals are herbivores that typically inhabit forests and mountain meadows. The term is preferred by some wildlife biologists and indigenous peoples to distinguish the North American species from the smaller European elk, which is actually what Americans call a moose.",
            "etymology": "From Shawnee 'wapiti' meaning 'white rump,' referring to the animal's distinctive white patch",
            "etymology_source": "Claude",
            "example_sentence": "The majestic _____ bugled across the valley during the autumn rutting season.",
            "memory_tip": "Think 'WA-PI-TI' - 'WAter PIcTure Island' - wapiti (elk) are often seen near water and make picture-perfect scenes in island-like meadows.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 7,
                "morphological_complexity": 5,
                "etymology_complexity": 6
            },
            "sources": "2022; 2023; 2024",
            "source_difficulty": "Three Bee; Two Bee"
        },
        "warden": {
            "word": "warden",
            "pronunciation": "/ˈwɔrdən/",
            "definition": "A person responsible for the supervision and security of a prison; an official charged with enforcing regulations in a particular area or institution; a guardian or keeper of something. The term applies to various supervisory roles, from prison wardens who oversee correctional facilities to park wardens who protect natural areas, fire wardens who monitor fire safety, and church wardens who assist with religious administration. The position typically involves authority, responsibility for safety and order, and accountability to higher authorities or the public.",
            "etymology": "From Old French 'wardein,' from Germanic 'ward' meaning 'to guard' + suffix '-en'",
            "etymology_source": "Claude",
            "example_sentence": "The prison _____ implemented new programs to improve rehabilitation and reduce recidivism.",
            "memory_tip": "Think 'WARD-EN' - someone who 'WARDs' off danger and keeps people safe, like a guardian with the suffix '-en' for a person.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 4,
                "morphological_complexity": 3,
                "etymology_complexity": 3
            },
            "sources": "2021",
            "source_difficulty": "One Bee"
        },
        "wardrobe": {
            "word": "wardrobe",
            "pronunciation": "/ˈwɔrdroʊb/",
            "definition": "A large cupboard or closet for storing clothes; the collection of clothes owned by a person, organization, or for a particular purpose; the costume department of a theater or film production. The term encompasses both the physical storage space for clothing and the clothing collection itself. In entertainment industry contexts, wardrobe refers to the department responsible for costume design, maintenance, and organization. A person's wardrobe reflects their style, profession, and lifestyle, and can range from basic functional clothing to extensive fashion collections.",
            "etymology": "From Old French 'warderobe,' from 'warder' (to guard) + 'robe' (garment), originally meaning 'guarded room for robes'",
            "etymology_source": "Claude",
            "example_sentence": "The actor's _____ for the period drama included authentic Victorian-era costumes.",
            "memory_tip": "Think 'WARD-ROBE' - a place that 'WARDs' (guards) your 'ROBE' and other clothes safely.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2022",
            "source_difficulty": "Two Bee"
        },
        "warison": {
            "word": "warison",
            "pronunciation": "/ˈwærɪsən/",
            "definition": "An archaic term meaning reward, recompense, or retribution; payment given for services or as compensation; sometimes used to mean vengeance or punishment. This obsolete or rare word appears primarily in historical texts, medieval literature, or academic contexts discussing older forms of English. It could refer to both positive rewards for good service and negative consequences for wrongdoing. The term reflects older concepts of justice and compensation that were common in medieval legal and social systems.",
            "etymology": "From Old French 'warison' meaning 'healing, cure, reward,' from 'warir' meaning 'to protect, heal'",
            "etymology_source": "Claude",
            "example_sentence": "The knight expected fair _____ for his loyal service to the realm.",
            "memory_tip": "Think 'WAR-I-SON' - 'WAR I won, SON' - in old times, a warrior son might expect warison (reward) for winning wars.",
            "difficulty_score": 8,
            "difficulty_factors": {
                "phonetic_transparency": 7,
                "word_frequency": 9,
                "morphological_complexity": 7,
                "etymology_complexity": 8
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "warm": {
            "word": "warm",
            "pronunciation": "/wɔrm/",
            "definition": "Having or giving off heat; having a moderate degree of heat; showing enthusiasm, friendliness, or affection; comfortable and cozy. This fundamental adjective describes temperature that is neither hot nor cold but pleasantly heated. Metaphorically, it describes personality traits (warm person), emotions (warm feelings), colors (warm tones like red and orange), and social interactions (warm welcome). The word can also function as a verb meaning to make or become warm, and suggests comfort, safety, and positive emotions.",
            "etymology": "From Old English 'wearm,' from Germanic origin, related to German 'warm'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ sunshine felt wonderful after the long, cold winter.",
            "memory_tip": "Think 'WARM' - one of the most basic words for comfortable temperature and friendly feelings.",
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
        "warning": {
            "word": "warning",
            "pronunciation": "/ˈwɔrnɪŋ/",
            "definition": "A statement or event that indicates a possible or impending danger, problem, or unpleasant situation; advance notice of something threatening or undesirable. Warnings serve to alert people to potential risks so they can take preventive action or prepare for consequences. They can be formal (legal warnings, weather warnings) or informal (friendly advice), immediate (fire alarm) or long-term (health warnings). The purpose is always protective, giving recipients the opportunity to avoid harm or make informed decisions.",
            "etymology": "From Old English 'warnian' meaning 'to give notice of danger' + suffix '-ing'",
            "etymology_source": "Claude",
            "example_sentence": "The weather service issued a severe storm _____ for the coastal region.",
            "memory_tip": "Think 'WARN-ING' - currently 'WARNing' someone about danger or problems that might be coming.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "warrior": {
            "word": "warrior",
            "pronunciation": "/ˈwɔriər/",
            "definition": "A person engaged in or experienced in warfare; a fighter or soldier, especially one who is brave and experienced; someone who shows great vigor and courage in fighting for a cause. The term encompasses both literal fighters in military conflicts and metaphorical fighters who battle against challenges, diseases, or social issues. Warriors are characterized by courage, skill in combat, dedication to their cause, and willingness to face danger. In many cultures, the warrior represents ideals of honor, bravery, and sacrifice for the greater good.",
            "etymology": "From Old French 'werreier,' from 'werre' meaning 'war' + suffix '-ier' meaning 'one who'",
            "etymology_source": "Claude",
            "example_sentence": "The ancient _____ fought bravely to defend his homeland from invaders.",
            "memory_tip": "Think 'WAR-RI-OR' - 'WAR' + 'RI' + 'OR' - someone who fights in war, or fights for important causes.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 3
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "washing": {
            "word": "washing",
            "pronunciation": "/ˈwɑʃɪŋ/",
            "definition": "The action of cleaning something with water and usually soap or detergent; the process of laundering clothes; items that have been or are to be washed. This common household activity involves removing dirt, stains, and odors from clothing, dishes, bodies, or other objects through the use of water and cleaning agents. The term can refer to the act itself, the items being cleaned, or the result of the cleaning process. Modern washing often involves machines, though hand washing remains common for delicate items.",
            "etymology": "From Old English 'wæscan' meaning 'to wash' + present participle suffix '-ing'",
            "etymology_source": "Claude",
            "example_sentence": "She hung the _____ on the line to dry in the warm afternoon sun.",
            "memory_tip": "Think 'WASH-ING' - currently 'WASHing' clothes or other items to clean them.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 2
            },
            "sources": "2023",
            "source_difficulty": "Two Bee"
        },
        "washington": {
            "word": "washington",
            "pronunciation": "/ˈwɑʃɪŋtən/",
            "definition": "The capital city of the United States; a state in the Pacific Northwest region of the United States; referring to George Washington, the first President of the United States. As a proper noun, it most commonly refers to Washington, D.C., the seat of the federal government, or Washington State on the Pacific coast. The name honors George Washington, the founding father and first president. In various contexts, it can represent American government, politics, or power (as in 'decisions made in Washington').",
            "etymology": "Named after George Washington, whose surname comes from Old English 'Wassingatun' meaning 'settlement of Wassa's people'",
            "etymology_source": "Claude",
            "example_sentence": "The legislation was debated extensively before being passed in _____.",
            "memory_tip": "Think 'WASHING-TON' - like 'washing a ton' of clothes, but it's actually named after President Washington.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 2,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "wasn": {
            "word": "wasn",
            "pronunciation": "/ˈwʌzən/ or /ˈwæzən/",
            "definition": "Informal contraction of 'was not'; used primarily in casual speech and informal writing to express negation of past tense being or existence. This contraction represents colloquial speech patterns where 'was not' is shortened for ease of pronunciation and conversational flow. While not typically found in formal writing, it appears in dialogue, informal texts, and representations of spoken language. The pronunciation and usage can vary by dialect and region.",
            "etymology": "Contraction of 'was not,' where 'was' comes from Old English 'wæs' (past tense of 'to be')",
            "etymology_source": "Claude",
            "example_sentence": "He _____ ready for the test despite studying all night.",
            "memory_tip": "Think 'WASN' = 'WAS + N(ot)' - a shortened way to say 'was not' in casual conversation.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 2
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "wasp": {
            "word": "wasp",
            "pronunciation": "/wæsp/",
            "definition": "A flying insect with a narrow waist and bright yellow and black stripes, capable of stinging; a person who is spiteful or snappish. These insects are distinguished from bees by their smooth bodies, defined waist, and ability to sting multiple times. Wasps can be social (living in colonies) or solitary, and they play important ecological roles as both predators of other insects and pollinators. Some species are beneficial to gardens and agriculture, while others can be aggressive and pose risks to humans, especially those allergic to their stings.",
            "etymology": "From Old English 'wæsp,' from Germanic origin, related to German 'Wespe'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ built its nest under the eaves of the house.",
            "memory_tip": "Think 'WASP' has a sharp 'P' sound at the end, just like a wasp has a sharp stinger that can hurt you.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 3,
                "morphological_complexity": 1,
                "etymology_complexity": 3
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "wassail": {
            "word": "wassail",
            "pronunciation": "/ˈwæseɪl/",
            "definition": "A hot mulled cider drink traditionally consumed during winter celebrations, especially Christmas and New Year; a festive drinking salute or toast; the act of going from house to house singing carols and drinking. This tradition dates back to medieval England and involves a warm alcoholic beverage typically made with ale or cider, spices, and sometimes eggs. Wassailing also refers to the custom of visiting orchards to sing to trees and pour cider on their roots to ensure a good harvest, combining agricultural ritual with community celebration.",
            "etymology": "From Old Norse 'ves heill' meaning 'be well' or 'be whole,' a greeting or toast",
            "etymology_source": "Claude",
            "example_sentence": "The carolers went _____ through the neighborhood, sharing warm cider and holiday songs.",
            "memory_tip": "Think 'WAS-SAIL' - 'WAS SAILing' through the neighborhood with warm drinks and songs during winter holidays.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 6,
                "morphological_complexity": 4,
                "etymology_complexity": 6
            },
            "sources": "2020; 2021; 2022; 2023; 2024",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "watch": {
            "word": "watch",
            "pronunciation": "/wɑtʃ/",
            "definition": "To look at or observe attentively over time; to keep under careful observation; a small timepiece worn on the wrist or carried in a pocket; a period of duty or vigil. As a verb, it means to observe, monitor, or pay attention to something or someone. As a noun, it refers to a portable timepiece or a period of standing guard. The word encompasses both passive observation (watching television) and active surveillance (watching for danger), as well as the concept of time measurement and vigilant duty.",
            "etymology": "From Old English 'wæcce' meaning 'vigil, watch,' related to 'wacian' meaning 'to be awake'",
            "etymology_source": "Claude",
            "example_sentence": "She liked to _____ the sunset from her balcony every evening.",
            "memory_tip": "Think 'WATCH' - you use your eyes to watch things, and you use a watch to see the time.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 1,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2021",
            "source_difficulty": "One Bee"
        },
        "watched": {
            "word": "watched",
            "pronunciation": "/wɑtʃt/",
            "definition": "Past tense of watch; observed attentively; kept under surveillance; looked at something or someone over a period of time in the past. This indicates completed action of observation, monitoring, or attention-paying. The watching could have been casual (watched a movie), protective (watched children), or investigative (watched for clues). The past tense indicates that the observation has concluded, though it may have lasted for varying periods of time.",
            "etymology": "From Old English 'wæcce' (vigil, watch) + past tense suffix '-ed'",
            "etymology_source": "Claude",
            "example_sentence": "The detective _____ the suspect's house for three hours before making an arrest.",
            "memory_tip": "Simply 'WATCH + ED' - you watched something in the past, the action of watching is completed.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "waters": {
            "word": "waters",
            "pronunciation": "/ˈwɔtərz/",
            "definition": "Plural form of water; bodies of water such as seas, lakes, or rivers; the liquid H2O in multiple contexts or locations; springs or spas known for therapeutic properties. The term can refer to territorial waters (national boundaries), international waters (open ocean), or specific water bodies (the waters of Lake Michigan). It can also mean multiple sources of water, different types of water (fresh waters, salt waters), or water-based substances. In some contexts, it refers to amniotic fluid or baptismal water.",
            "etymology": "From Old English 'wæter' meaning 'water' + plural suffix '-s'",
            "etymology_source": "Claude",
            "example_sentence": "The ship navigated through international _____ to reach the distant port.",
            "memory_tip": "Simply 'WATER + S' - multiple bodies of water or different types of water.",
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
        "wattage": {
            "word": "wattage",
            "pronunciation": "/ˈwɑtɪdʒ/",
            "definition": "The amount of electrical power expressed in watts; the power consumption or output rating of an electrical device; metaphorically, the power, energy, or influence someone possesses. In electrical contexts, wattage indicates how much power a device uses or produces, helping consumers understand energy consumption and costs. Higher wattage typically means brighter lights, more powerful motors, or greater energy consumption. The term has expanded metaphorically to describe personal power or influence ('star wattage' in entertainment).",
            "etymology": "From 'watt' (unit of power named after James Watt) + suffix '-age' indicating amount or collection",
            "etymology_source": "Claude",
            "example_sentence": "The new LED bulbs provide the same brightness as incandescent bulbs but use much lower _____.",
            "memory_tip": "Think 'WATT-AGE' - 'WATT' (power unit) + 'AGE' (amount) - the amount of watts or electrical power something uses.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "wattles": {
            "word": "wattles",
            "pronunciation": "/ˈwætəlz/",
            "definition": "Plural form of wattle; fleshy, often brightly colored appendages hanging from the throat or chin of certain birds (like turkeys and roosters); flexible rods or branches woven together to make walls, fences, or baskets; Australian acacia trees. In bird anatomy, wattles are distinctive features used for display, temperature regulation, and species identification. In construction, wattles refer to interwoven branches traditionally used in building walls (wattle and daub construction). In botany, Australian wattles are acacia trees known for their bright yellow flowers.",
            "etymology": "From Old English 'watol' meaning 'hurdle, framework of interwoven rods'",
            "etymology_source": "Claude",
            "example_sentence": "The turkey's bright red _____ became more prominent during mating season.",
            "memory_tip": "Think 'WATT-LES' - like 'WAT(ch) LES(s)' - wattles hang down from birds' necks, so you watch less of their neck and more of the dangling wattles.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 6,
                "morphological_complexity": 4,
                "etymology_complexity": 6
            },
            "sources": "2022",
            "source_difficulty": "Two Bee"
        },
        "wave": {
            "word": "wave",
            "pronunciation": "/weɪv/",
            "definition": "A moving ridge or swell on the surface of water; a gesture of greeting or farewell made by moving the hand; a sudden occurrence or increase in a phenomenon; to move back and forth or up and down in a flowing motion. The word encompasses physical phenomena (ocean waves, sound waves, light waves), human gestures (waving hello), and metaphorical surges (wave of emotion, crime wave). It can function as both a noun describing the thing itself and a verb describing the action of moving in an undulating pattern.",
            "etymology": "From Old English 'wafian' meaning 'to wave, fluctuate,' related to 'wæf' meaning 'waving thing'",
            "etymology_source": "Claude",
            "example_sentence": "She stood on the shore watching each _____ crash against the rocks.",
            "memory_tip": "Think 'WAVE' - move your hand in a wave motion, just like water waves move back and forth.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "ways": {
            "word": "ways",
            "pronunciation": "/weɪz/",
            "definition": "Plural form of way; methods, manners, or means of doing something; paths, routes, or directions; customs, habits, or characteristic behaviors; distances or extents. This versatile word encompasses physical paths (roads, trails), methods of accomplishment (ways to solve problems), behavioral patterns (someone's ways), and cultural practices (traditional ways). It can indicate multiple options, various approaches, or different aspects of behavior and methodology. The word suggests diversity in approaches, paths, or characteristics.",
            "etymology": "From Old English 'weg' meaning 'path, road, journey' + plural suffix '-s'",
            "etymology_source": "Claude",
            "example_sentence": "There are many different _____ to approach this complex problem.",
            "memory_tip": "Simply 'WAY + S' - multiple ways, methods, or paths to do things or go places.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 2,
                "word_frequency": 1,
                "morphological_complexity": 2,
                "etymology_complexity": 2
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "wayward": {
            "word": "wayward",
            "pronunciation": "/ˈweɪwərd/",
            "definition": "Difficult to control or predict because of willful or perverse behavior; following one's own inclinations; erratic or unpredictable in direction or tendency. This adjective describes people who resist guidance or authority, often acting according to their own desires rather than following expected patterns. It can apply to behavior, movements, or tendencies that are unpredictable or contrary to what is wanted or expected. The word suggests stubbornness, independence, and a tendency to go one's own way regardless of consequences or expectations.",
            "etymology": "From Middle English 'wayward,' from 'away' + 'ward' (direction), meaning 'turned away'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ teenager refused to follow any rules or guidance from his parents.",
            "memory_tip": "Think 'WAY-WARD' - someone who is 'WAY off toWARD' the wrong direction, not following the expected path.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 5,
                "morphological_complexity": 5,
                "etymology_complexity": 5
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "weakness": {
            "word": "weakness",
            "pronunciation": "/ˈwiknəs/",
            "definition": "The state or condition of lacking strength, power, or resistance; a particular area where someone or something is deficient or vulnerable; a failing or fault in character or judgment; a self-indulgent liking or fondness for something. The term encompasses physical frailty, emotional vulnerability, character flaws, and areas of inadequate performance. It can refer to temporary conditions (weakness from illness) or permanent characteristics (structural weakness). The word also describes personal preferences that may be excessive or self-indulgent (weakness for chocolate).",
            "etymology": "From Old English 'wacu' meaning 'weak' + suffix '-ness' indicating state or condition",
            "etymology_source": "Claude",
            "example_sentence": "His greatest _____ was his inability to say no to people asking for favors.",
            "memory_tip": "Think 'WEAK-NESS' - the 'NESS' (state) of being 'WEAK' in strength, character, or resistance.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 3
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "weald": {
            "word": "weald",
            "pronunciation": "/wild/",
            "definition": "An area of open or forested rolling countryside; specifically, a former forest area in southeastern England between the North and South Downs; any wooded upland area or former woodland that has been cleared for agriculture. The term is most famously associated with the Weald of Kent, Sussex, and Surrey in England, a region once heavily forested but now characterized by farmland, villages, and remaining woodland patches. In broader usage, it refers to any similar landscape of rolling hills that were once wooded.",
            "etymology": "From Old English 'weald' meaning 'forest, woodland,' related to 'wild'",
            "etymology_source": "Claude",
            "example_sentence": "The ancient _____ stretched for miles across the countryside, dotted with small farming villages.",
            "memory_tip": "Think 'WEALD' sounds like 'WILD' - a weald is an area that was once wild forest but is now open countryside.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 7,
                "morphological_complexity": 5,
                "etymology_complexity": 6
            },
            "sources": "2024; 2025",
            "source_difficulty": "Three Bee"
        },
        "wealthy": {
            "word": "wealthy",
            "pronunciation": "/ˈwɛlθi/",
            "definition": "Having a great deal of money, resources, or assets; rich; abundant in desirable qualities or characteristics. This adjective describes individuals, families, organizations, or nations that possess significant financial resources, property, or valuable assets. Wealth can be measured in monetary terms, but the concept can also extend to richness in other valuable qualities such as natural resources, cultural heritage, or opportunities. The term suggests not just adequacy but abundance and the ability to live comfortably without financial concerns.",
            "etymology": "From Middle English 'welthe' meaning 'happiness, prosperity' + suffix '-y'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ philanthropist donated millions to educational causes.",
            "memory_tip": "Think 'WEALTH-Y' - having a lot of 'WEALTH' makes you wealthy, meaning rich and prosperous.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 3
            },
            "sources": "2024; 2025",
            "source_difficulty": "Three Bee"
        },
        "weaponry": {
            "word": "weaponry",
            "pronunciation": "/ˈwɛpənri/",
            "definition": "Weapons collectively; the design, manufacture, or study of weapons; the array or collection of weapons available to an individual, group, or military force. This term encompasses all types of weapons, from ancient tools like swords and bows to modern firearms, missiles, and sophisticated military technology. It can refer to personal armaments, military arsenals, or the broader field of weapons development and technology. The word often appears in military, historical, and strategic contexts when discussing armed capabilities or weapon systems.",
            "etymology": "From 'weapon' (from Old English 'wæpen') + suffix '-ry' indicating collection or practice",
            "etymology_source": "Claude",
            "example_sentence": "The museum's medieval _____ collection included swords, crossbows, and armor from various periods.",
            "memory_tip": "Think 'WEAPON-RY' - 'WEAPON' + 'RY' (collection) - weaponry is a collection or array of weapons.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 4,
                "morphological_complexity": 4,
                "etymology_complexity": 4
            },
            "sources": "2022; 2023; 2024; 2025",
            "source_difficulty": "Three Bee; Two Bee"
        },
        "wearing": {
            "word": "wearing",
            "pronunciation": "/ˈwɛrɪŋ/",
            "definition": "Present participle of wear; currently having on one's body as clothing, jewelry, or accessories; gradually damaging or diminishing through use or time; causing fatigue or exhaustion. As a verb form, it indicates ongoing action of having clothes or accessories on the body. It can also describe the process of gradual deterioration (wearing away) or the effect of being tiring or exhausting (wearing experience). The word encompasses both the physical act of having items on one's person and the process of gradual degradation.",
            "etymology": "From Old English 'werian' meaning 'to carry, wear' + present participle suffix '-ing'",
            "etymology_source": "Claude",
            "example_sentence": "She was _____ a beautiful blue dress to the formal dinner.",
            "memory_tip": "Think 'WEAR-ING' - currently 'WEARing' clothes on your body, or something 'WEARing' down over time.",
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
        "wearisome": {
            "word": "wearisome",
            "pronunciation": "/ˈwɪrisəm/",
            "definition": "Causing one to feel tired or bored; tedious, tiresome, or monotonous; mentally or physically exhausting due to length, repetition, or lack of interest. This adjective describes activities, tasks, people, or situations that drain energy, patience, or enthusiasm through their demanding, repetitive, or uninteresting nature. Wearisome experiences are characterized by their ability to make one feel fatigued not necessarily through physical exertion but through boredom, frustration, or mental strain. The word suggests something that tests one's endurance or patience.",
            "etymology": "From 'weary' (from Old English 'werig' meaning 'tired') + suffix '-some' meaning 'characterized by'",
            "etymology_source": "Claude",
            "example_sentence": "The _____ task of data entry made the afternoon seem endless.",
            "memory_tip": "Think 'WEARY-SOME' - something that makes you 'WEARY' (tired), so wearisome things tire you out or bore you.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 6,
                "morphological_complexity": 5,
                "etymology_complexity": 4
            },
            "sources": "2020; 2021; 2022; 2023",
            "source_difficulty": "One Bee; Two Bee"
        },
        "wears": {
            "word": "wears",
            "pronunciation": "/wɛrz/",
            "definition": "Third person singular present tense of wear; has on one's body as clothing or accessories; gradually damages or erodes through use; endures or lasts over time. This verb form indicates that someone currently has clothing, jewelry, or other items on their person, or that something is undergoing gradual deterioration through use. It can also refer to how well something withstands use over time (wears well) or the process of gradual erosion or damage (water wears away rock).",
            "etymology": "From Old English 'werian' meaning 'to carry, wear' + third person singular present '-s'",
            "etymology_source": "Claude",
            "example_sentence": "He always _____ a tie to work, even on casual Fridays.",
            "memory_tip": "Simply 'WEAR + S' - someone currently wears something, or something wears down over time.",
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
        "weasels": {
            "word": "weasels",
            "pronunciation": "/ˈwizəlz/",
            "definition": "Plural form of weasel; small, slender carnivorous mammals with long bodies, short legs, and keen hunting abilities; people who are sneaky, untrustworthy, or who avoid responsibility through cunning. These animals are known for their agility, intelligence, and ability to hunt prey in tight spaces. They have earned a reputation for craftiness and persistence. Metaphorically, calling someone a weasel suggests they are devious, evasive, or untrustworthy, often wriggling out of commitments or responsibilities through clever but dishonest means.",
            "etymology": "From Old English 'wesle,' of Germanic origin, related to German 'Wiesel'",
            "etymology_source": "Claude",
            "example_sentence": "The farmer struggled to keep _____ from raiding his chicken coop.",
            "memory_tip": "Think 'WEAS-ELS' - 'WEASy ELusive animalS' - weasels are small, elusive animals that are hard to catch.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 4,
                "morphological_complexity": 3,
                "etymology_complexity": 3
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "weather": {
            "word": "weather",
            "pronunciation": "/ˈwɛðər/",
            "definition": "The state of the atmosphere at a particular place and time regarding temperature, precipitation, wind, humidity, and other meteorological conditions; to withstand or endure difficult conditions; to undergo change due to exposure to atmospheric conditions. As a noun, it describes atmospheric conditions that affect daily life and activities. As a verb, it means to survive hardships or to show effects of exposure to the elements. Weather influences agriculture, transportation, recreation, and virtually all aspects of human activity.",
            "etymology": "From Old English 'weder' meaning 'air, sky, weather,' from Germanic origin",
            "etymology_source": "Claude",
            "example_sentence": "The _____ forecast predicted rain for the entire weekend.",
            "memory_tip": "Think 'WEATHER' - what you see 'WHETHER' you look outside - the atmospheric conditions around you.",
            "difficulty_score": 2,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 2,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2020; 2021",
            "source_difficulty": "One Bee"
        },
        "weave": {
            "word": "weave",
            "pronunciation": "/wiv/",
            "definition": "To interlace threads, yarns, or strips to form fabric or material; to create by interlacing; to move in and out or back and forth; to create or tell a story by combining elements. This fundamental textile process involves crossing threads over and under each other to create cloth. Metaphorically, it describes creating complex narratives (weaving a tale), moving through obstacles (weaving through traffic), or combining elements into a unified whole (weaving ideas together). The process requires skill, patience, and attention to pattern.",
            "etymology": "From Old English 'wefan' meaning 'to weave,' from Germanic origin",
            "etymology_source": "Claude",
            "example_sentence": "The skilled artisan could _____ intricate patterns into beautiful tapestries.",
            "memory_tip": "Think 'WEAVE' - like 'WE' + 'AVE' - we have the ability to weave threads together to make fabric.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 3,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2023",
            "source_difficulty": "Two Bee"
        },
        "webisode": {
            "word": "webisode",
            "pronunciation": "/ˈwɛbɪˌsoʊd/",
            "definition": "An episode of a television show or series that is created specifically for viewing on the internet rather than traditional broadcast television; a short video program distributed via the web. This modern term represents the evolution of entertainment media in the digital age, where content creators produce programming specifically for online platforms. Webisodes are often shorter than traditional TV episodes and may supplement existing shows or serve as standalone web-based series. They represent the democratization of content creation and distribution through internet technology.",
            "etymology": "Blend of 'web' (World Wide Web) + 'episode,' coined in the early 2000s with the rise of internet video",
            "etymology_source": "Claude",
            "example_sentence": "The popular series released a new _____ every Tuesday on their YouTube channel.",
            "memory_tip": "Think 'WEB-ISODE' - 'WEB' (internet) + 'EPISODE' - an episode made for the web instead of TV.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 5,
                "morphological_complexity": 4,
                "etymology_complexity": 3
            },
            "sources": "2020; 2022",
            "source_difficulty": "One Bee; Two Bee"
        },
        "webster": {
            "word": "webster",
            "pronunciation": "/ˈwɛbstər/",
            "definition": "An archaic term for a weaver, especially a female weaver; a surname derived from the occupation of weaving; most famously associated with Noah Webster, the American lexicographer who created Webster's Dictionary. Historically, a webster was a person whose profession involved weaving cloth, and the term was often applied specifically to women in this trade. The word has largely fallen out of use as an occupational term but survives as a surname and in historical contexts. It represents the evolution of English occupational surnames.",
            "etymology": "From Old English 'webbestre,' feminine form of 'webba' (weaver), from 'webb' (web, woven fabric)",
            "etymology_source": "Claude",
            "example_sentence": "The village _____ was known throughout the region for her fine woolen cloth.",
            "memory_tip": "Think 'WEB-STER' - 'WEB' (woven fabric) + 'STER' (person who does something) - a webster makes webs of cloth.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 6,
                "morphological_complexity": 5,
                "etymology_complexity": 6
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "websterian": {
            "word": "websterian",
            "pronunciation": "/wɛbˈstɪriən/",
            "definition": "Of, relating to, or characteristic of Noah Webster or his approach to lexicography and language; following the style or principles of Webster's dictionaries. This adjective refers to the influential American lexicographer who created the first major American dictionary and established many spelling conventions that distinguish American English from British English. Websterian principles include simplified spelling, American usage preferences, and comprehensive etymological information. The term can also refer to the scholarly, systematic approach to language documentation that Webster pioneered.",
            "etymology": "From 'Webster' (Noah Webster, 1758-1843) + suffix '-ian' meaning 'relating to or characteristic of'",
            "etymology_source": "Claude",
            "example_sentence": "The dictionary's _____ approach included detailed etymologies and American spelling preferences.",
            "memory_tip": "Think 'WEBSTER-IAN' - relating to Noah Webster, like 'Victorian' relates to Queen Victoria - having Webster's characteristics.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 7,
                "morphological_complexity": 6,
                "etymology_complexity": 6
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "wedding": {
            "word": "wedding",
            "pronunciation": "/ˈwɛdɪŋ/",
            "definition": "A marriage ceremony; the celebration and formal union of two people in marriage; the act of joining or uniting closely. This significant life event typically involves legal and/or religious ceremonies that officially recognize a couple's commitment to each other. Weddings often include various traditions, celebrations, and rituals that vary by culture, religion, and personal preference. The term encompasses both the ceremony itself and the associated festivities, representing one of humanity's most universal and important social institutions.",
            "etymology": "From Old English 'weddung,' from 'weddian' meaning 'to pledge, marry'",
            "etymology_source": "Claude",
            "example_sentence": "The outdoor _____ ceremony was beautiful, with flowers decorating every arch and table.",
            "memory_tip": "Think 'WED-DING' - 'WED' (marry) + 'DING' (like wedding bells ringing) - a wedding is when people wed and bells ring.",
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
        "wednesday": {
            "word": "wednesday",
            "pronunciation": "/ˈwɛnzdeɪ/",
            "definition": "The fourth day of the week in most Western calendars, falling between Tuesday and Thursday; often considered the middle of the work week. Wednesday derives its name from the Germanic god Woden (or Odin in Norse mythology), continuing the pattern of weekday names based on ancient deities. In many cultures, Wednesday represents the midpoint of the traditional work week, often called 'hump day' because it represents getting over the 'hump' toward the weekend. The day has various cultural and religious significances across different traditions.",
            "etymology": "From Old English 'Wodnesdæg,' meaning 'Woden's day,' named after the Germanic god Woden (Odin)",
            "etymology_source": "Claude",
            "example_sentence": "The team meeting was scheduled for _____ afternoon at two o'clock.",
            "memory_tip": "Think 'WEDNES-DAY' - sounds like 'WED-NES-DAY' - the day in the middle of the week when you might feel 'wedged' between work days.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 2,
                "morphological_complexity": 4,
                "etymology_complexity": 5
            },
            "sources": "2025",
            "source_difficulty": "Three Bee"
        },
        "weevil": {
            "word": "weevil",
            "pronunciation": "/ˈwivəl/",
            "definition": "A small beetle with a long snout, many species of which are agricultural pests that damage crops, stored grains, and other plant materials. Weevils are characterized by their distinctive elongated mouthparts (rostrum) which they use to bore into plant material to feed and lay eggs. They can cause significant economic damage to crops like cotton (boll weevil), grains, nuts, and fruits. Many species are considered serious agricultural pests, though some have been used as biological control agents against invasive plants.",
            "etymology": "From Old English 'wifel,' of Germanic origin, related to German 'Wiebel'",
            "etymology_source": "Claude",
            "example_sentence": "The farmer discovered that _____ had infested his stored wheat grain.",
            "memory_tip": "Think 'WEE-VIL' - 'WEE' (small) + 'VILe' - weevils are small vile bugs that damage crops and stored food.",
            "difficulty_score": 4,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 5,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2020",
            "source_difficulty": "One Bee"
        },
        "weigh": {
            "word": "weigh",
            "pronunciation": "/weɪ/",
            "definition": "To determine the weight of something by using scales or balance; to have a particular weight; to consider carefully; to be a burden or source of worry. This versatile verb encompasses both physical measurement (weighing objects) and mental processes (weighing options). It can indicate the act of measuring mass, having a certain heaviness, or carefully considering decisions or evidence. The word also suggests evaluation, comparison, and the influence that factors have on decisions or outcomes.",
            "etymology": "From Old English 'wegan' meaning 'to carry, bear, move,' related to 'way' and 'wagon'",
            "etymology_source": "Claude",
            "example_sentence": "She needed to _____ the ingredients carefully to ensure the recipe turned out perfectly.",
            "memory_tip": "Think 'WEIGH' sounds like 'WAY' - you need to find the way to measure how heavy something is, or weigh your options to find the way forward.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 3,
                "morphological_complexity": 2,
                "etymology_complexity": 3
            },
            "sources": "2024; 2025",
            "source_difficulty": "Three Bee"
        },
        "weird": {
            "word": "weird",
            "pronunciation": "/wɪrd/",
            "definition": "Strange, unusual, or difficult to explain; having supernatural or unearthly qualities; suggesting something beyond normal experience. This adjective describes things that deviate from the ordinary, expected, or rational in ways that may be unsettling, mysterious, or simply odd. The word can range from mildly unusual (weird coincidence) to genuinely eerie or supernatural (weird phenomena). In modern usage, it's often used casually to describe anything that seems out of the ordinary or doesn't conform to normal patterns or expectations.",
            "etymology": "From Old English 'wyrd' meaning 'fate, destiny,' originally referring to supernatural fate or the power of destiny",
            "etymology_source": "Claude",
            "example_sentence": "The abandoned house had a _____ atmosphere that made everyone uncomfortable.",
            "memory_tip": "Think 'WEIRD' - when something is weird, it makes you think 'WE-iRD' (We are confused) because it's strange and unusual.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 3,
                "morphological_complexity": 2,
                "etymology_complexity": 4
            },
            "sources": "2022",
            "source_difficulty": "Two Bee"
        },
        "weka": {
            "word": "weka",
            "pronunciation": "/ˈwɛkə/",
            "definition": "A flightless brown bird native to New Zealand, belonging to the rail family; a stocky, curious bird known for its boldness and omnivorous diet. Wekas are characterized by their inability to fly, their inquisitive nature, and their tendency to investigate human settlements. They have brown plumage, strong legs for running, and are known to eat a wide variety of foods including insects, small animals, eggs, and even human food scraps. These birds are endemic to New Zealand and play important roles in Maori culture and New Zealand's natural heritage.",
            "etymology": "From Maori 'weka,' the native New Zealand name for this bird",
            "etymology_source": "Claude",
            "example_sentence": "The curious _____ approached the campsite, looking for food scraps left by the hikers.",
            "memory_tip": "Think 'WE-KA' - 'WE KAnnot fly' - the weka is a New Zealand bird that cannot fly but is very curious and bold.",
            "difficulty_score": 6,
            "difficulty_factors": {
                "phonetic_transparency": 5,
                "word_frequency": 7,
                "morphological_complexity": 5,
                "etymology_complexity": 6
            },
            "sources": "2021; 2022; 2023; 2024",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "welcome": {
            "word": "welcome",
            "pronunciation": "/ˈwɛlkəm/",
            "definition": "A greeting to someone arriving; gladly received or admitted; pleasing because it fulfills a need or desire; to greet someone in a warm and friendly way; to be pleased to receive or experience. This word functions as a greeting, an adjective describing positive reception, and a verb meaning to receive gladly. It represents hospitality, openness, and positive acknowledgment of someone's arrival or presence. The concept encompasses both formal and informal expressions of acceptance and hospitality.",
            "etymology": "From Old English 'wilcuma,' from 'wil' (pleasure) + 'cuma' (guest), literally meaning 'pleasing guest'",
            "etymology_source": "Claude",
            "example_sentence": "The hotel staff provided a warm _____ to all arriving guests.",
            "memory_tip": "Think 'WEL-COME' - 'WELL COME' - when someone is welcome, they are well (good) to come visit you.",
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
        "welding": {
            "word": "welding",
            "pronunciation": "/ˈwɛldɪŋ/",
            "definition": "The process of joining metals or thermoplastics by heating them to their melting point and fusing them together; the trade or skill of performing such joining operations. This industrial technique uses various methods including arc welding, gas welding, and resistance welding to create strong, permanent bonds between materials. Welding is essential in construction, manufacturing, automotive repair, and many other industries. The process requires skill, proper equipment, and safety measures due to the high temperatures and potentially dangerous conditions involved.",
            "etymology": "From 'weld' (from Old English 'wealdan' meaning 'to control, wield') + present participle suffix '-ing'",
            "etymology_source": "Claude",
            "example_sentence": "The skilled craftsman was _____ the steel beams together to complete the building's framework.",
            "memory_tip": "Think 'WELD-ING' - currently 'WELDing' metals together by heating and fusing them into one piece.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 3,
                "morphological_complexity": 3,
                "etymology_complexity": 4
            },
            "sources": "2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        },
        "welsh": {
            "word": "welsh",
            "pronunciation": "/wɛlʃ/",
            "definition": "Of or relating to Wales, its people, or their Celtic language; the Celtic language spoken in Wales; to fail to honor a debt or obligation (informal, often considered offensive). As an adjective and noun, it refers to the people and culture of Wales, including their distinct Celtic heritage and language. As a verb (often considered derogatory), it means to renege on a promise or fail to pay a debt. The linguistic and cultural meanings are neutral and descriptive, while the verb usage can be considered offensive and stereotypical.",
            "etymology": "From Old English 'Wielisc' meaning 'foreign,' originally used by Anglo-Saxons to describe Celtic peoples",
            "etymology_source": "Claude",
            "example_sentence": "The _____ language has experienced a revival in recent decades with increased education and cultural programs.",
            "memory_tip": "Think 'WELSH' - like 'WELL-wish' - the Welsh people and their beautiful language and culture from Wales.",
            "difficulty_score": 3,
            "difficulty_factors": {
                "phonetic_transparency": 3,
                "word_frequency": 4,
                "morphological_complexity": 2,
                "etymology_complexity": 4
            },
            "sources": "2024",
            "source_difficulty": "Three Bee"
        },
        "welterweight": {
            "word": "welterweight",
            "pronunciation": "/ˈwɛltərˌweɪt/",
            "definition": "A weight class in boxing and other combat sports, typically ranging from about 140 to 147 pounds (63.5 to 66.7 kg); a competitor in this weight class. This division represents one of the traditional weight categories in professional boxing, positioned between lightweight and middleweight classes. Welterweight has historically been one of the most popular and competitive divisions in boxing, featuring many legendary champions. The weight limits may vary slightly between different boxing organizations and other combat sports like mixed martial arts.",
            "etymology": "From 'welter' (meaning 'to roll about, wallow') + 'weight,' originally referring to a heavy horseman or someone who welters",
            "etymology_source": "Claude",
            "example_sentence": "The _____ champion defended his title successfully for the third consecutive time.",
            "memory_tip": "Think 'WELTER-WEIGHT' - 'WELTER' (rolling around) + 'WEIGHT' - a weight class where fighters are big enough to really welter around in the ring.",
            "difficulty_score": 5,
            "difficulty_factors": {
                "phonetic_transparency": 4,
                "word_frequency": 6,
                "morphological_complexity": 5,
                "etymology_complexity": 6
            },
            "sources": "2020; 2021; 2022; 2023; 2024; 2025",
            "source_difficulty": "One Bee; Three Bee; Two Bee"
        }
    }

def main():
    """
    Main function to process spelling bee words and create educational content.
    """
    logging.info("Processing Batch 193 with comprehensive Claude data...")
    
    # Define combined word errors (identified during analysis)
    combined_errors = [
        "wantedsprung",
        "wapitiweka",
        "wasteweirdiamanté",
        "wealdblink"
    ]
    
    # Get comprehensive word data
    word_data = create_word_data()
    
    # Filter out combined word errors and prepare final data
    valid_words = {word: data for word, data in word_data.items() 
                  if word not in combined_errors}
    
    # Define output file
    output_file = 'output/batch_193_processed.csv'
    
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
    logging.info("Batch 193 processing completed!")
    logging.info(f"Processed {successful_count} words with comprehensive Claude data")
    logging.info(f"Output saved to: {output_file}")
    logging.info(f"Results: {successful_count} successful, 0 failed")
    logging.info(f"Combined word errors detected: {len(combined_errors)}")
    for error in combined_errors:
        logging.info(f"  - {error}")

if __name__ == "__main__":
    main()