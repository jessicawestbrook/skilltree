import { supabase } from '../services/supabase'

export async function createStudyListTables(): Promise<boolean> {
  // Note: This function requires manual database table creation through Supabase dashboard
  // The RPC exec_sql function may not be available in all Supabase instances
  
  console.log(`
    📋 MANUAL DATABASE SETUP REQUIRED
    
    The study list feature requires the following tables to be created in your Supabase database.
    Please run these SQL commands in your Supabase SQL Editor:
    
    -- Create study_lists table
    CREATE TABLE IF NOT EXISTS study_lists (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
      name VARCHAR(200) NOT NULL,
      description TEXT,
      color VARCHAR(7) DEFAULT '#3B82F6',
      is_public BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create starred_items table
    CREATE TABLE IF NOT EXISTS starred_items (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
      item_type VARCHAR(50) NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node')),
      item_id VARCHAR(200) NOT NULL,
      item_data JSONB,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(user_id, item_type, item_id)
    );
    
    -- Create study_list_items table
    CREATE TABLE IF NOT EXISTS study_list_items (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      study_list_id UUID NOT NULL REFERENCES study_lists(id) ON DELETE CASCADE,
      item_type VARCHAR(50) NOT NULL CHECK (item_type IN ('spelling_word', 'vocabulary_word', 'language_question', 'question', 'skill_node', 'custom_flashcard')),
      item_id VARCHAR(200) NOT NULL,
      item_data JSONB,
      notes TEXT,
      added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(study_list_id, item_type, item_id)
    );
    
    -- Create custom_flashcards table
    CREATE TABLE IF NOT EXISTS custom_flashcards (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
      front TEXT NOT NULL,
      back TEXT NOT NULL,
      category VARCHAR(100),
      tags TEXT[],
      difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create study_sessions table
    CREATE TABLE IF NOT EXISTS study_sessions (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
      study_list_id UUID NOT NULL REFERENCES study_lists(id) ON DELETE CASCADE,
      started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      ended_at TIMESTAMP WITH TIME ZONE,
      items_studied INTEGER DEFAULT 0,
      items_correct INTEGER DEFAULT 0,
      total_time_seconds INTEGER DEFAULT 0
    );
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_study_lists_user_id ON study_lists(user_id);
    CREATE INDEX IF NOT EXISTS idx_study_lists_created_at ON study_lists(created_at);
    CREATE INDEX IF NOT EXISTS idx_starred_items_user_id ON starred_items(user_id);
    CREATE INDEX IF NOT EXISTS idx_starred_items_type ON starred_items(item_type);
    CREATE INDEX IF NOT EXISTS idx_starred_items_created_at ON starred_items(created_at);
    CREATE INDEX IF NOT EXISTS idx_study_list_items_study_list_id ON study_list_items(study_list_id);
    CREATE INDEX IF NOT EXISTS idx_study_list_items_type ON study_list_items(item_type);
    CREATE INDEX IF NOT EXISTS idx_study_list_items_added_at ON study_list_items(added_at);
    CREATE INDEX IF NOT EXISTS idx_custom_flashcards_user_id ON custom_flashcards(user_id);
    CREATE INDEX IF NOT EXISTS idx_custom_flashcards_category ON custom_flashcards(category);
    CREATE INDEX IF NOT EXISTS idx_custom_flashcards_difficulty ON custom_flashcards(difficulty_level);
    CREATE INDEX IF NOT EXISTS idx_study_sessions_user_id ON study_sessions(user_id);
    CREATE INDEX IF NOT EXISTS idx_study_sessions_study_list_id ON study_sessions(study_list_id);
    CREATE INDEX IF NOT EXISTS idx_study_sessions_started_at ON study_sessions(started_at);
  `)
  
  // For now, return false to indicate tables need manual creation
  return false
}

export async function checkStudyListTables(): Promise<boolean> {
  try {
    const { error } = await supabase
      .from('study_lists')
      .select('id')
      .limit(1)

    return !error
  } catch (error) {
    return false
  }
}