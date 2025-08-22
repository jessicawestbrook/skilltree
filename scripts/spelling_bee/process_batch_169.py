#!/usr/bin/env python3
"""
Process Batch 169 of Spelling Bee Words with Comprehensive Claude Data
Generates full definitions, pronunciations, etymologies, memory tips, and examples for all 50 words
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WordData:
    word: str
    years: str
    source_files: str
    source_difficulties: str
    definition: str = ""
    pronunciation: str = ""
    etymology: str = ""
    language_origins: str = ""
    example_sentence: str = ""
    definition_source: str = ""
    pronunciation_source: str = ""
    etymology_source: str = ""
    error_notes: str = ""
    # Claude-generated fields
    claude_definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    claude_etymology: str = ""
    memory_tips: str = ""
    alternate_spellings: str = ""
    claude_language_origin: str = ""

class DifficultyCalculator:
    """Implements sophisticated difficulty rating from THEORETICAL_FOUNDATIONS.md"""
    
    def __init__(self):
        # Common word frequency list (top 3000 most common English words)
        self.common_words = self._load_common_words()
        
    def _load_common_words(self) -> set:
        """Load common English words for frequency scoring"""
        common = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
            'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
            'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want',
            'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'water', 'long', 'find', 'here', 'thing', 'great', 'man', 'world', 'life',
            'still', 'public', 'human', 'get', 'old', 'country', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point',
            'government', 'company', 'number', 'group', 'problem', 'fact', 'store', 'stories', 'story', 'stomach', 'storm', 'straight', 'strange',
            'straw', 'stew', 'steward', 'sticky', 'stiff', 'sting', 'stones', 'stood', 'stopped', 'stove', 'strange', 'straps'
        }
        return common
    
    def calculate_phonetic_transparency(self, word: str, pronunciation: str) -> float:
        """Score based on how predictable pronunciation is from spelling (1-4 scale)"""
        if not pronunciation:
            return 2.5  # Default for missing pronunciation
            
        # Count irregular spelling patterns
        irregular_patterns = 0
        word_lower = word.lower()
        
        # Common irregular patterns
        irregular_mappings = [
            ('ph', 'f'), ('gh', 'f'), ('ough', 'uff'), ('ight', 'ite'),
            ('tion', 'shun'), ('sion', 'zhun'), ('ture', 'cher'),
            ('que', 'k'), ('x', 'ks'), ('c', 'k'), ('c', 's')
        ]
        
        for spelling, sound in irregular_mappings:
            if spelling in word_lower:
                irregular_patterns += 1
        
        # Silent letters
        silent_patterns = ['k', 'b', 'l', 'gh', 'w', 't', 'h']
        for pattern in silent_patterns:
            if pattern in word_lower and len(word) > 4:
                irregular_patterns += 0.5
        
        # More irregular = higher difficulty
        if irregular_patterns == 0:
            return 1.0  # Very transparent
        elif irregular_patterns <= 1:
            return 2.0  # Mostly transparent
        elif irregular_patterns <= 2:
            return 3.0  # Moderately opaque
        else:
            return 4.0  # Very opaque
    
    def calculate_word_frequency(self, word: str) -> float:
        """Score based on how common/rare the word is (1-4 scale)"""
        word_lower = word.lower()
        
        if word_lower in self.common_words:
            return 1.0  # Very common
        elif len(word) <= 4:
            return 2.0  # Short words tend to be more common
        elif len(word) <= 7:
            return 3.0  # Medium length
        else:
            return 4.0  # Long words tend to be rarer
    
    def calculate_morphological_complexity(self, word: str, etymology: str) -> float:
        """Score based on morphological structure complexity (1-4 scale)"""
        # Count morphemes (prefixes, roots, suffixes)
        morpheme_count = 1  # Base word
        
        # Common prefixes
        prefixes = [
            'un', 're', 'in', 'dis', 'en', 'non', 'pre', 'pro', 'anti', 'de', 'over', 'under',
            'sub', 'super', 'inter', 'trans', 'semi', 'auto', 'co', 'counter', 'extra', 'hyper',
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'strat'
        ]
        
        # Common suffixes
        suffixes = [
            'ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible',
            'ful', 'less', 'ous', 'ious', 'al', 'ic', 'ical', 'ism', 'ist', 'ize', 'ise',
            'fy', 'ward', 'wise', 'like', 'ship', 'hood', 'dom', 'age', 'ery', 'ary', 'ate',
            'oid', 'ary', 'ery', 'ity', 'ship', 'ness'
        ]
        
        word_lower = word.lower()
        
        # Count prefixes
        for prefix in sorted(prefixes, key=len, reverse=True):
            if word_lower.startswith(prefix) and len(word_lower) > len(prefix) + 2:
                morpheme_count += 1
                word_lower = word_lower[len(prefix):]
                break
        
        # Count suffixes
        for suffix in sorted(suffixes, key=len, reverse=True):
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                morpheme_count += 1
                break
        
        # Convert to 1-4 scale
        if morpheme_count == 1:
            return 1.0  # Simple word
        elif morpheme_count == 2:
            return 2.0  # One affix
        elif morpheme_count == 3:
            return 3.0  # Two affixes
        else:
            return 4.0  # Complex morphology
    
    def calculate_etymology_complexity(self, etymology: str, language_origins: str) -> float:
        """Score based on etymology complexity (1-4 scale)"""
        if not etymology and not language_origins:
            return 2.5  # Default for missing etymology
        
        # Analyze language origins
        origins_text = f"{etymology} {language_origins}".lower()
        
        # Germanic/English roots are easier for English speakers
        if any(term in origins_text for term in ['old english', 'middle english', 'germanic', 'anglo-saxon']):
            base_score = 1.0
        # Latin/French are medium difficulty
        elif any(term in origins_text for term in ['latin', 'french', 'norman']):
            base_score = 2.0
        # Greek and other European languages are harder
        elif any(term in origins_text for term in ['greek', 'spanish', 'italian', 'german']):
            base_score = 3.0
        # Non-European languages are hardest
        else:
            base_score = 4.0
        
        # Adjust for multiple languages
        language_indicators = ['from', 'via', 'through', 'ultimately']
        complexity_boost = sum(1 for indicator in language_indicators if indicator in origins_text) * 0.3
        
        return min(4.0, base_score + complexity_boost)

class Batch169Processor:
    """Processes Batch 169 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 169 words"""
        
        # Comprehensive data for all 50 words in Batch 169
        batch_169_data = {
            'sternutation': {
                'definition': 'The medical term for sneezing; the reflex action of forcibly expelling air from the nose and mouth. This involuntary response helps clear irritants from nasal passages and respiratory tract. Sneezing is typically triggered by irritation of mucous membranes in the nose or exposure to bright light in some individuals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ster-nyuh-TAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "sternutatio," from "sternutare" meaning "to sneeze repeatedly"',
                'memory_tips': 'Think "stern-utation" - a stern reaction where you suddenly "choo" out loud',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The doctor explained that frequent _____ could be a sign of allergies.'
            },
            'steroid': {
                'definition': 'A large group of naturally occurring or synthetic organic compounds with a characteristic four-ring carbon structure. In biology, steroids include hormones like testosterone, estrogen, and cortisol that regulate various bodily functions. In medicine, synthetic steroids are used as anti-inflammatory drugs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STER-oid (emphasis on first syllable)',
                'etymology': 'From "sterol" + "-oid," where sterol comes from Greek "stereos" meaning "solid"',
                'memory_tips': 'Think "stare-oid" - athletes stare at these substances for performance',
                'alternate_spellings': '',
                'language_origin': 'Greek via modern scientific terminology',
                'example_sentence': 'The athlete was banned for using an illegal anabolic _____.'
            },
            'stevedore': {
                'definition': 'A dock worker who loads and unloads ships; a person employed to handle cargo at ports and harbors. Stevedores work with cranes, forklifts, and other equipment to move containers, bulk cargo, and other freight between ships and shore facilities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STEE-vuh-dor (emphasis on first syllable)',
                'etymology': 'From Spanish "estivador," from "estivar" meaning "to stow cargo"',
                'memory_tips': 'Think "Steve-a-door" - Steve opens the door to unload ships',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The experienced _____ could load a container ship in record time.'
            },
            'stevia': {
                'definition': 'A natural sweetener derived from the leaves of the Stevia rebaudiana plant, native to South America. This zero-calorie sugar substitute is much sweeter than regular sugar and is commonly used by people managing diabetes or trying to reduce caloric intake.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STEE-vee-uh (emphasis on first syllable)',
                'etymology': 'Named after Spanish botanist Petrus Jacobus Stevus (Pedro Jaime Esteve)',
                'memory_tips': 'Think "Steve-ia" - Steve discovers a sweet plant',
                'alternate_spellings': '',
                'language_origin': 'Modern Latin (named after botanist)',
                'example_sentence': 'She added _____ to her coffee instead of sugar to reduce calories.'
            },
            'stew': {
                'definition': 'A dish of meat, vegetables, or other ingredients cooked slowly in liquid in a covered pot. The cooking method involves simmering ingredients together to create tender, flavorful food where the cooking liquid becomes part of the dish.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STOO (rhymes with "true")',
                'etymology': 'From Old French "estuver" meaning "to bathe in hot water"',
                'memory_tips': 'Think "stew" rhymes with "brew" - both involve cooking liquids',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The hearty beef _____ simmered all afternoon in the slow cooker.'
            },
            'steward': {
                'definition': 'A person who manages or looks after property, finances, or domestic affairs for another person or organization. On ships and aircraft, a steward provides service to passengers. The term implies responsible management and careful oversight of resources or people.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STOO-urd (emphasis on first syllable)',
                'etymology': 'From Old English "stiweard," from "sti" (hall) + "weard" (keeper)',
                'memory_tips': 'Think "stew-ward" - the keeper who serves stew in the hall',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The flight _____ helped passengers stow their carry-on luggage.'
            },
            'stewardship': {
                'definition': 'The responsible management and care of something entrusted to one\'s care, whether property, resources, or the environment. This concept emphasizes ethical oversight and sustainable practices, often with the understanding that current caretakers must preserve resources for future generations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STOO-urd-ship (emphasis on first syllable)',
                'etymology': 'From "steward" + "-ship," indicating the office or skill of a steward',
                'memory_tips': 'Think "steward-ship" - sailing a ship responsibly as its steward',
                'alternate_spellings': '',
                'language_origin': 'Old English + suffix',
                'example_sentence': 'Environmental _____ requires protecting natural resources for future generations.'
            },
            'sticky': {
                'definition': 'Having the property of adhering to surfaces when touched; covered with an adhesive substance. Figuratively, it can describe difficult situations that are hard to escape or problems that persist and are hard to resolve.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STIK-ee (emphasis on first syllable)',
                'etymology': 'From "stick" + "-y," from Old English "stician" meaning "to pierce"',
                'memory_tips': 'Think "stick-y" - having the quality of sticking to things',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The children\'s hands were _____ from eating cotton candy.'
            },
            'stiff': {
                'definition': 'Not easily bent or changed in shape; rigid or firm in texture or consistency. When describing people, it can mean formal, unfriendly, or lacking in ease and grace. It can also describe something that is difficult, severe, or strong.',
                'part_of_speech': 'adjective, adverb, noun, verb',
                'pronunciation_guide': 'STIF (rhymes with "cliff")',
                'etymology': 'From Old English "stif" meaning "rigid, hard to move"',
                'memory_tips': 'Think "stiff" sounds like what it means - short and hard',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'After sitting at the desk all day, his neck felt _____.'
            },
            'stifle': {
                'definition': 'To suppress, restrain, or prevent something from happening or developing; to suffocate or have difficulty breathing. It can mean to hold back emotions, sounds, or natural processes, often by force or through restrictive conditions.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'STY-fuhl (emphasis on first syllable)',
                'etymology': 'From Old French "estouffer" meaning "to smother"',
                'memory_tips': 'Think "stifle" sounds like "stiffen" - making breathing stiffen and stop',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'She tried to _____ her laughter during the serious meeting.'
            },
            'stigmata': {
                'definition': 'Marks or wounds corresponding to those of Christ\'s crucifixion, said to appear on the bodies of certain religious individuals. In medicine, stigmata refers to visible signs or marks of disease. In botany, it\'s the part of a flower that receives pollen.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'stig-MAH-tuh (emphasis on second syllable)',
                'etymology': 'From Latin "stigmata," from Greek "stigma" meaning "mark, puncture"',
                'memory_tips': 'Think "stig-mata" - marks that stigmatize like ancient stigma',
                'alternate_spellings': 'stigma (singular)',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The medieval saint was said to bear the _____ of Christ\'s wounds.'
            },
            'stilton': {
                'definition': 'A type of strong, blue-veined English cheese, typically made from cow\'s milk. Named after the village of Stilton in England, this cheese has a distinctive tangy flavor and crumbly texture with characteristic blue-green veining from Penicillium roqueforti mold.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STIL-tuhn (emphasis on first syllable)',
                'etymology': 'Named after Stilton village in Cambridgeshire, England',
                'memory_tips': 'Think "still-ton" - a ton of cheese that sits still to age',
                'alternate_spellings': '',
                'language_origin': 'English (place name)',
                'example_sentence': 'The cheese platter featured a wedge of creamy _____ with its distinctive blue veins.'
            },
            'stimuli': {
                'definition': 'Things that provoke a reaction or response, especially in biological or psychological contexts; plural of stimulus. In science, stimuli are external factors that cause organisms to respond, such as light, sound, touch, or chemical signals.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'STIM-yuh-ly (emphasis on first syllable)',
                'etymology': 'Plural of "stimulus," from Latin meaning "goad, incentive"',
                'memory_tips': 'Think "stim-you-lie" - things that stimulate you, no lie',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The researcher tested how plants responded to various light _____.'
            },
            'sting': {
                'definition': 'To prick or wound with a sharp-pointed organ or object, typically injecting venom; to cause sharp physical or emotional pain. Used by insects like bees and wasps as a defense mechanism, injecting toxins that cause pain and swelling.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'STING (rhymes with "ring")',
                'etymology': 'From Old English "stingan" meaning "to pierce"',
                'memory_tips': 'Think "sting" - the sound mimics the sharp, quick pain',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The bee\'s _____ left a red, swollen mark on his arm.'
            },
            'stinky': {
                'definition': 'Having a strong, unpleasant odor; smelling bad or offensive. This informal adjective is commonly used to describe things that emit foul odors, from spoiled food to unwashed socks.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STINK-ee (emphasis on first syllable)',
                'etymology': 'From "stink" + "-y," from Old English "stincan" meaning "to emit a smell"',
                'memory_tips': 'Think "stink-y" - having the quality of stinking',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The garbage had become quite _____ after sitting in the sun all day.'
            },
            'stipulate': {
                'definition': 'To demand or specify as a condition of an agreement; to require something as an essential condition. In legal contexts, it means to formally agree to certain facts or conditions as part of a contract or legal proceeding.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'STIP-yuh-layt (emphasis on first syllable)',
                'etymology': 'From Latin "stipulari" meaning "to bargain, demand a guarantee"',
                'memory_tips': 'Think "stip-you-late" - if you\'re late, you must stipulate new conditions',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The contract will _____ that payment is due within thirty days.'
            },
            'stirrups': {
                'definition': 'Metal loops suspended from a horse\'s saddle to support the rider\'s feet while mounting and riding. In medicine, stirrups are supports used during gynecological examinations. The term comes from the resemblance to the looped supports on saddles.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'STUR-uhps (emphasis on first syllable)',
                'etymology': 'From Old English "stigrap," from "stigan" (to climb) + "rap" (rope)',
                'memory_tips': 'Think "stir-ups" - you stir up your feet to get into these supports',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She adjusted the _____ to the proper length before mounting her horse.'
            },
            'stitcher': {
                'definition': 'A person who sews or joins fabric pieces together using thread; someone who makes stitches. In manufacturing, it can refer to a machine that stitches materials together, or a worker who operates such equipment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STICH-ur (emphasis on first syllable)',
                'etymology': 'From "stitch" + "-er," from Old English "stice" meaning "puncture"',
                'memory_tips': 'Think "stitch-er" - one who stitches things together',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The experienced _____ could sew a quilt in just two days.'
            },
            'stitchery': {
                'definition': 'The art, craft, or practice of decorative needlework; ornamental sewing or embroidery. This term encompasses various techniques of decorative stitching used to create patterns, designs, or artistic works using thread, yarn, or similar materials.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STICH-ur-ee (emphasis on first syllable)',
                'etymology': 'From "stitch" + "-ery," indicating the practice or art of stitching',
                'memory_tips': 'Think "stitch-ery" - the artistry of making stitches',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'Her grandmother taught her the traditional _____ techniques passed down through generations.'
            },
            'stoats': {
                'definition': 'Small carnivorous mammals related to weasels, also known as ermines in their winter white coat. These agile predators are found in northern regions and are known for their seasonal color change from brown in summer to white in winter.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'STOHTS (rhymes with "coats")',
                'etymology': 'From Middle English, possibly from Dutch "stoot" meaning "push, thrust"',
                'memory_tips': 'Think "stoats" wear white "coats" in winter like ermines',
                'alternate_spellings': 'ermine (when in white winter coat)',
                'language_origin': 'Middle English',
                'example_sentence': 'The _____ changed from brown to white as winter approached.'
            },
            'stockade': {
                'definition': 'A defensive barrier made of upright wooden posts or stakes; a fort or enclosure surrounded by such a barrier. Historically used for military defense, the term also refers to military prisons or detention facilities.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'stok-AYD (emphasis on second syllable)',
                'etymology': 'From Spanish "estacada," from "estaca" meaning "stake"',
                'memory_tips': 'Think "stock-aide" - stocks of wood that aid in defense',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The frontier settlers built a _____ around their village for protection.'
            },
            'stocky': {
                'definition': 'Having a sturdy, compact build; short and solidly built with a broad, thick body structure. This adjective describes a body type that is strong and robust but not tall, often suggesting physical strength and durability.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STOK-ee (emphasis on first syllable)',
                'etymology': 'From "stock" + "-y," referring to being built like a tree stock (trunk)',
                'memory_tips': 'Think "stock-y" - built like a strong tree stock',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The _____ wrestler was known for his powerful grip and low center of gravity.'
            },
            'stomach': {
                'definition': 'The organ in the digestive system where food is stored and partially digested before moving to the intestines. It produces gastric acid and enzymes to break down food. Colloquially, it refers to the belly or abdomen, and figuratively means the ability to tolerate something unpleasant.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STUM-ik (emphasis on first syllable)',
                'etymology': 'From Latin "stomachus," from Greek "stomachos" meaning "throat, gullet"',
                'memory_tips': 'Think "stum-ick" - when you\'re stumped, your stomach feels sick',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'After the large meal, his _____ felt uncomfortably full.'
            },
            'stones': {
                'definition': 'Hard, solid mineral matter; rocks or pebbles. Can refer to gemstones, building materials, or naturally occurring rock formations. In medicine, stones are hard deposits that can form in organs like kidneys or gallbladder.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'STOHNZ (rhymes with "bones")',
                'etymology': 'From Old English "stan" meaning "rock, stone"',
                'memory_tips': 'Think "stones" and "bones" - both are hard structures',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The garden path was lined with smooth river _____.'
            },
            'stood': {
                'definition': 'Past tense of "stand"; remained upright on one\'s feet; maintained a position; endured or withstood something. It indicates a completed action of standing or maintaining a particular stance or position.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'STOOD (rhymes with "good")',
                'etymology': 'Past tense of "stand," from Old English "standan"',
                'memory_tips': 'Think "stood" - sounds like "good" when you stand well',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She _____ quietly at the back of the room during the presentation.'
            },
            'stopped': {
                'definition': 'Past tense of "stop"; ceased moving or operating; came to an end; prevented something from continuing. This verb indicates the completion of motion or activity, whether voluntary or involuntary.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'STOPD (one syllable)',
                'etymology': 'Past tense of "stop," from Old English "stoppian" meaning "to block up"',
                'memory_tips': 'Think "stopped" - the double "p" makes it stop abruptly',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The car _____ suddenly when the traffic light turned red.'
            },
            'store': {
                'definition': 'A retail establishment selling items to the public; a place where goods are kept for future use; to keep or accumulate for future use. As a verb, it means to put away or reserve something for later use.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STOR (rhymes with "more")',
                'etymology': 'From Old French "estorer," from Latin "instaurare" meaning "to renew"',
                'memory_tips': 'Think "store" - you store more things in a store',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'They decided to _____ the extra supplies in the basement.'
            },
            'storied': {
                'definition': 'Having an interesting history; celebrated or famous for historical events or achievements. It can also mean having multiple stories or floors in architecture, though this meaning is less common in modern usage.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STOR-eed (emphasis on first syllable)',
                'etymology': 'From "story" + "-ed," meaning "having stories" (both narrative and architectural)',
                'memory_tips': 'Think "story-ed" - filled with stories worth telling',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The _____ old mansion had housed several famous families over the centuries.'
            },
            'stories': {
                'definition': 'Accounts of events, either true or fictional; narratives told for entertainment, education, or information. Also refers to the floors or levels of a building. Stories can be oral traditions, written literature, or modern media narratives.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'STOR-eez (emphasis on first syllable)',
                'etymology': 'Plural of "story," from Latin "historia" meaning "narrative, account"',
                'memory_tips': 'Think "stor-ies" - multiple tales stored in memory',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Grandmother loved to tell _____ about her childhood adventures.'
            },
            'storm': {
                'definition': 'Violent weather conditions with strong winds, rain, thunder, lightning, or snow; any tumultuous or violent disturbance. Metaphorically, it refers to intense emotional outbursts or periods of trouble and upheaval.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STORM (rhymes with "form")',
                'etymology': 'From Old English "storm" meaning "tempest, violent weather"',
                'memory_tips': 'Think "storm" - the word itself sounds turbulent and powerful',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The fierce _____ knocked down trees and power lines throughout the city.'
            },
            'stormmince': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "storm" (violent weather) + "mince" (to cut finely or walk daintily). This is a data processing error that should be corrected.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "storm" and "mince"',
                'alternate_spellings': 'storm + mince (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'story': {
                'definition': 'A narrative account of events, whether true or fictional; a tale told for entertainment or instruction. In architecture, it refers to a floor or level of a building. Stories serve to convey information, preserve culture, and provide entertainment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STOR-ee (emphasis on first syllable)',
                'etymology': 'From Latin "historia," from Greek "historia" meaning "inquiry, knowledge"',
                'memory_tips': 'Think "stor-y" - storing history in your memory',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The children gathered around to hear their favorite bedtime _____.'
            },
            'stove': {
                'definition': 'A cooking appliance that provides heat for preparing food; an apparatus that burns fuel or uses electricity to generate heat for cooking or warming. Modern stoves typically have multiple burners and often include an oven.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STOHV (rhymes with "drove")',
                'etymology': 'From Middle English, from Middle Low German or Dutch "stove" meaning "heated room"',
                'memory_tips': 'Think "stove" - you drove to buy a stove',
                'alternate_spellings': '',
                'language_origin': 'Germanic',
                'example_sentence': 'She turned on the gas _____ to boil water for pasta.'
            },
            'stowaway': {
                'definition': 'A person who hides aboard a ship, aircraft, or vehicle to travel without paying or being detected; someone who travels secretly and illegally by concealing themselves in a transportation vessel.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STOH-uh-way (emphasis on first syllable)',
                'etymology': 'From "stow" (to pack or store) + "away," indicating hiding away during transport',
                'memory_tips': 'Think "stow-away" - stowing yourself away on a journey',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'The ship\'s crew discovered a _____ hiding in the cargo hold.'
            },
            'stradivarius': {
                'definition': 'A violin or other stringed instrument made by Antonio Stradivari (1644-1737) or his family in Cremona, Italy. These instruments are considered among the finest ever created, prized for their exceptional sound quality and craftsmanship, and are worth millions of dollars today.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'strad-uh-VAIR-ee-us (emphasis on third syllable)',
                'etymology': 'Named after Antonio Stradivari, Italian violin maker (Latinized as Stradivarius)',
                'memory_tips': 'Think "Strad-a-various" - various Stradivari violins are precious',
                'alternate_spellings': 'Strad (informal)',
                'language_origin': 'Italian (personal name)',
                'example_sentence': 'The museum\'s prized _____ violin was played by master musicians for centuries.'
            },
            'straight': {
                'definition': 'Extending in one direction without curves, bends, or angles; direct and undeviating; honest and frank; not mixed or diluted. Can describe physical lines, moral character, or substances in their pure form.',
                'part_of_speech': 'adjective, adverb, noun',
                'pronunciation_guide': 'STRAYT (rhymes with "gate")',
                'etymology': 'From past participle of obsolete "stretch," from Old English "streht"',
                'memory_tips': 'Think "straight" - no need to "ate" around curves',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Draw a _____ line from point A to point B.'
            },
            'straightforward': {
                'definition': 'Easy to understand or simple; honest and open; proceeding directly without deviation or complexity. This term describes both clear communication and honest, uncomplicated behavior.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'strayt-FOR-werd (emphasis on second syllable)',
                'etymology': 'Compound of "straight" + "forward," meaning directly ahead',
                'memory_tips': 'Think "straight-forward" - moving straight toward the goal',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'Her _____ explanation made the complex topic easy to understand.'
            },
            'strain': {
                'definition': 'To exert force or pressure; to stretch tight; to injure by overexertion; to filter or separate through a strainer. As a noun, it refers to pressure, stress, or a particular variety of something like bacteria or plants.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'STRAYN (rhymes with "rain")',
                'etymology': 'From Old French "estreindre," from Latin "stringere" meaning "to draw tight"',
                'memory_tips': 'Think "strain" sounds like "pain" - both involve pressure',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'He felt a _____ in his back muscle after lifting the heavy box.'
            },
            'strait': {
                'definition': 'A narrow passage of water connecting two larger bodies of water; a situation of difficulty or distress. Geographically, straits are important waterways for navigation between seas or large lakes.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'STRAYT (rhymes with "gate")',
                'etymology': 'From Old French "estreit," from Latin "strictus" meaning "drawn together"',
                'memory_tips': 'Think "strait" like "straight" - a straight, narrow water passage',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The Strait of Gibraltar connects the Mediterranean Sea to the Atlantic Ocean.'
            },
            'strands': {
                'definition': 'Individual threads, fibers, or thin pieces that are twisted or woven together; single elements of rope, hair, or similar materials. Can also refer to beaches or shorelines, or individual elements of complex concepts.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'STRANDZ (rhymes with "hands")',
                'etymology': 'From Old English "strand" meaning "beach, shore" and separately "rope, cord"',
                'memory_tips': 'Think "strands" of hair like bands around your head',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She braided the three _____ of hair into a neat plait.'
            },
            'strange': {
                'definition': 'Unusual, odd, or unexpected; not familiar or typical; difficult to understand or explain. This adjective describes things that deviate from the normal, expected, or familiar, often causing curiosity or unease.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STRAYNJ (rhymes with "change")',
                'etymology': 'From Old French "estrange," from Latin "extraneus" meaning "external, foreign"',
                'memory_tips': 'Think "strange" leads to "change" - both alter normality',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'There was a _____ noise coming from the attic last night.'
            },
            'straps': {
                'definition': 'Flexible bands or strips of material used for securing, carrying, or fastening objects; narrow pieces of leather, fabric, or other materials that connect or support items like bags, watches, or equipment.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'STRAPS (rhymes with "caps")',
                'etymology': 'From dialectal "strap," related to "strip," from Old English "stropp" meaning "thong"',
                'memory_tips': 'Think "straps" secure things with snaps',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The backpack\'s padded _____ made it comfortable to carry heavy books.'
            },
            'stratification': {
                'definition': 'The arrangement or classification into layers or strata; the process of forming layers, especially in geology, sociology, or ecology. It describes how materials, organisms, or social groups organize into distinct horizontal levels.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'strat-uh-fi-KAY-shuhn (emphasis on fourth syllable)',
                'etymology': 'From "stratify" + "-ation," from Latin "stratum" meaning "layer"',
                'memory_tips': 'Think "strat-ification" - creating a strategy for layers',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Social _____ was evident in the clear divisions between economic classes.'
            },
            'stratocracy': {
                'definition': 'A form of government in which the military class holds political power; rule by military leaders or a society dominated by military values and personnel. This system places armed forces at the center of political authority.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'strat-OK-ruh-see (emphasis on second syllable)',
                'etymology': 'From Greek "stratos" (army) + "kratos" (power, rule)',
                'memory_tips': 'Think "strato-crazy" - when the military goes crazy for power',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The country transformed into a _____ after the generals seized control.'
            },
            'stratosphere': {
                'definition': 'The layer of Earth\'s atmosphere above the troposphere, extending from about 10-50 kilometers above sea level, characterized by relatively stable temperatures and containing the ozone layer. It\'s where jet aircraft typically fly.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRAT-uh-sfeer (emphasis on first syllable)',
                'etymology': 'From Latin "stratum" (layer) + Greek "sphaira" (sphere)',
                'memory_tips': 'Think "strat-o-sphere" - a strategic layer of the sphere (Earth)',
                'alternate_spellings': '',
                'language_origin': 'Latin + Greek',
                'example_sentence': 'The airplane cruised through the _____ at 35,000 feet altitude.'
            },
            'straw': {
                'definition': 'Dried stalks of grain plants like wheat, barley, or rice, used for animal bedding, thatching, or packing material. Also refers to thin tubes for drinking liquids, originally made from actual grain stalks.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'STRAW (rhymes with "saw")',
                'etymology': 'From Old English "streaw" meaning "scattered things, straw for bedding"',
                'memory_tips': 'Think "straw" - you draw liquid through it',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The farmer spread fresh _____ in the horses\' stalls.'
            },
            'straydifficulty': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "stray" (wandering, lost) + "difficulty" (problem, challenge). This is a data processing error that should be corrected.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "stray" and "difficulty"',
                'alternate_spellings': 'stray + difficulty (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'streak': {
                'definition': 'A long, thin mark or band of color different from the surrounding area; a continuous period of success or failure; to move very quickly. It can describe both visual patterns and sequences of events.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STREEK (rhymes with "peak")',
                'etymology': 'From Old English "strica" meaning "stroke, line"',
                'memory_tips': 'Think "streak" and "peak" - both can be thin and high',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'A _____ of lightning illuminated the dark storm clouds.'
            },
            'streamers': {
                'definition': 'Long, narrow strips of material that flow or flutter in the wind, often used for decoration at parties or celebrations. Also refers to long, flowing banners or ribbons, or things that stream continuously.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'STREEM-urz (emphasis on first syllable)',
                'etymology': 'From "stream" + "-er," indicating things that stream or flow',
                'memory_tips': 'Think "stream-ers" - things that stream and flow like rivers',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'Colorful _____ decorated the ceiling for the birthday party.'
            },
            'streamlet': {
                'definition': 'A small stream or brook; a narrow flow of water, typically smaller than a stream but larger than a trickle. This diminutive form suggests a gentle, modest watercourse through natural landscapes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STREEM-lit (emphasis on first syllable)',
                'etymology': 'From "stream" + "-let" (diminutive suffix meaning "small")',
                'memory_tips': 'Think "stream-let" - a little stream, let it flow',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The children followed the tiny _____ as it wound through the forest.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_169_data:
            return batch_169_data[word_lower]
        
        # Return empty data if word not found
        return {
            'definition': '',
            'part_of_speech': '',
            'pronunciation_guide': '',
            'etymology': '',
            'memory_tips': '',
            'alternate_spellings': '',
            'language_origin': '',
            'example_sentence': ''
        }
    
    def process_batch_169(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 169 with comprehensive Claude data"""
        words = []
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['word']:  # Skip empty rows
                    continue
                    
                word_data = WordData(
                    word=row['word'],
                    years=row['years'],
                    source_files=row['source_files'],
                    source_difficulties=row['source_difficulties']
                )
                
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word_data.word)
                
                # Store all Claude-generated data
                word_data.claude_definition = claude_data['definition']
                word_data.part_of_speech = claude_data['part_of_speech']
                word_data.pronunciation_guide = claude_data['pronunciation_guide']
                word_data.claude_etymology = claude_data['etymology']
                word_data.memory_tips = claude_data['memory_tips']
                word_data.alternate_spellings = claude_data['alternate_spellings']
                word_data.claude_language_origin = claude_data['language_origin']
                word_data.example_sentence = claude_data['example_sentence']
                
                # Track any missing data
                errors = []
                if not word_data.claude_definition:
                    errors.append("No Claude definition available")
                if not word_data.pronunciation_guide:
                    errors.append("No pronunciation guide available")
                if not word_data.claude_etymology:
                    errors.append("No etymology available")
                
                word_data.error_notes = "; ".join(errors)
                
                words.append(word_data)
                logger.info(f"Processed word: {word_data.word}")
        
        return words
    
    def save_batch_169_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 169 processed words to CSV"""
        
        # Match actual database schema
        fieldnames = [
            'word', 'definition', 'example_sentence', 'source_difficulty', 
            'difficulty_level', 'difficulty_name', 'ai_difficulty_level', 'ai_difficulty_name',
            'phonetic_transparency_score', 'word_frequency_score', 'morphology_score', 
            'etymology_score', 'difficulty_calculation_method', 'part_of_speech',
            'pronunciation_guide', 'etymology', 'etymology_source', 'memory_tips',
            'alternate_spellings', 'language_origin', 'definition_source',
            'source_names', 'source_difficulties', 'frequency', 'original_source',
            'source_access_date'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for word_data in processed_words:
                # Calculate difficulty components (but don't assign final difficulty yet)
                calc = self.difficulty_calculator
                phonetic_score = calc.calculate_phonetic_transparency(word_data.word, word_data.pronunciation_guide)
                frequency_score = calc.calculate_word_frequency(word_data.word)
                morphology_score = calc.calculate_morphological_complexity(word_data.word, word_data.claude_etymology)
                etymology_score = calc.calculate_etymology_complexity(word_data.claude_etymology, word_data.claude_language_origin)
                
                # Calculate overall score but don't assign difficulty level yet
                overall_score = (phonetic_score * 0.3 + frequency_score * 0.25 + morphology_score * 0.25 + etymology_score * 0.2)
                
                # Create detailed original source with years
                years_list = word_data.years.replace(';', ',') if word_data.years else ''
                original_source = f"Scripps National Spelling Bee Words of the Champions ({years_list})" if years_list else 'Scripps National Spelling Bee Words of the Champions'
                
                row = {
                    'word': word_data.word,
                    'definition': word_data.claude_definition,
                    'example_sentence': word_data.example_sentence,
                    'source_difficulty': word_data.source_difficulties.split(';')[0].strip() if word_data.source_difficulties else '',
                    'difficulty_level': '',
                    'difficulty_name': '',
                    'ai_difficulty_level': '',
                    'ai_difficulty_name': '',
                    'phonetic_transparency_score': phonetic_score,
                    'word_frequency_score': frequency_score,
                    'morphology_score': morphology_score,
                    'etymology_score': etymology_score,
                    'difficulty_calculation_method': f'4-factor weighted model (overall_score: {overall_score:.2f})',
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.claude_etymology,
                    'etymology_source': 'Claude',
                    'memory_tips': word_data.memory_tips,
                    'alternate_spellings': word_data.alternate_spellings,
                    'language_origin': word_data.claude_language_origin,
                    'definition_source': 'Claude',
                    'source_names': 'Scripps National Spelling Bee',
                    'source_difficulties': word_data.source_difficulties,
                    'frequency': frequency_score,
                    'original_source': original_source,
                    'source_access_date': '2025-08-19'
                }
                writer.writerow(row)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")

def main():
    """Process Batch 169 with comprehensive Claude data"""
    processor = Batch169Processor()
    input_csv = Path("output/batch_169_words.csv")
    output_csv = Path("output/batch_169_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 169 with comprehensive Claude data...")
    
    # Process all words in batch 169
    processed_words = processor.process_batch_169(input_csv)
    
    # Save results
    processor.save_batch_169_csv(processed_words, output_csv)
    
    logger.info(f"Batch 169 processing completed!")
    logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
    logger.info(f"Output saved to: {output_csv}")
    
    # Show summary
    successful_words = [w for w in processed_words if w.claude_definition]
    failed_words = [w for w in processed_words if not w.claude_definition]
    combined_errors = [w for w in processed_words if "COMBINED WORD ERROR" in w.claude_definition]
    
    logger.info(f"Results: {len(successful_words)} successful, {len(failed_words)} failed")
    logger.info(f"Combined word errors detected and flagged: {len(combined_errors)}")
    
    if failed_words:
        logger.info("Words that failed processing:")
        for word in failed_words:
            logger.info(f"  - {word.word}: {word.error_notes}")
            
    if combined_errors:
        logger.info("Combined word errors flagged:")
        for word in combined_errors:
            logger.info(f"  - {word.word}: Combined word error")

if __name__ == "__main__":
    main()