// Import all processed spelling bee batches to database
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Load environment variables
require('dotenv').config({ path: '../../.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase environment variables');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function readCSVFile(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', reject);
  });
}

function mapCSVToDatabase(csvRow) {
  // Map CSV columns to database columns
  return {
    word: csvRow.word,
    definition: csvRow.definition,
    example_sentence: csvRow.example_sentence,
    pronunciation_guide: csvRow.pronunciation,
    etymology: csvRow.etymology,
    etymology_source: csvRow.etymology_source,
    memory_tips: csvRow.memory_tip,
    
    // Map difficulty scores
    ai_difficulty_level: parseInt(csvRow.difficulty_score) || 5,
    phonetic_transparency_score: parseInt(csvRow.phonetic_transparency) || 5,
    word_frequency_score: parseInt(csvRow.word_frequency) || 5,
    morphology_score: parseInt(csvRow.morphological_complexity) || 5,
    etymology_score: parseInt(csvRow.etymology_complexity) || 5,
    
    // Source information
    source_names: csvRow.sources,
    source_difficulties: csvRow.source_difficulty,
    original_source: 'Scripps National Spelling Bee',
    definition_source: csvRow.etymology_source || 'Claude',
    source_access_date: new Date().toISOString(),
    
    // Calculated fields
    difficulty_calculation_method: '4-factor scoring system',
    ai_difficulty_name: getDifficultyName(parseInt(csvRow.difficulty_score) || 5),
    
    // Timestamps
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
}

function getDifficultyName(score) {
  if (score <= 2) return 'Easy';
  if (score <= 4) return 'Medium';
  if (score <= 6) return 'Hard';
  if (score <= 8) return 'Very Hard';
  return 'Expert';
}

async function importBatch(batchNumber, batchData) {
  console.log(`Importing batch ${batchNumber}: ${batchData.length} words`);
  
  const mappedData = batchData.map(mapCSVToDatabase);
  
  // Insert in chunks of 100 to avoid overwhelming the database
  const chunkSize = 100;
  let inserted = 0;
  
  for (let i = 0; i < mappedData.length; i += chunkSize) {
    const chunk = mappedData.slice(i, i + chunkSize);
    
    const { data, error } = await supabase
      .from('spelling_words')
      .insert(chunk)
      .select('id');
    
    if (error) {
      console.error(`Error inserting batch ${batchNumber} chunk ${Math.floor(i/chunkSize) + 1}:`, error.message);
      throw error;
    }
    
    inserted += chunk.length;
    console.log(`  ✅ Inserted ${inserted}/${mappedData.length} words from batch ${batchNumber}`);
  }
  
  return inserted;
}

async function importAllBatches() {
  console.log('🚀 Starting import of all spelling bee batches...');
  
  const outputDir = path.join(__dirname, 'output');
  const batchFiles = fs.readdirSync(outputDir)
    .filter(file => file.match(/^batch_\d+_processed\.csv$/))
    .sort((a, b) => {
      const numA = parseInt(a.match(/batch_(\d+)_processed\.csv/)[1]);
      const numB = parseInt(b.match(/batch_(\d+)_processed\.csv/)[1]);
      return numA - numB;
    });
  
  console.log(`Found ${batchFiles.length} batch files to import`);
  
  let totalImported = 0;
  let batchesProcessed = 0;
  
  for (const file of batchFiles) {
    const batchNumber = file.match(/batch_(\d+)_processed\.csv/)[1];
    const filePath = path.join(outputDir, file);
    
    try {
      const batchData = await readCSVFile(filePath);
      
      if (batchData.length === 0) {
        console.log(`⚠️  Batch ${batchNumber} is empty, skipping`);
        continue;
      }
      
      const imported = await importBatch(batchNumber, batchData);
      totalImported += imported;
      batchesProcessed++;
      
      console.log(`✅ Completed batch ${batchNumber}: ${imported} words imported`);
      
      // Small delay to avoid overwhelming the database
      await new Promise(resolve => setTimeout(resolve, 100));
      
    } catch (error) {
      console.error(`❌ Failed to import batch ${batchNumber}:`, error.message);
      console.log('Continuing with next batch...');
    }
  }
  
  console.log('\n🎉 IMPORT COMPLETE!');
  console.log(`📊 Summary:`);
  console.log(`   - Batches processed: ${batchesProcessed}`);
  console.log(`   - Total words imported: ${totalImported}`);
  console.log(`   - Average words per batch: ${Math.round(totalImported / batchesProcessed)}`);
  
  // Verify final count in database
  const { count, error } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  if (!error) {
    console.log(`   - Database verification: ${count} words now in spelling_words table`);
  }
}

// Run the import
importAllBatches().catch(console.error);