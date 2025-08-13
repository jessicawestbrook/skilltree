const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase credentials. Check your .env.local file.');
  process.exit(1);
}

// Since we can't execute raw SQL through Supabase client, 
// let's open the Supabase dashboard SQL editor
console.log('====================================');
console.log('📋 LOADING SAMPLE SOCIAL DATA');
console.log('====================================\n');

console.log('Since direct SQL execution requires database access,');
console.log('please follow these steps:\n');

console.log('1. Open your Supabase SQL Editor:');
console.log(`   https://supabase.com/dashboard/project/bedcscnprmaztktgklko/sql\n`);

console.log('2. Copy the SQL from this file:');
console.log(`   ${path.resolve(__dirname, 'seed-social-data.sql')}\n`);

console.log('3. Paste and run it in the SQL Editor\n');

console.log('The script will add:');
console.log('  ✅ 5 test users (Alice, Bob, Charlie, Diana, Eve)');
console.log('  ✅ User profiles with avatars and bios');
console.log('  ✅ Friend connections');
console.log('  ✅ Achievement unlocks');
console.log('  ✅ Leaderboard entries');
console.log('  ✅ Discussion posts and comments');
console.log('  ✅ Direct messages');
console.log('  ✅ Notifications');
console.log('  ✅ Quiz progress data\n');

console.log('====================================');
console.log('Opening the SQL in your default text editor...');

// Try to open the SQL file in the default editor
const { exec } = require('child_process');
const sqlFile = path.resolve(__dirname, 'seed-social-data.sql');

// Windows
if (process.platform === 'win32') {
  exec(`notepad "${sqlFile}"`, (err) => {
    if (err) {
      console.log('Could not open file automatically.');
      console.log(`Please open manually: ${sqlFile}`);
    }
  });
}

console.log('\n✨ Once you run the SQL, your social features will have sample data!');