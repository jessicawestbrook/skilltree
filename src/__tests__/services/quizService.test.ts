import { QuizService } from '../../services/quizService';

// Mock supabase client
const mockResult = { data: [], error: null };
const mockLimit = jest.fn(() => Promise.resolve(mockResult));

// Create a mock query object that can be awaited and has methods
const createMockQuery = () => {
  // Create a promise that resolves to the current value of mockResult when awaited
  const query = Promise.resolve().then(() => mockResult);
  query.limit = mockLimit;
  return query;
};

const mockOrder = jest.fn(() => createMockQuery());
const mockEq = jest.fn(() => ({ order: mockOrder }));
const mockSelect = jest.fn(() => ({ eq: mockEq }));

// Create stable mock objects for insert, update, delete
const mockInsertSelect = jest.fn(() => Promise.resolve({ data: null, error: null }));
const mockInsert = jest.fn(() => ({
  select: mockInsertSelect
}));

const mockUpdateSelect = jest.fn(() => Promise.resolve({ data: null, error: null }));
const mockUpdateEq = jest.fn(() => ({
  select: mockUpdateSelect
}));
const mockUpdate = jest.fn(() => ({
  eq: mockUpdateEq
}));

const mockDeleteEq = jest.fn(() => Promise.resolve({ data: null, error: null }));
const mockDelete = jest.fn(() => ({
  eq: mockDeleteEq
}));

const mockFrom = jest.fn(() => ({
  select: mockSelect,
  insert: mockInsert,
  update: mockUpdate,
  delete: mockDelete
}));

const mockSupabaseClient = {
  from: mockFrom
};

jest.mock('../../lib/supabase-client', () => ({
  createClient: jest.fn(() => mockSupabaseClient)
}));

describe('QuizService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.restoreAllMocks();
    mockResult.data = [];
    mockResult.error = null;
  });

  describe('getQuestions', () => {
    it('should fetch questions for a node successfully', async () => {
      const mockDatabaseQuestions = [
        {
          id: '1',
          node_id: 'node123',
          question: 'What is JavaScript?',
          options: ['Language', 'Framework', 'Library', 'Database'],
          correct_answer: 0,
          explanation: 'JavaScript is a programming language'
        },
        {
          id: '2',
          node_id: 'node123',
          question: 'What is React?',
          options: ['Language', 'Framework', 'Library', 'Database'],
          correct_answer: 2,
          explanation: 'React is a JavaScript library'
        }
      ];

      const expectedQuestions = [
        {
          question: 'What is JavaScript?',
          options: ['Language', 'Framework', 'Library', 'Database'],
          correct: 0,
          explanation: 'JavaScript is a programming language'
        },
        {
          question: 'What is React?',
          options: ['Language', 'Framework', 'Library', 'Database'],
          correct: 2,
          explanation: 'React is a JavaScript library'
        }
      ];

      mockResult.data = mockDatabaseQuestions;
      mockResult.error = null;

      const result = await QuizService.getQuestions('node123');

      expect(result).toEqual(expectedQuestions);
      expect(mockFrom).toHaveBeenCalledWith('quiz_questions');
      expect(mockSelect).toHaveBeenCalledWith('*');
    });

    it('should return empty array when no questions found', async () => {
      mockLimit.mockResolvedValueOnce({
        data: [],
        error: null
      });

      const result = await QuizService.getQuestions('node123');

      expect(result).toEqual([]);
    });

    it('should handle database errors', async () => {
      mockLimit.mockResolvedValueOnce({
        data: null,
        error: { message: 'Database error' }
      });

      const result = await QuizService.getQuestions('node123');

      expect(result).toEqual([]);
    });

    it('should limit number of questions returned', async () => {
      const mockQuestions = Array.from({ length: 20 }, (_, i) => ({
        id: `${i + 1}`,
        node_id: 'node123',
        question: `Question ${i + 1}`,
        options: ['A', 'B', 'C', 'D'],
        correct_answer: 0,
        explanation: `Explanation ${i + 1}`
      }));

      mockLimit.mockResolvedValueOnce({
        data: mockQuestions,
        error: null
      });

      await QuizService.getQuestions('node123', 10);

      expect(mockLimit).toHaveBeenCalledWith(10);
    });
  });

  describe('createQuestion', () => {
    it('should create a new question successfully', async () => {
      const newQuestion = {
        node_id: 'node123',
        question: 'What is TypeScript?',
        options: ['Language', 'Framework', 'Library', 'Compiler'],
        correct: 0,
        explanation: 'TypeScript is a programming language'
      };

      const createdQuestionFromDB = {
        id: '3',
        node_id: 'node123',
        question: 'What is TypeScript?',
        options: ['Language', 'Framework', 'Library', 'Compiler'],
        correct_answer: 0,
        explanation: 'TypeScript is a programming language',
        created_at: new Date().toISOString()
      };

      mockInsertSelect.mockResolvedValueOnce({
        data: [createdQuestionFromDB],
        error: null
      });

      const result = await QuizService.createQuestion(newQuestion);

      expect(result).toEqual(createdQuestionFromDB);
      expect(mockFrom).toHaveBeenCalledWith('quiz_questions');
      expect(mockInsert).toHaveBeenCalledWith([{
        node_id: newQuestion.node_id,
        question: newQuestion.question,
        options: newQuestion.options,
        correct_answer: newQuestion.correct,
        explanation: newQuestion.explanation,
        created_at: expect.any(String)
      }]);
    });

    it('should handle creation errors', async () => {
      const newQuestion = {
        node_id: 'node123',
        question: 'What is TypeScript?',
        options: ['Language', 'Framework', 'Library', 'Compiler'],
        correct: 0,
        explanation: 'TypeScript is a programming language'
      };

      mockInsertSelect.mockResolvedValueOnce({
        data: null,
        error: { message: 'Creation failed' }
      });

      const result = await QuizService.createQuestion(newQuestion);

      expect(result).toBeNull();
    });

    it('should validate question data before creation', async () => {
      const invalidQuestion = {
        node_id: '',
        question: '',
        options: [],
        correct: -1,
        explanation: ''
      };

      const result = await QuizService.createQuestion(invalidQuestion);

      expect(result).toBeNull();
      expect(mockInsert).not.toHaveBeenCalled();
    });
  });

  describe('updateQuestion', () => {
    it('should update a question successfully', async () => {
      const updates = {
        question: 'Updated question text',
        explanation: 'Updated explanation'
      };

      const updatedQuestionFromDB = {
        id: '1',
        node_id: 'node123',
        question: 'Updated question text',
        options: ['A', 'B', 'C', 'D'],
        correct_answer: 0,
        explanation: 'Updated explanation',
        updated_at: new Date().toISOString()
      };

      mockUpdateSelect.mockResolvedValueOnce({
        data: [updatedQuestionFromDB],
        error: null
      });

      const result = await QuizService.updateQuestion('1', updates);

      expect(result).toEqual(updatedQuestionFromDB);
      expect(mockFrom).toHaveBeenCalledWith('quiz_questions');
      expect(mockUpdate).toHaveBeenCalledWith({
        question: 'Updated question text',
        explanation: 'Updated explanation',
        updated_at: expect.any(String)
      });
    });

    it('should handle update errors', async () => {
      const updates = { question: 'Updated question' };

      mockUpdateSelect.mockResolvedValueOnce({
        data: null,
        error: { message: 'Update failed' }
      });

      const result = await QuizService.updateQuestion('1', updates);

      expect(result).toBeNull();
    });

    it('should return null for empty updates', async () => {
      const result = await QuizService.updateQuestion('1', {});

      expect(result).toBeNull();
      expect(mockUpdate).not.toHaveBeenCalled();
    });
  });

  describe('deleteQuestion', () => {
    it('should delete a question successfully', async () => {
      mockDeleteEq.mockResolvedValueOnce({
        data: null,
        error: null
      });

      const result = await QuizService.deleteQuestion('1');

      expect(result).toBe(true);
      expect(mockFrom).toHaveBeenCalledWith('quiz_questions');
      expect(mockDelete).toHaveBeenCalled();
      expect(mockDeleteEq).toHaveBeenCalledWith('id', '1');
    });

    it('should handle deletion errors', async () => {
      mockDeleteEq.mockResolvedValueOnce({
        data: null,
        error: { message: 'Deletion failed' }
      });

      const result = await QuizService.deleteQuestion('1');

      expect(result).toBe(false);
    });

    it('should return false for invalid question ID', async () => {
      const result = await QuizService.deleteQuestion('');

      expect(result).toBe(false);
      expect(mockDelete).not.toHaveBeenCalled();
    });
  });

  describe('validateQuestionData', () => {
    it('should validate correct question data', () => {
      const validQuestion = {
        node_id: 'node123',
        question: 'What is JavaScript?',
        options: ['Language', 'Framework', 'Library', 'Database'],
        correct: 0,
        explanation: 'JavaScript is a programming language'
      };

      const result = QuizService.validateQuestionData(validQuestion);
      expect(result).toBe(true);
    });

    it('should reject questions with missing node_id', () => {
      const invalidQuestion = {
        node_id: '',
        question: 'What is JavaScript?',
        options: ['Language', 'Framework', 'Library', 'Database'],
        correct: 0,
        explanation: 'JavaScript is a programming language'
      };

      const result = QuizService.validateQuestionData(invalidQuestion);
      expect(result).toBe(false);
    });

    it('should reject questions with empty question text', () => {
      const invalidQuestion = {
        node_id: 'node123',
        question: '',
        options: ['Language', 'Framework', 'Library', 'Database'],
        correct: 0,
        explanation: 'JavaScript is a programming language'
      };

      const result = QuizService.validateQuestionData(invalidQuestion);
      expect(result).toBe(false);
    });

    it('should reject questions with insufficient options', () => {
      const invalidQuestion = {
        node_id: 'node123',
        question: 'What is JavaScript?',
        options: ['Language'],
        correct: 0,
        explanation: 'JavaScript is a programming language'
      };

      const result = QuizService.validateQuestionData(invalidQuestion);
      expect(result).toBe(false);
    });

    it('should reject questions with invalid correct answer index', () => {
      const invalidQuestion = {
        node_id: 'node123',
        question: 'What is JavaScript?',
        options: ['Language', 'Framework', 'Library', 'Database'],
        correct: 5, // Out of range
        explanation: 'JavaScript is a programming language'
      };

      const result = QuizService.validateQuestionData(invalidQuestion);
      expect(result).toBe(false);
    });

    it('should reject questions with negative correct answer index', () => {
      const invalidQuestion = {
        node_id: 'node123',
        question: 'What is JavaScript?',
        options: ['Language', 'Framework', 'Library', 'Database'],
        correct: -1,
        explanation: 'JavaScript is a programming language'
      };

      const result = QuizService.validateQuestionData(invalidQuestion);
      expect(result).toBe(false);
    });
  });

  describe('getRandomQuestions', () => {
    it('should return random subset of questions', async () => {
      const mockDatabaseQuestions = Array.from({ length: 10 }, (_, i) => ({
        id: `${i + 1}`,
        node_id: 'node123',
        question: `Question ${i + 1}`,
        options: ['A', 'B', 'C', 'D'],
        correct_answer: 0,
        explanation: `Explanation ${i + 1}`
      }));

      // Set the mock data that will be returned
      mockResult.data = mockDatabaseQuestions;
      mockResult.error = null;

      const result = await QuizService.getRandomQuestions('node123', 5);

      expect(result).toHaveLength(5);
      expect(result.every(q => q.question && q.options && q.correct !== undefined && q.explanation)).toBe(true);
    });

    it('should return all questions if requested count exceeds available', async () => {
      const mockDatabaseQuestion = {
        id: '1',
        node_id: 'node123',
        question: 'Question 1',
        options: ['A', 'B', 'C', 'D'],
        correct_answer: 0,
        explanation: 'Explanation 1'
      };

      const expectedQuestion = {
        question: 'Question 1',
        options: ['A', 'B', 'C', 'D'],
        correct: 0,
        explanation: 'Explanation 1'
      };

      // Set the mock data that will be returned
      mockResult.data = [mockDatabaseQuestion];
      mockResult.error = null;

      const result = await QuizService.getRandomQuestions('node123', 5);

      expect(result).toEqual([expectedQuestion]);
    });
  });

  describe('error handling', () => {
    it('should handle network errors gracefully', async () => {
      mockLimit.mockRejectedValueOnce(
        new Error('Network error')
      );

      const result = await QuizService.getQuestions('node123');

      expect(result).toEqual([]);
    });

    it('should handle malformed data gracefully', async () => {
      mockLimit.mockResolvedValueOnce({
        data: [
          { id: '1', question: 'Test' }, // Missing required fields
          null, // Null entry
          undefined // Undefined entry
        ],
        error: null
      });

      const result = await QuizService.getQuestions('node123');

      // Should filter out invalid entries
      expect(result).toEqual([]);
    });
  });
});