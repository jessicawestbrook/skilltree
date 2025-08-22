import csv
import re

class DifficultyCalculator:
    def calculate_difficulty_score(self, word, pronunciation, etymology):
        """Calculate 4-factor difficulty score"""
        
        # Factor 1: Phonetic Transparency (1-10)
        phonetic_score = self._calculate_phonetic_transparency(word, pronunciation)
        
        # Factor 2: Word Frequency (1-10) 
        frequency_score = self._calculate_word_frequency(word)
        
        # Factor 3: Morphological Complexity (1-10)
        morphological_score = self._calculate_morphological_complexity(word)
        
        # Factor 4: Etymology Complexity (1-10)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        # Total score (4-40)
        total_score = phonetic_score + frequency_score + morphological_score + etymology_score
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score,
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'total_difficulty_score': total_score
        }
    
    def _calculate_phonetic_transparency(self, word, pronunciation):
        """Score 1-10: How well spelling matches pronunciation"""
        if not pronunciation:
            return 5
        
        # Count irregular patterns
        irregular_patterns = 0
        
        # Silent letters and irregular patterns
        if re.search(r'[bt](?![aeiou])|[kl](?=n)|[w](?=r)|[h](?=[^aeiou])|[p](?=s)|[pt](?=[^aeiou])|[gh]|[qu]|[ue]|[x]|[c](?=e|i)', word.lower()):
            irregular_patterns += 1
            
        # Double letters not in pronunciation
        if re.search(r'(.)\1', word) and 'double' not in pronunciation.lower():
            irregular_patterns += 1
            
        # Foreign/irregular patterns
        if any(pattern in word.lower() for pattern in ['ph', 'ch', 'tion', 'ous', 'eau', 'ei']):
            irregular_patterns += 1
            
        # Score inversely related to irregular patterns
        return min(10, max(1, 8 - irregular_patterns * 2))
    
    def _calculate_word_frequency(self, word):
        """Score 1-10: How common the word is (lower = more common)"""
        # Common words (1-3)
        common = ['rats', 'raven', 'razor', 'reach', 'reaches', 'read', 'reading', 'really', 'realm', 'reason', 'reasonable', 'rebound', 'rebuke', 'recede', 'receive', 'receives', 'recently', 'recess', 'recipe', 'recital', 'reckless', 'reckon']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['raspberry', 'rattled', 'raucous', 'ravine', 'reactionary', 'reagent', 'realtor', 'receptacle', 'recipient', 'recluse']
        if word.lower() in moderate:
            return 5
            
        # Specialized/rare (7-10)
        return 8
    
    def _calculate_morphological_complexity(self, word):
        """Score 1-10: Complexity of word structure"""
        complexity = 1
        
        # Add points for length
        if len(word) > 15:
            complexity += 4
        elif len(word) > 12:
            complexity += 3
        elif len(word) > 8:
            complexity += 2
        elif len(word) > 6:
            complexity += 1
            
        # Add points for prefixes/suffixes
        prefixes = ['ras', 'rat', 'rav', 'ray', 'raz', 'rea', 'reb', 'rec']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing', 'ly', 'ism', 'ist', 'er', 'eer', 'ful', 'ical', 'ial', 'able', 'ory']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                complexity += 1
                break
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                complexity += 1
                break
        
        return min(10, complexity)
    
    def _calculate_etymology_complexity(self, etymology):
        """Score 1-10: Complexity of word origins"""
        if not etymology:
            return 5
            
        complexity = 3  # Base score
        
        # Multiple language origins increase complexity
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english', 'arabic', 'hebrew', 'old french', 'middle english', 'hindi', 'portuguese', 'jamaican']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 145
word_data = {
    'rasorial': {
        'definition': 'Relating to or characteristic of birds that scratch the ground for food; adapted for scratching or scraping. Rasorial birds include chickens, turkeys, and other ground-dwelling species that use their feet to uncover seeds, insects, and other food items from soil and leaf litter.',
        'pronunciation': '/rəˈsɔːriəl/',
        'pronunciation_respelling': 'ruh-SOR-ee-ul',
        'etymology': 'From Latin "rasor," meaning "scraper," from "radere" (to scrape) + suffix "-ial."',
        'memory_tip': 'Think "razor" + "ial" = relating to scraping like a razor (birds scraping ground).',
        'example_sentence': 'The ___ behavior of chickens involves scratching the dirt to find hidden seeds.',
        'source': 'Claude'
    },
    'raspberry': {
        'definition': 'A red or black edible berry composed of many small drupelets; the plant that bears this fruit; a rude sound made by vibrating the lips and tongue. Raspberries are rich in vitamins and antioxidants, while the slang meaning refers to a sound expressing derision or contempt.',
        'pronunciation': '/ˈræzbəri/',
        'pronunciation_respelling': 'RAZ-ber-ee',
        'etymology': 'From earlier "raspis berry," possibly from "rasp" (rough texture) + "berry."',
        'memory_tip': 'Think "rasp" (rough) + "berry" = a rough-textured berry.',
        'example_sentence': 'The fresh ___ tart was topped with whipped cream and mint leaves.',
        'source': 'Claude'
    },
    'rastafarian': {
        'definition': 'A member of a Jamaican religious movement that regards Haile Selassie I as divine; relating to Rastafarianism. This movement emerged in the 1930s, incorporating elements of Christianity, Pan-Africanism, and Ethiopian traditions, with distinctive practices including dreadlocks and cannabis use.',
        'pronunciation': '/ˌræstəˈfɛəriən/',
        'pronunciation_respelling': 'ras-tuh-FAIR-ee-un',
        'etymology': 'From "Ras Tafari," the pre-coronation name of Ethiopian Emperor Haile Selassie I.',
        'memory_tip': 'Think "Ras Tafari" (Haile Selassie\'s name) + "an" = follower of Ras Tafari.',
        'example_sentence': 'The ___ community gathered to celebrate Ethiopian Orthodox holidays.',
        'source': 'Claude'
    },
    'rathskeller': {
        'definition': 'A restaurant or tavern located in a basement, especially one serving German food and beer; originally referring to the basement of a German city hall used as a restaurant. These establishments became popular in American cities with German immigrant populations.',
        'pronunciation': '/ˈrɑːtskɛlər/',
        'pronunciation_respelling': 'RAHTS-kel-ur',
        'etymology': 'From German "Ratskeller," from "Rat" (council) + "Keller" (cellar).',
        'memory_tip': 'Think "rats" + "keller" (cellar) = underground restaurant (though not actually about rats).',
        'example_sentence': 'The historic ___ served authentic German sausages and locally brewed beer.',
        'source': 'Claude'
    },
    'rationale': {
        'definition': 'A set of reasons or logical basis for a course of action or belief; the fundamental reason or explanation for something. Rationale provides the underlying logic that justifies decisions, policies, or actions, helping others understand the reasoning process.',
        'pronunciation': '/ˌræʃəˈnæl/',
        'pronunciation_respelling': 'rash-uh-NAL',
        'etymology': 'From Latin "rationalis," meaning "of reason," from "ratio" (reason, calculation).',
        'memory_tip': 'Think "rational" + "e" = the rational explanation for something.',
        'example_sentence': 'The committee explained the ___ behind their decision to change the policy.',
        'source': 'Claude'
    },
    'rats': {
        'definition': 'Plural of rat; rodents with long tails, pointed snouts, and gnawing teeth; an exclamation of annoyance or frustration. Rats are intelligent, adaptable animals that have lived alongside humans throughout history, sometimes as pests and sometimes as valued laboratory animals.',
        'pronunciation': '/ræts/',
        'pronunciation_respelling': 'RATS',
        'etymology': 'Plural of "rat," from Old English "ræt," of uncertain origin.',
        'memory_tip': 'Think of multiple small rodents = rats.',
        'example_sentence': 'The barn owl helped control the population of ___ in the grain storage area.',
        'source': 'Claude'
    },
    'rattled': {
        'definition': 'Past tense of rattle; shaken or disturbed; made nervous or upset; produced a rapid succession of short, sharp sounds. When someone is rattled, they have lost their composure or confidence, often due to unexpected events or pressure.',
        'pronunciation': '/ˈrætəld/',
        'pronunciation_respelling': 'RAT-uld',
        'etymology': 'From "rattle" + past tense "-ed," from Middle English "ratelen" (to make noise).',
        'memory_tip': 'Think "rattle" + "ed" = was shaken up like something in a rattle.',
        'example_sentence': 'The unexpected question ___ the normally confident speaker.',
        'source': 'Claude'
    },
    'raucous': {
        'definition': 'Making or characterized by a harsh, disturbing noise; boisterous and disorderly. Raucous describes sounds that are loud, rough, and often unpleasant, or behavior that is rowdy and lacks restraint or decorum.',
        'pronunciation': '/ˈrɔːkəs/',
        'pronunciation_respelling': 'RAW-kus',
        'etymology': 'From Latin "raucus," meaning "hoarse" or "harsh-sounding."',
        'memory_tip': 'Think "raw" + "cous" = raw, harsh sounds.',
        'example_sentence': 'The ___ laughter from the comedy club could be heard down the street.',
        'source': 'Claude'
    },
    'raven': {
        'definition': 'A large black bird related to the crow, known for intelligence and adaptability; having a glossy black color; to devour greedily. Ravens appear in mythology and literature as symbols of wisdom, death, or prophecy, most famously in Edgar Allan Poe\'s poem.',
        'pronunciation': '/ˈreɪvən/',
        'pronunciation_respelling': 'RAY-vun',
        'etymology': 'From Old English "hræfn," related to Old Norse "hrafn."',
        'memory_tip': 'Think of the large black bird that says "nevermore" in Poe\'s poem.',
        'example_sentence': 'The intelligent ___ learned to mimic human speech and solve simple puzzles.',
        'source': 'Claude'
    },
    'ravigote': {
        'definition': 'A cold French sauce made with herbs, capers, and vinegar; typically served with cold meats or fish. Ravigote sauce contains ingredients like tarragon, chervil, parsley, and shallots, creating a tangy, fresh flavor that complements rich dishes.',
        'pronunciation': '/ˈrævɪɡoʊt/',
        'pronunciation_respelling': 'RAV-ih-goht',
        'etymology': 'From French "ravigote," from "ravigoter" meaning "to revive" or "to invigorate."',
        'memory_tip': 'Think "revive" + "goat" = a sauce that revives the flavor of food.',
        'example_sentence': 'The chef served the cold salmon with a traditional ___ sauce.',
        'source': 'Claude'
    },
    'ravine': {
        'definition': 'A narrow, deep valley with steep sides, typically formed by water erosion; a gorge or gully. Ravines are natural formations created by flowing water cutting through rock and soil over long periods, often creating dramatic landscape features.',
        'pronunciation': '/rəˈviːn/',
        'pronunciation_respelling': 'ruh-VEEN',
        'etymology': 'From French "ravine," from "ravir" meaning "to carry away" or "to ravage."',
        'memory_tip': 'Think "rave" + "ine" = a deep cut in the land that would make you rave about its beauty.',
        'example_sentence': 'The hikers carefully descended into the rocky ___ to reach the hidden waterfall.',
        'source': 'Claude'
    },
    'rayleigh': {
        'definition': 'Relating to Lord Rayleigh or phenomena named after him; a unit of measurement for the brightness of aurora and airglow. Rayleigh scattering explains why the sky appears blue, and Rayleigh waves are seismic waves that travel along the Earth\'s surface.',
        'pronunciation': '/ˈreɪli/',
        'pronunciation_respelling': 'RAY-lee',
        'etymology': 'Named after Lord Rayleigh (John William Strutt), British physicist.',
        'memory_tip': 'Think "ray" + "leigh" = named after the physicist who studied light rays.',
        'example_sentence': 'The atmospheric physicist measured ___ scattering to study air pollution.',
        'source': 'Claude'
    },
    'razor': {
        'definition': 'A sharp-edged tool used for shaving or cutting hair; something very sharp or cutting. Razors have evolved from simple blades to complex multi-blade systems, representing precision cutting instruments essential for grooming and various professional applications.',
        'pronunciation': '/ˈreɪzər/',
        'pronunciation_respelling': 'RAY-zur',
        'etymology': 'From Old French "rasoir," from "raser" meaning "to scrape" or "to shave."',
        'memory_tip': 'Think "raz" (scrape) + "or" = tool that scrapes hair away.',
        'example_sentence': 'The barber stropped his straight ___ before giving the customer a traditional shave.',
        'source': 'Claude'
    },
    'razz': {
        'definition': 'To tease or make fun of someone in a good-natured way; to heckle or harass playfully. Razzing involves friendly mockery or banter, typically among friends or teammates, without malicious intent.',
        'pronunciation': '/ræz/',
        'pronunciation_respelling': 'RAZ',
        'etymology': 'Short for "raspberry," referring to the rude sound made to express derision.',
        'memory_tip': 'Think of making a "raspberry" sound to tease someone = razz.',
        'example_sentence': 'His teammates would ___ him about his unusual pre-game rituals.',
        'source': 'Claude'
    },
    'reach': {
        'definition': 'To stretch out an arm or hand to touch or grasp something; to arrive at or achieve; the extent or range of something. Reach encompasses physical extension, goal achievement, and the scope of influence or capability.',
        'pronunciation': '/riːtʃ/',
        'pronunciation_respelling': 'REECH',
        'etymology': 'From Old English "rǣcan," meaning "to extend" or "to stretch out."',
        'memory_tip': 'Think of stretching to reach something just out of range.',
        'example_sentence': 'She had to ___ high on the shelf to get the book.',
        'source': 'Claude'
    },
    'reaches': {
        'definition': 'Third person singular of reach; achieves or arrives at; stretches or extends; remote or distant areas, especially of rivers or lands. The noun form refers to stretches of waterways or remote regions.',
        'pronunciation': '/ˈriːtʃɪz/',
        'pronunciation_respelling': 'REECH-iz',
        'etymology': 'From "reach" + third person singular "-es" or plural "-es."',
        'memory_tip': 'Think "reach" + "es" = multiple stretches or someone reaching.',
        'example_sentence': 'The explorer mapped the upper ___ of the Amazon River.',
        'source': 'Claude'
    },
    'reactionary': {
        'definition': 'Opposing political or social liberalization or reform; characterized by reaction against progressive change; a person who holds such views. Reactionary politics involves resistance to change and preference for traditional or previous conditions.',
        'pronunciation': '/riˈækʃəˌnɛri/',
        'pronunciation_respelling': 'ree-AK-shun-air-ee',
        'etymology': 'From "reaction" + suffix "-ary," from Latin "reactio" (action in return).',
        'memory_tip': 'Think "reaction" + "ary" = relating to reacting against change.',
        'example_sentence': 'The ___ politician opposed all the proposed social reforms.',
        'source': 'Claude'
    },
    'read': {
        'definition': 'To look at and understand written or printed words; to interpret or understand the meaning of something; past tense can also mean having knowledge of through reading. Reading is fundamental to education and communication in literate societies.',
        'pronunciation': '/riːd/ or /rɛd/',
        'pronunciation_respelling': 'REED or RED',
        'etymology': 'From Old English "rǣdan," meaning "to advise" or "to interpret."',
        'memory_tip': 'Think of decoding written symbols to understand meaning = read.',
        'example_sentence': 'Children learn to ___ by recognizing letters and connecting them to sounds.',
        'source': 'Claude'
    },
    'reading': {
        'definition': 'The action of looking at and understanding written text; an interpretation or understanding of something; a measurement from an instrument. Reading encompasses literacy skills, comprehension abilities, and data interpretation across various contexts.',
        'pronunciation': '/ˈriːdɪŋ/',
        'pronunciation_respelling': 'REED-ing',
        'etymology': 'From "read" + suffix "-ing," from Old English "rǣding."',
        'memory_tip': 'Think "read" + "ing" = the action of reading text.',
        'example_sentence': 'The librarian encouraged daily ___ to improve vocabulary and comprehension.',
        'source': 'Claude'
    },
    'reagent': {
        'definition': 'A substance used in a chemical reaction to detect, measure, examine, or produce other substances. Reagents are essential tools in chemistry, medicine, and research, allowing scientists to analyze samples and conduct experiments with predictable results.',
        'pronunciation': '/riˈeɪdʒənt/',
        'pronunciation_respelling': 'ree-AY-junt',
        'etymology': 'From "react" + suffix "-ent," from Latin "reagere" (to react).',
        'memory_tip': 'Think "react" + "ent" = something that helps substances react.',
        'example_sentence': 'The laboratory technician added the ___ to test for the presence of glucose.',
        'source': 'Claude'
    },
    'realgar': {
        'definition': 'A bright red or orange mineral consisting of arsenic sulfide, historically used as a pigment and in traditional medicine. Realgar is toxic due to its arsenic content but was valued for its vibrant color in ancient art and decorative applications.',
        'pronunciation': '/riˈælɡər/',
        'pronunciation_respelling': 'ree-AL-gur',
        'etymology': 'From Arabic "rahj al-ghar," meaning "powder of the mine."',
        'memory_tip': 'Think "real" + "gar" = really red mineral (like garnet).',
        'example_sentence': 'Ancient Chinese artists used ___ to create brilliant red pigments for paintings.',
        'source': 'Claude'
    },
    'realia': {
        'definition': 'Real objects and materials from everyday life used in language teaching; authentic items that provide cultural context. Realia helps language learners understand practical applications and cultural significance of vocabulary and concepts.',
        'pronunciation': '/riˈeɪliə/',
        'pronunciation_respelling': 'ree-AY-lee-uh',
        'etymology': 'From Latin "realis," meaning "actual" or "real," + plural suffix "-ia."',
        'memory_tip': 'Think "real" + "ia" = real items used for teaching.',
        'example_sentence': 'The Spanish teacher used ___ like menus and newspapers to teach practical vocabulary.',
        'source': 'Claude'
    },
    'really': {
        'definition': 'Actually; in fact; to a great degree; very much; genuinely or truly. Really serves as an intensifier to emphasize truth, degree, or authenticity, expressing surprise, confirmation, or strong feeling about something.',
        'pronunciation': '/ˈriːəli/',
        'pronunciation_respelling': 'REE-uh-lee',
        'etymology': 'From "real" + suffix "-ly," from Latin "realis."',
        'memory_tip': 'Think "real" + "ly" = in a real, genuine way.',
        'example_sentence': 'She was ___ excited about starting her new job next week.',
        'source': 'Claude'
    },
    'realm': {
        'definition': 'A kingdom or domain ruled by a monarch; a field or sphere of activity or interest; an area of knowledge or experience. Realm can refer to both literal territories and metaphorical domains of expertise or influence.',
        'pronunciation': '/rɛlm/',
        'pronunciation_respelling': 'RELM',
        'etymology': 'From Old French "realme," from Latin "regalis" (royal).',
        'memory_tip': 'Think "real" + "m" = a real kingdom or domain.',
        'example_sentence': 'The professor was an expert in the ___ of molecular biology.',
        'source': 'Claude'
    },
    'realpolitik': {
        'definition': 'Politics based on practical rather than moral or ideological considerations; pragmatic political realism. Realpolitik involves making decisions based on actual circumstances and power relationships rather than abstract principles or ideals.',
        'pronunciation': '/riˈɑːlpɒlɪˌtiːk/',
        'pronunciation_respelling': 'ree-AHL-pol-ih-teek',
        'etymology': 'From German "Realpolitik," from "real" (practical) + "Politik" (politics).',
        'memory_tip': 'Think "real" + "politik" = realistic, practical politics.',
        'example_sentence': 'The diplomat practiced ___, focusing on achievable goals rather than idealistic principles.',
        'source': 'Claude'
    },
    'realtor': {
        'definition': 'A real estate agent who is a member of the National Association of Realtors; a person who arranges the buying and selling of real estate. Realtors must adhere to specific professional standards and ethical codes established by their professional organization.',
        'pronunciation': '/ˈriːəltər/',
        'pronunciation_respelling': 'REE-ul-tur',
        'etymology': 'Trademark term from "real" + suffix "-tor," coined by the National Association of Real Estate Boards.',
        'memory_tip': 'Think "real" + "tor" = one who deals with real estate.',
        'example_sentence': 'The experienced ___ helped them find a house within their budget.',
        'source': 'Claude'
    },
    'reason': {
        'definition': 'The power of thinking logically and rationally; a cause or explanation for an action or phenomenon; to think logically about something. Reason distinguishes humans as rational beings capable of analysis, judgment, and logical thought processes.',
        'pronunciation': '/ˈriːzən/',
        'pronunciation_respelling': 'REE-zun',
        'etymology': 'From Old French "raison," from Latin "ratio" meaning "calculation" or "reasoning."',
        'memory_tip': 'Think of logical thinking and explanations = reason.',
        'example_sentence': 'The scientist used careful ___ to develop her hypothesis about the phenomenon.',
        'source': 'Claude'
    },
    'reasonable': {
        'definition': 'Based on good sense and sound judgment; fair and sensible; not extreme or excessive. Reasonable describes actions, prices, demands, or expectations that are logical, appropriate, and within acceptable limits.',
        'pronunciation': '/ˈriːzənəbəl/',
        'pronunciation_respelling': 'REE-zun-uh-bul',
        'etymology': 'From "reason" + suffix "-able," meaning "capable of being reasoned."',
        'memory_tip': 'Think "reason" + "able" = able to be reasoned with or logical.',
        'example_sentence': 'The landlord set a ___ rent price for the well-maintained apartment.',
        'source': 'Claude'
    },
    'rebarbative': {
        'definition': 'Repellent or unattractive; serving to irritate or repel; forbidding in appearance or manner. Rebarbative describes things or people that create immediate negative reactions, whether through appearance, attitude, or behavior.',
        'pronunciation': '/rɪˈbɑːrbətɪv/',
        'pronunciation_respelling': 'rih-BAR-buh-tiv',
        'etymology': 'From French "rébarbatif," from "rebarber" meaning "to be repulsive," from "re-" + "barbe" (beard).',
        'memory_tip': 'Think "re" + "barb" + "ative" = having repelling barbs like a porcupine.',
        'example_sentence': 'The critic\'s ___ personality made even simple conversations unpleasant.',
        'source': 'Claude'
    },
    'reboation': {
        'definition': 'The act of shouting back; a loud echo or reverberation; the return of sound waves from a surface. Reboation describes both the intentional act of shouting in response and the natural acoustic phenomenon of sound reflection.',
        'pronunciation': '/ˌriːboʊˈeɪʃən/',
        'pronunciation_respelling': 'ree-boh-AY-shun',
        'etymology': 'From Latin "reboatio," from "reboar" meaning "to resound" or "to bellow back."',
        'memory_tip': 'Think "re" + "boat" + "ion" = sound bouncing back like a boat echo.',
        'example_sentence': 'The ___ of voices in the canyon created a natural amphitheater effect.',
        'source': 'Claude'
    },
    'rebound': {
        'definition': 'To bounce back after hitting something; to recover from a setback or disappointment; in basketball, retrieving the ball after a missed shot. Rebound suggests resilience and the ability to return to a previous state or position.',
        'pronunciation': '/rɪˈbaʊnd/',
        'pronunciation_respelling': 'rih-BOWND',
        'etymology': 'From "re-" (back) + "bound" (leap), from Old French "bondir" (to leap).',
        'memory_tip': 'Think "re" + "bound" = bouncing back again.',
        'example_sentence': 'The basketball player grabbed the ___ and quickly passed to his teammate.',
        'source': 'Claude'
    },
    'rebuff': {
        'definition': 'To reject someone or something in an abrupt or ungracious manner; a blunt or abrupt rejection. Rebuffs involve dismissive responses that discourage further attempts at contact, negotiation, or relationship.',
        'pronunciation': '/rɪˈbʌf/',
        'pronunciation_respelling': 'rih-BUF',
        'etymology': 'From Italian "ribuffo," meaning "a repulse," from "ribuffare" (to repel).',
        'memory_tip': 'Think "re" + "buff" = buffeting someone back with rejection.',
        'example_sentence': 'Despite the initial ___, he continued to pursue the business partnership.',
        'source': 'Claude'
    },
    'rebuffrecanted': {
        'definition': '[COMBINED WORD ERROR] This appears to be "rebuff" + "recanted" incorrectly joined. Should be separated into two distinct words: "rebuff" (reject abruptly) and "recanted" (withdrew a previous statement).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "rebuff" (Italian: repulse) with "recanted" (Latin: sang back).',
        'memory_tip': '[ERROR] This should be split into "rebuff" (rejection) and "recanted" (withdrew statement).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "rebuff" and "recanted."',
        'source': 'Claude'
    },
    'rebuke': {
        'definition': 'To express sharp disapproval or criticism; to reprove or scold; a stern expression of disapproval. Rebukes involve formal or serious criticism intended to correct behavior or express strong disagreement with actions or statements.',
        'pronunciation': '/rɪˈbjuːk/',
        'pronunciation_respelling': 'rih-BYOOK',
        'etymology': 'From Old French "rebuquer," meaning "to repel" or "to beat back."',
        'memory_tip': 'Think "re" + "buke" (duke) = telling off someone like a duke would.',
        'example_sentence': 'The teacher\'s gentle ___ helped the student understand the importance of honesty.',
        'source': 'Claude'
    },
    'recamier': {
        'definition': 'A type of elegant sofa or chaise lounge with a curved back and one raised end, popular in the Empire period; named after Madame Récamier. These pieces feature neoclassical design elements and were fashionable in early 19th-century French interiors.',
        'pronunciation': '/ˈrɛkəmiər/',
        'pronunciation_respelling': 'REK-uh-meer',
        'etymology': 'Named after Madame Récamier, a French socialite known for her salon and elegant furniture.',
        'memory_tip': 'Think "recline" + "meer" (more) = more elegant way to recline.',
        'example_sentence': 'The antique ___ in the parlor was upholstered in silk brocade.',
        'source': 'Claude'
    },
    'recanted': {
        'definition': 'Past tense of recant; formally withdrew or disavowed a previous statement, belief, or opinion; renounced a previously held position. Recanting often occurs under pressure or after reflection leads to changed convictions.',
        'pronunciation': '/rɪˈkæntɪd/',
        'pronunciation_respelling': 'rih-KAN-tid',
        'etymology': 'From Latin "recantare," meaning "to sing back" or "to revoke," from "re-" + "cantare" (to sing).',
        'memory_tip': 'Think "re" + "cant" (chant) = chanting back to take back what you said.',
        'example_sentence': 'The witness ___ his previous testimony after discovering new evidence.',
        'source': 'Claude'
    },
    'recede': {
        'definition': 'To move back or away from a previous position; to become gradually less or smaller; to withdraw or retreat. Receding describes gradual movement away from an observer or a diminishing of presence, intensity, or prominence.',
        'pronunciation': '/rɪˈsiːd/',
        'pronunciation_respelling': 'rih-SEED',
        'etymology': 'From Latin "recedere," meaning "to go back," from "re-" (back) + "cedere" (to go).',
        'memory_tip': 'Think "re" + "cede" (give up) = giving up ground by moving back.',
        'example_sentence': 'As the tide began to ___, the children searched for shells on the exposed beach.',
        'source': 'Claude'
    },
    'receive': {
        'definition': 'To be given or presented with something; to accept delivery of something; to welcome guests; to experience or suffer something. Receiving involves being on the accepting end of transfers, whether physical objects, information, or experiences.',
        'pronunciation': '/rɪˈsiːv/',
        'pronunciation_respelling': 'rih-SEEV',
        'etymology': 'From Old French "receivre," from Latin "recipere," from "re-" + "capere" (to take).',
        'memory_tip': 'Think "re" + "ceive" (conceive) = taking in or conceiving something given.',
        'example_sentence': 'Students will ___ their diplomas at the graduation ceremony.',
        'source': 'Claude'
    },
    'receives': {
        'definition': 'Third person singular of receive; accepts or gets something; welcomes someone; experiences something. This form indicates ongoing or habitual receiving actions performed by a third party.',
        'pronunciation': '/rɪˈsiːvz/',
        'pronunciation_respelling': 'rih-SEEVZ',
        'etymology': 'From "receive" + third person singular "-s."',
        'memory_tip': 'Think "receive" + "s" = he/she receives something.',
        'example_sentence': 'The charity ___ donations from generous supporters throughout the year.',
        'source': 'Claude'
    },
    'recently': {
        'definition': 'At a recent time; not long ago; lately or in the near past. Recently indicates temporal proximity to the present moment, suggesting events or conditions that occurred within a relatively short time frame.',
        'pronunciation': '/ˈriːsəntli/',
        'pronunciation_respelling': 'REE-sunt-lee',
        'etymology': 'From "recent" + suffix "-ly," from Latin "recens" (fresh, new).',
        'memory_tip': 'Think "recent" + "ly" = in a recent manner, not long ago.',
        'example_sentence': 'The company ___ announced a new policy regarding remote work.',
        'source': 'Claude'
    },
    'receptacle': {
        'definition': 'A container used to hold something; in botany, the part of a flower stalk that bears the floral organs; any structure that receives and contains something. Receptacles serve storage, collection, or organizational functions across various contexts.',
        'pronunciation': '/rɪˈsɛptəkəl/',
        'pronunciation_respelling': 'rih-SEP-tuh-kul',
        'etymology': 'From Latin "receptaculum," meaning "reservoir," from "receptare" (to receive).',
        'memory_tip': 'Think "recept" (receive) + "acle" = something that receives and holds things.',
        'example_sentence': 'The waste ___ in the park was designed to blend with the natural surroundings.',
        'source': 'Claude'
    },
    'recess': {
        'definition': 'A break in proceedings; a small space set back from the main area; a temporary cessation of activity; in schools, a period for play and relaxation. Recess provides necessary breaks from structured activities.',
        'pronunciation': '/rɪˈsɛs/',
        'pronunciation_respelling': 'rih-SES',
        'etymology': 'From Latin "recessus," meaning "a going back" or "withdrawal," from "recedere."',
        'memory_tip': 'Think "re" + "cess" (cease) = ceasing activity temporarily.',
        'example_sentence': 'The children played tag during their afternoon ___ period.',
        'source': 'Claude'
    },
    'recipe': {
        'definition': 'A set of instructions for preparing a dish or a formula for achieving a particular result; a method or procedure for accomplishing something. Recipes provide systematic approaches to creating desired outcomes, whether culinary or metaphorical.',
        'pronunciation': '/ˈrɛsəpi/',
        'pronunciation_respelling': 'RES-uh-pee',
        'etymology': 'From Latin "recipe," meaning "take" (imperative of "recipere"), used in medical prescriptions.',
        'memory_tip': 'Think of instructions that help you "receive" (create) a dish.',
        'example_sentence': 'Grandmother\'s secret ___ for apple pie included a hint of cardamom.',
        'source': 'Claude'
    },
    'recipient': {
        'definition': 'A person or thing that receives something; someone who is given an award, gift, or benefit. Recipients are on the receiving end of transfers, whether tangible items, honors, or assistance.',
        'pronunciation': '/rɪˈsɪpiənt/',
        'pronunciation_respelling': 'rih-SIP-ee-unt',
        'etymology': 'From Latin "recipiens," meaning "receiving," from "recipere" (to receive).',
        'memory_tip': 'Think "recip" (receive) + "ient" = one who receives.',
        'example_sentence': 'The scholarship ___ was chosen based on academic excellence and community service.',
        'source': 'Claude'
    },
    'reciprocity': {
        'definition': 'The practice of exchanging things with others for mutual benefit; a mutual exchange of privileges or advantages. Reciprocity forms the basis of many social, economic, and diplomatic relationships, creating balanced exchanges.',
        'pronunciation': '/ˌrɛsɪˈprɒsəti/',
        'pronunciation_respelling': 'res-ih-PROS-ih-tee',
        'etymology': 'From Latin "reciprocus," meaning "returning" or "alternating," + suffix "-ity."',
        'memory_tip': 'Think "recip" (receive) + "rocity" = receiving back what you give.',
        'example_sentence': 'The trade agreement was based on ___ between the two nations.',
        'source': 'Claude'
    },
    'reciprocityarchaic': {
        'definition': '[COMBINED WORD ERROR] This appears to be "reciprocity" + "archaic" incorrectly joined. Should be separated into two distinct words: "reciprocity" (mutual exchange) and "archaic" (very old or outdated).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "reciprocity" (Latin: returning) with "archaic" (Greek: ancient).',
        'memory_tip': '[ERROR] This should be split into "reciprocity" (mutual exchange) and "archaic" (ancient).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "reciprocity" and "archaic."',
        'source': 'Claude'
    },
    'recital': {
        'definition': 'A performance of music, poetry, or dance by a soloist or small group; a detailed account or description of events; an enumeration of facts or particulars. Recitals showcase individual talents and provide intimate performance experiences.',
        'pronunciation': '/rɪˈsaɪtəl/',
        'pronunciation_respelling': 'rih-SY-tul',
        'etymology': 'From "recite" + suffix "-al," from Latin "recitare" (to read aloud).',
        'memory_tip': 'Think "recite" + "al" = a performance involving reciting or playing.',
        'example_sentence': 'The piano student performed beautifully at her first solo ___.',
        'source': 'Claude'
    },
    'reckless': {
        'definition': 'Showing a lack of regard for danger or consequences; careless and irresponsible; acting without thinking about risks. Reckless behavior disregards safety and potential negative outcomes, often leading to dangerous situations.',
        'pronunciation': '/ˈrɛkləs/',
        'pronunciation_respelling': 'REK-lis',
        'etymology': 'From "reck" (to care) + suffix "-less," from Old English "recceleas."',
        'memory_tip': 'Think "reck" (care) + "less" = caring less about consequences.',
        'example_sentence': 'The ___ driver was speeding through the residential neighborhood.',
        'source': 'Claude'
    },
    'reckon': {
        'definition': 'To calculate or compute; to consider or regard in a particular way; to think or suppose. Reckoning involves both mathematical calculation and judgment or estimation about situations, people, or outcomes.',
        'pronunciation': '/ˈrɛkən/',
        'pronunciation_respelling': 'REK-un',
        'etymology': 'From Old English "recenian," meaning "to narrate" or "to account for."',
        'memory_tip': 'Think of counting and calculating = reckon.',
        'example_sentence': 'I ___ it will take about two hours to drive to the mountains.',
        'source': 'Claude'
    },
    'recluse': {
        'definition': 'A person who lives in seclusion and avoids contact with other people; someone who withdraws from society. Recluses choose isolation for various reasons, including spiritual pursuits, social anxiety, or preference for solitude.',
        'pronunciation': '/rɪˈkluːs/',
        'pronunciation_respelling': 'rih-KLOOS',
        'etymology': 'From Old French "reclus," meaning "shut up," from Latin "recludere" (to shut up).',
        'memory_tip': 'Think "re" + "cluse" (close) = someone who closes themselves away from others.',
        'example_sentence': 'The elderly ___ rarely left his mountain cabin except for essential supplies.',
        'source': 'Claude'
    }
}

def process_batch_145():
    """Process batch 145 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_145_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_145_processed.csv'
    
    processed_words = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            for i, row in enumerate(reader, 1):
                if i > 50:  # Limit to 50 words per batch
                    break
                    
                word = row['word'].strip().lower()
                years = row['years']
                source_files = row['source_files'] 
                source_difficulties = row['source_difficulties']
                
                print(f"Processing word {i}: {word}")
                
                # Get word data
                if word in word_data:
                    data = word_data[word]
                    
                    # Calculate difficulty scores
                    scores = calculator.calculate_difficulty_score(
                        word, 
                        data['pronunciation'], 
                        data['etymology']
                    )
                    
                    processed_word = {
                        'word': word,
                        'definition': data['definition'],
                        'pronunciation': data['pronunciation'],
                        'pronunciation_respelling': data['pronunciation_respelling'],
                        'etymology': data['etymology'],
                        'etymology_source': data['source'],
                        'memory_tip': data['memory_tip'],
                        'example_sentence': data['example_sentence'],
                        'example_sentence_source': data['source'],
                        'years': years,
                        'source_files': source_files,
                        'source_difficulties': source_difficulties,
                        'definition_source': data['source'],
                        'pronunciation_source': data['source'],
                        'phonetic_transparency_score': scores['phonetic_transparency_score'],
                        'word_frequency_score': scores['word_frequency_score'],
                        'morphological_complexity_score': scores['morphological_complexity_score'],
                        'etymology_complexity_score': scores['etymology_complexity_score'],
                        'total_difficulty_score': scores['total_difficulty_score'],
                        'assigned_difficulty': None,  # To be assigned later
                        'audio_file_path': None,
                        'created_at': '2025-01-01',
                        'updated_at': '2025-01-01',
                        'notes': 'Batch 145 processing',
                        'review_status': 'pending',
                        'batch_number': 145
                    }
                    
                    processed_words.append(processed_word)
                else:
                    print(f"Warning: No data found for word '{word}'")
        
        # Write output CSV
        if processed_words:
            fieldnames = [
                'word', 'definition', 'pronunciation', 'pronunciation_respelling', 
                'etymology', 'etymology_source', 'memory_tip', 'example_sentence',
                'example_sentence_source', 'years', 'source_files', 'source_difficulties',
                'definition_source', 'pronunciation_source', 'phonetic_transparency_score',
                'word_frequency_score', 'morphological_complexity_score', 
                'etymology_complexity_score', 'total_difficulty_score', 'assigned_difficulty',
                'audio_file_path', 'created_at', 'updated_at', 'notes', 'review_status', 'batch_number'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
            
            print(f"\nBatch 145 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 145: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_145()