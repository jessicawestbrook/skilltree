const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function createHiddenNodesTable() {
  try {
    console.log('Creating hidden_nodes management table...\n')
    
    // Check if the table already exists
    const { data: existingTable, error: checkError } = await supabase
      .from('hidden_nodes')
      .select('*')
      .limit(1)
    
    if (!checkError) {
      console.log('✅ Table hidden_nodes already exists')
      
      // Get stats
      const { count } = await supabase
        .from('hidden_nodes')
        .select('*', { count: 'exact', head: true })
      
      console.log(`Current hidden nodes: ${count || 0}`)
      return
    }
    
    // Create the table using raw SQL via RPC
    const createTableSQL = `
      CREATE TABLE IF NOT EXISTS hidden_nodes (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        node_id UUID NOT NULL REFERENCES skill_tree_nodes(id) ON DELETE CASCADE,
        hidden_by UUID REFERENCES auth.users(id),
        hidden_at TIMESTAMPTZ DEFAULT NOW(),
        reason TEXT,
        UNIQUE(node_id)
      );
      
      CREATE INDEX idx_hidden_nodes_node_id ON hidden_nodes(node_id);
    `
    
    console.log('Attempting to create table via exec_sql...')
    const { error: createError } = await supabase.rpc('exec_sql', {
      sql: createTableSQL
    })
    
    if (createError) {
      console.log('❌ Could not create table via exec_sql')
      console.log('Error:', createError.message)
      
      // Provide manual instructions
      console.log('\nPlease create the table manually in Supabase:')
      console.log('1. Go to SQL Editor in Supabase Dashboard')
      console.log('2. Run this SQL:')
      console.log('```sql')
      console.log(createTableSQL)
      console.log('```')
      
      // For now, we'll create a simple workaround using existing tables
      console.log('\n📝 Creating workaround using user preferences...')
      
      // We can use the user_preferences table to store hidden nodes
      const { data: prefs, error: prefsError } = await supabase
        .from('user_preferences')
        .select('*')
        .eq('user_id', 'system')
        .eq('preference_key', 'hidden_nodes')
        .single()
      
      if (prefsError && prefsError.code === 'PGRST116') {
        // Create a system preference for hidden nodes
        const { error: insertError } = await supabase
          .from('user_preferences')
          .insert({
            user_id: 'system',
            preference_key: 'hidden_nodes',
            preference_value: JSON.stringify([])
          })
        
        if (insertError) {
          console.log('Could not create system preference:', insertError)
        } else {
          console.log('✅ Created system preference for hidden nodes')
        }
      } else if (prefs) {
        console.log('✅ System preference for hidden nodes already exists')
        const hiddenNodes = JSON.parse(prefs.preference_value || '[]')
        console.log(`Currently hidden nodes: ${hiddenNodes.length}`)
      }
    } else {
      console.log('✅ Table created successfully!')
    }
    
  } catch (error) {
    console.error('Error:', error)
  }
}

createHiddenNodesTable()