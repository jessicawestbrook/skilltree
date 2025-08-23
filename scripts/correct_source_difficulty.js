const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function correctSourceDifficulty() {
  console.log('=== CORRECTING SOURCE DIFFICULTY TO MATCH SCRIPPS PDFs ===\n');

  try {
    // First, check if we have source year data or can map based on word source patterns
    console.log('Analyzing current data to determine year mappings...');
    
    // Get a sample of data to understand the current structure
    const { data: sampleData, error: sampleError } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty, created_at')
      .limit(100);
      
    if (sampleError) {
      console.error('Error fetching sample data:', sampleError);
      return;
    }
    
    console.log('Sample current source difficulties:');
    const currentDifficulties = {};
    sampleData.forEach(row => {
      if (row.source_difficulty) {
        currentDifficulties[row.source_difficulty] = (currentDifficulties[row.source_difficulty] || 0) + 1;
      }
    });
    
    Object.entries(currentDifficulties).forEach(([diff, count]) => {
      console.log(`  ${diff}: ${count} words (in sample)`);
    });
    
    console.log('\nBased on the extracted CSV, the correct source difficulties should be:');
    console.log('  - "2020" for words from 2020 Scripps PDF');
    console.log('  - "2021" for words from 2021 Scripps PDF');  
    console.log('  - "2022" for words from 2022 Scripps PDF');
    console.log('  - "2023" for words from 2023 Scripps PDF');
    console.log('  - "2024" for words from 2024 Scripps PDF');
    console.log('  - "2025" for words from 2025 Scripps PDF');
    
    console.log('\nHowever, we need to determine which words came from which year.');
    console.log('Since we don\'t have reliable year data in the current table,');
    console.log('we should either:');
    console.log('1. Re-extract from the original PDFs with proper year tracking');
    console.log('2. Use the processed CSV files that have the correct year data');
    console.log('3. Create a mapping based on word patterns if possible');
    
    console.log('\nRecommendation: Import the correctly processed data from');
    console.log('scripts/spelling_bee/output/spelling_words.csv which has proper year-based source difficulties.');

  } catch (error) {
    console.error('Error during analysis:', error);
  }
}

correctSourceDifficulty();