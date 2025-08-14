import { AnalyticsService } from '../../services/analyticsService';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock as any;

// Mock window.gtag
const mockGtag = jest.fn();
(global as any).gtag = mockGtag;

// Mock performance API
const mockPerformance = {
  now: jest.fn(() => 1000),
  mark: jest.fn(),
  measure: jest.fn(),
  getEntriesByType: jest.fn(() => []),
};
(global as any).performance = mockPerformance;

describe('AnalyticsService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
    mockPerformance.now.mockReturnValue(1000);
  });

  describe('initialization', () => {
    it('should initialize analytics service', () => {
      expect(() => AnalyticsService.initialize()).not.toThrow();
    });

    it('should cleanup analytics service', () => {
      expect(() => AnalyticsService.cleanup()).not.toThrow();
    });
  });

  describe('session management', () => {
    it('should start a new session', () => {
      const sessionId = AnalyticsService.startSession();
      
      expect(sessionId).toBeDefined();
      expect(typeof sessionId).toBe('string');
      expect(sessionId.length).toBeGreaterThan(0);
    });

    it('should end a session', () => {
      const sessionId = AnalyticsService.startSession();
      
      expect(() => AnalyticsService.endSession(sessionId)).not.toThrow();
    });

    it('should get current session', () => {
      const session = AnalyticsService.getCurrentSession();
      
      expect(session).toBeDefined();
      expect(session).toHaveProperty('id');
      expect(session).toHaveProperty('startTime');
    });
  });

  describe('event tracking', () => {
    it('should track page view', () => {
      AnalyticsService.trackPageView('/test-page', 'Test Page');
      
      expect(mockGtag).toHaveBeenCalledWith('config', expect.any(String), {
        page_title: 'Test Page',
        page_location: '/test-page'
      });
    });

    it('should track custom events', () => {
      AnalyticsService.trackEvent('test_event', {
        category: 'test',
        action: 'click',
        label: 'test_button'
      });
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'test_event', {
        category: 'test',
        action: 'click',
        label: 'test_button'
      });
    });

    it('should track node completion', () => {
      AnalyticsService.trackNodeCompletion('node123', 100, 85, 120);
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'node_completed', {
        event_category: 'learning',
        node_id: 'node123',
        points_earned: 100,
        quiz_score: 85,
        time_spent: 120
      });
    });

    it('should track learning path started', () => {
      AnalyticsService.trackLearningPathStarted('path123', 'JavaScript Basics');
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'learning_path_started', {
        event_category: 'learning',
        path_id: 'path123',
        path_name: 'JavaScript Basics'
      });
    });

    it('should track quiz attempt', () => {
      AnalyticsService.trackQuizAttempt('node123', 5, 4, 85);
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'quiz_attempt', {
        event_category: 'learning',
        node_id: 'node123',
        total_questions: 5,
        correct_answers: 4,
        score_percentage: 85
      });
    });

    it('should track feature usage', () => {
      AnalyticsService.trackFeatureUsage('search', { query: 'javascript' });
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'feature_used', {
        event_category: 'engagement',
        feature_name: 'search',
        metadata: { query: 'javascript' }
      });
    });

    it('should track errors', () => {
      const error = new Error('Test error');
      AnalyticsService.trackError(error, 'test_context');
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'exception', {
        description: 'Test error',
        fatal: false,
        context: 'test_context'
      });
    });
  });

  describe('performance tracking', () => {
    it('should track performance metrics', () => {
      AnalyticsService.trackPerformance('page_load', 1500);
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'timing_complete', {
        name: 'page_load',
        value: 1500
      });
    });

    it('should track user engagement time', () => {
      AnalyticsService.trackEngagementTime(300);
      
      expect(mockGtag).toHaveBeenCalledWith('event', 'user_engagement', {
        engagement_time_msec: 300000
      });
    });
  });

  describe('user properties', () => {
    it('should set user properties', () => {
      AnalyticsService.setUserProperties({
        user_type: 'premium',
        signup_date: '2024-01-01'
      });
      
      expect(mockGtag).toHaveBeenCalledWith('config', expect.any(String), {
        custom_map: {
          user_type: 'premium',
          signup_date: '2024-01-01'
        }
      });
    });

    it('should identify user', () => {
      AnalyticsService.identifyUser('user123', {
        email: 'test@example.com',
        plan: 'free'
      });
      
      expect(mockGtag).toHaveBeenCalledWith('config', expect.any(String), {
        user_id: 'user123',
        custom_map: {
          email: 'test@example.com',
          plan: 'free'
        }
      });
    });
  });

  describe('data collection consent', () => {
    it('should handle consent granted', () => {
      AnalyticsService.setConsentGranted(true);
      
      expect(mockGtag).toHaveBeenCalledWith('consent', 'update', {
        analytics_storage: 'granted'
      });
    });

    it('should handle consent denied', () => {
      AnalyticsService.setConsentGranted(false);
      
      expect(mockGtag).toHaveBeenCalledWith('consent', 'update', {
        analytics_storage: 'denied'
      });
    });
  });

  describe('error handling', () => {
    it('should handle gtag not available', () => {
      delete (global as any).gtag;
      
      expect(() => {
        AnalyticsService.trackEvent('test_event', {});
      }).not.toThrow();
    });

    it('should handle performance API not available', () => {
      delete (global as any).performance;
      
      expect(() => {
        AnalyticsService.trackPerformance('test_metric', 100);
      }).not.toThrow();
    });
  });
});