const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkDependencies() {
  try {
    console.log('=== CHECKING DEPENDENCIES ON DIFFICULTY FIELD ===\n');
    
    // Check the spelling_words_with_sources view
    console.log('1. Checking spelling_words_with_sources view...');
    const { data: viewData, error: viewError } = await supabase
      .from('spelling_words_with_sources')
      .select('*')
      .limit(1);
    
    if (!viewError && viewData && viewData.length > 0) {
      console.log('\nFields in spelling_words_with_sources view:');
      Object.keys(viewData[0]).forEach(field => {
        if (field === 'difficulty' || field.includes('difficulty')) {
          console.log(`  - ${field}: ${viewData[0][field]}`);
        }
      });
    } else if (viewError) {
      console.log('Error accessing view:', viewError.message);
    }
    
    // Try to get view definition using SQL
    console.log('\n2. Attempting to get view definition...');
    const viewDefSQL = `
      SELECT 
        viewname,
        definition 
      FROM pg_views 
      WHERE schemaname = 'public' 
      AND viewname = 'spelling_words_with_sources';
    `;
    
    console.log('SQL to check view definition:');
    console.log(viewDefSQL);
    
    // Check for other dependent views
    console.log('\n3. Checking for all views that might depend on spelling_words...');
    const dependentViewsSQL = `
      SELECT DISTINCT
        v.viewname,
        v.schemaname
      FROM pg_views v
      WHERE v.definition LIKE '%spelling_words%'
      AND v.schemaname = 'public';
    `;
    
    console.log('SQL to find dependent views:');
    console.log(dependentViewsSQL);
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkDependencies();