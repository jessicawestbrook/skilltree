const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkTableStructure() {
  console.log('=== CHECKING SPELLING_WORDS TABLE STRUCTURE ===\n');
  
  try {
    // Get column information from information_schema
    const { data: columns, error } = await supabase
      .rpc('get_table_columns', { table_name: 'spelling_words' });
    
    if (error) {
      // If RPC doesn't exist, try direct query
      console.log('Trying alternative method to get table structure...\n');
      
      // Get a sample row to see columns
      const { data: sampleRow, error: sampleError } = await supabase
        .from('spelling_words')
        .select('*')
        .limit(1)
        .single();
      
      if (sampleError) {
        console.error('Error getting sample row:', sampleError);
      } else {
        console.log('📊 CURRENT COLUMNS IN SPELLING_WORDS TABLE:');
        console.log('----------------------------------------');
        const columnNames = Object.keys(sampleRow || {});
        columnNames.forEach(col => {
          const value = sampleRow[col];
          const type = value === null ? 'null' : typeof value;
          console.log(`  - ${col} (sample type: ${type})`);
        });
      }
    } else {
      console.log('📊 DETAILED TABLE STRUCTURE:');
      console.log('----------------------------------------');
      columns?.forEach(col => {
        console.log(`  - ${col.column_name}: ${col.data_type}`);
      });
    }
    
    // Check for difficulty-related columns
    const { data: sampleData } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(5);
    
    if (sampleData && sampleData.length > 0) {
      const difficultyColumns = Object.keys(sampleData[0]).filter(col => 
        col.toLowerCase().includes('difficulty') ||
        col.toLowerCase().includes('spelling_difficulty') ||
        col.toLowerCase().includes('vocabulary_difficulty') ||
        col.toLowerCase().includes('source_difficulty')
      );
      
      console.log('\n🎯 DIFFICULTY-RELATED COLUMNS FOUND:');
      console.log('----------------------------------------');
      if (difficultyColumns.length > 0) {
        difficultyColumns.forEach(col => {
          // Get unique values for this column
          const uniqueValues = [...new Set(sampleData.map(row => row[col]))].filter(v => v !== null);
          console.log(`  - ${col}:`);
          console.log(`    Sample values: ${uniqueValues.slice(0, 3).join(', ')}`);
        });
      } else {
        console.log('  None found');
      }
    }
    
    // Check if there's a difficulty_id foreign key
    const { data: fkCheck } = await supabase
      .from('spelling_words')
      .select('difficulty_id')
      .limit(1);
    
    if (fkCheck && 'difficulty_id' in (fkCheck[0] || {})) {
      console.log('\n✅ Foreign key column "difficulty_id" exists');
      
      // Check the difficulties table
      const { data: difficulties } = await supabase
        .from('difficulties')
        .select('*')
        .order('id');
      
      if (difficulties) {
        console.log('\n📊 DIFFICULTIES TABLE:');
        console.log('----------------------------------------');
        difficulties.forEach(d => {
          console.log(`  ID ${d.id}: ${d.name} (${d.category || 'spelling'})`);
        });
      }
    } else {
      console.log('\n⚠️ No "difficulty_id" foreign key column found');
    }
    
    // Check for vocabulary_words table structure too
    console.log('\n=== CHECKING VOCABULARY_WORDS TABLE ===\n');
    const { data: vocabSample } = await supabase
      .from('vocabulary_words')
      .select('*')
      .limit(1);
    
    if (vocabSample && vocabSample.length > 0) {
      const vocabDiffColumns = Object.keys(vocabSample[0]).filter(col => 
        col.toLowerCase().includes('difficulty')
      );
      
      console.log('🎯 VOCABULARY DIFFICULTY COLUMNS:');
      console.log('----------------------------------------');
      vocabDiffColumns.forEach(col => {
        console.log(`  - ${col}`);
      });
    }
    
    console.log('\n=== ANALYSIS COMPLETE ===\n');
    console.log('Next steps:');
    console.log('1. Identify which difficulty columns are old/redundant');
    console.log('2. Ensure foreign key relationships are properly set');
    console.log('3. Remove old text-based difficulty columns');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

checkTableStructure().catch(console.error);