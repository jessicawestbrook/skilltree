import { supabase } from '../services/supabase'

export const checkDatabaseTables = async () => {
  try {
    // Query to get all table names from the information schema
    const { data, error } = await supabase
      .from('information_schema.tables')
      .select('table_name')
      .eq('table_schema', 'public')

    if (error) {
      console.error('Error fetching tables from information_schema:', error)
      
      // Alternative: Try to query each expected table
      const tables = [
        'skill_nodes', 'SkillNodes', 'skilltree',
        'questions', 'Questions', 
        'question_options', 'QuestionOptions',
        'starred_categories', 'StarredCategories',
        'user_progress', 'UserProgress',
        'user_question_attempts', 'UserQuestionAttempts',
        'learning_content', 'LearningContent',
        'feedback', 'Feedback'
      ]
      
      console.log('Testing table names:')
      for (const table of tables) {
        try {
          const { error: tableError } = await supabase.from(table).select('*').limit(1)
          if (!tableError) {
            console.log(`✓ Table exists: ${table}`)
          }
        } catch (e) {
          // Table doesn't exist
        }
      }
    } else {
      console.log('Tables in database:', data)
    }
  } catch (err) {
    console.error('Error checking tables:', err)
  }
}

// Run the check
checkDatabaseTables()