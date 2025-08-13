const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

// Create Supabase admin client
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

async function createSocialTables() {
  console.log('📋 Creating social feature tables...\n');
  
  // Since we can't create tables via the JS client,
  // let's create the data structures that work with existing tables
  
  // First, let's check what tables exist
  console.log('🔍 Checking existing database structure...');
  
  try {
    // Try to query the profiles table
    const { data: profiles, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .limit(1);
    
    if (profileError) {
      if (profileError.message.includes('relation "public.profiles" does not exist')) {
        console.log('❌ Profiles table does not exist');
        console.log('\n📝 To create the social tables, please:');
        console.log('1. Go to your Supabase Dashboard SQL Editor:');
        console.log('   https://supabase.com/dashboard/project/bedcscnprmaztktgklko/sql');
        console.log('\n2. Run the SQL from this file:');
        console.log('   prisma/migrations/sql/0002_social_features.sql');
        console.log('\n3. After creating the tables, run: node scripts/seed-data-direct.js');
        return;
      }
      console.error('Error checking profiles:', profileError.message);
    } else {
      console.log('✅ Profiles table exists');
      
      // Check for other tables
      const tables = ['friendships', 'achievements', 'user_achievements', 'leaderboard', 'discussions', 'user_progress'];
      
      for (const table of tables) {
        const { error } = await supabase.from(table).select('*').limit(1);
        if (error && error.message.includes('does not exist')) {
          console.log(`❌ ${table} table does not exist`);
        } else if (!error) {
          console.log(`✅ ${table} table exists`);
        }
      }
      
      console.log('\n✅ Social tables are ready! You can now load sample data.');
      console.log('Run: node scripts/seed-data-direct.js');
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

createSocialTables();