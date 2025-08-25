const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY // Use service role for admin operations
);

async function fixWordErrorDefinitions() {
  console.log('Starting to fix "word error" definitions...\n');
  
  // First, create a backup of affected records
  console.log('Creating backup of affected records...');
  
  // Get all words with "word error" in definition
  const { data: errorWords, error: fetchError } = await supabase
    .from('spelling_words')
    .select('*')
    .ilike('definition', '%word error%')
    .order('word');
    
  if (fetchError) {
    console.error('Error fetching words:', fetchError);
    return;
  }
  
  console.log(`Found ${errorWords.length} words with "word error" in definition\n`);
  
  // Save backup
  const backupPath = `spelling_words_word_error_backup_${Date.now()}.json`;
  fs.writeFileSync(backupPath, JSON.stringify(errorWords, null, 2));
  console.log(`Backup saved to: ${backupPath}\n`);
  
  // Process each word
  const fixedWords = [];
  const deletionCandidates = [];
  
  for (const word of errorWords) {
    console.log(`\nProcessing: ${word.word}`);
    console.log(`Current definition: ${word.definition.substring(0, 100)}...`);
    
    // These combined words should be deleted - they're not real words
    // The individual components should already exist separately
    const shouldDelete = true;
    
    if (shouldDelete) {
      deletionCandidates.push({
        id: word.id,
        word: word.word,
        reason: 'Combined word error from PDF parsing'
      });
      console.log(`  ➡️ Marked for deletion (combined word error)`);
    }
  }
  
  // Show summary before making changes
  console.log('\n========== SUMMARY ==========');
  console.log(`Words to delete: ${deletionCandidates.length}`);
  
  if (deletionCandidates.length > 0) {
    console.log('\nWords marked for deletion (first 20):');
    deletionCandidates.slice(0, 20).forEach(item => {
      console.log(`  - ${item.word}`);
    });
    if (deletionCandidates.length > 20) {
      console.log(`  ... and ${deletionCandidates.length - 20} more`);
    }
  }
  
  // Save deletion plan
  const planPath = 'word_error_deletion_plan.json';
  fs.writeFileSync(planPath, JSON.stringify({
    generatedAt: new Date().toISOString(),
    totalToDelete: deletionCandidates.length,
    deletions: deletionCandidates
  }, null, 2));
  console.log(`\nDeletion plan saved to: ${planPath}`);
  
  // Ask for confirmation
  console.log('\n⚠️  IMPORTANT: Review the deletion plan before proceeding.');
  console.log('These words appear to be parsing errors where two words were incorrectly combined.');
  console.log('The individual component words should already exist in the database.');
  
  // Create SQL for deletion
  const deletionIds = deletionCandidates.map(d => d.id);
  const sqlPath = 'delete_word_errors.sql';
  
  const sql = `-- Delete combined word errors from spelling_words table
-- Generated: ${new Date().toISOString()}
-- Total words to delete: ${deletionCandidates.length}

-- Create backup first
CREATE TABLE IF NOT EXISTS spelling_words_bkp_word_errors AS 
SELECT * FROM spelling_words 
WHERE id IN (
  ${deletionIds.map(id => `'${id}'`).join(',\n  ')}
);

-- Delete the error words
DELETE FROM spelling_words 
WHERE id IN (
  ${deletionIds.map(id => `'${id}'`).join(',\n  ')}
);

-- Verify deletion
SELECT COUNT(*) as remaining_errors 
FROM spelling_words 
WHERE definition ILIKE '%word error%';
`;
  
  fs.writeFileSync(sqlPath, sql);
  console.log(`\nSQL script saved to: ${sqlPath}`);
  console.log('You can review and run this script in your database when ready.');
  
  // Check if component words exist
  console.log('\n========== COMPONENT WORD CHECK ==========');
  console.log('Checking if individual component words exist...\n');
  
  const componentCheck = [];
  for (const candidate of deletionCandidates.slice(0, 10)) { // Check first 10
    // Try to extract component words from the combined word
    // Most are in format like "wordonewordtwo"
    const word = candidate.word;
    
    // Common patterns we see in the data
    const patterns = [
      { regex: /^(\w+)(difficulty|ottoman|canopy|documentary|bittern|ethylene)$/i, position: 1 },
      { regex: /^(sepulchral|hostile|indolent|subrident|grudgingly|evaporation|grandeur)(\w+)$/i, position: 0 }
    ];
    
    for (const pattern of patterns) {
      const match = word.match(pattern.regex);
      if (match) {
        const component = match[pattern.position === 0 ? 1 : pattern.position];
        
        // Check if component exists
        const { data: exists } = await supabase
          .from('spelling_words')
          .select('word')
          .eq('word', component.toLowerCase())
          .single();
          
        if (exists) {
          console.log(`✅ "${word}" -> component "${component}" exists`);
        } else {
          console.log(`❌ "${word}" -> component "${component}" NOT found`);
        }
        componentCheck.push({ combined: word, component, exists: !!exists });
        break;
      }
    }
  }
  
  console.log('\n✅ Analysis complete!');
  console.log('Please review the files and SQL script before executing database changes.');
}

fixWordErrorDefinitions()
  .then(() => console.log('\nDone!'))
  .catch(console.error);