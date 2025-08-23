const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Manual pronunciations for legitimate words that need them
const manualPronunciations = {
  'ringing': 'RING-ing',
  'referred': 'rih-FURD',
  'redingote': 'RED-ing-goht',
  'proselytizer': 'PROS-uh-ly-ty-zer',
  'pulverised': 'PUL-ver-yzd',
  'preserving': 'prih-ZUR-ving',
  'overweening': 'oh-ver-WEE-ning',
  'preternaturally': 'pree-ter-NACH-er-uh-lee',
  'proffered': 'PROF-erd',
  'unilaterally': 'yoo-ni-LAT-er-uh-lee',
  'veganism': 'VEE-gan-izm',
  'vegetables': 'VEJ-tuh-bulz',
  'vertere': 'VER-ter-ay',
  'smouldering': 'SMOHL-der-ing',
  'pâtissier': 'pah-tee-see-AY',
  'résumé': 'REZ-oo-may',
  'velouté': 'vel-oo-TAY',
  'soirée': 'swah-RAY',
  'soupçon': 'soup-SAWN',
  'reykjavík': 'RAY-kyah-veek'
};

// Words to delete (combined words that can't be separated)
const wordsToDelete = [
  'nostrilsthe',
  'nulliusnoun', 
  'obligeviscount',
  'obviouspulse',
  'oceaniancharitable',
  'ogivalnoun',
  'referralaerials',
  'reiterateremorseful',
  'renvoinoun',
  'rescissiblejungian',
  'rescissiblereveille',
  'resuscitateretina',
  'revelationarithmetic',
  'runesancestors',
  'ryeland',
  'ryelanddomesticity',
  'sherifftarry',
  'shutterscorner',
  'solderinterim',
  'soppinesssousaphone',
  'solitairedishevel',
  'shrivellimbering',
  'regnalattaché',
  'shhh'
];

async function createBackup() {
  console.log('Creating backup of words with missing pronunciations...');
  
  const { data: wordsToBackup, error } = await supabase
    .from('spelling_words')
    .select('*')
    .is('pronunciation_guide', null);
    
  if (error) {
    console.error('Error creating backup:', error);
    return false;
  }
  
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\pronunciation_backup_${timestamp}.json`;
  
  fs.writeFileSync(backupFile, JSON.stringify(wordsToBackup, null, 2));
  console.log(`Backup created: ${backupFile}`);
  return true;
}

async function deleteInvalidWords() {
  console.log('Deleting invalid combined words...');
  let deleted = 0;
  
  for (const word of wordsToDelete) {
    const { error } = await supabase
      .from('spelling_words')
      .delete()
      .eq('word', word);
      
    if (error) {
      console.error(`Error deleting ${word}:`, error);
    } else {
      console.log(`✓ Deleted: ${word}`);
      deleted++;
    }
  }
  
  console.log(`Deleted ${deleted} invalid words`);
  return deleted;
}

async function addManualPronunciations() {
  console.log('Adding manual pronunciations...');
  let updated = 0;
  
  for (const [word, pronunciation] of Object.entries(manualPronunciations)) {
    const { error } = await supabase
      .from('spelling_words')
      .update({ pronunciation_guide: pronunciation })
      .eq('word', word)
      .is('pronunciation_guide', null);
      
    if (error) {
      console.error(`Error updating ${word}:`, error);
    } else {
      console.log(`✓ Added pronunciation: ${word} = ${pronunciation}`);
      updated++;
    }
  }
  
  console.log(`Updated ${updated} words with pronunciations`);
  return updated;
}

async function verifyResults() {
  console.log('\n=== VERIFICATION ===');
  
  const { data: remainingMissing, error } = await supabase
    .from('spelling_words')
    .select('word, id')
    .is('pronunciation_guide', null);
    
  if (error) {
    console.error('Error checking remaining words:', error);
    return;
  }
  
  console.log(`Words still missing pronunciations: ${remainingMissing.length}`);
  
  if (remainingMissing.length > 0) {
    console.log('Remaining words:');
    remainingMissing.forEach(word => console.log(`- ${word.word} (ID: ${word.id})`));
  }
}

async function main() {
  console.log('Starting manual pronunciation fix...\n');
  
  try {
    // Create backup
    await createBackup();
    
    // Delete invalid words
    const deletedCount = await deleteInvalidWords();
    
    // Add pronunciations
    const updatedCount = await addManualPronunciations();
    
    console.log(`\n=== SUMMARY ===`);
    console.log(`Deleted words: ${deletedCount}`);
    console.log(`Updated pronunciations: ${updatedCount}`);
    
    // Verify results
    await verifyResults();
    
    console.log('\n✓ Manual pronunciation fix completed!');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}