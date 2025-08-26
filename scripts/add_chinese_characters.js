#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

// Common Chinese characters with comprehensive data
// These are the most frequent characters that make up a large percentage of written Chinese
const chineseCharacters = [
  // Basic characters - Level 1 (Most common)
  { char: '的', pinyin: 'de', translation: 'of, possessive particle', meaning: 'indicates possession, like apostrophe-s', frequency: 7.5 },
  { char: '一', pinyin: 'yī', translation: 'one', meaning: 'the number one, first', frequency: 7.2 },
  { char: '是', pinyin: 'shì', translation: 'to be, is', meaning: 'verb to be (am/is/are)', frequency: 7.0 },
  { char: '不', pinyin: 'bù', translation: 'not', meaning: 'negation word', frequency: 6.8 },
  { char: '了', pinyin: 'le', translation: 'completed action marker', meaning: 'indicates completion or change', frequency: 6.7 },
  { char: '在', pinyin: 'zài', translation: 'at, in', meaning: 'indicates location or ongoing action', frequency: 6.5 },
  { char: '人', pinyin: 'rén', translation: 'person, people', meaning: 'human being', frequency: 6.4 },
  { char: '有', pinyin: 'yǒu', translation: 'to have', meaning: 'possession, existence', frequency: 6.3 },
  { char: '我', pinyin: 'wǒ', translation: 'I, me', meaning: 'first person pronoun', frequency: 6.2 },
  { char: '他', pinyin: 'tā', translation: 'he, him', meaning: 'third person masculine', frequency: 6.0 },
  
  // Basic characters - Level 2
  { char: '这', pinyin: 'zhè', translation: 'this', meaning: 'demonstrative pronoun', frequency: 5.9 },
  { char: '个', pinyin: 'gè', translation: 'individual, measure word', meaning: 'general classifier', frequency: 5.8 },
  { char: '们', pinyin: 'men', translation: 'plural marker', meaning: 'makes pronouns plural', frequency: 5.7 },
  { char: '中', pinyin: 'zhōng', translation: 'middle, China', meaning: 'center, Chinese', frequency: 5.6 },
  { char: '来', pinyin: 'lái', translation: 'to come', meaning: 'movement towards', frequency: 5.5 },
  { char: '上', pinyin: 'shàng', translation: 'up, on', meaning: 'above, previous', frequency: 5.4 },
  { char: '大', pinyin: 'dà', translation: 'big', meaning: 'large, great', frequency: 5.3 },
  { char: '为', pinyin: 'wèi', translation: 'for, to be', meaning: 'purpose, because of', frequency: 5.2 },
  { char: '和', pinyin: 'hé', translation: 'and', meaning: 'conjunction', frequency: 5.1 },
  { char: '国', pinyin: 'guó', translation: 'country', meaning: 'nation, state', frequency: 5.0 },
  
  // Elementary characters - Level 3
  { char: '地', pinyin: 'dì', translation: 'earth, ground', meaning: 'land, adverb marker', frequency: 4.9 },
  { char: '到', pinyin: 'dào', translation: 'to arrive', meaning: 'reach, until', frequency: 4.8 },
  { char: '以', pinyin: 'yǐ', translation: 'with, by', meaning: 'using, according to', frequency: 4.7 },
  { char: '说', pinyin: 'shuō', translation: 'to say', meaning: 'speak, explain', frequency: 4.6 },
  { char: '时', pinyin: 'shí', translation: 'time', meaning: 'hour, period', frequency: 4.5 },
  { char: '要', pinyin: 'yào', translation: 'to want', meaning: 'need, will, important', frequency: 4.4 },
  { char: '就', pinyin: 'jiù', translation: 'then, just', meaning: 'immediately, exactly', frequency: 4.3 },
  { char: '出', pinyin: 'chū', translation: 'to exit', meaning: 'go out, produce', frequency: 4.2 },
  { char: '会', pinyin: 'huì', translation: 'can, will', meaning: 'ability, meeting', frequency: 4.1 },
  { char: '可', pinyin: 'kě', translation: 'can, may', meaning: 'able to, approve', frequency: 4.0 },
  
  // Numbers and basic concepts
  { char: '二', pinyin: 'èr', translation: 'two', meaning: 'the number two', frequency: 3.9 },
  { char: '三', pinyin: 'sān', translation: 'three', meaning: 'the number three', frequency: 3.8 },
  { char: '四', pinyin: 'sì', translation: 'four', meaning: 'the number four', frequency: 3.7 },
  { char: '五', pinyin: 'wǔ', translation: 'five', meaning: 'the number five', frequency: 3.6 },
  { char: '六', pinyin: 'liù', translation: 'six', meaning: 'the number six', frequency: 3.5 },
  { char: '七', pinyin: 'qī', translation: 'seven', meaning: 'the number seven', frequency: 3.4 },
  { char: '八', pinyin: 'bā', translation: 'eight', meaning: 'the number eight', frequency: 3.3 },
  { char: '九', pinyin: 'jiǔ', translation: 'nine', meaning: 'the number nine', frequency: 3.2 },
  { char: '十', pinyin: 'shí', translation: 'ten', meaning: 'the number ten', frequency: 3.1 },
  { char: '百', pinyin: 'bǎi', translation: 'hundred', meaning: 'one hundred', frequency: 3.0 },
  
  // Common verbs and adjectives
  { char: '看', pinyin: 'kàn', translation: 'to look', meaning: 'see, watch, read', frequency: 4.5 },
  { char: '好', pinyin: 'hǎo', translation: 'good', meaning: 'well, fine', frequency: 4.4 },
  { char: '小', pinyin: 'xiǎo', translation: 'small', meaning: 'little, young', frequency: 4.3 },
  { char: '多', pinyin: 'duō', translation: 'many', meaning: 'much, more', frequency: 4.2 },
  { char: '少', pinyin: 'shǎo', translation: 'few', meaning: 'less, young', frequency: 4.1 },
  { char: '去', pinyin: 'qù', translation: 'to go', meaning: 'leave, remove', frequency: 4.0 },
  { char: '做', pinyin: 'zuò', translation: 'to do', meaning: 'make, work', frequency: 3.9 },
  { char: '想', pinyin: 'xiǎng', translation: 'to think', meaning: 'want, miss', frequency: 3.8 },
  { char: '用', pinyin: 'yòng', translation: 'to use', meaning: 'employ, need', frequency: 3.7 },
  { char: '天', pinyin: 'tiān', translation: 'day, sky', meaning: 'heaven, weather', frequency: 3.6 }
];

async function addChineseCharacters() {
  try {
    console.log('Starting to add Chinese characters to vocabulary table...');
    
    // Get Chinese language ID
    const { data: chineseLang, error: langError } = await supabase
      .from('languages')
      .select('id')
      .eq('code', 'zh')
      .single();
    
    if (langError || !chineseLang) {
      console.error('Error finding Chinese language:', langError);
      return;
    }
    
    console.log(`Found Chinese language with ID: ${chineseLang.id}`);
    
    // Check if Chinese characters already exist
    const { data: existingChars, error: checkError } = await supabase
      .from('language_vocabulary')
      .select('word')
      .eq('language', 'zh')
      .eq('vocabulary_type', 'character')
      .limit(5);
    
    if (!checkError && existingChars && existingChars.length > 0) {
      console.log(`Found ${existingChars.length} existing Chinese characters. Sample:`, existingChars[0].word);
      console.log('Skipping insertion to avoid duplicates. Delete existing characters first if you want to re-add.');
      return;
    }
    
    // Get difficulty levels
    const { data: difficulties, error: diffError } = await supabase
      .from('spelling_difficulty_levels')
      .select('id, name')
      .order('id');
    
    if (diffError || !difficulties) {
      console.error('Error fetching difficulty levels:', diffError);
      return;
    }
    
    console.log('Found difficulty levels:', difficulties.map(d => d.name).join(', '));
    
    // Prepare character data for insertion
    const vocabularyEntries = chineseCharacters.map((char, index) => {
      // Assign difficulty based on frequency
      let difficultyId = 1; // Basic
      if (char.frequency < 4.0) difficultyId = 3; // Intermediate
      else if (char.frequency < 5.0) difficultyId = 2; // Elementary
      
      return {
        language: 'zh',
        word: char.char,
        vocabulary_type: 'character',
        zipf_frequency: char.frequency,
        difficulty_id: difficultyId,
        english_translation: char.translation,
        pronunciation_guide: char.pinyin,
        part_of_speech: 'character',
        definition_english: char.meaning,
        example_sentence: null, // Can be added later
        example_sentence_translation: null,
        memory_tips: `Pinyin: ${char.pinyin}. Common character ranked #${index + 1}`,
        difficulty_source: 'frequency_based',
        word_source: 'HSK_common_characters',
        translation_source: 'standard_dictionary'
      };
    });
    
    console.log(`\nPrepared ${vocabularyEntries.length} Chinese characters for insertion`);
    console.log('Distribution by difficulty:');
    const basic = vocabularyEntries.filter(e => e.difficulty_id === 1).length;
    const elementary = vocabularyEntries.filter(e => e.difficulty_id === 2).length;
    const intermediate = vocabularyEntries.filter(e => e.difficulty_id === 3).length;
    console.log(`  Basic: ${basic}`);
    console.log(`  Elementary: ${elementary}`);
    console.log(`  Intermediate: ${intermediate}`);
    
    // Insert in batches of 10
    const batchSize = 10;
    let inserted = 0;
    
    for (let i = 0; i < vocabularyEntries.length; i += batchSize) {
      const batch = vocabularyEntries.slice(i, i + batchSize);
      
      const { data, error } = await supabase
        .from('language_vocabulary')
        .insert(batch)
        .select();
      
      if (error) {
        console.error(`Error inserting batch ${i / batchSize + 1}:`, error);
        break;
      }
      
      inserted += data?.length || 0;
      console.log(`  Inserted batch ${i / batchSize + 1}: ${data?.length || 0} characters`);
    }
    
    console.log(`\n✓ Successfully inserted ${inserted} Chinese characters!`);
    
    // Verify insertion
    const { count } = await supabase
      .from('language_vocabulary')
      .select('id', { count: 'exact' })
      .eq('language', 'zh')
      .eq('vocabulary_type', 'character');
    
    console.log(`\nTotal Chinese characters in database: ${count}`);
    
    // Show sample entries
    const { data: samples } = await supabase
      .from('language_vocabulary')
      .select('word, pronunciation_guide, english_translation')
      .eq('language', 'zh')
      .eq('vocabulary_type', 'character')
      .limit(5);
    
    console.log('\nSample Chinese characters:');
    samples?.forEach(s => {
      console.log(`  ${s.word} (${s.pronunciation_guide}) - ${s.english_translation}`);
    });
    
  } catch (error) {
    console.error('Unexpected error:', error);
  }
}

// Run the script
addChineseCharacters();