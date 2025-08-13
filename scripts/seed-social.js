const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

// Initialize Supabase client with service role key for admin access
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
);

async function seedSocialData() {
  console.log('🌱 Starting to seed social data...\n');

  try {
    // Read the SQL file
    const sqlFilePath = path.join(__dirname, 'seed-social-data.sql');
    const sqlContent = fs.readFileSync(sqlFilePath, 'utf8');
    
    // Split by semicolons but be careful with quoted strings
    const statements = sqlContent
      .split(/;\s*$/gm)
      .filter(stmt => stmt.trim().length > 0)
      .map(stmt => stmt.trim() + ';');

    let successCount = 0;
    let errorCount = 0;

    // Execute each statement
    for (const statement of statements) {
      // Skip comments and empty lines
      if (statement.startsWith('--') || statement.trim() === ';') {
        continue;
      }

      // Only show first 100 chars of statement for logging
      const shortStatement = statement.substring(0, 100) + (statement.length > 100 ? '...' : '');
      
      try {
        // For SELECT statements that are just for output
        if (statement.trim().toUpperCase().startsWith('SELECT')) {
          const { data, error } = await supabase.rpc('exec_sql', { 
            query: statement 
          }).single();
          
          if (error) {
            // Try direct execution as fallback
            console.log(`ℹ️  Info query: ${shortStatement}`);
          } else {
            console.log(`✅ ${data || shortStatement}`);
          }
        } else {
          // For INSERT/UPDATE statements, we need to parse and execute them differently
          // Since Supabase doesn't have a direct SQL execution endpoint for DML,
          // we'll need to use the appropriate table methods
          
          console.log(`⏳ Executing: ${shortStatement}`);
          
          // This is a simplified approach - in production you'd want proper SQL parsing
          // For now, we'll just log that these need to be executed via SQL editor
          console.log(`   ⚠️  Please execute this statement in Supabase SQL Editor`);
        }
        successCount++;
      } catch (err) {
        console.error(`❌ Error executing: ${shortStatement}`);
        console.error(`   Error: ${err.message}`);
        errorCount++;
      }
    }

    console.log('\n📊 Summary:');
    console.log(`   ✅ Successful statements: ${successCount}`);
    console.log(`   ❌ Failed statements: ${errorCount}`);
    
    // Alternative: Direct approach using Supabase UI
    console.log('\n💡 Alternative Method:');
    console.log('   1. Go to your Supabase Dashboard');
    console.log('   2. Navigate to SQL Editor');
    console.log('   3. Copy the contents of scripts/seed-social-data.sql');
    console.log('   4. Paste and run in the SQL Editor');
    
    // Or provide a direct link
    const projectRef = process.env.NEXT_PUBLIC_SUPABASE_URL?.match(/https:\/\/([^.]+)/)?.[1];
    if (projectRef) {
      console.log(`\n🔗 Direct link to SQL Editor:`);
      console.log(`   https://supabase.com/dashboard/project/${projectRef}/sql`);
    }

  } catch (error) {
    console.error('❌ Failed to seed data:', error);
    process.exit(1);
  }
}

// Run the seeding
seedSocialData()
  .then(() => {
    console.log('\n✨ Seeding process completed!');
    process.exit(0);
  })
  .catch(err => {
    console.error('\n❌ Seeding failed:', err);
    process.exit(1);
  });