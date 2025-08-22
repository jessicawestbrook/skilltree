// Import all processed spelling bee batches to database - FIXED VERSION
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

function parseArrayField(value) {
  if (!value || value.trim() === '') return null;
  // Split by semicolon and clean each item
  return value.split(';').map(item => item.trim()).filter(item => item !== '');
}

function mapCSVToDatabase(csvRow) {
  // Map CSV columns to database columns with proper array handling
  return {
    word: csvRow.word,
    definition: csvRow.definition,
    example_sentence: csvRow.example_sentence,
    pronunciation_guide: csvRow.pronunciation_guide,
    etymology: csvRow.etymology,
    etymology_source: csvRow.etymology_source,
    memory_tips: csvRow.memory_tips,
    
    // Map difficulty scores
    ai_difficulty_level: parseInt(csvRow.ai_difficulty_level) || 5,
    phonetic_transparency_score: parseFloat(csvRow.phonetic_transparency_score) || 5,
    word_frequency_score: parseFloat(csvRow.word_frequency_score) || 5,
    morphology_score: parseFloat(csvRow.morphology_score) || 5,
    etymology_score: parseFloat(csvRow.etymology_score) || 5,
    
    // Source information - convert to arrays
    source_names: parseArrayField(csvRow.source_names),
    source_difficulties: parseArrayField(csvRow.source_difficulties),
    original_source: csvRow.original_source || 'Scripps National Spelling Bee',
    definition_source: csvRow.definition_source || 'Claude',
    source_access_date: csvRow.source_access_date || new Date().toISOString(),
    
    // Additional fields
    part_of_speech: csvRow.part_of_speech,
    alternate_spellings: csvRow.alternate_spellings,
    language_origin: csvRow.language_origin,
    frequency: parseFloat(csvRow.frequency) || null,
    
    // Calculated fields
    difficulty_calculation_method: csvRow.difficulty_calculation_method || '4-factor scoring system',
    ai_difficulty_name: csvRow.ai_difficulty_name || getDifficultyName(parseInt(csvRow.ai_difficulty_level) || 5),
    difficulty_level: csvRow.difficulty_level,
    difficulty_name: csvRow.difficulty_name,
    
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
  
  // Insert in chunks of 50 to avoid overwhelming the database
  const chunkSize = 50;
  let inserted = 0;
  
  for (let i = 0; i < mappedData.length; i += chunkSize) {
    const chunk = mappedData.slice(i, i + chunkSize);
    
    // Use upsert to handle duplicates gracefully
    const { data, error } = await supabase
      .from('spelling_words')
      .upsert(chunk, { 
        onConflict: 'word',
        ignoreDuplicates: false 
      })
      .select('id');
    
    if (error) {
      console.error(`Error inserting batch ${batchNumber} chunk ${Math.floor(i/chunkSize) + 1}:`, error.message);
      console.error('Sample data causing error:', JSON.stringify(chunk[0], null, 2));
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
      await new Promise(resolve => setTimeout(resolve, 200));
      
    } catch (error) {
      console.error(`❌ Failed to import batch ${batchNumber}:`, error.message);
      console.log('Continuing with next batch...');
    }
  }
  
  console.log('\n🎉 IMPORT COMPLETE!');
  console.log(`📊 Summary:`);
  console.log(`   - Batches processed: ${batchesProcessed}`);
  console.log(`   - Total words imported: ${totalImported}`);
  if (batchesProcessed > 0) {
    console.log(`   - Average words per batch: ${Math.round(totalImported / batchesProcessed)}`);
  }
  
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