#!/usr/bin/env python3

import csv
import os

class DifficultyCalculator:
    def calculate_difficulty(self, word, definition="", etymology=""):
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._estimate_word_frequency(word)
        morphology_score = self._analyze_morphological_complexity(word, definition)
        etymology_score = self._analyze_etymological_complexity(etymology)
        
        raw_score = (phonetic_score + frequency_score + morphology_score + etymology_score) / 4
        
        if raw_score <= 2.0:
            return "Beginner"
        elif raw_score <= 3.5:
            return "Intermediate" 
        elif raw_score <= 4.5:
            return "Advanced"
        else:
            return "Expert"
    
    def _calculate_phonetic_transparency(self, word):
        irregularities = 0
        word = word.lower()
        
        silent_patterns = ['ght', 'mb', 'kn', 'wr', 'gn', 'mn', 'bt', 'st', 'tch']
        for pattern in silent_patterns:
            if pattern in word:
                irregularities += 1
        
        vowel_digraphs = ['ea', 'ee', 'oo', 'ou', 'ie', 'ai', 'ay', 'ey', 'oy', 'aw', 'au', 'ue']
        for digraph in vowel_digraphs:
            irregularities += word.count(digraph) * 0.5
        
        if any(c in word for c in 'qxz'):
            irregularities += 1
        
        if len(word) > 10:
            irregularities += (len(word) - 10) * 0.2
        
        return min(5.0, 1.0 + irregularities)
    
    def _estimate_word_frequency(self, word):
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'had', 'day', 'get', 'use', 'man', 'new', 'now', 'way', 'may', 'say', 'each', 'which', 'their', 'time', 'will', 'about', 'there', 'been', 'many', 'some', 'what', 'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'very', 'after', 'words', 'first', 'where', 'much', 'through', 'work', 'good', 'woman', 'life', 'right', 'high', 'every', 'tell', 'should', 'follow', 'around', 'think', 'help', 'turn', 'found', 'number', 'system', 'still', 'learn', 'human', 'music', 'world', 'family', 'never', 'home', 'place', 'picture', 'try', 'back', 'hand', 'why', 'while', 'here', 'take', 'question', 'thought', 'school', 'important', 'children', 'example', 'begin', 'seem', 'together', 'got']
        
        if word.lower() in common_words[:50]:
            return 1.0
        elif word.lower() in common_words:
            return 2.0
        elif len(word) <= 5:
            return 2.5
        elif len(word) <= 8:
            return 3.0
        else:
            return 4.0
    
    def _analyze_morphological_complexity(self, word, definition):
        complexity = 1.0
        
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'over', 'under', 'out', 'up', 'sub', 'inter', 'fore', 'de', 'non', 'in', 'im', 'ir', 'il', 'anti', 'auto', 'co', 'ex', 'trans', 'super', 'semi', 'multi', 'bi', 'tri', 'uni', 'mono', 'poly', 'micro', 'macro', 'pseudo', 'neo', 'proto', 'meta', 'hyper', 'hypo', 'ultra', 'contra', 'counter', 'extra', 'intra', 'intro', 'retro', 'circum', 'peri', 'para', 'epi', 'endo', 'exo']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'ion', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'eous', 'ious', 'al', 'ial', 'ic', 'tic', 'ive', 'ative', 'itive', 'ory', 'ary', 'ery', 'y', 'ify', 'ize', 'ise', 'ate', 'ite', 'ure', 'age', 'dom', 'ship', 'hood', 'ward', 'wise', 'like', 'some', 'fold', 'teen', 'ty', 'th']
        
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                complexity += 0.5
                break
        
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                complexity += 0.3
                break
        
        if any(char in definition.lower() for char in ['technical', 'medical', 'scientific', 'legal', 'archaic', 'obsolete']):
            complexity += 1.0
        
        return min(5.0, complexity)
    
    def _analyze_etymological_complexity(self, etymology):
        if not etymology:
            return 3.0
        
        etymology_lower = etymology.lower()
        
        complex_origins = ['sanskrit', 'arabic', 'hebrew', 'chinese', 'japanese', 'nahuatl', 'quechua', 'persian', 'turkish', 'finnish', 'hungarian', 'basque', 'irish', 'welsh', 'scots gaelic']
        moderate_origins = ['old norse', 'old english', 'middle english', 'anglo-norman', 'old french', 'middle french', 'medieval latin', 'vulgar latin', 'proto-germanic', 'proto-indo-european']
        simple_origins = ['latin', 'greek', 'french', 'german', 'spanish', 'italian', 'portuguese', 'dutch', 'english']
        
        for origin in complex_origins:
            if origin in etymology_lower:
                return 5.0
        
        for origin in moderate_origins:
            if origin in etymology_lower:
                return 3.5
        
        for origin in simple_origins:
            if origin in etymology_lower:
                return 2.0
        
        multiple_origins = sum(1 for origin in simple_origins + moderate_origins + complex_origins if origin in etymology_lower)
        if multiple_origins > 1:
            return min(5.0, 2.0 + multiple_origins * 0.5)
        
        return 3.0

def process_words():
    calculator = DifficultyCalculator()
    
    words_data = [
        {
            "word": "bavaria",
            "definition": "A state in southeastern Germany, known for its culture and beer",
            "pronunciation": "/bəˈvɛriə/",
            "etymology": "From Germanic Bavarii, the name of a tribe that settled in the region",
            "memory_tip": "BAVARIA: Beautiful Alpine - Vibrant And Rich culture, In south-central europe, Amazing beer region",
            "example_sentence": "The Oktoberfest celebration originated in _____ and attracts visitors worldwide.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bavarian",
            "definition": "Relating to Bavaria or its people, culture, or language",
            "pronunciation": "/bəˈvɛriən/",
            "etymology": "From Bavaria + -an suffix, referring to the German state and its culture",
            "memory_tip": "BAVARIAN: Beautiful Alpine - Vibrant And Rich traditions, In Austria and Germany area, Native culture",
            "example_sentence": "The restaurant served traditional _____ sausages with sauerkraut and pretzels.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bavarois",
            "definition": "A cold dessert made from custard thickened with gelatin and lightened with whipped cream",
            "pronunciation": "/ˌbævəˈrwɑ/",
            "etymology": "From French bavarois meaning 'Bavarian', referring to its supposed Bavarian origin",
            "memory_tip": "BAVAROIS: Beautiful And - Velvet dessert, Amazing Rich custard, Offered In restaurants, Silky dessert",
            "example_sentence": "The chef prepared a delicate strawberry _____ for the elegant dinner party.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bawl",
            "definition": "To cry loudly; to shout or call out loudly",
            "pronunciation": "/bɔl/",
            "etymology": "From Middle English bawlen, possibly of imitative origin",
            "memory_tip": "BAWL: Big And - Wailing Loud cries and calls",
            "example_sentence": "The toddler began to _____ when his favorite toy was taken away.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bayonet",
            "definition": "A knife-like weapon attached to the end of a rifle",
            "pronunciation": "/ˈbeɪənət/",
            "etymology": "From French baïonnette, named after Bayonne, France, where it was first made",
            "memory_tip": "BAYONET: Blade Attached - Yard-long weapon On rifle, Nice sharp Edge, Tactical weapon",
            "example_sentence": "The soldier fixed his _____ to his rifle before the charge.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bayreuth",
            "definition": "A city in Germany famous for its Wagner opera festival",
            "pronunciation": "/ˈbaɪroɪt/",
            "etymology": "From German Bayreuth, from Old High German bei 'near' + reuth 'clearing'",
            "memory_tip": "BAYREUTH: Beautiful And - Year-round Wagner opera festival, Really Exceptional music, Unique Theater Heritage",
            "example_sentence": "Music lovers travel to _____ every summer for the prestigious Wagner festival.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bazaar",
            "definition": "A marketplace, especially in Middle Eastern countries; a fundraising sale",
            "pronunciation": "/bəˈzɑr/",
            "etymology": "From Persian bāzār meaning 'market'",
            "memory_tip": "BAZAAR: Bustling And - Zealous merchants, Amazing treasures, All kinds of goods, Really diverse marketplace",
            "example_sentence": "The charity _____ featured handmade crafts and delicious international foods.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bazar",
            "definition": "Alternative spelling of bazaar; a marketplace or market area",
            "pronunciation": "/bəˈzɑr/",
            "etymology": "From Persian bāzār meaning 'market', alternative spelling of bazaar",
            "memory_tip": "BAZAR: Bustling And - Zealous merchants, Alternative spelling, Really diverse marketplace",
            "example_sentence": "The old _____ in the city center sold spices, textiles, and traditional crafts.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bazooka",
            "definition": "A portable rocket launcher; a type of antitank weapon",
            "pronunciation": "/bəˈzukə/",
            "etymology": "Named after a musical instrument played by comedian Bob Burns, from its similar appearance",
            "memory_tip": "BAZOOKA: Big And - Zapping weapon, Outstanding rocket launcher, Kicks powerfully, Attacks tanks",
            "example_sentence": "The soldiers used a _____ to destroy the enemy's armored vehicle.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bdelloid",
            "definition": "Relating to a type of rotifer (microscopic aquatic animal) that reproduces asexually",
            "pronunciation": "/ˈdɛlɔɪd/",
            "etymology": "From Greek bdella meaning 'leech' + -oid suffix meaning 'resembling'",
            "memory_tip": "BDELLOID: Bizarre Definitely - Everyone knows they Look Like leeches, Odd aquatic organism, Interesting Diverse microscopic life",
            "example_sentence": "The _____ rotifers have survived for millions of years without sexual reproduction.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beacons",
            "definition": "Plural of beacon; signals or lights used for guidance or warning",
            "pronunciation": "/ˈbikənz/",
            "etymology": "From Old English beacen meaning 'sign, signal', from Proto-Germanic baukna",
            "memory_tip": "BEACONS: Bright Emergency - Amazing signals, Calling Out to people, Outstanding Navigation System",
            "example_sentence": "The lighthouse _____ guided ships safely through the rocky coastline.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beagle",
            "definition": "A small to medium-sized breed of hunting dog with excellent scenting ability",
            "pronunciation": "/ˈbiɡəl/",
            "etymology": "Possibly from Old French beegueule meaning 'open throat', referring to their baying",
            "memory_tip": "BEAGLE: Best And - Great hunting dog, Amazing scent tracking, Great Little Explorer dogs",
            "example_sentence": "The friendly _____ wagged its tail enthusiastically when children approached.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beak",
            "definition": "The hard, pointed mouth part of a bird; a person's nose",
            "pronunciation": "/bik/",
            "etymology": "From Old French bec, possibly from Gaulish bekko",
            "memory_tip": "BEAK: Bird's Amazing - Eating tool, All Kinds of birds have this mouth part",
            "example_sentence": "The eagle used its sharp _____ to tear apart its prey.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beam",
            "definition": "A ray of light; a structural support; to smile broadly",
            "pronunciation": "/bim/",
            "etymology": "From Old English beam meaning 'tree, beam of light'",
            "memory_tip": "BEAM: Bright Energy - Amazing light ray, Magnificent structural support",
            "example_sentence": "A _____ of sunlight streamed through the cathedral's stained glass window.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beans",
            "definition": "Plural of bean; edible seeds of various leguminous plants",
            "pronunciation": "/binz/",
            "etymology": "From Old English bean, from Proto-Germanic bauna",
            "memory_tip": "BEANS: Best And - Extremely Nutritious food, Amazing healthy Seeds",
            "example_sentence": "The vegetarian chili was made with kidney _____ and black _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bear",
            "definition": "A large mammal; to carry or support; to endure",
            "pronunciation": "/bɛr/",
            "etymology": "From Old English bera, from Proto-Germanic beron",
            "memory_tip": "BEAR: Big And - Extremely Amazing wild animal, Really powerful creature",
            "example_sentence": "The mother _____ protected her cubs from potential threats in the forest.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beatboxingmutate",
            "definition": "ERROR: Combined word - should be separate words",
            "pronunciation": "",
            "etymology": "",
            "memory_tip": "",
            "example_sentence": "",
            "etymology_source": "",
            "definition_source": "",
            "example_sentence_source": "",
            "audio_source": "",
            "combined_word_error": True
        },
        {
            "word": "beatific",
            "definition": "Blissfully serene; showing divine happiness",
            "pronunciation": "/ˌbiəˈtɪfɪk/",
            "etymology": "From Latin beatificus meaning 'making blessed', from beatus 'blessed' + facere 'to make'",
            "memory_tip": "BEATIFIC: Blessed Everyone - Always Totally peaceful, In divine happiness, Finding Inner Contentment",
            "example_sentence": "The meditation teacher had a _____ expression of peace and tranquility.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beatificbeguile",
            "definition": "ERROR: Combined word - should be separate words",
            "pronunciation": "",
            "etymology": "",
            "memory_tip": "",
            "example_sentence": "",
            "etymology_source": "",
            "definition_source": "",
            "example_sentence_source": "",
            "audio_source": "",
            "combined_word_error": True
        },
        {
            "word": "beauceron",
            "definition": "A breed of large French herding dog with a black and tan coat",
            "pronunciation": "/ˈboʊsəˌrɑn/",
            "etymology": "From French Beauceron, named after the Beauce region of France",
            "memory_tip": "BEAUCERON: Beautiful And - Excellent French herding dog, Cheerful outdoor companion, Really Outstanding Guardian dog, Nice breed",
            "example_sentence": "The _____ excelled at herding sheep and protecting the farm from intruders.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beaucoupbanal",
            "definition": "ERROR: Combined word - should be separate words",
            "pronunciation": "",
            "etymology": "",
            "memory_tip": "",
            "example_sentence": "",
            "etymology_source": "",
            "definition_source": "",
            "example_sentence_source": "",
            "audio_source": "",
            "combined_word_error": True
        },
        {
            "word": "beaumontage",
            "definition": "A type of wood filler made from shellac and fine sawdust",
            "pronunciation": "/ˈboʊmənˌtɑʒ/",
            "etymology": "Named after Élie de Beaumont, French geologist, possibly for its geological appearance",
            "memory_tip": "BEAUMONTAGE: Beautiful And - Understanding fine woodworking, Made from Organic material, Nice smooth finish, Tremendous wood repair, Amazing craftsman tool, Great Enhancement",
            "example_sentence": "The furniture restorer used _____ to fill the cracks and imperfections in the antique cabinet.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beautician",
            "definition": "A person whose job is to provide beauty treatments",
            "pronunciation": "/bjuˈtɪʃən/",
            "etymology": "From beauty + -ician suffix, referring to a specialist in beauty treatments",
            "memory_tip": "BEAUTICIAN: Beauty And - Understanding cosmetics, Talented professional, Improving appearances, Caring for clients, Inspiring Amazing transformations, Natural beauty expert",
            "example_sentence": "The skilled _____ gave her a relaxing facial and professional makeup application.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beaux",
            "definition": "Plural of beau; boyfriends or male admirers",
            "pronunciation": "/boʊz/",
            "etymology": "From French beaux, plural of beau meaning 'beautiful, handsome'",
            "memory_tip": "BEAUX: Beautiful And - Enamored admirers, Amazing Unwavering romantic partners, eXcellent gentlemen",
            "example_sentence": "The popular young woman had several _____ competing for her attention.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bebop",
            "definition": "A type of jazz characterized by fast tempos and improvisation",
            "pronunciation": "/ˈbiˌbɑp/",
            "etymology": "From nonsense syllables used in jazz singing, possibly imitative of the music's rhythm",
            "memory_tip": "BEBOP: Beautiful Energetic - Bold music style, Outstanding Performance jazz style",
            "example_sentence": "The jazz quintet played energetic _____ music that kept the audience dancing.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "became",
            "definition": "Past tense of become; came to be or grew to be",
            "pronunciation": "/bɪˈkeɪm/",
            "etymology": "From Old English becuman meaning 'to come to, arrive', from be- + cuman 'to come'",
            "memory_tip": "BECAME: Before Everything - Changed And gained More importance, Everyone transformed",
            "example_sentence": "After years of practice, she _____ an accomplished pianist.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "because",
            "definition": "For the reason that; since",
            "pronunciation": "/bɪˈkɔz/",
            "etymology": "From Middle English by cause, from by + cause",
            "memory_tip": "BECAUSE: By - Every Clear explanation, And Understanding Shows Explanation",
            "example_sentence": "She stayed home _____ she was feeling under the weather.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beccafico",
            "definition": "A small European songbird, considered a delicacy in Mediterranean cuisine",
            "pronunciation": "/ˌbɛkəˈfikoʊ/",
            "etymology": "From Italian beccafico, from beccare 'to peck' + fico 'fig', as the bird feeds on figs",
            "memory_tip": "BECCAFICO: Bird Eating - Cascading figs, Culinary And Famous delicate bird, Italian Cuisine Offering",
            "example_sentence": "The traditional Maltese dish featured roasted _____ served with herbs and wine.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beckon",
            "definition": "To make a gesture to encourage someone to approach",
            "pronunciation": "/ˈbɛkən/",
            "etymology": "From Old English becnian meaning 'to make signs', from beacen 'beacon'",
            "memory_tip": "BECKON: By Every - Calling gesture, Kindly Offering someone to come Near",
            "example_sentence": "She began to _____ the children over to see the baby rabbits.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "become",
            "definition": "To grow to be; to come to be through development",
            "pronunciation": "/bɪˈkʌm/",
            "etymology": "From Old English becuman meaning 'to come to, arrive', from be- + cuman 'to come'",
            "memory_tip": "BECOME: By Every - Change Or transformation, Makes Everyone different",
            "example_sentence": "With dedication and practice, anyone can _____ skilled at playing the piano.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "becoming",
            "definition": "In the process of coming to be; attractive or appropriate",
            "pronunciation": "/bɪˈkʌmɪŋ/",
            "etymology": "From become + -ing, referring to the process of change or appropriateness",
            "memory_tip": "BECOMING: By Every - Change Or development, Making people Into New things, Growing into something",
            "example_sentence": "The blue dress was very _____ on her and complemented her eyes perfectly.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "becquerel",
            "definition": "A unit of measurement for radioactivity, named after Henri Becquerel",
            "pronunciation": "/ˈbɛkəˌrɛl/",
            "etymology": "Named after Henri Becquerel, French physicist who discovered radioactivity",
            "memory_tip": "BECQUEREL: Big Energy - Counting radiation Quantities, Understanding science Experiments, Really Essential Laboratory unit",
            "example_sentence": "The radiation detector measured the sample at 500 _____ per second.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "becquereldarnel",
            "definition": "ERROR: Combined word - should be separate words",
            "pronunciation": "",
            "etymology": "",
            "memory_tip": "",
            "example_sentence": "",
            "etymology_source": "",
            "definition_source": "",
            "example_sentence_source": "",
            "audio_source": "",
            "combined_word_error": True
        },
        {
            "word": "bedraggled",
            "definition": "Wet, untidy, and exhausted in appearance",
            "pronunciation": "/bɪˈdræɡəld/",
            "etymology": "From be- + draggle (to drag through mud), meaning 'made wet and muddy'",
            "memory_tip": "BEDRAGGLED: Been Dragged - Really Awful appearance, Greatly Greatly Looking bad, Everything Disheveled",
            "example_sentence": "The hikers emerged from the forest _____ after being caught in the thunderstorm.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beelzebub",
            "definition": "A name for the devil or a powerful demon in Christian tradition",
            "pronunciation": "/biˈɛlzəˌbʌb/",
            "etymology": "From Hebrew ba'al zebub meaning 'lord of the flies', a Philistine god",
            "memory_tip": "BEELZEBUB: Bad Evil - Extremely Lethal demonic presence, Zealous Evil Being, Underworld Boss",
            "example_sentence": "In literature, _____ is often portrayed as a powerful figure of darkness.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bees",
            "definition": "Plural of bee; flying insects that collect nectar and produce honey",
            "pronunciation": "/biz/",
            "etymology": "From Old English beo, from Proto-Germanic bjon",
            "memory_tip": "BEES: Busy Everywhere - Excellent pollinators, Sweet honey makers",
            "example_sentence": "The garden was buzzing with _____ collecting pollen from the flowering plants.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beethovenian",
            "definition": "Relating to or characteristic of the musical style of Ludwig van Beethoven",
            "pronunciation": "/ˌbeɪtoʊˈviniən/",
            "etymology": "From Beethoven (German composer) + -ian suffix meaning 'relating to'",
            "memory_tip": "BEETHOVENIAN: Beautiful Emotional - Epic music, Tremendous musical Heritage, Outstanding Virtuoso musical style, Everyone loves his classical music, Notable remarkable music, Inspiring Artistic style, Notably excellent compositions",
            "example_sentence": "The symphony displayed _____ grandeur with its dramatic crescendos and powerful themes.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beetle",
            "definition": "A type of insect with hard wing covers; to overhang or jut out",
            "pronunciation": "/ˈbitəl/",
            "etymology": "From Old English bitula meaning 'biter', from bitan 'to bite'",
            "memory_tip": "BEETLE: Bug Eating - Everything That Lives around plants, Lots of varieties, Everywhere you look",
            "example_sentence": "The shiny black _____ crawled across the garden path toward the compost pile.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "began",
            "definition": "Past tense of begin; started or commenced",
            "pronunciation": "/bɪˈɡæn/",
            "etymology": "From Old English beginnan, from be- + ginnan 'to begin'",
            "memory_tip": "BEGAN: Before Everything - Going And starting, All New activities start",
            "example_sentence": "She _____ studying for her final exams three weeks before the test date.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "begin",
            "definition": "To start or commence an action or process",
            "pronunciation": "/bɪˈɡɪn/",
            "etymology": "From Old English beginnan, from be- + ginnan 'to begin'",
            "memory_tip": "BEGIN: Before Everything - Going Into New activities",
            "example_sentence": "The ceremony will _____ promptly at three o'clock this afternoon.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beginning",
            "definition": "The start or commencement of something; the first part",
            "pronunciation": "/bɪˈɡɪnɪŋ/",
            "etymology": "From begin + -ing suffix, referring to the start of something",
            "memory_tip": "BEGINNING: Before Everything - Going Into New activities, Noting Initial phases, No experience yet",
            "example_sentence": "At the _____ of the school year, students receive their class schedules.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "begins",
            "definition": "Third person singular present of begin; starts or commences",
            "pronunciation": "/bɪˈɡɪnz/",
            "etymology": "From begin + -s suffix for third person singular present tense",
            "memory_tip": "BEGINS: Before Everything - Going Into New activities, Single person Starting",
            "example_sentence": "The concert _____ at eight o'clock with the orchestra tuning their instruments.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beguile",
            "definition": "To charm or enchant; to trick or deceive",
            "pronunciation": "/bɪˈɡaɪl/",
            "etymology": "From Middle English begilen, from be- + guile 'deceit'",
            "memory_tip": "BEGUILE: Bewitch Everyone - Gracefully seducing, Using charm, Intriguing, Lovely Enchantment",
            "example_sentence": "The storyteller's captivating voice could _____ audiences for hours.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "behavior",
            "definition": "The way in which someone acts or conducts themselves",
            "pronunciation": "/bɪˈheɪvjər/",
            "etymology": "From Middle English behavour, from behave + -ior suffix",
            "memory_tip": "BEHAVIOR: Being Everybody - How Actions display Values, Individual Or group responses",
            "example_sentence": "The teacher praised the students for their excellent _____ during the field trip.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "behemoth",
            "definition": "Something enormous; a creature of monstrous size or power",
            "pronunciation": "/bɪˈhiməθ/",
            "etymology": "From Hebrew behemoth, plural of behemah meaning 'beast'",
            "memory_tip": "BEHEMOTH: Big Enormous - Huge monster, Extremely Massive creature, Outstanding giant, Tremendous creature, Huge",
            "example_sentence": "The cruise ship was a _____ of the seas, carrying thousands of passengers.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "behind",
            "definition": "At the back of; following; remaining after departure",
            "pronunciation": "/bɪˈhaɪnd/",
            "etymology": "From Old English behindan, from be- + hindan 'from behind'",
            "memory_tip": "BEHIND: Back End - Hindmost In position, Noting Distance",
            "example_sentence": "She left her umbrella _____ at the restaurant after lunch.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "behold",
            "definition": "To see or observe; used to call attention to something",
            "pronunciation": "/bɪˈhoʊld/",
            "etymology": "From Old English behealdan, from be- + healdan 'to hold'",
            "memory_tip": "BEHOLD: Bring Everyone - Here to see, Observe, Look, Definitely observe",
            "example_sentence": "_____ the magnificent sunset painting the sky in brilliant colors.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beijing",
            "definition": "The capital city of China, also known as Peking",
            "pronunciation": "/ˈbeɪˈdʒɪŋ/",
            "etymology": "From Chinese Beijing, from bei 'north' + jing 'capital'",
            "memory_tip": "BEIJING: Big Eastern - Important capital city, Just like an Important center of china, Never small, Great city",
            "example_sentence": "The Summer Olympics were held in _____ in 2008 with spectacular ceremonies.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "belgium",
            "definition": "A country in Western Europe known for chocolate, waffles, and beer",
            "pronunciation": "/ˈbɛldʒəm/",
            "etymology": "From Latin Belgium, from the Celtic tribe Belgae",
            "memory_tip": "BELGIUM: Beautiful European - Little country, Great chocolate and beer, International Union headquarters, Unique Multilingual country",
            "example_sentence": "We traveled to _____ to visit the historic city of Bruges and taste authentic chocolates.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "belgravia",
            "definition": "An upscale district in central London known for elegant architecture",
            "pronunciation": "/bɛlˈɡreɪviə/",
            "etymology": "Named after Belgrave Square, which was named after the village of Belgrave in Leicestershire",
            "memory_tip": "BELGRAVIA: Beautiful Elegant - London's Great wealthy area, Remarkable Architecture, Very Impressive luxury district, Amazing expensive neighborhood",
            "example_sentence": "The embassy was located in _____, one of London's most prestigious neighborhoods.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_018_processed.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'word', 'definition', 'pronunciation', 'etymology', 'memory_tip',
            'example_sentence', 'etymology_source', 'definition_source', 
            'example_sentence_source', 'audio_source', 'difficulty_level',
            'phonetic_score', 'frequency_score', 'morphology_score', 
            'etymology_score', 'combined_word_error'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        combined_errors = 0
        processed_count = 0
        
        for word_data in words_data:
            if word_data['combined_word_error']:
                combined_errors += 1
                difficulty_level = "N/A"
                phonetic_score = 0.0
                frequency_score = 0.0
                morphology_score = 0.0
                etymology_score = 0.0
            else:
                difficulty_level = calculator.calculate_difficulty(
                    word_data['word'], 
                    word_data['definition'], 
                    word_data['etymology']
                )
                phonetic_score = calculator._calculate_phonetic_transparency(word_data['word'])
                frequency_score = calculator._estimate_word_frequency(word_data['word'])
                morphology_score = calculator._analyze_morphological_complexity(word_data['word'], word_data['definition'])
                etymology_score = calculator._analyze_etymological_complexity(word_data['etymology'])
            
            row = {
                'word': word_data['word'],
                'definition': word_data['definition'],
                'pronunciation': word_data['pronunciation'],
                'etymology': word_data['etymology'],
                'memory_tip': word_data['memory_tip'],
                'example_sentence': word_data['example_sentence'],
                'etymology_source': word_data['etymology_source'],
                'definition_source': word_data['definition_source'],
                'example_sentence_source': word_data['example_sentence_source'],
                'audio_source': word_data['audio_source'],
                'difficulty_level': difficulty_level,
                'phonetic_score': round(phonetic_score, 2),
                'frequency_score': round(frequency_score, 2),
                'morphology_score': round(morphology_score, 2),
                'etymology_score': round(etymology_score, 2),
                'combined_word_error': word_data['combined_word_error']
            }
            
            writer.writerow(row)
            processed_count += 1
        
        print(f"Batch 018 processing complete!")
        print(f"Processed: {processed_count}/50 words")
        print(f"Combined word errors flagged: {combined_errors}")
        print(f"Valid spelling words: {processed_count - combined_errors}")
        
        if combined_errors > 0:
            print(f"\nCombined word errors found:")
            for word_data in words_data:
                if word_data['combined_word_error']:
                    print(f"  - {word_data['word']}")

if __name__ == "__main__":
    process_words()