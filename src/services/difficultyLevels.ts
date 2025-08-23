import { supabase } from './supabase';
import { SpellingDifficultyLevel, VocabularyDifficultyLevel } from '../types/difficultyLevels';

export async function getSpellingDifficultyLevels(): Promise<SpellingDifficultyLevel[]> {
  const { data, error } = await supabase
    .from('spelling_difficulty_levels')
    .select('*')
    .order('id');

  if (error) {
    console.error('Error fetching spelling difficulty levels:', error);
    // Fallback to hardcoded values if table doesn't exist yet
    return [
      { id: 1, name: 'Beginner', description: 'Common everyday vocabulary, phonetic spelling, basic patterns', grade_equivalent: 'Grades 1-3' },
      { id: 2, name: 'Elementary', description: 'Standard school vocabulary, introduction to silent letters, common prefixes/suffixes', grade_equivalent: 'Grades 4-5' },
      { id: 3, name: 'Intermediate', description: 'Complex patterns, foreign borrowings, multiple syllables, irregular spellings', grade_equivalent: 'Grades 6-8' },
      { id: 4, name: 'Advanced', description: 'Etymology-based spelling, uncommon letter combinations, technical vocabulary', grade_equivalent: 'Grades 9-12 (Regional)' },
      { id: 5, name: 'Expert', description: 'Championship words, rare etymology, complex linguistic origins', grade_equivalent: 'Competition Level' }
    ];
  }

  return data || [];
}

export async function getVocabularyDifficultyLevels(): Promise<VocabularyDifficultyLevel[]> {
  const { data, error } = await supabase
    .from('vocabulary_difficulty_levels')
    .select('*')
    .order('id');

  if (error) {
    console.error('Error fetching vocabulary difficulty levels:', error);
    // Fallback to hardcoded values if table doesn't exist yet
    return [
      { id: 1, name: 'Foundation', description: 'Basic everyday concepts' },
      { id: 2, name: 'Academic', description: 'School-level vocabulary' },
      { id: 3, name: 'Sophisticated', description: 'Advanced academic and professional' },
      { id: 4, name: 'Specialized', description: 'Domain-specific terminology' },
      { id: 5, name: 'Scholarly', description: 'Research and expert-level' }
    ];
  }

  return data || [];
}

export async function getSpellingDifficultyById(id: number): Promise<SpellingDifficultyLevel | null> {
  const levels = await getSpellingDifficultyLevels();
  return levels.find(level => level.id === id) || null;
}

export async function getVocabularyDifficultyById(id: number): Promise<VocabularyDifficultyLevel | null> {
  const levels = await getVocabularyDifficultyLevels();
  return levels.find(level => level.id === id) || null;
}

// Helper function to get difficulty name by level (for backward compatibility)
export async function getSpellingDifficultyName(level: number): Promise<string> {
  const difficulty = await getSpellingDifficultyById(level);
  return difficulty?.name || `Level ${level}`;
}

export async function getVocabularyDifficultyName(level: number): Promise<string> {
  const difficulty = await getVocabularyDifficultyById(level);
  return difficulty?.name || `Level ${level}`;
}