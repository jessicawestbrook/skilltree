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
            'regular': ['safe', 'saga', 'sailor', 'sailors', 'saints', 'salad', 'salamanders', 'salute', 'same', 'samples', 'samuel', 'sand', 'sandal', 'sandwich', 'sanitation'],
            'semi_regular': ['saeta', 'sagacious', 'sagittarius', 'sahel', 'sailage', 'sakura', 'salivate', 'salsa', 'saltwater', 'salubrious', 'salutary', 'salvador', 'sambal', 'samhain', 'samoa', 'samosas', 'samsara', 'sanctimonious', 'sangfroid'],
            'irregular': ['sais', 'sakcharon', 'saketh', 'salience', 'salmagundi', 'salmagundy', 'saltarellos', 'saltatory', 'saltern', 'salzkammergut', 'samarium', 'samian', 'sangamon', 'sanglier']
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
        high_frequency = ['safe', 'saga', 'sailor', 'sailors', 'saints', 'salad', 'salute', 'same', 'samples', 'sand', 'sandal', 'sandwich', 'sanitation']
        medium_frequency = ['sagacious', 'sagittarius', 'sakura', 'salivate', 'salsa', 'saltwater', 'salubrious', 'salutary', 'salvador', 'samoa', 'samosas', 'samsara', 'samuel', 'sanctimonious', 'sangfroid']
        low_frequency = ['saeta', 'sahel', 'sailage', 'sais', 'sakcharon', 'saketh', 'salamanders', 'salience', 'salmagundi', 'salmagundy', 'saltarellos', 'saltatory', 'saltern', 'salzkammergut', 'samarium', 'sambal', 'samhain', 'samian', 'sangamon', 'sanglier']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['safe', 'saga', 'sailor', 'sailors', 'saints', 'salad', 'salute', 'same', 'sand', 'samuel']
        moderate_words = ['saeta', 'sagacious', 'sagittarius', 'sahel', 'sailage', 'sakura', 'salamanders', 'salience', 'salivate', 'salsa', 'saltwater', 'salubrious', 'salutary', 'salvador', 'sambal', 'samoa', 'samosas', 'samsara', 'samples', 'sanctimonious', 'sandal', 'sandwich', 'sangfroid', 'sanitation'],
        complex_words = ['sais', 'sakcharon', 'saketh', 'salmagundi', 'salmagundy', 'saltarellos', 'saltatory', 'saltern', 'salzkammergut', 'samarium', 'samhain', 'samian', 'sangamon', 'sanglier']
        
        if word in simple_words:
            return 2
        elif word in moderate_words:
            return 4
        elif word in complex_words:
            return 7
        else:
            return 5
    
    def _calculate_etymology_complexity(self, etymology):
        if 'Sanskrit' in etymology or 'Japanese' in etymology:
            return 6
        elif 'Greek' in etymology:
            return 7
        elif 'Latin' in etymology and 'Greek' in etymology:
            return 8
        elif 'Latin' in etymology and 'prefix' in etymology:
            return 6
        elif 'Latin' in etymology or 'French' in etymology or 'Spanish' in etymology:
            return 4
        elif 'Old English' in etymology or 'Germanic' in etymology:
            return 3
        else:
            return 5

def main():
    calculator = DifficultyCalculator()
    
    word_data = {
        'saeta': {
            'definition': "A type of Andalusian religious song, typically performed during Holy Week; an arrow or dart; a bristle-like structure in certain animals. Saetas are passionate, improvised songs expressing religious devotion, particularly associated with Spanish Easter processions.",
            'pronunciation': "/saˈetə/",
            'pronunciation_respelling': "sah-AY-tuh",
            'etymology': "From Spanish \"saeta\" (arrow), from Latin \"sagitta\" (arrow).",
            'memory_tip': "Think Spanish \"arrow\" = piercing religious song.",
            'example_sentence': "The passionate ___ echoed through the narrow streets during the Holy Week procession."
        },
        'safe': {
            'definition': "Protected from danger or risk; not likely to cause harm; a strong box for storing valuables. Safety involves freedom from danger, harm, or loss through protective measures or secure storage.",
            'pronunciation': "/seɪf/",
            'pronunciation_respelling': "SAYF",
            'etymology': "From Old French \"sauf,\" from Latin \"salvus\" (whole, safe).",
            'memory_tip': "Think \"salv\" (save) = protected from harm.",
            'example_sentence': "The important documents were kept in a fireproof ___."
        },
        'saga': {
            'definition': "A long story of heroic achievement; a medieval Icelandic or Norwegian prose narrative; any long, involved story. Sagas traditionally recount the adventures and genealogies of legendary heroes and families.",
            'pronunciation': "/ˈsɑɡə/",
            'pronunciation_respelling': "SAH-guh",
            'etymology': "From Old Norse \"saga\" (story, history), from \"segja\" (to say).",
            'memory_tip': "Think Old Norse \"say\" = long story told.",
            'example_sentence': "The Icelandic ___ told of brave warriors and their epic adventures."
        },
        'sagacious': {
            'definition': "Having or showing keen mental discernment and good judgment; wise and shrewd. Sagacity involves the ability to make sound decisions based on wisdom and understanding rather than just intelligence.",
            'pronunciation': "/səˈɡeɪʃəs/",
            'pronunciation_respelling': "suh-GAY-shuhs",
            'etymology': "From Latin \"sagax\" (wise, shrewd), from \"sagire\" (to perceive acutely).",
            'memory_tip': "Think \"sag\" (wise) + \"acious\" = full of wisdom.",
            'example_sentence': "The ___ old judge was known for his fair and thoughtful decisions."
        },
        'sagittarius': {
            'definition': "The ninth sign of the zodiac; a constellation representing an archer; a person born under this astrological sign. Sagittarius is traditionally associated with adventure, philosophy, and truth-seeking.",
            'pronunciation': "/ˌsædʒɪˈtɛriəs/",
            'pronunciation_respelling': "saj-ih-TAIR-ee-uhs",
            'etymology': "From Latin \"sagittarius\" (archer), from \"sagitta\" (arrow).",
            'memory_tip': "Think \"sagitta\" (arrow) = archer constellation.",
            'example_sentence': "As a ___, she was known for her love of travel and adventure."
        },
        'sahel': {
            'definition': "A semi-arid region of Africa south of the Sahara Desert; the transitional zone between the Sahara and the tropical savannas. The Sahel is characterized by drought-prone grasslands and scattered trees.",
            'pronunciation': "/səˈhɛl/",
            'pronunciation_respelling': "suh-HEL",
            'etymology': "From Arabic \"sāḥil\" (border, shore), referring to the edge of the desert.",
            'memory_tip': "Think Arabic \"shore\" = border zone of the desert.",
            'example_sentence': "Climate change has severely affected agriculture in the ___."
        },
        'sailage': {
            'definition': "Collective term for sails; the complete set of sails on a vessel; canvas or fabric used for making sails. Sailage encompasses all the wind-catching apparatus of a sailing vessel.",
            'pronunciation': "/ˈseɪlɪdʒ/",
            'pronunciation_respelling': "SAYL-ij",
            'etymology': "From \"sail\" + suffix \"-age\" (collection of), from Old English \"segel.\"",
            'memory_tip': "Think \"sail\" + \"age\" = collection of sails.",
            'example_sentence': "The tall ship's impressive ___ caught the wind and propelled it forward."
        },
        'sailagesalience': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'sailage' + 'salience' incorrectly joined. 'Sailage' refers to a ship's sails, while 'salience' means prominence or importance. These should be separate words.]",
            'pronunciation': "/ˈseɪlɪdʒ ˈseɪliəns/",
            'pronunciation_respelling': "SAYL-ij SAY-lee-uhns",
            'etymology': "Combined word error: 'sailage' from Old English + 'salience' from Latin.",
            'memory_tip': "Error combination: sailage (ship's sails) + salience (prominence) - should be separate.",
            'example_sentence': "The ship's ___ was impressive, and the ___ of the mast made it visible from afar."
        },
        'sailor': {
            'definition': "A person who works on a ship or boat; a member of a navy; someone skilled in sailing. Sailors are experienced in maritime navigation, seamanship, and naval operations.",
            'pronunciation': "/ˈseɪlər/",
            'pronunciation_respelling': "SAYL-ur",
            'etymology': "From \"sail\" + suffix \"-or\" (one who), from Old English \"segel.\"",
            'memory_tip': "Think \"sail\" + \"or\" = one who sails.",
            'example_sentence': "The experienced ___ navigated the rough seas with confidence."
        },
        'sailors': {
            'definition': "Plural of sailor; people who work on ships or boats; members of a navy; those skilled in sailing. Sailors collectively form the crew responsible for operating vessels at sea.",
            'pronunciation': "/ˈseɪlərz/",
            'pronunciation_respelling': "SAYL-urz",
            'etymology': "Plural of \"sailor,\" from Old English \"segel\" (sail).",
            'memory_tip': "Think \"sailor\" + \"s\" = multiple people who sail.",
            'example_sentence': "The brave ___ returned home after months at sea."
        },
        'saints': {
            'definition': "Plural of saint; holy or virtuous people recognized by religious communities; people of exceptional virtue. Saints are venerated for their spiritual achievements and moral excellence.",
            'pronunciation': "/seɪnts/",
            'pronunciation_respelling': "SAYNTS",
            'etymology': "Plural of \"saint,\" from Latin \"sanctus\" (holy).",
            'memory_tip': "Think \"sanct\" (holy) = holy people.",
            'example_sentence': "The cathedral was dedicated to all ___ and martyrs."
        },
        'sais': {
            'definition': "Plural of sai; traditional Okinawan weapons with three prongs; used in martial arts for defense and offense. Sais are characterized by their central blade and two curved side guards.",
            'pronunciation': "/saɪz/",
            'pronunciation_respelling': "SYEZ",
            'etymology': "Plural of \"sai,\" from Japanese, possibly from Chinese \"chai\" (hairpin).",
            'memory_tip': "Think Japanese three-pronged martial arts weapons.",
            'example_sentence': "The martial artist practiced kata with traditional ___."
        },
        'sakcharon': {
            'definition': "An archaic or variant form of saccharon; referring to sugar or sweet substances; related to saccharide chemistry. Used in historical or specialized scientific contexts.",
            'pronunciation': "/ˈsækərɑn/",
            'pronunciation_respelling': "SAK-uh-ron",
            'etymology': "From Greek \"sakcharon\" (sugar), variant of \"saccharum.\"",
            'memory_tip': "Think Greek \"sugar\" = sakcharon.",
            'example_sentence': "The ancient text referred to ___ as a precious imported substance."
        },
        'saketh': {
            'definition': "An archaic third person singular form meaning \"says\" or \"speaks\"; old English verb form; used in historical or literary contexts. Appears in older texts and biblical language.",
            'pronunciation': "/ˈseɪkəθ/",
            'pronunciation_respelling': "SAY-kuhth",
            'etymology': "From Old English \"secgan\" (to say) + archaic third person ending \"-eth.\"",
            'memory_tip': "Think archaic \"says\" = saketh.",
            'example_sentence': "The prophet ___ unto the people in the ancient scripture."
        },
        'sakura': {
            'definition': "Japanese term for cherry blossoms; the cultural practice of viewing cherry blossoms; represents the ephemeral nature of life in Japanese philosophy. Sakura season is celebrated throughout Japan with festivals and gatherings.",
            'pronunciation': "/səˈkurə/",
            'pronunciation_respelling': "sah-KOO-rah",
            'etymology': "From Japanese \"sakura\" (cherry blossom), of uncertain origin.",
            'memory_tip': "Think Japanese cherry blossoms = sakura.",
            'example_sentence': "The ___ season draws millions of visitors to Japan's parks and temples."
        },
        'salad': {
            'definition': "A cold dish of mixed vegetables, fruits, or other ingredients; a mixture of raw or cooked ingredients served with dressing. Salads provide nutrition and refreshment through varied combinations of foods.",
            'pronunciation': "/ˈsæləd/",
            'pronunciation_respelling': "SAL-uhd",
            'etymology': "From Old French \"salade,\" from Provençal \"salada,\" from \"salar\" (to salt).",
            'memory_tip': "Think \"sal\" (salt) = salted/seasoned mixed dish.",
            'example_sentence': "The garden ___ was made with fresh lettuce, tomatoes, and cucumber."
        },
        'salamanders': {
            'definition': "Plural of salamander; amphibians that can regenerate lost limbs; mythical creatures associated with fire; heat-resistant cooking utensils. Salamanders are known for their remarkable regenerative abilities.",
            'pronunciation': "/ˈsæləˌmændərz/",
            'pronunciation_respelling': "SAL-uh-man-durz",
            'etymology': "Plural of \"salamander,\" from Latin \"salamandra,\" from Greek \"salamandra.\"",
            'memory_tip': "Think fire-resistant amphibians = salamanders.",
            'example_sentence': "The biologist studied how ___ regenerate their tails after injury."
        },
        'salience': {
            'definition': "The quality of being particularly noticeable or important; prominence; the most important or conspicuous feature. Salience involves standing out due to significance, urgency, or relevance.",
            'pronunciation': "/ˈseɪliəns/",
            'pronunciation_respelling': "SAY-lee-uhns",
            'etymology': "From Latin \"saliens\" (leaping), from \"salire\" (to leap), referring to things that leap out.",
            'memory_tip': "Think \"sal\" (leap) + \"ience\" = leaping out in importance.",
            'example_sentence': "The ___ of the environmental issue became clear during the drought."
        },
        'salinityanalogize': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'salinity' + 'analogize' incorrectly joined. 'Salinity' refers to salt content, while 'analogize' means to make analogies. These should be separate words.]",
            'pronunciation': "/səˈlɪnəti əˈnæləˌdʒaɪz/",
            'pronunciation_respelling': "suh-LIN-ih-tee uh-NAL-uh-jyz",
            'etymology': "Combined word error: 'salinity' from Latin + 'analogize' from Greek.",
            'memory_tip': "Error combination: salinity (salt content) + analogize (make comparisons) - should be separate.",
            'example_sentence': "The ___ of the water was high, and scientists ___ it to other mineral concentrations."
        },
        'salivate': {
            'definition': "To produce saliva; to show great desire or anticipation for something; to drool. Salivation can be a physiological response to food or a metaphor for eager anticipation.",
            'pronunciation': "/ˈsæləˌveɪt/",
            'pronunciation_respelling': "SAL-uh-vayt",
            'etymology': "From Latin \"salivare,\" from \"saliva\" (spittle).",
            'memory_tip': "Think \"saliva\" + \"ate\" = produce saliva.",
            'example_sentence': "The delicious aroma made everyone ___ in anticipation of dinner."
        },
        'salmagundi': {
            'definition': "A salad dish containing a mixture of chopped meat, anchovies, eggs, and vegetables; any heterogeneous mixture or medley. Salmagundi represents variety and mixture in both culinary and general contexts.",
            'pronunciation': "/ˌsælməˈɡʌndi/",
            'pronunciation_respelling': "sal-muh-GUHN-dee",
            'etymology': "From French \"salmigondis,\" of uncertain origin, possibly from \"sel\" (salt) + mixture.",
            'memory_tip': "Think mixed salad with everything = salmagundi.",
            'example_sentence': "The restaurant's ___ featured an eclectic mix of ingredients and flavors."
        },
        'salmagundy': {
            'definition': "Variant spelling of salmagundi; a mixed salad dish; any heterogeneous mixture or medley. This alternate spelling appears in historical cookbooks and literary works.",
            'pronunciation': "/ˌsælməˈɡʌndi/",
            'pronunciation_respelling': "sal-muh-GUHN-dee",
            'etymology': "Variant of \"salmagundi,\" from French \"salmigondis.\"",
            'memory_tip': "Alternate spelling of mixed salad dish = salmagundy.",
            'example_sentence': "The colonial cookbook included a recipe for traditional ___."
        },
        'salsa': {
            'definition': "A spicy sauce made from tomatoes, onions, and peppers; a style of Latin American dance and music; any sauce or mixture. Salsa encompasses both culinary and cultural expressions.",
            'pronunciation': "/ˈsælsə/",
            'pronunciation_respelling': "SAL-suh",
            'etymology': "From Spanish \"salsa\" (sauce), from Latin \"salsus\" (salted).",
            'memory_tip': "Think Spanish \"sauce\" = spicy mixture or lively dance.",
            'example_sentence': "The fresh ___ made with tomatoes and cilantro was perfect with the chips."
        },
        'saltarellos': {
            'definition': "Plural of saltarello; Italian folk dances characterized by lively jumping movements; musical compositions in triple meter for such dances. Saltarellos are energetic dances popular in Renaissance Italy.",
            'pronunciation': "/ˌsæltəˈreloʊz/",
            'pronunciation_respelling': "sal-tuh-REL-ohz",
            'etymology': "Plural of \"saltarello,\" from Italian, from \"saltare\" (to jump).",
            'memory_tip': "Think Italian \"jump\" = lively jumping dances.",
            'example_sentence': "The Renaissance ensemble performed several traditional ___."
        },
        'saltatory': {
            'definition': "Relating to leaping or dancing; characterized by jumping movements; proceeding by leaps rather than gradual stages. Saltatory describes motion or progression involving sudden jumps.",
            'pronunciation': "/ˈsæltəˌtɔri/",
            'pronunciation_respelling': "SAL-tuh-tor-ee",
            'etymology': "From Latin \"saltatorius,\" from \"saltare\" (to leap), from \"salire\" (to jump).",
            'memory_tip': "Think \"salt\" (jump) + \"atory\" = relating to jumping.",
            'example_sentence': "The ___ evolution of the species occurred in rapid bursts."
        },
        'saltern': {
            'definition': "A set of pools or beds for producing salt by evaporation of seawater; a saltworks or salt marsh used for salt production. Salterns are important for commercial salt harvesting and wildlife habitat.",
            'pronunciation': "/ˈsɔltərn/",
            'pronunciation_respelling': "SAWL-turn",
            'etymology': "From \"salt\" + suffix \"-ern\" (place), from Old English \"sealt.\"",
            'memory_tip': "Think \"salt\" + \"ern\" (place) = place for making salt.",
            'example_sentence': "The ancient ___ still produces sea salt using traditional evaporation methods."
        },
        'saltwater': {
            'definition': "Water that contains salt; seawater; relating to the ocean or marine environments. Saltwater distinguishes ocean water from freshwater and describes marine ecosystems.",
            'pronunciation': "/ˈsɔltˌwɔtər/",
            'pronunciation_respelling': "SAWLT-waw-tur",
            'etymology': "Compound of \"salt\" + \"water,\" from Old English \"sealt\" + \"wæter.\"",
            'memory_tip': "Think \"salt\" + \"water\" = ocean water.",
            'example_sentence': "The ___ aquarium featured tropical fish from coral reefs."
        },
        'salubrious': {
            'definition': "Health-giving; promoting health or well-being; having a beneficial effect on health. Salubrious conditions contribute to physical and mental wellness through positive environmental factors.",
            'pronunciation': "/səˈlubriəs/",
            'pronunciation_respelling': "suh-LOO-bree-uhs",
            'etymology': "From Latin \"salubris\" (healthy), from \"salus\" (health).",
            'memory_tip': "Think \"salub\" (health) + \"rious\" = promoting health.",
            'example_sentence': "The mountain air was considered ___ for patients with respiratory problems."
        },
        'salutary': {
            'definition': "Producing good effects; beneficial; tending to improve or promote health. Salutary influences contribute positively to well-being, learning, or moral development.",
            'pronunciation': "/ˈsæljəˌtɛri/",
            'pronunciation_respelling': "SAL-yuh-ter-ee",
            'etymology': "From Latin \"salutaris,\" from \"salus\" (health, welfare).",
            'memory_tip': "Think \"salut\" (health) + \"ary\" = promoting health/benefit.",
            'example_sentence': "The criticism had a ___ effect on his writing skills."
        },
        'salute': {
            'definition': "A gesture of respect or recognition; to greet respectfully; a formal military greeting. Salutes express honor, respect, or acknowledgment through specific gestures or actions.",
            'pronunciation': "/səˈlut/",
            'pronunciation_respelling': "suh-LOOT",
            'etymology': "From Latin \"salutare\" (to greet), from \"salus\" (health, greeting).",
            'memory_tip': "Think \"salut\" (greet) = respectful greeting.",
            'example_sentence': "The soldiers gave a crisp ___ to their commanding officer."
        },
        'salvador': {
            'definition': "Spanish name meaning \"savior\"; refers to El Salvador, a Central American country; a given name. Salvador can refer to the person, place, or concept of salvation.",
            'pronunciation': "/ˈsælvəˌdɔr/",
            'pronunciation_respelling': "SAL-vuh-dor",
            'etymology': "From Spanish \"salvador\" (savior), from Latin \"salvator,\" from \"salvare\" (to save).",
            'memory_tip': "Think \"salv\" (save) + \"ador\" = savior.",
            'example_sentence': "The artist ___ Dalí was known for his surrealist paintings."
        },
        'salzkammergut': {
            'definition': "A resort region in Austria known for its lakes and mountains; literally means \"salt chamber estate\"; a historic salt-producing area. The region is famous for its scenic beauty and cultural heritage.",
            'pronunciation': "/ˈzɑltsˌkæmərˌɡut/",
            'pronunciation_respelling': "ZAHLTS-kam-ur-goot",
            'etymology': "From German \"Salz\" (salt) + \"Kammer\" (chamber) + \"Gut\" (estate).",
            'memory_tip': "Think German \"salt chamber estate\" = Austrian lake region.",
            'example_sentence': "The ___ region attracts tourists with its crystal-clear alpine lakes."
        },
        'samarium': {
            'definition': "A rare earth metallic element with the symbol Sm; used in permanent magnets and nuclear applications. Samarium is valuable for its magnetic properties and role in advanced technologies.",
            'pronunciation': "/səˈmɛriəm/",
            'pronunciation_respelling': "suh-MAIR-ee-uhm",
            'etymology': "Named after samarskite, a mineral, which was named after Russian official V.E. Samarsky-Bykhovets.",
            'memory_tip': "Think named after Samarsky + element suffix \"-ium.\"",
            'example_sentence': "The high-tech speakers used ___ magnets for superior sound quality."
        },
        'sambal': {
            'definition': "A spicy Indonesian and Malaysian sauce or relish made with chili peppers; a condiment used to add heat and flavor to dishes. Sambal varieties differ by region and ingredients used.",
            'pronunciation': "/ˈsæmbæl/",
            'pronunciation_respelling': "SAM-bal",
            'etymology': "From Malay/Indonesian \"sambal,\" possibly from Javanese.",
            'memory_tip': "Think Indonesian spicy chili sauce = sambal.",
            'example_sentence': "The nasi goreng was served with fiery ___ on the side."
        },
        'same': {
            'definition': "Identical; not different; unchanged; the very one and not another. Sameness implies complete similarity or lack of variation between things being compared.",
            'pronunciation': "/seɪm/",
            'pronunciation_respelling': "SAYM",
            'etymology': "From Old Norse \"samr,\" of Germanic origin, related to \"similar.\"",
            'memory_tip': "Think identical or not different = same.",
            'example_sentence': "They were wearing the exact ___ dress to the party."
        },
        'samhain': {
            'definition': "An ancient Celtic festival marking the end of harvest season; the origin of modern Halloween; celebrated on October 31st. Samhain traditionally honored ancestors and marked the beginning of winter.",
            'pronunciation': "/ˈsaʊɪn/",
            'pronunciation_respelling': "SOW-in",
            'etymology': "From Irish \"Samhain,\" from \"sam\" (summer) + \"fuin\" (end).",
            'memory_tip': "Think Irish \"summer's end\" = ancient Halloween festival.",
            'example_sentence': "The Celtic celebration of ___ included bonfires and remembrance of the dead."
        },
        'samian': {
            'definition': "Relating to the Greek island of Samos; a type of ancient pottery from Samos; of or from Samos. Samian pottery was prized in antiquity for its quality and distinctive red color.",
            'pronunciation': "/ˈseɪmiən/",
            'pronunciation_respelling': "SAY-mee-uhn",
            'etymology': "From Latin \"Samius,\" from Greek \"Samios,\" relating to Samos island.",
            'memory_tip': "Think island of Samos = Samian pottery.",
            'example_sentence': "The archaeologist discovered fragments of ___ pottery at the ancient site."
        },
        'samoa': {
            'definition': "An island nation in the South Pacific; relating to Samoa or its people; a type of Girl Scout cookie. Samoa encompasses both the geographic location and cultural identity.",
            'pronunciation': "/səˈmoʊə/",
            'pronunciation_respelling': "suh-MOH-uh",
            'etymology': "From Samoan \"Sāmoa,\" possibly meaning \"sacred center.\"",
            'memory_tip': "Think Pacific island nation = Samoa.",
            'example_sentence': "___ is known for its beautiful beaches and rich Polynesian culture."
        },
        'samosas': {
            'definition': "Plural of samosa; triangular fried or baked pastries filled with spiced vegetables or meat; popular South Asian snacks. Samosas are crispy appetizers enjoyed throughout India and neighboring regions.",
            'pronunciation': "/səˈmoʊsəz/",
            'pronunciation_respelling': "suh-MOH-suhz",
            'etymology': "Plural of \"samosa,\" from Hindi \"samosa,\" possibly from Persian \"sambosag.\"",
            'memory_tip': "Think triangular Indian fried pastries = samosas.",
            'example_sentence': "The restaurant served crispy ___ with mint chutney as an appetizer."
        },
        'samples': {
            'definition': "Plural of sample; small portions taken as examples; specimens for testing or analysis; examples or instances. Samples represent larger groups or serve as test materials.",
            'pronunciation': "/ˈsæmpəlz/",
            'pronunciation_respelling': "SAM-puhlz",
            'etymology': "Plural of \"sample,\" from Old French \"essample,\" from Latin \"exemplum.\"",
            'memory_tip': "Think \"example\" = small portions representing the whole.",
            'example_sentence': "The laboratory analyzed blood ___ to check for infections."
        },
        'samsara': {
            'definition': "In Hindu and Buddhist philosophy, the cycle of death and rebirth; the continuous cycle of life, death, and reincarnation. Samsara represents the eternal cycle from which liberation is sought.",
            'pronunciation': "/sæmˈsɑrə/",
            'pronunciation_respelling': "sam-SAH-ruh",
            'etymology': "From Sanskrit \"saṃsāra,\" from \"saṃ\" (together) + \"sṛ\" (to flow).",
            'memory_tip': "Think Sanskrit \"flowing together\" = cycle of rebirth.",
            'example_sentence': "Buddhist teachings focus on escaping the endless cycle of ___."
        },
        'samuel': {
            'definition': "A Hebrew name meaning \"heard by God\"; a biblical prophet and judge; a common male given name. Samuel represents both religious significance and personal identity.",
            'pronunciation': "/ˈsæmjuəl/",
            'pronunciation_respelling': "SAM-yoo-uhl",
            'etymology': "From Hebrew \"Shemu'el,\" from \"shama\" (heard) + \"El\" (God).",
            'memory_tip': "Think Hebrew \"heard by God\" = Samuel.",
            'example_sentence': "The prophet ___ anointed the first kings of Israel."
        },
        'sanctimonious': {
            'definition': "Making a show of being morally superior; hypocritically pious; displaying false righteousness. Sanctimonious behavior involves pretentious moral superiority rather than genuine virtue.",
            'pronunciation': "/ˌsæŋktəˈmoʊniəs/",
            'pronunciation_respelling': "sangk-tuh-MOH-nee-uhs",
            'etymology': "From Latin \"sanctimonia\" (sanctity), from \"sanctus\" (holy).",
            'memory_tip': "Think \"sanct\" (holy) + \"monious\" = falsely showing holiness.",
            'example_sentence': "His ___ lecture about honesty rang hollow given his recent lies."
        },
        'sand': {
            'definition': "Fine particles of rock and mineral; material found on beaches and deserts; to smooth with sandpaper. Sand consists of weathered rock fragments and serves various construction and recreational purposes.",
            'pronunciation': "/sænd/",
            'pronunciation_respelling': "SAND",
            'etymology': "From Old English \"sand,\" of Germanic origin.",
            'memory_tip': "Think fine rock particles found on beaches = sand.",
            'example_sentence': "The children built elaborate castles in the soft beach ___."
        },
        'sandal': {
            'definition': "An open shoe consisting of a sole held to the foot by straps; light footwear for warm weather. Sandals provide foot protection while allowing air circulation and easy wear.",
            'pronunciation': "/ˈsændəl/",
            'pronunciation_respelling': "SAN-duhl",
            'etymology': "From Latin \"sandalium,\" from Greek \"sandalion.\"",
            'memory_tip': "Think open shoe with straps = sandal.",
            'example_sentence': "She wore comfortable leather ___ for the beach walk."
        },
        'sandwich': {
            'definition': "Food consisting of ingredients between slices of bread; to place between two things; to squeeze into a tight space. Sandwiches provide portable meals and the verb describes inserting between objects.",
            'pronunciation': "/ˈsændwɪtʃ/",
            'pronunciation_respelling': "SAND-wich",
            'etymology': "Named after the 4th Earl of Sandwich (1718-1792), who popularized this form of eating.",
            'memory_tip': "Think Earl of Sandwich who ate meat between bread slices.",
            'example_sentence': "She made a turkey and cheese ___ for lunch."
        },
        'sangamon': {
            'definition': "A county in Illinois; a geological period; relating to a specific interglacial stage. Sangamon represents both geographic and geological significance in North American classification systems.",
            'pronunciation': "/ˈsæŋɡəmən/",
            'pronunciation_respelling': "SANG-guh-muhn",
            'etymology': "From the Sangamon River in Illinois, from Native American origin.",
            'memory_tip': "Think Illinois county and geological period = Sangamon.",
            'example_sentence': "The ___ interglacial period occurred between ice ages."
        },
        'sangfroid': {
            'definition': "Composure or coolness shown in danger or under trying circumstances; self-possession in difficult situations. Sangfroid involves maintaining calm and rational thinking during stress or crisis.",
            'pronunciation': "/ˌsæŋˈfrɔɪd/",
            'pronunciation_respelling': "sang-FROYD",
            'etymology': "From French \"sang-froid,\" literally \"cold blood.\"",
            'memory_tip': "Think French \"cold blood\" = coolness under pressure.",
            'example_sentence': "The pilot's ___ during the emergency landing saved all passengers."
        },
        'sanglier': {
            'definition': "French term for wild boar; a heraldic representation of a wild boar; used in hunting and culinary contexts. Sanglier appears in French cuisine and European coat of arms.",
            'pronunciation': "/sɑnˈɡlie/",
            'pronunciation_respelling': "sahn-GLEE-ay",
            'etymology': "From French \"sanglier\" (wild boar), from Latin \"singularis\" (alone).",
            'memory_tip': "Think French wild boar = sanglier.",
            'example_sentence': "The restaurant featured ___ as a seasonal specialty dish."
        },
        'sanitation': {
            'definition': "Conditions relating to public health, especially sewage disposal and clean water supply; the process of keeping places clean and hygienic. Sanitation prevents disease through proper waste management and hygiene.",
            'pronunciation': "/ˌsænəˈteɪʃən/",
            'pronunciation_respelling': "san-ih-TAY-shuhn",
            'etymology': "From \"sanitary\" + suffix \"-ation,\" from Latin \"sanitas\" (health).",
            'memory_tip': "Think \"sanit\" (health) + \"ation\" = process of maintaining health.",
            'example_sentence': "Poor ___ in the refugee camp led to outbreaks of disease."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_153_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_153_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['sailagesalience', 'salinityanalogize']
    
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
                    'notes': 'Batch 153 processing',
                    'review_status': 'pending',
                    'batch_number': '153'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 153 processing complete!")
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