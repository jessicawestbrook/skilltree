import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: join(__dirname, '..', '.env.local') });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceRoleKey = process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);

async function checkGradeLevels() {
  console.log('=== CHECKING GRADE LEVELS IN SPELLING_WORDS ===\n');
  
  // Get total count
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`Total words: ${totalCount}`);
  
  // Check words with NULL grade_level
  const { count: nullGradeCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('grade_level', null);
  
  console.log(`Words with NULL grade_level: ${nullGradeCount}`);
  
  // Check distribution of existing grade levels
  console.log('\n--- Current Grade Level Distribution ---');
  
  // Get all unique grade levels
  const { data: gradeLevels } = await supabase
    .from('spelling_words')
    .select('grade_level')
    .not('grade_level', 'is', null);
  
  if (gradeLevels) {
    const gradeCounts = {};
    gradeLevels.forEach(row => {
      const grade = row.grade_level;
      gradeCounts[grade] = (gradeCounts[grade] || 0) + 1;
    });
    
    Object.entries(gradeCounts)
      .sort(([a], [b]) => Number(a) - Number(b))
      .forEach(([grade, count]) => {
        const percent = ((count / totalCount) * 100).toFixed(2);
        console.log(`  Grade ${grade}: ${count} words (${percent}%)`);
      });
  }
  
  // Sample words without grade levels
  console.log('\n--- Sample Words Missing Grade Levels ---');
  const { data: missingGrades } = await supabase
    .from('spelling_words')
    .select('id, word, spelling_difficulty_id, vocabulary_difficulty_id')
    .is('grade_level', null)
    .limit(10);
  
  if (missingGrades && missingGrades.length > 0) {
    missingGrades.forEach(word => {
      console.log(`  ${word.word} - Spelling Diff: ${word.spelling_difficulty_id}, Vocab Diff: ${word.vocabulary_difficulty_id}`);
    });
  }
  
  // Check correlation between difficulty levels and grade levels
  console.log('\n--- Difficulty to Grade Level Mapping (existing data) ---');
  
  const { data: mappingData } = await supabase
    .from('spelling_words')
    .select('spelling_difficulty_id, vocabulary_difficulty_id, grade_level')
    .not('grade_level', 'is', null)
    .limit(1000);
  
  if (mappingData) {
    // Analyze the mapping pattern
    const difficultyToGrade = {};
    
    mappingData.forEach(row => {
      const key = `S${row.spelling_difficulty_id}_V${row.vocabulary_difficulty_id}`;
      if (!difficultyToGrade[key]) {
        difficultyToGrade[key] = [];
      }
      difficultyToGrade[key].push(row.grade_level);
    });
    
    console.log('Common difficulty combinations and their grade levels:');
    Object.entries(difficultyToGrade)
      .sort(([a], [b]) => a.localeCompare(b))
      .slice(0, 10)
      .forEach(([combo, grades]) => {
        // Calculate average grade for this combination
        const avgGrade = grades.reduce((a, b) => a + b, 0) / grades.length;
        const [, spelling, vocab] = combo.match(/S(\d+)_V(\d+)/);
        console.log(`  Spelling ${spelling}, Vocab ${vocab}: Avg Grade ${avgGrade.toFixed(1)} (${grades.length} words)`);
      });
  }
  
  console.log('\n--- Summary ---');
  console.log(`Total words: ${totalCount}`);
  console.log(`Missing grade_level: ${nullGradeCount} (${((nullGradeCount/totalCount)*100).toFixed(1)}%)`);
  console.log(`Has grade_level: ${totalCount - nullGradeCount} (${(((totalCount - nullGradeCount)/totalCount)*100).toFixed(1)}%)`);
}

checkGradeLevels().catch(console.error);