#!/usr/bin/env python3

import csv
import logging
from typing import Dict, List, Any
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DifficultyCalculator:
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._calculate_word_frequency(word)
        morphological_score = self._calculate_morphological_complexity(word)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score,
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'difficulty': None
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        word = word.lower()
        irregularities = 0
        
        patterns = [
            (r'gh', 1), (r'ough', 2), (r'ph', 1), (r'ch(?![aeiouy])', 1),
            (r'qu', 0.5), (r'x', 1), (r'tion', 0.5), (r'sion', 0.5),
            (r'eau', 2), (r'ieu', 2), (r'ée', 1), (r'silent.*e$', 1)
        ]
        
        for pattern, weight in patterns:
            irregularities += len(re.findall(pattern, word)) * weight
        
        length_factor = len(word) / 10
        return min(5.0, irregularities + length_factor)
    
    def _calculate_word_frequency(self, word: str) -> float:
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        word_lower = word.lower()
        
        if word_lower in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 6:
            return 3.0
        elif len(word) <= 8:
            return 4.0
        else:
            return 5.0
    
    def _calculate_morphological_complexity(self, word: str) -> float:
        word = word.lower()
        
        prefixes = ['un', 're', 'pre', 'dis', 'over', 'under', 'out', 'up', 'sub', 'inter', 'fore', 'de', 'mis', 'anti', 'semi', 'super', 'trans', 'ultra', 'non']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'ive', 'al', 'ic', 'ism', 'ist', 'ize', 'ise']
        
        morphemes = 1
        temp_word = word
        
        for prefix in prefixes:
            if temp_word.startswith(prefix):
                morphemes += 1
                temp_word = temp_word[len(prefix):]
                break
        
        for suffix in suffixes:
            if temp_word.endswith(suffix):
                morphemes += 1
                temp_word = temp_word[:-len(suffix)]
                break
        
        if morphemes == 1:
            return 1.0
        elif morphemes == 2:
            return 2.5
        elif morphemes == 3:
            return 4.0
        else:
            return 5.0
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        if not etymology or etymology.lower() in ['unknown', 'uncertain']:
            return 3.0
        
        etymology_lower = etymology.lower()
        complex_origins = ['sanskrit', 'hebrew', 'arabic', 'mandarin', 'japanese', 'finnish', 'hungarian', 'czech', 'polish', 'russian', 'nahuatl', 'quechua']
        moderate_origins = ['greek', 'latin', 'old english', 'middle english', 'old french', 'german', 'dutch', 'scandinavian', 'norse']
        simple_origins = ['english', 'french', 'spanish', 'italian', 'portuguese']
        
        if any(origin in etymology_lower for origin in complex_origins):
            return 5.0
        elif any(origin in etymology_lower for origin in moderate_origins):
            return 3.0
        elif any(origin in etymology_lower for origin in simple_origins):
            return 2.0
        else:
            return 3.5

class Batch125Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.combined_words = []
        
    def detect_combined_words(self) -> List[str]:
        combined_patterns = [
            'outréululate',
            'oxalismyeloma',
            'ozonenoun'
        ]
        return combined_patterns
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        word_data = {
            'outer': {
                'definition': 'Located on the outside or external surface; farther from the center or interior. In anatomy, outer refers to structures closer to the surface of the body or farther from the midline. In geography and spatial contexts, it describes regions, areas, or boundaries that are external or peripheral. The term can also refer to superficial appearances versus deeper realities, as in "outer behavior" versus inner thoughts. In astronomy, outer planets are those farther from the sun. The concept of "outer" is fundamental to understanding spatial relationships, boundaries, and surface versus depth distinctions.',
                'pronunciation': '/ˈaʊtər/',
                'pronunciation_ipa': '/ˈaʊtər/',
                'etymology': 'Comparative form of "out," from Old English "ut" meaning outside or away. The "-er" suffix creates the comparative, meaning "more out" or "farther outside."',
                'memory_tip': 'OUTER = OUT + ER (more). Think of something that is "more out" than something else - farther from the center or outside.',
                'example_sentence': 'The _____ layer of the atmosphere protects Earth from harmful radiation.'
            },
            'outfits': {
                'definition': 'Sets of clothes worn together, typically coordinated for a specific occasion, activity, or style. Outfits can range from casual everyday clothing to formal attire for special events. The term also refers to organizations, groups, or companies, particularly in military or business contexts. In fashion, creating outfits involves matching colors, styles, and accessories to achieve a desired look. The word can also be used as a verb meaning to provide someone with equipment or clothing. Planning outfits is an important aspect of personal style and professional presentation.',
                'pronunciation': '/ˈaʊtˌfɪts/',
                'pronunciation_ipa': '/ˈaʊtˌfɪts/',
                'etymology': 'From "outfit," originally meaning equipment or supplies provided for a journey or expedition, from "out" + "fit" (to provide or equip). The clothing sense developed later.',
                'memory_tip': 'OUTFITS = OUT + FITS. Think of clothes that "fit" together when you go "out" - coordinated clothing sets for wearing outside.',
                'example_sentence': 'She planned several different _____ for her vacation, including casual wear and formal dinner attire.'
            },
            'outlandish': {
                'definition': 'Bizarre, strange, or unconventional to the point of being shocking or difficult to believe; extremely unusual or eccentric. The term describes behavior, ideas, appearance, or situations that deviate significantly from normal expectations or social norms. Outlandish things often attract attention because of their unusual nature and may be considered either fascinating or inappropriate depending on context. The word can apply to fashion choices, artistic expressions, theories, or any aspect of human behavior that seems extraordinarily different from what is considered typical or acceptable.',
                'pronunciation': '/aʊtˈlændɪʃ/',
                'pronunciation_ipa': '/aʊtˈlændɪʃ/',
                'etymology': 'From "outland" (foreign, remote land) + "-ish" suffix. Originally meant "foreign" or "from a remote place," later evolved to mean strange or bizarre.',
                'memory_tip': 'OUTLANDISH = OUT-LAND-ISH. Think of strange customs from "out" in foreign "lands" - so unusual they seem foreign or bizarre.',
                'example_sentence': 'His _____ theory about alien visitors was met with skepticism from the scientific community.'
            },
            'outlets': {
                'definition': 'Openings or channels through which something can flow, escape, or be released; retail stores that sell goods, often at discounted prices. In electrical contexts, outlets are receptacles where devices can be plugged in to receive power. In geography, outlets are points where water bodies discharge into larger bodies of water. The term also refers to means of expression, release, or communication, such as creative outlets or media outlets. In retail, outlet stores sell manufacturer goods directly to consumers, often at reduced prices.',
                'pronunciation': '/ˈaʊtˌlɛts/',
                'pronunciation_ipa': '/ˈaʊtˌlɛts/',
                'etymology': 'From "outlet," from "out" + "let" (to allow passage). Originally referred to places where water flows out, later extended to other types of openings and channels.',
                'memory_tip': 'OUTLETS = OUT + LETS. Think of places that "let" things go "out" - whether electricity, water, or goods in stores.',
                'example_sentence': 'The designer clothing _____ offered significant savings on last season\'s fashions.'
            },
            'outlined': {
                'definition': 'Drew the outer edge or boundary of something; described the main features or general plan of something without going into detail. In art and drawing, outlining involves creating the external contours of objects or figures. In writing and planning, outlining means organizing ideas into a structured framework showing main points and sub-points. The past tense indicates that this process has been completed. Outlining is fundamental to effective communication, allowing complex information to be presented in an organized, accessible manner.',
                'pronunciation': '/ˈaʊtˌlaɪnd/',
                'pronunciation_ipa': '/ˈaʊtˌlaɪnd/',
                'etymology': 'From "outline," from "out" + "line." The verb form means to draw lines around the outside or to sketch the main features of something.',
                'memory_tip': 'OUTLINED = OUT + LINED. Think of drawing "lines" around the "outside" of something, or laying out the main lines of a plan.',
                'example_sentence': 'The professor _____ the key topics that would be covered in the semester-long course.'
            },
            'outrageous': {
                'definition': 'Shockingly bad, excessive, or unreasonable; wildly unconventional or bold. The term describes actions, behavior, prices, or situations that exceed normal bounds of acceptability or propriety. Outrageous can express moral indignation at injustice or wrongdoing, or it can describe something so unusual or extreme that it provokes strong reactions. In entertainment, outrageous behavior might be deliberately provocative or attention-seeking. The word carries strong emotional connotations and suggests that something has crossed important boundaries of reasonableness or decency.',
                'pronunciation': '/aʊtˈreɪdʒəs/',
                'pronunciation_ipa': '/aʊtˈreɪdʒəs/',
                'etymology': 'From "outrage" (from Old French "outrage," meaning excess or violence) + "-ous" suffix meaning characterized by. Originally meant characterized by violent excess.',
                'memory_tip': 'OUTRAGEOUS = OUTRAGE + OUS. Think of something so extreme it causes "outrage" in people - shocking or excessive behavior.',
                'example_sentence': 'The restaurant\'s _____ prices made it impossible for most locals to afford dining there.'
            },
            'outright': {
                'definition': 'Completely, entirely, or without reservation; openly and directly without concealment or qualification. As an adjective, outright means complete, total, or unambiguous. As an adverb, it means immediately, on the spot, or without delay. The term suggests absolute directness and lack of ambiguity or half-measures. In legal contexts, outright ownership means complete possession without conditions. In communication, speaking outright means being completely frank and direct without diplomatically softening the message.',
                'pronunciation': '/ˈaʊtˌraɪt/',
                'pronunciation_ipa': '/ˈaʊtˌraɪt/',
                'etymology': 'From "out" + "right," literally meaning "completely right" or "straight out." The combination emphasizes completeness and directness.',
                'memory_tip': 'OUTRIGHT = OUT + RIGHT. Think of going "straight out" with the truth - completely and directly, no holding back.',
                'example_sentence': 'She rejected the proposal _____, saying it was completely unacceptable to her organization.'
            },
            'outré': {
                'definition': 'Unconventional to the point of being bizarre or shocking; violating established social norms or conventions in a dramatic way. This French-derived adjective describes behavior, art, fashion, or ideas that deliberately flout conventional standards. Outré implies a conscious choice to be different rather than accidental unconventionality. The term is often used in artistic, literary, or fashion contexts to describe works or styles that challenge traditional boundaries. It suggests sophisticated transgression rather than simple bad taste.',
                'pronunciation': '/uˈtreɪ/',
                'pronunciation_ipa': '/uˈtreɪ/',
                'etymology': 'From French "outré," past participle of "outrer" meaning to carry to excess, from "outre" meaning beyond. Entered English in the 18th century.',
                'memory_tip': 'OUTRÉ sounds like "OOH-TRAY" - think of someone saying "ooh" at a tray of bizarre, unconventional food that shocks dinner guests.',
                'example_sentence': 'The artist\'s _____ performance piece challenged audience expectations and sparked heated debate.'
            },
            'outside': {
                'definition': 'The external part, surface, or area of something; not inside or within the boundaries of a particular space, group, or organization. As an adverb, it means in or to a position away from the interior. As an adjective, it describes something external, foreign, or not belonging to the main group. The concept of outside is fundamental to spatial relationships, boundaries, and distinctions between interior and exterior. In social contexts, being outside can mean being excluded or not belonging to a particular group or community.',
                'pronunciation': '/aʊtˈsaɪd/',
                'pronunciation_ipa': '/aʊtˈsaɪd/',
                'etymology': 'From "out" + "side," literally meaning the side that is out or external. The compound has been used since Middle English to describe exterior positions.',
                'memory_tip': 'OUTSIDE = OUT + SIDE. Think of the "side" that is "out" - the external part or area away from the interior.',
                'example_sentence': 'The children played _____ in the garden while their parents prepared dinner indoors.'
            },
            'oval': {
                'definition': 'Having a rounded, elongated shape like an egg; an elliptical or ovoid form that is longer in one direction than the other. In geometry, an oval is a closed curve that resembles a flattened circle. The shape appears frequently in nature, architecture, and design. Oval objects include eggs, athletic tracks, certain leaves, and many decorative elements. The term can describe both two-dimensional shapes and three-dimensional objects. Oval designs are often chosen for their pleasing, organic appearance and efficient use of space.',
                'pronunciation': '/ˈoʊvəl/',
                'pronunciation_ipa': '/ˈoʊvəl/',
                'etymology': 'From Latin "ovum" meaning egg, through Medieval Latin "ovalis." The shape resembles that of an egg, which gave rise to the geometric term.',
                'memory_tip': 'OVAL comes from "OVum" (egg). Think of an egg shape - that\'s an oval, elongated and rounded like an egg.',
                'example_sentence': 'The president addressed the nation from behind the _____ desk in the Oval Office.'
            },
            'ovation': {
                'definition': 'An enthusiastic display of approval, typically involving prolonged applause and sometimes standing; a public demonstration of praise or welcome. Standing ovations represent the highest form of audience appreciation, where people rise from their seats while applauding. The term originates from ancient Roman celebrations honoring military commanders. Modern ovations occur in theaters, concert halls, sporting events, and other public gatherings. The duration and intensity of an ovation indicate the level of audience appreciation and can become memorable moments in performers\' careers.',
                'pronunciation': '/oʊˈveɪʃən/',
                'pronunciation_ipa': '/oʊˈveɪʃən/',
                'etymology': 'From Latin "ovatio," a type of Roman triumph celebration, from "ovare" meaning to rejoice or exult. Originally referred to a specific Roman military honor.',
                'memory_tip': 'OVATION sounds like "OH-VATION" - think of people saying "OH!" in approval and giving a vacation from sitting (standing ovation).',
                'example_sentence': 'The pianist received a thunderous _____ after her brilliant performance of the concerto.'
            },
            'overcome': {
                'definition': 'To succeed in dealing with or controlling a problem, difficulty, or challenging situation; to defeat or prevail over obstacles through effort, determination, or skill. The term can describe conquering fears, addictions, illnesses, or any form of adversity. Overcoming often requires persistence, courage, and sometimes external support. In emotional contexts, being overcome means being overwhelmed by strong feelings. The concept is central to personal development, psychology, and narratives of triumph over adversity.',
                'pronunciation': '/ˌoʊvərˈkʌm/',
                'pronunciation_ipa': '/ˌoʊvərˈkʌm/',
                'etymology': 'From Old English "ofercuman," from "ofer" (over) + "cuman" (to come). Literally means to come over or get the better of something.',
                'memory_tip': 'OVERCOME = OVER + COME. Think of "coming over" a mountain or obstacle - getting over and past difficulties through effort.',
                'example_sentence': 'Through years of therapy and support, she was able to _____ her fear of public speaking.'
            },
            'overlaid': {
                'definition': 'Past tense of overlay; covered with a layer of something else; placed on top of or superimposed upon another surface. In decorative arts, overlaying involves applying thin layers of precious metals, veneers, or other materials to enhance appearance. In technology, overlaid graphics or data are superimposed on base images or maps. The technique is used in manufacturing, art, cartography, and digital media. Overlaying can serve protective, decorative, or informational functions.',
                'pronunciation': '/ˌoʊvərˈleɪd/',
                'pronunciation_ipa': '/ˌoʊvərˈleɪd/',
                'etymology': 'From "overlay," from "over" + "lay" (to place). The past tense form indicates the completed action of placing something over another surface.',
                'memory_tip': 'OVERLAID = OVER + LAID. Think of something "laid" (placed) "over" something else - like laying a blanket over a bed.',
                'example_sentence': 'The antique table was _____ with intricate gold leaf patterns that gleamed in the candlelight.'
            },
            'overrun': {
                'definition': 'To spread over or occupy an area rapidly and in large numbers; to exceed a planned limit, budget, or timeframe. In military contexts, overrunning means conquering territory by rapid advance. In pest control, overrun describes rapid population growth that overwhelms an ecosystem. In project management, cost or time overruns indicate exceeding planned resources. The term suggests loss of control and unwanted excess. Overruns can be problematic in construction, software development, and any planned activity with defined constraints.',
                'pronunciation': '/ˌoʊvərˈrʌn/',
                'pronunciation_ipa': '/ˌoʊvərˈrʌn/',
                'etymology': 'From "over" + "run," literally meaning to run beyond or over something. The compound emphasizes exceeding boundaries or limits.',
                'memory_tip': 'OVERRUN = OVER + RUN. Think of something "running over" its boundaries - like weeds overrunning a garden or costs running over budget.',
                'example_sentence': 'The construction project was _____ by budget constraints due to unexpected material costs.'
            },
            'overseas': {
                'definition': 'In, to, or from a country across the sea; foreign countries, especially those requiring sea travel to reach. As an adjective, overseas describes things located in or relating to foreign countries. The term reflects historical perspectives when sea travel was the primary means of international transportation. In business, overseas operations refer to international activities. In military contexts, overseas deployment means service in foreign countries. The concept emphasizes distance and separation created by ocean barriers.',
                'pronunciation': '/ˌoʊvərˈsiz/',
                'pronunciation_ipa': '/ˌoʊvərˈsiz/',
                'etymology': 'From "over" + "seas," literally meaning across or beyond the seas. The term reflects the geographic separation created by ocean travel.',
                'memory_tip': 'OVERSEAS = OVER + SEAS. Think of traveling "over the seas" to reach foreign countries - across the ocean to other lands.',
                'example_sentence': 'The company expanded its _____ operations to include manufacturing facilities in three different continents.'
            },
            'overthrow': {
                'definition': 'To remove forcibly from power; to defeat and replace a government, ruler, or established system through revolution or coup. As a noun, overthrow refers to the act of deposing authority or the resulting political change. In sports, overthrow means throwing a ball beyond its intended target. The term implies sudden, dramatic change achieved through force rather than gradual reform. Political overthrows have shaped history, creating new governments and social systems. The concept raises questions about legitimacy, violence, and social change.',
                'pronunciation': '/ˌoʊvərˈθroʊ/',
                'pronunciation_ipa': '/ˌoʊvərˈθroʊ/',
                'etymology': 'From "over" + "throw," literally meaning to throw down or over. Originally meant to physically overturn, later extended to political meanings.',
                'memory_tip': 'OVERTHROW = OVER + THROW. Think of "throwing over" a government - tossing it out of power and replacing it.',
                'example_sentence': 'The military coup succeeded in its attempt to _____ the corrupt dictatorial regime.'
            },
            'overtly': {
                'definition': 'In an open, evident manner; without concealment or secrecy; publicly and obviously. The adverb describes actions or behaviors that are deliberately visible and undisguised. Overt behavior contrasts with covert or hidden activities. In psychology and sociology, overtly expressed attitudes are those people openly display rather than keeping private. In politics and diplomacy, overtly stated positions are official, public stances. The term emphasizes transparency and lack of subterfuge in communication or action.',
                'pronunciation': '/oʊˈvɜrtli/',
                'pronunciation_ipa': '/oʊˈvɜrtli/',
                'etymology': 'From "overt" (from Old French "overt," past participle of "ovrir" meaning to open) + "-ly" adverb suffix. Means in an open, unconcealed manner.',
                'memory_tip': 'OVERTLY = OVERT + LY. Think of being "OVER-T" (over the top) in openness - doing things openly and obviously.',
                'example_sentence': 'While not _____ hostile, the ambassador\'s comments contained subtle criticism of the trade agreement.'
            },
            'overtures': {
                'definition': 'Opening moves or initial approaches made to initiate negotiations, relationships, or communications; introductory musical pieces performed before operas, ballets, or concerts. In diplomacy, overtures are preliminary proposals or gestures designed to begin formal discussions. In music, overtures set the mood and introduce themes for larger works. Social overtures involve initial attempts to establish friendships or romantic relationships. The term suggests tentative, exploratory actions that may lead to more substantial developments. Successful overtures require careful timing and sensitivity to receptiveness.',
                'pronunciation': '/ˈoʊvərˌtʃʊrz/',
                'pronunciation_ipa': '/ˈoʊvərˌtʃʊrz/',
                'etymology': 'From French "ouverture" meaning opening, from "ouvrir" to open. In music, refers to opening pieces; in diplomacy, to opening moves.',
                'memory_tip': 'OVERTURES = OVER + TURES (openings). Think of "opening over" to someone - making initial approaches or opening moves.',
                'example_sentence': 'The ambassador made diplomatic _____ to resolve the border dispute through peaceful negotiations.'
            },
            'overweening': {
                'definition': 'Excessively arrogant, presumptuous, or confident; showing an unreasonable belief in one\'s own importance or abilities. The term describes pride or ambition that exceeds appropriate bounds and often leads to downfall. Overweening behavior typically involves overestimating one\'s capabilities while underestimating obstacles or opposition. In literature, overweening characters often serve as cautionary examples of hubris. The word carries strong negative connotations, suggesting that such excessive confidence is both morally objectionable and practically dangerous.',
                'pronunciation': '/ˌoʊvərˈwinɪŋ/',
                'pronunciation_ipa': '/ˌoʊvərˈwinɪŋ/',
                'etymology': 'From "over" + "weening" (thinking, supposing), from Old English "wenan" meaning to expect or suppose. Literally means "over-thinking" of oneself.',
                'memory_tip': 'OVERWEENING = OVER + WEENING (thinking). Think of "over-thinking" you\'re great - excessive arrogance and self-importance.',
                'example_sentence': 'His _____ confidence in the business plan blinded him to obvious market risks and competitive threats.'
            },
            'oviparous': {
                'definition': 'Producing eggs that develop and hatch outside the mother\'s body; describing animals that reproduce by laying eggs rather than giving birth to live young. Oviparous species include birds, most reptiles, amphibians, fish, and many invertebrates. The eggs contain all nutrients needed for embryonic development and are often protected by shells or other coverings. This reproductive strategy contrasts with viviparous (live birth) and ovoviviparous (eggs hatched internally) reproduction. Understanding oviparity is crucial in biology, ecology, and animal husbandry.',
                'pronunciation': '/oʊˈvɪpərəs/',
                'pronunciation_ipa': '/oʊˈvɪpərəs/',
                'etymology': 'From Latin "ovum" (egg) + "parere" (to bring forth) + "-ous" suffix. Literally means "egg-bearing" or producing eggs.',
                'memory_tip': 'OVIPAROUS = OVI (egg) + PAROUS (bearing). Think of animals that "bear eggs" - like chickens, turtles, and fish that lay eggs.',
                'example_sentence': 'Most bird species are _____, carefully constructing nests where they can safely incubate their eggs.'
            },
            'owlishly': {
                'definition': 'In a manner resembling an owl; with a solemn, wise, or studious appearance, often characterized by large, round eyes and serious expression. The adverb describes behavior or appearance that suggests wisdom, thoughtfulness, or scholarly attention. Owlish behavior often involves quiet observation, careful listening, and measured responses. The comparison to owls draws on cultural associations between these birds and wisdom or learning. People described as acting owlishly typically appear contemplative and intellectually engaged.',
                'pronunciation': '/ˈaʊlɪʃli/',
                'pronunciation_ipa': '/ˈaʊlɪʃli/',
                'etymology': 'From "owlish" (resembling an owl) + "-ly" adverb suffix. Owls have been associated with wisdom since ancient times, influencing the meaning.',
                'memory_tip': 'OWLISHLY = OWL + ISHLY. Think of acting like a wise OWL - looking thoughtful and studious with big, observant eyes.',
                'example_sentence': 'The professor peered _____ over his glasses at the student who had asked the complex question.'
            },
            'owners': {
                'definition': 'People who possess legal title to property, businesses, or other assets; individuals who have the right to use, control, and dispose of something they own. Ownership involves both rights and responsibilities, including maintenance, liability, and decision-making authority. In business contexts, owners may be individuals, partnerships, or corporations. Property owners must comply with laws and regulations governing their assets. The concept of ownership is fundamental to economic systems, legal frameworks, and personal wealth accumulation.',
                'pronunciation': '/ˈoʊnərz/',
                'pronunciation_ipa': '/ˈoʊnərz/',
                'etymology': 'From "owner" (from "own" + "-er" suffix indicating one who does something) + plural "-s." "Own" comes from Old English meaning to possess.',
                'memory_tip': 'OWNERS = OWN + ERS. Think of people who "own" things - the "ers" (people) who possess and control property or assets.',
                'example_sentence': 'The restaurant _____ decided to expand their business by opening a second location downtown.'
            },
            'oxalis': {
                'definition': 'A genus of flowering plants in the wood-sorrel family, commonly known as wood sorrels or shamrocks. Oxalis species are characterized by their distinctive three-leaflet leaves and delicate flowers in various colors. Many species are cultivated as ornamental plants, while others are considered weeds. Some oxalis varieties produce edible leaves and bulbs with a tart, lemony flavor due to oxalic acid content. The plants are found worldwide and include both annual and perennial species. Several oxalis species are associated with cultural symbols, particularly in Ireland.',
                'pronunciation': '/ˈɑksəlɪs/',
                'pronunciation_ipa': '/ˈɑksəlɪs/',
                'etymology': 'From Greek "oxalis" meaning sour, from "oxys" meaning sharp or acid, referring to the tart taste of the leaves due to oxalic acid content.',
                'memory_tip': 'OXALIS contains "OXA" (acid). Think of the "OX-ACID" taste - oxalis plants have sour, acidic-tasting leaves.',
                'example_sentence': 'The gardener planted purple _____ bulbs around the border to create a carpet of delicate spring flowers.'
            },
            'oxon': {
                'definition': 'An abbreviation for "Oxoniensis," meaning "of Oxford," used in academic titles and degrees from Oxford University. The term appears in post-nominal letters after names to indicate Oxford University graduation, such as "MA Oxon" (Master of Arts from Oxford). It derives from the Latin name for Oxford and maintains the university\'s traditional academic nomenclature. The abbreviation distinguishes Oxford degrees from those of other universities and preserves centuries-old academic traditions. Similar abbreviations exist for other ancient universities.',
                'pronunciation': '/ˈɑksən/',
                'pronunciation_ipa': '/ˈɑksən/',
                'etymology': 'From Latin "Oxoniensis," meaning "of Oxford," from "Oxonia," the Latin name for Oxford. Used in academic contexts to denote Oxford University affiliation.',
                'memory_tip': 'OXON sounds like "OX-ON" - think of the ox (bull) in Oxford\'s coat of arms, putting "OX ON" your degree from Oxford.',
                'example_sentence': 'The distinguished professor held an MA _____ degree from Oxford University.'
            },
            'oxyacetylene': {
                'definition': 'A combination of oxygen and acetylene gases used in welding and cutting torches to produce extremely high temperatures. Oxyacetylene flames can reach temperatures of about 3,500°C (6,330°F), making them ideal for cutting through steel and welding metals. The process involves mixing oxygen and acetylene in precise ratios and igniting the mixture to create an intense, focused flame. This technology revolutionized metalworking and construction industries. Safety protocols are crucial when handling these gases due to their explosive potential and the extreme heat generated.',
                'pronunciation': '/ˌɑksiəˈsɛtəˌlin/',
                'pronunciation_ipa': '/ˌɑksiəˈsɛtəˌlin/',
                'etymology': 'Compound of "oxy-" (from oxygen) + "acetylene" (a hydrocarbon gas). The combination describes the two gases mixed for high-temperature welding.',
                'memory_tip': 'OXYACETYLENE = OXY (oxygen) + ACETYLENE. Think of "OXY" helping "ACETYLENE" burn super hot for welding metal.',
                'example_sentence': 'The metalworker used an _____ torch to cut through the thick steel beams during the demolition project.'
            },
            'oxygenate': {
                'definition': 'To supply, treat, or impregnate with oxygen; to add oxygen to blood, water, or other substances. In biology, oxygenation is essential for cellular respiration and energy production. The lungs oxygenate blood by transferring oxygen from inhaled air to red blood cells. In aquaculture and water treatment, oxygenation systems maintain healthy oxygen levels for aquatic life. Medical oxygenation devices assist patients with breathing difficulties. The process is fundamental to life and various industrial applications requiring oxygen-rich environments.',
                'pronunciation': '/ˈɑksɪdʒəˌneɪt/',
                'pronunciation_ipa': '/ˈɑksɪdʒəˌneɪt/',
                'etymology': 'From "oxygen" + "-ate" suffix meaning to provide with or treat with. The verb form indicates the action of adding oxygen to something.',
                'memory_tip': 'OXYGENATE = OXYGEN + ATE. Think of "eating oxygen" or adding oxygen to something - like how lungs oxygenate blood.',
                'example_sentence': 'The aquarium\'s filtration system helps _____ the water to keep the fish healthy and active.'
            },
            'oyez': {
                'definition': 'A traditional court crier\'s call for attention, typically shouted three times to open court sessions or make public announcements. The exclamation commands silence and attention from all present. Oyez is still used in some ceremonial court proceedings, particularly in British and American Supreme Courts. The tradition dates back centuries to when public announcements were made orally in town squares and courts. The call serves both practical and symbolic functions, marking the formal beginning of legal proceedings and emphasizing the authority of the court.',
                'pronunciation': '/ˈoʊjɛz/',
                'pronunciation_ipa': '/ˈoʊjɛz/',
                'etymology': 'From Anglo-French "oyez," imperative of "oir" meaning to hear, from Latin "audire." Literally means "hear ye" or "listen."',
                'memory_tip': 'OYEZ sounds like "OH YES" - think of a court crier saying "Oh yes, listen up!" to get everyone\'s attention in court.',
                'example_sentence': '"_____, _____, _____! All rise for the Honorable Judge," called the bailiff as court came to session.'
            },
            'oysters': {
                'definition': 'Marine bivalve mollusks with irregular shells, many species of which are edible and considered delicacies. Oysters are filter feeders that live in coastal waters, attaching themselves to hard surfaces. They play important ecological roles by filtering water and providing habitat for other marine species. Commercially, oysters are cultivated in aquaculture operations and harvested from wild beds. Different species have distinct flavors influenced by their environment. Oysters are often eaten raw on the half shell but can also be cooked in various ways.',
                'pronunciation': '/ˈɔɪstərz/',
                'pronunciation_ipa': '/ˈɔɪstərz/',
                'etymology': 'From Old French "oistre," from Latin "ostrea," from Greek "ostreon." The word has maintained similar forms across multiple languages.',
                'memory_tip': 'OYSTERS sounds like "OY-STERS" - think of saying "Oy!" when you see the expensive price of these shellfish delicacies.',
                'example_sentence': 'The restaurant specialized in fresh _____ harvested daily from the nearby coastal waters.'
            },
            'ozone': {
                'definition': 'A triatomic form of oxygen (O₃) that occurs naturally in Earth\'s stratosphere and forms a protective layer against ultraviolet radiation. At ground level, ozone is a pollutant that can cause respiratory problems and environmental damage. The stratospheric ozone layer is crucial for protecting life on Earth by filtering harmful UV rays. Ozone depletion, caused by human-made chemicals, has led to international environmental agreements. The gas has a distinctive sharp smell and is used in water treatment and air purification applications.',
                'pronunciation': '/ˈoʊzoʊn/',
                'pronunciation_ipa': '/ˈoʊzoʊn/',
                'etymology': 'From German "Ozon," coined from Greek "ozein" meaning to smell, referring to the gas\'s distinctive sharp odor.',
                'memory_tip': 'OZONE sounds like "OH-ZONE" - think of the "O" (oxygen) protective "zone" around Earth that shields us from harmful rays.',
                'example_sentence': 'Scientists monitor the _____ layer carefully to track changes in Earth\'s atmospheric protection from UV radiation.'
            },
            'pabulum': {
                'definition': 'Food or nourishment, especially for intellectual or spiritual growth; bland or simplistic material lacking substance or stimulation. In medical contexts, pabulum refers to any nutrient substance. More commonly, the term describes entertainment, literature, or information that is unchallenging and lacks intellectual depth. The word often carries negative connotations, suggesting that something is dumbed-down or overly simplified. Critical reviewers might dismiss certain media as pabulum when they believe it fails to engage audiences meaningfully or provide substantive content.',
                'pronunciation': '/ˈpæbjələm/',
                'pronunciation_ipa': '/ˈpæbjələm/',
                'etymology': 'From Latin "pabulum" meaning food or nourishment, from "pascere" meaning to feed. Originally referred to physical food, later extended to intellectual nourishment.',
                'memory_tip': 'PABULUM sounds like "PAP-YOU-LOVE" - think of bland baby food (pap) that\'s easy to consume but lacks substance.',
                'example_sentence': 'Critics dismissed the television series as mindless _____ that offered no meaningful insights or character development.'
            },
            'pace': {
                'definition': 'The speed or rate at which something moves, develops, or changes; a single step in walking or running. In athletics, pace refers to the speed maintained during a race or workout. In life and work, pace describes the rhythm or intensity of activities. The term can also mean to walk steadily back and forth, often when thinking or anxious. Setting an appropriate pace is crucial for endurance, productivity, and avoiding burnout. Different situations require different paces, from leisurely strolls to urgent emergency responses.',
                'pronunciation': '/peɪs/',
                'pronunciation_ipa': '/peɪs/',
                'etymology': 'From Latin "passus" meaning step or stride, through Old French "pas." The word encompasses both the physical act of stepping and the concept of speed.',
                'memory_tip': 'PACE sounds like "PAYS" - think of how the speed at which you work "pays" off - finding the right pace for success.',
                'example_sentence': 'The marathon runner maintained a steady _____ throughout the race to avoid exhaustion in the final miles.'
            },
            'pachinko': {
                'definition': 'A Japanese mechanical game resembling pinball, played for prizes in specialized parlors. Players launch small steel balls into a vertical playing field filled with pins, pockets, and mechanical devices. Successful players win more balls that can be exchanged for prizes or tokens. Pachinko parlors are ubiquitous in Japan and constitute a major entertainment industry. The game combines elements of skill and chance, creating an engaging and sometimes addictive experience. Despite gambling restrictions, pachinko operates in a legal gray area through complex prize exchange systems.',
                'pronunciation': '/pəˈtʃɪŋkoʊ/',
                'pronunciation_ipa': '/pəˈtʃɪŋkoʊ/',
                'etymology': 'From Japanese, possibly onomatopoetic, imitating the sound of balls bouncing through the machine. The word entered English through cultural exchange.',
                'memory_tip': 'PACHINKO sounds like "PACK-IN-GO" - think of packing balls into a machine and watching them go bounce around.',
                'example_sentence': 'The tourist was fascinated by the rows of _____ machines and the intense concentration of the players.'
            },
            'pachyderm': {
                'definition': 'A large mammal with thick skin, traditionally including elephants, rhinoceroses, and hippopotamuses. The term was historically used in zoological classification but is now considered outdated scientifically, as these animals belong to different taxonomic groups. Despite its obsolete scientific status, pachyderm remains in popular usage to describe thick-skinned, large terrestrial mammals. The word is often used metaphorically to describe people who are insensitive or thick-skinned emotionally. Conservation efforts focus heavily on protecting these charismatic megafauna.',
                'pronunciation': '/ˈpækɪˌdɜrm/',
                'pronunciation_ipa': '/ˈpækɪˌdɜrm/',
                'etymology': 'From Greek "pachys" meaning thick + "derma" meaning skin. Literally means "thick-skinned" and was coined for zoological classification.',
                'memory_tip': 'PACHYDERM = PACHY (thick) + DERM (skin). Think of "PACK-THICK-SKIN" - elephants and rhinos with thick, tough skin.',
                'example_sentence': 'The wildlife sanctuary provided a safe habitat for several endangered _____ species, including Asian elephants.'
            },
            'packet': {
                'definition': 'A small package or bundle; a quantity of information or data grouped together for transmission. In computing, packets are units of data sent over networks, each containing destination information and part of a larger message. In everyday use, packets contain small amounts of goods like seeds, seasoning, or documents. Mail services often distinguish between letters and packets based on size and weight. The concept of packetization is fundamental to modern digital communications, allowing efficient and reliable data transmission across complex networks.',
                'pronunciation': '/ˈpækɪt/',
                'pronunciation_ipa': '/ˈpækɪt/',
                'etymology': 'Diminutive of "pack," from Middle English "pakke." The "-et" suffix indicates a small version of a pack or package.',
                'memory_tip': 'PACKET = PACK + ET (small). Think of a small "pack" - a little package containing a small amount of something.',
                'example_sentence': 'She tore open the _____ of seeds and carefully planted them in rows in her garden.'
            },
            'paddles': {
                'definition': 'Flat-bladed implements used for propelling boats through water or for mixing, stirring, or hitting. In canoeing and kayaking, paddles are essential tools for navigation and speed control. Table tennis paddles are used to hit the ball in recreational and competitive play. Kitchen paddles help mix thick batters and sauces. The design varies based on intended use, with different blade shapes, sizes, and materials optimized for specific activities. Proper paddle technique is crucial for efficiency and preventing injury in water sports.',
                'pronunciation': '/ˈpædəlz/',
                'pronunciation_ipa': '/ˈpædəlz/',
                'etymology': 'From "paddle," possibly from Low German "paddeln" meaning to tramp about. Related to the splashing motion made when using the implement.',
                'memory_tip': 'PADDLES sounds like "PAD-DLES" - think of flat "pads" that "dell" (push) through water to move boats.',
                'example_sentence': 'The canoeists dipped their _____ into the calm lake water and glided silently toward the distant shore.'
            },
            'padhy': {
                'definition': 'This appears to be a proper name or term with limited standard dictionary definition. It may be a surname of Indian origin, particularly common in Odisha state. In some contexts, it could be a variant spelling or transliteration of a name or term from Indian languages. Without more specific context, it\'s difficult to provide a comprehensive definition. The term might appear in specialized texts, regional literature, or as a personal name rather than as a common English vocabulary word.',
                'pronunciation': '/ˈpædi/',
                'pronunciation_ipa': '/ˈpædi/',
                'etymology': 'Likely derived from Indian languages, possibly Sanskrit or regional languages of India. The exact etymological development is uncertain without more context.',
                'memory_tip': 'PADHY sounds like "PAD-HY" - without more context, think of it as a name that might relate to "pad" (a flat surface) in some way.',
                'example_sentence': 'Mr. _____ was known in his community for his contributions to local education and cultural preservation.'
            },
            'padre': {
                'definition': 'A priest, especially a military chaplain or a priest in Spanish-speaking countries. In military contexts, padre refers to chaplains who provide religious services and counseling to service members. The term reflects the paternal role of priests in their communities. In Latin American and Spanish contexts, padre is the standard word for priest or father. Military padres often serve in challenging conditions, providing spiritual support during conflicts and deployments. The role combines religious duties with counseling and morale support.',
                'pronunciation': '/ˈpɑdreɪ/',
                'pronunciation_ipa': '/ˈpɑdreɪ/',
                'etymology': 'From Spanish and Italian "padre" meaning father, from Latin "pater." Used in military contexts to refer to chaplains who serve as spiritual fathers.',
                'memory_tip': 'PADRE sounds like "PAH-DRAY" - think of "Papa" or "Dad" - padre means father, especially a priest who is a spiritual father.',
                'example_sentence': 'The regiment\'s _____ conducted services every Sunday and was always available to counsel soldiers.'
            },
            'paella': {
                'definition': 'A traditional Spanish rice dish originating from Valencia, typically cooked in a wide, shallow pan and featuring saffron, vegetables, and various proteins such as seafood, chicken, or rabbit. The dish is characterized by its golden color from saffron and the crispy layer of rice (socarrat) that forms at the bottom. Paella has become one of Spain\'s most internationally recognized dishes, with many regional variations. The cooking process is often social, with families and friends gathering around the paella pan. Authentic preparation requires specific techniques and ingredients.',
                'pronunciation': '/paɪˈɛlə/',
                'pronunciation_ipa': '/paɪˈɛlə/',
                'etymology': 'From Valencian "paella," from Old French "paelle," from Latin "patella" meaning pan or dish. Named after the wide, shallow pan used for cooking.',
                'memory_tip': 'PAELLA sounds like "PIE-ELL-A" - think of a "pie" cooked in a wide pan with "yellow" (saffron) rice, especially the "ELL" shape of the pan.',
                'example_sentence': 'The chef prepared an authentic seafood _____ with fresh mussels, shrimp, and perfectly seasoned saffron rice.'
            },
            'pageantry': {
                'definition': 'Elaborate and colorful ceremonial display; spectacular show or ceremony featuring elaborate costumes, decorations, and formal presentations. Pageantry often involves parades, processions, competitions, or celebrations that emphasize visual splendor and theatrical presentation. Historical pageantry includes royal coronations, religious festivals, and cultural celebrations. Modern pageantry encompasses beauty contests, award ceremonies, and entertainment events. The term can sometimes carry negative connotations, suggesting superficial spectacle without substance. Pageantry serves social, cultural, and political functions in communities worldwide.',
                'pronunciation': '/ˈpædʒəntri/',
                'pronunciation_ipa': '/ˈpædʒəntri/',
                'etymology': 'From "pageant" (from Medieval Latin "pagina," originally meaning a scene in a play) + "-ry" suffix indicating collection or practice.',
                'memory_tip': 'PAGEANTRY = PAGEANT + RY. Think of the "RY" (array) of beautiful displays in pageants - colorful, elaborate ceremonial shows.',
                'example_sentence': 'The royal wedding featured magnificent _____ with ornate carriages, ceremonial guards, and elaborate costumes.'
            },
            'pages': {
                'definition': 'Individual sheets of paper in books, magazines, or documents; young people who serve as assistants in formal institutions like legislatures or courts. In literature and publishing, pages contain text, images, or both sides of printed material. Page numbering systems help readers navigate documents. In historical contexts, pages were young nobles who served in royal courts or wealthy households as part of their education. Modern page programs in government provide educational opportunities for young people while they assist with official duties.',
                'pronunciation': '/ˈpeɪdʒəz/',
                'pronunciation_ipa': '/ˈpeɪdʒəz/',
                'etymology': 'From "page," from Old French "page" (both the paper and servant meanings), ultimately from Latin "pagina" meaning a written page.',
                'memory_tip': 'PAGES can mean paper "pages" in books or young "pages" who serve - both help people access information or services.',
                'example_sentence': 'The ancient manuscript\'s _____ were carefully preserved and digitized for scholarly research.'
            },
            'paginate': {
                'definition': 'To number the pages of a book, document, or publication in sequential order; to arrange content into pages with appropriate formatting and page breaks. Pagination is essential for creating professional documents, enabling easy reference and navigation. Modern word processing software automates pagination, but manual control is often necessary for complex layouts. Academic papers, legal documents, and books require careful pagination to meet formatting standards. The process includes decisions about page numbering styles, starting numbers, and placement of page numbers.',
                'pronunciation': '/ˈpædʒəˌneɪt/',
                'pronunciation_ipa': '/ˈpædʒəˌneɪt/',
                'etymology': 'From "page" + "-inate" suffix meaning to make or cause. The verb form means to create or arrange pages with numbers.',
                'memory_tip': 'PAGINATE = PAGE + IN + ATE. Think of putting pages "in" order and numbering them - organizing pages systematically.',
                'example_sentence': 'The editor asked the author to _____ the manuscript properly before submitting it for final review.'
            },
            'pagoda': {
                'definition': 'A tiered tower with multiple eaves, typically found in Asia and associated with Buddhist and Hindu temple architecture. Pagodas serve religious functions as places of worship, meditation, and housing sacred relics. The distinctive multi-story design with upward-curving roofs creates an elegant silhouette that has become iconic of Asian architecture. Different cultures have developed unique pagoda styles, from Japanese wooden structures to Chinese stone towers. Many pagodas are significant cultural landmarks and tourist attractions, representing centuries of architectural tradition and religious heritage.',
                'pronunciation': '/pəˈɡoʊdə/',
                'pronunciation_ipa': '/pəˈɡoʊdə/',
                'etymology': 'From Portuguese "pagode," possibly from Tamil "pagavadi" (house belonging to a deity) or Persian "butkada" (idol temple).',
                'memory_tip': 'PAGODA sounds like "PAGE-ODA" - think of multiple "pages" (levels) stacked up like an "ode" (tribute) to reach toward heaven.',
                'example_sentence': 'The ancient _____ stood majestically on the hillside, its five tiers rising gracefully against the sunset sky.'
            },
            'pahoehoe': {
                'definition': 'A type of volcanic lava flow characterized by a smooth, undulating, or ropy surface texture that forms when fluid basaltic lava cools slowly while continuing to move. Pahoehoe lava creates distinctive patterns resembling twisted rope or flowing fabric. This type of lava flow is common in Hawaiian volcanism and contrasts with \'a\'a lava, which has a rough, clinky surface. The smooth surface of pahoehoe forms because the lava maintains a flexible skin while the interior remains molten. Geologists study pahoehoe formations to understand volcanic processes and lava behavior.',
                'pronunciation': '/pəˈhoʊeɪˌhoʊeɪ/',
                'pronunciation_ipa': '/pəˈhoʊeɪˌhoʊeɪ/',
                'etymology': 'From Hawaiian "pāhoehoe," literally meaning "smooth lava." The term was adopted into geological terminology to describe this specific lava type.',
                'memory_tip': 'PAHOEHOE sounds like "PA-HOE-HOE" - think of "Papa\'s hoe-hoe" making smooth, rope-like patterns in the field, like smooth lava.',
                'example_sentence': 'The geologist pointed out the distinctive _____ lava formations that looked like giant ropes frozen in stone.'
            },
            'pail': {
                'definition': 'A bucket, typically cylindrical container with a handle, used for carrying liquids or other materials. Pails are commonly made of metal, plastic, or wood and serve various domestic, agricultural, and industrial purposes. Traditional milk pails were essential farm equipment for dairy operations. Modern pails are used for cleaning, gardening, construction, and storage. The size and material of pails vary according to their intended use, from small household cleaning buckets to large industrial containers. The handle design allows for easy carrying and pouring.',
                'pronunciation': '/peɪl/',
                'pronunciation_ipa': '/peɪl/',
                'etymology': 'From Old English "pægel," possibly from Latin "pagella" meaning small page or measuring device. The sense evolved to mean a container for measuring or carrying.',
                'memory_tip': 'PAIL sounds like "PALE" - think of a pale (light-colored) bucket used for carrying water, making your skin pale from the cold water.',
                'example_sentence': 'The child carried a small _____ to the beach to collect seashells and build sandcastles.'
            },
            'paillard': {
                'definition': 'A culinary term referring to a piece of meat, typically chicken, veal, or beef, that has been pounded thin and flattened, often breaded and sautéed. The technique creates tender, quick-cooking portions that are ideal for elegant presentations. Paillard preparation involves careful pounding to achieve uniform thickness without tearing the meat. The flattened pieces cook rapidly and evenly, making them popular in fine dining. Various seasonings, coatings, and sauces can be applied to create different flavor profiles. The method is named after a famous 19th-century Parisian restaurant.',
                'pronunciation': '/paɪˈjɑrd/',
                'pronunciation_ipa': '/paɪˈjɑrd/',
                'etymology': 'Named after the Café Paillard in Paris, a famous restaurant in the 19th century where this preparation method was popularized.',
                'memory_tip': 'PAILLARD sounds like "PIE-YARD" - think of meat pounded flat like a "pie" crust spread across a "yard" - thin and wide.',
                'example_sentence': 'The chef prepared a delicate chicken _____ with lemon and herbs for the elegant dinner party.'
            },
            'pain': {
                'definition': 'An unpleasant physical sensation or emotional suffering; discomfort caused by injury, illness, or psychological distress. Pain serves as a protective mechanism, alerting the body to potential damage and promoting healing behaviors. Chronic pain differs from acute pain in duration and treatment approaches. Pain management is a crucial medical specialty involving various therapies and medications. Emotional pain accompanies loss, disappointment, and trauma. Understanding pain mechanisms helps healthcare providers develop effective treatments and helps individuals cope with unavoidable suffering.',
                'pronunciation': '/peɪn/',
                'pronunciation_ipa': '/peɪn/',
                'etymology': 'From Old French "peine," from Latin "poena" meaning punishment or penalty. The concept connects physical suffering with punishment or consequence.',
                'memory_tip': 'PAIN sounds like "PANE" (window glass) - think of the sharp pain when you cut yourself on broken glass panes.',
                'example_sentence': 'The athlete experienced sharp _____ in her knee during the final sprint of the marathon.'
            },
            'painted': {
                'definition': 'Past tense of paint; covered with paint or color; created artwork using pigments and brushes. Painted surfaces protect materials from weather and wear while providing decorative appearance. In art, painted works include portraits, landscapes, abstracts, and various styles across cultures and time periods. Face painting and body painting serve ceremonial, artistic, and entertainment purposes. Painted descriptions can also mean vividly described or portrayed in words. The quality of painted work depends on preparation, materials, technique, and artistic skill.',
                'pronunciation': '/ˈpeɪntəd/',
                'pronunciation_ipa': '/ˈpeɪntəd/',
                'etymology': 'From "paint," from Old French "peint," past participle of "peindre" meaning to paint, from Latin "pingere" meaning to color or decorate.',
                'memory_tip': 'PAINTED = PAINT + ED. Think of something that has been "paint-ED" - covered with color or artistic pigments.',
                'example_sentence': 'The artist _____ a beautiful landscape that captured the golden light of the setting sun.'
            }
        }
        
        return word_data.get(word, {
            'definition': f'[Definition for {word} not found in comprehensive dataset]',
            'pronunciation': f'[Pronunciation for {word} not available]',
            'pronunciation_ipa': f'[IPA for {word} not available]',
            'etymology': f'[Etymology for {word} not available]',
            'memory_tip': f'[Memory tip for {word} not available]',
            'example_sentence': f'[Example sentence for {word} not available]'
        })

def process_batch_125():
    processor = Batch125Processor()
    
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_125_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_125_processed.csv'
    
    combined_words = processor.detect_combined_words()
    if combined_words:
        logging.warning(f"Detected combined words that need manual review: {combined_words}")
    
    processed_data = []
    successful_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            word = row['word'].strip()
            if not word:
                continue
                
            try:
                claude_data = processor.get_comprehensive_claude_data(word)
                
                if claude_data['definition'] != f'[Definition for {word} not found in comprehensive dataset]':
                    difficulty_scores = processor.difficulty_calc.calculate_difficulty_score(
                        word, claude_data['definition'], claude_data['etymology']
                    )
                    
                    processed_row = {
                        'word': word,
                        'years': row['years'],
                        'source_files': row['source_files'],
                        'source_difficulties': row['source_difficulties'],
                        'definition': claude_data['definition'],
                        'pronunciation': claude_data['pronunciation'],
                        'pronunciation_ipa': claude_data['pronunciation_ipa'],
                        'etymology': claude_data['etymology'],
                        'memory_tip': claude_data['memory_tip'],
                        'example_sentence': claude_data['example_sentence'],
                        'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                        'word_frequency_score': difficulty_scores['word_frequency_score'],
                        'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                        'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                        'difficulty': difficulty_scores['difficulty'],
                        'combined_word_error': word in combined_words,
                        'source': 'Claude'
                    }
                    
                    processed_data.append(processed_row)
                    successful_count += 1
                    logging.info(f"Successfully processed word {successful_count}: {word}")
                else:
                    logging.error(f"No data found for word: {word}")
                    
            except Exception as e:
                logging.error(f"Error processing word '{word}': {str(e)}")
    
    fieldnames = [
        'word', 'years', 'source_files', 'source_difficulties', 'definition',
        'pronunciation', 'pronunciation_ipa', 'etymology', 'memory_tip', 'example_sentence',
        'phonetic_transparency_score', 'word_frequency_score', 'morphological_complexity_score',
        'etymology_complexity_score', 'difficulty', 'combined_word_error', 'source'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)
    
    logging.info(f"Batch 125 processing complete. Processed {successful_count}/50 words.")
    logging.info(f"Output saved to: {output_file}")
    
    if combined_words:
        logging.warning(f"Combined word errors detected: {combined_words}")
    
    return successful_count

if __name__ == "__main__":
    process_batch_125()