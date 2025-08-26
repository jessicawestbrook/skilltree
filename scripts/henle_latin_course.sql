
-- Insert Latin language if not exists
INSERT INTO languages (id, name, code, flag_emoji, created_at, updated_at)
VALUES (
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Latin',
    'la',
    '🏛️',
    NOW(),
    NOW()
) ON CONFLICT (code) DO NOTHING;

-- Insert language categories

INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Vocabulary',
    'Latin Vocabulary exercises',
    1,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    '22660823-a19f-40d7-8c34-adcd0acd7d7d',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Grammar',
    'Latin Grammar exercises',
    2,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    'c5cd32dc-9651-41b9-a02f-c535e51cc754',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Translation',
    'Latin Translation exercises',
    3,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    '2db6fdf1-ab7b-41fd-8320-3d80c0ed2249',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Reading Comprehension',
    'Latin Reading Comprehension exercises',
    4,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Declensions',
    'Latin Declensions exercises',
    5,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Conjugations',
    'Latin Conjugations exercises',
    6,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Insert Henle Latin course
INSERT INTO language_courses (
    id, language_id, name, description, level, 
    estimated_hours, created_at, updated_at
) VALUES (
    'cebb7f42-e51b-4ac4-8464-29fee0894024',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Henle Latin First Year',
    'A comprehensive Latin course based on Henle First Year Latin textbook',
    'Beginner to Intermediate',
    120,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Insert Latin questions
INSERT INTO language_questions (
    id, language_id, category_id, question_text, question_type,
    options, correct_answer_index, explanation, difficulty_level,
    source_url, created_at, updated_at
) VALUES
(
    '802f4860-9f95-41f0-a757-e1854ae68be7',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'What case is ''puellam''?',
    'multiple_choice',
    ARRAY['Accusative singular', 'Nominative singular', 'Genitive singular', 'Ablative singular'],
    0,
    '''puellam'' is Accusative singular',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '0f535935-474b-4ad1-b923-64bc86d6fd07',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'What case is ''puellae''?',
    'multiple_choice',
    ARRAY['Genitive singular', 'Nominative plural', 'Dative singular', 'Vocative plural'],
    0,
    'Could also be dative singular or nominative plural',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '13cc8de8-106d-406a-8157-b54f9f07437d',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'What case is ''puellis''?',
    'multiple_choice',
    ARRAY['Dative plural', 'Nominative plural', 'Accusative plural', 'Genitive plural'],
    0,
    'Could also be ablative plural',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '2a4262b8-a201-436b-b223-33a7aac0ab5f',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the accusative singular of ''terra''',
    'fill_in_blank',
    ARRAY['terram'],
    0,
    'The accusative singular of ''terra'' is ''terram''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '04025399-c535-4551-86c1-ec72e975922c',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the genitive plural of ''aqua''',
    'fill_in_blank',
    ARRAY['aquarum'],
    0,
    'The genitive plural of ''aqua'' is ''aquarum''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    'd7cfbad0-25cf-4451-a175-9fb2ede8621a',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the dative singular of ''femina''',
    'fill_in_blank',
    ARRAY['feminae'],
    0,
    'The dative singular of ''femina'' is ''feminae''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '006f9acc-88ec-4383-9caf-f56acf8422c7',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''aqua'' mean?',
    'multiple_choice',
    ARRAY['soldier', 'tree', 'water', 'friend'],
    0,
    '''aqua'' means ''water''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '48e29e85-b61e-42aa-bed3-192dded59edf',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''femina'' mean?',
    'multiple_choice',
    ARRAY['road', 'woman', 'friend', 'tree'],
    0,
    '''femina'' means ''woman''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '96296fbd-3409-420d-93cb-6b5c352cc18b',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''porta'' mean?',
    'multiple_choice',
    ARRAY['temple', 'gate', 'friend', 'road'],
    0,
    '''porta'' means ''gate''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    'b0760ee2-0c71-4c0f-923c-54784f41e621',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''puella'' mean?',
    'multiple_choice',
    ARRAY['road', 'house', 'friend', 'girl'],
    0,
    '''puella'' means ''girl''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '6b9a48dc-c390-4cdc-a11c-91442d18b706',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''terra'' mean?',
    'multiple_choice',
    ARRAY['tree', 'book', 'friend', 'land, earth'],
    0,
    '''terra'' means ''land, earth''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '1eb8e546-be94-424f-a14d-01ff23bf37f7',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the genitive singular of ''servus''',
    'fill_in_blank',
    ARRAY['servi'],
    0,
    'The genitive singular of ''servus'' is ''servi''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    '7dbcee0c-a07a-4c5d-b46d-468dabab5c20',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the accusative plural of ''dominus''',
    'fill_in_blank',
    ARRAY['dominos'],
    0,
    'The accusative plural of ''dominus'' is ''dominos''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    '670fdc74-1782-4321-94c1-66f502665863',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the vocative singular of ''filius''',
    'fill_in_blank',
    ARRAY['fili'],
    0,
    'The vocative singular of ''filius'' is ''fili''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    '31081b2e-4a0a-4082-b3b3-ed55ed191981',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the ablative singular of ''amicus''',
    'fill_in_blank',
    ARRAY['amico'],
    0,
    'The ablative singular of ''amicus'' is ''amico''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    'ce67d01f-6a35-4887-ac45-322c911c1071',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '22660823-a19f-40d7-8c34-adcd0acd7d7d',
    'What is special about neuter nouns?',
    'multiple_choice',
    ARRAY['Nominative and accusative are always the same', 'They have no plural forms', 'They only use three cases', 'They never change endings'],
    0,
    'In all neuter nouns, nominative and accusative forms are identical',
    3,
    'Henle First Year Latin - Chapter 3',
    NOW(),
    NOW()
),
(
    '6c4ee2a5-1271-4272-bead-524f40ff5ea6',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '22660823-a19f-40d7-8c34-adcd0acd7d7d',
    'What is the nominative plural ending for neuter nouns?',
    'multiple_choice',
    ARRAY['-a', '-um', '-i', '-os'],
    0,
    'All neuter nouns have -a in nominative and accusative plural',
    3,
    'Henle First Year Latin - Chapter 3',
    NOW(),
    NOW()
),
(
    'e1fdfb23-b80a-4b15-a0bf-83293ec73383',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''I am'' in Latin?',
    'fill_in_blank',
    ARRAY['sum'],
    0,
    '''I am'' is ''sum'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    '4d7e314a-f2ce-42d1-befd-044a6950f944',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''you are (singular)'' in Latin?',
    'fill_in_blank',
    ARRAY['es'],
    0,
    '''you are (singular)'' is ''es'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    '9488d624-4827-475c-a6a9-e84c93ad672e',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''he/she/it is'' in Latin?',
    'fill_in_blank',
    ARRAY['est'],
    0,
    '''he/she/it is'' is ''est'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    '661373d7-7e77-4219-b97e-c6a9305aa1fe',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''we are'' in Latin?',
    'fill_in_blank',
    ARRAY['sumus'],
    0,
    '''we are'' is ''sumus'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    '302dc9c2-4e5e-4549-b2e5-04c7aeba530c',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''they are'' in Latin?',
    'fill_in_blank',
    ARRAY['sunt'],
    0,
    '''they are'' is ''sunt'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    'b66e4465-3316-4052-8f2f-4c29cbc1b8e3',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'What case is ''puellam''?',
    'multiple_choice',
    ARRAY['Accusative singular', 'Nominative singular', 'Genitive singular', 'Ablative singular'],
    0,
    '''puellam'' is Accusative singular',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    'a056734a-e2aa-4abb-acd0-07bdfd1df40f',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'What case is ''puellae''?',
    'multiple_choice',
    ARRAY['Genitive singular', 'Nominative plural', 'Dative singular', 'Vocative plural'],
    0,
    'Could also be dative singular or nominative plural',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '449f4a96-af10-4a3f-b414-a48a7069496a',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'What case is ''puellis''?',
    'multiple_choice',
    ARRAY['Dative plural', 'Nominative plural', 'Accusative plural', 'Genitive plural'],
    0,
    'Could also be ablative plural',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '2224bcd8-6285-4cb4-8b4b-edfbb94d8d91',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the accusative singular of ''terra''',
    'fill_in_blank',
    ARRAY['terram'],
    0,
    'The accusative singular of ''terra'' is ''terram''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '4e166592-a2f4-4c82-bcd4-c889999a73db',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the genitive plural of ''aqua''',
    'fill_in_blank',
    ARRAY['aquarum'],
    0,
    'The genitive plural of ''aqua'' is ''aquarum''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '059911a5-2bcc-42af-9e6a-edca1c9de9ee',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the dative singular of ''femina''',
    'fill_in_blank',
    ARRAY['feminae'],
    0,
    'The dative singular of ''femina'' is ''feminae''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    'ed14a1d7-1f8f-4321-8412-daf2894821dc',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''aqua'' mean?',
    'multiple_choice',
    ARRAY['book', 'water', 'house', 'road'],
    0,
    '''aqua'' means ''water''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '43a2ea4d-3506-423f-afc5-8948e4dfe75d',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''femina'' mean?',
    'multiple_choice',
    ARRAY['woman', 'tree', 'soldier', 'road'],
    0,
    '''femina'' means ''woman''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    'a0a590b4-266c-4d19-81b7-a1c69064e5c5',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''porta'' mean?',
    'multiple_choice',
    ARRAY['book', 'soldier', 'gate', 'temple'],
    0,
    '''porta'' means ''gate''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '1fd83763-69b5-4fd7-8096-2598f4025017',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''puella'' mean?',
    'multiple_choice',
    ARRAY['temple', 'girl', 'road', 'tree'],
    0,
    '''puella'' means ''girl''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '9523cacc-741d-4b54-91db-54864c83be21',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '1b922f3b-71da-490a-a6de-2637b2313c95',
    'What does ''terra'' mean?',
    'multiple_choice',
    ARRAY['friend', 'temple', 'road', 'land, earth'],
    0,
    '''terra'' means ''land, earth''',
    1,
    'Henle First Year Latin - Chapter 1',
    NOW(),
    NOW()
),
(
    '7e55ab02-b66c-45c7-bd89-9f9155104885',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the genitive singular of ''servus''',
    'fill_in_blank',
    ARRAY['servi'],
    0,
    'The genitive singular of ''servus'' is ''servi''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    '65c9eef4-6538-43ac-b2b6-1377efaffbbb',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the accusative plural of ''dominus''',
    'fill_in_blank',
    ARRAY['dominos'],
    0,
    'The accusative plural of ''dominus'' is ''dominos''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    '9032d90b-9998-44a3-9793-9314c82c22a5',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the vocative singular of ''filius''',
    'fill_in_blank',
    ARRAY['fili'],
    0,
    'The vocative singular of ''filius'' is ''fili''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    '51bf6e20-c338-46f2-a34b-89ee0954a507',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'Form the ablative singular of ''amicus''',
    'fill_in_blank',
    ARRAY['amico'],
    0,
    'The ablative singular of ''amicus'' is ''amico''',
    2,
    'Henle First Year Latin - Chapter 2',
    NOW(),
    NOW()
),
(
    '05b080e5-76fa-46bb-8297-a184fc183c58',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '22660823-a19f-40d7-8c34-adcd0acd7d7d',
    'What is special about neuter nouns?',
    'multiple_choice',
    ARRAY['Nominative and accusative are always the same', 'They have no plural forms', 'They only use three cases', 'They never change endings'],
    0,
    'In all neuter nouns, nominative and accusative forms are identical',
    3,
    'Henle First Year Latin - Chapter 3',
    NOW(),
    NOW()
),
(
    '3fcfcc8d-a6b4-4363-81d2-187d1021237a',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    '22660823-a19f-40d7-8c34-adcd0acd7d7d',
    'What is the nominative plural ending for neuter nouns?',
    'multiple_choice',
    ARRAY['-a', '-um', '-i', '-os'],
    0,
    'All neuter nouns have -a in nominative and accusative plural',
    3,
    'Henle First Year Latin - Chapter 3',
    NOW(),
    NOW()
),
(
    '0cd0eb36-3919-4e82-8582-7012b187dd3d',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''I am'' in Latin?',
    'fill_in_blank',
    ARRAY['sum'],
    0,
    '''I am'' is ''sum'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    'df1b19e9-8795-41a1-99c1-665e16ba0c62',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''you are (singular)'' in Latin?',
    'fill_in_blank',
    ARRAY['es'],
    0,
    '''you are (singular)'' is ''es'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    '32981da0-33be-495c-a212-1cdef65c1b0d',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''he/she/it is'' in Latin?',
    'fill_in_blank',
    ARRAY['est'],
    0,
    '''he/she/it is'' is ''est'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    '4dc997ef-64a9-4c1c-a393-c674a207c161',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''we are'' in Latin?',
    'fill_in_blank',
    ARRAY['sumus'],
    0,
    '''we are'' is ''sumus'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
),
(
    'd15ef990-c0da-4faf-b5fc-0b27b8c00c05',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'fdab6231-4268-4518-be85-a4c746e36b6a',
    'How do you say ''they are'' in Latin?',
    'fill_in_blank',
    ARRAY['sunt'],
    0,
    '''they are'' is ''sunt'' in Latin',
    5,
    'Henle First Year Latin - Chapter 5',
    NOW(),
    NOW()
)
ON CONFLICT DO NOTHING;

-- Insert course chapters/modules

INSERT INTO course_modules (
    id, course_id, chapter_number, title, description,
    created_at, updated_at
) VALUES (
    '89108174-0344-4571-8d2e-2d0a885d2463',
    'cebb7f42-e51b-4ac4-8464-29fee0894024',
    1,
    'First Declension Nouns',
    'Introduction to Latin nouns of the first declension',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    'bade845f-b06c-40c2-968f-30d00b8ede08',
    '89108174-0344-4571-8d2e-2d0a885d2463',
    1,
    'Introduction to Latin Cases',
    'lesson',
    '{"text": "\n# Introduction to Latin Cases\n\nLatin is an inflected language, meaning that the endings of words change to show their function in a sentence. Nouns in Latin have six cases:\n\n## The Six Cases\n\n1. **Nominative** - Subject of the sentence\n   - Example: *Puella* cantat. (The girl sings.)\n\n2. **Genitive** - Possession (of, ''s)\n   - Example: Liber *puellae* (The girl''s book)\n\n3. **Dative** - Indirect object (to, for)\n   - Example: Do librum *puellae*. (I give the book to the girl.)\n\n4. **Accusative** - Direct object\n   - Example: Video *puellam*. (I see the girl.)\n\n5. **Ablative** - Various uses (by, with, from, in)\n   - Example: Ambulo cum *puella*. (I walk with the girl.)\n\n6. **Vocative** - Direct address\n   - Example: *Puella*, veni! (Girl, come!)\n\n## Why Cases Matter\n\nUnlike English, which relies on word order, Latin uses these case endings to show relationships between words. This means Latin has much more flexible word order than English.\n                ", "examples": ["Puella aquam portat. (The girl carries water.)", "Aquam puella portat. (The girl carries water.) - Same meaning, different emphasis"], "key_points": ["Case endings show the function of nouns in sentences", "Word order in Latin is flexible", "Each case has specific uses and meanings"]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    '620de514-fd47-4fa9-b6dc-4ae01cf8598e',
    '89108174-0344-4571-8d2e-2d0a885d2463',
    2,
    'First Declension Endings',
    'lesson',
    '{"text": "\n# First Declension Endings\n\nThe first declension includes mostly feminine nouns ending in -a. Here are the endings:\n\n## Singular\n- Nominative: -a\n- Genitive: -ae\n- Dative: -ae\n- Accusative: -am\n- Ablative: -\u0101 (long a)\n- Vocative: -a\n\n## Plural\n- Nominative: -ae\n- Genitive: -\u0101rum\n- Dative: -\u012bs\n- Accusative: -\u0101s\n- Ablative: -\u012bs\n- Vocative: -ae\n\n## Example: puella (girl)\n\n### Singular\n- Nom: puella (the girl - subject)\n- Gen: puellae (of the girl)\n- Dat: puellae (to/for the girl)\n- Acc: puellam (the girl - object)\n- Abl: puell\u0101 (by/with/from the girl)\n- Voc: puella (O girl!)\n\n### Plural\n- Nom: puellae (the girls - subject)\n- Gen: puell\u0101rum (of the girls)\n- Dat: puell\u012bs (to/for the girls)\n- Acc: puell\u0101s (the girls - object)\n- Abl: puell\u012bs (by/with/from the girls)\n- Voc: puellae (O girls!)\n                ", "examples": ["terra, terrae (f.) - land, earth", "aqua, aquae (f.) - water", "femina, feminae (f.) - woman", "porta, portae (f.) - gate"], "key_points": ["Most first declension nouns are feminine", "The genitive singular ending -ae identifies first declension", "Some endings are the same (dative and ablative plural)"]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Link questions to section: Practice: First Declension Cases

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', 'b66e4465-3316-4052-8f2f-4c29cbc1b8e3', 1)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', 'a056734a-e2aa-4abb-acd0-07bdfd1df40f', 2)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', '449f4a96-af10-4a3f-b414-a48a7069496a', 3)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', '2224bcd8-6285-4cb4-8b4b-edfbb94d8d91', 4)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', '4e166592-a2f4-4c82-bcd4-c889999a73db', 5)
ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    '9c09ab68-d23b-4434-842f-988e91521ab6',
    '89108174-0344-4571-8d2e-2d0a885d2463',
    4,
    'Chapter 1 Vocabulary',
    'lesson',
    '{"text": "\n# Chapter 1 Vocabulary\n\n## First Declension Nouns\n\n1. **aqua, aquae** (f.) - water\n2. **femina, feminae** (f.) - woman\n3. **patria, patriae** (f.) - fatherland, country\n4. **porta, portae** (f.) - gate\n5. **puella, puellae** (f.) - girl\n6. **terra, terrae** (f.) - land, earth\n7. **vita, vitae** (f.) - life\n\n## Verbs (Preview)\n\n1. **porto, portare** - to carry\n2. **laudo, laudare** - to praise\n3. **amo, amare** - to love\n\n## Prepositions\n\n1. **in** + ablative - in, on\n2. **in** + accusative - into\n3. **cum** + ablative - with\n                ", "vocabulary_list": [{"latin": "aqua", "english": "water", "gender": "f", "declension": "1st"}, {"latin": "femina", "english": "woman", "gender": "f", "declension": "1st"}, {"latin": "patria", "english": "fatherland", "gender": "f", "declension": "1st"}, {"latin": "porta", "english": "gate", "gender": "f", "declension": "1st"}, {"latin": "puella", "english": "girl", "gender": "f", "declension": "1st"}, {"latin": "terra", "english": "land", "gender": "f", "declension": "1st"}, {"latin": "vita", "english": "life", "gender": "f", "declension": "1st"}]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Link questions to section: Vocabulary Practice

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', 'ed14a1d7-1f8f-4321-8412-daf2894821dc', 1)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', '43a2ea4d-3506-423f-afc5-8948e4dfe75d', 2)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', 'a0a590b4-266c-4d19-81b7-a1c69064e5c5', 3)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', '1fd83763-69b5-4fd7-8096-2598f4025017', 4)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('89108174-0344-4571-8d2e-2d0a885d2463', '9523cacc-741d-4b54-91db-54864c83be21', 5)
ON CONFLICT DO NOTHING;

INSERT INTO course_modules (
    id, course_id, chapter_number, title, description,
    created_at, updated_at
) VALUES (
    'd5fb4522-b4f3-48ec-8f46-0cd6947a1c44',
    'cebb7f42-e51b-4ac4-8464-29fee0894024',
    2,
    'Second Declension Masculine Nouns',
    'Learn masculine nouns of the second declension',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    '027f09e1-6a73-4b6e-bae0-9e98fca07da2',
    'd5fb4522-b4f3-48ec-8f46-0cd6947a1c44',
    1,
    'Second Declension Masculine',
    'lesson',
    '{"text": "\n# Second Declension Masculine Nouns\n\nThe second declension includes mostly masculine nouns ending in -us or -er.\n\n## Endings for -us nouns\n\n### Singular\n- Nominative: -us\n- Genitive: -\u012b\n- Dative: -\u014d\n- Accusative: -um\n- Ablative: -\u014d\n- Vocative: -e\n\n### Plural\n- Nominative: -\u012b\n- Genitive: -\u014drum\n- Dative: -\u012bs\n- Accusative: -\u014ds\n- Ablative: -\u012bs\n- Vocative: -\u012b\n\n## Example: servus (slave, servant)\n\n### Singular\n- Nom: servus (the slave)\n- Gen: serv\u012b (of the slave)\n- Dat: serv\u014d (to/for the slave)\n- Acc: servum (the slave - object)\n- Abl: serv\u014d (by/with/from the slave)\n- Voc: serve (O slave!)\n\n### Plural\n- Nom: serv\u012b (the slaves)\n- Gen: serv\u014drum (of the slaves)\n- Dat: serv\u012bs (to/for the slaves)\n- Acc: serv\u014ds (the slaves - object)\n- Abl: serv\u012bs (by/with/from the slaves)\n- Voc: serv\u012b (O slaves!)\n                ", "examples": ["dominus, domin\u012b (m.) - master, lord", "filius, fili\u012b (m.) - son", "amicus, amic\u012b (m.) - friend"], "key_points": ["Second declension -us nouns are mostly masculine", "The genitive singular ending -\u012b identifies second declension", "Vocative singular has special ending -e"]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    'aaec9c2a-4fdc-4dd0-a201-3d09a7693a55',
    'd5fb4522-b4f3-48ec-8f46-0cd6947a1c44',
    2,
    'Second Declension -er Nouns',
    'lesson',
    '{"text": "\n# Second Declension -er Nouns\n\nSome second declension masculine nouns end in -er. They follow the same pattern except in the nominative and vocative singular.\n\n## Two types of -er nouns:\n\n1. **Those that keep the e**: puer, puer\u012b (boy)\n2. **Those that drop the e**: ager, agr\u012b (field)\n\n## Example: puer (boy) - keeps the e\n\n### Singular\n- Nom: puer\n- Gen: puer\u012b\n- Dat: puer\u014d\n- Acc: puerum\n- Abl: puer\u014d\n- Voc: puer\n\n## Example: ager (field) - drops the e\n\n### Singular\n- Nom: ager\n- Gen: agr\u012b (note: no e!)\n- Dat: agr\u014d\n- Acc: agrum\n- Abl: agr\u014d\n- Voc: ager\n\nThe genitive tells you whether to keep or drop the e in other forms.\n                ", "examples": ["liber, libr\u012b (m.) - book (drops e)", "magister, magistr\u012b (m.) - teacher (drops e)", "vir, vir\u012b (m.) - man (irregular)"]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Link questions to section: Practice: Second Declension Masculine

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('d5fb4522-b4f3-48ec-8f46-0cd6947a1c44', '7e55ab02-b66c-45c7-bd89-9f9155104885', 1)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('d5fb4522-b4f3-48ec-8f46-0cd6947a1c44', '65c9eef4-6538-43ac-b2b6-1377efaffbbb', 2)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('d5fb4522-b4f3-48ec-8f46-0cd6947a1c44', '9032d90b-9998-44a3-9793-9314c82c22a5', 3)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('d5fb4522-b4f3-48ec-8f46-0cd6947a1c44', '51bf6e20-c338-46f2-a34b-89ee0954a507', 4)
ON CONFLICT DO NOTHING;

INSERT INTO course_modules (
    id, course_id, chapter_number, title, description,
    created_at, updated_at
) VALUES (
    'e7373367-fb9d-44f5-a1ff-add91acd11e7',
    'cebb7f42-e51b-4ac4-8464-29fee0894024',
    3,
    'Second Declension Neuter Nouns',
    'Learn neuter nouns of the second declension',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    'e2ec7883-e016-442e-8853-8d4d1f5ff4c0',
    'e7373367-fb9d-44f5-a1ff-add91acd11e7',
    1,
    'Second Declension Neuter',
    'lesson',
    '{"text": "\n# Second Declension Neuter Nouns\n\nNeuter nouns of the second declension end in -um. They follow a similar pattern to masculine nouns with important differences.\n\n## Key Rule for All Neuter Nouns\n**Nominative and Accusative are always the same!**\n**Nominative and Accusative plural always end in -a!**\n\n## Endings\n\n### Singular\n- Nominative: -um\n- Genitive: -\u012b\n- Dative: -\u014d\n- Accusative: -um (same as nominative!)\n- Ablative: -\u014d\n- Vocative: -um\n\n### Plural\n- Nominative: -a\n- Genitive: -\u014drum\n- Dative: -\u012bs\n- Accusative: -a (same as nominative!)\n- Ablative: -\u012bs\n- Vocative: -a\n\n## Example: bellum (war)\n\n### Singular\n- Nom: bellum\n- Gen: bell\u012b\n- Dat: bell\u014d\n- Acc: bellum\n- Abl: bell\u014d\n- Voc: bellum\n\n### Plural\n- Nom: bella\n- Gen: bell\u014drum\n- Dat: bell\u012bs\n- Acc: bella\n- Abl: bell\u012bs\n- Voc: bella\n                ", "examples": ["oppidum, oppid\u012b (n.) - town", "regnum, regn\u012b (n.) - kingdom", "donum, don\u012b (n.) - gift"]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Link questions to section: Practice: Neuter Nouns

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('e7373367-fb9d-44f5-a1ff-add91acd11e7', '05b080e5-76fa-46bb-8297-a184fc183c58', 1)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('e7373367-fb9d-44f5-a1ff-add91acd11e7', '3fcfcc8d-a6b4-4363-81d2-187d1021237a', 2)
ON CONFLICT DO NOTHING;

INSERT INTO course_modules (
    id, course_id, chapter_number, title, description,
    created_at, updated_at
) VALUES (
    'de185630-f066-4d99-bf31-18ca759823c2',
    'cebb7f42-e51b-4ac4-8464-29fee0894024',
    4,
    'Adjectives of First and Second Declension',
    'Learn how adjectives agree with nouns',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    '7d6debf1-88c1-41d2-96a3-66a96ba9e8ff',
    'de185630-f066-4d99-bf31-18ca759823c2',
    1,
    'Adjective Agreement',
    'lesson',
    '{"text": "\n# Adjectives of First and Second Declension\n\nAdjectives must agree with the nouns they modify in:\n- **Gender** (masculine, feminine, neuter)\n- **Number** (singular, plural)\n- **Case** (nominative, genitive, etc.)\n\n## Forms of bonus, bona, bonum (good)\n\n### Masculine (2nd declension)\n- Nom: bonus\n- Gen: bon\u012b\n- Dat: bon\u014d\n- Acc: bonum\n- Abl: bon\u014d\n\n### Feminine (1st declension)\n- Nom: bona\n- Gen: bonae\n- Dat: bonae\n- Acc: bonam\n- Abl: bon\u0101\n\n### Neuter (2nd declension)\n- Nom: bonum\n- Gen: bon\u012b\n- Dat: bon\u014d\n- Acc: bonum\n- Abl: bon\u014d\n\n## Examples of Agreement\n\n- **Masculine**: servus bonus (good slave)\n- **Feminine**: puella bona (good girl)\n- **Neuter**: bellum bonum (good war)\n\nThe adjective changes its ending to match the noun!\n                ", "examples": ["magnus, magna, magnum - large, great", "parvus, parva, parvum - small", "malus, mala, malum - bad, evil"]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO course_modules (
    id, course_id, chapter_number, title, description,
    created_at, updated_at
) VALUES (
    '93b77afe-a8d5-4d81-8703-78ee474725a5',
    'cebb7f42-e51b-4ac4-8464-29fee0894024',
    5,
    'The Verb Sum (to be)',
    'Learn the present tense of the important irregular verb sum',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    '169e8cb0-dbcc-46e6-bf9f-5c0fc55db5db',
    '93b77afe-a8d5-4d81-8703-78ee474725a5',
    1,
    'Present Tense of Sum',
    'lesson',
    '{"text": "\n# The Verb Sum (to be)\n\nSum is one of the most important and most irregular verbs in Latin.\n\n## Present Tense\n\n### Singular\n- 1st person: **sum** (I am)\n- 2nd person: **es** (you are)\n- 3rd person: **est** (he/she/it is)\n\n### Plural\n- 1st person: **sumus** (we are)\n- 2nd person: **estis** (you are)\n- 3rd person: **sunt** (they are)\n\n## Usage\n\nSum is used:\n1. To show existence: *Est puella.* (There is a girl.)\n2. With predicate nominatives: *Puella est bona.* (The girl is good.)\n3. To show location: *In terra sunt.* (They are on the land.)\n\n## Important: Predicate Nominatives\n\nWhen sum links two nouns or a noun and adjective, both are in the nominative case:\n- *Marcus est servus.* (Marcus is a slave.) - Both Marcus and servus are nominative\n- *Puellae sunt bonae.* (The girls are good.) - Both match in nominative plural\n                ", "examples": ["Sum discipulus. (I am a student.)", "Estis amici. (You are friends.)", "Bella sunt mala. (Wars are bad.)"]}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Link questions to section: Practice: Sum

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('93b77afe-a8d5-4d81-8703-78ee474725a5', '0cd0eb36-3919-4e82-8582-7012b187dd3d', 1)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('93b77afe-a8d5-4d81-8703-78ee474725a5', 'df1b19e9-8795-41a1-99c1-665e16ba0c62', 2)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('93b77afe-a8d5-4d81-8703-78ee474725a5', '32981da0-33be-495c-a212-1cdef65c1b0d', 3)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('93b77afe-a8d5-4d81-8703-78ee474725a5', '4dc997ef-64a9-4c1c-a393-c674a207c161', 4)
ON CONFLICT DO NOTHING;

INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('93b77afe-a8d5-4d81-8703-78ee474725a5', 'd15ef990-c0da-4faf-b5fc-0b27b8c00c05', 5)
ON CONFLICT DO NOTHING;
