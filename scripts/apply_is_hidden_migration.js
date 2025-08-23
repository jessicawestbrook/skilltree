const { createClient } = require('@supabase/supabase-js')
const fs = require('fs')
const path = require('path')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function applyMigration() {
  try {
    console.log('Applying is_hidden migration...\n')
    
    // Read the migration file
    const migrationPath = path.join(__dirname, '..', 'supabase', 'migrations', '20250823_add_is_hidden_to_skill_nodes.sql')
    const migrationSQL = fs.readFileSync(migrationPath, 'utf8')
    
    // Split by semicolons and execute each statement
    const statements = migrationSQL
      .split(';')
      .map(s => s.trim())
      .filter(s => s.length > 0 && !s.startsWith('--'))
    
    for (const statement of statements) {
      console.log('Executing:', statement.substring(0, 50) + '...')
      
      const { error } = await supabase.rpc('exec_sql', {
        sql: statement + ';'
      })
      
      if (error) {
        // Try direct query if exec_sql doesn't work
        console.log('exec_sql failed, trying direct approach...')
        // For ALTER TABLE, we'll check if column exists first
        if (statement.includes('ALTER TABLE')) {
          const { data: columns } = await supabase
            .from('skill_tree_nodes')
            .select('*')
            .limit(1)
          
          if (columns && columns.length > 0 && !columns[0].hasOwnProperty('is_hidden')) {
            console.log('Column does not exist yet, would need to add via Supabase dashboard')
          } else {
            console.log('Column already exists')
          }
        }
      } else {
        console.log('✅ Success')
      }
    }
    
    // Verify the column exists
    console.log('\nVerifying migration...')
    const { data: sample, error: verifyError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, is_hidden')
      .limit(1)
    
    if (verifyError) {
      console.log('❌ Column is_hidden not found. Please add it manually via Supabase dashboard:')
      console.log('   1. Go to Table Editor > skill_tree_nodes')
      console.log('   2. Add column: is_hidden (boolean, default: false)')
      console.log('   3. Save changes')
    } else {
      console.log('✅ Migration successful! Column is_hidden exists')
      console.log('Sample record:', sample[0])
    }
    
  } catch (error) {
    console.error('Error applying migration:', error)
  }
}

applyMigration()