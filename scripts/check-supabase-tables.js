const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase credentials in environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

const requiredTables = [
  'activity_feed',
  'age_groups',
  'bookmarks',
  'comment_reports',
  'comment_votes',
  'course_content',
  'course_resources',
  'course_sections',
  'friend_requests',
  'friends',
  'key_concepts',
  'knowledge_nodes',
  'learning_path_nodes',
  'learning_paths',
  'learning_preferences',
  'learning_recommendations',
  'learning_sessions',
  'learning_tips',
  'node_comments',
  'profiles',
  'push_subscriptions',
  'quiz_questions',
  'study_group_members',
  'study_groups',
  'user_achievements',
  'user_notification_preferences',
  'user_profiles',
  'user_progress',
  'user_stats'
];

async function checkTables() {
  console.log('Checking Supabase tables...\n');
  
  const existingTables = [];
  const missingTables = [];
  
  for (const table of requiredTables) {
    try {
      // Try to query the table (limit 1 to be efficient)
      const { data, error } = await supabase
        .from(table)
        .select('*')
        .limit(1);
      
      if (error) {
        if (error.message.includes('relation') && error.message.includes('does not exist')) {
          missingTables.push(table);
          console.log(`❌ ${table} - MISSING`);
        } else {
          console.log(`⚠️  ${table} - EXISTS but has error: ${error.message}`);
          existingTables.push(table);
        }
      } else {
        existingTables.push(table);
        console.log(`✅ ${table} - EXISTS`);
      }
    } catch (err) {
      console.log(`❌ ${table} - Error checking: ${err.message}`);
      missingTables.push(table);
    }
  }
  
  console.log('\n=== SUMMARY ===');
  console.log(`Total tables required: ${requiredTables.length}`);
  console.log(`Tables found: ${existingTables.length}`);
  console.log(`Tables missing: ${missingTables.length}`);
  
  if (missingTables.length > 0) {
    console.log('\n=== MISSING TABLES ===');
    missingTables.forEach(table => console.log(`  - ${table}`));
    
    console.log('\n=== NEXT STEPS ===');
    console.log('1. Go to your Supabase dashboard');
    console.log('2. Navigate to the SQL Editor');
    console.log('3. Create the missing tables using the migration scripts in the /scripts folder');
    console.log('4. Or run: npm run migrate:all');
  } else {
    console.log('\n✅ All required tables exist!');
  }
}

checkTables().catch(console.error);