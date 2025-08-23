const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function verifyGradeLevels() {
  console.log('Verifying grade level assignment...');
  
  // Get all words and count grade levels manually (with batching)
  console.log('Fetching all words from database...');
  let allWords = [];
  const batchSize = 1000;
  let offset = 0;
  let hasMore = true;

  while (hasMore) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('grade_level')
      .range(offset, offset + batchSize - 1)
      .order('id');

    if (error) {
      console.error('Error fetching words:', error);
      return;
    }

    if (batch && batch.length > 0) {
      allWords = allWords.concat(batch);
      console.log(`Fetched ${allWords.length} words so far...`);
      offset += batchSize;
      hasMore = batch.length === batchSize;
    } else {
      hasMore = false;
    }
  }
  
  // Count grade levels
  const gradeCount = {};
  let nullCount = 0;
  
  allWords.forEach(word => {
    if (word.grade_level) {
      gradeCount[word.grade_level] = (gradeCount[word.grade_level] || 0) + 1;
    } else {
      nullCount++;
    }
  });
  
  console.log(`\nTotal words in database: ${allWords.length}`);
  console.log('\nGrade Level Distribution:');
  
  const sortedGrades = Object.keys(gradeCount).sort((a, b) => parseInt(a) - parseInt(b));
  let totalAssigned = 0;
  
  sortedGrades.forEach(grade => {
    const count = gradeCount[grade];
    totalAssigned += count;
    const percentage = ((count / allWords.length) * 100).toFixed(1);
    console.log(`Grade ${grade}: ${count} words (${percentage}%)`);
  });
  
  console.log(`\nWords with grade levels assigned: ${totalAssigned}`);
  
  if (nullCount > 0) {
    console.log(`⚠️  Words with NULL grade levels: ${nullCount}`);
  } else {
    console.log('✅ All words have been assigned grade levels!');
  }
}

verifyGradeLevels().then(() => process.exit(0)).catch(console.error);