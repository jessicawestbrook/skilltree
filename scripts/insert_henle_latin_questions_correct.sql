-- Insert Henle Latin First Year Questions
-- Total questions: 40
-- Using correct_answer as integer index (0-based)

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'ed106008-b5b5-4129-81d2-b88439f8058e',
    'What is the genitive singular ending for first declension nouns?',
    ARRAY['-a', '-ae', '-am', '-ā']::text[],
    1,
    'First declension nouns have -ae as their genitive singular ending. This is the key identifier of first declension.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '9b2cce89-29e0-47a0-b501-b11c669d5b9b',
    'Translate ''puella'' into English:',
    ARRAY['boy', 'girl', 'woman', 'man']::text[],
    1,
    'Puella means ''girl'' in Latin. It''s a common first declension noun.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'e590d62d-c7e4-4896-91ec-723a873e45a2',
    'Which case is ''puellārum''?',
    ARRAY['Nominative singular', 'Genitive singular', 'Genitive plural', 'Accusative plural']::text[],
    2,
    'The ending -ārum indicates genitive plural in the first declension.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '11b1dcfe-ee80-4614-84b2-a5f2e48718ac',
    'What is the nominative plural of ''porta'' (gate)?',
    ARRAY['portae', 'portās', 'portārum', 'portīs']::text[],
    0,
    'First declension nominative plural ends in -ae.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '98cfdc59-edec-4092-9912-77365794f523',
    'In ''Puella rosam habet'', what case is ''rosam''?',
    ARRAY['Nominative', 'Genitive', 'Dative', 'Accusative']::text[],
    3,
    'Rosam ends in -am, which is the accusative singular ending for first declension. It''s the direct object.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '4e8687d1-39a0-446a-976f-c2ecca531292',
    'Which of these is a first declension noun?',
    ARRAY['dominus', 'bellum', 'aqua', 'puer']::text[],
    2,
    'Aqua (water) is a first declension noun, ending in -a in the nominative.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'd417990e-eda7-4905-9311-46407672bad9',
    'What is the ablative singular ending for first declension?',
    ARRAY['-a', '-ae', '-ā', '-īs']::text[],
    2,
    'First declension ablative singular has a long -ā ending.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'e18d04f3-13d3-4a4b-8fc6-38de22043239',
    'Translate ''fēminae'' (genitive singular):',
    ARRAY['of the woman', 'to the woman', 'the women', 'by the woman']::text[],
    0,
    'Genitive case shows possession: ''of the woman''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'd58ce776-9e1f-4f80-8572-4fe6133d26c5',
    'What is the genitive singular ending for second declension masculine nouns?',
    ARRAY['-us', '-ī', '-um', '-ō']::text[],
    1,
    'Second declension masculine nouns have -ī as their genitive singular ending.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '26d6ce3d-47fe-4300-a21f-b1394fc277a5',
    'What is the nominative plural of ''servus'' (slave)?',
    ARRAY['servī', 'servōs', 'servum', 'servōrum']::text[],
    0,
    'Second declension masculine nominative plural ends in -ī.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '1d8a4071-9c46-423d-a2c4-fb66d362a6bc',
    'Translate ''amīcus'' into English:',
    ARRAY['enemy', 'friend', 'soldier', 'master']::text[],
    1,
    'Amīcus means ''friend'' in Latin.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '3fe98828-2a6d-46b0-b726-32111f93f987',
    'In ''Dominus servum videt'', what case is ''servum''?',
    ARRAY['Nominative', 'Genitive', 'Accusative', 'Ablative']::text[],
    2,
    'Servum ends in -um, which is the accusative singular for second declension masculine.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'ac450953-2bc3-4d21-9610-8570286268ab',
    'Which form is the vocative singular of ''fīlius'' (son)?',
    ARRAY['fīlie', 'fīlī', 'fīlius', 'fīliī']::text[],
    1,
    'Second declension nouns ending in -ius have vocative singular in -ī (not -ie).',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '9b22ec92-2101-403c-8458-998c1cf5602b',
    'What is the dative plural of ''deus'' (god)?',
    ARRAY['deīs', 'deōs', 'deōrum', 'deī']::text[],
    0,
    'Second declension dative/ablative plural ends in -īs.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'fc675238-24f0-46d0-a4dc-02b9f31b1e83',
    'Which ending indicates second declension masculine accusative plural?',
    ARRAY['-ōs', '-ās', '-a', '-ēs']::text[],
    0,
    'Second declension masculine accusative plural ends in -ōs.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '6bcaeedb-e6d0-40c1-9397-85d6cfd56cda',
    'Translate ''equus'':',
    ARRAY['foot soldier', 'horse', 'rider', 'chariot']::text[],
    1,
    'Equus means ''horse'' in Latin.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '857d5121-2c25-4511-b74c-14c8a5501c36',
    'What is the nominative plural ending for second declension neuter nouns?',
    ARRAY['-a', '-ī', '-um', '-ōrum']::text[],
    0,
    'Second declension neuter nouns have -a as their nominative AND accusative plural ending.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '5be91b39-79bb-4672-bd76-f10de963ed3d',
    'Translate ''bellum'' into English:',
    ARRAY['beautiful', 'war', 'good', 'book']::text[],
    1,
    'Bellum means ''war'' in Latin. It''s a common second declension neuter noun.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'c7d1d895-5bb6-4c2c-a66c-3a2a0de5f26a',
    'What cases are always the same in neuter nouns?',
    ARRAY['Nominative and Genitive', 'Nominative and Accusative', 'Genitive and Dative', 'Dative and Ablative']::text[],
    1,
    'In all neuter nouns, the nominative and accusative forms are identical.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'd6841256-2150-451c-917e-a246c0dd6d6a',
    'What is the genitive plural of ''dōnum'' (gift)?',
    ARRAY['dōna', 'dōnī', 'dōnōrum', 'dōnīs']::text[],
    2,
    'Second declension genitive plural is -ōrum for both masculine and neuter.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '4e00a99e-7728-4799-9966-0549de493eb3',
    'In ''Templa magna sunt'', what case is ''templa''?',
    ARRAY['Nominative singular', 'Nominative plural', 'Accusative singular', 'Accusative plural']::text[],
    1,
    'Templa with -a ending is nominative plural (subject). ''Sunt'' (are) confirms plural.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '3a70c1ef-a5c7-49a9-bcf2-e74653b539e3',
    'What is the ablative singular of ''verbum'' (word)?',
    ARRAY['verbō', 'verbī', 'verbīs', 'verba']::text[],
    0,
    'Second declension neuter ablative singular ends in -ō.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'fc576d86-c7bc-4251-ad22-134c0c5ebabb',
    'Which is a neuter second declension noun?',
    ARRAY['hortus', 'oppidum', 'servus', 'dominus']::text[],
    1,
    'Oppidum (town) is neuter, ending in -um.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'c1c3bf31-d605-4b8e-9ce5-31a5008d067f',
    'Translate ''rēgnum'':',
    ARRAY['king', 'queen', 'kingdom', 'royal']::text[],
    2,
    'Rēgnum means ''kingdom'' in Latin.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '0cb2b691-09f8-474f-a756-3a4a2ad01bbe',
    'What is the first person singular present of ''sum'' (to be)?',
    ARRAY['sum', 'es', 'est', 'sunt']::text[],
    0,
    'Sum means ''I am'' - first person singular present.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'f86042c5-d77f-4487-b8e0-99f3476ddbee',
    'Translate ''sunt'' into English:',
    ARRAY['I am', 'you are', 'he/she/it is', 'they are']::text[],
    3,
    'Sunt is third person plural: ''they are''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '25f5b450-c831-4c53-89bf-1585df553259',
    'What is the second person singular of ''sum''?',
    ARRAY['sum', 'es', 'est', 'sumus']::text[],
    1,
    'Es means ''you are'' (singular).',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'bb9ec6ce-5ccd-4bf9-91b6-d1c3f467fc95',
    'Complete: ''Nōs ___ amīcī'' (We are friends)',
    ARRAY['sum', 'es', 'sumus', 'sunt']::text[],
    2,
    'Sumus is first person plural: ''we are''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '01c25b4f-d600-4611-9c4e-c2529c2a1d53',
    'In ''Puellae in hortō sunt'', what does ''sunt'' indicate about ''puellae''?',
    ARRAY['It''s singular', 'It''s plural', 'It''s feminine', 'It''s accusative']::text[],
    1,
    'Sunt (they are) confirms that puellae is plural.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'eb27b59a-abd6-436b-8309-8c0f39afeee9',
    'What is the second person plural of ''sum''?',
    ARRAY['estis', 'sunt', 'sumus', 'es']::text[],
    0,
    'Estis means ''you (all) are'' - second person plural.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '21ddb2c1-4175-4318-811b-eb58da0f64aa',
    'Translate ''Est bonus'':',
    ARRAY['I am good', 'You are good', 'He is good', 'They are good']::text[],
    2,
    'Est (he/she/it is) bonus (good) = ''He is good''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '02872850-3ab1-4ebc-9a9d-b68475f6ff36',
    'Which form means ''we are''?',
    ARRAY['sum', 'sumus', 'sunt', 'estis']::text[],
    1,
    'Sumus is first person plural: ''we are''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'd91add38-31c0-423e-ac8b-51f47a0d7dd0',
    'What is the first person singular present of ''amō'' (to love)?',
    ARRAY['amō', 'amās', 'amat', 'amant']::text[],
    0,
    'Amō means ''I love'' - the first person singular keeps the -ō ending.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '2485087a-9964-4cc0-8e45-556b5cc0fe42',
    'What is the infinitive ending for first conjugation verbs?',
    ARRAY['-ō', '-āre', '-ēre', '-ere']::text[],
    1,
    'First conjugation infinitives end in -āre (long a).',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'e3108b7a-4893-4ef4-bc89-8d1fd653a4bb',
    'Translate ''laborant'' into English:',
    ARRAY['I work', 'you work', 'he works', 'they work']::text[],
    3,
    'The -ant ending indicates third person plural: ''they work''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'd57f4296-19af-41ce-83df-850edec02cb0',
    'What is the third person singular of ''portō'' (to carry)?',
    ARRAY['portō', 'portās', 'portat', 'portant']::text[],
    2,
    'Third person singular of first conjugation ends in -at.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '8f3daf64-07ee-4f0d-a7dc-30440431bbb0',
    'In ''Puella cantat'', what person and number is ''cantat''?',
    ARRAY['1st singular', '2nd singular', '3rd singular', '3rd plural']::text[],
    2,
    'The -at ending shows third person singular: ''she sings''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'f64ed20d-4479-4b67-83bf-0222ceab0e7e',
    'What is the second person plural of ''laudō'' (to praise)?',
    ARRAY['laudās', 'laudat', 'laudātis', 'laudant']::text[],
    2,
    'Second person plural of first conjugation ends in -ātis.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    'a66a1224-83eb-4ca2-a4d6-c054da48e678',
    'Which ending shows first person plural in first conjugation?',
    ARRAY['-āmus', '-ātis', '-ant', '-ō']::text[],
    0,
    'First person plural ends in -āmus: ''we [verb]''.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '4d39b02a-cb33-4b16-acc4-6e5a0ff66bb5',
    'Translate ''vocās'':',
    ARRAY['I call', 'you call', 'he calls', 'they call']::text[],
    1,
    'The -ās ending is second person singular.',
    'easy',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;
