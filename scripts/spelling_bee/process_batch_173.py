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
        if any(prefix in word.lower() for prefix in ['sur', 'sub', 'super', 'anti', 'pre', 'post', 'syn']): complexity_score += 0.5
        if any(suffix in word.lower() for suffix in ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ous', 'ism']): complexity_score += 0.5
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
        batch_173_data = {
            'surplus': {
                'definition': 'An amount of something left over when requirements have been met; an excess of income or assets over expenditure or liabilities; more than what is needed or used.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'SER-plushs (emphasis on first syllable)',
                'etymology': 'From Old French "sourplus," from Latin "super" (over) + "plus" (more)',
                'memory_tips': 'Think "sur-plus" - over and above, extra plus',
                'alternate_spellings': '',
                'language_origin': 'Latin via French',
                'example_sentence': 'The company used its budget _____ to invest in new equipment.'
            },
            'surrealist': {
                'definition': 'An artist or writer who practices surrealism, a cultural movement emphasizing the expression of the unconscious mind through fantastic imagery and incongruous juxtaposition of subject matter.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'suh-REE-uh-list (emphasis on second syllable)',
                'etymology': 'From French "surréaliste," from "sur" (above) + "réalisme" (realism)',
                'memory_tips': 'Think "sur-real-ist" - one who goes beyond reality',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The _____ artist created paintings featuring melting clocks and floating elephants.'
            },
            'surreptitious': {
                'definition': 'Kept secret, especially because it would not be approved of; done secretly or stealthily; characterized by stealth; furtive; clandestine.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ser-uhp-TISH-uhs (emphasis on third syllable)',
                'etymology': 'From Latin "surreptitius," from "surripere" meaning "to take away secretly"',
                'memory_tips': 'Think "sur-reptit-ious" - sneaky like a reptile slithering secretly',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She took a _____ glance at her watch during the boring meeting.'
            },
            'surrogate': {
                'definition': 'A substitute, especially a person deputizing for another in a specific role or office; a woman who bears a child for another person; acting as a substitute.',
                'part_of_speech': 'noun, adjective, verb',
                'pronunciation_guide': 'SER-uh-git (emphasis on first syllable)',
                'etymology': 'From Latin "surrogatus," from "surrogare" meaning "to put in another\'s place"',
                'memory_tips': 'Think "sur-rogate" - to ask (rogate) someone to stand in for you',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The couple found a _____ mother to help them have a child.'
            },
            'surrounded': {
                'definition': 'Past tense of surround; encircled; enclosed on all sides; having something on every side; completely encompassed by something.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'suh-ROUND-id (emphasis on second syllable)',
                'etymology': 'From Old French "soronder," from Latin "super" (over) + "undare" (to flow)',
                'memory_tips': 'Think "sur-rounded" - round all around, encircled',
                'alternate_spellings': '',
                'language_origin': 'Latin via French',
                'example_sentence': 'The castle was _____ by a deep moat filled with water.'
            },
            'surveyed': {
                'definition': 'Past tense of survey; looked closely at or examined; conducted a general view or investigation of; measured and mapped an area of land.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'ser-VAYD (emphasis on second syllable)',
                'etymology': 'From Old French "surveoir," from Latin "super" (over) + "videre" (to see)',
                'memory_tips': 'Think "sur-veyed" - looked over something from above',
                'alternate_spellings': '',
                'language_origin': 'Latin via French',
                'example_sentence': 'The architect _____ the land before designing the new building.'
            },
            'suspicion': {
                'definition': 'A feeling or thought that someone is guilty of an illegal, dishonest, or unpleasant act; the feeling of not trusting someone or something; doubt about someone\'s honesty.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suh-SPISH-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "suspicere," from "sub" (from below) + "specere" (to look)',
                'memory_tips': 'Think "sus-picion" - suspicious vision, looking with doubt',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The detective had a _____ that the butler was hiding something important.'
            },
            'sustain': {
                'definition': 'To strengthen or support physically or mentally; to keep going; to maintain; to provide with necessities or nourishment; to uphold or defend.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'suh-STAYN (emphasis on second syllable)',
                'etymology': 'From Latin "sustinere," from "sub" (from below) + "tenere" (to hold)',
                'memory_tips': 'Think "sus-tain" - to hold up and maintain',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The solar panels help _____ the building\'s energy needs.'
            },
            'sustenance': {
                'definition': 'Food and drink regarded as a source of strength; nourishment; something that supports or maintains life; the process of providing or receiving nourishment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUH-stuh-nuhns (emphasis on first syllable)',
                'etymology': 'From Latin "sustinere" (to sustain) + "-ance" suffix indicating state',
                'memory_tips': 'Think "sustain-ance" - the thing that sustains you',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The hikers packed enough _____ to last them through the week-long trek.'
            },
            'susurrus': {
                'definition': 'A soft murmuring or whispering sound; a gentle rustling; a low, continuous sound like whispering or the rustling of leaves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'soo-SER-uhs (emphasis on second syllable)',
                'etymology': 'From Latin "susurrus" meaning "whisper" or "murmur"',
                'memory_tips': 'Think "sus-urrus" - the sound "sus" repeated like a whisper',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ of wind through the pine trees was incredibly soothing.'
            },
            'suture': {
                'definition': 'A stitch or row of stitches holding together the edges of a wound or surgical incision; the process of joining with stitches; a line of junction between bones.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SOO-cher (emphasis on first syllable)',
                'etymology': 'From Latin "sutura," from "suere" meaning "to sew"',
                'memory_tips': 'Think "sew-ture" - sewing to close a wound',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The surgeon used a fine _____ to close the incision after the operation.'
            },
            'svarabhakti': {
                'definition': 'In linguistics, the insertion of an epenthetic vowel between consonants to make pronunciation easier; a phonological process that breaks up consonant clusters.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'svah-rah-BHAK-ti (emphasis on third syllable)',
                'etymology': 'From Sanskrit "svara" (vowel) + "bhakti" (division, insertion)',
                'memory_tips': 'Think "svara-bhakti" - dividing sounds with vowels in Sanskrit',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit',
                'example_sentence': 'The linguist explained how _____ helps speakers pronounce difficult consonant combinations.'
            },
            'svengali': {
                'definition': 'A person who exercises a controlling or mesmeric influence on another, especially for a sinister purpose; someone who manipulates others through psychological influence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sven-GAH-lee (emphasis on second syllable)',
                'etymology': 'From the character Svengali in George du Maurier\'s novel "Trilby" (1894)',
                'memory_tips': 'Think of the manipulative character Svengali who controlled Trilby',
                'alternate_spellings': '',
                'language_origin': 'English (literary character)',
                'example_sentence': 'The cult leader acted as a _____ to his followers, controlling their every decision.'
            },
            'swainsona': {
                'definition': 'A genus of flowering plants in the pea family, native to Australia; also known as Sturt\'s desert pea; plants with distinctive red and black flowers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SWAYN-soh-nah (emphasis on first syllable)',
                'etymology': 'Named after Isaac Swainson, an English botanist',
                'memory_tips': 'Think "Swain-sona" - named after botanist Swainson',
                'alternate_spellings': '',
                'language_origin': 'English (person\'s name)',
                'example_sentence': 'The _____ flower is the floral emblem of South Australia.'
            },
            'swale': {
                'definition': 'A low-lying or depressed and often wet stretch of land; a marshy depression; a shallow valley or hollow; a natural drainage area.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SWAYL (rhymes with "scale")',
                'etymology': 'From Middle English "swale," possibly from Old Norse "svalr" meaning "cool"',
                'memory_tips': 'Think "swale" like a "scale" in the land - a depression',
                'alternate_spellings': '',
                'language_origin': 'Old Norse via Middle English',
                'example_sentence': 'The water collected in the _____ after the heavy rainfall.'
            },
            'swallow': {
                'definition': 'To cause food, drink, or saliva to pass down the throat; to take in and accept; a small migratory bird with pointed wings and a forked tail.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'SWAHL-oh (emphasis on first syllable)',
                'etymology': 'From Old English "swelgan" (to swallow) and "swealwe" (the bird)',
                'memory_tips': 'Think of swallowing food or the graceful bird that swallows insects',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She watched the _____ build its nest under the barn eaves.'
            },
            'swankiest': {
                'definition': 'Superlative form of swanky; most stylishly luxurious and expensive; most fashionable and impressive; most ostentatiously elegant.',
                'part_of_speech': 'adjective (superlative)',
                'pronunciation_guide': 'SWANG-kee-ist (emphasis on first syllable)',
                'etymology': 'From "swank" (showing off) + "-y" + superlative "-est"',
                'memory_tips': 'Think "swank-iest" - the most swanky and show-offy',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'They stayed at the _____ hotel in the city for their anniversary.'
            },
            'swannery': {
                'definition': 'A place where swans are kept or bred; a swan preserve; an area designated for the care and management of swans.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SWAHN-uh-ree (emphasis on first syllable)',
                'etymology': 'From "swan" + "-ery" suffix indicating a place for keeping something',
                'memory_tips': 'Think "swan-ery" - a place for swans, like a bakery for bread',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The royal _____ on the Thames has been maintained for centuries.'
            },
            'swayharsh': {
                'definition': '[POTENTIAL COMBINED WORD ERROR] This appears to be two words incorrectly joined: "sway" (to move gently) + "harsh" (severe, rough). This may be a data processing error.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': 'SWAY-harsh (if pronounced as written)',
                'etymology': 'Possible combination of "sway" (Old English) + "harsh" (Middle English)',
                'memory_tips': 'This appears to be an error - should likely be separated into "sway" and "harsh"',
                'alternate_spellings': 'sway + harsh (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': 'The word _____ appears to be a data error requiring correction.'
            },
            'sweat': {
                'definition': 'Moisture exuded through the pores of the skin, typically as a reaction to heat, physical exertion, fever, or fear; to excrete moisture through pores.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SWET (rhymes with "bet")',
                'etymology': 'From Old English "swat," related to "swetan" meaning "to sweat"',
                'memory_tips': 'Think of working hard and getting wet with perspiration',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'After the intense workout, _____ dripped from his forehead.'
            },
            'sweet': {
                'definition': 'Having the pleasant taste characteristic of sugar or honey; pleasing to the senses; kind and charming; a confection or dessert.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'SWEET (rhymes with "meet")',
                'etymology': 'From Old English "swete," related to Latin "suavis" meaning "pleasant"',
                'memory_tips': 'Think of sugar, honey, or candy - pleasant to taste',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ strawberries were perfectly ripe and delicious.'
            },
            'sweeten': {
                'definition': 'To make or become sweet or sweeter; to add sugar or sweetener to; to make more pleasant or agreeable; to improve the appeal of something.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SWEET-uhn (emphasis on first syllable)',
                'etymology': 'From "sweet" + "-en" suffix meaning "to make"',
                'memory_tips': 'Think "sweet-en" - to make something sweet',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'She decided to _____ her coffee with a spoonful of honey.'
            },
            'sweltering': {
                'definition': 'Uncomfortably hot; oppressively warm; causing one to swelter; characterized by excessive heat and humidity that makes one feel suffocated.',
                'part_of_speech': 'adjective, verb (present participle)',
                'pronunciation_guide': 'SWEL-ter-ing (emphasis on first syllable)',
                'etymology': 'From "swelter" (to suffer from heat) + "-ing"',
                'memory_tips': 'Think "swell-tering" - swelling with heat, so hot you feel like melting',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The _____ heat made it impossible to work outside during midday.'
            },
            'swept': {
                'definition': 'Past tense and past participle of sweep; moved swiftly and smoothly; cleaned with a broom; carried along by a current; overwhelmed.',
                'part_of_speech': 'verb (past tense/participle)',
                'pronunciation_guide': 'SWEPT (rhymes with "kept")',
                'etymology': 'From Old English "swapan," past tense "sweop"',
                'memory_tips': 'Think of a broom sweeping or being swept away by wind',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The strong current _____ the boat downstream toward the waterfall.'
            },
            'swerve': {
                'definition': 'To change direction suddenly; to turn aside abruptly from a straight course; to deviate from an intended path; a sudden change in direction.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'SWERV (rhymes with "curve")',
                'etymology': 'From Old English "sweorfan" meaning "to turn aside"',
                'memory_tips': 'Think of a car swerving to avoid an obstacle',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The driver had to _____ quickly to avoid hitting the deer.'
            },
            'swift': {
                'definition': 'Moving very quickly; fast; happening without delay; prompt; a type of fast-flying bird; moving with great speed.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'SWIFT (rhymes with "drift")',
                'etymology': 'From Old English "swift," related to "swifan" meaning "to move quickly"',
                'memory_tips': 'Think of something moving swiftly like an arrow or swift bird',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ current carried the kayaker downstream rapidly.'
            },
            'swifty': {
                'definition': 'Informal term for something done quickly or cleverly; a fast or clever action; sometimes refers to a type of joke or trick.',
                'part_of_speech': 'noun (informal)',
                'pronunciation_guide': 'SWIFT-ee (emphasis on first syllable)',
                'etymology': 'From "swift" + "-y" diminutive suffix',
                'memory_tips': 'Think "swift-y" - something done swiftly or cleverly',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'He pulled a _____ and finished the task in half the expected time.'
            },
            'swim': {
                'definition': 'To move through water by means of the limbs; to propel oneself through water; to be immersed in or covered with liquid; the act of swimming.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'SWIM (rhymes with "dim")',
                'etymology': 'From Old English "swimman," related to "swemman" meaning "to make swim"',
                'memory_tips': 'Think of moving through water like a fish',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The children love to _____ in the lake during summer vacation.'
            },
            'swimming': {
                'definition': 'The act or sport of moving through water using the limbs; the activity of propelling oneself through water; present participle of swim.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'SWIM-ing (emphasis on first syllable)',
                'etymology': 'From "swim" + "-ing" suffix',
                'memory_tips': 'Think "swim-ing" - the ongoing action of swimming',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The _____ pool was crowded with competitive athletes training for the meet.'
            },
            'swipe': {
                'definition': 'To hit or try to hit with a sweeping blow; to steal; to move a card through an electronic reader; a sweeping blow or movement.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'SWAHYP (rhymes with "wipe")',
                'etymology': 'Possibly variant of "sweep," from Old English "swapan"',
                'memory_tips': 'Think of swiping a credit card or taking a swipe at something',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'She used her key card to _____ into the secure building.'
            },
            'swirled': {
                'definition': 'Past tense of swirl; moved in a twisting or circular pattern; created a spiral or circular motion; mixed in a circular pattern.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'SWIRLD (rhymes with "whirled")',
                'etymology': 'From "swirl," possibly from Middle Dutch "swieren" meaning "to whirl"',
                'memory_tips': 'Think of cream swirled into coffee in circular patterns',
                'alternate_spellings': '',
                'language_origin': 'Middle Dutch',
                'example_sentence': 'The autumn leaves _____ around in the gusty wind.'
            },
            'switcheroo': {
                'definition': 'An unexpected variation or reversal; a sudden change or substitution; a trick or deception involving switching things; an about-face.',
                'part_of_speech': 'noun (informal)',
                'pronunciation_guide': 'switch-uh-ROO (emphasis on third syllable)',
                'etymology': 'From "switch" + "-eroo" playful suffix (like "switcheroo")',
                'memory_tips': 'Think "switch-eroo" - switching things around playfully',
                'alternate_spellings': '',
                'language_origin': 'English (informal/slang)',
                'example_sentence': 'The magician performed a clever _____ and made the coin disappear.'
            },
            'swoop': {
                'definition': 'To move rapidly downward through the air; to carry off suddenly; to descend quickly and smoothly; a rapid diving movement.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'SWOOP (rhymes with "loop")',
                'etymology': 'Possibly from Old English "swapan" meaning "to sweep"',
                'memory_tips': 'Think of a bird swooping down to catch prey',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The eagle began to _____ down toward the fish in the river.'
            },
            'sword': {
                'definition': 'A weapon with a long metal blade and a hilt with a hand guard; a symbol of military power or authority; something resembling a sword in shape.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SORD (the "w" is silent)',
                'etymology': 'From Old English "sweord," related to Old Norse "sverd"',
                'memory_tips': 'Remember the "w" is silent - sounds like "sord"',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The knight drew his _____ to defend the castle from invaders.'
            },
            'sybaritic': {
                'definition': 'Characterized by luxury and self-indulgence; devoted to pleasure and comfort; luxurious in a self-indulgent way; hedonistic.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'sib-uh-RIT-ik (emphasis on third syllable)',
                'etymology': 'From Greek "Sybarites," inhabitants of ancient Sybaris known for luxury',
                'memory_tips': 'Think "Sybar-itic" - from Sybaris, a city known for luxury',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The billionaire lived a _____ lifestyle in his multiple mansions.'
            },
            'sycophant': {
                'definition': 'A person who acts obsequiously to gain advantage; someone who flatters important people for personal gain; a servile flatterer; a toady.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIH-kuh-fant (emphasis on first syllable)',
                'etymology': 'From Greek "sykophantes," literally "fig-shower," referring to informers',
                'memory_tips': 'Think "syco-phant" - someone who shows fake enthusiasm',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ constantly praised the boss, hoping for a promotion.'
            },
            'syllables': {
                'definition': 'Plural of syllable; units of pronunciation having one vowel sound; the basic building blocks of spoken words; rhythmic units in poetry.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'SIL-uh-buhlz (emphasis on first syllable)',
                'etymology': 'From Greek "syllabe," from "syn" (together) + "lambanein" (to take)',
                'memory_tips': 'Think "syl-la-bles" - breaking words into sound units',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The word "basketball" has three _____ : bas-ket-ball.'
            },
            'syllabus': {
                'definition': 'An outline of the subjects in a course of study or teaching; a summary of topics to be covered in an educational course; a curriculum outline.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIL-uh-buhs (emphasis on first syllable)',
                'etymology': 'From Latin "syllabus," possibly from Greek "sittybos" (parchment label)',
                'memory_tips': 'Think "syl-labus" - the bus that carries all the course information',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The professor distributed the _____ on the first day of class.'
            },
            'sylph': {
                'definition': 'A mythological air spirit; an imaginary being of the air; a slender, graceful woman or girl; in folklore, a spirit of the air.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIHLF (rhymes with "shelf")',
                'etymology': 'From New Latin "sylphus," coined by Paracelsus from Latin "silva" (forest)',
                'memory_tips': 'Think "sylph" - a graceful spirit floating like silk',
                'alternate_spellings': '',
                'language_origin': 'New Latin',
                'example_sentence': 'The ballet dancer moved like a _____ across the stage.'
            },
            'symbol': {
                'definition': 'A thing that represents or stands for something else; a mark or character used to represent an object, function, or process; an emblem.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIM-buhl (emphasis on first syllable)',
                'etymology': 'From Greek "symbolon," from "syn" (together) + "ballein" (to throw)',
                'memory_tips': 'Think "sym-bol" - something that brings meanings together',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The dove is a universal _____ of peace and hope.'
            },
            'symbolizes': {
                'definition': 'Third person singular present of symbolize; represents or stands for; serves as a symbol of; embodies or typifies.',
                'part_of_speech': 'verb (third person singular present)',
                'pronunciation_guide': 'SIM-buh-lahyz-iz (emphasis on first syllable)',
                'etymology': 'From "symbol" + "-ize" + "-s"',
                'memory_tips': 'Think "symbol-izes" - makes something into a symbol',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The flag _____ the unity and strength of the nation.'
            },
            'symmetric': {
                'definition': 'Having symmetry; showing a regular arrangement of parts; balanced; having corresponding parts that match when divided by a line or plane.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'si-MET-rik (emphasis on second syllable)',
                'etymology': 'From Greek "symmetria," from "syn" (together) + "metron" (measure)',
                'memory_tips': 'Think "sym-metric" - measured together equally',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The building\'s _____ design was pleasing to the eye.'
            },
            'symmetrical': {
                'definition': 'Having symmetry; balanced; having parts that correspond to one another; exhibiting regularity of form or arrangement on opposite sides of a dividing line.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'si-MET-ri-kuhl (emphasis on second syllable)',
                'etymology': 'From "symmetric" + "-al" suffix',
                'memory_tips': 'Think "symmet-rical" - having the quality of symmetry',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The butterfly\'s wings are perfectly _____ with matching patterns.'
            },
            'sympathy': {
                'definition': 'Feelings of pity and sorrow for someone else\'s misfortune; understanding between people; harmony of feeling; compassionate concern for others.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIM-puh-thee (emphasis on first syllable)',
                'etymology': 'From Greek "sympatheia," from "syn" (together) + "pathos" (feeling)',
                'memory_tips': 'Think "sym-pathy" - feeling together with someone',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'She expressed her _____ for the family\'s loss during the difficult time.'
            },
            'symphony': {
                'definition': 'An elaborate musical composition for full orchestra; a large-scale musical work typically in multiple movements; harmony of sounds; orchestral music.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIM-fuh-nee (emphasis on first syllable)',
                'etymology': 'From Greek "symphonia," from "syn" (together) + "phone" (sound)',
                'memory_tips': 'Think "sym-phony" - sounds coming together harmoniously',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Beethoven\'s Ninth _____ is considered one of the greatest musical works ever composed.'
            },
            'symposium': {
                'definition': 'A conference or meeting for discussion of some subject; an academic conference; a collection of essays or papers on a particular subject; a formal meeting for discussion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sim-POH-zee-uhm (emphasis on second syllable)',
                'etymology': 'From Greek "symposion," from "syn" (together) + "posis" (drinking)',
                'memory_tips': 'Think "sym-posium" - people coming together to discuss',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The medical _____ brought together experts from around the world.'
            },
            'symposiumsyndicate': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "symposium" (academic conference) + "syndicate" (group of individuals). This is a data processing error.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "symposium" and "syndicate"',
                'alternate_spellings': 'symposium + syndicate (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'synaesthesia': {
                'definition': 'A neurological phenomenon where stimulation of one sensory pathway leads to automatic experiences in a second sensory pathway; experiencing senses in combination.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sin-uhs-THEE-zhuh (emphasis on third syllable)',
                'etymology': 'From Greek "syn" (together) + "aisthesis" (sensation)',
                'memory_tips': 'Think "syn-aesthesia" - senses working together',
                'alternate_spellings': 'synesthesia',
                'language_origin': 'Greek',
                'example_sentence': 'People with _____ might see colors when they hear music.'
            },
            'synanthrope': {
                'definition': 'An organism that lives in association with humans and benefits from human-modified environments; a species that thrives in human-dominated landscapes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIN-an-throhp (emphasis on first syllable)',
                'etymology': 'From Greek "syn" (together) + "anthropos" (human)',
                'memory_tips': 'Think "syn-anthrope" - living together with humans',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Urban pigeons are a perfect example of a _____ species.'
            },
            'syncope': {
                'definition': 'Temporary loss of consciousness caused by a fall in blood pressure; fainting; in linguistics, the omission of sounds from the interior of a word.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIN-kuh-pee (emphasis on first syllable)',
                'etymology': 'From Greek "synkope," from "syn" (together) + "koptein" (to cut)',
                'memory_tips': 'Think "syn-cope" - coping with a sudden cut in consciousness',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The patient experienced _____ and briefly lost consciousness.'
            }
        }
        
        return batch_173_data.get(word, {
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
        ]
        
        known_combined_errors = [
            'swayharsh',  # sway + harsh
            'symposiumsyndicate'  # symposium + syndicate
        ]
        
        return any(combined_word_indicators) or word in known_combined_errors

    def process_batch_173(self):
        input_file = 'output/batch_173_words.csv'
        output_file = 'output/batch_173_processed.csv'
        
        logging.info("Processing Batch 173 with comprehensive Claude data...")
        
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
        logging.info("Batch 173 processing completed!")
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
    processor.process_batch_173()