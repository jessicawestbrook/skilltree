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
            'regular': ['rubble', 'rude', 'ruins', 'rule', 'ruled', 'rumor', 'rumour', 'running', 'runs', 'rush', 'russet', 'rustle', 'sacred', 'sacrifice'],
            'semi_regular': ['rubaiyat', 'rubato', 'rubicon', 'rubric', 'ruckus', 'rudiments', 'ruffian', 'rugby', 'ruminate', 'runcible', 'rustication', 'rutabaga', 'ryeland', 'résumé', 'sabbatical', 'sabotage', 'sacrament', 'sacristy', 'sacrosanct'],
            'irregular': ['rubefacient', 'rubeus', 'ruelle', 'rugose', 'rupicolous', 'ruscus', 'ryas', 'ryukyu', 'sabermetrics', 'saccadic', 'sacchar', 'saccharide', 'saccharum', 'sacerdotal', 'sackbuts']
        }
        
        if word in phonetic_patterns['regular']:
            return 3
        elif word in phonetic_patterns['semi_regular']:
            return 5
        elif word in phonetic_patterns['irregular']:
            return 8
        else:
            return 6
    
    def _calculate_word_frequency(self, word):
        high_frequency = ['rubble', 'rude', 'ruins', 'rule', 'ruled', 'rumor', 'rumour', 'running', 'runs', 'rush', 'rustle', 'sacred', 'sacrifice']
        medium_frequency = ['rubicon', 'rubric', 'ruckus', 'rudiments', 'ruffian', 'rugby', 'ruminate', 'russet', 'rutabaga', 'résumé', 'sabbatical', 'sabotage', 'sacrament', 'sacristy', 'sacrosanct']
        low_frequency = ['rubaiyat', 'rubato', 'rubefacient', 'rubeus', 'ruelle', 'rugose', 'runcible', 'rupicolous', 'ruscus', 'rustication', 'ryas', 'ryeland', 'ryukyu', 'sabermetrics', 'saccadic', 'sacchar', 'saccharide', 'saccharum', 'sacerdotal', 'sackbuts']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['rubble', 'rude', 'ruins', 'rule', 'ruled', 'runs', 'rush', 'rustle', 'sacred']
        moderate_words = ['rubaiyat', 'rubato', 'rubicon', 'rubric', 'ruckus', 'rudiments', 'ruffian', 'rugby', 'ruminate', 'rumor', 'rumour', 'running', 'russet', 'rutabaga', 'résumé', 'sabbatical', 'sabotage', 'sacrament', 'sacrifice', 'sacristy', 'sacrosanct']
        complex_words = ['rubefacient', 'rubeus', 'ruelle', 'rugose', 'runcible', 'rupicolous', 'ruscus', 'rustication', 'ryas', 'ryeland', 'ryukyu', 'sabermetrics', 'saccadic', 'sacchar', 'saccharide', 'saccharum', 'sacerdotal', 'sackbuts']
        
        if word in simple_words:
            return 2
        elif word in moderate_words:
            return 4
        elif word in complex_words:
            return 7
        else:
            return 5
    
    def _calculate_etymology_complexity(self, etymology):
        if 'Greek' in etymology:
            return 7
        elif 'Latin' in etymology and 'Greek' in etymology:
            return 8
        elif 'Latin' in etymology and 'prefix' in etymology:
            return 6
        elif 'Latin' in etymology or 'French' in etymology:
            return 4
        elif 'Old English' in etymology or 'Germanic' in etymology:
            return 3
        else:
            return 5

def main():
    calculator = DifficultyCalculator()
    
    word_data = {
        'rubaiyat': {
            'definition': "A collection of four-line verses; specifically refers to \"The Rubaiyat of Omar Khayyam,\" a famous collection of Persian poetry translated by Edward FitzGerald. Rubaiyat represents a classical Persian poetic form emphasizing themes of mortality, pleasure, and philosophical reflection.",
            'pronunciation': "/ˌrubɑˈjɑt/",
            'pronunciation_respelling': "roo-bah-YAHT",
            'etymology': "From Persian \"rubāʿīyāt,\" plural of \"rubāʿī\" (quatrain), from Arabic \"rubāʿī\" (consisting of four).",
            'memory_tip': "Think Persian \"four-line\" verses = rubaiyat.",
            'example_sentence': "The ___ of Omar Khayyam contains timeless wisdom about life's fleeting nature."
        },
        'rubato': {
            'definition': "A musical term indicating flexible tempo, allowing for expressive speeding up and slowing down within a phrase; the practice of giving emotional expression by subtle departures from strict tempo. Rubato adds personal interpretation to musical performance.",
            'pronunciation': "/ruˈbɑtoʊ/",
            'pronunciation_respelling': "roo-BAH-toh",
            'etymology': "From Italian \"rubato,\" literally \"robbed,\" from \"rubare\" (to rob), referring to stolen time.",
            'memory_tip': "Think Italian \"robbed\" time = flexible musical tempo.",
            'example_sentence': "The pianist's use of ___ brought emotional depth to the Chopin nocturne."
        },
        'rubble': {
            'definition': "Broken fragments of stone, brick, or concrete; debris from destroyed buildings; rough, irregular pieces of rock. Rubble results from demolition, natural disasters, or weathering processes.",
            'pronunciation': "/ˈrʌbəl/",
            'pronunciation_respelling': "RUHB-uhl",
            'etymology': "From Middle English \"robel,\" possibly from Old French \"robe\" (spoils).",
            'memory_tip': "Think of broken stones and debris from demolished buildings.",
            'example_sentence': "The earthquake left the ancient temple in a pile of ___."
        },
        'rubefacient': {
            'definition': "A substance that causes redness of the skin by increasing blood circulation; a counter-irritant used in medicine to relieve inflammation. Rubefacients work by dilating blood vessels near the skin surface.",
            'pronunciation': "/ˌrubəˈfeɪʃənt/",
            'pronunciation_respelling': "roo-buh-FAY-shuhnt",
            'etymology': "From Latin \"rubefaciens,\" from \"rubeus\" (red) + \"facere\" (to make).",
            'memory_tip': "Think \"rube\" (red) + \"facient\" (making) = making skin red.",
            'example_sentence': "The doctor applied a ___ ointment to increase blood flow to the injured area."
        },
        'rubeus': {
            'definition': "A Latin term meaning \"red\" or \"reddish\"; used in scientific nomenclature and heraldry; refers to red coloration in various contexts. Rubeus appears in botanical and zoological classifications.",
            'pronunciation': "/ˈrubiəs/",
            'pronunciation_respelling': "ROO-bee-uhs",
            'etymology': "From Latin \"rubeus\" (red), from \"ruber\" (red).",
            'memory_tip': "Think Latin \"red\" = rubeus.",
            'example_sentence': "The species name ___ indicates the plant's characteristic red flowers."
        },
        'rubicon': {
            'definition': "A point of no return; a boundary or limit that, once crossed, commits one to a course of action. Originally the river Caesar crossed in 49 BC, defying the Roman Senate and starting a civil war.",
            'pronunciation': "/ˈrubɪˌkɑn/",
            'pronunciation_respelling': "ROO-bi-kon",
            'etymology': "From Latin \"Rubicon,\" the river in northern Italy crossed by Julius Caesar.",
            'memory_tip': "Think Caesar crossing the river = point of no return.",
            'example_sentence': "By revealing the company secrets, she had crossed the ___."
        },
        'rubric': {
            'definition': "A set of criteria for grading or evaluation; a heading or title in red ink; a category or classification. Rubrics provide systematic standards for assessment and organization.",
            'pronunciation': "/ˈrubrɪk/",
            'pronunciation_respelling': "ROO-brik",
            'etymology': "From Latin \"rubrica,\" from \"ruber\" (red), referring to red headings in manuscripts.",
            'memory_tip': "Think \"red\" headings = rubric for organization.",
            'example_sentence': "The teacher created a detailed ___ to grade the research projects fairly."
        },
        'ruckus': {
            'definition': "A noisy disturbance or commotion; an uproar or row; a situation involving angry or excited behavior. Ruckus implies chaotic noise and disruption of normal order.",
            'pronunciation': "/ˈrʌkəs/",
            'pronunciation_respelling': "RUHK-uhs",
            'etymology': "Possibly from \"ruction\" (disturbance) or alteration of \"rumpus.\"",
            'memory_tip': "Think of noisy chaos and commotion = ruckus.",
            'example_sentence': "The announcement caused quite a ___ among the angry protesters."
        },
        'rude': {
            'definition': "Offensively impolite or ill-mannered; roughly made or crude; sudden and unpleasant. Rudeness involves lack of courtesy, refinement, or consideration for others.",
            'pronunciation': "/rud/",
            'pronunciation_respelling': "ROOD",
            'etymology': "From Old French \"rude,\" from Latin \"rudis\" (rough, raw).",
            'memory_tip': "Think of rough, unpolished behavior = rude.",
            'example_sentence': "It was ___ of him to interrupt the speaker during the presentation."
        },
        'rudiments': {
            'definition': "Basic principles or elements; the first principles of a subject; undeveloped or primitive parts. Rudiments represent fundamental knowledge or early stages of development.",
            'pronunciation': "/ˈrudəmənts/",
            'pronunciation_respelling': "ROO-duh-muhnts",
            'etymology': "From Latin \"rudimentum,\" from \"rudis\" (raw, rough).",
            'memory_tip': "Think \"rudi\" (rough) + \"ments\" = rough beginnings/basics.",
            'example_sentence': "She learned the ___ of piano playing before attempting complex pieces."
        },
        'ruelle': {
            'definition': "A narrow street or lane; a small passageway between buildings; in 17th-century France, the space between a bed and the wall where fashionable people received visitors. Ruelles represent intimate or confined spaces.",
            'pronunciation': "/ruˈɛl/",
            'pronunciation_respelling': "roo-EL",
            'etymology': "From French \"ruelle,\" from \"rue\" (street) + diminutive suffix \"-elle.\"",
            'memory_tip': "Think French \"little street\" = narrow lane.",
            'example_sentence': "The charming ___ was lined with ivy-covered walls and flower boxes."
        },
        'ruffian': {
            'definition': "A violent or lawless person; a brutal thug or hooligan; someone who engages in rough, aggressive behavior. Ruffians are characterized by their disregard for law and civility.",
            'pronunciation': "/ˈrʌfiən/",
            'pronunciation_respelling': "RUHF-ee-uhn",
            'etymology': "From Old French \"rufian,\" possibly from Italian \"ruffiano\" (pimp).",
            'memory_tip': "Think \"rough\" person = ruffian.",
            'example_sentence': "The ___ was arrested for starting fights in the tavern."
        },
        'rugby': {
            'definition': "A team sport played with an oval ball that may be kicked, carried, or passed; originated at Rugby School in England. Rugby emphasizes physical contact, teamwork, and continuous play.",
            'pronunciation': "/ˈrʌɡbi/",
            'pronunciation_respelling': "RUHG-bee",
            'etymology': "Named after Rugby School in England, where the sport was first played.",
            'memory_tip': "Think Rugby School where the sport was invented.",
            'example_sentence': "The ___ match was intense, with both teams fighting for possession."
        },
        'rugose': {
            'definition': "Having a wrinkled or ridged surface; characterized by wrinkles or folds; corrugated in appearance. Rugose describes textured surfaces with irregular patterns of ridges and depressions.",
            'pronunciation': "/ˈruɡoʊs/",
            'pronunciation_respelling': "ROO-gohs",
            'etymology': "From Latin \"rugosus,\" from \"ruga\" (wrinkle).",
            'memory_tip': "Think \"rug\" (wrinkle) + \"ose\" = wrinkled surface.",
            'example_sentence': "The coral's ___ surface provided habitat for many small marine creatures."
        },
        'ruins': {
            'definition': "Plural of ruin; the remains of buildings or structures that have fallen into decay; the state of being destroyed or decayed. Ruins represent the remnants of past civilizations or structures.",
            'pronunciation': "/ˈruɪnz/",
            'pronunciation_respelling': "ROO-inz",
            'etymology': "Plural of \"ruin,\" from Latin \"ruina,\" from \"ruere\" (to fall).",
            'memory_tip': "Think \"ruin\" + \"s\" = multiple fallen/decayed structures.",
            'example_sentence': "The ancient ___ attracted archaeologists from around the world."
        },
        'rule': {
            'definition': "A prescribed guide for conduct or action; to exercise authority or control; a regulation or law. Rules establish order, standards, and expectations for behavior or procedures.",
            'pronunciation': "/rul/",
            'pronunciation_respelling': "ROOL",
            'etymology': "From Old French \"riule,\" from Latin \"regula\" (straight stick, rule).",
            'memory_tip': "Think of straight line/regulation = rule.",
            'example_sentence': "The golden ___ states that you should treat others as you wish to be treated."
        },
        'ruled': {
            'definition': "Past tense of rule; exercised authority or control; governed or dominated; marked with straight lines. Having been under authority or having straight lines drawn.",
            'pronunciation': "/ruld/",
            'pronunciation_respelling': "ROOLD",
            'etymology': "Past tense of \"rule,\" from Latin \"regula.\"",
            'memory_tip': "Think \"rule\" + \"d\" = was controlled or had lines drawn.",
            'example_sentence': "The dictator ___ the country with an iron fist for decades."
        },
        'ruminate': {
            'definition': "To think deeply about something; to chew cud (for ruminant animals); to ponder or meditate. Rumination involves careful, prolonged consideration of ideas or experiences.",
            'pronunciation': "/ˈruməˌneɪt/",
            'pronunciation_respelling': "ROO-muh-nayt",
            'etymology': "From Latin \"ruminatus,\" from \"ruminare\" (to chew cud), from \"rumen\" (throat).",
            'memory_tip': "Think cows chewing cud = deep thinking/ruminating.",
            'example_sentence': "He would ___ for hours about the meaning of the philosophical text."
        },
        'rumor': {
            'definition': "Unverified information or gossip spread from person to person; a story or report of uncertain truth. Rumors often spread quickly but may lack factual basis.",
            'pronunciation': "/ˈrumər/",
            'pronunciation_respelling': "ROO-mur",
            'etymology': "From Latin \"rumor\" (noise, gossip), related to \"rugire\" (to roar).",
            'memory_tip': "Think unverified talk spreading like noise = rumor.",
            'example_sentence': "The ___ about the company's closure turned out to be false."
        },
        'rumour': {
            'definition': "British spelling of rumor; unverified information or gossip spread from person to person; a story of uncertain truth. This spelling variant is used in British English and Commonwealth countries.",
            'pronunciation': "/ˈrumər/",
            'pronunciation_respelling': "ROO-mur",
            'etymology': "British spelling of \"rumor,\" from Latin \"rumor\" (noise, gossip).",
            'memory_tip': "British spelling: rumor + \"u\" = rumour.",
            'example_sentence': "The ___ mill was working overtime after the announcement."
        },
        'runcible': {
            'definition': "A nonsense word invented by Edward Lear; used to describe fantastical or imaginary objects in his poetry; having no real meaning but suggesting something curved or spoon-like. Most famously used in \"runcible spoon.\"",
            'pronunciation': "/ˈrʌnsəbəl/",
            'pronunciation_respelling': "RUHN-suh-buhl",
            'etymology': "Coined by Edward Lear (1812-1888) in his nonsense poetry, possibly influenced by \"rounceval.\"",
            'memory_tip': "Think Edward Lear's nonsense word for curved utensils.",
            'example_sentence': "The owl and the pussycat dined with a ___ spoon in Lear's famous poem."
        },
        'runesancestors': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'runes' + 'ancestors' incorrectly joined. 'Runes' are ancient alphabetic symbols, while 'ancestors' refers to forebears. These should be separate words.]",
            'pronunciation': "/runz ˈænsɛstərz/",
            'pronunciation_respelling': "ROONZ AN-ses-turz",
            'etymology': "Combined word error: 'runes' from Old Norse + 'ancestors' from Latin.",
            'memory_tip': "Error combination: runes (ancient symbols) + ancestors (forebears) - should be separate.",
            'example_sentence': "The ancient ___ told stories of their ___ through carved symbols."
        },
        'running': {
            'definition': "Present participle of run; moving at a speed faster than walking; operating or functioning; continuous or ongoing. Running involves rapid movement or continuous operation.",
            'pronunciation': "/ˈrʌnɪŋ/",
            'pronunciation_respelling': "RUHN-ing",
            'etymology': "Present participle of \"run,\" from Old English \"rinnan.\"",
            'memory_tip': "Think \"run\" + \"ing\" = currently moving fast.",
            'example_sentence': "She enjoyed ___ through the park every morning before work."
        },
        'runs': {
            'definition': "Third person singular present of run; moves quickly on foot; operates or manages; flows. Current action of rapid movement, operation, or management.",
            'pronunciation': "/rʌnz/",
            'pronunciation_respelling': "RUHNZ",
            'etymology': "Third person singular of \"run,\" from Old English \"rinnan.\"",
            'memory_tip': "Think \"run\" + \"s\" = currently running.",
            'example_sentence': "The river ___ swiftly through the mountain valley."
        },
        'rupicolous': {
            'definition': "Living or growing on rocks; adapted to rocky environments; rock-dwelling. Rupicolous organisms have evolved specialized adaptations for surviving on or among rocks.",
            'pronunciation': "/ruˈpɪkələs/",
            'pronunciation_respelling': "roo-PIK-uh-luhs",
            'etymology': "From Latin \"rupes\" (rock) + \"colere\" (to inhabit) + suffix \"-ous.\"",
            'memory_tip': "Think \"rupi\" (rock) + \"colous\" (dwelling) = rock-dwelling.",
            'example_sentence': "The ___ plants had developed strong root systems to anchor in rocky crevices."
        },
        'ruscus': {
            'definition': "A genus of plants commonly known as butcher's broom; evergreen shrubs with flattened stems that resemble leaves. Ruscus species are used in floral arrangements and traditional medicine.",
            'pronunciation': "/ˈrʌskəs/",
            'pronunciation_respelling': "RUHS-kuhs",
            'etymology': "From Latin \"ruscus,\" referring to the butcher's broom plant.",
            'memory_tip': "Think of thorny shrub used by butchers = ruscus.",
            'example_sentence': "The florist used ___ branches to add texture to the holiday arrangement."
        },
        'rush': {
            'definition': "To move or act with urgent haste; a sudden quick movement; a marsh plant with cylindrical stems. Rush involves rapid action or the plant material used for weaving.",
            'pronunciation': "/rʌʃ/",
            'pronunciation_respelling': "RUHSH",
            'etymology': "From Old English \"risce\" (marsh plant) or \"hryscan\" (to make noise).",
            'memory_tip': "Think of quick, hurried movement = rush.",
            'example_sentence': "Don't ___ through the assignment; take time to do it properly."
        },
        'russet': {
            'definition': "A reddish-brown or rusty color; a variety of apple with rough, brownish skin; coarse homespun cloth. Russet describes earthy, brownish-red tones in various contexts.",
            'pronunciation': "/ˈrʌsɪt/",
            'pronunciation_respelling': "RUHS-it",
            'etymology': "From Old French \"rousset,\" from \"rous\" (red), from Latin \"russus.\"",
            'memory_tip': "Think reddish-brown autumn color = russet.",
            'example_sentence': "The ___ apples had a distinctive sweet flavor despite their rough appearance."
        },
        'rustication': {
            'definition': "The action of going to live in the countryside; temporary suspension from university; a style of masonry with rough-hewn stones. Rustication involves rural retreat or architectural texture.",
            'pronunciation': "/ˌrʌstɪˈkeɪʃən/",
            'pronunciation_respelling': "ruhs-ti-KAY-shuhn",
            'etymology': "From Latin \"rusticatio,\" from \"rusticus\" (rural), from \"rus\" (countryside).",
            'memory_tip': "Think \"rustic\" + \"ation\" = going to rural areas.",
            'example_sentence': "His ___ from Oxford gave him time to reflect on his academic goals."
        },
        'rustle': {
            'definition': "To make a soft crackling sound; to steal livestock; to move with a light, crackling noise. Rustling describes both gentle sounds and the act of cattle theft.",
            'pronunciation': "/ˈrʌsəl/",
            'pronunciation_respelling': "RUHS-uhl",
            'etymology': "From Middle English \"rustelen,\" imitative of the sound.",
            'memory_tip': "Think of leaves making soft crackling sounds = rustle.",
            'example_sentence': "The leaves began to ___ in the gentle evening breeze."
        },
        'rutabaga': {
            'definition': "A large yellow root vegetable; a cross between a cabbage and a turnip; also known as swede. Rutabagas are nutritious winter vegetables with sweet, mild flavor.",
            'pronunciation': "/ˌrutəˈbeɪɡə/",
            'pronunciation_respelling': "roo-tuh-BAY-guh",
            'etymology': "From Swedish \"rotabagge,\" from \"rot\" (root) + \"bagge\" (ram).",
            'memory_tip': "Think Swedish \"root\" vegetable = rutabaga.",
            'example_sentence': "The farmer harvested ___ from his winter garden for the local market."
        },
        'ryas': {
            'definition': "Plural of rya; Scandinavian knotted pile rugs with long, loose fibers; traditional Nordic textiles with distinctive shaggy texture. Ryas are prized for their warmth and decorative appeal.",
            'pronunciation': "/ˈriəz/",
            'pronunciation_respelling': "REE-uhz",
            'etymology': "Plural of \"rya,\" from Swedish \"rya\" (rough rug).",
            'memory_tip': "Think Scandinavian shaggy rugs = ryas.",
            'example_sentence': "The museum displayed beautiful traditional ___ from 18th-century Scandinavia."
        },
        'ryeland': {
            'definition': "A breed of sheep known for fine wool; originating in Herefordshire, England; characterized by white fleece and hardy constitution. Ryeland sheep produce high-quality wool for textiles.",
            'pronunciation': "/ˈraɪlənd/",
            'pronunciation_respelling': "RYE-luhnd",
            'etymology': "Named after the Ryeland district in Herefordshire, England.",
            'memory_tip': "Think rye-growing land where these sheep originated.",
            'example_sentence': "The ___ sheep were prized for their exceptionally soft and fine wool."
        },
        'ryelanddomesticity': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'ryeland' + 'domesticity' incorrectly joined. 'Ryeland' is a sheep breed, while 'domesticity' refers to home life. These should be separate words.]",
            'pronunciation': "/ˈraɪlənd dəˌmɛstɪsɪti/",
            'pronunciation_respelling': "RYE-luhnd duh-mes-TIS-ih-tee",
            'etymology': "Combined word error: 'ryeland' from place name + 'domesticity' from Latin.",
            'memory_tip': "Error combination: ryeland (sheep breed) + domesticity (home life) - should be separate.",
            'example_sentence': "The ___ sheep thrived in rural ___ settings."
        },
        'ryukyu': {
            'definition': "Relating to the Ryukyu Islands, a chain of Japanese islands; the historical kingdom that existed there; the indigenous culture and language of these islands. Ryukyu represents a distinct cultural region.",
            'pronunciation': "/riˈukju/",
            'pronunciation_respelling': "ree-OO-kyoo",
            'etymology': "From Japanese \"Ryūkyū,\" from Chinese \"Liu Qiu,\" meaning \"floating gourd.\"",
            'memory_tip': "Think Japanese island chain = Ryukyu.",
            'example_sentence': "The ___ Islands have a unique culture distinct from mainland Japan."
        },
        'résumé': {
            'definition': "A brief account of personal and professional qualifications; a curriculum vitae; a summary of education, work experience, and skills. Résumés are used for job applications and career advancement.",
            'pronunciation': "/ˈrezəˌmeɪ/",
            'pronunciation_respelling': "REZ-uh-may",
            'etymology': "From French \"résumé,\" past participle of \"résumer\" (to summarize).",
            'memory_tip': "Think French \"summarized\" = summary of qualifications.",
            'example_sentence': "She updated her ___ to include her recent professional accomplishments."
        },
        'sabbatical': {
            'definition': "A period of paid leave granted to academics for study or travel; an extended break from work for personal development. Sabbaticals provide opportunities for research, renewal, and professional growth.",
            'pronunciation': "/səˈbætɪkəl/",
            'pronunciation_respelling': "suh-BAT-ih-kuhl",
            'etymology': "From Latin \"sabbaticus,\" from Greek \"sabbatikos,\" from Hebrew \"shabbat\" (rest).",
            'memory_tip': "Think \"sabbath\" rest + academic leave = sabbatical.",
            'example_sentence': "The professor spent his ___ year researching climate change in Antarctica."
        },
        'sabermetrics': {
            'definition': "The application of statistical analysis to baseball records; the mathematical approach to analyzing baseball performance. Sabermetrics uses advanced statistics to evaluate players and strategies objectively.",
            'pronunciation': "/ˌseɪbərˈmɛtrɪks/",
            'pronunciation_respelling': "say-bur-MET-riks",
            'etymology': "From SABR (Society for American Baseball Research) + \"metrics\" (measurement).",
            'memory_tip': "Think \"saber\" (SABR) + \"metrics\" = baseball statistics.",
            'example_sentence': "The team's general manager relied heavily on ___ when making player acquisitions."
        },
        'sabotage': {
            'definition': "Deliberate destruction or disruption; to deliberately damage or obstruct; undermining of a cause or effort. Sabotage involves intentional interference with normal operations or processes.",
            'pronunciation': "/ˈsæbəˌtɑʒ/",
            'pronunciation_respelling': "SAB-uh-tahzh",
            'etymology': "From French \"sabotage,\" from \"sabot\" (wooden shoe), referring to workers throwing shoes into machinery.",
            'memory_tip': "Think wooden shoe thrown into machinery = sabotage.",
            'example_sentence': "The factory suspected someone was trying to ___ the production line."
        },
        'saccadic': {
            'definition': "Relating to saccades, rapid eye movements between fixation points; characterized by quick, jerky movements. Saccadic movements are essential for visual scanning and reading.",
            'pronunciation': "/səˈkædɪk/",
            'pronunciation_respelling': "suh-KAD-ik",
            'etymology': "From French \"saccade\" (jerk), from \"saquer\" (to pull), referring to jerky eye movements.",
            'memory_tip': "Think \"sac\" + \"cadic\" = jerky eye movements.",
            'example_sentence': "The researcher studied ___ eye movements during reading comprehension tests."
        },
        'sacchar': {
            'definition': "A combining form meaning sugar; used in scientific terminology related to sugars and carbohydrates; derived from saccharum (sugar). Appears in terms like saccharine and saccharide.",
            'pronunciation': "/ˈsækər/",
            'pronunciation_respelling': "SAK-ur",
            'etymology': "From Latin \"saccharum\" (sugar), from Greek \"sakcharon.\"",
            'memory_tip': "Think \"sacchar\" = sugar in scientific terms.",
            'example_sentence': "The prefix ___ appears in many chemistry terms related to sugars."
        },
        'saccharide': {
            'definition': "A sugar or carbohydrate; any of a class of compounds including sugars, starches, and cellulose. Saccharides are essential biomolecules that provide energy and structural support.",
            'pronunciation': "/ˈsækəˌraɪd/",
            'pronunciation_respelling': "SAK-uh-rahyd",
            'etymology': "From \"sacchar\" (sugar) + suffix \"-ide\" (chemical compound).",
            'memory_tip': "Think \"sacchar\" (sugar) + \"ide\" = sugar compound.",
            'example_sentence': "Glucose is a simple ___ that provides immediate energy to cells."
        },
        'saccharum': {
            'definition': "The scientific genus name for sugarcane; sugar in its natural form; the Latin term for sugar. Saccharum represents the botanical classification for sugar-producing plants.",
            'pronunciation': "/ˈsækərəm/",
            'pronunciation_respelling': "SAK-ur-uhm",
            'etymology': "From Latin \"saccharum\" (sugar), from Greek \"sakcharon.\"",
            'memory_tip': "Think Latin \"sugar\" = saccharum for sugarcane.",
            'example_sentence': "___ officinarum is the scientific name for commercial sugarcane."
        },
        'sacerdotal': {
            'definition': "Relating to priests or the priesthood; priestly in character or function; having to do with sacred duties. Sacerdotal describes the religious authority and functions of ordained clergy.",
            'pronunciation': "/ˌsæsərˈdoʊtəl/",
            'pronunciation_respelling': "sas-ur-DOHT-uhl",
            'etymology': "From Latin \"sacerdotalis,\" from \"sacerdos\" (priest), from \"sacer\" (sacred).",
            'memory_tip': "Think \"sacer\" (sacred) + \"dotal\" = relating to sacred priesthood.",
            'example_sentence': "The cathedral's ___ vestments were made of the finest silk and gold thread."
        },
        'sackbuts': {
            'definition': "Plural of sackbut; early trombones used in Renaissance and Baroque music; wind instruments with sliding tubes for changing pitch. Sackbuts were important brass instruments in historical ensembles.",
            'pronunciation': "/ˈsækbʌts/",
            'pronunciation_respelling': "SAK-buhts",
            'etymology': "Plural of \"sackbut,\" from Old French \"saqueboute,\" meaning \"pull-push.\"",
            'memory_tip': "Think \"sac\" (pull) + \"buts\" (push) = early slide instruments.",
            'example_sentence': "The Renaissance ensemble featured authentic ___ and other period instruments."
        },
        'sacrament': {
            'definition': "A religious ceremony regarded as an outward sign of spiritual grace; a sacred ritual in Christian churches; something regarded as sacred. Sacraments are formal religious observances with spiritual significance.",
            'pronunciation': "/ˈsækrəmənt/",
            'pronunciation_respelling': "SAK-ruh-muhnt",
            'etymology': "From Latin \"sacramentum,\" from \"sacer\" (sacred).",
            'memory_tip': "Think \"sacr\" (sacred) + \"ament\" = sacred ceremony.",
            'example_sentence': "Baptism is considered the first ___ in many Christian denominations."
        },
        'sacred': {
            'definition': "Connected with God or dedicated to religious purpose; regarded with reverence; inviolable or not to be interfered with. Sacred things are set apart as holy or deserving special respect.",
            'pronunciation': "/ˈseɪkrɪd/",
            'pronunciation_respelling': "SAY-krid",
            'etymology': "From Latin \"sacer\" (holy, sacred).",
            'memory_tip': "Think \"sacr\" (holy) + \"ed\" = made holy.",
            'example_sentence': "The ancient temple was considered ___ ground by all who lived nearby."
        },
        'sacrifice': {
            'definition': "The act of giving up something valued for something else; an offering to a deity; to surrender something for a greater cause. Sacrifice involves loss or surrender for a perceived benefit.",
            'pronunciation': "/ˈsækrəˌfaɪs/",
            'pronunciation_respelling': "SAK-ruh-fahys",
            'etymology': "From Latin \"sacrificium,\" from \"sacer\" (sacred) + \"facere\" (to make).",
            'memory_tip': "Think \"sacr\" (sacred) + \"fice\" (make) = make sacred offering.",
            'example_sentence': "She was willing to ___ her free time to help with the charity event."
        },
        'sacristy': {
            'definition': "A room in a church where sacred vessels and vestments are kept; a vestry where priests prepare for services. Sacristies serve as storage and preparation areas for religious ceremonies.",
            'pronunciation': "/ˈsækrɪsti/",
            'pronunciation_respelling': "SAK-ris-tee",
            'etymology': "From Medieval Latin \"sacristia,\" from \"sacer\" (sacred).",
            'memory_tip': "Think \"sacr\" (sacred) + \"isty\" = place for sacred items.",
            'example_sentence': "The priest put on his ceremonial robes in the church ___."
        },
        'sacrosanct': {
            'definition': "Regarded as too important and revered to be interfered with; inviolable; sacred and immune from criticism. Sacrosanct things are considered absolutely protected from violation.",
            'pronunciation': "/ˈsækroʊˌsæŋkt/",
            'pronunciation_respelling': "SAK-roh-sangkt",
            'etymology': "From Latin \"sacrosanctus,\" from \"sacer\" (sacred) + \"sanctus\" (holy).",
            'memory_tip': "Think \"sacro\" (sacred) + \"sanct\" (holy) = doubly sacred/protected.",
            'example_sentence': "The constitutional rights were considered ___ by all citizens."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_152_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_152_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['runesancestors', 'ryelanddomesticity']
    
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
                    'notes': 'Batch 152 processing',
                    'review_status': 'pending',
                    'batch_number': '152'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 152 processing complete!")
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