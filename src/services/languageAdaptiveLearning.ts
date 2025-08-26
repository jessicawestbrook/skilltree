import { supabase } from './supabase';

interface CALSession {
  id: string;
  user_id: string;
  language_id: string;
  started_at: string;
  last_updated: string;
  session_state: any;
  is_active: boolean;
  total_questions: number;
  correct_answers: number;
}

interface CALPerformance {
  id: string;
  user_id: string;
  language_id: string;
  category: 'vocabulary' | 'grammar' | 'listening' | 'reading';
  difficulty_level: number;
  total_attempts: number;
  correct_attempts: number;
  last_attempt_at: string | null;
  streak: number;
}

interface CALAttempt {
  session_id: string;
  user_id: string;
  language_id: string;
  category: string;
  question_id: string;
  question_type: string;
  difficulty_level: number;
  is_correct: boolean;
  response_time_ms: number;
}

interface Question {
  id: string;
  category: string;
  difficulty: number;
  question_text: string;
  question_type: string;
  options?: string[];
  correct_answer?: string;
  correct_answer_index?: number;
  audio_url?: string;
  image_url?: string;
}

export class LanguageAdaptiveLearning {
  private currentSession: CALSession | null = null;
  private performances: Map<string, CALPerformance> = new Map();
  private questionHistory: Set<string> = new Set();
  private recentQuestions: string[] = [];
  private readonly MAX_RECENT_QUESTIONS = 20;

  /**
   * Start or resume a CAL session
   */
  async startSession(userId: string, languageId: string): Promise<CALSession> {
    try {
      // Check for existing active session
      const { data: existingSession, error: fetchError } = await supabase
        .from('language_cal_sessions')
        .select('*')
        .eq('user_id', userId)
        .eq('language_id', languageId)
        .eq('is_active', true)
        .single();

      if (existingSession && !fetchError) {
        // Resume existing session
        this.currentSession = existingSession;
        
        // Load session state
        if (existingSession.session_state) {
          this.questionHistory = new Set(existingSession.session_state.questionHistory || []);
          this.recentQuestions = existingSession.session_state.recentQuestions || [];
        }
      } else {
        // Create new session
        const { data: newSession, error: createError } = await supabase
          .from('language_cal_sessions')
          .insert({
            user_id: userId,
            language_id: languageId,
            session_state: {
              questionHistory: [],
              recentQuestions: []
            }
          })
          .select()
          .single();

        if (createError || !newSession) throw createError || new Error('Failed to create session');
        this.currentSession = newSession;
      }

      // Load performance data for all categories
      await this.loadPerformanceData(userId, languageId);

      return this.currentSession as CALSession;
    } catch (error) {
      console.error('Error starting CAL session:', error);
      throw error;
    }
  }

  /**
   * Load performance data for all categories
   */
  private async loadPerformanceData(userId: string, languageId: string): Promise<void> {
    try {
      const { data, error } = await supabase
        .from('language_cal_performance')
        .select('*')
        .eq('user_id', userId)
        .eq('language_id', languageId);

      if (error) throw error;

      this.performances.clear();
      data?.forEach(perf => {
        this.performances.set(perf.category, perf);
      });

      // Initialize missing categories with default values
      const categories: Array<'vocabulary' | 'grammar' | 'listening' | 'reading'> = 
        ['vocabulary', 'grammar', 'listening', 'reading'];
      
      for (const category of categories) {
        if (!this.performances.has(category)) {
          // Default performance for new categories
          this.performances.set(category, {
            id: '',
            user_id: userId,
            language_id: languageId,
            category,
            difficulty_level: 1.0,
            total_attempts: 0,
            correct_attempts: 0,
            last_attempt_at: null,
            streak: 0
          });
        }
      }
    } catch (error) {
      console.error('Error loading performance data:', error);
    }
  }

  /**
   * Select the next question based on adaptive algorithm
   */
  async selectNextQuestion(languageId: string): Promise<Question | null> {
    if (!this.currentSession) return null;

    try {
      // Determine which category to select from based on performance
      const category = this.selectCategory();
      const difficulty = this.getDifficultyForCategory(category);

      // Fetch available questions
      const questions = await this.fetchQuestions(languageId, category, difficulty);
      
      // Filter out recently asked questions
      const availableQuestions = questions.filter(q => 
        !this.recentQuestions.includes(q.id)
      );

      if (availableQuestions.length === 0) {
        // If no new questions available, reset recent questions
        this.recentQuestions = [];
        return questions.length > 0 ? questions[0] : null;
      }

      // Select a random question from available ones
      const selectedQuestion = availableQuestions[
        Math.floor(Math.random() * availableQuestions.length)
      ];

      // Update recent questions list
      this.recentQuestions.push(selectedQuestion.id);
      if (this.recentQuestions.length > this.MAX_RECENT_QUESTIONS) {
        this.recentQuestions.shift();
      }

      // Save session state
      await this.saveSessionState();

      return selectedQuestion;
    } catch (error) {
      console.error('Error selecting next question:', error);
      return null;
    }
  }

  /**
   * Select category based on performance and variety
   */
  private selectCategory(): 'vocabulary' | 'grammar' | 'listening' | 'reading' {
    const categories: Array<'vocabulary' | 'grammar' | 'listening' | 'reading'> = 
      ['vocabulary', 'grammar', 'listening', 'reading'];
    
    // Calculate weights for each category
    const weights = categories.map(cat => {
      const perf = this.performances.get(cat);
      if (!perf) return { category: cat, weight: 1 };

      // Lower weight for categories with high success rate (to practice weaker areas)
      const successRate = perf.total_attempts > 0 
        ? perf.correct_attempts / perf.total_attempts 
        : 0.5;
      
      // Increase weight for categories not practiced recently
      const recencyBonus = perf.last_attempt_at 
        ? Math.min(1, (Date.now() - new Date(perf.last_attempt_at).getTime()) / (24 * 60 * 60 * 1000))
        : 1;

      // Calculate final weight (inverse of success rate, with recency bonus)
      const weight = (2 - successRate) * (1 + recencyBonus * 0.5);

      return { category: cat, weight };
    });

    // Weighted random selection
    const totalWeight = weights.reduce((sum, w) => sum + w.weight, 0);
    let random = Math.random() * totalWeight;

    for (const { category, weight } of weights) {
      random -= weight;
      if (random <= 0) {
        return category;
      }
    }

    return 'vocabulary'; // Fallback
  }

  /**
   * Get appropriate difficulty for a category
   */
  private getDifficultyForCategory(category: string): number {
    const perf = this.performances.get(category);
    if (!perf) return 1.0;

    // Add some randomization around the difficulty level
    const variance = 0.5;
    const minDiff = Math.max(0.5, perf.difficulty_level - variance);
    const maxDiff = Math.min(5.0, perf.difficulty_level + variance);
    
    return minDiff + Math.random() * (maxDiff - minDiff);
  }

  /**
   * Fetch questions based on criteria
   */
  private async fetchQuestions(
    languageId: string, 
    category: string, 
    targetDifficulty: number
  ): Promise<Question[]> {
    try {
      let questions: any[] = [];

      // Map difficulty number to difficulty levels
      const difficultyLevel = this.mapDifficultyToLevel(targetDifficulty);

      if (category === 'vocabulary') {
        // Fetch vocabulary questions
        const { data, error } = await supabase
          .from('language_vocabulary')
          .select('*')
          .eq('language_id', languageId)
          .eq('difficulty', difficultyLevel)
          .limit(50);

        if (!error && data) {
          questions = data.map(item => ({
            id: `vocab-${item.id}`,
            category: 'vocabulary',
            difficulty: targetDifficulty,
            question_text: item.word_original,
            question_type: 'translation',
            correct_answer: item.word_translated,
            options: this.generateVocabOptions(item.word_translated, data)
          }));
        }
      } else if (category === 'grammar') {
        // Fetch grammar questions
        const { data, error } = await supabase
          .from('language_questions')
          .select('*')
          .eq('language_id', languageId)
          .eq('difficulty_level', Math.round(targetDifficulty))
          .limit(50);

        if (!error && data) {
          questions = data.map(item => ({
            id: `grammar-${item.id}`,
            category: 'grammar',
            difficulty: targetDifficulty,
            question_text: item.question_text,
            question_type: item.question_type,
            options: item.options,
            correct_answer_index: item.correct_answer_index
          }));
        }
      }
      // TODO: Add support for listening and reading categories

      return questions;
    } catch (error) {
      console.error('Error fetching questions:', error);
      return [];
    }
  }

  /**
   * Map numeric difficulty to string levels
   */
  private mapDifficultyToLevel(difficulty: number): string {
    if (difficulty < 1) return 'basic';
    if (difficulty < 2) return 'elementary';
    if (difficulty < 3) return 'intermediate';
    if (difficulty < 4) return 'advanced';
    return 'expert';
  }

  /**
   * Generate multiple choice options for vocabulary
   */
  private generateVocabOptions(correct: string, allWords: any[]): string[] {
    const options = [correct];
    const otherWords = allWords
      .map(w => w.word_translated)
      .filter(w => w !== correct);

    // Add 3 random incorrect options
    while (options.length < 4 && otherWords.length > 0) {
      const randomIndex = Math.floor(Math.random() * otherWords.length);
      const option = otherWords[randomIndex];
      if (!options.includes(option)) {
        options.push(option);
      }
      otherWords.splice(randomIndex, 1);
    }

    // Shuffle options
    return options.sort(() => Math.random() - 0.5);
  }

  /**
   * Record an answer attempt
   */
  async recordAttempt(
    questionId: string,
    category: string,
    isCorrect: boolean,
    responseTimeMs: number,
    questionType: string = 'unknown',
    difficulty: number = 1.0
  ): Promise<void> {
    if (!this.currentSession) return;

    try {
      const attempt: CALAttempt = {
        session_id: this.currentSession.id,
        user_id: this.currentSession.user_id,
        language_id: this.currentSession.language_id,
        category,
        question_id: questionId,
        question_type: questionType,
        difficulty_level: difficulty,
        is_correct: isCorrect,
        response_time_ms: responseTimeMs
      };

      const { error } = await supabase
        .from('language_cal_attempts')
        .insert(attempt);

      if (error) throw error;

      // Update local performance data
      const perf = this.performances.get(category);
      if (perf) {
        perf.total_attempts++;
        if (isCorrect) {
          perf.correct_attempts++;
          perf.streak++;
          // Increase difficulty on streak
          if (perf.streak >= 3) {
            perf.difficulty_level = Math.min(5.0, perf.difficulty_level + 0.1);
          }
        } else {
          perf.streak = 0;
          // Decrease difficulty on incorrect
          perf.difficulty_level = Math.max(0.5, perf.difficulty_level - 0.05);
        }
        perf.last_attempt_at = new Date().toISOString();
      }

      // Add to question history
      this.questionHistory.add(questionId);

      // Update session state
      await this.saveSessionState();
    } catch (error) {
      console.error('Error recording attempt:', error);
    }
  }

  /**
   * Save current session state
   */
  private async saveSessionState(): Promise<void> {
    if (!this.currentSession) return;

    try {
      const sessionState = {
        questionHistory: Array.from(this.questionHistory),
        recentQuestions: this.recentQuestions
      };

      const { error } = await supabase
        .from('language_cal_sessions')
        .update({
          session_state: sessionState,
          last_updated: new Date().toISOString()
        })
        .eq('id', this.currentSession.id);

      if (error) throw error;
    } catch (error) {
      console.error('Error saving session state:', error);
    }
  }

  /**
   * End the current session
   */
  async endSession(): Promise<void> {
    if (!this.currentSession) return;

    try {
      const { error } = await supabase
        .from('language_cal_sessions')
        .update({
          is_active: false,
          last_updated: new Date().toISOString()
        })
        .eq('id', this.currentSession.id);

      if (error) throw error;

      this.currentSession = null;
      this.performances.clear();
      this.questionHistory.clear();
      this.recentQuestions = [];
    } catch (error) {
      console.error('Error ending session:', error);
    }
  }

  /**
   * Get current session statistics
   */
  getSessionStats(): {
    totalQuestions: number;
    correctAnswers: number;
    accuracy: number;
    categoryBreakdown: Map<string, { total: number; correct: number; accuracy: number }>;
  } | null {
    if (!this.currentSession) return null;

    const categoryStats = new Map<string, { total: number; correct: number; accuracy: number }>();
    
    this.performances.forEach((perf, category) => {
      const total = perf.total_attempts;
      const correct = perf.correct_attempts;
      const accuracy = total > 0 ? (correct / total) * 100 : 0;
      
      categoryStats.set(category, { total, correct, accuracy });
    });

    const totalQuestions = this.currentSession.total_questions;
    const correctAnswers = this.currentSession.correct_answers;
    const accuracy = totalQuestions > 0 ? (correctAnswers / totalQuestions) * 100 : 0;

    return {
      totalQuestions,
      correctAnswers,
      accuracy,
      categoryBreakdown: categoryStats
    };
  }

  /**
   * Get performance history for a specific category
   */
  getCategoryPerformance(category: string): CALPerformance | undefined {
    return this.performances.get(category);
  }
}

export const languageCAL = new LanguageAdaptiveLearning();