const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');
const path = require('path');

// Load .env.local file
dotenv.config({ path: path.join(__dirname, '..', '.env.local') });

// Check environment variables
console.log('Loading environment variables from .env.local...\n');

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing Supabase environment variables!');
  console.error('Please ensure your .env.local file contains:');
  console.error('  NEXT_PUBLIC_SUPABASE_URL=your_supabase_url');
  console.error('  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key\n');
  process.exit(1);
}

console.log('✅ Environment variables loaded successfully');
console.log(`📡 Connecting to Supabase at: ${supabaseUrl.substring(0, 30)}...\n`);

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
  'integrals': [
    {
      question: "What is the integral of 2x?",
      options: ["x²", "x² + C", "2x²", "x"],
      correct: 1,
      explanation: "The integral of 2x is x² + C, where C is the constant of integration"
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
  ],
  'descriptive-stats': [
    {
      question: "What is the middle value in a sorted dataset called?",
      options: ["Mean", "Median", "Mode", "Range"],
      correct: 1,
      explanation: "The median is the middle value when data is arranged in order"
    }
  ],
  'arrays-lists': [
    {
      question: "What is the time complexity of accessing an array element by index?",
      options: ["O(1)", "O(n)", "O(log n)", "O(n²)"],
      correct: 0,
      explanation: "Array access by index is O(1) - constant time operation"
    }
  ]
};

async function migrateQuestions() {
  console.log('Starting quiz questions migration to Supabase...\n');

  let totalInserted = 0;
  let totalFailed = 0;
  const errors = [];

  for (const [nodeId, questions] of Object.entries(quizQuestions)) {
    console.log(`📝 Migrating questions for node: ${nodeId}`);
    
    for (const question of questions) {
      try {
        // Prepare the data for insertion
        const questionData = {
          node_id: nodeId,
          question: question.question,
          options: question.options,
          correct_answer: question.correct,
          explanation: question.explanation,
          created_at: new Date().toISOString()
        };

        // Insert into Supabase
        const { data, error } = await supabase
          .from('quiz_questions')
          .insert([questionData])
          .select();

        if (error) {
          console.error(`  ❌ Failed: ${error.message}`);
          errors.push({ nodeId, error: error.message });
          totalFailed++;
        } else {
          console.log(`  ✅ Inserted: "${question.question.substring(0, 40)}..."`);
          totalInserted++;
        }
      } catch (err) {
        console.error(`  ❌ Error: ${err.message}`);
        errors.push({ nodeId, error: err.message });
        totalFailed++;
      }
    }
  }

  console.log('\n========================================');
  console.log('📊 Migration Summary:');
  console.log(`✅ Successfully inserted: ${totalInserted} questions`);
  console.log(`❌ Failed: ${totalFailed} questions`);
  
  if (errors.length > 0) {
    console.log('\n⚠️  Errors encountered:');
    errors.forEach(e => console.log(`  - ${e.nodeId}: ${e.error}`));
  }
  
  console.log('========================================\n');

  // Verify the migration
  console.log('🔍 Verifying migration...');
  const { count, error: countError } = await supabase
    .from('quiz_questions')
    .select('*', { count: 'exact', head: true });

  if (!countError && count !== null) {
    console.log(`✅ Total questions in database: ${count}`);
  } else if (countError) {
    console.log(`❌ Could not verify: ${countError.message}`);
  }
}

// Run the migration
console.log('🚀 NeuroQuest Quiz Questions Migration Tool\n');
console.log('========================================\n');

migrateQuestions()
  .then(() => {
    console.log('\n✨ Migration completed successfully!');
    process.exit(0);
  })
  .catch((err) => {
    console.error('\n❌ Migration failed:', err.message);
    process.exit(1);
  });