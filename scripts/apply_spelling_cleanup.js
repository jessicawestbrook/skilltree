const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function applySpellingCleanup() {
  console.log('=== APPLYING SPELLING WORDS CLEANUP ===\n');
  
  // Load the cleanup plan
  const planFiles = fs.readdirSync('scripts').filter(f => f.startsWith('spelling_cleanup_plan_'));
  if (planFiles.length === 0) {
    console.error('❌ No cleanup plan found. Run cleanup_invalid_spelling_words.js first.');
    return;
  }
  
  // Use the most recent plan
  const latestPlan = planFiles.sort().pop();
  const planPath = `scripts/${latestPlan}`;
  console.log(`📋 Loading plan from: ${planPath}`);
  
  const cleanupPlan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
  
  console.log('\n📊 PLAN SUMMARY:');
  console.log(`  - Words to delete (concatenated): ${cleanupPlan.concatenatedWords.toDelete.length}`);
  console.log(`  - Words to delete (invalid): ${cleanupPlan.invalidWords.toDelete.length}`);
  console.log(`  - New words to add: ${cleanupPlan.concatenatedWords.newWordsToAdd.length}`);
  console.log(`  - Valid words needing definitions: ${cleanupPlan.validWordsNeedingDefinitions.length}`);
  console.log(`  - Total changes: ${cleanupPlan.summary.totalChanges}`);
  
  const results = {
    timestamp: new Date().toISOString(),
    planFile: latestPlan,
    deletedConcatenated: [],
    deletedInvalid: [],
    addedWords: [],
    errors: []
  };
  
  try {
    // Step 1: Delete concatenated words
    if (cleanupPlan.concatenatedWords.toDelete.length > 0) {
      console.log('\n🗑️ Deleting concatenated words...');
      const allToDelete = [...cleanupPlan.concatenatedWords.toDelete, ...cleanupPlan.invalidWords.toDelete];
      
      // Remove duplicates (universalv appears in both lists)
      const uniqueToDelete = [...new Set(allToDelete)];
      
      const { data: deleted, error: deleteError } = await supabase
        .from('spelling_words')
        .delete()
        .in('word', uniqueToDelete)
        .select('word');
      
      if (deleteError) {
        console.error('❌ Error deleting words:', deleteError);
        results.errors.push({ step: 'delete', error: deleteError.message });
      } else {
        console.log(`✅ Deleted ${deleted?.length || 0} words`);
        results.deletedConcatenated = deleted?.map(d => d.word) || [];
      }
    }
    
    // Step 2: Add new words from splits
    if (cleanupPlan.concatenatedWords.newWordsToAdd.length > 0) {
      console.log('\n➕ Adding new words from splits...');
      
      // Prepare words with basic structure
      const wordsToInsert = cleanupPlan.concatenatedWords.newWordsToAdd.map(w => ({
        word: w.word,
        source_difficulty: w.source_difficulty,
        definition: null,
        example_sentence: null,
        pronunciation_guide: null,
        etymology: null
      }));
      
      const { data: inserted, error: insertError } = await supabase
        .from('spelling_words')
        .insert(wordsToInsert)
        .select('word');
      
      if (insertError) {
        console.error('❌ Error inserting words:', insertError);
        results.errors.push({ step: 'insert', error: insertError.message });
      } else {
        console.log(`✅ Added ${inserted?.length || 0} new words`);
        results.addedWords = inserted?.map(i => i.word) || [];
      }
    }
    
    // Step 3: Verify cleanup
    console.log('\n🔍 Verifying cleanup...');
    
    // Check if deleted words are really gone
    const { data: stillExists } = await supabase
      .from('spelling_words')
      .select('word')
      .in('word', cleanupPlan.concatenatedWords.toDelete.slice(0, 5));
    
    if (stillExists && stillExists.length > 0) {
      console.log('⚠️ Some words were not deleted:', stillExists.map(w => w.word));
      results.errors.push({ step: 'verify', error: 'Some words were not deleted' });
    } else {
      console.log('✅ Concatenated words successfully removed');
    }
    
    // Check if new words were added
    const { data: newWordsExist } = await supabase
      .from('spelling_words')
      .select('word, definition')
      .in('word', cleanupPlan.concatenatedWords.newWordsToAdd.slice(0, 5).map(w => w.word));
    
    if (newWordsExist) {
      console.log(`✅ Found ${newWordsExist.length} of the new words in database`);
      const withoutDef = newWordsExist.filter(w => !w.definition);
      if (withoutDef.length > 0) {
        console.log(`📝 ${withoutDef.length} new words need definitions`);
      }
    }
    
    // Count total words without definitions
    const { count: noDefCount } = await supabase
      .from('spelling_words')
      .select('word', { count: 'exact', head: true })
      .is('definition', null);
    
    console.log(`\n📊 Current status: ${noDefCount} words without definitions`);
    
    // Save results
    const resultsFile = `scripts/spelling_cleanup_results_${Date.now()}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ CLEANUP COMPLETE!');
    console.log('='.repeat(60));
    console.log(`Deleted: ${results.deletedConcatenated.length + results.deletedInvalid.length} words`);
    console.log(`Added: ${results.addedWords.length} words`);
    console.log(`Words still needing definitions: ${noDefCount}`);
    console.log(`\nResults saved to: ${resultsFile}`);
    
    if (results.addedWords.length > 0 || cleanupPlan.validWordsNeedingDefinitions.length > 0) {
      console.log('\n📝 Next step: Run populate_legitimate_words_claude_improved.js to add definitions');
    }
    
  } catch (error) {
    console.error('Error during cleanup:', error);
    results.errors.push({ step: 'general', error: error.message });
  }
}

applySpellingCleanup().catch(console.error);