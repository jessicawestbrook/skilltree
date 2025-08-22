const { createClient } = require('@supabase/supabase-js');
const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Claude API configuration
const CLAUDE_API_KEY = process.env.ANTHROPIC_API_KEY;
const CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages';

async function callClaudeAPI(prompt) {
  try {
    const response = await axios.post(CLAUDE_API_URL, {
      model: 'claude-3-haiku-20240307',
      max_tokens: 500,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ]
    }, {
      headers: {
        'Authorization': `Bearer ${CLAUDE_API_KEY}`,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
      }
    });
    
    return response.data.content[0].text.trim();
  } catch (error) {
    console.error('Claude API error:', error.response?.data || error.message);
    return null;
  }
}

async function generateRespellingFromAPI(word) {
  const prompt = `Provide the pronunciation for the word "${word}" using phonetic respelling format (like "AY-bul" for "able").

Use capital letters for stressed syllables, hyphens to separate syllables, and familiar letter combinations:
- AY for long A sound (like "day")
- EE for long E sound (like "see") 
- EYE for long I sound (like "my")
- OH for long O sound (like "go")
- OO for long U sound (like "blue")
- ER for "er" sound
- TH for "th" sound
- SH for "sh" sound
- etc.

Just return the respelling pronunciation, nothing else.`;

  const response = await callClaudeAPI(prompt);
  return response;
}

async function generatePartOfSpeechFromAPI(word) {
  const prompt = `What is the part of speech for the word "${word}"?

Return only one of these options:
- noun
- verb
- adjective
- adverb
- preposition
- conjunction
- interjection
- pronoun

Just return the part of speech, nothing else.`;

  const response = await callClaudeAPI(prompt);
  return response?.toLowerCase().trim();
}

// IPA to Respelling conversion patterns
function convertIPAToRespelling(ipaString) {
  if (!ipaString || typeof ipaString !== 'string') return null;
  
  let respelling = ipaString
    // Remove IPA markers
    .replace(/[\/\[\]]/g, '')
    // Convert stress markers
    .replace(/ˈ/g, '') // Primary stress - will handle with caps
    .replace(/ˌ/g, '') // Secondary stress
    // Convert vowels
    .replace(/iː/g, 'EE')
    .replace(/ɪ/g, 'IH')
    .replace(/eɪ/g, 'AY')
    .replace(/ɛ/g, 'EH')
    .replace(/æ/g, 'A')
    .replace(/ɑː?/g, 'AH')
    .replace(/ɔː?/g, 'AW')
    .replace(/oʊ/g, 'OH')
    .replace(/ʊ/g, 'UH')
    .replace(/uː/g, 'OO')
    .replace(/ʌ/g, 'UH')
    .replace(/ə/g, 'uh')
    .replace(/ɜː?r?/g, 'ER')
    .replace(/ɪr/g, 'EER')
    .replace(/ɛr/g, 'AIR')
    .replace(/ɑr/g, 'AR')
    .replace(/ɔr/g, 'OR')
    .replace(/ʊr/g, 'OOR')
    // Convert consonants
    .replace(/θ/g, 'TH')
    .replace(/ð/g, 'TH')
    .replace(/ʃ/g, 'SH')
    .replace(/ʒ/g, 'ZH')
    .replace(/tʃ/g, 'CH')
    .replace(/dʒ/g, 'J')
    .replace(/ŋ/g, 'NG')
    .replace(/j/g, 'Y')
    .replace(/w/g, 'W')
    .replace(/r/g, 'R')
    .replace(/l/g, 'L')
    // Convert remaining single letters to uppercase if they're consonants at start of syllable
    .replace(/^([bcdfghjklmnpqrstvwxyz])/gi, (match) => match.toUpperCase())
    // Handle common patterns
    .replace(/aɪ/g, 'EYE')
    .replace(/aʊ/g, 'OW')
    .replace(/ɔɪ/g, 'OY')
    // Clean up
    .replace(/[ː]/g, '') // Remove length markers
    .replace(/\s+/g, '-') // Convert spaces to hyphens
    .replace(/-+/g, '-') // Remove multiple hyphens
    .replace(/^-|-$/g, ''); // Remove leading/trailing hyphens
  
  return respelling || null;
}

// Enhanced respelling generator with more words
function generateRespellingPronunciation(word) {
  const pronunciationMap = {
    // Previously defined words
    'tricenary': 'try-SEE-ner-ee',
    'triste': 'TREEST',
    'alberta': 'al-BER-tuh',
    'difficulty': 'DIF-ih-kul-tee',
    'alcarraza': 'al-kar-RAH-sah',
    'americana': 'uh-mer-ih-KAH-nuh',
    'amiably': 'AY-mee-uh-blee',
    'amid': 'uh-MID',
    'cathect': 'kuh-THEKT',
    'andean': 'an-DEE-un',
    'scrawled': 'SKRAWLD',
    'abstruse': 'ab-STROOS',
    'nephrolith': 'NEF-roh-lith',
    'abnegation': 'ab-nih-GAY-shun',
    'beguile': 'bih-GYL',
    
    // Common spelling bee words
    'philosophy': 'fih-LOS-uh-fee',
    'necessary': 'NES-uh-ser-ee',
    'zephyr': 'ZEF-er',
    'sulcus': 'SUL-kus',
    'affenpinscher': 'AF-en-pin-sher',
    'aggrandizement': 'uh-GRAN-diz-ment',
    'amphitheater': 'AM-fih-thee-uh-ter',
    'anthropomorphic': 'an-throh-poh-MOR-fik',
    'antidisestablishmentarianism': 'AN-tee-dis-ih-stab-lish-men-TAIR-ee-uh-niz-um',
    'ardipithecus': 'ar-dih-PITH-eh-kus',
    'aromatherapy': 'uh-roh-muh-THER-uh-pee',
    'authenticate': 'aw-THEN-tih-kayt',
    'bisbigliando': 'bis-big-lee-AN-doh',
    
    // Add more common words
    'abundance': 'uh-BUN-dans',
    'calamitous': 'kuh-LAM-ih-tus',
    'acquit': 'uh-KWIT',
    'capnometer': 'kap-NOM-eh-ter',
    'addled': 'AD-uld',
    'adjudicate': 'uh-JOO-dih-kayt',
    'caricature': 'KAIR-ih-kuh-choor',
    'advocatory': 'AD-voh-kuh-tor-ee',
    'aerobics': 'air-OH-biks',
    'aethalium': 'ee-THAY-lee-um',
    'affiche': 'uh-FEESH',
    'affiliate': 'uh-FIL-ee-ayt',
    'affluent': 'AF-loo-ent',
    'agrypnia': 'uh-GRIP-nee-uh',
    'ague': 'AY-gyoo'
  };
  
  return pronunciationMap[word.toLowerCase()] || null;
}

// Enhanced definition generator
function generateDefinition(word) {
  const definitionMap = {
    'tricenary': 'Relating to or consisting of thirty; occurring every thirty years.',
    'triste': 'Sad, melancholy, or sorrowful in mood or character.',
    'abnegation': 'The practice of renouncing or rejecting something; self-denial.',
    'beguile': 'To charm or enchant someone, often in a deceptive way.',
    'abstruse': 'Difficult to understand; obscure or esoteric.',
    'nephrolith': 'A kidney stone; a solid deposit formed in the kidneys.',
    'abundance': 'A very large quantity of something; plentifulness.',
    'calamitous': 'Involving or causing a catastrophe; disastrous.',
    'acquit': 'To free someone from a criminal charge by a verdict of not guilty.',
    'capnometer': 'A medical device that measures carbon dioxide concentration.',
    'addled': 'Confused and unable to think clearly; muddled.',
    'adjudicate': 'To make a formal judgment or decision about a problem or disputed matter.',
    'caricature': 'A picture, description, or imitation that exaggerates certain characteristics.',
    'advocatory': 'Supporting or arguing in favor of something.',
    'aerobics': 'Vigorous physical exercise designed to strengthen the heart and lungs.',
    'aethalium': 'A large, cushion-like structure containing spores in slime molds.',
    'affiche': 'A poster or public notice, especially one posted on a wall.',
    'affiliate': 'To officially attach or connect to an organization.',
    'affluent': 'Having a great deal of money; wealthy.',
    'agrypnia': 'Insomnia; inability to sleep.',
    'ague': 'Malaria or another illness involving fever and shivering.'
  };
  
  return definitionMap[word.toLowerCase()] || `Definition for ${word}`;
}

// Enhanced example sentence generator
function generateExampleSentence(word) {
  const exampleMap = {
    'tricenary': 'The _____ celebration marked thirty years of the institution.',
    'triste': 'The _____ melody filled the concert hall with melancholy.',
    'abnegation': 'His _____ of worldly pleasures surprised his friends.',
    'beguile': 'The storyteller could _____ audiences with her tales.',
    'abstruse': 'The professor\'s _____ theories were difficult to follow.',
    'nephrolith': 'The doctor identified a _____ on the patient\'s kidney scan.',
    'abundance': 'The garden produced an _____ of fresh vegetables.',
    'calamitous': 'The earthquake had _____ effects on the region.',
    'acquit': 'The jury voted to _____ the defendant of all charges.',
    'capnometer': 'The _____ showed normal carbon dioxide levels.',
    'addled': 'The _____ witness gave contradictory testimony.',
    'adjudicate': 'The judge will _____ the property dispute.',
    'caricature': 'The artist drew a _____ of the politician.',
    'advocatory': 'She wrote an _____ letter supporting the proposal.',
    'aerobics': 'The gym offers _____ classes every morning.',
    'aethalium': 'Scientists studied the _____ formation on the log.',
    'affiche': 'The _____ advertised the upcoming concert.',
    'affiliate': 'The local club will _____ with the national organization.',
    'affluent': 'The _____ neighborhood had expensive homes.',
    'agrypnia': 'Her _____ lasted for several sleepless nights.',
    'ague': 'The tropical _____ left him weak and feverish.'
  };
  
  return exampleMap[word.toLowerCase()] || `The word _____ is used in this context.`;
}

// Enhanced etymology generator
function generateEtymology(word) {
  const etymologyMap = {
    'tricenary': 'From Latin tricenarius, from triceni ("thirty each")',
    'triste': 'From Latin tristis meaning "sad" or "sorrowful"',
    'abnegation': 'From Latin abnegatio, from abnegare "to deny"',
    'beguile': 'From Middle English, from be- + guile "deceit"',
    'abstruse': 'From Latin abstrusus "hidden, concealed"',
    'nephrolith': 'From Greek nephros "kidney" + lithos "stone"',
    'abundance': 'From Latin abundantia, from abundare "to overflow"',
    'calamitous': 'From Latin calamitosus, from calamitas "disaster"',
    'acquit': 'From Old French acquiter, from Latin ad- "to" + quietus "quiet"',
    'capnometer': 'From Greek kapnos "smoke" + metron "measure"'
  };
  
  return etymologyMap[word.toLowerCase()] || `Etymology for ${word} not available`;
}

// Parse combined words from error messages (enhanced)
function parseCombinedWord(word, definition) {
  let components = [];
  
  if (definition.includes('[COMBINED WORD ERROR]') || definition.includes('ERROR:')) {
    // Look for patterns like "word1" + "word2" or "word1" (description) + "word2"
    const matches = definition.match(/"([^"]+)"/g);
    if (matches && matches.length >= 2) {
      components = matches.slice(0, 2).map(m => m.replace(/"/g, ''));
    }
  }
  
  // Enhanced known combinations
  if (components.length === 0) {
    const knownCombinations = {
      'tricenarytriste': ['tricenary', 'triste'],
      'albertadifficulty': ['alberta'],
      'alcarrazadifficulty': ['alcarraza'],
      'americanaamiably': ['americana', 'amiably'],
      'americanamonopolize': ['americana'],
      'amidcathect': ['amid', 'cathect'],
      'amishamnesty': ['amish'],
      'andeanscrawled': ['andean', 'scrawled'],
      'abstrusenephrolith': ['abstruse', 'nephrolith'],
      'abnegationbeguile': ['abnegation', 'beguile'],
      'abundancecalamitous': ['abundance', 'calamitous'],
      'acquitcapnometer': ['acquit', 'capnometer'],
      'addledifficulty': ['addled'],
      'adjudicatecaricature': ['adjudicate', 'caricature'],
      'advocatoryaerobics': ['advocatory', 'aerobics'],
      'aethaliumaffiche': ['aethalium', 'affiche'],
      'affiliateaffluent': ['affiliate', 'affluent'],
      'agrypniaague': ['agrypnia', 'ague'],
      'chastisechortle': ['chastise', 'chortle'],
      'chemistryquandary': ['chemistry', 'quandary'],
      'chupacabraacadians': ['chupacabra'],
      'chupacabradifficulty': ['chupacabra'],
      'amusedpouch': ['amused', 'pouch'],
      'anabolicjimberjawed': ['anabolic'],
      'analepsisanalgesia': ['analepsis', 'analgesia'],
      'angolacontours': ['angola', 'contours'],
      'angularconcomitant': ['angular', 'concomitant'],
      'animustrillium': ['animus', 'trillium']
    };
    
    components = knownCombinations[word.toLowerCase()] || [];
  }
  
  return components.filter(c => c && c !== 'difficulty' && c.length > 2); // Filter out invalid components
}

async function fixNullPronunciations() {
  try {
    console.log('Fixing null pronunciations...');
    
    // Get all words with null pronunciations
    const { data: nullWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .is('pronunciation_guide', null)
      .limit(100); // Process in batches
      
    if (error) {
      console.error('Error fetching null pronunciation words:', error);
      return;
    }
    
    console.log(`Found ${nullWords.length} words with null pronunciations`);
    
    let fixed = 0;
    
    for (const wordEntry of nullWords) {
      console.log(`  Processing: ${wordEntry.word}`);
      
      // Try predefined first, then Claude API
      let respelling = generateRespellingPronunciation(wordEntry.word);
      
      if (!respelling) {
        respelling = await generateRespellingFromAPI(wordEntry.word);
        // Rate limiting for API calls
        await new Promise(resolve => setTimeout(resolve, 1500));
      }
      
      if (respelling) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ pronunciation_guide: respelling })
          .eq('id', wordEntry.id);
          
        if (updateError) {
          console.error(`Failed to update ${wordEntry.word}:`, updateError);
        } else {
          console.log(`✓ ${wordEntry.word}: null → ${respelling}`);
          fixed++;
        }
      } else {
        console.log(`⚠ Could not generate pronunciation for: ${wordEntry.word}`);
      }
    }
    
    console.log(`Fixed ${fixed} null pronunciations`);
    
  } catch (error) {
    console.error('Null pronunciation fix failed:', error);
  }
}

async function fixNullPartOfSpeech() {
  try {
    console.log('Fixing null part of speech...');
    
    // Get all words with null part of speech
    const { data: nullPosWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, part_of_speech')
      .is('part_of_speech', null)
      .limit(100); // Process in batches
      
    if (error) {
      console.error('Error fetching null part of speech words:', error);
      return;
    }
    
    console.log(`Found ${nullPosWords.length} words with null part of speech`);
    
    let fixed = 0;
    
    for (const wordEntry of nullPosWords) {
      console.log(`  Processing: ${wordEntry.word}`);
      
      const partOfSpeech = await generatePartOfSpeechFromAPI(wordEntry.word);
      // Rate limiting for API calls
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      if (partOfSpeech && ['noun', 'verb', 'adjective', 'adverb', 'preposition', 'conjunction', 'interjection', 'pronoun'].includes(partOfSpeech)) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ part_of_speech: partOfSpeech })
          .eq('id', wordEntry.id);
          
        if (updateError) {
          console.error(`Failed to update ${wordEntry.word}:`, updateError);
        } else {
          console.log(`✓ ${wordEntry.word}: null → ${partOfSpeech}`);
          fixed++;
        }
      } else {
        console.log(`⚠ Could not generate part of speech for: ${wordEntry.word} (got: ${partOfSpeech})`);
      }
    }
    
    console.log(`Fixed ${fixed} null part of speech entries`);
    
  } catch (error) {
    console.error('Null part of speech fix failed:', error);
  }
}

async function convertAllIPAToRespelling() {
  try {
    console.log('Converting IPA pronunciations to respelling format...');
    
    // Get all words with IPA pronunciations (containing forward slashes or IPA symbols)
    const { data: ipaWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, pronunciation_guide')
      .not('pronunciation_guide', 'is', null)
      .or('pronunciation_guide.like.%/%,pronunciation_guide.like.%ˈ%,pronunciation_guide.like.%ɪ%,pronunciation_guide.like.%ə%,pronunciation_guide.like.%ɑ%')
      .limit(100); // Process in batches
      
    if (error) {
      console.error('Error fetching IPA words:', error);
      return;
    }
    
    console.log(`Found ${ipaWords.length} words with IPA pronunciations to convert`);
    
    let converted = 0;
    
    for (const wordEntry of ipaWords) {
      console.log(`  Processing: ${wordEntry.word}`);
      
      let respelling = convertIPAToRespelling(wordEntry.pronunciation_guide) || 
                      generateRespellingPronunciation(wordEntry.word);
      
      // If conversion failed, use Claude API
      if (!respelling || respelling === wordEntry.pronunciation_guide) {
        respelling = await generateRespellingFromAPI(wordEntry.word);
        // Rate limiting for API calls
        await new Promise(resolve => setTimeout(resolve, 1500));
      }
      
      if (respelling && respelling !== wordEntry.pronunciation_guide) {
        const { error: updateError } = await supabase
          .from('spelling_words')
          .update({ pronunciation_guide: respelling })
          .eq('id', wordEntry.id);
          
        if (updateError) {
          console.error(`Failed to update ${wordEntry.word}:`, updateError);
        } else {
          console.log(`✓ ${wordEntry.word}: ${wordEntry.pronunciation_guide} → ${respelling}`);
          converted++;
        }
      }
    }
    
    console.log(`Converted ${converted} pronunciations from IPA to respelling`);
    
  } catch (error) {
    console.error('IPA conversion failed:', error);
  }
}

async function processCombinedWords() {
  try {
    console.log('Finding all combined words with errors...');
    
    // Get all words with error markers
    const { data: errorWords, error } = await supabase
      .from('spelling_words')
      .select('id, word, definition, source_difficulty, difficulty_level, difficulty_name, original_source, source_access_date')
      .or('definition.ilike.%[COMBINED WORD ERROR]%,definition.ilike.%ERROR:%,definition.ilike.%incorrectly joined%')
      .order('word')
      .limit(50); // Process in smaller batches for stability
      
    if (error) {
      console.error('Error fetching words:', error);
      return;
    }
    
    console.log(`Found ${errorWords.length} combined words to process in this batch`);
    
    let processedCount = 0;
    let successCount = 0;
    
    for (const wordEntry of errorWords) {
      processedCount++;
      console.log(`\n[${processedCount}/${errorWords.length}] Processing: ${wordEntry.word}`);
      
      // Parse the combined word
      const components = parseCombinedWord(wordEntry.word, wordEntry.definition);
      
      if (components.length === 0) {
        console.log(`  ⚠ Could not parse components for: ${wordEntry.word}`);
        continue;
      }
      
      console.log(`  → Separating into: ${components.join(', ')}`);
      
      // Delete the combined word
      const { error: deleteError } = await supabase
        .from('spelling_words')
        .delete()
        .eq('id', wordEntry.id);
        
      if (deleteError) {
        console.error(`  ✗ Failed to delete ${wordEntry.word}:`, deleteError);
        continue;
      }
      
      // Create entries for each component
      for (const component of components) {
        if (!component || component.length < 3) continue; // Skip very short words
        
        // Check if component already exists
        const { data: existing } = await supabase
          .from('spelling_words')
          .select('word')
          .eq('word', component)
          .single();
          
        if (existing) {
          console.log(`    ⚠ "${component}" already exists, skipping...`);
          continue;
        }
        
        // Create new entry
        const newEntry = {
          word: component,
          definition: generateDefinition(component),
          example_sentence: generateExampleSentence(component),
          part_of_speech: 'noun', // Default
          pronunciation_guide: generateRespellingPronunciation(component),
          etymology: generateEtymology(component),
          etymology_source: 'Claude',
          definition_source: 'Claude',
          memory_tips: `Remember the spelling of ${component}`,
          source_difficulty: wordEntry.source_difficulty,
          difficulty_level: wordEntry.difficulty_level || 2,
          difficulty_name: wordEntry.difficulty_name || 'Elementary',
          original_source: wordEntry.original_source,
          source_access_date: wordEntry.source_access_date,
          frequency: 1,
          phonetic_transparency_score: 50,
          word_frequency_score: 50,
          morphology_score: 50,
          etymology_score: 50,
          difficulty_calculation_method: 'manual_separation'
        };
        
        const { error: insertError } = await supabase
          .from('spelling_words')
          .insert(newEntry);
          
        if (insertError) {
          console.error(`    ✗ Failed to insert ${component}:`, insertError);
        } else {
          console.log(`    ✓ Created: ${component}`);
        }
      }
      
      successCount++;
      
      // Rate limiting
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    console.log(`\n✓ Batch processing complete!`);
    console.log(`Total processed: ${processedCount}`);
    console.log(`Successfully handled: ${successCount}`);
    
  } catch (error) {
    console.error('Process failed:', error);
  }
}

async function main() {
  if (!CLAUDE_API_KEY) {
    console.error('ANTHROPIC_API_KEY not found in environment variables');
    return;
  }
  
  console.log('Starting combined word cleanup and pronunciation fixing...');
  
  const choice = process.argv[2] || 'all';
  
  switch(choice) {
    case 'combined':
      await processCombinedWords();
      break;
    case 'ipa':
      await convertAllIPAToRespelling();
      break;
    case 'null-pronunciation':
      await fixNullPronunciations();
      break;
    case 'null-pos':
      await fixNullPartOfSpeech();
      break;
    case 'all':
    default:
      await processCombinedWords();
      await convertAllIPAToRespelling();
      await fixNullPronunciations();
      await fixNullPartOfSpeech();
      break;
  }
  
  // Final verification
  console.log('\n=== Final Verification ===');
  
  const { data: remainingErrors, error: verifyError } = await supabase
    .from('spelling_words')
    .select('word', { count: 'exact' })
    .or('definition.ilike.%[COMBINED WORD ERROR]%,definition.ilike.%ERROR:%');
    
  if (!verifyError) {
    console.log(`Remaining combined word errors: ${remainingErrors.length}`);
  }
  
  const { data: remainingIPA, error: ipaError } = await supabase
    .from('spelling_words')
    .select('word', { count: 'exact' })
    .like('pronunciation_guide', '%/%');
    
  if (!ipaError) {
    console.log(`Remaining IPA pronunciations: ${remainingIPA.length}`);
  }
  
  const { data: nullPronunciations, error: nullPronError } = await supabase
    .from('spelling_words')
    .select('word', { count: 'exact' })
    .is('pronunciation_guide', null);
    
  if (!nullPronError) {
    console.log(`Remaining null pronunciations: ${nullPronunciations.length}`);
  }
  
  const { data: nullPartOfSpeech, error: nullPosError } = await supabase
    .from('spelling_words')
    .select('word', { count: 'exact' })
    .is('part_of_speech', null);
    
  if (!nullPosError) {
    console.log(`Remaining null part of speech: ${nullPartOfSpeech.length}`);
  }
  
  console.log('\n✓ Process completed!');
}

main();