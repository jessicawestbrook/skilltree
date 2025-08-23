import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '..', '.env.local') });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceRoleKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);

async function checkDependentViews() {
  console.log('=== CHECKING FOR VIEWS DEPENDENT ON DIFFICULTY NAME COLUMNS ===\n');
  
  // Try to find views that might depend on these columns
  const viewsToCheck = [
    'spelling_words_with_sources',
    'spelling_words_view',
    'vocabulary_words_view',
    'spelling_words_with_difficulty',
    'vocabulary_words_with_difficulty'
  ];
  
  console.log('Checking for views that might use spelling_difficulty_name or vocabulary_difficulty_name...\n');
  
  for (const viewName of viewsToCheck) {
    try {
      // Try to query the view
      const { data, error } = await supabase
        .from(viewName)
        .select('*')
        .limit(1);
      
      if (!error) {
        console.log(`✓ Found view: ${viewName}`);
        
        // Check if the view has the columns we want to drop
        if (data && data.length > 0) {
          const columns = Object.keys(data[0]);
          const hasSpellingDifficultyName = columns.includes('spelling_difficulty_name');
          const hasVocabularyDifficultyName = columns.includes('vocabulary_difficulty_name');
          
          if (hasSpellingDifficultyName || hasVocabularyDifficultyName) {
            console.log(`  ⚠️  This view uses:`);
            if (hasSpellingDifficultyName) console.log(`    - spelling_difficulty_name`);
            if (hasVocabularyDifficultyName) console.log(`    - vocabulary_difficulty_name`);
            console.log(`  📝 This view needs to be updated!\n`);
          } else {
            console.log(`  ✅ This view does not use the columns to be dropped\n`);
          }
        }
      }
    } catch (e) {
      // View doesn't exist, continue
    }
  }
  
  // Also check if there's a generic way to find all views
  console.log('\n--- Attempting to list all views in the database ---');
  
  try {
    // This query gets all views from the information schema
    const { data: allViews, error } = await supabase.rpc('get_all_views');
    
    if (!error && allViews) {
      console.log('Found views:', allViews);
    } else {
      console.log('Could not retrieve view list (RPC function may not exist)');
    }
  } catch (e) {
    console.log('Could not retrieve view list');
  }
  
  console.log('\n--- RECOMMENDATION ---');
  console.log('Before dropping the columns, update any views that depend on them.');
  console.log('The most likely candidate is "spelling_words_with_sources" view.');
}

checkDependentViews().catch(console.error);