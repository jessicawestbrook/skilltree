const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Words to be deleted (not valid words or combined words)
const wordsToDelete = [
  { id: '6817d6b8-2730-475c-8921-a17430f8d33a', word: 'aaccdi', reason: 'Random letters, not a valid word' },
  { id: 'f8c38699-3ed5-4119-a559-974cbd1cdd86', word: 'dlailmnr', reason: 'Random letters, not a valid word' },
  { id: '18aefd86-92c5-4037-a544-0547fd5c9e32', word: 'centennialcertiorari', reason: 'Combined words (certiorari already exists separately)' }
];

// No words need fixing since certiorari already exists
const wordsToFix = [];

async function previewChanges() {
  console.log('='.repeat(60));
  console.log('PREVIEW OF CHANGES TO BE MADE');
  console.log('='.repeat(60));
  
  console.log('\n1. WORDS TO BE DELETED:');
  console.log('-'.repeat(40));
  for (const item of wordsToDelete) {
    console.log(`   Word: ${item.word}`);
    console.log(`   ID: ${item.id}`);
    console.log(`   Reason: ${item.reason}`);
    console.log();
  }
  
  if (wordsToFix.length > 0) {
    console.log('\n2. WORDS TO BE FIXED:');
    console.log('-'.repeat(40));
    for (const item of wordsToFix) {
      console.log(`   Current: ${item.currentWord}`);
      console.log(`   Will become: ${item.newWord}`);
      console.log(`   Definition: ${item.definition}`);
      console.log(`   Reason: ${item.reason}`);
      console.log();
    }
  }
  
  console.log('='.repeat(60));
  console.log('To apply these changes, run: node scripts/cleanup_invalid_words.js --execute');
}

async function executeCleanup() {
  console.log('Starting cleanup...\n');
  
  // First create backup
  console.log('Creating backup of affected records...');
  const affectedIds = [
    ...wordsToDelete.map(w => w.id),
    ...wordsToFix.map(w => w.id)
  ];
  
  const { data: backupData, error: backupError } = await supabase
    .from('spelling_words')
    .select('*')
    .in('id', affectedIds);
    
  if (backupError) {
    console.error('Error creating backup:', backupError);
    return;
  }
  
  // Save backup to file
  const fs = require('fs');
  const backupFile = `scripts/spelling_words_backup_${Date.now()}.json`;
  fs.writeFileSync(backupFile, JSON.stringify(backupData, null, 2));
  console.log(`Backup saved to ${backupFile}`);
  
  // Delete invalid words
  console.log('\nDeleting invalid words...');
  for (const item of wordsToDelete) {
    const { data, error } = await supabase
      .from('spelling_words')
      .delete()
      .eq('id', item.id)
      .select();
      
    if (error) {
      console.error(`Error deleting ${item.word}:`, error);
      console.error('Error details:', error.message, error.details, error.hint);
    } else if (data && data.length === 0) {
      console.log(`⚠ No rows deleted for: ${item.word} (may not exist or RLS policy blocking)`);
    } else {
      console.log(`✓ Deleted: ${item.word}`);
    }
  }
  
  // Fix combined words
  console.log('\nFixing combined words...');
  for (const item of wordsToFix) {
    const { error } = await supabase
      .from('spelling_words')
      .update({
        word: item.newWord,
        definition: item.definition,
        updated_at: new Date().toISOString()
      })
      .eq('id', item.id);
      
    if (error) {
      console.error(`Error fixing ${item.currentWord}:`, error);
    } else {
      console.log(`✓ Fixed: ${item.currentWord} → ${item.newWord}`);
    }
  }
  
  console.log('\nCleanup completed!');
  
  // Verify results
  console.log('\nVerifying cleanup...');
  
  // Check deleted words are gone
  const { data: checkDeleted } = await supabase
    .from('spelling_words')
    .select('id')
    .in('id', wordsToDelete.map(w => w.id));
    
  console.log(`Deleted words remaining: ${checkDeleted?.length || 0} (should be 0)`);
  
  // Check fixed words
  const { data: checkFixed } = await supabase
    .from('spelling_words')
    .select('word')
    .eq('id', wordsToFix[0].id)
    .single();
    
  if (checkFixed) {
    console.log(`Fixed word is now: ${checkFixed.word} (should be 'certiorari')`);
  }
}

// Main execution
const args = process.argv.slice(2);

if (args.includes('--execute')) {
  executeCleanup().catch(console.error);
} else {
  previewChanges().catch(console.error);
}