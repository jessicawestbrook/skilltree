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

async function verifyForeignKeys() {
  console.log('=== VERIFYING FOREIGN KEY RELATIONSHIPS ===\n');
  
  // Test if the joins work correctly
  console.log('Testing vocabulary difficulty join...');
  const { data: vocabTest, error: vocabError } = await supabase
    .from('spelling_words')
    .select(`
      word,
      vocabulary_difficulty_id,
      vocabulary_difficulty_levels!vocabulary_difficulty_id(id, name, description)
    `)
    .limit(2);
  
  if (vocabError) {
    console.log('❌ Error with vocabulary join:', vocabError.message);
    
    // Try alternative join syntax
    console.log('\nTrying alternative join syntax...');
    const { data: altVocab, error: altVocabError } = await supabase
      .from('spelling_words')
      .select(`
        word,
        vocabulary_difficulty_id,
        vocabulary_difficulty_levels(id, name, description)
      `)
      .limit(2);
    
    if (altVocabError) {
      console.log('❌ Alternative also failed:', altVocabError.message);
    } else {
      console.log('✓ Alternative vocabulary join works!');
      if (altVocab && altVocab.length > 0) {
        console.log('Sample:', JSON.stringify(altVocab[0], null, 2));
      }
    }
  } else {
    console.log('✓ Vocabulary join works!');
    if (vocabTest && vocabTest.length > 0) {
      console.log('Sample:', JSON.stringify(vocabTest[0], null, 2));
    }
  }
  
  console.log('\nTesting spelling difficulty join...');
  const { data: spellTest, error: spellError } = await supabase
    .from('spelling_words')
    .select(`
      word,
      spelling_difficulty_id,
      spelling_difficulty_levels!spelling_difficulty_id(id, name, description)
    `)
    .limit(2);
  
  if (spellError) {
    console.log('❌ Error with spelling join:', spellError.message);
    
    // Try alternative join syntax
    console.log('\nTrying alternative join syntax...');
    const { data: altSpell, error: altSpellError } = await supabase
      .from('spelling_words')
      .select(`
        word,
        spelling_difficulty_id,
        spelling_difficulty_levels(id, name, description)
      `)
      .limit(2);
    
    if (altSpellError) {
      console.log('❌ Alternative also failed:', altSpellError.message);
    } else {
      console.log('✓ Alternative spelling join works!');
      if (altSpell && altSpell.length > 0) {
        console.log('Sample:', JSON.stringify(altSpell[0], null, 2));
      }
    }
  } else {
    console.log('✓ Spelling join works!');
    if (spellTest && spellTest.length > 0) {
      console.log('Sample:', JSON.stringify(spellTest[0], null, 2));
    }
  }
  
  // Check if foreign key constraints exist
  console.log('\n=== CHECKING FOREIGN KEY CONSTRAINTS ===\n');
  
  const { data: constraints, error: constraintError } = await supabase.rpc('get_foreign_keys', {
    table_name: 'spelling_words'
  }).catch(() => ({ data: null, error: 'RPC not available' }));
  
  if (constraintError || !constraints) {
    console.log('Could not fetch foreign key constraints (RPC may not exist)');
  } else {
    console.log('Foreign key constraints on spelling_words:');
    constraints.forEach(c => {
      console.log(`  ${c.constraint_name}: ${c.column_name} -> ${c.foreign_table_name}(${c.foreign_column_name})`);
    });
  }
}

verifyForeignKeys().catch(console.error);