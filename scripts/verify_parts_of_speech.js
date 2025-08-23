const { createClient } = require('@supabase/supabase-js');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env.local') });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyUpdates() {
  console.log('=== VERIFYING PARTS OF SPEECH UPDATES ===\n');
  
  // Check overall statistics
  const { count: total } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  const { count: withPos } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .not('part_of_speech', 'is', null)
    .neq('part_of_speech', '');
  
  const { count: missing } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .or('part_of_speech.is.null,part_of_speech.eq.');
  
  console.log('📊 Overall Statistics:');
  console.log('  Total words:', total);
  console.log('  Words WITH part_of_speech:', withPos);
  console.log('  Words MISSING part_of_speech:', missing);
  console.log('  Coverage:', ((withPos / total) * 100).toFixed(1) + '%');
  
  // Get breakdown by part of speech
  const { data: breakdown } = await supabase
    .from('spelling_words')
    .select('part_of_speech');
  
  const counts = {};
  breakdown.forEach(item => {
    const pos = item.part_of_speech || 'null';
    counts[pos] = (counts[pos] || 0) + 1;
  });
  
  console.log('\n📈 Breakdown by part of speech:');
  Object.entries(counts)
    .sort(([,a], [,b]) => b - a)
    .forEach(([pos, count]) => {
      if (pos !== 'null') {
        const percent = ((count / total) * 100).toFixed(1);
        console.log(`  ${pos}: ${count} words (${percent}%)`);
      }
    });
  
  // Sample some of the words that should have been updated
  const { data: samples } = await supabase
    .from('spelling_words')
    .select('word, part_of_speech')
    .in('word', ['sound', 'help', 'mystery', 'overrun', 'spiteful', 'musings', 'mildew'])
    .order('word');
  
  console.log('\n✅ Sample words that were updated:');
  samples.forEach(w => {
    console.log(`  ${w.word} → ${w.part_of_speech}`);
  });
  
  // Check if the specific words from our NLP analysis were updated
  const testWords = ['sound', 'help', 'mystery'];
  const expectedPos = { 'sound': 'verb', 'help': 'verb', 'mystery': 'noun' };
  
  console.log('\n🔍 Verification of specific words:');
  for (const word of testWords) {
    const { data } = await supabase
      .from('spelling_words')
      .select('word, part_of_speech')
      .eq('word', word)
      .single();
    
    if (data) {
      const expected = expectedPos[word];
      const match = data.part_of_speech === expected ? '✅' : '❌';
      console.log(`  ${word}: ${data.part_of_speech} ${match} (expected: ${expected})`);
    }
  }
  
  // Summary
  console.log('\n📋 Summary:');
  if (missing === 0) {
    console.log('  🎉 SUCCESS! All words now have parts of speech assigned!');
  } else if (missing < 100) {
    console.log(`  ⚠️  Almost done! Only ${missing} words still missing parts of speech.`);
  } else {
    console.log(`  ℹ️  ${missing} words still need parts of speech.`);
  }
}

verifyUpdates().catch(console.error);