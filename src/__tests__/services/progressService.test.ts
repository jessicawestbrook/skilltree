import { ProgressService, ProgressSubmission, UserProgress } from '../../services/progressService';

// Mock fetch
global.fetch = jest.fn();
const mockFetch = global.fetch as jest.MockedFunction<typeof fetch>;

// Mock supabase
jest.mock('../../lib/supabase', () => ({
  supabase: {
    auth: {
      getUser: jest.fn()
    },
    from: jest.fn().mockReturnThis(),
    select: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    order: jest.fn().mockReturnThis(),
    single: jest.fn().mockReturnThis(),
    rpc: jest.fn()
  }
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

      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      } as Response);

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

      mockFetch.mockResolvedValue({
        ok: false,
        json: () => Promise.resolve(mockErrorResponse)
      } as Response);

      const result = await ProgressService.submitProgress(mockProgressData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid data');
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

      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: [mockProgress] })
      } as Response);

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
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: [] })
      } as Response);

      const result = await ProgressService.getNodeProgress('node1');
      expect(result).toBeNull();
    });

    it('should handle fetch errors', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        json: () => Promise.resolve({ error: 'Not found' })
      } as Response);

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

      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: mockProgressList })
      } as Response);

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
  });
});