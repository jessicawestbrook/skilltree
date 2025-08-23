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

// Grade level mapping
function calculateGradeLevel(spellingDifficultyId, vocabularyDifficultyId) {
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
  
  const spellingGrade = spellingGrades[spellingDifficultyId] || 6;
  const vocabularyGrade = vocabularyGrades[vocabularyDifficultyId] || 6;
  
  // Calculate weighted average (vocabulary is slightly more important)
  const gradeLevel = Math.round((spellingGrade * 0.4 + vocabularyGrade * 0.6));
  
  return Math.min(Math.max(gradeLevel, 1), 12);
}

async function applyAllGradeLevels() {
  console.log('=== APPLYING GRADE LEVELS TO ALL MISSING WORDS ===\n');
  
  // First, check how many are missing
  const { count: initialMissing } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('grade_level', null);
  
  console.log(`Words missing grade levels: ${initialMissing}\n`);
  
  if (initialMissing === 0) {
    console.log('✅ All words already have grade levels!');
    return;
  }
  
  let totalUpdated = 0;
  let offset = 0;
  const batchSize = 500; // Process 500 at a time
  
  while (true) {
    // Fetch batch of words missing grade levels
    const { data: wordsToUpdate, error } = await supabase
      .from('spelling_words')
      .select('id, word, spelling_difficulty_id, vocabulary_difficulty_id')
      .is('grade_level', null)
      .range(offset, offset + batchSize - 1);
    
    if (error) {
      console.error('Error fetching words:', error);
      break;
    }
    
    if (!wordsToUpdate || wordsToUpdate.length === 0) {
      console.log('No more words to update');
      break;
    }
    
    console.log(`Processing batch: ${wordsToUpdate.length} words...`);
    
    // Calculate grade levels and update
    const updatePromises = wordsToUpdate.map(async (word) => {
      const gradeLevel = calculateGradeLevel(
        word.spelling_difficulty_id || 1,
        word.vocabulary_difficulty_id || 1
      );
      
      const { error: updateError } = await supabase
        .from('spelling_words')
        .update({ grade_level: gradeLevel })
        .eq('id', word.id);
      
      if (!updateError) {
        return { success: true, word: word.word, gradeLevel };
      } else {
        return { success: false, word: word.word, error: updateError };
      }
    });
    
    const results = await Promise.all(updatePromises);
    const successCount = results.filter(r => r.success).length;
    
    totalUpdated += successCount;
    console.log(`  ✓ Updated ${successCount} words in this batch`);
    
    // Show some examples from this batch
    const examples = results.filter(r => r.success).slice(0, 3);
    examples.forEach(ex => {
      console.log(`    ${ex.word}: Grade ${ex.gradeLevel}`);
    });
    
    if (wordsToUpdate.length < batchSize) {
      // This was the last batch
      break;
    }
    
    offset += batchSize;
    
    // Small delay between batches
    await new Promise(resolve => setTimeout(resolve, 200));
  }
  
  // Final verification
  console.log('\n--- Final Summary ---');
  console.log(`Total words updated: ${totalUpdated}`);
  
  const { count: stillMissing } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('grade_level', null);
  
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`Words still missing grade_level: ${stillMissing}`);
  console.log(`Total words: ${totalCount}`);
  console.log(`Coverage: ${(((totalCount - stillMissing) / totalCount) * 100).toFixed(1)}%`);
  
  if (stillMissing === 0) {
    console.log('\n✅ Success! All words now have grade levels assigned!');
  } else {
    console.log('\n⚠️ Some words still missing grade levels. Run again if needed.');
  }
  
  // Show grade level distribution
  console.log('\n--- Final Grade Level Distribution ---');
  
  const { data: gradeDist } = await supabase
    .from('spelling_words')
    .select('grade_level');
  
  if (gradeDist) {
    const gradeCounts = {};
    gradeDist.forEach(row => {
      const grade = row.grade_level;
      if (grade !== null) {
        gradeCounts[grade] = (gradeCounts[grade] || 0) + 1;
      }
    });
    
    Object.entries(gradeCounts)
      .sort(([a], [b]) => Number(a) - Number(b))
      .forEach(([grade, count]) => {
        const percent = ((count / totalCount) * 100).toFixed(1);
        console.log(`  Grade ${grade}: ${count} words (${percent}%)`);
      });
  }
}

applyAllGradeLevels().catch(console.error);