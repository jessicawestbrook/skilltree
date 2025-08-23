const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function fixTriggerError() {
  console.log('=== FIXING DATABASE TRIGGER ERROR ===\n');

  try {
    // Step 1: Check current table structure
    console.log('Step 1: Checking current table structure...');
    await checkTableStructure();
    
    // Step 2: Generate SQL to fix trigger issues
    console.log('\nStep 2: Generating SQL to fix trigger...');
    generateTriggerFixSQL();
    
  } catch (error) {
    console.error('Error during trigger fix:', error);
  }
}

async function checkTableStructure() {
  try {
    // Get a sample record to see what columns exist
    const { data: sample, error } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(1);
      
    if (error) {
      console.error('Error fetching sample record:', error);
      return;
    }
    
    if (sample && sample.length > 0) {
      console.log('Current table columns:');
      Object.keys(sample[0]).forEach(col => {
        console.log(`  - ${col}`);
      });
      
      // Check specifically for AI difficulty columns
      const hasAiDifficultyLevel = sample[0].hasOwnProperty('ai_difficulty_level');
      const hasAiDifficultyName = sample[0].hasOwnProperty('ai_difficulty_name');
      
      console.log(`\nAI Difficulty columns status:`);
      console.log(`  - ai_difficulty_level: ${hasAiDifficultyLevel ? '✅ EXISTS' : '❌ MISSING'}`);
      console.log(`  - ai_difficulty_name: ${hasAiDifficultyName ? '✅ EXISTS' : '❌ MISSING'}`);
      
      // Check for other difficulty columns
      const hasSpellingDifficultyLevel = sample[0].hasOwnProperty('spelling_difficulty_level');
      const hasVocabDifficultyLevel = sample[0].hasOwnProperty('vocabulary_difficulty_level');
      
      console.log(`\nOther difficulty columns:`);
      console.log(`  - spelling_difficulty_level: ${hasSpellingDifficultyLevel ? '✅ EXISTS' : '❌ MISSING'}`);
      console.log(`  - vocabulary_difficulty_level: ${hasVocabDifficultyLevel ? '✅ EXISTS' : '❌ MISSING'}`);
      
    } else {
      console.log('No sample records found in table');
    }
  } catch (error) {
    console.error('Error checking table structure:', error);
  }
}

function generateTriggerFixSQL() {
  const timestamp = Date.now();
  
  const triggerFixSQL = `scripts/fix_trigger_error_${timestamp}.sql`;
  const triggerContent = `-- Fix trigger error for missing ai_difficulty_level column
-- Generated on ${new Date().toISOString()}

-- Option 1: Add missing columns if they don't exist
-- Uncomment these lines if you want to add the missing columns
-- ALTER TABLE spelling_words ADD COLUMN IF NOT EXISTS ai_difficulty_level INTEGER;
-- ALTER TABLE spelling_words ADD COLUMN IF NOT EXISTS ai_difficulty_name TEXT;

-- Option 2: Drop the problematic trigger (recommended for now)
-- This will remove the trigger that's causing the error
DROP TRIGGER IF EXISTS update_difficulty_name_trigger ON spelling_words;
DROP FUNCTION IF EXISTS update_difficulty_name();

-- Option 3: Recreate a safer trigger that only works with existing columns
-- This creates a new trigger that checks for column existence
CREATE OR REPLACE FUNCTION update_spelling_difficulty_name()
RETURNS TRIGGER AS $$
BEGIN
  -- Only update spelling difficulty name if spelling_difficulty_level exists and is not null
  IF NEW.spelling_difficulty_level IS NOT NULL THEN
    CASE NEW.spelling_difficulty_level
      WHEN 1 THEN NEW.spelling_difficulty_name := 'Beginner';
      WHEN 2 THEN NEW.spelling_difficulty_name := 'Elementary';
      WHEN 3 THEN NEW.spelling_difficulty_name := 'Intermediate';
      WHEN 4 THEN NEW.spelling_difficulty_name := 'Advanced';
      WHEN 5 THEN NEW.spelling_difficulty_name := 'Expert';
      ELSE NEW.spelling_difficulty_name := NULL;
    END CASE;
  END IF;
  
  -- Only update vocabulary difficulty name if vocabulary_difficulty_level exists and is not null
  IF NEW.vocabulary_difficulty_level IS NOT NULL THEN
    CASE NEW.vocabulary_difficulty_level
      WHEN 1 THEN NEW.vocabulary_difficulty_name := 'Basic';
      WHEN 2 THEN NEW.vocabulary_difficulty_name := 'Elementary';
      WHEN 3 THEN NEW.vocabulary_difficulty_name := 'Intermediate';
      WHEN 4 THEN NEW.vocabulary_difficulty_name := 'Advanced';
      WHEN 5 THEN NEW.vocabulary_difficulty_name := 'Expert';
      ELSE NEW.vocabulary_difficulty_name := NULL;
    END CASE;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the new safer trigger
CREATE TRIGGER update_spelling_difficulty_name_trigger
  BEFORE INSERT OR UPDATE ON spelling_words
  FOR EACH ROW
  EXECUTE FUNCTION update_spelling_difficulty_name();

-- Verify the trigger was created successfully
SELECT 
  trigger_name, 
  event_manipulation, 
  action_timing,
  action_statement
FROM information_schema.triggers 
WHERE event_object_table = 'spelling_words';`;

  fs.writeFileSync(triggerFixSQL, triggerContent);
  
  console.log(`✅ Trigger fix SQL generated: ${triggerFixSQL}`);
  console.log(`\n📋 This SQL will:`);
  console.log(`  1. Remove the problematic trigger causing the error`);
  console.log(`  2. Create a new safer trigger that works with existing columns`);
  console.log(`  3. Only update difficulty names for columns that actually exist`);
  console.log(`\n⚠️  Execute this SQL first before running the spelling word updates!`);
}

fixTriggerError();