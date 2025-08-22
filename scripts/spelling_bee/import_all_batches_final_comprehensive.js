// Import all processed spelling bee batches to database - FINAL COMPREHENSIVE VERSION
// Handles ALL CSV formats and edge cases
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
  if (name.includes('beginner') || name.includes('easy') || name === 'beginning') return 1;
  if (name.includes('elementary') || name.includes('medium')) return 2;
  if (name.includes('intermediate') || name.includes('hard')) return 3;
  if (name.includes('advanced') || name.includes('very hard')) return 4;
  if (name.includes('expert')) return 5;
  return 1;
}

function getDifficultyNameFromScore(score) {
  if (score <= 1) return 'Beginner';
  if (score <= 2) return 'Elementary';
  if (score <= 3) return 'Intermediate';
  if (score <= 4) return 'Advanced';
  return 'Expert';
}

function detectCSVFormat(csvRow) {
  // Format 1: Has columns like ai_difficulty_level, phonetic_transparency_score, etc.
  if (csvRow.hasOwnProperty('ai_difficulty_level') || csvRow.hasOwnProperty('phonetic_transparency_score')) {
    return 'format1';
  }
  // Format 2: Has columns like phonetic_score, frequency_score, etc.
  if (csvRow.hasOwnProperty('phonetic_score') || csvRow.hasOwnProperty('frequency_score')) {
    return 'format2';
  }
  // Format 3: Has columns like pronunciation_audio_url, source_url, etc.
  if (csvRow.hasOwnProperty('pronunciation_audio_url') || csvRow.hasOwnProperty('source_url')) {
    return 'format3';
  }
  return 'unknown';
}

function mapCSVToDatabase(csvRow, format) {
  // Skip error rows with combined words
  if (csvRow.combined_word_error === 'True' || csvRow.definition === 'ERROR: Combined word - should be separate words') {
    return null;
  }

  // Skip empty words
  if (!csvRow.word || csvRow.word.trim() === '') {
    return null;
  }

  let mappedData;
  
  if (format === 'format1') {
    // Original format mapping
    const aiDifficultyLevel = safeParseInt(csvRow.ai_difficulty_level, 2);
    const difficultyLevel = csvRow.difficulty_level ? 
      safeParseInt(csvRow.difficulty_level, 1) : 
      getDifficultyLevelFromName(csvRow.source_difficulty);
    const difficultyName = csvRow.difficulty_name || 
      getDifficultyNameFromScore(difficultyLevel);
    const aiDifficultyName = csvRow.ai_difficulty_name || 
      getDifficultyNameFromScore(aiDifficultyLevel);

    mappedData = {
      word: csvRow.word || null,
      definition: csvRow.definition || null,
      example_sentence: csvRow.example_sentence || `Please spell the word _____.`,
      source_difficulty: csvRow.source_difficulty || 'One Bee',
      
      difficulty_level: difficultyLevel,
      difficulty_name: difficultyName,
      ai_difficulty_level: aiDifficultyLevel,
      ai_difficulty_name: aiDifficultyName,
      
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
      
      source_names: parseArrayField(csvRow.source_names),
      source_difficulties: parseArrayField(csvRow.source_difficulties),
      frequency: safeParseInt(csvRow.frequency, 1),
      original_source: csvRow.original_source || 'Scripps National Spelling Bee',
      source_access_date: csvRow.source_access_date || '2025-08-19',
    };
  } else if (format === 'format2') {
    // Second format mapping
    const difficultyLevel = getDifficultyLevelFromName(csvRow.difficulty_level || 'Beginner');
    const difficultyName = csvRow.difficulty_level || 'Beginner';
    const aiDifficultyLevel = difficultyLevel;
    const aiDifficultyName = difficultyName;

    mappedData = {
      word: csvRow.word || null,
      definition: csvRow.definition || null,
      example_sentence: csvRow.example_sentence || `Please spell the word _____.`,
      source_difficulty: 'One Bee',
      
      difficulty_level: difficultyLevel,
      difficulty_name: difficultyName,
      ai_difficulty_level: aiDifficultyLevel,
      ai_difficulty_name: aiDifficultyName,
      
      phonetic_transparency_score: safeParseFloat(csvRow.phonetic_score, 50),
      word_frequency_score: safeParseFloat(csvRow.frequency_score, 50),
      morphology_score: safeParseFloat(csvRow.morphology_score, 50),
      etymology_score: safeParseFloat(csvRow.etymology_score, 50),
      
      difficulty_calculation_method: 'api_enriched',
      part_of_speech: null,
      pronunciation_guide: csvRow.pronunciation || null,
      etymology: csvRow.etymology || null,
      etymology_source: csvRow.etymology_source || 'Claude',
      memory_tips: csvRow.memory_tip || null,
      alternate_spellings: null,
      language_origin: null,
      definition_source: csvRow.definition_source || 'Claude',
      
      source_names: null,
      source_difficulties: null,
      frequency: 1,
      original_source: 'Scripps National Spelling Bee',
      source_access_date: '2025-08-19',
    };
  } else if (format === 'format3') {
    // Third format mapping
    const difficultyLevel = getDifficultyLevelFromName(csvRow.difficulty_level || 'Beginning');
    const difficultyName = csvRow.difficulty_level || 'Beginning';
    const aiDifficultyLevel = difficultyLevel;
    const aiDifficultyName = getDifficultyNameFromScore(difficultyLevel);

    mappedData = {
      word: csvRow.word || null,
      definition: csvRow.definition || null,
      example_sentence: csvRow.example_sentence || `Please spell the word _____.`,
      source_difficulty: csvRow.source_difficulty || 'One Bee',
      
      difficulty_level: difficultyLevel,
      difficulty_name: aiDifficultyName, // Use standardized name
      ai_difficulty_level: aiDifficultyLevel,
      ai_difficulty_name: aiDifficultyName,
      
      // Default scores for format3
      phonetic_transparency_score: 50,
      word_frequency_score: 50,
      morphology_score: 50,
      etymology_score: 50,
      
      difficulty_calculation_method: 'api_enriched',
      part_of_speech: null,
      pronunciation_guide: csvRow.pronunciation || null,
      etymology: csvRow.etymology || null,
      etymology_source: csvRow.etymology_source || 'Claude',
      memory_tips: csvRow.memory_tip || null,
      alternate_spellings: null,
      language_origin: null,
      definition_source: 'Claude',
      
      source_names: csvRow.source ? [csvRow.source] : null,
      source_difficulties: csvRow.source_difficulty ? [csvRow.source_difficulty] : null,
      frequency: 1,
      original_source: csvRow.source || 'Scripps National Spelling Bee',
      source_access_date: '2025-08-19',
    };
  } else {
    // Fallback for unknown format
    return null;
  }

  // Add timestamps
  mappedData.created_at = new Date().toISOString();
  mappedData.updated_at = new Date().toISOString();

  return mappedData;
}

async function importBatch(batchNumber, batchData) {
  console.log(`Importing batch ${batchNumber}: ${batchData.length} words`);
  
  if (batchData.length === 0) {
    console.log(`  ⚠️  Empty batch, skipping`);
    return 0;
  }

  // Detect CSV format from first row
  const format = detectCSVFormat(batchData[0]);
  console.log(`  📋 Detected format: ${format}`);
  
  const mappedData = batchData
    .map(row => mapCSVToDatabase(row, format))
    .filter(row => row !== null); // Remove invalid rows

  if (mappedData.length === 0) {
    console.log(`  ⚠️  No valid rows after filtering, skipping`);
    return 0;
  }

  console.log(`  📝 Processing ${mappedData.length} valid words`);
  
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
      console.error(`  ❌ Error inserting chunk ${Math.floor(i/chunkSize) + 1}:`, error.message);
      console.error('  Sample record:', JSON.stringify(chunk[0], null, 2));
      throw error;
    }
    
    inserted += chunk.length;
    console.log(`    ✅ Inserted ${inserted}/${mappedData.length} words`);
  }
  
  return inserted;
}

async function importAllBatches() {
  console.log('🚀 Starting COMPREHENSIVE import of all spelling bee batches...');
  
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
  const failedBatches = [];
  
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
      
      if (imported > 0) {
        batchesProcessed++;
        console.log(`✅ Completed batch ${batchNumber}: ${imported} words imported\n`);
      } else {
        console.log(`⚠️  Batch ${batchNumber}: No words imported (all filtered out)\n`);
      }
      
      // Small delay to avoid overwhelming the database
      await new Promise(resolve => setTimeout(resolve, 50));
      
    } catch (error) {
      console.error(`❌ Failed to import batch ${batchNumber}:`, error.message);
      batchesFailed++;
      failedBatches.push(batchNumber);
      console.log('Continuing with next batch...\n');
    }
  }
  
  console.log('\n🎉 COMPREHENSIVE IMPORT COMPLETE!');
  console.log(`📊 Summary:`);
  console.log(`   - Total batches found: ${batchFiles.length}`);
  console.log(`   - Batches with data imported: ${batchesProcessed}`);
  console.log(`   - Batches failed: ${batchesFailed}`);
  console.log(`   - Total words imported: ${totalImported}`);
  if (batchesProcessed > 0) {
    console.log(`   - Average words per successful batch: ${Math.round(totalImported / batchesProcessed)}`);
  }
  
  if (failedBatches.length > 0) {
    console.log(`   - Failed batches: ${failedBatches.join(', ')}`);
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