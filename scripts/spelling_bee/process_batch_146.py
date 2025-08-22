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
            'regular': ['recognition', 'record', 'recruit', 'refer', 'reflect', 'refuge'],
            'semi_regular': ['recognize', 'reconsider', 'recovery', 'reduce', 'reference', 'referred', 'reflection', 'reflects', 'regales'],
            'irregular': ['reconcilable', 'reconnoiter', 'reconnoitre', 'rectitude', 'recusancy', 'redingote', 'redolent', 'refrain', 'regalia', 'reggae']
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
        high_frequency = ['recognition', 'recognize', 'record', 'reduce', 'refer', 'reference', 'referred', 'reflect', 'reflection', 'reflects', 'refuge']
        medium_frequency = ['reconsider', 'recovery', 'recruit', 'redemption', 'refrain', 'regiment', 'regalia', 'reggae']
        low_frequency = ['reconcilable', 'reconnoiter', 'reconnoitre', 'recoup', 'recreant', 'rectitude', 'recusancy', 'redingote', 'redolent', 'redux', 'referendum', 'regicide']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['record', 'reduce', 'refer', 'refuge', 'reeds']
        moderate_words = ['recognition', 'recognize', 'reconsider', 'recovery', 'recruit', 'redemption', 'refrain', 'reference', 'referred', 'reflect', 'reflection', 'reflects', 'regales', 'regalia', 'reggae', 'regiment']
        complex_words = ['reconcilable', 'reconnoiter', 'reconnoitre', 'recreant', 'recriminatory', 'recrudescent', 'rectitude', 'recumbent', 'recuperation', 'recusancy', 'recyclable', 'redingote', 'redolent', 'redound', 'redux', 'reenactment', 'refectory', 'referendum', 'reflexology', 'refrigerant', 'refrigerated', 'refugium', 'regicide']
        
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
        'recognition': {
            'definition': "The action or process of identifying someone or something from having encountered them before; acknowledgment of the existence, validity, or legality of something. Recognition involves cognitive processes of memory retrieval and pattern matching, and can range from simple identification to formal acknowledgment of achievements, rights, or status.",
            'pronunciation': "/ˌrekəɡˈnɪʃən/",
            'pronunciation_respelling': "rek-uhg-NISH-uhn",
            'etymology': "From Latin \"recognitio,\" from \"recognoscere\" (to know again), from \"re-\" (again) + \"cognoscere\" (to know).",
            'memory_tip': "Think \"re-\" (again) + \"cognition\" = knowing again = recognition.",
            'example_sentence': "The facial ___ software quickly identified the suspect from the database."
        },
        'recognize': {
            'definition': "To identify someone or something from having encountered them before; to acknowledge the existence, validity, or legality of something; to show appreciation for achievements or service. Recognition can be immediate and unconscious or deliberate and formal.",
            'pronunciation': "/ˈrekəɡnaɪz/",
            'pronunciation_respelling': "REK-uhg-nahyz",
            'etymology': "From Latin \"recognoscere,\" from \"re-\" (again) + \"cognoscere\" (to know).",
            'memory_tip': "Think \"re-\" (again) + \"cognize\" (to perceive) = to perceive again.",
            'example_sentence': "She didn't ___ her childhood friend after twenty years apart."
        },
        'recoil': {
            'definition': "To suddenly spring or flinch back in fear, horror, or disgust; the backward movement of a gun when fired due to the force of the discharge. Recoil can be physical, as with weapons, or emotional, as a reaction to something unpleasant or shocking.",
            'pronunciation': "/rɪˈkɔɪl/",
            'pronunciation_respelling': "ri-KOYL",
            'etymology': "From Old French \"reculer,\" from \"re-\" (back) + \"cul\" (bottom), meaning to go back.",
            'memory_tip': "Think \"re-\" (back) + \"coil\" = springing back like a coiled spring.",
            'example_sentence': "The soldier learned to manage the rifle's ___ during target practice."
        },
        'reconcilable': {
            'definition': "Capable of being reconciled, harmonized, or made consistent; able to be brought into agreement or compatibility. Reconcilable differences are those that can be resolved through discussion, compromise, or understanding, unlike irreconcilable differences.",
            'pronunciation': "/ˈrekənsaɪləbəl/",
            'pronunciation_respelling': "REK-uhn-sahy-luh-buhl",
            'etymology': "From Latin \"reconciliare\" (to bring together again) + suffix \"-able\" (capable of).",
            'memory_tip': "Think \"reconcile\" + \"able\" = capable of being brought back together.",
            'example_sentence': "The couple's differences seemed ___ with proper counseling and communication."
        },
        'reconnoiter': {
            'definition': "To make a military observation of an area to locate an enemy or ascertain strategic features; to explore or examine with the goal of gaining information. Reconnoitering involves systematic observation and information gathering for tactical or strategic purposes.",
            'pronunciation': "/ˌrekəˈnɔɪtər/",
            'pronunciation_respelling': "rek-uh-NOY-tur",
            'etymology': "From French \"reconnaître,\" from \"re-\" (again) + \"connaître\" (to know).",
            'memory_tip': "Think \"re-\" (again) + \"know\" + \"iter\" (journey) = journey to know again.",
            'example_sentence': "The scouts were sent to ___ the enemy positions before the main assault."
        },
        'reconnoitre': {
            'definition': "British spelling of reconnoiter; to make a military observation of an area to locate an enemy or ascertain strategic features; to explore or examine systematically. This variant spelling is commonly used in British English and Commonwealth countries.",
            'pronunciation': "/ˌrekəˈnɔɪtə/",
            'pronunciation_respelling': "rek-uh-NOY-tur",
            'etymology': "From French \"reconnaître,\" from \"re-\" (again) + \"connaître\" (to know).",
            'memory_tip': "British spelling: think \"re-\" + \"connaitre\" (French for know) + \"re\" ending.",
            'example_sentence': "The British patrol was ordered to ___ the village before dawn."
        },
        'reconsider': {
            'definition': "To consider again, especially with a view to changing one's mind; to think about something again carefully, often because new information has become available. Reconsideration involves reviewing previous decisions or opinions with fresh perspective.",
            'pronunciation': "/ˌriːkənˈsɪdər/",
            'pronunciation_respelling': "ree-kuhn-SID-ur",
            'etymology': "From \"re-\" (again) + \"consider,\" from Latin \"considerare\" (to examine closely).",
            'memory_tip': "Think \"re-\" (again) + \"consider\" = think about it again.",
            'example_sentence': "After hearing the new evidence, the judge agreed to ___ the verdict."
        },
        'record': {
            'definition': "A thing constituting a piece of evidence about the past; information stored for future reference; to set down in writing or other permanent form. Records serve as documentation, evidence, or achievement markers that preserve information across time.",
            'pronunciation': "/ˈrekərd/ (noun), /rɪˈkɔrd/ (verb)",
            'pronunciation_respelling': "REK-urd (noun), ri-KORD (verb)",
            'etymology': "From Latin \"recordari,\" from \"re-\" (back) + \"cor\" (heart), originally meaning to remember.",
            'memory_tip': "Think \"re-\" (back) + \"cord\" (heart) = bringing back to heart/memory.",
            'example_sentence': "The athlete broke the world ___ in the 100-meter sprint."
        },
        'recoup': {
            'definition': "To recover or regain something, especially money that has been spent or lost; to compensate for losses or expenses. Recouping involves getting back what was previously lost, spent, or invested, often through subsequent gains or recoveries.",
            'pronunciation': "/rɪˈkup/",
            'pronunciation_respelling': "ri-KOOP",
            'etymology': "From French \"recouper,\" from \"re-\" (again) + \"couper\" (to cut).",
            'memory_tip': "Think \"re-\" (again) + \"coup\" (a successful move) = successful recovery.",
            'example_sentence': "The company hopes to ___ its research costs within two years."
        },
        'recovery': {
            'definition': "The action or process of regaining possession or control of something; return to a normal state of health, mind, or strength; the process of becoming well again after illness or injury. Recovery encompasses physical, emotional, financial, or situational restoration.",
            'pronunciation': "/rɪˈkʌvəri/",
            'pronunciation_respelling': "ri-KUHV-uh-ree",
            'etymology': "From \"recover\" + suffix \"-y,\" from Latin \"recuperare\" (to regain).",
            'memory_tip': "Think \"re-\" (again) + \"cover\" + \"y\" = getting covered/protected again.",
            'example_sentence': "Her ___ from the surgery was faster than the doctors expected."
        },
        'recreant': {
            'definition': "Cowardly; unfaithful to duty or allegiance; a person who shows disloyalty or cowardice. Recreant describes someone who fails to meet expectations of courage, loyalty, or moral duty, often abandoning principles under pressure.",
            'pronunciation': "/ˈrekrɪənt/",
            'pronunciation_respelling': "REK-ree-uhnt",
            'etymology': "From Old French \"recreant,\" from \"recreire\" (to surrender), from Latin \"re-\" (back) + \"credere\" (to believe).",
            'memory_tip': "Think \"re-\" (back) + \"credent\" (believing) = going back on beliefs = disloyal.",
            'example_sentence': "The knight was branded a ___ for fleeing from battle."
        },
        'recriminatory': {
            'definition': "Involving or characterized by recrimination; making counter-accusations in response to accusations. Recriminatory behavior involves blaming others in return when one is blamed, creating cycles of mutual accusation and defensiveness.",
            'pronunciation': "/rɪˈkrɪmɪnəˌtɔri/",
            'pronunciation_respelling': "ri-KRIM-uh-nuh-tor-ee",
            'etymology': "From \"recriminate\" + suffix \"-ory,\" from Latin \"recriminari\" (to accuse in return).",
            'memory_tip': "Think \"re-\" (back) + \"criminal\" + \"atory\" = accusing back like criminals.",
            'example_sentence': "The divorce proceedings became increasingly ___ as both parties blamed each other."
        },
        'recrudescent': {
            'definition': "Breaking out again; recurring after a period of inactivity or dormancy, especially referring to diseases or undesirable conditions. Recrudescence implies a return of something negative that had been dormant or seemingly resolved.",
            'pronunciation': "/ˌriːkruˈdesənt/",
            'pronunciation_respelling': "ree-kroo-DES-uhnt",
            'etymology': "From Latin \"recrudescere,\" from \"re-\" (again) + \"crudus\" (raw) + \"-escent\" (becoming).",
            'memory_tip': "Think \"re-\" (again) + \"crude\" + \"escent\" = becoming raw/bad again.",
            'example_sentence': "The doctor was concerned about the ___ infection despite the antibiotics."
        },
        'recruit': {
            'definition': "To enlist someone to join an organization, especially the military; a newly enlisted member; to form or strengthen with new members. Recruitment involves actively seeking and enrolling people for specific purposes or organizations.",
            'pronunciation': "/rɪˈkrut/",
            'pronunciation_respelling': "ri-KROOT",
            'etymology': "From French \"recrute,\" from \"recroître\" (to grow again), from Latin \"re-\" (again) + \"crescere\" (to grow).",
            'memory_tip': "Think \"re-\" (again) + \"cruit\" (growth) = growing the group again.",
            'example_sentence': "The college coach traveled nationwide to ___ talented basketball players."
        },
        'recruittableau': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'recruit' + 'tableau' incorrectly joined. 'Recruit' means to enlist new members, while 'tableau' refers to a vivid or graphic description or a static scene. These should be separate words.]",
            'pronunciation': "/rɪˈkrut ˈtæbloʊ/",
            'pronunciation_respelling': "ri-KROOT TAB-loh",
            'etymology': "Combined word error: 'recruit' from French + 'tableau' from French.",
            'memory_tip': "Error combination: recruit (enlisting) + tableau (scene) - should be separate.",
            'example_sentence': "The military ___ displayed a ___ showing different career paths."
        },
        'rectitude': {
            'definition': "Morally correct behavior or thinking; righteousness; the quality of being honest, moral, and having strong ethical principles. Rectitude encompasses both moral integrity and the consistent application of ethical standards in behavior and decision-making.",
            'pronunciation': "/ˈrektɪˌtud/",
            'pronunciation_respelling': "REK-ti-tood",
            'etymology': "From Latin \"rectitudo,\" from \"rectus\" (straight, right) + \"-tude\" (state of).",
            'memory_tip': "Think \"rect\" (straight/right) + \"itude\" = state of being morally straight.",
            'example_sentence': "Her moral ___ made her the obvious choice for the ethics committee."
        },
        'recumbent': {
            'definition': "Lying down; reclining; in a position of rest or relaxation. Recumbent describes a horizontal or resting position, often used in medical contexts, art descriptions, or to describe specialized equipment like recumbent bicycles.",
            'pronunciation': "/rɪˈkʌmbənt/",
            'pronunciation_respelling': "ri-KUHM-buhnt",
            'etymology': "From Latin \"recumbens,\" from \"recumbere\" (to lie down), from \"re-\" (back) + \"cumbere\" (to lie).",
            'memory_tip': "Think \"re-\" (back) + \"cumbent\" (lying) = lying back down.",
            'example_sentence': "The ___ bicycle allowed her to ride comfortably despite her back problems."
        },
        'recuperation': {
            'definition': "The process of recovering from illness, exertion, or other adverse conditions; restoration to health or strength. Recuperation involves gradual healing and restoration of normal function, whether physical, mental, or emotional.",
            'pronunciation': "/rɪˌkupəˈreɪʃən/",
            'pronunciation_respelling': "ri-koo-puh-RAY-shuhn",
            'etymology': "From Latin \"recuperatio,\" from \"recuperare\" (to recover), from \"re-\" (again) + \"capere\" (to take).",
            'memory_tip': "Think \"re-\" (again) + \"cuper\" + \"ation\" = taking back one's strength.",
            'example_sentence': "The athlete's ___ from the injury took longer than expected."
        },
        'recusancy': {
            'definition': "Refusal to submit to authority or comply with a regulation, especially historical refusal of English Catholics to attend Church of England services. Recusancy represents principled resistance to religious or political conformity.",
            'pronunciation': "/ˈrekjʊzənsi/",
            'pronunciation_respelling': "REK-yoo-zuhn-see",
            'etymology': "From Latin \"recusare\" (to refuse) + suffix \"-ancy\" (state of).",
            'memory_tip': "Think \"recuse\" (refuse/reject) + \"ancy\" = state of refusing.",
            'example_sentence': "Catholic ___ in Tudor England often resulted in severe penalties."
        },
        'recyclable': {
            'definition': "Able to be recycled; capable of being processed and reused in the manufacture of new products. Recyclable materials can be collected, processed, and transformed into new items, reducing waste and conserving resources.",
            'pronunciation': "/riˈsaɪkləbəl/",
            'pronunciation_respelling': "ree-SAHY-kluh-buhl",
            'etymology': "From \"recycle\" + suffix \"-able\" (capable of), from \"re-\" (again) + \"cycle\" (circular process).",
            'memory_tip': "Think \"recycle\" + \"able\" = able to be cycled through again.",
            'example_sentence': "All ___ containers should be placed in the blue bin for collection."
        },
        'reddish': {
            'definition': "Having a red tinge or somewhat red in color; tinged with red. Reddish describes colors that contain red as a component but are not purely red, often appearing as combinations like reddish-brown or reddish-orange.",
            'pronunciation': "/ˈredɪʃ/",
            'pronunciation_respelling': "RED-ish",
            'etymology': "From \"red\" + suffix \"-ish\" (having the quality of).",
            'memory_tip': "Think \"red\" + \"ish\" = somewhat like red in color.",
            'example_sentence': "The autumn leaves displayed beautiful ___ and golden hues."
        },
        'redemption': {
            'definition': "The action of saving or being saved from sin, error, or evil; the action of regaining possession of something in exchange for payment; compensation for fault or failure. Redemption can be religious, financial, or moral in nature.",
            'pronunciation': "/rɪˈdempʃən/",
            'pronunciation_respelling': "ri-DEMP-shuhn",
            'etymology': "From Latin \"redemptio,\" from \"redimere\" (to buy back), from \"re-\" (back) + \"emere\" (to buy).",
            'memory_tip': "Think \"re-\" (back) + \"deem\" + \"tion\" = buying back one's worth.",
            'example_sentence': "The story focused on the character's quest for personal ___."
        },
        'redingote': {
            'definition': "A long coat or dress with a fitted bodice and full skirt, worn by women in the 18th and 19th centuries; originally a man's long riding coat. The redingote was adapted from men's fashion into women's wear, becoming an elegant outer garment.",
            'pronunciation': "/ˈredɪŋˌɡoʊt/",
            'pronunciation_respelling': "RED-ing-goht",
            'etymology': "From French \"redingote,\" adaptation of English \"riding coat.\"",
            'memory_tip': "Think \"riding coat\" adapted into French fashion = redingote.",
            'example_sentence': "The museum displayed an elegant 19th-century ___ made of burgundy velvet."
        },
        'redolent': {
            'definition': "Strongly reminiscent or suggestive of something; having a strong, pleasant smell. Redolent can refer to literal scents that evoke memories or metaphorical associations that strongly suggest particular qualities or memories.",
            'pronunciation': "/ˈredələnt/",
            'pronunciation_respelling': "RED-uh-luhnt",
            'etymology': "From Latin \"redolere,\" from \"re-\" (back) + \"olere\" (to smell).",
            'memory_tip': "Think \"re-\" (back) + \"odor\" + \"lent\" = bringing back smells/memories.",
            'example_sentence': "The old library was ___ of leather bindings and aged paper."
        },
        'redound': {
            'definition': "To contribute greatly to a person's credit or honor; to have an effect or consequence, especially a good one. Redound suggests that actions or qualities result in benefit, reputation, or positive outcomes for someone.",
            'pronunciation': "/rɪˈdaʊnd/",
            'pronunciation_respelling': "ri-DOWND",
            'etymology': "From Latin \"redundare,\" from \"re-\" (back) + \"undare\" (to surge).",
            'memory_tip': "Think \"re-\" (back) + \"ound\" (sound) = good effects coming back like echoes.",
            'example_sentence': "His charitable works will ___ to his credit in the community."
        },
        'reduce': {
            'definition': "To make smaller or less in amount, degree, or size; to bring to a lower or weaker state; to simplify or break down into constituent parts. Reduction involves decreasing quantity, intensity, complexity, or importance.",
            'pronunciation': "/rɪˈdus/",
            'pronunciation_respelling': "ri-DOOS",
            'etymology': "From Latin \"reducere,\" from \"re-\" (back) + \"ducere\" (to lead).",
            'memory_tip': "Think \"re-\" (back) + \"duce\" (lead) = leading back to smaller size.",
            'example_sentence': "The new medication helped ___ his blood pressure significantly."
        },
        'redux': {
            'definition': "Brought back; revived; denoting a film, book, or other creative work that revives an earlier successful work. Redux suggests a return to earlier themes, styles, or subject matter, often with contemporary updates or perspectives.",
            'pronunciation': "/ˈridʌks/",
            'pronunciation_respelling': "REE-duhks",
            'etymology': "From Latin \"redux,\" meaning \"brought back,\" from \"re-\" (back) + \"ducere\" (to lead).",
            'memory_tip': "Think \"re-\" (back) + \"dux\" (leader) = brought back/revived.",
            'example_sentence': "The director's latest film was essentially Hamlet ___."
        },
        'reeds': {
            'definition': "Plural of reed; tall, slender plants that grow in wet areas; thin pieces of cane or metal in musical instruments that vibrate to produce sound. Reeds are both natural plants and essential components of woodwind instruments.",
            'pronunciation': "/rids/",
            'pronunciation_respelling': "REEDZ",
            'etymology': "Plural of \"reed,\" from Old English \"hreod,\" of Germanic origin.",
            'memory_tip': "Think of tall plants swaying in wetlands or vibrating in clarinets.",
            'example_sentence': "The clarinet player replaced the worn ___ before the concert."
        },
        'reenactment': {
            'definition': "The action of acting out a past event; a performance or recreation of historical events, often for educational or commemorative purposes. Reenactments involve careful recreation of clothing, equipment, and circumstances to authentically portray historical periods.",
            'pronunciation': "/ˌriɪˈnæktmənt/",
            'pronunciation_respelling': "ree-ih-NAKT-muhnt",
            'etymology': "From \"re-\" (again) + \"enactment,\" from \"enact\" (to perform) + \"-ment\" (action of).",
            'memory_tip': "Think \"re-\" (again) + \"enact\" + \"ment\" = acting out again.",
            'example_sentence': "The Civil War ___ drew thousands of spectators to the battlefield."
        },
        'refectory': {
            'definition': "A dining room in a monastery, convent, college, or other institution; a communal eating hall. Refectories are typically large spaces designed for group dining, often featuring long tables and simple, functional architecture.",
            'pronunciation': "/rɪˈfektəri/",
            'pronunciation_respelling': "ri-FEK-tuh-ree",
            'etymology': "From Latin \"refectorium,\" from \"reficere\" (to restore), from \"re-\" (again) + \"facere\" (to make).",
            'memory_tip': "Think \"re-\" (again) + \"fect\" (make) + \"ory\" = place to remake/restore oneself with food.",
            'example_sentence': "The monastery's ___ served simple meals to the resident monks."
        },
        'refer': {
            'definition': "To mention or allude to; to direct attention to something; to send someone to a specialist or expert for help. Reference involves directing attention, making connections, or transferring responsibility to appropriate sources.",
            'pronunciation': "/rɪˈfɜr/",
            'pronunciation_respelling': "ri-FUR",
            'etymology': "From Latin \"referre,\" from \"re-\" (back) + \"ferre\" (to carry).",
            'memory_tip': "Think \"re-\" (back) + \"fer\" (carry) = carrying back to a source.",
            'example_sentence': "Please ___ to page 47 for the detailed instructions."
        },
        'reference': {
            'definition': "The action of mentioning or alluding to something; a source of information; a statement testifying to someone's character or qualifications. References provide evidence, support, or connections to external sources or authorities.",
            'pronunciation': "/ˈrefərəns/",
            'pronunciation_respelling': "REF-ur-uhns",
            'etymology': "From \"refer\" + suffix \"-ence\" (state of), from Latin \"referre\" (to carry back).",
            'memory_tip': "Think \"refer\" + \"ence\" = the act of referring to something.",
            'example_sentence': "The research paper included over fifty scholarly ___."
        },
        'referendum': {
            'definition': "A general vote by the electorate on a single political question; a process of referring a political question to the electorate for direct decision. Referendums allow citizens to vote directly on specific issues rather than through representatives.",
            'pronunciation': "/ˌrefəˈrendəm/",
            'pronunciation_respelling': "ref-uh-REN-duhm",
            'etymology': "From Latin \"referendum,\" meaning \"something to be referred,\" from \"referre\" (to refer).",
            'memory_tip': "Think \"refer\" + \"endum\" = something to be referred to the people.",
            'example_sentence': "The constitutional amendment was decided by a national ___."
        },
        'referralaerials': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'referral' + 'aerials' incorrectly joined. 'Referral' means directing someone to another source, while 'aerials' refers to antennas or aerial maneuvers. These should be separate words.]",
            'pronunciation': "/rɪˈfɜrəl ˈɛriəlz/",
            'pronunciation_respelling': "ri-FUR-uhl AIR-ee-uhlz",
            'etymology': "Combined word error: 'referral' from 'refer' + 'aerials' from 'aerial'.",
            'memory_tip': "Error combination: referral (directing to source) + aerials (antennas) - should be separate.",
            'example_sentence': "The doctor's ___ led to treatment, while the TV ___ needed adjustment."
        },
        'referred': {
            'definition': "Past tense of refer; mentioned or alluded to; directed to another source or person for information or treatment. Being referred typically involves having one's case or inquiry transferred to someone with appropriate expertise or authority.",
            'pronunciation': "/rɪˈfɜrd/",
            'pronunciation_respelling': "ri-FURD",
            'etymology': "Past tense of \"refer,\" from Latin \"referre\" (to carry back).",
            'memory_tip': "Think \"refer\" + \"red\" (past tense ending) = was directed to.",
            'example_sentence': "She was ___ to a specialist for further examination."
        },
        'reflect': {
            'definition': "To throw back light, heat, or sound without absorbing it; to think deeply or carefully about something; to show or express a particular quality or characteristic. Reflection can be physical (mirrors) or mental (contemplation).",
            'pronunciation': "/rɪˈflekt/",
            'pronunciation_respelling': "ri-FLEKT",
            'etymology': "From Latin \"reflectere,\" from \"re-\" (back) + \"flectere\" (to bend).",
            'memory_tip': "Think \"re-\" (back) + \"flect\" (bend) = bending back light or thoughts.",
            'example_sentence': "The calm lake surface perfectly ___ the surrounding mountains."
        },
        'reflection': {
            'definition': "The throwing back of light, heat, or sound by a surface; serious thought or consideration; an image seen in a mirror or shiny surface. Reflection encompasses both physical phenomena and mental processes of contemplation.",
            'pronunciation': "/rɪˈflekʃən/",
            'pronunciation_respelling': "ri-FLEK-shuhn",
            'etymology': "From \"reflect\" + suffix \"-ion\" (action of), from Latin \"reflectere\" (to bend back).",
            'memory_tip': "Think \"reflect\" + \"ion\" = the action of reflecting.",
            'example_sentence': "Her ___ in the window showed her deep concentration."
        },
        'reflects': {
            'definition': "Third person singular present tense of reflect; throws back light, heat, or sound; shows or expresses particular qualities; thinks deeply about something. Current action of reflecting either physically or mentally.",
            'pronunciation': "/rɪˈflekts/",
            'pronunciation_respelling': "ri-FLEKTS",
            'etymology': "Third person singular of \"reflect,\" from Latin \"reflectere\" (to bend back).",
            'memory_tip': "Think \"reflect\" + \"s\" = currently reflecting back.",
            'example_sentence': "The mirror ___ light throughout the small room."
        },
        'reflexology': {
            'definition': "A system of massage used to relieve tension and treat illness, based on the theory that specific areas of feet, hands, and ears correspond to organs and structures of the body. Reflexology practitioners apply pressure to these reflex points.",
            'pronunciation': "/ˌriflekˈsɑlədʒi/",
            'pronunciation_respelling': "ree-flek-SOL-uh-jee",
            'etymology': "From \"reflex\" + suffix \"-ology\" (study of), from Latin \"reflexus\" (bent back).",
            'memory_tip': "Think \"reflex\" + \"ology\" = study of reflex points in body.",
            'example_sentence': "She studied ___ to help clients relax and reduce stress."
        },
        'refrain': {
            'definition': "To abstain from doing or indulging in something; a repeated line or phrase in a song or poem, especially at the end of verses. Refrain can mean self-restraint or a recurring musical/poetic element.",
            'pronunciation': "/rɪˈfreɪn/",
            'pronunciation_respelling': "ri-FRAYN",
            'etymology': "From Old French \"refraindre,\" from Latin \"refrenare,\" from \"re-\" (back) + \"frenum\" (bridle).",
            'memory_tip': "Think \"re-\" (back) + \"frain\" (bridle) = holding oneself back, or recurring phrase.",
            'example_sentence': "Please ___ from smoking in the building."
        },
        'refrigerant': {
            'definition': "A substance used for refrigeration; a fluid used in heat pumps and refrigeration cycles to absorb and remove heat. Refrigerants undergo phase changes between liquid and gas to transfer heat energy in cooling systems.",
            'pronunciation': "/rɪˈfrɪdʒərənt/",
            'pronunciation_respelling': "ri-FRIJ-ur-uhnt",
            'etymology': "From \"refrigerate\" + suffix \"-ant\" (performing action), from Latin \"refrigerare\" (to cool).",
            'memory_tip': "Think \"refrigerate\" + \"ant\" = substance that refrigerates.",
            'example_sentence': "The technician checked the ___ levels in the air conditioning system."
        },
        'refrigerated': {
            'definition': "Past tense of refrigerate; cooled by artificial means; kept at low temperature to preserve freshness. Refrigerated items have been subjected to controlled cooling to slow spoilage and maintain quality.",
            'pronunciation': "/rɪˈfrɪdʒəˌreɪtɪd/",
            'pronunciation_respelling': "ri-FRIJ-uh-ray-tid",
            'etymology': "Past tense of \"refrigerate,\" from Latin \"refrigeratus,\" from \"refrigerare\" (to cool).",
            'memory_tip': "Think \"refrigerate\" + \"ed\" = was cooled/chilled.",
            'example_sentence': "The ___ truck delivered fresh produce to the grocery store."
        },
        'refuge': {
            'definition': "A condition of being safe or sheltered from pursuit, danger, or trouble; a place or situation providing safety or shelter. Refuge implies protection from harm, whether physical, emotional, or circumstantial.",
            'pronunciation': "/ˈrefjudʒ/",
            'pronunciation_respelling': "REF-yooj",
            'etymology': "From Old French \"refuge,\" from Latin \"refugium,\" from \"refugere\" (to flee back).",
            'memory_tip': "Think \"re-\" (back) + \"fuge\" (flee) = fleeing back to safety.",
            'example_sentence': "The mountain cabin served as a peaceful ___ from city life."
        },
        'refugium': {
            'definition': "An area where relict populations of organisms survive through periods of unfavorable conditions; a biogeographic region that has remained relatively unchanged. Refugia are important for biodiversity conservation and evolutionary studies.",
            'pronunciation': "/rɪˈfjudʒiəm/",
            'pronunciation_respelling': "ri-FYOO-jee-uhm",
            'etymology': "From Latin \"refugium,\" from \"refugere\" (to flee back), from \"re-\" (back) + \"fugere\" (to flee).",
            'memory_tip': "Think \"refuge\" + \"ium\" = scientific place of refuge for species.",
            'example_sentence': "The isolated valley served as a ___ for rare plant species during the ice age."
        },
        'refugiumremuda': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'refugium' + 'remuda' incorrectly joined. 'Refugium' refers to a safe area for organisms, while 'remuda' is a herd of horses. These should be separate words.]",
            'pronunciation': "/rɪˈfjudʒiəm rɪˈmudə/",
            'pronunciation_respelling': "ri-FYOO-jee-uhm ri-MOO-duh",
            'etymology': "Combined word error: 'refugium' from Latin + 'remuda' from Spanish.",
            'memory_tip': "Error combination: refugium (safe area) + remuda (horse herd) - should be separate.",
            'example_sentence': "The ___ protected the species while the ___ grazed nearby."
        },
        'regales': {
            'definition': "Third person singular present tense of regale; entertains with stories; provides with abundant food and drink. To regale someone involves delighting them with entertaining accounts or lavish hospitality.",
            'pronunciation': "/rɪˈɡeɪlz/",
            'pronunciation_respelling': "ri-GAYLZ",
            'etymology': "Third person singular of \"regale,\" from French \"régaler\" (to feast).",
            'memory_tip': "Think \"regal\" + \"es\" = provides royal treatment/entertainment.",
            'example_sentence': "The storyteller ___ the audience with tales of adventure."
        },
        'regalia': {
            'definition': "The ceremonial clothes and items worn or carried by rulers on state occasions; special clothes or items associated with a particular office, rank, or organization. Regalia symbolize authority, tradition, and ceremonial importance.",
            'pronunciation': "/rɪˈɡeɪliə/",
            'pronunciation_respelling': "ri-GAY-lee-uh",
            'etymology': "From Latin \"regalia,\" plural of \"regalis\" (regal), from \"rex\" (king).",
            'memory_tip': "Think \"regal\" + \"ia\" = royal items and ceremonial dress.",
            'example_sentence': "The crown jewels and other royal ___ were displayed in the museum."
        },
        'reggae': {
            'definition': "A style of popular music originating in Jamaica, characterized by a strong rhythmic beat and often dealing with social and political themes. Reggae emerged in the late 1960s and gained international popularity through artists like Bob Marley.",
            'pronunciation': "/ˈreɡeɪ/",
            'pronunciation_respelling': "REG-ay",
            'etymology': "Of uncertain origin, possibly from Jamaican English, perhaps related to \"rege-rege\" (quarrel).",
            'memory_tip': "Think of the distinctive rhythm and Jamaican origins of this music style.",
            'example_sentence': "The ___ festival featured both classic and contemporary Jamaican artists."
        },
        'regicide': {
            'definition': "The action of killing a king; a person who kills or takes part in killing a king. Regicide represents one of the most serious political crimes in monarchical systems, often resulting in dramatic historical consequences.",
            'pronunciation': "/ˈredʒɪˌsaɪd/",
            'pronunciation_respelling': "REJ-ih-sahyd",
            'etymology': "From Latin \"rex\" (king) + \"-cide\" (killer), from \"caedere\" (to kill).",
            'memory_tip': "Think \"regi\" (king) + \"cide\" (kill) = killing a king.",
            'example_sentence': "The execution of Charles I was considered ___ by royalist supporters."
        },
        'regiment': {
            'definition': "A permanent unit of an army typically commanded by a colonel; to organize according to a strict system; to subject to strict discipline or order. Regiments are military organizational units and the term also means strict systematic control.",
            'pronunciation': "/ˈredʒɪmənt/",
            'pronunciation_respelling': "REJ-ih-muhnt",
            'etymology': "From Latin \"regimentum\" (rule, government), from \"regere\" (to rule).",
            'memory_tip': "Think \"regi\" (rule) + \"ment\" = organized ruling unit or strict system.",
            'example_sentence': "The infantry ___ was deployed to the front lines."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_146_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_146_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['recruittableau', 'referralaerials', 'refugiumremuda']
    
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
                    'notes': 'Batch 146 processing',
                    'review_status': 'pending',
                    'batch_number': '146'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 146 processing complete!")
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