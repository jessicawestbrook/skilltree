require('dotenv').config({ path: '.env.local' });

const hasServiceKey = !!(process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY);
console.log('Service role key exists:', hasServiceKey);

if (!hasServiceKey) {
  console.log('\nYou need to add the service role key to .env.local');
  console.log('Add one of these variables:');
  console.log('  SUPABASE_SERVICE_ROLE_KEY=your-service-role-key');
  console.log('  or');
  console.log('  REACT_APP_SUPABASE_SERVICE_ROLE_KEY=your-service-role-key');
  console.log('\nYou can find the service role key in your Supabase project settings under API.');
}