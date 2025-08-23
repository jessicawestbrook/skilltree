const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://ozujqlucqdyszxmzhigf.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dWpxbHVjcWR5c3p4bXpoaWdmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI0MTMzNSwiZXhwIjoyMDcwODE3MzM1fQ.x-QbhMeO7HzECupWqq_XuHXeTbQmQwvVKasC61jb7Ws';

const supabase = createClient(supabaseUrl, supabaseKey);

async function analyzeAllWords() {
  console.log('Analyzing all spelling words...');
  
  const { data: words, error } = await supabase
    .from('spelling_words')
    .select('source_difficulty');
  
  if (error) {
    console.error('Error fetching words:', error);
    return;
  }
  
  console.log(`Total words in database: ${words.length}`);
  
  const counts = {};
  words.forEach(w => {
    const diff = w.source_difficulty || 'NULL';
    counts[diff] = (counts[diff] || 0) + 1;
  });
  
  console.log('\nComplete distribution:');
  Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .forEach(([key, value]) => {
      console.log(`  ${key}: ${value} words`);
    });
  
  // Count words without clear Scripps difficulty
  const nonScripps = words.filter(w => {
    if (!w.source_difficulty) return true;
    const diff = w.source_difficulty;
    return !diff.includes('One Bee') && 
           !diff.includes('Two Bee') && 
           !diff.includes('Three Bee');
  }).length;
  
  console.log(`\nWords without clear Scripps difficulty: ${nonScripps}`);
  console.log(`Words with Scripps difficulty: ${words.length - nonScripps}`);
  
  // Show breakdown of Scripps words
  const scrippsWords = words.filter(w => {
    if (!w.source_difficulty) return false;
    const diff = w.source_difficulty;
    return diff.includes('One Bee') || 
           diff.includes('Two Bee') || 
           diff.includes('Three Bee');
  });
  
  console.log(`\nScripps words breakdown: ${scrippsWords.length} total`);
  
  const scriptsCounts = {};
  scrippsWords.forEach(w => {
    const diff = w.source_difficulty;
    scriptsCounts[diff] = (scriptsCounts[diff] || 0) + 1;
  });
  
  Object.entries(scriptsCounts)
    .sort((a, b) => b[1] - a[1])
    .forEach(([key, value]) => {
      console.log(`  ${key}: ${value} words`);
    });
}

if (require.main === module) {
  analyzeAllWords()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error('Script failed:', error);
      process.exit(1);
    });
}