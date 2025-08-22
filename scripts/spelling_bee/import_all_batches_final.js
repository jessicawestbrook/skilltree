// Import all processed spelling bee batches to database - FINAL VERSION
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

function safeParseInt(value) {
  if (!value || value.trim() === '') return null;
  const parsed = parseInt(value);
  return isNaN(parsed) ? null : parsed;
}

function safeParseFloat(value) {
  if (!value || value.trim() === '') return null;
  const parsed = parseFloat(value);
  return isNaN(parsed) ? null : parsed;
}

function mapCSVToDatabase(csvRow) {
  // Map CSV columns to database columns with proper handling of empty values
  return {
    word: csvRow.word || null,
    definition: csvRow.definition || null,
    example_sentence: csvRow.example_sentence || null,
    pronunciation_guide: csvRow.pronunciation_guide || null,
    etymology: csvRow.etymology || null,
    etymology_source: csvRow.etymology_source || null,
    memory_tips: csvRow.memory_tips || null,
    
    // Map difficulty scores (handle empty strings)
    ai_difficulty_level: safeParseInt(csvRow.ai_difficulty_level),
    phonetic_transparency_score: safeParseFloat(csvRow.phonetic_transparency_score),
    word_frequency_score: safeParseFloat(csvRow.word_frequency_score),
    morphology_score: safeParseFloat(csvRow.morphology_score),
    etymology_score: safeParseFloat(csvRow.etymology_score),
    
    // Source information - convert to arrays
    source_names: parseArrayField(csvRow.source_names),
    source_difficulties: parseArrayField(csvRow.source_difficulties),
    original_source: csvRow.original_source || 'Scripps National Spelling Bee',
    definition_source: csvRow.definition_source || 'Claude',
    source_access_date: csvRow.source_access_date || new Date().toISOString().split('T')[0],
    
    // Additional fields
    part_of_speech: csvRow.part_of_speech || null,
    alternate_spellings: csvRow.alternate_spellings || null,
    language_origin: csvRow.language_origin || null,
    frequency: safeParseFloat(csvRow.frequency),
    
    // Calculated fields
    difficulty_calculation_method: csvRow.difficulty_calculation_method || null,
    ai_difficulty_name: csvRow.ai_difficulty_name || null,
    difficulty_level: csvRow.difficulty_level || null,
    difficulty_name: csvRow.difficulty_name || null,
    
    // Timestamps
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
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
      // Show problematic data for debugging
      console.error('First record in chunk:', JSON.stringify(chunk[0], null, 2));
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
  let batchesFailed = 0;
  
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
      batchesFailed++;
      console.log('Continuing with next batch...');
    }
  }
  
  console.log('\n🎉 IMPORT COMPLETE!');
  console.log(`📊 Summary:`);
  console.log(`   - Batches processed successfully: ${batchesProcessed}`);
  console.log(`   - Batches failed: ${batchesFailed}`);
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
  } else {
    console.log(`   - Database verification failed: ${error.message}`);
  }
}

// Run the import
importAllBatches().catch(console.error);