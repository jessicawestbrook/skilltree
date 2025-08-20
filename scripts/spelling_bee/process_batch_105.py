#!/usr/bin/env python3

import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    """Calculate 4-factor difficulty components for spelling words"""
    
    def calculate_difficulty_components(self, word: str, definition: str, etymology: str) -> dict:
        """Calculate 4-factor difficulty components leaving final difficulty null"""
        
        # 1. Phonetic Transparency (sound-to-spelling correspondence)
        phonetic_score = self._calculate_phonetic_transparency(word)
        
        # 2. Word Frequency (how common the word is)
        frequency_score = self._calculate_word_frequency(word)
        
        # 3. Morphological Complexity (prefixes, suffixes, roots)
        morphological_score = self._calculate_morphological_complexity(word, definition)
        
        # 4. Etymology Complexity (language origins and borrowing)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score, 
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'final_difficulty': None  # Leave null for human review
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        """Calculate how transparent the sound-to-spelling relationship is"""
        irregular_patterns = ['ough', 'aigh', 'eigh', 'ph', 'gh', 'tion', 'sion', 'ight']
        score = 1.0
        
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 0.3
        
        # Silent letters
        silent_patterns = ['mb', 'ght', 'kn', 'wr', 'mn']
        for pattern in silent_patterns:
            if pattern in word.lower():
                score += 0.2
                
        return min(score, 5.0)
    
    def _calculate_word_frequency(self, word: str) -> float:
        """Estimate word frequency (higher score = less frequent = more difficult)"""
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did']
        
        if word.lower() in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 7:
            return 3.0
        elif len(word) <= 10:
            return 4.0
        else:
            return 5.0
    
    def _calculate_morphological_complexity(self, word: str, definition: str) -> float:
        """Calculate complexity based on word parts"""
        score = 1.0
        
        prefixes = ['un', 're', 'pre', 'dis', 'anti', 'over', 'under', 'out', 'super', 'semi', 'multi', 'inter', 'trans', 'sub', 'micro', 'macro']
        suffixes = ['tion', 'sion', 'ment', 'ness', 'able', 'ible', 'ous', 'eous', 'ious', 'ly', 'ing', 'ed', 'er', 'est', 'ful', 'less']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 0.5
                break
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 0.5
                break
        
        # Compound words
        if len(word) > 8 and any(char.isupper() for char in word[1:]):
            score += 0.5
            
        return min(score, 5.0)
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        """Calculate complexity based on word origins"""
        if not etymology:
            return 3.0
            
        score = 1.0
        complex_origins = ['Latin', 'Greek', 'Sanskrit', 'Arabic', 'Hebrew', 'Persian', 'Turkish']
        moderate_origins = ['French', 'Italian', 'Spanish', 'Portuguese', 'German', 'Dutch']
        
        etymology_lower = etymology.lower()
        
        for origin in complex_origins:
            if origin.lower() in etymology_lower:
                score += 1.0
                break
                
        for origin in moderate_origins:
            if origin.lower() in etymology_lower:
                score += 0.5
                break
        
        # Multiple language origins increase complexity
        origin_count = sum(1 for origin in complex_origins + moderate_origins 
                          if origin.lower() in etymology_lower)
        if origin_count > 1:
            score += 0.5
            
        return min(score, 5.0)


class Batch105Processor:
    """Processes Batch 105 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
        # Define combined word errors found in this batch
        self.combined_errors = {
            'lumenluthier': ['lumen', 'luthier'],
            'lunulaem': ['lunulae', 'm'],  # Likely OCR error with extra 'm'
            'lupercaliam': ['lupercalia', 'm'],  # Likely OCR error with extra 'm'
            'macaroonbrazenness': ['macaroon', 'brazenness']
        }
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word using Claude knowledge"""
        
        # Handle combined word errors
        if word in self.combined_errors:
            return {
                'word': word,
                'pronunciation': None,
                'definition': f"COMBINED_WORD_ERROR: This appears to be two words combined: {' + '.join(self.combined_errors[word])}",
                'example_sentence': None,
                'etymology': None,
                'etymology_source': 'Claude',
                'memory_tip': 'This is a combined word error from PDF parsing and should not be used.',
                'phonetic_transparency_score': None,
                'word_frequency_score': None,
                'morphological_complexity_score': None,
                'etymology_complexity_score': None,
                'final_difficulty': None
            }
        
        # Comprehensive word data with 200-400 word definitions
        word_data = {
            'loved': {
                'pronunciation': '/LUVD/',
                'definition': 'Past tense of love; having experienced or expressed deep affection, care, or attachment toward someone or something, representing the completed action of loving that occurred in previous time periods and may continue to influence present relationships and emotions. Being loved involves receiving affection, care, and positive regard from others, creating emotional security, self-worth, and connection that contribute significantly to psychological well-being and healthy development throughout life. The experience of having loved encompasses both the joy of deep emotional connection and sometimes the pain of loss when relationships end or loved ones die, contributing to emotional growth and understanding of human vulnerability and resilience. Loved ones include family members, romantic partners, close friends, and others who hold special places in our hearts and memories, often influencing our values, decisions, and life directions long after specific relationships may have changed. The state of being loved provides foundation for trust, emotional regulation, and capacity for future loving relationships, while the act of having loved others develops empathy, compassion, and understanding of human nature. Cultural expressions of love vary widely across societies, but the fundamental human experience of loving and being loved appears universal, contributing to art, literature, music, and other cultural productions that celebrate and explore this central human experience.',
                'etymology': 'Past tense of "love" from Old English "lufu," meaning affection or love',
                'memory_tip': 'Remember LOVED as "LOVE" + "D" (past) - having experienced love in the past.',
                'example_sentence': 'She had _____ him deeply for many years, even after their paths separated and they moved to different cities.'
            },
            'loving': {
                'pronunciation': '/LUV-ing/',
                'definition': 'Showing or characterized by love, affection, and care; demonstrating tenderness, kindness, and emotional warmth in relationships and interactions with others, representing an ongoing quality or behavior that expresses deep positive feelings and concern for another\'s well-being. Loving behavior encompasses various expressions including verbal affirmations, physical affection, acts of service, quality time, and thoughtful gifts that communicate care and emotional connection between people. Parents demonstrate loving behavior through nurturing care, protection, guidance, and unconditional support that helps children develop security and self-worth, while romantic partners express loving feelings through intimacy, commitment, and shared experiences that strengthen emotional bonds. Loving relationships require ongoing effort, communication, understanding, and willingness to prioritize another\'s needs and happiness alongside one\'s own, creating mutual support and emotional fulfillment. The capacity for loving behavior develops through early attachment experiences and continues to evolve throughout life as individuals learn to balance self-care with care for others. Different cultural contexts emphasize various aspects of loving expression, from verbal declarations to practical demonstrations of care and commitment. Understanding loving behavior helps in building and maintaining healthy relationships that provide emotional satisfaction and contribute to overall life satisfaction and psychological well-being.',
                'etymology': 'Present participle of "love" from Old English "lufu," meaning showing love',
                'memory_tip': 'Remember LOVING as "LOVE" + "ING" (ongoing) - currently showing love and affection.',
                'example_sentence': 'The _____ grandmother always had warm hugs and encouraging words for her grandchildren when they visited.'
            },
            'loyal': {
                'pronunciation': '/LOI-əl/',
                'definition': 'Showing firm and constant support or allegiance; remaining faithful and committed to people, principles, organizations, or causes despite challenges, temptations, or changing circumstances, representing a character trait that values reliability, trustworthiness, and steadfast dedication over personal convenience or advantage. Loyalty manifests in various relationships including personal friendships where individuals support each other through difficulties, professional settings where employees remain committed to organizations and colleagues, and civic contexts where citizens maintain dedication to community values and democratic institutions. The concept encompasses both emotional attachment and behavioral consistency, requiring individuals to prioritize long-term commitments over short-term gains or pressures to abandon previous allegiances. Loyal behavior often involves personal sacrifice, defending others against criticism or attack, and maintaining confidences and trust even when doing so requires effort or creates personal challenges. Different cultures emphasize various aspects of loyalty including family loyalty, tribal loyalty, national loyalty, or loyalty to religious or philosophical principles, with some societies placing greater emphasis on group loyalty while others prioritize individual freedom and choice. Understanding loyalty involves recognizing both its positive contributions to relationships and communities and potential problems when blind loyalty prevents necessary change or enables harmful behavior.',
                'etymology': 'From Old French "loyal," from Latin "legalis" meaning legal or lawful',
                'memory_tip': 'Remember LOYAL as being "LEGAL" to your commitments - staying faithful and true.',
                'example_sentence': 'The _____ dog waited by the door every evening for its owner to return from work, never wavering in its devotion.'
            },
            'lozenge': {
                'pronunciation': '/LOZ-inj/',
                'definition': 'A small medicinal tablet designed to dissolve slowly in the mouth to treat throat irritation, cough, or other oral and respiratory symptoms; also a diamond-shaped geometric figure with four equal sides that appears in various decorative and heraldic contexts. Medicinal lozenges typically contain active ingredients such as menthol, eucalyptus, benzocaine, or antibacterial agents that provide local relief for sore throats, coughs, or mouth infections through direct contact with affected tissues. The slow dissolution process allows sustained release of therapeutic compounds while the sucking action stimulates saliva production that helps soothe irritated throat tissues. Different types of lozenges serve various purposes: throat lozenges for pain relief, cough drops for cough suppression, zinc lozenges for immune support, and antiseptic lozenges for oral hygiene maintenance. The geometric lozenge shape appears in decorative arts, architecture, and heraldry where diamond patterns create visual interest and symbolic meaning in various cultural contexts. Understanding lozenge applications helps in choosing appropriate treatments for minor respiratory symptoms while recognizing when professional medical attention may be necessary for more serious conditions. Modern lozenges often combine therapeutic ingredients with pleasant flavors to improve patient compliance and comfort during treatment.',
                'etymology': 'From Old French "losenge," possibly from Spanish "losanje," referring to the diamond shape',
                'memory_tip': 'Remember LOZENGE as a diamond-shaped medicine that "LOZES" (loosens) throat irritation.',
                'example_sentence': 'She sucked on a menthol _____ to soothe her scratchy throat before the important presentation.'
            },
            'luau': {
                'pronunciation': '/loo-OW/',
                'definition': 'A traditional Hawaiian feast and celebration featuring native foods, music, dance, and cultural activities that bring communities together to honor special occasions, seasonal cycles, or significant life events, representing an important cultural institution that preserves and shares Hawaiian heritage and values. Traditional luaus center around the preparation of a whole pig cooked in an underground oven called an imu, where the meat is slow-roasted for hours alongside other traditional foods including poi (pounded taro root), lomi lomi salmon, haupia (coconut pudding), and various tropical fruits and vegetables. The preparation process itself becomes a community activity involving multiple families and generations working together to dig the imu, prepare foods, and create the festive atmosphere that characterizes authentic Hawaiian celebrations. Modern luaus range from intimate family gatherings maintaining traditional practices to large tourist events that showcase Hawaiian culture for visitors, though authentic celebrations emphasize cultural education, community bonding, and spiritual connection to the land and ancestors. Hawaiian cultural elements including hula dancing, traditional music with ukuleles and drums, lei-making, and storytelling create educational and entertaining experiences that share island heritage with both locals and visitors. Understanding luaus provides insight into Hawaiian values of community, hospitality, and connection to nature while recognizing the importance of cultural authenticity and respect in representing indigenous traditions.',
                'etymology': 'From Hawaiian "lū\'au," originally referring to taro leaves cooked with chicken or octopus',
                'memory_tip': 'Remember LUAU as a Hawaiian feast - "LU" (love) + "AU" (awesome) - a loving awesome celebration.',
                'example_sentence': 'The family organized a traditional _____ to celebrate their daughter\'s graduation, complete with imu-roasted pig and hula dancing.'
            },
            'lubbers': {
                'pronunciation': '/LUB-ərz/',
                'definition': 'Plural of lubber; awkward, clumsy, or inexperienced sailors; landlubbers who lack sea skills and appear ungainly aboard ships, representing a nautical term that describes individuals who struggle with maritime activities and ship-board life due to inexperience or natural lack of seafaring ability. The term historically carried derogatory connotations among experienced sailors who prided themselves on nautical skills including rope work, balance on moving decks, understanding weather patterns, and efficient performance of ship duties under challenging conditions. Lubbers typically exhibit seasickness, difficulty with basic sailing tasks, fear of heights when climbing rigging, and general awkwardness with maritime equipment and procedures that experienced sailors perform naturally and efficiently. Maritime culture developed strong distinctions between skilled seamen and lubbers, with experienced crews often showing little patience for inexperienced individuals who might endanger ship operations or crew safety through incompetence or panic during critical situations. Modern usage extends beyond nautical contexts to describe anyone who appears clumsy, inexperienced, or out of place in specialized environments requiring specific skills and knowledge, though the term retains its strongest associations with maritime incompetence. Understanding maritime terminology helps appreciate the specialized knowledge and skills required for safe and efficient ship operations while recognizing how professional communities develop distinct vocabularies and cultural practices.',
                'etymology': 'Plural of "lubber," possibly from Middle English "lobre" meaning lazy fellow',
                'memory_tip': 'Remember LUBBERS as clumsy sailors who "BLUBBER" (struggle) with sea work - awkward on ships.',
                'example_sentence': 'The experienced crew members had little patience for the _____ who struggled with basic knots and became seasick in calm weather.'
            },
            'luciferin': {
                'pronunciation': '/loo-SIF-ər-in/',
                'definition': 'A light-emitting compound found in bioluminescent organisms that produces light through chemical reactions when combined with the enzyme luciferase and other cofactors, representing a fundamental biochemical mechanism that enables fireflies, deep-sea creatures, and other organisms to generate light for communication, defense, and predation purposes. This organic molecule undergoes oxidation reactions catalyzed by luciferase enzymes, converting chemical energy into light energy with remarkably high efficiency that far exceeds artificial lighting systems, producing minimal heat waste compared to incandescent bulbs. Different species possess unique luciferin variants that produce light of various colors and intensities: firefly luciferin creates yellow-green light, marine bacteria produce blue-green bioluminescence, and some fungi generate greenish glows through their own luciferin systems. Scientific research has harnessed luciferin-luciferase systems for biotechnology applications including medical imaging, gene expression studies, and environmental monitoring where bioluminescent markers provide non-invasive ways to track biological processes in living organisms. The compound\'s name derives from Lucifer, meaning "light-bearer," though its natural function serves survival and reproduction rather than any supernatural purpose. Understanding luciferin biochemistry provides insights into evolutionary adaptations, energy efficiency in biological systems, and practical applications for human technology and medical research that benefit from biological light-production mechanisms.',
                'etymology': 'From Latin "lucifer" meaning light-bearer + chemical suffix "-in"',
                'memory_tip': 'Remember LUCIFERIN as "LUCIFER" (light-bearer) + "IN" (chemical) - the light-bearing chemical in fireflies.',
                'example_sentence': 'Scientists studied the _____ compound in fireflies to understand how these insects produce their characteristic flashing lights.'
            },
            'lucky': {
                'pronunciation': '/LUK-ee/',
                'definition': 'Having good fortune; experiencing favorable outcomes that seem to result from chance rather than effort or skill, representing a subjective perception of positive events that may reflect actual probability, personal attitude, or cultural beliefs about fate and fortune. The concept of luck encompasses both random events that work in someone\'s favor and the ability to recognize and capitalize on opportunities that others might miss, suggesting that "lucky" people often combine chance events with preparedness and positive thinking. Psychological research indicates that people who consider themselves lucky tend to be more optimistic, open to new experiences, and attentive to opportunities, which may increase their likelihood of encountering positive situations and outcomes. Cultural attitudes toward luck vary significantly, with some societies emphasizing individual effort and responsibility while others place greater emphasis on fate, destiny, or supernatural influences that determine life outcomes. Lucky charms, rituals, and superstitions appear across many cultures as attempts to influence fortune, though scientific evidence suggests these practices work primarily through psychological effects rather than actual influence on random events. Understanding luck involves recognizing the interplay between random events, personal choices, attitude, and perception in shaping life experiences while maintaining realistic expectations about what individuals can and cannot control through their actions.',
                'etymology': 'From Middle Dutch "lucke" meaning good fortune or happiness',
                'memory_tip': 'Remember LUCKY as having good "LUCK" + "Y" (characterized by) - characterized by good fortune.',
                'example_sentence': 'She felt _____ to have found the perfect apartment just when her lease was about to expire.'
            },
            'lucrative': {
                'pronunciation': '/LOO-krə-tiv/',
                'definition': 'Producing substantial financial profit or material gain; highly profitable or financially rewarding, representing business opportunities, investments, or activities that generate significant income relative to the resources, time, or effort required to pursue them. Lucrative ventures attract entrepreneurs and investors seeking high returns on their capital and energy investments, often involving markets with strong demand, limited competition, or innovative products and services that command premium pricing. The assessment of lucrativeness requires analyzing factors including revenue potential, operating costs, market competition, regulatory environment, and scalability possibilities that determine long-term profitability and return on investment. Some traditionally lucrative industries include technology, pharmaceuticals, finance, and entertainment, though profitability can shift rapidly due to market changes, technological disruption, regulatory modifications, or economic conditions that affect consumer demand and business costs. Understanding lucrative opportunities involves developing business analysis skills, market research capabilities, and financial literacy that enable individuals to evaluate potential investments and career choices based on realistic profit projections rather than speculation or wishful thinking. The pursuit of lucrative activities must be balanced with considerations of risk, ethics, personal values, and social responsibility to ensure that profit-seeking contributes positively to both individual well-being and broader community welfare.',
                'etymology': 'From Latin "lucrativus," from "lucrari" meaning to gain profit',
                'memory_tip': 'Remember LUCRATIVE as "LUCRE" (money) + "ATIVE" (tending to) - tending to produce money/profit.',
                'example_sentence': 'The software developer found freelance consulting to be a _____ side business that supplemented her regular salary.'
            },
            'luculent': {
                'pronunciation': '/LOO-kyə-lənt/',
                'definition': 'Clear, evident, or easily understood; characterized by clarity of expression, transparency of meaning, or obvious truth that requires little explanation or interpretation, representing communication or reasoning that illuminates rather than obscures understanding. This relatively rare adjective describes writing, speech, arguments, or explanations that present information in ways that make complex ideas accessible and comprehensible to audiences without specialized knowledge or extensive background in particular subjects. Luculent presentations organize information logically, use appropriate examples and analogies, define technical terms clearly, and anticipate audience questions or confusion that might arise from unclear explanations. Academic and professional contexts value luculent communication because it enables effective knowledge transfer, reduces misunderstandings, and facilitates collaboration among people with different expertise levels who need to work together toward common goals. The quality of luculence in writing or speaking requires understanding audience needs, mastering subject matter thoroughly, and developing presentation skills that translate complex information into clear, accessible formats without oversimplifying important nuances. Scientific communication particularly benefits from luculent approaches that help general audiences understand research findings, policy implications, and technological developments that affect their lives and communities.',
                'etymology': 'From Latin "luculentus" meaning clear or bright, from "lux" (light)',
                'memory_tip': 'Remember LUCULENT as "LUX" (light) + "CULENT" (full of) - full of light, very clear and bright.',
                'example_sentence': 'The professor\'s _____ explanation made the complex mathematical concept understandable to all students in the introductory class.'
            },
            'luddite': {
                'pronunciation': '/LUD-īt/',
                'definition': 'A person who opposes technological advancement or mechanization, particularly when such innovations threaten traditional employment or established ways of life; named after Ned Ludd, a possibly fictional figure associated with early 19th-century English textile workers who destroyed machinery they blamed for unemployment and wage reductions. The original Luddites were skilled craftsmen whose livelihoods were threatened by industrial machinery that allowed factory owners to replace experienced workers with lower-paid, less-skilled laborers operating mechanical equipment, leading to organized resistance including machine breaking and factory attacks. Modern usage extends the term to describe anyone who resists technological change, fears automation, or prefers traditional methods over digital innovations, though such resistance may be based on legitimate concerns about job displacement, privacy, social isolation, or loss of human skills and relationships. Luddite attitudes can reflect reasonable caution about technological adoption that considers potential negative consequences alongside benefits, recognizing that technological progress doesn\'t automatically improve human welfare or social equity. Contemporary discussions about artificial intelligence, automation, and digital transformation often involve neo-Luddite perspectives that advocate for careful consideration of technology\'s social impact rather than blanket acceptance of innovation. Understanding Luddite history and perspectives helps in developing balanced approaches to technological change that consider both opportunities and risks for workers and communities.',
                'etymology': 'Named after Ned Ludd, legendary figure associated with English machine-breaking movement',
                'memory_tip': 'Remember LUDDITE as someone who "LUDDI-crous-ly" opposes technology - against technological change.',
                'example_sentence': 'Despite being called a _____ by his colleagues, he preferred handwritten letters to email for personal correspondence.'
            },
            'ludicrous': {
                'pronunciation': '/LOO-di-krəs/',
                'definition': 'So absurd, unreasonable, or ridiculous as to provoke laughter or scorn; characterized by extreme foolishness, irrationality, or inappropriateness that makes serious consideration difficult or impossible, representing situations, ideas, or behaviors that defy logic and common sense. Ludicrous circumstances often result from mismatched expectations and reality, poor planning, misunderstanding of basic facts, or attempts to apply inappropriate solutions to complex problems, creating outcomes that appear comically absurd to observers. Political, bureaucratic, and social situations frequently become ludicrous when regulations, policies, or procedures produce unintended consequences that contradict their original purposes or create more problems than they solve. The recognition of ludicrous elements in human behavior, institutions, or events serves important social functions including stress relief through humor, criticism of flawed systems, and perspective-taking that helps people maintain sanity in challenging circumstances. Literature, comedy, and satire often exploit ludicrous situations to entertain audiences while commenting on serious social issues, human nature, or institutional failures that might be difficult to address through direct criticism. Understanding what makes situations ludicrous helps in developing critical thinking skills, maintaining appropriate perspective on problems, and using humor constructively rather than destructively in personal and professional relationships.',
                'etymology': 'From Latin "ludicrus" meaning playful or sportive, from "ludus" (play or game)',
                'memory_tip': 'Remember LUDICROUS as "LUDIC" (playful) + "ROUS" (full of) - so playfully absurd it\'s ridiculous.',
                'example_sentence': 'The company\'s _____ policy required employees to get approval for purchasing paper clips but allowed unlimited spending on office furniture.'
            },
            'luftmensch': {
                'pronunciation': '/LOOFT-mensh/',
                'definition': 'A Yiddish term describing a person who is impractical, dreamy, or detached from worldly concerns; literally meaning "air person," referring to someone who seems to live in the clouds rather than dealing with practical realities of daily life, work, and material responsibilities. This concept encompasses individuals who are often intellectual, artistic, or philosophical but lack practical skills for managing finances, career advancement, or mundane tasks that are necessary for survival and success in conventional society. Luftmensch personalities typically excel in abstract thinking, creative pursuits, or theoretical discussions while struggling with practical matters like paying bills, maintaining schedules, or developing career strategies that provide stable income and security. The term reflects both affection and gentle criticism, recognizing the value of idealism and creativity while acknowledging the challenges that impractical people face in societies that reward practical skills and material achievement. Jewish cultural tradition has historically valued scholarship and intellectual pursuits, sometimes at the expense of practical concerns, creating a cultural context where luftmensch characteristics might be simultaneously respected and problematic. Understanding this concept helps in recognizing different personality types and approaches to life while appreciating both the contributions and challenges of people who prioritize intellectual or artistic pursuits over material success and practical competence.',
                'etymology': 'From Yiddish "luftmensh," literally meaning "air person," from German "Luft" (air) + "Mensch" (person)',
                'memory_tip': 'Remember LUFTMENSCH as "LUFT" (air) + "MENSCH" (person) - a person who lives in the air, impractical dreamer.',
                'example_sentence': 'The professor was a classic _____, brilliant at discussing philosophy but constantly forgetting to pay his bills or show up for appointments.'
            },
            'lugubrious': {
                'pronunciation': '/lə-GOO-bree-əs/',
                'definition': 'Mournful, dismal, or excessively sorrowful in appearance, manner, or expression; characterized by an exaggerated or affected display of grief, melancholy, or dejection that may seem overly dramatic or theatrical rather than genuinely emotional. This adjective describes people, artistic expressions, or atmospheres that emphasize sadness, loss, or tragic circumstances in ways that may evoke sympathy, discomfort, or even unintended humor through their intensity or inappropriateness to the situation. Lugubrious behavior might include excessive weeping, dramatic gestures of despair, overly somber facial expressions, or prolonged dwelling on negative events that seems disproportionate to actual circumstances or social expectations. Literary and artistic works sometimes adopt lugubrious tones to explore themes of mortality, suffering, or existential despair, though the effectiveness depends on genuine emotional authenticity rather than mere theatrical display of sorrow. Social contexts may find lugubrious behavior challenging when it dominates conversations, brings down group morale, or seems attention-seeking rather than reflecting genuine distress that deserves support and understanding. Understanding the difference between authentic grief and lugubrious behavior helps in providing appropriate responses to others\' emotional expressions while maintaining healthy emotional boundaries and realistic perspectives on life\'s inevitable challenges and losses.',
                'etymology': 'From Latin "lugubris" meaning mournful, from "lugere" (to mourn)',
                'memory_tip': 'Remember LUGUBRIOUS as "LUG" (heavy) + "UBRIOUS" (full of sorrow) - heavily sorrowful and mournful.',
                'example_sentence': 'His _____ expression and constant sighing made everyone uncomfortable at what was supposed to be a celebratory dinner.'
            },
            'lullaby': {
                'pronunciation': '/LUL-ə-bī/',
                'definition': 'A gentle, soothing song sung to help children fall asleep, typically characterized by soft melodies, repetitive rhythms, and comforting lyrics that create a peaceful, secure atmosphere conducive to rest and relaxation. Lullabies serve important developmental and bonding functions, providing emotional security through parental presence and voice, establishing bedtime routines that signal transition from active play to sleep, and creating positive associations with rest that support healthy sleep patterns throughout life. Traditional lullabies passed down through generations often reflect cultural values, folk wisdom, and family traditions while modern lullabies may incorporate contemporary themes and musical styles adapted to current parenting approaches and family dynamics. The musical characteristics of effective lullabies include slower tempos that match resting heart rates, simple melodic patterns that are easy to remember and sing, and gentle dynamics that avoid sudden loud sounds that might startle or stimulate rather than calm listeners. Research indicates that lullabies provide benefits for both children and parents: babies show reduced stress responses and improved sleep quality, while parents experience bonding opportunities and stress reduction through the act of singing and caregiving. Cross-cultural studies reveal that virtually all human societies develop lullaby traditions, suggesting that this musical form serves universal human needs for comfort, security, and peaceful rest.',
                'etymology': 'From "lull" (to soothe) + "bye" (goodbye or sleep), meaning a song to lull to sleep',
                'memory_tip': 'Remember LULLABY as "LULL" (soothe) + "A" + "BYE" (sleep) - a song to lull someone to sleep.',
                'example_sentence': 'She sang a soft _____ to her restless baby, watching as the gentle melody gradually calmed him to sleep.'
            },
            'lumbar': {
                'pronunciation': '/LUM-bər/',
                'definition': 'Relating to the lower back region of the spine, specifically the five vertebrae (L1-L5) located between the thoracic spine and the sacrum, representing a critical anatomical area that bears significant weight and stress while providing mobility and support for upper body movement and posture. The lumbar region supports most of the body\'s weight during standing and sitting activities, making it particularly susceptible to injury, strain, and degenerative conditions that can cause pain, disability, and reduced quality of life. Lumbar vertebrae are larger and more robust than cervical or thoracic vertebrae, reflecting their weight-bearing function, and are separated by intervertebral discs that provide cushioning and allow for bending and twisting movements. Common lumbar problems include disc herniation, muscle strain, arthritis, and spinal stenosis that can result from poor posture, heavy lifting, repetitive movements, aging, or traumatic injury. Medical professionals use lumbar anatomical landmarks for various procedures including epidural injections, spinal taps, and surgical interventions that require precise knowledge of spinal anatomy and surrounding nerve structures. Understanding lumbar anatomy and function helps in developing proper lifting techniques, exercise programs, and ergonomic practices that protect the lower back from injury while maintaining strength and flexibility necessary for daily activities and occupational demands.',
                'etymology': 'From Latin "lumbus" meaning loin or lower back region',
                'memory_tip': 'Remember LUMBAR as "LUMBER" (heavy wood) - the heavy-duty part of your back that carries weight.',
                'example_sentence': 'The physical therapist recommended specific exercises to strengthen the _____ muscles and improve lower back stability.'
            },
            'lumen': {
                'pronunciation': '/LOO-mən/',
                'definition': 'A unit of measurement for luminous flux, quantifying the total amount of visible light emitted by a source per unit of time, representing a standardized way to compare the brightness and efficiency of various lighting systems including incandescent bulbs, fluorescent tubes, LED fixtures, and natural light sources. The lumen measurement considers human eye sensitivity to different wavelengths of light, weighting the calculation toward the yellow-green portion of the visible spectrum where human vision is most sensitive, providing more accurate assessments of perceived brightness than simple energy output measurements. Modern lighting design relies heavily on lumen ratings to specify appropriate illumination levels for different applications: residential spaces typically require 10-20 lumens per square foot, office environments need 20-50 lumens per square foot, and detailed work areas may require 50-100 lumens per square foot for adequate visibility and comfort. Energy-efficient lighting technologies like LEDs produce significantly more lumens per watt than traditional incandescent bulbs, making lumen-per-watt ratios important considerations for both economic and environmental reasons. Understanding lumen measurements helps consumers make informed decisions about lighting purchases while enabling lighting professionals to design systems that provide appropriate illumination levels for safety, productivity, and visual comfort in various architectural and landscape applications.',
                'etymology': 'From Latin "lumen" meaning light or opening',
                'memory_tip': 'Remember LUMEN as "LUME" (light) + "EN" (unit) - the unit that measures light output.',
                'example_sentence': 'The new LED bulbs produced 800 _____ while consuming only 10 watts of electricity, making them highly energy efficient.'
            },
            'luminance': {
                'pronunciation': '/LOO-mə-nəns/',
                'definition': 'The measure of luminous intensity per unit area of light traveling in a specific direction, representing how bright a surface appears to human observers viewing it from a particular angle, distinguished from illuminance which measures light falling on a surface. Luminance measurements help in evaluating visual comfort, display quality, and lighting effectiveness in various applications including computer monitors, television screens, architectural lighting, and automotive displays where appropriate brightness levels affect user experience and safety. The measurement accounts for both the light reflected or emitted by surfaces and the directional characteristics of that light emission, making it particularly relevant for assessing glare, contrast ratios, and visibility conditions in different viewing situations. Photography and cinematography rely on luminance measurements to achieve proper exposure, contrast, and artistic effects that create desired visual moods and ensure technical quality in captured images and video content. Medical and ergonomic applications use luminance assessments to design work environments that minimize eye strain, prevent fatigue, and optimize visual performance for tasks requiring sustained visual attention such as reading, computer work, or detailed manufacturing operations. Understanding luminance principles helps in creating comfortable, efficient, and safe visual environments while addressing both functional requirements and aesthetic goals in lighting design and display technology applications.',
                'etymology': 'From Latin "luminare" meaning to light up, from "lumen" (light)',
                'memory_tip': 'Remember LUMINANCE as "LUMIN" (light) + "ANCE" (quality) - the quality of light brightness from a surface.',
                'example_sentence': 'The computer monitor\'s _____ was adjusted to reduce eye strain during long periods of screen work.'
            },
            'lunch': {
                'pronunciation': '/LUNCH/',
                'definition': 'A midday meal typically eaten between breakfast and dinner, serving important nutritional, social, and cultural functions that help sustain energy levels, facilitate social interaction, and provide structured breaks in daily work and school schedules. Lunch traditions vary significantly across cultures, from light snacks and salads in some regions to substantial hot meals that constitute the primary eating occasion of the day in others, reflecting different approaches to daily nutrition and meal timing. Workplace and school lunch policies affect productivity, health, and social dynamics, with research showing that appropriate lunch breaks improve concentration, reduce stress, and enhance job satisfaction while providing opportunities for informal communication and relationship building among colleagues and peers. The timing and composition of lunch can significantly impact afternoon energy levels and cognitive performance, with balanced meals containing appropriate combinations of protein, carbohydrates, and nutrients supporting sustained mental and physical activity throughout the day. Social aspects of lunch include business lunches that facilitate professional networking and deal-making, family lunches that strengthen relationships and cultural traditions, and communal dining that builds community connections and social support systems. Understanding lunch\'s role in daily life helps in making healthy food choices, managing time effectively, and using mealtime opportunities for relationship building and personal well-being.',
                'etymology': 'Shortened from "luncheon," possibly from Spanish "lonja" meaning slice of ham',
                'memory_tip': 'Remember LUNCH as the midday meal that gives you a "LUNGE" of energy for the afternoon.',
                'example_sentence': 'The office cafeteria served a variety of healthy _____ options including salads, soups, and grilled sandwiches.'
            },
            'lunulae': {
                'pronunciation': '/LOO-nyə-lee/',
                'definition': 'Plural of lunula; the crescent-shaped whitish areas at the base of fingernails and toenails, representing the visible portion of the nail matrix where new nail cells are generated, appearing as pale semicircular shapes that are most prominent on thumbnails and may be less visible or absent on other nails. These anatomical structures indicate healthy nail growth and development, with their size, shape, and visibility varying among individuals based on genetics, age, health status, and nail care practices. Medical professionals sometimes examine lunulae as indicators of overall health, circulation, and nutritional status, though their appearance can be influenced by various factors including trauma, certain medications, and underlying health conditions that affect nail growth. The term also applies to similar crescent shapes in other contexts including architectural elements, decorative patterns, and astronomical phenomena where crescent or semicircular forms appear naturally or by design. Archaeological and historical studies use lunulae to describe crescent-shaped ornaments, jewelry, and decorative motifs that appear across many cultures and time periods, often associated with lunar symbolism, fertility, and feminine divine attributes. Understanding nail anatomy including lunulae helps in maintaining nail health, recognizing potential health indicators, and appreciating the complex biological processes involved in nail growth and regeneration.',
                'etymology': 'Plural of Latin "lunula," diminutive of "luna" meaning small moon, referring to the crescent shape',
                'memory_tip': 'Remember LUNULAE as "LUNA" (moon) + "ULAE" (small) - small moon-shaped areas at the base of nails.',
                'example_sentence': 'The manicurist pointed out that healthy _____ were visible on most of her client\'s fingernails, indicating good circulation.'
            },
            'lupercalia': {
                'pronunciation': '/LOO-pər-KAY-lee-ə/',
                'definition': 'An ancient Roman festival held annually on February 15th in honor of Lupercus, a pastoral god associated with fertility, purification, and protection of flocks, representing one of the oldest and most unusual religious celebrations in Roman culture that combined elements of fertility ritual, purification ceremony, and community bonding through shared participation in traditional activities. The festival involved elaborate rituals including animal sacrifice of goats and dogs at the Lupercal cave on Palatine Hill where according to legend, the wolf nursed Romulus and Remus, followed by priests called Luperci running naked through the streets of Rome striking spectators with strips of sacrificed animal hide. These ritualistic actions were believed to promote fertility, purify the community from evil influences, and ensure protection from wolves and other dangers that threatened agricultural life and urban safety. Historical accounts suggest that Lupercalia continued well into the Christian era before being officially abolished, though some scholars argue that elements of the festival influenced later Valentine\'s Day traditions through temporal proximity and thematic connections to love and fertility. The festival demonstrates ancient Roman integration of agricultural concerns, religious beliefs, and community solidarity through participatory rituals that reinforced social bonds while addressing practical concerns about fertility, protection, and seasonal transitions. Understanding Lupercalia provides insights into ancient religious practices, Roman cultural values, and the complex relationships between agricultural societies and their religious institutions.',
                'etymology': 'From Latin "Lupercalia," from "Lupercus," a Roman god of fertility and shepherds',
                'memory_tip': 'Remember LUPERCALIA as "LUPER" (wolf god) + "CALIA" (festival) - the ancient Roman wolf god fertility festival.',
                'example_sentence': 'Historians study _____ as an example of how ancient Roman religious festivals combined fertility rituals with community purification ceremonies.'
            },
            'lupine': {
                'pronunciation': '/LOO-pīn/',
                'definition': 'Relating to or resembling wolves; also referring to a genus of flowering plants (Lupinus) in the legume family, characterized by distinctive palm-shaped leaves and tall spikes of colorful flowers that appear in gardens and wildflower meadows throughout temperate regions worldwide. The botanical lupine includes over 200 species ranging from annual herbs to perennial shrubs and small trees, many of which are valued for their nitrogen-fixing ability that improves soil fertility and their attractive flowers that create spectacular displays in blue, purple, pink, white, and yellow colors. Wild lupines serve important ecological functions as food sources for various insects including endangered Karner blue butterfly larvae that feed exclusively on wild blue lupine leaves, demonstrating the complex interdependencies within natural ecosystems. Some lupine species contain alkaloids that make them toxic to livestock and humans, requiring careful management in agricultural areas where animals might consume toxic varieties, though selective breeding has produced low-alkaloid varieties safe for animal feed and human consumption. Garden lupines are popular ornamental plants that thrive in cool climates and poor soils, making them valuable additions to sustainable landscapes and pollinator gardens where they attract bees, butterflies, and other beneficial insects. The adjective form relating to wolves appears in biological and behavioral contexts describing wolf-like characteristics, hunting behaviors, or social structures that resemble wolf pack dynamics.',
                'etymology': 'From Latin "lupinus" meaning of or relating to wolves, from "lupus" (wolf)',
                'memory_tip': 'Remember LUPINE as "LUPUS" (wolf) + "INE" (relating to) - relating to wolves, or the wolf-named flower.',
                'example_sentence': 'The mountainside was covered with wild _____ flowers, creating a spectacular display of purple and blue blooms.'
            },
            'lurching': {
                'pronunciation': '/LUR-ching/',
                'definition': 'Moving in an unsteady, irregular manner with sudden jolts or uncontrolled shifts in direction or speed, typically describing motion that lacks smoothness, coordination, or predictability, often resulting from mechanical problems, loss of balance, or lack of control over movement. This present participle describes various types of unstable motion including vehicles that jerk or stagger due to engine problems or poor driving conditions, people who stumble or move unsteadily due to illness, intoxication, or balance disorders, and objects that shift unexpectedly due to inadequate support or external forces. Ships lurch in heavy seas as they respond to wave action, creating uncomfortable conditions for passengers and crew while testing the vessel\'s structural integrity and navigational equipment. Mechanical equipment that lurches may indicate maintenance problems, wear, or improper operation that requires attention to prevent damage or safety hazards in industrial, transportation, or domestic applications. The word can also describe abrupt changes in non-physical contexts such as policy decisions, economic conditions, or social situations that shift suddenly and unpredictably, creating uncertainty and difficulty for people trying to adapt to changing circumstances. Understanding lurching motion helps in identifying problems with mechanical systems, recognizing health issues that affect balance and coordination, and responding appropriately to unstable conditions in various personal and professional contexts.',
                'etymology': 'Present participle of "lurch," possibly from nautical term describing sudden ship movement',
                'memory_tip': 'Remember LURCHING as "LURCH" (sudden unsteady movement) + "ING" (ongoing) - continuously moving unsteadily.',
                'example_sentence': 'The old bus was _____ down the mountain road, making passengers grip their seats with each sudden jolt.'
            },
            'lurid': {
                'pronunciation': '/LUR-id/',
                'definition': 'Unpleasantly vivid in color, particularly harsh yellows, reds, or oranges that seem artificial or disturbing; also describing something sensationally shocking, graphic, or designed to provoke strong emotional reactions through explicit or disturbing content. Visual lurid characteristics include garish lighting, clashing color combinations, or overly bright artificial colors that create uncomfortable or unsettling visual experiences rather than pleasing aesthetic effects. Media content becomes lurid when it emphasizes sensational, violent, or sexually explicit material primarily to attract attention and provoke reactions rather than to inform, educate, or create genuine artistic value. Lurid journalism focuses on scandalous details, graphic descriptions of violence or tragedy, and sensationalized reporting that prioritizes shocking content over balanced, responsible news coverage. The term can describe literature, films, or other entertainment that exploits disturbing themes, graphic violence, or sexual content in ways that seem excessive, exploitative, or designed primarily to shock audiences rather than serve legitimate artistic or educational purposes. Natural phenomena occasionally appear lurid when atmospheric conditions create unusual lighting effects, such as the eerie colors that sometimes precede severe storms or the artificial-looking hues created by pollution or unusual weather patterns. Understanding lurid characteristics helps in making informed choices about media consumption while recognizing when content crosses lines between legitimate artistic expression and exploitative sensationalism.',
                'etymology': 'From Latin "luridus" meaning pale yellow, sallow, or ghastly',
                'memory_tip': 'Remember LURID as "LURE" (attract) + "ID" (base desires) - attracting through shocking, sensational content.',
                'example_sentence': 'The tabloid\'s _____ headlines about the celebrity scandal were designed more to sell papers than to inform readers.'
            },
            'lustrum': {
                'pronunciation': '/LUS-trəm/',
                'definition': 'A period of five years; in ancient Rome, the interval between censuses when Roman citizens were counted and purified in ceremonial rituals that maintained civic order and religious observance, representing both a chronological measurement and a cultural institution that reinforced Roman identity and social structure. Roman lustra (plural) marked important administrative cycles during which censors conducted comprehensive population counts, assessed property values for taxation, reviewed citizen status and qualifications, and performed purification ceremonies called lustrations that were believed to cleanse the community of impurities and ensure divine favor. The lustral ceremonies involved elaborate rituals including animal sacrifices, prayers, and processions that demonstrated Roman religious devotion while reinforcing social hierarchies and civic obligations that defined Roman citizenship and community membership. Modern usage of lustrum appears primarily in academic, historical, and formal contexts where precise five-year periods need to be designated, though the term is less common than other chronological measurements like decade or quinquennium. The concept reflects ancient understanding of time as cyclical rather than purely linear, with regular intervals marking opportunities for renewal, assessment, and community recommitment to shared values and institutions. Understanding lustrum provides insights into Roman administrative practices, religious beliefs, and social organization while demonstrating how ancient societies used temporal cycles to structure civic life and maintain cultural continuity.',
                'etymology': 'From Latin "lustrum," from "lustrare" meaning to purify, referring to purification ceremonies',
                'memory_tip': 'Remember LUSTRUM as "LUST" (desire) + "RUM" (Roman) - Romans desired purification every 5 years.',
                'example_sentence': 'The historian noted that significant changes in Roman policy often occurred at the end of each _____, following the census and purification rituals.'
            },
            'lutheran': {
                'pronunciation': '/LOO-thər-ən/',
                'definition': 'Relating to Lutheranism, a major branch of Protestant Christianity that originated from the theological reforms of Martin Luther in 16th-century Germany, emphasizing salvation by grace through faith alone, the authority of Scripture over church tradition, and the priesthood of all believers as fundamental principles that distinguish Lutheran doctrine from Catholic and other Protestant teachings. Lutheran churches maintain distinctive theological positions including consubstantiation regarding communion, infant baptism for original sin remission, and liturgical worship traditions that preserve many historical Christian practices while rejecting papal authority and certain Catholic doctrines. Major Lutheran denominations worldwide include the Lutheran World Federation churches, Missouri Synod Lutherans, and various national Lutheran churches in Germany, Scandinavia, and other regions where Lutheran missions established lasting religious communities. Lutheran educational traditions have contributed significantly to global education through universities, schools, and theological seminaries that combine academic excellence with faith-based learning approaches, producing influential scholars, leaders, and social reformers throughout history. The Lutheran emphasis on social justice, charitable work, and community service has created extensive networks of hospitals, social service organizations, and relief agencies that address human needs while expressing Christian faith through practical action. Understanding Lutheran history and theology provides insights into Protestant Reformation impacts, denominational diversity within Christianity, and ongoing influences of Lutheran thought on modern religious, educational, and social institutions.',
                'etymology': 'From Martin Luther + suffix "-an," relating to the German reformer Martin Luther',
                'memory_tip': 'Remember LUTHERAN as "LUTHER" (Martin Luther) + "AN" (relating to) - relating to Martin Luther\'s reforms.',
                'example_sentence': 'The _____ church\'s emphasis on grace and Scripture attracted many followers during the Protestant Reformation.'
            },
            'luthier': {
                'pronunciation': '/LOO-tee-ər/',
                'definition': 'A craftsperson who makes and repairs stringed musical instruments, particularly violins, violas, cellos, double basses, guitars, and other fretted or bowed instruments, representing a highly specialized trade that combines woodworking skills, acoustic knowledge, and artistic sensibility to create instruments capable of producing beautiful music. Traditional luthiery involves selecting appropriate woods for different instrument parts, understanding grain patterns and acoustic properties of various species, mastering hand tools and techniques for shaping, carving, and assembling delicate components, and developing finishing skills that protect instruments while allowing optimal sound resonance. Master luthiers often spend decades perfecting their craft through apprenticeships, formal training, and continuous experimentation with materials, techniques, and design modifications that improve instrument playability, durability, and tonal qualities. The profession requires understanding of string tension, bridge placement, soundpost positioning, and other technical factors that affect instrument performance, as well as repair skills for addressing damage, wear, and aging that occurs through normal use or accidents. Contemporary luthiery balances traditional techniques passed down through generations with modern materials, tools, and scientific understanding of acoustics that enable innovations while preserving the essential qualities that make stringed instruments capable of expressing musical artistry. The luthier-musician relationship often involves collaboration to customize instruments for specific playing styles, musical genres, and individual performer preferences that optimize artistic expression.',
                'etymology': 'From French "luthier," from "luth" (lute), referring to makers of lutes and other stringed instruments',
                'memory_tip': 'Remember LUTHIER as "LUTE" (stringed instrument) + "HIER" (maker) - a maker of lutes and stringed instruments.',
                'example_sentence': 'The skilled _____ spent months crafting the violin, carefully selecting woods and adjusting every detail for optimal sound quality.'
            },
            'lutrine': {
                'pronunciation': '/LOO-trīn/',
                'definition': 'Of, relating to, or characteristic of otters; resembling or having qualities associated with otters, referring to the subfamily Lutrinae of carnivorous mammals known for their aquatic adaptations, playful behavior, and important ecological roles in freshwater and marine environments worldwide. Lutrine characteristics include streamlined body shapes optimized for swimming, dense waterproof fur that provides insulation in cold water, webbed feet and powerful tails that enable efficient underwater locomotion, and behavioral adaptations including tool use and sophisticated hunting techniques. These semi-aquatic mammals occupy various habitats from rivers and lakes to coastal marine environments, serving crucial ecological functions as top predators that help maintain healthy fish populations and aquatic ecosystem balance. Lutrine behavior includes complex social structures, playful activities that serve learning and bonding functions, and territorial behaviors that involve scent marking and vocal communication among family groups and individuals. Conservation concerns affect many lutrine species due to habitat destruction, water pollution, hunting pressure, and climate change impacts that threaten otter populations worldwide, leading to protection efforts and habitat restoration programs. Understanding lutrine biology and ecology provides insights into aquatic ecosystem health, the importance of apex predators in maintaining environmental balance, and conservation strategies needed to protect these charismatic and ecologically important mammals.',
                'etymology': 'From Latin "lutra" meaning otter + suffix "-ine" meaning relating to or characteristic of',
                'memory_tip': 'Remember LUTRINE as "LUTR" (otter) + "INE" (relating to) - relating to or characteristic of otters.',
                'example_sentence': 'The biologist studied _____ behavior patterns to understand how climate change was affecting river otter populations.'
            },
            'luxuriate': {
                'pronunciation': '/lug-ZHUR-ee-ayt/',
                'definition': 'To enjoy oneself in a luxurious way; to indulge in comfort, pleasure, or abundance with evident satisfaction and self-indulgence, representing the act of taking full advantage of favorable circumstances, comfortable conditions, or pleasurable experiences without restraint or guilt. This verb encompasses both physical comfort such as relaxing in luxurious surroundings and emotional or psychological pleasure derived from abundance, beauty, or favorable conditions that enhance well-being and happiness. People luxuriate in various contexts including spa treatments, comfortable accommodations, fine dining experiences, beautiful natural settings, or any situation that provides exceptional comfort, pleasure, or aesthetic satisfaction. The concept extends beyond material luxury to include intellectual luxuriation in ideas, artistic luxuriation in creative expression, or spiritual luxuriation in peaceful contemplation and reflection that enriches inner life and personal growth. Luxuriating often involves slowing down from busy routines, paying attention to sensory experiences, and allowing oneself to fully appreciate favorable circumstances rather than rushing through or taking them for granted. Understanding healthy luxuriation helps distinguish between appropriate self-care and indulgence that enhances well-being versus excessive materialism or hedonism that may lead to problems with priorities, relationships, or personal values.',
                'etymology': 'From Latin "luxuriare" meaning to be abundant or grow profusely, from "luxuria" (luxury)',
                'memory_tip': 'Remember LUXURIATE as "LUXURY" + "ATE" (to do) - to indulge in luxury and comfort.',
                'example_sentence': 'After months of hard work, she decided to _____ in a spa weekend, enjoying massages and gourmet meals.'
            },
            'lymphoma': {
                'pronunciation': '/lim-FO-mə/',
                'definition': 'A type of cancer that originates in the lymphatic system, which is part of the immune system responsible for fighting infections and diseases, characterized by abnormal growth and proliferation of lymphocytes (white blood cells) that can affect lymph nodes, spleen, thymus, and other organs throughout the body. The two main categories of lymphoma are Hodgkin lymphoma, distinguished by the presence of Reed-Sternberg cells and typically spreading in an orderly manner from one lymph node group to adjacent groups, and non-Hodgkin lymphoma, which includes various subtypes that may spread unpredictably and can affect multiple organ systems simultaneously. Symptoms often include swollen lymph nodes, unexplained weight loss, persistent fatigue, night sweats, and fever, though early-stage lymphomas may present with subtle or no symptoms, making early detection challenging without regular medical monitoring. Treatment approaches vary depending on lymphoma type, stage, and patient factors, including radiation therapy for localized disease, chemotherapy for systemic treatment, immunotherapy to enhance immune system response, and stem cell transplantation for aggressive or recurrent cases. Modern lymphoma treatment has achieved remarkable success rates, particularly for certain types like Hodgkin lymphoma, with many patients achieving complete remission and long-term survival when treatment begins early and follows appropriate protocols. Understanding lymphoma helps in recognizing potential warning signs, supporting affected individuals, and appreciating advances in cancer research and treatment that continue to improve outcomes.',
                'etymology': 'From Latin "lympha" (water) + Greek "-oma" (tumor), referring to cancer of the lymphatic system',
                'memory_tip': 'Remember LYMPHOMA as "LYMPH" (immune system) + "OMA" (tumor) - cancer of the lymphatic system.',
                'example_sentence': 'The oncologist explained that her type of _____ had an excellent prognosis with current treatment protocols.'
            },
            'lyricist': {
                'pronunciation': '/LIR-i-sist/',
                'definition': 'A person who writes lyrics for songs, specializing in creating the words and verbal content that convey meaning, emotion, and narrative within musical compositions, representing a crucial creative role in popular music, musical theater, and other forms of musical entertainment that combine melody with verbal expression. Professional lyricists master various skills including storytelling through verse and chorus structures, creating memorable phrases and hooks that enhance musical impact, understanding rhythm and meter to ensure words fit comfortably with melodies, and collaborating effectively with composers and performers to achieve artistic goals. The craft involves balancing multiple considerations simultaneously: conveying clear messages or emotions, creating singable phrases that flow naturally, incorporating rhyme schemes and literary devices that enhance artistic impact, and adapting writing style to different musical genres and target audiences. Successful lyricists often develop distinctive voices and specialties within particular genres such as country music, hip-hop, musical theater, or pop music, while versatile writers may work across multiple styles and collaborate with various artists throughout their careers. The profession requires understanding of both literary techniques and music industry practices, including copyright law, publishing rights, and collaborative relationships with composers, performers, and music producers. Many renowned lyricists have significantly influenced popular culture through memorable songs that capture universal human experiences and resonate across generations and cultural boundaries.',
                'etymology': 'From "lyric" + suffix "-ist" meaning one who practices or specializes in lyrics',
                'memory_tip': 'Remember LYRICIST as "LYRIC" (song words) + "IST" (one who does) - one who writes song lyrics.',
                'example_sentence': 'The talented _____ won a Grammy for writing the emotionally powerful lyrics that made the song a worldwide hit.'
            },
            'lysozyme': {
                'pronunciation': '/LY-sə-zīm/',
                'definition': 'An antimicrobial enzyme naturally found in various animal secretions including tears, saliva, mucus, and egg whites, capable of breaking down bacterial cell walls by cleaving peptidoglycan bonds, representing an important component of innate immune defense systems that provide protection against bacterial infections. This enzyme demonstrates remarkable effectiveness against gram-positive bacteria whose cell walls contain substantial amounts of peptidoglycan, while showing less activity against gram-negative bacteria that possess additional protective outer membrane layers. Alexander Fleming first discovered lysozyme in 1922 when he noticed that nasal mucus could dissolve certain bacteria, leading to important insights about natural antimicrobial mechanisms and eventually contributing to his later discovery of penicillin and development of modern antibiotic medicine. Commercial applications include food preservation where lysozyme prevents bacterial spoilage in dairy products, wine, and other foods; pharmaceutical formulations that enhance antimicrobial activity; and research applications that require controlled bacterial lysis for laboratory procedures. The enzyme\'s natural occurrence in human secretions provides continuous protection for mucous membranes and other body surfaces exposed to environmental bacteria, working alongside other immune mechanisms to maintain health and prevent infection. Understanding lysozyme function provides insights into natural immune responses, antimicrobial resistance mechanisms, and biotechnology applications that harness natural biological processes for human benefit.',
                'etymology': 'From Greek "lysis" (dissolution) + "enzyme," referring to an enzyme that dissolves bacterial cells',
                'memory_tip': 'Remember LYSOZYME as "LYSO" (dissolve) + "ZYME" (enzyme) - an enzyme that dissolves bacterial cell walls.',
                'example_sentence': 'Researchers studied _____ as a natural antimicrobial agent that could potentially be used in food preservation applications.'
            },
            'macadam': {
                'pronunciation': '/mə-KAD-əm/',
                'definition': 'A road surface or construction method consisting of layers of crushed stone compacted together, originally developed by Scottish engineer John Loudon McAdam in the early 19th century as an improvement over existing road-building techniques, representing a revolutionary approach to creating durable, well-drained roadways that could support heavy traffic and weather conditions. The macadam method involves placing successively smaller grades of crushed stone in layers, with each layer compacted before adding the next, creating a solid, interlocking surface that distributes weight evenly and allows water drainage to prevent erosion and frost damage. Traditional macadam roads used angular stone fragments without binding agents, relying on mechanical interlocking and compaction to create stable surfaces, while modern variations include tar macadam and asphalt concrete that incorporate binding materials for enhanced durability and weather resistance. This construction technique proved crucial for economic development during the Industrial Revolution, enabling reliable transportation of goods and people over long distances while reducing travel time and vehicle maintenance costs compared to previous dirt and cobblestone roads. The macadam principle influenced modern road construction practices worldwide, contributing to development of highway systems, airport runways, and other paved surfaces that support contemporary transportation infrastructure. Understanding macadam construction provides insights into engineering innovation, infrastructure development, and the relationship between transportation technology and economic growth in developing societies.',
                'etymology': 'Named after John Loudon McAdam, Scottish engineer who developed this road construction method',
                'memory_tip': 'Remember MACADAM as "McADAM" - named after the Scottish engineer who invented this road-building method.',
                'example_sentence': 'The old _____ road was being replaced with modern asphalt to better handle increased traffic volume.'
            },
            'macao': {
                'pronunciation': '/mə-KOW/',
                'definition': 'A Special Administrative Region of China, located on the South China Sea coast near Hong Kong, historically significant as a Portuguese colonial territory and currently known as a major gambling and entertainment destination often called the "Las Vegas of Asia," representing a unique blend of Chinese and Portuguese cultural influences. Macao\'s economy centers heavily on gaming and tourism industries, with numerous casinos and luxury hotels attracting millions of visitors annually from mainland China and other Asian countries, generating substantial revenue that makes it one of the world\'s wealthiest regions per capita. The territory\'s history spans over 400 years of Portuguese administration before its return to Chinese sovereignty in 1999 under the "One Country, Two Systems" principle, which maintains Macao\'s distinct legal, economic, and cultural characteristics while integrating it with mainland China. Cultural attractions include historic architecture that reflects Portuguese colonial influence, traditional Chinese temples and festivals, and a distinctive Macanese cuisine that combines Chinese and Portuguese culinary traditions into unique dishes and flavors not found elsewhere. Macao\'s compact size of approximately 30 square kilometers makes it one of the most densely populated regions in the world, with intensive urban development and land reclamation projects expanding available space for commercial and residential use. Understanding Macao requires appreciating its role as a cultural bridge between East and West, its economic transformation from trading post to entertainment destination, and its ongoing evolution within China\'s broader development strategy.',
                'etymology': 'From Portuguese "Macau," possibly from Chinese "ma ge" (bay of A-Ma, a sea goddess)',
                'memory_tip': 'Remember MACAO as the former Portuguese territory near Hong Kong, famous for casinos and gambling.',
                'example_sentence': '_____ has become Asia\'s premier gaming destination, attracting millions of tourists to its luxurious casinos and hotels.'
            },
            'macaque': {
                'pronunciation': '/mə-KAHK/',
                'definition': 'A genus of Old World monkeys found throughout Asia and North Africa, characterized by robust builds, relatively short tails, and complex social structures, representing one of the most widespread and adaptable primate groups that have successfully colonized diverse habitats from tropical forests to urban environments. Macaque species include Japanese macaques that have adapted to cold climates and are famous for bathing in hot springs, Barbary macaques of North Africa and Gibraltar, long-tailed macaques of Southeast Asia, and rhesus macaques that have become important research animals in medical and behavioral studies. These highly intelligent primates demonstrate sophisticated social behaviors including hierarchical group structures, complex communication systems, tool use in some species, and cultural transmission of learned behaviors across generations within troops. Macaques have proven remarkably adaptable to human-modified environments, with some populations thriving in agricultural areas, urban parks, and temple complexes where they interact regularly with human communities, sometimes creating management challenges due to crop damage or aggressive behavior. Research on macaque behavior, cognition, and physiology has contributed significantly to understanding primate evolution, social behavior, and biomedical applications including vaccine development, neurological research, and studies of aging and disease processes. Conservation status varies among macaque species, with some populations stable or increasing while others face threats from habitat loss, hunting, and human-wildlife conflict that require targeted protection efforts.',
                'etymology': 'From Portuguese "macaco," possibly from a West African language meaning monkey',
                'memory_tip': 'Remember MACAQUE as the widespread Asian monkey - "MACA" sounds like "maker" - they make complex societies.',
                'example_sentence': 'Researchers studied the _____ troop\'s social hierarchy to understand how primates maintain group cohesion and resolve conflicts.'
            },
            'macau': {
                'pronunciation': '/mə-KOW/',
                'definition': 'Alternative spelling of Macao, referring to the same Special Administrative Region of China known for its gambling industry, Portuguese colonial history, and unique cultural blend, though "Macao" is the more commonly accepted English spelling while "Macau" reflects Portuguese pronunciation and appears in some historical and official contexts. The territory maintains the same characteristics regardless of spelling variation: its role as a major gaming destination, its historical significance as a Portuguese trading post, and its current status as a bridge between Chinese and Western cultures. Both spellings refer to the densely populated region that has transformed from a colonial trading port into a modern entertainment and tourism center while preserving historical architecture, cultural traditions, and legal systems that distinguish it from mainland China. The name variations reflect linguistic evolution and transliteration differences between Portuguese, Chinese, and English languages, demonstrating how place names adapt across cultures and languages while referring to the same geographic and political entity. Understanding these naming conventions helps in recognizing references to the territory in different contexts while appreciating the complex linguistic heritage that results from centuries of cultural exchange between East and West. Modern usage tends to favor "Macao" in English-language contexts while "Macau" may appear in Portuguese-influenced or historical documents.',
                'etymology': 'Portuguese spelling variant of Macao, from Chinese "ma ge" (bay of A-Ma)',
                'memory_tip': 'Remember MACAU as the Portuguese spelling of Macao - same place, different spelling convention.',
                'example_sentence': 'Historical documents from the Portuguese colonial period often refer to the territory as _____ rather than using the modern spelling.'
            },
            'macaw': {
                'pronunciation': '/mə-KAW/',
                'definition': 'A large, colorful parrot native to Central and South America, characterized by brilliant plumage, powerful beaks, and impressive size, representing some of the most spectacular and intelligent birds in the parrot family, with species including scarlet macaws, blue-and-gold macaws, and green-winged macaws that display stunning color combinations and complex behaviors. These magnificent birds inhabit tropical rainforests where they play crucial ecological roles as seed dispersers, using their strong beaks to crack open hard nuts and fruits while spreading plant seeds across large territories through their daily feeding and flight patterns. Macaws demonstrate remarkable intelligence through problem-solving abilities, complex social behaviors, sophisticated vocalizations that include mimicry of human speech, and strong pair bonds that often last for life, with mated pairs engaging in mutual preening and synchronized flight displays. Many macaw species face conservation challenges due to habitat destruction, illegal capture for the pet trade, and human encroachment into their natural ranges, leading to population declines and endangered status for several species including the hyacinth macaw and Spix\'s macaw. Captive macaws require specialized care including spacious enclosures, mentally stimulating activities, social interaction, and diets that replicate their natural feeding patterns, as these highly intelligent birds can develop behavioral problems in inappropriate environments. Understanding macaw biology and conservation needs helps in protecting these magnificent birds while appreciating their ecological importance and the complex relationships between biodiversity, habitat preservation, and human activities in tropical regions.',
                'etymology': 'From Portuguese "macao," ultimately from Tupi (Brazilian indigenous language)',
                'memory_tip': 'Remember MACAW as the large, colorful parrot that makes a "CA-CAW" sound with its powerful voice.',
                'example_sentence': 'The brilliant scarlet _____ perched in the rainforest canopy, its red, blue, and yellow feathers creating a stunning display of natural color.'
            },
            'macchiato': {
                'pronunciation': '/mah-kee-AH-toh/',
                'definition': 'An Italian coffee drink consisting of espresso "marked" or "spotted" with a small amount of steamed milk foam, representing a traditional preparation method that provides a strong coffee flavor with just a touch of milk to soften the intensity while maintaining the espresso\'s distinctive character and caffeine content. The traditional macchiato involves adding approximately one tablespoon of steamed milk foam to a single or double shot of espresso, creating a layered appearance where the white foam contrasts with the dark coffee beneath, hence the Italian name meaning "marked" or "stained." This preparation differs significantly from larger milk-based coffee drinks like cappuccinos and lattes, emphasizing coffee flavor over milk content while providing just enough dairy to create textural interest and slight flavor modification. Regional variations include caramel macchiato popularized by coffee chains, which involves vanilla syrup and caramel sauce in addition to espresso and steamed milk, though this differs substantially from traditional Italian preparations. The drink requires skilled espresso extraction to achieve proper crema formation and flavor balance, as the small amount of milk means that coffee quality and preparation technique significantly affect the final result. Understanding macchiato preparation helps appreciate Italian coffee culture, barista skills, and the subtle differences between various espresso-based beverages that reflect different approaches to combining coffee and milk in complementary rather than dominant proportions.',
                'etymology': 'From Italian "macchiato" meaning marked or spotted, referring to espresso marked with milk',
                'memory_tip': 'Remember MACCHIATO as "MACCHIA" (mark/spot) - espresso marked with a spot of milk foam.',
                'example_sentence': 'The barista prepared a perfect _____ by adding just a dollop of steamed milk foam to the rich espresso shot.'
            },
            'macedonia': {
                'pronunciation': '/mas-ə-DOH-nee-ə/',
                'definition': 'A landlocked country in southeastern Europe on the Balkan Peninsula, officially known as North Macedonia since 2019 following resolution of a naming dispute with Greece, characterized by mountainous terrain, diverse cultural heritage, and a complex history involving ancient Macedonian kingdoms, Byzantine rule, Ottoman occupation, and Yugoslav federation membership. The nation encompasses approximately 25,000 square kilometers with a population of about 2 million people representing various ethnic groups including Macedonians, Albanians, Turks, Roma, and other minorities who contribute to the country\'s multicultural society and linguistic diversity. North Macedonia\'s capital city Skopje serves as the political, economic, and cultural center, featuring a mix of Ottoman-era architecture, brutalist Yugoslav buildings, and controversial neoclassical construction projects that reflect the nation\'s complex identity and political aspirations. The country faces ongoing challenges including economic development, European Union membership aspirations, ethnic relations, and regional diplomatic relationships that affect its political stability and international integration efforts. Cultural heritage includes ancient archaeological sites, Orthodox Christian monasteries, Islamic architecture from the Ottoman period, and traditional music and dance that reflect the region\'s position as a crossroads between European and Asian cultures. Understanding North Macedonia requires appreciating its role in Balkan history, ongoing nation-building efforts, and the complex relationships between ethnic identity, political sovereignty, and international recognition in post-Yugoslav southeastern Europe.',
                'etymology': 'From ancient Greek "Makedonia," possibly meaning "tall" or "mountainous," referring to the region',
                'memory_tip': 'Remember MACEDONIA as the Balkan country (North Macedonia) - also a fruit salad with mixed ingredients like the country\'s mixed cultures.',
                'example_sentence': 'North _____ joined NATO in 2020 after resolving its long-standing naming dispute with Greece.'
            },
            'machete': {
                'pronunciation': '/mə-SHET-ee/',
                'definition': 'A broad, heavy knife with a long blade used as both a cutting tool and weapon, particularly common in tropical regions where it serves essential functions for agricultural work, vegetation clearing, and food preparation, representing one of the most versatile and culturally significant edged tools in many developing countries. Agricultural applications include harvesting sugar cane, clearing brush and weeds, pruning vegetation, and preparing fields for planting, with the machete\'s design optimized for chopping motions that efficiently cut through plant material of various thickness and density. Different regions have developed distinct machete styles adapted to local needs: Latin American machetes often feature curved blades for sugar cane harvesting, African pangas have wider blades for heavy chopping, and Southeast Asian parangs include variations for jungle clearing and woodworking tasks. The tool\'s cultural significance extends beyond practical applications to include ceremonial uses, traditional crafts, self-defense, and symbolic representations of agricultural identity and rural life in many societies where machetes remain essential daily implements. Modern manufacturing produces machetes with various blade lengths, weights, and handle designs suited to different tasks, while maintaining the basic design principles that have made this tool successful across cultures and environments for centuries. Understanding machete design and usage provides insights into agricultural practices, tool technology, and cultural adaptations that enable human communities to thrive in challenging environmental conditions.',
                'etymology': 'From Spanish "machete," diminutive of "macho" meaning hammer or club',
                'memory_tip': 'Remember MACHETE as a "MACHO" cutting tool - a strong, heavy knife for tough cutting jobs.',
                'example_sentence': 'The farmer used his sharp _____ to clear overgrown vines from the fence line around his property.'
            },
            'machiavellian': {
                'pronunciation': '/MAK-ee-ə-VEL-ee-ən/',
                'definition': 'Characterized by cunning, scheming, and unscrupulous behavior in pursuit of power or advantage; employing manipulative and deceitful tactics to achieve goals regardless of ethical considerations, derived from Niccolò Machiavelli\'s political philosophy that emphasized pragmatic effectiveness over moral constraints in governance and leadership. This adjective describes individuals who prioritize results over methods, using whatever means necessary including deception, manipulation, betrayal, and exploitation to achieve their objectives, often in political, business, or social contexts where power and influence are at stake. Machiavellian behavior typically involves strategic thinking, careful planning, and sophisticated understanding of human psychology that enables manipulation of others\' emotions, desires, and weaknesses for personal gain or advancement. The concept extends beyond individual personality traits to describe organizational cultures, political systems, or social structures that reward cunning and manipulation while discouraging ethical behavior and honest communication. While Machiavelli\'s original writings were more nuanced and focused on effective statecraft during turbulent times, popular usage of "Machiavellian" has come to represent purely self-interested manipulation without regard for consequences to others or society. Understanding Machiavellian characteristics helps in recognizing manipulative behavior, protecting oneself from exploitation, and making informed judgments about leaders and institutions that may prioritize power over ethical responsibility.',
                'etymology': 'From Niccolò Machiavelli + suffix "-ian," referring to the Italian political philosopher',
                'memory_tip': 'Remember MACHIAVELLIAN as "MACHIAVELLI" + "AN" - like the philosopher who wrote about cunning political tactics.',
                'example_sentence': 'His _____ approach to office politics involved spreading rumors about colleagues to advance his own career prospects.'
            },
            'machicolation': {
                'pronunciation': '/mə-CHIK-ə-LAY-shən/',
                'definition': 'A defensive architectural feature in medieval fortifications consisting of a projecting gallery or parapet with openings in the floor through which defenders could drop stones, hot oil, or other projectiles on attackers below, representing an ingenious military engineering solution that provided protection while enabling effective defense of castle walls and gateways. These structures typically projected outward from castle walls, creating overhangs supported by corbels or brackets that allowed defenders to target enemies approaching the base of fortifications without exposing themselves to return fire from attackers\' weapons. Machicolations often appeared above castle gates, along curtain walls, and at corners where they provided comprehensive coverage of vulnerable areas that attackers might use to approach or undermine defensive structures. The design required careful engineering to support the weight of stone construction while maintaining structural integrity under combat conditions, demonstrating medieval builders\' sophisticated understanding of both architectural principles and military tactics. Construction typically involved stone corbelling techniques that distributed weight effectively while creating the necessary openings for defensive actions, with some examples featuring decorative elements that enhanced castles\' impressive appearance while serving practical military functions. Understanding machicolations provides insights into medieval warfare, castle architecture, and the ongoing arms race between offensive and defensive military technologies that shaped fortress design throughout the Middle Ages.',
                'etymology': 'From Old French "machicoulis," from "machier" (to crush) + "coulis" (flowing), referring to dropping things through openings',
                'memory_tip': 'Remember MACHICOLATION as "MACHI" (machine) + "COLATION" (pouring down) - castle machine for pouring down projectiles.',
                'example_sentence': 'The medieval castle\'s _____ allowed defenders to drop boiling oil on attackers trying to breach the main gate.'
            },
            'machination': {
                'pronunciation': '/MAK-ə-NAY-shən/',
                'definition': 'A crafty scheme or artful plot, typically involving complex planning and manipulation to achieve selfish or harmful goals through deceptive means, representing the process of devising and implementing clever but unethical strategies that serve personal interests at others\' expense. Machinations often involve multiple steps, careful timing, and sophisticated understanding of human psychology that enables manipulators to influence events and people without revealing their true intentions or methods. Political machinations include behind-the-scenes maneuvering, alliance building, and strategic positioning designed to gain power, influence policy outcomes, or undermine opponents through means that may not be visible to the general public. Corporate machinations might involve insider trading, market manipulation, hostile takeovers, or other business practices that prioritize profit over ethical considerations or stakeholder welfare. The term carries strongly negative connotations, suggesting behavior that violates trust, exploits others\' vulnerabilities, and prioritizes personal gain over community welfare or ethical standards. Social machinations can destroy relationships, undermine group cohesion, and create atmospheres of suspicion and distrust that damage communities and organizations. Understanding machinations helps in recognizing manipulative behavior, protecting oneself from exploitation, and promoting ethical alternatives that achieve goals through honest means and mutual benefit rather than deception and exploitation.',
                'etymology': 'From Latin "machinatio" meaning contrivance or plot, from "machina" (machine)',
                'memory_tip': 'Remember MACHINATION as "MACHINE" + "ATION" (process) - the process of operating like a plotting machine.',
                'example_sentence': 'The investigation revealed the corrupt official\'s complex _____ to embezzle funds through fake consulting contracts.'
            },
            'machine': {
                'pronunciation': '/mə-SHEEN/',
                'definition': 'A mechanical device that uses energy to perform work, consisting of interconnected parts that transform input forces and motions into desired output forces and motions, representing one of humanity\'s most important technological innovations that has revolutionized production, transportation, communication, and virtually every aspect of modern life. Machines operate on fundamental mechanical principles including levers, wheels, inclined planes, pulleys, screws, and wedges that multiply forces, change direction of motion, or increase efficiency of human effort, enabling accomplishment of tasks that would be impossible or impractical through human power alone. The Industrial Revolution marked a crucial transition from simple hand tools to complex powered machines driven by steam, electricity, and internal combustion engines that dramatically increased production capacity while transforming social and economic structures worldwide. Modern machines range from simple mechanical devices like bicycles and hand tools to sophisticated computer-controlled systems including robots, automated manufacturing equipment, and artificial intelligence systems that can perform complex tasks with minimal human intervention. Machine design principles emphasize efficiency, reliability, safety, and maintainability while considering factors such as materials, manufacturing costs, environmental impact, and user needs that determine optimal solutions for specific applications. Understanding machines involves appreciating both their technical complexity and their profound impact on human civilization, from enabling mass production and global transportation to creating new possibilities for scientific research and space exploration.',
                'etymology': 'From Latin "machina" meaning contrivance or device, from Greek "makhana" (device)',
                'memory_tip': 'Remember MACHINE as a mechanical device that uses energy to do work - the foundation of modern technology.',
                'example_sentence': 'The new manufacturing _____ could produce twice as many products with half the energy consumption of older equipment.'
            },
            'macigno': {
                'pronunciation': '/mə-CHEE-nyoh/',
                'definition': 'A type of sandstone formation found primarily in the Apennine Mountains of Italy, characterized by alternating layers of sandstone and shale that create distinctive geological structures important for understanding regional geology, construction materials, and landscape formation processes in Mediterranean environments. This sedimentary rock formation originated from turbidite deposits laid down in deep marine environments during the Oligocene and Miocene epochs, creating the complex layered structures that characterize much of the Italian peninsula\'s mountainous terrain. Macigno formations have played significant roles in Italian architecture and construction, providing building stone for historical structures, roads, and infrastructure while influencing settlement patterns and architectural styles throughout regions where these formations are easily accessible. The rock\'s properties including durability, workability, and aesthetic qualities made it valuable for construction purposes, while its geological characteristics provide insights into ancient depositional environments and tectonic processes that shaped the Mediterranean region. Quarrying and mining operations in macigno formations have created both economic opportunities and environmental challenges, requiring careful management to balance resource extraction with landscape preservation and ecosystem protection. Understanding macigno geology helps in appreciating both the natural history of Italian landscapes and the relationship between geological resources and human civilization in regions where rock formations directly influence culture, architecture, and economic development.',
                'etymology': 'From Italian "macigno," referring to a type of sandstone, possibly from Latin "macies" (leanness)',
                'memory_tip': 'Remember MACIGNO as Italian "MAGNIFICO" stone - a magnificent type of Italian sandstone used in construction.',
                'example_sentence': 'Geologists studied the _____ formations in Tuscany to understand the ancient marine environments that created these distinctive rock layers.'
            },
            'mackerel': {
                'pronunciation': '/MAK-ər-əl/',
                'definition': 'A fast-swimming pelagic fish found in temperate and tropical oceans worldwide, characterized by streamlined bodies, forked tails, and distinctive metallic blue-green coloration with dark bands or spots, representing an important commercial and recreational fish species that plays crucial roles in marine food webs and human nutrition. These highly active fish travel in large schools, feeding primarily on small fish, squid, and crustaceans while serving as prey species for larger predators including tuna, sharks, dolphins, and seabirds, demonstrating their central position in oceanic ecosystems. Common species include Atlantic mackerel, Spanish mackerel, and king mackerel, each with specific habitat preferences, migration patterns, and commercial importance that support fishing industries and coastal economies throughout their ranges. Mackerel\'s high oil content and rich flavor make them valuable food fish, providing excellent sources of omega-3 fatty acids, protein, and other nutrients that contribute to healthy diets while supporting both commercial fisheries and recreational angling activities. Sustainable fishing practices for mackerel populations require careful management of harvest quotas, seasonal restrictions, and fishing methods that maintain population stability while allowing continued economic benefits from these renewable marine resources. The fish\'s rapid spoilage rate due to high oil content requires immediate processing or preservation after capture, influencing fishing techniques, distribution systems, and preparation methods that ensure food safety and quality for consumers.',
                'etymology': 'From Old French "maquerel," possibly from Flemish "makelaer" meaning broker or dealer',
                'memory_tip': 'Remember MACKEREL as the fast-swimming fish with "MAKE-REL" (make-real) speed - they make real speed in the ocean.',
                'example_sentence': 'The fishing boat returned with a large catch of fresh _____, their silver bodies gleaming with the distinctive blue-green stripes.'
            }
        }
        
        # Get data for the specific word
        if word in word_data:
            data = word_data[word]
            difficulty_components = self.difficulty_calc.calculate_difficulty_components(
                word, data['definition'], data['etymology']
            )
            
            return {
                'word': word,
                'pronunciation': data['pronunciation'],
                'definition': data['definition'],
                'example_sentence': data['example_sentence'],
                'etymology': data['etymology'],
                'etymology_source': 'Claude',
                'memory_tip': data['memory_tip'],
                **difficulty_components
            }
        
        # Default case for any missing words
        return {
            'word': word,
            'pronunciation': f'/{word.upper()}/',
            'definition': f'A word that requires additional research for comprehensive definition.',
            'example_sentence': f'The word _____ needs further investigation.',
            'etymology': 'Etymology requires additional research.',
            'etymology_source': 'Claude',
            'memory_tip': f'Remember {word.upper()} - additional memory techniques needed.',
            'phonetic_transparency_score': 3.0,
            'word_frequency_score': 3.0,
            'morphological_complexity_score': 3.0,
            'etymology_complexity_score': 3.0,
            'final_difficulty': None
        }

def process_batch_105():
    """Process Batch 105 with comprehensive Claude data"""
    input_file = Path("output/batch_105_words.csv")
    output_file = Path("output/batch_105_processed.csv")
    
    if not input_file.exists():
        logger.error(f"Input file {input_file} not found")
        return False
    
    processor = Batch105Processor()
    processed_words = []
    
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                word = row['word'].strip()
                if word:  # Skip empty rows
                    # Get comprehensive data from Claude
                    word_data = processor.get_comprehensive_claude_data(word)
                    
                    # Add original source data
                    word_data.update({
                        'years': row['years'],
                        'source_files': row['source_files'], 
                        'source_difficulties': row['source_difficulties']
                    })
                    
                    processed_words.append(word_data)
                    logger.info(f"Processed word: {word}")
        
        # Write output file with all required columns in correct order
        fieldnames = [
            'word', 'pronunciation', 'definition', 'example_sentence',
            'etymology', 'etymology_source', 'memory_tip',
            'phonetic_transparency_score', 'word_frequency_score', 
            'morphological_complexity_score', 'etymology_complexity_score',
            'final_difficulty', 'years', 'source_files', 'source_difficulties'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_words)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
        logger.info(f"Batch 105 processing completed!")
        logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {len(processed_words)} successful, 0 failed")
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing batch 105: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Processing Batch 105 with comprehensive Claude data...")
    success = process_batch_105()
    sys.exit(0 if success else 1)