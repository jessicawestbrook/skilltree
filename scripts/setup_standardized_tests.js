const { createClient } = require('@supabase/supabase-js')
const fs = require('fs')
const path = require('path')
require('dotenv').config({ path: '.env.local' })

// Initialize Supabase client
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function setupStandardizedTestsTables() {
  console.log('=== Setting Up Standardized Tests System ===\n')
  
  try {
    // Read the SQL schema file
    const schemaPath = path.join(__dirname, 'create_standardized_tests_schema.sql')
    const schemaSql = fs.readFileSync(schemaPath, 'utf8')
    
    // Split into individual statements (simple approach)
    const statements = schemaSql
      .split(';')
      .map(stmt => stmt.trim())
      .filter(stmt => stmt.length > 0 && !stmt.startsWith('--'))
    
    console.log(`Executing ${statements.length} SQL statements...`)
    
    // Execute each statement
    for (let i = 0; i < statements.length; i++) {
      const statement = statements[i]
      if (statement.trim()) {
        try {
          const { error } = await supabase.rpc('execute_sql', { sql_query: statement })
          
          if (error) {
            // Try alternative method for table creation
            console.log(`Retrying statement ${i + 1} with alternative method...`)
            const { error: altError } = await supabase.from('_schema').select('*').limit(1)
            // This is a fallback - in practice, we'll need to use Supabase dashboard or direct SQL
            console.log(`Statement ${i + 1}: May need manual execution`)
          } else {
            console.log(`✓ Statement ${i + 1} executed successfully`)
          }
        } catch (err) {
          console.log(`Statement ${i + 1}: ${err.message}`)
        }
      }
    }
    
    console.log('\n=== Manual Setup Required ===')
    console.log('Supabase client cannot execute DDL statements directly.')
    console.log('Please run the following SQL in your Supabase SQL Editor:')
    console.log(`\nFile: ${schemaPath}`)
    console.log('\nOr copy the SQL from the schema file and paste it into Supabase Dashboard > SQL Editor')
    
    return true
    
  } catch (error) {
    console.error('Setup failed:', error)
    throw error
  }
}

async function insertInitialTestData() {
  console.log('\n=== Inserting Initial Test Data ===\n')
  
  try {
    // Check if tables exist by trying to query them
    const { data: existingTests, error } = await supabase
      .from('standardized_tests')
      .select('id, name')
      .limit(1)
    
    if (error) {
      console.log('Tables not yet created. Please run the SQL schema first.')
      return false
    }
    
    // Insert Ravens Progressive Matrices test
    const ravensTest = {
      name: "Raven's Progressive Matrices Style Test",
      test_type: 'iq',
      subtype: 'ravens_matrices',
      description: 'Non-verbal pattern recognition test inspired by Raven\'s Progressive Matrices. Tests abstract reasoning and visual processing skills through matrix completion puzzles.',
      total_questions: 12,
      time_limit_minutes: 20,
      scoring_method: 'iq_scale',
      max_score: 160,
      min_score: 70,
      passing_score: 100,
      source_url: 'Original questions inspired by Raven\'s Progressive Matrices format',
      version: '1.0',
      is_active: true
    }
    
    const { data: insertedTest, error: testError } = await supabase
      .from('standardized_tests')
      .insert(ravensTest)
      .select()
      .single()
    
    if (testError) {
      console.error('Error inserting Ravens test:', testError)
      throw testError
    }
    
    console.log('✓ Created Ravens Progressive Matrices test:', insertedTest.id)
    
    // Insert Stanford-Binet style test
    const stanfordBinetTest = {
      name: "Stanford-Binet Style Intelligence Scale",
      test_type: 'iq',
      subtype: 'stanford_binet',
      description: 'Comprehensive cognitive assessment covering five factors: Fluid Reasoning, Knowledge, Quantitative Reasoning, Visual-Spatial Processing, and Working Memory.',
      total_questions: 50,
      time_limit_minutes: 45,
      scoring_method: 'iq_scale',
      max_score: 160,
      min_score: 70,
      passing_score: 100,
      source_url: 'Original questions inspired by Stanford-Binet Intelligence Scales format',
      version: '1.0',
      is_active: true
    }
    
    const { data: stanfordTest, error: stanfordError } = await supabase
      .from('standardized_tests')
      .insert(stanfordBinetTest)
      .select()
      .single()
    
    if (stanfordError) {
      console.error('Error inserting Stanford-Binet test:', stanfordError)
      throw stanfordError
    }
    
    console.log('✓ Created Stanford-Binet style test:', stanfordTest.id)
    
    // Insert test sections for Stanford-Binet
    const stanfordSections = [
      {
        test_id: stanfordTest.id,
        section_name: 'Fluid Reasoning',
        section_order: 1,
        description: 'Pattern recognition, logical thinking, and novel problem solving',
        time_limit_minutes: 10,
        question_count: 10,
        scoring_weight: 1.0
      },
      {
        test_id: stanfordTest.id,
        section_name: 'Knowledge',
        section_order: 2,
        description: 'Vocabulary, general information, and crystallized intelligence',
        time_limit_minutes: 10,
        question_count: 10,
        scoring_weight: 1.0
      },
      {
        test_id: stanfordTest.id,
        section_name: 'Quantitative Reasoning',
        section_order: 3,
        description: 'Mathematical concepts, number skills, and quantitative problem solving',
        time_limit_minutes: 10,
        question_count: 10,
        scoring_weight: 1.0
      },
      {
        test_id: stanfordTest.id,
        section_name: 'Visual-Spatial Processing',
        section_order: 4,
        description: 'Spatial relationships, visual patterns, and mental rotation',
        time_limit_minutes: 10,
        question_count: 10,
        scoring_weight: 1.0
      },
      {
        test_id: stanfordTest.id,
        section_name: 'Working Memory',
        section_order: 5,
        description: 'Short-term memory, attention, and cognitive control',
        time_limit_minutes: 5,
        question_count: 10,
        scoring_weight: 1.0
      }
    ]
    
    const { data: insertedSections, error: sectionsError } = await supabase
      .from('test_sections')
      .insert(stanfordSections)
      .select()
    
    if (sectionsError) {
      console.error('Error inserting test sections:', sectionsError)
      throw sectionsError
    }
    
    console.log(`✓ Created ${insertedSections.length} test sections for Stanford-Binet`)
    
    return { ravensTest: insertedTest, stanfordTest, sections: insertedSections }
    
  } catch (error) {
    console.error('Failed to insert initial test data:', error)
    throw error
  }
}

async function createStandardizedTestsTypes() {
  console.log('\n=== Creating TypeScript Types ===\n')
  
  const typesContent = `// Standardized Tests System Types
// Auto-generated from database schema

export interface StandardizedTest {
  id: string
  name: string
  test_type: 'iq' | 'sat' | 'act' | 'lsat' | 'gre' | 'mcat' | 'ap' | 'clep'
  subtype?: string // 'ravens_matrices', 'stanford_binet', 'sat_math', etc.
  description?: string
  total_questions: number
  time_limit_minutes?: number
  scoring_method: 'iq_scale' | 'sat_scale' | 'percentile' | 'raw_score'
  max_score?: number
  min_score?: number
  passing_score?: number
  source_url?: string
  version?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface StandardizedTestQuestion {
  id: string
  test_id: string
  question_number: number
  section?: string
  question_text: string
  question_type: 'multiple_choice' | 'fill_in_blank' | 'essay' | 'true_false'
  options?: string[] // For multiple choice
  correct_answer: any // Index for MC, text for others
  explanation?: string
  difficulty: 'easy' | 'medium' | 'hard' | 'very_hard'
  points_value: number
  time_limit_seconds?: number
  image_url?: string
  audio_url?: string
  pattern_type?: string // For IQ tests
  cognitive_area?: string // 'fluid_reasoning', 'working_memory', etc.
  topic?: string
  source_url?: string
  metadata?: any
  created_at: string
  updated_at: string
}

export interface UserTestAttempt {
  id: string
  user_id: string
  test_id: string
  attempt_number: number
  started_at: string
  completed_at?: string
  time_taken_seconds?: number
  raw_score?: number
  scaled_score?: number // IQ score, SAT score, etc.
  percentile?: number
  section_scores?: Record<string, number>
  is_completed: boolean
  is_practice: boolean
  metadata?: any
  created_at: string
}

export interface UserTestResponse {
  id: string
  attempt_id: string
  question_id: string
  user_answer: any
  is_correct?: boolean
  points_earned: number
  time_taken_seconds?: number
  response_metadata?: any
  created_at: string
}

export interface TestSection {
  id: string
  test_id: string
  section_name: string
  section_order: number
  description?: string
  time_limit_minutes?: number
  question_count?: number
  scoring_weight: number
  created_at: string
}

// Scoring interfaces
export interface IQScoreResult {
  raw_score: number
  iq_score: number
  percentile: number
  cognitive_areas: Record<string, number>
  interpretation: string
  confidence_interval?: [number, number]
}

export interface StandardizedTestResult {
  test_id: string
  test_name: string
  attempt_id: string
  raw_score: number
  scaled_score: number
  percentile: number
  section_scores: Record<string, number>
  time_taken: number
  completion_date: string
  interpretation: string
}
`
  
  const typesPath = path.join(__dirname, '../src/types/standardizedTests.types.ts')
  fs.writeFileSync(typesPath, typesContent)
  
  console.log(`✓ Created TypeScript types: ${typesPath}`)
}

// Main execution
async function main() {
  try {
    console.log('Setting up comprehensive standardized tests system...\n')
    
    // Step 1: Setup tables (requires manual SQL execution)
    await setupStandardizedTestsTables()
    
    // Step 2: Create TypeScript types
    await createStandardizedTestsTypes()
    
    console.log('\n=== Next Steps ===')
    console.log('1. Run the SQL schema in Supabase Dashboard')
    console.log('2. Come back and run: node scripts/setup_standardized_tests.js --insert-data')
    console.log('3. Then migrate Ravens questions to the new system')
    
  } catch (error) {
    console.error('Setup failed:', error)
    process.exit(1)
  }
}

// Handle command line arguments
if (require.main === module) {
  const args = process.argv.slice(2)
  
  if (args.includes('--insert-data')) {
    insertInitialTestData()
      .then(() => {
        console.log('✓ Initial test data inserted successfully')
        process.exit(0)
      })
      .catch((error) => {
        console.error('Failed to insert test data:', error)
        process.exit(1)
      })
  } else {
    main()
  }
}

module.exports = {
  setupStandardizedTestsTables,
  insertInitialTestData,
  createStandardizedTestsTypes
}