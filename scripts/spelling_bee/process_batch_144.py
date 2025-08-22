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
        if re.search(r'[bt](?![aeiou])|[kl](?=n)|[w](?=r)|[h](?=[^aeiou])|[p](?=s)|[pt](?=[^aeiou])|[gh]|[qu]|[ue]|[x]', word.lower()):
            irregular_patterns += 1
            
        # Double letters not in pronunciation
        if re.search(r'(.)\1', word) and 'double' not in pronunciation.lower():
            irregular_patterns += 1
            
        # Foreign/irregular patterns
        if any(pattern in word.lower() for pattern in ['ph', 'ch', 'tion', 'ous']):
            irregular_patterns += 1
            
        # Score inversely related to irregular patterns
        return min(10, max(1, 8 - irregular_patterns * 2))
    
    def _calculate_word_frequency(self, word):
        """Score 1-10: How common the word is (lower = more common)"""
        # Common words (1-3)
        common = ['radio', 'rage', 'raising', 'rallies', 'rampage', 'ranked', 'ransom', 'rapidly', 'rapids', 'rare', 'rarely', 'rascal']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['racial', 'radiation', 'railroad', 'raindrop', 'raisin', 'ramifications', 'ramparts', 'rancid', 'ransacked']
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
        prefixes = ['ra', 'rac', 'rad', 'raf', 'rag', 'rai', 'raj', 'ram', 'ran', 'rap', 'rar']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing', 'ly', 'ism', 'ist', 'er', 'eer', 'ful', 'ical', 'ial']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english', 'arabic', 'hebrew', 'old french', 'middle english', 'hindi', 'portuguese']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 144
word_data = {
    'rabid': {
        'definition': 'Extremely fanatical or zealous; affected with rabies; characterized by extreme intensity or violence. In medical contexts, rabid refers to animals infected with the rabies virus, displaying aggressive behavior and neurological symptoms. Figuratively, it describes people with intense, unreasonable devotion to causes or beliefs.',
        'pronunciation': '/ˈræbɪd/',
        'pronunciation_respelling': 'RAB-id',
        'etymology': 'From Latin "rabidus," meaning "raging" or "mad," from "rabere" (to rage).',
        'memory_tip': 'Think "rab" (grab) + "id" = grabbing onto ideas with intense fury.',
        'example_sentence': 'The ___ sports fan never missed a single game despite living hundreds of miles away.',
        'source': 'Claude'
    },
    'racecourse': {
        'definition': 'A track or course designed for racing, especially horse racing; a designated area where competitive races take place. Racecourses are carefully designed with specific distances, surfaces, and safety features to accommodate different types of racing competitions while ensuring fair and safe conditions for participants.',
        'pronunciation': '/ˈreɪskɔːrs/',
        'pronunciation_respelling': 'RAYS-kors',
        'etymology': 'Compound of "race" + "course," from Old French "racier" (to run) + Latin "cursus" (running).',
        'memory_tip': 'Think "race" + "course" = a course designed specifically for racing.',
        'example_sentence': 'The historic ___ hosted its annual derby with thousands of spectators in attendance.',
        'source': 'Claude'
    },
    'racial': {
        'definition': 'Relating to race or ethnic groups; involving or characterized by relations between people of different races. Racial considerations appear in discussions of equality, justice, demographics, and social policy, requiring sensitivity and understanding of historical and contemporary contexts.',
        'pronunciation': '/ˈreɪʃəl/',
        'pronunciation_respelling': 'RAY-shul',
        'etymology': 'From "race" + suffix "-ial," from French "race," possibly from Arabic "ras" (head).',
        'memory_tip': 'Think "race" + "ial" = relating to different races of people.',
        'example_sentence': 'The civil rights movement fought against ___ discrimination and segregation.',
        'source': 'Claude'
    },
    'racketeer': {
        'definition': 'A person who engages in dishonest and fraudulent business dealings; someone involved in organized crime or illegal schemes. Racketeering involves systematic criminal activity, often including extortion, fraud, or other illegal methods of generating income through intimidation or deception.',
        'pronunciation': '/ˌrækəˈtɪr/',
        'pronunciation_respelling': 'rak-uh-TEER',
        'etymology': 'From "racket" (fraudulent scheme) + suffix "-eer," from earlier "racket" meaning noise or disturbance.',
        'memory_tip': 'Think "racket" (noise/scheme) + "eer" = one who makes criminal schemes.',
        'example_sentence': 'The FBI investigation exposed the ___ who had been running illegal gambling operations.',
        'source': 'Claude'
    },
    'raclette': {
        'definition': 'A Swiss dish consisting of melted cheese scraped onto bread, potatoes, or vegetables; also the type of cheese used in this dish. Raclette originated in Swiss Alpine regions and involves heating a wheel of cheese and scraping the melted portion onto accompaniments, creating a communal dining experience.',
        'pronunciation': '/rəˈklɛt/',
        'pronunciation_respelling': 'ruh-KLET',
        'etymology': 'From French "racler," meaning "to scrape," referring to the method of preparation.',
        'memory_tip': 'Think "rack" + "lette" = racking up melted cheese on bread.',
        'example_sentence': 'The Swiss restaurant specialized in traditional ___ served with small potatoes and pickles.',
        'source': 'Claude'
    },
    'radiation': {
        'definition': 'The emission of energy as electromagnetic waves or atomic particles; the process of giving off energy in the form of rays or waves. Radiation occurs naturally in sunlight and cosmic rays, and artificially in medical treatments and nuclear processes. Understanding radiation is crucial for physics, medicine, and environmental science.',
        'pronunciation': '/ˌreɪdiˈeɪʃən/',
        'pronunciation_respelling': 'ray-dee-AY-shun',
        'etymology': 'From Latin "radiatio," from "radiare" meaning "to shine" or "to emit rays."',
        'memory_tip': 'Think "radiate" + "tion" = the process of radiating energy outward.',
        'example_sentence': 'Medical technicians wore protective equipment when working with ___ in the imaging department.',
        'source': 'Claude'
    },
    'radicchio': {
        'definition': 'A type of Italian chicory with red or purple leaves and white veins, used in salads and cooking; known for its slightly bitter taste and colorful appearance. Radicchio adds visual appeal and distinctive flavor to culinary preparations, particularly in Mediterranean cuisine.',
        'pronunciation': '/rəˈdɪkioʊ/',
        'pronunciation_respelling': 'ruh-DIK-ee-oh',
        'etymology': 'From Italian "radicchio," from Latin "radicula," diminutive of "radix" (root).',
        'memory_tip': 'Think "radical" + "chio" = radically colorful Italian vegetable.',
        'example_sentence': 'The chef tossed ___ with arugula and walnuts for a colorful winter salad.',
        'source': 'Claude'
    },
    'radio': {
        'definition': 'A system for transmitting sound by electromagnetic waves; a device for receiving such transmissions; the broadcasting industry using radio waves. Radio revolutionized communication and entertainment, enabling instant transmission of information, music, and programs across vast distances.',
        'pronunciation': '/ˈreɪdioʊ/',
        'pronunciation_respelling': 'RAY-dee-oh',
        'etymology': 'From Latin "radius," meaning "ray" or "beam," referring to electromagnetic rays.',
        'memory_tip': 'Think "ray" + "dio" = rays carrying sound through the air.',
        'example_sentence': 'The emergency ___ broadcast warned residents about the approaching storm.',
        'source': 'Claude'
    },
    'radioactivity': {
        'definition': 'The spontaneous emission of radiation from the nuclei of unstable atoms; the property of certain elements to decay and emit energy. Radioactivity occurs naturally in some elements and can be induced artificially, playing crucial roles in medicine, energy production, and scientific research.',
        'pronunciation': '/ˌreɪdioʊækˈtɪvəti/',
        'pronunciation_respelling': 'ray-dee-oh-ak-TIV-ih-tee',
        'etymology': 'From "radio" (radiation) + "activity," coined by Marie Curie to describe the phenomenon.',
        'memory_tip': 'Think "radio" + "activity" = active emission of radiation.',
        'example_sentence': 'Scientists studied the ___ of uranium samples to understand nuclear decay.',
        'source': 'Claude'
    },
    'radius': {
        'definition': 'The distance from the center of a circle to its edge; one of the two bones in the forearm; the range or scope of activity or influence. In geometry, radius is fundamental for calculating circumference and area, while anatomically it enables forearm rotation.',
        'pronunciation': '/ˈreɪdiəs/',
        'pronunciation_respelling': 'RAY-dee-us',
        'etymology': 'From Latin "radius," meaning "ray," "spoke of a wheel," or "staff."',
        'memory_tip': 'Think "ray" + "dius" = a ray extending from the center outward.',
        'example_sentence': 'The circle had a ___ of five centimeters, making its diameter ten centimeters.',
        'source': 'Claude'
    },
    'rafflesia': {
        'definition': 'A genus of parasitic flowering plants known for producing the largest individual flowers in the world; found in Southeast Asian rainforests. Rafflesia flowers can reach three feet in diameter, emit a rotting smell to attract flies for pollination, and lack stems, leaves, or visible roots.',
        'pronunciation': '/rəˈfliːziə/',
        'pronunciation_respelling': 'ruh-FLEE-zee-uh',
        'etymology': 'Named after Sir Stamford Raffles, British statesman who founded Singapore.',
        'memory_tip': 'Think "Raffles" + "ia" = named after Raffles, the giant stinky flower.',
        'example_sentence': 'Botanists traveled deep into the jungle to study the rare ___ in its natural habitat.',
        'source': 'Claude'
    },
    'ragamuffin': {
        'definition': 'A child wearing ragged, dirty clothes; a person of disreputable appearance; someone who looks disheveled or unkempt. Ragamuffin originally described street children in poor conditions but can affectionately refer to anyone with a charmingly messy appearance.',
        'pronunciation': '/ˈræɡəˌmʌfɪn/',
        'pronunciation_respelling': 'RAG-uh-muf-in',
        'etymology': 'From "rag" + "muffin," possibly influenced by a 14th-century poem character named Ragamuffyn.',
        'memory_tip': 'Think "rag" + "muffin" = a child wrapped in rags like a muffin.',
        'example_sentence': 'Despite being dressed like a ___, the child had an infectious smile and bright eyes.',
        'source': 'Claude'
    },
    'rage': {
        'definition': 'Violent, uncontrolled anger; intense fury or wrath; something that is very popular or fashionable. Rage represents extreme emotional intensity that can be destructive if uncontrolled, but the term also describes passionate enthusiasm for trends or activities.',
        'pronunciation': '/reɪdʒ/',
        'pronunciation_respelling': 'RAYJ',
        'etymology': 'From Old French "rage," from Latin "rabies," meaning "madness" or "fury."',
        'memory_tip': 'Think of explosive anger that "rages" like a storm.',
        'example_sentence': 'The driver\'s ___ over the traffic jam caused him to honk his horn repeatedly.',
        'source': 'Claude'
    },
    'ragwort': {
        'definition': 'A yellow-flowered plant of the daisy family, common in grasslands and waste areas; considered a weed in many regions but important for wildlife. Ragwort is toxic to livestock but provides nectar for numerous insects and supports several specialized caterpillar species.',
        'pronunciation': '/ˈræɡwɜːrt/',
        'pronunciation_respelling': 'RAG-wurt',
        'etymology': 'From "rag" (referring to the ragged leaf shape) + "wort" (plant).',
        'memory_tip': 'Think "ragged" + "wort" = a plant with ragged-looking leaves.',
        'example_sentence': 'The field was covered in yellow ___ flowers that attracted clouds of butterflies.',
        'source': 'Claude'
    },
    'railings': {
        'definition': 'Plural of railing; protective barriers consisting of rails supported by posts; fences or barriers designed to prevent falls or provide support. Railings serve safety functions on stairs, balconies, and elevated walkways while often contributing to architectural aesthetics.',
        'pronunciation': '/ˈreɪlɪŋz/',
        'pronunciation_respelling': 'RAY-lingz',
        'etymology': 'From "rail" + suffix "-ing" + plural "-s," from Old French "reille" (bar).',
        'memory_tip': 'Think "rail" + "ings" = multiple rail barriers for safety.',
        'example_sentence': 'The ornate iron ___ along the staircase were both beautiful and functional.',
        'source': 'Claude'
    },
    'railleur': {
        'definition': 'A person who engages in good-natured teasing or banter; someone who practices raillery or playful mockery. A railleur uses wit and humor to gently tease others, maintaining social bonds through clever verbal exchanges rather than mean-spirited criticism.',
        'pronunciation': '/raɪˈjɜːr/',
        'pronunciation_respelling': 'ry-YUR',
        'etymology': 'From French "railleur," from "railler" meaning "to tease" or "to jest."',
        'memory_tip': 'Think French "rail" + "leur" = one who rails/teases playfully.',
        'example_sentence': 'The dinner party\'s ___ kept everyone laughing with witty observations and gentle teasing.',
        'source': 'Claude'
    },
    'railroad': {
        'definition': 'A permanent road laid with rails for trains; a system of transportation using trains on tracks; to push something through quickly without proper consideration. Railroads revolutionized transportation and commerce, enabling rapid movement of people and goods across continents.',
        'pronunciation': '/ˈreɪlroʊd/',
        'pronunciation_respelling': 'RAYL-rohd',
        'etymology': 'Compound of "rail" + "road," from Old French "reille" (bar) + Old English "rad" (riding).',
        'memory_tip': 'Think "rail" + "road" = a road made of rails for trains.',
        'example_sentence': 'The transcontinental ___ connected the Atlantic and Pacific coasts for the first time.',
        'source': 'Claude'
    },
    'raindrop': {
        'definition': 'A single drop of rain; a small spherical mass of water falling from clouds during precipitation. Raindrops form when water vapor condenses around particles in clouds, growing until gravity causes them to fall, providing essential water for ecosystems and agriculture.',
        'pronunciation': '/ˈreɪndrɑːp/',
        'pronunciation_respelling': 'RAYN-drop',
        'etymology': 'Compound of "rain" + "drop," from Old English "regn" + "dropa."',
        'memory_tip': 'Think "rain" + "drop" = a single drop of falling rain.',
        'example_sentence': 'Each ___ on the spider\'s web sparkled like a tiny diamond in the morning light.',
        'source': 'Claude'
    },
    'raisin': {
        'definition': 'A dried grape, typically dark in color and wrinkled in appearance; used in cooking, baking, and as a snack. Raisins are produced by drying grapes in the sun or through dehydration, concentrating their natural sugars and creating a preserved fruit with extended shelf life.',
        'pronunciation': '/ˈreɪzən/',
        'pronunciation_respelling': 'RAY-zun',
        'etymology': 'From Old French "raisin," meaning "grape," from Latin "racemus" (cluster of grapes).',
        'memory_tip': 'Think "rays" + "in" = grapes dried in the sun\'s rays.',
        'example_sentence': 'The oatmeal cookies were studded with plump ___ and cinnamon.',
        'source': 'Claude'
    },
    'raising': {
        'definition': 'Present participle of raise; lifting up; increasing in amount or level; bringing up children; constructing or erecting. Raising encompasses physical lifting, numerical increases, child-rearing, and building activities, representing upward movement in various contexts.',
        'pronunciation': '/ˈreɪzɪŋ/',
        'pronunciation_respelling': 'RAY-zing',
        'etymology': 'From "raise" + suffix "-ing," from Old Norse "reisa" (to raise).',
        'memory_tip': 'Think "raise" + "ing" = the action of lifting or increasing something.',
        'example_sentence': 'The committee discussed ___ funds for the new community center.',
        'source': 'Claude'
    },
    'raja': {
        'definition': 'An Indian prince or king; a ruler of an Indian state under British colonial rule; a title of nobility in South Asian cultures. Raja represents traditional monarchical authority in Indian subcontinent history, often maintaining ceremonial roles in modern times.',
        'pronunciation': '/ˈrɑːdʒə/',
        'pronunciation_respelling': 'RAH-juh',
        'etymology': 'From Sanskrit "raja," meaning "king" or "ruler."',
        'memory_tip': 'Think "royal" + "ah" = royal ruler in Indian culture.',
        'example_sentence': 'The ___ lived in a magnificent palace overlooking the sacred river.',
        'source': 'Claude'
    },
    'rajpramukh': {
        'definition': 'The head of state of an Indian princely union under the early Indian Republic; a position created when princely states were integrated into India after independence. Rajpramukhs served as constitutional heads of merged princely states until the reorganization of Indian states.',
        'pronunciation': '/ˈrɑːdʒprəˌmʊx/',
        'pronunciation_respelling': 'RAHJ-pruh-mookh',
        'etymology': 'From Sanskrit "raja" (king) + "pramukh" (chief or head).',
        'memory_tip': 'Think "raja" (king) + "pramukh" (chief) = chief of kings.',
        'example_sentence': 'The ___ represented the merged princely states in India\'s federal structure.',
        'source': 'Claude'
    },
    'rallies': {
        'definition': 'Plural of rally; gatherings for a common purpose; political demonstrations; recoveries from decline; mass meetings to support causes. Rallies bring people together to express shared beliefs, recover from setbacks, or demonstrate strength in numbers.',
        'pronunciation': '/ˈræliːz/',
        'pronunciation_respelling': 'RAL-eez',
        'etymology': 'From "rally" + plural "-s," from French "rallier" (to reunite).',
        'memory_tip': 'Think "rally" + "ies" = multiple gatherings or recoveries.',
        'example_sentence': 'The candidate scheduled several campaign ___ in key swing states.',
        'source': 'Claude'
    },
    'ramadan': {
        'definition': 'The ninth month of the Islamic lunar calendar; a period of fasting, prayer, and reflection observed by Muslims worldwide. During Ramadan, Muslims fast from dawn to sunset, engage in spiritual practices, and focus on charity and community, concluding with Eid al-Fitr celebrations.',
        'pronunciation': '/ˌræməˈdɑːn/',
        'pronunciation_respelling': 'ram-uh-DAHN',
        'etymology': 'From Arabic "Ramadan," derived from "ramida" meaning "to be hot" or "to burn."',
        'memory_tip': 'Think "ram" + "adan" = the sacred month of fasting and prayer.',
        'example_sentence': 'During ___, the family gathered each evening to break their fast together.',
        'source': 'Claude'
    },
    'ramadhanthe': {
        'definition': '[COMBINED WORD ERROR] This appears to be "Ramadhan" + "the" incorrectly joined. Should be separated into two distinct words: "Ramadhan" (alternative spelling of Ramadan) and "the" (definite article).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "Ramadhan" (Arabic: hot month) with "the" (English: definite article).',
        'memory_tip': '[ERROR] This should be split into "Ramadhan" (Islamic month) and "the" (article).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "Ramadhan" and "the."',
        'source': 'Claude'
    },
    'rambla': {
        'definition': 'A broad, tree-lined avenue or promenade, especially in Spain; a seasonal watercourse or dry riverbed. The most famous example is Las Ramblas in Barcelona, a pedestrian street known for shopping, dining, and street entertainment.',
        'pronunciation': '/ˈræmblə/',
        'pronunciation_respelling': 'RAM-bluh',
        'etymology': 'From Spanish "rambla," from Arabic "raml" meaning "sand."',
        'memory_tip': 'Think "ramble" + "a" = a place where people ramble and stroll.',
        'example_sentence': 'Tourists enjoyed walking down the famous ___ in Barcelona, watching street performers.',
        'source': 'Claude'
    },
    'rambunctious': {
        'definition': 'Uncontrollably exuberant; boisterous and energetic in a playful way; difficult to control due to high spirits. Rambunctious describes lively, enthusiastic behavior that is generally positive but can be overwhelming, especially in children or animals.',
        'pronunciation': '/ræmˈbʌŋkʃəs/',
        'pronunciation_respelling': 'ram-BUNK-shus',
        'etymology': 'Possibly from "rumbustious," influenced by "rambunctious," of uncertain origin.',
        'memory_tip': 'Think "ram" + "bunch" + "ious" = like a bunch of rams, very energetic.',
        'example_sentence': 'The ___ puppies tumbled over each other in their eagerness to play.',
        'source': 'Claude'
    },
    'rambunctiousnoun': {
        'definition': '[COMBINED WORD ERROR] This appears to be "rambunctious" + "noun" incorrectly joined. Should be separated into two distinct words: "rambunctious" (boisterous) and "noun" (part of speech).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "rambunctious" (energetic) with "noun" (grammar term).',
        'memory_tip': '[ERROR] This should be split into "rambunctious" (boisterous) and "noun" (word type).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "rambunctious" and "noun."',
        'source': 'Claude'
    },
    'ramifications': {
        'definition': 'Complex or unwelcome consequences of an action or event; the results that follow from a particular action, often unintended. Ramifications suggest branching effects that extend beyond immediate results, creating networks of influence and consequence that may be difficult to predict or control.',
        'pronunciation': '/ˌræməfəˈkeɪʃənz/',
        'pronunciation_respelling': 'ram-ih-fih-KAY-shunz',
        'etymology': 'From Latin "ramificare," meaning "to branch," from "ramus" (branch) + "facere" (to make).',
        'memory_tip': 'Think "rami" (branches) + "fications" = branching out into consequences.',
        'example_sentence': 'The policy change had unexpected ___ that affected multiple departments.',
        'source': 'Claude'
    },
    'rampage': {
        'definition': 'A period of violent or destructive behavior; to rush about wildly or violently. Rampages involve loss of control and aggressive actions that cause damage or disruption, whether by individuals, groups, or even natural forces like storms.',
        'pronunciation': '/ˈræmpeɪdʒ/',
        'pronunciation_respelling': 'RAM-payj',
        'etymology': 'From Scottish "ramp," meaning "to storm" or "to rage," possibly from "ramp" (to rear up).',
        'memory_tip': 'Think "ramp" + "age" = going on a destructive ramp of rage.',
        'example_sentence': 'The angry crowd went on a ___ through the city center, breaking windows.',
        'source': 'Claude'
    },
    'ramparts': {
        'definition': 'Defensive walls of a castle or walled city; broad defensive embankments surrounding a fortification. Ramparts were essential military architecture, providing elevated positions for defenders and protection from attackers, often featuring walkways for guards and weapon emplacements.',
        'pronunciation': '/ˈræmpɑːrts/',
        'pronunciation_respelling': 'RAM-parts',
        'etymology': 'From French "rempart," from "remparer" (to fortify), from "re-" + "emparer" (to seize).',
        'memory_tip': 'Think "ramp" + "parts" = elevated parts that ramp up for defense.',
        'example_sentence': 'The medieval castle\'s ___ provided protection against enemy siege weapons.',
        'source': 'Claude'
    },
    'ramson': {
        'definition': 'Wild garlic; a European plant with broad leaves and white flowers, used as a culinary herb. Ramson grows in woodlands and has a strong garlic flavor, making it popular in traditional cooking and modern wild food foraging.',
        'pronunciation': '/ˈræmsən/',
        'pronunciation_respelling': 'RAM-sun',
        'etymology': 'From Old English "hramsan," related to "rams" (wild garlic).',
        'memory_tip': 'Think "rams" + "on" = rams would eat this wild garlic plant.',
        'example_sentence': 'The chef foraged for ___ in the spring woods to make a wild garlic soup.',
        'source': 'Claude'
    },
    'ranchero': {
        'definition': 'A ranch owner or worker; a style of Mexican music and dress; relating to ranch life in Mexico. Ranchero culture represents traditional rural Mexican lifestyle, including distinctive music, clothing, and customs associated with cattle ranching and rural communities.',
        'pronunciation': '/rænˈtʃɛroʊ/',
        'pronunciation_respelling': 'ran-CHER-oh',
        'etymology': 'From Spanish "ranchero," from "rancho" (ranch), from "rancharse" (to make camp).',
        'memory_tip': 'Think "ranch" + "ero" (Spanish ending) = one who works on a ranch.',
        'example_sentence': 'The ___ music filled the cantina with tales of love and life on the range.',
        'source': 'Claude'
    },
    'rancid': {
        'definition': 'Having an unpleasant smell or taste due to decomposition, especially of fats or oils; stale and offensive. Rancidity occurs when fats oxidize, creating compounds with strong, unpleasant odors and flavors that indicate food spoilage.',
        'pronunciation': '/ˈrænsɪd/',
        'pronunciation_respelling': 'RAN-sid',
        'etymology': 'From Latin "rancidus," meaning "stinking" or "rank."',
        'memory_tip': 'Think "ran" + "cid" = ran away because it smelled bad (rancid).',
        'example_sentence': 'The ___ butter had been left out too long and was no longer edible.',
        'source': 'Claude'
    },
    'ranine': {
        'definition': 'Relating to the underside of the tongue; pertaining to frogs or the frog family. In medical terminology, ranine refers to structures beneath the tongue, while in zoology, it describes characteristics of amphibians, particularly frogs and their relatives.',
        'pronunciation': '/ˈreɪnaɪn/',
        'pronunciation_respelling': 'RAY-nyn',
        'etymology': 'From Latin "rana," meaning "frog," + suffix "-ine."',
        'memory_tip': 'Think "rain" + "ine" = relating to creatures that love rain (frogs).',
        'example_sentence': 'The doctor examined the patient\'s ___ area for signs of inflammation.',
        'source': 'Claude'
    },
    'ranked': {
        'definition': 'Past tense of rank; arranged in order according to status, quality, or importance; classified in a hierarchy. Ranking provides systematic organization and comparison, whether in academic performance, sports competitions, or organizational structures.',
        'pronunciation': '/ræŋkt/',
        'pronunciation_respelling': 'RANKT',
        'etymology': 'From "rank" + past tense "-ed," from Old French "ranc" (row, line).',
        'memory_tip': 'Think "rank" + "ed" = arranged in ranks or order.',
        'example_sentence': 'The university ___ third in the national survey of educational institutions.',
        'source': 'Claude'
    },
    'rankles': {
        'definition': 'Third person singular of rankle; causes irritation, resentment, or anger; festers like a wound. When something rankles, it creates persistent annoyance or bitterness that continues to cause emotional discomfort over time.',
        'pronunciation': '/ˈræŋkəlz/',
        'pronunciation_respelling': 'RANK-ulz',
        'etymology': 'From Old French "rancler," from "draoncle" (festering sore).',
        'memory_tip': 'Think "rank" + "les" = creates rank/bad feelings that fester.',
        'example_sentence': 'The unfair criticism still ___ him years after the incident occurred.',
        'source': 'Claude'
    },
    'ransacked': {
        'definition': 'Past tense of ransack; searched thoroughly and roughly; plundered or pillaged. Ransacking involves aggressive searching that typically leaves the searched area in disarray, whether by thieves, investigators, or desperate searchers.',
        'pronunciation': '/ˈrænsækt/',
        'pronunciation_respelling': 'RAN-sakt',
        'etymology': 'From Old Norse "rannsaka," meaning "to search a house," from "rann" (house) + "saka" (to seek).',
        'memory_tip': 'Think "ran" + "sacked" = ran through and sacked/destroyed everything.',
        'example_sentence': 'Burglars had ___ the house, leaving drawers open and belongings scattered.',
        'source': 'Claude'
    },
    'ransom': {
        'definition': 'A sum of money demanded for the release of a captive; to obtain release by paying demanded money; the act of freeing someone by payment. Ransom represents exchange of money for freedom, appearing in kidnapping, historical prisoner exchanges, and metaphorical contexts.',
        'pronunciation': '/ˈrænsəm/',
        'pronunciation_respelling': 'RAN-sum',
        'etymology': 'From Old French "raançon," from Latin "redemptio" (buying back).',
        'memory_tip': 'Think "ran" + "some" = ran to get some money to free someone.',
        'example_sentence': 'The kidnappers demanded a million-dollar ___ for the businessman\'s release.',
        'source': 'Claude'
    },
    'ranunculus': {
        'definition': 'A genus of flowering plants in the buttercup family, known for their bright, layered petals and variety of colors; commonly called buttercups. Ranunculus flowers are popular in gardens and floral arrangements due to their full, ruffled appearance and long-lasting blooms.',
        'pronunciation': '/rəˈnʌŋkjələs/',
        'pronunciation_respelling': 'ruh-NUN-kyuh-lus',
        'etymology': 'From Latin "ranunculus," diminutive of "rana" (frog), because they often grow in moist places.',
        'memory_tip': 'Think "ran" + "uncle" + "us" = Uncle Ran\'s colorful garden flowers.',
        'example_sentence': 'The bride\'s bouquet featured white ___ mixed with roses and greenery.',
        'source': 'Claude'
    },
    'rapidly': {
        'definition': 'At a fast rate; quickly and speedily; with great haste or velocity. Rapidly describes actions or changes that occur in short time periods, emphasizing the speed and urgency of processes, movements, or developments.',
        'pronunciation': '/ˈræpɪdli/',
        'pronunciation_respelling': 'RAP-id-lee',
        'etymology': 'From "rapid" + suffix "-ly," from Latin "rapidus" (swift).',
        'memory_tip': 'Think "rapid" + "ly" = in a rapid, fast manner.',
        'example_sentence': 'Technology is advancing ___ in the field of artificial intelligence.',
        'source': 'Claude'
    },
    'rapids': {
        'definition': 'Sections of a river where water flows very fast over rocks; turbulent, fast-moving water in rivers. Rapids create challenging navigation for boats and provide exciting recreational opportunities for whitewater rafting and kayaking enthusiasts.',
        'pronunciation': '/ˈræpɪdz/',
        'pronunciation_respelling': 'RAP-idz',
        'etymology': 'Plural of "rapid," from Latin "rapidus" meaning "swift" or "hurried."',
        'memory_tip': 'Think "rapid" + "s" = multiple sections of rapid-flowing water.',
        'example_sentence': 'The experienced rafting guide navigated the dangerous ___ with expert skill.',
        'source': 'Claude'
    },
    'rapparee': {
        'definition': 'An irregular Irish soldier; a brigand or bandit in 17th-century Ireland; a member of guerrilla forces. Rapparees were often dispossessed Irish Catholics who engaged in irregular warfare against English rule, operating outside conventional military structures.',
        'pronunciation': '/ˌræpəˈriː/',
        'pronunciation_respelling': 'rap-uh-REE',
        'etymology': 'From Irish "rapaire," possibly from "ropaire" (one who wields a rope or noose).',
        'memory_tip': 'Think "rap" + "paree" = rapping (hitting) like an Irish irregular fighter.',
        'example_sentence': 'The ___ used guerrilla tactics against the occupying English forces.',
        'source': 'Claude'
    },
    'rappelled': {
        'definition': 'Past tense of rappel; descended a vertical surface using a rope; performed controlled descent technique. Rappelling is used in rock climbing, military operations, rescue missions, and recreation, requiring proper equipment and technique for safety.',
        'pronunciation': '/ræˈpɛld/',
        'pronunciation_respelling': 'rap-PELD',
        'etymology': 'From French "rappeler," meaning "to recall" or "to pull back."',
        'memory_tip': 'Think "rap" + "pelled" = rapped down using ropes, being pulled back.',
        'example_sentence': 'The rescue team ___ down the cliff face to reach the stranded hikers.',
        'source': 'Claude'
    },
    'rapprochement': {
        'definition': 'The reestablishment of harmonious relations; a coming together or reconciliation between parties previously in conflict. Rapprochement involves diplomatic efforts to restore friendly relations, reduce tensions, and create cooperative relationships after periods of hostility or estrangement.',
        'pronunciation': '/ˌræproʊʃˈmɑːn/',
        'pronunciation_respelling': 'rap-rohsh-MAHN',
        'etymology': 'From French "rapprochement," from "rapprocher" (to bring closer), from "re-" + "approcher" (to approach).',
        'memory_tip': 'Think "rap" + "approach" + "ment" = approaching each other again to make peace.',
        'example_sentence': 'The diplomatic ___ between the two nations ended decades of hostility.',
        'source': 'Claude'
    },
    'rapscallion': {
        'definition': 'A mischievous person, especially a child; a rascal or scamp who engages in playful troublemaking. Rapscallion implies endearing mischief rather than serious wrongdoing, often describing children whose antics are more amusing than harmful.',
        'pronunciation': '/ræpˈskæljən/',
        'pronunciation_respelling': 'rap-SKAL-yun',
        'etymology': 'Alteration of "rascallion," influenced by "rascal," of uncertain origin.',
        'memory_tip': 'Think "rap" + "scallion" = a rascal as sharp and mischievous as an onion.',
        'example_sentence': 'The little ___ had hidden all the cookies before dinner.',
        'source': 'Claude'
    },
    'raptatorial': {
        'definition': 'Relating to or characteristic of birds of prey; adapted for seizing and tearing prey; predatory in nature. Raptatorial features include sharp talons, hooked beaks, and keen eyesight that enable efficient hunting and killing of prey animals.',
        'pronunciation': '/ˌræptəˈtɔːriəl/',
        'pronunciation_respelling': 'rap-tuh-TOR-ee-ul',
        'etymology': 'From Latin "raptor" (seizer) + suffix "-ial," from "rapere" (to seize).',
        'memory_tip': 'Think "raptor" + "ial" = relating to raptors (birds of prey).',
        'example_sentence': 'The eagle\'s ___ claws were perfectly designed for catching fish.',
        'source': 'Claude'
    },
    'rare': {
        'definition': 'Occurring infrequently; unusual or uncommon; of meat, cooked for only a short time; valuable because of scarcity. Rarity creates value and interest, whether in natural phenomena, collectible items, or culinary preferences.',
        'pronunciation': '/rɛr/',
        'pronunciation_respelling': 'RAIR',
        'etymology': 'From Latin "rarus," meaning "thin," "loose," or "uncommon."',
        'memory_tip': 'Think of something so uncommon it\'s like "rarer than air."',
        'example_sentence': 'The ___ butterfly species was spotted only once every few years.',
        'source': 'Claude'
    },
    'rarely': {
        'definition': 'Not often; seldom; infrequently or uncommonly. Rarely indicates low frequency of occurrence, suggesting that events, actions, or conditions happen only occasionally or in exceptional circumstances.',
        'pronunciation': '/ˈrɛrli/',
        'pronunciation_respelling': 'RAIR-lee',
        'etymology': 'From "rare" + suffix "-ly," from Latin "rarus."',
        'memory_tip': 'Think "rare" + "ly" = in a rare manner, not often.',
        'example_sentence': 'She ___ missed a day of work despite the long commute.',
        'source': 'Claude'
    },
    'rascal': {
        'definition': 'A mischievous or playfully dishonest person; a person who behaves badly but in an appealing way; a scamp or rogue. Rascals are often endearing despite their troublemaking, suggesting mischief without malice.',
        'pronunciation': '/ˈræskəl/',
        'pronunciation_respelling': 'RAS-kul',
        'etymology': 'From Old French "rascaille," meaning "rabble" or "dregs of society."',
        'memory_tip': 'Think "rascal" rhymes with "paschal" but is the opposite of holy behavior.',
        'example_sentence': 'The old ___ charmed everyone with his stories and gentle humor.',
        'source': 'Claude'
    }
}

def process_batch_144():
    """Process batch 144 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_144_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_144_processed.csv'
    
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
                        'notes': 'Batch 144 processing',
                        'review_status': 'pending',
                        'batch_number': 144
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
            
            print(f"\nBatch 144 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 144: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_144()