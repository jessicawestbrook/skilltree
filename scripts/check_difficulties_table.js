const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkDifficultiesTable() {
  console.log('=== CHECKING DIFFICULTIES TABLE ===\n');
  
  try {
    // Check if difficulties table exists and has data
    const { data: difficulties, error } = await supabase
      .from('difficulties')
      .select('*');
    
    if (error) {
      console.error('Error accessing difficulties table:', error);
      console.log('\n⚠️ The difficulties table may not exist or may have different structure.');
      
      // Try alternative table names
      console.log('\n🔍 Checking alternative table names...');
      
      const tables = ['difficulty', 'difficulty_levels', 'spelling_difficulties', 'vocabulary_difficulties'];
      
      for (const tableName of tables) {
        const { data, error: tableError } = await supabase
          .from(tableName)
          .select('*')
          .limit(5);
        
        if (!tableError && data) {
          console.log(`✅ Found table: ${tableName}`);
          console.log(`   Sample data:`, data.slice(0, 2));
        }
      }
      
      // Check what foreign keys are actually being used
      console.log('\n🔍 Checking actual foreign key values in spelling_words...');
      
      const { data: fkValues } = await supabase
        .from('spelling_words')
        .select('spelling_difficulty_id, vocabulary_difficulty_id')
        .not('spelling_difficulty_id', 'is', null)
        .limit(10);
      
      if (fkValues && fkValues.length > 0) {
        const uniqueSpellingIds = [...new Set(fkValues.map(v => v.spelling_difficulty_id))];
        const uniqueVocabIds = [...new Set(fkValues.map(v => v.vocabulary_difficulty_id))];
        
        console.log('\nUnique spelling_difficulty_id values found:', uniqueSpellingIds);
        console.log('Unique vocabulary_difficulty_id values found:', uniqueVocabIds);
      }
      
    } else {
      console.log(`📊 Difficulties table has ${difficulties?.length || 0} rows\n`);
      
      if (difficulties && difficulties.length > 0) {
        console.log('DIFFICULTIES TABLE CONTENT:');
        console.log('='.repeat(60));
        difficulties.forEach(d => {
          console.log(`ID: ${d.id}`);
          Object.entries(d).forEach(([key, value]) => {
            if (key !== 'id') console.log(`  ${key}: ${value}`);
          });
          console.log('-'.repeat(40));
        });
      }
    }
    
    // Check if we need to create the difficulties data
    if (!difficulties || difficulties.length === 0) {
      console.log('\n📝 DIFFICULTIES TABLE NEEDS TO BE POPULATED');
      console.log('\nSuggested difficulty levels:');
      
      const suggestedDifficulties = [
        // Spelling difficulties
        { id: 1, level: 1, name: 'Beginner', category: 'spelling', description: 'Simple, phonetic words' },
        { id: 2, level: 2, name: 'Elementary', category: 'spelling', description: 'Common words with basic patterns' },
        { id: 3, level: 3, name: 'Intermediate', category: 'spelling', description: 'Words with irregular patterns' },
        { id: 4, level: 4, name: 'Advanced', category: 'spelling', description: 'Complex words with unusual spellings' },
        { id: 5, level: 5, name: 'Expert', category: 'spelling', description: 'Very difficult, specialized words' },
        // Vocabulary difficulties
        { id: 6, level: 1, name: 'Basic', category: 'vocabulary', description: 'Everyday common words' },
        { id: 7, level: 2, name: 'Intermediate', category: 'vocabulary', description: 'Moderately complex words' },
        { id: 8, level: 3, name: 'Advanced', category: 'vocabulary', description: 'Advanced vocabulary' },
        { id: 9, level: 4, name: 'Sophisticated', category: 'vocabulary', description: 'Sophisticated, nuanced words' },
        { id: 10, level: 5, name: 'Academic', category: 'vocabulary', description: 'Highly specialized academic words' }
      ];
      
      console.log('\nSQL to create difficulties:');
      console.log('INSERT INTO difficulties (id, level, name, category, description) VALUES');
      suggestedDifficulties.forEach((d, i) => {
        const comma = i < suggestedDifficulties.length - 1 ? ',' : ';';
        console.log(`  (${d.id}, ${d.level}, '${d.name}', '${d.category}', '${d.description}')${comma}`);
      });
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkDifficultiesTable().catch(console.error);