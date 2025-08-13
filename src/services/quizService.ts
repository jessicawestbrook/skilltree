import { supabase } from '../lib/supabase';
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
   * Batch add multiple questions to Supabase
   */
  static async batchAddQuestions(questions: Array<{ nodeId: string; question: QuizQuestion }>): Promise<{ success: boolean; inserted: number; errors: string[] }> {
    const errors: string[] = [];
    let insertedCount = 0;

    try {
      const questionsToInsert = questions.map(q => ({
        node_id: q.nodeId,
        question: q.question.question,
        options: q.question.options,
        correct_answer: q.question.correct,
        explanation: q.question.explanation,
        created_at: new Date().toISOString()
      }));

      const { data, error } = await supabase
        .from('quiz_questions')
        .insert(questionsToInsert)
        .select();

      if (error) {
        errors.push(`Database error: ${error.message}`);
        return { success: false, inserted: 0, errors };
      }

      insertedCount = data?.length || 0;
      return { success: true, inserted: insertedCount, errors };
    } catch (err) {
      errors.push(`Error in batchAddQuestions: ${err}`);
      return { success: false, inserted: insertedCount, errors };
    }
  }

  /**
   * Batch update multiple questions
   */
  static async batchUpdateQuestions(updates: Array<{ id: string; updates: Partial<QuizQuestion> }>): Promise<{ success: boolean; updated: number; errors: string[] }> {
    const errors: string[] = [];
    let updatedCount = 0;

    try {
      for (const update of updates) {
        const updateData: Record<string, string | string[] | number | Date> = {
          updated_at: new Date().toISOString()
        };

        if (update.updates.question) updateData.question = update.updates.question;
        if (update.updates.options) updateData.options = update.updates.options;
        if (update.updates.correct !== undefined) updateData.correct_answer = update.updates.correct;
        if (update.updates.explanation) updateData.explanation = update.updates.explanation;

        const { error } = await supabase
          .from('quiz_questions')
          .update(updateData)
          .eq('id', update.id);

        if (error) {
          errors.push(`Failed to update question ${update.id}: ${error.message}`);
        } else {
          updatedCount++;
        }
      }

      return { 
        success: errors.length === 0, 
        updated: updatedCount, 
        errors 
      };
    } catch (err) {
      errors.push(`Error in batchUpdateQuestions: ${err}`);
      return { success: false, updated: updatedCount, errors };
    }
  }

  /**
   * Batch delete multiple questions
   */
  static async batchDeleteQuestions(questionIds: string[]): Promise<{ success: boolean; deleted: number; errors: string[] }> {
    const errors: string[] = [];

    try {
      const { data, error } = await supabase
        .from('quiz_questions')
        .delete()
        .in('id', questionIds)
        .select();

      if (error) {
        errors.push(`Database error: ${error.message}`);
        return { success: false, deleted: 0, errors };
      }

      return { success: true, deleted: data?.length || 0, errors };
    } catch (err) {
      errors.push(`Error in batchDeleteQuestions: ${err}`);
      return { success: false, deleted: 0, errors };
    }
  }

  /**
   * Load questions from JSON format
   */
  static async loadQuestionsFromJSON(jsonData: any): Promise<{ success: boolean; loaded: number; errors: string[] }> {
    const errors: string[] = [];
    const questionsToAdd: Array<{ nodeId: string; question: QuizQuestion }> = [];

    try {
      // Handle different JSON formats
      if (Array.isArray(jsonData)) {
        // Array of questions with nodeId
        for (const item of jsonData) {
          if (!item.nodeId || !item.question) {
            errors.push(`Invalid question format: missing nodeId or question`);
            continue;
          }
          questionsToAdd.push({
            nodeId: item.nodeId,
            question: {
              question: item.question.question || item.question,
              options: item.question.options || item.options,
              correct: item.question.correct !== undefined ? item.question.correct : item.correct,
              explanation: item.question.explanation || item.explanation || ''
            }
          });
        }
      } else if (typeof jsonData === 'object') {
        // Object with nodeId as keys
        for (const [nodeId, questions] of Object.entries(jsonData)) {
          if (!Array.isArray(questions)) {
            errors.push(`Invalid format for node ${nodeId}: expected array of questions`);
            continue;
          }
          for (const q of questions) {
            questionsToAdd.push({
              nodeId,
              question: {
                question: q.question,
                options: q.options,
                correct: q.correct,
                explanation: q.explanation || ''
              }
            });
          }
        }
      } else {
        errors.push('Invalid JSON format: expected array or object');
        return { success: false, loaded: 0, errors };
      }

      if (questionsToAdd.length === 0) {
        errors.push('No valid questions found in JSON data');
        return { success: false, loaded: 0, errors };
      }

      // Batch insert the questions
      const result = await this.batchAddQuestions(questionsToAdd);
      return {
        success: result.success,
        loaded: result.inserted,
        errors: [...errors, ...result.errors]
      };
    } catch (err) {
      errors.push(`Error parsing JSON: ${err}`);
      return { success: false, loaded: 0, errors };
    }
  }

  /**
   * Load questions from CSV format
   */
  static async loadQuestionsFromCSV(csvData: string): Promise<{ success: boolean; loaded: number; errors: string[] }> {
    const errors: string[] = [];
    const questionsToAdd: Array<{ nodeId: string; question: QuizQuestion }> = [];

    try {
      const lines = csvData.trim().split('\n');
      if (lines.length < 2) {
        errors.push('CSV file is empty or has no data rows');
        return { success: false, loaded: 0, errors };
      }

      // Parse header
      const header = lines[0].split(',').map(h => h.trim().toLowerCase());
      const requiredFields = ['nodeid', 'question', 'option1', 'option2', 'option3', 'option4', 'correct'];
      
      const fieldIndices: Record<string, number> = {};
      for (const field of requiredFields) {
        const index = header.findIndex(h => h.replace(/[_\s-]/g, '') === field.replace(/[_\s-]/g, ''));
        if (index === -1 && field !== 'nodeid') {
          // Try alternative names for nodeId
          if (field === 'nodeid') {
            const altIndex = header.findIndex(h => h === 'node_id' || h === 'node');
            if (altIndex !== -1) {
              fieldIndices[field] = altIndex;
              continue;
            }
          }
          errors.push(`Missing required field in CSV header: ${field}`);
          return { success: false, loaded: 0, errors };
        }
        fieldIndices[field] = index;
      }

      // Find explanation field (optional)
      const explanationIndex = header.findIndex(h => h === 'explanation' || h === 'hint');

      // Parse data rows
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim());
        
        if (values.length < header.length) {
          errors.push(`Row ${i + 1}: Insufficient values`);
          continue;
        }

        const nodeId = values[fieldIndices['nodeid']];
        const question = values[fieldIndices['question']];
        const options = [
          values[fieldIndices['option1']],
          values[fieldIndices['option2']],
          values[fieldIndices['option3']],
          values[fieldIndices['option4']]
        ];
        const correct = parseInt(values[fieldIndices['correct']]);
        const explanation = explanationIndex !== -1 ? values[explanationIndex] : '';

        if (!nodeId || !question || options.some(o => !o) || isNaN(correct) || correct < 0 || correct > 3) {
          errors.push(`Row ${i + 1}: Invalid data`);
          continue;
        }

        questionsToAdd.push({
          nodeId,
          question: {
            question,
            options,
            correct,
            explanation
          }
        });
      }

      if (questionsToAdd.length === 0) {
        errors.push('No valid questions found in CSV data');
        return { success: false, loaded: 0, errors };
      }

      // Batch insert the questions
      const result = await this.batchAddQuestions(questionsToAdd);
      return {
        success: result.success,
        loaded: result.inserted,
        errors: [...errors, ...result.errors]
      };
    } catch (err) {
      errors.push(`Error parsing CSV: ${err}`);
      return { success: false, loaded: 0, errors };
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