INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    '470c8a21-c9e3-4a83-83d3-f31f54780df1',
    'es',
    'reading/listening',
    'comprehension',
    1,
    '[Read the passage below or listen to the audio]

"María va al mercado todos los sábados. Le gusta comprar frutas frescas y verduras. Su fruta favorita es la manzana roja. Siempre compra cinco manzanas para la semana."

¿Cuándo va María al mercado?',
    ARRAY['Todos los días', 'Los sábados', 'Los domingos', 'Los lunes'],
    1,
    'The passage states ''María va al mercado todos los sábados'' (María goes to the market every Saturday).',
    '{"passage":"María va al mercado todos los sábados. Le gusta comprar frutas frescas y verduras. Su fruta favorita es la manzana roja. Siempre compra cinco manzanas para la semana.","passage_index":0,"question_index":0}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    '526da408-0450-446a-bac9-99fc6fb95985',
    'es',
    'reading/listening',
    'comprehension',
    1,
    '[Read the passage below or listen to the audio]

"María va al mercado todos los sábados. Le gusta comprar frutas frescas y verduras. Su fruta favorita es la manzana roja. Siempre compra cinco manzanas para la semana."

¿Cuál es la fruta favorita de María?',
    ARRAY['La naranja', 'El plátano', 'La manzana roja', 'La pera'],
    2,
    'The text mentions ''Su fruta favorita es la manzana roja'' (Her favorite fruit is the red apple).',
    '{"passage":"María va al mercado todos los sábados. Le gusta comprar frutas frescas y verduras. Su fruta favorita es la manzana roja. Siempre compra cinco manzanas para la semana.","passage_index":0,"question_index":1}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    'f3726d1c-99d0-45ea-a1d7-ae2ef256a931',
    'es',
    'reading/listening',
    'comprehension',
    1,
    '[Read the passage below or listen to the audio]

"María va al mercado todos los sábados. Le gusta comprar frutas frescas y verduras. Su fruta favorita es la manzana roja. Siempre compra cinco manzanas para la semana."

¿Cuántas manzanas compra María?',
    ARRAY['Tres', 'Cuatro', 'Cinco', 'Seis'],
    2,
    'María ''siempre compra cinco manzanas para la semana'' (always buys five apples for the week).',
    '{"passage":"María va al mercado todos los sábados. Le gusta comprar frutas frescas y verduras. Su fruta favorita es la manzana roja. Siempre compra cinco manzanas para la semana.","passage_index":0,"question_index":2}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    '5bb5cf9f-413b-4798-bb0a-0d3d7ca49b77',
    'es',
    'reading/listening',
    'comprehension',
    2,
    '[Read the passage below or listen to the audio]

"Pedro es estudiante de medicina. Estudia en la universidad de Madrid. Todas las mañanas toma el autobús a las siete. Sus clases empiezan a las ocho y terminan a las dos de la tarde. Después de las clases, estudia en la biblioteca por tres horas."

¿Qué estudia Pedro?',
    ARRAY['Derecho', 'Medicina', 'Ingeniería', 'Arte'],
    1,
    'The passage clearly states ''Pedro es estudiante de medicina'' (Pedro is a medical student).',
    '{"passage":"Pedro es estudiante de medicina. Estudia en la universidad de Madrid. Todas las mañanas toma el autobús a las siete. Sus clases empiezan a las ocho y terminan a las dos de la tarde. Después de las clases, estudia en la biblioteca por tres horas.","passage_index":1,"question_index":0}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    'af0fc05c-85df-47d0-8999-c79d89bb8080',
    'es',
    'reading/listening',
    'comprehension',
    2,
    '[Read the passage below or listen to the audio]

"Pedro es estudiante de medicina. Estudia en la universidad de Madrid. Todas las mañanas toma el autobús a las siete. Sus clases empiezan a las ocho y terminan a las dos de la tarde. Después de las clases, estudia en la biblioteca por tres horas."

¿A qué hora toma el autobús Pedro?',
    ARRAY['A las seis', 'A las siete', 'A las ocho', 'A las nueve'],
    1,
    'The text says ''Todas las mañanas toma el autobús a las siete'' (Every morning he takes the bus at seven).',
    '{"passage":"Pedro es estudiante de medicina. Estudia en la universidad de Madrid. Todas las mañanas toma el autobús a las siete. Sus clases empiezan a las ocho y terminan a las dos de la tarde. Después de las clases, estudia en la biblioteca por tres horas.","passage_index":1,"question_index":1}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    'f5261ee4-f0b5-4a45-a06b-3122d7f2d396',
    'es',
    'reading/listening',
    'comprehension',
    2,
    '[Read the passage below or listen to the audio]

"Pedro es estudiante de medicina. Estudia en la universidad de Madrid. Todas las mañanas toma el autobús a las siete. Sus clases empiezan a las ocho y terminan a las dos de la tarde. Después de las clases, estudia en la biblioteca por tres horas."

¿Dónde estudia Pedro después de las clases?',
    ARRAY['En casa', 'En el parque', 'En la biblioteca', 'En la cafetería'],
    2,
    'After classes, Pedro ''estudia en la biblioteca por tres horas'' (studies in the library for three hours).',
    '{"passage":"Pedro es estudiante de medicina. Estudia en la universidad de Madrid. Todas las mañanas toma el autobús a las siete. Sus clases empiezan a las ocho y terminan a las dos de la tarde. Después de las clases, estudia en la biblioteca por tres horas.","passage_index":1,"question_index":2}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    'c8666a05-dc5a-4410-a9e6-ff6c93c6c796',
    'es',
    'reading/listening',
    'comprehension',
    3,
    '[Read the passage below or listen to the audio]

"La familia García vive en una casa grande con jardín. Tienen dos perros y un gato. Los perros se llaman Max y Luna. El gato se llama Misi. Los niños juegan con los animales en el jardín todos los días después de la escuela."

¿Cuántos perros tiene la familia García?',
    ARRAY['Uno', 'Dos', 'Tres', 'Cuatro'],
    1,
    'The passage mentions ''Tienen dos perros y un gato'' (They have two dogs and a cat).',
    '{"passage":"La familia García vive en una casa grande con jardín. Tienen dos perros y un gato. Los perros se llaman Max y Luna. El gato se llama Misi. Los niños juegan con los animales en el jardín todos los días después de la escuela.","passage_index":2,"question_index":0}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    'e76f072d-ca94-4a1c-9c49-9c1ce7915b24',
    'es',
    'reading/listening',
    'comprehension',
    3,
    '[Read the passage below or listen to the audio]

"La familia García vive en una casa grande con jardín. Tienen dos perros y un gato. Los perros se llaman Max y Luna. El gato se llama Misi. Los niños juegan con los animales en el jardín todos los días después de la escuela."

¿Cómo se llama el gato?',
    ARRAY['Max', 'Luna', 'Misi', 'García'],
    2,
    'The text states ''El gato se llama Misi'' (The cat is called Misi).',
    '{"passage":"La familia García vive en una casa grande con jardín. Tienen dos perros y un gato. Los perros se llaman Max y Luna. El gato se llama Misi. Los niños juegan con los animales en el jardín todos los días después de la escuela.","passage_index":2,"question_index":1}'::jsonb
  );

INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    'd34e16f3-8a4e-4a7c-8776-34f3929bfadf',
    'es',
    'reading/listening',
    'comprehension',
    3,
    '[Read the passage below or listen to the audio]

"La familia García vive en una casa grande con jardín. Tienen dos perros y un gato. Los perros se llaman Max y Luna. El gato se llama Misi. Los niños juegan con los animales en el jardín todos los días después de la escuela."

¿Dónde juegan los niños con los animales?',
    ARRAY['En la casa', 'En el parque', 'En el jardín', 'En la escuela'],
    2,
    'The children ''juegan con los animales en el jardín'' (play with the animals in the garden).',
    '{"passage":"La familia García vive en una casa grande con jardín. Tienen dos perros y un gato. Los perros se llaman Max y Luna. El gato se llama Misi. Los niños juegan con los animales en el jardín todos los días después de la escuela.","passage_index":2,"question_index":2}'::jsonb
  );