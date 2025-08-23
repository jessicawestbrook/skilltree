/**
 * Script to check available math nodes in the database
 */

const { createClient } = require('@supabase/supabase-js')
const path = require('path')

// Load environment variables
require('dotenv').config({ path: path.join(__dirname, '../..', '.env.local') })

// Initialize Supabase client
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function checkMathNodes() {
  console.log('Checking math nodes in database...\n')
  
  try {
    // Get all math-related nodes
    const { data: mathNodes, error } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, type, is_menu_leaf, has_learning_content, learning_area, parent_id')
      .or('learning_area.eq.Mathematics,name.ilike.%mathematics%,name.ilike.%math%')
      .limit(20)
    
    if (error) {
      console.error('Error fetching nodes:', error)
      return
    }
    
    console.log(`Found ${mathNodes.length} math-related nodes (showing first 20):\n`)
    
    // Group by whether they need content
    const needContent = mathNodes.filter(n => 
      n.is_menu_leaf && 
      !n.has_learning_content
    )
    
    const haveContent = mathNodes.filter(n => n.has_learning_content)
    
    console.log('Nodes needing content:')
    needContent.forEach(node => {
      console.log(`  - ${node.name} (type: ${node.type})`)
    })
    
    console.log(`\nNodes with content: ${haveContent.length}`)
    console.log(`Nodes needing content: ${needContent.length}`)
    
    // Check for easiest math topics
    console.log('\nChecking for basic math topics:')
    const basicTopics = ['counting', 'addition', 'subtraction', 'multiplication', 'numbers']
    
    for (const topic of basicTopics) {
      const { data, error } = await supabase
        .from('skill_tree_nodes')
        .select('name, type, has_learning_content, is_menu_leaf')
        .ilike('name', `%${topic}%`)
        .limit(3)
      
      if (data && data.length > 0) {
        console.log(`\n${topic.toUpperCase()}:`)
        data.forEach(node => {
          console.log(`  - ${node.name} (has content: ${node.has_learning_content}, leaf: ${node.is_menu_leaf})`)
        })
      }
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

checkMathNodes()