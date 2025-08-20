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
            "word": "beurre",
            "definition": "French word for butter, used in culinary contexts",
            "pronunciation": "/bɜr/",
            "etymology": "From Old French burre, from Latin butyrum, from Greek boutyron 'cow cheese'",
            "memory_tip": "BEURRE: Beautiful European - Understanding cooking, Rich food, Really Essential ingredient",
            "example_sentence": "The chef prepared the sauce with _____ blanc and fresh herbs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beverage",
            "definition": "A drink, especially one other than water",
            "pronunciation": "/ˈbɛvərɪdʒ/",
            "etymology": "From Old French beverage, from beivre 'to drink', from Latin bibere",
            "memory_tip": "BEVERAGE: Best Everyone - Very Enjoyable drink, Refreshing And thirst-quenching, Great Experience",
            "example_sentence": "The restaurant offered a variety of hot and cold _____ options.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beyond",
            "definition": "At or to the further side of; outside the scope or range of",
            "pronunciation": "/bɪˈjɑnd/",
            "etymology": "From Old English begeondan, from be- 'by' + geondan 'yonder'",
            "memory_tip": "BEYOND: Being Everyone - Yearning to go past limits, Outside Normal boundaries, Distance far away",
            "example_sentence": "The mountain peak was _____ what they could see through the clouds.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bezier",
            "definition": "Relating to mathematical curves used in computer graphics and design",
            "pronunciation": "/ˈbɛziər/",
            "etymology": "Named after Pierre Bézier, French engineer who developed the mathematical curves",
            "memory_tip": "BEZIER: Beautiful Elegant - curves in computer graphics, Innovation by Engineer, Really useful mathematical curves",
            "example_sentence": "The graphic designer used _____ curves to create smooth, flowing lines in the logo.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bhangra",
            "definition": "A type of folk dance and music from Punjab, popular in South Asian culture",
            "pronunciation": "/ˈbɑŋɡrə/",
            "etymology": "From Punjabi bhāṅgṛā, related to bhāṅg 'hemp' (traditionally associated with harvest celebrations)",
            "memory_tip": "BHANGRA: Boisterous Happy - Amazing cultural dance, Never stops moving, Great Rhythmic dancing, Amazing celebration dance",
            "example_sentence": "The wedding celebration featured energetic _____ dancing with traditional music.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bhikshuni",
            "definition": "A fully ordained Buddhist nun",
            "pronunciation": "/bɪkˈʃuni/",
            "etymology": "From Sanskrit bhikṣuṇī, from bhikṣu 'monk' + feminine suffix -ṇī",
            "memory_tip": "BHIKSHUNI: Buddhist Holy - Individual dedicated to spiritual practice, Kind Sacred woman, Holy religious life, Unique spiritual calling, Notable female monk, Inspiring spiritual devotion",
            "example_sentence": "The _____ devoted her life to meditation and teaching Buddhist philosophy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bhikshunisvarabhakti",
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
            "word": "bialy",
            "definition": "A Polish bread roll with a depression instead of a hole, topped with onions",
            "pronunciation": "/biˈɑli/",
            "etymology": "From Yiddish beyaly, short for beyalystoker, from Białystok, a city in Poland",
            "memory_tip": "BIALY: Bread In - Amazing Polish bread, Looks like bagel, Yummy delicious bread",
            "example_sentence": "She enjoyed a warm _____ with cream cheese and lox for breakfast.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bias",
            "definition": "Prejudice in favor of or against one thing; a diagonal line across fabric",
            "pronunciation": "/ˈbaɪəs/",
            "etymology": "From Old French biais meaning 'slant, slope', possibly from Greek epikarsios 'oblique'",
            "memory_tip": "BIAS: Being Influenced - Always Slanted toward one side, Strong personal preference",
            "example_sentence": "The researcher tried to eliminate _____ from the study design.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bibelot",
            "definition": "A small decorative object; a trinket or curio",
            "pronunciation": "/ˈbɪbəˌloʊ/",
            "etymology": "From French bibelot, possibly from bel 'beautiful' or from bibere 'to drink' (referring to decorative cups)",
            "memory_tip": "BIBELOT: Beautiful Interesting - Bijou ornamental decorative object, Everyone Likes these small treasures, Outstanding Trinkets",
            "example_sentence": "The antique shop was filled with charming _____ from various periods.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bibimbap",
            "definition": "A Korean dish of rice topped with vegetables, meat, and a fried egg",
            "pronunciation": "/ˈbibɪmˌbæp/",
            "etymology": "From Korean bibimbap, from bibim 'mixing' + bap 'rice'",
            "memory_tip": "BIBIMBAP: Beautiful Ingredients - Bowl of mixed vegetables, Including meat, Mixed colorful Bowl, Amazing Korean meal, Perfectly balanced dish",
            "example_sentence": "The restaurant's signature _____ featured fresh vegetables and spicy gochujang sauce.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bible",
            "definition": "The Christian or Jewish scriptures; an authoritative reference book",
            "pronunciation": "/ˈbaɪbəl/",
            "etymology": "From Old French bible, from Latin biblia, from Greek biblia 'books'",
            "memory_tip": "BIBLE: Book Inspiring - Belief, Important sacred book, Beautiful Lessons, Everyone reads this holy text",
            "example_sentence": "The family kept their ancestral _____ on the mantelpiece.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bibliopegist",
            "definition": "A person who binds books; a bookbinder",
            "pronunciation": "/ˌbɪblioʊˈpɛdʒɪst/",
            "etymology": "From Greek biblio- 'book' + pegist from Greek pegein 'to fasten, fix'",
            "memory_tip": "BIBLIOPEGIST: Book Binding - specialist working with books, Lovely Interesting craft, Outstanding Professional bookwork, Expert, Great book craftsmanship, Important trade, Skilled worker, artisan protecting books through quality bindings",
            "example_sentence": "The skilled _____ carefully restored the damaged medieval manuscript.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bibliophile",
            "definition": "A person who loves and collects books",
            "pronunciation": "/ˈbɪblioʊˌfaɪl/",
            "etymology": "From Greek biblio- 'book' + -phile 'lover of'",
            "memory_tip": "BIBLIOPHILE: Book reader - Books Inspire these readers, Lots of books, Interest in books, Outstanding People reading, Heavily Interested book Lovers, Everyone knows they love books",
            "example_sentence": "The _____ spent hours browsing rare book shops in search of first editions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bicameral",
            "definition": "Having two legislative chambers or houses",
            "pronunciation": "/baɪˈkæmərəl/",
            "etymology": "From Latin bi- 'two' + camera 'chamber' + -al suffix",
            "memory_tip": "BICAMERAL: Both Important - Chambers And government structures, Multiple divisions, Everyone Recognizes two parts, A Legislative system",
            "example_sentence": "The United States has a _____ legislature consisting of the House and Senate.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bicarbonate",
            "definition": "A salt containing the anion HCO3−; commonly sodium bicarbonate (baking soda)",
            "pronunciation": "/baɪˈkɑrbəˌneɪt/",
            "etymology": "From bi- 'two' + carbonate, referring to the chemical compound with two hydrogen atoms",
            "memory_tip": "BICARBONATE: Basic Important - Chemical And compound, Really Basic cooking ingredient, Outstanding Natural cleaner, Amazing Totally Essential cleaning agent",
            "example_sentence": "She used sodium _____ to neutralize the acid in the recipe.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biceps",
            "definition": "The large muscle at the front of the upper arm",
            "pronunciation": "/ˈbaɪsɛps/",
            "etymology": "From Latin biceps meaning 'two-headed', from bi- 'two' + caput 'head'",
            "memory_tip": "BICEPS: Big Important - muscle, Commonly Everyone works out these arm muscles, Everyone Practices Strengthening these muscles",
            "example_sentence": "He flexed his _____ to show the results of his weightlifting routine.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bidialectal",
            "definition": "Able to speak two dialects of the same language fluently",
            "pronunciation": "/ˌbaɪdaɪəˈlɛktəl/",
            "etymology": "From bi- 'two' + dialectal, relating to speaking two dialects",
            "memory_tip": "BIDIALECTAL: Both Important - Dialects And Language varieties, Everyone Communicates Through different varieties, Amazing Language ability",
            "example_sentence": "The _____ speaker could switch between formal and colloquial speech effortlessly.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biennial",
            "definition": "Taking place every two years; a plant that lives for two years",
            "pronunciation": "/baɪˈɛniəl/",
            "etymology": "From Latin biennium meaning 'two years', from bi- 'two' + annus 'year'",
            "memory_tip": "BIENNIAL: Both Important - Every other year, Never annually, Not every single year, In Alternative years, Always two year schedule, Lots of time between events",
            "example_sentence": "The _____ art exhibition attracts visitors from around the world.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bienvenu",
            "definition": "French masculine form of 'welcome'",
            "pronunciation": "/bjɛ̃vəˈny/",
            "etymology": "From French bienvenu, from bien 'well' + venu 'come' (past participle of venir)",
            "memory_tip": "BIENVENU: Being welcomed - In French language, Everyone makes visitors feel welcomed, Nice greeting, Very European hospitality, Everyone Needs welcome, Understanding hospitality",
            "example_sentence": "The hotel greeted every male guest with a warm '_____ monsieur.'",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bienvenue",
            "definition": "French feminine form of 'welcome'",
            "pronunciation": "/bjɛ̃vəˈny/",
            "etymology": "From French bienvenue, from bien 'well' + venue 'come' (past participle of venir)",
            "memory_tip": "BIENVENUE: Being welcomed - In French language, Everyone makes visitors feel welcomed, Nice greeting, Very European hospitality, Everyone Needs welcome, Understanding hospitality, Especially for women",
            "example_sentence": "The hostess said '_____ madame' as she showed the guest to her table.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bier",
            "definition": "A stand for holding a coffin or casket during a funeral",
            "pronunciation": "/bɪr/",
            "etymology": "From Old English bær meaning 'stretcher, litter', from Proto-Germanic baira",
            "memory_tip": "BIER: Basic Important - Equipment at funerals, Respectful ceremony stand",
            "example_sentence": "The flowers were arranged around the _____ during the memorial service.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bifurcate",
            "definition": "To divide into two branches or forks; to split",
            "pronunciation": "/ˈbaɪfərˌkeɪt/",
            "etymology": "From Latin bifurcus meaning 'two-forked', from bi- 'two' + furca 'fork'",
            "memory_tip": "BIFURCATE: Both Important - Forks splitting into branches, Understanding divisions, Recognizes splits, Creating And Two sections, Always Totally Everywhere splits happen",
            "example_sentence": "The river began to _____ into two separate streams near the delta.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bifurcatedrivel",
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
            "word": "bigotry",
            "definition": "Intolerance toward those who hold different opinions; prejudice",
            "pronunciation": "/ˈbɪɡətri/",
            "etymology": "From bigot + -ry, where bigot possibly comes from Old French, meaning 'sanctimonious person'",
            "memory_tip": "BIGOTRY: Bad Intolerance - Greed and hatred, Offensive Thinking, Really harmful attitude, Your mind closed to others",
            "example_sentence": "The organization worked to combat _____ and promote understanding between communities.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bijouterie",
            "definition": "Small decorative objects; jewelry and trinkets collectively",
            "pronunciation": "/ˌbiʒuˈtəri/",
            "etymology": "From French bijouterie, from bijou 'jewel' + -erie suffix indicating a place or collection",
            "memory_tip": "BIJOUTERIE: Beautiful Important - Jewelry Objects, Usually decorative items, Outstanding Treasures, Everyone Recognizes their sparkle, Important Expensive items",
            "example_sentence": "The boutique specialized in exquisite _____ from local artisans.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bike",
            "definition": "Short for bicycle; a two-wheeled vehicle powered by pedaling",
            "pronunciation": "/baɪk/",
            "etymology": "Shortened form of bicycle, from Greek bi- 'two' + kyklos 'circle, wheel'",
            "memory_tip": "BIKE: Basic Important - transportation vehicle, Keeping Everyone moving, Everyone rides these vehicles",
            "example_sentence": "She rode her _____ to work every day to stay fit and avoid traffic.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bilaterian",
            "definition": "An animal with bilateral symmetry (left and right sides mirror each other)",
            "pronunciation": "/ˌbaɪləˈtɪriən/",
            "etymology": "From bilateral + -ian, where bilateral comes from Latin bi- 'two' + latus 'side'",
            "memory_tip": "BILATERIAN: Both Important - Left And right sides mirror each other, Totally Even anatomy, Every animal part Reflects symmetrically, In Amazing Natural symmetry",
            "example_sentence": "Most complex animals are _____ organisms with distinct left and right sides.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bilbo",
            "definition": "A type of flexible sword blade; iron shackles for prisoners",
            "pronunciation": "/ˈbɪlboʊ/",
            "etymology": "From Bilbao, Spain, where high-quality sword blades were manufactured",
            "memory_tip": "BILBO: Blade Important - Long Blade weapon, Outstanding sword quality from spain",
            "example_sentence": "The museum displayed an antique _____ sword from 16th-century Spain.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bilge",
            "definition": "The lowest part of a ship's hull; nonsense or worthless talk",
            "pronunciation": "/bɪldʒ/",
            "etymology": "From Middle English bilge, probably from Old French bouge 'leather bag, curved part'",
            "memory_tip": "BILGE: Bottom Important - Location on ships, Getting water accumulated, Everything flows down there",
            "example_sentence": "The crew had to pump water from the ship's _____ after the storm.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "billabong",
            "definition": "An isolated water pool left by a receding river; an Australian term",
            "pronunciation": "/ˈbɪləˌbɔŋ/",
            "etymology": "From Australian Aboriginal languages, possibly Wiradjuri bilabang",
            "memory_tip": "BILLABONG: Beautiful Important - Lakes And water Bodies, Outstanding Natural Australian feature, Never connected to main river, Great water source",
            "example_sentence": "The kangaroos came to drink at the _____ during the dry season.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "billboard",
            "definition": "A large outdoor advertising display",
            "pronunciation": "/ˈbɪlˌbɔrd/",
            "etymology": "From bill (poster, advertisement) + board, referring to a board for posting bills",
            "memory_tip": "BILLBOARD: Big Important - Large advertising Board, Outstanding Advertising, Always Really visible, Driving past these large signs",
            "example_sentence": "The new _____ advertised the upcoming concert along the highway.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "billiards",
            "definition": "A cue sport played on a table with balls and a cue stick",
            "pronunciation": "/ˈbɪljərdz/",
            "etymology": "From French billard, from bille 'ball' + -ard suffix",
            "memory_tip": "BILLIARDS: Balls Important - Like cue sports, Learning tactics, Indoor game, Amazing Recreation, Demanding skill, Strategy games",
            "example_sentence": "The gentlemen's club had a beautiful mahogany _____ table.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "billingsgate",
            "definition": "Coarse or abusive language; foul-mouthed speech",
            "pronunciation": "/ˈbɪlɪŋzˌɡeɪt/",
            "etymology": "From Billingsgate, a London fish market known for the coarse language of its vendors",
            "memory_tip": "BILLINGSGATE: Bad Inappropriate - Language, Lots of Inappropriate speech, Nasty cursing and crude language, Generally Shocking language, Aggressive Talking, Extremely crude speech",
            "example_sentence": "The politician's speech was criticized for its _____ rather than substantive arguments.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "billow",
            "definition": "A large wave or surge; to swell outward like a sail",
            "pronunciation": "/ˈbɪloʊ/",
            "etymology": "From Old Norse bylgja meaning 'wave', related to 'to swell'",
            "memory_tip": "BILLOW: Big Important - Large wave motion, Like sails, Outward swelling, Wind fills fabric",
            "example_sentence": "The curtains began to _____ in the strong breeze from the open window.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "billy",
            "definition": "A metal pot or can for outdoor cooking; a police baton",
            "pronunciation": "/ˈbɪli/",
            "etymology": "Possibly from the name Billy, or from French bouilli 'boiled'",
            "memory_tip": "BILLY: Basic Important - Lightweight cooking pot, Lots of outdoor use, Years of camping cooking",
            "example_sentence": "The campers heated water for tea in their old _____ over the campfire.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biltong",
            "definition": "Dried and cured meat, similar to jerky, from Southern Africa",
            "pronunciation": "/ˈbɪlˌtɔŋ/",
            "etymology": "From Afrikaans biltong, from Dutch bil 'buttock' + tong 'tongue, strip'",
            "memory_tip": "BILTONG: Basic Important - Long preserved meat, Tough dried food, Outstanding Natural preservation, Great protein source",
            "example_sentence": "The hikers packed _____ as a high-protein snack for their trek.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "binary",
            "definition": "Consisting of two parts; relating to a number system with only 0 and 1",
            "pronunciation": "/ˈbaɪnəri/",
            "etymology": "From Latin binarius meaning 'consisting of two', from bini 'two by two'",
            "memory_tip": "BINARY: Basic Important - Numbers And computer systems, Always two choices, Really basic computer language, Yes/no decisions",
            "example_sentence": "Computer programmers work with _____ code consisting of ones and zeros.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bindi",
            "definition": "A decorative dot worn on the forehead in Hindu and Buddhist traditions",
            "pronunciation": "/ˈbɪndi/",
            "etymology": "From Hindi bindu meaning 'drop, dot', from Sanskrit binduka",
            "memory_tip": "BINDI: Beautiful Important - Nice cultural decoration, Decorative religious symbol, Indian traditional forehead marking",
            "example_sentence": "She wore a red _____ that complemented her traditional sari.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bingo",
            "definition": "A game of chance using numbered cards; an exclamation of success",
            "pronunciation": "/ˈbɪŋɡoʊ/",
            "etymology": "Possibly from the exclamation 'bang' + -o, or imitative of the sound of a bell",
            "memory_tip": "BINGO: Basic Interesting - Numbers Game, Great fun, Outstanding social activity",
            "example_sentence": "She shouted '____!' when she completed a row on her card.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "binoculars",
            "definition": "An optical instrument with lenses for both eyes, used for viewing distant objects",
            "pronunciation": "/bɪˈnɑkjələrz/",
            "etymology": "From French binoculaire, from Latin bini 'two' + oculus 'eye'",
            "memory_tip": "BINOCULARS: Both Important - Nearby Objects seen Clearly, Understanding far objects, Looking Around from Reasonable distance, Seeing everything clearly",
            "example_sentence": "The birdwatcher used her _____ to observe the eagles in their nest.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "binomial",
            "definition": "Consisting of two terms; in biology, a two-part scientific name",
            "pronunciation": "/baɪˈnoʊmiəl/",
            "etymology": "From Latin bi- 'two' + nomen 'name' + -al suffix",
            "memory_tip": "BINOMIAL: Both Important - Names Or scientific classification, Mathematical expressions, Important scientific naming, Always Learning biological classification",
            "example_sentence": "The _____ name for humans is Homo sapiens.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "binomialbiomimicry",
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
            "word": "binomialdifficulty",
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
            "word": "binturong",
            "definition": "A tree-dwelling mammal from Southeast Asia, also called a bearcat",
            "pronunciation": "/ˈbɪntəˌrɔŋ/",
            "etymology": "From Malay binturong, the native name for the animal",
            "memory_tip": "BINTURONG: Beautiful Important - National animal from southeast asia, Tree climbing animal, Understanding forest animals, Really Outstanding climbing, Nice Gentle animal",
            "example_sentence": "The _____ is known for its prehensile tail and distinctive musky scent.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biology",
            "definition": "The scientific study of living organisms and life processes",
            "pronunciation": "/baɪˈɑlədʒi/",
            "etymology": "From Greek bios 'life' + -logia 'study of'",
            "memory_tip": "BIOLOGY: Basic Important - Operating principles of Living organisms, Outstanding Great science, Yeast and all living things",
            "example_sentence": "She majored in _____ to pursue her dream of becoming a marine researcher.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biome",
            "definition": "A large naturally occurring community of flora and fauna",
            "pronunciation": "/ˈbaɪoʊm/",
            "etymology": "From Greek bios 'life' + -ome 'mass, group'",
            "memory_tip": "BIOME: Basic Important - area, Outstanding natural environment, Many species live together, Ecosystems everywhere",
            "example_sentence": "The rainforest _____ supports incredible biodiversity.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biomimicry",
            "definition": "The design of materials and systems modeled on biological processes",
            "pronunciation": "/ˌbaɪoʊˈmɪmɪkri/",
            "etymology": "From Greek bios 'life' + mimesis 'imitation' + -ry suffix",
            "memory_tip": "BIOMIMICRY: Biology Inspired - Outstanding technology, Mimicking nature's solutions, Including perfect animal designs, Making Industrial innovations, Copying natural solutions, Really smart engineering, Yes nature-inspired inventions",
            "example_sentence": "Velcro was invented through _____, inspired by how burr seeds stick to animal fur.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bird",
            "definition": "A warm-blooded vertebrate animal with feathers, wings, and a beak",
            "pronunciation": "/bɜrd/",
            "etymology": "From Old English bridd meaning 'young bird, chick'",
            "memory_tip": "BIRD: Beautiful Important - Really Diverse flying animals",
            "example_sentence": "The colorful _____ sang beautifully from its perch in the oak tree.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "birdie",
            "definition": "In golf, one stroke under par; informal term for a small bird",
            "pronunciation": "/ˈbɜrdi/",
            "etymology": "From bird + -ie diminutive suffix, originally referring to something excellent",
            "memory_tip": "BIRDIE: Better Important - Result in golf, Doing golf one stroke under par, In Everyone's golf vocabulary, Everyone celebrates this golf score",
            "example_sentence": "He made a _____ on the difficult par-4 hole with a perfect approach shot.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_020_processed.csv"
    
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
        
        print(f"Batch 020 processing complete!")
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