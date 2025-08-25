import { supabase } from '../services/supabase'

export async function checkTableExists(): Promise<boolean> {
  try {
    const { error } = await supabase
      .from('spelling_words')
      .select('id')
      .limit(1)
    
    return !error
  } catch (error) {
    console.error('Error checking table existence:', error)
    return false
  }
}

export async function setupSpellingTables() {
  const sql = `
    CREATE TABLE IF NOT EXISTS spelling_words (
      id SERIAL PRIMARY KEY,
      word VARCHAR(255) NOT NULL UNIQUE,
      definition TEXT,
      pronunciation VARCHAR(255),
      etymology TEXT,
      language_origins VARCHAR(255),
      example_sentence TEXT,
      difficulty VARCHAR(50),
      source_difficulty VARCHAR(50),
      source VARCHAR(255),
      source_url TEXT,
      definition_source VARCHAR(255),
      pronunciation_source VARCHAR(255),
      etymology_source VARCHAR(255),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `
  
  return { 
    sql,
    message: 'Table setup SQL generated. Please run this in your Supabase SQL editor.'
  }
}