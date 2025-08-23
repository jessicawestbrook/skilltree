const { createClient } = require('@supabase/supabase-js');
const axios = require('axios');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Words that need complete content population
const wordsToPopulate = [
  {
    "id": "001d1bc4-2432-454e-a158-4497661f1c49",
    "word": "fortune",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0061052d-f18f-4007-855c-42b10187acc7",
    "word": "drift",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "007a3672-f051-47f7-958f-c2e61e1efa8a",
    "word": "wring",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "00c77c14-cb41-4fc2-b4d9-0adb3ea0b4ec",
    "word": "constantbalm",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "00feb96b-2b9a-4ce4-bad4-1211167777cf",
    "word": "evildoer",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "01391acc-b315-46ac-b712-65bdba7967c7",
    "word": "exoneration",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "01447fed-2d06-4807-b3de-8742addee858",
    "word": "documentary",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0149f83b-1bcb-4bfa-8207-b4cc396d87f3",
    "word": "eminent",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0170d59d-9405-4f3c-bb67-b279b25aa547",
    "word": "wolfsbane",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0174496b-9f8a-474f-9744-5d78ea16c5bf",
    "word": "propinquityepidermis",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0193d7a2-e2a4-45ab-8767-d281d4227101",
    "word": "yonder",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0199dec5-dc57-4bb1-9c90-66178ecebd24",
    "word": "blockheap",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "019f272a-96d8-472b-ad95-518add9ea05a",
    "word": "wraith",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "01fab887-6818-47e1-8421-5585d1c3ed63",
    "word": "wrath",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0206cfa8-182f-44fa-8f5f-447cbf107f2d",
    "word": "dotted",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0209e8c3-c300-414d-b852-680e31a84fd4",
    "word": "dorking",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "02141779-6f72-4ec1-9241-130850406e6a",
    "word": "shar-pei",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "02cee441-4ac0-43a7-b14e-5a79e3d7d75e",
    "word": "accordaturacavalletti",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "02f24266-c3cf-4692-ab6d-0521e5658632",
    "word": "divot",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "036ad736-d2c2-4354-a847-2bd9b79de765",
    "word": "klutzenvoy",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "03e58ea9-03ef-4c18-b498-1ffd47248840",
    "word": "uvulaenumerated",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "03f81761-34e3-4572-a0ba-6443d48ea82c",
    "word": "polo",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "04101dbf-96f6-4a77-a235-c3674ce0100f",
    "word": "effervescent",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "045dca0a-d13b-4f3b-b02b-ab534d7a09c8",
    "word": "folate",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "05206c78-23f3-4bf7-8cc1-7913c225e087",
    "word": "abstrusenephrolith",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0556a7df-a765-4bcc-8a7d-ecba9080bbfe",
    "word": "duress",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "057b397d-ccf1-4775-9d8b-7a63eb54aac4",
    "word": "drooped",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "057f4ab7-353d-4a45-9251-d64830a89b61",
    "word": "drum",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "059f3481-f681-4b23-85f6-da122d147f24",
    "word": "amuse-gueule",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "05a466c7-2d63-419e-9368-ac7fe4788895",
    "word": "wombat",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0708e0d1-6b24-40c2-a7bd-8348fa6e4d76",
    "word": "foible",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "071b9a0e-b254-4c6c-9fdd-54d3e41ca8d3",
    "word": "floruitbunyanesque",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "07212aa9-518b-4be3-9d08-fcedf4d4566a",
    "word": "kerneltawny",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "07253238-38f2-4e5e-97b7-7241954917b8",
    "word": "dreikanter",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0737a145-6593-457f-ba7f-ac55cdeea3ad",
    "word": "tic",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "07c92592-e4ee-4914-b648-174b53d08ed9",
    "word": "distraught",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "07d5fc39-1381-4162-82f7-e8a0331ce16a",
    "word": "laterigradehyssop",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "08ca1bba-43fd-4668-9514-b5f12767ce98",
    "word": "prodigiousprofligacy",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "08d7dad8-3fd9-4f88-b54d-6743dd77cf06",
    "word": "zygotenoun",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "08f58980-ee05-42a6-968f-57e97e007a1c",
    "word": "diversion",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "08fcaa96-d10e-4b7b-8abb-166d04fef5d3",
    "word": "worse",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "08fcea26-1178-4f02-9a3e-375d6de9f19d",
    "word": "diverge",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0978882d-536d-4186-90f6-a4d365606c1e",
    "word": "chi",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "09b31628-1e39-4d81-8476-35b5f475fee3",
    "word": "consecrateadjective",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "09dff980-3794-4c16-9766-483c2acde91c",
    "word": "effluxfrugivore",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "09e2e201-2fff-403a-9c27-6ab1b037b3d6",
    "word": "dutifully",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "09efc186-e64f-40ac-8699-34d7ffc7e9fd",
    "word": "lanternmince",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0a24bfdb-2fd6-4be7-b824-f64f5ff00144",
    "word": "tug",
    "source_difficulty": "One Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0a2970d9-ae94-4eb1-a672-e42e8c32f7f5",
    "word": "mooc",
    "source_difficulty": "Three Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  },
  {
    "id": "0a527385-8bea-43bf-907b-51e141d3d7a5",
    "word": "dilapidated",
    "source_difficulty": "Two Bee",
    "missing_definition": true,
    "missing_example_sentence": true,
    "missing_pronunciation": true,
    "missing_etymology": true
  }
];

let processedCount = 0;
let successCount = 0;
let failedWords = [];

async function populateWordContent() {
  console.log(`=== POPULATING CONTENT FOR ${wordsToPopulate.length} WORDS ===\n`);
  
  for (const wordData of wordsToPopulate) {
    try {
      console.log(`Processing: "${wordData.word}" (${processedCount + 1}/${wordsToPopulate.length})`);
      
      // Get definition and pronunciation from Dictionary API
      const dictionaryData = await fetchDictionaryData(wordData.word);
      
      // Generate example sentence (you'll need Claude API key for this)
      const exampleSentence = generateExampleSentence(wordData.word, dictionaryData?.definition);
      
      // Extract etymology if available
      const etymology = dictionaryData?.etymology || '';
      
      // Update database
      const { error } = await supabase
        .from('spelling_words')
        .update({
          definition: dictionaryData?.definition || '',
          example_sentence: exampleSentence,
          pronunciation_guide: dictionaryData?.pronunciation || '',
          etymology: etymology,
          definition_source: dictionaryData?.definition ? 'Dictionary API' : '',
          etymology_source: dictionaryData?.etymology ? 'Dictionary API' : ''
        })
        .eq('id', wordData.id);
      
      if (error) {
        console.log(`  ❌ Failed to update database: ${error.message}`);
        failedWords.push({ word: wordData.word, error: error.message });
      } else {
        console.log(`  ✅ Successfully updated`);
        successCount++;
      }
      
      processedCount++;
      
      // Rate limiting - wait 1 second between requests
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Save progress every 10 words
      if (processedCount % 10 === 0) {
        saveProgress();
      }
      
    } catch (error) {
      console.log(`  ❌ Error processing "${wordData.word}": ${error.message}`);
      failedWords.push({ word: wordData.word, error: error.message });
      processedCount++;
    }
  }
  
  // Final summary
  console.log(`\n📊 COMPLETION SUMMARY:`);
  console.log(`  Processed: ${processedCount}/${wordsToPopulate.length}`);
  console.log(`  Successful: ${successCount}`);
  console.log(`  Failed: ${failedWords.length}`);
  
  if (failedWords.length > 0) {
    const failedFile = `content_population_failed_${Date.now()}.json`;
    fs.writeFileSync(failedFile, JSON.stringify(failedWords, null, 2));
    console.log(`  ❌ Failed words saved to: ${failedFile}`);
  }
}

async function fetchDictionaryData(word) {
  try {
    const response = await axios.get(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
    const entry = response.data[0];
    
    const definition = entry.meanings[0]?.definitions[0]?.definition || '';
    const pronunciation = entry.phonetics?.find(p => p.text)?.text || '';
    const etymology = entry.origin || '';
    
    return { definition, pronunciation, etymology };
  } catch (error) {
    console.log(`    Dictionary API failed for "${word}": ${error.message}`);
    return null;
  }
}

function generateExampleSentence(word, definition) {
  // Simple example sentence generation - replace with Claude API call if available
  if (definition && definition.length > 10) {
    return `The word _____ can be understood from its definition.`;
  }
  return `The spelling of _____ requires careful attention.`;
}

function saveProgress() {
  const progress = {
    processed: processedCount,
    successful: successCount,
    failed: failedWords.length,
    timestamp: new Date().toISOString()
  };
  
  fs.writeFileSync(`content_population_progress_${Date.now()}.json`, JSON.stringify(progress, null, 2));
}

// Run the population
populateWordContent().catch(console.error);