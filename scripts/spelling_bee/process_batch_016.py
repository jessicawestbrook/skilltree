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
            "word": "badger",
            "definition": "A burrowing mammal with distinctive black and white stripes; to persistently ask or pester",
            "pronunciation": "/ˈbædʒər/",
            "etymology": "From Middle English bageard, possibly from badge (referring to the white mark on its forehead) + -ard suffix",
            "memory_tip": "BADGER: Bold Animal Digging - Great Earth tunneler, Relentlessly asks questions",
            "example_sentence": "The persistent reporter continued to _____ the politician for answers about the scandal.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "badgerbailiff",
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
            "word": "badinage",
            "definition": "Humorous or witty conversation; playful repartee",
            "pronunciation": "/ˌbædɪˈnɑʒ/",
            "etymology": "From French badinage, from badiner 'to jest', from badin 'silly, playful'",
            "memory_tip": "BADINAGE: Banter And Delightful - Intelligent playful conversation, Nice And Graceful Exchange",
            "example_sentence": "The dinner party was filled with clever _____ between the witty guests.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baggy",
            "definition": "Loose-fitting and hanging in folds; not tight",
            "pronunciation": "/ˈbæɡi/",
            "etymology": "From bag + -y suffix, referring to clothing that hangs like a bag",
            "memory_tip": "BAGGY: Big And Generously sized - Garments hang loosely, not tight, Yielding comfortable fit",
            "example_sentence": "The oversized _____ jeans were popular in the 1990s fashion trend.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bagpipe",
            "definition": "A musical instrument with pipes that are sounded by air squeezed from a bag",
            "pronunciation": "/ˈbæɡˌpaɪp/",
            "etymology": "From bag + pipe, referring to the air bag and the pipes that produce sound",
            "memory_tip": "BAGPIPE: Bag And Great - Pipes produce music, Inspiring musical Performances, Everybody loves Scottish music",
            "example_sentence": "The Scottish _____ player filled the Highland air with traditional melodies.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bagwyn",
            "definition": "A heraldic creature resembling a deer or goat with curved horns and a long tail",
            "pronunciation": "/ˈbæɡwɪn/",
            "etymology": "From Welsh bagwyn, possibly from bag 'testicle' + gwyn 'white', referring to the creature's appearance",
            "memory_tip": "BAGWYN: Blazoned Animal - Graceful Welsh heraldic creature, Yielding distinctive Noble appearance",
            "example_sentence": "The family coat of arms featured a _____ as their heraldic symbol.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bahamas",
            "definition": "An island nation in the Atlantic Ocean southeast of Florida",
            "pronunciation": "/bəˈhɑməz/",
            "etymology": "From Spanish baja mar meaning 'shallow water', referring to the shallow seas around the islands",
            "memory_tip": "BAHAMAS: Beautiful Atlantic - Heavenly Archipelago of Many Amazing tropical islands, Stunning beaches",
            "example_sentence": "The cruise ship sailed through the crystal-clear waters of the _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bahr",
            "definition": "An Arabic word meaning 'sea' or 'large river', used in place names",
            "pronunciation": "/bɑr/",
            "etymology": "From Arabic bahr meaning 'sea, large river'",
            "memory_tip": "BAHR: Big Arabic water - Huge Rivers in Middle Eastern geography",
            "example_sentence": "The ancient city was located near _____ el-nil, the great river.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bahuvrihi",
            "definition": "A type of compound word where the meaning refers to something outside the compound itself",
            "pronunciation": "/bɑhuˈvrihi/",
            "etymology": "From Sanskrit bahuvrihi meaning 'having much rice', which is itself an example of this type of compound",
            "memory_tip": "BAHUVRIHI: Big And complex - Having Unusual Verbal structure, Referring to something outside the compound, Highly technical linguistic term, Impressive grammatical concept",
            "example_sentence": "The term 'redhead' is a _____ compound because it refers to a person, not a head.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bahuvrihipanjandrum",
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
            "word": "bailiff",
            "definition": "A court officer who maintains order and serves legal papers; a sheriff's deputy",
            "pronunciation": "/ˈbeɪlɪf/",
            "etymology": "From Old French baillif, from bailler 'to deliver, control', from Latin bajulare 'to bear a burden'",
            "memory_tip": "BAILIFF: Bravely Always - Insuring Law Is properly followed - Firmly maintaining court order",
            "example_sentence": "The _____ escorted the defendant from the courtroom after the verdict.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bailiffinfiltrate",
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
            "word": "bailiwick",
            "definition": "A person's area of skill, knowledge, or authority; a bailiff's jurisdiction",
            "pronunciation": "/ˈbeɪlɪˌwɪk/",
            "etymology": "From bailiff + wick (Old English wic meaning 'dwelling place, jurisdiction')",
            "memory_tip": "BAILIWICK: Bailiff's Area - Interests Leading to Individual areas of expertise, With Initial expertise, Control, Knowledge areas",
            "example_sentence": "Computer programming was clearly his _____ among the team members.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bailly",
            "definition": "The outer wall or ward of a castle; a fortified enclosure",
            "pronunciation": "/ˈbeɪli/",
            "etymology": "From Old French baile meaning 'enclosure', from Latin bajulus 'carrier, manager'",
            "memory_tip": "BAILLY: Barrier Around - Inside castle, Lined wall Yielding protection",
            "example_sentence": "The soldiers defended the castle's _____ against the approaching enemy forces.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bakery",
            "definition": "A place where bread and cakes are made or sold",
            "pronunciation": "/ˈbeɪkəri/",
            "etymology": "From bake + -ery suffix, referring to a place where baking occurs",
            "memory_tip": "BAKERY: Bread And Kneaded dough - Everyone Relies on for fresh baked goods, Yummy treats",
            "example_sentence": "The local _____ filled the street with the aroma of fresh-baked croissants.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bakeryporridge",
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
            "word": "baklava",
            "definition": "A rich sweet pastry made of layers of filo filled with chopped nuts and honey",
            "pronunciation": "/ˈbɑkləvə/",
            "etymology": "From Turkish baklava, possibly from Ottoman Turkish baklavak",
            "memory_tip": "BAKLAVA: Beautiful And Krunchy - Layers And Vibrant honey sweetness, Amazing dessert",
            "example_sentence": "The _____ was perfectly flaky with layers of phyllo pastry and chopped walnuts.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baklawa",
            "definition": "Alternative spelling of baklava, a Middle Eastern layered pastry dessert",
            "pronunciation": "/ˈbɑkləwə/",
            "etymology": "From Arabic baqlawa, related to Turkish baklava",
            "memory_tip": "BAKLAWA: Beautiful Arabic - Krunchy Layers And sweet honey, Wonderful Alternative spelling",
            "example_sentence": "The Lebanese restaurant served traditional _____ with pistachios and rose water syrup.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "balance",
            "definition": "A state of equilibrium; to keep steady or in proportion",
            "pronunciation": "/ˈbæləns/",
            "etymology": "From Old French balance, from Latin bilanx meaning 'having two scales', from bi- 'two' + lanx 'scale pan'",
            "memory_tip": "BALANCE: Being Able to Land Accurately - Neutralizing uneven forces, Coordinating Evenly",
            "example_sentence": "She worked hard to _____ her career responsibilities with family time.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "balata",
            "definition": "A type of rubber obtained from a South American tree; the tree that produces this rubber",
            "pronunciation": "/bəˈlɑtə/",
            "etymology": "From Spanish balata, from Taíno or another indigenous Caribbean language",
            "memory_tip": "BALATA: Bouncy And Latex - Amazonian Tree producing rubber, Amazing tree sap",
            "example_sentence": "The golf ball was made from _____ rubber for better durability and performance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "balbriggan",
            "definition": "A type of fine, unbleached knitted cotton fabric; underwear made from this fabric",
            "pronunciation": "/bælˈbrɪɡən/",
            "etymology": "From Balbriggan, a town in Ireland where this type of cotton fabric was originally manufactured",
            "memory_tip": "BALBRIGGAN: Beautiful And Light - Breathable fabric Really Is Great for underGarments, And comfy, Natural cotton material",
            "example_sentence": "The vintage _____ undershirt was prized for its softness and breathability.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "balderdash",
            "definition": "Senseless talk or writing; nonsense",
            "pronunciation": "/ˈbɔldərˌdæʃ/",
            "etymology": "Origin uncertain, possibly from a mixture of liquors, later extended to mean 'nonsense'",
            "memory_tip": "BALDERDASH: Babble And Lies - Definitely Ridiculous statements, Absolutely Senseless talk, Hogwash",
            "example_sentence": "The professor dismissed the student's theory as complete _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baleen",
            "definition": "Flexible plates hanging from the upper jaws of certain whales, used for filtering food",
            "pronunciation": "/bəˈlin/",
            "etymology": "From Old French baleine meaning 'whale', from Latin balaena 'whale'",
            "memory_tip": "BALEEN: Big Animals - Large whales use for Eating tiny organisms, Efficiently filtering, Natural strainer",
            "example_sentence": "The humpback whale used its _____ to filter krill and small fish from the seawater.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballabile",
            "definition": "A piece of music suitable for dancing; a dance movement in a ballet or opera",
            "pronunciation": "/ˌbæləˈbilə/",
            "etymology": "From Italian ballabile meaning 'suitable for dancing', from ballare 'to dance'",
            "memory_tip": "BALLABILE: Beautiful And Lively - Lovely And Bouncy dance music, Inspiring Lively movement, Everyone dances",
            "example_sentence": "The opera's second act featured a delightful _____ that showcased the corps de ballet.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballad",
            "definition": "A narrative song or poem, often romantic or tragic; a slow sentimental song",
            "pronunciation": "/ˈbæləd/",
            "etymology": "From Old French balade, from Provençal balada meaning 'dancing song', from balar 'to dance'",
            "memory_tip": "BALLAD: Beautiful And Lyrical - Lovely And emotional story, Deeply touching music",
            "example_sentence": "The folk singer performed a haunting _____ about lost love.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballast",
            "definition": "Heavy material placed in a ship or vehicle for stability; something that provides stability",
            "pronunciation": "/ˈbæləst/",
            "etymology": "From Low German or Scandinavian, possibly from bare 'bare' + last 'load'",
            "memory_tip": "BALLAST: Big And Loaded - Lots of weight Added for Stability, Thick heavy material",
            "example_sentence": "The ship took on water as _____ to lower its center of gravity.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballerina",
            "definition": "A female ballet dancer, especially a principal dancer",
            "pronunciation": "/ˌbæləˈrinə/",
            "etymology": "From Italian ballerina, feminine of ballerino, from ballare 'to dance'",
            "memory_tip": "BALLERINA: Beautiful And Lovely - Leaping Elegantly, Remarkably Inspiring graceful dancing, Natural Artist",
            "example_sentence": "The prima _____ performed the lead role in Swan Lake with extraordinary grace.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballistic",
            "definition": "Relating to projectiles or their flight; extremely angry or agitated",
            "pronunciation": "/bəˈlɪstɪk/",
            "etymology": "From Latin ballista meaning 'military engine for hurling stones', from Greek ballein 'to throw'",
            "memory_tip": "BALLISTIC: Bullets And Launch - Launched In Straight trajectory, extremely mad, Intense Calculated motion",
            "example_sentence": "The forensic expert analyzed the _____ evidence to determine the bullet's trajectory.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "balloon",
            "definition": "An inflatable rubber or plastic bag; a large bag filled with hot air for flying",
            "pronunciation": "/bəˈlun/",
            "etymology": "From French ballon meaning 'large ball', from Italian ballone, augmentative of balla 'ball'",
            "memory_tip": "BALLOON: Big Air - Lifting Lovely colorful sphere, Offering fun, Natural floating",
            "example_sentence": "The colorful _____ floated high above the carnival grounds.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballotage",
            "definition": "A second round of voting when no candidate receives a majority in the first round",
            "pronunciation": "/ˈbæləˌtɑʒ/",
            "etymology": "From French ballottage, from ballotter 'to toss about, vote by ballot'",
            "memory_tip": "BALLOTAGE: Balloting Again - Lacking Leaders with enough majority, Open To Another Go, Everyone votes again",
            "example_sentence": "The presidential election required a _____ between the two leading candidates.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballroom",
            "definition": "A large room used for dancing; a style of formal partner dancing",
            "pronunciation": "/ˈbɔlˌrum/",
            "etymology": "From ball (formal dance) + room, where ball comes from French bal",
            "memory_tip": "BALLROOM: Beautiful And Large - Luxurious space for dancing, Refined Organized social events, Outstanding Magnificent venue",
            "example_sentence": "The elegant _____ was decorated with crystal chandeliers for the charity gala.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ballyhooed",
            "definition": "Publicized or promoted with exaggerated or sensational claims",
            "pronunciation": "/ˈbæliˌhud/",
            "etymology": "From ballyhoo (possibly from ballyhooley, a town in Ireland) + -ed, meaning extravagant publicity",
            "memory_tip": "BALLYHOOED: Big Advertising - Loudly Yelling to promote, Highly Overstated, Overdone promotion, Everything Dramatized",
            "example_sentence": "The _____ restaurant failed to live up to its exaggerated reputation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "balsamic",
            "definition": "Relating to balsam; describing a type of dark, sweet Italian vinegar",
            "pronunciation": "/bɔlˈsæmɪk/",
            "etymology": "From Latin balsamum meaning 'balsam', from Greek balsamon 'balsam tree'",
            "memory_tip": "BALSAMIC: Beautiful And Luscious - Sweet And flavorful Mediterranean vinegar, Italian Culinary ingredient",
            "example_sentence": "The salad was drizzled with aged _____ vinegar from Modena.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baltic",
            "definition": "Relating to the Baltic Sea or the region around it",
            "pronunciation": "/ˈbɔltɪk/",
            "etymology": "From Medieval Latin balticus, possibly from a Germanic source related to 'belt'",
            "memory_tip": "BALTIC: Big And Large - The Incredible Cold northern sea region",
            "example_sentence": "The _____ states gained independence from the Soviet Union in the early 1990s.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bamboozled",
            "definition": "Deceived or cheated through trickery; confused or bewildered",
            "pronunciation": "/bæmˈbuzəld/",
            "etymology": "Origin uncertain, possibly from French embabouiner 'to make a baboon of'",
            "memory_tip": "BAMBOOZLED: Been A victim - Made Bewildered, Obviously fooled, Outwitted, Zealously tricked, Led Entirely astray, Deceived",
            "example_sentence": "The tourists were _____ by the street vendor's clever shell game.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "banal",
            "definition": "Lacking originality or freshness; dull and commonplace",
            "pronunciation": "/bəˈnɑl/",
            "etymology": "From French banal meaning 'commonplace', from ban 'feudal service' + -al",
            "memory_tip": "BANAL: Boring And Not - Amazing or Lovely, totally ordinary and predictable",
            "example_sentence": "The movie's _____ plot failed to capture the audience's attention.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "banana",
            "definition": "A long curved fruit with a yellow skin when ripe",
            "pronunciation": "/bəˈnænə/",
            "etymology": "From Spanish/Portuguese banana, possibly from a West African language",
            "memory_tip": "BANANA: Bright And Natural - Always Nutritious tasty fruit, Always sweet",
            "example_sentence": "She packed a _____ in her lunch for a healthy potassium-rich snack.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bandage",
            "definition": "A strip of material used to bind up a wound or injury",
            "pronunciation": "/ˈbændɪdʒ/",
            "etymology": "From French bandage, from bande 'strip, band' + -age suffix",
            "memory_tip": "BANDAGE: Binding And Neat - Dressing And covering wounds, Great Effective medical covering",
            "example_sentence": "The nurse applied a clean _____ to the patient's injured arm.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bandana",
            "definition": "A large colored handkerchief, typically worn around the neck or head",
            "pronunciation": "/bænˈdænə/",
            "etymology": "From Hindi bandhana meaning 'to tie', from bandhna 'to bind'",
            "memory_tip": "BANDANA: Bright And Nice - Decorative And Neat head covering, Always colorful",
            "example_sentence": "The cowboy tied a red _____ around his neck to protect against dust.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bandanna",
            "definition": "Alternative spelling of bandana - a large colored handkerchief",
            "pronunciation": "/bænˈdænə/",
            "etymology": "From Hindi bandhana meaning 'to tie', from bandhna 'to bind'",
            "memory_tip": "BANDANNA: Bright And Nice - Decorative And Neat head covering, Natural Alternative spelling",
            "example_sentence": "She wore a paisley _____ to keep her hair out of her face while gardening.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bandicoot",
            "definition": "A small marsupial native to Australia and New Guinea with a long snout",
            "pronunciation": "/ˈbændɪˌkut/",
            "etymology": "From Telugu pandikokku, from pandi 'pig' + kokku 'rat'",
            "memory_tip": "BANDICOOT: Big Australian - Native Digger creature, Interesting Cute marsupial, Outstanding burrowing, Tiny pouch mammal",
            "example_sentence": "The _____ emerged from its burrow at dusk to search for insects and grubs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bandits",
            "definition": "Plural of bandit; robbers or outlaws who attack travelers",
            "pronunciation": "/ˈbændɪts/",
            "etymology": "From Italian bandito meaning 'banished', from bandire 'to banish'",
            "memory_tip": "BANDITS: Bad And Notorious - Dangerous criminals, Infamous Thieves, Stealing everything",
            "example_sentence": "The stagecoach was attacked by _____ seeking to steal the passengers' valuables.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bandmates",
            "definition": "Fellow members of a musical band",
            "pronunciation": "/ˈbændˌmeɪts/",
            "etymology": "From band + mates, where band refers to a musical group",
            "memory_tip": "BANDMATES: Brothers And musicians - Nice Diverse group, Music friends And Teammates, Everyone plays music, Sharing musical talents",
            "example_sentence": "The drummer got along well with all of his _____ in the rock band.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bango",
            "definition": "A type of traditional African musical instrument similar to a banjo",
            "pronunciation": "/ˈbæŋɡoʊ/",
            "etymology": "From African origin, possibly related to various West African stringed instruments",
            "memory_tip": "BANGO: Beautiful African - Native music, Great Orchestral stringed instrument",
            "example_sentence": "The musician played traditional melodies on his handcrafted _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "banh",
            "definition": "Vietnamese word for cake or bread, used in names of Vietnamese dishes",
            "pronunciation": "/bɑn/",
            "etymology": "From Vietnamese bánh meaning 'cake, bread, pastry'",
            "memory_tip": "BANH: Beautiful Asian - Nutritious Vietnamese bread, Happy food traditions",
            "example_sentence": "The restaurant served _____ mi sandwiches with pickled vegetables and cilantro.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "banishment",
            "definition": "The action of sending someone away as a punishment; exile",
            "pronunciation": "/ˈbænɪʃmənt/",
            "etymology": "From Old French banissement, from banir 'to banish' + -ment suffix",
            "memory_tip": "BANISHMENT: Banned And - Never Invited back, Sent away Horribly, Miserable Exile, No more home, Total separation",
            "example_sentence": "The king decreed _____ as punishment for treason against the crown.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bankrupt",
            "definition": "Unable to pay debts; completely lacking in a particular good quality",
            "pronunciation": "/ˈbæŋkˌrʌpt/",
            "etymology": "From Italian banca rotta meaning 'broken bench', referring to the practice of breaking a moneylender's bench when they failed",
            "memory_tip": "BANKRUPT: Broke And - No money or resources to keep going, Really Utterly Poor, Total failure",
            "example_sentence": "The company went _____ after years of declining sales and mounting debts.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "banners",
            "definition": "Plural of banner; flags or signs displayed for decoration or advertisement",
            "pronunciation": "/ˈbænərz/",
            "etymology": "From Old French baniere, from ban 'summons' + -iere suffix",
            "memory_tip": "BANNERS: Bright And Noticeable - Decorative flags, Everyone Recognizes these Signs",
            "example_sentence": "Colorful _____ hung across the street to celebrate the town's annual festival.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bannock",
            "definition": "A type of flatbread originally from Scotland, often baked on a griddle",
            "pronunciation": "/ˈbænək/",
            "etymology": "From Scottish Gaelic bannach meaning 'cake', possibly from Latin panicium 'bread'",
            "memory_tip": "BANNOCK: Bread And - Nice homemade griddle bread, Nutritious Old Scottish flatbread, Creative Kitchen bread",
            "example_sentence": "The campers cooked _____ over the open fire for their evening meal.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "banquet",
            "definition": "A formal dinner for many people in celebration of a special occasion",
            "pronunciation": "/ˈbæŋkwɪt/",
            "etymology": "From Old French banquet, diminutive of banc 'bench', referring to a small table or feast",
            "memory_tip": "BANQUET: Big And Numerous - Qualité eating feast, Upscale Event, Tables full of special food",
            "example_sentence": "The annual awards _____ honored the company's top-performing employees.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_016_processed.csv"
    
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
        
        print(f"Batch 016 processing complete!")
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