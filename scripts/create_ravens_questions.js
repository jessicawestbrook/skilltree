const { createClient } = require('@supabase/supabase-js')
const { randomUUID } = require('crypto')
require('dotenv').config({ path: '.env.local' })

// Initialize Supabase client
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

/**
 * Raven's-style Pattern Recognition Questions
 * Original questions inspired by Raven's Progressive Matrices format
 * These are NOT copied from copyrighted material
 */

const ravensStyleQuestions = [
  {
    question_text: 'Look at this 2x2 pattern. Which option completes the bottom-right position?\n\nPattern: Top-left has 1 circle, top-right has 2 circles, bottom-left has 3 circles, bottom-right is missing.',
    options: ['4 circles', '2 circles', '1 circle', '5 circles'],
    correct_answer: 0,
    explanation: 'The pattern increases by 1 circle in each position moving left-to-right, top-to-bottom: 1, 2, 3, so the next should be 4.',
    difficulty: 'easy'
  },
  {
    question_text: 'Examine this 3x3 matrix. What shape belongs in the missing bottom-right corner?\n\nPattern: Each row shows shapes rotating 90° clockwise. Row 1: triangle up → triangle right → triangle down. Row 2: square → diamond → square rotated. Row 3: circle → oval horizontal → [missing]',
    options: ['Oval vertical', 'Circle', 'Triangle up', 'Square'],
    correct_answer: 0,
    explanation: 'Each row shows a shape rotating 90° clockwise. Row 3 starts with circle, then oval horizontal, so next is oval vertical.',
    difficulty: 'medium'
  },
  {
    question_text: 'Study this 2x2 matrix pattern. Which option should replace the question mark?\n\nPattern: Top-left: 2 black dots, Top-right: 1 black dot, Bottom-left: 3 black dots, Bottom-right: ?',
    options: ['2 black dots', '4 black dots', '1 black dot', '0 black dots'],
    correct_answer: 2,
    explanation: 'The pattern alternates: top row decreases (2→1), bottom row increases then decreases (3→1). Following the alternating pattern.',
    difficulty: 'medium'
  },
  {
    question_text: 'Analyze this 3x3 matrix pattern. What should appear in the empty bottom-right cell?\n\nPattern: Row 1: triangle, square, triangle+square combined. Row 2: circle, diamond, circle+diamond combined. Row 3: hexagon, star, [missing]',
    options: ['Hexagon+star combined', 'Star alone', 'Hexagon alone', 'Circle+triangle'],
    correct_answer: 0,
    explanation: 'Each row follows the pattern: shape A + shape B = combination of both. Row 3: hexagon + star = hexagon+star combined.',
    difficulty: 'hard'
  },
  {
    question_text: 'Complete the sequence in this 2x3 matrix.\n\nPattern: Top row shows black squares getting smaller: large → medium → small. Bottom row shows white circles getting larger: small → medium → [missing]',
    options: ['Large white circle', 'Small white circle', 'Medium black square', 'Large black circle'],
    correct_answer: 0,
    explanation: 'Top row: black squares decrease in size. Bottom row: white circles increase in size. The patterns are inverse progressions.',
    difficulty: 'medium'
  },
  {
    question_text: 'What pattern completes this 3x3 matrix?\n\nPattern: Row 1: 1 vertical line, 2 vertical lines, 3 vertical lines. Row 2: 1 horizontal line, 2 horizontal lines, 3 horizontal lines. Row 3: 1 diagonal line, 2 diagonal lines, [missing]',
    options: ['3 diagonal lines', '1 diagonal line', '3 vertical lines', '2 horizontal lines'],
    correct_answer: 0,
    explanation: 'Each row increases the count of a specific line type: vertical (row 1), horizontal (row 2), diagonal (row 3). Row 3 needs 3 diagonal lines.',
    difficulty: 'easy'
  },
  {
    question_text: 'Identify the missing element in this spatial pattern.\n\nPattern: Top-left: filled triangle pointing up, Top-right: empty triangle pointing down, Bottom-left: filled circle, Bottom-right: [missing]',
    options: ['Empty circle', 'Filled triangle up', 'Empty triangle up', 'Filled square'],
    correct_answer: 0,
    explanation: 'Pattern alternates between filled and empty shapes. Top row: filled→empty. Bottom row follows same pattern: filled→empty.',
    difficulty: 'medium'
  },
  {
    question_text: 'Complete this complex matrix pattern.\n\nPattern: 3x3 grid where shapes transform systematically. Each position shows overlapping geometric forms that follow a rotation and layering sequence.',
    options: ['Two overlapping triangles', 'Single hexagon', 'Three separate circles', 'Overlapping square and circle'],
    correct_answer: 3,
    explanation: 'The matrix shows systematic overlapping of geometric shapes. Following the established pattern of shape combinations and rotations.',
    difficulty: 'hard'
  },
  {
    question_text: 'What comes next in this logical sequence matrix?\n\nPattern: 3x3 grid where shapes transform in cycles: triangles become squares, squares become circles, circles become triangles.',
    options: ['Triangle', 'Square', 'Circle', 'Diamond'],
    correct_answer: 0,
    explanation: 'Systematic transformation cycle: triangle→square→circle→triangle. Following this cycle, the next transformation results in a triangle.',
    difficulty: 'hard'
  },
  {
    question_text: 'Find the pattern rule and complete the matrix.\n\nPattern: 2x2 grid where top row shows symmetrical shapes, bottom row shows asymmetrical versions of the same shapes.',
    options: ['Asymmetrical star', 'Symmetrical star', 'Asymmetrical circle', 'Symmetrical triangle'],
    correct_answer: 0,
    explanation: 'Rule: top row shows symmetrical shapes, bottom row shows their asymmetrical counterparts. Following this rule for the missing piece.',
    difficulty: 'medium'
  },
  {
    question_text: 'Analyze this numerical pattern matrix and find the missing number.\n\nPattern: Row 1: 2, 4, 8. Row 2: 3, 6, 12. Row 3: 5, 10, [missing]',
    options: ['15', '20', '25', '30'],
    correct_answer: 1,
    explanation: 'Each row follows multiplication by 2: first number × 2 = second number, second number × 2 = third number. Row 3: 5 × 2 = 10, 10 × 2 = 20.',
    difficulty: 'easy'
  },
  {
    question_text: 'Complete this advanced numerical matrix pattern.\n\nPattern: Row 1: 1, 4, 9. Row 2: 4, 16, 36. Row 3: 9, 36, [missing]',
    options: ['64', '81', '100', '121'],
    correct_answer: 1,
    explanation: 'Pattern shows perfect squares in sequence: Row 1: 1², 2², 3². Row 2: 2², 4², 6². Row 3: 3², 6², 9². So 9² = 81.',
    difficulty: 'hard'
  }
]

async function insertRavensQuestions() {
  console.log('=== Creating Raven\'s-Style Pattern Recognition Questions ===\n')
  
  try {
    // Check if questions already exist by looking for pattern keywords
    const { data: existingPatternQuestions } = await supabase
      .from('questions')
      .select('id, question_text')
      .or('question_text.ilike.%matrix%,question_text.ilike.%pattern%,question_text.ilike.%grid%')
    
    console.log(`Found ${existingPatternQuestions.length} existing pattern-related questions`)
    
    // Prepare questions for insertion with UUIDs
    const questionsToInsert = ravensStyleQuestions.map(q => ({
      id: randomUUID(),
      question_text: q.question_text,
      options: q.options,
      correct_answer: q.correct_answer,
      explanation: q.explanation,
      difficulty: q.difficulty,
      image_url: null, // No images for these text-based pattern descriptions
      created_at: new Date().toISOString()
    }))
    
    console.log(`Preparing to insert ${questionsToInsert.length} new Ravens-style questions...`)
    
    // Insert questions in smaller batches to avoid timeouts
    const batchSize = 3
    const insertedIds = []
    
    for (let i = 0; i < questionsToInsert.length; i += batchSize) {
      const batch = questionsToInsert.slice(i, i + batchSize)
      
      console.log(`Inserting batch ${Math.floor(i/batchSize) + 1}/${Math.ceil(questionsToInsert.length/batchSize)}...`)
      
      const { data, error } = await supabase
        .from('questions')
        .insert(batch)
        .select('id, question_text, difficulty')
      
      if (error) {
        console.error(`Error inserting batch ${Math.floor(i/batchSize) + 1}:`, error)
        throw error
      }
      
      if (data) {
        insertedIds.push(...data.map(q => q.id))
        console.log(`✓ Successfully inserted ${data.length} questions`)
        data.forEach(q => {
          console.log(`  - ${q.question_text.substring(0, 50)}... (${q.difficulty})`)
        })
      }
    }
    
    console.log(`\n✓ Successfully inserted all ${insertedIds.length} Ravens-style questions!`)
    
    // Verification query
    const verificationQuery = `
SELECT 
  id,
  LEFT(question_text, 60) as question_preview,
  difficulty,
  array_length(options, 1) as option_count,
  correct_answer
FROM questions 
WHERE id IN (${insertedIds.map(id => `'${id}'`).join(', ')})
ORDER BY difficulty, question_text;`
    
    console.log('\n=== Verification Query ===')
    console.log('Run this query in your database to see the inserted Ravens questions:')
    console.log(verificationQuery)
    
    return insertedIds
    
  } catch (error) {
    console.error('Failed to insert Ravens questions:', error)
    throw error
  }
}

// Run if called directly
if (require.main === module) {
  insertRavensQuestions()
    .then((ids) => {
      console.log(`\n✓ Process completed successfully. Inserted ${ids.length} questions.`)
      process.exit(0)
    })
    .catch((error) => {
      console.error('Process failed:', error)
      process.exit(1)
    })
}

module.exports = {
  ravensStyleQuestions,
  insertRavensQuestions
}