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
            'regular': ['register', 'rehearsal', 'release', 'relief', 'relish', 'rely', 'remain', 'remember', 'rental'],
            'semi_regular': ['registrar', 'reign', 'reindeer', 'related', 'relating', 'relative', 'relegated', 'reliable', 'religious', 'reluctant', 'remaining', 'remarkable', 'remedial', 'remnants', 'renowned'],
            'irregular': ['regnal', 'regurgitate', 'reimbursable', 'reiterate', 'rejoinder', 'rejuvenate', 'reminiscent', 'remonstrance', 'remorseful', 'remuneration', 'renegotiate', 'renewable', 'renitency', 'renminbi', 'rennet', 'renvoi']
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
        high_frequency = ['register', 'release', 'relief', 'religious', 'remember', 'remain', 'related', 'relating', 'relative', 'reliable', 'remarkable', 'rental']
        medium_frequency = ['registrar', 'rehearsal', 'reign', 'reindeer', 'relegated', 'relish', 'reluctant', 'rely', 'remaining', 'remedial', 'reminiscent', 'remnants', 'renowned', 'renewable']
        low_frequency = ['regnal', 'regurgitate', 'reimbursable', 'reiterate', 'rejoinder', 'rejuvenate', 'relentlessly', 'rembrandt', 'remonstrance', 'remorseful', 'remuda', 'remuneration', 'renal', 'rendition', 'renegotiate', 'renitency', 'renminbi', 'rennet', 'renvoi']
        
        if word in high_frequency:
            return 2
        elif word in medium_frequency:
            return 5
        elif word in low_frequency:
            return 8
        else:
            return 7
    
    def _calculate_morphological_complexity(self, word):
        simple_words = ['register', 'reign', 'rely', 'remain', 'relief', 'relish', 'rental', 'renal']
        moderate_words = ['registrar', 'rehearsal', 'reindeer', 'release', 'related', 'relating', 'relative', 'relegated', 'reliable', 'religious', 'reluctant', 'remaining', 'remarkable', 'remember', 'reminiscent', 'remnants', 'renowned', 'renewable', 'rennet']
        complex_words = ['regnal', 'regurgitate', 'reimbursable', 'reiterate', 'rejoinder', 'rejuvenate', 'relentlessly', 'rembrandt', 'remedial', 'remonstrance', 'remorseful', 'remuda', 'remuneration', 'rendition', 'renegotiate', 'renitency', 'renminbi', 'renvoi']
        
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
        'register': {
            'definition': "A formal list or record of names or items; to record formally and officially; to show or express an emotion. Registers can be physical books, electronic databases, or vocal ranges in music, and the act involves official documentation or emotional display.",
            'pronunciation': "/ˈredʒɪstər/",
            'pronunciation_respelling': "REJ-ih-stur",
            'etymology': "From Latin \"registrum,\" from \"regere\" (to rule) + \"gerere\" (to carry).",
            'memory_tip': "Think \"reg\" (rule) + \"ister\" = ruled list/record.",
            'example_sentence': "Please ___ your name on the attendance sheet before entering."
        },
        'registrar': {
            'definition': "An official responsible for keeping a register or official records; a senior administrative officer in a university or college; a qualified doctor who is training to be a specialist. Registrars maintain official documentation and records in various institutions.",
            'pronunciation': "/ˌredʒɪˈstrɑr/",
            'pronunciation_respelling': "rej-ih-STRAR",
            'etymology': "From \"register\" + suffix \"-ar\" (one who), from Latin \"registrarius.\"",
            'memory_tip': "Think \"register\" + \"ar\" = one who registers/keeps records.",
            'example_sentence': "The university ___ verified all student transcripts before graduation."
        },
        'regnal': {
            'definition': "Of or concerning a reign or the years of a sovereign's rule; relating to the period during which a monarch rules. Regnal years are used in historical dating systems to mark events during specific monarchical reigns.",
            'pronunciation': "/ˈreɡnəl/",
            'pronunciation_respelling': "REG-nuhl",
            'etymology': "From Latin \"regnalis,\" from \"regnum\" (kingdom), from \"rex\" (king).",
            'memory_tip': "Think \"reign\" + \"al\" = relating to a king's reign.",
            'example_sentence': "The historian calculated the event occurred in the fifteenth ___ year of the monarch."
        },
        'regnalattaché': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'regnal' + 'attaché' incorrectly joined. 'Regnal' relates to a sovereign's reign, while 'attaché' refers to a diplomatic officer. These should be separate words.]",
            'pronunciation': "/ˈreɡnəl ˌætəˈʃeɪ/",
            'pronunciation_respelling': "REG-nuhl at-uh-SHAY",
            'etymology': "Combined word error: 'regnal' from Latin + 'attaché' from French.",
            'memory_tip': "Error combination: regnal (royal reign) + attaché (diplomat) - should be separate.",
            'example_sentence': "The ___ records were maintained by the diplomatic ___."
        },
        'regurgitate': {
            'definition': "To bring swallowed food up again to the mouth; to repeat information without understanding or analyzing it. Regurgitation can be biological (bringing up food) or metaphorical (mechanically repeating information without comprehension).",
            'pronunciation': "/rɪˈɡɜrdʒɪˌteɪt/",
            'pronunciation_respelling': "ri-GUR-ji-tayt",
            'etymology': "From Latin \"regurgitare,\" from \"re-\" (back) + \"gurges\" (whirlpool).",
            'memory_tip': "Think \"re-\" (back) + \"gurgitate\" (whirlpool) = bringing back up.",
            'example_sentence': "Students shouldn't just ___ facts but should analyze and understand them."
        },
        'rehearsal': {
            'definition': "A practice performance of a play, concert, or other work for later public performance; a trial performance or run-through. Rehearsals allow performers to practice, refine timing, and prepare for actual performances.",
            'pronunciation': "/rɪˈhɜrsəl/",
            'pronunciation_respelling': "ri-HUR-suhl",
            'etymology': "From \"rehearse\" + suffix \"-al,\" from Old French \"rehercier\" (to repeat).",
            'memory_tip': "Think \"re-\" (again) + \"hearsal\" (hearing) = hearing again for practice.",
            'example_sentence': "The orchestra scheduled a final ___ before opening night."
        },
        'reign': {
            'definition': "The period during which a sovereign rules; to hold royal office; to be the dominant feature or influence. Reign can refer to monarchical rule or metaphorical dominance in any field or situation.",
            'pronunciation': "/reɪn/",
            'pronunciation_respelling': "RAYN",
            'etymology': "From Old French \"regne,\" from Latin \"regnum\" (kingdom), from \"rex\" (king).",
            'memory_tip': "Think of a king's rule - sounds like \"rain\" but spelled with \"gn.\"",
            'example_sentence': "Queen Victoria's ___ lasted for over sixty years."
        },
        'reigndifficulty': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'reign' + 'difficulty' incorrectly joined. 'Reign' refers to a monarch's rule, while 'difficulty' means something hard to accomplish. These should be separate words.]",
            'pronunciation': "/reɪn ˈdɪfɪkəlti/",
            'pronunciation_respelling': "RAYN DIF-ih-kuhl-tee",
            'etymology': "Combined word error: 'reign' from Latin + 'difficulty' from Latin.",
            'memory_tip': "Error combination: reign (royal rule) + difficulty (hardship) - should be separate.",
            'example_sentence': "The monarch's ___ faced numerous political ___."
        },
        'reimbursable': {
            'definition': "Eligible for reimbursement; capable of being repaid or compensated. Reimbursable expenses are those that an organization agrees to pay back to individuals who initially covered the costs on behalf of the organization.",
            'pronunciation': "/ˌriɪmˈbɜrsəbəl/",
            'pronunciation_respelling': "ree-im-BUR-suh-buhl",
            'etymology': "From \"reimburse\" + suffix \"-able,\" from \"re-\" (back) + \"imburse\" (to put in purse).",
            'memory_tip': "Think \"re-\" (back) + \"imburse\" (purse) + \"able\" = able to put back in purse.",
            'example_sentence': "Business travel expenses are ___ with proper receipts and documentation."
        },
        'reindeer': {
            'definition': "A deer of the tundra and subarctic regions, domesticated in northern Eurasia and wild in North America where it is called caribou. Reindeer are known for their adaptations to cold climates and their use by Arctic peoples for transportation and sustenance.",
            'pronunciation': "/ˈreɪnˌdɪr/",
            'pronunciation_respelling': "RAYN-deer",
            'etymology': "From Old Norse \"hreindýr,\" from \"hreinn\" (reindeer) + \"dýr\" (deer).",
            'memory_tip': "Think \"rain\" + \"deer\" = deer that live where it's cold like freezing rain.",
            'example_sentence': "The Sami people have herded ___ across the Arctic tundra for centuries."
        },
        'reiterate': {
            'definition': "To say something again or repeatedly, typically for emphasis or clarity. Reiteration involves restating important points to ensure understanding, emphasize significance, or clarify meaning through repetition.",
            'pronunciation': "/riˈɪtəˌreɪt/",
            'pronunciation_respelling': "ree-IT-uh-rayt",
            'etymology': "From Latin \"reiterare,\" from \"re-\" (again) + \"iterare\" (to repeat).",
            'memory_tip': "Think \"re-\" (again) + \"iterate\" (repeat) = repeat again.",
            'example_sentence': "Let me ___ the importance of following safety procedures."
        },
        'reiterateremorseful': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'reiterate' + 'remorseful' incorrectly joined. 'Reiterate' means to repeat, while 'remorseful' means feeling regret. These should be separate words.]",
            'pronunciation': "/riˈɪtəˌreɪt rɪˈmɔrsfəl/",
            'pronunciation_respelling': "ree-IT-uh-rayt ri-MORS-fuhl",
            'etymology': "Combined word error: 'reiterate' from Latin + 'remorseful' from Latin.",
            'memory_tip': "Error combination: reiterate (repeat) + remorseful (regretful) - should be separate.",
            'example_sentence': "He continued to ___ his apology, appearing genuinely ___."
        },
        'rejoinder': {
            'definition': "A sharp, clever, or witty reply, especially to criticism; a defendant's response to a plaintiff's reply in legal proceedings. Rejoinders are typically quick responses that counter previous statements with wit or legal argumentation.",
            'pronunciation': "/rɪˈdʒɔɪndər/",
            'pronunciation_respelling': "ri-JOYN-dur",
            'etymology': "From French \"rejoindre,\" from \"re-\" (back) + \"joindre\" (to join).",
            'memory_tip': "Think \"re-\" (back) + \"join\" + \"der\" = joining back with a response.",
            'example_sentence': "Her witty ___ to the critic's comment drew laughter from the audience."
        },
        'rejuvenate': {
            'definition': "To make or become young again; to give new energy or vigor to something. Rejuvenation involves restoration of youthful qualities, whether physical appearance, energy levels, or organizational vitality.",
            'pronunciation': "/rɪˈdʒuvəˌneɪt/",
            'pronunciation_respelling': "ri-JOO-vuh-nayt",
            'etymology': "From Latin \"re-\" (again) + \"juvenis\" (young) + \"-ate\" (to make).",
            'memory_tip': "Think \"re-\" (again) + \"juvenile\" (young) = make young again.",
            'example_sentence': "The spa treatment promised to ___ her tired skin."
        },
        'related': {
            'definition': "Connected; having a logical or causal connection; belonging to the same family. Related items share common characteristics, origins, or connections that link them together in meaningful ways.",
            'pronunciation': "/rɪˈleɪtɪd/",
            'pronunciation_respelling': "ri-LAY-tid",
            'etymology': "Past participle of \"relate,\" from Latin \"relatus,\" from \"referre\" (to carry back).",
            'memory_tip': "Think \"relate\" + \"ed\" = connected or linked together.",
            'example_sentence': "These two scientific discoveries are closely ___ to each other."
        },
        'relating': {
            'definition': "Present participle of relate; having reference or connection to; establishing a connection between things. The process of connecting ideas, events, or people through shared characteristics or logical links.",
            'pronunciation': "/rɪˈleɪtɪŋ/",
            'pronunciation_respelling': "ri-LAY-ting",
            'etymology': "Present participle of \"relate,\" from Latin \"relatus,\" from \"referre\" (to carry back).",
            'memory_tip': "Think \"relate\" + \"ing\" = currently connecting or referring to.",
            'example_sentence': "The chapter ___ to environmental issues was particularly enlightening."
        },
        'relative': {
            'definition': "A person connected by blood or marriage; considered in relation to something else; not absolute but dependent on context. Relative can refer to family members or to comparative relationships between different things.",
            'pronunciation': "/ˈrelətɪv/",
            'pronunciation_respelling': "REL-uh-tiv",
            'etymology': "From Latin \"relativus,\" from \"relatus\" (related), from \"referre\" (to carry back).",
            'memory_tip': "Think \"relate\" + \"ive\" = relating to family or comparison.",
            'example_sentence': "My distant ___ from Scotland visited us last summer."
        },
        'release': {
            'definition': "To allow or enable to escape from confinement; to make available to the public; to free from something that restrains. Release involves liberation, whether physical, legal, emotional, or in terms of publication.",
            'pronunciation': "/rɪˈlis/",
            'pronunciation_respelling': "ri-LEES",
            'etymology': "From Old French \"relaissier,\" from Latin \"relaxare\" (to relax).",
            'memory_tip': "Think \"re-\" (away) + \"lease\" (let go) = let go away.",
            'example_sentence': "The prisoner was scheduled for ___ next month."
        },
        'relegated': {
            'definition': "Past tense of relegate; assigned to a lower position; demoted or transferred to a less important place or role. Relegation involves moving something or someone to a position of lesser importance or authority.",
            'pronunciation': "/ˈreləˌɡeɪtɪd/",
            'pronunciation_respelling': "REL-uh-gay-tid",
            'etymology': "Past tense of \"relegate,\" from Latin \"relegatus,\" from \"re-\" (away) + \"legare\" (to send).",
            'memory_tip': "Think \"re-\" (away) + \"leg\" (send) + \"ated\" = was sent away to lower position.",
            'example_sentence': "The team was ___ to a lower division after poor performance."
        },
        'relentlessly': {
            'definition': "In a harsh or inflexible manner; without pause or let-up; persistently and determinedly. Relentless action continues without mercy, rest, or change of intensity, often describing sustained effort or pressure.",
            'pronunciation': "/rɪˈlentləsli/",
            'pronunciation_respelling': "ri-LENT-lis-lee",
            'etymology': "From \"relentless\" + suffix \"-ly,\" from \"re-\" (again) + \"lent\" (soft) + \"-less\" (without).",
            'memory_tip': "Think \"re-\" + \"lent\" (soft) + \"less\" + \"ly\" = without softening, continuously.",
            'example_sentence': "She pursued her goals ___ despite numerous setbacks."
        },
        'reliable': {
            'definition': "Consistently good in quality or performance; able to be trusted or depended upon. Reliable people, systems, or information provide consistency and trustworthiness that others can count on in various situations.",
            'pronunciation': "/rɪˈlaɪəbəl/",
            'pronunciation_respelling': "ri-LYE-uh-buhl",
            'etymology': "From \"rely\" + suffix \"-able,\" from Old French \"relier\" (to bind).",
            'memory_tip': "Think \"rely\" + \"able\" = able to be relied upon.",
            'example_sentence': "She has proven to be a ___ employee who always meets deadlines."
        },
        'relief': {
            'definition': "A feeling of reassurance and relaxation following release from anxiety or distress; assistance given to those in need; a sculpture or carving that stands out from a flat background. Relief encompasses emotional comfort, aid, and artistic techniques.",
            'pronunciation': "/rɪˈlif/",
            'pronunciation_respelling': "ri-LEEF",
            'etymology': "From Old French \"relief,\" from \"relever\" (to raise up), from Latin \"relevare.\"",
            'memory_tip': "Think \"re-\" (away) + \"lief\" (burden) = taking burden away.",
            'example_sentence': "She felt immense ___ when the test results came back negative."
        },
        'religious': {
            'definition': "Relating to or believing in a religion; having or showing deep reverence for a deity and commitment to religious faith. Religious can describe formal organized worship, personal spiritual beliefs, or zealous devotion to principles.",
            'pronunciation': "/rɪˈlɪdʒəs/",
            'pronunciation_respelling': "ri-LIJ-uhs",
            'etymology': "From Latin \"religiosus,\" from \"religio\" (obligation, reverence).",
            'memory_tip': "Think \"religion\" + \"ous\" = characterized by religion.",
            'example_sentence': "The ___ ceremony brought the community together in prayer."
        },
        'relish': {
            'definition': "Great enjoyment or satisfaction; a pickled vegetable condiment; to enjoy greatly or take pleasure in something. Relish can be emotional enjoyment, a food accompaniment, or the act of savoring experiences.",
            'pronunciation': "/ˈrelɪʃ/",
            'pronunciation_respelling': "REL-ish",
            'etymology': "From Old French \"relais,\" meaning \"something remaining,\" from \"relaissier\" (to release).",
            'memory_tip': "Think of savoring and enjoying something with great pleasure.",
            'example_sentence': "He ate the hot dog with mustard and ___ at the baseball game."
        },
        'reluctant': {
            'definition': "Unwilling and hesitant; disinclined to do something; showing doubt or unwillingness. Reluctant behavior involves resistance or hesitation to engage in actions, often due to doubt, fear, or preference for alternatives.",
            'pronunciation': "/rɪˈlʌktənt/",
            'pronunciation_respelling': "ri-LUHK-tuhnt",
            'etymology': "From Latin \"reluctari,\" from \"re-\" (back) + \"luctari\" (to struggle).",
            'memory_tip': "Think \"re-\" (back) + \"luct\" (struggle) = struggling back against doing something.",
            'example_sentence': "She was ___ to accept the promotion because it required relocating."
        },
        'rely': {
            'definition': "To depend on with full trust or confidence; to be dependent on someone or something for support or help. Relying involves placing trust and confidence in others' abilities, promises, or reliability.",
            'pronunciation': "/rɪˈlaɪ/",
            'pronunciation_respelling': "ri-LYE",
            'etymology': "From Old French \"relier,\" from Latin \"religare,\" from \"re-\" (back) + \"ligare\" (to bind).",
            'memory_tip': "Think \"re-\" (back) + \"ly\" (bind) = bind oneself back to someone trustworthy.",
            'example_sentence': "You can always ___ on her to keep her promises."
        },
        'remain': {
            'definition': "To continue to exist; to stay in the same place; to be left after others have gone or been dealt with. Remaining involves persistence, continuation, or what is left after other elements have been removed or changed.",
            'pronunciation': "/rɪˈmeɪn/",
            'pronunciation_respelling': "ri-MAYN",
            'etymology': "From Old French \"remaindre,\" from Latin \"remanere,\" from \"re-\" (back) + \"manere\" (to stay).",
            'memory_tip': "Think \"re-\" (back) + \"main\" (stay) = stay back/continue to stay.",
            'example_sentence': "Only a few questions ___ to be answered on the test."
        },
        'remaining': {
            'definition': "Still existing; left over; continuing to exist after other parts have gone or been dealt with. Remaining items are those that persist after others have been removed, used, or processed.",
            'pronunciation': "/rɪˈmeɪnɪŋ/",
            'pronunciation_respelling': "ri-MAYN-ing",
            'etymology': "Present participle of \"remain,\" from Latin \"remanere\" (to stay behind).",
            'memory_tip': "Think \"remain\" + \"ing\" = currently staying/continuing to exist.",
            'example_sentence': "Please distribute the ___ cookies to the children."
        },
        'remarkable': {
            'definition': "Worthy of attention; striking or extraordinary; notably unusual or exceptional. Remarkable things stand out from the ordinary due to their exceptional qualities, unusual characteristics, or significant impact.",
            'pronunciation': "/rɪˈmɑrkəbəl/",
            'pronunciation_respelling': "ri-MAR-kuh-buhl",
            'etymology': "From \"remark\" + suffix \"-able,\" from French \"remarquer\" (to observe).",
            'memory_tip': "Think \"remark\" + \"able\" = worthy of being remarked upon.",
            'example_sentence': "Her recovery from the accident was ___."
        },
        'rembrandt': {
            'definition': "Rembrandt van Rijn (1606-1669), Dutch painter and etcher, one of the greatest masters of European art; relating to his distinctive style of painting with dramatic light and shadow. Used to describe artistic techniques reminiscent of his work.",
            'pronunciation': "/ˈrembrɑnt/",
            'pronunciation_respelling': "REM-brahnt",
            'etymology': "Dutch painter's name, from Germanic \"ragin\" (advice) + \"berht\" (bright).",
            'memory_tip': "Think of the famous Dutch master painter known for dramatic lighting.",
            'example_sentence': "The museum's ___ collection includes several of his most famous self-portraits."
        },
        'remedial': {
            'definition': "Giving or intended as a remedy; providing or intended as education for students with learning difficulties. Remedial measures are designed to correct problems, deficiencies, or educational gaps.",
            'pronunciation': "/rɪˈmidiəl/",
            'pronunciation_respelling': "ri-MEE-dee-uhl",
            'etymology': "From \"remedy\" + suffix \"-al,\" from Latin \"remedium\" (cure).",
            'memory_tip': "Think \"remedy\" + \"al\" = relating to providing a cure or fix.",
            'example_sentence': "Students who struggled with basic math were enrolled in ___ classes."
        },
        'remember': {
            'definition': "To have in or be able to bring to one's mind an awareness of someone or something from the past; to keep in mind for attention or consideration. Memory involves retrieval of stored information and experiences.",
            'pronunciation': "/rɪˈmembər/",
            'pronunciation_respelling': "ri-MEM-bur",
            'etymology': "From Old French \"remembrer,\" from Latin \"rememorari,\" from \"re-\" (again) + \"memor\" (mindful).",
            'memory_tip': "Think \"re-\" (again) + \"member\" (put together) = put together again in mind.",
            'example_sentence': "I can't ___ where I left my car keys."
        },
        'reminiscent': {
            'definition': "Tending to remind one of something; having characteristics that recall or suggest something else. Reminiscent things evoke memories or associations with past experiences, people, places, or other familiar elements.",
            'pronunciation': "/ˌreməˈnɪsənt/",
            'pronunciation_respelling': "rem-uh-NIS-uhnt",
            'etymology': "From Latin \"reminisci\" (to remember), from \"re-\" (again) + \"mens\" (mind).",
            'memory_tip': "Think \"re-\" (again) + \"mini\" (mind) + \"scent\" = bringing back to mind.",
            'example_sentence': "The music was ___ of her childhood summers at the lake."
        },
        'reminiscentmenial': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'reminiscent' + 'menial' incorrectly joined. 'Reminiscent' means recalling memories, while 'menial' refers to lowly work. These should be separate words.]",
            'pronunciation': "/ˌreməˈnɪsənt ˈminiəl/",
            'pronunciation_respelling': "rem-uh-NIS-uhnt MEE-nee-uhl",
            'etymology': "Combined word error: 'reminiscent' from Latin + 'menial' from Latin.",
            'memory_tip': "Error combination: reminiscent (recalling) + menial (lowly work) - should be separate.",
            'example_sentence': "The scene was ___ of her past, though the work seemed ___."
        },
        'remnants': {
            'definition': "Small remaining quantities of something; pieces of cloth left over after the greater part has been used; survivors of a group. Remnants are what remain after the majority has been used, destroyed, or dispersed.",
            'pronunciation': "/ˈremnənts/",
            'pronunciation_respelling': "REM-nuhnts",
            'etymology': "Plural of \"remnant,\" from Old French \"remanant,\" from \"remaindre\" (to remain).",
            'memory_tip': "Think \"remain\" + \"ants\" = small pieces that remain.",
            'example_sentence': "The fabric store sold ___ at discounted prices."
        },
        'remonstrance': {
            'definition': "A forcefully reproachful protest; an expression of strong disagreement or disapproval. Remonstrance involves formal objection or complaint, often regarding perceived injustice, error, or inappropriate behavior.",
            'pronunciation': "/rɪˈmɑnstrəns/",
            'pronunciation_respelling': "ri-MON-struhns",
            'etymology': "From Latin \"remonstrare,\" from \"re-\" (again) + \"monstrare\" (to show).",
            'memory_tip': "Think \"re-\" (again) + \"monstrate\" (show) = show again why something is wrong.",
            'example_sentence': "The citizens' ___ against the new tax was delivered to city hall."
        },
        'remorseful': {
            'definition': "Filled with deep regret or guilt for wrongdoing; showing sincere penitence. Remorseful feelings involve genuine sorrow and regret for past actions, typically accompanied by desire for forgiveness or redemption.",
            'pronunciation': "/rɪˈmɔrsfəl/",
            'pronunciation_respelling': "ri-MORS-fuhl",
            'etymology': "From \"remorse\" + suffix \"-ful,\" from Latin \"remorsus\" (biting back).",
            'memory_tip': "Think \"re-\" (back) + \"morse\" (bite) + \"ful\" = full of biting back guilt.",
            'example_sentence': "He appeared genuinely ___ for his harsh words."
        },
        'remuda': {
            'definition': "A herd of horses from which ranch hands select their mounts; the collection of saddle horses used on a ranch. Remudas are essential for cattle ranching operations, providing working horses for cowboys and ranch work.",
            'pronunciation': "/rɪˈmudə/",
            'pronunciation_respelling': "ri-MOO-duh",
            'etymology': "From Spanish \"remuda,\" from \"remudar\" (to change), from Latin \"re-\" (again) + \"mutare\" (to change).",
            'memory_tip': "Think \"re-\" (again) + \"muda\" (change) = changing horses again for work.",
            'example_sentence': "The cowboys selected fresh horses from the ___ for the day's cattle drive."
        },
        'remuneration': {
            'definition': "Money paid for work or a service; compensation or payment for employment or professional services. Remuneration encompasses salary, wages, fees, and other forms of payment for labor or professional services.",
            'pronunciation': "/rɪˌmjunəˈreɪʃən/",
            'pronunciation_respelling': "ri-myoo-nuh-RAY-shuhn",
            'etymology': "From Latin \"remuneratio,\" from \"remunerare\" (to reward), from \"re-\" (back) + \"munus\" (gift).",
            'memory_tip': "Think \"re-\" (back) + \"muneration\" (gift) = giving back gifts for work.",
            'example_sentence': "The contract specified the terms of ___ for consulting services."
        },
        'renal': {
            'definition': "Relating to the kidneys; of or concerning kidney function and health. Renal refers to the anatomical, physiological, or pathological aspects of the kidneys and their role in filtering blood and producing urine.",
            'pronunciation': "/ˈrinəl/",
            'pronunciation_respelling': "REE-nuhl",
            'etymology': "From Latin \"renalis,\" from \"renes\" (kidneys).",
            'memory_tip': "Think \"ren\" (kidney) + \"al\" = relating to kidneys.",
            'example_sentence': "The patient was referred to a ___ specialist for kidney problems."
        },
        'rendition': {
            'definition': "A performance or interpretation of a piece of music or drama; a translation or version of a text. Rendition involves artistic presentation, whether musical performance, dramatic interpretation, or textual translation.",
            'pronunciation': "/renˈdɪʃən/",
            'pronunciation_respelling': "ren-DISH-uhn",
            'etymology': "From Latin \"reddition,\" from \"reddere\" (to give back), from \"re-\" (back) + \"dare\" (to give).",
            'memory_tip': "Think \"render\" + \"ition\" = the action of rendering/performing something.",
            'example_sentence': "Her ___ of the national anthem moved the entire audience."
        },
        'renegotiate': {
            'definition': "To negotiate again; to revise the terms of an agreement through new negotiations. Renegotiation involves revisiting and potentially changing previously agreed-upon terms, conditions, or arrangements.",
            'pronunciation': "/ˌrinɪˈɡoʊʃiˌeɪt/",
            'pronunciation_respelling': "ree-ni-GOH-shee-ayt",
            'etymology': "From \"re-\" (again) + \"negotiate,\" from Latin \"negotiatus\" (to trade).",
            'memory_tip': "Think \"re-\" (again) + \"negotiate\" = negotiate the terms again.",
            'example_sentence': "The union voted to ___ their contract for better benefits."
        },
        'renewable': {
            'definition': "Capable of being renewed; relating to energy sources that are not depleted when used. Renewable resources can be replenished naturally or through human action, making them sustainable for long-term use.",
            'pronunciation': "/rɪˈnuəbəl/",
            'pronunciation_respelling': "ri-NOO-uh-buhl",
            'etymology': "From \"renew\" + suffix \"-able,\" from \"re-\" (again) + \"new.\"",
            'memory_tip': "Think \"renew\" + \"able\" = able to be renewed or replenished.",
            'example_sentence': "Solar and wind power are important ___ energy sources."
        },
        'renitency': {
            'definition': "The quality of being renitent; resistance to pressure or force; reluctance to yield or comply. Renitency describes the property of resisting change, pressure, or attempts at modification.",
            'pronunciation': "/rɪˈnaɪtənsi/",
            'pronunciation_respelling': "ri-NYE-tuhn-see",
            'etymology': "From Latin \"renitentia,\" from \"reniti\" (to resist), from \"re-\" (back) + \"niti\" (to strive).",
            'memory_tip': "Think \"re-\" (back) + \"nitency\" (striving) = striving back against force.",
            'example_sentence': "The material's ___ made it difficult to shape into the desired form."
        },
        'renminbi': {
            'definition': "The official currency of the People's Republic of China, literally meaning \"people's currency\"; the yuan is the basic unit of renminbi. Often abbreviated as RMB in financial contexts and international trade.",
            'pronunciation': "/ˌrɛnmɪnˈbi/",
            'pronunciation_respelling': "ren-min-BEE",
            'etymology': "From Chinese \"rénmínbì,\" literally \"people's currency.\"",
            'memory_tip': "Think \"ren\" (people) + \"min\" (people) + \"bi\" (currency) = people's currency.",
            'example_sentence': "The exchange rate between the dollar and the ___ fluctuated daily."
        },
        'rennet': {
            'definition': "A complex of enzymes used to coagulate milk in the manufacture of cheese; traditionally obtained from the stomach lining of calves. Rennet is essential in cheesemaking, causing milk proteins to form curds.",
            'pronunciation': "/ˈrenɪt/",
            'pronunciation_respelling': "REN-it",
            'etymology': "From Middle English \"rennet,\" from \"rennen\" (to run), referring to the curdling action.",
            'memory_tip': "Think of the enzyme that makes milk \"run\" together to form cheese.",
            'example_sentence': "The cheesemaker added ___ to begin the curdling process."
        },
        'renowned': {
            'definition': "Known or talked about by many people; famous and respected. Renowned individuals, places, or things have achieved widespread recognition and reputation for excellence, achievement, or notable characteristics.",
            'pronunciation': "/rɪˈnaʊnd/",
            'pronunciation_respelling': "ri-NOWND",
            'etymology': "From \"renown\" + suffix \"-ed,\" from Old French \"renomer\" (to make famous).",
            'memory_tip': "Think \"re-\" (again) + \"nowned\" (named) = named again and again = famous.",
            'example_sentence': "The hospital is ___ for its excellent cardiac surgery program."
        },
        'rental': {
            'definition': "The action of renting something; an amount paid or received as rent; available for rent. Rental involves temporary use of property, equipment, or services in exchange for payment.",
            'pronunciation': "/ˈrentəl/",
            'pronunciation_respelling': "REN-tuhl",
            'etymology': "From \"rent\" + suffix \"-al,\" from Old French \"rente\" (income).",
            'memory_tip': "Think \"rent\" + \"al\" = relating to renting or rent payment.",
            'example_sentence': "The ___ agreement specified a one-year lease with monthly payments."
        },
        'renvoi': {
            'definition': "In international law, the doctrine by which a court applies the law of another jurisdiction but takes into account that jurisdiction's conflict of laws rules. A complex legal concept dealing with which country's laws apply in international disputes.",
            'pronunciation': "/ˈrɑnvɔɪ/",
            'pronunciation_respelling': "rahn-VOY",
            'etymology': "From French \"renvoi,\" literally \"sending back,\" from \"renvoyer\" (to send back).",
            'memory_tip': "Think French \"ren\" (back) + \"voi\" (send) = sending back to original law.",
            'example_sentence': "The judge had to consider the principle of ___ when determining applicable law."
        },
        'renvoinoun': {
            'definition': "[COMBINED WORD ERROR: This appears to be 'renvoi' + 'noun' incorrectly joined. 'Renvoi' is a legal doctrine, while 'noun' is a grammatical term. These should be separate words.]",
            'pronunciation': "/ˈrɑnvɔɪ naʊn/",
            'pronunciation_respelling': "rahn-VOY NOWN",
            'etymology': "Combined word error: 'renvoi' from French + 'noun' from Latin.",
            'memory_tip': "Error combination: renvoi (legal doctrine) + noun (word type) - should be separate.",
            'example_sentence': "The legal concept of ___ is a ___ in international law."
        }
    }
    
    # Read input CSV
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_147_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_147_processed.csv'
    
    words_processed = 0
    combined_errors = []
    
    # Combined word error detection
    combined_patterns = ['regnalattaché', 'reigndifficulty', 'reiterateremorseful', 'reminiscentmenial', 'renvoinoun']
    
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
                    'notes': 'Batch 147 processing',
                    'review_status': 'pending',
                    'batch_number': '147'
                }
                
                writer.writerow(output_row)
                words_processed += 1
    
    print(f"\nBatch 147 processing complete!")
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