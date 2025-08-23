const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function addIsHiddenColumn() {
  try {
    console.log('Checking if is_hidden column exists...\n')
    
    // First, let's check the current structure
    const { data: sample, error: checkError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .limit(1)
    
    if (checkError) {
      console.error('Error checking table:', checkError)
      return
    }
    
    if (sample && sample.length > 0) {
      const columns = Object.keys(sample[0])
      console.log('Current columns:', columns)
      
      if (columns.includes('is_hidden')) {
        console.log('✅ Column is_hidden already exists!')
        
        // Check some stats
        const { count: totalCount } = await supabase
          .from('skill_tree_nodes')
          .select('*', { count: 'exact', head: true })
        
        const { count: hiddenCount } = await supabase
          .from('skill_tree_nodes')
          .select('*', { count: 'exact', head: true })
          .eq('is_hidden', true)
        
        console.log(`\nStats:`)
        console.log(`  Total nodes: ${totalCount}`)
        console.log(`  Hidden nodes: ${hiddenCount || 0}`)
        
      } else {
        console.log('❌ Column is_hidden does not exist')
        console.log('\nTo add it manually:')
        console.log('1. Go to https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/editor')
        console.log('2. Select skill_tree_nodes table')
        console.log('3. Click "Add column"')
        console.log('4. Name: is_hidden')
        console.log('5. Type: boolean')
        console.log('6. Default value: false')
        console.log('7. Click "Save"')
        
        // For now, we'll work without the column and handle it in the application layer
        console.log('\n📝 Note: We can work around this in the application by maintaining a separate hidden nodes list')
      }
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

addIsHiddenColumn()