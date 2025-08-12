import { supabase } from '../lib/superbase';
import { QuizQuestion } from '../types';

export interface DatabaseQuizQuestion {
  id: string;
  node_id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
  created_at: string;
  updated_at?: string;
}

export class QuizService {
  /**
   * Fetch quiz questions for a specific node from Supabase
   */
  static async getQuestionsForNode(nodeId: string): Promise<QuizQuestion[]> {
    try {
      const { data, error } = await supabase
        .from('quiz_questions')
        .select('*')
        .eq('node_id', nodeId)
        .order('created_at', { ascending: true });

      if (error) {
        console.error(`Error fetching questions for node ${nodeId}:`, error);
        return this.getFallbackQuestions(nodeId);
      }

      if (!data || data.length === 0) {
        console.log(`No questions found for node ${nodeId}, using fallback`);
        return this.getFallbackQuestions(nodeId);
      }

      // Transform database format to app format
      return data.map(q => ({
        question: q.question,
        options: q.options,
        correct: q.correct_answer,
        explanation: q.explanation
      }));
    } catch (err) {
      console.error('Error in getQuestionsForNode:', err);
      return this.getFallbackQuestions(nodeId);
    }
  }

  /**
   * Fetch all quiz questions from Supabase
   */
  static async getAllQuestions(): Promise<Record<string, QuizQuestion[]>> {
    try {
      const { data, error } = await supabase
        .from('quiz_questions')
        .select('*')
        .order('node_id', { ascending: true });

      if (error) {
        console.error('Error fetching all questions:', error);
        return this.getAllFallbackQuestions();
      }

      if (!data || data.length === 0) {
        return this.getAllFallbackQuestions();
      }

      // Group questions by node_id
      const groupedQuestions: Record<string, QuizQuestion[]> = {};
      
      data.forEach(q => {
        if (!groupedQuestions[q.node_id]) {
          groupedQuestions[q.node_id] = [];
        }
        
        groupedQuestions[q.node_id].push({
          question: q.question,
          options: q.options,
          correct: q.correct_answer,
          explanation: q.explanation
        });
      });

      return groupedQuestions;
    } catch (err) {
      console.error('Error in getAllQuestions:', err);
      return this.getAllFallbackQuestions();
    }
  }

  /**
   * Add a new question to Supabase
   */
  static async addQuestion(nodeId: string, question: QuizQuestion): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('quiz_questions')
        .insert([{
          node_id: nodeId,
          question: question.question,
          options: question.options,
          correct_answer: question.correct,
          explanation: question.explanation,
          created_at: new Date().toISOString()
        }]);

      if (error) {
        console.error('Error adding question:', error);
        return false;
      }

      return true;
    } catch (err) {
      console.error('Error in addQuestion:', err);
      return false;
    }
  }

  /**
   * Update an existing question
   */
  static async updateQuestion(questionId: string, updates: Partial<QuizQuestion>): Promise<boolean> {
    try {
      const updateData: Record<string, string | string[] | number | Date> = {
        updated_at: new Date().toISOString()
      };

      if (updates.question) updateData.question = updates.question;
      if (updates.options) updateData.options = updates.options;
      if (updates.correct !== undefined) updateData.correct_answer = updates.correct;
      if (updates.explanation) updateData.explanation = updates.explanation;

      const { error } = await supabase
        .from('quiz_questions')
        .update(updateData)
        .eq('id', questionId);

      if (error) {
        console.error('Error updating question:', error);
        return false;
      }

      return true;
    } catch (err) {
      console.error('Error in updateQuestion:', err);
      return false;
    }
  }

  /**
   * Delete a question
   */
  static async deleteQuestion(questionId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('quiz_questions')
        .delete()
        .eq('id', questionId);

      if (error) {
        console.error('Error deleting question:', error);
        return false;
      }

      return true;
    } catch (err) {
      console.error('Error in deleteQuestion:', err);
      return false;
    }
  }

  /**
   * Get fallback questions when database is unavailable
   */
  private static getFallbackQuestions(nodeId: string): QuizQuestion[] {
    // Import the local questions as fallback
    const fallbackQuestions: Record<string, QuizQuestion[]> = {
      'symbols-meaning': [
        {
          question: "What is the primary purpose of symbols?",
          options: ["To represent ideas", "To look pretty", "To confuse", "To take up space"],
          correct: 0,
          explanation: "Symbols are visual representations of ideas, concepts, or objects"
        }
      ]
    };

    return fallbackQuestions[nodeId] || fallbackQuestions['symbols-meaning'];
  }

  /**
   * Get all fallback questions
   */
  private static getAllFallbackQuestions(): Record<string, QuizQuestion[]> {
    return {
      'symbols-meaning': [
        {
          question: "What is the primary purpose of symbols?",
          options: ["To represent ideas", "To look pretty", "To confuse", "To take up space"],
          correct: 0,
          explanation: "Symbols are visual representations of ideas, concepts, or objects"
        }
      ]
    };
  }
}