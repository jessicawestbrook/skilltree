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
            'regular': ['replace', 'replaced', 'replica', 'reply', 'report', 'reporting', 'repress', 'reptile', 'republic', 'requires', 'resemble', 'resembled', 'resembles', 'resort', 'resource', 'respect', 'respond', 'responsible', 'rest', 'restaurant'],
            'semi_regular': ['reparations', 'repast', 'repentant', 'repercussion', 'replete', 'repose', 'repository', 'reprieve', 'reprisal', 'reputation', 'reservation', 'residence', 'residential', 'residue', 'resilience', 'resinous', 'resonate', 'respiratory', 'respite'],
            'irregular': ['repartee', 'repudiate', 'requiem', 'requisition', 'rescissible', 'reseau', 'resplendence']
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
        high_frequency = ['replace', 'replaced', 'reply', 'report', 'reporting', 'resemble', 'resembled', 'resembles', 'resort', 'resource', 'respect', 'respond', 'responsible', 'rest', 'restaurant', 'requires', 'reputation', 'residence']
        medium_frequency = ['reparations', 'repentant', 'repercussion', 'replica', 'reptile', 'republic', 'reservation', 'residential', 'residue', 'resilience', 'respiratory', 'respite']
        low_frequency = ['repartee', 'repast', 'replete', 'repose', 'repository', 'repoussage', 'repress', 'reprieve', 'reprisal', 'repudiate', 'requiem', 'requisition', 'rescissible', 'reseau', 'resinous', 'resonate', 'resplendence']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['replace', 'replaced', 'reply', 'report', 'reptile', 'respect', 'respond', 'rest']
        moderate_words = ['reparations', 'repentant', 'repercussion', 'replica', 'reporting', 'repose', 'reprieve', 'reprisal', 'republic', 'reputation', 'requires', 'resemble', 'resembled', 'resembles', 'reservation', 'residence', 'residential', 'residue', 'resilience', 'resort', 'resource', 'responsible', 'restaurant', 'respiratory', 'respite']
        complex_words = ['repartee', 'repast', 'replete', 'repository', 'repoussage', 'repress', 'repudiate', 'requiem', 'requisition', 'rescissible', 'reseau', 'resinous', 'resonate', 'resplendence']
        
        if word in simple_words:
            return 2
        elif word in moderate_words:
            return 4
        elif word in complex_words:
            return 7
        else:
            return 5
    
    def _calculate_etymology_complexity(self, etymology):
        if 'Latin' in etymology and 'prefix' in etymology:
            return 6
        elif 'Latin' in etymology or 'French' in etymology:
            return 4
        elif 'Old English' in etymology or 'Germanic' in etymology:
            return 3
        elif 'Greek' in etymology:
            return 7
        else:
            return 5

def main():
    calculator = DifficultyCalculator()
    
    word_data = {
        'reparations': {
            'definition': "The action of making amends for a wrong that has been done; compensation paid by a country defeated in war to another country for damage; payments made to individuals or groups who suffered historical injustices. Reparations aim to restore victims to their condition before harm occurred.",
            'pronunciation': "/ˌrepəˈreɪʃənz/",
            'pronunciation_respelling': "rep-uh-RAY-shuhnz",
            'etymology': "From Latin \"reparatio,\" from \"reparare\" (to repair), from \"re-\" (again) + \"parare\" (to prepare).",
            'memory_tip': "Think \"repair\" + \"ations\" = actions to repair damage done.",
            'example_sentence': "The government established a fund for ___ to families affected by past injustices."
        },
        'repartee': {
            'definition': "Conversation or speech characterized by quick, witty comments or replies; the practice of exchanging clever remarks. Repartee involves verbal dexterity and humor, often in social or competitive conversational settings.",
            'pronunciation': "/ˌrepɑrˈti/",
            'pronunciation_respelling': "rep-ar-TEE",
            'etymology': "From French \"repartie,\" from \"repartir\" (to set out again), from \"re-\" (again) + \"partir\" (to depart).",
            'memory_tip': "Think \"re-\" (back) + \"partee\" (party talk) = witty back-and-forth conversation.",
            'example_sentence': "The dinner party was filled with lively ___ between the guests."
        },
        'repast': {
            'definition': "A meal, especially a large or elaborate one; the act of taking food; nourishment or refreshment. Repast is a formal or literary term for dining, often suggesting a substantial or ceremonial meal.",
            'pronunciation': "/rɪˈpæst/",
            'pronunciation_respelling': "ri-PAST",
            'etymology': "From Old French \"repast,\" from \"repaistre\" (to feed), from Latin \"repascere\" (to feed again).",
            'memory_tip': "Think \"re-\" (again) + \"past\" (feed) = feeding again = meal.",
            'example_sentence': "The medieval feast was a sumptuous ___ lasting several hours."
        },
        'repentant': {
            'definition': "Expressing or feeling sincere regret and remorse for wrongdoing; showing genuine sorrow for past actions with intention to change. Repentance involves both emotional regret and commitment to behavioral change.",
            'pronunciation': "/rɪˈpentənt/",
            'pronunciation_respelling': "ri-PEN-tuhnt",
            'etymology': "From Latin \"repentere\" (to regret), from \"re-\" (back) + \"pentere\" (to make regret).",
            'memory_tip': "Think \"re-\" (back) + \"pentant\" (feeling pain) = feeling pain about past actions.",
            'example_sentence': "The ___ criminal asked for forgiveness from the victim's family."
        },
        'repercussion': {
            'definition': "An unintended consequence of an event or action; a widespread, indirect, or unforeseen effect; the rebound or recoil of something. Repercussions often involve negative consequences that follow from decisions or events.",
            'pronunciation': "/ˌripərˈkʌʃən/",
            'pronunciation_respelling': "ree-pur-KUHSH-uhn",
            'etymology': "From Latin \"repercussio,\" from \"repercutere\" (to drive back), from \"re-\" (back) + \"percutere\" (to strike).",
            'memory_tip': "Think \"re-\" (back) + \"percussion\" = striking back effects.",
            'example_sentence': "The company didn't anticipate the ___ of their policy change."
        },
        'replace': {
            'definition': "To take the place of something; to substitute one thing for another; to put something back in its former position. Replacement involves removal of one item and installation or positioning of another in its place.",
            'pronunciation': "/rɪˈpleɪs/",
            'pronunciation_respelling': "ri-PLAYS",
            'etymology': "From \"re-\" (back) + \"place,\" from Old French \"placer\" (to place).",
            'memory_tip': "Think \"re-\" (again) + \"place\" = place again in same position.",
            'example_sentence': "We need to ___ the broken window before winter arrives."
        },
        'replaced': {
            'definition': "Past tense of replace; took the place of something; substituted one thing for another; put something back in its former position. The action of replacement has been completed.",
            'pronunciation': "/rɪˈpleɪst/",
            'pronunciation_respelling': "ri-PLAYST",
            'etymology': "Past tense of \"replace,\" from \"re-\" (back) + \"place.\"",
            'memory_tip': "Think \"replace\" + \"d\" = the replacement was completed.",
            'example_sentence': "The old computer was ___ with a newer, faster model."
        },
        'replete': {
            'definition': "Filled or well-supplied with something; abundantly provided or stocked; completely full. Replete suggests thorough abundance or completeness, often used to describe something filled to capacity.",
            'pronunciation': "/rɪˈplit/",
            'pronunciation_respelling': "ri-PLEET",
            'etymology': "From Latin \"repletus,\" from \"replere\" (to fill up), from \"re-\" (again) + \"plere\" (to fill).",
            'memory_tip': "Think \"re-\" (completely) + \"plete\" (fill) = completely filled.",
            'example_sentence': "The library was ___ with rare manuscripts and ancient texts."
        },
        'replica': {
            'definition': "An exact copy or reproduction of something, especially a work of art; a duplicate made to resemble an original. Replicas are intended to be faithful reproductions that closely match the original in appearance and details.",
            'pronunciation': "/ˈrepləkə/",
            'pronunciation_respelling': "REP-li-kuh",
            'etymology': "From Italian \"replica,\" from \"replicare\" (to reply), from Latin \"re-\" (back) + \"plicare\" (to fold).",
            'memory_tip': "Think \"rep\" (repeat) + \"lica\" = repeated copy of original.",
            'example_sentence': "The museum displayed a perfect ___ of the famous sculpture."
        },
        'reply': {
            'definition': "To say something in response to something that has been said; a spoken or written answer; to respond to a question, letter, or statement. Reply involves reciprocal communication and acknowledgment.",
            'pronunciation': "/rɪˈplaɪ/",
            'pronunciation_respelling': "ri-PLYE",
            'etymology': "From Old French \"replier,\" from Latin \"replicare,\" from \"re-\" (back) + \"plicare\" (to fold).",
            'memory_tip': "Think \"re-\" (back) + \"ply\" (respond) = respond back.",
            'example_sentence': "Please ___ to my email when you have a chance."
        },
        'report': {
            'definition': "To give a spoken or written account of something; a detailed description or analysis of an event or situation; to present information officially. Reports provide structured information for decision-making or record-keeping.",
            'pronunciation': "/rɪˈpɔrt/",
            'pronunciation_respelling': "ri-PORT",
            'etymology': "From Old French \"reporter,\" from Latin \"reportare,\" from \"re-\" (back) + \"portare\" (to carry).",
            'memory_tip': "Think \"re-\" (back) + \"port\" (carry) = carry information back.",
            'example_sentence': "The journalist will ___ on the election results tonight."
        },
        'reporting': {
            'definition': "The action of giving an account of something; the activity of writing about news events for newspapers, television, or radio; presenting information in an organized manner. Journalism and documentation activities.",
            'pronunciation': "/rɪˈpɔrtɪŋ/",
            'pronunciation_respelling': "ri-PORT-ing",
            'etymology': "Present participle of \"report,\" from Latin \"reportare\" (to carry back).",
            'memory_tip': "Think \"report\" + \"ing\" = currently carrying information back.",
            'example_sentence': "The ___ from the war zone provided crucial information to the public."
        },
        'repose': {
            'definition': "A state of rest, sleep, or tranquility; to rest or lie down; peaceful relaxation or freedom from activity. Repose suggests calm, restful states and peaceful positioning or mental states.",
            'pronunciation': "/rɪˈpoʊz/",
            'pronunciation_respelling': "ri-POHZ",
            'etymology': "From Old French \"reposer,\" from Latin \"repausare,\" from \"re-\" (back) + \"pausare\" (to pause).",
            'memory_tip': "Think \"re-\" (back) + \"pose\" = pose back in restful position.",
            'example_sentence': "She found ___ in the peaceful garden after a stressful day."
        },
        'repository': {
            'definition': "A place where things are stored and can be found; a warehouse or storehouse; a person regarded as a store of information. Repositories serve as organized storage systems for materials, data, or knowledge.",
            'pronunciation': "/rɪˈpɑzəˌtɔri/",
            'pronunciation_respelling': "ri-POZ-ih-tor-ee",
            'etymology': "From Latin \"repositorium,\" from \"reponere\" (to replace), from \"re-\" (back) + \"ponere\" (to place).",
            'memory_tip': "Think \"re-\" (back) + \"posit\" (place) + \"ory\" = place to put things back.",
            'example_sentence': "The library serves as a ___ for the community's historical documents."
        },
        'repoussage': {
            'definition': "A metalworking technique in which a design is hammered into the reverse side of metal to create a raised design on the front; the art of decorating metal by hammering from the reverse side. Used in decorative arts and jewelry making.",
            'pronunciation': "/rɪˈpusɑʒ/",
            'pronunciation_respelling': "ri-poo-SAHZH",
            'etymology': "From French \"repoussage,\" from \"repousser\" (to push back), from \"re-\" (back) + \"pousser\" (to push).",
            'memory_tip': "Think \"re-\" (back) + \"pousse\" (push) = push back technique for metal art.",
            'example_sentence': "The artisan used ___ to create intricate patterns on the copper bowl."
        },
        'repress': {
            'definition': "To hold back or restrain; to suppress a thought, feeling, or memory; to control or subdue by force. Repression can be psychological (blocking memories) or political (controlling populations).",
            'pronunciation': "/rɪˈpres/",
            'pronunciation_respelling': "ri-PRES",
            'etymology': "From Latin \"reprimere,\" from \"re-\" (back) + \"premere\" (to press).",
            'memory_tip': "Think \"re-\" (back) + \"press\" = press back down/control.",
            'example_sentence': "She struggled not to ___ her anger during the meeting."
        },
        'reprieve': {
            'definition': "A temporary postponement of punishment; relief from something unpleasant; to give temporary relief from punishment or suffering. Reprieves provide temporary respite from negative consequences.",
            'pronunciation': "/rɪˈpriv/",
            'pronunciation_respelling': "ri-PREEV",
            'etymology': "From Old French \"repris,\" past participle of \"reprendre\" (to take back).",
            'memory_tip': "Think \"re-\" (back) + \"prieve\" (take) = taking back punishment temporarily.",
            'example_sentence': "The governor granted a last-minute ___ to the condemned prisoner."
        },
        'reprisal': {
            'definition': "An act of retaliation; revenge taken for an injury or wrong; retaliatory action against an enemy. Reprisals involve responding to harmful actions with similar harmful actions in return.",
            'pronunciation': "/rɪˈpraɪzəl/",
            'pronunciation_respelling': "ri-PRYE-zuhl",
            'etymology': "From Old French \"reprisaille,\" from \"reprendre\" (to take back), from Latin \"reprehendere.\"",
            'memory_tip': "Think \"re-\" (back) + \"prisal\" (taking) = taking back through retaliation.",
            'example_sentence': "The attack was seen as a ___ for the previous bombing."
        },
        'reptile': {
            'definition': "A cold-blooded vertebrate animal with scales, breathing air through lungs, typically laying eggs on land; includes snakes, lizards, turtles, and crocodiles. Reptiles are characterized by their scaly skin and ectothermic metabolism.",
            'pronunciation': "/ˈreptaɪl/",
            'pronunciation_respelling': "REP-tahyl",
            'etymology': "From Latin \"reptilis,\" from \"reptare\" (to creep), from \"repere\" (to crawl).",
            'memory_tip': "Think \"rept\" (creep) + \"ile\" = creature that creeps along ground.",
            'example_sentence': "The iguana is a large ___ native to Central and South America."
        },
        'republic': {
            'definition': "A state in which supreme power is held by the people through their elected representatives; a form of government without a monarch. Republics feature democratic elements and elected leadership rather than hereditary rule.",
            'pronunciation': "/rɪˈpʌblɪk/",
            'pronunciation_respelling': "ri-PUHB-lik",
            'etymology': "From Latin \"respublica,\" from \"res\" (thing) + \"publica\" (public).",
            'memory_tip': "Think \"re-\" (thing) + \"public\" = thing belonging to the public.",
            'example_sentence': "The United States is a federal ___ with democratically elected leaders."
        },
        'repudiate': {
            'definition': "To refuse to accept or be associated with; to deny the truth or validity of something; to reject with disapproval or condemnation. Repudiation involves formal rejection or disavowal of claims, debts, or associations.",
            'pronunciation': "/rɪˈpjudɪˌeɪt/",
            'pronunciation_respelling': "ri-PYOO-dee-ayt",
            'etymology': "From Latin \"repudiare,\" from \"repudium\" (divorce), from \"re-\" (back) + \"pudere\" (to feel shame).",
            'memory_tip': "Think \"re-\" (back) + \"pudi\" (shame) = push back shameful claims.",
            'example_sentence': "The politician chose to ___ the extremist endorsement."
        },
        'reputation': {
            'definition': "The beliefs or opinions that are generally held about someone or something; the estimation in which a person or thing is held; widespread recognition for particular qualities. Reputation reflects public perception and standing.",
            'pronunciation': "/ˌrepjuˈteɪʃən/",
            'pronunciation_respelling': "rep-yuh-TAY-shuhn",
            'etymology': "From Latin \"reputatio,\" from \"reputare\" (to think over), from \"re-\" (again) + \"putare\" (to think).",
            'memory_tip': "Think \"re-\" (again) + \"putation\" (thinking) = what people think again and again.",
            'example_sentence': "The chef's ___ for excellence attracted customers from across the city."
        },
        'requiem': {
            'definition': "A mass for the dead; a musical composition for this mass; any composition commemorating the dead. Requiems are solemn musical works or religious services honoring and remembering deceased persons.",
            'pronunciation': "/ˈrekwɪəm/",
            'pronunciation_respelling': "REK-wee-uhm",
            'etymology': "From Latin \"requiem,\" from \"requies\" (rest), first word of the mass \"Requiem aeternam\" (eternal rest).",
            'memory_tip': "Think \"requ\" (rest) + \"iem\" = rest for the dead.",
            'example_sentence': "Mozart's ___ is considered one of the greatest choral works ever composed."
        },
        'requires': {
            'definition': "Third person singular present tense of require; needs or demands as necessary; makes something obligatory. Indicates present necessity, obligation, or essential need for something.",
            'pronunciation': "/rɪˈkwaɪərz/",
            'pronunciation_respelling': "ri-KWYE-urz",
            'etymology': "Third person singular of \"require,\" from Latin \"requirere,\" from \"re-\" (again) + \"quaerere\" (to seek).",
            'memory_tip': "Think \"re-\" (again) + \"quires\" (seeks) = seeks again = needs.",
            'example_sentence': "This job ___ at least five years of experience in the field."
        },
        'requisition': {
            'definition': "An official order laying claim to the use of property or materials; to demand the use or supply of something; a formal written request for something needed. Requisitions are official demands for resources or property.",
            'pronunciation': "/ˌrekwəˈzɪʃən/",
            'pronunciation_respelling': "rek-wuh-ZISH-uhn",
            'etymology': "From Latin \"requisitio,\" from \"requirere\" (to require), from \"re-\" (again) + \"quaerere\" (to seek).",
            'memory_tip': "Think \"re-\" (again) + \"quisition\" (seeking) = official seeking of resources.",
            'example_sentence': "The army issued a ___ for additional medical supplies."
        },
        'rescissible': {
            'definition': "Capable of being rescinded, revoked, or annulled; able to be cancelled or made void. Rescissible contracts or agreements can be legally terminated under certain conditions.",
            'pronunciation': "/rɪˈsɪsəbəl/",
            'pronunciation_respelling': "ri-SIS-uh-buhl",
            'etymology': "From Latin \"rescindere\" (to cut off) + suffix \"-ible\" (capable of), from \"re-\" (back) + \"scindere\" (to cut).",
            'memory_tip': "Think \"re-\" (back) + \"sciss\" (cut) + \"ible\" = able to be cut back/cancelled.",
            'example_sentence': "The contract was deemed ___ due to fraudulent misrepresentation."
        },
        'rescissiblejungian': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'rescissible' + 'jungian' incorrectly joined. 'Rescissible' means capable of being revoked, while 'Jungian' relates to Carl Jung's psychology. These should be separate words.]",
            'pronunciation': "/rɪˈsɪsəbəl ˈjʊŋɡiən/",
            'pronunciation_respelling': "ri-SIS-uh-buhl YUUNG-gee-uhn",
            'etymology': "Combined word error: 'rescissible' from Latin + 'Jungian' from Jung (surname).",
            'memory_tip': "Error combination: rescissible (revokable) + Jungian (psychology) - should be separate.",
            'example_sentence': "The ___ contract involved ___ psychological principles."
        },
        'rescissiblereveille': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'rescissible' + 'reveille' incorrectly joined. 'Rescissible' means capable of being revoked, while 'reveille' is a military wake-up call. These should be separate words.]",
            'pronunciation': "/rɪˈsɪsəbəl ˈrevəli/",
            'pronunciation_respelling': "ri-SIS-uh-buhl REV-uh-lee",
            'etymology': "Combined word error: 'rescissible' from Latin + 'reveille' from French.",
            'memory_tip': "Error combination: rescissible (revokable) + reveille (wake-up call) - should be separate.",
            'example_sentence': "The ___ agreement was cancelled before the morning ___."
        },
        'rescuedifficulty': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'rescue' + 'difficulty' incorrectly joined. 'Rescue' means to save from danger, while 'difficulty' means something hard to accomplish. These should be separate words.]",
            'pronunciation': "/ˈreskju ˈdɪfɪkəlti/",
            'pronunciation_respelling': "RES-kyoo DIF-ih-kuhl-tee",
            'etymology': "Combined word error: 'rescue' from Old French + 'difficulty' from Latin.",
            'memory_tip': "Error combination: rescue (save) + difficulty (hardship) - should be separate.",
            'example_sentence': "The mountain ___ presented extreme ___ due to weather conditions."
        },
        'reseau': {
            'definition': "A network or netlike pattern; in textiles, a mesh ground in lace; a grid pattern used in surveying or photography. Reseau refers to systematic network patterns in various technical applications.",
            'pronunciation': "/rɪˈzoʊ/",
            'pronunciation_respelling': "ri-ZOH",
            'etymology': "From French \"réseau,\" from Old French \"roisel,\" diminutive of \"rois\" (network).",
            'memory_tip': "Think French \"réseau\" = network pattern like a net.",
            'example_sentence': "The delicate lace featured an intricate ___ of interconnected threads."
        },
        'resemble': {
            'definition': "To have qualities or features in common with something; to be like or similar to; to have a likeness to someone or something. Resemblance involves shared characteristics that create similarity.",
            'pronunciation': "/rɪˈzembəl/",
            'pronunciation_respelling': "ri-ZEM-buhl",
            'etymology': "From Old French \"resembler,\" from \"re-\" (again) + \"sembler\" (to seem).",
            'memory_tip': "Think \"re-\" (again) + \"semble\" (seem) = seem like again = be similar to.",
            'example_sentence': "The twins ___ each other so closely that people often confuse them."
        },
        'resembled': {
            'definition': "Past tense of resemble; had qualities or features in common with something; was like or similar to something. The similarity or likeness existed in the past.",
            'pronunciation': "/rɪˈzembəld/",
            'pronunciation_respelling': "ri-ZEM-buhld",
            'etymology': "Past tense of \"resemble,\" from Old French \"resembler.\"",
            'memory_tip': "Think \"resemble\" + \"d\" = was similar to in the past.",
            'example_sentence': "The ancient ruins ___ a magnificent temple from Roman times."
        },
        'resembles': {
            'definition': "Third person singular present tense of resemble; has qualities or features in common with something; is like or similar to something. Current similarity or likeness to something else.",
            'pronunciation': "/rɪˈzembəlz/",
            'pronunciation_respelling': "ri-ZEM-buhlz",
            'etymology': "Third person singular of \"resemble,\" from Old French \"resembler.\"",
            'memory_tip': "Think \"resemble\" + \"s\" = currently looks like or is similar to.",
            'example_sentence': "This painting ___ the work of a famous Renaissance master."
        },
        'reservation': {
            'definition': "The action of reserving something; an arrangement to have something held for one's use; a qualification to an expression of agreement; an area of land set aside for a specific purpose. Reservations involve setting aside or holding back.",
            'pronunciation': "/ˌrezərˈveɪʃən/",
            'pronunciation_respelling': "rez-ur-VAY-shuhn",
            'etymology': "From \"reserve\" + suffix \"-ation,\" from Latin \"reservare\" (to keep back).",
            'memory_tip': "Think \"reserve\" + \"ation\" = action of keeping something reserved.",
            'example_sentence': "Please make a ___ for dinner at eight o'clock tonight."
        },
        'residence': {
            'definition': "A person's home or place where they live; the fact of living in a place; a large house or official home. Residence encompasses both the physical dwelling and the act of living there.",
            'pronunciation': "/ˈrezədəns/",
            'pronunciation_respelling': "REZ-ih-duhns",
            'etymology': "From Latin \"residentia,\" from \"residere\" (to remain), from \"re-\" (back) + \"sidere\" (to sit).",
            'memory_tip': "Think \"re-\" (back) + \"sidence\" (sitting) = place where one sits back/lives.",
            'example_sentence': "The ambassador's official ___ was an elegant mansion downtown."
        },
        'residential': {
            'definition': "Relating to or designed for people to live in; providing housing or accommodation; containing private houses rather than commercial buildings. Residential areas are designated for living rather than business.",
            'pronunciation': "/ˌrezəˈdenʃəl/",
            'pronunciation_respelling': "rez-ih-DEN-shuhl",
            'etymology': "From \"residence\" + suffix \"-al,\" from Latin \"residere\" (to remain).",
            'memory_tip': "Think \"residence\" + \"al\" = relating to where people reside.",
            'example_sentence': "The city planned to develop the area into a ___ neighborhood."
        },
        'residue': {
            'definition': "A small amount of something that remains after the main part has gone or been taken away; matter that remains after processing; a remainder. Residue represents what is left over after removal or consumption.",
            'pronunciation': "/ˈrezəˌdu/",
            'pronunciation_respelling': "REZ-ih-doo",
            'etymology': "From Latin \"residuum,\" from \"residere\" (to remain), from \"re-\" (back) + \"sidere\" (to sit).",
            'memory_tip': "Think \"re-\" (back) + \"sidue\" (sitting) = what sits back/remains.",
            'example_sentence': "The chemical reaction left a white ___ at the bottom of the beaker."
        },
        'resilience': {
            'definition': "The ability to recover quickly from difficulties; the capacity to withstand or recover from adverse conditions; elasticity or flexibility. Resilience involves bouncing back from challenges and adapting to change.",
            'pronunciation': "/rɪˈzɪljəns/",
            'pronunciation_respelling': "ri-ZIL-yuhnts",
            'etymology': "From Latin \"resilire\" (to leap back), from \"re-\" (back) + \"salire\" (to leap).",
            'memory_tip': "Think \"re-\" (back) + \"silience\" (leaping) = leaping back from adversity.",
            'example_sentence': "Her ___ helped her overcome the challenges of starting a new business."
        },
        'resinous': {
            'definition': "Containing, producing, or resembling resin; having the characteristics of resin such as stickiness or amber color. Resinous substances have the properties of natural tree resins used in various applications.",
            'pronunciation': "/ˈrezənəs/",
            'pronunciation_respelling': "REZ-ih-nuhs",
            'etymology': "From \"resin\" + suffix \"-ous\" (having the quality of), from Latin \"resina.\"",
            'memory_tip': "Think \"resin\" + \"ous\" = having the quality of sticky tree resin.",
            'example_sentence': "The pine tree produced a ___ sap that hardened into amber-like chunks."
        },
        'resonate': {
            'definition': "To produce a deep, reverberating sound; to evoke a feeling of shared emotion or belief; to have significance or meaning for someone. Resonance can be acoustic, emotional, or conceptual.",
            'pronunciation': "/ˈrezəˌneɪt/",
            'pronunciation_respelling': "REZ-uh-nayt",
            'etymology': "From Latin \"resonare,\" from \"re-\" (again) + \"sonare\" (to sound).",
            'memory_tip': "Think \"re-\" (again) + \"sonate\" (sound) = sound again/echo.",
            'example_sentence': "The speaker's message seemed to ___ with the entire audience."
        },
        'resort': {
            'definition': "To turn to and adopt a course of action, especially an extreme one; a place frequented for holidays or recreation; a source of help in a difficult situation. Resort can mean both a vacation destination and a last option.",
            'pronunciation': "/rɪˈzɔrt/",
            'pronunciation_respelling': "ri-ZORT",
            'etymology': "From Old French \"resortir,\" from \"re-\" (again) + \"sortir\" (to go out).",
            'memory_tip': "Think \"re-\" (again) + \"sort\" = go out again to a place or option.",
            'example_sentence': "When negotiation failed, they had to ___ to legal action."
        },
        'resource': {
            'definition': "A stock or supply of money, materials, staff, or other assets that can be drawn on when needed; a means of supplying what is needed; natural materials or capabilities. Resources provide the means to accomplish goals.",
            'pronunciation': "/ˈriˌsɔrs/",
            'pronunciation_respelling': "REE-sors",
            'etymology': "From Old French \"ressource,\" from \"ressourcir\" (to rise again), from \"re-\" (again) + \"source\" (to spring up).",
            'memory_tip': "Think \"re-\" (again) + \"source\" = source that springs up again when needed.",
            'example_sentence': "The company's most valuable ___ is its experienced workforce."
        },
        'respect': {
            'definition': "A feeling of deep admiration for someone or something; to admire someone or something deeply; to have due regard for someone's feelings or rights. Respect involves recognition of worth and appropriate treatment.",
            'pronunciation': "/rɪˈspekt/",
            'pronunciation_respelling': "ri-SPEKT",
            'etymology': "From Latin \"respectus,\" from \"respicere\" (to look back), from \"re-\" (back) + \"specere\" (to look).",
            'memory_tip': "Think \"re-\" (back) + \"spect\" (look) = look back with admiration.",
            'example_sentence': "The students showed great ___ for their elderly teacher."
        },
        'respiratory': {
            'definition': "Relating to breathing or the organs involved in breathing; concerning the process of respiration in living organisms. Respiratory systems involve the intake of oxygen and release of carbon dioxide.",
            'pronunciation': "/ˈrespərəˌtɔri/",
            'pronunciation_respelling': "RES-pur-uh-tor-ee",
            'etymology': "From Latin \"respirare\" (to breathe again) + suffix \"-ory,\" from \"re-\" (again) + \"spirare\" (to breathe).",
            'memory_tip': "Think \"re-\" (again) + \"spiratory\" (breathing) = relating to breathing again and again.",
            'example_sentence': "The doctor specialized in treating ___ diseases like asthma and pneumonia."
        },
        'respite': {
            'definition': "A short period of rest or relief from something difficult or unpleasant; a temporary delay or postponement. Respite provides temporary relief from ongoing challenges, work, or suffering.",
            'pronunciation': "/ˈrespɪt/",
            'pronunciation_respelling': "RES-pit",
            'etymology': "From Old French \"respit,\" from Latin \"respectus\" (regard, consideration).",
            'memory_tip': "Think \"rest\" + \"pit\" (stop) = stopping for rest.",
            'example_sentence': "The vacation provided a welcome ___ from the stressful work environment."
        },
        'resplendence': {
            'definition': "The quality of being resplendent; brilliant or magnificent appearance; splendor and dazzling beauty. Resplendence involves impressive brightness, luxury, or magnificence that attracts attention and admiration.",
            'pronunciation': "/rɪˈsplendəns/",
            'pronunciation_respelling': "ri-SPLEN-duhns",
            'etymology': "From Latin \"resplendere\" (to shine brightly), from \"re-\" (again) + \"splendere\" (to shine).",
            'memory_tip': "Think \"re-\" (again) + \"splendence\" = shining again with brilliance.",
            'example_sentence': "The palace ballroom was decorated in golden ___ for the royal wedding."
        },
        'respond': {
            'definition': "To say or do something as a reaction to something that has been said or done; to reply or answer; to react in a particular way to something. Responses involve reciprocal action or communication.",
            'pronunciation': "/rɪˈspɑnd/",
            'pronunciation_respelling': "ri-SPOND",
            'etymology': "From Latin \"respondere,\" from \"re-\" (back) + \"spondere\" (to pledge).",
            'memory_tip': "Think \"re-\" (back) + \"spond\" (pledge) = pledge back a response.",
            'example_sentence': "The patient began to ___ positively to the new treatment."
        },
        'responsible': {
            'definition': "Having a duty to deal with something; being the cause of something; having good judgment and the ability to act correctly; accountable for one's actions. Responsibility involves obligation and accountability.",
            'pronunciation': "/rɪˈspɑnsəbəl/",
            'pronunciation_respelling': "ri-SPON-suh-buhl",
            'etymology': "From \"response\" + suffix \"-ible,\" from Latin \"respondere\" (to respond).",
            'memory_tip': "Think \"response\" + \"ible\" = able to respond/answer for actions.",
            'example_sentence': "As team leader, she felt ___ for the project's success."
        },
        'rest': {
            'definition': "To cease work or movement in order to relax or recover strength; the remaining part of something; a pause in activity; peace and quiet. Rest involves cessation of activity for restoration or what remains after other parts are removed.",
            'pronunciation': "/rest/",
            'pronunciation_respelling': "REST",
            'etymology': "From Old English \"rest,\" of Germanic origin, related to German \"Rast.\"",
            'memory_tip': "Think of stopping activity to relax and restore energy.",
            'example_sentence': "After the long hike, they needed to ___ for several hours."
        },
        'restaurant': {
            'definition': "A business that prepares and serves food and drinks to customers; an eating establishment where meals are cooked and served to paying customers. Restaurants provide dining services in commercial settings.",
            'pronunciation': "/ˈrestərənt/",
            'pronunciation_respelling': "RES-tur-uhnt",
            'etymology': "From French \"restaurant,\" from \"restaurer\" (to restore), from Latin \"restaurare.\"",
            'memory_tip': "Think \"restor\" (restore) + \"ant\" = place that restores you with food.",
            'example_sentence': "The new Italian ___ downtown serves authentic pasta dishes."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_148_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_148_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['rescissiblejungian', 'rescissiblereveille', 'rescuedifficulty']
    
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
                    'notes': 'Batch 148 processing',
                    'review_status': 'pending',
                    'batch_number': '148'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 148 processing complete!")
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