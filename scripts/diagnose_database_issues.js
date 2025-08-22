/**
 * Comprehensive database diagnostic script
 * Checks table existence, permissions, and RLS policies
 */

// Load environment variables
require('dotenv').config({ path: '.env.local' })

const { createClient } = require('@supabase/supabase-js')

// Initialize Supabase client
const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
)

async function testTableAccess(tableName) {
  try {
    console.log(`Testing ${tableName}...`)
    
    // Try to select with limit 0 to test access without getting data
    const { data, error } = await supabase
      .from(tableName)
      .select('*')
      .limit(0)

    if (error) {
      console.log(`❌ ${tableName}: ${error.message} (Code: ${error.code})`)
      return false
    } else {
      console.log(`✅ ${tableName}: Accessible`)
      return true
    }
  } catch (err) {
    console.log(`❌ ${tableName}: ${err.message}`)
    return false
  }
}

async function testStarredItemsSpecifically() {
  console.log('\n=== Testing starred_items table specifically ===')
  
  try {
    // Test basic access
    const { data, error } = await supabase
      .from('starred_items')
      .select('id')
      .limit(1)

    console.log('Basic select result:', { data, error })

    // Test with specific filters (like the failing query)
    const { data: data2, error: error2 } = await supabase
      .from('starred_items')
      .select('id')
      .eq('user_id', '5876bd4e-5e68-4b4d-be15-8f0171bfae93')
      .eq('item_type', 'skill_node')
      .eq('item_id', 'test-id')

    console.log('Filtered select result:', { data: data2, error: error2 })

  } catch (err) {
    console.log('starred_items test error:', err)
  }
}

async function checkAuthStatus() {
  console.log('\n=== Checking Authentication ===')
  
  try {
    const { data: { user }, error } = await supabase.auth.getUser()
    
    if (error) {
      console.log('❌ Auth error:', error.message)
    } else if (user) {
      console.log('✅ User authenticated:', user.id)
    } else {
      console.log('⚠️  No user authenticated')
    }
  } catch (err) {
    console.log('❌ Auth check failed:', err.message)
  }
}

async function main() {
  console.log('=== Database Diagnostic Script ===\n')

  // Check authentication first
  await checkAuthStatus()

  console.log('\n=== Testing Table Access ===')
  
  const tables = [
    'skill_tree_nodes',
    'starred_items', 
    'notifications',
    'notification_preferences',
    'user_progress',
    'study_lists',
    'questions',
    'learning_content'
  ]

  const results = {}
  
  for (const table of tables) {
    results[table] = await testTableAccess(table)
    await new Promise(resolve => setTimeout(resolve, 100)) // Small delay
  }

  // Specific test for starred_items
  await testStarredItemsSpecifically()

  console.log('\n=== Summary ===')
  const accessible = Object.values(results).filter(Boolean).length
  const total = Object.keys(results).length
  
  console.log(`Accessible tables: ${accessible}/${total}`)
  
  console.log('\nTable Status:')
  Object.entries(results).forEach(([table, accessible]) => {
    console.log(`  ${accessible ? '✅' : '❌'} ${table}`)
  })

  if (results.starred_items === false) {
    console.log('\n=== starred_items Table Issue ===')
    console.log('The starred_items table is not accessible.')
    console.log('Possible causes:')
    console.log('1. Table does not exist')
    console.log('2. RLS policies are blocking access')
    console.log('3. User is not authenticated')
    console.log('4. Column names or structure mismatch')
    console.log('\nNext steps:')
    console.log('1. Run the fix_starred_items_table.sql script in Supabase')
    console.log('2. Ensure user is properly authenticated')
    console.log('3. Check RLS policies in Supabase dashboard')
  }
}

if (require.main === module) {
  main().catch(console.error)
}

module.exports = { main, testTableAccess }