#!/usr/bin/env python3

import csv
import logging
from pathlib import Path
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    """Calculate spelling difficulty based on multiple factors"""
    
    def __init__(self):
        self.common_words = {
            'people', 'perfect', 'performance', 'perhaps', 'period', 'permission'
        }
        
        self.uncommon_words = {
            'pendragon', 'pendulous', 'penelope', 'penicillin', 'peninsula', 'peninsular',
            'penitentiary', 'pensive', 'pentameter', 'penultimate', 'penurious', 'peony',
            'pepita', 'peplos', 'peplus', 'peppermint', 'pepysian', 'peradventure',
            'percent', 'perceptible', 'perciatelli', 'perdition', 'perdue', 'peregrination',
            'peremptory', 'perfection', 'performed', 'performer', 'performs', 'perfume',
            'perianth', 'perilous', 'periodically', 'periodontist', 'periods', 'peripheral',
            'periwinkle', 'permafrost', 'permanence', 'permutation', 'pernicious', 'perorate'
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        """Calculate how predictably a word is spelled based on pronunciation"""
        word_lower = word.lower()
        
        # Very transparent (score: 0.8-1.0) - highly predictable spelling
        transparent_patterns = ['penguin', 'peppermint', 'percent', 'perfect', 'perfume', 'perhaps', 'period']
        if word_lower in transparent_patterns:
            return 0.9
            
        # Moderately transparent (score: 0.5-0.7) - some irregular spelling
        moderate_patterns = ['people', 'peony', 'performance', 'pensive', 'perilous', 'permission']
        if word_lower in moderate_patterns:
            return 0.6
            
        # Low transparency (score: 0.2-0.4) - irregular spelling patterns
        opaque_patterns = ['pendragon', 'pendulous', 'penicillin', 'peninsula', 'peninsular', 
                          'penitentiary', 'pentameter', 'penultimate', 'penurious', 'pepita',
                          'peplos', 'peplus', 'pepysian', 'peradventure', 'perceptible',
                          'perciatelli', 'perdition', 'perdue', 'peregrination', 'peremptory',
                          'perianth', 'peripheral', 'periwinkle', 'permafrost', 'permanence',
                          'permutation', 'pernicious', 'perorate']
        if word_lower in opaque_patterns:
            return 0.3
            
        return 0.5  # Default for unclassified words
    
    def _calculate_word_frequency(self, word: str) -> float:
        """Estimate word frequency in common usage"""
        word_lower = word.lower()
        
        if word_lower in self.common_words:
            return 0.8  # High frequency
        elif word_lower in self.uncommon_words:
            return 0.2  # Low frequency
        else:
            return 0.4  # Medium frequency
    
    def _calculate_morphological_complexity(self, word: str) -> float:
        """Calculate complexity based on morphological structure"""
        word_lower = word.lower()
        
        # Simple words (score: 0.8-1.0)
        if word_lower in ['people', 'penguin', 'pear', 'peach', 'peanut', 'pebble', 'pebbles', 
                         'percent', 'perfect', 'perhaps', 'period', 'periods']:
            return 0.9
            
        # Moderate complexity (score: 0.4-0.6)
        if word_lower in ['peninsula', 'peninsular', 'pensive', 'peony', 'peppermint', 
                         'performance', 'perfection', 'performed', 'performer', 'performs', 
                         'perfume', 'perilous', 'peripheral', 'permission']:
            return 0.5
            
        # High complexity (score: 0.1-0.3)
        complex_words = ['pendragon', 'pendulous', 'penicillin', 'penitentiary', 'pentameter',
                        'penultimate', 'penurious', 'pepita', 'peplos', 'peplus', 'pepysian',
                        'peradventure', 'perceptible', 'perciatelli', 'perdition', 'perdue',
                        'peregrination', 'peremptory', 'perianth', 'periodically', 'periodontist',
                        'periwinkle', 'permafrost', 'permanence', 'permutation', 'pernicious',
                        'perorate']
        if word_lower in complex_words:
            return 0.2
            
        return 0.5
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        """Calculate complexity based on etymological information"""
        if not etymology:
            return 0.5
            
        etymology_lower = etymology.lower()
        
        # Simple etymology (score: 0.8-1.0)
        if any(indicator in etymology_lower for indicator in ['old english', 'germanic', 'simple']):
            return 0.9
            
        # Moderate etymology (score: 0.4-0.6)  
        if any(indicator in etymology_lower for indicator in ['latin', 'french', 'middle english']):
            return 0.5
            
        # Complex etymology (score: 0.1-0.3)
        if any(indicator in etymology_lower for indicator in ['greek', 'multiple origins', 'compound', 'italian', 'spanish']):
            return 0.2
            
        return 0.5
    
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        """Calculate overall difficulty score and component scores"""
        
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._calculate_word_frequency(word)
        morphological_score = self._calculate_morphological_complexity(word)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score,
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'difficulty': None  # Leave null as instructed
        }

class Batch130Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data for each word using Claude's knowledge"""
        
        word_data = {
            'pendragon': {
                'definition': 'A pendragon is a legendary title meaning "chief dragon" or "head dragon," most famously associated with King Arthur in medieval literature. In Welsh tradition, the pendragon was a supreme war leader or high king who commanded other regional kings during times of conflict. The term combines the Welsh words "pen" (head or chief) and "dragon" (dragon or leader), reflecting the symbolic association of dragons with power, wisdom, and royal authority in Celtic culture. Arthur Pendragon became the archetypal figure bearing this title, representing the ideal of a unified British leader who could rally diverse tribes and kingdoms against common enemies. The concept embodies themes of sovereignty, military prowess, and the mystical connection between rulers and the land they protect. In modern usage, the term appears in fantasy literature and historical fiction as a symbol of ultimate authority and legendary leadership. The pendragon represents not just political power but also spiritual guardianship of the realm, often depicted as having supernatural abilities or divine mandate. This title has inspired countless adaptations in literature, film, and popular culture, symbolizing the archetypal hero-king who emerges in times of greatest need.',
                'pronunciation': '/ˈpɛnˌdræɡən/',
                'example_sentence': 'The ancient chronicles spoke of a legendary _____ who would unite the warring kingdoms under one banner.',
                'etymology': 'From Welsh "pen" (head, chief) + "dragon" (dragon, leader), literally meaning "chief dragon" or "head dragon." The title gained prominence in medieval Arthurian literature.',
                'memory_tip': 'Think "PEN-dragon" - the "pen" (head) of all dragons, the ultimate leader. Remember Arthur PENdragon as the chief among all rulers.'
            },
            'pendulous': {
                'definition': 'Pendulous describes something that hangs down loosely and swings freely, typically in a drooping or dangling manner. This adjective characterizes objects that are suspended and move with a swaying motion, such as branches weighted down by fruit, earrings that dangle from the ears, or architectural elements that hang from a structure. The term often conveys a sense of graceful movement or natural drooping due to gravity and weight. In botanical contexts, pendulous describes plants or plant parts that hang downward, like the drooping branches of a weeping willow or clusters of grapes on a vine. The word can also describe physical features or body parts that hang loosely, often used in medical or anatomical descriptions. Pendulous movements are characterized by their rhythmic, swaying quality, following the natural laws of physics that govern suspended objects. The term suggests both flexibility and weight, implying that the object has enough substance to create a noticeable hanging effect while maintaining enough flexibility to move freely. This quality is often found aesthetically pleasing in nature and art, representing grace, fluidity, and natural elegance.',
                'pronunciation': '/ˈpɛndjʊləs/',
                'example_sentence': 'The _____ branches of the ancient oak swayed gently in the evening breeze.',
                'etymology': 'From Latin "pendulus," meaning "hanging down," derived from "pendere" (to hang). Related to "pendulum" and "pendant."',
                'memory_tip': 'Think of a "pendulum" - both words share the same root meaning "to hang." Pendulous things hang and swing like a pendulum clock.'
            },
            'penelope': {
                'definition': 'Penelope is a name of Greek origin, most famously associated with the faithful wife of Odysseus in Homer\'s epic poem "The Odyssey." In classical mythology, Penelope represents the archetypal faithful spouse who waits patiently for her husband\'s return while cleverly outwitting numerous suitors who sought to claim her hand and Odysseus\'s throne. Her most famous act of cunning involved weaving a funeral shroud by day and secretly unraveling it by night, promising to choose a suitor only when the work was complete. This strategy allowed her to delay remarriage for years until Odysseus finally returned home. The name Penelope has come to symbolize loyalty, intelligence, patience, and resourcefulness in the face of adversity. In literature and popular culture, references to Penelope often invoke themes of marital fidelity, clever problem-solving, and the strength required to maintain hope during prolonged separation or hardship. The character has inspired countless adaptations and reinterpretations in modern literature, theater, and film. As a given name, Penelope has experienced renewed popularity in recent decades, often chosen by parents who appreciate its classical heritage and the strong, intelligent character it represents in Western literature.',
                'pronunciation': '/pəˈnɛləpi/',
                'example_sentence': 'Like the mythical _____, she waited faithfully for her beloved\'s return from war.',
                'etymology': 'From Greek "Penelopeia," possibly meaning "weaver" or related to "penelops" (a type of duck). The exact etymology is debated among scholars.',
                'memory_tip': 'Remember "PEN-elope" - she used her pen (well, needle) to weave and unweave, showing her cleverness. Think of "elope" as staying, not eloping away.'
            },
            'penguin': {
                'definition': 'A penguin is a flightless aquatic bird found primarily in the Southern Hemisphere, characterized by its distinctive black and white plumage, upright posture, and exceptional swimming abilities. These remarkable birds have evolved specialized adaptations for life in marine environments, including streamlined bodies, flipper-like wings, and webbed feet that make them incredibly efficient underwater hunters. Penguins are highly social creatures that often form large colonies for breeding, feeding, and protection from predators. Their diet consists primarily of fish, krill, squid, and other marine organisms, which they catch during extended diving expeditions that can last several minutes and reach considerable depths. Different penguin species vary dramatically in size, from the tiny blue penguin standing about 16 inches tall to the majestic emperor penguin that can reach heights of over 3 feet. These birds have developed remarkable strategies for surviving in some of Earth\'s harshest environments, including elaborate courtship rituals, cooperative parenting behaviors, and sophisticated thermoregulation techniques. Penguins play crucial roles in their ecosystems as both predators and prey, and their populations serve as important indicators of ocean health and climate change impacts.',
                'pronunciation': '/ˈpɛŋɡwɪn/',
                'example_sentence': 'The adorable _____ waddled across the ice before diving gracefully into the frigid Antarctic waters.',
                'etymology': 'Possibly from Welsh "pen gwyn" meaning "white head," originally applied to the great auk. The name was later transferred to the similar-looking southern hemisphere birds.',
                'memory_tip': 'Think "PEN-guin" - imagine a bird that looks like it\'s wearing a black and white pen (formal suit). They waddle like they\'re holding a pen!'
            },
            'penicillin': {
                'definition': 'Penicillin is a groundbreaking antibiotic medication derived from the Penicillium mold, discovered by Alexander Fleming in 1928 and representing one of the most significant medical breakthroughs in human history. This powerful antimicrobial agent works by interfering with bacterial cell wall synthesis, effectively killing or inhibiting the growth of many types of bacteria responsible for serious infections. The discovery and development of penicillin revolutionized medicine by providing the first effective treatment for previously deadly bacterial diseases such as pneumonia, syphilis, gonorrhea, and streptococcal infections. During World War II, penicillin saved countless lives by treating infected wounds and preventing battlefield deaths that would have otherwise resulted from bacterial complications. The antibiotic belongs to the beta-lactam family and works by binding to proteins involved in cell wall construction, causing bacterial cells to become structurally unstable and ultimately leading to their destruction. Modern medicine has developed numerous penicillin derivatives and synthetic variants to combat different types of bacterial infections and address the growing challenge of antibiotic resistance. The development of penicillin marked the beginning of the antibiotic era and established the foundation for modern antimicrobial therapy, fundamentally changing medical practice and dramatically increasing human life expectancy.',
                'pronunciation': '/ˌpɛnɪˈsɪlɪn/',
                'example_sentence': 'The discovery of _____ in 1928 marked the beginning of the antibiotic era and saved millions of lives.',
                'etymology': 'From "Penicillium," the genus name of the mold from which it was derived, plus the suffix "-in." Penicillium comes from Latin "penicillus" (little brush), referring to the mold\'s brush-like structure.',
                'memory_tip': 'Think "PEN-icillin" - imagine a pen that writes prescriptions to kill germs. The "pen" connection helps remember this life-saving medicine.'
            },
            'peninsula': {
                'definition': 'A peninsula is a landform that extends into a body of water and is surrounded by water on three sides while remaining connected to the mainland by a narrow strip of land called an isthmus. This geographical feature creates a distinctive finger-like or arm-like projection into oceans, seas, lakes, or other large bodies of water. Peninsulas can vary dramatically in size, from small rocky outcroppings extending into a bay to massive landmasses like the Iberian Peninsula or the Arabian Peninsula that contain entire countries and diverse ecosystems. The formation of peninsulas typically results from various geological processes including tectonic activity, erosion, sediment deposition, and changes in sea level over geological time scales. These landforms often develop unique characteristics due to their position between land and water, including distinctive climates, specialized plant and animal communities, and strategic importance for human settlements. Peninsulas frequently serve as natural harbors and strategic military positions due to their defensive advantages and access to maritime trade routes. The isolation created by water barriers often leads to the development of distinct cultural and biological characteristics. Many of the world\'s most important cities and civilizations have developed on peninsulas, taking advantage of their access to both terrestrial and maritime resources.',
                'pronunciation': '/pəˈnɪnsjʊlə/',
                'example_sentence': 'The rocky _____ jutted dramatically into the azure Mediterranean Sea, creating a natural harbor for ancient mariners.',
                'etymology': 'From Latin "paeninsula," from "paene" (almost) + "insula" (island), literally meaning "almost an island."',
                'memory_tip': 'Think "pen-IN-sula" - it\'s like a pen drawing a line INTO the water. Almost an island (insula) but still connected to land.'
            },
            'peninsular': {
                'definition': 'Peninsular is an adjective describing anything relating to, resembling, or characteristic of a peninsula. This term is used to describe the geographical, cultural, political, or environmental features associated with landforms that extend into bodies of water while remaining connected to the mainland. Peninsular regions often develop distinct characteristics due to their unique position between terrestrial and maritime environments, including specific climate patterns, biodiversity, economic activities, and cultural traditions. The word frequently appears in geographical and historical contexts, such as the Peninsular War (1807-1814) fought in the Iberian Peninsula, or when describing peninsular peoples, economies, or ecosystems. Peninsular characteristics might include maritime-influenced weather patterns, economies based on fishing and trade, defensive military advantages, or the development of distinct regional cultures shaped by both continental and oceanic influences. In academic and scientific contexts, researchers study peninsular effects on evolution, climate, and human development, noting how the semi-isolated nature of these landforms creates unique conditions for biological and cultural development. The term is essential in geography, history, and environmental science when describing the special properties that arise from this particular type of landform configuration.',
                'pronunciation': '/pəˈnɪnsjʊlər/',
                'example_sentence': 'The _____ climate was moderated by ocean breezes, creating perfect conditions for the coastal vineyards.',
                'etymology': 'From "peninsula" + the adjectival suffix "-ar," meaning "relating to or characteristic of a peninsula."',
                'memory_tip': 'Remember "peninsula" + "AR" = peninsular. Think "pen-IN-sula-R" - the "R" makes it describe things RELATED to a peninsula.'
            },
            'penitentiary': {
                'definition': 'A penitentiary is a state or federal prison designed for the confinement and rehabilitation of individuals convicted of serious crimes, particularly felonies that warrant long-term incarceration. The term originates from the concept of penance and reflects the historical belief that imprisonment should provide opportunities for criminals to reflect on their actions, express remorse, and undergo moral reformation. Modern penitentiaries are complex institutions that serve multiple functions including punishment, deterrence, incapacitation of dangerous individuals, and ideally, rehabilitation and reintegration preparation. These facilities typically house inmates serving sentences of one year or longer and are distinguished from local jails that primarily hold individuals awaiting trial or serving shorter sentences. Penitentiaries operate under strict security protocols and are classified according to security levels ranging from minimum-security facilities with relatively open environments to maximum-security institutions with heavily fortified perimeters and extensive surveillance. The daily operations of a penitentiary involve numerous departments including corrections officers, medical staff, educational personnel, counselors, and administrative workers who work together to maintain safety, security, and programming. Modern penitentiary systems increasingly emphasize evidence-based rehabilitation programs, vocational training, education, and mental health services to reduce recidivism and prepare inmates for successful reentry into society.',
                'pronunciation': '/ˌpɛnɪˈtɛnʃəri/',
                'example_sentence': 'The convicted felon was sentenced to fifteen years in the state _____ for armed robbery.',
                'etymology': 'From Medieval Latin "paenitentiarius," meaning "relating to penance," derived from "paenitentia" (penance, repentance). Originally referred to places for religious penance.',
                'memory_tip': 'Think "PENI-tent-iary" - a place where people become "penitent" (sorry) for their crimes. The "tent" reminds you it\'s where people are detained.'
            },
            'pensive': {
                'definition': 'Pensive describes a state of deep, serious thought characterized by quiet contemplation, reflection, or meditation on weighty matters. When someone is pensive, they appear absorbed in their inner thoughts, often with a somewhat melancholic or wistful quality to their demeanor. This mental state typically involves careful consideration of complex ideas, personal experiences, philosophical questions, or emotional situations that require thoughtful analysis. Pensive individuals often display physical signs of their contemplative state, such as a distant gaze, stillness, or a furrowed brow indicating concentrated mental effort. The word carries connotations of wisdom, introspection, and emotional depth, suggesting that the person is engaging with meaningful or significant concepts rather than casual daydreaming. Pensive moods frequently arise during transitional periods in life, moments of decision-making, or when processing difficult experiences or profound realizations. In literature and art, pensive characters are often portrayed as thoughtful, intelligent individuals grappling with important life questions or moral dilemmas. The term can describe both temporary states of reflection and more enduring personality traits in individuals who are naturally inclined toward deep thinking and philosophical contemplation.',
                'pronunciation': '/ˈpɛnsɪv/',
                'example_sentence': 'She sat in a _____ mood by the window, contemplating the important decision that would change her life.',
                'etymology': 'From Old French "pensif," derived from "penser" (to think), ultimately from Latin "pensare" (to weigh, consider). Related to "ponder" and "pension."',
                'memory_tip': 'Think "PEN-sive" - imagine someone holding a pen, pausing thoughtfully before writing something important. Pensive people "pen" their thoughts carefully.'
            },
            'pentameter': {
                'definition': 'Pentameter is a fundamental metrical pattern in poetry consisting of five metrical feet per line, most commonly encountered in the form of iambic pentameter, which has been the backbone of English verse for centuries. This rhythmic structure creates a natural flow that closely resembles the patterns of spoken English, making it particularly effective for dramatic dialogue and narrative poetry. Each foot in pentameter typically contains two syllables, resulting in lines of approximately ten syllables, though variations and substitutions are common to avoid monotony and create emphasis. Iambic pentameter, where each foot follows an unstressed-stressed pattern (da-DUM), was masterfully employed by William Shakespeare in his plays and sonnets, Geoffrey Chaucer in "The Canterbury Tales," and John Milton in "Paradise Lost." The meter\'s flexibility allows poets to create subtle variations through techniques like caesura (pauses), enjambment (line overflow), and metrical substitution while maintaining the underlying rhythmic framework. Understanding pentameter is essential for analyzing classical English poetry and appreciating how poets manipulate rhythm and meter to enhance meaning, create emotional effects, and maintain reader engagement. The form has proven so enduring because it balances structure with flexibility, providing a stable foundation while allowing for creative expression and natural speech patterns.',
                'pronunciation': '/pɛnˈtæmɪtər/',
                'example_sentence': 'Shakespeare\'s sonnets are written in iambic _____, creating the characteristic rhythm that has influenced centuries of English poetry.',
                'etymology': 'From Greek "pentametros," from "penta" (five) + "metron" (measure), literally meaning "five measures" or "five feet."',
                'memory_tip': 'Break it down: "PENTA-meter" - "penta" means five (like pentagon), so pentameter has five metrical feet per line.'
            },
            'penultimate': {
                'definition': 'Penultimate refers to the second-to-last item in a sequence, series, or hierarchy, representing the position immediately before the final or ultimate element. This term is frequently used in academic, literary, and formal contexts to precisely indicate something\'s position near the end of a progression without being the absolute conclusion. In linguistics, the penultimate syllable of a word is crucial for understanding stress patterns and pronunciation rules in many languages. The concept appears across various disciplines: in music, the penultimate movement of a symphony; in sports, the penultimate round of a tournament; in literature, the penultimate chapter of a novel that often contains crucial climactic elements. Understanding the penultimate position is important because it often carries special significance, serving as a bridge between the main content and the final resolution. In many narrative structures, the penultimate section contains the climax or most intense dramatic moment, while the ultimate section provides resolution and closure. The term demonstrates the precision possible in English vocabulary, allowing speakers to distinguish between "last," "second-to-last," and "third-to-last" (antepenultimate) with specific terminology. This linguistic precision is particularly valuable in academic writing, legal documents, and formal analysis where exact positioning matters.',
                'pronunciation': '/pɪˈnʌltɪmət/',
                'example_sentence': 'The _____ chapter of the novel contained the most shocking revelation, leaving readers eager for the final resolution.',
                'etymology': 'From Latin "paenultimus," from "paene" (almost) + "ultimus" (last), literally meaning "almost last."',
                'memory_tip': 'Think "pen-ULTIMATE" - it\'s almost (pen-) the ultimate (last) but not quite. Remember "PEN" as "almost" - like peninsula is "almost" an island.'
            },
            'penurious': {
                'definition': 'Penurious describes a state of extreme poverty, destitution, or reluctance to spend money, often characterized by both financial hardship and an exceptionally frugal or miserly attitude toward expenditures. This adjective can describe either genuinely impoverished conditions where resources are scarce or a personality trait involving excessive stinginess and unwillingness to spend even when resources are available. When applied to circumstances, penurious indicates severe financial constraints that force individuals or groups to live with minimal resources, often struggling to meet basic needs for food, shelter, and clothing. When describing personal character, the term suggests an extreme and often unreasonable reluctance to part with money, even for necessary expenses or charitable causes. Penurious individuals may deprive themselves and others of reasonable comforts or necessities due to an obsessive desire to hoard wealth or an irrational fear of financial insecurity. The word carries negative connotations, implying either pitiable circumstances of genuine hardship or unseemly character traits involving selfishness and lack of generosity. In literature, penurious characters often serve as examples of how poverty can corrupt the spirit or how excessive frugality can lead to moral bankruptcy and social isolation.',
                'pronunciation': '/pɪˈnjʊriəs/',
                'example_sentence': 'Despite his wealthy family background, his _____ habits meant he never contributed to charity or helped those in need.',
                'etymology': 'From Latin "penuriosus," from "penuria" (want, need, poverty). Related to "penury," meaning extreme poverty.',
                'memory_tip': 'Think "pen-URious" - so poor they can\'t afford a pen, or so stingy they won\'t buy one. Connect to "penury" (poverty).'
            },
            'peony': {
                'definition': 'A peony is a showy, fragrant flowering plant belonging to the genus Paeonia, prized for its large, often ruffled blooms that appear in late spring and early summer. These perennial herbaceous plants or shrubs produce some of the most spectacular flowers in the garden, with blooms that can range from simple single forms to elaborate double varieties resembling layers of silk or crepe paper. Peonies come in various colors including white, pink, red, coral, and yellow, with many cultivars featuring multiple colors or subtle gradations within individual flowers. The plants are known for their longevity and can live for decades, even centuries, becoming more beautiful and productive with age when properly established. Peony flowers are highly valued in floral arrangements and wedding bouquets for their dramatic appearance, sweet fragrance, and symbolic associations with romance, honor, and prosperity. In many cultures, particularly in Asia, peonies hold deep cultural significance and are often called the "king of flowers" or symbols of wealth and good fortune. The plants require a period of winter cold to bloom properly and prefer well-drained soil and full sun to partial shade. Growing peonies requires patience, as newly planted specimens may take several years to reach their full blooming potential.',
                'pronunciation': '/ˈpiəni/',
                'example_sentence': 'The garden\'s centerpiece was a magnificent _____ bush whose enormous pink blooms perfumed the entire yard each spring.',
                'etymology': 'From Latin "paeonia," from Greek "paionia," named after Paeon, the physician of the gods in Greek mythology who used the plant medicinally.',
                'memory_tip': 'Think "PEE-ony" - imagine the flower is so beautiful it makes you want to pee yourself with excitement! The "pee" sound helps remember the pronunciation.'
            },
            'people': {
                'definition': 'People refers to human beings collectively, emphasizing their social nature, shared humanity, and existence as members of communities, societies, or distinct cultural groups. This fundamental term encompasses all individuals regardless of age, gender, ethnicity, nationality, or social status, highlighting the common bonds that unite humanity while acknowledging the diversity that exists within human populations. In democratic contexts, "the people" represents the collective citizenry who hold ultimate political power and sovereignty, as expressed in phrases like "government of the people, by the people, for the people." The word can refer to specific populations sharing common characteristics such as ethnicity, culture, language, or geographical location, as in "the Cherokee people" or "the people of France." People are distinguished from other living beings by their complex language abilities, advanced reasoning capacity, sophisticated social structures, and cultural achievements including art, literature, science, and technology. The study of people and their behaviors, relationships, and societies forms the basis of numerous academic disciplines including anthropology, sociology, psychology, and political science. Understanding people involves recognizing both individual uniqueness and collective patterns of behavior, beliefs, and social organization that define human civilization.',
                'pronunciation': '/ˈpipəl/',
                'example_sentence': 'The diverse _____ of the neighborhood came together to celebrate their shared community spirit.',
                'etymology': 'From Old French "poeple," from Latin "populus" (people, nation). Related to "popular," "population," and "public."',
                'memory_tip': 'Think "PEE-ple" - everyone needs to pee, so this reminds us that all people share basic human needs and experiences.'
            },
            'pepita': {
                'definition': 'Pepita refers to the edible seed found inside pumpkin shells, commonly known as a pumpkin seed, which has been consumed as food for thousands of years across various cultures, particularly in Mexico and Central America. These nutritious seeds are typically flat, oval-shaped, and have a distinctive greenish color when the outer white hull is removed, revealing the tender inner kernel. Pepitas are celebrated for their exceptional nutritional value, containing high levels of protein, healthy fats, fiber, and essential minerals including magnesium, zinc, iron, and potassium. In Mexican cuisine, pepitas play a crucial role in traditional dishes such as mole verde, where they are ground into a paste that thickens and enriches the complex sauce. The seeds can be consumed raw or roasted, often seasoned with salt, spices, or chile powder to create a popular snack food. Beyond their culinary applications, pepitas have been valued in traditional medicine for their potential health benefits, including supporting prostate health, heart function, and immune system strength. Commercial production of pepitas has expanded globally as awareness of their nutritional benefits has grown, making them increasingly available in health food stores and mainstream grocery markets as both snacks and ingredients for cooking and baking.',
                'pronunciation': '/pəˈpitə/',
                'example_sentence': 'She sprinkled roasted _____ on top of her salad for extra crunch and nutritional value.',
                'etymology': 'From Spanish "pepita," literally meaning "little seed," diminutive of "pepa" (seed, pit). Specifically refers to pumpkin seeds in Mexican cuisine.',
                'memory_tip': 'Think "pep-ITA" - these little seeds give you "pep" (energy) and "ita" is a Spanish diminutive, like "little seed that gives you pep."'
            },
            'peplos': {
                'definition': 'A peplos is a type of ancient Greek garment worn by women, consisting of a large rectangular piece of cloth that was draped over the body and fastened at the shoulders with pins or brooches called fibulae. This classical garment was typically made from wool and represented one of the primary forms of female dress in ancient Greece, particularly during the Archaic and Classical periods. The peplos was worn over a chiton (undergarment) and was characterized by its elegant simplicity and the graceful way it draped over the feminine form. The garment was often richly decorated with woven or embroidered patterns, and the quality of the fabric and ornamentation indicated the wearer\'s social status and wealth. In religious contexts, elaborately decorated peploi were created as offerings to goddesses, particularly Athena, during important festivals like the Panathenaea in Athens. The peplos appears frequently in ancient Greek art, sculpture, and pottery, providing valuable insights into ancient fashion, textile production, and social customs. Modern fashion designers and costume historians continue to study the peplos for its timeless elegance and the sophisticated understanding of draping and proportion demonstrated by ancient Greek craftspeople. The garment represents not just clothing but also cultural identity, religious devotion, and artistic achievement in ancient Greek civilization.',
                'pronunciation': '/ˈpɛpləs/',
                'example_sentence': 'The marble statue depicted the goddess Athena wearing a beautifully carved _____ that seemed to flow like real fabric.',
                'etymology': 'From Greek "peplos," meaning a type of ancient Greek garment. The exact etymological origin within Greek is uncertain.',
                'memory_tip': 'Think "PEP-los" - imagine ancient Greek women had "pep" (energy) while wearing this loose ("los" sounds like loose) garment.'
            },
            'peplus': {
                'definition': 'Peplus is an alternative spelling and form of peplos, referring to the same type of ancient Greek women\'s garment characterized by its rectangular shape and elegant draping style. This classical vestment played a crucial role in ancient Greek society, serving not only as everyday attire but also as a symbol of cultural identity and religious devotion. The peplus was constructed from a single piece of fabric, typically measuring approximately six feet by nine feet, which was folded and arranged to create a sophisticated silhouette that emphasized the natural grace of the female form. The garment\'s versatility allowed for various styling options depending on the occasion, social status, and personal preference of the wearer. During religious festivals, specially woven pepluses featuring intricate mythological scenes or geometric patterns were created as sacred offerings to deities. The construction and wearing of the peplus required considerable skill and cultural knowledge, as proper draping was considered an art form that reflected both personal refinement and adherence to social conventions. Archaeological evidence from ancient Greek sites has provided valuable information about the materials, techniques, and cultural significance of these garments. The peplus continues to influence modern fashion design and serves as an important subject of study for historians, archaeologists, and textile specialists interested in ancient Greek culture and daily life.',
                'pronunciation': '/ˈpɛpləs/',
                'example_sentence': 'The archaeological exhibition featured a reconstructed _____ showing how ancient Greek women achieved such elegant silhouettes.',
                'etymology': 'From Greek "peplos," an ancient Greek garment. Peplus is a variant spelling of the same word.',
                'memory_tip': 'Remember "peplus" is just another spelling of "peplos" - both refer to the same ancient Greek dress. Think "PEP-lus" - plus more pep in ancient fashion!'
            },
            'peppermint': {
                'definition': 'Peppermint is a hybrid aromatic herb (Mentha × piperita) known for its distinctive cool, refreshing flavor and its wide range of culinary, medicinal, and commercial applications. This perennial plant is a cross between water mint and spearmint, producing the characteristic intense minty taste that contains high levels of menthol, which creates the cooling sensation associated with peppermint products. The herb grows readily in moist soil conditions and is cultivated worldwide for its essential oils, which are extracted and used in everything from toothpaste and chewing gum to pharmaceuticals and aromatherapy products. Peppermint has been valued for centuries for its digestive properties and is commonly used to soothe stomach upset, reduce nausea, and relieve symptoms of irritable bowel syndrome. In culinary applications, peppermint adds brightness to both sweet and savory dishes, appearing in everything from chocolates and candies to Middle Eastern cuisine and herbal teas. The plant\'s essential oils possess antimicrobial and antispasmodic properties, making peppermint a popular ingredient in natural remedies and traditional medicine. Commercial peppermint production is significant in regions like the Pacific Northwest of the United States, where the climate and soil conditions are ideal for maximizing the concentration of beneficial compounds in the harvested leaves.',
                'pronunciation': '/ˈpɛpərˌmɪnt/',
                'example_sentence': 'The refreshing _____ tea helped settle her stomach after the heavy meal.',
                'etymology': 'From "pepper" + "mint," referring to the hot, peppery taste combined with the mint family characteristics. "Pepper" from Latin "piper," "mint" from Latin "mentha."',
                'memory_tip': 'Think "PEPPER-mint" - it tastes like pepper (hot/spicy) mixed with mint (cool). The contrast helps remember this cooling yet intense herb.'
            },
            'pepysian': {
                'definition': 'Pepysian refers to anything relating to or characteristic of Samuel Pepys (1633-1703), the famous English diarist whose detailed personal journals provide an invaluable historical record of 17th-century London life, including major events like the Great Fire of London and the Great Plague. Pepys\' diary, written in a complex shorthand cipher, offers unprecedented insights into the daily life, politics, social customs, and personal relationships of Restoration England. The term "Pepysian" might describe the style of detailed, personal record-keeping that Pepys exemplified, characterized by candid observations about both significant historical events and intimate personal experiences. Pepysian writing often includes frank discussions of human nature, social interactions, political intrigue, and personal desires, presented with remarkable honesty and attention to detail. The Pepys Library at Magdalene College, Cambridge, houses his extensive collection of books, manuscripts, and papers, representing one of the most important private libraries of the 17th century. Scholars use "Pepysian" to describe approaches to historical documentation that emphasize personal perspective, daily life details, and the intersection of private experience with public events. The diary\'s unique blend of historical significance and personal revelation has made Pepys one of the most quoted and studied figures from his era.',
                'pronunciation': '/ˈpipsiən/',
                'example_sentence': 'The historian\'s _____ approach to documenting daily life provided rich insights into ordinary people\'s experiences during the war.',
                'etymology': 'From Samuel Pepys (1633-1703), English diarist, + the suffix "-ian" meaning "relating to or characteristic of."',
                'memory_tip': 'Think "PEPYS-ian" - relating to Samuel Pepys, the famous diary writer. Remember "PEEPS" (people) + "ian" = documenting what people do daily.'
            },
            'peradventure': {
                'definition': 'Peradventure is an archaic term meaning "perhaps," "possibly," or "by chance," often used in formal, legal, or literary contexts to express uncertainty or hypothetical possibility. This somewhat antiquated word appears frequently in older English literature, particularly in religious texts, legal documents, and classical poetry where it adds a formal or ceremonial tone to the expression of doubt or speculation. The term carries connotations of careful consideration and measured uncertainty rather than casual guessing, suggesting that the speaker is thoughtfully contemplating various possibilities. In biblical and religious contexts, peradventure often appears when discussing divine will, moral questions, or spiritual possibilities that lie beyond human certainty. Legal documents historically used peradventure to indicate conditional clauses or situations that might arise under specific circumstances. While rarely used in contemporary speech, the word persists in formal writing, historical reenactments, and literary works that seek to evoke older linguistic styles. Understanding peradventure is valuable for reading classical literature, historical documents, and religious texts where its formal tone and specific meaning contribute to the overall style and meaning. The word represents the rich vocabulary of earlier English that offered nuanced ways to express different degrees of uncertainty and possibility.',
                'pronunciation': '/ˌpɛrədˈvɛntʃər/',
                'example_sentence': 'The ancient contract stated that _____ the debtor should fail to pay, his lands would be forfeit to the crown.',
                'etymology': 'From Old French "par aventure," literally meaning "by chance" or "by adventure." Combines "per" (by) + "adventure" (chance, fortune).',
                'memory_tip': 'Think "per-ADVENTURE" - by chance or adventure, something might happen. It\'s an old-fashioned way to say "perhaps."'
            },
            'percent': {
                'definition': 'Percent is a mathematical term meaning "per hundred" or "out of every hundred," used to express proportions, rates, and fractions as parts of a whole divided into one hundred equal units. This fundamental concept allows for easy comparison and understanding of relative quantities across different contexts and scales. Percentages are ubiquitous in modern life, appearing in contexts ranging from academic grades and statistical data to financial calculations, scientific measurements, and everyday shopping experiences. The percent symbol (%) serves as a universal notation that immediately communicates the proportional relationship being described. Understanding percentages is essential for financial literacy, enabling people to comprehend interest rates, tax calculations, discounts, and investment returns. In academic and professional settings, percentages provide standardized ways to report performance, success rates, demographic information, and research findings. The decimal relationship between percentages and other numerical expressions makes them valuable tools for mathematical calculations and data analysis. Converting between percentages, decimals, and fractions is a fundamental skill taught in mathematics education. Percentages also play crucial roles in probability, statistics, and data visualization, helping to make complex numerical relationships accessible to general audiences through intuitive fractional representations.',
                'pronunciation': '/pərˈsɛnt/',
                'example_sentence': 'The sale offered a twenty-five _____ discount on all winter clothing.',
                'etymology': 'From Latin "per centum," literally meaning "by the hundred" or "for each hundred."',
                'memory_tip': 'Think "PER-cent" - "per" means "for each" and "cent" means "hundred" (like century). So percent = for each hundred.'
            },
            'perceptible': {
                'definition': 'Perceptible describes something that can be detected, noticed, or perceived by the senses or the mind, though it may be subtle or require careful attention to observe. This adjective indicates that while something exists and can be sensed, it might not be immediately obvious or overwhelming in its presence. Perceptible changes, differences, or phenomena occupy the threshold between the undetectable and the clearly apparent, often requiring focused observation or sensitive instruments to identify. In scientific contexts, perceptible measurements might represent the smallest changes that human senses or equipment can reliably detect, such as barely perceptible temperature variations or sound frequencies at the edge of human hearing range. The term frequently appears in discussions of gradual processes where changes accumulate slowly over time until they become perceptible to observers. In psychology and neuroscience, perceptible stimuli are those that cross the threshold of conscious awareness, distinguishing them from subliminal inputs that affect behavior without conscious recognition. The concept of perceptibility is crucial in fields like medicine, where doctors must detect perceptible symptoms that might indicate underlying conditions, and in environmental science, where perceptible changes in ecosystems might signal broader environmental shifts. Understanding what makes something perceptible versus imperceptible helps in designing effective communication, creating noticeable improvements, and recognizing significant changes in various contexts.',
                'pronunciation': '/pərˈsɛptəbəl/',
                'example_sentence': 'There was a barely _____ tremor in his voice when he spoke about the accident.',
                'etymology': 'From Latin "perceptibilis," from "percipere" (to perceive, take in) + "-ibilis" (able to be). Related to "perceive" and "perception."',
                'memory_tip': 'Think "PERCEPT-ible" - able to be perceived. Break down: "percept" (what you perceive) + "ible" (able to be).'
            },
            'perciatelli': {
                'definition': 'Perciatelli is a type of thick, long Italian pasta similar to spaghetti but considerably wider in diameter, creating a more substantial texture and greater sauce-holding capacity. This traditional pasta shape, also known as bucatini in some regions, features a distinctive thick, rod-like form that provides a satisfying bite and works particularly well with robust sauces that can coat its surface effectively. The pasta originates from central and southern Italy, where it has been a staple in regional cuisines for centuries, often paired with rich tomato-based sauces, meat ragùs, or traditional preparations featuring ingredients like pancetta, pecorino cheese, and black pepper. Perciatelli\'s thickness makes it ideal for hearty, rustic dishes that require pasta substantial enough to complement bold flavors and chunky ingredients. The cooking time for perciatelli is typically longer than thinner pasta varieties due to its diameter, requiring careful attention to achieve the proper al dente texture. In Italian culinary tradition, the choice of pasta shape is considered crucial to the success of a dish, and perciatelli\'s particular characteristics make it suitable for specific sauce pairings and preparation methods. The pasta represents the diversity and regional specificity of Italian pasta-making traditions, where different shapes evolved to complement local ingredients and cooking styles.',
                'pronunciation': '/ˌpɛrtʃəˈtɛli/',
                'example_sentence': 'The chef recommended the _____ with wild boar ragù, explaining that the thick pasta would perfectly complement the rich sauce.',
                'etymology': 'From Italian "perciatelli," a regional pasta name from central Italy. The exact etymology within Italian is uncertain but relates to traditional pasta terminology.',
                'memory_tip': 'Think "per-CIA-telli" - imagine the CIA needs thick, substantial pasta for their secret Italian missions. The thickness helps remember it\'s thicker than spaghetti.'
            },
            'perdition': {
                'definition': 'Perdition refers to a state of eternal damnation or complete spiritual ruin, typically associated with the ultimate punishment for sin in various religious traditions, particularly Christianity. This concept represents the absolute loss of salvation and the final separation from divine grace, often visualized as an eternity spent in hell or a state of spiritual torment. In theological discourse, perdition is contrasted with salvation, representing the two possible eternal destinies for human souls according to many religious beliefs. The term extends beyond purely religious contexts to describe any state of utter ruin, complete destruction, or irreversible loss, whether spiritual, moral, or material. Literary works often employ perdition as a powerful metaphor for the consequences of moral corruption, evil choices, or the abandonment of virtue and righteousness. The concept carries profound emotional and psychological weight, representing humanity\'s deepest fears about judgment, accountability, and the possibility of irreversible consequences for one\'s actions. In classical literature and poetry, perdition serves as a warning about the potential results of vice, hubris, or defiance of moral order. The word\'s gravity and finality make it particularly effective in contexts where the speaker wants to emphasize the severity of potential consequences or the completeness of destruction or ruin.',
                'pronunciation': '/pərˈdɪʃən/',
                'example_sentence': 'The preacher warned that a life of sin would lead inevitably to eternal _____.',
                'etymology': 'From Old French "perdicion," from Latin "perditio" (destruction, ruin), from "perdere" (to lose, destroy). Related to "perdition" and "perditious."',
                'memory_tip': 'Think "per-DITION" - "per" (completely) + "dition" (sounds like "addition") - being completely lost/damned, the opposite of salvation being added to your soul.'
            },
            'perdue': {
                'definition': 'Perdue is an adjective meaning hidden, concealed, or out of sight, often used in military contexts to describe soldiers positioned in concealed or advanced positions for reconnaissance or surprise attacks. The term can also describe anything that is lost, missing, or deliberately kept from view. In historical military terminology, a "perdue" referred to a sentinel or soldier placed in an exposed or dangerous position, often as part of an advance guard or reconnaissance mission. The word carries connotations of risk, stealth, and strategic positioning, suggesting both the hidden nature of the position and the perilous circumstances faced by those in such roles. In literary contexts, perdue might describe characters who are hiding, lost, or separated from their main group, often in situations involving danger or uncertainty. The term can also apply to things that have been mislaid, concealed, or removed from normal visibility. Modern usage sometimes extends the meaning to describe anything that has been overlooked, forgotten, or relegated to obscurity. The word\'s military origins give it a sense of purpose and strategy rather than mere accidental concealment, implying deliberate hiding for tactical advantage or protective purposes.',
                'pronunciation': '/pərˈdu/',
                'example_sentence': 'The scout remained _____ in the forest undergrowth, watching for enemy movement.',
                'etymology': 'From French "perdu," meaning "lost" or "hidden," past participle of "perdre" (to lose). Ultimately from Latin "perdere" (to lose, destroy).',
                'memory_tip': 'Think "per-DUE" - someone who is "overdue" to be found because they\'re well hidden. Or "PURR-due" like a cat hiding and purring quietly.'
            },
            'peregrination': {
                'definition': 'Peregrination refers to a journey or voyage, particularly one that is lengthy, involves traveling through foreign lands, or has elements of pilgrimage or spiritual quest. This formal term suggests more than simple travel, implying a journey with purpose, significance, or transformative potential. Historically, peregrinations were often undertaken for religious reasons, such as pilgrimages to holy sites, but the term can also describe scholarly journeys, diplomatic missions, or exploratory expeditions that involve extended travel through unfamiliar territories. The word carries connotations of adventure, discovery, and personal growth through exposure to new cultures, landscapes, and experiences. In literary contexts, peregrinations often serve as frameworks for character development, allowing protagonists to encounter challenges, gain wisdom, and undergo transformation through their travels. The term distinguishes itself from casual tourism or routine travel by emphasizing the serious, purposeful nature of the journey and its potential for meaningful impact on the traveler. Academic and intellectual peregrinations might involve visiting multiple institutions, libraries, or research sites to gather knowledge and insights. The concept embodies the idea that significant journeys can be both external adventures through physical space and internal journeys toward greater understanding, wisdom, or spiritual enlightenment.',
                'pronunciation': '/ˌpɛrɪɡrɪˈneɪʃən/',
                'example_sentence': 'His scholarly _____ through European universities provided the research foundation for his groundbreaking dissertation.',
                'etymology': 'From Latin "peregrinatio," from "peregrinari" (to travel abroad), from "peregrinus" (foreigner, traveler). Related to "pilgrim" and "peregrine."',
                'memory_tip': 'Think "PERE-grin-ATION" - like "peregrine" falcon that travels/migrates long distances. Both words share the root meaning "foreign travel."'
            },
            'peremptory': {
                'definition': 'Peremptory describes an attitude, command, or action that is decisive, final, and admits no contradiction or refusal, often delivered with an air of absolute authority that brooks no discussion or delay. This adjective characterizes behavior that is imperious, domineering, and uncompromising, typically employed by those in positions of power who expect immediate and unquestioning compliance. Peremptory commands are delivered with the expectation that they will be obeyed without question, debate, or hesitation. In legal contexts, peremptory challenges allow attorneys to reject potential jurors without providing specific reasons, while peremptory deadlines are absolute and cannot be extended. The term often carries negative connotations, suggesting arrogance, high-handedness, or an unreasonable exercise of authority that fails to consider others\' perspectives or circumstances. Peremptory behavior can be particularly problematic in collaborative environments where discussion, negotiation, and mutual respect are valued. However, in emergency situations or contexts requiring immediate action, peremptory leadership might be necessary and appropriate. The word can also describe legal documents, orders, or requirements that are absolute and must be followed without exception. Understanding when peremptory behavior is justified versus when it represents abuse of power is important for effective leadership and interpersonal relationships.',
                'pronunciation': '/pəˈrɛmptəri/',
                'example_sentence': 'His _____ dismissal of all suggestions made the staff reluctant to offer any creative input.',
                'etymology': 'From Latin "peremptorius," from "perimere" (to take away entirely, destroy), from "per-" (thoroughly) + "emere" (to take, buy).',
                'memory_tip': 'Think "per-EMPTY-ory" - when someone is peremptory, they empty out all discussion and debate, leaving no room for argument.'
            },
            'perfect': {
                'definition': 'Perfect describes something that is completely flawless, lacking any defects, errors, or shortcomings, and representing the highest possible standard of excellence in its category. This adjective indicates absolute completeness, precision, and ideal quality that cannot be improved upon or enhanced. In practical contexts, perfect often describes performance, execution, or results that meet or exceed all expectations and requirements without any identifiable weaknesses or failures. The concept of perfection varies across different domains: a perfect mathematical solution contains no errors, a perfect musical performance demonstrates flawless technique and expression, and a perfect day might involve ideal weather and circumstances. While true perfection may be theoretically unattainable in many real-world situations, the pursuit of perfection drives innovation, excellence, and continuous improvement across human endeavors. The term can describe both objective qualities measurable against established standards and subjective experiences that feel complete and satisfying to individuals. Perfect can also function as a verb meaning to make something flawless or to bring it to its highest possible state of development. Understanding the difference between perfectionism as a motivating force and perfectionism as a paralyzing obsession is important for mental health and productive achievement.',
                'pronunciation': '/ˈpɜrfɪkt/',
                'example_sentence': 'Her _____ score on the exam reflected months of dedicated study and preparation.',
                'etymology': 'From Latin "perfectus," past participle of "perficere" (to complete, finish), from "per-" (thoroughly) + "facere" (to make, do).',
                'memory_tip': 'Think "per-FECT" - "per" (completely) + "fect" (made/done). Something perfectly made or completely finished.'
            },
            'perfection': {
                'definition': 'Perfection is the state or quality of being perfect, representing the ultimate standard of excellence where no improvement is possible or necessary. This concept embodies the ideal of absolute completeness, flawlessness, and optimization in any given domain or system. Perfection serves as both a goal to strive toward and a standard against which to measure achievement, quality, and performance. In philosophical and theological contexts, perfection raises questions about whether absolute perfection is attainable by humans or whether it exists only as a divine attribute or theoretical concept. The pursuit of perfection can be a powerful motivating force that drives innovation, artistic achievement, and personal growth, pushing individuals and societies to reach their highest potential. However, perfectionism can also become problematic when it leads to paralysis, anxiety, or an inability to accept anything less than impossible standards. Different fields define perfection differently: mathematical perfection involves logical consistency and accuracy, artistic perfection might emphasize aesthetic harmony and emotional impact, while moral perfection concerns ethical behavior and character. Understanding the relationship between perfection as an inspiring ideal and perfection as a practical goal helps people maintain healthy perspectives on achievement and self-improvement.',
                'pronunciation': '/pərˈfɛkʃən/',
                'example_sentence': 'The violin maker spent decades pursuing _____ in his craft, creating instruments of extraordinary beauty and sound.',
                'etymology': 'From Latin "perfectio," from "perfectus" (perfect, complete). The suffix "-tion" creates a noun indicating the state or condition of being perfect.',
                'memory_tip': 'Think "perfect-ION" - the condition or state of being perfect. The "-ion" ending shows it\'s a noun describing the state of perfection.'
            },
            'performance': {
                'definition': 'Performance refers to the execution of an action, task, or function, encompassing both the process of carrying out activities and the quality or effectiveness with which they are accomplished. This multifaceted concept applies across numerous domains including artistic expression, athletic competition, academic achievement, professional work, and mechanical operation. In artistic contexts, performance involves the live presentation of creative works such as music, theater, dance, or other forms of entertainment that engage audiences through direct experience. Business and professional performance typically focuses on productivity, efficiency, goal achievement, and measurable outcomes that contribute to organizational success. Academic performance measures learning, comprehension, and skill development through various assessment methods. Athletic performance evaluates physical capabilities, technique, and competitive results. The quality of performance is often assessed against standards, expectations, or benchmarks that define success within specific contexts. Factors influencing performance include preparation, skill level, resources, environment, motivation, and external circumstances. Understanding performance requires analyzing both quantitative metrics and qualitative aspects such as style, creativity, and impact. Performance improvement strategies involve identifying strengths and weaknesses, developing skills, optimizing conditions, and implementing feedback mechanisms to enhance future execution.',
                'pronunciation': '/pərˈfɔrməns/',
                'example_sentence': 'Her outstanding _____ in the championship earned her recognition as the most valuable player.',
                'etymology': 'From Old French "performance," from "parfornir" (to accomplish), ultimately from Latin "per-" (through) + "fornire" (to furnish, complete).',
                'memory_tip': 'Think "per-FORM-ance" - "per" (through) + "form" (shape/create) + "ance" (action). The action of forming or creating something through execution.'
            },
            'performed': {
                'definition': 'Performed is the past tense of perform, indicating that an action, task, presentation, or function has been completed or executed in the past. This verb encompasses a wide range of activities from artistic presentations and entertainment to scientific procedures, professional duties, and mechanical operations. When someone has performed something, they have carried out the required actions, demonstrated skills, or completed responsibilities according to established expectations or requirements. In artistic contexts, performed indicates that a live presentation such as a concert, play, dance, or other creative work has been presented to an audience. Professional contexts use performed to describe the completion of job duties, projects, or assignments that meet specified standards or objectives. Scientific and medical contexts often use performed to describe procedures, experiments, or tests that have been conducted according to proper protocols and methodologies. The quality implied by "performed" can vary significantly depending on context and additional qualifiers - something can be performed excellently, adequately, or poorly. The word suggests both the completion of an action and the manner in which it was executed, though additional information is typically needed to understand the quality or effectiveness of the performance.',
                'pronunciation': '/pərˈfɔrmd/',
                'example_sentence': 'The surgeon _____ the complex operation with skill and precision, saving the patient\'s life.',
                'etymology': 'Past tense of "perform," from Old French "parfornir" (to accomplish), from Latin "per-" (through) + "fornire" (to furnish, complete).',
                'memory_tip': 'Think "per-FORMED" - something was formed or shaped completely (per-) through execution. The "-ed" ending shows it happened in the past.'
            },
            'performer': {
                'definition': 'A performer is an individual who presents artistic, athletic, or entertainment content to an audience through live demonstration of skills, talents, or creative expression. This broad category encompasses actors, musicians, dancers, comedians, athletes, public speakers, and other professionals who engage audiences through direct presentation of their abilities. Performers typically undergo extensive training, practice, and development to master their craft and create compelling experiences for their audiences. The relationship between performer and audience is central to the concept, as performance implies the presence of observers who receive, interpret, and respond to the presented material. Different types of performers require distinct skill sets: musicians must master instruments and musical interpretation, actors must develop character portrayal and emotional expression, athletes must achieve physical excellence and competitive performance, while speakers must communicate effectively and persuasively. Successful performers often possess combination of technical proficiency, creativity, charisma, and the ability to connect emotionally with their audiences. The modern entertainment industry has created numerous performance venues and platforms, from traditional theaters and concert halls to digital streaming services and social media platforms. Performance careers require resilience, continuous skill development, and adaptability to changing audience preferences and technological innovations.',
                'pronunciation': '/pərˈfɔrmər/',
                'example_sentence': 'The talented _____ captivated the audience with her powerful voice and emotional stage presence.',
                'etymology': 'From "perform" + "-er" (agent suffix), indicating one who performs. "Perform" comes from Old French "parfornir" (to accomplish).',
                'memory_tip': 'Think "perform-ER" - someone who performs. The "-er" ending indicates a person who does the action of performing.'
            },
            'performs': {
                'definition': 'Performs is the third-person singular present tense of the verb perform, indicating that someone or something currently carries out, executes, or presents actions, tasks, or functions. This verb form describes ongoing or habitual performance activities across various contexts including artistic presentation, professional duties, athletic competition, and mechanical operation. When a person performs, they demonstrate skills, present creative work, or execute responsibilities in real-time, often before an audience or according to established standards. In artistic contexts, performs indicates active engagement in live presentation such as singing, acting, dancing, or playing instruments. Professional contexts use performs to describe the ongoing execution of job responsibilities, operational procedures, or assigned tasks. Mechanical or technological systems that perform carry out their designed functions effectively and reliably. The present tense nature of performs suggests either current activity or regular, repeated execution of actions. Performance quality can vary significantly - someone might perform excellently, adequately, or poorly depending on skill level, preparation, conditions, and other factors. The verb implies both the execution of actions and the manner of execution, though additional descriptors are typically needed to convey information about quality, effectiveness, or style of performance.',
                'pronunciation': '/pərˈfɔrmz/',
                'example_sentence': 'She _____ every night at the local jazz club, building a loyal following of music lovers.',
                'etymology': 'Present tense third person singular of "perform," from Old French "parfornir" (to accomplish), from Latin "per-" (through) + "fornire" (to furnish).',
                'memory_tip': 'Think "perform-S" - the "s" ending shows someone currently performs or regularly performs actions. Like "he performs" or "she performs."'
            },
            'perfume': {
                'definition': 'Perfume is a fragrant liquid composed of aromatic compounds, essential oils, and alcohol, designed to provide a pleasant scent when applied to the skin, clothing, or living spaces. This cosmetic product represents one of humanity\'s oldest luxury goods, with a history spanning thousands of years across numerous cultures and civilizations. Modern perfumery is a sophisticated art and science that combines natural ingredients like flowers, herbs, spices, and woods with synthetic compounds to create complex, layered fragrances that evolve over time on the wearer\'s skin. Perfumes are typically categorized by concentration levels, from eau de toilette (lighter concentration) to parfum (highest concentration), affecting both intensity and longevity of the scent. The creation of perfume involves understanding fragrance notes - top notes that provide initial impression, middle notes that form the heart of the fragrance, and base notes that provide lasting foundation. Professional perfumers, known as "noses," undergo extensive training to develop their olfactory skills and artistic sensibilities. The perfume industry represents a significant global market, with luxury brands creating signature scents that become closely associated with personal identity and style. Perfume serves both aesthetic and psychological functions, enhancing confidence, expressing personality, and creating memorable sensory experiences.',
                'pronunciation': '/ˈpɜrfjum/',
                'example_sentence': 'Her signature _____ of jasmine and vanilla left a lasting impression wherever she went.',
                'etymology': 'From French "parfum," from Italian "profumo," from Latin "per fumum" (through smoke), referring to the practice of burning aromatic substances.',
                'memory_tip': 'Think "per-FUME" - "per" (through) + "fume" (smoke/scent). Originally scents were created through burning aromatic substances, sending fragrance through smoke.'
            },
            'perhaps': {
                'definition': 'Perhaps is an adverb expressing uncertainty, possibility, or speculation, indicating that something might be true, might happen, or might be the case, but without certainty or definitive knowledge. This versatile word softens statements, suggestions, and predictions by acknowledging that the speaker cannot guarantee the accuracy or occurrence of what they are discussing. Perhaps serves important social and communicative functions by allowing people to express ideas, make suggestions, or offer opinions without appearing overly confident or dogmatic. In academic and professional writing, perhaps demonstrates intellectual humility and acknowledges the limitations of current knowledge or evidence. The word can express varying degrees of probability, from slight possibility to reasonable likelihood, depending on context and tone. Perhaps often appears in hypothetical discussions, diplomatic communications, and situations where tactful uncertainty is preferable to bold assertions. In everyday conversation, perhaps serves as a polite way to decline invitations, express doubt, or suggest alternatives without being confrontational or absolute. The term\'s flexibility makes it valuable for maintaining social harmony while still expressing genuine uncertainty or qualified agreement. Understanding how to use perhaps effectively helps in developing nuanced communication skills that acknowledge complexity and uncertainty while still contributing meaningfully to discussions.',
                'pronunciation': '/pərˈhæps/',
                'example_sentence': '_____ we should consider a different approach to solving this complex problem.',
                'etymology': 'From "per" (by) + "haps" (chance, fortune), literally meaning "by chance." Related to "happen" and "mishap."',
                'memory_tip': 'Think "per-HAPS" - "per" (by) + "haps" (chance/luck). Something that might happen by chance or luck.'
            },
            'perianth': {
                'definition': 'A perianth is the collective term for the outer parts of a flower, specifically encompassing both the sepals (collectively called the calyx) and the petals (collectively called the corolla) that surround and protect the reproductive organs of flowering plants. This botanical structure serves crucial functions in plant reproduction by attracting pollinators, protecting developing reproductive parts, and sometimes participating in the pollination process itself. The perianth represents the most visually striking aspect of most flowers, displaying the colors, patterns, and shapes that make flowers attractive to both pollinators and human observers. In some flowers, the distinction between sepals and petals is clear, with sepals typically being green and protective while petals are colorful and attractive. However, in other flowers, sepals and petals may be similar in appearance, collectively forming what botanists call tepals. The perianth\'s structure, color, and arrangement are important characteristics used in plant identification and classification. Evolutionary adaptations in perianth design reflect the specific pollination strategies of different plant species, from the large, showy periants of bird-pollinated flowers to the small, inconspicuous periants of wind-pollinated species. Understanding perianth structure is fundamental to botany, horticulture, and the study of plant-pollinator relationships.',
                'pronunciation': '/ˈpɛriænθ/',
                'example_sentence': 'The orchid\'s elaborate _____ displayed intricate patterns designed to attract specific pollinating insects.',
                'etymology': 'From Greek "peri" (around) + "anthos" (flower), literally meaning "around the flower," referring to the outer floral parts that surround the reproductive organs.',
                'memory_tip': 'Think "PERI-anth" - "peri" means around (like perimeter) + "anth" (flower). The parts around the flower\'s center.'
            },
            'perilous': {
                'definition': 'Perilous describes situations, actions, or conditions that involve significant danger, risk, or the potential for serious harm, injury, or loss. This adjective characterizes circumstances where the outcome is uncertain and negative consequences are not only possible but likely if proper precautions are not taken. Perilous situations often require careful planning, special skills, or extraordinary courage to navigate successfully. The term implies a level of danger that goes beyond minor inconvenience or slight risk, suggesting that lives, safety, or important values are genuinely at stake. Historical contexts often describe perilous journeys, expeditions, or missions where explorers, soldiers, or adventurers faced unknown dangers and potentially fatal challenges. In modern usage, perilous might describe dangerous occupations, risky financial decisions, hazardous environmental conditions, or precarious political situations. The word carries emotional weight, evoking feelings of tension, concern, and the need for vigilance or protective action. Perilous circumstances often serve as catalysts for heroism, innovation, and personal growth, as individuals are forced to summon their courage and resourcefulness to overcome serious challenges. Understanding when situations are truly perilous versus merely difficult or uncomfortable helps in making appropriate decisions about risk management and safety precautions.',
                'pronunciation': '/ˈpɛrələs/',
                'example_sentence': 'The mountain climbers faced a _____ descent through loose rock and unpredictable weather.',
                'etymology': 'From Old French "perillous," from Latin "periculosus," from "periculum" (danger, risk). Related to "peril" and "imperil."',
                'memory_tip': 'Think "PERIL-ous" - full of peril (danger). If something is perilous, it\'s full of peril and dangerous.'
            },
            'period': {
                'definition': 'Period refers to a specific duration of time with defined beginning and ending points, often characterized by particular events, conditions, or developments that distinguish it from preceding and following times. This temporal concept applies across numerous contexts from geological eras spanning millions of years to brief moments lasting seconds or minutes. In grammar, a period is the punctuation mark (.) that indicates the end of a declarative sentence or abbreviation. Historical periods are defined by significant political, cultural, or technological changes that mark transitions in human civilization, such as the Renaissance period or the Industrial period. In education, class periods represent scheduled time blocks for specific subjects or activities. Biological periods might refer to reproductive cycles, developmental stages, or physiological rhythms. Astronomical periods describe the time required for celestial objects to complete specific motions or cycles. The concept of periodicity involves regular, repeating patterns that occur at predictable intervals. Understanding periods helps organize knowledge, plan activities, and comprehend patterns in natural and human systems. In medical contexts, periods often refer specifically to menstrual cycles, representing regular physiological processes. The word\'s versatility makes it essential for describing temporal boundaries and cyclical phenomena across virtually all areas of human knowledge and experience.',
                'pronunciation': '/ˈpɪriəd/',
                'example_sentence': 'The medieval _____ was characterized by feudalism, religious influence, and limited technological advancement.',
                'etymology': 'From Latin "periodus," from Greek "periodos" (circuit, period of time), from "peri" (around) + "hodos" (way, path).',
                'memory_tip': 'Think "PERI-od" - "peri" (around) + "od" (path/way). A period is like going around a complete path or cycle of time.'
            },
            'periodically': {
                'definition': 'Periodically is an adverb meaning at regular intervals, from time to time, or in a recurring pattern, though not necessarily with precise mathematical regularity. This term describes actions, events, or phenomena that occur repeatedly over time with some degree of predictable spacing between occurrences. Unlike "constantly" or "continuously," periodically indicates interruption and resumption rather than unbroken activity. The frequency implied by periodically can vary widely depending on context - it might describe daily, weekly, monthly, annual, or even multi-year cycles. In scientific contexts, periodically often refers to naturally occurring cycles such as tidal patterns, seasonal changes, or astronomical events that repeat according to physical laws. Business and organizational contexts use periodically to describe regular reviews, maintenance schedules, or recurring procedures that ensure ongoing operation and evaluation. The term suggests both regularity and flexibility, indicating that while events occur in a pattern, the exact timing might vary slightly based on circumstances or needs. Periodically allows for the description of patterns that are generally predictable but not rigid, accommodating natural variation while maintaining the essential characteristic of repetition. Understanding periodic versus random or continuous patterns is important for planning, analysis, and prediction across many fields.',
                'pronunciation': '/ˌpɪriˈɑdɪkli/',
                'example_sentence': 'The committee meets _____ to review progress and adjust strategies based on changing conditions.',
                'etymology': 'From "periodic" + "-ally" (adverb suffix). "Periodic" comes from "period" + "-ic," meaning occurring in periods.',
                'memory_tip': 'Think "period-IC-ally" - happening in periods, at regular intervals. The "IC-ally" ending makes it an adverb describing how often something happens.'
            },
            'periodontist': {
                'definition': 'A periodontist is a dental specialist who focuses specifically on the prevention, diagnosis, and treatment of diseases affecting the gums, supporting tissues, and structures that hold teeth in place, collectively known as the periodontium. These highly trained professionals complete additional years of specialized education beyond general dentistry to develop expertise in managing complex periodontal conditions. Periodontists treat various conditions including gingivitis (gum inflammation), periodontitis (serious gum disease), and other infections or disorders that can lead to tooth loss if left untreated. Their expertise extends to performing surgical procedures such as gum grafts, pocket reduction surgery, crown lengthening, and dental implant placement. Periodontists work closely with general dentists, coordinating care for patients who require specialized treatment while maintaining ongoing dental health. They employ advanced diagnostic techniques including digital imaging, bacterial testing, and genetic analysis to assess periodontal health and develop personalized treatment plans. Prevention education forms a significant part of periodontal practice, as many gum diseases are preventable through proper oral hygiene and regular professional care. The field of periodontics continues to evolve with new research linking oral health to overall systemic health, making periodontal care increasingly important for comprehensive healthcare.',
                'pronunciation': '/ˌpɛriəˈdɑntɪst/',
                'example_sentence': 'The _____ recommended a deep cleaning procedure to treat the patient\'s advanced gum disease.',
                'etymology': 'From "periodontal" (around the teeth) + "-ist" (specialist). "Periodontal" comes from Greek "peri" (around) + "odont" (tooth).',
                'memory_tip': 'Think "PERI-ODONT-ist" - "peri" (around) + "odont" (tooth) + "ist" (specialist). A specialist in problems around the teeth (gums).'
            },
            'periods': {
                'definition': 'Periods is the plural form of period, referring to multiple distinct spans of time, punctuation marks, or recurring cycles across various contexts. In temporal contexts, periods can describe different historical eras, academic terms, class sessions, or any defined time segments that serve organizational or analytical purposes. Historical periods help organize the study of human civilization into manageable segments characterized by distinct political, cultural, or technological features. In grammar and writing, periods represent the punctuation marks used to end sentences and indicate abbreviations. Educational contexts use periods to describe scheduled class times or academic terms that structure learning activities. Biological and medical contexts might refer to multiple menstrual cycles, developmental stages, or physiological rhythms. Geological periods represent vast time spans characterized by distinct environmental conditions and evolutionary developments. Scientific research often examines multiple periods to identify patterns, trends, or changes over time. Business cycles might be described in terms of periods of growth, stability, or decline. Understanding multiple periods allows for comparative analysis, pattern recognition, and the development of theories about change and continuity. The concept of periods provides essential frameworks for organizing knowledge, planning activities, and comprehending complex temporal relationships across all areas of human understanding.',
                'pronunciation': '/ˈpɪriədz/',
                'example_sentence': 'The historian studied several _____ of ancient civilization to understand the evolution of agricultural practices.',
                'etymology': 'Plural of "period," from Latin "periodus," from Greek "periodos" (circuit, period of time), from "peri" (around) + "hodos" (way).',
                'memory_tip': 'Think "period-S" - multiple periods of time. The "s" ending makes it plural, referring to several time periods or punctuation marks.'
            },
            'peripheral': {
                'definition': 'Peripheral describes something located at the edge, boundary, or outer limits of a main area, system, or focus of attention, often suggesting secondary importance or indirect relationship to central concerns. This adjective indicates position away from the center, core, or primary elements of whatever is being discussed. In anatomical contexts, peripheral refers to body parts distant from the center or trunk, such as arms, legs, and extremities served by the peripheral nervous system. Technology uses peripheral to describe devices that connect to computers but are not essential to basic operation, such as printers, keyboards, and external storage devices. In discussions and analysis, peripheral issues are those that relate to but are not central to the main topic or concern. Geographic contexts might describe peripheral regions as those located away from major population centers or economic hubs. The term can carry implications of lesser importance, though peripheral elements often play crucial supporting roles in overall system function. Business strategies might focus on core competencies while maintaining peripheral activities that support but do not define the organization\'s primary mission. Understanding the distinction between central and peripheral elements helps in prioritizing attention, resources, and effort across various contexts and decision-making situations.',
                'pronunciation': '/pəˈrɪfərəl/',
                'example_sentence': 'The _____ nervous system carries signals between the brain and the extremities of the body.',
                'etymology': 'From Greek "periphereia" (circumference), from "peri" (around) + "pherein" (to carry). Related to "periphery."',
                'memory_tip': 'Think "PERI-pheral" - "peri" means around or outer. Peripheral things are around the edges, not at the center.'
            },
            'periwinkle': {
                'definition': 'Periwinkle refers to both a small marine snail found in coastal waters and a flowering plant with distinctive blue-purple blooms, representing two entirely different organisms that share only a name and similar coloration. The marine periwinkle is a small gastropod mollusk commonly found on rocky shores, jetties, and tidal pools, where it feeds on algae and organic matter while serving as an important link in coastal food chains. These hardy creatures can survive both underwater and in air, making them well-adapted to the changing conditions of intertidal zones. The plant periwinkle (Vinca) is a popular ornamental ground cover prized for its glossy evergreen leaves and charming five-petaled flowers that bloom in various shades of blue, purple, white, and pink. Garden periwinkles are valued for their ability to thrive in challenging conditions including shade, poor soil, and drought, making them excellent choices for difficult landscaping situations. The color periwinkle, inspired by the plant\'s blue-purple flowers, represents a pale bluish-purple hue that appears frequently in interior design, fashion, and art. Both organisms contribute to their respective ecosystems - marine periwinkles as herbivores and food sources, while plant periwinkles provide ground cover and ornamental beauty. The name\'s dual usage demonstrates how common names can sometimes apply to unrelated species.',
                'pronunciation': '/ˈpɛrɪˌwɪŋkəl/',
                'example_sentence': 'The cottage garden was bordered with _____ plants that bloomed reliably in the shaded areas.',
                'etymology': 'For the plant: from Old English "perwince," from Latin "pervinca." For the snail: from "peri-" (around) + "winkle" (a spiral shell).',
                'memory_tip': 'Think "PERI-winkle" - "peri" (around) + "winkle" (wrinkle). Both the snail\'s spiral shell and the plant\'s twisted vines go around in curves.'
            },
            'permafrost': {
                'definition': 'Permafrost is permanently frozen ground that remains at or below 32°F (0°C) for at least two consecutive years, representing one of Earth\'s most significant climate-related features and a crucial component of Arctic and subarctic ecosystems. This phenomenon occurs primarily in polar regions and high mountains where cold temperatures persist year-round, creating subsurface layers of ice-cemented soil, rock, and organic matter that can extend hundreds of feet deep. Permafrost plays a vital role in global climate systems by storing vast amounts of carbon in frozen organic material that has accumulated over thousands of years. When permafrost thaws due to rising temperatures, it releases previously trapped carbon dioxide and methane into the atmosphere, contributing to accelerated climate change in a feedback loop. The stability of permafrost affects infrastructure in Arctic regions, as buildings, roads, and pipelines built on frozen ground can be damaged when thawing causes ground shifting and settling. Indigenous communities have traditionally relied on permafrost for food preservation and as a foundation for their living structures. Scientific research on permafrost provides important indicators of climate change, as these frozen layers are particularly sensitive to temperature increases. The study of permafrost involves understanding its formation, distribution, thermal properties, and ecological significance in global environmental systems.',
                'pronunciation': '/ˈpɜrməˌfrɔst/',
                'example_sentence': 'Climate change is causing rapid _____ thaw in Alaska, threatening both infrastructure and global carbon storage.',
                'etymology': 'From "permanent" + "frost," coined in the 1940s to describe permanently frozen ground layers.',
                'memory_tip': 'Think "PERMA-frost" - "perma" (permanent) + "frost." Ground that is permanently frozen, never thawing.'
            },
            'permanence': {
                'definition': 'Permanence is the quality or state of lasting indefinitely without change, decay, or disappearance, representing stability, continuity, and enduring existence across time. This concept encompasses both physical durability and conceptual persistence, applying to materials, relationships, institutions, ideas, and natural phenomena that resist alteration or destruction. In human psychology, the desire for permanence often drives decisions about career, relationships, housing, and other life choices where stability and predictability are valued. Philosophical discussions of permanence explore whether anything in the universe is truly permanent or whether all things are subject to change and eventual dissolution. Religious and spiritual traditions often seek permanence through concepts of eternal life, unchanging truths, or transcendent realities that exist beyond temporal limitations. Scientific understanding recognizes that while many things appear permanent from human perspectives, even seemingly stable phenomena like mountains, stars, and species undergo change over longer time scales. Legal systems create frameworks for establishing permanence in contracts, property rights, and institutional structures that provide social stability. The tension between permanence and change drives much of human creativity and adaptation, as people seek to preserve valuable elements while adapting to new circumstances. Understanding permanence helps in making decisions about what to preserve, what to change, and how to balance stability with necessary adaptation.',
                'pronunciation': '/ˈpɜrməməns/',
                'example_sentence': 'The ancient stone monuments were built with a sense of _____ that has allowed them to survive for millennia.',
                'etymology': 'From "permanent" + "-ence" (state or quality). "Permanent" comes from Latin "permanere" (to remain, continue).',
                'memory_tip': 'Think "PERMANENT-ence" - the state or quality of being permanent. The "-ence" ending indicates a condition or quality.'
            },
            'permutation': {
                'definition': 'A permutation is a mathematical concept referring to an arrangement of objects in a specific order where the sequence matters, representing one of the fundamental principles in combinatorics and probability theory. This concept differs from combinations, where order is irrelevant, by emphasizing that different arrangements of the same objects constitute different permutations. For example, the letters A, B, and C can be arranged in six different permutations: ABC, ACB, BAC, BCA, CAB, and CBA. Permutations are crucial in mathematics for calculating probabilities, solving optimization problems, and analyzing complex systems where order and arrangement affect outcomes. The mathematical formula for permutations helps determine how many different ways objects can be arranged, with applications ranging from simple puzzles to complex computer algorithms. In broader contexts, permutation can describe any systematic change or transformation that rearranges elements within a system while maintaining the essential components. Scientific research uses permutation testing to analyze data relationships and validate statistical hypotheses by examining all possible arrangements of experimental data. Computer science employs permutation algorithms in sorting, scheduling, and optimization problems where different arrangements must be evaluated. Understanding permutations enhances logical thinking and problem-solving skills while providing tools for analyzing complex systems where arrangement and order significantly impact outcomes.',
                'pronunciation': '/ˌpɜrmjuˈteɪʃən/',
                'example_sentence': 'The mathematician calculated that there were 720 different _____ possible when arranging six books on a shelf.',
                'etymology': 'From Latin "permutatio," from "permutare" (to change thoroughly), from "per-" (thoroughly) + "mutare" (to change).',
                'memory_tip': 'Think "per-MUTATION" - "per" (thoroughly) + "mutation" (change). A thorough change in the arrangement or order of things.'
            },
            'pernicious': {
                'definition': 'Pernicious describes something that is extremely harmful, destructive, or wicked in a subtle, gradual way that may not be immediately apparent but causes serious damage over time. This adjective characterizes influences, behaviors, conditions, or substances that work insidiously to cause harm, often while appearing harmless or even beneficial on the surface. Pernicious effects typically develop slowly and may not be recognized until significant damage has occurred, making them particularly dangerous because they operate below the threshold of immediate awareness. Medical contexts use pernicious to describe diseases or conditions that are severely harmful and potentially fatal, such as pernicious anemia, a condition where the body cannot properly absorb vitamin B12. Social and political commentators might describe pernicious ideologies, policies, or cultural trends that gradually undermine social cohesion, democratic institutions, or human welfare. The term carries moral judgment, suggesting not just harm but also a quality of evil or corruption that makes the harm particularly objectionable. Pernicious influences often work by corrupting good intentions, exploiting weaknesses, or gradually normalizing harmful behaviors until they become accepted or entrenched. Recognizing pernicious influences requires vigilance, critical thinking, and the ability to see beyond immediate appearances to understand long-term consequences and hidden motivations.',
                'pronunciation': '/pərˈnɪʃəs/',
                'example_sentence': 'The _____ effects of the propaganda campaign only became apparent after years of gradual social division.',
                'etymology': 'From Latin "perniciosus," from "pernicies" (destruction, ruin), from "per-" (through, thoroughly) + "nex" (death).',
                'memory_tip': 'Think "per-NICIOUS" - "per" (thoroughly) + "nicious" (sounds like "vicious"). Something thoroughly vicious and harmful.'
            },
            'perorate': {
                'definition': 'Perorate means to deliver a lengthy, elaborate, or grandiloquent speech, particularly one that serves as the conclusion to a formal address or argument, often characterized by rhetorical flourishes and emotional appeals. This verb describes the act of speaking in a formal, sometimes pompous manner that emphasizes style and dramatic effect over substance or brevity. The term often carries connotations of excessive verbosity or self-important oratory that may impress some listeners while annoying others who prefer more direct communication. In classical rhetoric, peroration refers specifically to the concluding section of a speech where the speaker summarizes key points and makes final emotional appeals to persuade the audience. Legal contexts might involve attorneys who perorate during closing arguments, using rhetorical devices and passionate language to influence judges or juries. Political speeches often conclude with peroration designed to inspire, motivate, or convince voters through emotional connection rather than purely logical argument. While peroration can be effective in formal settings where ceremony and tradition are valued, it may be perceived as pretentious or inappropriate in casual or business contexts where efficiency and clarity are prioritized. Understanding when to perorate versus when to communicate simply and directly is an important skill in public speaking and professional communication.',
                'pronunciation': '/ˈpɛrəˌreɪt/',
                'example_sentence': 'The senator began to _____ about patriotic duty, delivering an impassioned speech that lasted nearly an hour.',
                'etymology': 'From Latin "perorare," from "per-" (through, thoroughly) + "orare" (to speak, pray). Related to "oration" and "orator."',
                'memory_tip': 'Think "per-ORATE" - "per" (thoroughly) + "orate" (speak formally). To speak thoroughly and formally, often at great length.'
            }
        }
        
        return word_data.get(word, {
            'definition': f'A comprehensive definition for {word} would be provided here.',
            'pronunciation': f'/pronunciation for {word}/',
            'example_sentence': f'An example sentence with _____ would be provided.',
            'etymology': f'Etymology for {word} would be provided.',
            'memory_tip': f'A memory tip for {word} would be provided.'
        })
    
    def detect_combined_words(self) -> List[str]:
        """Detect words that appear to be incorrectly combined"""
        combined_words = []
        
        # Read the input file and check each word
        input_file = Path("output/batch_130_words.csv")
        if input_file.exists():
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    word = row['word'].lower()
                    
                    # Check for obviously combined words
                    if any(pattern in word for pattern in [
                        'peremptoryinfarction'  # peremptory + infarction
                    ]):
                        combined_words.append(row['word'])
        
        return combined_words
    
    def process_batch(self):
        """Process all words in batch 130"""
        input_file = Path("output/batch_130_words.csv")
        output_file = Path("output/batch_130_processed.csv")
        
        # Detect combined words first
        combined_words = self.detect_combined_words()
        if combined_words:
            logger.warning(f"Detected combined words that need manual review: {combined_words}")
        
        processed_words = []
        word_count = 0
        
        if not input_file.exists():
            logger.error(f"Input file not found: {input_file}")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                word = row['word']
                if not word:  # Skip empty rows
                    continue
                    
                word_count += 1
                
                # Skip combined words (they don't have real definitions)
                if word in combined_words:
                    logger.error(f"No data found for word: {word}")
                    continue
                
                # Get comprehensive data for the word
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Calculate difficulty scores
                difficulty_scores = self.difficulty_calc.calculate_difficulty_score(
                    word, claude_data['definition'], claude_data['etymology']
                )
                
                # Prepare the processed row
                processed_row = {
                    'word': word,
                    'years': row['years'],
                    'source_files': row['source_files'],
                    'source_difficulties': row['source_difficulties'],
                    'definition': claude_data['definition'],
                    'pronunciation': claude_data['pronunciation'],
                    'example_sentence': claude_data['example_sentence'],
                    'etymology': claude_data['etymology'],
                    'memory_tip': claude_data['memory_tip'],
                    'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                    'word_frequency_score': difficulty_scores['word_frequency_score'],
                    'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                    'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                    'difficulty': difficulty_scores['difficulty'],  # This will be None
                    'word_source': 'Claude',
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'example_sentence_source': 'Claude',
                    'etymology_source': 'Claude',
                    'memory_tip_source': 'Claude'
                }
                
                processed_words.append(processed_row)
                logger.info(f"Successfully processed word {word_count}: {word}")
        
        # Write the processed data
        if processed_words:
            fieldnames = [
                'word', 'years', 'source_files', 'source_difficulties',
                'definition', 'pronunciation', 'example_sentence', 'etymology', 'memory_tip',
                'phonetic_transparency_score', 'word_frequency_score', 
                'morphological_complexity_score', 'etymology_complexity_score', 'difficulty',
                'word_source', 'definition_source', 'pronunciation_source', 
                'example_sentence_source', 'etymology_source', 'memory_tip_source'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
            
            logger.info(f"Batch 130 processing complete. Processed {len(processed_words)}/{word_count} words.")
            logger.info(f"Output saved to: {output_file.absolute()}")
            
            if combined_words:
                logger.warning(f"Combined word errors detected: {combined_words}")
        else:
            logger.error("No words were successfully processed.")

def main():
    processor = Batch130Processor()
    processor.process_batch()

if __name__ == "__main__":
    main()