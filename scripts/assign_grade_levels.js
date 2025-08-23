import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

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

// Grade level mapping based on difficulty levels
// This mapping is based on typical US grade level expectations
function calculateGradeLevel(spellingDifficultyId, vocabularyDifficultyId) {
  // Spelling difficulty levels:
  // 1 = Beginner (grades K-2)
  // 2 = Elementary (grades 2-4)
  // 3 = Intermediate (grades 4-7)
  // 4 = Advanced (grades 7-10)
  // 5 = Expert (grades 10+)
  
  // Vocabulary difficulty levels:
  // 1 = Foundation (grades K-3)
  // 2 = Academic (grades 3-6)
  // 3 = Sophisticated (grades 6-9)
  // 4 = Specialized (grades 9-12)
  // 5 = Scholarly (college+)
  
  const spellingGrades = {
    1: 2,  // Beginner -> Grade 2
    2: 3,  // Elementary -> Grade 3
    3: 5,  // Intermediate -> Grade 5
    4: 8,  // Advanced -> Grade 8
    5: 11  // Expert -> Grade 11
  };
  
  const vocabularyGrades = {
    1: 2,  // Foundation -> Grade 2
    2: 4,  // Academic -> Grade 4
    3: 7,  // Sophisticated -> Grade 7
    4: 10, // Specialized -> Grade 10
    5: 12  // Scholarly -> Grade 12+
  };
  
  // Get base grades from difficulty levels
  const spellingGrade = spellingGrades[spellingDifficultyId] || 6;
  const vocabularyGrade = vocabularyGrades[vocabularyDifficultyId] || 6;
  
  // Calculate weighted average (vocabulary is slightly more important for grade level)
  const gradeLevel = Math.round((spellingGrade * 0.4 + vocabularyGrade * 0.6));
  
  // Ensure grade level is within reasonable bounds
  return Math.min(Math.max(gradeLevel, 1), 12);
}

async function assignGradeLevels() {
  console.log('=== ASSIGNING GRADE LEVELS TO SPELLING WORDS ===\n');
  
  // Fetch words missing grade levels (with no limit to get all)
  const { data: wordsToUpdate, error } = await supabase
    .from('spelling_words')
    .select('id, word, spelling_difficulty_id, vocabulary_difficulty_id')
    .is('grade_level', null)
    .limit(10000); // Set high limit to get all records
  
  if (error) {
    console.error('Error fetching words:', error);
    return;
  }
  
  console.log(`Found ${wordsToUpdate.length} words missing grade levels\n`);
  
  // Calculate grade levels for each word
  const updates = wordsToUpdate.map(word => {
    const gradeLevel = calculateGradeLevel(
      word.spelling_difficulty_id || 1,
      word.vocabulary_difficulty_id || 1
    );
    
    return {
      id: word.id,
      word: word.word,
      spelling_difficulty_id: word.spelling_difficulty_id,
      vocabulary_difficulty_id: word.vocabulary_difficulty_id,
      grade_level: gradeLevel
    };
  });
  
  // Show distribution of proposed grade levels
  console.log('--- Proposed Grade Level Distribution ---');
  const gradeCounts = {};
  updates.forEach(u => {
    gradeCounts[u.grade_level] = (gradeCounts[u.grade_level] || 0) + 1;
  });
  
  Object.entries(gradeCounts)
    .sort(([a], [b]) => Number(a) - Number(b))
    .forEach(([grade, count]) => {
      const percent = ((count / updates.length) * 100).toFixed(1);
      console.log(`  Grade ${grade}: ${count} words (${percent}%)`);
    });
  
  // Show sample assignments
  console.log('\n--- Sample Grade Level Assignments ---');
  updates.slice(0, 10).forEach(u => {
    console.log(`  ${u.word}: Grade ${u.grade_level} (S${u.spelling_difficulty_id}, V${u.vocabulary_difficulty_id})`);
  });
  
  // Save to file for review
  const outputPath = join(__dirname, 'grade_level_assignments.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalWords: updates.length,
    distribution: gradeCounts,
    assignments: updates
  }, null, 2));
  
  console.log(`\n✓ Saved assignments to: ${outputPath}`);
  console.log('\nReview the assignments before applying to database.');
}

// Function to apply the grade level updates
async function applyGradeLevelUpdates() {
  console.log('\n=== APPLYING GRADE LEVEL UPDATES ===\n');
  
  // Load the assignments
  const assignmentsPath = join(__dirname, 'grade_level_assignments.json');
  
  if (!fs.existsSync(assignmentsPath)) {
    console.error('Assignments file not found. Run assignGradeLevels() first.');
    return;
  }
  
  const data = JSON.parse(fs.readFileSync(assignmentsPath, 'utf8'));
  const updates = data.assignments;
  
  console.log(`Applying grade levels to ${updates.length} words...`);
  
  // Process in batches
  const batchSize = 50;
  let successCount = 0;
  let errorCount = 0;
  
  for (let i = 0; i < updates.length; i += batchSize) {
    const batch = updates.slice(i, i + batchSize);
    const batchNumber = Math.floor(i / batchSize) + 1;
    const totalBatches = Math.ceil(updates.length / batchSize);
    
    process.stdout.write(`Batch ${batchNumber}/${totalBatches}: `);
    
    const promises = batch.map(async (update) => {
      const { error } = await supabase
        .from('spelling_words')
        .update({ grade_level: update.grade_level })
        .eq('id', update.id);
      
      return !error;
    });
    
    const results = await Promise.all(promises);
    const batchSuccess = results.filter(r => r).length;
    const batchErrors = results.filter(r => !r).length;
    
    successCount += batchSuccess;
    errorCount += batchErrors;
    
    console.log(`✓ ${batchSuccess} updated, ${batchErrors} errors`);
    
    // Small delay between batches
    if (i + batchSize < updates.length) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  console.log('\n--- Update Summary ---');
  console.log(`Successfully updated: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  
  // Verify the updates
  const { count: stillMissing } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('grade_level', null);
  
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`\nWords still missing grade_level: ${stillMissing}`);
  console.log(`Total words: ${totalCount}`);
  console.log(`Coverage: ${(((totalCount - stillMissing) / totalCount) * 100).toFixed(1)}%`);
  
  if (stillMissing === 0) {
    console.log('\n✅ All words now have grade levels assigned!');
  }
}

// Run assignment
assignGradeLevels().catch(console.error);

// Export the apply function for manual execution
export { applyGradeLevelUpdates };