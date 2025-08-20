import { supabase } from '../services/supabase'

export async function createLanguageTrainerTables() {
  try {
    // Create language trainer tables
    const { error: createTableError } = await supabase.rpc('exec_sql', {
      sql: `
        -- Languages table
        CREATE TABLE IF NOT EXISTS languages (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          name VARCHAR(100) NOT NULL UNIQUE,
          code VARCHAR(10) NOT NULL UNIQUE,
          flag_emoji VARCHAR(10),
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Language learning categories table
        CREATE TABLE IF NOT EXISTS language_categories (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          language_id UUID NOT NULL REFERENCES languages(id) ON DELETE CASCADE,
          name VARCHAR(200) NOT NULL,
          description TEXT,
          display_order INTEGER DEFAULT 0,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(language_id, name)
        );
        
        -- Language questions table
        CREATE TABLE IF NOT EXISTS language_questions (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          language_id UUID NOT NULL REFERENCES languages(id) ON DELETE CASCADE,
          category_id UUID NOT NULL REFERENCES language_categories(id) ON DELETE CASCADE,
          question_text TEXT NOT NULL,
          question_type VARCHAR(50) NOT NULL DEFAULT 'multiple_choice',
          options TEXT[] NOT NULL, -- JSON array of answer options
          correct_answer_index INTEGER NOT NULL,
          explanation TEXT,
          difficulty_level INTEGER DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 5),
          image_url TEXT,
          audio_url TEXT,
          source_url TEXT,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- User language question attempts table
        CREATE TABLE IF NOT EXISTS user_language_attempts (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
          question_id UUID NOT NULL REFERENCES language_questions(id) ON DELETE CASCADE,
          selected_option_index INTEGER NOT NULL,
          is_correct BOOLEAN NOT NULL,
          time_taken_seconds INTEGER DEFAULT 0,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(user_id, question_id, created_at)
        );
        
        -- User language progress table
        CREATE TABLE IF NOT EXISTS user_language_progress (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
          language_id UUID NOT NULL REFERENCES languages(id) ON DELETE CASCADE,
          category_id UUID NOT NULL REFERENCES language_categories(id) ON DELETE CASCADE,
          questions_attempted INTEGER DEFAULT 0,
          questions_correct INTEGER DEFAULT 0,
          accuracy_percentage DECIMAL(5,2) DEFAULT 0,
          last_practiced TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(user_id, language_id, category_id)
        );
        
        -- Create indexes for performance
        CREATE INDEX IF NOT EXISTS idx_languages_code ON languages(code);
        CREATE INDEX IF NOT EXISTS idx_language_categories_language ON language_categories(language_id);
        CREATE INDEX IF NOT EXISTS idx_language_questions_language ON language_questions(language_id);
        CREATE INDEX IF NOT EXISTS idx_language_questions_category ON language_questions(category_id);
        CREATE INDEX IF NOT EXISTS idx_language_questions_difficulty ON language_questions(difficulty_level);
        CREATE INDEX IF NOT EXISTS idx_user_language_attempts_user ON user_language_attempts(user_id);
        CREATE INDEX IF NOT EXISTS idx_user_language_attempts_question ON user_language_attempts(question_id);
        CREATE INDEX IF NOT EXISTS idx_user_language_progress_user_lang ON user_language_progress(user_id, language_id);
      `
    })

    if (createTableError) {
      console.error('Error creating language trainer tables:', createTableError)
      return false
    }

    // Insert sample languages
    const sampleLanguages = [
      { name: 'Spanish', code: 'es', flag_emoji: '🇪🇸' },
      { name: 'French', code: 'fr', flag_emoji: '🇫🇷' },
      { name: 'German', code: 'de', flag_emoji: '🇩🇪' },
      { name: 'Italian', code: 'it', flag_emoji: '🇮🇹' },
      { name: 'Portuguese', code: 'pt', flag_emoji: '🇵🇹' },
      { name: 'Japanese', code: 'ja', flag_emoji: '🇯🇵' },
      { name: 'Chinese (Mandarin)', code: 'zh', flag_emoji: '🇨🇳' },
      { name: 'Korean', code: 'ko', flag_emoji: '🇰🇷' },
      { name: 'Russian', code: 'ru', flag_emoji: '🇷🇺' },
      { name: 'Arabic', code: 'ar', flag_emoji: '🇸🇦' }
    ]

    // Insert languages
    for (const language of sampleLanguages) {
      const { data: languageData, error: insertError } = await supabase
        .from('languages')
        .upsert(language, { onConflict: 'code' })
        .select()
        .single()

      if (insertError) {
        console.error(`Error inserting language ${language.name}:`, insertError)
      } else if (languageData) {
        // Insert sample categories for Spanish (as an example)
        if (language.code === 'es') {
          const spanishCategories = [
            { language_id: languageData.id, name: 'Basic Vocabulary', description: 'Common everyday words', display_order: 1 },
            { language_id: languageData.id, name: 'Family & Relationships', description: 'Family members and relationships', display_order: 2 },
            { language_id: languageData.id, name: 'Food & Dining', description: 'Food, drinks, and restaurant vocabulary', display_order: 3 },
            { language_id: languageData.id, name: 'Numbers & Time', description: 'Numbers, dates, and time expressions', display_order: 4 },
            { language_id: languageData.id, name: 'Colors & Descriptions', description: 'Colors and descriptive adjectives', display_order: 5 },
            { language_id: languageData.id, name: 'Transportation', description: 'Vehicles and travel vocabulary', display_order: 6 },
            { language_id: languageData.id, name: 'Greetings & Politeness', description: 'Common greetings and polite expressions', display_order: 7 },
            { language_id: languageData.id, name: 'House & Home', description: 'Home, furniture, and household items', display_order: 8 }
          ]

          for (const category of spanishCategories) {
            const { data: categoryData, error: categoryError } = await supabase
              .from('language_categories')
              .upsert(category, { onConflict: 'language_id,name' })
              .select()
              .single()

            if (categoryError) {
              console.error(`Error inserting category ${category.name}:`, categoryError)
            } else if (categoryData) {
              // Insert sample questions for Basic Vocabulary
              if (category.name === 'Basic Vocabulary') {
                const sampleQuestions = [
                  {
                    language_id: languageData.id,
                    category_id: categoryData.id,
                    question_text: 'What is the Spanish word for "hello"?',
                    question_type: 'multiple_choice',
                    options: ['hola', 'adiós', 'gracias', 'por favor'],
                    correct_answer_index: 0,
                    explanation: '"Hola" is the most common greeting in Spanish, used in both formal and informal situations.',
                    difficulty_level: 1
                  },
                  {
                    language_id: languageData.id,
                    category_id: categoryData.id,
                    question_text: 'How do you say "thank you" in Spanish?',
                    question_type: 'multiple_choice',
                    options: ['de nada', 'por favor', 'gracias', 'perdón'],
                    correct_answer_index: 2,
                    explanation: '"Gracias" means "thank you" and is one of the most important polite expressions to learn.',
                    difficulty_level: 1
                  },
                  {
                    language_id: languageData.id,
                    category_id: categoryData.id,
                    question_text: 'What does "agua" mean in English?',
                    question_type: 'multiple_choice',
                    options: ['food', 'water', 'house', 'book'],
                    correct_answer_index: 1,
                    explanation: '"Agua" is a feminine noun meaning "water". It\'s an essential vocabulary word.',
                    difficulty_level: 1
                  },
                  {
                    language_id: languageData.id,
                    category_id: categoryData.id,
                    question_text: 'Which word means "yes" in Spanish?',
                    question_type: 'multiple_choice',
                    options: ['no', 'sí', 'tal vez', 'nunca'],
                    correct_answer_index: 1,
                    explanation: '"Sí" (with an accent) means "yes". Don\'t confuse it with "si" (without accent) which means "if".',
                    difficulty_level: 1
                  },
                  {
                    language_id: languageData.id,
                    category_id: categoryData.id,
                    question_text: 'What is the Spanish word for "goodbye"?',
                    question_type: 'multiple_choice',
                    options: ['hola', 'adiós', 'buenas noches', 'hasta mañana'],
                    correct_answer_index: 1,
                    explanation: '"Adiós" is the general word for "goodbye". Other options are specific greetings for different times.',
                    difficulty_level: 1
                  }
                ]

                for (const question of sampleQuestions) {
                  const { error: questionError } = await supabase
                    .from('language_questions')
                    .insert(question)

                  if (questionError) {
                    console.error('Error inserting question:', questionError)
                  }
                }
              }
            }
          }
        }

        // Insert basic categories for other languages
        if (language.code === 'fr') {
          const frenchCategories = [
            { language_id: languageData.id, name: 'Basic Vocabulary', description: 'Common everyday words', display_order: 1 },
            { language_id: languageData.id, name: 'Family & Relationships', description: 'Family members and relationships', display_order: 2 },
            { language_id: languageData.id, name: 'Food & Dining', description: 'Food, drinks, and restaurant vocabulary', display_order: 3 }
          ]

          for (const category of frenchCategories) {
            await supabase
              .from('language_categories')
              .upsert(category, { onConflict: 'language_id,name' })
          }
        }

        if (language.code === 'de') {
          const germanCategories = [
            { language_id: languageData.id, name: 'Basic Vocabulary', description: 'Common everyday words', display_order: 1 },
            { language_id: languageData.id, name: 'Family & Relationships', description: 'Family members and relationships', display_order: 2 },
            { language_id: languageData.id, name: 'Food & Dining', description: 'Food, drinks, and restaurant vocabulary', display_order: 3 }
          ]

          for (const category of germanCategories) {
            await supabase
              .from('language_categories')
              .upsert(category, { onConflict: 'language_id,name' })
          }
        }
      }
    }

    console.log('Language trainer tables created and sample data inserted successfully!')
    return true
  } catch (error) {
    console.error('Error setting up language trainer:', error)
    return false
  }
}

// Function to check if tables exist
export async function checkLanguageTrainerTables() {
  try {
    const { error } = await supabase
      .from('languages')
      .select('count')
      .limit(1)

    if (error) {
      console.log('Language trainer tables do not exist')
      return false
    }

    return true
  } catch (error) {
    return false
  }
}