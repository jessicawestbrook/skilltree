export interface SpellingDifficultyLevel {
  id: number;
  name: string;
  description: string;
  grade_equivalent?: string;
  characteristics?: string;
  created_at?: string;
  updated_at?: string;
}

export interface VocabularyDifficultyLevel {
  id: number;
  name: string;
  description: string;
  characteristics?: string;
  created_at?: string;
  updated_at?: string;
}

export interface SpellingWordWithDifficulties {
  id: string;
  word: string;
  definition: string;
  example_sentence: string;
  spelling_difficulty_id?: number;
  vocabulary_difficulty_id?: number;
  etymology?: string;
  etymology_source?: string;
  pronunciation_guide?: string;
  part_of_speech?: string;
  memory_tips?: string;
  pronunciation_tips?: string;
  common_misspellings?: string[];
  phonetic_transparency_score?: number;
  word_frequency_score?: number;
  morphology_score?: number;
  etymology_score?: number;
  source_names?: string[];
  source_difficulties?: string[];
  original_source?: string;
  audio_url?: string;
  // Join fields from difficulty tables
  spelling_difficulty?: SpellingDifficultyLevel;
  vocabulary_difficulty?: VocabularyDifficultyLevel;
}