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
            "word": "blouse",
            "definition": "A woman's loose-fitting upper garment, typically worn with a skirt or pants",
            "pronunciation": "/blaʊs/",
            "etymology": "From French blouse, possibly from Provençal bluco meaning 'blue'",
            "memory_tip": "BLOUSE: Beautiful Light - Outfit for women, Usually worn with Stylish pants, Everyone recognizes this clothing",
            "example_sentence": "She wore a silk _____ to the business meeting.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bloviate",
            "definition": "To talk at length in a pompous or boastful manner",
            "pronunciation": "/ˈbloʊviˌeɪt/",
            "etymology": "Possibly a blend of blow + deviate, coined in American slang",
            "memory_tip": "BLOVIATE: Blowing hot air - Long-winded talking, Obviously Verbose, Irritating And Totally Empty speech",
            "example_sentence": "The politician continued to _____ about his achievements without substance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blue",
            "definition": "A color between green and violet in the spectrum; sad or melancholy",
            "pronunciation": "/blu/",
            "etymology": "From Old French bleu, from Germanic origin",
            "memory_tip": "BLUE: Beautiful Light - color, Usually associated with sky, Everyone knows this primary color",
            "example_sentence": "The _____ sky stretched endlessly over the ocean.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blurb",
            "definition": "A short description of a book or other product for promotional purposes",
            "pronunciation": "/blɜrb/",
            "etymology": "Coined by American humorist Gelett Burgess in 1907",
            "memory_tip": "BLURB: Brief Little - Understanding a book, Reads like a summary, Brief description",
            "example_sentence": "The _____ on the back cover convinced her to buy the mystery novel.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blurtedwallet",
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
            "word": "blustery",
            "definition": "Characterized by strong winds; aggressively boastful",
            "pronunciation": "/ˈblʌstəri/",
            "etymology": "From bluster + -y, where bluster comes from Middle Low German blusteren 'to blow violently'",
            "memory_tip": "BLUSTERY: Blowing Like - windy weather, Usually Stormy weather, Totally Extremely windy, Really windy day, Year-round weather pattern",
            "example_sentence": "The _____ March wind made it difficult to walk outside.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "board",
            "definition": "A flat piece of wood or other material; a group that manages an organization",
            "pronunciation": "/bɔrd/",
            "etymology": "From Old English bord meaning 'plank, table', from Proto-Germanic burdam",
            "memory_tip": "BOARD: Basic Object - Always used for building, Rectangular flat material, Durable construction material",
            "example_sentence": "The _____ of directors met to discuss the company's future.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boarders",
            "definition": "People who live in someone else's house for payment; students who live at school",
            "pronunciation": "/ˈbɔrdərz/",
            "etymology": "From board + -er + -s, referring to those who receive board (meals and lodging)",
            "memory_tip": "BOARDERS: Basic Organization - And paying renters, Renting Dormitory space, Everyone Receiving housing, Staying at school",
            "example_sentence": "The _____ at the boarding school were required to follow strict curfew rules.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boats",
            "definition": "Watercraft designed for transportation or recreation on water",
            "pronunciation": "/boʊts/",
            "etymology": "From Old English bat, from Proto-Germanic baitaz",
            "memory_tip": "BOATS: Big Objects - Always Transport people, Sailing everywhere on water",
            "example_sentence": "The harbor was filled with fishing _____ preparing for the morning catch.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boba",
            "definition": "Tapioca pearls used in bubble tea drinks, originally from Taiwan",
            "pronunciation": "/ˈboʊbə/",
            "etymology": "From Chinese bōbà meaning 'bubble tea', referring to the tapioca pearls",
            "memory_tip": "BOBA: Bubble Objects - Bouncy Asian treats, Amazing tea drink addition",
            "example_sentence": "She ordered a taro _____ tea with extra chewy pearls.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bobcat",
            "definition": "A North American wild cat with a short tail and tufted ears",
            "pronunciation": "/ˈbɑbˌkæt/",
            "etymology": "From bob (short) + cat, referring to its short bobbed tail",
            "memory_tip": "BOBCAT: Big Outdoor - Bold wild cat, Always Territorial predator",
            "example_sentence": "The _____ silently stalked through the forest undergrowth.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bobolink",
            "definition": "A migratory songbird of North America with distinctive plumage",
            "pronunciation": "/ˈboʊboʊˌlɪŋk/",
            "etymology": "Imitative of the bird's call, first recorded in 1796",
            "memory_tip": "BOBOLINK: Beautiful Outdoor - Bird that sings, Outstanding musical bird, Lovely musical singing, Including Natural melodic songs, Nice Keeping everyone listening",
            "example_sentence": "The _____ sang its melodious song from the meadow grass.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bodega",
            "definition": "A small neighborhood store, especially in Hispanic communities",
            "pronunciation": "/boʊˈdeɪɡə/",
            "etymology": "From Spanish bodega meaning 'wine cellar' or 'storeroom'",
            "memory_tip": "BODEGA: Basic Organization - Delivering Essential Groceries, Always neighborhood store",
            "example_sentence": "He stopped at the corner _____ to buy milk and newspapers.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bodhran",
            "definition": "A traditional Irish frame drum played with a wooden stick",
            "pronunciation": "/ˈboʊrən/",
            "etymology": "From Irish bodhrán, possibly from bodhar meaning 'deaf' or 'dull sounding'",
            "memory_tip": "BODHRAN: Beautiful Old - Drum for traditional music, Historic Rhythmic percussion, And Nice traditional drumming",
            "example_sentence": "The musician played a haunting melody on the _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bodies",
            "definition": "Physical forms of people or animals; organized groups",
            "pronunciation": "/ˈbɑdiz/",
            "etymology": "From body + -ies, where body comes from Old English bodig",
            "memory_tip": "BODIES: Basic Objects - Describing Individual physical forms, Everyone has physical forms, Something everyone possesses",
            "example_sentence": "The ancient burial site contained several well-preserved _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bodkin",
            "definition": "A sharp, slender instrument for making holes; a large blunt needle",
            "pronunciation": "/ˈbɑdkɪn/",
            "etymology": "From Middle English bodekyn, possibly from Celtic origin",
            "memory_tip": "BODKIN: Basic Object - Designed for sewing, Keeping fabric pieces together, Including Needle-like tool",
            "example_sentence": "She used a _____ to thread the ribbon through the fabric eyelets.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boffin",
            "definition": "British slang for a scientist or technical expert",
            "pronunciation": "/ˈbɑfɪn/",
            "etymology": "British slang, possibly from the name of a character in a comic strip",
            "memory_tip": "BOFFIN: Brainy Outstanding - scientist, Frequently studying, Finding Important discoveries, Never stopping research",
            "example_sentence": "The brilliant _____ solved the complex engineering problem.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bogus",
            "definition": "Fake or fraudulent; not genuine",
            "pronunciation": "/ˈboʊɡəs/",
            "etymology": "American slang, possibly from a machine that made counterfeit coins",
            "memory_tip": "BOGUS: Bad Obviously - Getting everyone fooled, Utterly fake, Something completely false",
            "example_sentence": "The detective discovered the _____ documents were expertly forged.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bohemian",
            "definition": "A person with artistic or literary interests who lives unconventionally",
            "pronunciation": "/boʊˈhimiən/",
            "etymology": "From Bohemia (Czech region), referring to unconventional lifestyle",
            "memory_tip": "BOHEMIAN: Beautiful Outstanding - Highly creative person, Everyone Minds their artistic freedom, Interesting Artist, Never conventional lifestyle",
            "example_sentence": "The _____ artist lived in a colorful studio filled with paintings.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boiled",
            "definition": "Cooked in boiling water; heated to boiling point",
            "pronunciation": "/bɔɪld/",
            "etymology": "From boil + -ed, where boil comes from Old French boillir",
            "memory_tip": "BOILED: Basic Operation - In hot water, Liquid Extremely heated, Definitely cooked completely",
            "example_sentence": "She served _____ potatoes with butter and herbs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boise",
            "definition": "The capital city of Idaho; French word meaning 'wooded'",
            "pronunciation": "/ˈbɔɪsi/",
            "etymology": "From French boisé meaning 'wooded', referring to the area's trees",
            "memory_tip": "BOISE: Beautiful Outdoor - Idaho State capital, Surrounded by trees, Everyone knows this western city",
            "example_sentence": "The conference was held in downtown _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boiserie",
            "definition": "Ornate wood paneling used in interior decoration",
            "pronunciation": "/ˌbwɑzəˈri/",
            "etymology": "From French boiserie, from bois meaning 'wood'",
            "memory_tip": "BOISERIE: Beautiful Ornate - Interior decoration, Sophisticated Elaborate wood panels, Rich Impressive interior design, Everyone admires elegant woodwork",
            "example_sentence": "The palace's _____ featured intricate carved panels from the 18th century.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boisterous",
            "definition": "Noisy, energetic, and cheerful; rough or stormy",
            "pronunciation": "/ˈbɔɪstərəs/",
            "etymology": "From Middle English boisterous, possibly from boister meaning 'rough'",
            "memory_tip": "BOISTEROUS: Bold Outgoing - Individuals making noise, Spirited Totally Energetic people, Really Outgoing behavior, Utterly Spirited energy",
            "example_sentence": "The _____ children ran through the playground with endless energy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bold",
            "definition": "Showing courage and confidence; clearly visible or striking",
            "pronunciation": "/boʊld/",
            "etymology": "From Old English beald meaning 'brave, confident'",
            "memory_tip": "BOLD: Brave Outstanding - Leadership Demonstrated confidently",
            "example_sentence": "She made a _____ decision to start her own business.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bolide",
            "definition": "A large meteor that explodes in the atmosphere; a fireball",
            "pronunciation": "/ˈboʊlaɪd/",
            "etymology": "From Greek bolis meaning 'javelin' or 'missile'",
            "memory_tip": "BOLIDE: Bright Object - Like a meteor, Including Dramatic explosion, Everyone sees spectacular fireball",
            "example_sentence": "The _____ streaked across the night sky before exploding brilliantly.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bolognese",
            "definition": "A meat-based pasta sauce originating from Bologna, Italy",
            "pronunciation": "/ˌboʊləˈniz/",
            "etymology": "From Italian bolognese, meaning 'from Bologna', the Italian city",
            "memory_tip": "BOLOGNESE: Basic Outstanding - Long-cooked sauce, Outstanding Gourmet cooking, Never plain Eating, Superb European dish",
            "example_sentence": "The restaurant's _____ sauce simmered for hours with fresh herbs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bolts",
            "definition": "Metal fasteners with threaded ends; sudden movements or escapes",
            "pronunciation": "/boʊlts/",
            "etymology": "From Old English bolt meaning 'arrow' or 'missile'",
            "memory_tip": "BOLTS: Basic Objects - Linking Things together, Strong mechanical fasteners",
            "example_sentence": "The carpenter used steel _____ to secure the heavy wooden beams.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bombard",
            "definition": "To attack continuously with artillery; to assail persistently",
            "pronunciation": "/bɑmˈbɑrd/",
            "etymology": "From Old French bombarde, from Latin bombus meaning 'booming sound'",
            "memory_tip": "BOMBARD: Big Objects - Making explosive attacks, Bringing Artillery, Relentless attacking, Devastating military action",
            "example_sentence": "The reporters continued to _____ the politician with difficult questions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bombastic",
            "definition": "High-sounding but with little meaning; pompous or inflated in style",
            "pronunciation": "/bɑmˈbæstɪk/",
            "etymology": "From bombast (cotton padding) via Latin bombax 'silk', referring to inflated speech",
            "memory_tip": "BOMBASTIC: Big Obvious - Making impressive noise, Bragging And Speaking Theatrically, Inflated Communication",
            "example_sentence": "The speaker's _____ rhetoric impressed no one with its empty grandeur.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bona",
            "definition": "Genuine or real; part of the phrase 'bona fide' meaning authentic",
            "pronunciation": "/ˈboʊnə/",
            "etymology": "From Latin bona meaning 'good things' or 'goods'",
            "memory_tip": "BONA: Basic Original - Nothing fake, Always genuine and authentic",
            "example_sentence": "She was a _____ fide expert in marine biology.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bonanza",
            "definition": "A situation creating sudden wealth or luck; a rich source",
            "pronunciation": "/bəˈnænzə/",
            "etymology": "From Spanish bonanza meaning 'fair weather' or 'prosperity'",
            "memory_tip": "BONANZA: Big Outstanding - Newfound wealth, Amazing financial discovery, Never-ending good fortune, Zeal about sudden riches, Amazing prosperity",
            "example_sentence": "The discovery of oil created a _____ for the small desert town.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bones",
            "definition": "The hard structures that form the skeleton in vertebrates",
            "pronunciation": "/boʊnz/",
            "etymology": "From Old English ban, from Proto-Germanic bainam",
            "memory_tip": "BONES: Basic Objects - Never soft, Everyone has skeletal structure, Strong framework",
            "example_sentence": "The archaeologist carefully excavated the ancient _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bonfire",
            "definition": "A large outdoor fire for celebration or disposal of waste",
            "pronunciation": "/ˈbɑnˌfaɪər/",
            "etymology": "From bone + fire, originally referring to fires that burned bones",
            "memory_tip": "BONFIRE: Big Outdoor - Night celebration fire, Flames Inspiring everyone, Really spectacular burning, Everyone gathering around warmth",
            "example_sentence": "The beach _____ crackled as friends gathered to roast marshmallows.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boniface",
            "definition": "An innkeeper or hotel proprietor; a jovial host",
            "pronunciation": "/ˈbɑnəˌfeɪs/",
            "etymology": "From the character Boniface in Farquhar's play 'The Beaux' Stratagem' (1707)",
            "memory_tip": "BONIFACE: Basic Outstanding - Nice host, Innkeeper Friendly And Caring, Everyone feels welcome",
            "example_sentence": "The cheerful _____ welcomed weary travelers to his countryside inn.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bonobo",
            "definition": "A species of great ape closely related to chimpanzees, found in Congo",
            "pronunciation": "/bəˈnoʊboʊ/",
            "etymology": "From a local Congolese name, possibly a mispronunciation of the town Bolobo",
            "memory_tip": "BONOBO: Beautiful Outstanding - Natural primate, Outstanding Behavioral patterns, Outstanding ape species",
            "example_sentence": "The _____ is known for its peaceful and cooperative social behavior.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bonoboabrogate",
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
            "word": "bonsai",
            "definition": "The art of growing miniature trees in containers; such a tree",
            "pronunciation": "/bɑnˈsaɪ/",
            "etymology": "From Japanese bonsai, from bon 'tray' + sai 'planting'",
            "memory_tip": "BONSAI: Beautiful Outstanding - Nature art, Small And Incredibly detailed trees",
            "example_sentence": "The ancient _____ tree had been carefully tended for over a century.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bonspiel",
            "definition": "A curling tournament or match",
            "pronunciation": "/ˈbɑnˌspil/",
            "etymology": "From Scots bonspiel, possibly from Dutch bond 'league' + spel 'game'",
            "memory_tip": "BONSPIEL: Basic Organization - Never casual curling, Special Professional competition, Including Expert curling, League tournament",
            "example_sentence": "The annual _____ attracted curling teams from across the province.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bonus",
            "definition": "An extra payment or benefit; something given in addition",
            "pronunciation": "/ˈboʊnəs/",
            "etymology": "From Latin bonus meaning 'good'",
            "memory_tip": "BONUS: Basic Outstanding - Number above normal payment, Usually extra money, Something additional and good",
            "example_sentence": "Employees received a generous year-end _____ for their hard work.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boogie",
            "definition": "A style of blues music; to dance energetically",
            "pronunciation": "/ˈbʊɡi/",
            "etymology": "Possibly from African American slang, related to 'booger' or African origins",
            "memory_tip": "BOOGIE: Bold Outdoor - Outstanding music, Getting Inspired by rhythms, Everyone dancing energetically",
            "example_sentence": "The band played a lively _____ that got everyone on the dance floor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "book",
            "definition": "A set of printed pages bound together; to reserve or schedule",
            "pronunciation": "/bʊk/",
            "etymology": "From Old English boc, from Proto-Germanic bokiz, originally meaning 'beech' (wood used for writing tablets)",
            "memory_tip": "BOOK: Basic Object - Obviously for reading, Knowledge storage system",
            "example_sentence": "She found the perfect _____ to read during her vacation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "books",
            "definition": "Multiple sets of printed pages bound together for reading",
            "pronunciation": "/bʊks/",
            "etymology": "From book + -s plural, where book comes from Old English boc",
            "memory_tip": "BOOKS: Basic Objects - Obviously for reading, Knowledge Storage systems",
            "example_sentence": "The library contained thousands of _____ on every imaginable subject.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bookshelf",
            "definition": "A shelf designed to hold books",
            "pronunciation": "/ˈbʊkˌʃɛlf/",
            "etymology": "From book + shelf, referring to furniture for storing books",
            "memory_tip": "BOOKSHELF: Basic Object - Obviously for storing reading materials, Keeping books organized, Storing books Horizontally, Every library Furnishing",
            "example_sentence": "The tall _____ was filled with her collection of mystery novels.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bookworm",
            "definition": "A person devoted to reading; an insect that damages books",
            "pronunciation": "/ˈbʊkˌwɜrm/",
            "etymology": "From book + worm, originally referring to insects that ate through books",
            "memory_tip": "BOOKWORM: Basic Outstanding - Obviously reading constantly, Knowledge enthusiast, Who Obviously Reads More than others",
            "example_sentence": "As a lifelong _____, she had read thousands of novels by age thirty.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boom",
            "definition": "A loud deep sound; a period of rapid economic growth",
            "pronunciation": "/bum/",
            "etymology": "Imitative of a deep resonant sound",
            "memory_tip": "BOOM: Big Outstanding - Overwhelming sound, Making everyone startled",
            "example_sentence": "The thunder created a loud _____ that echoed across the valley.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boomslang",
            "definition": "A highly venomous tree snake found in sub-Saharan Africa",
            "pronunciation": "/ˈbumslæŋ/",
            "etymology": "From Afrikaans boom 'tree' + slang 'snake'",
            "memory_tip": "BOOMSLANG: Bold Outstanding - Obviously dangerous snake, Makes everyone cautious, Seriously dangerous, Lives And Never Goes down, dangerous African snake",
            "example_sentence": "The _____ is one of Africa's most dangerous arboreal serpents.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boondoggle",
            "definition": "Work or activity that is wasteful or pointless but appears important",
            "pronunciation": "/ˈbunˌdɑɡəl/",
            "etymology": "American slang, possibly from Boy Scout term for braided cord work",
            "memory_tip": "BOONDOGGLE: Basic Obvious - Obviously wasted effort, Never Doing meaningful work, Obviously Getting nowhere, Going nowhere, Lazy wasteful Enterprise",
            "example_sentence": "The expensive software project turned out to be a complete _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boorish",
            "definition": "Rude and ill-mannered; lacking refinement",
            "pronunciation": "/ˈbʊrɪʃ/",
            "etymology": "From boor (a rude person) + -ish, where boor comes from Dutch boer 'farmer'",
            "memory_tip": "BOORISH: Bad Obvious - Obviously Rude behavior, Irritating Socially unacceptable, Horrible manners",
            "example_sentence": "His _____ behavior at dinner embarrassed everyone at the table.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "booth",
            "definition": "A small enclosed compartment; a temporary stall or stand",
            "pronunciation": "/buθ/",
            "etymology": "From Old Norse buð meaning 'dwelling' or 'booth'",
            "memory_tip": "BOOTH: Basic Outdoor - Obviously small space, Temporary Housing structure",
            "example_sentence": "They sat in a corner _____ at the diner and ordered coffee.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bootless",
            "definition": "Useless or ineffectual; serving no purpose",
            "pronunciation": "/ˈbutləs/",
            "etymology": "From boot (profit, benefit) + -less, meaning 'without benefit'",
            "memory_tip": "BOOTLESS: Basic Obvious - Obviously useless effort, Totally Lacking useful results, Everyone Seeing wasted effort, Something Stupid",
            "example_sentence": "Their _____ attempts to repair the ancient machine only wasted time.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_022_processed.csv"
    
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
        
        print(f"Batch 022 processing complete!")
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