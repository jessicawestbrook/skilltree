const { createClient } = require('@supabase/supabase-js')
const fs = require('fs')
const path = require('path')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function executeSQLFix() {
  console.log('Executing signup trigger fix...\n')
  console.log('=' .repeat(50))
  
  try {
    // Read the SQL file
    const sqlPath = path.join(__dirname, 'fix_signup_trigger.sql')
    const sqlContent = fs.readFileSync(sqlPath, 'utf8')
    
    // Split SQL into individual statements
    const statements = sqlContent
      .split(/;(?=\s*(?:--|$|CREATE|DROP|SELECT|ALTER|GRANT|DELETE))/i)
      .map(s => s.trim())
      .filter(s => s && !s.startsWith('--'))
    
    console.log(`Found ${statements.length} SQL statements to execute\n`)
    
    for (let i = 0; i < statements.length; i++) {
      const statement = statements[i].trim()
      if (!statement) continue
      
      // Get first line for logging
      const firstLine = statement.split('\n')[0].substring(0, 60)
      console.log(`\n[${i + 1}/${statements.length}] Executing: ${firstLine}...`)
      
      // Execute via RPC for DDL statements
      if (statement.match(/^(CREATE|DROP|ALTER|GRANT)/i)) {
        const { error } = await supabase.rpc('exec_sql', { 
          sql_query: statement + ';'
        }).single()
        
        if (error) {
          if (error.message?.includes('function exec_sql does not exist')) {
            console.log('⚠️  Cannot execute DDL directly. Please run in Supabase SQL Editor')
            console.log('\nSQL to execute:')
            console.log('-'.repeat(50))
            console.log(statement + ';')
            console.log('-'.repeat(50))
          } else {
            console.log('❌ Error:', error.message)
          }
        } else {
          console.log('✅ Success')
        }
      } else {
        // For SELECT statements, use regular query
        const { data, error } = await supabase
          .from('profiles')
          .select('*')
          .limit(0)
        
        if (error) {
          console.log('❌ Error:', error.message)
        } else {
          console.log('✅ Query executed')
        }
      }
    }
    
    console.log('\n' + '=' .repeat(50))
    console.log('\n📝 IMPORTANT: Since DDL statements cannot be executed directly,')
    console.log('please run the following in Supabase SQL Editor:\n')
    console.log('1. Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/sql/new')
    console.log('2. Copy the contents of scripts/fix_signup_trigger.sql')
    console.log('3. Paste and click "Run"')
    console.log('4. Then test signup again with jessicawestbrook88@gmail.com')
    
  } catch (error) {
    console.error('Error:', error)
  }
}

executeSQLFix()