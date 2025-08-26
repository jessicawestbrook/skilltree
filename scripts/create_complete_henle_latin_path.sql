-- Create complete Henle Latin learning path with all 5 textbooks
-- Generated: 2025-08-25 08:35:42

-- Execute the create_learning_paths_tables.sql first if tables don't exist

-- Insert Henle Latin Second Year
INSERT INTO language_courses (
    id, language_id, name, description, level, estimated_hours, is_active, display_order
) VALUES (
    'b1661d5c-7e1f-44a9-bbb4-17265e521670',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Henle Latin Second Year',
    'Second year Latin course focusing on subjunctive mood, participles, and Caesar readings',
    'Intermediate',
    80,
    true,
    2
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Chapter 1: Review of First Year Grammar
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '35dd8b6e-fbf9-4658-b3f2-6b8699352aa8',
    'b1661d5c-7e1f-44a9-bbb4-17265e521670',
    1,
    'Review of First Year Grammar',
    'Comprehensive review of first year concepts',
    'chapter',
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'cd0fd154-4c59-498c-8e31-55ed65a5087e',
    '35dd8b6e-fbf9-4658-b3f2-6b8699352aa8',
    1,
    'Case Review',
    'lesson',
    '{"text": "Review of all six Latin cases and their uses", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '6d1f29ff-d5c2-4978-8189-92495b7934de',
    '35dd8b6e-fbf9-4658-b3f2-6b8699352aa8',
    2,
    'Verb Conjugations Review',
    'lesson',
    '{"text": "Review of present, imperfect, and future tenses", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'c7c6e121-7d1d-4a6d-adac-952834cdf119',
    '35dd8b6e-fbf9-4658-b3f2-6b8699352aa8',
    3,
    'Advanced Vocabulary',
    'lesson',
    '{"text": "Extended vocabulary from first year", "type": "vocabulary"}'::jsonb,
    3
);

-- Chapter 2: Subjunctive Mood
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    'cda2f843-36ff-494b-b67f-349ac1fecf97',
    'b1661d5c-7e1f-44a9-bbb4-17265e521670',
    2,
    'Subjunctive Mood',
    'Introduction to the subjunctive mood',
    'chapter',
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'a3fae19e-1270-4e6b-adc3-bb214bfa6beb',
    'cda2f843-36ff-494b-b67f-349ac1fecf97',
    1,
    'Present Subjunctive',
    'lesson',
    '{"text": "Formation and uses of present subjunctive", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '8a3bc17d-57aa-4ae7-b26c-e302c38b7c85',
    'cda2f843-36ff-494b-b67f-349ac1fecf97',
    2,
    'Imperfect Subjunctive',
    'lesson',
    '{"text": "Formation and uses of imperfect subjunctive", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '2128411a-f458-42f4-a239-641c159bca94',
    'cda2f843-36ff-494b-b67f-349ac1fecf97',
    3,
    'Purpose Clauses',
    'lesson',
    '{"text": "Using ut and ne with subjunctive", "type": "grammar_rule"}'::jsonb,
    3
);

-- Chapter 3: Participles
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '5f961120-d137-4866-9545-fdabc325e3c1',
    'b1661d5c-7e1f-44a9-bbb4-17265e521670',
    3,
    'Participles',
    'Present, perfect, and future participles',
    'chapter',
    3
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'dcc8a871-7776-4ee3-8d5d-f69453174e78',
    '5f961120-d137-4866-9545-fdabc325e3c1',
    1,
    'Present Active Participle',
    'lesson',
    '{"text": "Formation and use of present participles", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '5ffc2ba2-9dd3-49eb-8cf2-43526fac5289',
    '5f961120-d137-4866-9545-fdabc325e3c1',
    2,
    'Perfect Passive Participle',
    'lesson',
    '{"text": "Formation and use of perfect participles", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '0d37b27e-5f1b-4847-86b1-d471381cd73c',
    '5f961120-d137-4866-9545-fdabc325e3c1',
    3,
    'Ablative Absolute',
    'lesson',
    '{"text": "Construction and translation of ablative absolute", "type": "grammar_rule"}'::jsonb,
    3
);

-- Chapter 4: Indirect Discourse
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    'd90d6fb6-ef41-44c1-85d4-5d941c854c05',
    'b1661d5c-7e1f-44a9-bbb4-17265e521670',
    4,
    'Indirect Discourse',
    'Reporting speech and thoughts in Latin',
    'chapter',
    4
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '918143f0-f09c-4d27-b6a2-cf3415f8ceaf',
    'd90d6fb6-ef41-44c1-85d4-5d941c854c05',
    1,
    'Accusative with Infinitive',
    'lesson',
    '{"text": "Basic indirect statement construction", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'c242be5e-91c6-4118-ad3d-4ab70c24a103',
    'd90d6fb6-ef41-44c1-85d4-5d941c854c05',
    2,
    'Sequence of Tenses',
    'lesson',
    '{"text": "Time relationships in indirect discourse", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '8992d800-67ee-4961-9be6-010d1bd9c7d2',
    'd90d6fb6-ef41-44c1-85d4-5d941c854c05',
    3,
    'Caesar Readings',
    'lesson',
    '{"text": "Selections from De Bello Gallico", "type": "reading_comprehension"}'::jsonb,
    3
);

-- Chapter 5: Advanced Syntax
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    'f18ed9bc-4f12-49dd-8dd1-24470043b00a',
    'b1661d5c-7e1f-44a9-bbb4-17265e521670',
    5,
    'Advanced Syntax',
    'Complex grammatical constructions',
    'chapter',
    5
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'd487ddc6-25d8-49d0-b718-857c71b1c7c8',
    'f18ed9bc-4f12-49dd-8dd1-24470043b00a',
    1,
    'Gerunds and Gerundives',
    'lesson',
    '{"text": "Formation and uses of verbal nouns and adjectives", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '111fe6c9-9096-4588-8efa-c2c39f9f66e0',
    'f18ed9bc-4f12-49dd-8dd1-24470043b00a',
    2,
    'Conditional Sentences',
    'lesson',
    '{"text": "Types of conditional clauses", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'bb9726ef-5946-4d62-90b2-d37a21f7dc1f',
    'f18ed9bc-4f12-49dd-8dd1-24470043b00a',
    3,
    'Advanced Caesar',
    'lesson',
    '{"text": "Extended passages from Caesar", "type": "reading_comprehension"}'::jsonb,
    3
);

-- Insert Henle Latin Third Year
INSERT INTO language_courses (
    id, language_id, name, description, level, estimated_hours, is_active, display_order
) VALUES (
    'b72b43fa-c306-40da-b7a1-bfd46990cb80',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Henle Latin Third Year',
    'Third year Latin featuring Cicero, introduction to Virgil, and advanced prose composition',
    'Advanced',
    100,
    true,
    3
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Chapter 1: Cicero: In Catilinam
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    'b2073696-cb6d-41ca-bfb9-9938887c60e4',
    'b72b43fa-c306-40da-b7a1-bfd46990cb80',
    1,
    'Cicero: In Catilinam',
    'Introduction to Ciceronian prose',
    'chapter',
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'd947e63f-82af-4ded-a29e-2489e427fc38',
    'b2073696-cb6d-41ca-bfb9-9938887c60e4',
    1,
    'Historical Context',
    'lesson',
    '{"text": "The Catiline Conspiracy", "type": "reading_comprehension"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '4c0e29ff-cc71-481b-8e83-809f2c2573ff',
    'b2073696-cb6d-41ca-bfb9-9938887c60e4',
    2,
    'Ciceronian Style',
    'lesson',
    '{"text": "Periodic sentences and rhetorical devices", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '601f5717-ab6f-4ad9-aa48-694d48135fd8',
    'b2073696-cb6d-41ca-bfb9-9938887c60e4',
    3,
    'First Catiline Oration',
    'lesson',
    '{"text": "Opening passages of In Catilinam I", "type": "translation"}'::jsonb,
    3
);

-- Chapter 2: Advanced Subjunctive Uses
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '15daea95-14ab-4f21-a98c-f24885f6ebc5',
    'b72b43fa-c306-40da-b7a1-bfd46990cb80',
    2,
    'Advanced Subjunctive Uses',
    'Complex subjunctive constructions',
    'chapter',
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '596b97eb-2e58-4510-8791-d033c1e48085',
    '15daea95-14ab-4f21-a98c-f24885f6ebc5',
    1,
    'Result Clauses',
    'lesson',
    '{"text": "Ut and ut non with subjunctive", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'ade7a8b3-362e-4c55-9b22-2370803ccb60',
    '15daea95-14ab-4f21-a98c-f24885f6ebc5',
    2,
    'Cum Clauses',
    'lesson',
    '{"text": "Temporal, causal, and concessive cum", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'fa4cb7f0-e8a5-4423-85f4-4cc51cad737e',
    '15daea95-14ab-4f21-a98c-f24885f6ebc5',
    3,
    'Indirect Questions',
    'lesson',
    '{"text": "Question words with subjunctive", "type": "grammar_rule"}'::jsonb,
    3
);

-- Chapter 3: Virgil: Aeneid Introduction
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '5cc6f9ed-c419-494c-807c-7384c61707fa',
    'b72b43fa-c306-40da-b7a1-bfd46990cb80',
    3,
    'Virgil: Aeneid Introduction',
    'Beginning epic poetry',
    'chapter',
    3
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'db7c7fd1-44b9-46ae-97db-31c32a38e914',
    '5cc6f9ed-c419-494c-807c-7384c61707fa',
    1,
    'Dactylic Hexameter',
    'lesson',
    '{"text": "Meter and scansion basics", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'c4141af5-61c2-43ce-9c11-8ced675032f7',
    '5cc6f9ed-c419-494c-807c-7384c61707fa',
    2,
    'Epic Conventions',
    'lesson',
    '{"text": "Invocation, epithets, and similes", "type": "reading_comprehension"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'e7526279-d198-4fbf-9905-74d7099ec99b',
    '5cc6f9ed-c419-494c-807c-7384c61707fa',
    3,
    'Aeneid Book I Opening',
    'lesson',
    '{"text": "Arma virumque cano...", "type": "translation"}'::jsonb,
    3
);

-- Chapter 4: Advanced Prose Composition
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '7919dad3-fb72-4c6d-8573-d5183726d17a',
    'b72b43fa-c306-40da-b7a1-bfd46990cb80',
    4,
    'Advanced Prose Composition',
    'Writing Latin prose',
    'chapter',
    4
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '36aaaf0a-fdd9-4d90-85d4-6212de1fe8ad',
    '7919dad3-fb72-4c6d-8573-d5183726d17a',
    1,
    'Word Order',
    'lesson',
    '{"text": "Latin word order principles", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '025d0dfa-ee14-4a8f-83e3-44d753a43a76',
    '7919dad3-fb72-4c6d-8573-d5183726d17a',
    2,
    'Prose Rhythm',
    'lesson',
    '{"text": "Clausulae and periodic structure", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '5e12ba2b-b44a-4ece-855e-c301f2488e38',
    '7919dad3-fb72-4c6d-8573-d5183726d17a',
    3,
    'Translation Exercises',
    'lesson',
    '{"text": "English to Latin prose", "type": "translation"}'::jsonb,
    3
);

-- Chapter 5: Livy: Ab Urbe Condita
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    'bd6caf16-bbd9-4574-b6b6-185c1314e70e',
    'b72b43fa-c306-40da-b7a1-bfd46990cb80',
    5,
    'Livy: Ab Urbe Condita',
    'Historical narrative',
    'chapter',
    5
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'db9c4ee2-b4bf-4470-b10f-8ce213be2bf0',
    'bd6caf16-bbd9-4574-b6b6-185c1314e70e',
    1,
    'Livy's Style',
    'lesson',
    '{"text": "Narrative techniques", "type": "reading_comprehension"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'a39ddec1-8af4-45fc-8a1d-cd93f05b1983',
    'bd6caf16-bbd9-4574-b6b6-185c1314e70e',
    2,
    'Hannibal Passages',
    'lesson',
    '{"text": "Selections from the Second Punic War", "type": "translation"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'c8b6e8b8-71d7-4d58-8516-a7d485629172',
    'bd6caf16-bbd9-4574-b6b6-185c1314e70e',
    3,
    'Historical Present',
    'lesson',
    '{"text": "Use of present tense in narrative", "type": "grammar_rule"}'::jsonb,
    3
);

-- Insert Henle Latin Fourth Year
INSERT INTO language_courses (
    id, language_id, name, description, level, estimated_hours, is_active, display_order
) VALUES (
    '6794c142-289f-40b2-a9db-a1dfaeb0d778',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Henle Latin Fourth Year',
    'Fourth year Latin featuring extensive Virgil, Horace, Ovid, and Tacitus',
    'Advanced',
    120,
    true,
    4
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Chapter 1: Virgil: Aeneid Books I-VI
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '66ceef0c-b1a5-413f-9961-5b595b02b6a5',
    '6794c142-289f-40b2-a9db-a1dfaeb0d778',
    1,
    'Virgil: Aeneid Books I-VI',
    'Extended reading of the Aeneid',
    'chapter',
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '891129cc-ba20-464e-bf33-ab75fdbba07f',
    '66ceef0c-b1a5-413f-9961-5b595b02b6a5',
    1,
    'Book I: Storm and Carthage',
    'lesson',
    '{"text": "Complete Book I selections", "type": "translation"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '41029ef2-6b64-4c1d-b473-eca1a7e6d5ad',
    '66ceef0c-b1a5-413f-9961-5b595b02b6a5',
    2,
    'Book II: Fall of Troy',
    'lesson',
    '{"text": "Trojan Horse and destruction", "type": "translation"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'b70a2c11-e116-4b57-9b8b-28f941780166',
    '66ceef0c-b1a5-413f-9961-5b595b02b6a5',
    3,
    'Book IV: Dido and Aeneas',
    'lesson',
    '{"text": "The tragedy of Dido", "type": "translation"}'::jsonb,
    3
);

-- Chapter 2: Horace: Odes
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '580bba16-3765-403b-b334-8b38a119b715',
    '6794c142-289f-40b2-a9db-a1dfaeb0d778',
    2,
    'Horace: Odes',
    'Lyric poetry',
    'chapter',
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '06a57403-686f-4422-af86-be9b86c867cc',
    '580bba16-3765-403b-b334-8b38a119b715',
    1,
    'Lyric Meters',
    'lesson',
    '{"text": "Sapphic and Alcaic stanzas", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '0c87b0dd-4268-403f-bff5-0039b030ca9c',
    '580bba16-3765-403b-b334-8b38a119b715',
    2,
    'Carpe Diem',
    'lesson',
    '{"text": "Odes I.11 and similar poems", "type": "translation"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'dfb0d7d1-ae52-4559-9da0-a12a7609530d',
    '580bba16-3765-403b-b334-8b38a119b715',
    3,
    'Roman Values in Horace',
    'lesson',
    '{"text": "Themes of moderation and virtue", "type": "reading_comprehension"}'::jsonb,
    3
);

-- Chapter 3: Ovid: Metamorphoses
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '189e6162-a630-47c2-9c61-f0e0cb19bcc8',
    '6794c142-289f-40b2-a9db-a1dfaeb0d778',
    3,
    'Ovid: Metamorphoses',
    'Mythological epic',
    'chapter',
    3
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'a3831a37-af51-40b0-ac58-5666f788f305',
    '189e6162-a630-47c2-9c61-f0e0cb19bcc8',
    1,
    'Creation Story',
    'lesson',
    '{"text": "Book I: Chaos to Cosmos", "type": "translation"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '71eb17f5-e75f-4d62-8442-93c94c177647',
    '189e6162-a630-47c2-9c61-f0e0cb19bcc8',
    2,
    'Daedalus and Icarus',
    'lesson',
    '{"text": "Book VIII: The flight", "type": "translation"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '30abb009-e241-4057-a6d3-6cc393c3fac1',
    '189e6162-a630-47c2-9c61-f0e0cb19bcc8',
    3,
    'Pyramus and Thisbe',
    'lesson',
    '{"text": "Book IV: Tragic love", "type": "translation"}'::jsonb,
    3
);

-- Chapter 4: Tacitus: Annales
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '47e0c495-7386-42df-a553-f479f8a6ac63',
    '6794c142-289f-40b2-a9db-a1dfaeb0d778',
    4,
    'Tacitus: Annales',
    'Imperial historiography',
    'chapter',
    4
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '88f20f81-280a-434a-9ae5-8caee51347ee',
    '47e0c495-7386-42df-a553-f479f8a6ac63',
    1,
    'Tacitean Style',
    'lesson',
    '{"text": "Brevity and variation", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '8ecc852b-2bd9-4f14-848d-73bc887c6775',
    '47e0c495-7386-42df-a553-f479f8a6ac63',
    2,
    'Death of Germanicus',
    'lesson',
    '{"text": "Annales II selections", "type": "translation"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '000f06f3-2237-4142-bc79-258620fe3798',
    '47e0c495-7386-42df-a553-f479f8a6ac63',
    3,
    'Nero and the Fire',
    'lesson',
    '{"text": "Annales XV: Great Fire of Rome", "type": "translation"}'::jsonb,
    3
);

-- Chapter 5: Advanced Poetry Analysis
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    'd5b01b12-9026-4663-b4fa-6c846a94e4a6',
    '6794c142-289f-40b2-a9db-a1dfaeb0d778',
    5,
    'Advanced Poetry Analysis',
    'Literary criticism and analysis',
    'chapter',
    5
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'be612584-3d92-4a4e-bc1a-b27a47d8e022',
    'd5b01b12-9026-4663-b4fa-6c846a94e4a6',
    1,
    'Figures of Speech',
    'lesson',
    '{"text": "Metaphor, metonymy, synecdoche", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '3701655e-0f9b-4f2f-9758-20ba843a2e4c',
    'd5b01b12-9026-4663-b4fa-6c846a94e4a6',
    2,
    'Allusion and Intertextuality',
    'lesson',
    '{"text": "Literary references", "type": "reading_comprehension"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '7e0d4154-9e8d-4706-b18d-25248b97c748',
    'd5b01b12-9026-4663-b4fa-6c846a94e4a6',
    3,
    'Comparative Analysis',
    'lesson',
    '{"text": "Comparing authors and styles", "type": "translation"}'::jsonb,
    3
);

-- Insert Henle Latin Grammar
INSERT INTO language_courses (
    id, language_id, name, description, level, estimated_hours, is_active, display_order
) VALUES (
    '9fa4a1e7-4dcc-4fa9-a4be-d0ec3d2fc75a',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    'Henle Latin Grammar',
    'Complete Latin grammar reference covering all forms and constructions',
    'Reference',
    40,
    true,
    5
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Chapter 1: Complete Declension System
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '843dfa90-d332-42f3-b145-7468fdb198f4',
    '9fa4a1e7-4dcc-4fa9-a4be-d0ec3d2fc75a',
    1,
    'Complete Declension System',
    'All noun and adjective forms',
    'chapter',
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '54063977-145e-4d8c-a48c-229e05a4f953',
    '843dfa90-d332-42f3-b145-7468fdb198f4',
    1,
    'All Five Declensions',
    'lesson',
    '{"text": "Complete paradigms and exceptions", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '0b60344b-3e01-4372-98fd-91ba7fc027da',
    '843dfa90-d332-42f3-b145-7468fdb198f4',
    2,
    'Adjective Agreement',
    'lesson',
    '{"text": "Three-termination and two-termination adjectives", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '1ddf74a2-a522-4641-b281-c9dfb5f5ede3',
    '843dfa90-d332-42f3-b145-7468fdb198f4',
    3,
    'Comparative and Superlative',
    'lesson',
    '{"text": "Regular and irregular comparisons", "type": "grammar_rule"}'::jsonb,
    3
);

-- Chapter 2: Complete Conjugation System
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '9c731c3b-9057-4f5a-a204-46d71d59c218',
    '9fa4a1e7-4dcc-4fa9-a4be-d0ec3d2fc75a',
    2,
    'Complete Conjugation System',
    'All verb forms and constructions',
    'chapter',
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '96319411-8d3d-4055-b565-cdac4ff6b28a',
    '9c731c3b-9057-4f5a-a204-46d71d59c218',
    1,
    'All Tenses Active',
    'lesson',
    '{"text": "Present, imperfect, future, perfect, pluperfect, future perfect", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'd834e58c-90c6-4d35-ab0a-4770123383e3',
    '9c731c3b-9057-4f5a-a204-46d71d59c218',
    2,
    'All Tenses Passive',
    'lesson',
    '{"text": "Complete passive system", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'd8b2495f-54dc-47d3-b5ff-a29dbbe181dd',
    '9c731c3b-9057-4f5a-a204-46d71d59c218',
    3,
    'Deponent Verbs',
    'lesson',
    '{"text": "Passive form, active meaning", "type": "grammar_rule"}'::jsonb,
    3
);

-- Chapter 3: Syntax Reference
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '481d1d95-331c-4a91-a57c-9daa77c5d64f',
    '9fa4a1e7-4dcc-4fa9-a4be-d0ec3d2fc75a',
    3,
    'Syntax Reference',
    'Complete syntax rules',
    'chapter',
    3
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'de3bcfc4-eac5-4796-9866-ef82eb1879b5',
    '481d1d95-331c-4a91-a57c-9daa77c5d64f',
    1,
    'Case Uses',
    'lesson',
    '{"text": "All uses of all cases", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '980d80ec-4885-4b1d-b6f7-641ab30e9c5a',
    '481d1d95-331c-4a91-a57c-9daa77c5d64f',
    2,
    'Clause Types',
    'lesson',
    '{"text": "All subordinate clause types", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'e0b04a52-a17e-466c-b503-640481b3ce3f',
    '481d1d95-331c-4a91-a57c-9daa77c5d64f',
    3,
    'Sequence of Tenses',
    'lesson',
    '{"text": "Complete tense relationships", "type": "grammar_rule"}'::jsonb,
    3
);

-- Chapter 4: Irregular Forms
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '937a09c4-6b21-4b72-86b5-7aefafd8fb17',
    '9fa4a1e7-4dcc-4fa9-a4be-d0ec3d2fc75a',
    4,
    'Irregular Forms',
    'Exceptions and irregularities',
    'chapter',
    4
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'cf268fe7-ebfe-4d81-a347-22f04315cb0a',
    '937a09c4-6b21-4b72-86b5-7aefafd8fb17',
    1,
    'Irregular Verbs',
    'lesson',
    '{"text": "Sum, possum, fero, eo, volo, etc.", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '2ee900b6-1375-4a11-8e6f-db667e661f99',
    '937a09c4-6b21-4b72-86b5-7aefafd8fb17',
    2,
    'Irregular Nouns',
    'lesson',
    '{"text": "Vis, domus, and defective nouns", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'ac178e86-b935-4df7-b3b5-eb19c06d2878',
    '937a09c4-6b21-4b72-86b5-7aefafd8fb17',
    3,
    'Greek Forms',
    'lesson',
    '{"text": "Greek declensions in Latin", "type": "grammar_rule"}'::jsonb,
    3
);

-- Chapter 5: Advanced Topics
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description, module_type, display_order
) VALUES (
    '3ee3a2e7-bb01-44dc-8801-2102a2300fb9',
    '9fa4a1e7-4dcc-4fa9-a4be-d0ec3d2fc75a',
    5,
    'Advanced Topics',
    'Specialized grammar topics',
    'chapter',
    5
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '38c57a8c-7fa7-4cc4-94c0-c689b0176416',
    '3ee3a2e7-bb01-44dc-8801-2102a2300fb9',
    1,
    'Supines and Gerunds',
    'lesson',
    '{"text": "Verbal nouns and their uses", "type": "grammar_rule"}'::jsonb,
    1
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    'c76add8e-ac50-4760-9097-5b5099edc133',
    '3ee3a2e7-bb01-44dc-8801-2102a2300fb9',
    2,
    'Impersonal Verbs',
    'lesson',
    '{"text": "Licet, oportet, interest, etc.", "type": "grammar_rule"}'::jsonb,
    2
);

INSERT INTO module_content (
    id, module_id, section_number, title, content_type, content, display_order
) VALUES (
    '402b203c-1c85-4a72-990f-573beb2e6849',
    '3ee3a2e7-bb01-44dc-8801-2102a2300fb9',
    3,
    'Archaic and Poetic Forms',
    'lesson',
    '{"text": "Old and poetic variations", "type": "grammar_rule"}'::jsonb,
    3
);

-- Create the Learn Latin learning path
INSERT INTO learning_paths (
    id, name, description, category, difficulty, estimated_hours,
    icon_name, color, language_id, is_active, display_order
) VALUES (
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a',
    'Complete Henle Latin Program',
    'Master Latin through the complete Henle Latin series, from basic grammar to advanced literature including Caesar, Cicero, Virgil, Horace, Ovid, and Tacitus',
    'language',
    'comprehensive',
    420,
    'AcademicCapIcon',
    'purple',
    '84acf185-0b8c-4c2a-99f3-c5056be86d23',
    true,
    1
);

-- Link course 1: first_year
INSERT INTO learning_path_courses (
    learning_path_id, course_id, sequence_number, is_required, unlock_after_course_id
) VALUES (
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a',
    'cebb7f42-e51b-4ac4-8464-29fee0894024',
    1,
    true,
    NULL
);

-- Link course 2: second_year
INSERT INTO learning_path_courses (
    learning_path_id, course_id, sequence_number, is_required, unlock_after_course_id
) VALUES (
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a',
    'b1661d5c-7e1f-44a9-bbb4-17265e521670',
    2,
    true,
    'cebb7f42-e51b-4ac4-8464-29fee0894024'
);

-- Link course 3: third_year
INSERT INTO learning_path_courses (
    learning_path_id, course_id, sequence_number, is_required, unlock_after_course_id
) VALUES (
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a',
    'b72b43fa-c306-40da-b7a1-bfd46990cb80',
    3,
    true,
    'b1661d5c-7e1f-44a9-bbb4-17265e521670'
);

-- Link course 4: fourth_year
INSERT INTO learning_path_courses (
    learning_path_id, course_id, sequence_number, is_required, unlock_after_course_id
) VALUES (
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a',
    '6794c142-289f-40b2-a9db-a1dfaeb0d778',
    4,
    true,
    'b72b43fa-c306-40da-b7a1-bfd46990cb80'
);

-- Link course 5: grammar
INSERT INTO learning_path_courses (
    learning_path_id, course_id, sequence_number, is_required, unlock_after_course_id
) VALUES (
    '97765ae5-4d73-43eb-8072-6b110a8c6a8a',
    '9fa4a1e7-4dcc-4fa9-a4be-d0ec3d2fc75a',
    5,
    false,
    NULL
);
