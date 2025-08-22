// Import all processed spelling bee batches to database - SERVICE ROLE VERSION
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Load environment variables
require('dotenv').config({ path: '../../.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  console.error('Missing Supabase environment variables');
  console.error('URL:', !!supabaseUrl);
  console.error('Service Key:', !!supabaseServiceKey);
  process.exit(1);
}

// Use service role key to bypass RLS
const supabase = createClient(supabaseUrl, supabaseServiceKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: false
  }
});

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

function safeParseInt(value, defaultValue = 1) {
  if (!value || value.trim() === '') return defaultValue;
  const parsed = parseInt(value);
  return isNaN(parsed) ? defaultValue : parsed;
}

function safeParseFloat(value, defaultValue = 50) {
  if (!value || value.trim() === '') return defaultValue;
  const parsed = parseFloat(value);
  if (isNaN(parsed)) return defaultValue;
  // Convert decimals like 2.3 to integers like 23 (multiply by 10 if < 10)
  return parsed < 10 ? Math.round(parsed * 10) : Math.round(parsed);
}

function getDifficultyLevelFromName(difficultyName) {
  if (!difficultyName) return 1;
  const name = difficultyName.toLowerCase();
  if (name.includes('beginner') || name.includes('easy')) return 1;
  if (name.includes('elementary') || name.includes('medium')) return 2;
  if (name.includes('intermediate') || name.includes('hard')) return 3;
  if (name.includes('advanced') || name.includes('very hard')) return 4;
  if (name.includes('expert')) return 5;
  return 1;
}

function getDifficultyNameFromScore(score) {
  if (score <= 2) return 'Beginner';
  if (score <= 4) return 'Elementary';
  if (score <= 6) return 'Intermediate';
  if (score <= 8) return 'Advanced';
  return 'Expert';
}

function mapCSVToDatabase(csvRow) {
  // Calculate difficulty level and name to match existing data
  const aiDifficultyLevel = safeParseInt(csvRow.ai_difficulty_level, 2);
  const difficultyLevel = csvRow.difficulty_level ? 
    safeParseInt(csvRow.difficulty_level, 1) : 
    getDifficultyLevelFromName(csvRow.source_difficulty);
  const difficultyName = csvRow.difficulty_name || 
    getDifficultyNameFromScore(difficultyLevel);
  const aiDifficultyName = csvRow.ai_difficulty_name || 
    getDifficultyNameFromScore(aiDifficultyLevel);

  return {
    word: csvRow.word || null,
    definition: csvRow.definition || null,
    example_sentence: csvRow.example_sentence || null,
    source_difficulty: csvRow.source_difficulty || 'One Bee',
    
    // Ensure these match existing integer format
    difficulty_level: difficultyLevel,
    difficulty_name: difficultyName,
    ai_difficulty_level: aiDifficultyLevel,
    ai_difficulty_name: aiDifficultyName,
    
    // Convert decimal scores to integers like existing data
    phonetic_transparency_score: safeParseFloat(csvRow.phonetic_transparency_score, 50),
    word_frequency_score: safeParseFloat(csvRow.word_frequency_score, 50),
    morphology_score: safeParseFloat(csvRow.morphology_score, 50),
    etymology_score: safeParseFloat(csvRow.etymology_score, 50),
    
    difficulty_calculation_method: csvRow.difficulty_calculation_method || 'api_enriched',
    part_of_speech: csvRow.part_of_speech || null,
    pronunciation_guide: csvRow.pronunciation_guide || null,
    etymology: csvRow.etymology || null,
    etymology_source: csvRow.etymology_source || 'Claude',
    memory_tips: csvRow.memory_tips || null,
    alternate_spellings: csvRow.alternate_spellings || null,
    language_origin: csvRow.language_origin || null,
    definition_source: csvRow.definition_source || 'Claude',
    
    // Source information - convert to arrays
    source_names: parseArrayField(csvRow.source_names),
    source_difficulties: parseArrayField(csvRow.source_difficulties),
    frequency: safeParseInt(csvRow.frequency, 1),
    original_source: csvRow.original_source || 'Scripps National Spelling Bee',
    source_access_date: csvRow.source_access_date || '2025-08-19',
    
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
      console.error('First record in chunk:', JSON.stringify(chunk[0], null, 2));
      throw error;
    }
    
    inserted += chunk.length;
    console.log(`  ✅ Inserted ${inserted}/${mappedData.length} words from batch ${batchNumber}`);
  }
  
  return inserted;
}

async function importAllBatches() {
  console.log('🚀 Starting import of all spelling bee batches with SERVICE ROLE...');
  
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
      await new Promise(resolve => setTimeout(resolve, 100));
      
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