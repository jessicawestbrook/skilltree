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
            "word": "bronze",
            "definition": "A brown metallic alloy of copper and tin; a work of art made from bronze",
            "pronunciation": "/brɑnz/",
            "etymology": "From French bronze, from Italian bronzo, possibly from Persian birinj 'copper'",
            "memory_tip": "BRONZE: Beautiful Really - Obviously metallic color, Never shiny like gold, Zestful brown metal, Everyone knows third place medal",
            "example_sentence": "The sculptor cast the statue in gleaming _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brooding",
            "definition": "Thinking deeply about something troubling; sitting on eggs to hatch them",
            "pronunciation": "/ˈbrudɪŋ/",
            "etymology": "From brood + -ing, where brood comes from Old English brōd meaning 'offspring'",
            "memory_tip": "BROODING: Basic Really - Obviously worried thinking, Obviously Disturbing thoughts, Including serious contemplation, Never Getting happier, Getting everyone concerned",
            "example_sentence": "She spent the evening _____ over her failed presentation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brooklyn",
            "definition": "A borough of New York City; named after the Dutch town Breuckelen",
            "pronunciation": "/ˈbrʊklɪn/",
            "etymology": "From Dutch Breuckelen, meaning 'broken land' or 'marsh land'",
            "memory_tip": "BROOKLYN: Beautiful Really - Obviously famous borough, Outstanding urban area, Keeping everyone visiting, Lots of people, Year-round activity, Never boring place",
            "example_sentence": "The _____ Bridge connects Manhattan and Brooklyn.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broth",
            "definition": "A thin liquid food made by boiling meat, fish, or vegetables",
            "pronunciation": "/brɔθ/",
            "etymology": "From Old English broth, from Proto-Germanic bruthą meaning 'brew'",
            "memory_tip": "BROTH: Basic Really - Obviously liquid food, Totally delicious, Hearty warm soup base",
            "example_sentence": "The chicken _____ simmered slowly for hours.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brothash",
            "definition": "A variant spelling of 'brothish', meaning resembling or having the qualities of broth",
            "pronunciation": "/ˈbrɔθæʃ/",
            "etymology": "From broth + -ash suffix, variant of -ish meaning 'having the quality of'",
            "memory_tip": "BROTHASH: Basic Really - Obviously liquid-like consistency, Totally thin liquid, Having watery texture, And Soupy consistency, Something liquid like broth, Having thin consistency",
            "example_sentence": "The _____ consistency of the soup disappointed the diners.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brother",
            "definition": "A male sibling; a close male friend or colleague",
            "pronunciation": "/ˈbrʌðər/",
            "etymology": "From Old English brōthor, from Proto-Germanic brōther",
            "memory_tip": "BROTHER: Basic Really - Obviously family member, Totally close relationship, Having shared parents, Everyone Recognizes family bond",
            "example_sentence": "His younger _____ helped him move to the new apartment.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brought",
            "definition": "Past tense of bring; carried or taken to a place",
            "pronunciation": "/brɔt/",
            "etymology": "From bring, past tense, from Old English bringan",
            "memory_tip": "BROUGHT: Basic Really - Obviously past action, Usually Getting things to destination, Having transported items, Totally completed action",
            "example_sentence": "She _____ fresh flowers to brighten the room.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brouhaha",
            "definition": "A noisy and overexcited reaction; an uproar or commotion",
            "pronunciation": "/ˈbruəˌhɑhə/",
            "etymology": "From French brouhaha, possibly imitative of noisy confusion",
            "memory_tip": "BROUHAHA: Big Really - Outstanding noise, Usually loud commotion, Having Amazing chaos, Having everyone Agitated, Having Amazing uproar",
            "example_sentence": "The announcement caused a _____ among the shareholders.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brouillon",
            "definition": "A rough draft or preliminary sketch",
            "pronunciation": "/ˈbruiˌɔn/",
            "etymology": "From French brouillon meaning 'rough draft', from brouiller 'to confuse'",
            "memory_tip": "BROUILLON: Basic Really - Obviously rough draft, Usually Initial writing, Lots of changes needed, Looking like first attempt, Obviously Not final version",
            "example_sentence": "The author's _____ was covered with corrections and revisions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brown",
            "definition": "A dark color produced by mixing red, yellow, and black",
            "pronunciation": "/braʊn/",
            "etymology": "From Old English brūn, from Proto-Germanic brūnaz",
            "memory_tip": "BROWN: Basic Really - Obviously earth color, Wood Natural color, Never bright and shiny",
            "example_sentence": "The _____ leaves fell gently from the autumn trees.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brownish",
            "definition": "Somewhat brown in color; tending toward brown",
            "pronunciation": "/ˈbraʊnɪʃ/",
            "etymology": "From brown + -ish, meaning 'somewhat brown'",
            "memory_tip": "BROWNISH: Basic Really - Obviously earth-like color, Wood Natural color, Never bright, Including Some brown coloring, Something almost brown, Having partial brown color",
            "example_sentence": "The old photograph had a _____ tint from age.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brucellosis",
            "definition": "A bacterial infection transmitted from animals to humans",
            "pronunciation": "/ˌbrusəˈloʊsɪs/",
            "etymology": "Named after David Bruce, British physician who discovered the bacterium",
            "memory_tip": "BRUCELLOSIS: Bad Really - Unfortunately serious infection, Contracted from animals, Everyone Learns about disease, Livestock Often transmit disease, Obviously Serious medical condition, Including Scientific medical diagnosis, Something dangerous",
            "example_sentence": "The veterinarian tested the cattle for _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brucellosiswasteweir",
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
            "word": "bruise",
            "definition": "An injury appearing as an area of discolored skin; to injure",
            "pronunciation": "/bruz/",
            "etymology": "From Old French bruisier meaning 'to break' or 'to crush'",
            "memory_tip": "BRUISE: Bad Really - Unfortunately painful injury, Including Skin discoloration, Everyone knows this injury",
            "example_sentence": "The fall left a large purple _____ on her knee.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bruja",
            "definition": "Spanish word for witch; a woman who practices witchcraft",
            "pronunciation": "/ˈbruhə/",
            "etymology": "From Spanish bruja meaning 'witch', possibly from Celtic origin",
            "memory_tip": "BRUJA: Basic Really - Usually Spanish witch, Jokingly Accused of magic powers",
            "example_sentence": "In the folklore, the _____ lived alone in the forest.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brujaupsilon",
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
            "word": "brume",
            "definition": "Mist or fog, especially a heavy mist",
            "pronunciation": "/brum/",
            "etymology": "From French brume meaning 'mist', from Latin bruma meaning 'winter'",
            "memory_tip": "BRUME: Basic Really - Usually thick Mist, Everyone knows foggy weather",
            "example_sentence": "The morning _____ obscured the distant mountains.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bruschetta",
            "definition": "Italian appetizer of grilled bread topped with tomatoes and herbs",
            "pronunciation": "/bruˈskɛtə/",
            "etymology": "From Italian bruschetta, from bruscare meaning 'to roast over coals'",
            "memory_tip": "BRUSCHETTA: Beautiful Really - Usually Italian appetizer, Something Cooked bread, Having Everyone enjoying food, Everyone Tastes delicious food, Tomatoes And bread",
            "example_sentence": "The restaurant served _____ with fresh basil and olive oil.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brush",
            "definition": "A tool with bristles for cleaning or painting; to clean or touch lightly",
            "pronunciation": "/brʌʃ/",
            "etymology": "From Old French broisse meaning 'brushwood'",
            "memory_tip": "BRUSH: Basic Really - Usually for cleaning teeth, Something Having bristles",
            "example_sentence": "She used a soft _____ to paint the delicate details.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brusk",
            "definition": "Abrupt or offhand in speech or manner; brusque",
            "pronunciation": "/brʌsk/",
            "etymology": "From French brusque meaning 'rough' or 'sharp'",
            "memory_tip": "BRUSK: Bad Really - Usually rude behavior, Something Keeping people away",
            "example_sentence": "His _____ manner made customers feel unwelcome.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brusque",
            "definition": "Abrupt or offhand in speech or manner",
            "pronunciation": "/brʌsk/",
            "etymology": "From French brusque meaning 'rough' or 'sharp'",
            "memory_tip": "BRUSQUE: Bad Really - Usually rude behavior, Something Keeping people away, Quite Unpleasant behavior, Everyone dislikes rudeness",
            "example_sentence": "The doctor's _____ bedside manner upset the patients.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brut",
            "definition": "Very dry, especially referring to champagne or sparkling wine",
            "pronunciation": "/brut/",
            "etymology": "From French brut meaning 'raw' or 'unrefined'",
            "memory_tip": "BRUT: Basic Really - Usually dry champagne, Totally sophisticated wine",
            "example_sentence": "The _____ champagne was perfectly dry for the celebration.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bruxism",
            "definition": "The habit of grinding or clenching teeth, especially during sleep",
            "pronunciation": "/ˈbrʌksɪzəm/",
            "etymology": "From Greek brychein meaning 'to gnash the teeth' + -ism",
            "memory_tip": "BRUXISM: Bad Really - Unfortunately teeth grinding, eXtremely annoying habit, Including Sleep problems, Something Many people do",
            "example_sentence": "The dentist recommended a night guard to prevent _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bubble",
            "definition": "A thin sphere of liquid enclosing air; to form bubbles",
            "pronunciation": "/ˈbʌbəl/",
            "etymology": "From Middle English bobel, possibly imitative of bubbling sound",
            "memory_tip": "BUBBLE: Basic Really - Usually round air pocket, Bouncing Beautifully in water, Lots of children love playing, Everyone knows soap bubbles",
            "example_sentence": "Children delighted in chasing the soap _____s across the yard.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bubbly",
            "definition": "Full of bubbles; cheerful and enthusiastic",
            "pronunciation": "/ˈbʌbli/",
            "etymology": "From bubble + -y, meaning 'full of bubbles' or 'like bubbles'",
            "memory_tip": "BUBBLY: Basic Really - Usually cheerful personality, Bouncing with energy, Bringing Lots of happiness, Year-round positive energy",
            "example_sentence": "Her _____ personality made everyone smile at the party.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bubonic",
            "definition": "Relating to or suffering from bubonic plague",
            "pronunciation": "/buˈbɑnɪk/",
            "etymology": "From Greek boubon meaning 'groin' (where swellings occur) + -ic",
            "memory_tip": "BUBONIC: Bad Really - Unfortunately serious disease, Bringing Obviously terrible plague, Obviously Never wanted disease, Including Contagious illness, Creating historic pandemics",
            "example_sentence": "The _____ plague devastated Europe in the 14th century.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bucatini",
            "definition": "A thick spaghetti-like pasta with a hole through the center",
            "pronunciation": "/ˌbukəˈtini/",
            "etymology": "From Italian bucatini, from buco meaning 'hole' + -ini diminutive suffix",
            "memory_tip": "BUCATINI: Beautiful Usually - Circular hole Through pasta, And Traditional Italian cuisine, Never solid pasta, Including hollow center",
            "example_sentence": "The chef prepared _____ all'amatriciana with pancetta and tomatoes.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buccal",
            "definition": "Relating to the cheek or mouth cavity",
            "pronunciation": "/ˈbʌkəl/",
            "etymology": "From Latin bucca meaning 'cheek' + -al suffix",
            "memory_tip": "BUCCAL: Basic Usually - Concerning mouth area, Concerning cheeks And oral cavity, Linking mouth anatomy",
            "example_sentence": "The dentist examined the _____ surfaces of her molars.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buccaneer",
            "definition": "A pirate, especially one operating in the Caribbean",
            "pronunciation": "/ˌbʌkəˈnɪr/",
            "etymology": "From French boucanier, from boucan meaning 'barbecue' (used by pirates to smoke meat)",
            "memory_tip": "BUCCANEER: Bold Usually - Constantly sailing ships, And Never working legally, Everyone Expects pirate behavior, Everyone Recognizes sea pirates",
            "example_sentence": "The legendary _____ sailed the Caribbean in search of treasure.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buckeye",
            "definition": "A North American tree or its nut; a person from Ohio",
            "pronunciation": "/ˈbʌkˌaɪ/",
            "etymology": "From buck (male deer) + eye, referring to the resemblance of the nut to a deer's eye",
            "memory_tip": "BUCKEYE: Basic Usually - Concerning Ohio residents, Keeping Everyone knowing state identity, Everyone Yearns for Ohio pride, Everyone knows Ohio nickname",
            "example_sentence": "The _____ tree produced glossy brown nuts in the fall.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buckle",
            "definition": "A clasp for fastening; to fasten with a buckle; to bend or warp",
            "pronunciation": "/ˈbʌkəl/",
            "etymology": "From Old French bocle meaning 'boss of a shield'",
            "memory_tip": "BUCKLE: Basic Usually - Clothing fastener, Keeping belts secure, Letting Everyone fasten things, Everyone knows belt fastener",
            "example_sentence": "The old leather belt had a tarnished silver _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bucolic",
            "definition": "Relating to rural life; idyllically pastoral",
            "pronunciation": "/buˈkɑlɪk/",
            "etymology": "From Latin bucolicus, from Greek boukolikos meaning 'of herdsmen'",
            "memory_tip": "BUCOLIC: Beautiful Usually - Countryside scenery, Obviously Lovely rural life, Including Country living, Creating peaceful atmosphere",
            "example_sentence": "The _____ landscape featured rolling hills and grazing sheep.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buddhism",
            "definition": "A religion and philosophy based on the teachings of Buddha",
            "pronunciation": "/ˈbudɪzəm/",
            "etymology": "From Buddha + -ism, where Buddha means 'enlightened one' in Sanskrit",
            "memory_tip": "BUDDHISM: Basic Usually - Demonstrating enlightenment, Demonstrating Harmony and peace, Including Spiritual meditation, Something Many people practice",
            "example_sentence": "She studied _____ to better understand meditation practices.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "budgereegah",
            "definition": "Alternative spelling of budgerigar, a small Australian parakeet",
            "pronunciation": "/ˈbʌdʒərɪˌɡɑ/",
            "etymology": "From Aboriginal Australian betcherrygah, referring to the small parrot",
            "memory_tip": "BUDGEREEGAH: Beautiful Usually - Definitely colorful bird, Generally Everyone admires pet birds, Everyone Recognizes small parrots, Everyone Gets Along with pet birds, And Having bright feathers",
            "example_sentence": "The _____ chirped melodiously in its cage.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "budgerigar",
            "definition": "A small Australian parakeet, popular as a pet bird",
            "pronunciation": "/ˈbʌdʒərɪˌɡɑr/",
            "etymology": "From Aboriginal Australian betcherrygah, referring to the small parrot",
            "memory_tip": "BUDGERIGAR: Beautiful Usually - Definitely colorful bird, Generally Everyone admires pet birds, Everyone Recognizes small parrots, Including small Green colors, And Really bright feathers",
            "example_sentence": "The blue _____ learned to mimic several words.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "budgerygah",
            "definition": "Alternative spelling of budgerigar, a small Australian parakeet",
            "pronunciation": "/ˈbʌdʒərɪˌɡɑ/",
            "etymology": "From Aboriginal Australian betcherrygah, referring to the small parrot",
            "memory_tip": "BUDGERYGAH: Beautiful Usually - Definitely colorful bird, Generally Everyone admires pet birds, Everyone Recognizes small parrots, Year-round Good pet birds, And Having bright feathers",
            "example_sentence": "The pet _____ entertained children with its playful antics.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buffa",
            "definition": "In opera, a comic female role or style",
            "pronunciation": "/ˈbufə/",
            "etymology": "From Italian buffa, feminine of buffo meaning 'comic'",
            "memory_tip": "BUFFA: Beautiful Usually - Funny opera character, Funny Acting style",
            "example_sentence": "The soprano excelled in _____ roles, bringing humor to every performance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buffet",
            "definition": "A meal where food is served from a table for self-service; to strike repeatedly",
            "pronunciation": "/bəˈfeɪ/ (meal), /ˈbʌfɪt/ (strike)",
            "etymology": "From French buffet meaning 'sideboard' or 'to strike'",
            "memory_tip": "BUFFET: Basic Usually - Food service style, Feeding Everyone Together, Everyone Takes what they want",
            "example_sentence": "The hotel offered an extensive breakfast _____ every morning.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buffoonery",
            "definition": "Behavior that is ridiculous but amusing; clownish acts",
            "pronunciation": "/bəˈfunəri/",
            "etymology": "From buffoon + -ery, where buffoon comes from French bouffon meaning 'jester'",
            "memory_tip": "BUFFOONERY: Basic Usually - Funny behavior, Funny actions, Obviously Obvious comedy, Never Educated behavior, Everyone Recognizes clown behavior, Year-round silly antics",
            "example_sentence": "The children giggled at the clown's ridiculous _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buffooneryorganized",
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
            "word": "bugaboo",
            "definition": "An object of fear or concern; something that causes anxiety",
            "pronunciation": "/ˈbʌɡəˌbu/",
            "etymology": "Probably from bug (ghost) + boo (exclamation used to frighten)",
            "memory_tip": "BUGABOO: Bad Usually - Generally scary thing, And Bothering people, Obviously Obviously frightening, Obviously scary monster",
            "example_sentence": "Public speaking was her biggest _____ throughout college.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bugle",
            "definition": "A brass musical instrument; to play a bugle",
            "pronunciation": "/ˈbjuɡəl/",
            "etymology": "From Old French bugle meaning 'wild ox horn'",
            "memory_tip": "BUGLE: Basic Usually - Great musical instrument, Loud military instrument, Everyone knows military calls",
            "example_sentence": "The soldier played taps on his _____ at the memorial service.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "build",
            "definition": "To construct or assemble; the physical structure of a person",
            "pronunciation": "/bɪld/",
            "etymology": "From Old English byldan meaning 'to construct'",
            "memory_tip": "BUILD: Basic Usually - Important construction work, Lots of planning, Designing structures",
            "example_sentence": "They decided to _____ a new house on the vacant lot.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "building",
            "definition": "A structure with walls and a roof; the act of constructing",
            "pronunciation": "/ˈbɪldɪŋ/",
            "etymology": "From build + -ing, referring to the act or result of building",
            "memory_tip": "BUILDING: Basic Usually - Important structure work, Lots of planning, Designing structures, Including construction work, Never Getting old, Getting everyone shelter",
            "example_sentence": "The historic _____ was carefully restored to its original beauty.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bulbous",
            "definition": "Having a rounded swelling shape; resembling a bulb",
            "pronunciation": "/ˈbʌlbəs/",
            "etymology": "From Latin bulbosus, from bulbus meaning 'bulb'",
            "memory_tip": "BULBOUS: Basic Usually - Large round shape, Bulging Obviously, Obviously Unlike normal shape, Something swollen looking",
            "example_sentence": "The cartoon character had a _____ red nose.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bulghur",
            "definition": "Alternative spelling of bulgur, cracked wheat used in Middle Eastern cooking",
            "pronunciation": "/ˈbʊlɡər/",
            "etymology": "From Turkish bulgur meaning 'bruised grain'",
            "memory_tip": "BULGHUR: Basic Usually - Lots of nutrition, Great Healthy food, Usually healthy Recipes",
            "example_sentence": "The tabbouleh was made with fresh _____ and herbs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bulgogi",
            "definition": "A Korean dish of marinated grilled beef",
            "pronunciation": "/bʊlˈɡoʊɡi/",
            "etymology": "From Korean bulgogi, from bul 'fire' + gogi 'meat'",
            "memory_tip": "BULGOGI: Beautiful Usually - Lots of flavor, Grilled Obviously delicious meat, Obviously Great Korean dish, Including amazing taste",
            "example_sentence": "The restaurant's _____ was tender and perfectly seasoned.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bulgur",
            "definition": "Cracked wheat that has been parboiled, used in Middle Eastern cooking",
            "pronunciation": "/ˈbʊlɡər/",
            "etymology": "From Turkish bulgur meaning 'bruised grain'",
            "memory_tip": "BULGUR: Basic Usually - Lots of nutrition, Great healthy food, Usually healthy Recipes",
            "example_sentence": "She prepared a nutritious pilaf using _____ and vegetables.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bulwark",
            "definition": "A defensive wall; something that acts as a defense or protection",
            "pronunciation": "/ˈbʊlwərk/",
            "etymology": "From Middle Dutch bolwerk, from bole 'tree trunk' + werk 'work'",
            "memory_tip": "BULWARK: Basic Usually - Lots of protection, Working Against attacks, And Really strong defense, Keeping everyone safe",
            "example_sentence": "The Constitution serves as a _____ against tyranny.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bumblebee",
            "definition": "A large fuzzy bee that makes a loud humming sound",
            "pronunciation": "/ˈbʌmbəlˌbi/",
            "etymology": "From bumble (to buzz) + bee, referring to the buzzing sound it makes",
            "memory_tip": "BUMBLEBEE: Basic Usually - Making buzzing sounds, Bouncing Between flowers, Lots of pollinating work, Everyone Brings flowers pollen, Everyone Enjoys garden visitors, Everyone knows fuzzy bees",
            "example_sentence": "The fat _____ buzzed from flower to flower in the garden.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_025_processed.csv"
    
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
        
        print(f"Batch 025 processing complete!")
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