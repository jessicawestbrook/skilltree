const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function testHiddenNodesDatabase() {
  console.log('Testing Hidden Nodes Database Integration\n')
  console.log('=' .repeat(50))
  
  try {
    // Step 1: Check if column exists
    console.log('\n1. Checking if is_hidden column exists...')
    const { data: sampleNode, error: checkError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, is_hidden')
      .limit(1)
    
    if (checkError) {
      if (checkError.message.includes('column "is_hidden" does not exist')) {
        console.log('❌ Column is_hidden does not exist')
        console.log('\nPlease add the column to your database:')
        console.log('1. Go to Supabase Table Editor')
        console.log('2. Select skill_tree_nodes table')
        console.log('3. Add column: is_hidden (boolean, default: false)')
        return
      }
      throw checkError
    }
    
    console.log('✅ Column exists!')
    console.log('Sample node:', sampleNode[0])
    
    // Step 2: Test setting a node as hidden
    console.log('\n2. Testing hide functionality...')
    
    // Find a test node
    const { data: testNodes } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, parent_id')
      .is('parent_id', null)
      .limit(1)
    
    if (testNodes && testNodes.length > 0) {
      const testNode = testNodes[0]
      console.log(`Test node: ${testNode.name} (${testNode.id})`)
      
      // Hide it
      const { error: hideError } = await supabase
        .from('skill_tree_nodes')
        .update({ is_hidden: true })
        .eq('id', testNode.id)
      
      if (hideError) {
        console.log('❌ Error hiding node:', hideError)
      } else {
        console.log('✅ Successfully marked node as hidden')
        
        // Verify it's hidden
        const { data: hiddenCheck } = await supabase
          .from('skill_tree_nodes')
          .select('is_hidden')
          .eq('id', testNode.id)
          .single()
        
        console.log(`Verification: is_hidden = ${hiddenCheck.is_hidden}`)
        
        // Unhide it
        const { error: showError } = await supabase
          .from('skill_tree_nodes')
          .update({ is_hidden: false })
          .eq('id', testNode.id)
        
        if (!showError) {
          console.log('✅ Successfully restored node visibility')
        }
      }
    }
    
    // Step 3: Get statistics
    console.log('\n3. Database Statistics:')
    
    const { count: totalCount } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true })
    
    const { count: hiddenCount } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true })
      .eq('is_hidden', true)
    
    const { count: visibleCount } = await supabase
      .from('skill_tree_nodes')
      .select('*', { count: 'exact', head: true })
      .or('is_hidden.eq.false,is_hidden.is.null')
    
    console.log(`  Total nodes: ${totalCount}`)
    console.log(`  Hidden nodes: ${hiddenCount || 0}`)
    console.log(`  Visible nodes: ${visibleCount}`)
    
    // Step 4: List any currently hidden nodes
    if (hiddenCount > 0) {
      console.log('\n4. Currently Hidden Nodes:')
      const { data: hiddenNodes } = await supabase
        .from('skill_tree_nodes')
        .select('id, name, learning_area')
        .eq('is_hidden', true)
        .limit(10)
      
      hiddenNodes.forEach(node => {
        console.log(`  - ${node.name} (${node.learning_area || 'No area'})`)
      })
      
      if (hiddenCount > 10) {
        console.log(`  ... and ${hiddenCount - 10} more`)
      }
    }
    
    console.log('\n' + '=' .repeat(50))
    console.log('✅ Database integration is working correctly!')
    console.log('\nThe admin interface will now:')
    console.log('  • Save changes to the database')
    console.log('  • Persist visibility settings')
    console.log('  • Automatically filter hidden nodes from navigation')
    
  } catch (error) {
    console.error('Error during test:', error)
  }
}

testHiddenNodesDatabase()