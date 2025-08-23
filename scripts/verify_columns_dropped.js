const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function verifyColumnsDropped() {
  console.log('Verifying columns were dropped\n')
  console.log('=' .repeat(50))
  
  try {
    // Check current columns
    const { data: sample, error } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .limit(1)
    
    if (error) {
      console.error('Error checking table:', error)
      return
    }
    
    if (sample && sample.length > 0) {
      const columns = Object.keys(sample[0])
      console.log('\nCurrent columns in skill_tree_nodes:')
      columns.forEach(col => {
        console.log(`  • ${col}`)
      })
      
      const unwantedColumns = ['type', 'path', 'learning_area']
      const stillPresent = unwantedColumns.filter(col => columns.includes(col))
      
      if (stillPresent.length === 0) {
        console.log('\n✅ SUCCESS! All unwanted columns have been removed')
        console.log('\nRemaining columns are:')
        console.log('  - id (primary key)')
        console.log('  - parent_id (for hierarchy)')
        console.log('  - name (node name)')
        console.log('  - metadata (JSON data)')
        console.log('  - display_order (for sorting)')
        console.log('  - created_at (timestamp)')
        console.log('  - updated_at (timestamp)')
        console.log('  - learning_content_ids (array of content IDs)')
        console.log('  - description (node description)')
        console.log('  - is_hidden (visibility control)')
      } else {
        console.log('\n⚠️  These columns still need to be dropped:', stillPresent)
        console.log('\nPlease run this SQL in Supabase:')
        console.log(`ALTER TABLE skill_tree_nodes DROP COLUMN IF EXISTS ${stillPresent.join(', DROP COLUMN IF EXISTS ')};`)
      }
      
      // Show table stats
      const { count } = await supabase
        .from('skill_tree_nodes')
        .select('*', { count: 'exact', head: true })
      
      console.log(`\n📊 Table Statistics:`)
      console.log(`  Total rows: ${count}`)
      console.log(`  Column count: ${columns.length}`)
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

verifyColumnsDropped()