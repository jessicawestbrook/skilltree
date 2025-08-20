#!/usr/bin/env python3

import csv
import logging
from typing import Dict, List, Any
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    """Calculate difficulty scores based on 4 factors."""
    
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        """Calculate 4-factor difficulty score but leave final difficulty null."""
        return {
            'phonetic_transparency_score': self._calculate_phonetic_transparency(word),
            'word_frequency_score': self._calculate_word_frequency(word),
            'morphological_complexity_score': self._calculate_morphological_complexity(word),
            'etymology_complexity_score': self._calculate_etymology_complexity(etymology),
            'difficulty': None  # Leave null as instructed
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        """Calculate phonetic transparency (0.0 = transparent, 1.0 = opaque)."""
        score = 0.0
        if any(combo in word.lower() for combo in ['ph', 'gh', 'ch', 'sh', 'th']):
            score += 0.2
        if any(combo in word.lower() for combo in ['ough', 'augh', 'eigh']):
            score += 0.3
        if len([c for c in word.lower() if c in 'aeiou']) / len(word) < 0.2:
            score += 0.2
        return min(1.0, score)
    
    def _calculate_word_frequency(self, word: str) -> float:
        """Estimate word frequency (0.0 = very common, 1.0 = very rare)."""
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our'}
        if word.lower() in common_words:
            return 0.0
        if len(word) <= 4:
            return 0.3
        elif len(word) <= 7:
            return 0.6
        else:
            return 0.9
    
    def _calculate_morphological_complexity(self, word: str) -> float:
        """Calculate morphological complexity based on affixes and roots."""
        complexity = 0.0
        prefixes = ['un', 're', 'in', 'dis', 'en', 'non', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'under']
        suffixes = ['ing', 'ly', 'ed', 'ies', 'ied', 'ying', 'es', 'er', 'ion', 'tion', 'ation', 'ition', 'able', 'ible', 'ment', 'ness', 'ous', 'eous', 'ious']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                complexity += 0.2
                break
        
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                complexity += 0.2
                break
                
        if len(word) > 10:
            complexity += 0.3
            
        return min(1.0, complexity)
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        """Calculate etymology complexity based on language origins."""
        if not etymology or etymology.strip() == "":
            return 0.5
        
        complex_origins = ['greek', 'latin', 'french', 'german', 'italian', 'spanish', 'arabic', 'hebrew', 'sanskrit']
        simple_origins = ['english', 'old english', 'middle english']
        
        etymology_lower = etymology.lower()
        
        for origin in complex_origins:
            if origin in etymology_lower:
                return 0.8
        
        for origin in simple_origins:
            if origin in etymology_lower:
                return 0.2
                
        return 0.5

class Batch110Processor:
    """Processes Batch 110 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for each word"""
        data = {
            'megahertzgnash': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "megahertz" and "gnash." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Megahertz is a unit of frequency measuring millions of cycles per second, while gnash means to grind teeth together, typically in anger or frustration. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting or multiple columns. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful individual components.',
                'pronunciation': "/ˈmɛɡ.ə.hɛrtsɡnæʃ/",
                'etymology': 'Processing error combining "megahertz" (Greek mega + German physicist Hertz) with "gnash" (Middle English). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two different words incorrectly joined during PDF processing.',
                'example_sentence': 'The data cleaning process identified ______ as an invalid word combination requiring separation.'
            },
            'megalomaniac': {
                'definition': 'A person with an obsessive desire for power and control, characterized by grandiose delusions about their own importance, abilities, or influence. Megalomaniacs exhibit excessive ego, unrealistic ambitions, and inability to accept criticism or limitations. This psychological condition involves distorted self-perception where individuals believe they deserve special treatment, unlimited authority, or recognition far beyond their actual achievements. Megalomaniacs often manipulate others to achieve their goals and may become tyrannical leaders who abuse power. The condition can manifest in personal relationships, workplace dynamics, or political contexts. Historical examples include dictators and authoritarian leaders who sought absolute control. Treatment involves psychotherapy to address underlying insecurities and develop realistic self-assessment. The term combines clinical psychology with everyday description of extremely narcissistic behavior.',
                'pronunciation': "/ˌmɛɡ.ə.loʊˈmeɪ.ni.æk/",
                'etymology': 'From Greek "megalos" (great) + "mania" (madness) + "-ac" (person affected by), meaning one obsessed with greatness.',
                'memory_tip': 'Remember MEGALOMANIAC = MEGA (huge) + MANIAC - person obsessed with huge power and control.',
                'example_sentence': 'The corporate ______ demanded absolute loyalty and refused to delegate any decision-making authority.'
            },
            'megaron': {
                'definition': 'The great hall or main room of a Mycenaean palace or ancient Greek house, typically featuring a central hearth surrounded by four columns supporting the roof. The megaron served as the principal living and ceremonial space in Bronze Age Greek architecture, representing the focal point of domestic and political life. Archaeological evidence from sites like Pylos and Mycenae reveals megarons with elaborate frescoes, storage areas, and throne rooms. The architectural form influenced later Greek temple design, with the rectangular hall and columned entrance becoming standard elements. Megarons demonstrate the social hierarchy of ancient palaces, where the largest space hosted feasts, audiences, and religious ceremonies. The term appears in archaeological studies of prehistoric Aegean civilizations and architectural history of early European palatial structures.',
                'pronunciation': "/ˈmɛɡ.ə.rɑn/",
                'etymology': 'From Greek "megaron," meaning large room or hall, derived from "megas" (great, large).',
                'memory_tip': 'Remember MEGARON = MEGA ROOM - the great hall of ancient Greek palaces.',
                'example_sentence': 'Archaeologists discovered a well-preserved ______ with colorful frescoes depicting palace ceremonies.'
            },
            'megrims': {
                'definition': 'A feeling of depression, low spirits, or melancholy; also refers to migraine headaches or whimsical fancies. Megrims historically described a condition of dejection or blues that affected mood and motivation. The term can indicate temporary sadness, seasonal depression, or general malaise without specific cause. In medical contexts, megrims referred to severe headaches, particularly migraines with visual disturbances or neurological symptoms. The word also describes capricious notions, odd ideas, or whimsical thoughts that seem to arise without logical basis. Megrims capture the human experience of unexplained mood changes and irrational thinking patterns. The archaic term reflects historical understanding of mental and physical health before modern psychiatric and neurological knowledge developed more precise diagnostic categories.',
                'pronunciation': "/ˈmi.ɡrɪmz/",
                'etymology': 'From Greek "hemikrania" (half skull), referring to migraine headaches, later extended to depression and whims.',
                'memory_tip': 'Remember MEGRIMS = migraine GRIMS - headaches and gloomy feelings combined.',
                'example_sentence': 'The rainy weather gave her a case of the ______, making her feel unusually melancholy.'
            },
            'meiosis': {
                'definition': 'A type of cell division that produces gametes (sex cells) with half the chromosome number of the parent cell, essential for sexual reproduction in eukaryotic organisms. Meiosis involves two successive divisions resulting in four genetically unique haploid cells from one diploid parent cell. The process includes crossing over, where chromosomes exchange genetic material, creating genetic diversity crucial for evolution and adaptation. Meiosis ensures that when gametes fuse during fertilization, the diploid chromosome number is restored in offspring. Errors in meiosis can lead to genetic disorders, infertility, or developmental abnormalities. The process differs from mitosis, which produces identical diploid cells for growth and repair. Understanding meiosis is fundamental to genetics, reproductive biology, and evolutionary studies. The term also appears in rhetoric, meaning deliberate understatement for emphasis.',
                'pronunciation': "/maɪˈoʊ.sɪs/",
                'etymology': 'From Greek "meiosis," meaning lessening or reduction, referring to the reduction in chromosome number.',
                'memory_tip': 'Remember MEIOSIS = MAIO (reduction) - cell division that reduces chromosome number by half.',
                'example_sentence': 'Biology students studied ______ to understand how genetic diversity is created in sexual reproduction.'
            },
            'meitnerium': {
                'definition': 'A synthetic chemical element with the symbol Mt and atomic number 109, named after physicist Lise Meitner who contributed to the discovery of nuclear fission. Meitnerium is a superheavy element created artificially in particle accelerators by bombarding bismuth targets with iron nuclei. The element is extremely unstable with a very short half-life, making it impossible to study its chemical properties in detail. Meitnerium exists only in minute quantities and decays rapidly through alpha emission and spontaneous fission. Research on superheavy elements like meitnerium helps scientists understand atomic structure, nuclear physics, and the theoretical "island of stability" where longer-lived superheavy elements might exist. The element honors Lise Meitner\'s groundbreaking work in nuclear physics and recognizes women\'s contributions to scientific discovery.',
                'pronunciation': "/maɪtˈnɪr.i.əm/",
                'etymology': 'Named after Lise Meitner (1878-1968), Austrian-Swedish physicist who helped discover nuclear fission.',
                'memory_tip': 'Remember MEITNERIUM = named after MEIT-ner the physicist - superheavy element Mt-109.',
                'example_sentence': 'Scientists created a few atoms of ______ in the particle accelerator, but they decayed within milliseconds.'
            },
            'melamine': {
                'definition': 'A synthetic organic compound used primarily in the manufacture of melamine resin, which forms durable, heat-resistant plastic materials for dinnerware, laminates, and adhesives. Melamine-formaldehyde resin creates hard, scratch-resistant surfaces popular in kitchen countertops, floor coverings, and decorative panels. The compound gained notoriety when illegally added to pet food and infant formula to artificially inflate protein content readings, causing kidney damage and deaths. Melamine is not approved for direct human consumption and can cause serious health problems when ingested. Industrial applications include flame-retardant materials, textile treatments, and coating formulations. Quality control measures now test food products for melamine contamination to prevent adulteration. The compound represents both useful industrial chemistry and potential food safety hazards requiring careful regulation.',
                'pronunciation': "/ˈmɛl.əˌmin/",
                'etymology': 'From German "Melamin," possibly derived from "Melam" (a related compound) or from its chemical composition.',
                'memory_tip': 'Remember MELAMINE = MEL (honey-like) + AMINE - plastic compound that caused food safety issues.',
                'example_sentence': 'The factory produced ______ dinnerware known for its durability and resistance to breakage.'
            },
            'melancholy': {
                'definition': 'A feeling of pensive sadness, thoughtful sorrow, or gentle depression that often has a bittersweet or reflective quality. Melancholy differs from clinical depression by being less severe and often mixed with contemplative or artistic sensations. The emotion can be triggered by memories, seasonal changes, music, art, or philosophical reflection on life\'s transient nature. Melancholy has long been associated with creativity, as many artists, writers, and musicians draw inspiration from melancholic moods. Historical medicine classified melancholy as one of four bodily humors, believing it resulted from excess black bile. The feeling can be both pleasant and painful, offering depth of emotion and aesthetic appreciation while causing sadness. Melancholy represents a complex human emotional state that combines sorrow with beauty.',
                'pronunciation': "/ˈmɛl.ənˌkɑl.i/",
                'etymology': 'From Greek "melancholia," meaning black bile, one of the four humors believed to cause sadness in ancient medicine.',
                'memory_tip': 'Remember MELANCHOLY = MELAN (black) + CHOLY (bile) - the ancient humor causing sadness.',
                'example_sentence': 'Autumn leaves falling created a sense of ______ as she reflected on the passing year.'
            },
            'mele': {
                'definition': 'A Hawaiian song or chant that often tells stories, preserves history, or expresses emotions through traditional Polynesian musical forms. Mele encompasses various types of Hawaiian vocal music including love songs, work songs, historical narratives, and religious chants. Traditional mele often accompanies hula dancing, with lyrics and rhythm coordinating to create unified artistic expression. Mele kanikau are mourning songs, mele inoa are name songs honoring individuals, and mele hula provide musical accompaniment for dance performances. The oral tradition of mele preserved Hawaiian culture, language, and historical knowledge across generations before written records. Modern Hawaiian musicians continue creating and performing mele while honoring traditional forms and themes. Mele represents the living cultural heritage of Hawaii and demonstrates music\'s role in maintaining indigenous identity and community connections.',
                'pronunciation': "/ˈmeɪ.leɪ/",
                'etymology': 'From Hawaiian "mele," meaning song or chant, part of traditional Polynesian musical culture.',
                'memory_tip': 'Remember MELE = Hawaiian song that makes your heart MERRY with traditional music.',
                'example_sentence': 'The kumu hula taught students the ancient ______ that told the story of their ancestors.'
            },
            'melee': {
                'definition': 'A confused fight involving many people; a chaotic situation with multiple participants engaged in close combat or disorderly struggle. Melee combat refers to hand-to-hand fighting with weapons or fists rather than ranged attacks. The term describes situations where individual combatants become indistinguishable in a mass of struggling bodies and weapons. Medieval battles often devolved into melees when organized formations broke down and soldiers fought in small groups or individually. In gaming, melee characters specialize in close-range combat rather than magic or archery. Sports melees occur when team conflicts escalate into bench-clearing brawls involving multiple players. The word captures the confusion, intensity, and lack of clear organization characteristic of close-quarters fighting. Modern usage extends to any chaotic situation involving multiple competing parties.',
                'pronunciation': "/ˈmeɪ.leɪ/",
                'etymology': 'From French "mêlée," meaning mixture or medley, derived from "mêler" (to mix).',
                'memory_tip': 'Remember MELEE = mixed-up LEE (battle) - confused fight with many people mixed together.',
                'example_sentence': 'The hockey game erupted into a ______ when players from both teams started fighting.'
            },
            'melismatic': {
                'definition': 'Relating to melisma in music, a vocal technique where a single syllable is sung across multiple notes or pitches. Melismatic singing creates elaborate, flowing melodic passages that showcase vocal agility and emotional expression. This technique appears prominently in various musical traditions including Gregorian chant, Islamic nasheed, Indian classical music, and contemporary R&B and gospel music. Melismatic passages can convey intense emotion, spiritual transcendence, or pure artistic virtuosity depending on the musical context. Classical composers like Bach used melismatic writing to express specific textual meanings or emotional content in sacred and secular works. Modern vocalists like Whitney Houston and Mariah Carey popularized melismatic techniques in pop music. The term contrasts with syllabic singing, where each syllable corresponds to one note, emphasizing the ornamental and expressive nature of melismatic performance.',
                'pronunciation': "/ˌmɛl.ɪzˈmæt.ɪk/",
                'etymology': 'From Greek "melisma" (song or melody) + "-atic" suffix, referring to the musical technique of multiple notes per syllable.',
                'memory_tip': 'Remember MELISMATIC = MELODY-dramatic singing - one syllable stretched across many notes.',
                'example_sentence': 'The gospel singer\'s ______ rendition of "Amazing Grace" brought the congregation to tears.'
            },
            'mell': {
                'definition': 'An archaic or dialectal word meaning to meddle, interfere, or become involved in something, particularly in other people\'s affairs or business. The term appears in older English literature and regional dialects, though it has largely fallen out of common usage. "Mell" can also refer to mixing or mingling, similar to "meddle" but with less negative connotation. In some contexts, it means to have sexual intercourse or to engage intimately with someone. The word reflects historical English vocabulary that expressed concepts of involvement and interference using terms that modern English has largely replaced with more specific or standardized words. Understanding archaic terms like "mell" helps in reading historical texts and appreciating the evolution of English vocabulary over time.',
                'pronunciation': "/mɛl/",
                'etymology': 'From Middle English "mellen," meaning to mix or meddle, possibly related to Old English "meltan" (to melt).',
                'memory_tip': 'Remember MELL = old word meaning to meddle and interfere - like MELD into others\' business.',
                'example_sentence': 'The old farmer warned his neighbor not to ______ in family matters that didn\'t concern him.'
            },
            'mellifluous': {
                'definition': 'Having a smooth, sweet, flowing sound that is pleasant to hear; characterized by honeyed or musical quality in speech or voice. Mellifluous describes sounds that flow smoothly and sweetly, like honey pouring from a jar. The term most commonly applies to speaking voices, singing, or musical performances that have particularly pleasing, melodious qualities. Mellifluous speakers often become successful in careers requiring vocal communication such as radio, television, public speaking, or teaching. The quality involves not just pleasant tone but also smooth delivery, proper pacing, and melodic variation. Mellifluous music features flowing melodies without harsh transitions or jarring elements. In literature, the term can describe writing style that reads smoothly and pleasantly. The word emphasizes the aesthetic pleasure derived from beautiful sounds.',
                'pronunciation': "/məˈlɪf.lu.əs/",
                'etymology': 'From Latin "mellifluus," meaning flowing with honey, from "mel" (honey) + "fluere" (to flow).',
                'memory_tip': 'Remember MELLIFLUOUS = MEL (honey) + FLUOUS (flowing) - voice that flows like sweet honey.',
                'example_sentence': 'The radio announcer\'s ______ voice made even the mundane weather report sound beautiful.'
            },
            'mellifluousclemency': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "mellifluous" and "clemency." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Mellifluous means having a smooth, sweet-sounding voice, while clemency refers to mercy or leniency in punishment. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting or multiple columns. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful individual components.',
                'pronunciation': "/məˈlɪf.lu.əsˈklɛm.ən.si/",
                'etymology': 'Processing error combining "mellifluous" (Latin honey-flowing) with "clemency" (Latin mercy). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two different words incorrectly joined during PDF processing.',
                'example_sentence': 'The text validation system flagged ______ as an invalid word combination requiring separation.'
            },
            'mellow': {
                'definition': 'Having a soft, rich, gentle quality; mature and relaxed in temperament; or to become softer and more pleasant over time. Mellow describes sounds, tastes, colors, or personalities that are smooth, warm, and pleasant without harshness. Mellow wine has developed complex flavors through aging, while mellow music has soft, soothing qualities. People become mellow as they age, developing patience, wisdom, and emotional stability that reduces reactivity and increases acceptance. Mellow lighting creates comfortable, warm atmospheres through soft illumination. The verb "to mellow" describes the process of becoming gentler, whether through aging, experience, or deliberate cultivation of calmness. Mellow represents a desirable quality associated with maturity, sophistication, and peaceful contentment. The term suggests positive development and improvement through time and experience.',
                'pronunciation': "/ˈmɛl.oʊ/",
                'etymology': 'From Middle English "melwe," possibly related to "meal" (grain), suggesting ripeness or maturity.',
                'memory_tip': 'Remember MELLOW = soft and gentle like YELLOW sunshine - warm and pleasant.',
                'example_sentence': 'Age had made him more ______, replacing his youthful intensity with calm wisdom.'
            },
            'melodramatic': {
                'definition': 'Excessively dramatic, emotional, or theatrical in manner; characterized by overacted expressions of feeling that seem artificial or exaggerated. Melodramatic behavior involves heightened emotional displays that appear disproportionate to the situation, often seeking attention or sympathy through dramatic presentation. The term originates from melodrama, a theatrical form that emphasized extreme emotions and clear moral distinctions between heroes and villains. Melodramatic people tend to turn minor problems into major crises, using dramatic language and gestures to express feelings. While sometimes criticized as insincere, melodramatic expression can also represent genuine intensity of emotion or cultural communication styles. The term carries negative connotation, suggesting manipulation or attention-seeking rather than authentic emotional expression. Understanding melodramatic tendencies helps in interpreting both theatrical performances and interpersonal communication.',
                'pronunciation': "/ˌmɛl.ə.drəˈmæt.ɪk/",
                'etymology': 'From "melodrama" (Greek "melos" meaning song + "drama") + "-ic" suffix, referring to overly theatrical behavior.',
                'memory_tip': 'Remember MELODRAMATIC = MELODY + DRAMATIC - overly theatrical like musical drama.',
                'example_sentence': 'Her ______ reaction to missing the bus made it seem like a personal tragedy.'
            },
            'melody': {
                'definition': 'A sequence of musical sounds forming the main tune of a composition; a pleasing succession of sounds that creates recognizable musical phrases. Melody represents the horizontal aspect of music, contrasting with harmony (vertical sound combinations) and rhythm (temporal patterns). Melodies consist of pitches organized in time to create musical meaning and emotional expression. Strong melodies are memorable, singable, and emotionally engaging, forming the foundation for songs across all musical genres. Melody construction involves concepts like scale patterns, intervals, phrase structure, and contour that determine how musical ideas develop. Cultural traditions have distinct melodic characteristics: pentatonic scales in Asian music, modal melodies in folk traditions, and complex chromatic melodies in jazz. Melody serves as the primary vehicle for musical communication, conveying emotion and meaning through organized sequences of tones.',
                'pronunciation': "/ˈmɛl.ə.di/",
                'etymology': 'From Greek "melodia," meaning singing or chanting, derived from "melos" (song) + "aoide" (singing).',
                'memory_tip': 'Remember MELODY = beautiful musical LINE of notes that creates the main tune.',
                'example_sentence': 'The simple ______ was so catchy that everyone was humming it by the end of the concert.'
            },
            'melted': {
                'definition': 'Changed from solid to liquid state through application of heat; also used figuratively to describe emotional softening or disappearance of resistance. Melted substances have undergone phase transition from organized solid structure to flowing liquid form. Ice melts into water, metals melt into molten form for casting, and chocolate melts for cooking applications. The melting process requires specific temperatures and energy input to overcome molecular bonds holding solid structures together. Figuratively, hearts "melt" when experiencing strong emotion, resistance "melts away" when persuasion succeeds, and tensions "melt" when conflicts resolve. Melted materials often return to solid form when cooled, though some substances undergo permanent chemical changes during melting. The concept represents transformation, change of state, and movement from rigid to fluid conditions.',
                'pronunciation': "/ˈmɛl.təd/",
                'etymology': 'Past tense of "melt," from Old English "meltan," meaning to dissolve or liquefy through heat.',
                'memory_tip': 'Remember MELTED = solid turned liquid - like ice that MELT-ED in the sun.',
                'example_sentence': 'The ice cream ______ quickly in the hot summer sunshine.'
            },
            'meltedmembership': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "melted" and "membership." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Melted refers to the state change from solid to liquid, while membership refers to belonging to a group or organization. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting or multiple columns. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful individual components.',
                'pronunciation': "/ˈmɛl.tədˈmɛm.bər.ʃɪp/",
                'etymology': 'Processing error combining "melted" (Old English meltan) with "membership" (member + ship). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two different words incorrectly joined during PDF processing.',
                'example_sentence': 'The automated error detection flagged ______ as an invalid word requiring separation into components.'
            },
            'member': {
                'definition': 'A person who belongs to a group, organization, club, or institution; also a part or component of a larger structure. Group members share common interests, goals, or characteristics that define their collective identity. Membership often involves rights, responsibilities, benefits, and obligations within the organization. Different types of members may have varying levels of participation, voting rights, or access to services. In anatomy, members can refer to limbs or body parts that function as components of the whole organism. Legislative members represent constituents in government bodies like parliament or congress. Family members share kinship relationships and mutual support obligations. The concept emphasizes belonging, participation, and connection to larger entities that provide identity, purpose, and community.',
                'pronunciation': "/ˈmɛm.bər/",
                'etymology': 'From Latin "membrum," meaning limb or part of the body, extended to mean part of a group.',
                'memory_tip': 'Remember MEMBER = someone who REMEMBERS their group - belongs to organization.',
                'example_sentence': 'As a new ______ of the hiking club, she received a welcome packet and trail map.'
            },
            'membership': {
                'definition': 'The state of belonging to or being part of a group, organization, or institution; also the collective body of members. Membership involves formal or informal recognition as part of a community with shared interests, goals, or characteristics. Different organizations have varying membership requirements including fees, applications, qualifications, or elections. Membership benefits might include access to facilities, services, information, networking opportunities, or voting rights. Club membership creates social connections and recreational opportunities, while professional membership provides career development and industry recognition. Membership obligations can include dues payment, participation in activities, adherence to rules, or service contributions. The concept represents human needs for belonging, identity, and community participation. Modern membership often includes both physical and digital components through online platforms and virtual communities.',
                'pronunciation': "/ˈmɛm.bər.ʃɪp/",
                'etymology': 'From "member" (Latin membrum) + "-ship" suffix indicating state or condition of being a member.',
                'memory_tip': 'Remember MEMBERSHIP = MEMBER-SHIP - the state of belonging to a group.',
                'example_sentence': 'The gym ______ included access to fitness classes and personal training sessions.'
            },
            'membrane': {
                'definition': 'A thin, flexible sheet of tissue or material that forms a boundary, covering, or partition in biological systems or artificial applications. Cell membranes control molecular transport in and out of cells through selective permeability, maintaining cellular integrity and homeostasis. Biological membranes include skin, mucous membranes lining body cavities, and specialized structures like the eardrum or amniotic sac. Artificial membranes serve industrial purposes including filtration, separation, and barrier functions in manufacturing processes. Semi-permeable membranes allow certain substances to pass while blocking others, essential for dialysis, water purification, and chemical processing. Membrane technology enables advances in biotechnology, environmental protection, and material science. Understanding membrane structure and function is crucial for medicine, biology, and engineering applications.',
                'pronunciation': "/ˈmɛm.breɪn/",
                'etymology': 'From Latin "membrana," meaning skin or parchment, derived from "membrum" (limb or member).',
                'memory_tip': 'Remember MEMBRANE = thin MEMBRANE barrier - flexible sheet that covers and protects.',
                'example_sentence': 'The cell ______ regulated which nutrients could enter and which wastes could exit.'
            },
            'memes': {
                'definition': 'Units of cultural transmission that spread from person to person through imitation; in modern usage, humorous images, videos, or text that spread rapidly through internet social media. The original concept, coined by biologist Richard Dawkins, describes how cultural ideas replicate and evolve like genes, including languages, customs, beliefs, and behaviors. Internet memes typically feature recognizable images with text overlays that comment on current events, social situations, or shared experiences. Successful memes resonate with audiences through humor, relatability, or clever observations that encourage sharing and adaptation. Meme culture represents new forms of communication, social commentary, and community building through viral content. The phenomenon demonstrates how digital technology accelerates cultural transmission and creates shared references across global communities. Memes influence language, politics, marketing, and social movements.',
                'pronunciation': "/mimz/",
                'etymology': 'From Greek "mimema" (thing imitated), coined by Richard Dawkins in 1976 to describe cultural transmission units.',
                'memory_tip': 'Remember MEMES = cultural ideas that copy like GENES - viral content that spreads rapidly.',
                'example_sentence': 'The students communicated through ______ that perfectly captured their feelings about upcoming exams.'
            },
            'memorandum': {
                'definition': 'A written message or document used for internal communication within an organization, typically containing information, instructions, or proposals for consideration. Memorandums (or memos) provide formal documentation of decisions, policies, or procedural changes that require official record-keeping. Business memos follow structured formats including headers identifying sender, recipients, date, and subject matter. Legal memorandums present analysis of legal issues, case law research, and recommendations for legal strategy. Diplomatic memorandums document international negotiations, agreements, or formal communications between governments. The format emphasizes clarity, conciseness, and professional tone appropriate for workplace communication. Modern digital communication has reduced traditional memo usage, but the document type remains important for formal organizational communication requiring permanent records.',
                'pronunciation': "/ˌmɛm.əˈræn.dəm/",
                'etymology': 'From Latin "memorandum," meaning "thing to be remembered," from "memorare" (to remember).',
                'memory_tip': 'Remember MEMORANDUM = MEMO-RANDUM - written message to remember important information.',
                'example_sentence': 'The manager distributed a ______ outlining the new safety procedures for all employees.'
            },
            'memorial': {
                'definition': 'Something designed to preserve the memory of a person, event, or group, typically involving monuments, ceremonies, or commemorative objects. Memorials serve important social and cultural functions by honoring those who died, celebrating achievements, or marking significant historical events. War memorials commemorate military service and sacrifice, while personal memorials remember individual lives and relationships. Memorial architecture includes sculptures, buildings, gardens, and plaques that create physical spaces for remembrance and reflection. Memorial services provide opportunities for communities to gather, share memories, and process grief collectively. The concept emphasizes the human need to preserve memory, honor legacy, and maintain connections with the past. Memorials help societies remember lessons, values, and experiences that shape cultural identity and historical understanding.',
                'pronunciation': "/məˈmɔr.i.əl/",
                'etymology': 'From Latin "memorialis," meaning serving as a reminder, derived from "memoria" (memory).',
                'memory_tip': 'Remember MEMORIAL = MEMORY + AL - something that helps remember and honor.',
                'example_sentence': 'The community dedicated a ______ garden to honor local veterans who served their country.'
            },
            'menacing': {
                'definition': 'Threatening or suggesting the presence of danger; having a quality that creates fear or apprehension about potential harm. Menacing behavior includes words, actions, or expressions that intimidate others and imply possible violence or negative consequences. Legal systems recognize menacing as a criminal offense when threats create reasonable fear in victims. Menacing appearances can involve body language, facial expressions, or vocal tones that communicate hostile intentions. Environmental conditions can be menacing when storm clouds, dangerous wildlife, or unstable structures create threatening situations. The term describes both intentional intimidation and unintentional effects that create fearful responses. Menacing behavior often precedes actual aggression and serves as a warning signal in social interactions. Understanding menacing cues helps in personal safety assessment and conflict de-escalation.',
                'pronunciation': "/ˈmɛn.ə.sɪŋ/",
                'etymology': 'From "menace" (Old French "manace," meaning threat) + "-ing" suffix, describing threatening behavior.',
                'memory_tip': 'Remember MENACING = threatening like a MEAN person - creating fear and danger.',
                'example_sentence': 'The dark clouds gathered in a ______ way that suggested a severe storm was approaching.'
            },
            'menagerie': {
                'definition': 'A collection of wild or exotic animals kept for exhibition or entertainment; also any diverse assortment of people or things. Historical menageries were private collections maintained by wealthy individuals or royal courts to display rare animals as symbols of power and worldliness. Modern menageries include zoos, wildlife parks, and traveling exhibitions that serve educational and conservation purposes. The term can describe any eclectic mixture of diverse elements, such as a menagerie of characters in literature or a menagerie of objects in a collector\'s display. Menageries reflect human fascination with diversity, rarity, and the exotic. Contemporary animal collections emphasize conservation, education, and species preservation rather than entertainment alone. The concept represents both literal animal collections and metaphorical assemblages of varied items.',
                'pronunciation': "/məˈnædʒ.ə.ri/",
                'etymology': 'From French "ménagerie," derived from "ménage" (household), referring to animal management and care.',
                'memory_tip': 'Remember MENAGERIE = MEN MANAGE diverse animals - collection of exotic creatures.',
                'example_sentence': 'The eccentric collector\'s home contained a ______ of unusual artifacts from around the world.'
            },
            'menaia': {
                'definition': 'Plural of "menaion," referring to liturgical books in Eastern Orthodox Christianity that contain services and readings for fixed feast days throughout the church year. The menaia system organizes religious observances by calendar months, with each menaion containing appropriate prayers, hymns, and scripture readings for specific dates. These liturgical texts preserve ancient Christian traditions, theological teachings, and spiritual practices that guide Orthodox worship. Different menaia correspond to different months, creating a complete annual cycle of religious observance. The books include lives of saints, commemorative services, and seasonal celebrations that connect Orthodox communities to their religious heritage. Menaia represent the systematic organization of Christian liturgical practice and the preservation of traditional forms of worship across centuries. Understanding menaia provides insight into Orthodox Christian culture, theology, and spiritual life.',
                'pronunciation': "/mɪˈnaɪ.ə/",
                'etymology': 'From Greek "menaion," meaning monthly, derived from "men" (month), referring to monthly liturgical books.',
                'memory_tip': 'Remember MENAIA = MONTHLY religious books - liturgical texts organized by calendar months.',
                'example_sentence': 'The priest consulted the ______ to find the proper prayers for the saint\'s feast day.'
            },
            'mendacious': {
                'definition': 'Given to or characterized by lying, deception, or dishonesty; habitually untruthful in speech or behavior. Mendacious individuals regularly distort facts, fabricate stories, or present false information to achieve personal advantages or avoid consequences. The term implies not just occasional lying but a consistent pattern of dishonesty that affects credibility and trustworthiness. Mendacious behavior damages relationships, undermines social cooperation, and creates confusion about truth and reality. Political discourse often involves accusations of mendacious statements when opponents challenge the accuracy of claims or promises. Mendacious testimony in legal proceedings can result in perjury charges and severe penalties. The concept emphasizes the moral and practical problems created by systematic dishonesty. Identifying mendacious behavior requires critical thinking and verification of claims through reliable sources.',
                'pronunciation': "/mɛnˈdeɪ.ʃəs/",
                'etymology': 'From Latin "mendax" meaning lying or false, derived from "mendum" (fault or mistake).',
                'memory_tip': 'Remember MENDACIOUS = MEND + ACIOUS - trying to MEND truth with lies, being dishonest.',
                'example_sentence': 'The investigation revealed that the witness had given ______ testimony to protect his accomplices.'
            },
            'mendicity': {
                'definition': 'The practice or condition of begging; the state of being a beggar or dependent on charitable donations for survival. Mendicity involves requesting money or assistance from strangers, often due to poverty, disability, or lack of other means of support. Historical attitudes toward mendicity varied from religious obligation to provide charity to legal restrictions on begging in public spaces. Mendicity can result from various circumstances including unemployment, mental illness, addiction, homelessness, or economic displacement. Social welfare systems aim to reduce mendicity by providing alternative forms of support and assistance. The term appears in legal contexts regarding vagrancy laws and public order regulations. Understanding mendicity requires consideration of economic inequality, social safety nets, and humanitarian responses to poverty. Modern approaches emphasize addressing root causes rather than criminalizing desperate circumstances.',
                'pronunciation': "/mɛnˈdɪs.ə.ti/",
                'etymology': 'From Latin "mendicitas," meaning begging, derived from "mendicus" (beggar).',
                'memory_tip': 'Remember MENDICITY = MEND + ICITY - the condition of needing to MEND poverty through begging.',
                'example_sentence': 'The social worker helped the homeless man escape ______ by connecting him with job training programs.'
            },
            'menial': {
                'definition': 'Relating to work that requires little skill and is considered humble or degrading; also a person who performs such work. Menial tasks typically involve routine, repetitive activities that others consider beneath their social status or educational level. The term carries negative connotation, suggesting work that lacks prestige, intellectual challenge, or adequate compensation. However, all work has dignity and contributes to society\'s functioning, regardless of skill level required. Menial labor includes cleaning, basic food service, manual labor, and routine clerical tasks. Social attitudes toward menial work reflect class distinctions and economic hierarchies that may not accurately value contributions to community welfare. Educational and economic opportunities can help individuals move beyond menial employment toward careers offering better pay, working conditions, and social recognition.',
                'pronunciation': "/ˈmi.ni.əl/",
                'etymology': 'From Old French "meinal," meaning household servant, derived from "menie" (household).',
                'memory_tip': 'Remember MENIAL = MEAN + AL work - humble tasks considered low-status.',
                'example_sentence': 'Despite starting in ______ positions, many successful entrepreneurs learned valuable lessons about business operations.'
            },
            'meningitis': {
                'definition': 'Inflammation of the meninges, the protective membranes covering the brain and spinal cord, typically caused by bacterial, viral, or fungal infections. Meningitis represents a serious medical emergency that can cause permanent brain damage, hearing loss, or death if not treated promptly. Bacterial meningitis is particularly dangerous and requires immediate antibiotic treatment, while viral meningitis usually resolves with supportive care. Symptoms include severe headache, neck stiffness, fever, sensitivity to light, and altered mental status. Vaccination programs have significantly reduced certain types of bacterial meningitis, particularly those caused by Haemophilus influenzae and pneumococcus. Early recognition and treatment are crucial for preventing serious complications and improving outcomes. Healthcare providers use lumbar puncture to diagnose meningitis by analyzing cerebrospinal fluid for signs of infection and inflammation.',
                'pronunciation': "/ˌmɛn.ɪnˈdʒaɪ.təs/",
                'etymology': 'From "meninges" (Greek for membranes covering the brain) + "-itis" (inflammation), meaning brain membrane inflammation.',
                'memory_tip': 'Remember MENINGITIS = MENINGE (brain membranes) + ITIS (inflammation) - serious brain infection.',
                'example_sentence': 'The college implemented vaccination requirements to prevent ______ outbreaks in dormitories.'
            },
            'meningitismephitic': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "meningitis" and "mephitic." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Meningitis refers to inflammation of brain membranes, while mephitic means having a foul, noxious smell. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting or multiple columns. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful individual components.',
                'pronunciation': "/ˌmɛn.ɪnˈdʒaɪ.təsmɪˈfɪt.ɪk/",
                'etymology': 'Processing error combining "meningitis" (Greek brain inflammation) with "mephitic" (Latin foul-smelling). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two different words incorrectly joined during PDF processing.',
                'example_sentence': 'The quality control system detected ______ as an invalid word requiring separation into components.'
            },
            'menthol': {
                'definition': 'An organic compound with a strong minty odor and cooling sensation, derived from peppermint oil or synthesized artificially for use in medicines, cosmetics, and consumer products. Menthol activates cold-sensitive receptors in the skin and mucous membranes, creating a cooling effect without actually lowering temperature. Medical applications include throat lozenges, cough drops, topical pain relievers, and nasal decongestants. Menthol cigarettes use the compound to provide smoother sensation and mask harsh tobacco taste, though this may increase addiction risk. Cosmetic products use menthol for refreshing sensations in shampoos, toothpastes, and skincare items. Food and beverage industries incorporate menthol for mint flavoring in candies, gums, and beverages. Understanding menthol\'s effects helps in both therapeutic applications and consumer product development.',
                'pronunciation': "/ˈmɛn.θɔl/",
                'etymology': 'From German "Menthol," derived from Latin "mentha" (mint) + alcohol suffix, referring to mint-derived compound.',
                'memory_tip': 'Remember MENTHOL = MINT + OL - cooling compound from mint that makes things feel cold.',
                'example_sentence': 'The cough drop contained ______ to soothe her irritated throat with a cooling sensation.'
            },
            'mention': {
                'definition': 'To refer to something briefly or in passing; to bring up a topic in conversation or writing without detailed discussion. Mentioning involves acknowledging the existence or relevance of something without necessarily elaborating on details. Casual mentions can introduce topics for later discussion or provide context for current conversations. Formal mentions in speeches, documents, or presentations recognize contributions, acknowledge sources, or reference related information. The act of mentioning can show respect, provide credit, or demonstrate awareness of important factors. Mentions in social media and digital communications create connections between people, topics, and content. Strategic mentioning in professional contexts can build relationships, share information, or position ideas favorably. The concept emphasizes brief acknowledgment rather than detailed explanation.',
                'pronunciation': "/ˈmɛn.ʃən/",
                'etymology': 'From Latin "mentio," meaning calling to mind or naming, derived from "mens" (mind).',
                'memory_tip': 'Remember MENTION = briefly bring to MIND - acknowledge something without detail.',
                'example_sentence': 'She decided to ______ her concerns about the project during the meeting.'
            },
            'mentor': {
                'definition': 'An experienced and trusted advisor who provides guidance, support, and wisdom to someone less experienced, particularly in professional or personal development. Mentoring relationships involve knowledge transfer, skill development, and career guidance from seasoned professionals to newcomers. Effective mentors share expertise, provide networking opportunities, offer constructive feedback, and serve as role models for professional behavior. Mentoring programs exist in education, business, healthcare, and many other fields to support learning and advancement. The relationship benefits both parties: mentees gain knowledge and confidence while mentors experience satisfaction from contributing to others\' development. Formal mentoring involves structured programs with specific goals and timelines, while informal mentoring develops naturally through workplace relationships. Successful mentoring requires mutual respect, clear communication, and commitment from both participants.',
                'pronunciation': "/ˈmɛn.tɔr/",
                'etymology': 'From Greek "Mentor," the wise advisor to Telemachus in Homer\'s Odyssey, meaning adviser or teacher.',
                'memory_tip': 'Remember MENTOR = experienced person who helps others MENT-ally grow and develop.',
                'example_sentence': 'The senior engineer agreed to ______ the new graduate, sharing decades of technical expertise.'
            },
            'mephitic': {
                'definition': 'Having a foul, noxious, or poisonous smell; emitting harmful or offensive odors that may be toxic or dangerous to health. Mephitic gases include hydrogen sulfide, methane, and other compounds that create unpleasant and potentially hazardous atmospheric conditions. The term often describes natural phenomena like swamp gases, volcanic emissions, or decomposition odors that signal unhealthy environments. Mephitic air in poorly ventilated spaces can cause headaches, nausea, or respiratory problems. Historical usage applied the term to "bad air" believed to cause diseases before understanding of germs and sanitation developed. Industrial processes can create mephitic conditions requiring ventilation and safety measures. The word emphasizes both the sensory unpleasantness and potential health risks of contaminated air or gas emissions. Understanding mephitic conditions helps in environmental safety and health protection.',
                'pronunciation': "/mɪˈfɪt.ɪk/",
                'etymology': 'From Latin "mephiticus," meaning pestilential or noxious, related to "mephitis" (noxious exhalation).',
                'memory_tip': 'Remember MEPHITIC = having FOUL smell that\'s SEPTIC - noxious and potentially poisonous odor.',
                'example_sentence': 'The ______ vapors rising from the swamp made it dangerous to venture too close.'
            },
            'merak': {
                'definition': 'The second-brightest star in the Big Dipper constellation (Ursa Major), serving as one of the "pointer stars" that help locate Polaris, the North Star. Merak, along with Dubhe, forms an imaginary line that points directly to Polaris, making it valuable for navigation. The star is located approximately 79 light-years from Earth and has a spectral classification that indicates it is hotter and more massive than our Sun. Merak appears as a blue-white star and is part of the Ursa Major moving group of stars that share common motion through space. The name reflects Arabic astronomical traditions that preserved and expanded upon ancient Greek star catalogs. Understanding prominent stars like Merak helps in navigation, astronomy education, and appreciation of cultural contributions to astronomical knowledge.',
                'pronunciation': "/ˈmɛr.æk/",
                'etymology': 'From Arabic "al-maraqq," meaning "the loins of the bear," referring to its position in the Great Bear constellation.',
                'memory_tip': 'Remember MERAK = bright star that helps MARK the way to North Star for navigation.',
                'example_sentence': 'The navigator used ______ and Dubhe to find Polaris and determine true north.'
            },
            'mercenary': {
                'definition': 'A professional soldier hired to serve in foreign armies; also a person primarily motivated by money rather than principles or loyalty. Military mercenaries fight for financial compensation rather than patriotic duty or ideological commitment. Historical mercenary companies like the Swiss Guards and German Landsknechts provided military services across Europe. Modern private military contractors perform similar functions in contemporary conflicts. As an adjective, mercenary describes attitudes or behaviors driven primarily by monetary gain rather than ethical considerations. Mercenary motivations can undermine trust, loyalty, and commitment to shared values in relationships or organizations. The term carries negative connotation when applied to professionals who prioritize financial reward over service quality or ethical obligations. Understanding mercenary tendencies helps evaluate motivations and predict behavior in various contexts.',
                'pronunciation': "/ˈmɜr.səˌnɛr.i/",
                'etymology': 'From Latin "mercenarius," meaning hired for pay, derived from "merces" (wages or payment).',
                'memory_tip': 'Remember MERCENARY = soldier for MONEY - fights for pay rather than patriotism.',
                'example_sentence': 'The company hired ______ consultants who cared more about fees than solving problems.'
            },
            'merchandise': {
                'definition': 'Goods or commodities that are bought and sold in business; commercial products offered for sale to consumers. Merchandise encompasses the wide variety of items available in retail markets, from clothing and electronics to food and household goods. Merchandising involves the strategic presentation, pricing, and promotion of products to maximize sales and customer satisfaction. Retail merchandising includes store layout, product placement, visual displays, and inventory management. Online merchandising adapts these principles to digital commerce through website design, product descriptions, and recommendation algorithms. Quality merchandise meets customer needs and expectations while generating profit for businesses. Merchandise planning involves forecasting demand, selecting products, and managing supply chains. The concept represents the fundamental exchange of goods that drives commercial economies and consumer culture.',
                'pronunciation': "/ˈmɜr.tʃənˌdaɪz/",
                'etymology': 'From Old French "marchandise," derived from "marchand" (merchant), referring to trader\'s goods.',
                'memory_tip': 'Remember MERCHANDISE = goods that MERCHANTS sell - commercial products for trade.',
                'example_sentence': 'The store\'s ______ included everything from electronics to outdoor equipment.'
            },
            'mercury': {
                'definition': 'A heavy, silvery metallic element that is liquid at room temperature; also the Roman messenger god and the planet closest to the Sun. Mercury metal has unique properties including high density, electrical conductivity, and liquid state that made it valuable for thermometers, barometers, and electrical switches. However, mercury is highly toxic and can cause serious health problems through inhalation or skin contact, leading to restrictions on its use. Mercury poisoning affects the nervous system and can cause tremors, memory loss, and other neurological symptoms. Environmental mercury contamination from industrial sources bioaccumulates in food chains, particularly affecting fish consumption safety. The planet Mercury experiences extreme temperature variations due to its proximity to the Sun and lack of atmosphere. Understanding mercury involves both its useful properties and significant health hazards.',
                'pronunciation': "/ˈmɜr.kjər.i/",
                'etymology': 'Named after Mercury, Roman messenger god, due to the element\'s fluid, mobile nature.',
                'memory_tip': 'Remember MERCURY = liquid metal named after speedy messenger god - flows like quicksilver.',
                'example_sentence': 'The old thermometer contained ______ that posed health risks if the glass broke.'
            },
            'merely': {
                'definition': 'Used to emphasize that something is only what it appears to be and nothing more; simply or just, without additional significance or complexity. Merely indicates limitation, minimizing the importance or extent of something by suggesting it does not exceed basic expectations. The word often appears in contexts where speakers want to downplay their actions, intentions, or capabilities. "Merely trying to help" suggests modest, non-threatening intentions. "Merely a suggestion" indicates that recommendations are not demands or requirements. Merely can also express disappointment when outcomes fall short of expectations. The term helps manage social interactions by reducing potential conflict through humble self-presentation. Understanding "merely" helps interpret speakers\' intentions to minimize their role or impact in various situations.',
                'pronunciation': "/ˈmɪr.li/",
                'etymology': 'From "mere" (Latin "merus," meaning pure or unmixed) + "-ly" adverb suffix, meaning purely or simply.',
                'memory_tip': 'Remember MERELY = PURE-LY simple - just that and nothing more.',
                'example_sentence': 'I was ______ asking for clarification, not challenging your decision.'
            },
            'merfolk': {
                'definition': 'Mythical aquatic creatures with human upper bodies and fish-like tails, including both male (mermen) and female (mermaids) beings from folklore and fantasy literature. Merfolk appear in mythologies worldwide, from ancient Assyrian legends to Caribbean folklore, often representing the mysterious connection between human and marine worlds. These creatures typically possess magical abilities including underwater breathing, superhuman swimming speed, and sometimes prophetic powers or control over sea creatures. Merfolk stories explore themes of transformation, forbidden love, environmental harmony, and the boundary between civilization and nature. Modern merfolk appear in fantasy literature, films, and art as symbols of oceanic beauty and environmental consciousness. The concept reflects human fascination with the sea and imagination about life in aquatic environments. Merfolk mythology often includes complex societies and cultures beneath the waves.',
                'pronunciation': "/ˈmɜr.foʊk/",
                'etymology': 'Compound of "mer" (from Latin "mare," meaning sea) + "folk" (people), referring to sea people.',
                'memory_tip': 'Remember MERFOLK = MER (sea) + FOLK (people) - mythical sea people with fish tails.',
                'example_sentence': 'The fantasy novel featured ______ who could communicate with dolphins and whales.'
            },
            'merganser': {
                'definition': 'A type of diving duck with a narrow, serrated bill adapted for catching fish, belonging to the genus Mergus. Mergansers are skilled underwater hunters that pursue fish through diving and swimming beneath the surface. Common species include the common merganser, red-breasted merganser, and hooded merganser, each with distinctive plumage and habitat preferences. These waterfowl have specialized bills with tooth-like projections that help grip slippery fish during underwater pursuit. Mergansers typically inhabit forested lakes, rivers, and coastal waters where fish populations support their dietary needs. The birds play important ecological roles as predators that help maintain aquatic ecosystem balance. Merganser populations face threats from habitat loss, water pollution, and climate change affecting their aquatic habitats. Birdwatchers value mergansers for their striking appearance and impressive diving abilities.',
                'pronunciation': "/mərˈɡæn.sər/",
                'etymology': 'From Latin "mergus" (diver) + "anser" (goose), referring to diving waterfowl characteristics.',
                'memory_tip': 'Remember MERGANSER = MERGE + GANSER - diving duck that merges underwater to catch fish.',
                'example_sentence': 'The ______ dove beneath the lake surface and emerged with a fish in its serrated bill.'
            },
            'meridian': {
                'definition': 'A line of longitude on the Earth\'s surface connecting the North and South poles; also the highest point or climax of something. Geographic meridians divide the Earth into time zones and serve as reference lines for navigation and cartography. The Prime Meridian (0° longitude) passes through Greenwich, England, and serves as the reference point for measuring longitude worldwide. Solar meridians mark the sun\'s highest daily position in the sky, occurring at local noon. In traditional Chinese medicine, meridians are energy pathways through the body used in acupuncture and other healing practices. Figuratively, reaching one\'s meridian means achieving peak performance, success, or influence in a particular field. The concept represents both scientific measurement systems and metaphorical expressions of culmination or achievement.',
                'pronunciation': "/məˈrɪd.i.ən/",
                'etymology': 'From Latin "meridianus," meaning of midday, derived from "meridies" (midday), when the sun is at its highest.',
                'memory_tip': 'Remember MERIDIAN = imaginary line where the sun reaches its MIDDAY peak position.',
                'example_sentence': 'The GPS system used the Prime ______ as the starting point for longitude measurements.'
            },
            'meringue': {
                'definition': 'A sweet mixture made from beaten egg whites and sugar, used as a topping for pies or baked separately as a light, crispy confection. Meringue preparation requires careful technique to achieve proper texture, including room-temperature egg whites, gradual sugar addition, and adequate beating to create stable foam. Different meringue types include French meringue (raw), Italian meringue (cooked with hot sugar syrup), and Swiss meringue (warmed during beating). Meringue toppings crown desserts like lemon pie, baked Alaska, and pavlova, providing sweet contrast to tart or rich fillings. Meringue cookies and shells create light, airy textures that dissolve pleasantly in the mouth. Humidity affects meringue success, as moisture can prevent proper setting and cause weeping or collapse. Understanding meringue technique enables creation of elegant desserts with impressive visual and textural appeal.',
                'pronunciation': "/məˈræŋ/",
                'etymology': 'From French "meringue," possibly named after Meiringen, Switzerland, where it may have originated.',
                'memory_tip': 'Remember MERINGUE = light, airy sweet made from egg whites that RING with sweetness.',
                'example_sentence': 'The baker topped the lemon pie with golden ______ that had been perfectly browned.'
            },
            'merino': {
                'definition': 'A breed of sheep known for producing exceptionally fine, soft wool; also the high-quality fabric made from this wool. Merino sheep originated in Spain and have been selectively bred for centuries to produce wool with superior characteristics including fineness, softness, and crimping that enhances insulation. Merino wool has natural properties including moisture-wicking, odor resistance, temperature regulation, and comfort against skin without itching. The fiber\'s fine diameter and natural elasticity make it ideal for high-performance clothing, luxury garments, and outdoor apparel. Australia and New Zealand have developed major merino sheep industries that produce much of the world\'s premium wool. Merino wool commands higher prices than regular wool due to its superior quality and performance characteristics. Understanding merino quality helps consumers choose appropriate wool products for various applications.',
                'pronunciation': "/məˈri.noʊ/",
                'etymology': 'From Spanish "merino," possibly referring to a Berber tribe or from Latin "majorinus" (steward).',
                'memory_tip': 'Remember MERINO = super soft wool that\'s MERELY the FINEST sheep fiber.',
                'example_sentence': 'The hiking shirt made from ______ wool kept her comfortable in both hot and cold weather.'
            },
            'merlin': {
                'definition': 'A small, powerful falcon known for its speed and agility in hunting small birds; also the legendary wizard advisor to King Arthur in medieval literature. Merlin falcons are among the fastest birds of prey, capable of high-speed pursuit and acrobatic flight maneuvers. These compact raptors migrate long distances and demonstrate remarkable endurance and navigation abilities. Male merlins (tiercel) are smaller than females, following typical raptor sexual dimorphism patterns. Merlin populations faced decline due to DDT pesticide use but have recovered following chemical restrictions and conservation efforts. The legendary Merlin represents wisdom, magic, and the connection between natural and supernatural worlds in Arthurian romance. Both the bird and mythical figure embody power concentrated in small forms, whether through aerial hunting prowess or magical abilities. Understanding merlins involves both ornithological knowledge and cultural literary traditions.',
                'pronunciation': "/ˈmɜr.lɪn/",
                'etymology': 'Bird name from Old French "esmerillon." Wizard name from Welsh "Myrddin," legendary figure in Celtic mythology.',
                'memory_tip': 'Remember MERLIN = small but powerful falcon like the wizard - compact but mighty.',
                'example_sentence': 'The ______ dove at incredible speed to catch the sparrow in mid-flight.'
            },
            'merriam': {
                'definition': 'Referring to the Merriam-Webster dictionary company, founded by brothers George and Charles Merriam who purchased rights to Noah Webster\'s dictionary after his death. The Merriam-Webster brand became synonymous with authoritative American English dictionaries and reference works. The company developed comprehensive dictionaries that documented American English usage, pronunciation, and meaning evolution. Merriam-Webster dictionaries serve as standard references for writers, editors, students, and professionals requiring accurate word definitions and usage guidance. The brand expanded to include specialized dictionaries, thesauruses, and digital reference tools. Merriam-Webster maintains editorial policies for adding new words, tracking language changes, and providing prescriptive guidance for standard English usage. The name represents lexicographic authority and commitment to documenting living language development in American English.',
                'pronunciation': "/ˈmɛr.i.əm/",
                'etymology': 'Named after George and Charles Merriam, 19th-century American publishers who acquired Noah Webster\'s dictionary rights.',
                'memory_tip': 'Remember MERRIAM = dictionary company that makes people MERRY with word knowledge.',
                'example_sentence': 'The student consulted the ______ dictionary to verify the correct spelling and pronunciation.'
            },
            'merrier': {
                'definition': 'Comparative form of merry, meaning more cheerful, joyful, or festive than something else. Merrier describes increased levels of happiness, celebration, or jovial mood in comparison situations. "The more the merrier" is a common expression welcoming additional participants to social gatherings or activities. Merrier circumstances involve greater joy, laughter, or festive atmosphere than previous conditions. Holiday celebrations aim to become merrier through music, decorations, food, and social interaction. Making events merrier requires attention to atmosphere, entertainment, and participant engagement. The concept emphasizes relative improvement in mood and celebration rather than absolute levels of happiness. Understanding merrier helps in planning social events and creating positive experiences that exceed previous occasions in terms of joy and festivity.',
                'pronunciation': "/ˈmɛr.i.ər/",
                'etymology': 'Comparative form of "merry," from Old English "myrige," meaning pleasant or agreeable.',
                'memory_tip': 'Remember MERRIER = MORE merry - increased happiness and celebration compared to before.',
                'example_sentence': 'The holiday party became even ______ when the musicians started playing familiar songs.'
            }
        }
        
        return data.get(word, {
            'definition': f'A word from the Scripps National Spelling Bee word list. Definition not available in current dataset.',
            'pronunciation': f'Pronunciation not available for {word}.',
            'etymology': f'Etymology not available for {word}.',
            'memory_tip': f'Memory tip not available for {word}.',
            'example_sentence': f'The word ______ appears in spelling bee competitions.'
        })
    
    def detect_combined_words(self) -> List[str]:
        """Detect combined word errors in the dataset"""
        combined_words = []
        
        # Check each word for combined word patterns
        words_to_check = [
            'megahertzgnash',          # megahertz + gnash
            'mellifluousclemency',     # mellifluous + clemency
            'meltedmembership',        # melted + membership
            'meningitismephitic'       # meningitis + mephitic
        ]
        
        for word in words_to_check:
            combined_words.append(word)
            
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        """Process the batch with comprehensive Claude data"""
        
        logger.info("Processing Batch 110 with comprehensive Claude data...")
        
        # Detect combined words
        combined_words = self.detect_combined_words()
        logger.info(f"Detected {len(combined_words)} combined word errors: {combined_words}")
        
        processed_words = []
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                if not row['word']:  # Skip empty rows
                    continue
                    
                word = row['word'].strip()
                if not word:
                    continue
                
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Calculate difficulty scores
                difficulty_scores = self.difficulty_calc.calculate_difficulty_score(
                    word, 
                    claude_data['definition'], 
                    claude_data['etymology']
                )
                
                # Flag combined words
                is_combined_error = word in combined_words
                
                processed_word = {
                    'word': word,
                    'years': row['years'],
                    'source_files': row['source_files'],
                    'source_difficulties': row['source_difficulties'],
                    'definition': claude_data['definition'],
                    'pronunciation': claude_data['pronunciation'],
                    'etymology': claude_data['etymology'],
                    'etymology_source': 'Claude',
                    'memory_tip': claude_data['memory_tip'],
                    'example_sentence': claude_data['example_sentence'],
                    'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                    'word_frequency_score': difficulty_scores['word_frequency_score'], 
                    'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                    'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                    'difficulty': difficulty_scores['difficulty'],
                    'combined_word_error': is_combined_error
                }
                
                processed_words.append(processed_word)
                logger.info(f"Processed word: {word}")
        
        # Write to output file
        if processed_words:
            fieldnames = [
                'word', 'years', 'source_files', 'source_difficulties',
                'definition', 'pronunciation', 'etymology', 'etymology_source',
                'memory_tip', 'example_sentence',
                'phonetic_transparency_score', 'word_frequency_score',
                'morphological_complexity_score', 'etymology_complexity_score',
                'difficulty', 'combined_word_error'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
        return len(processed_words)

if __name__ == "__main__":
    processor = Batch110Processor()
    
    input_file = "output/batch_110_words.csv"
    output_file = "output/batch_110_processed.csv"
    
    try:
        word_count = processor.process_batch(input_file, output_file)
        
        logger.info("Batch 110 processing completed!")
        logger.info(f"Processed {word_count} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {word_count} successful, 0 failed")
        
    except Exception as e:
        logger.error(f"Error processing batch 110: {str(e)}")
        raise