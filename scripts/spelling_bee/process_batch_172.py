import pandas as pd
import csv
import logging
from typing import Dict, Any
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DifficultyCalculator:
    def calculate_4_factor_difficulty(self, word: str, definition: str, etymology: str, frequency: float) -> Dict[str, Any]:
        phonetic_transparency = self._assess_phonetic_transparency(word)
        word_frequency_score = frequency
        morphology_score = self._assess_morphological_complexity(word, definition)
        etymology_score = self._assess_etymological_complexity(etymology)
        
        overall_score = (phonetic_transparency * 0.25 + word_frequency_score * 0.30 + 
                        morphology_score * 0.25 + etymology_score * 0.20)
        
        return {
            'phonetic_transparency_score': phonetic_transparency,
            'word_frequency_score': word_frequency_score,
            'morphology_score': morphology_score,
            'etymology_score': etymology_score,
            'overall_score': overall_score,
            'calculation_method': '4-factor weighted model'
        }
    
    def _assess_phonetic_transparency(self, word: str) -> float:
        if len(word) <= 4: return 1.0
        elif len(word) <= 6: return 1.5
        elif len(word) <= 8: return 2.0
        elif len(word) <= 10: return 2.5
        else: return 3.0
    
    def _assess_morphological_complexity(self, word: str, definition: str) -> float:
        complexity_score = 1.0
        if any(prefix in word.lower() for prefix in ['sub', 'super', 'anti', 'pre', 'post']): complexity_score += 0.5
        if any(suffix in word.lower() for suffix in ['tion', 'sion', 'ness', 'ment', 'able', 'ible']): complexity_score += 0.5
        if len(word) > 10: complexity_score += 0.5
        if 'technical' in definition.lower() or 'scientific' in definition.lower(): complexity_score += 0.5
        return min(complexity_score, 4.0)
    
    def _assess_etymological_complexity(self, etymology: str) -> float:
        if 'Latin' in etymology: return 2.0
        elif 'Greek' in etymology: return 2.5
        elif 'French' in etymology: return 2.3
        elif 'German' in etymology: return 2.0
        elif 'Sanskrit' in etymology: return 3.0
        elif 'multiple' in etymology.lower(): return 3.0
        else: return 1.5

class SpellingBeeProcessor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_172_data = {
            'sugars': {
                'definition': 'Plural of sugar; sweet crystalline substances obtained from various plants, especially sugar cane and sugar beet, used as a sweetener in food and drink. Can also refer to various carbohydrates that provide energy to living organisms.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'SHUG-erz (emphasis on first syllable)',
                'etymology': 'From Old French "sucre," from Latin "saccharum," from Greek "sakkharon"',
                'memory_tips': 'Think of multiple sugar cubes - just add "s" to sugar',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin and French',
                'example_sentence': 'The recipe called for two different types of _____ to achieve the perfect sweetness.'
            },
            'suitable': {
                'definition': 'Right or appropriate for a particular person, purpose, or situation; fitting; proper. Describes something that meets the requirements or standards needed for a specific use or context.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SOOT-uh-buhl (emphasis on first syllable)',
                'etymology': 'From "suit" (to fit) + "-able" suffix meaning "capable of"',
                'memory_tips': 'Think "suit-able" - able to suit the situation',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The candidate\'s experience made her highly _____ for the position.'
            },
            'sukhatankar': {
                'definition': 'A proper noun, likely a surname of Indian origin. In spelling bee contexts, it represents the challenge of spelling unfamiliar proper names that may not follow standard English phonetic patterns.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'soo-KAH-tan-kar (emphasis on second syllable)',
                'etymology': 'Sanskrit origin, likely meaning "happiness" (sukha) combined with a suffix',
                'memory_tips': 'Break into parts: "sukha" (happiness in Sanskrit) + "tankar"',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit',
                'example_sentence': 'The student carefully spelled the surname _____ during the competition.'
            },
            'sulcus': {
                'definition': 'A groove, furrow, or fissure, especially one on the surface of the brain that separates adjacent convolutions. In anatomy, it refers to any linear depression or valley-like structure on a body surface.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUL-kuhs (emphasis on first syllable)',
                'etymology': 'From Latin "sulcus" meaning "furrow" or "groove"',
                'memory_tips': 'Think "sulk-us" - a groove that makes the brain sulk',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The neurosurgeon identified the central _____ of the brain during the examination.'
            },
            'sultana': {
                'definition': 'A small, light-colored, seedless raisin; also the wife or mother of a sultan; a type of pale yellow grape. The term can refer to the dried fruit commonly used in baking or the royal female title.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suhl-TAN-uh (emphasis on second syllable)',
                'etymology': 'From Arabic "sultan" (ruler) with feminine suffix "-a"',
                'memory_tips': 'Think "sultan-a" - the female version of sultan, or a golden raisin',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'The recipe called for a cup of _____ raisins to add sweetness to the bread.'
            },
            'sultanate': {
                'definition': 'The territory ruled by a sultan; the office, position, or dominion of a sultan. Refers to both the geographical area under a sultan\'s control and the institution of sultanic rule.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUL-tuh-nayt (emphasis on first syllable)',
                'etymology': 'From Arabic "sultan" (ruler) + "-ate" suffix indicating office or territory',
                'memory_tips': 'Think "sultan-ate" - the territory that a sultan ate up (conquered)',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'The Ottoman _____ lasted for over six centuries.'
            },
            'sumatran': {
                'definition': 'Of or relating to Sumatra, a large island in western Indonesia. Often used to describe things originating from or characteristic of Sumatra, such as Sumatran tigers or Sumatran coffee.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'soo-MAH-truhn (emphasis on second syllable)',
                'etymology': 'From "Sumatra" (Sanskrit "Swarnadwipa" meaning "island of gold") + "-an" suffix',
                'memory_tips': 'Think "Sumatra-n" - from the island of Sumatra',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit',
                'example_sentence': 'The _____ tiger is critically endangered with fewer than 400 remaining in the wild.'
            },
            'sumerian': {
                'definition': 'Of or relating to ancient Sumer or its people, language, or culture. The Sumerians created one of the world\'s first civilizations in Mesopotamia and developed the earliest known writing system.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'soo-MEER-ee-uhn (emphasis on second syllable)',
                'etymology': 'From "Sumer" (ancient region in Mesopotamia) + "-ian" suffix',
                'memory_tips': 'Think "Sumer-ian" - from ancient Sumer civilization',
                'alternate_spellings': '',
                'language_origin': 'English (from place name)',
                'example_sentence': 'The _____ cuneiform tablets contain some of humanity\'s earliest written records.'
            },
            'summer': {
                'definition': 'The warmest season of the year, occurring between spring and autumn when the sun is highest in the sky. Characterized by long days, warm weather, and in many regions, school vacations.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SUH-mer (emphasis on first syllable)',
                'etymology': 'From Old English "sumor," related to Sanskrit "sama" meaning "season"',
                'memory_tips': 'Think of the sun making everything warmer',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit via Old English',
                'example_sentence': 'The children looked forward to their _____ vacation at the beach.'
            },
            'summit': {
                'definition': 'The highest point of a mountain or hill; the top or apex of something; a meeting between heads of state or other high-ranking officials. Can refer to physical peaks or metaphorical high points.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SUH-mit (emphasis on first syllable)',
                'etymology': 'From Old French "sommet," from Latin "summum" meaning "highest"',
                'memory_tips': 'Think "sum-mit" - the sum of all the climbing effort',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The climbers reached the _____ of Mount Everest after weeks of preparation.'
            },
            'summoned': {
                'definition': 'Past tense of summon; called upon or requested to appear, especially in an official capacity; invoked or called forth through magic or supernatural means; commanded to come.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'SUH-muhnd (emphasis on first syllable)',
                'etymology': 'From Latin "summonere," from "sub" (under) + "monere" (to warn)',
                'memory_tips': 'Think "sum-moned" - called to sum up and appear',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The witness was _____ to appear in court the following Monday.'
            },
            'summoning': {
                'definition': 'The act of calling someone or something to appear; the process of invoking or calling forth, especially through magical means; requesting presence in an official capacity.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'SUH-muh-ning (emphasis on first syllable)',
                'etymology': 'From Latin "summonere," from "sub" (under) + "monere" (to warn)',
                'memory_tips': 'Think "summon-ing" - the ongoing act of calling forth',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The wizard began _____ ancient spirits to aid in the battle.'
            },
            'sumpsimus': {
                'definition': 'A correct expression or reading that is retained instead of a popular but erroneous one; adherence to a correct but unpopular usage. Represents scholarly accuracy over popular misconception.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHMP-si-muhs (emphasis on first syllable)',
                'etymology': 'From Latin, literally "we have taken," used in a story about correct vs. incorrect Latin',
                'memory_tips': 'Think "sump-simus" - we sump up the correct version',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The professor insisted on the _____ despite students preferring the popular incorrect version.'
            },
            'sundae': {
                'definition': 'A dessert consisting of ice cream served in a dish and topped with syrup, nuts, whipped cream, fruit, or other garnishments. A popular frozen treat often served in ice cream parlors.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHN-day (emphasis on first syllable)',
                'etymology': 'Possibly named after Sunday, when it was originally served, or variant spelling to avoid religious association',
                'memory_tips': 'Think "sun-dae" - a sunny day treat, but spelled differently than the day',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'She ordered a hot fudge _____ with extra whipped cream and a cherry on top.'
            },
            'sundar': {
                'definition': 'A name of Sanskrit origin meaning "beautiful" or "handsome." In spelling bee contexts, represents the challenge of spelling names from different cultural backgrounds with specific phonetic patterns.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'SOON-dar (emphasis on first syllable)',
                'etymology': 'From Sanskrit "sundara" meaning "beautiful" or "handsome"',
                'memory_tips': 'Think "sun-dar" - as beautiful as the sun',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit',
                'example_sentence': 'The student spelled the name _____ correctly by remembering its Sanskrit meaning.'
            },
            'sundering': {
                'definition': 'Present participle of sunder; the act of breaking apart, splitting, or separating something that was previously joined; tearing asunder; dividing forcibly or violently.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'SUHN-der-ing (emphasis on first syllable)',
                'etymology': 'From Old English "sundrian," related to "asunder" meaning "apart"',
                'memory_tips': 'Think "sun-dering" - like the sun coming through clouds, splitting them apart',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The earthquake was _____ the earth into deep chasms and crevices.'
            },
            'sundry': {
                'definition': 'Various; several; miscellaneous items of different kinds; diverse or assorted things not specifically categorized. Often used to describe a collection of different small items.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'SUHN-dree (emphasis on first syllable)',
                'etymology': 'From Old English "syndrig" meaning "separate" or "individual"',
                'memory_tips': 'Think "sun-dry" - various things dried in the sun',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The shop sold _____ items including soap, candy, and small tools.'
            },
            'sunflower': {
                'definition': 'A tall plant with large yellow flower heads that turn to face the sun throughout the day; the seeds of this plant, often eaten as snacks or used to produce oil.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHN-flow-er (emphasis on first syllable)',
                'etymology': 'Compound word: "sun" + "flower," named for its sun-following behavior',
                'memory_tips': 'Compound word: sun + flower - a flower that follows the sun',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The giant _____ in the garden grew over ten feet tall this summer.'
            },
            'sunrise': {
                'definition': 'The daily appearance of the sun above the eastern horizon; the time when the sun rises; dawn; the colors and phenomena associated with the sun\'s morning appearance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHN-rahyz (emphasis on first syllable)',
                'etymology': 'Compound word: "sun" + "rise," describing the sun\'s upward movement',
                'memory_tips': 'Compound word: sun + rise - when the sun rises up',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The photographer captured the beautiful _____ over the mountain lake.'
            },
            'sunseeker': {
                'definition': 'A person who seeks out sunny places or warm climates; someone who travels to find sunshine and warmth, especially during colder months; a sun-worshipper.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHN-see-ker (emphasis on first syllable)',
                'etymology': 'Compound word: "sun" + "seeker," one who seeks the sun',
                'memory_tips': 'Compound word: sun + seeker - someone who seeks the sun',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'As a dedicated _____, she spent every winter vacation in tropical destinations.'
            },
            'sunt': {
                'definition': 'Latin word meaning "they are" or "there are"; the third person plural present indicative of the verb "esse" (to be). Used in Latin texts and legal terminology.',
                'part_of_speech': 'verb (Latin)',
                'pronunciation_guide': 'SOONT (rhymes with "hunt")',
                'etymology': 'From Latin "esse" (to be), third person plural present form',
                'memory_tips': 'Think "s-unt" - they are (s for "they" + unt ending)',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The Latin phrase "_____ quod videntur" means "they are what they seem."'
            },
            'superb': {
                'definition': 'Excellent; of very high quality; impressive; magnificent; exceptionally good or outstanding. Used to describe something that exceeds expectations or standards.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'soo-PERB (emphasis on second syllable)',
                'etymology': 'From Latin "superbus" meaning "proud" or "excellent," from "super" (above)',
                'memory_tips': 'Think "super-b" - beyond super, it\'s superb!',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The chef\'s _____ presentation of the dish impressed all the food critics.'
            },
            'supercilious': {
                'definition': 'Behaving or looking as though one thinks oneself superior to others; showing arrogant disdain; condescending; haughty. Characterized by an attitude of superiority and contempt.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'soo-per-SIL-ee-uhs (emphasis on third syllable)',
                'etymology': 'From Latin "superciliosus," from "supercilium" (eyebrow), referring to raised eyebrows',
                'memory_tips': 'Think "super-cilious" - super silly attitude of superiority',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'His _____ attitude toward his coworkers made him unpopular in the office.'
            },
            'superficiality': {
                'definition': 'The quality of being concerned only with surface aspects rather than underlying realities; lack of depth in thought, feeling, or understanding; shallowness; the state of being superficial.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'soo-per-fish-ee-AL-i-tee (emphasis on fifth syllable)',
                'etymology': 'From Latin "superficies" (surface) + "-ality" suffix indicating quality or state',
                'memory_tips': 'Think "super-ficial-ity" - the quality of being only on the surface',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The critic dismissed the novel\'s _____ and lack of meaningful character development.'
            },
            'superhero': {
                'definition': 'A fictional character with extraordinary or superhuman powers who fights against evil and protects people; a person admired for exceptional courage, nobility, or achievements.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SOO-per-hee-roh (emphasis on first syllable)',
                'etymology': 'Compound word: "super" (above, beyond) + "hero" (brave person)',
                'memory_tips': 'Compound word: super + hero - a hero with super powers',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'Every child dreams of being a _____ who can save the world from danger.'
            },
            'superhuman': {
                'definition': 'Having or showing exceptional ability or powers beyond normal human capacity; surpassing ordinary human capabilities; extraordinary; exceeding what is normal for humans.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'soo-per-HYOO-muhn (emphasis on second syllable)',
                'etymology': 'Compound word: "super" (above, beyond) + "human"',
                'memory_tips': 'Compound word: super + human - beyond normal human ability',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The athlete showed _____ strength during the weightlifting competition.'
            },
            'superintendent': {
                'definition': 'A person who supervises or is in charge of an organization, institution, or building; the chief administrator of a school district; a caretaker or manager of an apartment building.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'soo-per-in-TEN-duhnt (emphasis on fourth syllable)',
                'etymology': 'From Latin "superintendere," from "super" (over) + "intendere" (to direct)',
                'memory_tips': 'Think "super-intend-ent" - someone who super-intends (oversees)',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The school _____ announced new policies for the upcoming academic year.'
            },
            'superior': {
                'definition': 'Higher in rank, status, or quality; better than average; excellent; of high quality; more advanced or skilled; a person of higher rank or authority.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'soo-PEER-ee-er (emphasis on second syllable)',
                'etymology': 'From Latin "superior," comparative of "superus" meaning "above"',
                'memory_tips': 'Think "super-ior" - super quality, above others',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The new model showed _____ performance compared to its predecessor.'
            },
            'superlative': {
                'definition': 'Of the highest quality or degree; excellent; in grammar, expressing the highest degree of comparison; an exaggerated or extravagant expression of praise.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'soo-PER-luh-tiv (emphasis on second syllable)',
                'etymology': 'From Latin "superlativus," from "superlatus" meaning "carried above"',
                'memory_tips': 'Think "super-lative" - super praise, the highest level',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The food critic used _____ language to describe the restaurant\'s exceptional cuisine.'
            },
            'superstar': {
                'definition': 'A widely celebrated performer or athlete; a person who has achieved great fame and success in their field; someone who stands out exceptionally among their peers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SOO-per-star (emphasis on first syllable)',
                'etymology': 'Compound word: "super" (exceptional) + "star" (celebrity)',
                'memory_tips': 'Compound word: super + star - a star that\'s super famous',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The young tennis player became a _____ after winning three consecutive championships.'
            },
            'superstitious': {
                'definition': 'Having or showing a belief in superstitions; characterized by irrational fear or reverence for the supernatural; believing in magical thinking or unfounded beliefs about cause and effect.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'soo-per-STISH-uhs (emphasis on third syllable)',
                'etymology': 'From Latin "superstitiosus," from "superstitio" meaning "excessive fear of the gods"',
                'memory_tips': 'Think "super-stitious" - super worried about supernatural things',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She was too _____ to walk under ladders or open umbrellas indoors.'
            },
            'supervises': {
                'definition': 'Third person singular present tense of supervise; watches over and directs the work or performance of others; oversees; manages; monitors to ensure proper execution.',
                'part_of_speech': 'verb (third person singular present)',
                'pronunciation_guide': 'SOO-per-vahy-ziz (emphasis on first syllable)',
                'etymology': 'From Latin "supervisus," from "super" (over) + "videre" (to see)',
                'memory_tips': 'Think "super-vises" - super sees over everything',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The manager _____ a team of twenty employees in the manufacturing department.'
            },
            'supine': {
                'definition': 'Lying face upward; lying on the back; showing a lack of initiative or will; passive; inactive; in grammar, a type of verbal noun in Latin.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'soo-PAHYN (emphasis on second syllable)',
                'etymology': 'From Latin "supinus" meaning "bent backward" or "lying on one\'s back"',
                'memory_tips': 'Think "soup-ine" - lying back like relaxing with soup',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The patient remained in a _____ position during the medical examination.'
            },
            'supper': {
                'definition': 'An evening meal; dinner; the last meal of the day, typically eaten in the evening; in some regions, a light meal eaten late in the evening.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUH-per (emphasis on first syllable)',
                'etymology': 'From Old French "soper," from "supe" meaning "soup," referring to evening soup',
                'memory_tips': 'Think "sup-per" - the meal when you sup (eat) in the evening',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The family gathered around the table for their traditional Sunday _____.'
            },
            'supplicate': {
                'definition': 'To ask humbly and earnestly; to petition respectfully; to make a humble, earnest request or prayer; to beseech or implore with humility.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SUH-pli-kayt (emphasis on first syllable)',
                'etymology': 'From Latin "supplicatus," from "supplex" meaning "kneeling, humble"',
                'memory_tips': 'Think "supply-cate" - asking to supply something you need',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The villagers came to _____ the king for relief from the heavy taxes.'
            },
            'supremacy': {
                'definition': 'The state of being supreme; ultimate authority or power; the condition of being superior to others in authority, power, or status; dominance or preeminence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'soo-PREM-uh-see (emphasis on second syllable)',
                'etymology': 'From Latin "supremus" (highest) + "-acy" suffix indicating state or quality',
                'memory_tips': 'Think "supreme-acy" - the state of being supreme',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The empire maintained its naval _____ for several centuries.'
            },
            'surcease': {
                'definition': 'An end or cessation; a stop or pause; relief from something unpleasant; the action of stopping or coming to an end; archaic term for ending or conclusion.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ser-SEES (emphasis on second syllable)',
                'etymology': 'From Old French "sursis," from Latin "supersedere" meaning "to sit above, refrain"',
                'memory_tips': 'Think "sure-cease" - sure to cease, definitely stopping',
                'alternate_spellings': '',
                'language_origin': 'Latin via French',
                'example_sentence': 'The refugees longed for _____ from their suffering and hardship.'
            },
            'surcharge': {
                'definition': 'An additional charge or payment on top of the usual amount; an extra fee; to impose an additional charge; an overcharge or excessive burden.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SER-chahrj (emphasis on first syllable)',
                'etymology': 'From French "surcharge," from "sur" (over) + "charge" (load, burden)',
                'memory_tips': 'Think "sur-charge" - an extra charge over the normal charge',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The airline added a fuel _____ to all ticket prices during the energy crisis.'
            },
            'sure': {
                'definition': 'Confident in what one thinks or knows; having no doubt; certain; reliable; trustworthy; definitely going to happen; secure or stable.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'SHUR (rhymes with "pure")',
                'etymology': 'From Old French "sur," from Latin "securus" meaning "secure, safe"',
                'memory_tips': 'Think of being secure in your knowledge - you\'re sure',
                'alternate_spellings': '',
                'language_origin': 'Latin via French',
                'example_sentence': 'She was _____ that she had locked the door before leaving the house.'
            },
            'surefire': {
                'definition': 'Certain to succeed; guaranteed to work; reliable; foolproof; bound to achieve the intended result; having a high probability of success.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SHUR-fahyr (emphasis on first syllable)',
                'etymology': 'Compound word: "sure" (certain) + "fire" (from firearms that fire reliably)',
                'memory_tips': 'Compound word: sure + fire - certain as a gun that fires reliably',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'His grandmother\'s recipe was a _____ way to impress dinner guests.'
            },
            'surety': {
                'definition': 'A formal guarantee or pledge; certainty; confidence; a person who takes responsibility for another\'s debt or obligation; security given for the fulfillment of an undertaking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SHUR-i-tee (emphasis on first syllable)',
                'etymology': 'From Old French "sureté," from Latin "securitas" meaning "security"',
                'memory_tips': 'Think "sure-ty" - the quality of being sure, a guarantee',
                'alternate_spellings': '',
                'language_origin': 'Latin via French',
                'example_sentence': 'The bank required a _____ before approving the large business loan.'
            },
            'surface': {
                'definition': 'The outside part or uppermost layer of something; the top or face of an object; to come to the top of water; to emerge; to become apparent or known.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SER-fis (emphasis on first syllable)',
                'etymology': 'From French "surface," from "sur" (above) + "face" (face)',
                'memory_tips': 'Think "sur-face" - the face that\'s on top',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The submarine rose to the _____ of the ocean after completing its mission.'
            },
            'surfactant': {
                'definition': 'A substance that reduces surface tension between two liquids or between a liquid and a solid; a compound that helps substances mix that normally don\'t combine, such as oil and water.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ser-FAK-tuhnt (emphasis on second syllable)',
                'etymology': 'Blend of "surface" + "active" + "-ant" suffix indicating agent',
                'memory_tips': 'Think "surf-act-ant" - acts on surfaces to reduce tension',
                'alternate_spellings': '',
                'language_origin': 'English (coined term)',
                'example_sentence': 'Soap works as a _____ to help water wash away grease and oil.'
            },
            'surfeit': {
                'definition': 'An excessive amount of something; overabundance; the state of being fed or supplied to excess; to supply with too much; to overfeed or oversupply.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SER-fit (emphasis on first syllable)',
                'etymology': 'From Old French "surfait," from "sur" (over) + "fait" (done)',
                'memory_tips': 'Think "surf-eit" - surfing on too much of something',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'After the holidays, many people experience a _____ of rich food and sweets.'
            },
            'surgeon': {
                'definition': 'A medical doctor who specializes in performing surgical operations; a physician trained to treat diseases, injuries, and deformities by cutting into the body and manipulating or removing organs and tissues.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SER-juhn (emphasis on first syllable)',
                'etymology': 'From Old French "surgien," from "cirurgie" (surgery), from Greek "kheirourgia" (hand-work)',
                'memory_tips': 'Think "surg-eon" - one who does surgery',
                'alternate_spellings': '',
                'language_origin': 'Greek via French',
                'example_sentence': 'The skilled _____ successfully removed the patient\'s appendix in a two-hour operation.'
            },
            'surimi': {
                'definition': 'A paste made from fish that has been deboned, washed, and pureed; processed seafood product often used to make imitation crab meat; a Japanese culinary preparation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'soo-REE-mee (emphasis on second syllable)',
                'etymology': 'From Japanese "surimi," from "suru" (to grind) + "mi" (meat)',
                'memory_tips': 'Think "sure-me" - Japanese ground fish, sure it\'s meat',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'The California roll contained _____ instead of real crab meat.'
            },
            'surly': {
                'definition': 'Bad-tempered and unfriendly; rude; gruff; showing a tendency to be uncooperative or hostile; churlish; displaying an unfriendly or threatening manner.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SER-lee (emphasis on first syllable)',
                'etymology': 'From Middle English "sirly," originally meaning "lordly," later became "arrogant, rude"',
                'memory_tips': 'Think "sure-ly" grumpy - surely in a bad mood',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The _____ waiter barely acknowledged the customers and seemed annoyed by their questions.'
            },
            'surlyw': {
                'definition': '[POTENTIAL ERROR] This appears to be a misspelling or variant of "surly." If this is an intentional variant, it would mean bad-tempered and unfriendly, similar to surly.',
                'part_of_speech': 'error/variant',
                'pronunciation_guide': 'SER-lee-w (if pronounced as written)',
                'etymology': 'Possible variant or error of "surly"',
                'memory_tips': 'This may be a spelling error - check if it should be "surly"',
                'alternate_spellings': 'surly',
                'language_origin': 'English (variant/error)',
                'example_sentence': 'The word _____ may be a variant spelling that needs verification.'
            },
            'surmised': {
                'definition': 'Past tense of surmise; guessed or inferred something without certain proof; supposed or concluded based on incomplete evidence; formed an opinion based on available clues.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'ser-MAHYZD (emphasis on second syllable)',
                'etymology': 'From Old French "surmise," from "sur" (upon) + "mis" (put, placed)',
                'memory_tips': 'Think "sur-mised" - placed upon what you think might be true',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The detective _____ that the crime had been committed by someone familiar with the building.'
            },
            'surmountable': {
                'definition': 'Able to be overcome or conquered; capable of being climbed over or passed; possible to deal with successfully; not insurmountable; achievable despite difficulties.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ser-MOUN-tuh-buhl (emphasis on second syllable)',
                'etymology': 'From "surmount" (to overcome) + "-able" suffix meaning "capable of"',
                'memory_tips': 'Think "sur-mount-able" - able to mount over and conquer',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'Despite the challenges, the team believed their goals were _____ with hard work and determination.'
            }
        }
        
        return batch_172_data.get(word, {
            'definition': f'[WORD NOT FOUND: {word}] This word was not found in the comprehensive data set.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'[PRONUNCIATION NOT AVAILABLE FOR {word.upper()}]',
            'etymology': f'[ETYMOLOGY NOT AVAILABLE FOR {word}]',
            'memory_tips': f'[MEMORY TIPS NOT AVAILABLE FOR {word}]',
            'alternate_spellings': '',
            'language_origin': 'unknown',
            'example_sentence': f'The word _____ requires further research for proper definition.'
        })

    def detect_combined_words(self, word: str) -> bool:
        combined_word_indicators = [
            len(word) > 15,  # Unusually long
            word.count('tion') > 1,  # Multiple common endings
            word.count('ing') > 1,
            word.count('ed') > 1,
            'lw' in word,  # Unusual letter combination suggesting error
        ]
        
        known_combined_errors = [
            'surlyw'  # Appears to be surly + w
        ]
        
        return any(combined_word_indicators) or word in known_combined_errors

    def process_batch_172(self):
        input_file = 'output/batch_172_words.csv'
        output_file = 'output/batch_172_processed.csv'
        
        logging.info("Processing Batch 172 with comprehensive Claude data...")
        
        # Read input CSV
        df = pd.read_csv(input_file)
        processed_words = []
        successful_count = 0
        failed_count = 0
        combined_errors = []
        
        for _, row in df.iterrows():
            word = row['word']
            
            try:
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Detect combined word errors
                is_combined = self.detect_combined_words(word)
                if is_combined:
                    combined_errors.append(f"{word}: Combined word error")
                
                # Extract source information
                source_difficulties = row['source_difficulties']
                years = row['years']
                
                # Map source difficulty to frequency score
                frequency_map = {"One Bee": 1.0, "Two Bee": 2.0, "Three Bee": 3.0}
                frequency_scores = [frequency_map.get(diff.strip(), 2.0) for diff in source_difficulties.split(';')]
                avg_frequency = sum(frequency_scores) / len(frequency_scores)
                
                # Calculate 4-factor difficulty but leave final difficulty assignments null
                difficulty_data = self.difficulty_calc.calculate_4_factor_difficulty(
                    word, claude_data['definition'], claude_data['etymology'], avg_frequency
                )
                
                processed_word = {
                    'word': word,
                    'definition': claude_data['definition'],
                    'example_sentence': claude_data['example_sentence'],
                    'source_difficulty': source_difficulties,
                    'difficulty_level': '',  # Leave null as requested
                    'difficulty_name': '',   # Leave null as requested
                    'ai_difficulty_level': '',  # Leave null as requested
                    'ai_difficulty_name': '',   # Leave null as requested
                    'phonetic_transparency_score': difficulty_data['phonetic_transparency_score'],
                    'word_frequency_score': difficulty_data['word_frequency_score'],
                    'morphology_score': difficulty_data['morphology_score'],
                    'etymology_score': difficulty_data['etymology_score'],
                    'difficulty_calculation_method': f"{difficulty_data['calculation_method']} (overall_score: {difficulty_data['overall_score']:.2f})",
                    'part_of_speech': claude_data['part_of_speech'],
                    'pronunciation_guide': claude_data['pronunciation_guide'],
                    'etymology': claude_data['etymology'],
                    'etymology_source': 'Claude',
                    'memory_tips': claude_data['memory_tips'],
                    'alternate_spellings': claude_data['alternate_spellings'],
                    'language_origin': claude_data['language_origin'],
                    'definition_source': 'Claude',
                    'source_names': 'Scripps National Spelling Bee',
                    'source_difficulties': source_difficulties,
                    'frequency': avg_frequency,
                    'original_source': f'Scripps National Spelling Bee Words of the Champions ({years})',
                    'source_access_date': '2025-08-19'
                }
                
                processed_words.append(processed_word)
                successful_count += 1
                logging.info(f"Processed word: {word}")
                
            except Exception as e:
                logging.error(f"Error processing word '{word}': {str(e)}")
                failed_count += 1
        
        # Save to CSV
        output_df = pd.DataFrame(processed_words)
        output_df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
        
        logging.info(f"Saved {len(processed_words)} words to {output_file}")
        logging.info("Batch 172 processing completed!")
        logging.info(f"Processed {successful_count} words with comprehensive Claude data")
        logging.info(f"Output saved to: {output_file}")
        logging.info(f"Results: {successful_count} successful, {failed_count} failed")
        logging.info(f"Combined word errors detected and flagged: {len(combined_errors)}")
        
        if combined_errors:
            logging.info("Combined word errors flagged:")
            for error in combined_errors:
                logging.info(f"  - {error}")

if __name__ == "__main__":
    processor = SpellingBeeProcessor()
    processor.process_batch_172()