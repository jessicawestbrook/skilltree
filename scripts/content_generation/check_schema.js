/**
 * Script to check the actual schema of skill_tree_nodes table
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

async function checkSchema() {
  console.log('Checking skill_tree_nodes table schema...\n')
  
  try {
    // Get a single row to see the structure
    const { data, error } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .limit(1)
    
    if (error) {
      console.error('Error fetching data:', error)
      return
    }
    
    if (data && data.length > 0) {
      console.log('Table columns:')
      Object.keys(data[0]).forEach(key => {
        const value = data[0][key]
        const type = value === null ? 'null' : typeof value
        console.log(`  - ${key}: ${type}`)
      })
      
      console.log('\nExample row:')
      console.log(JSON.stringify(data[0], null, 2))
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

checkSchema()