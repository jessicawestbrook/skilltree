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

async function finalVerification() {
  console.log('=== FINAL VERIFICATION OF DIFFICULTY ASSIGNMENTS ===\n');
  
  // Check for any remaining null values
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  const { count: missingVocab } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('vocabulary_difficulty_id', null);
  
  const { count: missingSpelling } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .is('spelling_difficulty_id', null);
  
  console.log('Database Status:');
  console.log(`Total words: ${totalCount}`);
  console.log(`Missing vocabulary difficulty: ${missingVocab}`);
  console.log(`Missing spelling difficulty: ${missingSpelling}`);
  
  if (missingVocab === 0 && missingSpelling === 0) {
    console.log('\n✅ ALL WORDS HAVE DIFFICULTY LEVELS ASSIGNED!\n');
  } else {
    console.log('\n⚠ Some words still missing difficulty levels\n');
  }
  
  // Get complete distribution
  console.log('--- Vocabulary Difficulty Distribution ---');
  
  const { data: vocabDifficulties } = await supabase
    .from('vocabulary_difficulties')
    .select('id, name, description')
    .order('id');
  
  for (const diff of vocabDifficulties || []) {
    const { count } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .eq('vocabulary_difficulty_id', diff.id);
    
    const percent = ((count / totalCount) * 100).toFixed(2);
    console.log(`Level ${diff.id} - ${diff.name} (${diff.description}): ${count} words (${percent}%)`);
  }
  
  console.log('\n--- Spelling Difficulty Distribution ---');
  
  const { data: spellingDifficulties } = await supabase
    .from('spelling_difficulties')
    .select('id, name, description')
    .order('id');
  
  for (const diff of spellingDifficulties || []) {
    const { count } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .eq('spelling_difficulty_id', diff.id);
    
    const percent = ((count / totalCount) * 100).toFixed(2);
    console.log(`Level ${diff.id} - ${diff.name} (${diff.description}): ${count} words (${percent}%)`);
  }
  
  // Sample some words from each difficulty level
  console.log('\n--- Sample Words by Difficulty ---');
  
  for (const vocabDiff of vocabDifficulties || []) {
    const { data: samples } = await supabase
      .from('spelling_words')
      .select('word')
      .eq('vocabulary_difficulty_id', vocabDiff.id)
      .limit(5);
    
    if (samples && samples.length > 0) {
      const words = samples.map(s => s.word).join(', ');
      console.log(`\nVocab ${vocabDiff.name}: ${words}`);
    }
  }
  
  console.log('\n=== VERIFICATION COMPLETE ===');
}

finalVerification().catch(console.error);