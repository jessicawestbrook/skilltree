import { ProgressService, ProgressSubmission, UserProgress } from '../../services/progressService';

// Mock fetch
global.fetch = jest.fn();
const mockFetch = global.fetch as jest.MockedFunction<typeof fetch>;

// Helper to create mock response
const createMockResponse = (data: any, ok: boolean = true, status: number = 200) => ({
  ok,
  status,
  headers: {
    get: (name: string) => name === 'content-type' ? 'application/json' : null
  },
  json: () => Promise.resolve(data),
  text: () => Promise.resolve(JSON.stringify(data))
});

// Mock supabase client
const mockSupabaseClient = {
  auth: {
    getUser: jest.fn()
  },
  from: jest.fn(() => ({
    select: jest.fn(() => ({
      eq: jest.fn(() => ({
        order: jest.fn(() => ({
          single: jest.fn()
        }))
      }))
    }))
  })),
  rpc: jest.fn()
};

jest.mock('../../lib/supabase-client', () => ({
  createClient: jest.fn(() => mockSupabaseClient)
}));

describe('ProgressService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('submitProgress', () => {
    const mockProgressData: ProgressSubmission = {
      nodeId: 'node1',
      quiz_score: 85,
      time_spent_seconds: 120
    };

    it('should submit progress successfully', async () => {
      const mockResponse = {
        success: true,
        data: {
          id: '1',
          user_id: 'user1',
          node_id: 'node1',
          completed_at: '2023-01-01T00:00:00Z',
          points_earned: 100,
          quiz_score: 85,
          time_spent_seconds: 120
        }
      };

      mockFetch.mockResolvedValue(createMockResponse(mockResponse) as any);

      const result = await ProgressService.submitProgress(mockProgressData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResponse.data);
      expect(mockFetch).toHaveBeenCalledWith('/api/progress', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(mockProgressData),
      });
    });

    it('should handle submission errors', async () => {
      const mockErrorResponse = {
        error: 'Invalid data'
      };

      mockFetch.mockResolvedValue(createMockResponse(mockErrorResponse, false, 400) as any);

      const result = await ProgressService.submitProgress(mockProgressData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('HTTP 400: {"error":"Invalid data"}');
    });

    it('should handle network errors', async () => {
      mockFetch.mockRejectedValue(new Error('Network error'));

      const result = await ProgressService.submitProgress(mockProgressData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Network error');
    });
  });

  describe('getNodeProgress', () => {
    it('should fetch node progress successfully', async () => {
      const mockProgress: UserProgress = {
        id: '1',
        user_id: 'user1',
        node_id: 'node1',
        completed_at: '2023-01-01T00:00:00Z',
        points_earned: 100,
        quiz_score: 85,
        time_spent_seconds: 120
      };

      mockFetch.mockResolvedValue(createMockResponse({ data: [mockProgress] }) as any);

      const result = await ProgressService.getNodeProgress('node1');

      expect(result).toEqual(mockProgress);
      expect(mockFetch).toHaveBeenCalledWith('/api/progress?nodeId=node1', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    });

    it('should return null when no progress found', async () => {
      mockFetch.mockResolvedValue(createMockResponse({ data: [] }) as any);

      const result = await ProgressService.getNodeProgress('node1');
      expect(result).toBeNull();
    });

    it('should handle fetch errors', async () => {
      mockFetch.mockResolvedValue(createMockResponse({ error: 'Not found' }, false) as any);

      const result = await ProgressService.getNodeProgress('node1');
      expect(result).toBeNull();
    });
  });

  describe('getAllProgress', () => {
    it('should fetch all progress successfully', async () => {
      const mockProgressList: UserProgress[] = [
        {
          id: '1',
          user_id: 'user1',
          node_id: 'node1',
          completed_at: '2023-01-01T00:00:00Z',
          points_earned: 100,
          quiz_score: 85,
          time_spent_seconds: 120
        },
        {
          id: '2',
          user_id: 'user1',
          node_id: 'node2',
          completed_at: '2023-01-02T00:00:00Z',
          points_earned: 90,
          quiz_score: 78,
          time_spent_seconds: 150
        }
      ];

      mockFetch.mockResolvedValue(createMockResponse({ data: mockProgressList }) as any);

      const result = await ProgressService.getAllProgress();

      expect(result).toEqual(mockProgressList);
      expect(mockFetch).toHaveBeenCalledWith('/api/progress', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    });

    it('should return empty array on error', async () => {
      mockFetch.mockRejectedValue(new Error('Network error'));

      const result = await ProgressService.getAllProgress();
      expect(result).toEqual([]);
    });
  });

  describe('calculateTimeSpent', () => {
    it('should calculate time spent correctly', () => {
      const startTime = new Date('2023-01-01T10:00:00Z');
      const endTime = new Date('2023-01-01T10:02:00Z'); // 2 minutes later
      
      // Mock Date.now to return the end time
      jest.spyOn(global, 'Date').mockImplementation(() => endTime as any);

      const timeSpent = ProgressService.calculateTimeSpent(startTime);
      
      expect(timeSpent).toBe(120); // 2 minutes = 120 seconds

      // Restore Date
      (global.Date as any).mockRestore();
    });

    it('should handle fractional seconds', () => {
      const startTime = new Date('2023-01-01T10:00:00.000Z');
      const endTime = new Date('2023-01-01T10:00:01.500Z'); // 1.5 seconds later
      
      jest.spyOn(global, 'Date').mockImplementation(() => endTime as any);

      const timeSpent = ProgressService.calculateTimeSpent(startTime);
      
      expect(timeSpent).toBe(2); // Rounded to 2 seconds

      (global.Date as any).mockRestore();
    });

    it('should handle invalid start time', () => {
      const invalidDate = new Date('invalid');
      
      expect(() => {
        ProgressService.calculateTimeSpent(invalidDate);
      }).not.toThrow();
      
      const result = ProgressService.calculateTimeSpent(invalidDate);
      expect(typeof result).toBe('number');
    });
  });

  describe('Error handling and edge cases', () => {
    it('should handle network timeout errors', async () => {
      mockFetch.mockImplementation(() => 
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Request timeout')), 100)
        )
      );

      const result = await ProgressService.submitProgress({
        nodeId: 'node1',
        quiz_score: 85,
        time_spent_seconds: 120
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('Request timeout');
    });

    it('should handle malformed JSON responses', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        headers: {
          get: (name: string) => name === 'content-type' ? 'application/json' : null
        },
        json: () => Promise.reject(new Error('Invalid JSON')),
        text: () => Promise.resolve('{"invalid json}')
      } as any);

      const result = await ProgressService.submitProgress({
        nodeId: 'node1',
        quiz_score: 85,
        time_spent_seconds: 120
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid JSON');
    });

    it('should handle server errors with status codes', async () => {
      mockFetch.mockResolvedValue(createMockResponse({ error: 'Internal server error' }, false, 500) as any);

      const result = await ProgressService.submitProgress({
        nodeId: 'node1',
        quiz_score: 85,
        time_spent_seconds: 120
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('HTTP 500: {"error":"Internal server error"}');
    });

    it('should handle empty or null responses gracefully', async () => {
      mockFetch.mockResolvedValue(createMockResponse({ data: null }) as any);

      const result = await ProgressService.getAllProgress();
      expect(result).toEqual([]);
    });

    it('should handle extremely large progress data', async () => {
      const largeProgressData = {
        nodeId: 'node1',
        quiz_score: 100,
        time_spent_seconds: Number.MAX_SAFE_INTEGER
      };

      mockFetch.mockResolvedValue(createMockResponse({ success: true, data: largeProgressData }) as any);

      const result = await ProgressService.submitProgress(largeProgressData);
      expect(result.success).toBe(true);
    });

    it('should validate progress submission data', async () => {
      const invalidProgressData = {
        nodeId: '',
        quiz_score: -10,
        time_spent_seconds: -5
      };

      mockFetch.mockResolvedValue(createMockResponse({ error: 'Invalid progress data' }, false, 400) as any);

      const result = await ProgressService.submitProgress(invalidProgressData);
      expect(result.success).toBe(false);
      expect(result.error).toBe('HTTP 400: {"error":"Invalid progress data"}');
    });

    it('should handle concurrent progress submissions', async () => {
      const mockProgressData = {
        nodeId: 'node1',
        quiz_score: 85,
        time_spent_seconds: 120
      };

      mockFetch.mockResolvedValue(createMockResponse({ success: true, data: mockProgressData }) as any);

      // Submit multiple requests concurrently
      const promises = Array.from({ length: 5 }, () => 
        ProgressService.submitProgress(mockProgressData)
      );

      const results = await Promise.all(promises);
      
      // All should succeed
      results.forEach(result => {
        expect(result.success).toBe(true);
      });

      // Verify all calls were made
      expect(mockFetch).toHaveBeenCalledTimes(5);
    });
  });
});