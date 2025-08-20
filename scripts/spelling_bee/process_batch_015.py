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
            "word": "auspices",
            "definition": "Guidance and protection provided by someone or a divine power; favorable circumstances",
            "pronunciation": "/ˈɔspɪsəz/",
            "etymology": "From Latin auspicium meaning 'divination by observing birds', from avis 'bird' + specere 'to look at'",
            "memory_tip": "AUSPICES: Ancient bird watchers Used Signs - People Interpreted bird flight patterns, Considered Ensuring good fortune, Success",
            "example_sentence": "The new community center was built under the _____ of the local government.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "austere",
            "definition": "Severely simple and unadorned; strict or stern in manner",
            "pronunciation": "/ɔˈstɪr/",
            "etymology": "From Latin austerus meaning 'harsh, sour, severe', from Greek austeros meaning 'making the tongue dry'",
            "memory_tip": "AUSTERE: Absolutely no Unnecessary Style - Totally Eliminating Relaxed Environments",
            "example_sentence": "The monk lived an _____ life with minimal possessions and simple food.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "australian",
            "definition": "Relating to Australia or its people",
            "pronunciation": "/ɔˈstreɪliən/",
            "etymology": "From Australia (from Latin terra australis meaning 'southern land') + -an suffix",
            "memory_tip": "AUSTRALIAN: A continent Under Southern hemisphere - The Really Amazing Land Is with Abundant Natural animals",
            "example_sentence": "The _____ wildlife includes many unique species like kangaroos and koalas.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "auteur",
            "definition": "A filmmaker who exercises creative control and has a distinctive personal style",
            "pronunciation": "/oʊˈtɜr/",
            "etymology": "From French auteur meaning 'author', from Latin auctor meaning 'originator, creator'",
            "memory_tip": "AUTEUR: Artist Using Total control - Everyone Understands this director has personal flair",
            "example_sentence": "The acclaimed director was considered an _____ for his unique cinematic vision.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "authenticate",
            "definition": "To prove or verify that something is genuine or valid",
            "pronunciation": "/ɔˈθɛntɪˌkeɪt/",
            "etymology": "From Greek authentikos meaning 'original, genuine', from authentes 'master, one acting on his own authority'",
            "memory_tip": "AUTHENTICATE: Always Understand - These are the things To Help validate Evidence, Not Take Invalid Claims As Truth Even",
            "example_sentence": "The museum hired experts to _____ the newly discovered ancient artifacts.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "authenticatefiscal",
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
            "word": "authority",
            "definition": "The power or right to give orders and enforce obedience; expert knowledge",
            "pronunciation": "/əˈθɔrəti/",
            "etymology": "From Old French autorite, from Latin auctoritas meaning 'influence, command', from auctor 'originator'",
            "memory_tip": "AUTHORITY: Always Understands - This Higher Official person Reliably Influences Through Years of experience",
            "example_sentence": "The principal had the _____ to make important decisions about school policies.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "autism",
            "definition": "A developmental disorder characterized by difficulties in social interaction and communication",
            "pronunciation": "/ˈɔtɪzəm/",
            "etymology": "From Greek autos meaning 'self' + -ism, referring to self-absorption",
            "memory_tip": "AUTISM: A Unique brain Type - Individuals Special Mind processes information differently",
            "example_sentence": "The school provided specialized support for students with _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "autodidact",
            "definition": "A self-taught person who learns without formal instruction",
            "pronunciation": "/ˈɔtoʊˌdaɪdækt/",
            "etymology": "From Greek autodidaktos meaning 'self-taught', from autos 'self' + didaskein 'to teach'",
            "memory_tip": "AUTODIDACT: Always Teaching oneself - Understanding Through Original Discovery - Independently Developing Advanced Cognitive Training",
            "example_sentence": "The famous inventor was an _____ who never attended engineering school.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "autographs",
            "definition": "Signatures or handwritten items by famous people; signs one's name",
            "pronunciation": "/ˈɔtəˌɡræfs/",
            "etymology": "From Greek autos 'self' + graphein 'to write'",
            "memory_tip": "AUTOGRAPHS: Always Taking Original - Genuine Representative Art, Personal Handwriting Signatures",
            "example_sentence": "The fans eagerly collected _____ from their favorite celebrities.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "autophagy",
            "definition": "The process by which cells break down and recycle their own components",
            "pronunciation": "/ɔˈtɑfədʒi/",
            "etymology": "From Greek autos 'self' + phagein 'to eat'",
            "memory_tip": "AUTOPHAGY: Always Taking Old - Proteins Hurting cells - Actively Getting rid of worn out cellular parts, Yielding health",
            "example_sentence": "Scientists study _____ to understand how cells maintain themselves by recycling damaged proteins.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "available",
            "definition": "Able to be used or obtained; present and ready for use",
            "pronunciation": "/əˈveɪləbəl/",
            "etymology": "From avail (from Old French avaler 'to lower, to be of use') + -able suffix",
            "memory_tip": "AVAILABLE: Always Very Accessible - In Location And can Be Immediately Leveraged - Everyone can access",
            "example_sentence": "The library books are _____ for checkout by all students.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avalanche",
            "definition": "A large mass of snow, ice, and rocks falling rapidly down a mountainside",
            "pronunciation": "/ˈævəˌlæntʃ/",
            "etymology": "From French avalanche, possibly from Franco-Provençal lavantse, related to Latin lavare 'to wash'",
            "memory_tip": "AVALANCHE: Always Very Aggressive - Loud And Natural Catastrophic Hazard Event",
            "example_sentence": "The mountaineers took shelter when they heard the rumble of an approaching _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avalon",
            "definition": "In Arthurian legend, a mythical island paradise where King Arthur was taken",
            "pronunciation": "/ˈævəˌlɑn/",
            "etymology": "From Welsh Ynys Afallach meaning 'isle of apples', or possibly from Celtic abal meaning 'apple'",
            "memory_tip": "AVALON: Arthurian legend's Virtual Adventure - Legendary island Of paradise, Natural sanctuary",
            "example_sentence": "According to legend, King Arthur was taken to _____ to heal from his wounds.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avarice",
            "definition": "Extreme greed for wealth or material gain",
            "pronunciation": "/ˈævərɪs/",
            "etymology": "From Old French avarice, from Latin avaritia meaning 'greed', from avarus 'greedy'",
            "memory_tip": "AVARICE: Always Very Aggressive - Relentless pursuit of money, Insatiable Craving for Everything",
            "example_sentence": "His _____ led him to make unethical business decisions for personal profit.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avatar",
            "definition": "A digital representation of a person; an incarnation or embodiment",
            "pronunciation": "/ˈævəˌtɑr/",
            "etymology": "From Sanskrit avatara meaning 'descent', from ava 'down' + tarati 'he crosses'",
            "memory_tip": "AVATAR: A Virtual Artistic Representation - Anyone's digital persona, Taking Alternative visual form",
            "example_sentence": "She customized her _____ to look exactly like herself in the virtual world.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avens",
            "definition": "A type of flowering plant in the rose family with yellow or white flowers",
            "pronunciation": "/ˈeɪvənz/",
            "etymology": "From Middle English, from Old French avence, possibly from a pre-Indo-European source",
            "memory_tip": "AVENS: A Versatile Elegant Natural flower - Species in rose family",
            "example_sentence": "The mountain _____ bloomed brightly among the rocky alpine terrain.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avenue",
            "definition": "A wide road or path; a way of approaching a problem or opportunity",
            "pronunciation": "/ˈævəˌnu/",
            "etymology": "From French avenue meaning 'approach', from avenir 'to come to', from Latin advenire",
            "memory_tip": "AVENUE: A Very Elegant route - New Urban Environment pathway",
            "example_sentence": "The tree-lined _____ led directly to the grand entrance of the mansion.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aversion",
            "definition": "A strong dislike or disinclination toward something",
            "pronunciation": "/əˈvɜrʒən/",
            "etymology": "From Latin aversio meaning 'a turning away', from avertere 'to turn away'",
            "memory_tip": "AVERSION: Actively Very against - Everyone Rejects Something that causes negative reaction",
            "example_sentence": "She had a strong _____ to public speaking and avoided it whenever possible.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avgolemono",
            "definition": "A Greek soup made with eggs, lemon juice, and rice or orzo",
            "pronunciation": "/ˌɑvɡoʊˈlɛmoʊnoʊ/",
            "etymology": "From Greek avgolemono, from avgo 'egg' + lemoni 'lemon'",
            "memory_tip": "AVGOLEMONO: A Very Greek bowl Of Lemon Egg soup - Making Nutritious Offerings",
            "example_sentence": "The restaurant's _____ was perfectly creamy with a bright lemon flavor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aviation",
            "definition": "The operation and navigation of aircraft; the aircraft industry",
            "pronunciation": "/ˌeɪviˈeɪʃən/",
            "etymology": "From Latin avis meaning 'bird' + -ation suffix",
            "memory_tip": "AVIATION: Always Very Inspiring - Aircraft Transportation Innovation, Operating aircraft Naturally",
            "example_sentence": "He pursued a career in _____ and became a commercial airline pilot.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avifauna",
            "definition": "The birds of a particular region, habitat, or geological period",
            "pronunciation": "/ˌeɪvɪˈfɔnə/",
            "etymology": "From Latin avis 'bird' + fauna 'animals of a region'",
            "memory_tip": "AVIFAUNA: All Various Indigenous Flying Animals - Understanding Natural Animals of specific regions",
            "example_sentence": "The tropical rainforest supported a diverse _____ including colorful parrots and toucans.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avoid",
            "definition": "To keep away from or prevent something from happening",
            "pronunciation": "/əˈvɔɪd/",
            "etymology": "From Old French evuidier meaning 'to empty out', from Latin ex- 'out' + viduus 'empty'",
            "memory_tip": "AVOID: Always Very Overt about staying away - Intentionally Distance yourself",
            "example_sentence": "She tried to _____ walking through the construction zone for safety reasons.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avuncular",
            "definition": "Kind and friendly toward a younger person; like a benevolent uncle",
            "pronunciation": "/əˈvʌŋkjələr/",
            "etymology": "From Latin avunculus meaning 'maternal uncle', diminutive of avus 'grandfather'",
            "memory_tip": "AVUNCULAR: Always Very Understanding - Nice Caring Uncle-Like caring Adult person",
            "example_sentence": "The professor's _____ manner made students feel comfortable asking questions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "avversiera",
            "definition": "A type of traditional Italian glazed ceramic pottery with distinctive patterns",
            "pronunciation": "/ˌɑvərˈsjɛrə/",
            "etymology": "From Italian avversiera, regional term for a specific type of ceramic work",
            "memory_tip": "AVVERSIERA: Artisan Very Vibrant - Elaborate ceramic pottery, Richly Styled Italian Elegant ceramic artwork, A specific style pattern",
            "example_sentence": "The museum displayed beautiful examples of traditional _____ pottery from Renaissance Italy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "award",
            "definition": "To give something as a prize or honor; a prize or honor given",
            "pronunciation": "/əˈwɔrd/",
            "etymology": "From Anglo-Norman awarder meaning 'to decide, grant', from a- 'to' + warder 'to guard'",
            "memory_tip": "AWARD: Always Well-deserved - Admirable Recognition for Distinguished work",
            "example_sentence": "The committee will _____ the scholarship to the most deserving student.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aware",
            "definition": "Having knowledge or perception of a situation or fact",
            "pronunciation": "/əˈwɛr/",
            "etymology": "From Old English gewær meaning 'wary, cautious', from Proto-Germanic ga-waraz",
            "memory_tip": "AWARE: Always Watching - Actively Recognizing Everything around you",
            "example_sentence": "She became _____ of the approaching storm from the darkening clouds.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "awesome",
            "definition": "Inspiring awe or admiration; extremely impressive",
            "pronunciation": "/ˈɔsəm/",
            "etymology": "From awe + -some suffix, where awe comes from Old Norse agi meaning 'terror'",
            "memory_tip": "AWESOME: Absolutely Wonderful - Everybody Sees Outstanding Magnificent Events",
            "example_sentence": "The _____ view from the mountain peak took their breath away.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "awfully",
            "definition": "Very; extremely (informal intensifier); in a terrible manner",
            "pronunciation": "/ˈɔfəli/",
            "etymology": "From awful + -ly, where awful originally meant 'inspiring awe'",
            "memory_tip": "AWFULLY: Absolutely - Wonder Fully emphasizing extremely, Lots of intensity, very much",
            "example_sentence": "The weather was _____ cold during the winter camping trip.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "awkwardly",
            "definition": "In a clumsy or uncomfortable manner; in a way that causes embarrassment",
            "pronunciation": "/ˈɔkwərdli/",
            "etymology": "From awkward + -ly, where awkward comes from Middle English awkeward meaning 'turned the wrong way'",
            "memory_tip": "AWKWARDLY: Actions Walking Klumsily - Weirdly And Really Distinctly clumsily, Looking very unnatural in motion, with discomfort",
            "example_sentence": "He _____ dropped his books while trying to impress his classmates.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "awry",
            "definition": "Away from the correct or expected course; amiss or wrong",
            "pronunciation": "/əˈraɪ/",
            "etymology": "From Middle English, from a- 'on' + wry 'twisted'",
            "memory_tip": "AWRY: Always Wrong - Rotating off course, not going as You planned",
            "example_sentence": "Their carefully planned surprise party went _____ when the guest of honor arrived early.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "awryb",
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
            "word": "axiomatic",
            "definition": "Self-evidently true; taken as established fact without proof",
            "pronunciation": "/ˌæksiəˈmætɪk/",
            "etymology": "From Greek axiomatikos, from axioma meaning 'that which is thought worthy', from axios 'worthy'",
            "memory_tip": "AXIOMATIC: Absolutely eXpected - Immediately Obvious - Mathematical And True principles Inherent in foundations, Clearly obvious truth",
            "example_sentence": "It was _____ that students who studied more would perform better on exams.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "axis",
            "definition": "An imaginary line about which a body rotates; a fixed reference line",
            "pronunciation": "/ˈæksɪs/",
            "etymology": "From Latin axis meaning 'axle, axis', possibly related to Greek axon 'axle'",
            "memory_tip": "AXIS: Always eXact - Imaginary line - Straight through center",
            "example_sentence": "The Earth rotates on its _____ once every twenty-four hours.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "axle",
            "definition": "A rod or spindle passing through the center of a wheel",
            "pronunciation": "/ˈæksəl/",
            "etymology": "From Middle English axel, from Old Norse öxull, related to axis",
            "memory_tip": "AXLE: Always eXtends through wheel center - Lets vehicle wheels Efficiently turn",
            "example_sentence": "The mechanic replaced the broken _____ to fix the wobbling wheel.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ayurvedic",
            "definition": "Relating to Ayurveda, a traditional Hindu system of medicine",
            "pronunciation": "/ˌaɪjʊrˈveɪdɪk/",
            "etymology": "From Sanskrit ayurveda, from ayus 'life' + veda 'knowledge'",
            "memory_tip": "AYURVEDIC: Ancient Yoga Understanding - Restoring Vitality through Early holistic healing Discipline - Indian medical practice, healing Complex conditions",
            "example_sentence": "She consulted an _____ practitioner for natural treatments to improve her health.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "azedarach",
            "definition": "A tree in the mahogany family, also known as chinaberry or bead tree",
            "pronunciation": "/əˈzɛdərˌæk/",
            "etymology": "From Persian azad-darakht meaning 'free tree', from azad 'free' + darakht 'tree'",
            "memory_tip": "AZEDARACH: A tree that grows Zealously - Everyone Definitely Admires its Rapid growth And Characteristic berries, Hardiness",
            "example_sentence": "The _____ tree produced clusters of small purple berries that birds enjoyed.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "azorestankard",
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
            "word": "azotea",
            "definition": "A flat roof terrace or rooftop used as a living space in Hispanic architecture",
            "pronunciation": "/ˌɑzəˈteɪə/",
            "etymology": "From Spanish azotea, from Arabic as-sutayha meaning 'the little terrace'",
            "memory_tip": "AZOTEA: Amazing Zenith - Outdoor Terrace Everyone enjoys - Atop roof space",
            "example_sentence": "The family gathered on the _____ to enjoy the evening breeze and city views.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aztec",
            "definition": "Relating to the Aztecs, a Mesoamerican civilization that flourished in central Mexico",
            "pronunciation": "/ˈæztɛk/",
            "etymology": "From Spanish azteca, from Nahuatl aztecatl meaning 'people from Aztlan'",
            "memory_tip": "AZTEC: Ancient Zealous - Talented Empire with Complex pyramids and culture",
            "example_sentence": "The museum displayed beautiful _____ artifacts including gold jewelry and stone carvings.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "azulejo",
            "definition": "A form of Spanish and Portuguese painted tin-glazed ceramic tilework",
            "pronunciation": "/ˌɑzuˈleɪhoʊ/",
            "etymology": "From Spanish/Portuguese azulejo, from Arabic az-zulaykha meaning 'little polished stone'",
            "memory_tip": "AZULEJO: Amazing azure Unique - Little Elegant decorative tiles from ancient times, Joining Ornamental patterns",
            "example_sentence": "The palace walls were covered with intricate blue and white _____ depicting historical scenes.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "azulejoorganized",
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
            "word": "baby",
            "definition": "A very young child; an infant",
            "pronunciation": "/ˈbeɪbi/",
            "etymology": "From Middle English babi, possibly from babbling sounds infants make",
            "memory_tip": "BABY: Beautiful And adorable person - Born Young, innocent",
            "example_sentence": "The _____ giggled happily when her mother played peek-a-boo.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baccate",
            "definition": "Berry-like; having a pulpy fruit with seeds embedded in the flesh",
            "pronunciation": "/ˈbækeɪt/",
            "etymology": "From Latin baccatus meaning 'having berries', from bacca 'berry'",
            "memory_tip": "BACCATE: Berries And fruit Contents - Creating Attractive Tasty fruit Easily recognizable",
            "example_sentence": "The _____ fruits of the elderberry bush were dark purple and clustered together.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bachelorette",
            "definition": "An unmarried young woman; a woman celebrating before her wedding",
            "pronunciation": "/ˌbætʃələˈrɛt/",
            "etymology": "From bachelor + -ette (feminine suffix), where bachelor comes from Old French bacheler",
            "memory_tip": "BACHELORETTE: Beautiful And Cheerful - Having Exciting Life Occasions - Relaxed, Exciting fun Times - Taking Everybody out for celebration",
            "example_sentence": "The bride-to-be enjoyed her _____ party with her closest friends.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "back",
            "definition": "The rear surface of the human body; to support or move backward",
            "pronunciation": "/bæk/",
            "etymology": "From Old English bæc, from Proto-Germanic bakam",
            "memory_tip": "BACK: Behind And Curved anatomy - Keeps your body upright and strong",
            "example_sentence": "She carried the heavy backpack that strained her _____ during the long hike.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "backgammon",
            "definition": "A board game for two players with pieces moved according to dice rolls",
            "pronunciation": "/ˈbækˌɡæmən/",
            "etymology": "From back + gammon (Middle English gamen 'game'), referring to pieces sent back",
            "memory_tip": "BACKGAMMON: Board And Checkers - Knights Gamble And Move Moving Over Numbered spaces",
            "example_sentence": "They spent the evening playing _____ by the fireplace.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "backgammonintuitable",
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
            "word": "background",
            "definition": "The area behind the main focus; a person's education and experience",
            "pronunciation": "/ˈbækˌɡraʊnd/",
            "etymology": "From back + ground, originally referring to the part of a picture behind the main subjects",
            "memory_tip": "BACKGROUND: Behind And Covering - Knowledge, Growing personal history, Records Of Understanding, Notable past experiences, Developing over time",
            "example_sentence": "Her strong academic _____ in science helped her excel in medical school.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bacteriolytic",
            "definition": "Capable of destroying or dissolving bacteria",
            "pronunciation": "/bækˌtɪrioʊˈlɪtɪk/",
            "etymology": "From bacterio- (from Greek bakterion 'small rod') + lytic (from Greek lytikos 'able to dissolve')",
            "memory_tip": "BACTERIOLYTIC: Bacteria - Actively Crushing These microorganisms, Entirely Reducing Infections - Obliterating germs, Lysing bacteria Rapidly, yielding immunity Through totally destroying, Intense medical Compound agents",
            "example_sentence": "The new _____ enzyme showed promise in treating antibiotic-resistant infections.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_015_processed.csv"
    
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
        
        print(f"Batch 015 processing complete!")
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