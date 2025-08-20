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
            "word": "asylum",
            "definition": "A sanctuary or place of refuge and protection",
            "pronunciation": "/ˈæsaɪləm/",
            "etymology": "From Latin asylum, from Greek asylon meaning 'inviolable place of refuge', from a- 'not' + sylon 'right of seizure'",
            "memory_tip": "Remember ASYLUM: A Sanctuary You Live Until Matters improve",
            "example_sentence": "The political refugee sought _____ in the embassy during the conflict.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "asymptote",
            "definition": "A straight line that a curve approaches but never meets",
            "pronunciation": "/ˈæsɪmptoʊt/",
            "etymology": "From Greek asymptotos meaning 'not falling together', from a- 'not' + syn- 'together' + ptotos 'falling'",
            "memory_tip": "ASYMPTOTE: A curve Approaches Straight line but Never Meets - Picture Two Objects Eternally",
            "example_sentence": "The hyperbola has a horizontal _____ that it approaches but never crosses.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ataxia",
            "definition": "Loss of coordination of muscle movements, often affecting gait and speech",
            "pronunciation": "/əˈtæksiə/",
            "etymology": "From Greek ataxia meaning 'disorder, lack of arrangement', from a- 'without' + taxis 'order, arrangement'",
            "memory_tip": "ATAXIA: Affected muscles Totally Are eXtremely Incoordinated Always",
            "example_sentence": "The neurological condition caused severe _____ in the patient's walking and hand movements.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "ataxiapageantry",
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
            "word": "aten",
            "definition": "The solar disk deity in ancient Egyptian religion, prominently worshipped during Akhenaten's reign",
            "pronunciation": "/ˈɑtən/",
            "etymology": "From ancient Egyptian itn meaning 'solar disk', related to the sun god in Egyptian mythology",
            "memory_tip": "ATEN: Ancient Temple Egyptian deity - the solar disk that shines bright",
            "example_sentence": "Pharaoh Akhenaten promoted worship of _____ as the supreme solar deity.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atencatjang",
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
            "word": "athenaeum",
            "definition": "A literary or scientific institution or club; a library or reading room",
            "pronunciation": "/ˌæθəˈniəm/",
            "etymology": "From Latin Athenaeum, from Greek Athenaion, referring to the temple of Athena where scholars met",
            "memory_tip": "ATHENAEUM: Athena's Temple Housing Educational Activities - Named for goddess of wisdom",
            "example_sentence": "The local _____ hosted lectures and maintained an extensive research library.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atheneum",
            "definition": "Alternative spelling of athenaeum - a literary or scientific institution",
            "pronunciation": "/ˌæθəˈniəm/",
            "etymology": "From Latin Athenaeum, from Greek Athenaion, referring to the temple of Athena where scholars met",
            "memory_tip": "ATHENEUM: Alternative spelling - Athena's Temple for Educational Nurturing and University-like Meetings",
            "example_sentence": "The _____ featured rare manuscripts and scholarly discussions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "athlete",
            "definition": "A person who competes in sports requiring physical skill and training",
            "pronunciation": "/ˈæθlit/",
            "etymology": "From Greek athletes meaning 'contestant for a prize', from athlein 'to compete for a prize'",
            "memory_tip": "ATHLETE: Active Training Helps Leaders Excel Through Exercise",
            "example_sentence": "The Olympic _____ trained for years to perfect her technique.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "athletejotted",
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
            "word": "atlas",
            "definition": "A collection of maps bound together; the first cervical vertebra",
            "pronunciation": "/ˈætləs/",
            "etymology": "From Greek Atlas, the Titan condemned to hold up the heavens; maps named after him because early atlases depicted him holding up the world",
            "memory_tip": "ATLAS: A Titan Lifting And Supporting - maps show the world like Atlas held it",
            "example_sentence": "The geography student consulted her _____ to locate the remote island.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atlatl",
            "definition": "A spear-throwing device used by ancient hunters to increase range and force",
            "pronunciation": "/ˈætlætəl/",
            "etymology": "From Nahuatl atlatl meaning 'water thrower', from atl 'water' + the verb root meaning 'to throw'",
            "memory_tip": "ATLATL: Ancient Tool Launching spears Across The Land",
            "example_sentence": "The archaeological site revealed several _____ used by prehistoric hunters.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atmospheric",
            "definition": "Relating to the atmosphere; creating a distinctive mood or emotional tone",
            "pronunciation": "/ˌætməsˈfɛrɪk/",
            "etymology": "From atmosphere + -ic, where atmosphere comes from Greek atmos 'vapor' + sphaira 'sphere'",
            "memory_tip": "ATMOSPHERIC: Air That Makes Others See Perfectly How Environment Radiates Inspiring Character",
            "example_sentence": "The concert hall's _____ lighting created a mystical ambiance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atomic",
            "definition": "Relating to atoms or atomic energy; extremely small",
            "pronunciation": "/əˈtɑmɪk/",
            "etymology": "From Greek atomikos, from atomos meaning 'indivisible', from a- 'not' + tomos 'a cutting'",
            "memory_tip": "ATOMIC: A Tiny Object - Matter's Indivisible Core",
            "example_sentence": "The _____ structure of carbon includes six protons in its nucleus.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atonement",
            "definition": "The action of making amends for wrongdoing or reconciliation",
            "pronunciation": "/əˈtoʊnmənt/",
            "etymology": "From at-one-ment, literally 'the condition of being at one', expressing unity or reconciliation",
            "memory_tip": "ATONEMENT: At ONE with others through Making amends and Emotional Nurturing Together",
            "example_sentence": "He sought _____ for his past mistakes by volunteering at the charity.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atrabilious",
            "definition": "Melancholy or ill-tempered; characterized by depression or irritability",
            "pronunciation": "/ˌætrəˈbɪliəs/",
            "etymology": "From Latin atra bilis meaning 'black bile', from ater 'black' + bilis 'bile', relating to medieval belief that black bile caused melancholy",
            "memory_tip": "ATRABILIOUS: Always Temperamental - Related to Ancient Belief that Internal bile caused Longterm sadness",
            "example_sentence": "His _____ mood made him difficult to be around during stressful times.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atresia",
            "definition": "Congenital absence or closure of a normal body opening or tubular structure",
            "pronunciation": "/əˈtriʒə/",
            "etymology": "From Greek atretos meaning 'not perforated', from a- 'not' + tretos 'perforated'",
            "memory_tip": "ATRESIA: Anatomical Tubes Remain Entirely Sealed - Impossible Access",
            "example_sentence": "Biliary _____ is a serious condition affecting newborns' bile ducts.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atrium",
            "definition": "An open-roofed entrance hall or central court in ancient Roman houses; a heart chamber",
            "pronunciation": "/ˈeɪtriəm/",
            "etymology": "From Latin atrium meaning 'central hall of a Roman house', possibly from ater 'black' (referring to smoke-blackened walls)",
            "memory_tip": "ATRIUM: Ancient Temple Room - the central meeting place",
            "example_sentence": "The hotel's glass-covered _____ featured a beautiful fountain and tropical plants.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atrocious",
            "definition": "Horrifyingly wicked; extremely bad or unpleasant",
            "pronunciation": "/əˈtroʊʃəs/",
            "etymology": "From Latin atrox meaning 'fierce, cruel', from ater 'black, dark' suggesting something ominous",
            "memory_tip": "ATROCIOUS: Absolutely Terrible - Really Objectionable, Cruel, Insufferable, Outrageous behavior",
            "example_sentence": "The critic described the movie as having _____ dialogue and poor acting.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atrophy",
            "definition": "The gradual decline or wasting away of muscles, organs, or tissues",
            "pronunciation": "/ˈætrəfi/",
            "etymology": "From Greek atrophia meaning 'a wasting away', from a- 'without' + trophe 'nourishment'",
            "memory_tip": "ATROPHY: All Tissues Reduced to Ongoing Pathetic, Withered Years",
            "example_sentence": "Without regular exercise, muscle _____ can occur in just a few weeks.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "atrophyattempt",
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
            "word": "attacca",
            "definition": "Musical direction meaning to proceed immediately to the next movement without pause",
            "pronunciation": "/əˈtækə/",
            "etymology": "From Italian attacca meaning 'attack' or 'begin', from attaccare 'to attach, to begin'",
            "memory_tip": "ATTACCA: Always Transition To Another movement - Continue Continuous music Automatically",
            "example_sentence": "The composer wrote _____ at the end of the third movement to ensure seamless flow.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attached",
            "definition": "Fastened or connected to something; emotionally close or devoted",
            "pronunciation": "/əˈtætʃt/",
            "etymology": "From Old French atachier meaning 'to fasten', possibly from a- 'to' + tache 'nail, fastener'",
            "memory_tip": "ATTACHED: Always Together - Two hearts Connected and Holding Each other",
            "example_sentence": "The _____ document contained all the necessary supporting evidence.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attaché",
            "definition": "A diplomatic official attached to an embassy; a thin briefcase",
            "pronunciation": "/ˌætəˈʃeɪ/",
            "etymology": "From French attaché meaning 'attached', past participle of attacher 'to attach'",
            "memory_tip": "ATTACHÉ: An expert officially Assigned To embAassy - Connected to diplomatic Heritage",
            "example_sentence": "The cultural _____ organized events to promote international understanding.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attagirl",
            "definition": "An exclamation of encouragement or approval directed at a girl or woman",
            "pronunciation": "/ˈætəɡɜrl/",
            "etymology": "From 'that's a girl', contracted and evolved into an interjection of praise",
            "memory_tip": "ATTAGIRL: Always Tell girls they're Amazing - Positive words Inspiring young women",
            "example_sentence": "Her coach shouted '____!' when she scored the winning goal.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attempt",
            "definition": "To try to do or accomplish something; an effort to achieve a goal",
            "pronunciation": "/əˈtɛmpt/",
            "etymology": "From Old French attempter, from Latin attemptare meaning 'to try', from ad- 'to' + temptare 'to test, try'",
            "memory_tip": "ATTEMPT: Always Try - Take Every Measured Plan Thoughtfully",
            "example_sentence": "She made her first _____ at skydiving with careful preparation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attendee",
            "definition": "A person who attends or is present at an event or gathering",
            "pronunciation": "/ˌætənˈdi/",
            "etymology": "From attend + -ee, where attend comes from Old French atendre meaning 'to wait for, listen to'",
            "memory_tip": "ATTENDEE: Always There - The person Engaged, Never absent from Designated Events",
            "example_sentence": "Each conference _____ received a welcome packet and name tag.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attending",
            "definition": "Being present at; taking care of or serving as a doctor in charge",
            "pronunciation": "/əˈtɛndɪŋ/",
            "etymology": "From Old French atendre meaning 'to wait for, listen to', from Latin attendere 'to stretch toward'",
            "memory_tip": "ATTENDING: Always There - Taking care Every Need, Diligently present, Including medical care",
            "example_sentence": "The _____ physician reviewed all patient cases with the medical students.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attention",
            "definition": "The action of paying close notice; consideration or special care",
            "pronunciation": "/əˈtɛnʃən/",
            "etymology": "From Latin attentio meaning 'a stretching toward', from attendere 'to stretch toward, pay attention'",
            "memory_tip": "ATTENTION: Always Totally focusing Thoughts - Every Neuron Tuned Into Object Now",
            "example_sentence": "The speaker demanded complete _____ before beginning the important announcement.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attitude",
            "definition": "A settled way of thinking or feeling about something; a position of the body",
            "pronunciation": "/ˈætɪˌtud/",
            "etymology": "From French attitude, from Italian attitudine meaning 'disposition', from Latin aptitudo 'fitness'",
            "memory_tip": "ATTITUDE: Approach To life That Influences behavior - The Ultimate Determining Element",
            "example_sentence": "Her positive _____ helped her overcome many challenges in her career.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attorney",
            "definition": "A person appointed to act for another in legal matters; a lawyer",
            "pronunciation": "/əˈtɜrni/",
            "etymology": "From Old French atorné meaning 'appointed', from atorner 'to appoint', from a- 'to' + torner 'to turn'",
            "memory_tip": "ATTORNEY: Appointed To Take Over legal Representation - Navigates court Expertly for You",
            "example_sentence": "The defense _____ presented compelling evidence to support her client's case.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attributed",
            "definition": "Regarded as being caused by or credited to someone or something",
            "pronunciation": "/əˈtrɪbjutəd/",
            "etymology": "From Latin attributus, past participle of attribuere meaning 'to assign to', from ad- 'to' + tribuere 'to give'",
            "memory_tip": "ATTRIBUTED: Always Traced - The Recognition Indicates the Believed source, Using Trust Evidence",
            "example_sentence": "The painting was _____ to a famous Renaissance master after careful analysis.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attributive",
            "definition": "Relating to or having the nature of an attribute; describing a grammatical modifier",
            "pronunciation": "/əˈtrɪbjətɪv/",
            "etymology": "From attribute + -ive, where attribute comes from Latin attributum meaning 'something assigned'",
            "memory_tip": "ATTRIBUTIVE: Adjectives Truly Tell Real Information - Basic descriptive words Used To explain Important features",
            "example_sentence": "In the phrase 'red car,' the word 'red' serves an _____ function.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "attrition",
            "definition": "The process of gradually reducing strength or effectiveness through sustained pressure",
            "pronunciation": "/əˈtrɪʃən/",
            "etymology": "From Latin attritio meaning 'a rubbing against', from atterere 'to rub away', from ad- 'against' + terere 'to rub'",
            "memory_tip": "ATTRITION: Always The gradual Tearing - Reducing numbers through Internal struggles, Tasks depleting people's resources, energy, staff, willpower, etc.",
            "example_sentence": "The company's high _____ rate indicated serious problems with employee satisfaction.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aubergine",
            "definition": "An eggplant; a dark purple color",
            "pronunciation": "/ˈoʊbərˌʒin/",
            "etymology": "From French aubergine, from Arabic al-badinjan, from Persian badin-gan",
            "memory_tip": "AUBERGINE: A Unique purple vegetable - Big Egg-shaped fruit with Rich color, Growing In gardens, Notable for Eggplant name",
            "example_sentence": "The recipe called for sliced _____ to be grilled with olive oil and herbs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "auburn",
            "definition": "A reddish-brown color, especially of hair",
            "pronunciation": "/ˈɔbərn/",
            "etymology": "From Old French auborn meaning 'whitish', later influenced by brown to mean reddish-brown",
            "memory_tip": "AUBURN: A Beautiful Uniform Red-Brown color - Natural hair shade",
            "example_sentence": "Her _____ hair gleamed with copper highlights in the sunlight.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "auction",
            "definition": "A public sale where goods are sold to the highest bidder",
            "pronunciation": "/ˈɔkʃən/",
            "etymology": "From Latin auctio meaning 'an increasing', from augere 'to increase'",
            "memory_tip": "AUCTION: Always Upward - Calling out higher and higher bids Through bidding processes, bidders, auctioneers, etc. Including Objects and items for Niche buyers",
            "example_sentence": "The rare painting sold for millions at the prestigious art _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "audacious",
            "definition": "Extremely bold or daring; recklessly brave",
            "pronunciation": "/ɔˈdeɪʃəs/",
            "etymology": "From Latin audax meaning 'bold', from audere 'to dare'",
            "memory_tip": "AUDACIOUS: Absolutely Unafraid of Danger - Amazing Courage In daring situations, Outrageous confidence, Undertaking unbelievable actions, Standing bravely",
            "example_sentence": "Her _____ plan to climb the mountain in winter surprised even experienced mountaineers.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "audience",
            "definition": "A group of people assembled to watch or listen to a performance",
            "pronunciation": "/ˈɔdiəns/",
            "etymology": "From Latin audientia meaning 'a hearing', from audire 'to hear'",
            "memory_tip": "AUDIENCE: All United During an Intelligence-Entertaining event - Neighbors Coming for Entertainment",
            "example_sentence": "The _____ gave the performers a standing ovation after the brilliant concert.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "audiences",
            "definition": "Plural of audience; multiple groups of spectators or listeners",
            "pronunciation": "/ˈɔdiənsəz/",
            "etymology": "Plural form of audience, from Latin audientia meaning 'a hearing', from audire 'to hear'",
            "memory_tip": "AUDIENCES: All United During an Intelligence-Entertaining event - No Corner Empty - including Everyone, Students",
            "example_sentence": "The touring theater company performed for diverse _____ across the country.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "audio",
            "definition": "Sound or the reproduction of sound; relating to hearing or sound",
            "pronunciation": "/ˈɔdioʊ/",
            "etymology": "From Latin audire meaning 'to hear'",
            "memory_tip": "AUDIO: All sounds - Understanding through Direct listening through natural Input/Output",
            "example_sentence": "The _____ quality of the recording was excellent despite the age of the equipment.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "auditorium",
            "definition": "A large room or building for public gatherings, typically with tiered seating",
            "pronunciation": "/ˌɔdɪˈtɔriəm/",
            "etymology": "From Latin auditorium meaning 'a place for hearing', from audire 'to hear'",
            "memory_tip": "AUDITORIUM: All United During listening, Seated In Tiered Organized Rows - Impressive space for Unified Meetings",
            "example_sentence": "The school _____ was packed for the graduation ceremony.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aughts",
            "definition": "The first decade of the 21st century (2000-2009); zeros",
            "pronunciation": "/ɔts/",
            "etymology": "From aught meaning 'nothing, zero', from Old English awiht meaning 'anything'",
            "memory_tip": "AUGHTS: All zeros - Understanding this decade as the 'double-zero' years in Gaming, Having Technology Start",
            "example_sentence": "Many people remember the _____ as a time of significant technological change.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aughtsaugment",
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
            "word": "augment",
            "definition": "To make something greater by adding to it; to increase",
            "pronunciation": "/ɔɡˈmɛnt/",
            "etymology": "From Latin augmentum meaning 'increase', from augere 'to increase'",
            "memory_tip": "AUGMENT: Always Upgrading - Great Money Enhancement through Natural Technology",
            "example_sentence": "The company decided to _____ its workforce by hiring fifty new employees.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "auklet",
            "definition": "A small seabird of the auk family found in northern Pacific waters",
            "pronunciation": "/ˈɔklət/",
            "etymology": "From auk (from Old Norse alka) + diminutive suffix -let",
            "memory_tip": "AUKLET: Arctic bird - Unknown to many but Known by Little Expert birders, specializing in ocean swimming and diving underwater ",
            "example_sentence": "The _____ colonies nested on remote rocky islands in the Aleutians.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aura",
            "definition": "A distinctive atmosphere or quality surrounding a person or thing",
            "pronunciation": "/ˈɔrə/",
            "etymology": "From Latin aura meaning 'breeze, air', from Greek aura meaning 'breath, vapor'",
            "memory_tip": "AURA: An invisible Radiance Around people - like a mystical energy field",
            "example_sentence": "The ancient temple had an _____ of mystery and spiritual power.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aureole",
            "definition": "A circle of light or brightness surrounding something; a halo",
            "pronunciation": "/ˈɔriˌoʊl/",
            "etymology": "From Latin aureola meaning 'golden crown', from aureus 'golden', from aurum 'gold'",
            "memory_tip": "AUREOLE: Always Radiating - Understanding beautiful light Energy - Obvious Light Encircling divine figures",
            "example_sentence": "In the painting, saints were depicted with golden _____ around their heads.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "auricular",
            "definition": "Relating to the ear or hearing; spoken privately into someone's ear",
            "pronunciation": "/ɔˈrɪkjələr/",
            "etymology": "From Latin auricularis meaning 'of the ear', from auricula 'external ear', diminutive of auris 'ear'",
            "memory_tip": "AURICULAR: Always Understanding through ears - Relating to Information Carefully delivered Understated and private, Like Acoustic Reception",
            "example_sentence": "The _____ confession was whispered so quietly that only the priest could hear it.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "aurora",
            "definition": "A natural light display in polar skies; the dawn or early morning light",
            "pronunciation": "/ɔˈrɔrə/",
            "etymology": "From Latin Aurora, the Roman goddess of dawn, related to Greek Eos",
            "memory_tip": "AURORA: Amazing Universal natural light display - Radiant colors Often seen in Remote northern skies After sundown",
            "example_sentence": "The northern _____ painted the sky with brilliant green and purple curtains of light.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_014_processed.csv"
    
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
        
        print(f"Batch 014 processing complete!")
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