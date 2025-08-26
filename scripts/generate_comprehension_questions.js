#!/usr/bin/env node

/**
 * Generate reading and listening comprehension questions for languages
 * These can be used for both reading and listening exercises
 */

const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

// Sample Spanish comprehension passages and questions
const spanishComprehension = [
  {
    passage: "María va al mercado todos los sábados. Le gusta comprar frutas frescas y verduras. Su fruta favorita es la manzana roja. Siempre compra cinco manzanas para la semana.",
    questions: [
      {
        question: "¿Cuándo va María al mercado?",
        options: ["Todos los días", "Los sábados", "Los domingos", "Los lunes"],
        correct_answer_index: 1,
        explanation: "The passage states 'María va al mercado todos los sábados' (María goes to the market every Saturday)."
      },
      {
        question: "¿Cuál es la fruta favorita de María?",
        options: ["La naranja", "El plátano", "La manzana roja", "La pera"],
        correct_answer_index: 2,
        explanation: "The text mentions 'Su fruta favorita es la manzana roja' (Her favorite fruit is the red apple)."
      },
      {
        question: "¿Cuántas manzanas compra María?",
        options: ["Tres", "Cuatro", "Cinco", "Seis"],
        correct_answer_index: 2,
        explanation: "María 'siempre compra cinco manzanas para la semana' (always buys five apples for the week)."
      }
    ]
  },
  {
    passage: "Pedro es estudiante de medicina. Estudia en la universidad de Madrid. Todas las mañanas toma el autobús a las siete. Sus clases empiezan a las ocho y terminan a las dos de la tarde. Después de las clases, estudia en la biblioteca por tres horas.",
    questions: [
      {
        question: "¿Qué estudia Pedro?",
        options: ["Derecho", "Medicina", "Ingeniería", "Arte"],
        correct_answer_index: 1,
        explanation: "The passage clearly states 'Pedro es estudiante de medicina' (Pedro is a medical student)."
      },
      {
        question: "¿A qué hora toma el autobús Pedro?",
        options: ["A las seis", "A las siete", "A las ocho", "A las nueve"],
        correct_answer_index: 1,
        explanation: "The text says 'Todas las mañanas toma el autobús a las siete' (Every morning he takes the bus at seven)."
      },
      {
        question: "¿Dónde estudia Pedro después de las clases?",
        options: ["En casa", "En el parque", "En la biblioteca", "En la cafetería"],
        correct_answer_index: 2,
        explanation: "After classes, Pedro 'estudia en la biblioteca por tres horas' (studies in the library for three hours)."
      }
    ]
  },
  {
    passage: "La familia García vive en una casa grande con jardín. Tienen dos perros y un gato. Los perros se llaman Max y Luna. El gato se llama Misi. Los niños juegan con los animales en el jardín todos los días después de la escuela.",
    questions: [
      {
        question: "¿Cuántos perros tiene la familia García?",
        options: ["Uno", "Dos", "Tres", "Cuatro"],
        correct_answer_index: 1,
        explanation: "The passage mentions 'Tienen dos perros y un gato' (They have two dogs and a cat)."
      },
      {
        question: "¿Cómo se llama el gato?",
        options: ["Max", "Luna", "Misi", "García"],
        correct_answer_index: 2,
        explanation: "The text states 'El gato se llama Misi' (The cat is called Misi)."
      },
      {
        question: "¿Dónde juegan los niños con los animales?",
        options: ["En la casa", "En el parque", "En el jardín", "En la escuela"],
        correct_answer_index: 2,
        explanation: "The children 'juegan con los animales en el jardín' (play with the animals in the garden)."
      }
    ]
  }
];

function generateComprehensionQuestions() {
  const questions = [];
  
  spanishComprehension.forEach((item, passageIndex) => {
    item.questions.forEach((q, questionIndex) => {
      // Generate comprehension questions (can be used for both reading and listening)
      const question = {
        id: uuidv4(),
        language_id: 'es', // Spanish
        category: 'reading/listening',
        question_type: 'comprehension',
        difficulty_level: passageIndex + 1, // 1-3 based on passage complexity
        question_text: `"${item.passage}"\n\n${q.question}`,
        options: q.options,
        correct_answer_index: q.correct_answer_index,
        explanation: q.explanation,
        metadata: {
          passage: item.passage,
          passage_index: passageIndex,
          question_index: questionIndex
        }
      };
      questions.push(question);
    });
  });
  
  return questions;
}

// Generate the questions
const comprehensionQuestions = generateComprehensionQuestions();

// Save to JSON file
const outputPath = path.join(__dirname, 'spanish_comprehension_questions.json');
fs.writeFileSync(outputPath, JSON.stringify(comprehensionQuestions, null, 2));

console.log(`Generated ${comprehensionQuestions.length} reading/listening comprehension questions`);
console.log(`\nSaved to: ${outputPath}`);

// Also create SQL insert statements
const sqlPath = path.join(__dirname, 'insert_comprehension_questions.sql');
const sqlStatements = comprehensionQuestions.map(q => {
  return `INSERT INTO language_questions (id, language_id, category, question_type, difficulty_level, question_text, options, correct_answer_index, explanation, metadata) VALUES (
    '${q.id}',
    '${q.language_id}',
    '${q.category}',
    '${q.question_type}',
    ${q.difficulty_level},
    '${q.question_text.replace(/'/g, "''")}',
    ARRAY[${q.options.map(o => `'${o.replace(/'/g, "''")}'`).join(', ')}],
    ${q.correct_answer_index},
    '${q.explanation.replace(/'/g, "''")}',
    '${JSON.stringify(q.metadata).replace(/'/g, "''")}'::jsonb
  );`;
}).join('\n\n');

fs.writeFileSync(sqlPath, sqlStatements);
console.log(`SQL statements saved to: ${sqlPath}`);