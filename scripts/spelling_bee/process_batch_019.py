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
            "word": "believed",
            "definition": "Past tense of believe; accepted as true or real",
            "pronunciation": "/bɪˈlivd/",
            "etymology": "From Middle English beleven, from Old English belefan, from be- + lief 'dear'",
            "memory_tip": "BELIEVED: Before Everyone - Learned and accepted Ideas, Everyone Valued truth, Everyone Decided to trust",
            "example_sentence": "She _____ in the importance of education and hard work.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "believers",
            "definition": "Plural of believer; people who have faith or trust in something",
            "pronunciation": "/bɪˈlivərz/",
            "etymology": "From believer + -s, where believer comes from believe + -er suffix",
            "memory_tip": "BELIEVERS: Before Everyone - Learned Ideas, Everyone Values truth, Everyone Really Shares faith",
            "example_sentence": "The _____ gathered every Sunday for worship and community fellowship.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bell",
            "definition": "A hollow metal device that makes a ringing sound when struck",
            "pronunciation": "/bɛl/",
            "etymology": "From Old English belle, from Proto-Germanic bella",
            "memory_tip": "BELL: Beautiful Echoing - Loud resonating sound, Listeners enjoy the chimes",
            "example_sentence": "The church _____ rang out across the village every hour.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bellatrix",
            "definition": "A bright star in the constellation Orion; a female warrior",
            "pronunciation": "/bəˈleɪtrɪks/",
            "etymology": "From Latin bellatrix meaning 'female warrior', from bellator 'warrior'",
            "memory_tip": "BELLATRIX: Bright star - Exceptional Light appearing in constellation, Amazing Tremendous star, Really Important eXtraordinary celestial object",
            "example_sentence": "_____ is one of the most luminous stars visible in the winter sky.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "belle",
            "definition": "A beautiful woman; the most attractive woman at a social gathering",
            "pronunciation": "/bɛl/",
            "etymology": "From French belle meaning 'beautiful', feminine of bel",
            "memory_tip": "BELLE: Beautiful Elegant - Lovely Lady, Everyone admires her beauty",
            "example_sentence": "She was considered the _____ of the ball in her stunning evening gown.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bellwether",
            "definition": "A leader or indicator of trends; originally a sheep with a bell around its neck",
            "pronunciation": "/ˈbɛlˌwɛðər/",
            "etymology": "From bell + wether (castrated male sheep), referring to the lead sheep with a bell",
            "memory_tip": "BELLWETHER: Bell Wearing - Everyone Looks at this Leader, Weather predictive indicator, Everyone Takes direction, Helpful Early indicator, Everyone Recognizes trends",
            "example_sentence": "The state is often considered a _____ for national political trends.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bellyache",
            "definition": "A stomach pain; to complain persistently",
            "pronunciation": "/ˈbɛliˌeɪk/",
            "etymology": "From belly + ache, literally referring to pain in the belly area",
            "memory_tip": "BELLYACHE: Bad Eating - Lots of discomfort, Yucky Aching stomach, Complaining Hurts Everyone",
            "example_sentence": "The child had a _____ after eating too much candy at the party.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "belongs",
            "definition": "Third person singular of belong; is the property of or is a member of",
            "pronunciation": "/bɪˈlɔŋz/",
            "etymology": "From Middle English belongen, from be- + longen 'to be suitable'",
            "memory_tip": "BELONGS: Being Everyone's - Love and ownership, Naturally Goes together, Someone's possession",
            "example_sentence": "This book _____ to the library and must be returned by Friday.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beloved",
            "definition": "Dearly loved; a person who is loved",
            "pronunciation": "/bɪˈlʌvɪd/",
            "etymology": "From be- + loved, meaning 'greatly loved'",
            "memory_tip": "BELOVED: Being Everyone's - Love and devotion, Obvious Valued person, Everyone's Dear one",
            "example_sentence": "The _____ teacher was remembered fondly by generations of students.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "below",
            "definition": "At a lower level or position; underneath",
            "pronunciation": "/bɪˈloʊ/",
            "etymology": "From Middle English bilogh, from bi 'by' + logh 'low'",
            "memory_tip": "BELOW: Being Everyone's - Lower position, Obviously Underneath area, Way down low",
            "example_sentence": "The submarine descended to depths far _____ the ocean surface.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "belt",
            "definition": "A strip of material worn around the waist; a continuous band",
            "pronunciation": "/bɛlt/",
            "etymology": "From Old English belt, from Latin balteus 'sword belt'",
            "memory_tip": "BELT: Basic Equipment - Leather or fabric holding up clothing, Tight around waist",
            "example_sentence": "He tightened his _____ after losing weight during his diet.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "belted",
            "definition": "Past tense of belt; struck forcefully or wore a belt",
            "pronunciation": "/ˈbɛltɪd/",
            "etymology": "From belt + -ed, referring to the action of striking or wearing a belt",
            "memory_tip": "BELTED: Basic Equipment - Leather Tight around waist, Everyone Dressed properly",
            "example_sentence": "The baseball player _____ the ball over the fence for a home run.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "benches",
            "definition": "Plural of bench; long seats for multiple people",
            "pronunciation": "/ˈbɛntʃəz/",
            "etymology": "From Old English benc, from Proto-Germanic bankiz",
            "memory_tip": "BENCHES: Basic Everyone - Nice seating for groups, Comfortable Helpful seats Everyone uses, Seating arrangements",
            "example_sentence": "The park had wooden _____ where visitors could rest and enjoy the scenery.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "benedictinearcane",
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
            "word": "beneficent",
            "definition": "Doing good or causing good to be done; charitable",
            "pronunciation": "/bəˈnɛfɪsənt/",
            "etymology": "From Latin beneficent-, from bene 'well' + facere 'to do'",
            "memory_tip": "BENEFICENT: Being Everyone's - Nice friend, Encouraging Favorable actions, Inspiring good deeds, Creating Everyone's happiness, Everyone Needs These people",
            "example_sentence": "The _____ donor funded scholarships for underprivileged students.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "benefited",
            "definition": "Past tense of benefit; received advantage or profit from something",
            "pronunciation": "/ˈbɛnəˌfɪtɪd/",
            "etymology": "From benefit + -ed, where benefit comes from Latin benefactum 'good deed'",
            "memory_tip": "BENEFITED: Being Everyone's - Nice friend, Everyone Feels good, Improved by experience, Everyone Definitely helped",
            "example_sentence": "The students _____ greatly from the additional tutoring sessions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "benefitted",
            "definition": "Alternative spelling of benefited; received advantage or profit",
            "pronunciation": "/ˈbɛnəˌfɪtɪd/",
            "etymology": "From benefit + -ted, alternative spelling with double 't'",
            "memory_tip": "BENEFITTED: Being Everyone's - Nice friend, Everyone Feels good, Improved by experience, Everyone definitely Twin help, Two T's, Everyone Definitely helped",
            "example_sentence": "The community _____ from the new public transportation system.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bengal",
            "definition": "A region in South Asia; a type of cat breed with spotted markings",
            "pronunciation": "/bɛŋˈɡɔl/",
            "etymology": "From Bengali Bangla, referring to the region in South Asia",
            "memory_tip": "BENGAL: Beautiful Eastern - New Geography Area, Located in south asia",
            "example_sentence": "The _____ tiger is known for its distinctive orange coat with black stripes.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "benighted",
            "definition": "In moral or intellectual darkness; ignorant",
            "pronunciation": "/bɪˈnaɪtɪd/",
            "etymology": "From be- + night + -ed, literally 'overtaken by night', metaphorically 'in darkness'",
            "memory_tip": "BENIGHTED: Being Everyone's - Night shadows, In darkness, Greatly lacking enlightenment, Having Terrible Education, Darkness surrounds them",
            "example_sentence": "The _____ villagers refused to accept modern medical practices.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "benin",
            "definition": "A country in West Africa, formerly known as Dahomey",
            "pronunciation": "/bəˈnin/",
            "etymology": "From the Bini people and the historical Kingdom of Benin in the region",
            "memory_tip": "BENIN: Beautiful Equatorial - Nation In africa, Nice west african country",
            "example_sentence": "_____ is known for its rich cultural heritage and historical bronze sculptures.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "benison",
            "definition": "A blessing; an expression of good wishes",
            "pronunciation": "/ˈbɛnɪsən/",
            "etymology": "From Old French beneiçon, from Latin benedictio 'blessing'",
            "memory_tip": "BENISON: Blessed Everyone - Nice words, Inspiring good fortune, Spiritual blessing, Outstanding wishes, Nice prayer",
            "example_sentence": "The priest offered a _____ for the newlyweds' happiness and prosperity.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bent",
            "definition": "Past tense of bend; curved or crooked; determined or inclined",
            "pronunciation": "/bɛnt/",
            "etymology": "From Old English bendan meaning 'to bend, curve'",
            "memory_tip": "BENT: Basic shape - Everyone Notices curved objects, Twisted shape",
            "example_sentence": "The old tree was _____ from years of strong coastal winds.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beowulf",
            "definition": "An Old English epic poem about a legendary hero",
            "pronunciation": "/ˈbeɪəˌwʊlf/",
            "etymology": "From Old English, possibly meaning 'bee wolf' (kenning for bear) or 'war wolf'",
            "memory_tip": "BEOWULF: Bold Epic - Outstanding Warrior story, Unique Literature, Legendary Fighter hero",
            "example_sentence": "_____ is considered one of the most important works of Old English literature.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "berber",
            "definition": "A member of the indigenous peoples of North Africa; their languages",
            "pronunciation": "/ˈbɜrbər/",
            "etymology": "From Arabic barbar, possibly from Greek barbaros 'foreign'",
            "memory_tip": "BERBER: Beautiful Ethnic - people of Real north african heritage, Brave cultural group, Everyone Respects their traditions",
            "example_sentence": "The _____ tribes have maintained their distinct culture across North Africa.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "berceuse",
            "definition": "A lullaby; a soothing piece of music in lullaby style",
            "pronunciation": "/bɛrˈsøz/",
            "etymology": "From French berceuse, from bercer 'to rock' (as in rocking a baby to sleep)",
            "memory_tip": "BERCEUSE: Beautiful Relaxing - Calming music Everyone enjoys, Useful Soothing music for sleeping, Everyone loves these gentle lullabies",
            "example_sentence": "Chopin's _____ in D-flat major is a beloved piano piece with a gentle, rocking rhythm.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bereavement",
            "definition": "The state of being deprived of someone close through death; grief",
            "pronunciation": "/bɪˈrivmənt/",
            "etymology": "From bereave + -ment, where bereave comes from Old English bereafian 'to rob, deprive'",
            "memory_tip": "BEREAVEMENT: Being Everyone - Remembers close friend, Everyone grieves, Always Very Emotional, Missing Everyone, Not going to see Them again",
            "example_sentence": "The family received support from friends during their time of _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beret",
            "definition": "A flat, round cap typically made of wool or felt",
            "pronunciation": "/bəˈreɪ/",
            "etymology": "From French béret, from Gascon berret, from Latin birrus 'hooded cloak'",
            "memory_tip": "BERET: Basic European - Round head covering, Everyone recognizes this french hat, Traditional stylish cap",
            "example_sentence": "The artist wore a black _____ tilted at a jaunty angle.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bergamot",
            "definition": "A citrus fruit used to flavor Earl Grey tea; an aromatic herb",
            "pronunciation": "/ˈbɜrɡəˌmɑt/",
            "etymology": "From French bergamote, from Italian bergamotto, possibly from Turkish beg armudi 'prince's pear'",
            "memory_tip": "BERGAMOT: Beautiful Elegant - Refined citrus fruit, Great Aromatic scent, Making Outstanding Tea flavoring",
            "example_sentence": "The distinctive flavor of Earl Grey tea comes from _____ oil.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bergère",
            "definition": "A type of upholstered armchair with exposed wooden frame",
            "pronunciation": "/bɛrˈʒɛr/",
            "etymology": "From French bergère meaning 'shepherdess', referring to its comfortable, pastoral style",
            "memory_tip": "BERGÈRE: Beautiful Elegant - Really Grande furniture, Everyone Recognizes this upholstered chair, Everyone loves comfort",
            "example_sentence": "The antique _____ chair was reupholstered in silk damask.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bermudas",
            "definition": "Plural of Bermuda; casual knee-length shorts",
            "pronunciation": "/bərˈmjudəz/",
            "etymology": "From Bermuda, the island territory where this style of shorts became popular",
            "memory_tip": "BERMUDAS: Breezy Easy - Relaxed clothing, Made for hot weather, Useful Daytime Apparel, Summer clothing",
            "example_sentence": "He wore khaki _____ and a polo shirt to the country club.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bermudasamusement",
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
            "word": "bernoulli",
            "definition": "Relating to the Bernoulli family of mathematicians or their principles",
            "pronunciation": "/bərˈnuli/",
            "etymology": "Named after the Bernoulli family, particularly Jakob and Daniel Bernoulli, Swiss mathematicians",
            "memory_tip": "BERNOULLI: Brilliant European - Researchers who made Notable advances, Outstanding mathematics, Understood fluid dynamics, Legendary scientists, Learning Important principles",
            "example_sentence": "_____ principle explains how airplane wings generate lift through air pressure differences.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "berries",
            "definition": "Plural of berry; small, juicy fruits",
            "pronunciation": "/ˈbɛriz/",
            "etymology": "From Old English berie, from Proto-Germanic bazja",
            "memory_tip": "BERRIES: Beautiful Edible - Really Refreshing fruit, In many colors, Everyone Sees them in nature",
            "example_sentence": "The forest was full of wild _____ that the hikers could safely eat.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "berry",
            "definition": "A small, round, juicy fruit without a stone",
            "pronunciation": "/ˈbɛri/",
            "etymology": "From Old English berie, from Proto-Germanic bazja",
            "memory_tip": "BERRY: Beautiful Edible - Really tasty sweet fruit, Round tiny fruit, Everyone loves them, Yummy snacks",
            "example_sentence": "She picked a ripe _____ from the bush and popped it into her mouth.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "berserk",
            "definition": "Wildly frenzied and out of control; extremely violent or destructive",
            "pronunciation": "/bərˈsɜrk/",
            "etymology": "From Old Norse berserkr, from ber 'bear' + serkr 'shirt', referring to Norse warriors",
            "memory_tip": "BERSERK: Brutal Enraged - Really Savage warrior, Extremely violent Rage, Killing intensely",
            "example_sentence": "The crowd went _____ when their team scored the winning goal.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "berth",
            "definition": "A sleeping place on a ship or train; a mooring place for a ship",
            "pronunciation": "/bɜrθ/",
            "etymology": "Probably from bear (to carry) + -th, originally meaning 'sea room'",
            "memory_tip": "BERTH: Boat Everyone - Rests There, Home sleeping space on ship",
            "example_sentence": "The passenger reserved a private _____ for the overnight train journey.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "beseech",
            "definition": "To ask someone urgently and fervently to do something; to implore",
            "pronunciation": "/bɪˈsitʃ/",
            "etymology": "From Middle English bisechen, from be- + sechen 'to seek'",
            "memory_tip": "BESEECH: Beg Everyone - Seriously Earnestly asking, Everyone Carefully Hears pleading requests",
            "example_sentence": "I _____ you to reconsider your decision before it's too late.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "besieged",
            "definition": "Past tense of besiege; surrounded and attacked; overwhelmed",
            "pronunciation": "/bɪˈsidʒd/",
            "etymology": "From Middle English besegen, from be- + sege 'siege'",
            "memory_tip": "BESIEGED: Being Everyone - Surrounded by enemies, In military attack, Everyone Given difficulty, Everyone Defended against attackers",
            "example_sentence": "The castle was _____ for months before the defenders finally surrendered.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "besmirch",
            "definition": "To damage someone's reputation; to make dirty or stained",
            "pronunciation": "/bɪˈsmɜrtʃ/",
            "etymology": "From be- + smirch (to make dirty), from Middle English smorchan",
            "memory_tip": "BESMIRCH: Being Someone's - reputation damaged, Making reputation stained, In public, Reducing Credibility, Hurting reputation deliberately",
            "example_sentence": "The scandal threatened to _____ the politician's previously spotless reputation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bespoke",
            "definition": "Custom-made; made to order according to individual requirements",
            "pronunciation": "/bɪˈspoʊk/",
            "etymology": "From be- + spoke (past tense of speak), originally meaning 'spoken for' or ordered",
            "memory_tip": "BESPOKE: Being Specifically - Perfectly Ordered custom item, Keeping Everyone happy with personalized goods",
            "example_sentence": "The gentleman wore a _____ suit tailored specifically for his measurements.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bessemer",
            "definition": "Relating to a steelmaking process invented by Henry Bessemer",
            "pronunciation": "/ˈbɛsəmər/",
            "etymology": "Named after Sir Henry Bessemer, British inventor of the steel-making process",
            "memory_tip": "BESSEMER: Better Efficient - Steel making process, Everyone Makes steel more efficiently, Revolutionizing metal production",
            "example_sentence": "The _____ process revolutionized steel production in the 19th century.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "best",
            "definition": "Of the highest quality; most excellent",
            "pronunciation": "/bɛst/",
            "etymology": "From Old English betst, superlative of good",
            "memory_tip": "BEST: Better Everyone - Superior To all others, Top quality",
            "example_sentence": "She always tried to do her _____ work on every assignment.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bestial",
            "definition": "Of or like an animal; savagely cruel",
            "pronunciation": "/ˈbɛstʃəl/",
            "etymology": "From Latin bestialis, from bestia meaning 'beast'",
            "memory_tip": "BESTIAL: Brutal Extremely - Savage behavior, Terrible cruel Instincts, Animal-Like cruelty",
            "example_sentence": "The prisoner's _____ treatment shocked the human rights investigators.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bestie",
            "definition": "Informal term for best friend",
            "pronunciation": "/ˈbɛsti/",
            "etymology": "From best + -ie diminutive suffix, informal for 'best friend'",
            "memory_tip": "BESTIE: Best Special - The closest friend, Important close friend, Everyone loves their closest companion",
            "example_sentence": "She and her _____ have been inseparable since elementary school.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bestow",
            "definition": "To give or present as a gift or honor",
            "pronunciation": "/bɪˈstoʊ/",
            "etymology": "From Middle English bestowen, from be- + stowen 'to place'",
            "memory_tip": "BESTOW: Being Special - To give someone something, Outstanding gift, Wonderful present delivered",
            "example_sentence": "The university will _____ an honorary degree upon the distinguished alumnus.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bethesda",
            "definition": "A biblical pool in Jerusalem; a place of healing",
            "pronunciation": "/bəˈθɛzdə/",
            "etymology": "From Hebrew beth hesda meaning 'house of mercy' or 'house of grace'",
            "memory_tip": "BETHESDA: Biblical Every - Totally Healing place, Everyone Seeking healing, Divine healing, Amazing healing place",
            "example_sentence": "The hospital was named _____ in reference to the biblical place of healing.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "betony",
            "definition": "A purple-flowered plant of the mint family, historically used medicinally",
            "pronunciation": "/ˈbɛtəni/",
            "etymology": "From Latin betonica, possibly from Vettones, a Spanish tribe that used the plant",
            "memory_tip": "BETONY: Beautiful Effective - Traditional healing plant, Outstanding Natural medicine, Years of medicinal use",
            "example_sentence": "Medieval herbalists valued _____ for its supposed ability to cure headaches.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "betrothal",
            "definition": "A formal engagement to be married; the act of becoming engaged",
            "pronunciation": "/bɪˈtroʊθəl/",
            "etymology": "From betroth + -al, where betroth comes from Middle English, from be- + troth 'faith'",
            "memory_tip": "BETROTHAL: Being Together - really committed relationship, Romantic Official announcement, Together two people, Hopeful wedding celebration, All families involved, Love commitment ceremony",
            "example_sentence": "The _____ ceremony was attended by both families to celebrate the engagement.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "better",
            "definition": "Of higher quality or more excellent; improved",
            "pronunciation": "/ˈbɛtər/",
            "etymology": "From Old English betera, comparative of good",
            "memory_tip": "BETTER: Being Everyone - Top quality, Totally Excellent, Really improved condition",
            "example_sentence": "The new medicine made her feel much _____ within a few days.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "between",
            "definition": "In the space separating two objects; in the time separating two events",
            "pronunciation": "/bɪˈtwin/",
            "etymology": "From Old English betweonum, from be- + tweonum 'two each'",
            "memory_tip": "BETWEEN: Being Two - We can see the space, Exactly Exactly in the middle of them, Nothing else around",
            "example_sentence": "The cat sat _____ the two dogs on the couch.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_019_processed.csv"
    
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
        
        print(f"Batch 019 processing complete!")
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