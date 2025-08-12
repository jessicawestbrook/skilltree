import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

// Get the directory of the current module
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env.local file from project root
dotenv.config({ path: join(__dirname, '..', '..', '.env.local') });

// Initialize Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

console.log('Checking environment variables...');
console.log('Supabase URL:', supabaseUrl ? 'Found' : 'Not found');
console.log('Supabase Anon Key:', supabaseAnonKey ? 'Found' : 'Not found');

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Quiz questions data
const quizQuestions = {
  'symbols-meaning': [
    {
      question: "What is the primary purpose of symbols?",
      options: ["To represent ideas", "To look pretty", "To confuse", "To take up space"],
      correct: 0,
      explanation: "Symbols are visual representations of ideas, concepts, or objects"
    }
  ],
  'quantity-concept': [
    {
      question: "Which represents 'more'?",
      options: ["3 < 5", "5 > 3", "3 = 3", "None"],
      correct: 1,
      explanation: "The symbol > means 'greater than', so 5 > 3 means 5 is more than 3"
    }
  ],
  'cooking-fundamentals': [
    {
      question: "What happens to water at 100°C?",
      options: ["It freezes", "It boils", "Nothing", "It disappears"],
      correct: 1,
      explanation: "Water boils at 100°C (212°F) at sea level"
    }
  ],
  'spanish': [
    {
      question: "How do you say 'Hello' in Spanish?",
      options: ["Bonjour", "Hola", "Ciao", "Guten Tag"],
      correct: 1,
      explanation: "Hola is the Spanish greeting for 'Hello'"
    }
  ],
  'french': [
    {
      question: "What does 'Bonjour' mean in French?",
      options: ["Goodbye", "Hello", "Please", "Thank you"],
      correct: 1,
      explanation: "Bonjour means 'Hello' or 'Good day' in French"
    }
  ],
  'programming-basics': [
    {
      question: "What is a variable in programming?",
      options: ["A fixed number", "A storage location with a name", "A type of loop", "An error"],
      correct: 1,
      explanation: "A variable is a storage location that has a name and can hold data"
    }
  ],
  'javascript': [
    {
      question: "Which keyword declares a constant in JavaScript?",
      options: ["var", "let", "const", "constant"],
      correct: 2,
      explanation: "The 'const' keyword declares a constant variable that cannot be reassigned"
    }
  ],
  'python': [
    {
      question: "How do you create a list in Python?",
      options: ["[]", "{}", "()", "<>"],
      correct: 0,
      explanation: "Square brackets [] are used to create lists in Python"
    }
  ],
  'limits': [
    {
      question: "What is the limit of 1/x as x approaches infinity?",
      options: ["0", "1", "Infinity", "Undefined"],
      correct: 0,
      explanation: "As x approaches infinity, 1/x approaches 0"
    }
  ],
  'derivatives': [
    {
      question: "What is the derivative of x²?",
      options: ["x", "2x", "x²", "2"],
      correct: 1,
      explanation: "The derivative of x² is 2x using the power rule"
    }
  ],
  'cell-structure': [
    {
      question: "What is the control center of a cell?",
      options: ["Mitochondria", "Nucleus", "Ribosome", "Cell wall"],
      correct: 1,
      explanation: "The nucleus is the control center containing the cell's genetic material"
    }
  ],
  'html-css': [
    {
      question: "Which HTML tag is used for the largest heading?",
      options: ["<h6>", "<h1>", "<header>", "<head>"],
      correct: 1,
      explanation: "<h1> is the largest heading tag in HTML"
    }
  ],
  'drawing-basics': [
    {
      question: "What is the technique of shading using dots called?",
      options: ["Hatching", "Stippling", "Blending", "Sketching"],
      correct: 1,
      explanation: "Stippling is a drawing technique that uses dots to create shading and texture"
    }
  ],
  'music-theory-basics': [
    {
      question: "How many notes are in a major scale?",
      options: ["5", "7", "8", "12"],
      correct: 1,
      explanation: "A major scale contains 7 unique notes before repeating at the octave"
    }
  ]
};

async function migrateQuestions() {
  console.log('Starting quiz questions migration to Supabase...\n');

  let totalInserted = 0;
  let totalFailed = 0;

  for (const [nodeId, questions] of Object.entries(quizQuestions)) {
    console.log(`Migrating questions for node: ${nodeId}`);
    
    for (const question of questions) {
      try {
        // Prepare the data for insertion
        const questionData = {
          node_id: nodeId,
          question: question.question,
          options: question.options, // Supabase will handle JSON array
          correct_answer: question.correct,
          explanation: question.explanation,
          created_at: new Date().toISOString()
        };

        // Insert into Supabase
        const { error } = await supabase
          .from('quiz_questions')
          .insert([questionData])
          .select();

        if (error) {
          console.error(`  ❌ Failed to insert question for ${nodeId}:`, error.message);
          totalFailed++;
        } else {
          console.log(`  ✅ Inserted: "${question.question.substring(0, 50)}..."`);
          totalInserted++;
        }
      } catch (err) {
        console.error(`  ❌ Error processing question for ${nodeId}:`, err);
        totalFailed++;
      }
    }
  }

  console.log('\n========================================');
  console.log('Migration Summary:');
  console.log(`✅ Successfully inserted: ${totalInserted} questions`);
  console.log(`❌ Failed: ${totalFailed} questions`);
  console.log('========================================\n');

  // Verify the migration
  console.log('Verifying migration...');
  const { data: count, error: countError } = await supabase
    .from('quiz_questions')
    .select('*', { count: 'exact', head: true });

  if (!countError) {
    console.log(`Total questions in database: ${count}`);
  }
}

// Run the migration
migrateQuestions()
  .then(() => {
    console.log('Migration completed!');
    process.exit(0);
  })
  .catch((err) => {
    console.error('Migration failed:', err);
    process.exit(1);
  });