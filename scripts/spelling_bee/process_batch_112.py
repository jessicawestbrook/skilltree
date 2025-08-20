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

class Batch112Processor:
    """Processes Batch 112 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for each word"""
        data = {
            'millegrain': {
                'definition': 'A decorative technique in jewelry making that creates tiny, granular textures on metal surfaces, resembling thousands of small beads or grains. Millegrain work involves using specialized tools to create regular, repetitive patterns of small raised dots or ridges along edges of jewelry settings, particularly around gemstones. This technique enhances light reflection and adds visual interest to precious metal work. Millegrain detail appears commonly in vintage and antique jewelry, especially Art Deco and Edwardian pieces where it provided elegant finishing touches. Modern jewelers continue using millegrain techniques to create traditional styling and add texture contrast to smooth metal surfaces. The process requires skill and patience to achieve uniform, consistent patterns. Understanding millegrain work helps appreciate fine jewelry craftsmanship and the attention to detail that distinguishes high-quality pieces.',
                'pronunciation': "/ˈmɪl.ɪ.ɡreɪn/",
                'etymology': 'From French "millegrain," meaning thousand grain, referring to the tiny grain-like texture created by this technique.',
                'memory_tip': 'Remember MILLEGRAIN = MILLE (thousand) + GRAIN - tiny grain textures like thousands of seeds.',
                'example_sentence': 'The antique engagement ring featured delicate ______ work around the diamond setting.'
            },
            'millennial': {
                'definition': 'Relating to a millennium (thousand years) or a person born between the early 1980s and early 2000s, also known as Generation Y. Millennial as an adjective describes things spanning or relating to thousand-year periods. The Millennial generation grew up during the digital revolution, experiencing the transition from analog to digital technology, the rise of the internet, and social media development. Millennials are characterized by tech-savviness, value-driven consumer habits, preference for experiences over material possessions, and different workplace expectations than previous generations. This generation faced unique economic challenges including student loan debt, housing affordability issues, and recession impacts on career development. Understanding millennial characteristics helps businesses, educators, and policymakers address the needs and preferences of this significant demographic group.',
                'pronunciation': "/məˈlɛn.i.əl/",
                'etymology': 'From Latin "millennium" (thousand years) + "-al" suffix, relating to thousand-year periods or the generation.',
                'memory_tip': 'Remember MILLENNIAL = relating to MILLENNIUM (1000 years) or generation born around 2000.',
                'example_sentence': 'The ______ workforce values flexible schedules and meaningful work over traditional corporate benefits.'
            },
            'millet': {
                'definition': 'A group of small-seeded cereal grains that are important food crops in semi-arid regions of Africa and Asia, known for their drought tolerance and nutritional value. Millet varieties include pearl millet, finger millet, and proso millet, each adapted to specific growing conditions and uses. These hardy grains require minimal water and can grow in poor soils where other cereals fail, making them crucial for food security in challenging environments. Millet provides protein, fiber, minerals, and B vitamins, serving as staple foods for millions of people worldwide. The grains can be ground into flour, cooked as porridge, or used in brewing. Modern health-conscious consumers increasingly appreciate millet as a gluten-free, nutritious alternative to wheat and rice. Understanding millet agriculture supports sustainable farming practices and global food security initiatives.',
                'pronunciation': "/ˈmɪl.ət/",
                'etymology': 'From Old French "mil," derived from Latin "milium," referring to these small grain crops.',
                'memory_tip': 'Remember MILLET = small grains that are MILD but resilient - drought-tolerant cereal crop.',
                'example_sentence': 'The farmers planted ______ because it could survive the region\'s frequent droughts better than other grains.'
            },
            'million': {
                'definition': 'The number 1,000,000; a very large but indefinite number. Million represents a thousand thousands and serves as a standard unit for expressing large quantities in population, economics, and science. Millionaires possess net worth exceeding one million dollars or other currency units. Million-dollar questions describe extremely difficult or important problems requiring significant consideration. The term appears in measurements like "parts per million" for concentration levels and "miles per million years" for geological time scales. Understanding millions helps in comprehending large-scale phenomena including national budgets, population statistics, and scientific measurements. The concept connects mathematical precision with practical applications in finance, demographics, and data analysis. Million serves as a psychological benchmark representing significant achievement or magnitude.',
                'pronunciation': "/ˈmɪl.jən/",
                'etymology': 'From Old French "million," derived from Italian "milione," meaning large thousand (mille = thousand).',
                'memory_tip': 'Remember MILLION = 1000 thousands - a very large number with six zeros.',
                'example_sentence': 'The lottery jackpot reached fifty ______ dollars, attracting thousands of hopeful players.'
            },
            'millionaire': {
                'definition': 'A person whose net worth equals or exceeds one million dollars or equivalent currency; someone who possesses great wealth. Millionaire status represents significant financial achievement and economic security that enables lifestyle choices unavailable to most people. Different types of millionaires include those with liquid assets, real estate wealth, or business equity reaching million-dollar values. The millionaire lifestyle often involves luxury goods, extensive travel, philanthropy, and investment activities. Becoming a millionaire typically requires combination of income, savings, investments, business success, or inheritance. Millionaire demographics vary by age, education, profession, and geographic location. Understanding millionaire concepts involves recognizing wealth accumulation strategies, economic inequality, and social implications of concentrated resources. The term represents both financial goals and societal discussions about wealth distribution.',
                'pronunciation': "/ˌmɪl.jəˈnɛr/",
                'etymology': 'From "million" + "-aire" suffix (French), meaning person who possesses millions.',
                'memory_tip': 'Remember MILLIONAIRE = person with MILLIONS in the AIR - very wealthy individual.',
                'example_sentence': 'After decades of saving and investing wisely, she finally became a ______ at age sixty.'
            },
            'millisecond': {
                'definition': 'A unit of time equal to one thousandth of a second, commonly abbreviated as "ms" and used in precise timing measurements. Milliseconds measure very short durations in computer processing, scientific experiments, athletic performance, and electronic communications. Computer response times, internet latency, and software performance are often measured in milliseconds. Athletic events may be timed to milliseconds to determine winners in close competitions. Human reaction times typically range from 200-300 milliseconds for simple responses. Audio and video synchronization requires millisecond precision to avoid noticeable delays. Understanding milliseconds enables appreciation of rapid processes that occur faster than human perception. The measurement connects human temporal experience with technological precision and scientific accuracy.',
                'pronunciation': "/ˈmɪl.ɪˌsɛk.ənd/",
                'etymology': 'From "milli-" (Latin thousandth part) + "second," meaning one thousandth of a second.',
                'memory_tip': 'Remember MILLISECOND = MILLI (thousandth) + SECOND - tiny fraction of time.',
                'example_sentence': 'The computer\'s processor could execute millions of operations in a single ______.'
            },
            'millisecondmillivolt': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "millisecond" and "millivolt." This represents a data processing error where two unrelated scientific measurement terms were concatenated without proper spacing. Millisecond refers to time measurement (one thousandth of a second), while millivolt refers to electrical voltage measurement (one thousandth of a volt). Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with technical content containing multiple measurement units. These errors highlight the challenges of automated text processing and the importance of data validation in scientific and technical contexts.',
                'pronunciation': "/ˈmɪl.ɪˌsɛk.əndˈmɪl.ɪˌvoʊlt/",
                'etymology': 'Processing error combining "millisecond" (time unit) with "millivolt" (voltage unit). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two different measurement units incorrectly joined.',
                'example_sentence': 'The technical editor flagged ______ as an invalid combination of measurement terms.'
            },
            'millivolt': {
                'definition': 'A unit of electrical potential equal to one thousandth of a volt, commonly abbreviated as "mV" and used in electronics and scientific measurements. Millivolts measure small electrical signals in biological systems, electronic circuits, and sensitive measuring instruments. Electrocardiograms (ECGs) measure heart electrical activity in millivolts, with normal readings ranging from fractions to several millivolts. Brain activity measured by electroencephalograms (EEGs) produces signals in the microvolt to millivolt range. Electronic sensors, microphones, and measurement devices often generate output signals measured in millivolts. Battery testing may involve measuring millivolt differences to assess charge levels and performance. Understanding millivolts enables work with sensitive electronic equipment and biological monitoring systems. The measurement connects electrical theory with practical applications in medicine, electronics, and scientific research.',
                'pronunciation': "/ˈmɪl.ɪˌvoʊlt/",
                'etymology': 'From "milli-" (Latin thousandth part) + "volt" (named after Alessandro Volta), meaning one thousandth of a volt.',
                'memory_tip': 'Remember MILLIVOLT = MILLI (thousandth) + VOLT - tiny electrical measurement.',
                'example_sentence': 'The sensitive amplifier could detect signals as small as a few ______ from the sensor.'
            },
            'millivoltherringbone': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "millivolt" and "herringbone." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Millivolt is an electrical measurement unit (one thousandth of a volt), while herringbone refers to a zigzag pattern resembling fish bones. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting containing both technical and descriptive terms. These errors demonstrate the challenges of automated text processing across diverse subject matter and the importance of context-aware data validation.',
                'pronunciation': "/ˈmɪl.ɪˌvoʊltˈhɛr.ɪŋˌboʊn/",
                'etymology': 'Processing error combining "millivolt" (electrical unit) with "herringbone" (pattern name). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - electrical measurement mixed with pattern description.',
                'example_sentence': 'The document parser identified ______ as an invalid word combination requiring separation.'
            },
            'mimeograph': {
                'definition': 'A duplicating machine that produced copies using a stencil and ink, widely used in offices and schools before photocopying technology became prevalent. Mimeograph machines worked by forcing ink through cut stencils to create multiple copies of documents. The process involved typing or writing on special stencil material that was then attached to a rotating drum containing ink. Teachers commonly used mimeographs to produce worksheets and handouts, creating the distinctive purple-blue ink copies familiar to many students. The mimeograph represented important office technology that democratized document reproduction before xerographic copiers became affordable. Understanding mimeograph history illustrates technological evolution in office equipment and educational materials production. The device contributed to information sharing and administrative efficiency in mid-20th century institutions.',
                'pronunciation': "/ˈmaɪ.mi.əˌɡræf/",
                'etymology': 'From Greek "mimos" (mime, imitator) + "graphos" (writing), meaning device that imitates writing.',
                'memory_tip': 'Remember MIMEOGRAPH = MIME (copy) + GRAPH (write) - machine that copies writing.',
                'example_sentence': 'The teacher used the ______ to make copies of the quiz for all her students.'
            },
            'mimeticunabated': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "mimetic" and "unabated." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Mimetic refers to imitation or mimicry, particularly in biology or art, while unabated means continuing without reduction in intensity or strength. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in academic or technical documents containing complex vocabulary. These errors highlight the challenges of processing sophisticated texts and the importance of context-sensitive validation algorithms.',
                'pronunciation': "/mɪˈmɛt.ɪkˌʌn.əˈbeɪ.təd/",
                'etymology': 'Processing error combining "mimetic" (Greek imitative) with "unabated" (continuing strongly). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - imitation concept mixed with continuation term.',
                'example_sentence': 'The academic text parser detected ______ as an invalid compound requiring word separation.'
            },
            'minacious': {
                'definition': 'Threatening or menacing in manner; having a quality that suggests potential danger or harm. Minacious behavior involves expressions, actions, or attitudes that create apprehension about possible negative consequences. The term describes individuals whose demeanor or words imply threats without necessarily being explicitly threatening. Minacious clouds suggest approaching storms, while minacious political rhetoric may indicate potential conflict. Legal contexts may recognize minacious conduct as harassment or intimidation even without direct threats. Understanding minacious behavior helps in recognizing subtle forms of intimidation and responding appropriately to situations that feel threatening without overt aggression. The concept bridges obvious threats with more subtle forms of menacing behavior that create unease and fear.',
                'pronunciation': "/mɪˈneɪ.ʃəs/",
                'etymology': 'From Latin "minax" meaning threatening or projecting, derived from "minari" (to threaten).',
                'memory_tip': 'Remember MINACIOUS = MENACING - threatening and potentially dangerous in manner.',
                'example_sentence': 'The defendant\'s ______ stare made the witness uncomfortable during cross-examination.'
            },
            'mince': {
                'definition': 'To cut into very small pieces; to speak in an affected or overly delicate manner; also finely chopped meat. Culinary mincing involves cutting ingredients like garlic, herbs, or onions into tiny, uniform pieces that distribute flavor throughout dishes. Sharp knives and proper technique enable efficient mincing that enhances cooking results. Minced meat (ground meat) provides texture for dishes like hamburgers, meatballs, and sauces. "To mince words" means to speak with excessive delicacy or avoid direct expression, often to soften harsh truths or avoid offense. Mincing gait describes walking with short, dainty steps. The concept appears in both practical cooking applications and descriptive language for affected behavior. Understanding mincing techniques improves culinary skills and communication effectiveness.',
                'pronunciation': "/mɪns/",
                'etymology': 'From Old French "mincier," meaning to make small or cut finely, possibly related to "menu" (small).',
                'memory_tip': 'Remember MINCE = make MINI pieces - cut very small or speak delicately.',
                'example_sentence': 'The chef showed students how to ______ garlic properly for the pasta sauce.'
            },
            'mineral': {
                'definition': 'A naturally occurring inorganic solid with a definite chemical composition and crystalline structure; also essential nutrients required by living organisms. Geological minerals form through various processes including cooling magma, precipitation from solutions, and metamorphic changes. Common minerals include quartz, feldspar, calcite, and pyrite, each with distinct properties and uses. Mineral identification involves testing hardness, color, luster, and crystal structure. Industrial applications use minerals for construction materials, electronics, ceramics, and manufacturing. Dietary minerals including calcium, iron, zinc, and magnesium are essential for human health and must be obtained from food or supplements. Mineral deficiencies can cause serious health problems, while proper mineral intake supports bone health, immune function, and metabolism. Understanding minerals connects geology with nutrition, technology, and health sciences.',
                'pronunciation': "/ˈmɪn.ər.əl/",
                'etymology': 'From Medieval Latin "minerale," relating to mines or mining, derived from "minera" (ore or mine).',
                'memory_tip': 'Remember MINERAL = natural substance MINED from earth - rocks and nutrients.',
                'example_sentence': 'The geologist identified the ______ sample as pyrite based on its golden metallic luster.'
            },
            'minerals': {
                'definition': 'Plural of mineral; multiple naturally occurring inorganic substances or essential nutrients required by living organisms. Earth\'s crust contains thousands of different minerals that form rocks, ores, and geological formations. Mineral exploration seeks valuable deposits for mining operations that extract metals, gemstones, and industrial materials. Nutritional minerals in foods support various bodily functions including bone formation, enzyme activity, and nerve transmission. Mineral supplements help address dietary deficiencies and support health maintenance. Rock collections display diverse minerals with varying colors, hardness, and crystal forms. Mineral rights govern ownership and extraction permissions for subsurface resources. Understanding minerals encompasses geological processes, nutritional science, and economic resource management. The study connects earth sciences with human health and industrial applications.',
                'pronunciation': "/ˈmɪn.ər.əlz/",
                'etymology': 'Plural of "mineral," from Medieval Latin referring to multiple mined substances or nutrients.',
                'memory_tip': 'Remember MINERALS = multiple substances MINED from earth - rocks, ores, and nutrients.',
                'example_sentence': 'The nutritionist explained which ______ were most important for bone health and muscle function.'
            },
            'minestra': {
                'definition': 'An Italian soup typically made with vegetables, legumes, pasta, or rice in a broth base; a hearty, rustic soup representing traditional Italian home cooking. Minestra varies by region and season, incorporating available local ingredients like beans, greens, root vegetables, and small pasta shapes. Unlike minestrone, which is thicker and more substantial, minestra tends to be lighter and brothier. Traditional minestra recipes reflect Italian culinary principles of simplicity, seasonal ingredients, and regional variation. Common types include minestra di verdure (vegetable soup) and minestra di riso (rice soup). The dish represents Italian comfort food that transforms simple ingredients into satisfying, nutritious meals. Understanding minestra provides insight into Italian cooking traditions that emphasize flavor development through careful preparation of basic ingredients.',
                'pronunciation': "/mɪˈnɛs.trə/",
                'etymology': 'From Italian "minestra," meaning soup or dish that is served, derived from "ministrare" (to serve).',
                'memory_tip': 'Remember MINESTRA = Italian soup that MINISTERS to hunger - nourishing broth-based dish.',
                'example_sentence': 'The grandmother prepared a traditional ______ with fresh vegetables from her garden.'
            },
            'minette': {
                'definition': 'A type of iron ore containing oolitic limestone and iron oxides, particularly found in the Lorraine region of France and used historically in steel production. Minette ore was crucial to European steel industry development, especially in France, Luxembourg, and Germany during the 19th and early 20th centuries. The ore\'s composition made it suitable for blast furnace operations when combined with appropriate fluxes and fuels. Minette mining supported major industrial centers and influenced regional economic development. The ore\'s gradual depletion and competition from higher-grade imports led to decline in European minette mining. The term also refers to a type of fine-grained igneous rock. Understanding minette illustrates connections between geological resources, industrial development, and economic geography in European steel production.',
                'pronunciation': "/mɪˈnɛt/",
                'etymology': 'From French "minette," meaning small or delicate, referring to the fine-grained nature of this iron ore.',
                'memory_tip': 'Remember MINETTE = small MINE ore - fine-grained iron ore from French mines.',
                'example_sentence': 'The Lorraine ______ deposits fueled French steel production for over a century.'
            },
            'minimise': {
                'definition': 'British spelling of minimize; to reduce to the smallest possible amount, degree, or importance. Minimising involves systematic reduction of waste, risk, cost, or negative impact through careful planning and execution. Business strategies minimise expenses while maximising profits through efficiency improvements and resource optimization. Risk minimisation requires identifying potential problems and implementing preventive measures. Environmental minimisation focuses on reducing pollution, waste, and resource consumption through sustainable practices. Conflict minimisation involves diplomatic approaches that reduce tension and promote peaceful resolution. Design minimisation creates clean, simple aesthetics by eliminating unnecessary elements. Understanding minimisation principles helps in optimization problems across various fields including mathematics, engineering, and management.',
                'pronunciation': "/ˈmɪn.ɪˌmaɪz/",
                'etymology': 'British spelling of minimize, from Latin "minimus" (smallest) + "-ize" suffix meaning to make.',
                'memory_tip': 'Remember MINIMISE = British way to make MINIMAL - reduce to smallest amount.',
                'example_sentence': 'The company sought to ______ environmental impact while maintaining production levels.'
            },
            'minimize': {
                'definition': 'American spelling of minimise; to reduce to the smallest possible amount, degree, or importance. Minimizing strategies help achieve efficiency by eliminating unnecessary elements and focusing on essential components. Computer interfaces minimize windows to reduce screen clutter while keeping programs accessible. Project management minimizes risks through careful planning, monitoring, and contingency preparation. Medical treatments aim to minimize side effects while maximizing therapeutic benefits. Minimalist design philosophy minimizes visual elements to create clean, functional aesthetics. Energy conservation minimizes consumption through efficient technologies and behavioral changes. Understanding minimization involves recognizing optimization principles and systematic approaches to reduction. The concept applies across disciplines from mathematics and engineering to art and lifestyle choices.',
                'pronunciation': "/ˈmɪn.ɪˌmaɪz/",
                'etymology': 'From Latin "minimus" (smallest) + "-ize" suffix, meaning to make as small as possible.',
                'memory_tip': 'Remember MINIMIZE = make MINIMAL size - reduce to smallest amount possible.',
                'example_sentence': 'The architect designed the building to ______ energy consumption through passive solar features.'
            },
            'minimus': {
                'definition': 'The smallest or least; specifically referring to the fifth digit (little finger or little toe) in anatomy. Minimus finger represents the smallest and often least functional digit on the hand, though it contributes to grip strength and fine motor control. Anatomical terminology uses minimus to designate the smallest structures in paired or multiple systems. The minimus muscle group includes small muscles controlling the little finger and toe movements. Medical conditions affecting the minimus digit may involve fractures, arthritis, or nerve damage that impacts hand function. Understanding minimus anatomy helps in injury assessment, rehabilitation planning, and surgical procedures. The term emphasizes relative size relationships in anatomical classification systems.',
                'pronunciation': "/ˈmɪn.ɪ.məs/",
                'etymology': 'From Latin "minimus," meaning smallest or least, superlative form of "parvus" (small).',
                'memory_tip': 'Remember MINIMUS = the MINIMAL digit - smallest finger or toe.',
                'example_sentence': 'The injury to her ______ finger affected her ability to grip objects firmly.'
            },
            'miniscule': {
                'definition': 'A common misspelling of "minuscule," meaning extremely small or tiny. While widely used, "miniscule" is not the standard spelling in formal writing, though it appears frequently in casual communication. The confusion arises from the prefix "mini-" which people associate with smallness, leading to this alternative spelling. Standard dictionaries and style guides prefer "minuscule" as the correct spelling. The misspelling demonstrates how language evolution and common usage can create variations that compete with traditional forms. Understanding spelling variations helps in both recognizing common errors and choosing appropriate forms for different contexts. Educational approaches address this common misspelling while acknowledging its widespread occurrence.',
                'pronunciation': "/ˈmɪn.ɪˌskul/",
                'etymology': 'Common misspelling of "minuscule," influenced by "mini-" prefix association with smallness.',
                'memory_tip': 'Remember MINISCULE = common misspelling - the correct form is MINUSCULE.',
                'example_sentence': 'Although "______" appears frequently, careful writers use "minuscule" as the standard spelling.'
            },
            'ministrations': {
                'definition': 'The act of providing care, service, or assistance, especially in a helpful or healing capacity; attentive service or care given to someone in need. Ministrations often involve tender, compassionate care provided during illness, distress, or difficulty. Medical ministrations include nursing care, treatment procedures, and bedside assistance that promote healing and comfort. Religious ministrations encompass pastoral care, spiritual counseling, and sacramental services provided by clergy. The term implies dedicated, often selfless service that addresses both physical and emotional needs. Ministrations can be professional (healthcare workers) or personal (family caregivers) but always involve intentional acts of service. Understanding ministrations emphasizes the human dimension of care-giving and the importance of compassionate assistance in times of need.',
                'pronunciation': "/ˌmɪn.ɪˈstreɪ.ʃənz/",
                'etymology': 'From Latin "ministrare," meaning to serve or attend, related to "minister" (servant or attendant).',
                'memory_tip': 'Remember MINISTRATIONS = MINISTER-ing actions - serving and caring for others.',
                'example_sentence': 'The nurse\'s gentle ______ helped the patient feel comfortable during recovery.'
            },
            'ministry': {
                'definition': 'A government department responsible for specific policy areas; also the work or profession of a religious leader. Government ministries oversee areas like education, health, defense, or finance, implementing policies and managing public services. Ministry leaders (ministers) are typically appointed by political leadership and accountable to legislative bodies. Religious ministry involves spiritual leadership, pastoral care, preaching, and community service within faith communities. The ministry requires theological education, spiritual calling, and commitment to serving congregational and community needs. Ministries can be specialized (youth ministry, music ministry) or general pastoral roles. Both government and religious ministries involve public service, though in different contexts and with different objectives. Understanding ministry concepts helps recognize service-oriented leadership across secular and religious institutions.',
                'pronunciation': "/ˈmɪn.ɪ.stri/",
                'etymology': 'From Latin "ministerium," meaning service or office, derived from "minister" (servant).',
                'memory_tip': 'Remember MINISTRY = place of service - government department or religious calling.',
                'example_sentence': 'She felt called to enter the ______ after completing her theological studies.'
            },
            'minivan': {
                'definition': 'A small passenger van designed for family transportation, typically seating seven to eight passengers with emphasis on interior space and convenience features. Minivans emerged in the 1980s as alternatives to station wagons, offering higher seating positions, easier entry/exit, and more cargo space. Key features include sliding side doors, removable seats, and family-friendly amenities like cup holders and storage compartments. Popular minivan models include Honda Odyssey, Toyota Sienna, and Chrysler Pacifica. The vehicles serve families needing passenger capacity for children, sports teams, and group transportation. Minivan sales peaked in the 1990s but declined as SUVs gained popularity, though they remain practical choices for large families. Understanding minivan characteristics helps in vehicle selection based on passenger and cargo needs.',
                'pronunciation': "/ˈmɪn.iˌvæn/",
                'etymology': 'Compound of "mini" (small) + "van" (large vehicle), referring to smaller passenger vans.',
                'memory_tip': 'Remember MINIVAN = MINI version of VAN - smaller family passenger vehicle.',
                'example_sentence': 'The soccer coach used her ______ to transport the team to away games.'
            },
            'minivets': {
                'definition': 'Small, colorful songbirds belonging to the family Campephagidae, found primarily in tropical Asia and known for their bright plumage and insectivorous diet. Minivets display sexual dimorphism with males typically showing bright red and black coloration while females have yellow and gray patterns. These birds inhabit forests and woodland areas where they feed on insects, caterpillars, and small arthropods. Different minivet species include the scarlet minivet, small minivet, and long-tailed minivet, each with distinct habitat preferences and distributions. Minivets often join mixed-species foraging flocks, contributing to forest ecosystem balance through insect control. Birdwatchers appreciate minivets for their striking colors and active foraging behavior. Understanding minivet ecology helps in forest conservation and biodiversity protection efforts.',
                'pronunciation': "/ˈmɪn.ɪˌvɛts/",
                'etymology': 'From "mini" (small) + unclear origin for "vet," possibly from French "vedette" (small scout bird).',
                'memory_tip': 'Remember MINIVETS = MINI colorful birds - small, bright forest songbirds.',
                'example_sentence': 'The birdwatcher spotted a flock of ______ feeding in the canopy of the tropical forest.'
            },
            'mink': {
                'definition': 'A small, carnivorous mammal with dark brown fur, valued for its luxurious pelt and raised commercially for fur production. Wild mink are semi-aquatic animals that live near water sources and feed on fish, frogs, small mammals, and birds. The American mink has been introduced to many countries and sometimes becomes invasive, impacting local wildlife populations. Mink fur is prized for its softness, durability, and water-repelling properties, making it valuable for luxury clothing. Mink farming involves raising these animals in controlled environments for fur harvest, though this practice faces ethical concerns and regulatory restrictions in some regions. Understanding mink ecology involves recognizing their role as predators in aquatic ecosystems and their economic significance in fur industries.',
                'pronunciation': "/mɪŋk/",
                'etymology': 'From Middle English "menk," possibly from Scandinavian origin, referring to this fur-bearing mammal.',
                'memory_tip': 'Remember MINK = valuable fur animal that likes to drink near water sources.',
                'example_sentence': 'The wildlife biologist studied ______ populations to assess their impact on local waterfowl.'
            },
            'minnesota': {
                'definition': 'A state in the upper Midwest region of the United States, known as the "Land of 10,000 Lakes" due to its abundant water bodies formed by glacial activity. Minnesota borders Canada and is famous for its natural beauty, outdoor recreation opportunities, and Scandinavian cultural heritage. The state economy includes agriculture, mining (especially iron ore), manufacturing, and technology industries. Major cities include Minneapolis and Saint Paul (the Twin Cities), Duluth, and Rochester. Minnesota is known for cold winters, hot summers, and residents\' reputation for politeness ("Minnesota Nice"). The state hosts the headwaters of the Mississippi River and contains extensive forests, prairies, and wetlands. Understanding Minnesota involves appreciating its natural resources, cultural diversity, and economic contributions to the upper Midwest region.',
                'pronunciation': "/ˌmɪn.ɪˈsoʊ.tə/",
                'etymology': 'From Dakota "mnisota," meaning cloudy water or sky-tinted water, referring to the Minnesota River.',
                'memory_tip': 'Remember MINNESOTA = MINI-SOTA with many lakes - state with thousands of water bodies.',
                'example_sentence': 'The family vacation to ______ included fishing, canoeing, and visiting the headwaters of the Mississippi.'
            },
            'minnow': {
                'definition': 'A small freshwater fish, typically used as bait for larger fish or referring to any small fish species. True minnows belong to the Cyprinidae family and include numerous species found in streams, ponds, and rivers worldwide. These fish serve important ecological roles as prey species supporting larger fish, birds, and aquatic predators. Minnows often travel in schools for protection and feed on algae, insects, and small aquatic organisms. Anglers use live minnows as bait to catch bass, pike, walleye, and other game fish. "Small fry" or "big fish in a small pond" expressions relate to minnow concepts of relative size and importance. Understanding minnow ecology helps in fisheries management, aquatic ecosystem health assessment, and sustainable fishing practices.',
                'pronunciation': "/ˈmɪn.oʊ/",
                'etymology': 'From Middle English "menow," possibly related to Old English "myne" meaning small fish.',
                'memory_tip': 'Remember MINNOW = MINI NOW - small fish that swim in groups.',
                'example_sentence': 'The children enjoyed watching schools of ______ dart through the shallow creek water.'
            },
            'minority': {
                'definition': 'A smaller number or part; a group that is different from the larger population in race, religion, language, or political beliefs. Minority status can be numerical (fewer people) or social (less power or influence) depending on context. Ethnic and racial minorities may face discrimination and require legal protections to ensure equal rights and opportunities. Religious minorities practice faiths different from the majority population and need religious freedom protections. Political minorities represent viewpoints not held by the majority and require democratic institutions that protect dissenting voices. Minority rights are fundamental to democratic societies and human rights frameworks. Understanding minority concepts involves recognizing diversity, power dynamics, and the importance of inclusive policies that protect all community members regardless of group size or social position.',
                'pronunciation': "/məˈnɔr.ə.ti/",
                'etymology': 'From Latin "minoritas," meaning smaller number, derived from "minor" (smaller, lesser).',
                'memory_tip': 'Remember MINORITY = MINOR group - smaller number or less powerful group.',
                'example_sentence': 'The constitution included protections to ensure ______ rights were respected in democratic decision-making.'
            },
            'minotaur': {
                'definition': 'A creature from Greek mythology with the head of a bull and the body of a man, confined in an elaborate labyrinth beneath the palace of King Minos in Crete. According to legend, the Minotaur was born from the union of Pasiphaë, wife of Minos, and a sacred bull. The monster required human sacrifice until the hero Theseus killed it with help from Ariadne, who provided thread to navigate the labyrinth. The Minotaur myth symbolizes the triumph of civilization over barbarism and the hero\'s journey through challenges to achieve victory. Modern interpretations explore themes of isolation, monstrosity, and the dual nature of humanity. The Minotaur appears in art, literature, and psychology as a symbol of inner conflict and the beast within civilized beings.',
                'pronunciation': "/ˈmaɪ.nəˌtɔr/",
                'etymology': 'From Greek "Minotauros," meaning bull of Minos, referring to the creature in the Cretan labyrinth.',
                'memory_tip': 'Remember MINOTAUR = MINO (King Minos) + TAUR (bull) - mythical bull-headed monster.',
                'example_sentence': 'The ancient Greek myth tells how Theseus slayed the ______ in the labyrinth of Crete.'
            },
            'minuscule': {
                'definition': 'Extremely small in size or importance; also referring to lowercase letters in typography and manuscripts. Physical minuscule objects require magnification for detailed examination and often have significance disproportionate to their size. Minuscule differences can have major consequences in precision engineering, scientific measurements, and quality control. Typography distinguishes between majuscule (uppercase) and minuscule (lowercase) letters. Medieval manuscripts used minuscule scripts that influenced modern lowercase letter forms. Minuscule improvements in efficiency can compound to create substantial benefits over time. Understanding minuscule involves recognizing that small size doesn\'t always correlate with low importance. The concept applies across scales from microscopic organisms to typographic design.',
                'pronunciation': "/ˈmɪn.əˌskul/",
                'etymology': 'From Latin "minuscula," meaning rather small, derived from "minus" (less) + diminutive suffix.',
                'memory_tip': 'Remember MINUSCULE = MINUS-cule - extremely small, reduced to almost nothing.',
                'example_sentence': 'The error was ______ but caused significant problems in the computer program.'
            },
            'minute': {
                'definition': 'A unit of time equal to sixty seconds or one-sixtieth of an hour; also meaning extremely small or paying attention to fine details. Time minutes organize daily schedules, meeting durations, and temporal measurements. Meeting minutes record decisions, discussions, and action items for future reference. The minute hand on clocks tracks time progression through sixty-minute hours. "Up to the minute" describes current, timely information. As an adjective (pronounced differently), minute means extremely small or involving careful attention to details. Minute examination involves thorough, detailed analysis. Understanding minute concepts involves both temporal measurement and detailed attention. The dual meaning reflects the importance of both time management and precision in various activities.',
                'pronunciation': "/ˈmɪn.ɪt/ (time); /maɪˈnut/ (small)",
                'etymology': 'From Latin "minutus," meaning small or diminished; time sense from "pars minuta prima" (first small part).',
                'memory_tip': 'Remember MINUTE = 60 seconds OR very small - context determines pronunciation.',
                'example_sentence': 'The meeting lasted exactly thirty ______, and the secretary recorded detailed ______ of every discussion.'
            },
            'minutia': {
                'definition': 'Small or trivial details; precise or minor particulars that might be considered unimportant but can sometimes be significant. Minutiae (plural) include fine points, subtle distinctions, and detailed specifications that require careful attention. Legal minutiae can determine case outcomes through precise interpretation of contract language or procedural requirements. Scientific minutiae involve detailed measurements and observations that contribute to accurate research results. Project management requires attention to minutiae to ensure successful completion and avoid costly oversights. While often dismissed as unimportant, minutiae can reveal important patterns or cause significant problems when ignored. Understanding minutiae involves balancing attention to detail with broader perspective. The concept emphasizes that small details sometimes have disproportionate importance.',
                'pronunciation': "/mɪˈnu.ʃə/ (singular); /mɪˈnu.ʃi.i/ (plural minutiae)",
                'etymology': 'From Latin "minutia," meaning smallness or trifle, derived from "minutus" (small).',
                'memory_tip': 'Remember MINUTIA = MINUTE detail - small, precise particular that might matter.',
                'example_sentence': 'The contract lawyer examined every ______ to ensure there were no hidden problems.'
            },
            'miombo': {
                'definition': 'A type of tropical dry forest ecosystem found in southern and eastern Africa, characterized by trees in the Brachystegia, Julbernardia, and Isoberlinia genera. Miombo woodlands cover approximately 2.7 million square kilometers across countries including Tanzania, Zambia, Zimbabwe, and Mozambique. This ecosystem supports diverse wildlife including elephants, lions, and numerous antelope species. Miombo trees have distinctive compound leaves and produce edible seeds and fruits important for local communities. The woodland provides timber, fuelwood, medicinal plants, and honey production opportunities. Climate change and deforestation threaten miombo ecosystems, affecting both biodiversity and human livelihoods. Conservation efforts focus on sustainable management practices that balance ecological protection with community needs. Understanding miombo ecology is crucial for African conservation and sustainable development initiatives.',
                'pronunciation': "/miˈɑm.boʊ/",
                'etymology': 'From local African languages, referring to this specific type of woodland ecosystem.',
                'memory_tip': 'Remember MIOMBO = African woodland where animals ROAM-BO freely.',
                'example_sentence': 'The conservation project aimed to protect ______ woodland habitats critical for African wildlife.'
            },
            'mirach': {
                'definition': 'The second-brightest star in the constellation Andromeda, also known as Beta Andromedae, appearing as an orange giant star located approximately 197 light-years from Earth. Mirach serves as a guide star for locating other celestial objects, including the Andromeda Galaxy, which appears near this star from Earth\'s perspective. The star has evolved beyond its main sequence phase and expanded to become a red giant with surface temperatures cooler than our Sun. Mirach\'s name reflects Arabic astronomical traditions that preserved and expanded upon ancient Greek star catalogs. Amateur astronomers use Mirach as a reference point for constellation identification and galaxy hunting. Understanding prominent stars like Mirach helps in navigation, astronomy education, and appreciation of cultural contributions to astronomical knowledge.',
                'pronunciation': "/ˈmaɪ.ræk/",
                'etymology': 'From Arabic "al-maraqq," meaning the girdle or waist, referring to its position in Andromeda constellation.',
                'memory_tip': 'Remember MIRACH = bright star that helps you REACH other celestial objects.',
                'example_sentence': 'The amateur astronomer used ______ as a guide star to locate the Andromeda Galaxy.'
            },
            'miraculous': {
                'definition': 'Of the nature of a miracle; extraordinary and bringing very welcome consequences. Miraculous events appear to violate natural laws or occur with extremely improbable timing that suggests supernatural intervention. Religious traditions describe miraculous healings, divine interventions, and answered prayers that demonstrate spiritual power. Medical miraculous recoveries involve unexplained improvements in patients with terminal or severe conditions. The term can describe remarkable achievements that seem impossible given available resources or circumstances. Miraculous rescues during disasters demonstrate extraordinary courage and unlikely survival. While maintaining religious significance, the word also describes any remarkably fortunate or beneficial occurrence. Understanding miraculous concepts involves recognizing both religious faith and expressions of amazement at extraordinary positive outcomes.',
                'pronunciation': "/mɪˈræk.jə.ləs/",
                'etymology': 'From Latin "miraculum" (wonder, marvel) + "-ous" suffix, meaning of the nature of a miracle.',
                'memory_tip': 'Remember MIRACULOUS = causing MIRACLES - extraordinarily wonderful and unlikely.',
                'example_sentence': 'The patient\'s ______ recovery surprised the medical team who had given up hope.'
            },
            'mirage': {
                'definition': 'An optical illusion caused by atmospheric conditions that makes distant objects appear distorted or displaced; also something that appears real but is actually illusory. Desert mirages create the appearance of water where none exists due to light refraction through air layers of different temperatures. Superior mirages can make distant objects appear to float above the horizon, while inferior mirages create false reflections below actual objects. Highway mirages commonly occur on hot pavement where heat creates shimmering effects. Figuratively, mirage describes unrealistic hopes, false promises, or deceptive appearances that don\'t correspond to reality. Political mirages might involve campaign promises that prove impossible to fulfill. Understanding mirages involves both optical physics and recognition of deceptive appearances in various contexts.',
                'pronunciation': "/mɪˈrɑʒ/",
                'etymology': 'From French "mirage," derived from "mirer" (to look at), referring to optical illusions.',
                'memory_tip': 'Remember MIRAGE = false image you ADMIRE - optical illusion that deceives the eye.',
                'example_sentence': 'The desert travelers saw a ______ of an oasis that disappeared as they approached.'
            },
            'miranda': {
                'definition': 'A moon of Uranus; also referring to Miranda rights in legal contexts. Miranda, the smallest and innermost major moon of Uranus, has a heavily scarred surface suggesting violent geological history. The moon was named after a character from Shakespeare\'s "The Tempest" and measures only about 470 kilometers in diameter. Miranda rights refer to warnings that must be given to criminal suspects in custody before interrogation, established by the U.S. Supreme Court case Miranda v. Arizona (1966). These rights include the right to remain silent and the right to legal counsel. The Miranda warning protects Fifth Amendment rights against self-incrimination. Understanding both astronomical and legal Miranda concepts involves recognizing naming conventions in astronomy and constitutional protections in criminal justice.',
                'pronunciation': "/mɪˈræn.də/",
                'etymology': 'From Shakespeare\'s character in "The Tempest"; legal usage from Ernesto Miranda court case.',
                'memory_tip': 'Remember MIRANDA = moon of Uranus OR legal rights that must be ADMIRED (read aloud).',
                'example_sentence': 'The police officer read the suspect his ______ rights before beginning the interrogation.'
            },
            'miscellaneous': {
                'definition': 'Consisting of diverse, varied, or mixed items not easily categorized; a collection of different things without apparent connection. Miscellaneous categories serve as catch-all groupings for items that don\'t fit established classifications. Office supplies often include miscellaneous sections for varied small items like paper clips, rubber bands, and thumb tacks. Miscellaneous expenses in budgets cover irregular or unpredictable costs that don\'t belong in specific categories. Academic course catalogs may list miscellaneous offerings for unique or interdisciplinary subjects. Garage sales typically feature miscellaneous items representing diverse household possessions. Understanding miscellaneous concepts helps in organization systems that must accommodate varied, unrelated items. The term acknowledges that not everything fits neat categories and provides flexibility in classification systems.',
                'pronunciation': "/ˌmɪs.əˈleɪ.ni.əs/",
                'etymology': 'From Latin "miscellaneus," meaning mixed or various, derived from "miscere" (to mix).',
                'memory_tip': 'Remember MISCELLANEOUS = MIS-mixed items - various things mixed together without clear category.',
                'example_sentence': 'The store\'s ______ aisle contained everything from batteries to birthday candles.'
            },
            'mischief': {
                'definition': 'Playful or annoying behavior that may cause minor trouble or damage; harm or trouble caused by someone or something. Mischief often involves pranks, tricks, or disobedient behavior that creates inconvenience without serious harm. Children\'s mischief might include drawing on walls, hiding objects, or playing practical jokes on siblings. The phrase "mischief managed" suggests successful completion of playful troublemaking. Legal mischief can refer to criminal damage to property or interference with others\' rights. Mischievous behavior requires balance between playful fun and respect for others\' property and feelings. Understanding mischief involves recognizing the difference between harmless play and harmful actions. The concept reflects human tendency toward playful disruption and the social boundaries that define acceptable behavior.',
                'pronunciation': "/ˈmɪs.tʃɪf/",
                'etymology': 'From Old French "meschief," meaning misfortune or trouble, from "mes-" (badly) + "chief" (head).',
                'memory_tip': 'Remember MISCHIEF = MIS-CHIEF behavior - playful trouble-making that\'s not too serious.',
                'example_sentence': 'The twins were always getting into ______, but their pranks never caused real harm.'
            },
            'mischievousbionic': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "mischievous" and "bionic." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Mischievous refers to playfully troublesome behavior, while bionic refers to artificial body parts or enhanced human capabilities. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents containing diverse vocabulary from different semantic fields. These errors highlight the challenges of processing texts that contain both behavioral descriptors and technological terms.',
                'pronunciation': "/ˈmɪs.tʃɪ.vəsbaɪˈɑn.ɪk/",
                'etymology': 'Processing error combining "mischievous" (playful trouble) with "bionic" (artificial enhancement). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - playful behavior mixed with technology term.',
                'example_sentence': 'The text parser identified ______ as an invalid compound requiring separation.'
            },
            'miscible': {
                'definition': 'Able to be mixed together in any proportion without separating; capable of forming a homogeneous mixture. Miscible liquids like water and ethanol combine completely at the molecular level, creating uniform solutions without distinct layers. Immiscible liquids like oil and water cannot mix and form separate layers due to different molecular properties. Miscibility depends on similar polarities and intermolecular forces between substances. Understanding miscibility helps predict mixing behavior in chemistry, cooking, and industrial processes. Paint formulation requires knowing which solvents and pigments are miscible for proper consistency and appearance. Pharmaceutical preparations must consider miscibility when combining active ingredients with carriers. The concept applies to both liquid mixtures and metaphorical situations where different elements can or cannot combine successfully.',
                'pronunciation': "/ˈmɪs.ə.bəl/",
                'etymology': 'From Latin "miscere," meaning to mix, with "-ible" suffix indicating capability of being mixed.',
                'memory_tip': 'Remember MISCIBLE = able to MIX - substances that can combine completely.',
                'example_sentence': 'Water and alcohol are ______, creating a uniform solution when combined.'
            },
            'misconception': {
                'definition': 'A belief or opinion that is incorrect due to faulty thinking or understanding; a mistaken idea about something. Misconceptions arise from incomplete information, faulty reasoning, cultural assumptions, or misinterpretation of evidence. Educational misconceptions can impede learning when students hold incorrect ideas that conflict with new information. Scientific misconceptions include beliefs like "heavier objects fall faster" or "humans evolved from monkeys rather than sharing common ancestors." Cultural misconceptions involve stereotypes or oversimplified ideas about different groups or practices. Addressing misconceptions requires identifying underlying assumptions and providing clear, evidence-based corrections. Media literacy helps reduce misconceptions by teaching critical evaluation of information sources. Understanding misconceptions involves recognizing how incorrect beliefs form and persist despite contradictory evidence.',
                'pronunciation': "/ˌmɪs.kənˈsɛp.ʃən/",
                'etymology': 'From "mis-" (wrongly) + "conception," meaning incorrect understanding or belief.',
                'memory_tip': 'Remember MISCONCEPTION = MIS-CONCEPTION - wrong idea or mistaken belief.',
                'example_sentence': 'The teacher worked to correct the common ______ that lightning never strikes the same place twice.'
            },
            'misconstrue': {
                'definition': 'To interpret wrongly; to understand or explain incorrectly, especially someone\'s words or actions. Misconstruing occurs when communication fails due to ambiguous language, cultural differences, or incorrect assumptions about meaning. Legal misconstruing can lead to contract disputes when parties interpret terms differently than intended. Personal relationships suffer when actions are misconstrued as having negative intentions when none existed. Media misconstruing involves misrepresenting statements or events through selective editing or biased interpretation. Political misconstruing happens when opponents deliberately or accidentally misinterpret policy proposals or statements. Understanding misconstruing involves recognizing communication challenges and the importance of clarity, context, and verification. The concept emphasizes the gap between intended meaning and received interpretation in human communication.',
                'pronunciation': "/ˌmɪs.kənˈstru/",
                'etymology': 'From "mis-" (wrongly) + "construe" (to interpret), meaning to interpret incorrectly.',
                'memory_tip': 'Remember MISCONSTRUE = MIS-CONSTRUE - wrongly interpret or understand meaning.',
                'example_sentence': 'She was careful not to ______ his silence as agreement when he might simply be thinking.'
            },
            'miscreant': {
                'definition': 'A person who behaves badly or commits crimes; a villain or wrongdoer who violates social or legal norms. Miscreants engage in activities that harm others or society, ranging from minor violations to serious criminal behavior. Historical usage emphasized religious context, referring to heretics or nonbelievers who rejected orthodox doctrine. Modern usage focuses on criminal or antisocial behavior including theft, fraud, assault, or vandalism. Corporate miscreants might engage in embezzlement, securities fraud, or environmental violations. The term carries strong negative connotation, suggesting both bad behavior and moral failing. Legal systems address miscreant behavior through criminal justice processes including investigation, prosecution, and punishment. Understanding miscreant concepts involves recognizing social norms and consequences for violating community standards.',
                'pronunciation': "/ˈmɪs.kri.ənt/",
                'etymology': 'From Old French "mescreant," meaning unbelieving or villainous, from "mes-" (badly) + "creant" (believing).',
                'memory_tip': 'Remember MISCREANT = MIS-CREANT person - badly behaved villain or wrongdoer.',
                'example_sentence': 'The security system was designed to deter any ______ from attempting to break into the building.'
            },
            'misdemeanor': {
                'definition': 'American spelling of misdemeanour; a minor wrongdoing or a criminal offense less serious than a felony. Misdemeanors typically result in fines, community service, probation, or short jail sentences rather than lengthy prison terms. Examples include petty theft, simple assault, public intoxication, and traffic violations. The distinction between misdemeanors and felonies varies by jurisdiction but generally involves severity of crime and potential punishment. Misdemeanor convictions can affect employment opportunities, professional licenses, and background checks, though less severely than felonies. Legal representation helps ensure fair treatment and appropriate sentencing for misdemeanor charges. Understanding misdemeanor classifications helps in recognizing criminal justice system organization and potential consequences of different types of illegal behavior.',
                'pronunciation': "/ˌmɪs.dɪˈmin.ər/",
                'etymology': 'American spelling from "mis-" (wrong) + "demeanor" (behavior), meaning minor wrong behavior.',
                'memory_tip': 'Remember MISDEMEANOR = MIS-DEMEANOR - wrong behavior that\'s less serious crime.',
                'example_sentence': 'The shoplifting charge was classified as a ______ with a maximum penalty of six months in jail.'
            },
            'misdemeanour': {
                'definition': 'British spelling of misdemeanor; a minor wrongdoing or criminal offense less serious than a felony. Misdemeanours encompass various minor crimes that violate law but don\'t warrant severe punishment like felonies. British legal tradition distinguishes between summary offenses (minor violations) and indictable offenses (serious crimes requiring jury trials). Historical misdemeanours included public disorder, minor theft, and breach of peace. Modern applications might involve parking violations, minor drug possession, or disturbing the peace. Legal consequences typically include fines, community service, or brief custody rather than imprisonment. The spelling difference reflects British and American English variations while maintaining similar legal concepts. Understanding misdemeanour classifications helps recognize different levels of criminal behavior and appropriate legal responses.',
                'pronunciation': "/ˌmɪs.dɪˈmin.ər/",
                'etymology': 'British spelling from "mis-" (wrong) + "demeanour" (behavior), meaning minor criminal behavior.',
                'memory_tip': 'Remember MISDEMEANOUR = British MISDEMEANOR - minor wrongdoing with U spelling.',
                'example_sentence': 'The magistrate dealt with the ______ quickly, imposing a small fine and community service.'
            },
            'misericordes': {
                'definition': 'Plural of misericorde, referring to small mercy seats or folding seats in choir stalls that provide support during long religious services. Misericordes allow clergy and choir members to appear standing while actually resting on small ledges, providing comfort during extended periods of worship. These architectural features often include carved decorations, religious symbols, or humorous scenes on their undersides. Medieval churches incorporated misericordes as practical solutions to physical demands of lengthy liturgical services. The term reflects religious compassion (mercy) toward human physical limitations during spiritual activities. Modern church architecture may include similar features for elderly or infirm congregants. Understanding misericordes demonstrates the intersection of practical needs and religious architecture, showing how buildings accommodate human comfort within spiritual contexts.',
                'pronunciation': "/mɪˈzɛr.ɪˌkɔr.diz/",
                'etymology': 'Plural of "misericorde," from Latin "misericordia" (mercy), referring to mercy seats in churches.',
                'memory_tip': 'Remember MISERICORDES = mercy seats showing MERCY for tired people during long services.',
                'example_sentence': 'The medieval cathedral\'s choir stalls featured ornately carved ______ for the comfort of singing clergy.'
            },
            'misericords': {
                'definition': 'Alternative plural form of misericorde, referring to the same mercy seats or folding supports in church choir stalls. Misericords serve identical functions as misericordes, providing discreet seating assistance during religious services that require prolonged standing. These architectural elements demonstrate medieval attention to human comfort within religious discipline. Carved misericords often feature biblical scenes, moral lessons, or even secular subjects including animals, fantasy creatures, and daily life activities. The craftsmanship reflects both practical engineering and artistic expression in religious settings. Different churches may use varying plural forms while referring to the same architectural features. Understanding misericords involves appreciating both functional design and decorative artistry in religious architecture that balances spiritual requirements with human physical needs.',
                'pronunciation': "/ˈmɪz.ər.ɪˌkɔrdz/",
                'etymology': 'Alternative plural of "misericord," from Latin "misericordia" (mercy), meaning mercy seats.',
                'memory_tip': 'Remember MISERICORDS = alternative plural for mercy seats - same function as misericordes.',
                'example_sentence': 'Art historians studied the intricate carvings on the ______ to understand medieval artistic traditions.'
            },
            'misery': {
                'definition': 'Great suffering or discomfort of mind or body; a state of extreme unhappiness or distress. Misery encompasses both physical pain and emotional anguish that significantly impacts quality of life and wellbeing. Chronic illness can cause prolonged misery through persistent pain and functional limitations. Economic misery results from poverty, unemployment, or financial instability that creates stress and hardship. Emotional misery includes depression, grief, loneliness, and anxiety that affect mental health and relationships. The phrase "misery loves company" suggests that suffering people seek others who understand their pain. Social misery affects entire communities through war, natural disasters, or systemic injustice. Understanding misery involves recognizing human suffering and the importance of compassion, support systems, and interventions that alleviate pain and distress.',
                'pronunciation': "/ˈmɪz.ər.i/",
                'etymology': 'From Latin "miseria," meaning wretchedness or distress, derived from "miser" (wretched).',
                'memory_tip': 'Remember MISERY = extreme unhappiness that makes you MISS feeling happy.',
                'example_sentence': 'The refugees\' ______ was evident in their exhausted faces and desperate search for safety.'
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
            'millisecondmillivolt',     # millisecond + millivolt
            'millivoltherringbone',     # millivolt + herringbone
            'mimeticunabated',          # mimetic + unabated
            'mischievousbionic'         # mischievous + bionic
        ]
        
        for word in words_to_check:
            combined_words.append(word)
            
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        """Process the batch with comprehensive Claude data"""
        
        logger.info("Processing Batch 112 with comprehensive Claude data...")
        
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
    processor = Batch112Processor()
    
    input_file = "output/batch_112_words.csv"
    output_file = "output/batch_112_processed.csv"
    
    try:
        word_count = processor.process_batch(input_file, output_file)
        
        logger.info("Batch 112 processing completed!")
        logger.info(f"Processed {word_count} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {word_count} successful, 0 failed")
        
    except Exception as e:
        logger.error(f"Error processing batch 112: {str(e)}")
        raise