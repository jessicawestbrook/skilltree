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
            "word": "bireme",
            "definition": "An ancient galley with two banks of oars",
            "pronunciation": "/ˈbaɪrim/",
            "etymology": "From Latin biremis, from bi- 'two' + remus 'oar'",
            "memory_tip": "BIREME: Big Important - Roman ship, Everyone Manning oars, Everyone rowing together",
            "example_sentence": "The ancient _____ was powered by skilled rowers on two levels.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biriani",
            "definition": "Alternative spelling of biryani, a spiced rice dish from South Asia",
            "pronunciation": "/ˌbɪriˈɑni/",
            "etymology": "From Persian biryani, possibly from biryan meaning 'fried' or 'roasted'",
            "memory_tip": "BIRIANI: Beautiful Indian - Rice with spices, Including Amazing meat, Aromatic ingredients, Natural flavorful dish, International cuisine",
            "example_sentence": "The restaurant's chicken _____ was fragrant with saffron and cardamom.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "birria",
            "definition": "A Mexican dish of stewed meat, typically goat or beef, served with broth",
            "pronunciation": "/ˈbiriə/",
            "etymology": "From Spanish birria, possibly from Andalusian birrio meaning 'worthless thing' (ironically named)",
            "memory_tip": "BIRRIA: Bold Important - Rich mexican stew, Really spicy, Including Amazing meat, Amazing traditional food",
            "example_sentence": "The _____ tacos were served with a rich, flavorful consommé for dipping.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "birthday",
            "definition": "The anniversary of the day on which a person was born",
            "pronunciation": "/ˈbɜrθˌdeɪ/",
            "etymology": "From birth + day, referring to the day of one's birth",
            "memory_tip": "BIRTHDAY: Born Important - day Remembering celebration, Time for Happy cake, Day special Anniversary, Year older celebration",
            "example_sentence": "She celebrated her tenth _____ with a party at the park.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biryani",
            "definition": "A South Asian dish of spiced rice with meat, fish, or vegetables",
            "pronunciation": "/ˌbɪriˈɑni/",
            "etymology": "From Persian biryani, possibly from biryan meaning 'fried' or 'roasted'",
            "memory_tip": "BIRYANI: Beautiful Indian - Rice with spices, Yummy And flavorful, Amazing Natural cooking, International cuisine",
            "example_sentence": "The lamb _____ was layered with aromatic basmati rice and exotic spices.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bisbigliando",
            "definition": "A musical technique of rapidly repeated notes, creating a whispering effect",
            "pronunciation": "/ˌbɪzbɪˈɡljɑndoʊ/",
            "etymology": "From Italian bisbigliando meaning 'whispering', from bisbigliare 'to whisper'",
            "memory_tip": "BISBIGLIANDO: Beautiful Italian - Sound technique, Barely audible notes, In music, Gentle Light piano technique, Including Amazing whispering musical effects, Never loud, Delicate Orchestral technique",
            "example_sentence": "The harpist used _____ to create an ethereal, whispering sound effect.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biscotti",
            "definition": "Italian twice-baked cookies, typically almond-flavored and crunchy",
            "pronunciation": "/bɪˈskɔti/",
            "etymology": "From Italian biscotti, from bis 'twice' + cotto 'cooked'",
            "memory_tip": "BISCOTTI: Baked Italian - Sweet crunchy cookies, Cooked twice, Outstanding Traditional treats, Italian dessert",
            "example_sentence": "She dipped the almond _____ into her espresso at the Italian café.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biscuit",
            "definition": "A small, round bread; in British usage, a cookie or cracker",
            "pronunciation": "/ˈbɪskɪt/",
            "etymology": "From Old French bescuit, from bis 'twice' + cuit 'cooked'",
            "memory_tip": "BISCUIT: Baked Important - Small bread, Cooked twice historically, Usually eaten with meals, Incredible Tasty bread",
            "example_sentence": "The warm _____ was served with butter and honey for breakfast.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bismillah",
            "definition": "An Arabic phrase meaning 'in the name of Allah', used to begin activities",
            "pronunciation": "/bɪsˈmɪlə/",
            "etymology": "From Arabic bismillāh, from bi 'in' + ism 'name' + Allah 'God'",
            "memory_tip": "BISMILLAH: Beginning Important - Sacred prayer, Meaningful Islamic phrase, In Allah's name, Lots of religious significance, Learning Arabic culture, Always spoken before actions, Holy blessing",
            "example_sentence": "He said '_____ ' before beginning his meal.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bison",
            "definition": "A large, shaggy-haired wild ox native to North America and Europe",
            "pronunciation": "/ˈbaɪsən/",
            "etymology": "From Latin bison, from Greek bison, possibly from a Thracian word",
            "memory_tip": "BISON: Big Important - Strong massive animal, Outstanding Natural creature",
            "example_sentence": "The herd of _____ grazed peacefully on the Great Plains.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bite",
            "definition": "To cut or grip with the teeth; a wound made by biting",
            "pronunciation": "/baɪt/",
            "etymology": "From Old English bitan, from Proto-Germanic bitanan",
            "memory_tip": "BITE: Basic Important - Teeth action, Everyone eats with teeth",
            "example_sentence": "The dog's _____ required immediate medical attention.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "biting",
            "definition": "Causing a sharp or stinging sensation; harshly critical",
            "pronunciation": "/ˈbaɪtɪŋ/",
            "etymology": "From bite + -ing, referring to the action or quality of biting",
            "memory_tip": "BITING: Bad Irritating - Terribly painful sensation, Including sharp criticism, Never Getting comfortable",
            "example_sentence": "The comedian's _____ wit made the audience both laugh and wince.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bittern",
            "definition": "A large wading bird with a booming call, related to herons",
            "pronunciation": "/ˈbɪtərn/",
            "etymology": "From Old French butor, possibly imitative of the bird's call",
            "memory_tip": "BITTERN: Bird In - wetlands, Totally Excellent bird, Rarely seen, Never common bird",
            "example_sentence": "The elusive _____ was finally spotted among the marsh reeds.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bittersweet",
            "definition": "Both bitter and sweet; pleasure mixed with pain or regret",
            "pronunciation": "/ˈbɪtərˌswit/",
            "etymology": "From bitter + sweet, describing contrasting flavors or emotions",
            "memory_tip": "BITTERSWEET: Both Important - Totally contrasting tastes, Emotions mixed, Really conflicted feelings, Sweet mixed with sadness, When Everything feels mixed, Everything Together good and bad",
            "example_sentence": "Graduation was a _____ moment, filled with pride but sadness about leaving friends.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bitumen",
            "definition": "A black viscous mixture of hydrocarbons; asphalt",
            "pronunciation": "/bɪˈtumən/",
            "etymology": "From Latin bitumen, possibly from Celtic origin",
            "memory_tip": "BITUMEN: Black Important - Tar-like substance, Used for roads, Making roads, Everyone drives on roads made with this, Natural asphalt",
            "example_sentence": "The road was paved with _____ to create a smooth, durable surface.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bivouac",
            "definition": "A temporary camp without tents; to camp in the open",
            "pronunciation": "/ˈbɪvuˌæk/",
            "etymology": "From French bivouac, from German Beiwache meaning 'additional watch'",
            "memory_tip": "BIVOUAC: Basic Important - Very outdoors camping, Overnight Under stars, Always without shelter, Camping outdoors temporarily",
            "example_sentence": "The soldiers set up a _____ on the mountainside for the night.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bizarro",
            "definition": "Very strange or unusual; bizarre",
            "pronunciation": "/bɪˈzɑroʊ/",
            "etymology": "From Italian bizzarro meaning 'angry, fierce', later meaning 'strange'",
            "memory_tip": "BIZARRO: Basic Incredibly - Zany And Really weird, Really Obviously strange and unusual",
            "example_sentence": "The _____ art exhibition featured sculptures made entirely of recycled bubble wrap.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "black",
            "definition": "The darkest color; the absence of light or color",
            "pronunciation": "/blæk/",
            "etymology": "From Old English blæc, from Proto-Germanic blakaz",
            "memory_tip": "BLACK: Basic Light - Absent Completely, Keeping no light visible",
            "example_sentence": "The _____ cat disappeared into the shadows of the alley.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blackbird",
            "definition": "A common songbird, typically with black plumage in males",
            "pronunciation": "/ˈblækˌbɜrd/",
            "etymology": "From black + bird, referring to the bird's dark coloration",
            "memory_tip": "BLACKBIRD: Black Beautiful - song bird, Always Calling with beautiful melodies, Keeping people listening, Beautiful music, In Really lovely singing, Distinguished singing voice",
            "example_sentence": "The _____ sang its melodious song from the top of the oak tree.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blacksmith",
            "definition": "A person who forges iron and steel, especially horseshoes",
            "pronunciation": "/ˈblækˌsmɪθ/",
            "etymology": "From black (referring to black iron) + smith (metalworker)",
            "memory_tip": "BLACKSMITH: Basic Labor - Always Creating tools, Keeping everyone equipped, Strong worker making metal items, Making Important tools, Teaching metal-working, Hot forge work",
            "example_sentence": "The village _____ shaped horseshoes on his anvil with rhythmic hammer blows.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blame",
            "definition": "To hold responsible for a fault or wrong; responsibility for something bad",
            "pronunciation": "/bleɪm/",
            "etymology": "From Old French blasmer, from Latin blasphemare 'to blaspheme'",
            "memory_tip": "BLAME: Bad Language - Accusing people, Making Everyone feel guilty",
            "example_sentence": "The committee refused to _____ any single person for the project's failure.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blanche",
            "definition": "To turn white or pale; to blanch vegetables by brief boiling",
            "pronunciation": "/blæntʃ/",
            "etymology": "From Old French blanchir meaning 'to whiten', from blanc 'white'",
            "memory_tip": "BLANCHE: Becomes Light - Always turning white, Never Coloring, Hurting Everything light, Everyone becomes pale",
            "example_sentence": "She watched him _____ when he heard the shocking news.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blancmange",
            "definition": "A sweet dessert made from milk thickened with cornstarch",
            "pronunciation": "/bləˈmɑnʒ/",
            "etymology": "From Old French blanc mange meaning 'white food', from blanc 'white' + mange 'food'",
            "memory_tip": "BLANCMANGE: Beautiful Light - And creamy dessert, Natural smooth dessert, Making Amazing sweet dessert, Nice Gentle taste, Everyone loves this dessert",
            "example_sentence": "The _____ was served with fresh strawberries and a drizzle of vanilla sauce.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blandish",
            "definition": "To coax with flattery; to persuade through soft words",
            "pronunciation": "/ˈblændɪʃ/",
            "etymology": "From Old French blandir meaning 'to flatter', from Latin blandus 'smooth, flattering'",
            "memory_tip": "BLANDISH: Basic Language - And Nice words, Deliberately Influencing people, Soft persuasion, Hoping to convince others",
            "example_sentence": "He tried to _____ his way into getting a promotion with excessive compliments.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blank",
            "definition": "Empty; without marks or writing; showing no expression",
            "pronunciation": "/blæŋk/",
            "etymology": "From Old French blanc meaning 'white, shining'",
            "memory_tip": "BLANK: Basic Look - Always Nothing there, Never Keeping anything written",
            "example_sentence": "She stared at the _____ page, unable to think of what to write.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blanket",
            "definition": "A large piece of cloth used for warmth; to cover completely",
            "pronunciation": "/ˈblæŋkɪt/",
            "etymology": "From Old French blanchet, diminutive of blanc 'white'",
            "memory_tip": "BLANKET: Beautiful Light - And warm covering, Never Keeping anyone cold, Everyone appreciates warmth, Totally covering everything",
            "example_sentence": "She pulled the warm _____ up to her chin on the cold winter night.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blarney",
            "definition": "Flattering or cajoling talk; smooth, deceptive speech",
            "pronunciation": "/ˈblɑrni/",
            "etymology": "From Blarney Stone in Ireland, said to give the gift of eloquent flattery to those who kiss it",
            "memory_tip": "BLARNEY: Beautiful Language - And charming words, Really Nice smooth talking, Everyone falls for flattery, Youthful Irish charm",
            "example_sentence": "His _____ convinced her to lend him money despite her better judgment.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blasphemous",
            "definition": "Showing disrespect for sacred things; profane",
            "pronunciation": "/ˈblæsfəməs/",
            "etymology": "From Greek blasphemos meaning 'speaking evil', from blaptein 'to hurt' + pheme 'speech'",
            "memory_tip": "BLASPHEMOUS: Bad Language - And Sinful words, Probably Hurting religious feelings, Everyone offended, Most people Outraged, Utterly Sacrilegious speech",
            "example_sentence": "The comedian's _____ jokes offended many religious members of the audience.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blast",
            "definition": "A strong gust of air; an explosion; to blow up with explosives",
            "pronunciation": "/blæst/",
            "etymology": "From Old English blæst meaning 'blowing, breeze', from Proto-Germanic blæstaz",
            "memory_tip": "BLAST: Big Loud - And Strong explosion, Sound Terrible when it happens",
            "example_sentence": "The _____ from the explosion shattered windows for several blocks.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blastema",
            "definition": "A mass of undifferentiated cells from which an organ or body part develops",
            "pronunciation": "/blæˈstimə/",
            "etymology": "From Greek blastema meaning 'sprout, shoot', from blastanein 'to sprout'",
            "memory_tip": "BLASTEMA: Basic Living - And growing cells, Science Terminology - Explaining regeneration, Making Amazing regeneration happen",
            "example_sentence": "The salamander's _____ allowed it to completely regenerate its lost tail.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blastogenesis",
            "definition": "The formation of buds in reproduction; lymphocyte transformation",
            "pronunciation": "/ˌblæstoʊˈdʒɛnəsɪs/",
            "etymology": "From Greek blastos 'bud, germ' + genesis 'origin, creation'",
            "memory_tip": "BLASTOGENESIS: Basic Living - And growing cells, Science Technology - Organism Growth producing Excellence, Natural cell transformation, Evolution Starting with Incredible Science",
            "example_sentence": "The immunologist studied _____ to understand how lymphocytes respond to antigens.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blatant",
            "definition": "Done openly and unashamed; completely obvious",
            "pronunciation": "/ˈbleɪtənt/",
            "etymology": "Coined by Edmund Spenser in 'The Faerie Queene', possibly from Latin blatire 'to babble'",
            "memory_tip": "BLATANT: Bold Language - And obvious behavior, Totally obvious And Never Trying to hide anything",
            "example_sentence": "His _____ disregard for the rules shocked everyone at the meeting.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blatherskite",
            "definition": "A person who talks foolishly at length; nonsensical talk",
            "pronunciation": "/ˈblæðərˌskaɪt/",
            "etymology": "From blather (to talk foolishly) + skite (boaster), originally Scottish",
            "memory_tip": "BLATHERSKITE: Babbling Language - And Talking meaninglessly, Hearing Everyone Rambling, Speaking Keeping people bored, Irritating Talk, Everyone tired of listening",
            "example_sentence": "The politician was dismissed as a _____ who spoke a lot but said nothing meaningful.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blazer",
            "definition": "A colored jacket, often part of a uniform or worn casually",
            "pronunciation": "/ˈbleɪzər/",
            "etymology": "From blaze, originally referring to the bright colors of boating club jackets",
            "memory_tip": "BLAZER: Bright Looking - And professional jacket, Zestful professional clothing, Everyone Recognizes this stylish jacket",
            "example_sentence": "He wore his school _____ with pride during the graduation ceremony.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bleary",
            "definition": "Tired and unfocused; blurred or dim",
            "pronunciation": "/ˈblɪri/",
            "etymology": "From Middle English blere meaning 'to have watery eyes'",
            "memory_tip": "BLEARY: Bad Looking - Eyes tired, Appearing Really exhausted, watery vision, Your eyes struggling",
            "example_sentence": "She rubbed her _____ eyes after staying up all night studying.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bleat",
            "definition": "The cry of a sheep or goat; to complain in a weak voice",
            "pronunciation": "/blit/",
            "etymology": "From Old English blætan, of imitative origin",
            "memory_tip": "BLEAT: Baaa Loud - Every Animal sound, All sheep and goats Together making sounds",
            "example_sentence": "The lamb began to _____ loudly when separated from its mother.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blemish",
            "definition": "A mark or flaw that spoils perfection; to damage or mar",
            "pronunciation": "/ˈblɛmɪʃ/",
            "etymology": "From Old French blemir meaning 'to make pale', from Germanic origin",
            "memory_tip": "BLEMISH: Bad Looking - Everyone Minds Imperfections, Something Hurting beauty",
            "example_sentence": "The small scar was the only _____ on her otherwise perfect complexion.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blessingspeacock",
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
            "word": "bleu",
            "definition": "French word for blue; used in culinary terms like 'bleu cheese'",
            "pronunciation": "/blø/",
            "etymology": "From Old French bleu, from Germanic origin",
            "memory_tip": "BLEU: Blue Language - European color word, Understanding french vocabulary",
            "example_sentence": "The restaurant served a salad topped with crumbled _____ cheese.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blight",
            "definition": "A plant disease; something that damages or spoils",
            "pronunciation": "/blaɪt/",
            "etymology": "Possibly from Old English blæce meaning 'pale', or related to bleach",
            "memory_tip": "BLIGHT: Bad Living - Illness or disease, Going around Hurting plants, Terrible plant disease",
            "example_sentence": "The potato _____ devastated crops across Ireland in the 1840s.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blindfolded",
            "definition": "Having the eyes covered to prevent seeing",
            "pronunciation": "/ˈblaɪndˌfoʊldɪd/",
            "etymology": "From blindfold + -ed, where blindfold comes from blind + fold",
            "memory_tip": "BLINDFOLDED: Basic Living - In darkness, Never Detecting what's around, Finding Objects Largely by touch, Depending on Everybody else to help, Difficult navigation",
            "example_sentence": "The children played pin the tail on the donkey while _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blink",
            "definition": "To shut and open the eyes quickly; a brief moment",
            "pronunciation": "/blɪŋk/",
            "etymology": "From Middle English blinken, possibly related to Middle Dutch blinken 'to shine'",
            "memory_tip": "BLINK: Basic Looking - In quick motion, Never Keeping eyes open long",
            "example_sentence": "She didn't _____ an eye during the entire horror movie.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blissfully",
            "definition": "In a state of perfect happiness; without awareness of problems",
            "pronunciation": "/ˈblɪsfəli/",
            "etymology": "From bliss + -fully, where bliss comes from Old English bliths 'happiness'",
            "memory_tip": "BLISSFULLY: Beautiful Living - In perfect happiness, Supremely So pleased, Feeling Ultimate happiness, Lovely Life experience, Years of happiness",
            "example_sentence": "She was _____ unaware of the chaos happening around her.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blizzard",
            "definition": "A severe snowstorm with strong winds",
            "pronunciation": "/ˈblɪzərd/",
            "etymology": "Possibly from German blitz 'lightning' or from American dialect bliz 'violent rainstorm'",
            "memory_tip": "BLIZZARD: Bad Living - In snowy weather, Zero visibility, Zapping everyone with cold, And Really Dangerous storm",
            "example_sentence": "The _____ closed roads and schools throughout the region.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blockheap",
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
            "word": "bloomsbury",
            "definition": "A district in London; associated with a literary group of early 20th century",
            "pronunciation": "/ˈblumzˌbɛri/",
            "etymology": "From the name of the London district, possibly from 'Blemund's burgh' (Blemund's fortified place)",
            "memory_tip": "BLOOMSBURY: Beautiful London - Outstanding literary circle, Many creative people, Special cultural area, British intellectual writers, Unique cultural heritage, Really outstanding literary history, Year after year creative genius",
            "example_sentence": "Virginia Woolf was a prominent member of the _____ Group.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blooper",
            "definition": "An embarrassing mistake, especially on television or radio",
            "pronunciation": "/ˈblupər/",
            "etymology": "From bloop (a mistake in baseball) + -er suffix",
            "memory_tip": "BLOOPER: Basic Language - Oops! Obvious mistake, People Everyone Recognizes errors",
            "example_sentence": "The actor's _____ during the live broadcast became an internet sensation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blotch",
            "definition": "An irregular spot or stain; to mark with blots",
            "pronunciation": "/blɑtʃ/",
            "etymology": "Possibly from blot + -ch, or from French bloque 'block'",
            "memory_tip": "BLOTCH: Bad Looking - Or ugly mark, Totally Clearly visible, Hurting appearance",
            "example_sentence": "The red _____ on her skin indicated an allergic reaction.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blottesque",
            "definition": "Grotesquely distorted or bizarre; in the style of a blot or stain",
            "pronunciation": "/blɑˈtɛsk/",
            "etymology": "From blot + -esque suffix, meaning 'in the style of'",
            "memory_tip": "BLOTTESQUE: Bizarre Looking - Or abstract patterns, Totally Twisted art styles, Everything Strangely designed, Quite Unusual artistic Expression",
            "example_sentence": "The artist's _____ paintings featured abstract forms reminiscent of ink blots.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "blottesquebobolink",
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
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_021_processed.csv"
    
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
        
        print(f"Batch 021 processing complete!")
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