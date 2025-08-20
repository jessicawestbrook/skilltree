#!/usr/bin/env python3

import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Any
import re

@dataclass
class WordData:
    word: str
    years: str
    source_files: str
    source_difficulties: str
    
    # Comprehensive Claude data fields
    definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    language_origins: str = ""
    example_sentence: str = ""
    memory_tip: str = ""
    phonetic_transparency: float = None
    word_frequency: float = None
    morphological_complexity: float = None
    etymology_complexity: float = None
    final_difficulty: str = None

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word: str) -> float:
        transparent_patterns = ['th', 'ch', 'sh', 'ph']
        score = 0.5
        for pattern in transparent_patterns:
            if pattern in word.lower():
                score += 0.1
        return min(score, 1.0)
    
    @staticmethod
    def calculate_word_frequency(word: str) -> float:
        common_words = ['the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that']
        if word.lower() in common_words:
            return 1.0
        elif len(word) <= 4:
            return 0.8
        elif len(word) <= 7:
            return 0.6
        else:
            return 0.4
    
    @staticmethod
    def calculate_morphological_complexity(word: str) -> float:
        prefixes = ['un', 're', 'pre', 'dis', 'over', 'under', 'out', 'up']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment']
        
        complexity = 0.3
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                complexity += 0.1
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                complexity += 0.1
        
        return min(complexity, 1.0)
    
    @staticmethod
    def calculate_etymology_complexity(word: str) -> float:
        if len(word) > 10:
            return 0.8
        elif len(word) > 7:
            return 0.6
        else:
            return 0.4

class Batch095Processor:
    def __init__(self):
        self.batch_095_data = {
            'janthina': {
                'definition': 'A genus of small, delicate pelagic gastropod mollusks, commonly known as violet snails or bubble raft snails. These marine creatures are famous for constructing bubble rafts from which they hang upside down at the ocean surface. Janthina species secrete mucus and trap air bubbles to create these floating platforms, allowing them to drift across warm ocean waters while feeding on other surface-dwelling organisms like Portuguese man-o-war and blue bottles. The shells of janthina are typically violet or purple in color, becoming paler toward the apex. These mollusks are found in tropical and subtropical waters worldwide, representing one of the few gastropod groups that spend their entire lives floating at the sea surface. Their unique lifestyle and beautiful coloration make them fascinating subjects for marine biologists studying pelagic ecosystems and adaptation strategies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/janˈθiːnə/ (jan-THEE-nuh)',
                'etymology': 'From New Latin, derived from Greek "ianthinos" meaning violet-colored, referring to the characteristic purple-violet coloration of the shells. The genus name was established in scientific taxonomy to describe these distinctive violet snails.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'Marine biologists discovered several _______ species floating on their characteristic bubble rafts during the research expedition.',
                'memory_tip': 'Remember "jan-THIN-a" - think of "thin" violet shells floating on the ocean, and the "jan" sounds like "jan-uary" when you might see purple sunsets over water.'
            },
            'january': {
                'definition': 'The first month of the Gregorian calendar year, containing 31 days and named after Janus, the Roman god of beginnings, transitions, and doorways. January marks the start of the new year in most cultures using the Gregorian calendar, often associated with fresh starts, resolutions, and new opportunities. In the Northern Hemisphere, January is typically the coldest month of winter, characterized by snow, frost, and shorter daylight hours. The month holds cultural significance across many societies as a time for reflection on the past year and planning for the future. January weather patterns significantly influence agriculture, seasonal activities, and human behavior patterns. Many important historical events, cultural celebrations, and personal milestones occur during this transitional month, making it a period of both retrospection and anticipation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒænjuˌɛri/ (JAN-yoo-air-ee)',
                'etymology': 'From Middle English, derived from Latin "Ianuarius" meaning "of Janus," named after the Roman god Janus who had two faces looking in opposite directions, symbolizing transitions and new beginnings. The month was added to the Roman calendar by King Numa Pompilius.',
                'language_origins': 'Latin, Middle English',
                'example_sentence': 'Many people make resolutions in _______ as they welcome the beginning of a new year.',
                'memory_tip': 'Remember "JAN-u-ary" - "JAN" like the name Jan, plus "u" for "you" starting something new, then "ary" like "are-we" ready for the new year.'
            },
            'japan': {
                'definition': 'An island nation in East Asia located in the Pacific Ocean, consisting of four main islands (Honshu, Hokkaido, Kyushu, and Shikoku) and numerous smaller islands. Japan is renowned for its unique blend of ancient traditions and cutting-edge technology, featuring distinctive cultural elements such as samurai history, traditional arts like calligraphy and tea ceremony, and modern innovations in electronics and automotive industries. The country has a population of approximately 125 million people and is known for its mountainous terrain, including the iconic Mount Fuji. Japan has played a significant role in global economics, technology development, and cultural exchange, contributing innovations in manufacturing, robotics, and entertainment. The nation\'s rich history includes periods of isolation and rapid modernization, resulting in a fascinating cultural landscape that attracts millions of visitors annually.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': '/dʒəˈpæn/ (juh-PAN)',
                'etymology': 'From Dutch "Japan," derived from Chinese "Riben" meaning "origin of the sun," which became "Nippon" in Japanese. The name reflects the country\'s position east of China, where the sun appears to rise.',
                'language_origins': 'Chinese, Dutch, Japanese',
                'example_sentence': 'Many tourists visit _______ to experience the unique combination of traditional culture and modern technology.',
                'memory_tip': 'Remember "ja-PAN" - think of "ja" (yes in German) + "PAN" like a cooking pan, since Japan is famous for its distinctive cuisine and cooking techniques.'
            },
            'japanese': {
                'definition': 'Relating to or characteristic of Japan, its people, language, or culture. As an adjective, Japanese describes anything originating from or associated with the island nation of Japan in East Asia. The term encompasses the Japanese language, a complex linguistic system featuring three writing systems (hiragana, katakana, and kanji), as well as cultural practices, traditions, arts, and social customs unique to Japan. Japanese culture is known for its emphasis on harmony, respect, precision, and aesthetic beauty, reflected in practices like the tea ceremony, martial arts, and traditional crafts. When used as a noun, Japanese refers to the people of Japan or their language. The Japanese language is spoken by approximately 125 million people and is known for its sophisticated system of honorific expressions and contextual communication patterns.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': '/ˌdʒæpəˈniːz/ (jap-uh-NEEZ)',
                'etymology': 'From "Japan" + suffix "-ese" indicating nationality or language, following the pattern of other nationality words like "Chinese" or "Portuguese." The suffix comes from Latin and French linguistic traditions.',
                'language_origins': 'English, Latin suffix',
                'example_sentence': 'She studied _______ calligraphy to better understand the artistic traditions of Japan.',
                'memory_tip': 'Remember "Japan-ESE" - "Japan" + "ESE" suffix used for nationalities, like "Chin-ESE" or "Portugu-ESE."'
            },
            'jargon': {
                'definition': 'Specialized terminology, vocabulary, or language used by members of a particular profession, trade, hobby, or social group that may be difficult for outsiders to understand. Jargon serves as a form of professional shorthand, allowing experts in a field to communicate complex concepts efficiently and precisely. While jargon can enhance communication within specialized communities, it can also create barriers to understanding for those unfamiliar with the specific terminology. Examples include medical jargon used by healthcare professionals, legal jargon in the legal system, computer jargon in technology fields, and military jargon in armed forces. The use of jargon can sometimes be criticized when it unnecessarily excludes or confuses non-specialists, but it remains an important tool for professional communication. Understanding the appropriate use of jargon versus plain language is crucial for effective communication across different audiences.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɑrgən/ (JAR-guhn)',
                'etymology': 'From Old French "jargon" meaning chatter or gibberish, possibly from an imitative origin suggesting confused or unintelligible speech. The word evolved to describe specialized professional language.',
                'language_origins': 'Old French',
                'example_sentence': 'The technical _______ used by the engineers made it difficult for the marketing team to understand the product specifications.',
                'memory_tip': 'Remember "JAR-gon" - think of words trapped in a "JAR" that only certain groups can open, plus "gon" like "gone" over most people\'s heads.'
            },
            'jarl': {
                'definition': 'A Scandinavian nobleman or chieftain during the Viking Age and medieval period, ranking below a king but above ordinary freemen in the social hierarchy. Jarls were powerful feudal lords who controlled large territories, commanded armies, and owed allegiance directly to the king. They possessed significant wealth, land holdings, and political influence within their regions, often serving as military leaders during conflicts and raids. The position of jarl was typically hereditary, passed down through noble bloodlines, though exceptional warriors or leaders could sometimes be elevated to this status through royal favor. Jarls played crucial roles in Viking society, organizing expeditions, administering justice, and maintaining order within their domains. The title is roughly equivalent to "earl" in English nobility, and jarls are frequently mentioned in Norse sagas and historical accounts of Scandinavian medieval society.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/jɑrl/ (yarl)',
                'etymology': 'From Old Norse "jarl" meaning nobleman or chieftain, related to the English "earl." The word derives from a Germanic root meaning "free man" or "warrior," reflecting the martial aristocratic culture of medieval Scandinavia.',
                'language_origins': 'Old Norse, Germanic',
                'example_sentence': 'The powerful _______ commanded a fleet of longships and controlled vast territories along the Norwegian coast.',
                'memory_tip': 'Remember "JARL" rhymes with "CARL" - imagine a noble Viking named Carl who became a jarl (chieftain) through his brave deeds.'
            },
            'jars': {
                'definition': 'Plural form of jar, referring to multiple cylindrical containers typically made of glass, ceramic, or plastic, used for storing food, liquids, or other materials. Jars come in various sizes and shapes, featuring wide openings that can be sealed with lids for preservation purposes. Common types include mason jars used for canning and food preservation, storage jars for dry goods like flour or sugar, and decorative jars for organizing household items. The design of jars makes them ideal for both short-term storage and long-term preservation, as their wide mouths allow for easy filling and cleaning. Jars have been used throughout human history for food storage, with archaeological evidence showing ceramic jars dating back thousands of years. Modern jars often feature airtight seals and are designed for specific purposes such as jam-making, pickling, or general household storage.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': '/dʒɑrz/ (jarz)',
                'etymology': 'Plural of "jar," from French "jarre" meaning large earthenware vessel, ultimately from Arabic "jarrah." The word entered English through Old French and has been used for centuries to describe storage containers.',
                'language_origins': 'French, Arabic, Old French',
                'example_sentence': 'She organized her pantry by storing dried beans and grains in clear glass _______.',
                'memory_tip': 'Remember "JARS" - think of "J" for "jelly," "AR" like "are," and "S" for "storage" - jelly jars are storage containers.'
            },
            'jasmone': {
                'definition': 'A volatile organic compound with the chemical formula C11H16O, naturally occurring in jasmine flowers and other plants, responsible for contributing to the characteristic floral fragrance of jasmine. Jasmone belongs to the chemical class of cyclopentenones and serves as an important component in perfumery and fragrance industry applications. This compound can exist in different isomeric forms, with cis-jasmone being particularly significant for its olfactory properties. Beyond its role in natural flower fragrances, jasmone has been studied for its potential biological activities and its use as a synthetic fragrance component in cosmetics, perfumes, and scented products. The compound represents one of many volatile molecules that plants produce to attract pollinators, and its isolation and synthesis have been important developments in understanding plant chemistry and creating artificial fragrances that mimic natural flower scents.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒæsmoʊn/ (JAS-mohn)',
                'etymology': 'From "jasmine" (the flower) + chemical suffix "-one" indicating a ketone compound. The name directly relates to its discovery and isolation from jasmine flowers, following standard chemical nomenclature conventions.',
                'language_origins': 'English, chemical nomenclature',
                'example_sentence': 'Perfumers value _______ for its ability to replicate the sweet, floral scent of natural jasmine in synthetic fragrances.',
                'memory_tip': 'Remember "JASM-ONE" - "JASM" from "jasmine" flower + "ONE" like "one" compound that makes jasmine smell so sweet.'
            },
            'jasper': {
                'definition': 'An opaque, microcrystalline variety of quartz mineral characterized by its rich colors and patterns, commonly found in red, yellow, brown, and green hues. Jasper forms through the slow precipitation of silica from groundwater, often incorporating iron oxides and other minerals that create its distinctive coloration and banding patterns. This semi-precious stone has been prized throughout human history for jewelry, decorative objects, and ceremonial purposes, with archaeological evidence showing its use in ancient civilizations across multiple continents. Different varieties of jasper are named for their appearance or origin, such as red jasper, yellow jasper, and picture jasper with landscape-like patterns. The stone typically exhibits a waxy to vitreous luster when polished and ranks 6.5-7 on the Mohs hardness scale, making it durable enough for various ornamental applications. Jasper deposits are found worldwide, with notable sources in India, Russia, Australia, and the United States.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒæspər/ (JAS-per)',
                'etymology': 'From Old French "jaspre," derived from Latin "iaspis" and Greek "iaspis," ultimately from a Semitic language. The word has maintained its essential form across many languages, reflecting the stone\'s widespread recognition.',
                'language_origins': 'Greek, Latin, Old French, Semitic',
                'example_sentence': 'The artisan carved an intricate design into the red _______ to create a beautiful pendant.',
                'memory_tip': 'Remember "JASP-ER" - think of "JASP" like "grasp" (you can grasp this stone) + "ER" - it\'s harder than many other decorative stones.'
            },
            'jaundiced': {
                'definition': 'Having a yellowish discoloration of the skin, eyes, or mucous membranes, typically caused by an excess of bilirubin in the blood due to liver dysfunction, bile duct obstruction, or excessive breakdown of red blood cells. In a medical context, jaundice is a symptom rather than a disease itself, often indicating underlying health conditions such as hepatitis, cirrhosis, gallstones, or hemolytic anemia. The term can also be used metaphorically to describe a person\'s outlook or perspective as being cynical, bitter, or prejudiced, suggesting that their judgment has been colored by negative experiences or bias. This figurative usage draws on the visual association between the yellow discoloration of jaundice and the idea of seeing things through a "colored" or distorted lens. Treatment of physical jaundice focuses on addressing the underlying cause, while metaphorical jaundice refers to attitude or perspective issues.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': '/ˈdʒɔndɪst/ (JAWN-dist)',
                'etymology': 'From "jaundice" + suffix "-ed," where "jaundice" comes from Old French "jaunisse," derived from "jaune" meaning yellow. The medical term evolved from the obvious yellow coloration associated with the condition.',
                'language_origins': 'Old French, Middle English',
                'example_sentence': 'The patient\'s _______ appearance prompted immediate liver function tests to determine the underlying cause.',
                'memory_tip': 'Remember "JAUN-diced" - "JAUN" sounds like "yawn" and people with jaundice look yellow and tired, plus "diced" like cut up (the liver is affected).'
            },
            'javas': {
                'definition': 'Plural form of Java, which can refer to multiple contexts: the large island in Indonesia known for its dense population, rich cultural heritage, and important role in Indonesian history and economy; multiple cups of coffee (slang usage, as Java is a well-known coffee-producing region); or multiple instances of the Java programming language or Java-based computer programs. In geographical terms, javas could refer to multiple regions similar to the island of Java. In computing contexts, it might refer to multiple Java applications, Java runtime environments, or Java-based systems. The island of Java is home to over half of Indonesia\'s population and includes major cities like Jakarta, Surabaya, and Bandung. It has been a center of civilization for centuries, featuring important historical sites like Borobudur and Prambanan temples, and continues to be economically vital to Indonesia.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': '/ˈdʒɑvəz/ (JAH-vuhz)',
                'etymology': 'Plural of "Java," from Sanskrit "Yavadvipa" meaning "island of barley," referring to the Indonesian island. In coffee slang, it derives from the island\'s reputation as a major coffee producer.',
                'language_origins': 'Sanskrit, Indonesian',
                'example_sentence': 'The programmer had to update multiple _______ applications to ensure compatibility with the new system requirements.',
                'memory_tip': 'Remember "JAV-AS" - "JAV" from Java (island or coffee) + "AS" for "as many" instances as you need (multiple Javas).'
            },
            'javelin': {
                'definition': 'A light spear designed specifically for throwing as far as possible, used both as an ancient hunting weapon and as a modern track and field athletic event. The modern athletic javelin consists of three main parts: a metal head, a shaft (typically made of metal, carbon fiber, or fiberglass), and a grip area wrapped with cord. In track and field competition, athletes sprint down a runway and throw the javelin for maximum distance while adhering to strict technical rules about grip, release, and landing angle. The javelin throw is one of the classic field events in athletics, featured in the Olympics, World Championships, and other major competitions. Historical javelins were used in warfare and hunting across many cultures, evolving from simple wooden spears to sophisticated weapons. The modern sporting javelin has undergone several design changes to ensure safety and fair competition, with specific regulations governing its weight, length, and balance point.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒævəlɪn/ (JAV-uh-lin)',
                'etymology': 'From Old French "javeline," a diminutive of "javelot" meaning dart or spear. The word entered English in the late Middle Ages and has maintained its association with throwing weapons and athletic implements.',
                'language_origins': 'Old French, Middle English',
                'example_sentence': 'The athlete\'s powerful throw sent the _______ soaring across the field to set a new personal record.',
                'memory_tip': 'Remember "JAVE-LIN" - "JAVE" sounds like "wave" (you wave it through the air) + "LIN" like "line" (it flies in a straight line when thrown).'
            },
            'jazzy': {
                'definition': 'Having the characteristics of jazz music, including syncopated rhythms, improvisation, and energetic or lively qualities; or describing something that is flashy, showy, or stylish in an attention-getting way. When applied to music, jazzy suggests rhythmic complexity, spontaneous creativity, and the distinctive swing feel associated with jazz genres. In broader usage, jazzy can describe anything with flair, excitement, or sophisticated style, such as fashion, interior design, or behavior. The term captures the essence of jazz culture\'s influence on American and global society, representing creativity, innovation, and dynamic energy. Something described as jazzy often stands out from conventional or ordinary approaches, displaying originality and verve. The word can be used positively to suggest liveliness and sophistication, though occasionally it might imply something is overly flashy or ostentatious.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': '/ˈdʒæzi/ (JAZ-ee)',
                'etymology': 'From "jazz" + suffix "-y" indicating having the quality of. "Jazz" itself has uncertain etymology, possibly from American slang meaning energy or excitement, first applied to music in early 20th century America.',
                'language_origins': 'American English, slang origin',
                'example_sentence': 'The musician added _______ rhythms and improvised solos to transform the classical piece into something uniquely creative.',
                'memory_tip': 'Remember "JAZZ-Y" - "JAZZ" music + "Y" meaning "having the quality of" - so it has the lively, improvisational quality of jazz.'
            },
            'jealousy': {
                'definition': 'A complex emotional state characterized by feelings of insecurity, resentment, and anxiety arising from a perceived threat to a valued relationship or from comparison with others who appear to possess something desired. Jealousy involves fear of losing someone important to a rival, combined with anger toward both the perceived threat and sometimes the valued person. This emotion can manifest in romantic relationships, friendships, family dynamics, and professional settings. Psychologists distinguish between cognitive jealousy (suspicious thoughts), emotional jealousy (negative feelings), and behavioral jealousy (actions taken in response). While mild jealousy might indicate care and attachment, extreme jealousy can become destructive, leading to controlling behavior, aggression, or relationship breakdown. Understanding and managing jealousy involves developing self-awareness, communication skills, and emotional regulation strategies. The emotion has been studied extensively in psychology and has cultural variations in expression and acceptability.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɛləsi/ (JEL-uh-see)',
                'etymology': 'From Old French "jalousie," derived from "jaloux" meaning jealous, ultimately from Late Latin "zelosus" meaning zealous. The evolution reflects the close relationship between zealous devotion and possessive jealousy.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'Her _______ over her sister\'s success began to strain their previously close relationship.',
                'memory_tip': 'Remember "JEAL-OUSY" - "JEAL" sounds like "steal" (fear someone will steal what you value) + "OUSY" like "ouch-y" (it hurts emotionally).'
            },
            'jeans': {
                'definition': 'Durable casual trousers made from denim fabric, typically featuring a distinctive blue color created by indigo dyeing. Originally designed as workwear for miners, cowboys, and laborers in the American West during the 19th century, jeans have evolved into one of the most popular and versatile clothing items worldwide. The fabric consists of cotton warp threads dyed with indigo and white weft threads, creating the characteristic appearance where the blue exterior contrasts with white interior fibers. Modern jeans come in numerous styles, cuts, colors, and treatments, ranging from traditional straight-leg designs to skinny, wide-leg, distressed, and designer variations. The global popularity of jeans represents a significant cultural phenomenon, symbolizing American casual culture while being adapted and embraced by diverse societies worldwide. Jeans are manufactured through various processes including stone washing, acid washing, and other treatments to achieve different textures and appearances.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': '/dʒiːnz/ (jeenz)',
                'etymology': 'From "jean," referring to a type of fabric originally from Gênes (Genoa), Italy. The plural form became standard as the garment consists of two legs joined together, following the pattern of other trouser-related words.',
                'language_origins': 'French, Italian (place name)',
                'example_sentence': 'She wore her favorite pair of _______ to the casual Friday event at work.',
                'memory_tip': 'Remember "JEANS" - think of "JEAN" (a person\'s name) + "S" for plural, like "Jean\'s pants" became just "jeans" for everyone.'
            },
            'jeepney': {
                'definition': 'A distinctively Filipino form of public transportation that evolved from U.S. military jeeps left over from World War II. These colorful, elongated vehicles serve as buses or shared taxis throughout the Philippines, particularly in urban and suburban areas. Jeepneys are known for their vibrant decorations, including bright colors, chrome ornaments, religious symbols, and personalized artwork that reflect Filipino culture and individual driver preferences. The typical jeepney features bench seating along the sides, open-air design for tropical climate comfort, and a unique "jeep" front end combined with an extended passenger compartment. They operate on fixed routes but can stop anywhere along the way to pick up or drop off passengers. Jeepneys represent an important part of Filipino cultural identity and provide affordable transportation for millions of people daily. The vehicles embody Filipino ingenuity and creativity in adapting military surplus into practical civilian transportation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒiːpni/ (JEEP-nee)',
                'etymology': 'Compound word from "jeep" (the military vehicle) + "ney" (a Filipino suffix), created in the Philippines after World War II when surplus U.S. military jeeps were converted into public transportation vehicles.',
                'language_origins': 'American English, Filipino',
                'example_sentence': 'Tourists often enjoy riding a colorfully decorated _______ to experience authentic Filipino transportation culture.',
                'memory_tip': 'Remember "JEEP-NEY" - "JEEP" (military vehicle) + "NEY" (Filipino ending), like a jeep that became a Filipino trolley.'
            },
            'jelly': {
                'definition': 'A semi-solid, translucent food product made by boiling fruit juice with sugar and a gelling agent (typically pectin) until it reaches a gel-like consistency. Unlike jam, jelly is made without pieces of fruit, resulting in a smooth, clear appearance that maintains the fruit\'s flavor while achieving a firm yet spreadable texture. Jelly can also refer to gelatin-based desserts, savory aspics, or any substance with a similar consistency. The preservation process involved in making jelly allows fruit flavors to be enjoyed year-round and was historically important for food storage before refrigeration. Commercial and homemade jellies come in numerous fruit varieties, from traditional grape and strawberry to exotic tropical fruits. The term can also describe any gelatinous substance, including natural biological materials like the jellyfish\'s body composition or petroleum jelly used in cosmetics and medical applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɛli/ (JEL-ee)',
                'etymology': 'From Old French "gelée," meaning frozen or congealed, derived from Latin "gelare" meaning to freeze. The culinary term developed from the process of liquid becoming solid through cooling or gelling agents.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The homemade grape _______ spread perfectly on the warm toast for breakfast.',
                'memory_tip': 'Remember "JELL-Y" - "JELL" like "gel" (it gels/sets) + "Y" ending - it\'s something that has gelled into a wobbly consistency.'
            },
            'jeopardy': {
                'definition': 'A state of danger, risk, or uncertainty where someone or something faces the possibility of loss, harm, or failure. In legal contexts, jeopardy specifically refers to the danger of conviction and punishment that a defendant faces in criminal proceedings, leading to the constitutional principle of "double jeopardy" which prevents being tried twice for the same crime. More generally, being in jeopardy means being in a precarious situation where negative consequences are possible or likely. The term suggests immediate or imminent threat rather than distant or theoretical risk. Common usage includes situations where jobs, relationships, health, safety, or success are at stake. The word has gained additional cultural recognition through the popular television game show "Jeopardy!" where contestants must provide questions to given answers, metaphorically putting their knowledge and winnings at risk.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɛpərdi/ (JEP-er-dee)',
                'etymology': 'From Old French "jeu parti," literally meaning "divided game" or "even game," referring to a situation where the outcome is uncertain. The term evolved through Middle English to its modern meaning of danger or risk.',
                'language_origins': 'Old French, Middle English',
                'example_sentence': 'The company\'s financial problems put hundreds of jobs in _______ as management considered layoffs.',
                'memory_tip': 'Remember "JEOP-ARDY" - "JEOP" sounds like "jump" (jumping into danger) + "ARDY" like "hardy" (you need to be hardy to survive jeopardy).'
            },
            'jerboa': {
                'definition': 'A small, jumping desert rodent belonging to the family Dipodidae, characterized by extremely long hind legs, a long tail with a tufted tip, and large ears adapted for life in arid environments. Jerboas are found primarily in the deserts of Africa and Asia, where they have evolved remarkable adaptations for surviving in harsh, dry conditions with limited water sources. These nocturnal animals can hop at high speeds using their powerful hind legs, similar to miniature kangaroos, and their oversized ears help with both hearing and heat regulation. Jerboas obtain most of their water from their food and have highly efficient kidneys that minimize water loss. Their sandy-colored fur provides camouflage against desert terrain, while their long tails serve as balancing aids during rapid hopping movements. Various species exist, ranging from the tiny baluchistan pygmy jerboa to the larger great jerboa, each adapted to specific desert environments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/dʒərˈboʊə/ (jer-BOH-uh)',
                'etymology': 'From Arabic "yarbu," the name for these desert rodents in their native regions. The word entered scientific taxonomy and then common English usage through biological classification systems.',
                'language_origins': 'Arabic',
                'example_sentence': 'The tiny _______ bounded across the desert sand using its powerful hind legs like a miniature kangaroo.',
                'memory_tip': 'Remember "JER-BOA" - "JER" like "jerk" (they jerk/jump quickly) + "BOA" like the snake (but this one hops instead of slithers).'
            },
            'jerky': {
                'definition': 'Lean meat that has been cut into strips and dried to remove moisture, creating a preserved food product that can be stored for extended periods without refrigeration. Traditional jerky is made by salting meat and allowing it to dry naturally in the sun or using controlled heat sources, resulting in a tough, chewy texture and concentrated flavor. Modern jerky production often includes marinades, spices, and controlled dehydration processes to enhance taste and ensure food safety. Common varieties include beef jerky, turkey jerky, and exotic options made from game meats like venison or elk. The preservation method dates back thousands of years and was essential for early human survival, allowing protein to be transported and stored during long journeys or harsh seasons. As an adjective, jerky describes movement that is characterized by sudden, irregular starts and stops, lacking smoothness or continuity.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': '/ˈdʒərki/ (JER-kee)',
                'etymology': 'From Spanish "charqui," derived from Quechua "ch\'arki" meaning dried meat. The word entered English through contact with Spanish colonial culture in the Americas, where indigenous preservation techniques were adopted.',
                'language_origins': 'Quechua, Spanish',
                'example_sentence': 'The hikers packed beef _______ as a lightweight, high-protein snack for their mountain expedition.',
                'memory_tip': 'Remember "JERK-Y" - "JERK" like jerking motions (the tough texture makes your jaw work) + "Y" - it\'s dried meat that\'s hard and chewy.'
            },
            'jersey': {
                'definition': 'A close-fitting pullover shirt, typically made from knitted fabric, commonly worn as athletic wear or casual clothing. In sports contexts, jerseys serve as team uniforms that identify players and often feature numbers, names, and team logos or colors. The term also refers to the specific knitted fabric used to make such garments, characterized by its stretch properties and comfortable fit. Jersey fabric is created using a knitting process that produces a smooth surface on one side and a looped texture on the other, making it ideal for form-fitting clothing. Beyond sports, jersey material is used for various casual garments including t-shirts, dresses, and undergarments. The word can also refer to Jersey cattle, a breed of dairy cows originally from the Isle of Jersey, known for producing rich, high-butterfat milk. Additionally, Jersey refers to the British Crown dependency island in the English Channel.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒərzi/ (JER-zee)',
                'etymology': 'Named after the Isle of Jersey in the English Channel, where a distinctive type of knitted fabric was originally produced. The association with the island led to both the fabric and garments made from it being called "jersey."',
                'language_origins': 'English (place name)',
                'example_sentence': 'The basketball player\'s _______ displayed his number prominently on both the front and back.',
                'memory_tip': 'Remember "JER-SEY" - "JER" like "jeer" (fans cheer or jeer players wearing jerseys) + "SEY" sounds like "say" (jerseys say which team you\'re on).'
            },
            'jesuit': {
                'definition': 'A member of the Society of Jesus, a Roman Catholic religious order founded by Saint Ignatius of Loyola in 1540. Jesuits are known for their emphasis on education, missionary work, and intellectual pursuits, operating schools, universities, and missions worldwide. The order played a significant role in the Counter-Reformation and has been involved in theological scholarship, scientific research, and social justice advocacy. Jesuits take traditional religious vows of poverty, chastity, and obedience, plus a special fourth vow of obedience to the Pope regarding missions. They are often called "the Pope\'s soldiers" due to their direct allegiance and disciplined approach to religious service. The Society of Jesus has produced numerous saints, scholars, scientists, and educators, including several Popes. Jesuit institutions are renowned for their academic excellence and commitment to forming students intellectually, spiritually, and ethically according to Catholic principles.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɛʒuɪt/ (JEZH-oo-it)',
                'etymology': 'From "Jesus" + suffix "-uit," meaning "of Jesus" or belonging to Jesus. The name "Society of Jesus" was chosen by founder Ignatius of Loyola to emphasize dedication to Christ.',
                'language_origins': 'Latin, Catholic ecclesiastical',
                'example_sentence': 'The _______ priest combined rigorous academic scholarship with deep spiritual commitment in his teaching and ministry.',
                'memory_tip': 'Remember "JESU-IT" - "JESU" from "Jesus" + "IT" like "in it" (they are "in it" for Jesus, totally dedicated to Christ\'s mission).'
            },
            'jettison': {
                'definition': 'To deliberately throw away, discard, or abandon something, especially in an emergency situation to reduce weight or eliminate unnecessary burden. The term originates from maritime and aviation contexts where cargo or equipment might be thrown overboard or dropped to prevent disaster, such as a sinking ship or crashing aircraft. In broader usage, jettison means to abandon plans, ideas, policies, or possessions that are no longer useful or have become impediments to progress. The action typically involves a conscious decision to sacrifice something of potential value for greater benefit or necessity. Businesses might jettison unprofitable divisions, individuals might jettison outdated beliefs, or governments might jettison ineffective policies. The word implies both urgency and calculated decision-making, suggesting that what is jettisoned could have value under different circumstances but must be sacrificed for immediate survival or improvement.',
                'part_of_speech': 'verb',
                'pronunciation_guide': '/ˈdʒɛtɪsən/ (JET-ih-sun)',
                'etymology': 'From Old French "getaison," derived from Latin "jactare" meaning to throw. The nautical term originally referred to throwing cargo overboard during emergencies, later expanding to general usage meaning to abandon or discard.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The airline had to _______ its expansion plans when fuel costs rose dramatically.',
                'memory_tip': 'Remember "JETTI-SON" - "JETTI" like "jet" (throwing things off a jet plane) + "SON" (you have to "son," or abandon something to survive).'
            },
            'jewel': {
                'definition': 'A precious stone, typically cut and polished for use in jewelry, or any ornamental object of great beauty and value. Jewels include gemstones such as diamonds, rubies, sapphires, and emeralds, which are prized for their rarity, beauty, hardness, and brilliance. The term can also refer metaphorically to anything considered precious, exceptional, or highly valued, such as a person of outstanding character or a particularly fine example of something. In mechanical contexts, jewels are synthetic gems used as bearings in precision instruments like watches to reduce friction and wear. The cutting and setting of jewels requires specialized skills and has developed into sophisticated art forms across different cultures. Historically, jewels have served as symbols of wealth, power, and status, featuring prominently in royal regalia, religious artifacts, and ceremonial objects. The appreciation of jewels combines aesthetic beauty with material value and cultural significance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒuːəl/ (JOO-uhl)',
                'etymology': 'From Old French "juel," derived from Latin "jocale" meaning plaything or ornament, related to "jocus" meaning joke or game. The evolution reflects the decorative and pleasurable aspects of precious stones.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The ancient crown was adorned with a magnificent _______ that sparkled in the candlelight.',
                'memory_tip': 'Remember "JEW-EL" - "JEW" like "jewel-ry" + "EL" like "elegant" - jewels are elegant precious stones used in jewelry.'
            },
            'jibboom': {
                'definition': 'A spar (long wooden or metal pole) that extends forward from the bowsprit of a sailing ship, used to support the jib sail and other forward sails. The jibboom is an essential component of traditional sailing vessel rigging, extending the ship\'s ability to carry sail area forward of the main mast. It typically consists of one or more sections that can be extended or retracted as needed, allowing sailors to adjust the configuration based on wind conditions and sailing requirements. The jibboom works in conjunction with the bowsprit to create a platform for multiple triangular sails that improve the vessel\'s ability to sail close to the wind. On larger ships, there might be multiple jibbooms including a flying jibboom that extends even further forward. The proper rigging and maintenance of the jibboom system requires skilled seamanship and is crucial for optimal sailing performance, particularly when sailing upwind or in changing weather conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɪbbuːm/ (JIB-boom)',
                'etymology': 'Compound word from "jib" (a triangular sail) + "boom" (a spar or pole). The term developed in nautical terminology to describe the specific spar that supports jib sails extending forward from the bowsprit.',
                'language_origins': 'English nautical terminology',
                'example_sentence': 'The experienced sailors carefully extended the _______ to set additional forward sails for better upwind performance.',
                'memory_tip': 'Remember "JIB-BOOM" - "JIB" (the sail it supports) + "BOOM" (the pole/spar) - it\'s the boom that holds the jib sail.'
            },
            'jicama': {
                'definition': 'A edible tuberous root vegetable native to Mexico and Central America, also known as Mexican turnip or yam bean. Jicama has a brown, fibrous exterior skin that is inedible, but the interior flesh is white, crisp, and mildly sweet with a texture similar to water chestnut or crisp apple. This low-calorie vegetable is rich in vitamin C, fiber, and potassium while containing minimal starch compared to other root vegetables. Jicama can be eaten raw in salads, slaws, and as a crunchy snack, often served with lime juice and chili powder in Mexican cuisine. It can also be cooked, though it tends to lose some of its characteristic crispness when heated. The vegetable belongs to the legume family despite growing underground like a tuber. Jicama has gained popularity in health-conscious diets due to its nutritional profile and versatility as a substitute for higher-calorie ingredients in various dishes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈhiːkəmə/ (HEE-kuh-muh)',
                'etymology': 'From Spanish "jícama," derived from Nahuatl "xicamatl," the indigenous Mexican name for this root vegetable. The word entered English through Spanish colonial influence and Mexican culinary traditions.',
                'language_origins': 'Nahuatl, Spanish',
                'example_sentence': 'The chef added crisp _______ slices to the salad for extra crunch and a mild, sweet flavor.',
                'memory_tip': 'Remember "JIC-AMA" - "JIC" sounds like "kick" (it has a crisp kick texture) + "AMA" (sounds like "mama" - mama\'s crispy root vegetable).'
            },
            'jicarilla': {
                'definition': 'A federally recognized Native American tribe, specifically a subgroup of the Apache people, primarily located in north-central New Mexico. The Jicarilla Apache Nation has a reservation covering approximately 742,000 acres and is known for their traditional practices including basket weaving, pottery, and beadwork. The name "Jicarilla" comes from Spanish meaning "little basket," referring to the tribe\'s exceptional skill in creating waterproof baskets. Historically, the Jicarilla Apache were semi-nomadic, following seasonal patterns for hunting and gathering across the Great Plains and Southwestern regions. They traditionally lived in tipis and brush shelters, practicing a lifestyle that combined Plains and Southwestern cultural elements. The tribe has maintained their cultural identity while adapting to modern circumstances, operating businesses including a casino, timber operations, and tourism ventures. The Jicarilla Apache Nation continues to preserve their language, ceremonies, and traditional arts while providing education and services to tribal members.',
                'part_of_speech': 'noun, proper noun',
                'pronunciation_guide': '/ˌhiːkəˈriːjə/ (hee-kuh-REE-yah)',
                'etymology': 'From Spanish "jicarilla," diminutive of "jícara" meaning bowl or cup, which itself comes from Nahuatl. The Spanish named this Apache group after their skill in making small baskets and containers.',
                'language_origins': 'Spanish, Nahuatl',
                'example_sentence': 'The _______ Apache Nation continues to maintain their traditional basket-making techniques while operating modern tribal enterprises.',
                'memory_tip': 'Remember "JIC-A-RILLA" - "JIC" like "jícara" (bowl/basket) + "RILLA" like "gorilla" (strong people known for making strong baskets).'
            },
            'jiggery': {
                'definition': 'Trickery, deception, or underhanded manipulation, especially involving clever but dishonest schemes or fraudulent practices. The term suggests cunning behavior designed to mislead or cheat others, often involving complex or elaborate methods to achieve illegitimate goals. Jiggery typically implies a level of sophistication in the deceptive practices, going beyond simple lies to involve calculated manipulation or fraud. The word can also refer to mysterious or suspicious activity where the exact nature of what is happening is unclear but appears questionable. In some contexts, jiggery might describe elaborate practical jokes or pranks, though the connotation is generally negative, suggesting behavior that crosses ethical boundaries. The term emphasizes the clever or intricate nature of the deception rather than crude or obvious forms of dishonesty.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɪɡəri/ (JIG-uh-ree)',
                'etymology': 'Possibly from "jigger" meaning to manipulate or fidget with something, combined with suffix "-ery" indicating action or practice. The word suggests the fidgety, manipulative actions associated with trickery.',
                'language_origins': 'English, colloquial',
                'example_sentence': 'The accountant\'s financial _______ was eventually discovered when auditors found the hidden transactions.',
                'memory_tip': 'Remember "JIGG-ERY" - "JIGG" like "jig" (a tricky dance) + "ERY" (the practice of) - it\'s the practice of tricky, deceptive moves.'
            },
            'jigsaw': {
                'definition': 'A power tool with a thin, reciprocating blade designed for cutting curved lines, intricate patterns, and detailed shapes in various materials including wood, metal, and plastic. The jigsaw\'s blade moves up and down rapidly, allowing for precise control when following marked cutting lines or creating freehand curves. This versatility makes it an essential tool for woodworking, crafting, and home improvement projects where straight-cutting tools like circular saws would be inadequate. The term also refers to jigsaw puzzles, which are puzzles consisting of numerous interlocking pieces that form a complete picture when assembled correctly. Jigsaw puzzles range from simple children\'s versions with large pieces to complex adult puzzles with thousands of tiny pieces. The puzzle name derives from the original method of creating them by cutting pictures mounted on wood using a jigsaw tool, creating the characteristic interlocking shapes that define the hobby.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɪɡsɔ/ (JIG-saw)',
                'etymology': 'Compound word from "jig" (a guide or template) + "saw" (cutting tool). Originally referred to a type of narrow saw used with a jig for cutting intricate patterns, later applied to the power tool and puzzles cut with such tools.',
                'language_origins': 'English compound word',
                'example_sentence': 'She used a _______ to cut the decorative curves in the wooden cabinet door.',
                'memory_tip': 'Remember "JIG-SAW" - "JIG" (like a dance with many moves) + "SAW" (cutting tool) - it\'s a saw that can "dance" around curves and intricate cuts.'
            },
            'jimberjawed': {
                'definition': 'Having a protruding or prominent jaw, characterized by an irregular or asymmetrical jawline that extends noticeably beyond normal proportions. This descriptive term refers to a facial feature where the lower jaw projects forward significantly, creating a distinctive appearance. The condition can be natural variation in bone structure or result from developmental or genetic factors affecting jaw formation. In some contexts, jimberjawed might describe someone whose jaw appears to jut out when speaking or expressing emotion, giving them a distinctive facial profile. The term can also be used more broadly to describe anything that appears crooked, askew, or irregularly shaped, extending beyond the original anatomical reference. While primarily descriptive, the word sometimes carries informal connotations about appearance, though jaw prominence can be a completely normal variation in human facial structure.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': '/ˈdʒɪmbərˌdʒɔd/ (JIM-ber-jawd)',
                'etymology': 'Compound word possibly from "jimber" (meaning crooked or askew) + "jawed" (having jaws). The "jimber" component may relate to "gimber" meaning to make faces or grimace, describing the appearance of an irregular jaw.',
                'language_origins': 'English dialect, compound formation',
                'example_sentence': 'The cartoon character was drawn with an exaggerated _______ appearance to emphasize his gruff personality.',
                'memory_tip': 'Remember "JIMBER-JAWED" - "JIMBER" like "timber" that\'s crooked + "JAWED" - having a crooked or prominent jaw like twisted timber.'
            },
            'jingoism': {
                'definition': 'Extreme patriotism characterized by aggressive foreign policy advocacy, bellicose nationalism, and support for military action against other countries. Jingoism goes beyond healthy national pride to embrace an antagonistic stance toward other nations, often involving calls for war or military intervention to assert national dominance. This ideology typically includes belief in national superiority, suspicion of international cooperation, and support for expansionist policies. Jingoistic attitudes often emerge during periods of international tension and can influence public opinion toward supporting military conflicts even when diplomatic solutions might be available. The term carries negative connotations, distinguishing between reasonable patriotism and dangerous ultra-nationalism that can lead to unnecessary conflicts. Jingoism can be exploited by political leaders seeking public support for aggressive policies, and it often involves oversimplified views of complex international relationships. Historical examples include various periods of aggressive nationalism that preceded or accompanied major military conflicts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɪŋɡoʊɪzəm/ (JING-go-izm)',
                'etymology': 'From "jingo," a term that emerged from a British music hall song supporting aggressive action against Russia in 1878, combined with suffix "-ism." The song contained the phrase "by jingo," an oath expressing determination to fight.',
                'language_origins': 'English, from popular song lyrics',
                'example_sentence': 'The politician\'s speeches reflected dangerous _______ that could lead the nation into unnecessary conflicts.',
                'memory_tip': 'Remember "JINGO-ISM" - "JINGO" sounds like "jingling" war bells + "ISM" (a belief system) - it\'s the belief in jingling war bells instead of peaceful solutions.'
            },
            'jingoismjitney': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely consisting of "jingoism" (extreme patriotism and aggressive nationalism) merged with "jitney" (a small public bus or shared taxi). This type of error occurs when PDF text extraction fails to properly separate distinct words that appear close together in the original document formatting. Jingoism refers to bellicose nationalism and support for aggressive foreign policy, while jitney describes an informal public transportation vehicle. These are completely unrelated concepts that have been artificially combined due to technical parsing issues. Such errors are common when processing PDF documents containing spelling bee word lists, where formatting irregularities can cause adjacent words to be merged without proper spacing. The combined form has no legitimate meaning and represents a data quality issue that should be flagged for correction.',
                'part_of_speech': 'error (combined words)',
                'pronunciation_guide': 'Not applicable (parsing error)',
                'etymology': 'PDF parsing error combining "jingoism" and "jitney" - two unrelated words incorrectly merged during text extraction from source documents.',
                'language_origins': 'Technical error, not linguistic',
                'example_sentence': 'This _______ entry represents a parsing error and should be separated into "jingoism" and "jitney."',
                'memory_tip': 'This is a PDF parsing error - remember to separate "JINGOISM" (extreme nationalism) and "JITNEY" (small bus) as two different words.'
            },
            'jinx': {
                'definition': 'A person, thing, or circumstance that is believed to bring bad luck or cause unfortunate events to occur. The concept of a jinx involves superstitious beliefs about certain individuals, objects, or situations having the power to influence outcomes negatively. As a verb, to jinx means to cast a spell of bad luck on someone or something, or to mention something positive in a way that might cause it to go wrong. The term is commonly used in sports contexts where fans might avoid saying positive things about their team\'s performance for fear of "jinxing" the outcome. Jinxes can be intentional (when someone deliberately wishes ill fortune) or accidental (when an innocent comment or action is believed to have caused bad luck). While scientifically unfounded, belief in jinxes remains widespread across cultures and can influence behavior through psychological effects and confirmation bias.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': '/dʒɪŋks/ (jinks)',
                'etymology': 'Possibly from Latin "jynx" meaning wryneck (a bird used in magic), or from "jinks" meaning to dodge or move quickly. The magical/superstitious associations developed through folk beliefs about luck and curses.',
                'language_origins': 'Latin, English folk etymology',
                'example_sentence': 'The team refused to discuss their winning streak, afraid that talking about it might _______ their good fortune.',
                'memory_tip': 'Remember "JINX" - sounds like "JINKS" as in "high jinks" (mischief), and jinxes are mischievous bad luck that spoils good things.'
            },
            'jitney': {
                'definition': 'A small public bus or shared taxi that operates on a flexible route, typically charging low fares and providing informal transportation services. Jitneys originated in the early 20th century United States as an alternative to more expensive streetcars and taxis, offering affordable transportation for working-class passengers. These vehicles usually follow semi-fixed routes but can deviate to pick up and drop off passengers at convenient locations. The jitney system represents a form of informal public transit that fills gaps in official transportation networks, particularly serving areas underserved by regular bus routes. In many developing countries, jitneys remain an important part of urban transportation systems, operating under various local names. The term can also refer to any small coin, particularly a nickel (five-cent piece), which was originally the typical fare for jitney rides. Modern jitneys continue to operate in some U.S. cities, providing supplemental public transportation services.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɪtni/ (JIT-nee)',
                'etymology': 'Possibly from French "jeton" meaning token or small coin, referring to the small fare charged for rides. The transportation meaning developed from the coin reference, as jitneys typically charged a nickel (five cents) for rides.',
                'language_origins': 'French, American English',
                'example_sentence': 'The _______ driver picked up passengers along the busy street, offering affordable transportation to the downtown area.',
                'memory_tip': 'Remember "JIT-NEY" - "JIT" like "jittery" (quick, nervous movement) + "NEY" like "money" (small coins) - it\'s quick transportation for small money.'
            },
            'jitterbug': {
                'definition': 'A lively, acrobatic form of swing dance that became popular in the 1930s and 1940s, characterized by energetic movements, lifts, spins, and jumps performed to big band and swing music. The jitterbug encompasses various swing dance styles including the Lindy Hop, East Coast Swing, and regional variations that emphasized improvisation and athletic partnering. Dancers typically performed rapid footwork, dramatic dips, and aerial moves that required significant skill and stamina. The dance became a cultural phenomenon during the swing era, representing youth culture and musical innovation of the time. The term can also refer to a person who dances the jitterbug or, more broadly, anyone who is nervous, restless, or hyperactive. Jitterbug dancing experienced revivals in later decades and continues to be practiced in dance communities worldwide. The energetic nature of the dance reflected the optimistic, high-energy spirit of swing music and served as a form of social expression during challenging historical periods.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': '/ˈdʒɪtərˌbʌɡ/ (JIT-er-bug)',
                'etymology': 'Compound word from "jitter" (nervous, shaky movement) + "bug" (enthusiast or person affected by something). The name captures the energetic, somewhat frantic quality of the dance style.',
                'language_origins': 'American English, 20th century slang',
                'example_sentence': 'The couple impressed everyone at the dance hall with their energetic _______ performance to the big band music.',
                'memory_tip': 'Remember "JITTER-BUG" - "JITTER" (shaky, energetic) + "BUG" (enthusiast) - people were "bugged" or crazy about this jittery, energetic dance.'
            },
            'jitterbugkennel': {
                'definition': 'This appears to be a combined word error from PDF parsing, likely consisting of "jitterbug" (a swing dance or nervous person) merged with "kennel" (a shelter for dogs). This type of error occurs when PDF text extraction fails to properly separate distinct words that appear close together in the original document formatting. Jitterbug refers to an energetic swing dance from the 1930s-40s or describes someone who is nervous and restless, while kennel describes a small shelter or boarding facility for dogs. These are completely unrelated concepts that have been artificially combined due to technical parsing issues. Such errors are common when processing PDF documents containing spelling bee word lists, where formatting irregularities can cause adjacent words to be merged without proper spacing. The combined form has no legitimate meaning and represents a data quality issue that should be flagged for correction.',
                'part_of_speech': 'error (combined words)',
                'pronunciation_guide': 'Not applicable (parsing error)',
                'etymology': 'PDF parsing error combining "jitterbug" and "kennel" - two unrelated words incorrectly merged during text extraction from source documents.',
                'language_origins': 'Technical error, not linguistic',
                'example_sentence': 'This _______ entry represents a parsing error and should be separated into "jitterbug" and "kennel."',
                'memory_tip': 'This is a PDF parsing error - remember to separate "JITTERBUG" (swing dance) and "KENNEL" (dog house) as two different words.'
            },
            'joaquin': {
                'definition': 'A Spanish and Portuguese masculine given name, equivalent to Joachim in English, commonly used in Hispanic and Latin American cultures. The name has biblical origins, traditionally associated with Saint Joachim, who is believed to have been the father of the Virgin Mary in Christian tradition. Joaquin is pronounced differently in Spanish compared to English, with the Spanish pronunciation emphasizing the "wah-KEEN" sound. The name has gained recognition in American culture through various prominent figures including actors, musicians, and historical personalities. In some contexts, Joaquin may refer to geographical features, particularly rivers or valleys named after individuals with this name, such as the San Joaquin Valley in California. The name carries cultural significance in Spanish-speaking communities and represents a connection to Catholic religious traditions and Hispanic heritage.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': '/hwɑˈkin/ (hwah-KEEN) in Spanish, /dʒoʊəˈkin/ (jo-uh-KEEN) in English',
                'etymology': 'From Hebrew "Yehoyakim" meaning "God will establish," through Latin "Joachim" and Spanish adaptation. The name has strong biblical and religious associations in Christian tradition.',
                'language_origins': 'Hebrew, Latin, Spanish',
                'example_sentence': '_______ was a popular name choice among Hispanic families celebrating their cultural heritage.',
                'memory_tip': 'Remember "JOA-QUIN" - "JOA" sounds like "wah" in Spanish + "QUIN" like "keen" - it\'s pronounced "wah-KEEN" in Spanish.'
            },
            'jocote': {
                'definition': 'A tropical fruit native to Central America and Mexico, scientifically known as Spondias purpurea, also called red mombin, purple mombin, or hog plum. The jocote is a small, oval-shaped fruit with smooth, thin skin that ranges in color from green to yellow, orange, red, or purple when ripe. The flesh is juicy, sweet-tart, and surrounds a large seed, similar to a plum but with a more tropical flavor profile. Jocote trees are common throughout Central America, particularly in Guatemala, El Salvador, Honduras, and southern Mexico, where the fruit is eaten fresh, made into beverages, or used in traditional desserts. The fruit is rich in vitamin C and antioxidants, and the tree is valued for its ability to grow in poor soils and withstand drought conditions. In local markets, jocotes are often sold by street vendors and are considered a nostalgic childhood treat by many Central Americans.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/hoˈkote/ (ho-KO-teh)',
                'etymology': 'From Nahuatl "xocotl" meaning fruit, adopted into Spanish and used throughout Central America to describe this specific tropical fruit. The word reflects the indigenous Mexican origins of the fruit\'s cultivation.',
                'language_origins': 'Nahuatl, Spanish',
                'example_sentence': 'The children eagerly climbed the _______ tree to pick the sweet, colorful fruits during the harvest season.',
                'memory_tip': 'Remember "JO-COTE" - "JO" like "joy" (joyful fruit) + "COTE" sounds like "coat" (the fruit has a colorful coat/skin).'
            },
            'jocularity': {
                'definition': 'The quality of being jocular; humor, jest, or playful behavior characterized by good-natured fun and lightheartedness. Jocularity involves the tendency to joke, laugh, and engage in witty conversation, often serving to create a pleasant, relaxed atmosphere in social situations. This trait encompasses both the ability to appreciate humor and the skill to generate amusing remarks or situations. Jocularity differs from sarcasm or mean-spirited humor in that it aims to entertain and uplift rather than to mock or belittle. People who exhibit jocularity are often considered good company and effective at diffusing tension through appropriate humor. The quality can be particularly valuable in leadership, teaching, and social contexts where maintaining morale and engagement is important. However, jocularity must be balanced with seriousness when situations require it, as inappropriate humor can be counterproductive or offensive.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˌdʒɑkjəˈlɛrɪti/ (jahk-yuh-LAIR-ih-tee)',
                'etymology': 'From Latin "jocularis" meaning given to jesting, derived from "jocus" meaning joke or jest, combined with suffix "-ity" indicating a quality or state. The word emphasizes the disposition toward humor.',
                'language_origins': 'Latin',
                'example_sentence': 'The teacher\'s natural _______ helped create a positive classroom environment where students felt comfortable participating.',
                'memory_tip': 'Remember "JOCUL-ARITY" - "JOCUL" from "jocular" (joking) + "ARITY" like "rarity" - it\'s the rare quality of being naturally funny and playful.'
            },
            'jodhpurs': {
                'definition': 'Close-fitting riding pants that are loose through the hips and thighs but tight from the knee to the ankle, originally designed for horseback riding. Jodhpurs feature a distinctive flared cut above the knee that narrows dramatically to fit snugly around the lower leg, allowing them to be worn comfortably inside tall riding boots. The design originated in India and was adapted by British cavalry officers, becoming standard equestrian attire. Traditional jodhpurs are made from stretchy, durable materials that provide freedom of movement while maintaining a sleek appearance in the saddle. They often feature reinforced inner leg panels to prevent wear from stirrup leathers and saddle contact. While originally designed for practical riding purposes, jodhpurs have also been adopted as a fashion statement and are worn in various equestrian disciplines from casual trail riding to formal dressage competitions. The distinctive silhouette has influenced other fashion designs beyond equestrian wear.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': '/ˈdʒɑdpərz/ (JAHD-purz)',
                'etymology': 'Named after Jodhpur, a city in Rajasthan, India, where this style of riding breeches originated. British cavalry officers adopted the design during colonial period and brought it to Western equestrian culture.',
                'language_origins': 'Hindi (place name), English adaptation',
                'example_sentence': 'The equestrian competitor wore traditional _______ with tall black boots for the dressage event.',
                'memory_tip': 'Remember "JODH-PURS" - "JODH" from Jodhpur, India + "PURS" like "purse strings" (they\'re tight around the ankles like pulling purse strings tight).'
            },
            'jody': {
                'definition': 'In military slang, a term referring to the civilian man who stays home while soldiers are deployed, often with the implication that he might steal the affections of servicemen\'s girlfriends or wives. The concept of "Jody" represents the fears and anxieties of deployed military personnel about what might happen in their absence. Jody calls or cadences are rhythmic chants used during military training and marching that often reference this character, serving both as motivation and as a way to express and cope with deployment concerns. The term has become embedded in military culture and appears in various forms of military folklore, songs, and traditions. As a proper name, Jody is also used as both a masculine and feminine given name in American culture, unrelated to the military usage. The military usage reflects the psychological challenges faced by service members during separation from home and loved ones.',
                'part_of_speech': 'noun, proper noun',
                'pronunciation_guide': '/ˈdʒoʊdi/ (JOH-dee)',
                'etymology': 'Origin uncertain in military slang context, possibly from the name "Joe" or "Joe the Grinder." As a personal name, it\'s a diminutive of various names including Joseph, Jodene, or used independently.',
                'language_origins': 'American military slang, English name variations',
                'example_sentence': 'The soldiers sang a traditional _______ call during their morning march to maintain rhythm and unit cohesion.',
                'memory_tip': 'Remember "JODY" - in military context, think "JOE-dy" like "Joe" who stays home while soldiers go away.'
            },
            'joggled': {
                'definition': 'Past tense of joggle, meaning to shake or move with slight, irregular motions; to bump or jar gently and repeatedly. Joggling describes a continuous, mild shaking or vibrating action that causes something to move in a jerky, unsteady manner. The motion is typically not violent but persistent enough to be noticeable and potentially annoying or disruptive. Examples might include being joggled while riding in a rough vehicle, having objects joggled on a vibrating surface, or being joggled by someone accidentally bumping into you repeatedly. In construction and carpentry, joggle can also refer to a specific type of joint where pieces fit together with a notch or projection, and "joggled" would describe something constructed with such joints. The word implies a repetitive, rhythmic disturbance rather than a single sharp movement.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': '/ˈdʒɑɡəld/ (JAH-guhld)',
                'etymology': 'Past tense of "joggle," which is a frequentative form of "jog," meaning to shake or move with small, repeated motions. The word developed from the basic concept of jogging or light shaking.',
                'language_origins': 'English, from "jog" + frequentative suffix',
                'example_sentence': 'The rough road _______ the passengers in the old bus for the entire journey.',
                'memory_tip': 'Remember "JOGG-LED" - "JOGG" like "jog" (bouncing motion) + "LED" (past tense) - something was led through a bouncing, shaking motion.'
            },
            'john': {
                'definition': 'A common masculine given name of Hebrew origin, one of the most popular names in English-speaking cultures throughout history. John has numerous variations across different languages and cultures, including Juan (Spanish), Jean (French), Johann (German), and Giovanni (Italian). The name has biblical significance, associated with John the Baptist and John the Apostle in Christian tradition. In colloquial usage, "john" can refer to a toilet or bathroom, and in some contexts may refer to a customer of prostitution (though this usage is considered crude). The name John has been borne by countless notable figures throughout history, including kings, presidents, saints, artists, and scientists. Its popularity stems partly from its simple pronunciation and spelling across many languages. The name\'s prevalence has made it synonymous with the "common man" or "everyman" in various cultural expressions.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': '/dʒɑn/ (jahn)',
                'etymology': 'From Hebrew "Yohanan" meaning "God is gracious," through Greek "Ioannes," Latin "Iohannes," and Old French "Jehan" into Middle English "John." The name has maintained remarkable consistency across languages.',
                'language_origins': 'Hebrew, Greek, Latin, Old French',
                'example_sentence': '_______ was named after his grandfather, continuing the family tradition of biblical names.',
                'memory_tip': 'Remember "JOHN" - one of the most common names, think "Johnny" or "Jack" as nicknames, and it means "God is gracious."'
            },
            'johnson': {
                'definition': 'A patronymic surname meaning "son of John," one of the most common surnames in English-speaking countries. The name follows the traditional English pattern of adding "-son" to a father\'s name to indicate lineage, making it extremely prevalent due to the popularity of the given name John. Johnson appears frequently in American history and culture, with numerous notable figures bearing this surname including presidents, civil rights leaders, entertainers, and business leaders. The name\'s ubiquity has made it representative of typical American family names. In some informal contexts, "johnson" may be used as slang, though this usage is considered crude. The surname has various spelling alternatives including Johnston, Jonsson (Scandinavian), and similar variations. Due to its frequency, Johnson often requires additional identifiers to distinguish between individuals, leading to the common use of middle names or initials.',
                'part_of_speech': 'proper noun (surname)',
                'pronunciation_guide': '/ˈdʒɑnsən/ (JAHN-suhn)',
                'etymology': 'Patronymic surname from "John" + "-son," literally meaning "son of John." This naming pattern was common in English and Scandinavian cultures for indicating paternal lineage.',
                'language_origins': 'English patronymic formation',
                'example_sentence': 'Mrs. _______ introduced herself as the new principal at the school board meeting.',
                'memory_tip': 'Remember "JOHN-SON" - literally "John\'s son," following the pattern where "-son" means "son of" the first name.'
            },
            'joie': {
                'definition': 'A French word meaning joy, happiness, or delight, commonly encountered in English through the phrase "joie de vivre," which translates to "joy of living" or enthusiasm for life. Joie represents more than simple happiness; it conveys a sense of exuberant enjoyment and zest for existence. The concept encompasses an appreciation for life\'s pleasures, an optimistic outlook, and the ability to find satisfaction in everyday experiences. While primarily used in the borrowed phrase "joie de vivre," the word joie itself embodies the French cultural appreciation for enjoying life\'s finer aspects. This philosophy emphasizes living fully, appreciating beauty, savoring experiences, and maintaining a positive attitude despite life\'s challenges. The concept has been adopted into English-speaking cultures as a desirable life philosophy, representing the balance between responsibility and the pursuit of happiness.',
                'part_of_speech': 'noun (French)',
                'pronunciation_guide': '/ʒwa/ (zhwah) in French, /dʒɔɪ/ (joy) when anglicized',
                'etymology': 'From Old French "joie," derived from Latin "gaudia" (plural of "gaudium") meaning joy or gladness. The word has maintained its essential meaning throughout its linguistic evolution.',
                'language_origins': 'French, from Latin',
                'example_sentence': 'Her natural _______ de vivre made her the most popular person at every social gathering.',
                'memory_tip': 'Remember "JOIE" - it sounds like "JOY" in English, and that\'s exactly what it means in French - pure joy and happiness.'
            },
            'join': {
                'definition': 'To connect, unite, or bring together two or more things, people, or concepts into a single entity or group. Join can describe physical actions such as connecting pieces of material, assembling components, or linking objects together. It also encompasses social and organizational meanings, such as becoming a member of a group, participating in an activity, or aligning with others for a common purpose. In relationships, join suggests partnership, collaboration, or coming together for mutual benefit. The word implies a conscious decision to become part of something larger or to create connections where none existed before. Joining often involves commitment, whether temporary or permanent, and can occur in contexts ranging from casual social gatherings to formal organizational memberships. The concept of joining is fundamental to human cooperation and community building.',
                'part_of_speech': 'verb',
                'pronunciation_guide': '/dʒɔɪn/ (joyn)',
                'etymology': 'From Old French "joindre," derived from Latin "jungere" meaning to yoke or bind together. The concept of joining has remained consistent across language evolution, emphasizing connection and unity.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'She decided to _______ the community garden project to help beautify the neighborhood.',
                'memory_tip': 'Remember "JOIN" - think of "joint" where two bones connect, or linking hands to "join" together with others.'
            },
            'joinery': {
                'definition': 'The craft or trade of constructing wooden joints and assembling wooden components into furniture, buildings, or other structures without using nails, screws, or other metal fasteners. Joinery represents a sophisticated woodworking skill that relies on precisely cut interlocking joints such as dovetails, mortise and tenon, finger joints, and dado joints to create strong, durable connections. This traditional building technique has been practiced for thousands of years and continues to be valued for its strength, beauty, and longevity. Master joiners possess deep knowledge of wood properties, joint geometry, and construction techniques that allow them to create complex wooden structures. Joinery differs from carpentry in its emphasis on precision fitting and the creation of furniture-quality work rather than rough construction. The craft encompasses both functional and decorative aspects, often producing beautiful wooden objects that showcase the natural properties of different wood species.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɔɪnəri/ (JOY-nuh-ree)',
                'etymology': 'From "join" + suffix "-ery" indicating a place of work, craft, or collection of items. The word developed to describe the specific woodworking trade focused on creating wooden joints and connections.',
                'language_origins': 'English, from "join" + craft suffix',
                'example_sentence': 'The antique cabinet showcased exceptional _______ with its perfectly fitted dovetail joints and smooth-operating drawers.',
                'memory_tip': 'Remember "JOIN-ERY" - "JOIN" (connecting pieces) + "ERY" (the craft of) - it\'s the craft of joining wood pieces without nails or screws.'
            },
            'joists': {
                'definition': 'Horizontal structural beams that run parallel to each other and support floors, ceilings, or roofs in building construction. Joists are typically made from wood, steel, or engineered materials and are designed to bear loads and transfer weight to the main support beams or walls. In residential construction, floor joists create the framework upon which subfloors and finish floors are installed, while ceiling joists support the ceiling materials and sometimes upper floors. The spacing, size, and material of joists are determined by building codes and engineering requirements based on the span distance and expected load. Proper joist installation is crucial for structural integrity and preventing sagging, bouncing, or failure. Joists may also accommodate utilities such as electrical wiring, plumbing, and HVAC systems that run between floors or through ceiling spaces. Different types include solid wood joists, I-joists (engineered), and steel joists for different applications.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': '/dʒɔɪsts/ (joysts)',
                'etymology': 'From Old French "giste," meaning "beam on which something rests," derived from "gesir" meaning to lie. The word evolved through Middle English to describe horizontal support beams in construction.',
                'language_origins': 'Old French, Middle English',
                'example_sentence': 'The contractor inspected the floor _______ to ensure they could support the weight of the new kitchen island.',
                'memory_tip': 'Remember "JOISTS" - sounds like "HOISTS" (they hoist/support floors) - these are the horizontal beams that hold up floors and ceilings.'
            },
            'jolly': {
                'definition': 'Cheerful, merry, and good-humored; characterized by happiness, friendliness, and an upbeat disposition. A jolly person typically displays infectious enthusiasm, laughs easily, and spreads positive feelings to those around them. The word suggests not just happiness but a robust, hearty form of cheerfulness that is often associated with celebration, festivity, and social enjoyment. Jolly can describe both temporary moods and permanent personality traits, indicating someone who approaches life with optimism and finds reasons to be pleased even in ordinary circumstances. The term is often associated with holiday seasons, parties, and social gatherings where merriment is expected. In British usage, "jolly" can also serve as an intensifier meaning "very" or "quite." The concept of jolliness encompasses both personal contentment and the ability to share that positive energy with others.',
                'part_of_speech': 'adjective, adverb (British)',
                'pronunciation_guide': '/ˈdʒɑli/ (JAH-lee)',
                'etymology': 'From Old French "joli" meaning pretty or pleasant, which evolved in English to emphasize cheerfulness and merriment rather than just physical attractiveness. The meaning shift reflects cultural values around personality.',
                'language_origins': 'Old French, Middle English',
                'example_sentence': 'The _______ shopkeeper always greeted customers with a warm smile and friendly conversation.',
                'memory_tip': 'Remember "JOLLY" - think of "jolly old Saint Nicholas" (Santa Claus) who is always cheerful, merry, and spreading joy.'
            },
            'jonquil': {
                'definition': 'A type of narcissus flower, specifically Narcissus jonquilla, characterized by small, fragrant, bright yellow blooms with a sweet scent and narrow, rush-like leaves. Jonquils are spring-flowering bulbous plants native to Spain and Portugal but widely cultivated in gardens throughout temperate regions. The flowers typically appear in clusters of 2-6 blooms per stem, each featuring six petals surrounding a small central cup or corona. Jonquils are distinguished from other daffodils by their distinctive fragrance, smaller size, and multiple flowers per stem. They prefer well-drained soil and full to partial sun, making them popular choices for naturalized plantings, rock gardens, and borders. The bulbs are planted in fall and bloom in early to mid-spring, often among the first flowers to appear after winter. Jonquils have been cultivated for centuries and are valued both for their ornamental beauty and their sweet perfume.',
                'part_of_speech': 'noun',
                'pronunciation_guide': '/ˈdʒɑŋkwɪl/ (JAHN-kwil)',
                'etymology': 'From French "jonquille," derived from Spanish "junquillo," a diminutive of "junco" meaning rush, referring to the plant\'s narrow, rush-like leaves. The name reflects the plant\'s distinctive foliage.',
                'language_origins': 'Spanish, French',
                'example_sentence': 'The garden path was lined with fragrant _______ that filled the air with their sweet perfume each spring.',
                'memory_tip': 'Remember "JON-QUIL" - "JON" like the name John + "QUIL" like "quill" (narrow like a quill pen, referring to the thin leaves of this daffodil).'
            }
        }
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        return self.batch_095_data.get(word, {
            'definition': f'Comprehensive definition for {word} not found in batch data.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'Pronunciation for {word} not available.',
            'etymology': f'Etymology for {word} not available.',
            'language_origins': 'Unknown',
            'example_sentence': f'Example sentence for {word} not available.',
            'memory_tip': f'Memory tip for {word} not available.'
        })

def main():
    print("Processing output/batch_095_words.csv...")
    
    # Read the CSV file
    df = pd.read_csv('output/batch_095_words.csv')
    
    # Initialize the processor and difficulty calculator
    processor = Batch095Processor()
    calc = DifficultyCalculator()
    
    # Process each word
    processed_words = []
    errors_found = []
    
    for _, row in df.iterrows():
        word = row['word'].strip()
        
        # Check for combined word errors and other issues
        error_flags = []
        
        # Combined word detection for batch 095
        if word == 'jingoismjitney':
            error_flags.append('Combined word error: "jingoismjitney" appears to be "jingoism" (extreme nationalism) + "jitney" (small bus) merged together. This is likely a PDF parsing error.')
        elif word == 'jitterbugkennel':
            error_flags.append('Combined word error: "jitterbugkennel" appears to be "jitterbug" (swing dance) + "kennel" (dog house) merged together. This is likely a PDF parsing error.')
        
        if error_flags:
            errors_found.extend([f'{word}: {error}' for error in error_flags])
        
        # Get comprehensive Claude data
        claude_data = processor.get_comprehensive_claude_data(word)
        
        # Calculate difficulty factors
        phonetic_transparency = calc.calculate_phonetic_transparency(word)
        word_frequency = calc.calculate_word_frequency(word) 
        morphological_complexity = calc.calculate_morphological_complexity(word)
        etymology_complexity = calc.calculate_etymology_complexity(word)
        
        word_data = WordData(
            word=word,
            years=row['years'],
            source_files=row['source_files'],
            source_difficulties=row['source_difficulties'],
            definition=claude_data['definition'],
            part_of_speech=claude_data['part_of_speech'],
            pronunciation_guide=claude_data['pronunciation_guide'],
            etymology=claude_data['etymology'],
            language_origins=claude_data['language_origins'],
            example_sentence=claude_data['example_sentence'],
            memory_tip=claude_data['memory_tip'],
            phonetic_transparency=phonetic_transparency,
            word_frequency=word_frequency,
            morphological_complexity=morphological_complexity,
            etymology_complexity=etymology_complexity,
            final_difficulty=None
        )
        
        processed_words.append(word_data)
    
    # Create output DataFrame
    output_data = []
    for word_data in processed_words:
        output_data.append({
            'word': word_data.word,
            'years': word_data.years,
            'source_files': word_data.source_files,
            'source_difficulties': word_data.source_difficulties,
            'definition': word_data.definition,
            'part_of_speech': word_data.part_of_speech,
            'pronunciation_guide': word_data.pronunciation_guide,
            'etymology': word_data.etymology,
            'language_origins': word_data.language_origins,
            'example_sentence': word_data.example_sentence,
            'memory_tip': word_data.memory_tip,
            'phonetic_transparency': word_data.phonetic_transparency,
            'word_frequency': word_data.word_frequency,
            'morphological_complexity': word_data.morphological_complexity,
            'etymology_complexity': word_data.etymology_complexity,
            'final_difficulty': word_data.final_difficulty
        })
    
    # Save to CSV
    output_df = pd.DataFrame(output_data)
    output_df.to_csv('output/batch_095_processed.csv', index=False)
    
    # Print results
    print(f"Successfully processed {len(processed_words)}/50 words to output/batch_095_processed.csv")
    if errors_found:
        print(f"Found {len(errors_found)} error(s):")
        for error in errors_found:
            print(f"  - {error}")
    else:
        print("No errors detected in this batch.")
    
    print("Batch 095 processing completed successfully!")

if __name__ == "__main__":
    main()