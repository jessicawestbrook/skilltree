-- SAFE INSERT: New words with duplicate prevention
-- Generated on 2025-08-23T06:12:53.357Z  
-- Unique new words: 636
-- Uses ON CONFLICT DO NOTHING for safety

BEGIN;

-- Insert new words, skip if word already exists
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('grown-ups', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hem', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('polo', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drum', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('mix', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drool', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pie', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('workhorse', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forgive', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fragrance', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('explanation', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ecotourism', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dojo', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foxes', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wan', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('flexibleskeleton', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yarn', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('winsome', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('uglinessquack', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('elderlyamigo', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('tweeholiday', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bakeryporridge', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('klutzenvoy', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dinosaur', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('earthquake', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drastic', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yoga', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('police', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wren', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('obviouspulse', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('rabble-rouser', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wreath', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('differed', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exhibits', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('disturbancewily', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('writers', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('diminished', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('distressed', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('domain', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('evidence', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('sherifftarry', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('beatboxingmutate', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hunky-dory', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('withers', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('beaucoupbanal', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pharmacyfondant', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ecstatic', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pharaohopponency', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('effusiveprimitive', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('jurassicmyoglobin', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('resuscitateapprobatory', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('phoneticianmacular', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pauperepoch', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('designerleisure', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('centenarymatrimony', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('egressgeocaching', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('driveljettison', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cyberneticsgarniture', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('tympanumfisticuffs', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('celeryidiosyncratic', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('vernalaardvark', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('vinegarfiduciary', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pashminautilitarian', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('moribundrecriminatory', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bromidealgae', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dispositionremonstrance', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('patronymicodometer', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('backgammonintuitable', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('animustrillium', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('depredationignominious', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dovecote', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('billiardsobstreperous', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('establishmentruminate', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('obligeviscount', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('solitairedishevel', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('peremptoryinfarction', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('solderinterim', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exhaust', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('sententiouscardiopathy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foliage', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yeoman', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('angularconcomitant', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('abundancecalamitous', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dropsonde', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bantamapprentice', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('divanbadminton', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('emphatic', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('contaminatedmadagascar', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('xylyl', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cinerariumpolemic', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('embroglio', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('briocheadumbrate', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('woad', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('politeia', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('voceinesculent', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('framboise', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('examen', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zymurgy', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('carapacedauerlauf', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('emanant', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('effrontery', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('polydactyly', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('elision', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('oxalismyeloma', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('paraffinvigneron', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('upsilonsakura', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('rescissiblejungian', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('coiffurerepartee', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yakitoripejorate', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('panjandrumcatachresis', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('camarillanidicolous', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('coaxationardoise', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foleysyzygy', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eel', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dome', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hit', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ray', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dusk', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fineday', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('jam', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dinner', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fed', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('sir', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('each', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forever', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('double', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('piperhear', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('awe', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('presencesizzle', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('followed', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('window', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pocket', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('athletejotted', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('worse', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('duo', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('else', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('competitivelounge', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('elderly', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('boycottcalzone', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kilnwebisode', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('proneselfie', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kerneltawny', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drape', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('plush', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('whimperbracelet', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eddy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drowsy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fragment', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fortran', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('podium', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('runesancestors', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fountain', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ramificationstemerity', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('urgencybifurcate', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('porcelaindeglaciation', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('circuitousveracity', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('braillevignette', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('reiterateremorseful', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('collegialityinclement', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ataxiapageantry', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wobbulatormahogany', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('clarinetcapillary', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('anabolicjimberjawed', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('limpidsyllabus', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('revelationarithmetic', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ectoplasmolfactory', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('duchypagoda', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('authenticatefiscal', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('latencyepitaphs', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('decumbituremultivalent', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('chemistryquandary', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ministrationsracketeer', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('legerityvatican', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('commissionergrande', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ryelanddomesticity', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('princepsprocurement', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('chupacabraacadians', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wrath', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('divulge', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('franchise', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('embellishes', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eviction', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('parishionerastrologers', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fodder', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('unprepossessingbipolar', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dosages', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exhalation', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('prosceniumpolitesse', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('benedictinearcane', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('retinoscopysepulchral', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('whippoorwillficus', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('laterigradehyssop', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bunyanesqueexsect', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('lapidarycachexia', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foley', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('brucellosiswasteweir', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dulcinea', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('haplographytchefuncte', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('son', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('try', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('duckling', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('car', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('verylast', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drill', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('lid', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hat', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wantedsprung', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zoomed', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cog', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('oil', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('frames', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('frankly', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('basketsbonnet', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wrenches', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('polish', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exas', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('direct', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forty', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('embers', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('blurtedwallet', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('climateyankee', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('postponewafer', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dough', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('excavating', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bailiffinfiltrate', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('quantifyredemption', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('deceitfulcinderella', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('physicalpunily', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drone', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dire', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wizard', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('crockerygauze', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exception', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dingoes', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dormitories', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('flaxentriplicate', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('emboldened', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('withered', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('emitting', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wretched', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('charlotteelation', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wreaked', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dutifully', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exerts', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('complacencykraken', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('abstrusenephrolith', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('vivaciousxenoglossy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('grandiloquentarmature', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('newfoundlandfulminate', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('quinaryafroth', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('polyesteranoint', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eluateheterophony', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('acquitcapnometer', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('referralaerials', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exile', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drudgery', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kimcheemenorahs', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('embroidery', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('feintedhumus', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fortuitous', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fractious', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wiesbadenmontmorency', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ducats', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yom', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('linsey-woolsey', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('edinburgh', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ziggurat', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('durham', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('des', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('brujaupsilon', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('daguerreotypeyakitori', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('focacciapahoehoe', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bahuvrihipanjandrum', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('portmanteaucoaxation', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('vizierialcrescive', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cachexiaconnoisseur', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('effluxfrugivore', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('amidcathect', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('atencatjang', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('sit', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cry', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hey', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('poke', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drag', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('off', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('came', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dollbill', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pod', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('top', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('map', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ten', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('food', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('moo', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('like', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hot', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ears', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('few', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wiggle', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('only', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forgetrare', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('during', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('frantic', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('blessingspeacock', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('elves', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('everyone', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wonder', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kiltwhirlybird', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('jitterbugkennel', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bermudasamusement', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('turkenriddance', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('oceaniancharitable', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dowdycorkscrew', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('evildoer', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('castigateveered', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wieldscuppers', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wealdblink', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('flashbackquonk', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('tutti-frutticantor', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wi-fi', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pitch-black', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ebb', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('doodled', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('everlasting', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('landlinesparrow', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('former', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('easily', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foster', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('shrivellimbering', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('spick-and-span', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('spic-and-span', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('donkeys', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('disband', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('constantbalm', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exciting', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yurt', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('andeanscrawled', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('embrace', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dredged', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('angolacontours', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('economy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wrestle', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('doorjamb', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('darjeelingrecusancy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zamboniblarney', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('glengarrycommissioner', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pothospolysyllabic', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('laudeevo-devo', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('jiggery-pokerysobersides', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('accordaturacavalletti', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('creelboniface', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('efficient', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exhilaration', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('embossed', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('effigy', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('azorestankard', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('emigrate', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zimbabwe', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cul-de-sac', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pell-mell', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forsooth', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('leanderpneumonia', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('xylem', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('aye-aye', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hurdy-gurdy', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cirrhosisbangalore', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('nom', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('feldenkraisbailiwick', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ficusagelicism', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('floruitbunyanesque', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cordillerazazen', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('becquereldarnel', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kyphoplastyaten', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bhikshunisvarabhakti', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('aal', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('puzzlespage', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wow', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hug', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('why', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bow', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('find', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('more', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('four', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('blockheap', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('tug', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wag', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zip', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('rug', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dots', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pat', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pole', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wish', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('state', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('otherbedroom', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('doctor', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drooped', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('shutterscorner', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('worth', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('amishamnesty', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('badgerbailiff', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('chastisechortle', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('contusionconundrum', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('disasternoun', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('edible', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fadeawayfallacy', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fortificationnoun', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dotted', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kenningnoun', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('round-shaped', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('elongated', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('portraitpraise', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('rebuffrecanted', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('excessive', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('short-winged', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('undergirdnoun', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('different', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('virtuallyvisibility', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('whetnoun', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drawl', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('practice', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('amusedpouch', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yesterday', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('doughnut', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('donut', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('poisonous', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drawers', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forearms', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fragrant', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fowl', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('diode', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('droll', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('voraciousnoun', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('affiliateaffluent', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('analepsisanalgesia', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('aughtsaugment', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('binomialbiomimicry', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('busbyadjective', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cathodecattalo', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('circuitouscircumflex', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('consecrateadjective', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cutiscyanosis', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('derelictderisive', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exiguousexodus', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fiduciaryadjective', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('have', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ice', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('formed', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('without', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('lambentlyadjective', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('joy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eats', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foods', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foresight', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('octonocularoctuplicate', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('parabolaparameters', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('perspicaciousadjective', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('show', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('politickpollutant', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('prodigiousprofligacy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('rambunctiousnoun', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('form', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('repercussionrepository', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forcefully', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pei', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cordaunchristened', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('veneernoun', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('vigilvincible', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wootzy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zygotenoun', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eastern', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wok', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dynasty', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('koi', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('deficienciesincarnated', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dilute', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('propitiousellipsis', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('forsook', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('divot', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('haw', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pronaoscraquelure', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('tea', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('agrypniaague', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('made', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('egg', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yolks', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('blottesquebobolink', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('canaillecantatrice', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('colcannonnoun', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('derring-dodeseret', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ichthyologyicosahedron', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ogivalnoun', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('sea', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('parquetparterre', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pralltrillerpratique', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('renvoinoun', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('reddish-brown', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('woman', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fairesbrinz', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('nulliusnoun', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('following', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zugzwangterre', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('vizierialnoun', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eaten', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wood', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cathodecatnap', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fensterfiat', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('palookapannose', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('viscidityw', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('plaaac', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bwlalay', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('siotetro', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('beix', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kmleerac', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('poika', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dlailmnr', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('odlcceroi', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eoaoadldrbl', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('aaccdi', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('kreteloi', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('economic', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('downcastjubilant', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('vindictiveattitudes', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('emotionsword', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dunk', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('drift', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('worldmath', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eagle', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('young', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('women', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('womyn', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wriggle', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('americanaamiably', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('awryb', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('chastisechief', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('condimentsconference', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cookie-cutter', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('doomed', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eclectic', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('effortlesseighth', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('extinctextinguish', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('fractions', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('leisureleotard', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('palatialpallor', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('polarized', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('policy', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('premonitionprevious', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('written', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('regional', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zithersustain', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('worried', 'One Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wrench', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dimple', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exactly', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('twinklesnicker', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('champion', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dodgy', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('bowlerphantom', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wreckage', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('diploma', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('embroiled', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hocus-pocus', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hokus-pokus', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('faminelinoleum', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('advocatoryaerobics', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('beatificbeguile', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('breviloquencenoun', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('capillarycapnometer', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('cohesiveadjectives', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('contrivancecontumelious', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('curiecurmudgeon', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('diatribe', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('diaulos', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('diocese', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('diptych', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('doppler', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dystopiae', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eburnean', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('echidna', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ecuador', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('edwardian', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('existential', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('extrorsef', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('flotusfluoride', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('frass', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('hydriotaphiahydrocortisone', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('jingoismjitney', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('languorouslanolated', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('mea', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('ostensiblyosteopath', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pelagialpelerine', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('posterityposthumous', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pugilistpugnacious', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('resuscitateretina', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('soppinesssousaphone', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('being', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('veritableinterjection', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('yoruba', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zygotea', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('niger-congo', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('eliminate', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('writhes', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('leewardhurly-burly', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foyer', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('foist', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('san', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('pinyondysfunctional', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('emblem', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('effectual', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('aethaliumaffiche', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('propreamphistylar', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('chauve-sourisadjective', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wings', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('couverturecreances', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('doxycycline', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('dysphasiae', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('exchequerf', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('krewekriegspiel', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('mortadellamotherumbung', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('folding', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('podotheca', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('polyandry', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('rescissiblereveille', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wapitiweka', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('xiphophyllous', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zyzomysadjective', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('winegrower', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('atrophyattempt', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('centennialcertiorari', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('chauve-souris', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('potentatepotoroo', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('universalv', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('zyzomys', 'Three Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('polymerized', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('french-derived', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('covid', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('lawmusic', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;
INSERT INTO spelling_words (word, source_difficulty) 
            VALUES ('wheytrademarks', 'Two Bee') 
            ON CONFLICT (word) DO NOTHING;

COMMIT;

-- Verification queries
SELECT 'Total words after safe insert' as description, COUNT(*) as count FROM spelling_words;

SELECT 'Words with source difficulties' as description, COUNT(*) as count 
FROM spelling_words WHERE source_difficulty IS NOT NULL;

SELECT 'Source difficulty distribution' as description, source_difficulty, COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY source_difficulty;