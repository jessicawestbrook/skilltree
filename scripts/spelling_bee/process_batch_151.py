import csv
import os

class DifficultyCalculator:
    def calculate_difficulty_score(self, word, pronunciation, etymology):
        phonetic_score = self._calculate_phonetic_transparency(word, pronunciation)
        frequency_score = self._calculate_word_frequency(word)
        morphological_score = self._calculate_morphological_complexity(word)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        total_score = phonetic_score + frequency_score + morphological_score + etymology_score
        return phonetic_score, frequency_score, morphological_score, etymology_score, total_score
    
    def _calculate_phonetic_transparency(self, word, pronunciation):
        phonetic_patterns = {
            'regular': ['roger', 'rogue', 'role', 'roll', 'roller', 'roman', 'rome', 'romeo', 'roof', 'rookie', 'rooster', 'root', 'roots', 'rope', 'rotten', 'round', 'rounded', 'rounds', 'rouser', 'routine', 'rover', 'royal'],
            'semi_regular': ['rohan', 'roiling', 'rollicking', 'romaine', 'romano', 'rookery', 'roughly', 'roulette', 'roustabout', 'rowan', 'royale'],
            'irregular': ['rond', 'rondeau', 'rongeur', 'ronin', 'rooibos', 'rooseveltite', 'rorschach', 'rosemaling', 'roseola', 'rosin', 'rostrum', 'rotary', 'rotisserie', 'rotulet', 'rouille', 'roux']
        }
        
        if word in phonetic_patterns['regular']:
            return 3
        elif word in phonetic_patterns['semi_regular']:
            return 5
        elif word in phonetic_patterns['irregular']:
            return 7
        else:
            return 6
    
    def _calculate_word_frequency(self, word):
        high_frequency = ['roger', 'rogue', 'role', 'roll', 'roller', 'roman', 'rome', 'romeo', 'roof', 'root', 'roots', 'rope', 'round', 'rounded', 'rounds', 'routine', 'rover', 'royal']
        medium_frequency = ['roiling', 'rollicking', 'romaine', 'romano', 'rookie', 'rooster', 'rookery', 'rotten', 'roughly', 'roulette', 'roustabout', 'rowan', 'royale']
        low_frequency = ['rohan', 'rond', 'rondeau', 'rongeur', 'ronin', 'rooibos', 'rooseveltite', 'rorschach', 'rosemaling', 'roseola', 'rosin', 'rostrum', 'rotary', 'rotisserie', 'rotulet', 'rouille', 'roux', 'rouser']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['roger', 'rogue', 'role', 'roll', 'roman', 'rome', 'roof', 'root', 'roots', 'rope', 'round', 'rounds', 'rover', 'royal']
        moderate_words = ['roller', 'rollicking', 'romaine', 'romano', 'romeo', 'rookie', 'rooster', 'rookery', 'rotten', 'rounded', 'roughly', 'roulette', 'routine', 'rowan', 'royale', 'rouser']
        complex_words = ['rohan', 'roiling', 'rond', 'rondeau', 'rongeur', 'ronin', 'rooibos', 'rooseveltite', 'rorschach', 'rosemaling', 'roseola', 'rosin', 'rostrum', 'rotary', 'rotisserie', 'rotulet', 'rouille', 'roustabout', 'roux']
        
        if word in simple_words:
            return 2
        elif word in moderate_words:
            return 4
        elif word in complex_words:
            return 7
        else:
            return 5
    
    def _calculate_etymology_complexity(self, etymology):
        if 'Japanese' in etymology or 'Afrikaans' in etymology:
            return 6
        elif 'French' in etymology:
            return 5
        elif 'Latin' in etymology and 'prefix' in etymology:
            return 6
        elif 'Latin' in etymology:
            return 4
        elif 'Old English' in etymology or 'Germanic' in etymology:
            return 3
        else:
            return 5

def main():
    calculator = DifficultyCalculator()
    
    word_data = {
        'roger': {
            'definition': "Used to express acknowledgment or agreement in radio communication; an affirmative response meaning \"understood\" or \"received\"; a male given name. In military and aviation contexts, Roger confirms message reception.",
            'pronunciation': "/ˈrɑdʒər/",
            'pronunciation_respelling': "ROJ-ur",
            'etymology': "From the NATO phonetic alphabet, where \"Roger\" represents the letter R for \"received.\"",
            'memory_tip': "Think radio communication \"R\" for \"received\" = Roger.",
            'example_sentence': "The pilot responded \"___ that\" to confirm he understood the instructions."
        },
        'rogue': {
            'definition': "A dishonest or unprincipled person; a mischievous but likable person; something that is defective or uncontrollable. Rogue can describe both villainous characters and endearingly mischievous individuals.",
            'pronunciation': "/roʊɡ/",
            'pronunciation_respelling': "ROHG",
            'etymology': "From obsolete \"roger,\" meaning \"beggar,\" of uncertain origin.",
            'memory_tip': "Think of a mischievous character who goes against the rules.",
            'example_sentence': "The ___ elephant separated from its herd and wandered into the village."
        },
        'rohan': {
            'definition': "A fictional kingdom in J.R.R. Tolkien's Middle-earth; a place name meaning \"horse country\"; can refer to various geographical locations named after Tolkien's creation. Known for its horse-riding culture and grasslands.",
            'pronunciation': "/ˈroʊhæn/",
            'pronunciation_respelling': "ROH-han",
            'etymology': "Created by J.R.R. Tolkien, possibly from Old English \"rocc\" (horse) + \"ham\" (home).",
            'memory_tip': "Think Tolkien's horse-riding kingdom = Rohan.",
            'example_sentence': "The riders of ___ were known throughout Middle-earth for their horsemanship."
        },
        'roiling': {
            'definition': "Present participle of roil; making turbulent or muddy; disturbing or annoying; churning violently. Roiling describes both physical agitation of liquids and emotional disturbance.",
            'pronunciation': "/ˈrɔɪlɪŋ/",
            'pronunciation_respelling': "ROYL-ing",
            'etymology': "Present participle of \"roil,\" from Old French \"roiller\" (to roll around).",
            'memory_tip': "Think \"roil\" + \"ing\" = currently churning/disturbing.",
            'example_sentence': "The storm left the river ___ with mud and debris."
        },
        'role': {
            'definition': "A part played by an actor; a function or position; the characteristic behavior expected of someone in a particular position. Roles define responsibilities, expectations, and social functions.",
            'pronunciation': "/roʊl/",
            'pronunciation_respelling': "ROHL",
            'etymology': "From French \"rôle,\" from \"rolle\" (roll of paper), referring to actor's script.",
            'memory_tip': "Think of an actor's part written on a roll of paper.",
            'example_sentence': "She played the ___ of Lady Macbeth with great intensity."
        },
        'roll': {
            'definition': "To move by turning over and over; a small round piece of bread; a list of names; to move smoothly. Roll involves rotational movement or cylindrical objects.",
            'pronunciation': "/roʊl/",
            'pronunciation_respelling': "ROHL",
            'etymology': "From Old French \"roler,\" from Latin \"rotula\" (little wheel).",
            'memory_tip': "Think of a wheel rolling or bread rolls on a table.",
            'example_sentence': "The ball began to ___ down the steep hill."
        },
        'roller': {
            'definition': "A cylinder that rotates; a large wave; a small wheel; a device for flattening or smoothing. Rollers are used in various applications from painting to hairstyling.",
            'pronunciation': "/ˈroʊlər/",
            'pronunciation_respelling': "ROHL-ur",
            'etymology': "From \"roll\" + suffix \"-er\" (one that), from Latin \"rotula.\"",
            'memory_tip': "Think \"roll\" + \"er\" = thing that rolls.",
            'example_sentence': "The painter used a ___ to apply paint evenly to the wall."
        },
        'rollicking': {
            'definition': "Exuberantly lively and amusing; characterized by high spirits and boisterous fun; carefree and energetic. Rollicking describes joyful, uninhibited activity or entertainment.",
            'pronunciation': "/ˈrɑlɪkɪŋ/",
            'pronunciation_respelling': "ROL-ih-king",
            'etymology': "From \"rollick\" (to move carelessly), possibly from \"roll\" + \"frolic.\"",
            'memory_tip': "Think \"roll\" + \"frolic\" = rolling around in fun.",
            'example_sentence': "The children had a ___ good time at the carnival."
        },
        'romaine': {
            'definition': "A type of lettuce with long, crisp leaves; cos lettuce with elongated heads and sturdy ribs. Romaine is commonly used in Caesar salads and provides excellent nutritional value.",
            'pronunciation': "/roʊˈmeɪn/",
            'pronunciation_respelling': "roh-MAYN",
            'etymology': "From French \"romaine\" (Roman lettuce), referring to its supposed Roman origin.",
            'memory_tip': "Think \"Roman\" lettuce = romaine.",
            'example_sentence': "The Caesar salad was made with fresh ___ lettuce and parmesan cheese."
        },
        'romainemigraine': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'romaine' + 'migraine' incorrectly joined. 'Romaine' is a type of lettuce, while 'migraine' is a severe headache. These should be separate words.]",
            'pronunciation': "/roʊˈmeɪn ˈmaɪɡreɪn/",
            'pronunciation_respelling': "roh-MAYN MYE-grayn",
            'etymology': "Combined word error: 'romaine' from French + 'migraine' from French.",
            'memory_tip': "Error combination: romaine (lettuce) + migraine (headache) - should be separate.",
            'example_sentence': "The ___ salad was prepared while she suffered from a severe ___."
        },
        'roman': {
            'definition': "Relating to ancient Rome or its empire; a citizen of Rome; relating to the Roman Catholic Church; upright lettering style. Roman encompasses historical, religious, and typographical meanings.",
            'pronunciation': "/ˈroʊmən/",
            'pronunciation_respelling': "ROH-muhn",
            'etymology': "From Latin \"Romanus,\" from \"Roma\" (Rome).",
            'memory_tip': "Think of ancient Rome and its empire.",
            'example_sentence': "The ___ Empire stretched across much of the ancient world."
        },
        'romano': {
            'definition': "A type of hard Italian cheese similar to Parmesan; relating to Roman style or origin; a variety of cheese made from sheep's or cow's milk. Romano cheese is aged and has a sharp, salty flavor.",
            'pronunciation': "/roʊˈmɑnoʊ/",
            'pronunciation_respelling': "roh-MAH-noh",
            'etymology': "From Italian \"romano\" (Roman), referring to its Roman origin.",
            'memory_tip': "Think \"Roman\" cheese = Romano.",
            'example_sentence': "The pasta was topped with grated ___ cheese and black pepper."
        },
        'rome': {
            'definition': "The capital city of Italy; the former center of the Roman Empire; the seat of the Roman Catholic Church. Rome is known as the \"Eternal City\" for its enduring historical significance.",
            'pronunciation': "/roʊm/",
            'pronunciation_respelling': "ROHM",
            'etymology': "From Latin \"Roma,\" of uncertain origin, possibly from Etruscan.",
            'memory_tip': "Think of the eternal city with the Colosseum.",
            'example_sentence': "All roads lead to ___, according to the ancient saying."
        },
        'romeo': {
            'definition': "The male protagonist in Shakespeare's tragedy \"Romeo and Juliet\"; a passionate male lover; the NATO phonetic alphabet code for the letter R. Romeo represents romantic love and tragic devotion.",
            'pronunciation': "/ˈroʊmiˌoʊ/",
            'pronunciation_respelling': "ROH-mee-oh",
            'etymology': "From Italian \"Romeo,\" ultimately from Latin \"Romaeus\" (Roman).",
            'memory_tip': "Think of Shakespeare's tragic lover who died for Juliet.",
            'example_sentence': "He was such a ___, always writing love poems to his girlfriend."
        },
        'rond': {
            'definition': "A circular form or shape; in ballet, a circular movement of the leg; a round dance or musical form. Rond describes circular motions and round formations in various contexts.",
            'pronunciation': "/rɔnd/",
            'pronunciation_respelling': "ROND",
            'etymology': "From French \"rond\" (round), from Latin \"rotundus\" (round).",
            'memory_tip': "Think French \"round\" = rond.",
            'example_sentence': "The ballet dancer performed a perfect ___ de jambe."
        },
        'rondeau': {
            'definition': "A French verse form with a fixed structure and repeated refrains; a musical composition based on this poetic form. Rondeaux feature recurring lines and specific rhyme schemes.",
            'pronunciation': "/rɑnˈdoʊ/",
            'pronunciation_respelling': "ron-DOH",
            'etymology': "From French \"rondeau,\" from \"rond\" (round), referring to the circular structure.",
            'memory_tip': "Think French \"rond\" (round) = circular verse form.",
            'example_sentence': "The poet composed a beautiful ___ about spring's arrival."
        },
        'rongeur': {
            'definition': "A surgical instrument used to remove small pieces of bone; a medical tool with sharp, curved jaws for cutting bone or tissue. Rongeurs are essential instruments in orthopedic and neurosurgical procedures.",
            'pronunciation': "/rɔnˈʒɜr/",
            'pronunciation_respelling': "ron-ZHUR",
            'etymology': "From French \"rongeur,\" from \"ronger\" (to gnaw), from Latin \"rodicare.\"",
            'memory_tip': "Think French \"ronger\" (gnaw) = instrument that gnaws bone.",
            'example_sentence': "The surgeon used a ___ to carefully remove damaged bone tissue."
        },
        'ronin': {
            'definition': "In feudal Japan, a samurai who had no lord or master; a wandering warrior; someone without affiliation or allegiance. Ronin represents independence but also social displacement in Japanese culture.",
            'pronunciation': "/ˈroʊnɪn/",
            'pronunciation_respelling': "ROH-nin",
            'etymology': "From Japanese \"ronin,\" from \"ro\" (wave) + \"nin\" (person), meaning \"wave person.\"",
            'memory_tip': "Think Japanese \"wave person\" = wandering masterless samurai.",
            'example_sentence': "The ___ wandered the countryside seeking a new master to serve."
        },
        'roof': {
            'definition': "The covering of the top of a building; the upper limit or ceiling; to provide with a roof. Roofs protect buildings from weather and provide structural completion.",
            'pronunciation': "/ruf/",
            'pronunciation_respelling': "ROOF",
            'etymology': "From Old English \"hrof,\" of Germanic origin.",
            'memory_tip': "Think of the protective covering on top of a house.",
            'example_sentence': "The new ___ was designed to withstand heavy snow loads."
        },
        'rooibos': {
            'definition': "A South African shrub whose leaves are used to make herbal tea; the reddish tea made from this plant. Rooibos tea is caffeine-free and has a naturally sweet flavor.",
            'pronunciation': "/ˈrɔɪbɔs/",
            'pronunciation_respelling': "ROY-boss",
            'etymology': "From Afrikaans \"rooibos,\" from \"rooi\" (red) + \"bos\" (bush).",
            'memory_tip': "Think Afrikaans \"red bush\" = rooibos tea.",
            'example_sentence': "She enjoyed a cup of ___ tea with honey before bedtime."
        },
        'rookery': {
            'definition': "A breeding colony of rooks, penguins, seals, or other animals; a crowded, squalid dwelling place; a place where rooks nest. Rookeries are communal breeding sites for various species.",
            'pronunciation': "/ˈrʊkəri/",
            'pronunciation_respelling': "ROOK-ur-ee",
            'etymology': "From \"rook\" (bird) + suffix \"-ery\" (place of), referring to nesting areas.",
            'memory_tip': "Think \"rook\" + \"ery\" (place) = place where rooks nest.",
            'example_sentence': "The penguin ___ was bustling with activity during breeding season."
        },
        'rookie': {
            'definition': "A new recruit; a person new to an activity or organization; a first-year player in professional sports. Rookies are inexperienced but eager to learn and prove themselves.",
            'pronunciation': "/ˈrʊki/",
            'pronunciation_respelling': "ROOK-ee",
            'etymology': "From \"recruit,\" possibly influenced by \"rook\" (to cheat a novice).",
            'memory_tip': "Think \"rook\" (novice) + \"ie\" = new person.",
            'example_sentence': "The ___ police officer was partnered with an experienced veteran."
        },
        'rooseveltite': {
            'definition': "A rare mineral named after President Theodore Roosevelt; a hydrated arsenate mineral; a yellowish-green mineral found in uranium deposits. Rooseveltite contains uranium and arsenic in its chemical composition.",
            'pronunciation': "/ˈroʊzəˌvɛltaɪt/",
            'pronunciation_respelling': "ROH-zuh-velt-ahyt",
            'etymology': "Named after Theodore Roosevelt (1858-1919), 26th President of the United States.",
            'memory_tip': "Think President Roosevelt + mineral suffix \"-ite.\"",
            'example_sentence': "The geologist discovered traces of ___ in the uranium-rich rock formation."
        },
        'rooster': {
            'definition': "An adult male chicken; a cock; a male domestic fowl known for crowing at dawn. Roosters are characterized by their prominent combs, wattles, and colorful plumage.",
            'pronunciation': "/ˈrustər/",
            'pronunciation_respelling': "ROO-stur",
            'etymology': "From \"roost\" + suffix \"-er\" (one that), referring to the bird that roosts.",
            'memory_tip': "Think \"roost\" + \"er\" = male bird that roosts and crows.",
            'example_sentence': "The ___ crowed loudly every morning at sunrise."
        },
        'root': {
            'definition': "The part of a plant that typically grows underground; the basic cause or source; to establish deeply; the fundamental basis. Roots provide stability, nutrition, and origin.",
            'pronunciation': "/rut/",
            'pronunciation_respelling': "ROOT",
            'etymology': "From Old English \"rot,\" of Germanic origin, related to Latin \"radix.\"",
            'memory_tip': "Think of underground plant parts that anchor and feed.",
            'example_sentence': "The tree's ___ system extended deep into the soil."
        },
        'roots': {
            'definition': "Plural of root; origins or sources; family heritage or cultural background; underground plant parts; fundamental causes. Roots represent both botanical structures and cultural connections.",
            'pronunciation': "/ruts/",
            'pronunciation_respelling': "ROOTS",
            'etymology': "Plural of \"root,\" from Old English \"rot.\"",
            'memory_tip': "Think \"root\" + \"s\" = multiple origins or plant parts.",
            'example_sentence': "She traced her family ___ back to Ireland and Scotland."
        },
        'rope': {
            'definition': "A thick cord made of twisted or braided fibers; to catch with a lasso; to persuade or entice. Rope serves practical purposes in climbing, sailing, and securing objects.",
            'pronunciation': "/roʊp/",
            'pronunciation_respelling': "ROHP",
            'etymology': "From Old English \"rap,\" of Germanic origin.",
            'memory_tip': "Think of thick twisted cord for climbing or tying.",
            'example_sentence': "The mountain climber secured the ___ before beginning the ascent."
        },
        'rorschach': {
            'definition': "Relating to the Rorschach test, a psychological test using inkblot patterns; Hermann Rorschach, Swiss psychiatrist who developed this test. The test analyzes personality through interpretation of ambiguous images.",
            'pronunciation': "/ˈrɔrʃɑk/",
            'pronunciation_respelling': "ROR-shahk",
            'etymology': "Named after Hermann Rorschach (1884-1922), Swiss psychiatrist.",
            'memory_tip': "Think of inkblot psychological test by Dr. Rorschach.",
            'example_sentence': "The psychologist administered a ___ test to assess the patient's personality."
        },
        'rosemaling': {
            'definition': "A Norwegian folk art involving decorative painting with stylized floral designs; traditional decorative art using flowing floral patterns in bright colors. Rosemaling adorns furniture, walls, and household items.",
            'pronunciation': "/ˈroʊzəˌmɑlɪŋ/",
            'pronunciation_respelling': "ROH-zuh-mah-ling",
            'etymology': "From Norwegian \"rosemaling,\" from \"rose\" (rose) + \"maling\" (painting).",
            'memory_tip': "Think Norwegian \"rose painting\" = decorative floral art.",
            'example_sentence': "The antique cabinet featured beautiful ___ with traditional Norwegian motifs."
        },
        'roseola': {
            'definition': "A mild viral infection causing fever and rash, typically in young children; also called sixth disease; characterized by high fever followed by a pink rash. Roseola is common in infants and toddlers.",
            'pronunciation': "/roʊˈziələ/",
            'pronunciation_respelling': "roh-ZEE-uh-luh",
            'etymology': "From Latin \"roseola,\" diminutive of \"roseus\" (rosy), referring to the pink rash.",
            'memory_tip': "Think \"rose\" + \"ola\" = little rosy rash.",
            'example_sentence': "The pediatrician diagnosed the toddler with ___ after the characteristic rash appeared."
        },
        'rosin': {
            'definition': "A solid resin obtained from pine trees; used on violin bows and in various manufacturing processes; a sticky substance that improves grip. Rosin provides friction for string instruments and industrial applications.",
            'pronunciation': "/ˈrɑzən/",
            'pronunciation_respelling': "ROZ-uhn",
            'etymology': "From Old French \"rosine,\" from Latin \"resina\" (resin).",
            'memory_tip': "Think \"resin\" modified = rosin for violin bows.",
            'example_sentence': "The violinist applied ___ to her bow before the concert."
        },
        'rostrum': {
            'definition': "A raised platform for public speaking; a beak-like projection; the curved front part of an ancient warship. Rostrums serve as elevated speaking platforms or anatomical structures.",
            'pronunciation': "/ˈrɑstrəm/",
            'pronunciation_respelling': "ROS-truhm",
            'etymology': "From Latin \"rostrum\" (beak), from \"rodere\" (to gnaw).",
            'memory_tip': "Think \"rostr\" (beak) + \"um\" = beak-like speaking platform.",
            'example_sentence': "The speaker approached the ___ to address the assembled crowd."
        },
        'rotary': {
            'definition': "Relating to or characterized by rotation; a traffic circle; an organization of business and professional people. Rotary involves circular motion or circular organizational structures.",
            'pronunciation': "/ˈroʊtəri/",
            'pronunciation_respelling': "ROH-tuh-ree",
            'etymology': "From Latin \"rotarius,\" from \"rota\" (wheel).",
            'memory_tip': "Think \"rot\" (turn) + \"ary\" = relating to turning/rotation.",
            'example_sentence': "The old telephone had a ___ dial instead of push buttons."
        },
        'rotisserie': {
            'definition': "A cooking method using a rotating spit; a restaurant specializing in roasted meats; equipment for rotating food while cooking. Rotisserie cooking ensures even browning and self-basting.",
            'pronunciation': "/roʊˈtɪsəri/",
            'pronunciation_respelling': "roh-TIS-uh-ree",
            'etymology': "From French \"rôtisserie,\" from \"rôtir\" (to roast), from Germanic origin.",
            'memory_tip': "Think \"rotate\" + cooking = rotisserie.",
            'example_sentence': "The ___ chicken was perfectly seasoned and evenly cooked."
        },
        'rotten': {
            'definition': "Decayed or decomposed; morally corrupt; very bad or unpleasant; suffering from rot. Rotten describes both physical decay and moral deterioration.",
            'pronunciation': "/ˈrɑtən/",
            'pronunciation_respelling': "ROT-uhn",
            'etymology': "From Old English \"rotian\" (to rot) + past participle ending.",
            'memory_tip': "Think \"rot\" + \"ten\" = has rotted/decayed.",
            'example_sentence': "The ___ apple had to be thrown away immediately."
        },
        'rotulet': {
            'definition': "A small wheel or disk; a little roll or scroll; a circular ornament. Rotulets are decorative elements or small mechanical components with circular shapes.",
            'pronunciation': "/ˈrɑtjələt/",
            'pronunciation_respelling': "ROT-yuh-lit",
            'etymology': "From Latin \"rotula\" (little wheel) + diminutive suffix \"-et.\"",
            'memory_tip': "Think \"rotula\" (little wheel) + \"et\" = very small wheel.",
            'example_sentence': "The medieval manuscript was decorated with gold ___."
        },
        'roughly': {
            'definition': "In a rough manner; approximately; not gently or smoothly; harshly or violently. Roughly indicates imprecise measurement, crude treatment, or aggressive action.",
            'pronunciation': "/ˈrʌfli/",
            'pronunciation_respelling': "RUHF-lee",
            'etymology': "From \"rough\" + suffix \"-ly\" (in the manner of).",
            'memory_tip': "Think \"rough\" + \"ly\" = in a rough manner.",
            'example_sentence': "The package was handled ___ during shipping."
        },
        'rouille': {
            'definition': "A spicy mayonnaise-like sauce from Provence, France, typically served with fish soup or bouillabaisse; made with garlic, chili peppers, and saffron. Rouille adds heat and flavor to Mediterranean seafood dishes.",
            'pronunciation': "/ruˈi/",
            'pronunciation_respelling': "roo-EE",
            'etymology': "From French \"rouille\" (rust), referring to its reddish color.",
            'memory_tip': "Think French \"rust\" color = reddish spicy sauce.",
            'example_sentence': "The bouillabaisse was served with a dollop of spicy ___."
        },
        'roulette': {
            'definition': "A gambling game with a spinning wheel and ball; a tool with a small wheel for making dotted lines; any activity involving chance. Roulette combines luck with mathematical probability.",
            'pronunciation': "/ruˈlɛt/",
            'pronunciation_respelling': "roo-LET",
            'etymology': "From French \"roulette,\" diminutive of \"rouelle\" (little wheel).",
            'memory_tip': "Think French \"little wheel\" = spinning gambling wheel.",
            'example_sentence': "The casino's ___ wheel spun as players placed their bets."
        },
        'round': {
            'definition': "Having a circular or spherical shape; a series or sequence; to make circular; a complete circuit. Round describes both geometric shapes and cyclical processes.",
            'pronunciation': "/raʊnd/",
            'pronunciation_respelling': "ROWND",
            'etymology': "From Old French \"reont,\" from Latin \"rotundus\" (round).",
            'memory_tip': "Think of circular shape like a ball or coin.",
            'example_sentence': "The ___ table seated twelve people comfortably."
        },
        'rounded': {
            'definition': "Past tense of round; made circular or smooth; having curved edges; completed a circuit. Rounded describes objects with smooth, curved contours rather than sharp angles.",
            'pronunciation': "/ˈraʊndəd/",
            'pronunciation_respelling': "ROWN-did",
            'etymology': "Past tense of \"round,\" from Latin \"rotundus.\"",
            'memory_tip': "Think \"round\" + \"ed\" = was made circular/smooth.",
            'example_sentence': "The carpenter ___ the edges of the table for safety."
        },
        'rounds': {
            'definition': "Plural of round; a series of visits or inspections; ammunition for firearms; circular objects; regular tours of duty. Rounds represent repetitive cycles or circular items.",
            'pronunciation': "/raʊndz/",
            'pronunciation_respelling': "ROWNDZ",
            'etymology': "Plural of \"round,\" from Latin \"rotundus.\"",
            'memory_tip': "Think \"round\" + \"s\" = multiple circuits or circular objects.",
            'example_sentence': "The security guard made his nightly ___ through the building."
        },
        'rouser': {
            'definition': "A person or thing that rouses or stirs up; something that excites or stimulates; an inspiring speech or performance. Rousers motivate people to action or heightened emotion.",
            'pronunciation': "/ˈraʊzər/",
            'pronunciation_respelling': "ROW-zur",
            'etymology': "From \"rouse\" + suffix \"-er\" (one who), from Old French \"reuser.\"",
            'memory_tip': "Think \"rouse\" + \"er\" = one who stirs up excitement.",
            'example_sentence': "The political speech was a real ___ that energized the crowd."
        },
        'roustabout': {
            'definition': "An unskilled laborer, especially on an oil rig or ranch; a casual worker who does various jobs; a circus worker who sets up equipment. Roustabouts perform physical labor requiring versatility.",
            'pronunciation': "/ˈraʊstəˌbaʊt/",
            'pronunciation_respelling': "ROWST-uh-bowt",
            'etymology': "From \"roust\" (to stir up) + \"about,\" referring to workers moving around doing various tasks.",
            'memory_tip': "Think \"roust about\" = worker who moves around doing various jobs.",
            'example_sentence': "The ___ worked long hours maintaining equipment on the offshore oil platform."
        },
        'routine': {
            'definition': "A regular course of procedure; a set sequence of activities; ordinary or standard; performed as part of a regular schedule. Routines provide structure and efficiency to daily activities.",
            'pronunciation': "/ruˈtin/",
            'pronunciation_respelling': "roo-TEEN",
            'etymology': "From French \"routine,\" from \"route\" (road), referring to a well-traveled path.",
            'memory_tip': "Think \"route\" for regular path = routine.",
            'example_sentence': "Her morning ___ included yoga and meditation."
        },
        'roux': {
            'definition': "A mixture of flour and fat cooked together, used as a thickening agent in sauces and soups; a fundamental component of many French and Creole dishes. Roux provides body and richness to culinary preparations.",
            'pronunciation': "/ru/",
            'pronunciation_respelling': "ROO",
            'etymology': "From French \"roux\" (reddish-brown), from Latin \"russus\" (red).",
            'memory_tip': "Think French \"reddish\" = flour mixture that browns.",
            'example_sentence': "The chef prepared a dark ___ for the gumbo base."
        },
        'rover': {
            'definition': "A person who travels without a fixed destination; a vehicle designed for exploring terrain; a dog trained to retrieve; a wanderer or explorer. Rovers are characterized by mobility and exploration.",
            'pronunciation': "/ˈroʊvər/",
            'pronunciation_respelling': "ROH-vur",
            'etymology': "From \"rove\" (to wander) + suffix \"-er\" (one who).",
            'memory_tip': "Think \"rove\" + \"er\" = one who wanders/explores.",
            'example_sentence': "The Mars ___ transmitted stunning images back to Earth."
        },
        'rowan': {
            'definition': "A type of tree with white flowers and red berries; mountain ash; the wood of this tree. Rowan trees are valued for their ornamental appearance and wildlife benefits.",
            'pronunciation': "/ˈroʊən/",
            'pronunciation_respelling': "ROH-uhn",
            'etymology': "From Old Norse \"reynir,\" related to \"rauðr\" (red), referring to the red berries.",
            'memory_tip': "Think of tree with red berries = rowan.",
            'example_sentence': "The ___ tree's bright red berries attracted many birds."
        },
        'royal': {
            'definition': "Relating to a monarch or monarchy; magnificent or impressive; used in the service of royalty. Royal indicates association with kings, queens, or exceptional quality.",
            'pronunciation': "/ˈrɔɪəl/",
            'pronunciation_respelling': "ROY-uhl",
            'etymology': "From Old French \"roial,\" from Latin \"regalis\" (regal).",
            'memory_tip': "Think of kings and queens = royal.",
            'example_sentence': "The ___ wedding was watched by millions around the world."
        },
        'royale': {
            'definition': "A French term meaning \"royal style\"; used in culinary terms for elaborate preparations; indicates something prepared in a luxurious manner. Royale suggests elegance and sophistication.",
            'pronunciation': "/rɔɪˈæl/",
            'pronunciation_respelling': "roy-AL",
            'etymology': "From French \"royale,\" feminine form of \"royal.\"",
            'memory_tip': "Think French \"royal\" style = elaborate preparation.",
            'example_sentence': "The soup was garnished with a delicate custard ___."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_151_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_151_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['romainemigraine']
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = [
                'word', 'definition', 'pronunciation', 'pronunciation_respelling', 'etymology', 
                'etymology_source', 'memory_tip', 'example_sentence', 'example_sentence_source',
                'years', 'source_files', 'source_difficulties', 'definition_source', 
                'pronunciation_source', 'phonetic_transparency_score', 'word_frequency_score',
                'morphological_complexity_score', 'etymology_complexity_score', 'total_difficulty_score',
                'assigned_difficulty', 'audio_file_path', 'created_at', 'updated_at', 'notes',
                'review_status', 'batch_number'
            ]
            
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                word = row['word'].strip()
                
                if not word:
                    continue
                    
                print(f"Processing word {words_processed + 1}: {word}")
                
                # Check for combined word errors
                if word in combined_patterns:
                    combined_errors.append(word)
                
                # Get word data
                word_info = word_data.get(word, {})
                
                # Calculate difficulty scores
                pronunciation = word_info.get('pronunciation', '')
                etymology = word_info.get('etymology', '')
                
                phonetic_score, frequency_score, morphological_score, etymology_score, total_score = calculator.calculate_difficulty_score(word, pronunciation, etymology)
                
                # Write row
                output_row = {
                    'word': word,
                    'definition': word_info.get('definition', ''),
                    'pronunciation': pronunciation,
                    'pronunciation_respelling': word_info.get('pronunciation_respelling', ''),
                    'etymology': etymology,
                    'etymology_source': 'Claude',
                    'memory_tip': word_info.get('memory_tip', ''),
                    'example_sentence': word_info.get('example_sentence', ''),
                    'example_sentence_source': 'Claude',
                    'years': row['years'],
                    'source_files': row['source_files'],
                    'source_difficulties': row['source_difficulties'],
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'phonetic_transparency_score': phonetic_score,
                    'word_frequency_score': frequency_score,
                    'morphological_complexity_score': morphological_score,
                    'etymology_complexity_score': etymology_score,
                    'total_difficulty_score': total_score,
                    'assigned_difficulty': '',  # Left blank as requested
                    'audio_file_path': '',
                    'created_at': '2025-01-01',
                    'updated_at': '2025-01-01',
                    'notes': 'Batch 151 processing',
                    'review_status': 'pending',
                    'batch_number': '151'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 151 processing complete!")
    print(f"Successfully processed {words_processed}/50 words")
    print(f"Output saved to: {output_file}")
    
    if combined_errors:
        print(f"\nCombined word errors detected: {len(combined_errors)}")
        for error in combined_errors:
            print(f"  - {error}")
    else:
        print("\nNo combined word errors detected.")

if __name__ == "__main__":
    main()