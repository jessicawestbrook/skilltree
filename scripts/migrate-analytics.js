// Load environment variables
require('dotenv').config({ path: '.env.local' });

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Initialize Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function runMigration() {
  try {
    console.log('Starting analytics schema migration...');
    
    // Read the SQL file
    const sqlPath = path.join(__dirname, '08-analytics-schema.sql');
    const sqlContent = fs.readFileSync(sqlPath, 'utf8');
    
    console.log('\n===========================================');
    console.log('IMPORTANT: Manual steps required!');
    console.log('===========================================');
    console.log('The analytics schema needs to be executed manually in Supabase:');
    console.log('1. Go to your Supabase Dashboard');
    console.log('2. Navigate to SQL Editor');
    console.log('3. Copy and paste the contents of scripts/08-analytics-schema.sql');
    console.log('4. Execute the SQL');
    console.log('===========================================\n');
    
    // Test basic connectivity
    console.log('Testing database connectivity...');
    const { data, error } = await supabase
      .from('user_progress')
      .select('*')
      .limit(1);
    
    if (error) {
      console.error('Error connecting to database:', error.message);
    } else {
      console.log('✓ Database connection successful');
    }
    
    console.log('\nMigration script completed.');
    console.log('Please execute the analytics schema manually in Supabase Dashboard.');
    console.log('\nAfter running the schema, the following features will be available:');
    console.log('  - Learning session tracking');
    console.log('  - Detailed analytics events');
    console.log('  - Personalized insights');
    console.log('  - Learning recommendations');
    console.log('  - Weekly progress summaries');
    
  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}

runMigration();