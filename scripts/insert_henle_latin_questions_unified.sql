-- Insert Henle Latin First Year Questions into unified questions table
-- Total questions: 40
-- These use the same table as assessment questions

INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '51d0472d-2792-4c60-b735-bbced96a2182',
    'What is the genitive singular ending for first declension nouns?',
    ARRAY['-a', '-ae', '-am', '-ā']::text[],
    '-ae',
    'First declension nouns have -ae as their genitive singular ending. This is the key identifier of first declension.',
    'beginner',
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
    '0e4e72c9-f2ad-462d-9917-ec224cc7480c',
    'Translate ''puella'' into English:',
    ARRAY['boy', 'girl', 'woman', 'man']::text[],
    'girl',
    'Puella means ''girl'' in Latin. It''s a common first declension noun.',
    'beginner',
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
    '3277f24b-e58c-4597-8221-c24c8c1ca210',
    'Which case is ''puellārum''?',
    ARRAY['Nominative singular', 'Genitive singular', 'Genitive plural', 'Accusative plural']::text[],
    'Genitive plural',
    'The ending -ārum indicates genitive plural in the first declension.',
    'beginner',
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
    'a6dfce9b-dbc1-4635-b192-453fd9957b5e',
    'What is the nominative plural of ''porta'' (gate)?',
    ARRAY['portae', 'portās', 'portārum', 'portīs']::text[],
    'portae',
    'First declension nominative plural ends in -ae.',
    'beginner',
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
    '5d7aab4e-f2b3-408e-8773-b016037a5da3',
    'In ''Puella rosam habet'', what case is ''rosam''?',
    ARRAY['Nominative', 'Genitive', 'Dative', 'Accusative']::text[],
    'Accusative',
    'Rosam ends in -am, which is the accusative singular ending for first declension. It''s the direct object.',
    'beginner',
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
    'a4acf73b-467f-48d7-8636-fc5e341aac36',
    'Which of these is a first declension noun?',
    ARRAY['dominus', 'bellum', 'aqua', 'puer']::text[],
    'aqua',
    'Aqua (water) is a first declension noun, ending in -a in the nominative.',
    'beginner',
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
    '947bd7c9-0df6-46bf-88f0-a42ba87e1303',
    'What is the ablative singular ending for first declension?',
    ARRAY['-a', '-ae', '-ā', '-īs']::text[],
    '-ā',
    'First declension ablative singular has a long -ā ending.',
    'beginner',
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
    'b4e72e13-0afa-4f76-aaa2-b2d00ca07d22',
    'Translate ''fēminae'' (genitive singular):',
    ARRAY['of the woman', 'to the woman', 'the women', 'by the woman']::text[],
    'of the woman',
    'Genitive case shows possession: ''of the woman''.',
    'beginner',
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
    'ab706f00-fbeb-46f9-8397-278c6ba7f109',
    'What is the genitive singular ending for second declension masculine nouns?',
    ARRAY['-us', '-ī', '-um', '-ō']::text[],
    '-ī',
    'Second declension masculine nouns have -ī as their genitive singular ending.',
    'beginner',
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
    'e2edef3d-1c25-4247-8eea-1f2326b5e1bd',
    'What is the nominative plural of ''servus'' (slave)?',
    ARRAY['servī', 'servōs', 'servum', 'servōrum']::text[],
    'servī',
    'Second declension masculine nominative plural ends in -ī.',
    'beginner',
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
    '72ff5972-625b-4591-a3f1-b103f037439c',
    'Translate ''amīcus'' into English:',
    ARRAY['enemy', 'friend', 'soldier', 'master']::text[],
    'friend',
    'Amīcus means ''friend'' in Latin.',
    'beginner',
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
    'f493b075-fc7f-4e22-b9d4-f51e4d04355b',
    'In ''Dominus servum videt'', what case is ''servum''?',
    ARRAY['Nominative', 'Genitive', 'Accusative', 'Ablative']::text[],
    'Accusative',
    'Servum ends in -um, which is the accusative singular for second declension masculine.',
    'beginner',
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
    '2649423f-2377-4532-969d-a2d311324581',
    'Which form is the vocative singular of ''fīlius'' (son)?',
    ARRAY['fīlie', 'fīlī', 'fīlius', 'fīliī']::text[],
    'fīlī',
    'Second declension nouns ending in -ius have vocative singular in -ī (not -ie).',
    'beginner',
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
    '9e6b4a28-af3b-4720-8245-717a6b103f2e',
    'What is the dative plural of ''deus'' (god)?',
    ARRAY['deīs', 'deōs', 'deōrum', 'deī']::text[],
    'deīs',
    'Second declension dative/ablative plural ends in -īs.',
    'beginner',
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
    '378ca82b-ad36-4bd5-8b49-e01d2ac9c0cf',
    'Which ending indicates second declension masculine accusative plural?',
    ARRAY['-ōs', '-ās', '-a', '-ēs']::text[],
    '-ōs',
    'Second declension masculine accusative plural ends in -ōs.',
    'beginner',
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
    '7c359896-959a-4541-b7a3-336c01b3b47d',
    'Translate ''equus'':',
    ARRAY['foot soldier', 'horse', 'rider', 'chariot']::text[],
    'horse',
    'Equus means ''horse'' in Latin.',
    'beginner',
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
    '8c690156-9bce-49fc-9747-78244abf52b5',
    'What is the nominative plural ending for second declension neuter nouns?',
    ARRAY['-a', '-ī', '-um', '-ōrum']::text[],
    '-a',
    'Second declension neuter nouns have -a as their nominative AND accusative plural ending.',
    'beginner',
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
    'afc8277d-4c83-45fb-a4d3-6475342c22bb',
    'Translate ''bellum'' into English:',
    ARRAY['beautiful', 'war', 'good', 'book']::text[],
    'war',
    'Bellum means ''war'' in Latin. It''s a common second declension neuter noun.',
    'beginner',
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
    '1cc2c929-f320-46f7-b51a-4ec6a5a6cb6e',
    'What cases are always the same in neuter nouns?',
    ARRAY['Nominative and Genitive', 'Nominative and Accusative', 'Genitive and Dative', 'Dative and Ablative']::text[],
    'Nominative and Accusative',
    'In all neuter nouns, the nominative and accusative forms are identical.',
    'beginner',
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
    'fba306d6-2b8d-406f-bd2b-828c6076f46c',
    'What is the genitive plural of ''dōnum'' (gift)?',
    ARRAY['dōna', 'dōnī', 'dōnōrum', 'dōnīs']::text[],
    'dōnōrum',
    'Second declension genitive plural is -ōrum for both masculine and neuter.',
    'beginner',
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
    'fe3f7824-ff98-4d3f-b604-775f512c84eb',
    'In ''Templa magna sunt'', what case is ''templa''?',
    ARRAY['Nominative singular', 'Nominative plural', 'Accusative singular', 'Accusative plural']::text[],
    'Nominative plural',
    'Templa with -a ending is nominative plural (subject). ''Sunt'' (are) confirms plural.',
    'beginner',
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
    '72e4535b-468a-4819-9d9b-3379d082d86d',
    'What is the ablative singular of ''verbum'' (word)?',
    ARRAY['verbō', 'verbī', 'verbīs', 'verba']::text[],
    'verbō',
    'Second declension neuter ablative singular ends in -ō.',
    'beginner',
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
    'cdfda1b7-6cad-48d5-8dce-c5a0b96631e4',
    'Which is a neuter second declension noun?',
    ARRAY['hortus', 'oppidum', 'servus', 'dominus']::text[],
    'oppidum',
    'Oppidum (town) is neuter, ending in -um.',
    'beginner',
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
    '4b2056f7-f368-409e-b230-81c8154dbaa0',
    'Translate ''rēgnum'':',
    ARRAY['king', 'queen', 'kingdom', 'royal']::text[],
    'kingdom',
    'Rēgnum means ''kingdom'' in Latin.',
    'beginner',
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
    '656ce3c9-9c72-4137-825a-d6daaca39b61',
    'What is the first person singular present of ''sum'' (to be)?',
    ARRAY['sum', 'es', 'est', 'sunt']::text[],
    'sum',
    'Sum means ''I am'' - first person singular present.',
    'beginner',
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
    '5873cd30-0e8d-4d16-a73e-d2f0b3682d84',
    'Translate ''sunt'' into English:',
    ARRAY['I am', 'you are', 'he/she/it is', 'they are']::text[],
    'they are',
    'Sunt is third person plural: ''they are''.',
    'beginner',
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
    'ab136bbe-6c02-4f0a-836a-57fbd3f76392',
    'What is the second person singular of ''sum''?',
    ARRAY['sum', 'es', 'est', 'sumus']::text[],
    'es',
    'Es means ''you are'' (singular).',
    'beginner',
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
    '208da382-bba0-4e11-bc48-c72f42713ca9',
    'Complete: ''Nōs ___ amīcī'' (We are friends)',
    ARRAY['sum', 'es', 'sumus', 'sunt']::text[],
    'sumus',
    'Sumus is first person plural: ''we are''.',
    'beginner',
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
    '46db5373-bd1f-45a5-b002-e80064bbc114',
    'In ''Puellae in hortō sunt'', what does ''sunt'' indicate about ''puellae''?',
    ARRAY['It''s singular', 'It''s plural', 'It''s feminine', 'It''s accusative']::text[],
    'It''s plural',
    'Sunt (they are) confirms that puellae is plural.',
    'beginner',
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
    'b443bf9b-e8f4-43f8-9fc4-1192c5a49197',
    'What is the second person plural of ''sum''?',
    ARRAY['estis', 'sunt', 'sumus', 'es']::text[],
    'estis',
    'Estis means ''you (all) are'' - second person plural.',
    'beginner',
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
    '74704d83-0e33-4c70-b929-8bcbb13668b8',
    'Translate ''Est bonus'':',
    ARRAY['I am good', 'You are good', 'He is good', 'They are good']::text[],
    'He is good',
    'Est (he/she/it is) bonus (good) = ''He is good''.',
    'beginner',
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
    'f9442db0-4d97-41e0-8fae-49ef25198332',
    'Which form means ''we are''?',
    ARRAY['sum', 'sumus', 'sunt', 'estis']::text[],
    'sumus',
    'Sumus is first person plural: ''we are''.',
    'beginner',
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
    '181d62fc-807b-46c2-ab28-b22700167e7c',
    'What is the first person singular present of ''amō'' (to love)?',
    ARRAY['amō', 'amās', 'amat', 'amant']::text[],
    'amō',
    'Amō means ''I love'' - the first person singular keeps the -ō ending.',
    'beginner',
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
    '54737df7-a11e-4b23-998a-1ae028dc1ad1',
    'What is the infinitive ending for first conjugation verbs?',
    ARRAY['-ō', '-āre', '-ēre', '-ere']::text[],
    '-āre',
    'First conjugation infinitives end in -āre (long a).',
    'beginner',
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
    '21bd6c55-234b-4946-8c69-3622c82c9a53',
    'Translate ''laborant'' into English:',
    ARRAY['I work', 'you work', 'he works', 'they work']::text[],
    'they work',
    'The -ant ending indicates third person plural: ''they work''.',
    'beginner',
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
    'e32b0400-9721-48c6-8b61-c23d0a3fccdd',
    'What is the third person singular of ''portō'' (to carry)?',
    ARRAY['portō', 'portās', 'portat', 'portant']::text[],
    'portat',
    'Third person singular of first conjugation ends in -at.',
    'beginner',
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
    'ec21afbf-28fa-4a5a-8806-31dd2ea1c038',
    'In ''Puella cantat'', what person and number is ''cantat''?',
    ARRAY['1st singular', '2nd singular', '3rd singular', '3rd plural']::text[],
    '3rd singular',
    'The -at ending shows third person singular: ''she sings''.',
    'beginner',
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
    '35b84e3b-c7d1-4443-a26a-892b25d7dd78',
    'What is the second person plural of ''laudō'' (to praise)?',
    ARRAY['laudās', 'laudat', 'laudātis', 'laudant']::text[],
    'laudātis',
    'Second person plural of first conjugation ends in -ātis.',
    'beginner',
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
    '68ca5f9c-5aa3-4221-aa10-212067ebd571',
    'Which ending shows first person plural in first conjugation?',
    ARRAY['-āmus', '-ātis', '-ant', '-ō']::text[],
    '-āmus',
    'First person plural ends in -āmus: ''we [verb]''.',
    'beginner',
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
    '00a053f8-a79b-4167-9e24-e6a26345734f',
    'Translate ''vocās'':',
    ARRAY['I call', 'you call', 'he calls', 'they call']::text[],
    'you call',
    'The -ās ending is second person singular.',
    'beginner',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;

-- Link questions to course modules
-- This creates the module_questions relationships

-- For module: First Declension Nouns

-- INSERT INTO module_questions (module_id, question_id, display_order)
-- SELECT 
--     m.id as module_id,
--     q.id as question_id,
--     ROW_NUMBER() OVER (ORDER BY q.created_at) as display_order
-- FROM course_modules m
-- CROSS JOIN questions q
-- WHERE m.title = 'First Declension Nouns'
-- AND q.question_text IN (
--     /* List specific question texts for this module */
-- )
-- ON CONFLICT DO NOTHING;

-- For module: Second Declension Masculine Nouns

-- INSERT INTO module_questions (module_id, question_id, display_order)
-- SELECT 
--     m.id as module_id,
--     q.id as question_id,
--     ROW_NUMBER() OVER (ORDER BY q.created_at) as display_order
-- FROM course_modules m
-- CROSS JOIN questions q
-- WHERE m.title = 'Second Declension Masculine Nouns'
-- AND q.question_text IN (
--     /* List specific question texts for this module */
-- )
-- ON CONFLICT DO NOTHING;

-- For module: Second Declension Neuter Nouns

-- INSERT INTO module_questions (module_id, question_id, display_order)
-- SELECT 
--     m.id as module_id,
--     q.id as question_id,
--     ROW_NUMBER() OVER (ORDER BY q.created_at) as display_order
-- FROM course_modules m
-- CROSS JOIN questions q
-- WHERE m.title = 'Second Declension Neuter Nouns'
-- AND q.question_text IN (
--     /* List specific question texts for this module */
-- )
-- ON CONFLICT DO NOTHING;

-- For module: Present Tense of Sum

-- INSERT INTO module_questions (module_id, question_id, display_order)
-- SELECT 
--     m.id as module_id,
--     q.id as question_id,
--     ROW_NUMBER() OVER (ORDER BY q.created_at) as display_order
-- FROM course_modules m
-- CROSS JOIN questions q
-- WHERE m.title = 'Present Tense of Sum'
-- AND q.question_text IN (
--     /* List specific question texts for this module */
-- )
-- ON CONFLICT DO NOTHING;

-- For module: First Conjugation Verbs Present

-- INSERT INTO module_questions (module_id, question_id, display_order)
-- SELECT 
--     m.id as module_id,
--     q.id as question_id,
--     ROW_NUMBER() OVER (ORDER BY q.created_at) as display_order
-- FROM course_modules m
-- CROSS JOIN questions q
-- WHERE m.title = 'First Conjugation Verbs Present'
-- AND q.question_text IN (
--     /* List specific question texts for this module */
-- )
-- ON CONFLICT DO NOTHING;
