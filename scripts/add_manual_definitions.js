const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Manual definitions for the 46 words
const manualDefinitions = {
  'permission': 'Authorization or consent to do something; formal approval or allowance.',
  'weltschmerz': 'A feeling of melancholy and world-weariness; sadness from the difference between reality and ideals.',
  'wensleydale': 'A type of white cheese from Yorkshire, England, known for its crumbly texture and mild flavor.',
  'went': 'Past tense of "go"; moved from one place to another.',
  'wentletrap': 'A type of marine gastropod mollusk with a spiral shell, often found in tropical waters.',
  'werf': 'An obsolete term for a homestead or small settlement; also used in place names.',
  'western': 'Relating to or situated in the west; characteristic of western regions or culture.',
  'whakapapa': 'In Māori culture, a genealogical descent or family tree showing ancestral connections.',
  'whales': 'Large marine mammals that breathe air and have streamlined bodies adapted for swimming.',
  'wharf': 'A structure built along the water where ships can dock to load and unload cargo.',
  'whee': 'An exclamation expressing excitement or joy, especially when moving fast.',
  'wheedle': 'To persuade someone through flattery or coaxing; to cajole or sweet-talk.',
  'wheedling': 'The act of persuading through flattery; coaxing or cajoling behavior.',
  'wheezy': 'Making a whistling or rattling sound when breathing; characterized by wheezing.',
  'whelp': 'A young dog, wolf, or other carnivorous mammal; also used as a mild insult.',
  'whenever': 'At whatever time; on any occasion that something happens.',
  'whereas': 'While on the contrary; used to introduce a contrasting fact or consideration.',
  'wherewithal': 'The necessary means, especially financial resources, to accomplish something.',
  'whet': 'To sharpen something, especially a blade; to stimulate or increase appetite or interest.',
  'whether': 'Used to express doubt or choice between alternatives; if it is the case that.',
  'whey': 'The watery part of milk that separates from the curds when making cheese.',
  'whidah': 'An alternative spelling of "whydah," a type of African songbird.',
  'whiff': 'A brief, light smell or scent; a slight trace or hint of something.',
  'while': 'During the time that; throughout a period when something is happening.',
  'whimsical': 'Playfully quaint or fanciful; characterized by sudden changes of mood or behavior.',
  'whine': 'To complain in an annoying, high-pitched voice; to make a long, high sound.',
  'whipped': 'Past tense of "whip"; beaten or stirred vigorously; defeated decisively.',
  'whippoorwill': 'A North American bird known for its distinctive call that sounds like its name.',
  'whirlybird': 'Informal term for a helicopter, named for its spinning rotor blades.',
  'whisk': 'To move quickly and lightly; a kitchen utensil used for beating or mixing.',
  'whiskers': 'Long, stiff hairs growing from the face of certain animals, especially cats.',
  'whisper': 'To speak very softly or quietly; a very quiet or soft spoken sound.',
  'white': 'The color of fresh snow or milk; the lightest color, opposite of black.',
  'whitefish': 'Any of various freshwater fish with white or silvery scales, often used for food.',
  'whittle': 'To carve wood by cutting away small pieces; to gradually reduce something.',
  'whizzed': 'Past tense of "whiz"; moved very quickly with a humming or buzzing sound.',
  'whole': 'Complete; entire; not broken or damaged; all of something.',
  'wholehearted': 'Done with complete sincerity and commitment; enthusiastic and unreserved.',
  'whose': 'Belonging to or associated with which person; possessive form of "who."',
  'whydah': 'A type of African songbird, some species of which have very long tail feathers.',
  'wickiup': 'A dome-shaped dwelling used by some Native American tribes, made of poles and brush.',
  'widdershins': 'In a direction contrary to the sun\'s course; counterclockwise; the wrong way.',
  'wide': 'Having a great extent from side to side; broad; not narrow.',
  'widely': 'Over a large area or range; extensively; by many people.',
  'widget': 'A small gadget or device; in computing, a small application or interface element.',
  'wield': 'To handle or use something effectively, especially a tool or weapon; to exercise power.'
};

async function createBackup() {
  console.log('Creating backup of records to be updated...');
  
  const { data: recordsToUpdate, error } = await supabase
    .from('spelling_words')
    .select('*')
    .ilike('definition', '%[Definition needed%');
    
  if (error) {
    console.error('Error creating backup:', error);
    return false;
  }
  
  const fs = require('fs');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\manual_definitions_backup_${timestamp}.json`;
  
  fs.writeFileSync(backupFile, JSON.stringify(recordsToUpdate, null, 2));
  console.log(`Backup created: ${backupFile} (${recordsToUpdate.length} records)`);
  return true;
}

async function addManualDefinitions() {
  console.log('Adding manual definitions to words...');
  
  const results = {
    updated: 0,
    errors: [],
    notFound: []
  };
  
  for (const [word, definition] of Object.entries(manualDefinitions)) {
    try {
      const { data: matchingRecords, error: selectError } = await supabase
        .from('spelling_words')
        .select('id, word, definition')
        .eq('word', word)
        .ilike('definition', '%[Definition needed%');
        
      if (selectError) throw selectError;
      
      if (matchingRecords.length === 0) {
        console.log(`⚠ Word "${word}" not found or doesn't need definition`);
        results.notFound.push(word);
        continue;
      }
      
      for (const record of matchingRecords) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ definition: definition })
          .eq('id', record.id);
          
        if (updateError) throw updateError;
        
        console.log(`✓ Updated definition for: ${word}`);
        results.updated++;
      }
      
    } catch (error) {
      console.error(`Error updating ${word}:`, error);
      results.errors.push({ word, error: error.message });
    }
  }
  
  return results;
}

async function verifyUpdates() {
  console.log('\n=== VERIFICATION ===');
  
  // Check how many records still need definitions
  const { count: stillNeedDefs } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .ilike('definition', '%[Definition needed%');
    
  console.log(`Records still needing definitions: ${stillNeedDefs}`);
  
  // Show sample of updated records
  const { data: updatedSamples } = await supabase
    .from('spelling_words')
    .select('word, definition')
    .in('word', Object.keys(manualDefinitions))
    .limit(5);
    
  if (updatedSamples && updatedSamples.length > 0) {
    console.log('\nSample updated definitions:');
    updatedSamples.forEach(record => {
      console.log(`- ${record.word}: ${record.definition.substring(0, 60)}...`);
    });
  }
}

async function main() {
  console.log('Starting manual definition updates...');
  console.log(`Adding definitions for ${Object.keys(manualDefinitions).length} words\n`);
  
  try {
    // Create backup
    await createBackup();
    
    // Add manual definitions
    const results = await addManualDefinitions();
    
    console.log('\n=== RESULTS ===');
    console.log(`Successfully updated: ${results.updated} records`);
    console.log(`Words not found: ${results.notFound.length}`);
    console.log(`Errors: ${results.errors.length}`);
    
    if (results.notFound.length > 0) {
      console.log('\nWords not found:');
      results.notFound.forEach(word => console.log(`- ${word}`));
    }
    
    if (results.errors.length > 0) {
      console.log('\nErrors:');
      results.errors.forEach(error => {
        console.log(`- ${error.word}: ${error.error}`);
      });
    }
    
    // Verify the updates
    await verifyUpdates();
    
    // Save results
    const fs = require('fs');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const resultsFile = `C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\manual_definitions_results_${timestamp}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify({
      summary: {
        totalDefinitions: Object.keys(manualDefinitions).length,
        updated: results.updated,
        notFound: results.notFound.length,
        errors: results.errors.length
      },
      results
    }, null, 2));
    
    console.log(`\nResults saved to: ${resultsFile}`);
    console.log('\n✓ Manual definition updates completed!');
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

if (require.main === module) {
  main();
}