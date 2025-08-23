const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function debugDatabaseIssue() {
  try {
    console.log('🔍 DEBUGGING DATABASE UPDATE ISSUE\n');
    
    // Test if we can update a specific word
    console.log('Testing database update capability...');
    
    const { data: testWord, error: selectError } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .eq('word', 'nares')
      .limit(1);
    
    if (selectError) {
      console.error('❌ Select error:', selectError);
      return;
    }
    
    if (!testWord || testWord.length === 0) {
      console.log('❌ Word "nares" not found in database');
      return;
    }
    
    console.log(`Found word: ${testWord[0].word}`);
    console.log(`Current pronunciation_guide: "${testWord[0].pronunciation_guide}"`);
    
    // Test updating this word
    console.log('\nAttempting to update pronunciation...');
    const testPronunciation = 'NAY-reez-TEST';
    
    const { error: updateError } = await supabase
      .from('spelling_words')
      .update({ 
        pronunciation_guide: testPronunciation,
        updated_at: new Date().toISOString()
      })
      .eq('id', testWord[0].id);
    
    if (updateError) {
      console.error('❌ Update error:', updateError);
      console.log('\n🔧 POSSIBLE SOLUTIONS:');
      console.log('1. Check if SUPABASE_SERVICE_ROLE_KEY should be used instead of ANON_KEY');
      console.log('2. Verify RLS (Row Level Security) policies allow updates');
      console.log('3. Check if the user has proper permissions');
      return;
    }
    
    console.log('✅ Update command succeeded');
    
    // Verify the update worked
    const { data: updatedWord, error: verifyError } = await supabase
      .from('spelling_words')
      .select('pronunciation_guide, updated_at')
      .eq('id', testWord[0].id)
      .limit(1);
    
    if (verifyError) {
      console.error('❌ Verify error:', verifyError);
      return;
    }
    
    console.log(`\nVerified pronunciation_guide: "${updatedWord[0].pronunciation_guide}"`);
    console.log(`Updated at: ${updatedWord[0].updated_at}`);
    
    if (updatedWord[0].pronunciation_guide === testPronunciation) {
      console.log('\n✅ DATABASE UPDATES ARE WORKING!');
      console.log('The issue may have been temporary network problems during batch processing.');
      
      // Reset the test word back
      await supabase
        .from('spelling_words')
        .update({ pronunciation_guide: null })
        .eq('id', testWord[0].id);
      
    } else {
      console.log('\n❌ DATABASE UPDATES ARE NOT WORKING!');
      console.log('The update command succeeded but the data was not actually saved.');
    }
    
    // Test using service role key instead
    console.log('\n🔄 Testing with SERVICE ROLE KEY...');
    
    const serviceSupabase = createClient(
      process.env.REACT_APP_SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE_KEY
    );
    
    const { error: serviceUpdateError } = await serviceSupabase
      .from('spelling_words')
      .update({ 
        pronunciation_guide: 'NAY-reez-SERVICE-TEST',
        updated_at: new Date().toISOString()
      })
      .eq('id', testWord[0].id);
    
    if (serviceUpdateError) {
      console.error('❌ Service role update error:', serviceUpdateError);
    } else {
      console.log('✅ Service role update succeeded');
      
      // Verify service role update
      const { data: serviceVerify } = await serviceSupabase
        .from('spelling_words')
        .select('pronunciation_guide')
        .eq('id', testWord[0].id)
        .limit(1);
      
      if (serviceVerify && serviceVerify[0].pronunciation_guide === 'NAY-reez-SERVICE-TEST') {
        console.log('✅ SERVICE ROLE KEY WORKS! Use this for updates.');
        
        // Clean up
        await serviceSupabase
          .from('spelling_words')
          .update({ pronunciation_guide: null })
          .eq('id', testWord[0].id);
      }
    }
    
  } catch (error) {
    console.error('Debug failed:', error);
    
    if (error.message.includes('permission') || error.message.includes('policy')) {
      console.log('\n🔧 PERMISSION ISSUE DETECTED:');
      console.log('Need to use SUPABASE_SERVICE_ROLE_KEY for write operations');
    }
  }
}

debugDatabaseIssue();