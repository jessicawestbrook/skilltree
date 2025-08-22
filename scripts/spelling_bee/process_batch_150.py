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
            'regular': ['ribbon', 'ribs', 'rice', 'rich', 'rifle', 'ringing', 'ripe', 'ripple', 'rise', 'robin', 'rock', 'rocket', 'rodent', 'road', 'roads', 'roast'],
            'semi_regular': ['rialto', 'rico', 'ricochet', 'ricotta', 'riddance', 'ridiculously', 'riffled', 'riffraff', 'rigatoni', 'righteous', 'rigorous', 'rigourous', 'riparian', 'rishik', 'risibility', 'rituals', 'rivalry', 'river', 'riviera', 'robigalia', 'rococo', 'rodeo'],
            'irregular': ['rhyton', 'richter', 'rictus', 'rigueur', 'rinceau', 'risorgimento', 'risposta', 'rissole', 'ritenuto', 'ritziness', 'rocaille']
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
        high_frequency = ['ribbon', 'ribs', 'rice', 'rich', 'rifle', 'ripe', 'rise', 'road', 'roads', 'roast', 'robin', 'rock', 'rocket', 'river', 'rivalry']
        medium_frequency = ['ricochet', 'riddance', 'ridiculously', 'righteous', 'rigorous', 'rigourous', 'ringing', 'ripple', 'rituals', 'riviera', 'rodent', 'rodeo', 'rococo']
        low_frequency = ['rhyton', 'rialto', 'richter', 'rico', 'ricotta', 'rictus', 'riffled', 'riffraff', 'rigatoni', 'rigueur', 'rinceau', 'riparian', 'rishik', 'risibility', 'risorgimento', 'risposta', 'rissole', 'ritenuto', 'ritziness', 'robigalia', 'rocaille']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['ribbon', 'ribs', 'rice', 'rich', 'rifle', 'ripe', 'rise', 'road', 'roads', 'roast', 'robin', 'rock', 'rodent']
        moderate_words = ['rialto', 'rico', 'ricochet', 'ricotta', 'riddance', 'ridiculously', 'riffled', 'riffraff', 'rigatoni', 'righteous', 'rigorous', 'rigourous', 'ringing', 'ripple', 'rituals', 'rivalry', 'river', 'riviera', 'rocket', 'rococo', 'rodeo']
        complex_words = ['rhyton', 'richter', 'rictus', 'rigueur', 'rinceau', 'riparian', 'rishik', 'risibility', 'risorgimento', 'risposta', 'rissole', 'ritenuto', 'ritziness', 'robigalia', 'rocaille']
        
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
        elif 'Italian' in etymology or 'French' in etymology:
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
        'rhyton': {
            'definition': "An ancient Greek drinking vessel, typically in the shape of an animal head or horn; a ceremonial cup used in religious rituals and banquets. Rhytons were often made of precious metals and featured elaborate decorative designs representing gods, animals, or mythological scenes.",
            'pronunciation': "/ˈraɪtɑn/",
            'pronunciation_respelling': "RYE-ton",
            'etymology': "From Greek \"rhyton,\" from \"rhein\" (to flow), referring to liquid flowing from the vessel.",
            'memory_tip': "Think \"rhy\" (flow) + \"ton\" = flowing vessel for drinking.",
            'example_sentence': "The museum displayed a golden ___ shaped like a ram's head from ancient Persia."
        },
        'rialto': {
            'definition': "A marketplace or exchange; a commercial district or trading center; specifically refers to the famous bridge and market area in Venice. The term represents centers of commercial activity and trade.",
            'pronunciation': "/riˈæltoʊ/",
            'pronunciation_respelling': "ree-AL-toh",
            'etymology': "From Italian \"Rialto,\" from \"rivo alto\" (high bank), referring to Venice's commercial district.",
            'memory_tip': "Think \"ri\" (high) + \"alto\" (bank) = high commercial area.",
            'example_sentence': "Merchants gathered at the ___ to conduct their daily business transactions."
        },
        'ribbon': {
            'definition': "A long, narrow strip of fabric used for tying, decorating, or trimming; a strip of material awarded as a prize or honor; any long, thin strip resembling fabric ribbon. Ribbons serve decorative, ceremonial, and practical purposes.",
            'pronunciation': "/ˈrɪbən/",
            'pronunciation_respelling': "RIB-uhn",
            'etymology': "From Old French \"riban,\" possibly from Middle Dutch \"ringband\" (ring band).",
            'memory_tip': "Think of colorful strips tied around gifts or worn as decorations.",
            'example_sentence': "She tied a red ___ around the present to make it look festive."
        },
        'ribs': {
            'definition': "Plural of rib; curved bones forming the cage that protects the chest cavity; the meat from this part of an animal; ridged structures resembling ribs. Ribs provide structural support and protection for vital organs.",
            'pronunciation': "/rɪbz/",
            'pronunciation_respelling': "RIBZ",
            'etymology': "Plural of \"rib,\" from Old English \"ribb,\" of Germanic origin.",
            'memory_tip': "Think of the curved bones protecting your heart and lungs.",
            'example_sentence': "The barbecue restaurant was famous for its tender, smoky ___."
        },
        'rice': {
            'definition': "A cereal grain that is a staple food for billions of people worldwide; the plant that produces this grain; small granular particles resembling rice grains. Rice is cultivated in flooded fields and serves as a primary carbohydrate source.",
            'pronunciation': "/raɪs/",
            'pronunciation_respelling': "RYSE",
            'etymology': "From Old French \"ris,\" from Italian \"riso,\" from Greek \"oryza.\"",
            'memory_tip': "Think of small white grains that expand when cooked with water.",
            'example_sentence': "The chef prepared perfectly steamed ___ to accompany the stir-fried vegetables."
        },
        'rich': {
            'definition': "Having abundant money, property, or valuable possessions; containing large amounts of desirable ingredients; full of color, sound, or other pleasing qualities. Richness implies abundance, luxury, or high quality.",
            'pronunciation': "/rɪtʃ/",
            'pronunciation_respelling': "RICH",
            'etymology': "From Old English \"rice,\" from Germanic \"rikijaz\" (mighty, powerful).",
            'memory_tip': "Think of abundant wealth, flavor, or qualities.",
            'example_sentence': "The chocolate cake was incredibly ___ and decadent."
        },
        'richter': {
            'definition': "Relating to the Richter scale, which measures earthquake magnitude; Charles Francis Richter, the seismologist who developed this scale. The Richter scale quantifies seismic energy release using logarithmic measurements.",
            'pronunciation': "/ˈrɪktər/",
            'pronunciation_respelling': "RIK-tur",
            'etymology': "Named after Charles Francis Richter (1900-1985), American seismologist.",
            'memory_tip': "Think of the scientist who measured earthquake strength.",
            'example_sentence': "The earthquake registered 6.2 on the ___ scale."
        },
        'rico': {
            'definition': "Spanish and Portuguese word meaning \"rich\" or \"wealthy\"; used in place names like Puerto Rico; slang term for a wealthy person. Often appears in geographic names and colloquial expressions.",
            'pronunciation': "/ˈrikoʊ/",
            'pronunciation_respelling': "REE-koh",
            'etymology': "From Spanish/Portuguese \"rico,\" from Latin \"dives\" (rich).",
            'memory_tip': "Think Spanish word for \"rich\" = rico.",
            'example_sentence': "Puerto ___ is known for its beautiful beaches and tropical climate."
        },
        'ricochet': {
            'definition': "A shot or hit that rebounds off a surface; to rebound off a surface after impact; an indirect or unintended consequence of an action. Ricochet involves projectiles changing direction after striking objects.",
            'pronunciation': "/ˈrɪkəˌʃeɪ/",
            'pronunciation_respelling': "RIK-uh-shay",
            'etymology': "From French \"ricochet,\" of uncertain origin, possibly from \"riquer\" (to skip).",
            'memory_tip': "Think of a bullet bouncing off a hard surface.",
            'example_sentence': "The ball hit the wall and took an unexpected ___ toward the window."
        },
        'ricotta': {
            'definition': "A soft, white Italian cheese made from whey; a mild, creamy cheese used in cooking and baking. Ricotta is produced by heating whey leftover from other cheese production.",
            'pronunciation': "/rɪˈkɑtə/",
            'pronunciation_respelling': "ri-KOT-uh",
            'etymology': "From Italian \"ricotta,\" from \"ricuocere\" (to cook again), from Latin \"recoquere.\"",
            'memory_tip': "Think \"ri\" (again) + \"cotta\" (cooked) = cooked again cheese.",
            'example_sentence': "The lasagna recipe called for a mixture of ___ and spinach."
        },
        'rictus': {
            'definition': "A gaping grimace; a fixed, unnatural grin or expression of horror; the gape of an open mouth or beak. Rictus describes facial expressions frozen in unnatural positions, often suggesting death or extreme emotion.",
            'pronunciation': "/ˈrɪktəs/",
            'pronunciation_respelling': "RIK-tuhs",
            'etymology': "From Latin \"rictus,\" from \"ringi\" (to gape), referring to an open mouth.",
            'memory_tip': "Think \"rict\" (gape) + \"us\" = gaping mouth expression.",
            'example_sentence': "The horror mask displayed a terrifying ___ that frightened the children."
        },
        'riddance': {
            'definition': "The action of getting rid of someone or something undesirable; relief from an unwanted person or thing. Riddance implies satisfaction at being free from something troublesome or unpleasant.",
            'pronunciation': "/ˈrɪdəns/",
            'pronunciation_respelling': "RID-uhns",
            'etymology': "From \"rid\" + suffix \"-dance,\" from Old English \"hreddan\" (to rescue).",
            'memory_tip': "Think \"rid\" + \"dance\" = celebration of getting rid of something.",
            'example_sentence': "Good ___ to that noisy neighbor who finally moved away."
        },
        'ridiculously': {
            'definition': "In a manner that invites derision or mockery; to an absurd or unreasonable degree; extremely or excessively. Ridiculously indicates something so extreme it seems worthy of laughter or disbelief.",
            'pronunciation': "/rɪˈdɪkjələsli/",
            'pronunciation_respelling': "ri-DIK-yuh-luhs-lee",
            'etymology': "From \"ridiculous\" + suffix \"-ly,\" from Latin \"ridiculus\" (laughable).",
            'memory_tip': "Think \"ridiculous\" + \"ly\" = in a laughably extreme way.",
            'example_sentence': "The movie tickets were ___ expensive for such poor quality entertainment."
        },
        'riffled': {
            'definition': "Past tense of riffle; shuffled cards by bending and releasing them; searched through quickly; created small waves on water surface. Riffling involves rapid, superficial movement through materials.",
            'pronunciation': "/ˈrɪfəld/",
            'pronunciation_respelling': "RIF-uhld",
            'etymology': "Past tense of \"riffle,\" possibly from \"rifle\" (to search), of uncertain origin.",
            'memory_tip': "Think \"riffle\" + \"d\" = quickly searched through or shuffled.",
            'example_sentence': "She ___ through the papers looking for the important document."
        },
        'riffraff': {
            'definition': "Disreputable or undesirable people; the rabble or common crowd; people regarded as worthless or of low social status. Riffraff is often used dismissively to describe groups considered unworthy or troublesome.",
            'pronunciation': "/ˈrɪfˌræf/",
            'pronunciation_respelling': "RIF-raf",
            'etymology': "From Old French \"rif et raf\" (one and all), meaning everyone including the lowly.",
            'memory_tip': "Think \"riff\" + \"raff\" = rough, undesirable people.",
            'example_sentence': "The exclusive club tried to keep out what they considered ___."
        },
        'riffraffrestive': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'riffraff' + 'restive' incorrectly joined. 'Riffraff' means disreputable people, while 'restive' means restless or impatient. These should be separate words.]",
            'pronunciation': "/ˈrɪfˌræf ˈrestɪv/",
            'pronunciation_respelling': "RIF-raf REST-iv",
            'etymology': "Combined word error: 'riffraff' from Old French + 'restive' from Old French.",
            'memory_tip': "Error combination: riffraff (undesirable people) + restive (restless) - should be separate.",
            'example_sentence': "The ___ crowd became increasingly ___ during the long wait."
        },
        'rifle': {
            'definition': "A firearm with a long spirally grooved barrel for accurate long-distance shooting; to search through hastily and carelessly; to steal. Rifles are designed for precision shooting and hunting.",
            'pronunciation': "/ˈraɪfəl/",
            'pronunciation_respelling': "RYE-fuhl",
            'etymology': "From Old French \"rifler\" (to scrape, file), referring to the grooved barrel.",
            'memory_tip': "Think of grooved barrel for accurate shooting.",
            'example_sentence': "The hunter carried his ___ carefully through the dense forest."
        },
        'rigatoni': {
            'definition': "A type of tube-shaped pasta with ridges on the outside; large, ridged pasta tubes used in Italian cooking. Rigatoni's ridges help hold sauce and its hollow center allows even cooking.",
            'pronunciation': "/ˌrɪɡəˈtoʊni/",
            'pronunciation_respelling': "rig-uh-TOH-nee",
            'etymology': "From Italian \"rigatoni,\" from \"rigato\" (ridged), from \"riga\" (line).",
            'memory_tip': "Think \"rig\" (ridged) + \"atoni\" = ridged tube pasta.",
            'example_sentence': "The chef tossed the ___ with marinara sauce and fresh basil."
        },
        'righteous': {
            'definition': "Morally right or justifiable; acting in accordance with moral principles; characterized by virtue and integrity. Righteous behavior reflects adherence to ethical standards and moral correctness.",
            'pronunciation': "/ˈraɪtʃəs/",
            'pronunciation_respelling': "RYE-chuhs",
            'etymology': "From \"right\" + suffix \"-eous,\" from Old English \"rihtwise\" (rightwise).",
            'memory_tip': "Think \"right\" + \"eous\" = full of rightness/virtue.",
            'example_sentence': "She felt ___ anger at the injustice she witnessed."
        },
        'rigorous': {
            'definition': "Extremely thorough and careful; demanding exact conformity to rules; harsh or severe in application. Rigorous standards require strict adherence and comprehensive attention to detail.",
            'pronunciation': "/ˈrɪɡərəs/",
            'pronunciation_respelling': "RIG-ur-uhs",
            'etymology': "From Latin \"rigorosus,\" from \"rigor\" (stiffness, severity).",
            'memory_tip': "Think \"rigor\" + \"ous\" = full of strict thoroughness.",
            'example_sentence': "The medical school required ___ training and extensive study."
        },
        'rigourous': {
            'definition': "British spelling of rigorous; extremely thorough and careful; demanding exact conformity to rules. This spelling variant is used in British English while American English uses 'rigorous'.",
            'pronunciation': "/ˈrɪɡərəs/",
            'pronunciation_respelling': "RIG-ur-uhs",
            'etymology': "British spelling of \"rigorous,\" from Latin \"rigorosus\" (stiff, severe).",
            'memory_tip': "British spelling: \"rigour\" + \"ous\" = thorough (British style).",
            'example_sentence': "The British university maintained ___ academic standards."
        },
        'rigueur': {
            'definition': "Strictness or severity; rigid adherence to rules or standards; from French meaning strictness. Often used in the phrase \"de rigueur\" meaning required by etiquette or current fashion.",
            'pronunciation': "/rɪˈɡɜr/",
            'pronunciation_respelling': "ri-GUR",
            'etymology': "From French \"rigueur,\" from Latin \"rigor\" (stiffness, severity).",
            'memory_tip': "Think French \"rigour\" = strict adherence to standards.",
            'example_sentence': "Formal attire was de ___ at the diplomatic reception."
        },
        'rinceau': {
            'definition': "A decorative motif consisting of stylized vine or plant scrollwork; an ornamental design featuring intertwining foliage. Rinceaux are common in classical and neoclassical architectural decoration.",
            'pronunciation': "/rɪnˈsoʊ/",
            'pronunciation_respelling': "rin-SOH",
            'etymology': "From French \"rinceau,\" from \"ronce\" (bramble), referring to vine-like decorations.",
            'memory_tip': "Think French \"rince\" (vine) + \"eau\" = vine-like decoration.",
            'example_sentence': "The ceiling featured elaborate ___ patterns of intertwining leaves and vines."
        },
        'ringing': {
            'definition': "Present participle of ring; producing clear, resonant sounds; making telephone calls; encircling something. The ongoing action of creating bell-like sounds or circular movements.",
            'pronunciation': "/ˈrɪŋɪŋ/",
            'pronunciation_respelling': "RING-ing",
            'etymology': "Present participle of \"ring,\" from Old English \"hringan\" (to ring).",
            'memory_tip': "Think \"ring\" + \"ing\" = currently making ringing sounds.",
            'example_sentence': "The church bells were ___ to announce the wedding ceremony."
        },
        'riparian': {
            'definition': "Relating to or situated on the banks of a river; concerning the rights and responsibilities of riverbank property owners. Riparian zones are ecologically important areas where land meets water.",
            'pronunciation': "/raɪˈpɛriən/",
            'pronunciation_respelling': "rye-PAIR-ee-uhn",
            'etymology': "From Latin \"riparius,\" from \"ripa\" (riverbank).",
            'memory_tip': "Think \"ripa\" (riverbank) + \"arian\" = relating to riverbanks.",
            'example_sentence': "The ___ vegetation helps prevent erosion along the river."
        },
        'ripe': {
            'definition': "Fully developed and ready to eat (of fruit); ready for action or development; mature and suitable. Ripeness indicates optimal condition for use, consumption, or action.",
            'pronunciation': "/raɪp/",
            'pronunciation_respelling': "RYEP",
            'etymology': "From Old English \"ripe,\" of Germanic origin, related to \"reap.\"",
            'memory_tip': "Think of fruit at perfect eating condition.",
            'example_sentence': "The tomatoes were perfectly ___ and ready for harvesting."
        },
        'ripple': {
            'definition': "A small wave on the surface of water; a wave-like motion or pattern; to form or cause small waves. Ripples represent gentle, spreading disturbances across surfaces or through materials.",
            'pronunciation': "/ˈrɪpəl/",
            'pronunciation_respelling': "RIP-uhl",
            'etymology': "From Middle English \"riplen,\" possibly related to \"rip\" (to tear).",
            'memory_tip': "Think of small waves spreading across calm water.",
            'example_sentence': "The stone created a gentle ___ across the pond's surface."
        },
        'rise': {
            'definition': "To move upward; to increase in amount, degree, or intensity; to get up from a lying or sitting position; an upward movement or increase. Rise involves elevation, growth, or emergence.",
            'pronunciation': "/raɪz/",
            'pronunciation_respelling': "RYEZ",
            'etymology': "From Old English \"risan,\" of Germanic origin, related to \"rear.\"",
            'memory_tip': "Think of moving upward like the sun rising.",
            'example_sentence': "The bread dough needs time to ___ before baking."
        },
        'rishik': {
            'definition': "A Sanskrit term meaning sage or seer; in Hindu tradition, a person who has attained spiritual insight through meditation and austerity. Rishis are revered as wise teachers and spiritual guides.",
            'pronunciation': "/ˈrɪʃɪk/",
            'pronunciation_respelling': "RISH-ik",
            'etymology': "From Sanskrit \"ṛṣi\" (seer, sage), from \"ṛṣ\" (to flow, move).",
            'memory_tip': "Think Sanskrit sage who flows with spiritual wisdom.",
            'example_sentence': "The ancient ___ taught meditation techniques to his disciples."
        },
        'risibility': {
            'definition': "The ability or inclination to laugh; the quality of provoking laughter; amusement or humor. Risibility relates to both the capacity for laughter and the tendency to find things amusing.",
            'pronunciation': "/ˌrɪzəˈbɪləti/",
            'pronunciation_respelling': "riz-uh-BIL-ih-tee",
            'etymology': "From Latin \"risibilitas,\" from \"risibilis\" (able to laugh), from \"ridere\" (to laugh).",
            'memory_tip': "Think \"ris\" (laugh) + \"ibility\" = ability to laugh.",
            'example_sentence': "His natural ___ made him popular at social gatherings."
        },
        'risorgimento': {
            'definition': "The 19th-century political and social movement that consolidated different states of the Italian peninsula into the single state of Italy; any movement of rebirth or resurgence. The term means \"resurgence\" or \"revival.\"",
            'pronunciation': "/rɪˌzɔrdʒɪˈmentoʊ/",
            'pronunciation_respelling': "ri-zor-ji-MEN-toh",
            'etymology': "From Italian \"risorgimento,\" from \"risorgere\" (to rise again), from Latin \"resurgere.\"",
            'memory_tip': "Think Italian \"ri\" (again) + \"sorgimento\" (rising) = rising again/rebirth.",
            'example_sentence': "The ___ unified Italy under a single government in the 1860s."
        },
        'risposta': {
            'definition': "An Italian musical term meaning \"response\" or \"answer\"; in fugues, the second voice's restatement of the main theme. Risposta represents the answering voice that follows the initial musical statement.",
            'pronunciation': "/rɪˈspoʊstə/",
            'pronunciation_respelling': "ri-SPOH-stuh",
            'etymology': "From Italian \"risposta,\" from \"rispondere\" (to respond), from Latin \"respondere.\"",
            'memory_tip': "Think Italian \"ri\" (back) + \"sposta\" (place) = musical answer.",
            'example_sentence': "The fugue's ___ entered in the dominant key as tradition dictates."
        },
        'rissole': {
            'definition': "A small fried cake or ball of minced meat, fish, or vegetables; a type of pastry filled with meat or vegetables. Rissoles are popular in European cuisine and can be fried or baked.",
            'pronunciation': "/ˈrɪsoʊl/",
            'pronunciation_respelling': "RIS-ohl",
            'etymology': "From French \"rissole,\" from Old French \"roussole,\" from \"rousser\" (to redden).",
            'memory_tip': "Think French \"ris\" + \"sole\" = fried cake that gets reddened.",
            'example_sentence': "The chef prepared delicious potato and herb ___ for the appetizer course."
        },
        'ritenuto': {
            'definition': "A musical term meaning \"held back\" or \"becoming gradually slower\"; indicates a gradual decrease in tempo. Ritenuto is used to create expressive effects in musical performance.",
            'pronunciation': "/ˌrɪtəˈnutoʊ/",
            'pronunciation_respelling': "rit-uh-NOO-toh",
            'etymology': "From Italian \"ritenuto,\" past participle of \"ritenere\" (to hold back).",
            'memory_tip': "Think Italian \"ri\" (back) + \"tenuto\" (held) = held back in tempo.",
            'example_sentence': "The pianist played the final phrase ___ to create a dramatic ending."
        },
        'rituals': {
            'definition': "Plural of ritual; religious or ceremonial acts performed according to prescribed order; habitual or customary activities. Rituals provide structure, meaning, and continuity to cultural and personal practices.",
            'pronunciation': "/ˈrɪtʃuəlz/",
            'pronunciation_respelling': "RICH-oo-uhlz",
            'etymology': "Plural of \"ritual,\" from Latin \"ritualis,\" from \"ritus\" (religious ceremony).",
            'memory_tip': "Think \"rit\" (rite) + \"uals\" = ceremonial practices.",
            'example_sentence': "The wedding included both traditional and modern ___."
        },
        'ritziness': {
            'definition': "The quality of being ritzy; pretentious elegance or luxury; ostentatious sophistication. Ritziness implies expensive taste displayed in a showy or pretentious manner.",
            'pronunciation': "/ˈrɪtsɪnəs/",
            'pronunciation_respelling': "RIT-see-nuhs",
            'etymology': "From \"ritzy\" (after the Ritz hotels) + suffix \"-ness,\" meaning luxury quality.",
            'memory_tip': "Think \"Ritz\" (luxury hotel) + \"iness\" = quality of luxury.",
            'example_sentence': "The restaurant's ___ made it popular with wealthy celebrities."
        },
        'rivalry': {
            'definition': "Competition for the same objective or for superiority in the same field; the state of being rivals; ongoing competition between equals. Rivalry involves sustained competitive relationships.",
            'pronunciation': "/ˈraɪvəlri/",
            'pronunciation_respelling': "RYE-vuhl-ree",
            'etymology': "From \"rival\" + suffix \"-ry,\" from Latin \"rivalis\" (using the same stream).",
            'memory_tip': "Think \"rival\" + \"ry\" = competitive relationship.",
            'example_sentence': "The intense ___ between the two schools made the game exciting."
        },
        'river': {
            'definition': "A large natural stream of water flowing toward an ocean, sea, lake, or another river; a copious flow of something. Rivers are important geographical features that shape landscapes and provide water resources.",
            'pronunciation': "/ˈrɪvər/",
            'pronunciation_respelling': "RIV-ur",
            'etymology': "From Old French \"riviere,\" from Latin \"riparia\" (of a riverbank).",
            'memory_tip': "Think of water flowing continuously toward the sea.",
            'example_sentence': "The Amazon ___ is the longest waterway in the world."
        },
        'riviera': {
            'definition': "A coastal region with a subtropical climate and vegetation; specifically the Mediterranean coastal areas of France and Italy. Riviera suggests luxury resorts and pleasant coastal living.",
            'pronunciation': "/ˌrɪviˈɛrə/",
            'pronunciation_respelling': "riv-ee-AIR-uh",
            'etymology': "From Italian \"riviera,\" from \"riva\" (shore), from Latin \"ripa\" (riverbank).",
            'memory_tip': "Think Italian \"riva\" (shore) = beautiful coastal area.",
            'example_sentence': "The French ___ attracts tourists with its glamorous beaches and resorts."
        },
        'road': {
            'definition': "A paved way for vehicles, pedestrians, and animals; a route or path between places; a way forward toward achieving something. Roads provide transportation infrastructure connecting communities.",
            'pronunciation': "/roʊd/",
            'pronunciation_respelling': "ROHD",
            'etymology': "From Old English \"rad\" (ride, journey), from Germanic \"raido.\"",
            'memory_tip': "Think of paved path for traveling between places.",
            'example_sentence': "The winding ___ through the mountains offered spectacular views."
        },
        'roads': {
            'definition': "Plural of road; paved ways for vehicles and pedestrians; routes connecting different locations; systems of transportation infrastructure. Roads form networks that enable commerce and communication.",
            'pronunciation': "/roʊdz/",
            'pronunciation_respelling': "ROHDZ",
            'etymology': "Plural of \"road,\" from Old English \"rad\" (ride, journey).",
            'memory_tip': "Think \"road\" + \"s\" = multiple transportation routes.",
            'example_sentence': "The city's ___ were congested during rush hour traffic."
        },
        'roast': {
            'definition': "To cook food with dry heat in an oven; to criticize harshly or mock publicly; meat cooked by roasting. Roasting involves high-temperature cooking that creates browning and concentrated flavors.",
            'pronunciation': "/roʊst/",
            'pronunciation_respelling': "ROHST",
            'etymology': "From Old French \"rostir,\" of Germanic origin, related to \"rust.\"",
            'memory_tip': "Think of cooking meat in dry heat until browned.",
            'example_sentence': "The chef decided to ___ the chicken with herbs and vegetables."
        },
        'robigalia': {
            'definition': "An ancient Roman festival held on April 25th to protect crops from blight and disease; ceremonies to honor Robigus, god of grain rust. This agricultural festival sought divine protection for harvests.",
            'pronunciation': "/ˌroʊbɪˈɡeɪliə/",
            'pronunciation_respelling': "roh-bi-GAY-lee-uh",
            'etymology': "From Latin \"Robigalia,\" from \"Robigus\" (god of grain rust) + festival suffix \"-alia.\"",
            'memory_tip': "Think \"Robig\" (rust god) + \"alia\" (festival) = festival against crop rust.",
            'example_sentence': "Ancient Romans celebrated ___ to ensure healthy grain harvests."
        },
        'robin': {
            'definition': "A small songbird with a red breast; a familiar garden bird known for its melodic song and territorial behavior. Robins are often considered harbingers of spring in many cultures.",
            'pronunciation': "/ˈrɑbɪn/",
            'pronunciation_respelling': "ROB-in",
            'etymology': "From Old French \"robin,\" diminutive of \"Robert,\" used as a familiar name for the bird.",
            'memory_tip': "Think of small red-breasted bird that signals spring.",
            'example_sentence': "The ___ built its nest in the apple tree outside the kitchen window."
        },
        'rocaille': {
            'definition': "An 18th-century decorative style featuring elaborate ornamentation with shells, pebbles, and artificial rock work; shell work or pebble work used in garden grottos. Rocaille influenced the development of Rococo style.",
            'pronunciation': "/roʊˈkaɪ/",
            'pronunciation_respelling': "roh-KYE",
            'etymology': "From French \"rocaille,\" from \"roc\" (rock) + suffix \"-aille\" (collection of).",
            'memory_tip': "Think French \"roc\" (rock) + \"aille\" = decorative rockwork.",
            'example_sentence': "The garden grotto featured intricate ___ decorations with shells and stones."
        },
        'rock': {
            'definition': "Hard mineral matter forming part of the earth's surface; a large mass of stone; to move back and forth; a style of popular music. Rock represents both geological formations and rhythmic movement.",
            'pronunciation': "/rɑk/",
            'pronunciation_respelling': "RAHK",
            'etymology': "From Old English \"rocc,\" from Old Norse \"rokkr\" (distaff).",
            'memory_tip': "Think of hard stone or back-and-forth motion.",
            'example_sentence': "The lighthouse was built on a solid ___ foundation."
        },
        'rocket': {
            'definition': "A vehicle propelled by jet engines; a projectile weapon; a plant with edible leaves; to increase rapidly. Rockets use combustion or other propulsion methods to achieve flight or rapid motion.",
            'pronunciation': "/ˈrɑkɪt/",
            'pronunciation_respelling': "ROK-it",
            'etymology': "From Italian \"rocchetta,\" diminutive of \"rocca\" (distaff), referring to shape.",
            'memory_tip': "Think of projectile shooting rapidly upward.",
            'example_sentence': "The space ___ launched successfully carrying supplies to the space station."
        },
        'rococo': {
            'definition': "An 18th-century artistic style characterized by elaborate ornamentation and pastel colors; ornate and florid in style; excessively ornamental. Rococo developed from and reacted against Baroque formality.",
            'pronunciation': "/rəˈkoʊkoʊ/",
            'pronunciation_respelling': "ruh-KOH-koh",
            'etymology': "From French \"rococo,\" from \"rocaille\" (shell work) + \"coquille\" (shell).",
            'memory_tip': "Think \"roc\" (rock) + \"coco\" (shell) = elaborate decorative style.",
            'example_sentence': "The palace interior exemplified ___ style with its gilded mirrors and delicate pastels."
        },
        'rodent': {
            'definition': "A mammal characterized by continuously growing front teeth used for gnawing; includes mice, rats, squirrels, and beavers. Rodents comprise the largest order of mammals.",
            'pronunciation': "/ˈroʊdənt/",
            'pronunciation_respelling': "ROH-duhnt",
            'etymology': "From Latin \"rodens,\" from \"rodere\" (to gnaw).",
            'memory_tip': "Think \"rod\" (gnaw) + \"ent\" = gnawing animal.",
            'example_sentence': "The scientist studied the behavior of various ___ species in the laboratory."
        },
        'rodeo': {
            'definition': "A competitive event featuring cowboys and cowgirls in various riding and roping competitions; a gathering or exhibition. Rodeos showcase traditional ranching skills in competitive format.",
            'pronunciation': "/ˈroʊdiˌoʊ/",
            'pronunciation_respelling': "ROH-dee-oh",
            'etymology': "From Spanish \"rodeo,\" from \"rodear\" (to encircle), from Latin \"rotare\" (to rotate).",
            'memory_tip': "Think Spanish \"rodear\" (encircle) = encircling cattle.",
            'example_sentence': "The annual ___ featured bull riding and barrel racing competitions."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_150_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_150_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['riffraffrestive']
    
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
                    'notes': 'Batch 150 processing',
                    'review_status': 'pending',
                    'batch_number': '150'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 150 processing complete!")
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