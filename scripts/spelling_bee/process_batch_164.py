#!/usr/bin/env python3

import csv
import os

class DifficultyCalculator:
    def __init__(self):
        self.phonetic_patterns = {
            'silent_letters': ['k', 'w', 'l', 'b', 't', 'h'],
            'irregular_sounds': ['ph', 'gh', 'ough', 'augh', 'eigh'],
            'double_letters': ['ss', 'll', 'tt', 'nn', 'mm', 'pp', 'ff', 'cc', 'dd'],
            'vowel_teams': ['ea', 'oa', 'ie', 'ai', 'ey', 'ay', 'ow', 'ou']
        }
        
        self.morphological_markers = {
            'prefixes': ['un', 'pre', 'dis', 'mis', 'over', 'under', 'sub', 'super', 'anti', 're', 'de', 'ex'],
            'suffixes': ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ous', 'ious', 'ly', 'ing', 'ed', 'er', 'est'],
            'roots': ['spect', 'dict', 'graph', 'phon', 'bio', 'geo', 'auto', 'tele']
        }

    def calculate_phonetic_transparency(self, word):
        score = 0
        word_lower = word.lower()
        
        for pattern in self.phonetic_patterns['silent_letters']:
            if pattern in word_lower and not word_lower.endswith(pattern + 'e'):
                score += 1
                
        for pattern in self.phonetic_patterns['irregular_sounds']:
            if pattern in word_lower:
                score += 2
                
        for pattern in self.phonetic_patterns['double_letters']:
            if pattern in word_lower:
                score += 0.5
                
        return min(score, 5)

    def calculate_word_frequency(self, word):
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
        
        word_lower = word.lower()
        if word_lower in common_words:
            return 1
        elif len(word) <= 4:
            return 2
        elif len(word) <= 6:
            return 3
        elif len(word) <= 8:
            return 4
        else:
            return 5

    def calculate_morphological_complexity(self, word):
        score = 0
        word_lower = word.lower()
        
        prefix_count = sum(1 for prefix in self.morphological_markers['prefixes'] if word_lower.startswith(prefix))
        suffix_count = sum(1 for suffix in self.morphological_markers['suffixes'] if word_lower.endswith(suffix))
        root_count = sum(1 for root in self.morphological_markers['roots'] if root in word_lower)
        
        total_morphemes = prefix_count + suffix_count + root_count
        
        if total_morphemes == 0:
            score = 1
        elif total_morphemes == 1:
            score = 2
        elif total_morphemes == 2:
            score = 3
        elif total_morphemes == 3:
            score = 4
        else:
            score = 5
            
        return score

    def calculate_etymology_complexity(self, word):
        etymology_indicators = {
            'latin': ['tion', 'sion', 'ous', 'ious', 'able', 'ible'],
            'greek': ['ph', 'th', 'ch', 'ps', 'pt', 'rh'],
            'french': ['eau', 'eur', 'oir', 'ique'],
            'german': ['sch', 'tch', 'tz'],
            'other': ['kh', 'gh', 'zh', 'x']
        }
        
        word_lower = word.lower()
        complexity_score = 1
        
        for origin, patterns in etymology_indicators.items():
            for pattern in patterns:
                if pattern in word_lower:
                    if origin in ['greek', 'other']:
                        complexity_score += 2
                    elif origin in ['french', 'german']:
                        complexity_score += 1.5
                    else:
                        complexity_score += 1
                    break
                    
        return min(complexity_score, 5)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'output', 'batch_164_words.csv')
    output_file = os.path.join(script_dir, 'output', 'batch_164_processed.csv')
    
    calculator = DifficultyCalculator()
    
    # Comprehensive word data with educational content
    word_data = {
        'sommelier': {
            'definition': 'A sommelier is a trained wine professional who specializes in all aspects of wine service, including wine selection, wine and food pairing, wine presentation, and wine storage. These experts possess extensive knowledge of wine regions, grape varieties, vintages, and production methods, often holding certifications from recognized wine education organizations. Sommeliers work in upscale restaurants, hotels, wine shops, and other hospitality establishments where they guide customers in choosing appropriate wines for their preferences and budget. Their expertise extends beyond wine to include knowledge of beer, spirits, sake, and other beverages. The profession requires continuous education as wine regions and styles evolve, and top sommeliers are respected for their refined palates and deep understanding of wine culture.',
            'pronunciation': '/ˌsʌməlˈjeɪ/',
            'example_sentence': 'The restaurant\'s _____ recommended a perfect wine pairing that enhanced both the meal and the dining experience.',
            'etymology': 'From French "sommelier," originally meaning "court official in charge of transportation supplies," later applied to wine stewards.',
            'mnemonic': 'Think "SOMM-ELIER = SOMe of the Most knowledgeable, Making Every wine pairing great, Loves wine, Including Every variety, Expertly Recommending selections" - wine expert and advisor.',
            'source': 'Claude'
        },
        'somniloquy': {
            'definition': 'Somniloquy is the formal medical term for sleep talking, a sleep disorder where individuals speak, mumble, or make sounds while asleep without being consciously aware of their vocalizations. This relatively common phenomenon can range from simple sounds and mumbling to clear, coherent speech, and may occur during any stage of sleep. Sleep talking episodes can last from a few seconds to several minutes and may involve the person responding to dreams or unconscious thoughts. While generally harmless, somniloquy can sometimes disturb sleep partners or indicate underlying sleep disorders. The content of sleep talk often reflects current concerns, memories, or dream content, though it should not be considered reliable or meaningful communication.',
            'pronunciation': '/sɑmˈnɪləkwi/',
            'example_sentence': 'Her frequent _____ during the night kept her roommate awake with unexpected conversations.',
            'etymology': 'From Latin "somnus" (sleep) + "loqui" (to speak), literally meaning "sleep speaking."',
            'mnemonic': 'Think "SOMNI-LOQUY = SOMNus (sleep) plus LoQUacious talking, Including vocal sounds while asleep" - talking while sleeping.',
            'source': 'Claude'
        },
        'somnolent': {
            'definition': 'Somnolent describes a state of drowsiness, sleepiness, or inclination toward sleep, characterized by reduced alertness, heavy eyelids, and difficulty maintaining wakefulness. This adjective applies to both people experiencing natural tiredness and situations that induce sleepiness, such as warm environments, boring activities, or post-meal lethargy. Somnolent conditions can result from various factors including insufficient sleep, medication side effects, medical conditions, or circadian rhythm disruptions. The term suggests a peaceful, gentle drowsiness rather than exhaustion or pathological sleepiness. Understanding somnolence is important for recognizing when rest is needed and for identifying potentially dangerous situations like drowsy driving.',
            'pronunciation': '/ˈsɑmnələnt/',
            'example_sentence': 'The warm afternoon sun and gentle breeze made the students increasingly _____ during the outdoor lecture.',
            'etymology': 'From Latin "somnolentus," from "somnus" (sleep), meaning "inclined to sleep" or "drowsy."',
            'mnemonic': 'Think "SOMNO-LENT = SOMNus (sleep) feeling, Obviously drowsy, Making someone sleepy, Nearly asleep, Obviously tired, Lethargic and drowsy, Everyone feels heavy eyelids, Nearly unconscious, Tired" - feeling very drowsy.',
            'source': 'Claude'
        },
        'sonar': {
            'definition': 'Sonar is a technology that uses sound waves to detect, locate, and identify objects underwater or to measure distances and depths in aquatic environments. The system works by emitting acoustic signals and analyzing the echoes that bounce back from objects, allowing operators to create detailed images of underwater terrain, locate submarines, find schools of fish, or navigate safely in murky waters. Sonar technology has military applications for submarine detection, civilian uses for fishing and navigation, and scientific applications for ocean exploration and marine research. The term encompasses both active sonar (which transmits sounds) and passive sonar (which only listens for sounds made by other sources).',
            'pronunciation': '/ˈsoʊnɑr/',
            'example_sentence': 'The submarine used _____ to navigate through the dark ocean depths and avoid underwater obstacles.',
            'etymology': 'Acronym from "SOund Navigation And Ranging," coined during World War II for underwater detection technology.',
            'mnemonic': 'Think "SONAR = SOund Navigation And Ranging system" - sound-based detection and navigation technology.',
            'source': 'Claude'
        },
        'songbird': {
            'definition': 'A songbird is a bird belonging to the suborder Passeri (passerines), characterized by their ability to produce complex, melodious vocalizations often used for communication, territory establishment, and mate attraction. These birds possess specialized vocal organs called syringes that allow them to create intricate songs with multiple notes, rhythms, and patterns. Common songbirds include robins, cardinals, wrens, and finches, each species having distinctive songs that serve various social and biological functions. Songbirds play important ecological roles as insect controllers and seed dispersers, while their music has inspired human culture throughout history. Many songbird populations face challenges from habitat loss, requiring conservation efforts to protect these melodious creatures.',
            'pronunciation': '/ˈsɔŋˌbɜrd/',
            'example_sentence': 'The morning chorus of each _____ species created a natural symphony in the garden.',
            'etymology': 'Compound word from "song" + "bird," referring to birds known for their melodious vocalizations.',
            'mnemonic': 'Think "SONG-BIRD = SONG-making BIRD with melodious voice" - bird that sings beautifully.',
            'source': 'Claude'
        },
        'soon': {
            'definition': 'Soon is an adverb indicating that something will happen in the near future, within a short period of time, or earlier than might otherwise be expected. This temporal reference provides a sense of immediacy without specifying exact timing, making it useful for expressing anticipation, urgency, or proximity in time. The interpretation of "soon" depends on context - it might mean minutes in emergency situations, days in business contexts, or weeks in long-term planning. The word helps communicate expectations about timing while maintaining flexibility about precise schedules. Understanding how to use "soon" appropriately is important for managing expectations and expressing time relationships effectively.',
            'pronunciation': '/sun/',
            'example_sentence': 'The storm clouds suggested that rain would arrive _____, so they decided to head indoors.',
            'etymology': 'From Old English "sōna," meaning "immediately" or "at once," related to "sooner."',
            'mnemonic': 'Think "SOON = Something will happen Ordinarily in near future, Obviously Not far away" - in the near future.',
            'source': 'Claude'
        },
        'soothsayer': {
            'definition': 'A soothsayer is a person who claims to have the ability to predict future events or reveal hidden truths through supernatural means, divination, or prophetic insight. Historically, soothsayers served important roles in ancient civilizations, advising rulers and interpreting omens through various methods including reading animal entrails, observing celestial patterns, or consulting oracles. The term combines "sooth" (truth) with "sayer" (one who speaks), literally meaning "truth-teller." While modern science generally dismisses supernatural prediction, the concept of soothsaying persists in various forms including fortune telling, astrology, and psychic readings. The word often appears in historical, literary, or cultural contexts discussing ancient practices and beliefs.',
            'pronunciation': '/ˈsuθˌseɪər/',
            'example_sentence': 'The ancient king consulted his trusted _____ before making important decisions about war and peace.',
            'etymology': 'From Middle English, combining "sooth" (truth) + "sayer" (one who speaks), meaning "truth-teller."',
            'mnemonic': 'Think "SOOTH-SAYER = SOOTH (truth) SAYER who speaks truth about future events" - one who predicts the future.',
            'source': 'Claude'
        },
        'sopapilla': {
            'definition': 'A sopapilla is a traditional fried pastry popular in Mexican, New Mexican, and southwestern United States cuisine, made from simple dough that puffs up when deep-fried to create a light, airy texture with a crispy exterior. These golden, pillowy pastries are typically served warm and can be enjoyed as either a sweet dessert drizzled with honey or cinnamon sugar, or as a savory accompaniment to meals. The dough usually contains flour, baking powder, salt, and shortening, rolled thin and cut into squares or triangles before frying. Sopapillas hold cultural significance in southwestern cuisine and are often featured at traditional celebrations, family gatherings, and Mexican restaurants throughout the American Southwest.',
            'pronunciation': '/ˌsoʊpəˈpijə/',
            'example_sentence': 'The restaurant served warm _____ with honey for dessert, their golden puffed exterior giving way to a soft, airy interior.',
            'etymology': 'From Spanish "sopaipilla," possibly from "sopaipa" (a type of fried bread) + diminutive suffix "-illa."',
            'mnemonic': 'Think "SOPA-PILLA = SOft Pastry that Puffs up, Always fried, Perfectly golden, Including honey, Light and airy, Loved in southwest America" - fried puffy pastry.',
            'source': 'Claude'
        },
        'sophisticated': {
            'definition': 'Sophisticated describes something or someone that is complex, refined, worldly, or having advanced knowledge and understanding of culture, technology, or social situations. When applied to people, it suggests education, elegance, and familiarity with refined tastes and social conventions. Sophisticated technology or systems are advanced, complex, and highly developed. The term can describe art, literature, or ideas that demonstrate depth, nuance, and intellectual complexity. While often carrying positive connotations of refinement and advancement, sophisticated can sometimes suggest artificiality or excessive complexity. The word implies a level of development, knowledge, or cultivation that goes beyond basic or simple forms.',
            'pronunciation': '/səˈfɪstɪˌkeɪtɪd/',
            'example_sentence': 'The museum\'s _____ security system used advanced technology to protect its priceless art collection.',
            'etymology': 'From Latin "sophisticatus," past participle of "sophisticare" (to tamper with, adulterate), later meaning "to make complex."',
            'mnemonic': 'Think "SOPHISTI-CATED = SOPHisticated thinking, Including Complexity, Advanced Technology, Everyone Developed in knowledge" - complex and refined.',
            'source': 'Claude'
        },
        'sophomoric': {
            'definition': 'Sophomoric describes behavior, ideas, or attitudes that are immature, pretentious, or overconfident in a way that reveals lack of real knowledge or wisdom, particularly characteristic of someone who knows just enough to be dangerous but not enough to be truly informed. The term originally related to second-year students (sophomores) who had gained some knowledge but might overestimate their understanding. Sophomoric behavior often involves intellectual arrogance, shallow thinking presented as profound insight, or juvenile humor in inappropriate contexts. The word suggests a particularly annoying form of immaturity that combines ignorance with false confidence, making it more problematic than simple naivety or honest inexperience.',
            'pronunciation': '/ˌsɑfəˈmɔrɪk/',
            'example_sentence': 'His _____ remarks during the serious meeting revealed his lack of understanding about the complex issues.',
            'etymology': 'From "sophomore" (second-year student) + "-ic," referring to the perceived arrogance of students with partial knowledge.',
            'mnemonic': 'Think "SOPHO-MORIC = SOPHomore attitude, Only partial knowledge, Making Overconfident Remarks, Immature Comments" - immature and overconfident.',
            'source': 'Claude'
        },
        'soporific': {
            'definition': 'Soporific describes something that tends to induce drowsiness or sleep, whether intentionally (like sleep medications) or unintentionally (like boring lectures or warm environments). This adjective can apply to substances, activities, environments, or presentations that have sleep-inducing effects. Medical soporifics include sedatives and sleep aids designed to help people fall asleep, while everyday soporifics might include warm milk, comfortable temperatures, or monotonous activities. The term often carries mild negative connotations when describing unintentionally boring content that puts audiences to sleep. Understanding soporific effects is important for both therapeutic applications and for recognizing when activities or environments might impair alertness.',
            'pronunciation': '/ˌsɑpəˈrɪfɪk/',
            'example_sentence': 'The professor\'s monotone delivery had a _____ effect that left half the class struggling to stay awake.',
            'etymology': 'From Latin "soporificus," from "sopor" (deep sleep) + "facere" (to make), meaning "sleep-making."',
            'mnemonic': 'Think "SOPOR-IFIC = SOPOR (sleep) making, Including sleep effects, FICient at causing drowsiness" - causing sleepiness.',
            'source': 'Claude'
        },
        'soppiness': {
            'definition': 'Soppiness refers to the quality of being overly sentimental, maudlin, or emotionally excessive in a way that seems insincere, childish, or inappropriately dramatic. This characteristic involves displaying emotions that appear exaggerated, self-indulgent, or lacking genuine depth, often evoking eye-rolling or impatience from observers. Soppy behavior might include excessive crying over minor issues, overly romantic gestures that seem contrived, or sentimental expressions that feel forced or artificial. While genuine emotion is valuable, soppiness suggests emotional expression that has crossed the line into melodrama or manipulation. The term carries distinctly negative connotations, implying that the emotional display is somehow inauthentic or disproportionate to circumstances.',
            'pronunciation': '/ˈsɑpɪnəs/',
            'example_sentence': 'The movie\'s excessive _____ made it difficult to take the romantic storyline seriously.',
            'etymology': 'From "soppy" (overly sentimental) + "-ness" suffix, where "soppy" comes from "sop" (something soaked).',
            'mnemonic': 'Think "SOPP-INESS = SOPPy emotions, Including excessive sentiments, Not genuine reactions, Everyone rolls eyes, Sentimental overdone" - overly sentimental quality.',
            'source': 'Claude'
        },
        'soppinesssousaphone': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "soppiness" and "sousaphone." Soppiness refers to overly sentimental or maudlin behavior. A sousaphone is a large brass musical instrument similar to a tuba, designed to be worn around the player\'s body for marching bands. These are completely unrelated concepts - one describing emotional behavior and the other describing a musical instrument. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/ˈsɑpɪnəs ˈsuzəˌfoʊn/',
            'example_sentence': 'The romantic movie\'s _____ was almost as overwhelming as the marching band\'s _____ during the halftime show.',
            'etymology': 'Soppiness: from "soppy" + "-ness." Sousaphone: named after John Philip Sousa, American composer and bandleader.',
            'mnemonic': 'Remember these as TWO words: SOPPINESS (excessive sentimentality) + SOUSAPHONE (large brass instrument).',
            'source': 'Claude'
        },
        'soprano': {
            'definition': 'Soprano refers to the highest female voice type in classical music, characterized by the ability to sing notes in the upper vocal range, typically from middle C to high C and beyond. This voice classification encompasses various subtypes including coloratura soprano (featuring agility and high notes), lyric soprano (emphasizing beauty and expressiveness), and dramatic soprano (powerful voice for intense roles). Sopranos often perform leading roles in operas, oratorios, and choral works, with their voices cutting through orchestral accompaniment due to their high pitch and bright timbre. The term also applies to male singers who sing in the soprano range, typically young boys before their voices change, or adult male countertenors using falsetto technique.',
            'pronunciation': '/səˈprɑnoʊ/',
            'example_sentence': 'The opera\'s lead _____ delivered a breathtaking performance that brought the audience to tears.',
            'etymology': 'From Italian "soprano," from "sopra" (above), referring to the highest voice part above other vocal ranges.',
            'mnemonic': 'Think "SOPRANO = SOPRa (above) voice, Above all other voices, Never lower, Outstanding high notes" - highest female voice type.',
            'source': 'Claude'
        },
        'sorbet': {
            'definition': 'Sorbet is a frozen dessert made primarily from water, sugar, and fruit juice or puree, creating a smooth, refreshing treat that is typically dairy-free and lighter than ice cream. This elegant dessert originated in the Middle East and became popular in European cuisine, where it was often served between courses to cleanse the palate. Modern sorbets come in numerous flavors including lemon, raspberry, mango, and exotic fruit combinations, and may include herbs, wine, or liqueurs for sophisticated variations. The texture should be smooth and scoopable, achieved through proper sugar balance and sometimes the addition of stabilizers. Sorbet appeals to those seeking lighter desserts or those with dietary restrictions avoiding dairy products.',
            'pronunciation': '/ˈsɔrbət/',
            'example_sentence': 'The restaurant served a refreshing lemon _____ between courses to cleanse diners\' palates.',
            'etymology': 'From French "sorbet," from Turkish "şerbet," from Arabic "sharab" (drink), referring to sweetened beverages.',
            'mnemonic': 'Think "SORBET = Sweet, Original frozen treat, Refreshing and light, Based on fruit, Everyone enjoys, Totally dairy-free" - frozen fruit dessert.',
            'source': 'Claude'
        },
        'sorghum': {
            'definition': 'Sorghum is a versatile cereal grain crop belonging to the grass family, grown primarily in arid and semi-arid regions due to its exceptional drought tolerance and adaptability to harsh growing conditions. This nutritious grain serves multiple purposes: as animal feed, human food (particularly in Africa and parts of Asia), and raw material for products like syrup, ethanol biofuel, and building materials. Sorghum varieties include grain sorghum for food and feed, sweet sorghum for syrup and biofuel production, and forage sorghum for animal grazing. The crop\'s ability to thrive in low-water conditions makes it increasingly important for food security in regions affected by climate change. Sorghum is naturally gluten-free, making it valuable for people with celiac disease.',
            'pronunciation': '/ˈsɔrɡəm/',
            'example_sentence': 'Farmers in drought-prone regions increasingly planted _____ because of its ability to produce grain with minimal water.',
            'etymology': 'From Italian "sorgo," possibly from Arabic "durra," referring to the grain crop.',
            'mnemonic': 'Think "SORGHUM = Sturdy grain, Outstanding drought tolerance, Really Good for dry areas, Growing Healthy crops, Useful for Multiple purposes" - drought-resistant grain crop.',
            'source': 'Claude'
        },
        'sororal': {
            'definition': 'Sororal means relating to or characteristic of sisters or the relationship between sisters, describing the bonds, behaviors, or qualities associated with sisterhood. This adjective captures the unique dynamics of female sibling relationships, including shared experiences, mutual support, competition, and lifelong connections that develop between sisters. Sororal relationships often involve deep emotional bonds, protective instincts, and complex interactions that combine love with rivalry. The term appears in anthropological and sociological contexts when discussing family structures, kinship patterns, and gender dynamics within families. Understanding sororal relationships helps explain family dynamics and the significant influence sisters have on each other\'s development, values, and life choices.',
            'pronunciation': '/səˈrɔrəl/',
            'example_sentence': 'The _____ bond between the twins was evident in their synchronized gestures and protective attitudes toward each other.',
            'etymology': 'From Latin "soror" (sister) + "-al" suffix, meaning "relating to sisters."',
            'mnemonic': 'Think "SOROR-AL = SORORity of sisters, Always Living together, Relating to sisterhood" - relating to sisters.',
            'source': 'Claude'
        },
        'sororalepideictic': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "sororal" and "epideictic." Sororal relates to sisters or sisterhood. Epideictic refers to a type of rhetoric or speech that praises or blames, often used in ceremonial contexts like eulogies or award presentations. These are completely unrelated concepts - one from family relationships and the other from rhetorical theory. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/səˈrɔrəl ˌɛpɪˈdaɪktɪk/',
            'example_sentence': 'The _____ relationship between the sisters was celebrated in an _____ speech praising their mutual achievements.',
            'etymology': 'Sororal: from Latin "soror" (sister). Epideictic: from Greek "epideixis" (display, demonstration).',
            'mnemonic': 'Remember these as TWO words: SORORAL (relating to sisters) + EPIDEICTIC (ceremonial rhetoric).',
            'source': 'Claude'
        },
        'sorrel': {
            'definition': 'Sorrel refers to several plants in the genus Rumex, known for their distinctive sour taste due to oxalic acid content, commonly used as culinary herbs or leafy vegetables in various cuisines worldwide. The most common varieties include garden sorrel and French sorrel, which have bright, tangy flavors that add acidity to salads, soups, and sauces. Sorrel leaves are rich in vitamins A and C, though they should be consumed in moderation due to oxalic acid content. The term also describes a reddish-brown color, particularly when referring to horse coat colors. Wild sorrel species grow as weeds in many regions, while cultivated varieties are grown specifically for culinary use in herb gardens and specialty farming operations.',
            'pronunciation': '/ˈsɔrəl/',
            'example_sentence': 'The chef added fresh _____ leaves to the soup, providing a bright, lemony tartness that balanced the rich flavors.',
            'etymology': 'From Old French "surele," diminutive of "sur" (sour), referring to the plant\'s tart taste.',
            'mnemonic': 'Think "SORREL = SOuR plant, Really Edible Leaves that taste tart" - sour-tasting leafy plant.',
            'source': 'Claude'
        },
        'sorry': {
            'definition': 'Sorry is an expression of regret, apology, or sympathy used to acknowledge wrongdoing, express remorse, or show compassion for others\' misfortunes. As an apology, sorry indicates recognition that one\'s actions or words have caused harm, inconvenience, or offense, serving as a first step toward reconciliation and repair of relationships. The word can also express sympathy or compassion, as in "I\'m sorry for your loss." The sincerity and appropriateness of apologies affect their effectiveness in resolving conflicts and maintaining social harmony. Understanding when and how to apologize properly is crucial for healthy relationships and social interaction, though the meaning and expectations around apologies vary across cultures.',
            'pronunciation': '/ˈsɔri/',
            'example_sentence': 'She felt genuinely _____ about missing her friend\'s important presentation due to the scheduling conflict.',
            'etymology': 'From Old English "sārig," meaning "grieved" or "distressed," related to "sore."',
            'mnemonic': 'Think "SORRY = Sincerely Offering Regret, Recognizing Your mistake" - expressing regret or apology.',
            'source': 'Claude'
        },
        'sortition': {
            'definition': 'Sortition is a method of selecting decision-makers or officials through random drawing or lottery rather than through elections or appointments, used historically in ancient Athens and various other democratic systems. This selection process aims to ensure that representatives come from all segments of society rather than just those wealthy or politically connected enough to run successful campaigns. Modern applications of sortition include jury selection, some citizen assemblies, and certain government advisory bodies. Proponents argue that sortition can reduce corruption, increase diversity, and provide more representative governance, while critics question whether randomly selected individuals have necessary qualifications for complex decision-making. The method offers an alternative to traditional electoral democracy.',
            'pronunciation': '/sɔrˈtɪʃən/',
            'example_sentence': 'The ancient Athenian democracy used _____ to select many government officials, ensuring broad participation in governance.',
            'etymology': 'From Latin "sortitio," from "sortiri" (to draw lots), meaning "selection by lot."',
            'mnemonic': 'Think "SORT-ITION = SORTing by random selection, Including Everyone, Taking turns through lottery, Involving random drawing, Officials chosen by chance, Never by election" - selection by random drawing.',
            'source': 'Claude'
        },
        'sostenuto': {
            'definition': 'Sostenuto is a musical term indicating that notes should be played in a sustained, smooth manner, maintaining their full duration without rushing or clipping the sound. This Italian direction appears in musical scores to instruct performers to hold notes for their complete time value while maintaining a connected, flowing style. Sostenuto differs from legato (which emphasizes smooth connection between notes) by specifically focusing on sustaining individual note durations. The technique is particularly important for melodic lines where the composer wants to ensure notes receive their full rhythmic value and emotional weight. Many pianos feature a sostenuto pedal that allows selective sustaining of certain notes while others remain unaffected.',
            'pronunciation': '/ˌsɔstəˈnuto/',
            'example_sentence': 'The pianist carefully observed the _____ marking, ensuring each note received its full duration for maximum emotional impact.',
            'etymology': 'From Italian "sostenuto," past participle of "sostenere" (to sustain), meaning "sustained."',
            'mnemonic': 'Think "SOSTEN-UTO = SOSTain Each Note, Using Time Optimally, Not rushed, Understanding sustained sound, Taking time for full notes, Only sustained playing" - sustained musical style.',
            'source': 'Claude'
        },
        'sotto': {
            'definition': 'Sotto is an Italian musical term meaning "under" or "below," most commonly encountered in the phrase "sotto voce," which instructs performers to sing or speak in an undertone, quietly, or in a subdued manner. This direction indicates that the passage should be performed with reduced volume and intensity, often to create intimate, secretive, or mysterious effects. In musical contexts, sotto voce passages require careful control to maintain audibility while achieving the desired soft dynamic. The term can also appear in other Italian musical directions where the concept of "under" or "below" applies to tempo, dynamics, or other performance aspects. Understanding sotto markings is essential for proper interpretation of classical music.',
            'pronunciation': '/ˈsɔtoʊ/',
            'example_sentence': 'The composer marked the mysterious passage "_____ voce" to create an atmosphere of whispered secrets.',
            'etymology': 'From Italian "sotto," from Latin "subtus," meaning "under" or "below."',
            'mnemonic': 'Think "SOTTO = Soft, Only quiet volumes, Totally Toned down, Organs of voice whisper" - quietly or under (in music).',
            'source': 'Claude'
        },
        'souchong': {
            'definition': 'Souchong is a category of black tea characterized by large, bold leaves that produce a robust, full-bodied brew with distinctive smoky or malty flavors. The term originally described teas from the Fujian province of China, where traditional processing methods created teas with unique characteristics. Lapsang Souchong, the most famous variety, is smoke-dried over pine fires, giving it a distinctive smoky aroma and flavor that\'s either loved or disliked by tea drinkers. Other souchong varieties may have malty, fruity, or earthy notes depending on processing methods and growing conditions. These teas typically withstand multiple infusions and pair well with hearty foods, making them popular choices for breakfast teas and afternoon drinking.',
            'pronunciation': '/ˈsuˌʃɔŋ/',
            'example_sentence': 'The tea connoisseur preferred Lapsang _____ for its distinctive smoky flavor that reminded him of campfires.',
            'etymology': 'From Chinese "xiaozhong," meaning "small variety," referring to a specific type of tea processing.',
            'mnemonic': 'Think "SOU-CHONG = Smoky flavored tea, Outstanding Chinese tea, Unique processing, CHaracteristic flavor, Heavy Oxidized leaves, Notable smoky taste, Great for breakfast" - bold, smoky Chinese black tea.',
            'source': 'Claude'
        },
        'sound': {
            'definition': 'Sound functions as both a noun referring to vibrations that travel through the air or other medium and can be heard when they reach the ear, and as an adjective meaning healthy, solid, reliable, or well-founded. As a physical phenomenon, sound involves pressure waves that carry information about their source, enabling communication, music, and environmental awareness. As an adjective, sound describes things that are structurally solid, logically valid, or in good condition. Sound can also function as a verb meaning to make noise, to seem or appear, or to measure depth. The versatility of this word makes it fundamental to discussions of physics, health, logic, and sensory experience.',
            'pronunciation': '/saʊnd/',
            'example_sentence': 'The structural engineer confirmed that the building\'s foundation was _____ and could support the planned addition.',
            'etymology': 'From Old English "sund" (healthy, whole) and Old French "son" (noise), with meanings converging in Middle English.',
            'mnemonic': 'Think "SOUND = Solid and reliable, Or vibrations heard, Usually good quality, Not broken, Dependable" - vibrations heard or reliable quality.',
            'source': 'Claude'
        },
        'soundboard': {
            'definition': 'A soundboard is a thin, resonant wooden surface on musical instruments like pianos, guitars, and violins that amplifies and shapes the sound produced by vibrating strings or other sound sources. This crucial component transfers energy from the strings to the surrounding air, significantly affecting the instrument\'s tone, volume, and projection. Soundboards are typically made from carefully selected woods like spruce or cedar, chosen for their acoustic properties and ability to vibrate freely. The term also refers to mixing consoles used in recording studios and live performances to control and balance multiple audio sources. In digital contexts, soundboards are collections of audio clips that can be triggered for entertainment or practical purposes.',
            'pronunciation': '/ˈsaʊndˌbɔrd/',
            'example_sentence': 'The piano\'s cracked _____ needed restoration to bring back the instrument\'s rich, resonant tone.',
            'etymology': 'Compound word from "sound" + "board," referring to the board that produces or controls sound.',
            'mnemonic': 'Think "SOUND-BOARD = SOUND amplifying BOARD, Only makes sound better, Usually wooden, Not silent, Designed for resonance" - surface that amplifies sound.',
            'source': 'Claude'
        },
        'sounded': {
            'definition': 'Sounded is the past tense of "sound," with multiple meanings depending on context: it can mean that something made a noise or was heard, that something appeared or seemed a certain way when heard, or that depth was measured using a sounding device. In acoustic contexts, sounded indicates that a noise was produced or perceived. When describing impressions, sounded refers to how something appeared based on what was heard, such as "it sounded angry" or "sounded promising." In nautical contexts, sounded means depth was measured using sonar or other depth-finding equipment. The word captures both the production and perception of sound across various applications.',
            'pronunciation': '/ˈsaʊndəd/',
            'example_sentence': 'The warning bell _____ throughout the building, alerting everyone to evacuate immediately.',
            'etymology': 'Past tense of "sound," from Old English "sundian" (to make sound) and Old French "soner" (to ring).',
            'mnemonic': 'Think "SOUND-ED = SOUND was produced, Everyone heard it, Detected by ears" - made a sound or seemed a certain way.',
            'source': 'Claude'
        },
        'sounds': {
            'definition': 'Sounds functions as both the plural noun form of "sound" (referring to multiple auditory vibrations or noises) and the third-person singular present tense of the verb "sound" (meaning to produce noise, seem, or appear). As a noun, sounds encompass all the various noises, tones, and acoustic phenomena that we perceive through hearing, from music and speech to environmental noises and mechanical sounds. As a verb, sounds describes how something appears or seems when heard, such as "that sounds good" or "sounds reasonable." The word is fundamental to communication about auditory experiences and impressions based on what we hear.',
            'pronunciation': '/saʊndz/',
            'example_sentence': 'The forest was full of natural _____ including bird calls, rustling leaves, and flowing water.',
            'etymology': 'Plural/verb form of "sound," from Old English and Old French origins meaning audible vibrations.',
            'mnemonic': 'Think "SOUNDS = Several auditory vibrations, Or something that Ultimately seems reasonable, Not silent, Detected by ears, Surely audible" - multiple noises or seems to be.',
            'source': 'Claude'
        },
        'soup': {
            'definition': 'Soup is a liquid dish typically made by combining water or stock with various ingredients such as vegetables, meat, grains, or legumes, cooked together to create a nutritious and flavorful meal. This versatile food category includes countless varieties from clear broths and cream-based soups to thick stews and cold preparations like gazpacho. Soups serve important cultural and nutritional functions, providing warmth, comfort, and an efficient way to consume multiple food groups in a single dish. They can be light appetizers or hearty main courses, and many cultures have traditional soup recipes that reflect local ingredients and cooking methods. The cooking process allows flavors to meld and ingredients to become tender and digestible.',
            'pronunciation': '/sup/',
            'example_sentence': 'The homemade chicken _____ helped her recover from the cold with its warm, comforting broth.',
            'etymology': 'From Old French "soupe," from a Germanic source meaning "bread soaked in broth."',
            'mnemonic': 'Think "SOUP = Several ingredients cooking, Often warm, Usually liquid, Perfect for cold days" - liquid dish with mixed ingredients.',
            'source': 'Claude'
        },
        'soupçon': {
            'definition': 'Soupçon is a French culinary term meaning a very small amount or hint of something, typically used to describe the addition of a subtle flavoring, spice, or ingredient that enhances a dish without dominating it. This sophisticated cooking concept emphasizes restraint and precision, where just a tiny amount of an ingredient can transform the overall flavor profile. In broader usage, soupçon can describe any small trace or suggestion of a quality, emotion, or characteristic. The term reflects the French culinary philosophy that values subtle, nuanced flavors over heavy-handed seasoning. Understanding the concept of soupçon is important for developing refined cooking skills and appreciating delicate flavor combinations.',
            'pronunciation': '/supˈsɔn/',
            'example_sentence': 'The chef added just a _____ of truffle oil to the pasta, providing subtle luxury without overwhelming the delicate flavors.',
            'etymology': 'From French "soupçon," literally meaning "suspicion," referring to a barely detectable amount.',
            'mnemonic': 'Think "SOUP-ÇON = Small Uptake, One tiny bit, Usually just a hint, Perfectly measured small amount, Çulinary ONly needs a trace" - very small amount.',
            'source': 'Claude'
        },
        'source': {
            'definition': 'Source refers to the origin, starting point, or provider of something, whether information, materials, energy, or other resources. In research and journalism, sources are the people, documents, or references that provide information or evidence. In geography, a source is the starting point of a river or stream. For energy, sources include the sun, fossil fuels, or other power origins. Understanding and identifying sources is crucial for verifying information reliability, tracing supply chains, and making informed decisions. The concept emphasizes the importance of knowing where things come from, whether for academic credibility, quality control, or environmental responsibility. Reliable sources form the foundation of trustworthy knowledge and effective problem-solving.',
            'pronunciation': '/sɔrs/',
            'example_sentence': 'The journalist carefully verified each _____ before publishing the investigative report.',
            'etymology': 'From Old French "sorse," from Latin "surgere" (to rise), referring to the rising or beginning of something.',
            'mnemonic': 'Think "SOURCE = Starting Origin, Usually where it begins, Reliable Credible provider, Everything\'s beginning" - origin or provider.',
            'source': 'Claude'
        },
        'sourcrout': {
            'definition': 'Sourcrout appears to be a misspelling of "sauerkraut," which is a fermented cabbage dish popular in German cuisine and throughout Central Europe. Sauerkraut is made by finely shredding fresh cabbage and fermenting it with salt, creating a tangy, sour flavor and preserving the vegetable for long-term storage. This traditional food preparation method not only extends shelf life but also creates beneficial probiotics that support digestive health. Sauerkraut is commonly served as a side dish with sausages, pork, or other hearty meals, and its distinctive sour taste comes from lactic acid produced during fermentation. The correct spelling emphasizes its German origins where "sauer" means sour and "kraut" means cabbage.',
            'pronunciation': '/ˈsaʊərˌkraʊt/',
            'example_sentence': 'The German restaurant served traditional _____ alongside bratwurst and mustard.',
            'etymology': 'Appears to be misspelling of "sauerkraut," from German "sauer" (sour) + "kraut" (cabbage).',
            'mnemonic': 'Think "SOUR-CROUT = SOUR fermented cabbage, Correctly spelled sauerkraut, Really Outstanding fermented food, Usually tangy, Traditional German food" - fermented cabbage (misspelled).',
            'source': 'Claude'
        },
        'souris': {
            'definition': 'Souris is French for "mouse," referring to the small rodent known for its quick movements, small size, and ability to squeeze through tiny spaces. In French cuisine, souris can also refer to the "mouse" of lamb, a small, tender cut of meat from the shank area that resembles a mouse in shape when prepared. The word appears in various French expressions and contexts, and may be encountered in English when discussing French language, cuisine, or culture. Understanding basic French vocabulary like souris helps in appreciating French cultural references, culinary terms, and language learning. The term exemplifies how animal names often have both literal and culinary applications in French.',
            'pronunciation': '/suˈri/',
            'example_sentence': 'The French children\'s book featured a clever little _____ who outwitted the cat.',
            'etymology': 'From Old French "soris," from Latin "sorex" (shrew), later applied to mice.',
            'mnemonic': 'Think "SOURIS = Small creature, Often quiet, Usually running, Really tiny, In French means mouse, Small rodent" - French word for mouse.',
            'source': 'Claude'
        },
        'sourisadjective': {
            'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly combined: "souris" and "adjective." Souris is French for "mouse," referring to the small rodent. An adjective is a word that describes or modifies nouns and pronouns, providing additional information about qualities, characteristics, or attributes. These are completely unrelated concepts - one being a French noun for an animal and the other being a grammatical term. The error likely occurred during document scanning or data processing where spacing between words was lost.',
            'pronunciation': '/suˈri ˈædʒɪktɪv/',
            'example_sentence': 'The word _____ (mouse) in French can be modified by an _____ like "petit" (small).',
            'etymology': 'Souris: from Latin "sorex" (shrew). Adjective: from Latin "adjectivum" (added word).',
            'mnemonic': 'Remember these as TWO words: SOURIS (French for mouse) + ADJECTIVE (descriptive word).',
            'source': 'Claude'
        },
        'sourkrout': {
            'definition': 'Sourkrout appears to be another misspelling of "sauerkraut," the traditional German fermented cabbage dish known for its tangy, sour flavor and probiotic benefits. Sauerkraut is prepared by finely shredding fresh cabbage and allowing it to ferment with salt, creating lactic acid that gives the characteristic sour taste while preserving the vegetable. This ancient preservation method was historically important for providing vitamin C during long sea voyages and harsh winters. The fermentation process creates beneficial bacteria that support digestive health. Proper sauerkraut is crisp, tangy, and slightly salty, commonly served with German dishes like bratwurst, schnitzel, or sauerbraten. The correct spelling reflects its German heritage.',
            'pronunciation': '/ˈsaʊərˌkraʊt/',
            'example_sentence': 'The delicatessen offered fresh homemade _____ made from locally grown cabbage.',
            'etymology': 'Misspelling of "sauerkraut," from German "sauer" (sour) + "kraut" (cabbage).',
            'mnemonic': 'Think "SOUR-KROUT = SOUR fermented cabbage, Keep spelling as sauerkraut, Really Outstanding fermented food, Often with sausages, Usually tangy, Traditional preservation method" - fermented cabbage (misspelled).',
            'source': 'Claude'
        },
        'sourly': {
            'definition': 'Sourly is an adverb describing the manner of doing something with a sour, unpleasant, bitter, or ill-tempered attitude, often reflecting displeasure, resentment, or bad mood. This word characterizes actions, expressions, or speech that convey negativity, hostility, or dissatisfaction. Someone might respond sourly to criticism, look sourly at unwelcome news, or speak sourly about disappointing circumstances. The adverb suggests that the person\'s attitude or expression has turned unpleasant, like something that has gone sour. Sourly behavior often indicates underlying frustration, disappointment, or anger that colors how someone interacts with others or responds to situations.',
            'pronunciation': '/ˈsaʊərli/',
            'example_sentence': 'She looked _____ at the rainy weather that ruined her carefully planned outdoor wedding.',
            'etymology': 'From "sour" + "-ly" adverbial suffix, where "sour" comes from Old English "sūr."',
            'mnemonic': 'Think "SOUR-LY = SOUR attitude expressed, Like bitter mood, Years of disappointment showing" - in a sour, unpleasant manner.',
            'source': 'Claude'
        },
        'sous': {
            'definition': 'Sous is a French preposition meaning "under" or "below," most commonly encountered in English in the culinary term "sous chef" (under chef) and "sous vide" (under vacuum). In professional kitchens, the sous chef is the second-in-command who works under the head chef and helps manage kitchen operations. Sous vide is a cooking technique where food is vacuum-sealed and cooked at precisely controlled low temperatures in a water bath. The word appears in various French expressions and has been adopted into English culinary vocabulary due to French influence on professional cooking. Understanding sous helps in comprehending French culinary terminology and kitchen hierarchy.',
            'pronunciation': '/su/',
            'example_sentence': 'The _____ chef expertly managed the kitchen staff while the head chef was away.',
            'etymology': 'From French "sous," from Latin "subtus," meaning "under" or "below."',
            'mnemonic': 'Think "SOUS = Something Under chef position, Obviously beneath, Usually second-in-command, Superior to line cooks" - French word meaning under.',
            'source': 'Claude'
        },
        'sousaphone': {
            'definition': 'A sousaphone is a large brass musical instrument that wraps around the player\'s body, designed specifically for marching bands as a portable alternative to the concert tuba. Named after John Philip Sousa, the famous American composer and bandleader, this instrument features a forward-facing bell that projects sound toward the audience rather than upward like traditional tubas. The sousaphone provides the bass foundation for marching band music, capable of producing deep, resonant tones that carry well in outdoor performance venues. Modern sousaphones are often made from lightweight materials like fiberglass to reduce the physical burden on marching musicians. The instrument requires significant lung capacity and physical strength to play while marching.',
            'pronunciation': '/ˈsuzəˌfoʊn/',
            'example_sentence': 'The marching band\'s _____ section provided a powerful bass line that could be heard throughout the stadium.',
            'etymology': 'Named after John Philip Sousa (1854-1932), American composer and bandleader, combined with Greek "phone" (sound).',
            'mnemonic': 'Think "SOUSA-PHONE = SOUSA\'s designed instrument, Obviously for marching, Usually wrapped around body, Sounds deep bass notes, Always in marching bands, Portable large brass instrument, Heavy but mobile, Only bass voice, Never quiet, Everyone hears it" - large marching band brass instrument.',
            'source': 'Claude'
        },
        'souterrain': {
            'definition': 'A souterrain is an underground stone-lined passage or chamber, particularly those built during the Iron Age and early medieval periods in Scotland, Ireland, and other parts of northern Europe. These mysterious structures typically consist of long, curved tunnels with stone walls and roofs, often connected to above-ground settlements. Archaeologists debate their original purposes, with theories including food storage, refuge during attacks, religious or ceremonial use, or simply cool storage spaces for preserving grain and other provisions. Many souterrains show evidence of careful construction with corbelled stone roofing and drainage systems. These ancient underground structures provide valuable insights into the lives and building techniques of early Celtic and Pictish peoples.',
            'pronunciation': '/ˌsutəˈreɪn/',
            'example_sentence': 'The archaeological team discovered a well-preserved Iron Age _____ beneath the Scottish farmland.',
            'etymology': 'From French "souterrain," from "sous" (under) + "terrain" (ground), meaning "underground."',
            'mnemonic': 'Think "SOUT-ERRAIN = SOUth (under) TERRAIN, Everyone built them, Really ancient, Really underground, Always stone-lined, Including Iron Age structures, Never above ground" - underground stone passage.',
            'source': 'Claude'
        },
        'south': {
            'definition': 'South is one of the four cardinal directions, opposite to north on a compass, representing the direction toward the Earth\'s South Pole and generally associated with warmer climates in the Northern Hemisphere. This directional concept is fundamental to navigation, geography, and spatial orientation, with south typically corresponding to the bottom on standard maps. In many cultures, south carries symbolic associations with warmth, light, and life due to the sun\'s apparent path across the southern sky in northern regions. The term also designates geographical regions, such as the American South, characterized by shared cultural, historical, or political features. Understanding cardinal directions like south is essential for navigation, weather patterns, and geographical literacy.',
            'pronunciation': '/saʊθ/',
            'example_sentence': 'The migrating birds flew _____ to escape the harsh northern winter.',
            'etymology': 'From Old English "sūth," related to Old Norse "suthr" and German "süd," meaning the southern direction.',
            'mnemonic': 'Think "SOUTH = Sun\'s warmth direction, Opposite of north, Usually warmer, Toward heat and light, Hemisphere bottom" - direction toward Earth\'s South Pole.',
            'source': 'Claude'
        },
        'southern': {
            'definition': 'Southern refers to anything located in, coming from, or characteristic of the south or the southern part of a region, country, or area. This directional adjective describes geographical locations, weather patterns, cultural traditions, or other features associated with southern regions. In the United States, "Southern" often refers specifically to the southeastern states with their distinct cultural heritage, cuisine, climate, and historical background. Southern characteristics might include warmer temperatures, different vegetation, unique dialects, or regional customs that distinguish them from northern areas. The term helps identify and describe regional differences in geography, culture, climate, and social patterns.',
            'pronunciation': '/ˈsʌðərn/',
            'example_sentence': 'The _____ states experienced an unusually cold winter that damaged many tropical plants.',
            'etymology': 'From Old English "sūtherne," from "sūth" (south) + "-erne" (direction suffix), meaning "of the south."',
            'mnemonic': 'Think "SOUTH-ERN = SOUTH-oriented region, Everyone knows it\'s warmer, Really hot climate, Not northern" - relating to the south.',
            'source': 'Claude'
        },
        'southwest': {
            'definition': 'Southwest refers to the direction that is halfway between south and west on a compass, or to regions located in this direction relative to a reference point. In the United States, the Southwest commonly describes states like Arizona, New Mexico, Nevada, and parts of Texas, California, Colorado, and Utah, characterized by arid climates, desert landscapes, and distinctive cultural influences from Native American, Spanish, and Mexican heritage. This region is known for its dramatic scenery, including canyons, mesas, and desert flora, as well as unique architectural styles and cuisine. The southwestern direction corresponds to 225 degrees on a compass, making it an important bearing for navigation and geographical description.',
            'pronunciation': '/ˌsaʊθˈwɛst/',
            'example_sentence': 'The family moved to the _____ to enjoy the warm, dry climate and stunning desert scenery.',
            'etymology': 'Compound word from "south" + "west," indicating the direction between these two cardinal points.',
            'mnemonic': 'Think "SOUTH-WEST = SOUTH plus WEST direction, Often dry climate, Usually hot, Typically desert, High desert landscape, Where sun sets in summer, Everyone knows Arizona, Southwest cultures, Together makes 225 degrees" - direction or region between south and west.',
            'source': 'Claude'
        },
        'southwestern': {
            'definition': 'Southwestern describes anything characteristic of, located in, or relating to the southwestern region or direction, particularly in reference to the American Southwest with its distinctive geography, culture, and climate. This adjective encompasses the unique features of desert regions, including arid landscapes, adobe architecture, Native American and Hispanic cultural influences, and specialized flora and fauna adapted to dry conditions. Southwestern cuisine features ingredients like chilies, corn, and beans, while southwestern art often incorporates earth tones and geometric patterns reflecting indigenous traditions. The term also applies to the directional orientation toward the southwest or weather patterns coming from that direction.',
            'pronunciation': '/ˌsaʊθˈwɛstərn/',
            'example_sentence': 'The restaurant specialized in _____ cuisine featuring green chilies and traditional adobe oven-baked bread.',
            'etymology': 'From "southwest" + "-ern" suffix, meaning "of or relating to the southwest."',
            'mnemonic': 'Think "SOUTHWEST-ERN = SOUTHWEST-oriented culture, Everyone knows the desert, Really hot climate, Not humid like southeast" - relating to southwestern regions.',
            'source': 'Claude'
        },
        'space': {
            'definition': 'Space refers to the three-dimensional area or volume in which objects exist and events occur, encompassing both the vast cosmos beyond Earth\'s atmosphere and the measurable dimensions around us. In astronomy, space is the near-vacuum environment containing stars, planets, and other celestial bodies, while in everyday contexts, space describes room, area, or distance between objects. The concept includes physical space (measured dimensions), personal space (psychological comfort zones), and abstract space (mathematical or conceptual frameworks). Space exploration has expanded human understanding of the universe, while architectural and design professionals manipulate space to create functional and aesthetic environments. Understanding spatial relationships is fundamental to navigation, planning, and scientific inquiry.',
            'pronunciation': '/speɪs/',
            'example_sentence': 'The astronauts marveled at the infinite _____ surrounding their spacecraft as Earth appeared as a small blue marble.',
            'etymology': 'From Old French "espace," from Latin "spatium," meaning "room," "area," or "distance."',
            'mnemonic': 'Think "SPACE = Stars and Planets in vast Area, Cosmos Everywhere, or Empty room" - three-dimensional area or outer space.',
            'source': 'Claude'
        },
        'spaces': {
            'definition': 'Spaces is the plural form of "space," referring to multiple areas, rooms, or volumes, whether physical locations, gaps between objects, or designated areas for specific purposes. This word encompasses various types of spatial divisions: living spaces in homes, parking spaces for vehicles, green spaces in cities, and storage spaces for belongings. The term also applies to intervals or gaps, such as spaces between words in text or spaces between musical notes. In design and architecture, creating effective spaces involves considering flow, function, and aesthetics. Understanding how to organize and utilize multiple spaces efficiently is important for urban planning, interior design, and resource management.',
            'pronunciation': '/ˈspeɪsəz/',
            'example_sentence': 'The new office building featured flexible _____ that could be reconfigured for different types of work.',
            'etymology': 'Plural of "space," from Latin "spatium" through Old French "espace."',
            'mnemonic': 'Think "SPACES = Several Places for Activities, Creating areas for Everyone, Separated rooms" - multiple areas or rooms.',
            'source': 'Claude'
        },
        'spacious': {
            'definition': 'Spacious describes areas, rooms, or environments that have plenty of space, feeling open, roomy, and comfortable rather than cramped or confined. This adjective suggests generous dimensions that allow for easy movement, storage, and activities without feeling crowded. Spacious environments often create feelings of comfort, luxury, and freedom, whether in homes, vehicles, or public spaces. The quality of spaciousness can be enhanced through design techniques like high ceilings, large windows, minimal clutter, and open floor plans. Spacious areas are generally preferred for their practical benefits and psychological comfort, though they may require more heating, cooling, and maintenance than smaller spaces.',
            'pronunciation': '/ˈspeɪʃəs/',
            'example_sentence': 'The _____ living room with its high ceilings and large windows created a perfect gathering place for family celebrations.',
            'etymology': 'From Latin "spatiosus," from "spatium" (space), meaning "having much space."',
            'mnemonic': 'Think "SPAC-IOUS = SPACe that\'s generous, Including Ample room, Obviously comfortable, Usually feels open, Surely not cramped" - having plenty of room.',
            'source': 'Claude'
        },
        'spading': {
            'definition': 'Spading refers to the act of digging, turning, or breaking up soil using a spade, a flat-bladed tool designed for cutting through earth and roots. This fundamental gardening and agricultural activity prepares soil for planting by loosening compacted earth, incorporating organic matter, and creating better conditions for root growth and water penetration. Proper spading technique involves inserting the blade vertically into the soil, using foot pressure to drive it deep, then lifting and turning the earth. The process aerates soil, buries weeds and debris, and helps mix amendments like compost or fertilizer. Spading is typically done in spring or fall when soil moisture conditions are optimal for working.',
            'pronunciation': '/ˈspeɪdɪŋ/',
            'example_sentence': 'After _____ the vegetable garden, she added compost to enrich the soil before planting.',
            'etymology': 'From "spade" (digging tool) + "-ing" suffix, where "spade" comes from Old English "spadu."',
            'mnemonic': 'Think "SPAD-ING = SPADe working in garden, Including soil turning, Never gentle, Getting ready for planting" - digging with a spade.',
            'source': 'Claude'
        },
        'span': {
            'definition': 'Span functions as both a noun meaning the extent, reach, or duration of something, and a verb meaning to extend across or bridge a gap. As a measurement, span describes the distance between two points, the time duration of events, or the breadth of coverage. Famous spans include bridge spans crossing rivers, attention spans in psychology, and lifespans in biology. As a verb, span means to extend across space or time, such as a bridge spanning a river or a career spanning decades. The concept emphasizes the idea of connection, extension, or coverage across distances, whether physical, temporal, or conceptual.',
            'pronunciation': '/spæn/',
            'example_sentence': 'The magnificent bridge was designed to _____ the entire width of the harbor.',
            'etymology': 'From Old English "spann," meaning "the distance between thumb and little finger when extended."',
            'mnemonic': 'Think "SPAN = Space Across, or Period of time, Always measures extent, Never short distance" - extent or to reach across.',
            'source': 'Claude'
        },
        'spandau': {
            'definition': 'Spandau most commonly refers to a district in Berlin, Germany, known for the historic Spandau Citadel, a Renaissance fortress, and historically for the Spandau Prison where Nazi war criminals were held after World War II. The area has a rich history dating back to medieval times and features significant architectural and cultural landmarks. Spandau can also refer to the Spandau machine gun, a German automatic weapon used extensively during World War I and World War II. In architectural contexts, spandau might be confused with "spandrel," which refers to the triangular space between the curve of an arch and the rectangular frame around it.',
            'pronunciation': '/ˈspændaʊ/',
            'example_sentence': 'The historic _____ Citadel in Berlin attracts thousands of visitors interested in medieval German architecture.',
            'etymology': 'From the German city name Spandau, possibly from Slavic origins meaning "place on water."',
            'mnemonic': 'Think "SPANDAU = SPecial Place And District in berlin, Always historical, Never just ordinary, Distinguished fortress city, Always remembered for prison, Usually visited for history" - Berlin district with historic fortress.',
            'source': 'Claude'
        },
        'spangled': {
            'definition': 'Spangled describes something decorated or covered with small, shiny objects called spangles, or more generally, anything that sparkles or glitters with scattered bright spots resembling stars or jewels. The most famous use appears in "The Star-Spangled Banner," where it describes the American flag gleaming with stars. Spangled items feature numerous small, reflective decorations that catch and reflect light, creating a dazzling, festive appearance. The term can apply to clothing, decorations, natural phenomena like dewdrops on grass, or anything that displays scattered points of light or brightness. Spangled effects are often used in performance costumes, party decorations, and ceremonial items to create visual impact.',
            'pronunciation': '/ˈspæŋɡəld/',
            'example_sentence': 'Her costume was _____ with hundreds of sequins that caught the stage lights beautifully.',
            'etymology': 'From "spangle" (small shiny disk) + "-ed," where "spangle" comes from Middle English, possibly from Dutch "spang" (clasp).',
            'mnemonic': 'Think "SPANG-LED = SPArkly decorations that GLITTER, Led to shiny appearance, Everyone notices, Definitely eye-catching" - decorated with shiny spots.',
            'source': 'Claude'
        }
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            words = list(reader)
        
        print(f"Processing {len(words)} words from batch 164...")
        
        processed_data = []
        combined_errors = []
        
        for i, row in enumerate(words, 1):
            word = row['word'].strip()
            print(f"Processing word {i}: {word}")
            
            if word in word_data:
                data = word_data[word]
                
                # Check for combined word errors
                is_combined_error = '[COMBINED WORD ERROR]' in data['definition']
                if is_combined_error:
                    combined_errors.append(word)
                
                # Calculate difficulty scores
                phonetic_score = calculator.calculate_phonetic_transparency(word)
                frequency_score = calculator.calculate_word_frequency(word)
                morphological_score = calculator.calculate_morphological_complexity(word)
                etymology_score = calculator.calculate_etymology_complexity(word)
                
                processed_row = {
                    'word': word,
                    'definition': data['definition'],
                    'pronunciation': data['pronunciation'],
                    'example_sentence': data['example_sentence'],
                    'etymology': data['etymology'],
                    'mnemonic': data['mnemonic'],
                    'phonetic_transparency_score': phonetic_score,
                    'word_frequency_score': frequency_score,
                    'morphological_complexity_score': morphological_score,
                    'etymology_complexity_score': etymology_score,
                    'average_difficulty_score': round((phonetic_score + frequency_score + morphological_score + etymology_score) / 4, 2),
                    'source_years': row['years'],
                    'source_files': row['source_files'], 
                    'source_difficulties': row['source_difficulties'],
                    'definition_source': data['source'],
                    'pronunciation_source': data['source'],
                    'example_sentence_source': data['source'],
                    'etymology_source': data['source'],
                    'mnemonic_source': data['source'],
                    'final_difficulty_level': None,
                    'review_status': 'auto_processed',
                    'notes': 'Combined word error detected and flagged' if is_combined_error else 'Processed successfully'
                }
                
                processed_data.append(processed_row)
            else:
                print(f"Warning: No data found for word '{word}'")
        
        # Write to CSV
        if processed_data:
            fieldnames = [
                'word', 'definition', 'pronunciation', 'example_sentence', 'etymology', 'mnemonic',
                'phonetic_transparency_score', 'word_frequency_score', 'morphological_complexity_score', 'etymology_complexity_score', 'average_difficulty_score',
                'source_years', 'source_files', 'source_difficulties',
                'definition_source', 'pronunciation_source', 'example_sentence_source', 'etymology_source', 'mnemonic_source',
                'final_difficulty_level', 'review_status', 'notes'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_data)
        
        print(f"\nBatch 164 processing complete!")
        print(f"Successfully processed {len(processed_data)}/{len(words)} words")
        print(f"Output saved to: {output_file}")
        
        if combined_errors:
            print(f"\nCombined word errors detected: {len(combined_errors)}")
            for error in combined_errors:
                print(f"  - {error}")
        
    except Exception as e:
        print(f"Error processing batch 164: {str(e)}")
        raise

if __name__ == "__main__":
    main()