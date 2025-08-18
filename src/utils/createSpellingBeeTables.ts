import { supabase } from '../services/supabase'

export async function createSpellingBeeTables() {
  try {
    // Create spelling_words table
    const { error: createTableError } = await supabase.rpc('exec_sql', {
      sql: `
        CREATE TABLE IF NOT EXISTS spelling_words (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          word VARCHAR(100) NOT NULL UNIQUE,
          definition TEXT NOT NULL,
          example_sentence TEXT NOT NULL,
          difficulty_level INTEGER NOT NULL CHECK (difficulty_level BETWEEN 1 AND 5),
          etymology TEXT,
          pronunciation_tips TEXT,
          common_misspellings TEXT[],
          audio_url TEXT,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS user_spelling_attempts (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
          word_id UUID NOT NULL REFERENCES spelling_words(id) ON DELETE CASCADE,
          correct BOOLEAN NOT NULL,
          user_spelling VARCHAR(200) NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(user_id, word_id, created_at)
        );
        
        CREATE INDEX IF NOT EXISTS idx_spelling_words_difficulty ON spelling_words(difficulty_level);
        CREATE INDEX IF NOT EXISTS idx_user_spelling_attempts_user ON user_spelling_attempts(user_id);
        CREATE INDEX IF NOT EXISTS idx_user_spelling_attempts_word ON user_spelling_attempts(word_id);
      `
    })

    if (createTableError) {
      console.error('Error creating tables:', createTableError)
      return false
    }

    // Insert sample words
    const sampleWords = [
      {
        word: 'accommodate',
        definition: 'to provide lodging or sufficient space for; to fit in with the wishes or needs of',
        example_sentence: 'The hotel can ___ up to 500 guests for the conference.',
        difficulty_level: 3,
        etymology: 'From Latin accommodare, meaning "to make fit, adapt, or adjust"',
        pronunciation_tips: 'Remember: double C, double M - think "CC-MM-date"',
        common_misspellings: ['accomodate', 'acommodate', 'acomodate']
      },
      {
        word: 'rhythm',
        definition: 'a strong, regular, repeated pattern of movement or sound',
        example_sentence: 'The drummer kept a steady ___ throughout the song.',
        difficulty_level: 4,
        etymology: 'From Greek rhythmos, meaning "measured flow or movement"',
        pronunciation_tips: 'Remember: Rhythm Has Your Two Hips Moving',
        common_misspellings: ['rythm', 'rhythem', 'rhytm']
      },
      {
        word: 'necessary',
        definition: 'required to be done, achieved, or present; needed; essential',
        example_sentence: 'It is ___ to wear safety equipment in the laboratory.',
        difficulty_level: 2,
        etymology: 'From Latin necessarius, meaning "unavoidable, indispensable"',
        pronunciation_tips: 'Remember: one C, two S\'s - think "one Collar, two Sleeves"',
        common_misspellings: ['neccessary', 'necesary', 'neccesary']
      },
      {
        word: 'conscience',
        definition: 'an inner feeling or voice acting as a guide to rightness or wrongness of behavior',
        example_sentence: 'His ___ wouldn\'t let him keep the money he found.',
        difficulty_level: 3,
        etymology: 'From Latin conscientia, meaning "knowledge within oneself"',
        pronunciation_tips: 'Remember: con-SCIENCE - it\'s the science of knowing right from wrong',
        common_misspellings: ['conscious', 'concience', 'consience']
      },
      {
        word: 'mischievous',
        definition: 'causing or showing a fondness for causing trouble in a playful way',
        example_sentence: 'The ___ puppy chewed on everyone\'s shoes.',
        difficulty_level: 4,
        etymology: 'From Old French meschief, meaning "misfortune, harm"',
        pronunciation_tips: 'Remember: MIS-chie-vous (3 syllables, not 4) - think "chief of mischief"',
        common_misspellings: ['mischievious', 'mischeivous', 'mischevious']
      },
      {
        word: 'definitely',
        definition: 'without doubt; certainly',
        example_sentence: 'I will ___ attend the meeting tomorrow.',
        difficulty_level: 2,
        etymology: 'From Latin definitus, meaning "defined, limited, determined"',
        pronunciation_tips: 'Remember: definite + ly - think "finite" in the middle',
        common_misspellings: ['definately', 'definitly', 'defintely']
      },
      {
        word: 'embarrass',
        definition: 'to cause someone to feel awkward, self-conscious, or ashamed',
        example_sentence: 'Please don\'t ___ me in front of my friends.',
        difficulty_level: 3,
        etymology: 'From French embarrasser, meaning "to block, obstruct"',
        pronunciation_tips: 'Remember: double R, double S - think "Really Red, So Shy"',
        common_misspellings: ['embarass', 'embarras', 'embarrass']
      },
      {
        word: 'privilege',
        definition: 'a special right, advantage, or immunity granted to a particular person or group',
        example_sentence: 'It is a ___ to be able to attend this prestigious school.',
        difficulty_level: 3,
        etymology: 'From Latin privilegium, meaning "law for an individual"',
        pronunciation_tips: 'Remember: PRIVI-lege (not privelege) - think "private privilege"',
        common_misspellings: ['privelege', 'priviledge', 'privilage']
      },
      {
        word: 'separate',
        definition: 'forming or viewed as a unit apart or by itself',
        example_sentence: 'Please keep the white and colored clothes ___ when washing.',
        difficulty_level: 2,
        etymology: 'From Latin separatus, meaning "to pull apart"',
        pronunciation_tips: 'Remember: SE-PAR-ATE - think "A RAT" in the middle',
        common_misspellings: ['seperate', 'seprate', 'separete']
      },
      {
        word: 'occurrence',
        definition: 'an instance or event of something happening',
        example_sentence: 'This is the third ___ of theft this month.',
        difficulty_level: 3,
        etymology: 'From Latin occurrere, meaning "to run to meet, to happen"',
        pronunciation_tips: 'Remember: double C, double R - think "occur + rence"',
        common_misspellings: ['occurence', 'occurance', 'occurrance']
      }
    ]

    // Insert sample words
    for (const word of sampleWords) {
      const { error: insertError } = await supabase
        .from('spelling_words')
        .upsert(word, { onConflict: 'word' })

      if (insertError) {
        console.error(`Error inserting word ${word.word}:`, insertError)
      }
    }

    console.log('Spelling bee tables created and sample data inserted successfully!')
    return true
  } catch (error) {
    console.error('Error setting up spelling bee:', error)
    return false
  }
}

// Function to check if tables exist
export async function checkSpellingBeeTables() {
  try {
    const { error } = await supabase
      .from('spelling_words')
      .select('count')
      .limit(1)

    if (error) {
      console.log('Spelling words table does not exist')
      return false
    }

    return true
  } catch (error) {
    return false
  }
}