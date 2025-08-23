const { createClient } = require('@supabase/supabase-js')
require('dotenv').config({ path: '.env.local' })

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
)

async function setupHiddenNodes() {
  try {
    console.log('Setting up hidden nodes system...\n')
    
    // First check if we have a simple settings/config table we can use
    const tables = ['app_settings', 'system_config', 'user_preferences', 'settings']
    
    for (const tableName of tables) {
      const { data, error } = await supabase
        .from(tableName)
        .select('*')
        .limit(1)
      
      if (!error) {
        console.log(`✅ Found table: ${tableName}`)
        console.log('Sample data:', data)
        break
      }
    }
    
    // Let's create a simple JSON file to store hidden nodes for now
    // This will be replaced with a database solution later
    const fs = require('fs')
    const path = require('path')
    
    const hiddenNodesPath = path.join(__dirname, '..', 'src', 'config', 'hiddenNodes.json')
    const configDir = path.join(__dirname, '..', 'src', 'config')
    
    // Create config directory if it doesn't exist
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true })
      console.log('Created config directory')
    }
    
    // Create hidden nodes file if it doesn't exist
    if (!fs.existsSync(hiddenNodesPath)) {
      const initialConfig = {
        hiddenNodes: [],
        hiddenByDefault: [],
        lastUpdated: new Date().toISOString(),
        notes: "This file stores node IDs that should be hidden from users. Add node IDs to the hiddenNodes array."
      }
      
      fs.writeFileSync(hiddenNodesPath, JSON.stringify(initialConfig, null, 2))
      console.log('✅ Created hidden nodes configuration file')
    } else {
      console.log('✅ Hidden nodes configuration already exists')
      const config = JSON.parse(fs.readFileSync(hiddenNodesPath, 'utf8'))
      console.log(`Currently hidden nodes: ${config.hiddenNodes.length}`)
    }
    
    console.log('\nSetup complete!')
    console.log('Hidden nodes will be managed via: src/config/hiddenNodes.json')
    
  } catch (error) {
    console.error('Error:', error)
  }
}

setupHiddenNodes()