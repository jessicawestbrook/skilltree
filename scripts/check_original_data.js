const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkOriginalData() {
  console.log('Checking available original difficulty data...');
  
  const { data: sample } = await supabase
    .from('spelling_words')
    .select('word, source_difficulty, source_difficulties, source_names')
    .limit(10);
  
  console.log('Sample of 10 words:');
  sample?.forEach((word, i) => {
    console.log(`${i+1}. ${word.word}`);
    console.log(`   source_difficulty: ${word.source_difficulty}`);
    console.log(`   source_difficulties: ${word.source_difficulties}`);
    console.log(`   source_names: ${word.source_names}`);
    console.log('');
  });
  
  // Check for non-null source_difficulties
  const { data: nonNull } = await supabase
    .from('spelling_words')
    .select('word, source_difficulties')
    .not('source_difficulties', 'is', null)
    .limit(10);
    
  console.log(`Words with non-null source_difficulties: ${nonNull?.length || 0}`);
  
  if (nonNull && nonNull.length > 0) {
    console.log('Examples:');
    nonNull.forEach(word => {
      console.log(`  ${word.word}: ${word.source_difficulties}`);
    });
  }
  
  // Since source_difficulties might be null, let me create a balanced redistribution
  // based on other factors like word length, AI difficulty, etc.
  console.log('\nSince original distribution data may not be available,');
  console.log('I should create a balanced redistribution based on word characteristics:');
  console.log('Target: 40% One Bee, 35% Two Bee, 25% Three Bee');
}

checkOriginalData()
  .then(() => process.exit(0))
  .catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });