import pandas as pd
import csv
import random

class DifficultyCalculator:
    def __init__(self):
        self.phonetic_patterns = {
            'silent_letters': ['b', 'k', 'l', 'w', 'h'],
            'double_consonants': ['ss', 'tt', 'nn', 'mm', 'll', 'dd', 'cc'],
            'irregular_vowels': ['ough', 'augh', 'eigh', 'ieu']
        }
        
    def calculate_difficulty(self, word, definition="", etymology=""):
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._estimate_word_frequency(word)
        morphology_score = self._analyze_morphological_complexity(word, definition)
        etymology_score = self._analyze_etymological_complexity(etymology)
        
        raw_score = (phonetic_score + frequency_score + morphology_score + etymology_score) / 4
        
        if raw_score <= 2:
            return "Beginning"
        elif raw_score <= 4:
            return "Intermediate"
        elif raw_score <= 6:
            return "Advanced"
        else:
            return "Expert"
    
    def _calculate_phonetic_transparency(self, word):
        score = 1
        word_lower = word.lower()
        
        for pattern in self.phonetic_patterns['silent_letters']:
            if pattern in word_lower and not self._is_pronounced(word_lower, pattern):
                score += 1
                
        for pattern in self.phonetic_patterns['double_consonants']:
            if pattern in word_lower:
                score += 0.5
                
        for pattern in self.phonetic_patterns['irregular_vowels']:
            if pattern in word_lower:
                score += 1.5
                
        return min(score, 8)
    
    def _is_pronounced(self, word, letter):
        silent_contexts = {
            'b': ['mb', 'bt'],
            'k': ['kn'],
            'l': ['lf', 'lk', 'lm'],
            'w': ['wr', 'wh'],
            'h': ['rh', 'gh']
        }
        
        if letter in silent_contexts:
            for context in silent_contexts[letter]:
                if context in word:
                    return False
        return True
    
    def _estimate_word_frequency(self, word):
        length = len(word)
        if length <= 4:
            return 1
        elif length <= 6:
            return 2
        elif length <= 8:
            return 3
        elif length <= 10:
            return 4
        else:
            return 5
    
    def _analyze_morphological_complexity(self, word, definition):
        score = 1
        
        prefixes = ['pre', 'post', 'anti', 'semi', 'multi', 'inter', 'super', 'sub', 'trans', 'over', 'under']
        suffixes = ['tion', 'sion', 'ment', 'ness', 'able', 'ible', 'ous', 'ful', 'less', 'ing', 'ed']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 0.5
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 0.5
                
        if any(char.isupper() for char in word[1:]):
            score += 1
            
        return min(score, 6)
    
    def _analyze_etymological_complexity(self, etymology):
        if not etymology:
            return 2
            
        etymology_lower = etymology.lower()
        complex_origins = ['greek', 'latin', 'sanskrit', 'arabic', 'hebrew', 'chinese', 'japanese']
        
        score = 1
        for origin in complex_origins:
            if origin in etymology_lower:
                score += 1
                
        return min(score, 6)

def process_batch_029():
    # Read the batch file
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_029_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_029_processed.csv"
    
    # Read the input file
    df = pd.read_csv(input_file)
    
    # Initialize difficulty calculator
    calc = DifficultyCalculator()
    
    # Combined word errors detected
    combined_errors = ["carapacedauerlauf"]
    
    # Create comprehensive word data
    word_data = [
        {
            "word": "capnometer",
            "definition": "An instrument for measuring or monitoring the concentration of carbon dioxide, especially in exhaled breath or in blood.",
            "pronunciation": "/ˈkæpnəˌmitər/",
            "pronunciation_audio_url": "",
            "example_sentence": "The medical team used a _____ to monitor the patient's carbon dioxide levels during surgery.",
            "etymology": "From Greek kapnos 'smoke' + -meter 'measure'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPNOMETER: Carcinogenic Air Particles Need Optical Measurement Equipment To Evaluate Respiration - measuring CO2 in breath.",
            "fun_fact": "Capnometers are essential in anesthesia monitoring and can detect breathing problems before they become life-threatening.",
            "difficulty_level": calc.calculate_difficulty("capnometer", "An instrument for measuring or monitoring the concentration of carbon dioxide", "From Greek kapnos 'smoke' + -meter 'measure'"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "capoeira",
            "definition": "A Brazilian martial art that combines elements of dance, acrobatics, and music, often performed in a circle.",
            "pronunciation": "/ˌkæpoʊˈɛrə/",
            "pronunciation_audio_url": "",
            "example_sentence": "The dancers performed an energetic _____ routine that captivated the audience with its fluid movements.",
            "etymology": "From Portuguese capoeira, originally meaning 'land cleared for cultivation'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPOEIRA: Combat And Performance Organizing Elite Individual Rhythmic Activities - Brazilian martial art dance.",
            "fun_fact": "Capoeira was developed by African slaves in Brazil and was disguised as a dance to hide its martial arts training from overseers.",
            "difficulty_level": calc.calculate_difficulty("capoeira", "A Brazilian martial art that combines elements of dance, acrobatics, and music", "From Portuguese capoeira"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "capotasto",
            "definition": "A device used on the neck of a stringed instrument to shorten all the strings simultaneously, raising their pitch.",
            "pronunciation": "/ˌkæpoʊˈtæstoʊ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The guitarist placed a _____ on the third fret to transpose the song to a higher key.",
            "etymology": "From Italian capotasto, from capo 'head' + tasto 'fret'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPOTASTO: Clamping And Positioning Operates To Adjust String Tone Output - guitar device.",
            "fun_fact": "The capotasto was invented in the 17th century and allows guitarists to change keys without learning new chord shapes.",
            "difficulty_level": calc.calculate_difficulty("capotasto", "A device used on the neck of a stringed instrument", "From Italian capotasto"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "capricious",
            "definition": "Given to sudden and unaccountable changes of mood or behavior; unpredictable and impulsive.",
            "pronunciation": "/kəˈprɪʃəs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The weather in spring can be quite _____, changing from sunny to stormy within minutes.",
            "etymology": "From French capricieux, from Italian capriccioso, from capriccio 'sudden start'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPRICIOUS: Constantly Altering Preferences Reflects Inconsistent Character In Ordinary Unpredictable Situations - changeable behavior.",
            "fun_fact": "The word originally came from the Italian word for 'hedgehog,' relating to sudden, spiky movements.",
            "difficulty_level": calc.calculate_difficulty("capricious", "Given to sudden and unaccountable changes of mood or behavior", "From French capricieux"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caprifig",
            "definition": "A wild fig tree, especially one whose fruit is used to pollinate edible figs through a process involving fig wasps.",
            "pronunciation": "/ˈkæprɪˌfɪɡ/",
            "pronunciation_audio_url": "",
            "example_sentence": "Farmers planted _____ trees near their orchards to ensure proper pollination of their commercial fig crops.",
            "etymology": "From Latin caprificus, from caper 'goat' + ficus 'fig'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPRIFIG: Cultivation And Pollination Requires Individual Fig Insects Gathering - wild fig for pollination.",
            "fun_fact": "The relationship between caprifigs and fig wasps is one of nature's most intricate examples of mutualistic symbiosis.",
            "difficulty_level": calc.calculate_difficulty("caprifig", "A wild fig tree used for pollination", "From Latin caprificus"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "capsaicin",
            "definition": "The chemical compound that gives chili peppers their spicy heat, used medicinally as a topical analgesic.",
            "pronunciation": "/kæpˈseɪɪsɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The hot sauce contained high levels of _____, making it almost unbearably spicy for most people.",
            "etymology": "From Latin capsicum 'pepper' + -in (chemical suffix)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPSAICIN: Chemical And Pharmaceutical Substance Activates Intense Chemical Inflammation Naturally - spicy compound.",
            "fun_fact": "Capsaicin binds to pain receptors in mammals but birds cannot taste it, helping peppers spread their seeds through bird droppings.",
            "difficulty_level": calc.calculate_difficulty("capsaicin", "The chemical compound that gives chili peppers their spicy heat", "From Latin capsicum"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "capstan",
            "definition": "A vertical machine used for winding in heavy ropes or chains, especially on ships for raising anchors.",
            "pronunciation": "/ˈkæpstən/",
            "pronunciation_audio_url": "",
            "example_sentence": "The sailors worked together to turn the _____ and raise the massive anchor from the ocean floor.",
            "etymology": "From Old French cabestrant, from cabestre 'halter'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPSTAN: Crew And Personnel Struggle To Activate Naval device - ship winch mechanism.",
            "fun_fact": "Traditional capstans were operated by sailors walking in circles around the device, often while singing sea shanties to coordinate their efforts.",
            "difficulty_level": calc.calculate_difficulty("capstan", "A vertical machine used for winding in heavy ropes or chains", "From Old French cabestrant"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "capsule",
            "definition": "A small container, typically made of gelatin, containing medicine; or a detachable compartment of a spacecraft.",
            "pronunciation": "/ˈkæpsuːl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The doctor prescribed antibiotic pills in _____ form to make them easier to swallow.",
            "etymology": "From Latin capsula, diminutive of capsa 'box'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPSULE: Container And Protective Structure Utilizes Little Enclosed space - small container.",
            "fun_fact": "Space capsules are designed to protect astronauts during the most dangerous phases of spaceflight: launch and re-entry.",
            "difficulty_level": calc.calculate_difficulty("capsule", "A small container for medicine or spacecraft compartment", "From Latin capsula"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "captain",
            "definition": "The person in command of a ship or aircraft; or the leader of a sports team or military unit.",
            "pronunciation": "/ˈkæptɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ship's _____ navigated through the storm with skill and determination.",
            "etymology": "From Old French capitaine, from Late Latin capitaneus, from caput 'head'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPTAIN: Commanding Authority Person Takes Authority In Navigation - ship or team leader.",
            "fun_fact": "The tradition of a ship's captain going down with the ship comes from the maritime law principle that the captain has ultimate responsibility for the vessel and crew.",
            "difficulty_level": calc.calculate_difficulty("captain", "The person in command of a ship or team", "From Old French capitaine"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "captivated",
            "definition": "Attracted and held the interest or attention of; charmed or fascinated completely.",
            "pronunciation": "/ˈkæptɪˌveɪtɪd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The audience was _____ by the magician's incredible illusions and charismatic performance.",
            "etymology": "From Latin captivatus, past participle of captivare 'to capture'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPTIVATED: Completely Absorbed People Think In Very Attentive Total Engaging Delight - fascinated.",
            "fun_fact": "The word shares its root with 'captive,' originally meaning to take prisoner, but evolved to mean capturing attention rather than freedom.",
            "difficulty_level": calc.calculate_difficulty("captivated", "Attracted and held the interest or attention of", "From Latin captivatus"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "captive",
            "definition": "A person or animal that has been taken prisoner or confined; unable to escape from a place or situation.",
            "pronunciation": "/ˈkæptɪv/",
            "pronunciation_audio_url": "",
            "example_sentence": "The wildlife rescue center cared for the _____ eagle until it was ready to be released back into the wild.",
            "etymology": "From Latin captivus, from captus 'taken'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPTIVE: Confined And Prevented To Independently Visit Environments - imprisoned or confined.",
            "fun_fact": "Captive breeding programs have helped save numerous endangered species from extinction, including the California condor.",
            "difficulty_level": calc.calculate_difficulty("captive", "A person or animal that has been taken prisoner", "From Latin captivus"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "capture",
            "definition": "To take possession or control of; to record accurately in words or images; to attract and hold.",
            "pronunciation": "/ˈkæptʃər/",
            "pronunciation_audio_url": "",
            "example_sentence": "The photographer hoped to _____ the perfect sunset over the mountain range.",
            "etymology": "From French capture, from Latin captura, from captus 'taken'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAPTURE: Catching And Preserving Things Under Recorded Evidence - to take or record.",
            "fun_fact": "In chess, 'capture' means to remove an opponent's piece by moving your piece to the same square.",
            "difficulty_level": calc.calculate_difficulty("capture", "To take possession or control of", "From French capture"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carabinieri",
            "definition": "The national police force of Italy, originally a military corps that now serves as both military and civilian police.",
            "pronunciation": "/ˌkærəbɪniˈɛri/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ patrol the streets of Rome, maintaining order with their distinctive uniforms and authority.",
            "etymology": "From Italian carabiniere, from carabina 'carbine' (a type of firearm)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARABINIERI: Capable Armed Response And Brigade Investigating National Italian Emergency Response Incidents - Italian police.",
            "fun_fact": "The Carabinieri is one of the oldest police forces in the world, founded in 1814, and they wear distinctive dress uniforms with plumed hats.",
            "difficulty_level": calc.calculate_difficulty("carabinieri", "The national police force of Italy", "From Italian carabiniere"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caracas",
            "definition": "The capital and largest city of Venezuela, located in a valley near the Caribbean coast.",
            "pronunciation": "/kəˈrækəs/",
            "pronunciation_audio_url": "",
            "example_sentence": "_____ is known for its vibrant culture, museums, and mountainous setting in northern Venezuela.",
            "etymology": "Named after the Caracas people, an indigenous group that lived in the area",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARACAS: Caribbean And Regional Administrative Center And South American capital - Venezuelan city.",
            "fun_fact": "Caracas was founded in 1567 and is the birthplace of Simón Bolívar, the liberator of South America.",
            "difficulty_level": calc.calculate_difficulty("caracas", "The capital and largest city of Venezuela", "Named after the Caracas people"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caramel",
            "definition": "A sweet, chewy candy made by heating sugar until it browns; or the golden-brown color of this substance.",
            "pronunciation": "/ˈkærəməl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The baker drizzled warm _____ sauce over the vanilla ice cream for a perfect dessert.",
            "etymology": "From French caramel, from Spanish caramelo, possibly from Latin cannamellis 'sugar cane'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARAMEL: Cooking And Roasting Amazing Methods Extract Lovely flavors - sweet candy.",
            "fun_fact": "Caramel forms through the Maillard reaction, the same chemical process that gives bread crusts and roasted coffee their flavors.",
            "difficulty_level": calc.calculate_difficulty("caramel", "A sweet, chewy candy made by heating sugar", "From French caramel"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caravan",
            "definition": "A group of travelers journeying together for safety in desert or hostile regions; or a covered vehicle for living in.",
            "pronunciation": "/ˈkærəˌvæn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The merchant _____ crossed the Sahara Desert, following ancient trade routes between Africa and the Middle East.",
            "etymology": "From Persian karwan, meaning 'group of travelers'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARAVAN: Crossing Arid Regions And Valleys And Navigating - group of travelers.",
            "fun_fact": "The Silk Road was traveled by countless caravans carrying goods between Asia and Europe for over 1,400 years.",
            "difficulty_level": calc.calculate_difficulty("caravan", "A group of travelers journeying together", "From Persian karwan"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carbohydrates",
            "definition": "Organic compounds consisting of carbon, hydrogen, and oxygen, serving as a major source of energy in living organisms.",
            "pronunciation": "/ˌkɑrboʊˈhaɪdreɪts/",
            "pronunciation_audio_url": "",
            "example_sentence": "Athletes often consume foods rich in _____ before competitions to fuel their energy needs.",
            "etymology": "From carbon + hydrate, reflecting their chemical composition",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARBOHYDRATES: Carbon And Related Body Organs Harvest Yeast Derived Readily Available Tremendous Energy Sources - energy nutrients.",
            "fun_fact": "Carbohydrates provide 4 calories per gram and are the body's preferred source of quick energy, especially for the brain.",
            "difficulty_level": calc.calculate_difficulty("carbohydrates", "Organic compounds serving as energy sources", "From carbon + hydrate"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carborane",
            "definition": "A type of molecular cluster composed of carbon, boron, and hydrogen atoms, used in specialized chemical applications.",
            "pronunciation": "/ˈkɑrboʊreɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The chemistry laboratory synthesized a new _____ compound for potential use in advanced materials research.",
            "etymology": "From carbo- (carbon) + borane (boron hydride compound)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARBORANE: Carbon And Related Boron Organize Robust And Novel Elements - chemical compound.",
            "fun_fact": "Carboranes are among the most thermally and chemically stable compounds known, making them useful in extreme conditions.",
            "difficulty_level": calc.calculate_difficulty("carborane", "A molecular cluster of carbon, boron, and hydrogen", "From carbo- + borane"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carcajou",
            "definition": "Another name for the wolverine, a large carnivorous mammal of the weasel family found in northern regions.",
            "pronunciation": "/ˈkɑrkəˌʒuː/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ is known for its incredible strength and ability to drive bears away from their kills.",
            "etymology": "From French carcajou, from Cree kwingwaage",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARCAJOU: Carnivorous Arctic Creature Aggressively Jumps And Overcomes prey - wolverine.",
            "fun_fact": "The wolverine is so fierce that it's the only animal that can consistently steal kills from bears and wolves.",
            "difficulty_level": calc.calculate_difficulty("carcajou", "Another name for the wolverine", "From French carcajou, from Cree"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carcass",
            "definition": "The dead body of an animal, especially one prepared for food; the remains or shell of something.",
            "pronunciation": "/ˈkɑrkəs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The vultures circled overhead, waiting to feast on the _____ left behind by the lions.",
            "etymology": "From Old French carcasse, possibly from Arabic qarqas 'to gnaw'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARCASS: Corpse And Remains Constitute Animal Structure Skeleton - dead animal body.",
            "fun_fact": "In automotive terminology, 'carcass' refers to the structural framework of a tire, made of fabric or steel cords.",
            "difficulty_level": calc.calculate_difficulty("carcass", "The dead body of an animal", "From Old French carcasse"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carcinogenic",
            "definition": "Having the potential to cause cancer; relating to or tending to produce cancer in living tissue.",
            "pronunciation": "/ˌkɑrsɪnoʊˈdʒɛnɪk/",
            "pronunciation_audio_url": "",
            "example_sentence": "The warning label clearly stated that the chemical was _____ and should be handled with extreme caution.",
            "etymology": "From Greek karkinos 'crab, cancer' + -genic 'producing'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARCINOGENIC: Cancer And Related Cellular Irregularities Naturally Occurring Generate Environmental Negative Impact Consequences - cancer-causing.",
            "fun_fact": "The link between certain substances and cancer was first discovered in the 18th century when scrotal cancer was observed in chimney sweeps.",
            "difficulty_level": calc.calculate_difficulty("carcinogenic", "Having the potential to cause cancer", "From Greek karkinos + -genic"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cardigan",
            "definition": "A knitted jacket or sweater with an opening down the front, typically fastened with buttons.",
            "pronunciation": "/ˈkɑrdɪɡən/",
            "pronunciation_audio_url": "",
            "example_sentence": "She wore a cozy wool _____ over her blouse to stay warm in the cool autumn air.",
            "etymology": "Named after the 7th Earl of Cardigan, a British military officer",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARDIGAN: Comfortable And Relaxed Design In Garment And Neat clothing - button-front sweater.",
            "fun_fact": "The cardigan was named after the Earl of Cardigan, who led the infamous Charge of the Light Brigade during the Crimean War.",
            "difficulty_level": calc.calculate_difficulty("cardigan", "A knitted jacket with front opening", "Named after Earl of Cardigan"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cardoon",
            "definition": "A large Mediterranean plant related to the artichoke, cultivated for its edible leaf stalks and roots.",
            "pronunciation": "/kɑrˈduːn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The chef prepared the _____ by braising the tender stalks with herbs and olive oil.",
            "etymology": "From French cardon, from Provençal cardon, from Latin carduus 'thistle'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARDOON: Culinary And Regional Delicacy Often Overlooked Nutritious vegetable - artichoke relative.",
            "fun_fact": "Cardoon is considered an invasive species in some areas but is prized in Mediterranean cuisine for its unique, slightly bitter flavor.",
            "difficulty_level": calc.calculate_difficulty("cardoon", "A Mediterranean plant related to artichoke", "From French cardon"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "career",
            "definition": "An occupation undertaken for a significant period of a person's life, typically with opportunities for progress.",
            "pronunciation": "/kəˈrɪr/",
            "pronunciation_audio_url": "",
            "example_sentence": "She chose a _____ in medicine because she wanted to help people and make a difference in their lives.",
            "etymology": "From French carrière, from Latin carrus 'cart, wagon'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAREER: Continuous And Rewarding Employment And Responsibility - professional occupation.",
            "fun_fact": "The word originally meant 'a race course' and evolved to mean a person's course through life or profession.",
            "difficulty_level": calc.calculate_difficulty("career", "An occupation undertaken for life", "From French carrière"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carefully",
            "definition": "In a way that deliberately avoids harm or errors; with attention and caution.",
            "pronunciation": "/ˈkɛrfəli/",
            "pronunciation_audio_url": "",
            "example_sentence": "The surgeon _____ examined the X-rays before proceeding with the delicate operation.",
            "etymology": "From careful + -ly, from care + -ful + -ly",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAREFULLY: Cautious And Responsible Effort Fully Understands Logical Lessons Yielding safety - with caution.",
            "fun_fact": "The concept of being 'careful' originally meant 'full of care' in the sense of being worried or anxious, before evolving to mean 'cautious.'",
            "difficulty_level": calc.calculate_difficulty("carefully", "In a way that avoids harm or errors", "From careful + -ly"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caricature",
            "definition": "A picture or description that exaggerates certain features or characteristics for comic or dramatic effect.",
            "pronunciation": "/ˈkærɪkəˌtʃʊr/",
            "pronunciation_audio_url": "",
            "example_sentence": "The political _____ in the newspaper showed the mayor with an enormously oversized head and tiny body.",
            "etymology": "From Italian caricatura, from caricare 'to load, exaggerate'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARICATURE: Comically Amplified Representation Incorporating Creative And Theatrical Unusual Ridiculous Elements - exaggerated drawing.",
            "fun_fact": "Leonardo da Vinci is credited with creating some of the first caricatures, though the formal art form developed later in 16th-century Italy.",
            "difficulty_level": calc.calculate_difficulty("caricature", "A picture that exaggerates features for effect", "From Italian caricatura"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carillon",
            "definition": "A set of bells in a tower, played using a keyboard or automatic mechanism to produce melodies.",
            "pronunciation": "/ˈkærəˌlɑn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The university's _____ played beautiful melodies every hour, filling the campus with music.",
            "etymology": "From French carillon, from Old French quarregnon, from Latin quaternio 'set of four'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARILLON: Chiming And Ringing In Lovely Lingering Orchestra Notes - bell tower music.",
            "fun_fact": "The largest carillon in the world has 77 bells and weighs over 100 tons, located at the Kirk in the Hills in Michigan.",
            "difficulty_level": calc.calculate_difficulty("carillon", "A set of bells in a tower", "From French carillon"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carlisle",
            "definition": "A city in northwestern England near the Scottish border, historically significant as a frontier town.",
            "pronunciation": "/kɑrˈlaɪl/",
            "pronunciation_audio_url": "",
            "example_sentence": "_____ has a rich history as a border city, with its castle serving as a stronghold for centuries.",
            "etymology": "From Brythonic Caer Luguvalos, meaning 'fort of Luguvalos'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARLISLE: Castle And Regional Location In Scotland's Lower English border - English border city.",
            "fun_fact": "Carlisle Castle has been besieged more times than any other place in Britain due to its strategic border location.",
            "difficulty_level": calc.calculate_difficulty("carlisle", "A city in northwestern England", "From Brythonic Caer Luguvalos"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carmagnole",
            "definition": "A popular song and dance of the French Revolution, or the short jacket worn by French revolutionaries.",
            "pronunciation": "/ˌkɑrməˈnjoʊl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The revolutionaries danced the _____ in the streets of Paris, celebrating their political victories.",
            "etymology": "From French carmagnole, named after the town of Carmagnola in Italy",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARMAGNOLE: Celebratory And Revolutionary Music And Great National Official Liberation Expression - French revolutionary song.",
            "fun_fact": "The carmagnole became so associated with the French Revolution that wearing the jacket or singing the song was later banned under Napoleon.",
            "difficulty_level": calc.calculate_difficulty("carmagnole", "A song and dance of the French Revolution", "From French carmagnole"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carmelite",
            "definition": "A member of a Roman Catholic religious order founded in the 12th century on Mount Carmel in Palestine.",
            "pronunciation": "/ˈkɑrməˌlaɪt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ monastery was known for its contemplative lifestyle and dedication to prayer and meditation.",
            "etymology": "From Mount Carmel + -ite, referring to the mountain where the order was founded",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARMELITE: Catholic And Religious Monks Embrace Life In Thoughtful Environments - religious order.",
            "fun_fact": "The Carmelite order produced many famous mystics, including Saint Teresa of Ávila and Saint John of the Cross.",
            "difficulty_level": calc.calculate_difficulty("carmelite", "A member of a Catholic religious order", "From Mount Carmel + -ite"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carnage",
            "definition": "The killing of a large number of people; widespread and bloody slaughter or massacre.",
            "pronunciation": "/ˈkɑrnɪdʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The battlefield was a scene of terrible _____, with evidence of the fierce fighting scattered everywhere.",
            "etymology": "From French carnage, from Italian carnaggio, from carne 'flesh'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARNAGE: Catastrophic And Relentless Numerous Armed Groups Engage - widespread killing.",
            "fun_fact": "The word was first used in English to describe the aftermath of battles, but now applies to any scene of widespread destruction.",
            "difficulty_level": calc.calculate_difficulty("carnage", "The killing of a large number of people", "From French carnage"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carnassial",
            "definition": "Relating to the large shearing teeth of carnivorous mammals, adapted for cutting meat and crushing bones.",
            "pronunciation": "/kɑrˈnæsiəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The wolf's _____ teeth are perfectly designed for slicing through tough hide and muscle.",
            "etymology": "From French carnassier 'carnivorous', from Latin carn- 'flesh'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARNASSIAL: Carnivore And Related Natural Adaptive Strong Sharp Incredibly Aggressive Lions teeth - meat-cutting teeth.",
            "fun_fact": "Carnassial teeth are so specialized that they can exert over 1,500 pounds of pressure per square inch in large carnivores.",
            "difficulty_level": calc.calculate_difficulty("carnassial", "Relating to shearing teeth of carnivores", "From French carnassier"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carnation",
            "definition": "A fragrant flower with fringed petals, typically pink, white, or red, popular in gardens and bouquets.",
            "pronunciation": "/kɑrˈneɪʃən/",
            "pronunciation_audio_url": "",
            "example_sentence": "She picked a bright red _____ from the garden to add to her mother's birthday bouquet.",
            "etymology": "From French carnation, from Italian carnagione 'flesh color'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARNATION: Colorful And Romantic Nature Always Takes Interest Over Neighboring flowers - fringed flower.",
            "fun_fact": "Carnations are the birth flower for January and are symbols of love, fascination, and distinction.",
            "difficulty_level": calc.calculate_difficulty("carnation", "A fragrant flower with fringed petals", "From French carnation"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carnifices",
            "definition": "Plural of carnifex; executioners or those who inflict death, especially in ancient Rome.",
            "pronunciation": "/kɑrˈnɪfɪˌsiːz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ancient Roman _____ carried out executions in the arena as part of public spectacles.",
            "etymology": "From Latin carnifex, from caro 'flesh' + facere 'to make'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARNIFICES: Cruel And Ruthless Notorious Individuals Forcefully Inflict Cutting Execution Sentences - executioners.",
            "fun_fact": "In ancient Rome, carnifices were often slaves or freedmen who performed executions, as Roman citizens considered the work beneath their status.",
            "difficulty_level": calc.calculate_difficulty("carnifices", "Executioners in ancient Rome", "From Latin carnifex"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carnitas",
            "definition": "A Mexican dish of pork that is braised or roasted slowly until tender, then shredded and often crisped.",
            "pronunciation": "/kɑrˈnitəs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The restaurant's _____ tacos were filled with succulent, slow-cooked pork and topped with fresh cilantro.",
            "etymology": "From Spanish carnitas, diminutive of carne 'meat'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARNITAS: Cooked And Roasted Now Into Tender Amazing Savory dish - Mexican pork.",
            "fun_fact": "Traditional carnitas are cooked in their own fat (lard) in large copper pots, giving them their distinctive flavor and texture.",
            "difficulty_level": calc.calculate_difficulty("carnitas", "A Mexican dish of slow-cooked pork", "From Spanish carnitas"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carnitine",
            "definition": "A compound found in muscle tissue that helps transport fatty acids into mitochondria for energy production.",
            "pronunciation": "/ˈkɑrnɪˌtin/",
            "pronunciation_audio_url": "",
            "example_sentence": "Athletes sometimes take _____ supplements to help improve their body's fat-burning capacity during exercise.",
            "etymology": "From Latin carn- 'flesh' + -itine (chemical suffix)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARNITINE: Chemical And Related Nutrient Involved Transport Into Nearby Enzymes - fat-burning compound.",
            "fun_fact": "Carnitine was discovered in 1905 in muscle extracts and was initially thought to be a vitamin before its true function was understood.",
            "difficulty_level": calc.calculate_difficulty("carnitine", "A compound that helps transport fatty acids", "From Latin carn- + -itine"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carnival",
            "definition": "A public celebration with music, dancing, and entertainment; or a traveling amusement show with rides and games.",
            "pronunciation": "/ˈkɑrnɪvəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The annual _____ filled the town square with colorful costumes, lively music, and delicious food stands.",
            "etymology": "From Italian carnevale, from Latin carnem levare 'put away meat'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARNIVAL: Celebration And Revelry Now Includes Various Amazing Lively entertainment - festive celebration.",
            "fun_fact": "The word 'carnival' originally referred to the period before Lent when people would 'put away meat' for fasting.",
            "difficulty_level": calc.calculate_difficulty("carnival", "A public celebration with entertainment", "From Italian carnevale"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caroling",
            "definition": "The practice of singing Christmas songs door-to-door or in public places during the holiday season.",
            "pronunciation": "/ˈkærəlɪŋ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The children went _____ through the neighborhood, spreading holiday cheer with traditional Christmas songs.",
            "etymology": "From carol + -ing, from Old French carole 'ring dance with singing'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAROLING: Christmas And Regional Outdoor Lively Inspiring Neighborly Gathering singing - holiday singing.",
            "fun_fact": "The tradition of caroling dates back to medieval times when wassailing involved singing to fruit trees to ensure a good harvest.",
            "difficulty_level": calc.calculate_difficulty("caroling", "Singing Christmas songs door-to-door", "From carol + -ing"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carolling",
            "definition": "British spelling of caroling; the practice of singing Christmas songs in public during the holidays.",
            "pronunciation": "/ˈkærəlɪŋ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The choir spent their evening _____ at the local nursing home, bringing joy to the elderly residents.",
            "etymology": "British spelling from carol + -ling, from Old French carole",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAROLLING: Christmas And Regional Outdoor Lively Lingering In Neighborly Gathering - British holiday singing.",
            "fun_fact": "The double 'l' in 'carolling' follows British spelling conventions, similar to 'travelling' versus American 'traveling.'",
            "difficulty_level": calc.calculate_difficulty("carolling", "British spelling of Christmas singing", "British spelling from carol + -ling"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carpal",
            "definition": "Relating to the carpus or wrist; of or pertaining to the bones of the wrist.",
            "pronunciation": "/ˈkɑrpəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The doctor diagnosed her with _____ tunnel syndrome after she complained of numbness in her wrist.",
            "etymology": "From Greek karpos 'wrist' + -al",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARPAL: Concerning And Related Parts Around Ligaments - wrist-related.",
            "fun_fact": "Carpal tunnel syndrome affects millions of people worldwide and is often caused by repetitive motions like typing.",
            "difficulty_level": calc.calculate_difficulty("carpal", "Relating to the wrist", "From Greek karpos + -al"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carpenter",
            "definition": "A skilled worker who builds and repairs wooden structures, furniture, and other items made of wood.",
            "pronunciation": "/ˈkɑrpəntər/",
            "pronunciation_audio_url": "",
            "example_sentence": "The skilled _____ crafted beautiful custom cabinets for the kitchen renovation project.",
            "etymology": "From Old French carpentier, from Latin carpentarius 'wagon maker'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARPENTER: Crafting And Repairing Projects Everyone Needs Through Expert Renovation - wood worker.",
            "fun_fact": "Jesus of Nazareth is often referred to as a carpenter, though the Greek word 'tekton' could also mean a general craftsman or builder.",
            "difficulty_level": calc.calculate_difficulty("carpenter", "A skilled worker who builds with wood", "From Old French carpentier"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carrageenan",
            "definition": "A gelling agent extracted from red seaweed, commonly used as a thickener and stabilizer in food products.",
            "pronunciation": "/ˌkærəˈɡinən/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ice cream manufacturer used _____ to give their product a smooth, creamy texture.",
            "etymology": "From Irish carraigín, from carraig 'rock' + -ín diminutive",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARRAGEENAN: Creamy And Related Refreshing Additives Generate Excellent Eating Natural Applications - seaweed thickener.",
            "fun_fact": "Carrageenan has been used in Ireland for over 600 years, traditionally to make a pudding called 'Irish moss.'",
            "difficulty_level": calc.calculate_difficulty("carrageenan", "A gelling agent from red seaweed", "From Irish carraigín"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carrageenin",
            "definition": "An alternative spelling of carrageenan; a gelatinous substance extracted from certain red seaweeds.",
            "pronunciation": "/ˌkærəˈɡinɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The food scientist studied the properties of _____ as a natural alternative to artificial thickening agents.",
            "etymology": "Variant spelling of carrageenan, from Irish carraigín",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARRAGEENIN: Creamy And Related Refreshing Additives Generate Excellent Eating Natural In Nature - seaweed extract.",
            "fun_fact": "Carrageenin is classified into different types (kappa, iota, lambda) based on its molecular structure and gelling properties.",
            "difficulty_level": calc.calculate_difficulty("carrageenin", "Alternative spelling of carrageenan", "Variant of carrageenan"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carragheenin",
            "definition": "Another spelling variant of carrageenan; a substance from red algae used in food and industrial applications.",
            "pronunciation": "/ˌkærəˈɡinɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The pharmaceutical company investigated _____ as a potential coating for time-release medications.",
            "etymology": "Another variant spelling of carrageenan, from Irish carraigín",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARRAGHEENIN: Creamy And Related Refreshing Additives Gathered Harvested Expertly Eating Natural In Nature - algae substance.",
            "fun_fact": "The multiple spellings of this word reflect its journey from Irish Gaelic through various scientific naming conventions.",
            "difficulty_level": calc.calculate_difficulty("carragheenin", "Variant spelling of carrageenan", "Variant of carrageenan"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carriage",
            "definition": "A vehicle with wheels drawn by horses; or the way someone holds and moves their body; bearing or posture.",
            "pronunciation": "/ˈkærɪdʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The royal _____ proceeded slowly through the town square, drawn by four magnificent white horses.",
            "etymology": "From Old French cariage, from carier 'to carry'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARRIAGE: Classic And Royal Riding Involving Aristocratic Graceful Elegant transportation - horse-drawn vehicle.",
            "fun_fact": "The phrase 'carriage return' on typewriters and computers comes from the mechanism that moved the carriage back to start a new line.",
            "difficulty_level": calc.calculate_difficulty("carriage", "A horse-drawn vehicle or bearing", "From Old French cariage"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carrickmacross",
            "definition": "A type of Irish lace characterized by floral motifs appliquéd onto machine-made net, named after the town where it originated.",
            "pronunciation": "/ˌkærɪkməˈkrɔs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The antique wedding dress featured intricate _____ lace that had been passed down through generations.",
            "etymology": "Named after Carrickmacross, a town in County Monaghan, Ireland",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARRICKMACROSS: Classic And Regional Rich Irish Craft Keeping Magnificent Art Carefully Refined Ornate Special Stitching - Irish lace.",
            "fun_fact": "Carrickmacross lace was developed in the 1820s and became so popular that it was worn by European royalty.",
            "difficulty_level": calc.calculate_difficulty("carrickmacross", "A type of Irish lace", "Named after Irish town"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carried",
            "definition": "Past tense of carry; transported or conveyed from one place to another; supported while moving.",
            "pronunciation": "/ˈkærid/",
            "pronunciation_audio_url": "",
            "example_sentence": "She _____ the heavy books to the library and returned them before the due date.",
            "etymology": "From carry + -ed, from Old French carier",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARRIED: Carefully And Responsibly Reaching Intended Ending Destination - past tense of transport.",
            "fun_fact": "The word 'carry' has over 30 different meanings in English, from physical transport to mathematical operations.",
            "difficulty_level": calc.calculate_difficulty("carried", "Past tense of carry", "From carry + -ed"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carrion",
            "definition": "The decaying flesh of dead animals; dead and rotting animal matter that serves as food for scavengers.",
            "pronunciation": "/ˈkæriən/",
            "pronunciation_audio_url": "",
            "example_sentence": "The vultures soared overhead, searching for _____ to feed their young back at the nest.",
            "etymology": "From Old French caroigne, from Latin caro 'flesh'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARRION: Corpses And Rotting Remains Insects Often Naturally consume - dead animal flesh.",
            "fun_fact": "Carrion beetles play a crucial ecological role by burying small animal carcasses, which helps recycle nutrients in ecosystems.",
            "difficulty_level": calc.calculate_difficulty("carrion", "The decaying flesh of dead animals", "From Old French caroigne"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carrot",
            "definition": "An orange-colored root vegetable that is commonly eaten raw or cooked; rich in beta-carotene and vitamin A.",
            "pronunciation": "/ˈkærət/",
            "pronunciation_audio_url": "",
            "example_sentence": "The rabbit munched happily on the fresh _____ from the garden, its orange color bright against the green leaves.",
            "etymology": "From French carotte, from Latin carota, from Greek karoton",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARROT: Crunchy And Rich Root Orange Tasty vegetable - orange root vegetable.",
            "fun_fact": "Carrots were originally purple, white, or yellow - the orange variety was developed by Dutch farmers in the 17th century.",
            "difficulty_level": calc.calculate_difficulty("carrot", "An orange root vegetable", "From French carotte"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        }
    ]
    
    # Create output CSV
    output_data = []
    combined_word_errors = []
    
    for _, row in df.iterrows():
        word = row['word'].strip()
        
        # Check for combined word errors
        if word in combined_errors:
            combined_word_errors.append({
                'word': word,
                'error_type': 'combined_word',
                'reason': 'Contains multiple words joined together from PDF extraction error'
            })
            continue
            
        # Find word data
        word_info = next((item for item in word_data if item['word'] == word), None)
        if word_info:
            output_data.append(word_info)
    
    # Write to CSV
    fieldnames = [
        'word', 'definition', 'pronunciation', 'pronunciation_audio_url',
        'example_sentence', 'etymology', 'etymology_source', 'memory_tip',
        'fun_fact', 'difficulty_level', 'source_difficulty', 'source', 'source_url'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)
    
    print(f"Batch 029 processing complete!")
    print(f"Processed: {len(df)}/50 words")
    print(f"Combined word errors flagged: {len(combined_word_errors)}")
    print(f"Valid spelling words: {len(output_data)}")
    
    if combined_word_errors:
        print(f"\nCombined word errors found:")
        for error in combined_word_errors:
            print(f"  - {error['word']}")

if __name__ == "__main__":
    process_batch_029()