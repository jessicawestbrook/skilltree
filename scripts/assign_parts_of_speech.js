import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

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

// Common word endings and their typical parts of speech
const suffixPatterns = {
  noun: [
    'tion', 'sion', 'ment', 'ness', 'ity', 'ance', 'ence', 
    'er', 'or', 'ist', 'ism', 'ship', 'hood', 'dom', 'age',
    'ure', 'ry', 'cy', 'ty', 'al', 'ice', 'itude'
  ],
  verb: [
    'ize', 'ise', 'ify', 'ate', 'en'
  ],
  adjective: [
    'able', 'ible', 'ful', 'less', 'ous', 'ious', 'eous', 
    'ive', 'ish', 'al', 'ic', 'ical', 'ant', 'ent', 'ary',
    'some', 'like', 'ly'
  ],
  adverb: [
    'ly', 'ward', 'wards', 'wise'
  ]
};

// Definition patterns that indicate parts of speech
const definitionPatterns = {
  noun: [
    /^(a |an |the )?(?:type|kind|form|person|place|thing|act|state|quality|instance|example|piece|part|member|group|collection|system|process|property|amount|measure|unit)/i,
    /^(a |an |the )?(?:one who|someone who|something that|somebody who)/i,
    /^(a |an |the )?(?:[A-Z][a-z]+)/,  // Capitalized words are often nouns
    /\b(?:animal|plant|object|device|tool|instrument|machine|structure|building|location|area|region|country|city|food|drink|material|substance)\b/i
  ],
  verb: [
    /^to (?!be\b)/i,  // Starts with "to" (infinitive)
    /^(?:do|does|did|doing|done)/i,
    /^(?:make|makes|making|made)/i,
    /^(?:have|has|having|had)/i,
    /^(?:be|am|is|are|was|were|being|been)/i,
    /^(?:become|becomes|becoming|became)/i,
    /^(?:act|acts|acting|acted)/i,
    /^(?:move|moves|moving|moved)/i,
    /^(?:cause|causes|causing|caused)/i,
    /\b(?:perform|execute|accomplish|achieve|create|produce|generate)\b/i
  ],
  adjective: [
    /^(?:of |relating to |pertaining to |characterized by |having |showing |displaying |marked by)/i,
    /^(?:able to |capable of |likely to |prone to |suitable for)/i,
    /^(?:full of |lacking |without |free from)/i,
    /^(?:more |most |very |extremely |quite |rather |somewhat)/i,
    /\b(?:quality|characteristic|trait|property|attribute|feature)\b.*\bof\b/i,
    /^(?:being |becoming |appearing |seeming |looking |feeling)/i
  ],
  adverb: [
    /^(?:in a |in an |with |without |by |through |via)/i,
    /\b(?:manner|way|fashion|style)\b/i,
    /^(?:how |when |where |why )/i
  ]
};

function inferPartOfSpeech(word, definition) {
  if (!definition) return null;
  
  const wordLower = word.toLowerCase();
  const defLower = definition.toLowerCase();
  
  // Check for plural nouns
  if (wordLower.endsWith('s') && !wordLower.endsWith('ss') && !wordLower.endsWith('us')) {
    if (defLower.includes('plural') || defLower.includes('more than one')) {
      return 'noun';
    }
  }
  
  // Check for -ed endings (often past tense verbs or adjectives)
  if (wordLower.endsWith('ed')) {
    if (defLower.includes('past tense') || defLower.includes('past participle')) {
      return 'verb';
    }
    // Could also be an adjective (e.g., "excited")
    if (defLower.match(/^(?:feeling |being |having been |characterized by)/i)) {
      return 'adjective';
    }
  }
  
  // Check for -ing endings
  if (wordLower.endsWith('ing')) {
    if (defLower.includes('present participle') || defLower.includes('continuous')) {
      return 'verb';
    }
    // Could be a gerund (noun)
    if (defLower.match(/^(the |a |an )?(?:act|action|process|practice|activity) of/i)) {
      return 'noun';
    }
  }
  
  // Check definition patterns
  for (const [pos, patterns] of Object.entries(definitionPatterns)) {
    for (const pattern of patterns) {
      if (pattern.test(definition)) {
        return pos;
      }
    }
  }
  
  // Check suffix patterns
  for (const [pos, suffixes] of Object.entries(suffixPatterns)) {
    for (const suffix of suffixes) {
      if (wordLower.endsWith(suffix) && wordLower.length > suffix.length + 2) {
        // Additional checks for more accuracy
        if (pos === 'adjective' && suffix === 'ly' && !defLower.includes('manner')) {
          continue; // 'ly' ending but not an adverb
        }
        return pos;
      }
    }
  }
  
  // Default fallback based on common patterns
  if (defLower.startsWith('a ') || defLower.startsWith('an ') || defLower.startsWith('the ')) {
    return 'noun';
  }
  
  if (defLower.startsWith('to ')) {
    return 'verb';
  }
  
  // If still uncertain, make an educated guess based on word structure
  if (wordLower.length <= 4) {
    // Short words are often basic nouns or verbs
    return Math.random() < 0.7 ? 'noun' : 'verb';
  }
  
  // Default to noun as it's the most common
  return 'noun';
}

async function assignPartsOfSpeech() {
  console.log('=== ASSIGNING PARTS OF SPEECH ===\n');
  
  // Fetch words missing parts of speech in batches
  let allWords = [];
  let offset = 0;
  const batchSize = 1000;
  
  while (true) {
    const { data: batch, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition')
      .or('part_of_speech.is.null,part_of_speech.eq.')
      .range(offset, offset + batchSize - 1);
    
    if (error) {
      console.error('Error fetching words:', error);
      break;
    }
    
    if (!batch || batch.length === 0) break;
    
    allWords = allWords.concat(batch);
    console.log(`Fetched ${allWords.length} words...`);
    
    if (batch.length < batchSize) break;
    offset += batchSize;
  }
  
  console.log(`\nTotal words to process: ${allWords.length}\n`);
  
  // Process each word
  const assignments = allWords.map(wordData => {
    const pos = inferPartOfSpeech(wordData.word, wordData.definition);
    return {
      id: wordData.id,
      word: wordData.word,
      part_of_speech: pos,
      definition_preview: wordData.definition ? 
        wordData.definition.substring(0, 50) + (wordData.definition.length > 50 ? '...' : '') : 
        null
    };
  });
  
  // Count distribution
  const distribution = {};
  assignments.forEach(a => {
    distribution[a.part_of_speech] = (distribution[a.part_of_speech] || 0) + 1;
  });
  
  console.log('--- Proposed Part of Speech Distribution ---');
  Object.entries(distribution)
    .sort(([,a], [,b]) => b - a)
    .forEach(([pos, count]) => {
      const percent = ((count / assignments.length) * 100).toFixed(1);
      console.log(`  ${pos}: ${count} words (${percent}%)`);
    });
  
  // Show samples
  console.log('\n--- Sample Assignments ---');
  const samples = assignments.slice(0, 20);
  samples.forEach(s => {
    console.log(`  ${s.word} → ${s.part_of_speech}`);
    if (s.definition_preview) {
      console.log(`    "${s.definition_preview}"`);
    }
  });
  
  // Save to file
  const outputPath = join(__dirname, 'parts_of_speech_assignments.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalWords: assignments.length,
    distribution: distribution,
    assignments: assignments
  }, null, 2));
  
  console.log(`\n✓ Saved assignments to: ${outputPath}`);
  console.log('\nReview the assignments before applying to database.');
  
  return assignments;
}

async function applyPartsOfSpeech() {
  console.log('=== APPLYING PARTS OF SPEECH ===\n');
  
  const assignmentsPath = join(__dirname, 'parts_of_speech_assignments.json');
  
  if (!fs.existsSync(assignmentsPath)) {
    console.log('Assignments file not found. Generating new assignments...\n');
    await assignPartsOfSpeech();
  }
  
  const data = JSON.parse(fs.readFileSync(assignmentsPath, 'utf8'));
  const assignments = data.assignments;
  
  console.log(`Applying parts of speech to ${assignments.length} words...\n`);
  
  // Process in batches
  const batchSize = 100;
  let successCount = 0;
  let errorCount = 0;
  
  for (let i = 0; i < assignments.length; i += batchSize) {
    const batch = assignments.slice(i, i + batchSize);
    const batchNumber = Math.floor(i / batchSize) + 1;
    const totalBatches = Math.ceil(assignments.length / batchSize);
    
    process.stdout.write(`Batch ${batchNumber}/${totalBatches}: `);
    
    const promises = batch.map(async (assignment) => {
      const { error } = await supabase
        .from('spelling_words')
        .update({ part_of_speech: assignment.part_of_speech })
        .eq('id', assignment.id);
      
      return !error;
    });
    
    const results = await Promise.all(promises);
    const batchSuccess = results.filter(r => r).length;
    const batchErrors = results.filter(r => !r).length;
    
    successCount += batchSuccess;
    errorCount += batchErrors;
    
    console.log(`✓ ${batchSuccess} updated, ${batchErrors} errors`);
    
    // Small delay between batches
    if (i + batchSize < assignments.length) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  console.log('\n--- Update Summary ---');
  console.log(`Successfully updated: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  
  // Verify
  const { count: stillMissing } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true })
    .or('part_of_speech.is.null,part_of_speech.eq.');
  
  const { count: totalCount } = await supabase
    .from('spelling_words')
    .select('*', { count: 'exact', head: true });
  
  console.log(`\nWords still missing part_of_speech: ${stillMissing}`);
  console.log(`Total words: ${totalCount}`);
  console.log(`Coverage: ${(((totalCount - stillMissing) / totalCount) * 100).toFixed(1)}%`);
  
  if (stillMissing === 0) {
    console.log('\n✅ All words now have parts of speech assigned!');
  }
}

// Run assignment or apply based on command line argument
const command = process.argv[2];

if (command === 'apply') {
  applyPartsOfSpeech().catch(console.error);
} else {
  assignPartsOfSpeech().catch(console.error);
}