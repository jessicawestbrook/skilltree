const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

async function testConnection() {
  console.log('Testing Supabase connection...\n');
  
  // Check environment variables
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  
  console.log('Environment Check:');
  console.log('✓ SUPABASE_URL:', supabaseUrl ? `${supabaseUrl.slice(0, 30)}...` : 'NOT SET');
  console.log('✓ ANON_KEY:', supabaseAnonKey ? `${supabaseAnonKey.slice(0, 20)}...` : 'NOT SET');
  console.log('✓ SERVICE_KEY:', supabaseServiceKey ? `${supabaseServiceKey.slice(0, 20)}...` : 'NOT SET');
  console.log();
  
  if (!supabaseUrl || !supabaseAnonKey) {
    console.error('❌ Missing required environment variables!');
    console.log('\nPlease ensure your .env.local file contains:');
    console.log('  NEXT_PUBLIC_SUPABASE_URL=your_supabase_url');
    console.log('  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key');
    console.log('  SUPABASE_SERVICE_ROLE_KEY=your_service_key');
    process.exit(1);
  }
  
  // Test with anon key (public access)
  console.log('Testing public connection (anon key)...');
  const supabaseAnon = createClient(supabaseUrl, supabaseAnonKey);
  
  try {
    // Try to fetch from a public table or auth users
    const { data, error } = await supabaseAnon.auth.getSession();
    
    if (error) {
      console.log('⚠️  Auth session check failed (expected for anon key):', error.message);
    } else {
      console.log('✓ Connected successfully with anon key');
    }
    
    // Try to query a table (this will fail if RLS is enabled and no user is logged in)
    const { data: tableData, error: tableError } = await supabaseAnon
      .from('knowledge_nodes')
      .select('count')
      .limit(1);
    
    if (tableError) {
      if (tableError.message.includes('relation') && tableError.message.includes('does not exist')) {
        console.log('⚠️  Table "knowledge_nodes" does not exist - you may need to run migrations');
      } else if (tableError.message.includes('permission denied')) {
        console.log('✓ RLS is enabled (good for security)');
      } else {
        console.log('⚠️  Query error:', tableError.message);
      }
    } else {
      console.log('✓ Successfully queried database');
    }
  } catch (err) {
    console.error('❌ Connection failed:', err.message);
  }
  
  // Test with service key if available
  if (supabaseServiceKey && supabaseServiceKey !== 'placeholder_service_role_key_for_build') {
    console.log('\nTesting admin connection (service key)...');
    const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey);
    
    try {
      const { data, error } = await supabaseAdmin
        .from('knowledge_nodes')
        .select('count')
        .limit(1);
      
      if (error) {
        if (error.message.includes('relation') && error.message.includes('does not exist')) {
          console.log('⚠️  Table "knowledge_nodes" does not exist');
          console.log('\n📝 Next Steps:');
          console.log('1. Go to your Supabase dashboard: ' + supabaseUrl);
          console.log('2. Navigate to SQL Editor');
          console.log('3. Run the migration scripts in order:');
          console.log('   - 00-prepare-for-migration.sql');
          console.log('   - 01-create-core-tables.sql');
          console.log('   - 02-create-dependent-tables.sql');
          console.log('   - 03-create-user-tables.sql');
          console.log('   - 04-create-views-and-functions.sql');
          console.log('   - 10-social-features.sql');
          console.log('4. Then run: npm run migrate:all');
        } else {
          console.log('❌ Admin query error:', error.message);
        }
      } else {
        console.log('✓ Admin connection successful!');
        console.log('✓ Database is properly configured');
      }
    } catch (err) {
      console.error('❌ Admin connection failed:', err.message);
    }
  } else {
    console.log('\n⚠️  Service role key not configured or using placeholder');
    console.log('To get your service role key:');
    console.log('1. Go to your Supabase dashboard');
    console.log('2. Navigate to Settings > API');
    console.log('3. Copy the "service_role" secret key');
    console.log('4. Update SUPABASE_SERVICE_ROLE_KEY in .env.local');
  }
  
  console.log('\n📋 Summary:');
  console.log('- Supabase URL: Configured ✓');
  console.log('- Anon Key: Configured ✓');
  console.log('- Service Key:', supabaseServiceKey && supabaseServiceKey !== 'placeholder_service_role_key_for_build' ? 'Configured ✓' : 'Needs configuration ⚠️');
  console.log('\nFor more help, visit: https://supabase.com/docs');
}

testConnection().catch(console.error);