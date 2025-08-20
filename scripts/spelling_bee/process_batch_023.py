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
            "word": "bordereaux",
            "definition": "Detailed statements or memoranda, especially in insurance or shipping",
            "pronunciation": "/ˌbɔrdəˈroʊ/",
            "etymology": "From French bordereau meaning 'memorandum' or 'statement'",
            "memory_tip": "BORDEREAUX: Basic Organization - Record Documents, Everyone Reviews shipping records, And business accounts, Ultimately eXtensive documentation",
            "example_sentence": "The insurance company required detailed _____ for all claims processed.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "born",
            "definition": "Brought into existence; having a natural talent for something",
            "pronunciation": "/bɔrn/",
            "etymology": "From Old English beran meaning 'to bear' or 'to carry'",
            "memory_tip": "BORN: Basic Origin - Really Natural beginning",
            "example_sentence": "She was _____ with an exceptional gift for music.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "borough",
            "definition": "A town or district with local government; an administrative division",
            "pronunciation": "/ˈbɜroʊ/",
            "etymology": "From Old English burg meaning 'fortress' or 'fortified town'",
            "memory_tip": "BOROUGH: Basic Organization - Really Outstanding municipal area, Government Having local control",
            "example_sentence": "The _____ council voted to approve the new park construction.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "borrowed",
            "definition": "Took temporarily with permission; adopted from another source",
            "pronunciation": "/ˈbɑroʊd/",
            "etymology": "From borrow + -ed, where borrow comes from Old English borgian",
            "memory_tip": "BORROWED: Basic Operation - Really Returned later, Obviously temporary, With Everyone's permission, Everyone Deserves their items back",
            "example_sentence": "He _____ his friend's car for the weekend trip.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bosc",
            "definition": "A variety of pear with brown russet skin and sweet flesh",
            "pronunciation": "/bɑsk/",
            "etymology": "Named after Louis Bosc, an 18th-century French botanist",
            "memory_tip": "BOSC: Beautiful Outstanding - Sweet fruit, Crunchy delicious pear variety",
            "example_sentence": "The _____ pears were perfectly ripe and juicy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bossa",
            "definition": "A style of Brazilian music; part of 'bossa nova'",
            "pronunciation": "/ˈbɑsə/",
            "etymology": "From Portuguese bossa meaning 'trend' or 'style'",
            "memory_tip": "BOSSA: Beautiful Outstanding - South American music, Smooth Amazing rhythms",
            "example_sentence": "The _____ nova rhythm filled the café with smooth, relaxing melodies.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bossiness",
            "definition": "The quality of being domineering or overly controlling",
            "pronunciation": "/ˈbɔsinəs/",
            "etymology": "From bossy + -ness, where bossy comes from boss + -y",
            "memory_tip": "BOSSINESS: Bad Obvious - Controlling behavior, Showing Irritating controlling Nature, Everyone Suffering under dominance, Some people showing control",
            "example_sentence": "Her _____ made it difficult for others to contribute their ideas.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boston",
            "definition": "The capital city of Massachusetts; a card game; a dance",
            "pronunciation": "/ˈbɔstən/",
            "etymology": "Named after Boston, England, or from Massachusett bosutuwon meaning 'at the little big hill'",
            "memory_tip": "BOSTON: Big Outstanding - Seaport Town, Outstanding New England city",
            "example_sentence": "The historic _____ Tea Party was a pivotal moment in American history.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "botany",
            "definition": "The scientific study of plants and their life processes",
            "pronunciation": "/ˈbɑtəni/",
            "etymology": "From Greek botanikos meaning 'of plants', from botane 'plant'",
            "memory_tip": "BOTANY: Basic Outstanding - Teaching About plants, And Natural plant science, Year-long scientific study",
            "example_sentence": "She pursued a degree in _____ to better understand plant ecosystems.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "botch",
            "definition": "To carry out a task badly or carelessly; to bungle",
            "pronunciation": "/bɑtʃ/",
            "etymology": "From Middle English bocchen meaning 'to mend' or 'to patch'",
            "memory_tip": "BOTCH: Bad Operation - Totally Careless work, Hurting the final result",
            "example_sentence": "He managed to _____ the simple repair job completely.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "both",
            "definition": "The two together; one and the other",
            "pronunciation": "/boʊθ/",
            "etymology": "From Old English ba meaning 'both', from Proto-Germanic bai",
            "memory_tip": "BOTH: Basic Operation - Together equally, Holding two things together",
            "example_sentence": "_____ children enjoyed the trip to the zoo.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bother",
            "definition": "To trouble or annoy; to make the effort to do something",
            "pronunciation": "/ˈbɑðər/",
            "etymology": "Possibly from Irish bodhaire meaning 'to deafen' or 'to trouble'",
            "memory_tip": "BOTHER: Bad Operation - Troubling someone, Hurting Everyone's peace, Really annoying others",
            "example_sentence": "Please don't _____ me while I'm trying to concentrate.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bottle",
            "definition": "A container with a narrow neck for holding liquids",
            "pronunciation": "/ˈbɑtəl/",
            "etymology": "From Old French boteille, from Late Latin buttila 'small cask'",
            "memory_tip": "BOTTLE: Basic Object - Totally Tight container, Liquids Everywhere contained",
            "example_sentence": "She filled the glass _____ with fresh spring water.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bottom",
            "definition": "The lowest part or point; the underside of something",
            "pronunciation": "/ˈbɑtəm/",
            "etymology": "From Old English botm meaning 'lowest part' or 'foundation'",
            "memory_tip": "BOTTOM: Basic Object - Totally at the lowest point, Obviously down, Mostly underneath",
            "example_sentence": "The treasure chest lay at the _____ of the deep lake.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boucle",
            "definition": "A yarn with loops creating a bumpy texture; fabric made from such yarn",
            "pronunciation": "/ˈbukəl/",
            "etymology": "From French bouclé meaning 'curled' or 'buckled'",
            "memory_tip": "BOUCLE: Beautiful Outstanding - Unique fabric, Curly Looped texture, Everything textured",
            "example_sentence": "The designer chose a cream _____ fabric for the elegant sofa.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bouclé",
            "definition": "A yarn with loops creating a bumpy texture; fabric made from such yarn (with accent)",
            "pronunciation": "/ˈbukəl/",
            "etymology": "From French bouclé meaning 'curled' or 'buckled'",
            "memory_tip": "BOUCLÉ: Beautiful Outstanding - Unique fabric, Curly Looped texture, Everyone recognizes textured fabric",
            "example_sentence": "The _____ jacket had an elegant, textured appearance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boudin",
            "definition": "A spicy Cajun sausage made with rice and pork",
            "pronunciation": "/ˈbudɪn/",
            "etymology": "From French boudin meaning 'blood sausage', from Latin botellus 'sausage'",
            "memory_tip": "BOUDIN: Bold Outstanding - Unique spicy sausage, Delicious Ingredient, Never bland flavor",
            "example_sentence": "The Cajun restaurant served authentic _____ with rice and vegetables.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bouffant",
            "definition": "A hairstyle with hair puffed out; having a puffy, voluminous shape",
            "pronunciation": "/buˈfɑnt/",
            "etymology": "From French bouffant meaning 'puffing' or 'swelling', from bouffer 'to puff'",
            "memory_tip": "BOUFFANT: Big Outstanding - Unique hairstyle, Fluffy Fashionable style, Fluffy And Never flat, Totally voluminous hairstyle",
            "example_sentence": "Her _____ hairstyle was perfectly styled for the 1960s themed party.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bough",
            "definition": "A main branch of a tree",
            "pronunciation": "/baʊ/",
            "etymology": "From Old English bog meaning 'arm' or 'shoulder' (of a tree)",
            "memory_tip": "BOUGH: Big Outstanding - Usually Growing from tree trunk, Heavy tree branch",
            "example_sentence": "The heavy _____ broke under the weight of the snow.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bouillon",
            "definition": "A clear broth made from meat, fish, or vegetables",
            "pronunciation": "/ˈbuljən/",
            "etymology": "From French bouillon, from bouillir meaning 'to boil'",
            "memory_tip": "BOUILLON: Basic Outstanding - Usually in soup, Liquid broth, Liquid Ingredient, Obviously for cooking, Never solid food",
            "example_sentence": "She added the chicken _____ to enhance the soup's flavor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boulevardier",
            "definition": "A wealthy man about town; a frequenter of fashionable places",
            "pronunciation": "/ˌbuləvɑrˈdir/",
            "etymology": "From French boulevardier, from boulevard + -ier suffix",
            "memory_tip": "BOULEVARDIER: Big Outstanding - Urban sophisticated person, Lives Elegantly, Very wealthy And Really cultured, Dressed like gentleman, Impressive social figure, Everyone Recognizes wealthy lifestyle",
            "example_sentence": "The well-dressed _____ was seen at all the finest restaurants in the city.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bounce",
            "definition": "To spring back after hitting a surface; to move in a lively manner",
            "pronunciation": "/baʊns/",
            "etymology": "From Middle English bunsen meaning 'to beat' or 'to thump'",
            "memory_tip": "BOUNCE: Basic Operation - Usually springs back, Never staying down, Coming back up, Everyone knows this motion",
            "example_sentence": "The basketball began to _____ rapidly on the gymnasium floor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bounding",
            "definition": "Moving with leaping strides; jumping with energy",
            "pronunciation": "/ˈbaʊndɪŋ/",
            "etymology": "From bound + -ing, where bound comes from Old French bondir 'to leap'",
            "memory_tip": "BOUNDING: Bold Outstanding - Usually energetic movement, Never slow motion, Definitely enthusiastic, Incredibly energetic motion, Never Getting tired",
            "example_sentence": "The excited dog came _____ across the field toward its owner.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bountiful",
            "definition": "Abundant and copious; generous in giving",
            "pronunciation": "/ˈbaʊntɪfəl/",
            "etymology": "From bounty + -ful, where bounty comes from Old French bonte 'goodness'",
            "memory_tip": "BOUNTIFUL: Beautiful Outstanding - Usually Numerous abundant things, Totally Incredible abundance, Filled with generous gifts, Usually Large amounts",
            "example_sentence": "The harvest was _____ this year, providing food for the entire community.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bouquet",
            "definition": "An arrangement of flowers; a distinctive scent or flavor",
            "pronunciation": "/buˈkeɪ/",
            "etymology": "From French bouquet meaning 'little wood' or 'cluster'",
            "memory_tip": "BOUQUET: Beautiful Outstanding - Usually collected flowers, Quality fragrant arrangement, Usually Elegant flower arrangement, Together flowers",
            "example_sentence": "He presented her with a _____ of red roses for their anniversary.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bourgeois",
            "definition": "Of or relating to the middle class; conventional or materialistic",
            "pronunciation": "/bʊrˈʒwɑ/",
            "etymology": "From French bourgeois meaning 'townsman', from bourg 'town'",
            "memory_tip": "BOURGEOIS: Basic Organization - Usually wealthy people, Really Generating wealth, Everyone Obviously comfortable lifestyle, Interested in material things, Some wealthy people",
            "example_sentence": "The novel criticized the _____ values of 19th-century society.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boutade",
            "definition": "A sudden outburst or whim; a creative inspiration",
            "pronunciation": "/buˈtɑd/",
            "etymology": "From French boutade meaning 'sudden start' or 'whim'",
            "memory_tip": "BOUTADE: Bold Outstanding - Unexpected sudden idea, Totally Amazing creative impulse, Definitely Explosive creative energy",
            "example_sentence": "The artist's latest painting was inspired by a sudden _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boutonniere",
            "definition": "A flower or small bouquet worn on a man's lapel",
            "pronunciation": "/ˌbutənˈjɛr/",
            "etymology": "From French boutonnière meaning 'buttonhole'",
            "memory_tip": "BOUTONNIERE: Beautiful Outstanding - Usually formal decoration, Traditionally On men's jacket, Obviously Nice elegant accessory, Nice flower on lapel, Including Elegant formal wear, Everyone Recognizes wedding accessory",
            "example_sentence": "The groom wore a white rose _____ that matched the bride's bouquet.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bovines",
            "definition": "Cattle or other members of the ox family; cows and bulls",
            "pronunciation": "/ˈboʊvaɪnz/",
            "etymology": "From Latin bovinus meaning 'of cattle', from bos 'cow'",
            "memory_tip": "BOVINES: Big Outstanding - Very Important farm animals, Including cattle, Never wild animals, Everyone knows farm animals, Something cattle",
            "example_sentence": "The pasture was filled with grazing _____ enjoying the warm sunshine.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bowie",
            "definition": "A large hunting knife with a curved blade; associated with Jim Bowie",
            "pronunciation": "/ˈboʊi/",
            "etymology": "Named after James Bowie, American pioneer and soldier",
            "memory_tip": "BOWIE: Big Outstanding - Weapon for cutting, Important Equipment",
            "example_sentence": "The frontiersman carried a sharp _____ knife on his belt.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bowl",
            "definition": "A round container for food; to play bowling; a stadium",
            "pronunciation": "/boʊl/",
            "etymology": "From Old English bolla meaning 'cup' or 'bowl'",
            "memory_tip": "BOWL: Basic Object - Wide container, Liquids fit inside",
            "example_sentence": "She filled the ceramic _____ with fresh fruit.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bowlerphantom",
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
            "word": "bowsprit",
            "definition": "A spar projecting from the front of a ship's bow",
            "pronunciation": "/ˈboʊsprɪt/",
            "etymology": "From Middle Dutch boechspriet, from boech 'bow' + spriet 'pole'",
            "memory_tip": "BOWSPRIT: Big Outstanding - Water ship equipment, Sailing Perfectly positioned, Really Important sailing equipment, Incredibly Tactical ship part",
            "example_sentence": "The ship's _____ cut through the waves as it sailed into the harbor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bowyer",
            "definition": "A person who makes bows for archery",
            "pronunciation": "/ˈboʊjər/",
            "etymology": "From bow + -yer suffix (meaning 'one who works with')",
            "memory_tip": "BOWYER: Basic Outstanding - Worker making archery equipment, Year-round craftsman, Everyone Recognizes bow maker",
            "example_sentence": "The skilled _____ crafted custom bows for the archery competition.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boxer",
            "definition": "A person who fights with fists as a sport; a breed of dog",
            "pronunciation": "/ˈbɑksər/",
            "etymology": "From box (to fight) + -er, where box comes from Middle English",
            "memory_tip": "BOXER: Bold Outstanding - athlete, eXcellent fighter, Everyone Recognizes fighting sport",
            "example_sentence": "The professional _____ trained for hours every day preparing for the championship.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boycott",
            "definition": "To refuse to buy from or deal with as a form of protest",
            "pronunciation": "/ˈbɔɪkɑt/",
            "etymology": "Named after Charles Boycott, Irish land agent who was ostracized in 1880",
            "memory_tip": "BOYCOTT: Basic Operation - You refuse to support, Completely avoiding business, Obviously Taking a stand, Together protesting",
            "example_sentence": "Consumers decided to _____ the company until it changed its labor practices.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "boycottcalzone",
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
            "word": "bozzetto",
            "definition": "A small clay or wax model for a sculpture; a preliminary sketch",
            "pronunciation": "/boˈtsɛtoʊ/",
            "etymology": "From Italian bozzetto meaning 'small sketch', from bozza 'rough draft'",
            "memory_tip": "BOZZETTO: Beautiful Outstanding - Zestful artistic work, Zestful Early art model, Testing art ideas, Talented artist's model, Outstanding sculpture preparation",
            "example_sentence": "The sculptor created a detailed _____ before beginning work on the full-sized statue.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brac",
            "definition": "A fragment or piece, especially of pottery or stone",
            "pronunciation": "/bræk/",
            "etymology": "From Old Norse brǫk meaning 'debris' or 'fragments'",
            "memory_tip": "BRAC: Basic Remaining - Archaeological artifact, Collected by archaeologists",
            "example_sentence": "The archaeologist carefully catalogued each _____ found at the ancient site.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brachiopods",
            "definition": "Marine animals with two shells, resembling but unrelated to clams",
            "pronunciation": "/ˈbreɪkiəˌpɑdz/",
            "etymology": "From Greek brachion 'arm' + pous 'foot', referring to their feeding apparatus",
            "memory_tip": "BRACHIOPODS: Basic Really - Ancient sea creatures, Commonly Having shells, Including Ocean fossils, Obviously Prehistoric sea life, Diverse Sea creatures",
            "example_sentence": "The paleontologist discovered well-preserved _____ fossils in the limestone.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brackish",
            "definition": "Water that is somewhat salty, between fresh and salt water",
            "pronunciation": "/ˈbrækɪʃ/",
            "etymology": "From Dutch brak meaning 'salty' + -ish suffix",
            "memory_tip": "BRACKISH: Basic Really - And slightly salty water, Carefully mixing salt with fresh water, Keeping some salt taste, Including Some Halite minerals",
            "example_sentence": "The estuary contained _____ water where the river met the sea.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "braeburn",
            "definition": "A variety of apple with red and yellow skin and crisp flesh",
            "pronunciation": "/ˈbreɪbərn/",
            "etymology": "Named after Braeburn Orchard in New Zealand where it was first grown",
            "memory_tip": "BRAEBURN: Beautiful Red - Apple variety, Everyone likes crispy fruit, Beautiful colorful apple, Usually eaten fresh, Really Nice fruit",
            "example_sentence": "The _____ apples were perfect for making a crisp autumn pie.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "braggart",
            "definition": "A person who boasts about their achievements or possessions",
            "pronunciation": "/ˈbræɡərt/",
            "etymology": "From brag + -art suffix (meaning 'one who does excessively')",
            "memory_tip": "BRAGGART: Bad Rude - Always Grossly boasting, Getting everyone's Attention, Really annoying behavior, Totally showing off",
            "example_sentence": "The _____ constantly told stories about his supposed accomplishments.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "braids",
            "definition": "Hair arranged in interwoven strands; decorative cords",
            "pronunciation": "/breɪdz/",
            "etymology": "From Old English bregdan meaning 'to weave' or 'to intertwine'",
            "memory_tip": "BRAIDS: Beautiful Rope - Always Interwoven hair, Decorative hair Style",
            "example_sentence": "She wore her long hair in intricate _____ for the cultural celebration.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "braille",
            "definition": "A system of raised dots that allows blind people to read by touch",
            "pronunciation": "/breɪl/",
            "etymology": "Named after Louis Braille, who invented the system in 1824",
            "memory_tip": "BRAILLE: Basic Reading - Always Important for blind people, Lets everyone read by touch, Learning Everything by touch",
            "example_sentence": "The library had an extensive collection of books printed in _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "braillevignette",
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
            "word": "brain",
            "definition": "The organ that controls thought, memory, and body functions",
            "pronunciation": "/breɪn/",
            "etymology": "From Old English brægen, from Proto-Germanic bragnjan",
            "memory_tip": "BRAIN: Basic Really - Amazing Intelligence center, Never stops working",
            "example_sentence": "The human _____ contains approximately 86 billion neurons.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brambles",
            "definition": "Prickly shrubs, especially wild blackberry bushes",
            "pronunciation": "/ˈbræmbəlz/",
            "etymology": "From Old English bræmbel, related to broom (the plant)",
            "memory_tip": "BRAMBLES: Basic Really - Always thorny plants, Making walking difficult, Blocking paths Everywhere, Lots of thorns, Everyone avoids sharp plants, Something prickly",
            "example_sentence": "The children picked berries carefully to avoid the sharp _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "branch",
            "definition": "A part of a tree that grows from the trunk; a division of an organization",
            "pronunciation": "/bræntʃ/",
            "etymology": "From Old French branche, from Late Latin branca meaning 'paw'",
            "memory_tip": "BRANCH: Basic Really - Always Naturally growing from tree, Connecting Hanging leaves",
            "example_sentence": "The bird built its nest on a sturdy _____ of the oak tree.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brand",
            "definition": "A particular make of product; to mark with a hot iron",
            "pronunciation": "/brænd/",
            "etymology": "From Old English brand meaning 'fire' or 'torch'",
            "memory_tip": "BRAND: Basic Recognition - Always Noticeable company mark, Distinguishing products",
            "example_sentence": "The company's _____ became synonymous with quality and reliability.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_023_processed.csv"
    
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
        
        print(f"Batch 023 processing complete!")
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