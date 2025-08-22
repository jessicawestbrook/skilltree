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
            'regular': ['restaurants', 'resting', 'results', 'retina', 'retorts', 'retreat', 'return', 'reunion', 'reveal', 'revolution', 'revved', 'rhythmic'],
            'semi_regular': ['restitutory', 'restive', 'resuscitate', 'reticulated', 'reticule', 'retinitis', 'retinol', 'retriever', 'retroactive', 'retrograde', 'retribution', 'revelation', 'revenant', 'reverberant', 'revulsive', 'rhapsody', 'rhetorical', 'rheumatic', 'rhinestone', 'rhombus', 'rhubarb', 'rhythmically'],
            'irregular': ['retinoscopy', 'retrocedence', 'retrodict', 'revanche', 'reveille', 'revendicate', 'revoir', 'reykjavík', 'reynard', 'rhabdoid', 'rheostat', 'rhinorrhagia', 'rhizome', 'rhododendron']
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
        high_frequency = ['restaurants', 'resting', 'results', 'retreat', 'return', 'reunion', 'reveal', 'revolution', 'retina', 'rhythmic']
        medium_frequency = ['restive', 'resuscitate', 'retriever', 'retroactive', 'revelation', 'retorts', 'retribution', 'revved', 'rhetorical', 'rheumatic', 'rhombus', 'rhubarb', 'rhythmically']
        low_frequency = ['restitutory', 'reticulated', 'reticule', 'retinitis', 'retinol', 'retinoscopy', 'retrocedence', 'retrodict', 'retrograde', 'revanche', 'reveille', 'revenant', 'revendicate', 'reverberant', 'revoir', 'revulsive', 'reykjavík', 'reynard', 'rhabdoid', 'rhapsody', 'rheostat', 'rhinestone', 'rhinorrhagia', 'rhizome', 'rhododendron']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['restaurants', 'resting', 'results', 'retina', 'retorts', 'retreat', 'return', 'reunion', 'reveal', 'revved', 'rhombus', 'rhubarb', 'rhythmic']
        moderate_words = ['restive', 'resuscitate', 'reticulated', 'reticule', 'retinitis', 'retinol', 'retriever', 'retroactive', 'retribution', 'revelation', 'revenant', 'reverberant', 'revolution', 'revulsive', 'rhapsody', 'rhetorical', 'rheumatic', 'rhinestone', 'rhythmically']
        complex_words = ['restitutory', 'retinoscopy', 'retrocedence', 'retrodict', 'retrograde', 'revanche', 'reveille', 'revendicate', 'revoir', 'reykjavík', 'reynard', 'rhabdoid', 'rheostat', 'rhinorrhagia', 'rhizome', 'rhododendron']
        
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
        'restaurants': {
            'definition': "Plural of restaurant; businesses that prepare and serve food and drinks to customers; eating establishments where meals are cooked and served to paying customers. Restaurants provide dining services in commercial settings for the public.",
            'pronunciation': "/ˈrestərənts/",
            'pronunciation_respelling': "RES-tur-uhnts",
            'etymology': "Plural of \"restaurant,\" from French \"restaurant,\" from \"restaurer\" (to restore).",
            'memory_tip': "Think \"restaurant\" + \"s\" = multiple eating establishments.",
            'example_sentence': "The food critic reviewed several ___ in the downtown district."
        },
        'resting': {
            'definition': "Present participle of rest; ceasing work or movement to relax or recover strength; lying down or being in a state of repose. The ongoing action of taking rest or remaining in a peaceful state.",
            'pronunciation': "/ˈrestɪŋ/",
            'pronunciation_respelling': "REST-ing",
            'etymology': "Present participle of \"rest,\" from Old English \"rest,\" of Germanic origin.",
            'memory_tip': "Think \"rest\" + \"ing\" = currently taking rest.",
            'example_sentence': "The exhausted hikers were ___ beside the mountain stream."
        },
        'restitutory': {
            'definition': "Relating to or characterized by restitution; involving the restoration of something lost or stolen to its proper owner; aimed at making compensation for loss or damage. Restitutory actions seek to restore previous conditions.",
            'pronunciation': "/rɪˈstɪtjəˌtɔri/",
            'pronunciation_respelling': "ri-STIT-yuh-tor-ee",
            'etymology': "From Latin \"restitutus\" (restored) + suffix \"-ory,\" from \"restituere\" (to restore).",
            'memory_tip': "Think \"restitute\" + \"ory\" = relating to restoring things.",
            'example_sentence': "The court ordered ___ damages to compensate the victims."
        },
        'restive': {
            'definition': "Unable to remain still; restless or impatient; refusing to be controlled or subdued. Restive behavior involves resistance to restraint and difficulty remaining calm or stationary, often due to frustration or anxiety.",
            'pronunciation': "/ˈrestɪv/",
            'pronunciation_respelling': "REST-iv",
            'etymology': "From Old French \"restif,\" from \"rester\" (to remain), ironically meaning the opposite.",
            'memory_tip': "Think \"rest\" + \"ive\" but ironically means can't rest = restless.",
            'example_sentence': "The horse became ___ when kept in the stable too long."
        },
        'results': {
            'definition': "Plural of result; consequences or outcomes of actions, processes, or events; findings from tests, experiments, or investigations. Results represent the final products or effects of various activities or procedures.",
            'pronunciation': "/rɪˈzʌlts/",
            'pronunciation_respelling': "ri-ZUHLTS",
            'etymology': "Plural of \"result,\" from Latin \"resultare\" (to rebound), from \"re-\" (back) + \"saltare\" (to leap).",
            'memory_tip': "Think \"re-\" (back) + \"sults\" (leaps) = what leaps back as consequences.",
            'example_sentence': "The laboratory ___ confirmed the presence of the rare mineral."
        },
        'resuscitate': {
            'definition': "To revive someone from unconsciousness or apparent death; to restore life or consciousness; to bring back to life or activity. Resuscitation involves medical procedures to restore breathing, heartbeat, or consciousness.",
            'pronunciation': "/rɪˈsʌsəˌteɪt/",
            'pronunciation_respelling': "ri-SUHS-uh-tayt",
            'etymology': "From Latin \"resuscitare,\" from \"re-\" (again) + \"suscitare\" (to raise up).",
            'memory_tip': "Think \"re-\" (again) + \"suscitate\" (raise up) = raise up to life again.",
            'example_sentence': "The paramedics worked frantically to ___ the drowning victim."
        },
        'resuscitateretina': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'resuscitate' + 'retina' incorrectly joined. 'Resuscitate' means to revive from unconsciousness, while 'retina' is the light-sensitive layer of the eye. These should be separate words.]",
            'pronunciation': "/rɪˈsʌsəˌteɪt ˈretənə/",
            'pronunciation_respelling': "ri-SUHS-uh-tayt RET-ih-nuh",
            'etymology': "Combined word error: 'resuscitate' from Latin + 'retina' from Latin.",
            'memory_tip': "Error combination: resuscitate (revive) + retina (eye part) - should be separate.",
            'example_sentence': "Doctors attempted to ___ the patient while examining damage to the ___."
        },
        'reticulated': {
            'definition': "Constructed, arranged, or marked like a net; having a pattern of interlacing lines resembling a network. Reticulated structures feature systematic interconnected patterns commonly found in nature and engineering.",
            'pronunciation': "/rɪˈtɪkjəˌleɪtɪd/",
            'pronunciation_respelling': "ri-TIK-yuh-lay-tid",
            'etymology': "From Latin \"reticulatus,\" from \"reticulum\" (little net), from \"rete\" (net).",
            'memory_tip': "Think \"retic\" (net) + \"ulated\" = arranged like a net pattern.",
            'example_sentence': "The leaf showed a beautiful ___ pattern of veins."
        },
        'reticule': {
            'definition': "A woman's small handbag or purse, typically having a drawstring and made of soft material; a small bag carried by women in the 18th and 19th centuries. Reticules were fashionable accessories for carrying personal items.",
            'pronunciation': "/ˈretɪˌkjul/",
            'pronunciation_respelling': "RET-ih-kyool",
            'etymology': "From French \"réticule,\" from Latin \"reticulum\" (little net).",
            'memory_tip': "Think \"retic\" (net) + \"ule\" = small net-like bag.",
            'example_sentence': "The Victorian lady carried her coins in an embroidered ___."
        },
        'retina': {
            'definition': "The light-sensitive layer of tissue at the back of the inner eye; contains photoreceptor cells that convert light into electrical signals sent to the brain. The retina is essential for vision and image formation.",
            'pronunciation': "/ˈretənə/",
            'pronunciation_respelling': "RET-ih-nuh",
            'etymology': "From Latin \"retina,\" from \"rete\" (net), referring to its network-like appearance.",
            'memory_tip': "Think \"ret\" (net) + \"ina\" = net-like layer in the eye.",
            'example_sentence': "The ophthalmologist examined the ___ for signs of damage."
        },
        'retinitis': {
            'definition': "Inflammation of the retina; a medical condition affecting the light-sensitive tissue at the back of the eye. Retinitis can cause vision problems and may result from infections, autoimmune conditions, or other factors.",
            'pronunciation': "/ˌretəˈnaɪtɪs/",
            'pronunciation_respelling': "ret-ih-NYE-tis",
            'etymology': "From \"retina\" + suffix \"-itis\" (inflammation), from Latin \"rete\" (net).",
            'memory_tip': "Think \"retina\" + \"itis\" (inflammation) = inflammation of the retina.",
            'example_sentence': "The patient was diagnosed with ___ and prescribed anti-inflammatory medication."
        },
        'retinol': {
            'definition': "Vitamin A in its pure form; a fat-soluble vitamin essential for vision, immune function, and cell growth. Retinol is commonly used in skincare products for its anti-aging properties and ability to promote cell turnover.",
            'pronunciation': "/ˈretəˌnɔl/",
            'pronunciation_respelling': "RET-ih-nol",
            'etymology': "From \"retina\" + suffix \"-ol\" (alcohol), referring to its importance for retinal function.",
            'memory_tip': "Think \"retin\" (retina) + \"ol\" = vitamin important for retina/vision.",
            'example_sentence': "The dermatologist recommended a cream containing ___ for anti-aging benefits."
        },
        'retinoscopy': {
            'definition': "An objective method of determining refractive errors of the eye; a medical procedure using a retinoscope to assess how light reflects from the retina. Retinoscopy helps eye care professionals prescribe corrective lenses.",
            'pronunciation': "/ˌretəˈnɑskəpi/",
            'pronunciation_respelling': "ret-ih-NOS-kuh-pee",
            'etymology': "From \"retina\" + Greek \"skopein\" (to look at), literally \"looking at the retina.\"",
            'memory_tip': "Think \"retino\" (retina) + \"scopy\" (looking) = looking at the retina.",
            'example_sentence': "The optometrist performed ___ to determine the patient's prescription."
        },
        'retorts': {
            'definition': "Plural of retort; sharp, angry, or witty replies; glass vessels with long necks used in distillation; quick responses to criticism or questions. Retorts can be verbal comebacks or laboratory equipment.",
            'pronunciation': "/rɪˈtɔrts/",
            'pronunciation_respelling': "ri-TORTS",
            'etymology': "Plural of \"retort,\" from Latin \"retortus\" (twisted back), from \"retorquere.\"",
            'memory_tip': "Think \"re-\" (back) + \"torts\" (twisted) = twisted back responses.",
            'example_sentence': "Her clever ___ to the critic's comments impressed the audience."
        },
        'retreat': {
            'definition': "To move back or withdraw from a difficult situation; a quiet place for rest or spiritual renewal; the act of withdrawing from advancing enemy forces. Retreat involves strategic withdrawal or peaceful withdrawal for restoration.",
            'pronunciation': "/rɪˈtrit/",
            'pronunciation_respelling': "ri-TREET",
            'etymology': "From Old French \"retraite,\" from \"retraire\" (to withdraw), from Latin \"retrahere.\"",
            'memory_tip': "Think \"re-\" (back) + \"treat\" (go) = go back/withdraw.",
            'example_sentence': "The army was forced to ___ after facing overwhelming opposition."
        },
        'retribution': {
            'definition': "Punishment inflicted on someone as vengeance for wrongdoing; deserved punishment for evil done; divine or morally justified payback. Retribution involves consequences that match the severity of wrongdoing.",
            'pronunciation': "/ˌretrəˈbjuʃən/",
            'pronunciation_respelling': "ret-ruh-BYOO-shuhn",
            'etymology': "From Latin \"retributio,\" from \"retribuere\" (to pay back), from \"re-\" (back) + \"tribuere\" (to assign).",
            'memory_tip': "Think \"re-\" (back) + \"tribution\" (giving) = giving back punishment.",
            'example_sentence': "The villain's cruel actions eventually brought swift ___."
        },
        'retriever': {
            'definition': "A dog trained to retrieve shot game; a breed of dog known for its ability to fetch objects; something or someone that retrieves. Retrievers are characterized by their gentle mouths and swimming ability.",
            'pronunciation': "/rɪˈtrivər/",
            'pronunciation_respelling': "ri-TREE-vur",
            'etymology': "From \"retrieve\" + suffix \"-er\" (one who), from Old French \"retrover\" (to find again).",
            'memory_tip': "Think \"retrieve\" + \"er\" = one who retrieves things.",
            'example_sentence': "The golden ___ fetched the duck from the cold lake water."
        },
        'retroactive': {
            'definition': "Taking effect from a date in the past; applying to situations that occurred before the law or decision was made. Retroactive measures affect previous events or circumstances as if the new rule had always existed.",
            'pronunciation': "/ˌretroʊˈæktɪv/",
            'pronunciation_respelling': "ret-roh-AK-tiv",
            'etymology': "From \"retro-\" (backward) + \"active,\" from Latin \"retro\" (backward) + \"activus\" (active).",
            'memory_tip': "Think \"retro\" (backward) + \"active\" = actively applying backward in time.",
            'example_sentence': "The pay raise was ___, so employees received back pay for six months."
        },
        'retrocedence': {
            'definition': "The action of going back or retreating; a recession or withdrawal; the act of yielding or surrendering territory or rights. Retrocedence involves moving backward or giving up previously held positions.",
            'pronunciation': "/ˌretroʊˈsidəns/",
            'pronunciation_respelling': "ret-roh-SEED-uhns",
            'etymology': "From Latin \"retrocedere,\" from \"retro-\" (backward) + \"cedere\" (to go).",
            'memory_tip': "Think \"retro\" (backward) + \"cedence\" (going) = going backward.",
            'example_sentence': "The treaty included provisions for the ___ of disputed territories."
        },
        'retrodict': {
            'definition': "To use present knowledge to infer or explain past events; to work backward from current evidence to understand previous occurrences. Retrodiction is the opposite of prediction, explaining the past rather than forecasting the future.",
            'pronunciation': "/ˈretroʊˌdɪkt/",
            'pronunciation_respelling': "RET-roh-dikt",
            'etymology': "From \"retro-\" (backward) + \"dict\" (speak), from Latin \"retro\" + \"dicere\" (to say).",
            'memory_tip': "Think \"retro\" (backward) + \"dict\" (speak) = speak about the past.",
            'example_sentence': "Scientists used geological evidence to ___ the ancient climate patterns."
        },
        'retrograde': {
            'definition': "Directed or moving backward; returning to an earlier and typically worse condition; relating to orbital motion opposite to normal direction. Retrograde suggests regression or movement contrary to expected progress.",
            'pronunciation': "/ˈretroʊˌɡreɪd/",
            'pronunciation_respelling': "RET-roh-grayd",
            'etymology': "From Latin \"retrogradus,\" from \"retro-\" (backward) + \"gradi\" (to step).",
            'memory_tip': "Think \"retro\" (backward) + \"grade\" (step) = stepping backward.",
            'example_sentence': "The planet appeared to move in ___ motion against the background stars."
        },
        'return': {
            'definition': "To come or go back to a place, person, or condition; to give, put, or send something back; the action of coming back. Return involves movement back to a previous location, state, or person.",
            'pronunciation': "/rɪˈtɜrn/",
            'pronunciation_respelling': "ri-TURN",
            'etymology': "From Old French \"retorner,\" from \"re-\" (back) + \"torner\" (to turn).",
            'memory_tip': "Think \"re-\" (back) + \"turn\" = turn back to where you came from.",
            'example_sentence': "She promised to ___ home before midnight."
        },
        'reunion': {
            'definition': "An instance of people coming together again after being separated; a social gathering of people who have not seen each other for some time. Reunions celebrate renewed connections and shared memories.",
            'pronunciation': "/riˈjunjən/",
            'pronunciation_respelling': "ree-YOON-yuhn",
            'etymology': "From \"re-\" (again) + \"union,\" from Latin \"unio\" (unity).",
            'memory_tip': "Think \"re-\" (again) + \"union\" = joining together again.",
            'example_sentence': "The family ___ brought together relatives from across the country."
        },
        'revanche': {
            'definition': "The policy of seeking to retaliate or recover lost territory; revenge or retaliation, especially in international relations. Revanche involves systematic efforts to regain power, territory, or status after defeat.",
            'pronunciation': "/rəˈvɑnʃ/",
            'pronunciation_respelling': "ruh-VAHNSH",
            'etymology': "From French \"revanche,\" from \"revancher\" (to revenge), from \"re-\" (again) + \"venger\" (to avenge).",
            'memory_tip': "Think French \"re-\" (again) + \"vanche\" (revenge) = seeking revenge again.",
            'example_sentence': "The nation's ___ policy aimed to reclaim territories lost in the previous war."
        },
        'reveal': {
            'definition': "To make previously hidden or secret information known; to show or display something previously concealed; to disclose or unveil. Revelation involves bringing hidden things into the open or making them visible.",
            'pronunciation': "/rɪˈvil/",
            'pronunciation_respelling': "ri-VEEL",
            'etymology': "From Old French \"reveler,\" from Latin \"revelare,\" from \"re-\" (back) + \"velare\" (to veil).",
            'memory_tip': "Think \"re-\" (back) + \"veal\" (veil) = pull back the veil.",
            'example_sentence': "The investigation will ___ the truth about the corruption scandal."
        },
        'reveille': {
            'definition': "A signal sounded especially on a bugle or drum to wake military personnel in the morning; the time at which this signal is sounded. Reveille marks the official start of the military day.",
            'pronunciation': "/ˈrevəli/",
            'pronunciation_respelling': "REV-uh-lee",
            'etymology': "From French \"réveillez,\" imperative of \"réveiller\" (to wake up), from \"re-\" + \"veiller\" (to watch).",
            'memory_tip': "Think French \"re-\" + \"veille\" (wake) = wake up call.",
            'example_sentence': "The soldiers assembled for morning formation after ___."
        },
        'revelation': {
            'definition': "A surprising disclosure of information; the divine or supernatural disclosure of truth; an enlightening or astonishing realization. Revelations provide new understanding or expose previously unknown information.",
            'pronunciation': "/ˌrevəˈleɪʃən/",
            'pronunciation_respelling': "rev-uh-LAY-shuhn",
            'etymology': "From Latin \"revelatio,\" from \"revelare\" (to unveil), from \"re-\" (back) + \"velare\" (to veil).",
            'memory_tip': "Think \"reveal\" + \"ation\" = action of revealing/unveiling truth.",
            'example_sentence': "The documents contained a shocking ___ about the company's finances."
        },
        'revelationarithmetic': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'revelation' + 'arithmetic' incorrectly joined. 'Revelation' means a surprising disclosure, while 'arithmetic' refers to basic mathematics. These should be separate words.]",
            'pronunciation': "/ˌrevəˈleɪʃən əˈrɪθmətɪk/",
            'pronunciation_respelling': "rev-uh-LAY-shuhn uh-RITH-muh-tik",
            'etymology': "Combined word error: 'revelation' from Latin + 'arithmetic' from Greek.",
            'memory_tip': "Error combination: revelation (disclosure) + arithmetic (math) - should be separate.",
            'example_sentence': "The ___ about the budget involved complex ___ calculations."
        },
        'revenant': {
            'definition': "A person who has returned from the dead; a ghost or spirit that returns to the world of the living; someone who returns after a long absence. Revenants appear in folklore and supernatural literature.",
            'pronunciation': "/ˈrevənənt/",
            'pronunciation_respelling': "REV-uh-nuhnt",
            'etymology': "From French \"revenant,\" from \"revenir\" (to return), from Latin \"revenire.\"",
            'memory_tip': "Think \"reven\" (return) + \"ant\" = one who returns from death.",
            'example_sentence': "The horror story featured a ___ seeking revenge against his murderers."
        },
        'revendicate': {
            'definition': "To claim back; to demand the return of something; to assert a right to something previously owned. Revendication involves legal or formal claims to recover property or rights.",
            'pronunciation': "/rɪˈvendɪˌkeɪt/",
            'pronunciation_respelling': "ri-VEN-dih-kayt",
            'etymology': "From Latin \"revendicare,\" from \"re-\" (back) + \"vindicare\" (to claim).",
            'memory_tip': "Think \"re-\" (back) + \"vindicate\" (claim) = claim back.",
            'example_sentence': "The family sought to ___ their ancestral lands from the government."
        },
        'reverberant': {
            'definition': "Characterized by reverberation; echoing or resounding; producing or capable of producing echoes. Reverberant spaces have acoustic properties that cause sounds to reflect and persist.",
            'pronunciation': "/rɪˈvɜrbərənt/",
            'pronunciation_respelling': "ri-VUR-bur-uhnt",
            'etymology': "From Latin \"reverberare\" (to beat back), from \"re-\" (back) + \"verberare\" (to beat).",
            'memory_tip': "Think \"re-\" (back) + \"verberant\" (beating) = beating back sound waves.",
            'example_sentence': "The cathedral's ___ acoustics made every whisper audible."
        },
        'revoir': {
            'definition': "French term meaning \"to see again\"; commonly used in \"au revoir\" (goodbye, until we see again); a farewell with expectation of future meeting. Used in English contexts referencing French farewells.",
            'pronunciation': "/rəˈvwɑr/",
            'pronunciation_respelling': "ruh-VWAR",
            'etymology': "From French \"revoir,\" from \"re-\" (again) + \"voir\" (to see).",
            'memory_tip': "Think French \"re-\" (again) + \"voir\" (see) = see again.",
            'example_sentence': "She bid him ___ with the hope of meeting again soon."
        },
        'revolution': {
            'definition': "A forcible overthrow of a government or social order; a dramatic and wide-reaching change; a single complete turn around an axis. Revolution can be political transformation or physical rotation.",
            'pronunciation': "/ˌrevəˈluʃən/",
            'pronunciation_respelling': "rev-uh-LOO-shuhn",
            'etymology': "From Latin \"revolutio,\" from \"revolvere\" (to roll back), from \"re-\" (back) + \"volvere\" (to roll).",
            'memory_tip': "Think \"re-\" (back) + \"volution\" (rolling) = rolling back to create change.",
            'example_sentence': "The industrial ___ transformed manufacturing and society."
        },
        'revulsive': {
            'definition': "Causing a strong feeling of disgust or repugnance; having the power to repel; in medicine, causing revulsion or diversion of disease. Revulsive things provoke aversion or withdrawal reactions.",
            'pronunciation': "/rɪˈvʌlsɪv/",
            'pronunciation_respelling': "ri-VUHL-siv",
            'etymology': "From Latin \"revulsus,\" from \"revellere\" (to tear away), from \"re-\" (away) + \"vellere\" (to pull).",
            'memory_tip': "Think \"re-\" (away) + \"vulsive\" (pulling) = pulling away in disgust.",
            'example_sentence': "The patient had a ___ reaction to the bitter medicine."
        },
        'revved': {
            'definition': "Past tense of rev; increased the speed of an engine; accelerated; made more active or intense. Revving involves increasing engine RPMs or intensifying activity.",
            'pronunciation': "/revd/",
            'pronunciation_respelling': "REVD",
            'etymology': "Past tense of \"rev,\" short for \"revolution\" (of an engine).",
            'memory_tip': "Think \"rev\" (revolution of engine) + \"ed\" = engine was accelerated.",
            'example_sentence': "He ___ the motorcycle engine before racing down the track."
        },
        'reykjavík': {
            'definition': "The capital and largest city of Iceland; located on the southwestern coast of Iceland. Reykjavík is known for its cultural attractions, geothermal energy, and as a center of Icelandic government and commerce.",
            'pronunciation': "/ˈreɪkjəˌvɪk/",
            'pronunciation_respelling': "RAYK-yuh-vik",
            'etymology': "From Icelandic, literally \"smoky bay,\" from \"reykur\" (smoke) + \"vík\" (bay).",
            'memory_tip': "Think \"reyk\" (smoke) + \"javik\" (bay) = smoky bay city.",
            'example_sentence': "___ serves as Iceland's political and cultural center."
        },
        'reynard': {
            'definition': "A name for a fox, especially in medieval literature and fables; refers to the cunning fox character in European folklore. Reynard represents cleverness, trickery, and wit in traditional stories.",
            'pronunciation': "/ˈreɪnərd/",
            'pronunciation_respelling': "RAY-nurd",
            'etymology': "From Old French \"Renart,\" a proper name used for the fox in medieval tales.",
            'memory_tip': "Think of the clever fox character from old European fables.",
            'example_sentence': "The story featured ___ outwitting the other forest animals."
        },
        'rhabdoid': {
            'definition': "Resembling or having the shape of a rod; rod-like in appearance; in medicine, relating to certain types of tumors with rod-shaped characteristics. Rhabdoid describes structures with elongated, rod-like morphology.",
            'pronunciation': "/ˈræbdɔɪd/",
            'pronunciation_respelling': "RAB-doyd",
            'etymology': "From Greek \"rhabdos\" (rod) + suffix \"-oid\" (resembling).",
            'memory_tip': "Think \"rhabd\" (rod) + \"oid\" (like) = like a rod shape.",
            'example_sentence': "The pathologist identified ___ cells in the tissue sample."
        },
        'rhapsody': {
            'definition': "An emotional piece of music in irregular form; an effusively enthusiastic or ecstatic expression of feeling; a literary work marked by emotional intensity. Rhapsodies express passionate emotion through artistic medium.",
            'pronunciation': "/ˈræpsədi/",
            'pronunciation_respelling': "RAP-suh-dee",
            'etymology': "From Greek \"rhapsodia,\" from \"rhaptein\" (to stitch) + \"oide\" (song).",
            'memory_tip': "Think \"rhap\" (stitch) + \"sody\" (song) = stitched together emotional song.",
            'example_sentence': "Liszt's Hungarian ___ No. 2 is a beloved classical piece."
        },
        'rheostat': {
            'definition': "An electrical instrument used to control current by varying resistance; a variable resistor that regulates electrical flow. Rheostats are used to control motor speed, lighting intensity, and other electrical applications.",
            'pronunciation': "/ˈrioʊˌstæt/",
            'pronunciation_respelling': "REE-oh-stat",
            'etymology': "From Greek \"rheos\" (current) + \"statos\" (standing), literally \"current controller.\"",
            'memory_tip': "Think \"rheo\" (current) + \"stat\" (control) = controls electrical current.",
            'example_sentence': "The technician adjusted the ___ to reduce the motor's speed."
        },
        'rhetorical': {
            'definition': "Relating to rhetoric or the effective use of language; designed to persuade or impress; asked for effect rather than for information. Rhetorical techniques focus on persuasive communication and stylistic expression.",
            'pronunciation': "/rɪˈtɔrɪkəl/",
            'pronunciation_respelling': "ri-TOR-ih-kuhl",
            'etymology': "From \"rhetoric\" + suffix \"-al,\" from Greek \"rhetorike\" (art of speaking).",
            'memory_tip': "Think \"rhetoric\" + \"al\" = relating to persuasive speaking.",
            'example_sentence': "The politician's ___ question was meant to emphasize his point."
        },
        'rheumatic': {
            'definition': "Relating to or caused by rheumatism; affecting the joints, muscles, or connective tissues; characterized by inflammation and pain in joints. Rheumatic conditions involve inflammatory diseases of connective tissues.",
            'pronunciation': "/ruˈmætɪk/",
            'pronunciation_respelling': "roo-MAT-ik",
            'etymology': "From Greek \"rheumatikos,\" from \"rheuma\" (flow), referring to bodily humors.",
            'memory_tip': "Think \"rheum\" (flow) + \"atic\" = relating to joint flow problems.",
            'example_sentence': "The elderly patient suffered from ___ pain in her knees."
        },
        'rhinestone': {
            'definition': "A colorless artificial gem made from rock crystal, glass, or paste; an imitation diamond used in costume jewelry and decorations. Rhinestones provide sparkle and decoration at lower cost than genuine gems.",
            'pronunciation': "/ˈraɪnˌstoʊn/",
            'pronunciation_respelling': "RHYNE-stohn",
            'etymology': "From \"Rhine\" (river) + \"stone,\" originally rock crystal from the Rhine region.",
            'memory_tip': "Think \"Rhine\" (river) + \"stone\" = crystal from Rhine river area.",
            'example_sentence': "Her costume jewelry sparkled with numerous ___."
        },
        'rhinorrhagia': {
            'definition': "Severe nosebleed; profuse bleeding from the nose; medical term for significant nasal hemorrhage. Rhinorrhagia indicates excessive nasal bleeding requiring medical attention.",
            'pronunciation': "/ˌraɪnoʊˈreɪdʒiə/",
            'pronunciation_respelling': "rye-noh-RAY-jee-uh",
            'etymology': "From Greek \"rhinos\" (nose) + \"rhagia\" (bursting forth), literally \"nose bursting.\"",
            'memory_tip': "Think \"rhino\" (nose) + \"rhagia\" (bursting) = nose bleeding burst.",
            'example_sentence': "The patient was hospitalized due to severe ___."
        },
        'rhizome': {
            'definition': "A horizontal underground plant stem that produces shoots above and roots below; a root-like stem that spreads underground. Rhizomes allow plants to reproduce vegetatively and store nutrients.",
            'pronunciation': "/ˈraɪzoʊm/",
            'pronunciation_respelling': "RYE-zohm",
            'etymology': "From Greek \"rhizoma,\" from \"rhiza\" (root) + \"-oma\" (mass).",
            'memory_tip': "Think \"rhiz\" (root) + \"ome\" (mass) = root-like mass underground.",
            'example_sentence': "Ginger grows from an edible ___ that spreads horizontally."
        },
        'rhododendron': {
            'definition': "A woody shrub or tree of the heath family, bearing large clusters of trumpet-shaped flowers; ornamental plants known for their colorful blooms. Rhododendrons are popular landscaping plants in temperate climates.",
            'pronunciation': "/ˌroʊdəˈdendrən/",
            'pronunciation_respelling': "roh-duh-DEN-druhn",
            'etymology': "From Greek \"rhodon\" (rose) + \"dendron\" (tree), literally \"rose tree.\"",
            'memory_tip': "Think \"rhodo\" (rose) + \"dendron\" (tree) = rose-like flowering tree.",
            'example_sentence': "The garden was spectacular when the ___ bushes bloomed in spring."
        },
        'rhombus': {
            'definition': "A parallelogram with all four sides of equal length; a diamond-shaped quadrilateral; a geometric figure with opposite sides parallel and all sides equal. Rhombuses are specific types of parallelograms.",
            'pronunciation': "/ˈrɑmbəs/",
            'pronunciation_respelling': "ROM-buhs",
            'etymology': "From Greek \"rhombos,\" meaning \"spinning top\" or \"magic wheel.\"",
            'memory_tip': "Think of a diamond shape that spins = rhombus.",
            'example_sentence': "The geometry student calculated the area of the ___."
        },
        'rhubarb': {
            'definition': "A plant with large leaves and thick red or green leafstalks that are edible when cooked; the edible leafstalks of this plant used in cooking. Rhubarb is commonly used in pies and desserts.",
            'pronunciation': "/ˈrubɑrb/",
            'pronunciation_respelling': "ROO-barb",
            'etymology': "From Old French \"rubarbe,\" from Latin \"rheubarbarum,\" from Greek \"rha barbaros.\"",
            'memory_tip': "Think \"rhu\" + \"barb\" = plant with reddish stalks like barbs.",
            'example_sentence': "Grandmother made delicious ___ pie from plants in her garden."
        },
        'rhythmic': {
            'definition': "Having a regular, repeated pattern of movement or sound; marked by rhythm; relating to or characterized by rhythm. Rhythmic elements create patterns that repeat in predictable intervals.",
            'pronunciation': "/ˈrɪðmɪk/",
            'pronunciation_respelling': "RITH-mik",
            'etymology': "From \"rhythm\" + suffix \"-ic,\" from Greek \"rhythmos\" (measured flow).",
            'memory_tip': "Think \"rhythm\" + \"ic\" = having the quality of rhythm.",
            'example_sentence': "The dancers moved to the ___ beat of the drums."
        },
        'rhythmically': {
            'definition': "In a manner characterized by rhythm; with regular, repeated patterns of movement or sound; according to rhythmic principles. Rhythmical action follows predictable timing patterns.",
            'pronunciation': "/ˈrɪðmɪkli/",
            'pronunciation_respelling': "RITH-mik-lee",
            'etymology': "From \"rhythmic\" + suffix \"-ally,\" from Greek \"rhythmos\" (measured flow).",
            'memory_tip': "Think \"rhythmic\" + \"ally\" = in a rhythmic manner.",
            'example_sentence': "The waves crashed ___ against the rocky shore."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_149_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_149_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['resuscitateretina', 'revelationarithmetic']
    
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
                    'notes': 'Batch 149 processing',
                    'review_status': 'pending',
                    'batch_number': '149'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 149 processing complete!")
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