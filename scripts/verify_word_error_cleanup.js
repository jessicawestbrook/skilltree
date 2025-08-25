const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyWordErrorCleanup() {
  console.log('Verifying word error cleanup...\n');
  
  // 1. Check if any "word error" definitions remain
  console.log('1. Checking for remaining "word error" definitions:');
  const { data: remainingErrors, error: errorCheck } = await supabase
    .from('spelling_words')
    .select('id, word, definition')
    .ilike('definition', '%word error%');
    
  if (errorCheck) {
    console.error('Error checking:', errorCheck);
  } else {
    console.log(`   Found ${remainingErrors?.length || 0} remaining "word error" definitions`);
    if (remainingErrors && remainingErrors.length > 0) {
      console.log('   ⚠️ These still need to be addressed:');
      remainingErrors.forEach(w => console.log(`      - ${w.word}`));
    } else {
      console.log('   ✅ All "word error" definitions have been removed!');
    }
  }
  
  // 2. Check if backup table was created
  console.log('\n2. Checking for backup table:');
  const { data: backupCheck } = await supabase
    .from('spelling_words_bkp_word_errors')
    .select('count', { count: 'exact', head: true });
    
  if (backupCheck !== null) {
    console.log('   ✅ Backup table exists: spelling_words_bkp_word_errors');
  } else {
    console.log('   ℹ️ Backup table may not exist or may not be accessible');
  }
  
  // 3. Verify some component words still exist
  console.log('\n3. Verifying component words still exist:');
  const componentWords = [
    'sepulchral', 'sangfroid', 'hostile', 'howler', 
    'indolent', 'documentary', 'grandeur', 'ottoman',
    'evaporation', 'bittern', 'grudgingly', 'canopy'
  ];
  
  const { data: existingComponents } = await supabase
    .from('spelling_words')
    .select('word')
    .in('word', componentWords)
    .order('word');
    
  if (existingComponents) {
    console.log(`   Found ${existingComponents.length}/${componentWords.length} component words:`);
    existingComponents.forEach(w => console.log(`      ✅ ${w.word}`));
    
    const missing = componentWords.filter(w => 
      !existingComponents.find(e => e.word === w)
    );
    if (missing.length > 0) {
      console.log('   Missing component words:');
      missing.forEach(w => console.log(`      ❌ ${w}`));
    }
  }
  
  // 4. Check that the combined words are gone
  console.log('\n4. Verifying combined words were deleted:');
  const combinedWords = [
    'sepulchralsangfroid', 'hostilehowler', 'indolentdocumentary',
    'grandeurottoman', 'evaporationbittern', 'grudginglycanopy'
  ];
  
  const { data: remainingCombined } = await supabase
    .from('spelling_words')
    .select('word')
    .in('word', combinedWords);
    
  if (remainingCombined && remainingCombined.length > 0) {
    console.log(`   ⚠️ Found ${remainingCombined.length} combined words still in database:`);
    remainingCombined.forEach(w => console.log(`      - ${w.word}`));
  } else {
    console.log('   ✅ All sample combined words have been removed!');
  }
  
  // 5. Get current total count
  console.log('\n5. Database statistics:');
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
    
  console.log(`   Total words in database: ${totalCount}`);
  console.log(`   Expected reduction: 238 words`);
  
  // 6. Check for other potential combined words (unusually long words without spaces)
  console.log('\n6. Checking for other potential combined words:');
  const { data: longWords } = await supabase
    .from('spelling_words')
    .select('word')
    .gte('length(word)', 20)
    .not('word', 'ilike', '% %')  // No spaces
    .not('word', 'ilike', '%-%')  // No hyphens
    .limit(10);
    
  if (longWords && longWords.length > 0) {
    console.log(`   Found ${longWords.length} very long words without spaces or hyphens:`);
    longWords.forEach(w => console.log(`      - ${w.word} (${w.word.length} chars)`));
    console.log('   These might need review for potential combined word errors.');
  } else {
    console.log('   No suspicious long words found.');
  }
  
  // Summary
  console.log('\n========== CLEANUP SUMMARY ==========');
  console.log(`✅ "Word error" definitions removed: ${remainingErrors?.length === 0 ? 'SUCCESS' : 'INCOMPLETE'}`);
  console.log(`✅ Component words preserved: ${existingComponents?.length > 0 ? 'YES' : 'CHECK NEEDED'}`);
  console.log(`✅ Combined words deleted: ${remainingCombined?.length === 0 ? 'SUCCESS' : 'INCOMPLETE'}`);
  console.log(`📊 Total words in database: ${totalCount}`);
}

verifyWordErrorCleanup()
  .then(() => console.log('\nVerification complete!'))
  .catch(console.error);