const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function dropUnusedColumns() {
  console.log('Dropping unused columns from skill_tree_nodes table\n')
  console.log('=' .repeat(50))
  
  try {
    // Step 1: Check current columns
    console.log('\n1. Current table structure:')
    const { data: currentSample, error: checkError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .limit(1)
    
    if (checkError) {
      console.error('Error checking table:', checkError)
      return
    }
    
    if (currentSample && currentSample.length > 0) {
      const columns = Object.keys(currentSample[0])
      console.log('Current columns:', columns)
      
      const columnsToRemove = ['type', 'path', 'learning_area']
      const existingToRemove = columnsToRemove.filter(col => columns.includes(col))
      
      if (existingToRemove.length === 0) {
        console.log('\n✅ Columns already removed or don\'t exist')
        return
      }
      
      console.log('\nColumns to remove:', existingToRemove)
      
      // Step 2: Provide SQL to run
      console.log('\n2. SQL to execute in Supabase:')
      console.log('=' .repeat(50))
      console.log(`
ALTER TABLE skill_tree_nodes 
DROP COLUMN IF EXISTS type,
DROP COLUMN IF EXISTS path,
DROP COLUMN IF EXISTS learning_area;
`)
      console.log('=' .repeat(50))
      
      console.log('\n📝 Instructions:')
      console.log('1. Go to: https://supabase.com/dashboard/project/ozujqlucqdyszxmzhigf/sql/new')
      console.log('2. Copy and paste the SQL above')
      console.log('3. Click "Run" button')
      console.log('4. Verify columns are removed in Table Editor')
      
      // Step 3: Show sample data that uses these columns
      if (existingToRemove.includes('learning_area')) {
        console.log('\n3. Sample data in learning_area column:')
        const { data: areaData } = await supabase
          .from('skill_tree_nodes')
          .select('name, learning_area')
          .not('learning_area', 'is', null)
          .limit(5)
        
        if (areaData && areaData.length > 0) {
          areaData.forEach(node => {
            console.log(`  - ${node.name}: ${node.learning_area}`)
          })
          
          const { count } = await supabase
            .from('skill_tree_nodes')
            .select('*', { count: 'exact', head: true })
            .not('learning_area', 'is', null)
          
          console.log(`  Total nodes with learning_area: ${count}`)
          console.log('  Note: This data will be lost when column is dropped')
        }
      }
      
      if (existingToRemove.includes('type')) {
        console.log('\n4. Sample data in type column:')
        const { data: typeData } = await supabase
          .from('skill_tree_nodes')
          .select('name, type')
          .not('type', 'is', null)
          .limit(5)
        
        if (typeData && typeData.length > 0) {
          typeData.forEach(node => {
            console.log(`  - ${node.name}: ${node.type}`)
          })
        }
      }
      
      if (existingToRemove.includes('path')) {
        console.log('\n5. Sample data in path column:')
        const { data: pathData } = await supabase
          .from('skill_tree_nodes')
          .select('name, path')
          .not('path', 'is', null)
          .limit(5)
        
        if (pathData && pathData.length > 0) {
          pathData.forEach(node => {
            console.log(`  - ${node.name}: ${node.path}`)
          })
        }
      }
      
    } else {
      console.log('No data found in table')
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

dropUnusedColumns()