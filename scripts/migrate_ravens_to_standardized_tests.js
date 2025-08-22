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
 * Now with full metadata for the standardized tests system
 */
const ravensStyleQuestions = [
  {
    question_number: 1,
    section: 'Pattern Recognition',
    question_text: 'Look at this 2x2 pattern. Which option completes the bottom-right position?\n\nPattern: Top-left has 1 circle, top-right has 2 circles, bottom-left has 3 circles, bottom-right is missing.',
    question_type: 'multiple_choice',
    options: ['4 circles', '2 circles', '1 circle', '5 circles'],
    correct_answer: 0,
    explanation: 'The pattern increases by 1 circle in each position moving left-to-right, top-to-bottom: 1, 2, 3, so the next should be 4.',
    difficulty: 'easy',
    points_value: 1,
    time_limit_seconds: 45,
    pattern_type: 'arithmetic_progression',
    cognitive_area: 'fluid_reasoning',
    topic: 'number_sequences'
  },
  {
    question_number: 2,
    section: 'Pattern Recognition',
    question_text: 'Examine this 3x3 matrix. What shape belongs in the missing bottom-right corner?\n\nPattern: Each row shows shapes rotating 90° clockwise. Row 1: triangle up → triangle right → triangle down. Row 2: square → diamond → square rotated. Row 3: circle → oval horizontal → [missing]',
    question_type: 'multiple_choice',
    options: ['Oval vertical', 'Circle', 'Triangle up', 'Square'],
    correct_answer: 0,
    explanation: 'Each row shows a shape rotating 90° clockwise. Row 3 starts with circle, then oval horizontal, so next is oval vertical.',
    difficulty: 'medium',
    points_value: 2,
    time_limit_seconds: 60,
    pattern_type: 'rotation',
    cognitive_area: 'visual_spatial_processing',
    topic: 'spatial_transformation'
  },
  {
    question_number: 3,
    section: 'Pattern Recognition',
    question_text: 'Study this 2x2 matrix pattern. Which option should replace the question mark?\n\nPattern: Top-left: 2 black dots, Top-right: 1 black dot, Bottom-left: 3 black dots, Bottom-right: ?',
    question_type: 'multiple_choice',
    options: ['2 black dots', '4 black dots', '1 black dot', '0 black dots'],
    correct_answer: 2,
    explanation: 'The pattern alternates: top row decreases (2→1), bottom row increases then decreases (3→1). Following the alternating pattern.',
    difficulty: 'medium',
    points_value: 2,
    time_limit_seconds: 50,
    pattern_type: 'alternating_sequence',
    cognitive_area: 'fluid_reasoning',
    topic: 'logical_patterns'
  },
  {
    question_number: 4,
    section: 'Pattern Recognition',
    question_text: 'Analyze this 3x3 matrix pattern. What should appear in the empty bottom-right cell?\n\nPattern: Row 1: triangle, square, triangle+square combined. Row 2: circle, diamond, circle+diamond combined. Row 3: hexagon, star, [missing]',
    question_type: 'multiple_choice',
    options: ['Hexagon+star combined', 'Star alone', 'Hexagon alone', 'Circle+triangle'],
    correct_answer: 0,
    explanation: 'Each row follows the pattern: shape A + shape B = combination of both. Row 3: hexagon + star = hexagon+star combined.',
    difficulty: 'hard',
    points_value: 3,
    time_limit_seconds: 75,
    pattern_type: 'addition_combination',
    cognitive_area: 'fluid_reasoning',
    topic: 'logical_operations'
  },
  {
    question_number: 5,
    section: 'Pattern Recognition',
    question_text: 'Complete the sequence in this 2x3 matrix.\n\nPattern: Top row shows black squares getting smaller: large → medium → small. Bottom row shows white circles getting larger: small → medium → [missing]',
    question_type: 'multiple_choice',
    options: ['Large white circle', 'Small white circle', 'Medium black square', 'Large black circle'],
    correct_answer: 0,
    explanation: 'Top row: black squares decrease in size. Bottom row: white circles increase in size. The patterns are inverse progressions.',
    difficulty: 'medium',
    points_value: 2,
    time_limit_seconds: 55,
    pattern_type: 'inverse_size_progression',
    cognitive_area: 'visual_spatial_processing',
    topic: 'size_relationships'
  },
  {
    question_number: 6,
    section: 'Pattern Recognition',
    question_text: 'What pattern completes this 3x3 matrix?\n\nPattern: Row 1: 1 vertical line, 2 vertical lines, 3 vertical lines. Row 2: 1 horizontal line, 2 horizontal lines, 3 horizontal lines. Row 3: 1 diagonal line, 2 diagonal lines, [missing]',
    question_type: 'multiple_choice',
    options: ['3 diagonal lines', '1 diagonal line', '3 vertical lines', '2 horizontal lines'],
    correct_answer: 0,
    explanation: 'Each row increases the count of a specific line type: vertical (row 1), horizontal (row 2), diagonal (row 3). Row 3 needs 3 diagonal lines.',
    difficulty: 'easy',
    points_value: 1,
    time_limit_seconds: 40,
    pattern_type: 'counting_progression',
    cognitive_area: 'fluid_reasoning',
    topic: 'counting_patterns'
  },
  {
    question_number: 7,
    section: 'Pattern Recognition',
    question_text: 'Identify the missing element in this spatial pattern.\n\nPattern: Top-left: filled triangle pointing up, Top-right: empty triangle pointing down, Bottom-left: filled circle, Bottom-right: [missing]',
    question_type: 'multiple_choice',
    options: ['Empty circle', 'Filled triangle up', 'Empty triangle up', 'Filled square'],
    correct_answer: 0,
    explanation: 'Pattern alternates between filled and empty shapes. Top row: filled→empty. Bottom row follows same pattern: filled→empty.',
    difficulty: 'medium',
    points_value: 2,
    time_limit_seconds: 50,
    pattern_type: 'fill_alternation',
    cognitive_area: 'visual_spatial_processing',
    topic: 'visual_patterns'
  },
  {
    question_number: 8,
    section: 'Pattern Recognition',
    question_text: 'Complete this complex matrix pattern.\n\nPattern: 3x3 grid where shapes transform systematically. Each position shows overlapping geometric forms that follow a rotation and layering sequence.',
    question_type: 'multiple_choice',
    options: ['Two overlapping triangles', 'Single hexagon', 'Three separate circles', 'Overlapping square and circle'],
    correct_answer: 3,
    explanation: 'The matrix shows systematic overlapping of geometric shapes. Following the established pattern of shape combinations and rotations.',
    difficulty: 'hard',
    points_value: 3,
    time_limit_seconds: 90,
    pattern_type: 'complex_overlay',
    cognitive_area: 'visual_spatial_processing',
    topic: 'complex_spatial_relationships'
  },
  {
    question_number: 9,
    section: 'Pattern Recognition',
    question_text: 'What comes next in this logical sequence matrix?\n\nPattern: 3x3 grid where shapes transform in cycles: triangles become squares, squares become circles, circles become triangles.',
    question_type: 'multiple_choice',
    options: ['Triangle', 'Square', 'Circle', 'Diamond'],
    correct_answer: 0,
    explanation: 'Systematic transformation cycle: triangle→square→circle→triangle. Following this cycle, the next transformation results in a triangle.',
    difficulty: 'hard',
    points_value: 3,
    time_limit_seconds: 85,
    pattern_type: 'cyclic_transformation',
    cognitive_area: 'fluid_reasoning',
    topic: 'logical_cycles'
  },
  {
    question_number: 10,
    section: 'Pattern Recognition',
    question_text: 'Find the pattern rule and complete the matrix.\n\nPattern: 2x2 grid where top row shows symmetrical shapes, bottom row shows asymmetrical versions of the same shapes.',
    question_type: 'multiple_choice',
    options: ['Asymmetrical star', 'Symmetrical star', 'Asymmetrical circle', 'Symmetrical triangle'],
    correct_answer: 0,
    explanation: 'Rule: top row shows symmetrical shapes, bottom row shows their asymmetrical counterparts. Following this rule for the missing piece.',
    difficulty: 'medium',
    points_value: 2,
    time_limit_seconds: 65,
    pattern_type: 'symmetry_transformation',
    cognitive_area: 'visual_spatial_processing',
    topic: 'symmetry_concepts'
  },
  {
    question_number: 11,
    section: 'Numerical Reasoning',
    question_text: 'Analyze this numerical pattern matrix and find the missing number.\n\nPattern: Row 1: 2, 4, 8. Row 2: 3, 6, 12. Row 3: 5, 10, [missing]',
    question_type: 'multiple_choice',
    options: ['15', '20', '25', '30'],
    correct_answer: 1,
    explanation: 'Each row follows multiplication by 2: first number × 2 = second number, second number × 2 = third number. Row 3: 5 × 2 = 10, 10 × 2 = 20.',
    difficulty: 'easy',
    points_value: 1,
    time_limit_seconds: 35,
    pattern_type: 'multiplication_sequence',
    cognitive_area: 'quantitative_reasoning',
    topic: 'numerical_patterns'
  },
  {
    question_number: 12,
    section: 'Numerical Reasoning',
    question_text: 'Complete this advanced numerical matrix pattern.\n\nPattern: Row 1: 1, 4, 9. Row 2: 4, 16, 36. Row 3: 9, 36, [missing]',
    question_type: 'multiple_choice',
    options: ['64', '81', '100', '121'],
    correct_answer: 1,
    explanation: 'Pattern shows perfect squares in sequence: Row 1: 1², 2², 3². Row 2: 2², 4², 6². Row 3: 3², 6², 9². So 9² = 81.',
    difficulty: 'hard',
    points_value: 3,
    time_limit_seconds: 80,
    pattern_type: 'square_number_pattern',
    cognitive_area: 'quantitative_reasoning',
    topic: 'advanced_numerical_relationships'
  }
]

async function migrateRavensToStandardizedTests() {
  console.log('=== Migrating Ravens Questions to Standardized Tests System ===\n')
  
  try {
    // Step 1: Find the Ravens test record
    const { data: ravensTest, error: testError } = await supabase
      .from('standardized_tests')
      .select('*')
      .eq('subtype', 'ravens_matrices')
      .single()
    
    if (testError || !ravensTest) {
      console.error('Ravens test not found. Please run setup_standardized_tests.js first.')
      console.error('Error:', testError)
      return false
    }
    
    console.log(`Found Ravens test: ${ravensTest.name} (${ravensTest.id})`)
    
    // Step 2: Check if questions already exist for this test
    const { data: existingQuestions } = await supabase
      .from('standardized_test_questions')
      .select('id')
      .eq('test_id', ravensTest.id)
    
    if (existingQuestions && existingQuestions.length > 0) {
      console.log(`Found ${existingQuestions.length} existing questions for this test.`)
      console.log('Skipping insertion to avoid duplicates.')
      return true
    }
    
    // Step 3: Prepare questions for insertion
    const questionsToInsert = ravensStyleQuestions.map(q => ({
      id: randomUUID(),
      test_id: ravensTest.id,
      question_number: q.question_number,
      section: q.section,
      question_text: q.question_text,
      question_type: q.question_type,
      options: q.options,
      correct_answer: q.correct_answer,
      explanation: q.explanation,
      difficulty: q.difficulty,
      points_value: q.points_value,
      time_limit_seconds: q.time_limit_seconds,
      image_url: null,
      audio_url: null,
      pattern_type: q.pattern_type,
      cognitive_area: q.cognitive_area,
      topic: q.topic,
      source_url: 'Original questions inspired by Raven\'s Progressive Matrices format',
      metadata: {
        test_version: '1.0',
        created_by: 'automated_migration',
        original_inspiration: 'ravens_progressive_matrices'
      }
    }))
    
    console.log(`Preparing to insert ${questionsToInsert.length} Ravens questions...`)
    
    // Step 4: Insert questions in batches
    const batchSize = 4
    const insertedQuestions = []
    
    for (let i = 0; i < questionsToInsert.length; i += batchSize) {
      const batch = questionsToInsert.slice(i, i + batchSize)
      
      console.log(`Inserting batch ${Math.floor(i/batchSize) + 1}/${Math.ceil(questionsToInsert.length/batchSize)}...`)
      
      const { data, error } = await supabase
        .from('standardized_test_questions')
        .insert(batch)
        .select('id, question_number, difficulty, pattern_type')
      
      if (error) {
        console.error(`Error inserting batch ${Math.floor(i/batchSize) + 1}:`, error)
        throw error
      }
      
      if (data) {
        insertedQuestions.push(...data)
        console.log(`✓ Successfully inserted ${data.length} questions`)
        data.forEach(q => {
          console.log(`  - Question ${q.question_number}: ${q.difficulty} (${q.pattern_type})`)
        })
      }
    }
    
    console.log(`\n✓ Successfully migrated all ${insertedQuestions.length} Ravens questions!`)
    
    // Step 5: Generate verification queries
    console.log('\n=== Verification Queries ===')
    
    const testQuery = `
-- View the Ravens test
SELECT * FROM standardized_tests 
WHERE subtype = 'ravens_matrices';`
    
    const questionsQuery = `
-- View all Ravens questions
SELECT 
  q.question_number,
  LEFT(q.question_text, 60) as question_preview,
  q.difficulty,
  q.pattern_type,
  q.cognitive_area,
  q.points_value,
  q.time_limit_seconds
FROM standardized_test_questions q
JOIN standardized_tests t ON q.test_id = t.id
WHERE t.subtype = 'ravens_matrices'
ORDER BY q.question_number;`
    
    const summaryQuery = `
-- Summary by difficulty and cognitive area
SELECT 
  q.difficulty,
  q.cognitive_area,
  COUNT(*) as question_count,
  AVG(q.points_value) as avg_points,
  AVG(q.time_limit_seconds) as avg_time_limit
FROM standardized_test_questions q
JOIN standardized_tests t ON q.test_id = t.id
WHERE t.subtype = 'ravens_matrices'
GROUP BY q.difficulty, q.cognitive_area
ORDER BY q.difficulty, q.cognitive_area;`
    
    console.log('Test overview:', testQuery)
    console.log('\nQuestions overview:', questionsQuery)
    console.log('\nSummary stats:', summaryQuery)
    
    return insertedQuestions
    
  } catch (error) {
    console.error('Migration failed:', error)
    throw error
  }
}

async function createTestAttemptExample() {
  console.log('\n=== Creating Example Test Attempt ===')
  
  // This would be called when a user starts taking the test
  const exampleUserId = '00000000-0000-0000-0000-000000000000' // Placeholder
  
  try {
    const { data: ravensTest } = await supabase
      .from('standardized_tests')
      .select('id')
      .eq('subtype', 'ravens_matrices')
      .single()
    
    if (!ravensTest) {
      console.log('Ravens test not found for example attempt')
      return
    }
    
    console.log('Example code for starting a test attempt:')
    console.log(`
const startTestAttempt = async (userId: string) => {
  const { data, error } = await supabase
    .from('user_test_attempts')
    .insert({
      user_id: userId,
      test_id: '${ravensTest.id}',
      attempt_number: 1,
      is_practice: true
    })
    .select()
    .single()
  
  return data
}`)
    
  } catch (error) {
    console.error('Error creating example:', error)
  }
}

// Main execution
async function main() {
  try {
    const insertedQuestions = await migrateRavensToStandardizedTests()
    await createTestAttemptExample()
    
    console.log('\n=== Migration Complete ===')
    console.log('✓ Ravens questions migrated to standardized tests system')
    console.log('✓ Full metadata preserved (pattern types, cognitive areas, etc.)')
    console.log('✓ Ready for IQ test taking and scoring')
    console.log('\nNext steps:')
    console.log('1. Update IQTestPage.tsx to use new standardized_test_questions table')
    console.log('2. Implement scoring using the new user_test_attempts system')
    console.log('3. Add other standardized tests (SAT, ACT, etc.) using same system')
    
  } catch (error) {
    console.error('Migration failed:', error)
    process.exit(1)
  }
}

if (require.main === module) {
  main()
}

module.exports = {
  ravensStyleQuestions,
  migrateRavensToStandardizedTests
}