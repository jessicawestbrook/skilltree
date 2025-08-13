# Analytics and Insights System

NeuroQuest includes a comprehensive analytics and insights system that tracks user learning behavior, provides personalized recommendations, and offers detailed performance insights.

## Overview

The analytics system consists of several components:

1. **Database Schema** - Tables for storing learning sessions, events, and insights
2. **Analytics Service** - Client-side service for tracking events and managing sessions
3. **API Endpoints** - Server-side APIs for data collection and retrieval
4. **Dashboard Components** - UI components for displaying analytics data
5. **Performance Monitoring** - Real-time performance and error tracking

## Database Schema

### Core Tables

#### `learning_sessions`
Tracks detailed user learning sessions:
- Session start/end times
- Total duration
- Nodes attempted and completed
- Device and browser information

#### `learning_analytics`
Stores granular learning events:
- Event types (quiz_start, quiz_complete, node_visit, etc.)
- Node-specific data
- Custom event data in JSONB format
- Timestamp tracking

#### `weekly_insights`
Aggregated weekly learning summaries:
- Study time and nodes completed
- Quiz accuracy trends
- Domain focus analysis
- Achievement tracking

#### `learning_recommendations`
Personalized learning suggestions:
- Next node recommendations
- Review suggestions for weak areas
- Challenge recommendations
- Priority scoring (1-100)

## Analytics Service

### Core Methods

```typescript
// Session Management
AnalyticsService.startSession()
AnalyticsService.endSession()

// Event Tracking
AnalyticsService.trackEvent(event)
AnalyticsService.trackQuizStart(nodeId, questionCount)
AnalyticsService.trackQuizComplete(nodeId, score, timeSpent, totalQuestions, correctAnswers)
AnalyticsService.trackNodeVisit(nodeId, nodeName)
AnalyticsService.trackContentView(nodeId, contentType, duration)

// Data Retrieval
AnalyticsService.getUserAnalytics(daysBack)
AnalyticsService.getLearningInsights()
AnalyticsService.getRecommendations()
```

### Automatic Tracking

The service automatically tracks:
- Session start/end on page load/unload
- Quiz interactions and completions
- Node visits and content views
- Performance metrics
- JavaScript errors and unhandled rejections

## API Endpoints

### `/api/analytics`

**GET** - Retrieve analytics data
- `?type=summary&days=30` - Get user analytics summary
- `?type=insights` - Get learning insights
- `?type=recommendations` - Get personalized recommendations
- `?type=sessions` - Get recent learning sessions

**POST** - Track analytics events
```json
{
  "event_type": "quiz_complete",
  "node_id": "node_123",
  "event_data": {
    "score": 85,
    "time_spent_seconds": 120
  }
}
```

### `/api/analytics/session`

**POST** - Manage learning sessions
```json
{
  "action": "start" | "end",
  "session_id": "uuid",
  "duration_seconds": 300
}
```

## Analytics Dashboard

### Key Metrics Displayed

1. **Study Time** - Total hours spent learning
2. **Nodes Completed** - Number of knowledge nodes mastered
3. **Average Quiz Score** - Performance across all quizzes
4. **Study Streak** - Consecutive days of learning activity

### Charts and Visualizations

- **Daily Activity Chart** - Study time and progress over time
- **Domain Distribution** - Focus areas and topic preferences
- **Quiz Performance Trend** - Score improvements over time
- **Progress Bars** - Visual representation of goals and achievements

### Learning Insights

The system generates intelligent insights such as:
- Performance improvement suggestions
- Consistency and engagement feedback
- Weak area identification
- Achievement celebrations

### Personalized Recommendations

- **Next Node** - Optimal next learning steps based on prerequisites
- **Review** - Nodes with poor performance scores that need attention
- **Challenge** - Advanced topics to push learning boundaries

## Performance Monitoring

### Tracked Metrics

1. **Web Vitals**
   - First Contentful Paint (FCP)
   - Largest Contentful Paint (LCP)
   - Cumulative Layout Shift (CLS)
   - First Input Delay (FID)
   - Time to Interactive (TTI)

2. **Network Information**
   - Connection type and speed
   - Downlink bandwidth
   - Round-trip time (RTT)

3. **Memory Usage**
   - JavaScript heap usage
   - Memory limits and optimization

4. **Error Tracking**
   - JavaScript errors with stack traces
   - Unhandled promise rejections
   - Performance bottlenecks

## Setup and Configuration

### 1. Database Migration

Run the analytics schema migration:

```bash
npm run migrate:analytics
```

**Note**: The migration requires manual execution in Supabase Dashboard due to complex function definitions.

### 2. Environment Setup

Ensure these environment variables are configured:
- `NEXT_PUBLIC_SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### 3. Client Initialization

Analytics are automatically initialized when users log in:

```typescript
// Automatic initialization
useEffect(() => {
  if (isAuthenticated) {
    AnalyticsService.initialize();
    return () => {
      AnalyticsService.cleanup();
    };
  }
}, [isAuthenticated]);
```

## Data Privacy and Security

### Row Level Security (RLS)

All analytics tables use RLS policies to ensure:
- Users can only access their own data
- Authenticated access is required for all operations
- Data isolation between users

### Data Retention

- Session data: 90 days
- Event data: 1 year
- Insights: 6 months
- Recommendations: 1 week (auto-refresh)

### GDPR Compliance

- Users can request data export via the analytics dashboard
- Data deletion on account closure
- Minimal data collection principle
- Transparent data usage policies

## Usage Examples

### Track Custom Learning Event

```typescript
await AnalyticsService.trackEvent({
  event_type: 'custom_study_method',
  node_id: 'math_algebra',
  event_data: {
    method: 'flashcards',
    duration_minutes: 15,
    effectiveness_rating: 4
  }
});
```

### Get Weekly Progress

```typescript
const analytics = await AnalyticsService.getUserAnalytics(7);
console.log(`This week: ${analytics.total_study_time_hours}h study time`);
```

### Display Recommendations

```typescript
const recommendations = await AnalyticsService.getRecommendations();
recommendations.forEach(rec => {
  console.log(`${rec.recommendation_type}: ${rec.reasoning}`);
});
```

## Monitoring and Debugging

### Client-Side Debugging

Enable detailed logging:
```javascript
localStorage.setItem('analytics_debug', 'true');
```

### Server-Side Monitoring

- API endpoint response times tracked
- Database query performance monitored  
- Error rates and patterns analyzed
- Resource usage optimized

### Analytics Health Check

The system includes self-monitoring to ensure:
- Session tracking accuracy
- Event delivery reliability
- Recommendation freshness
- Performance metric validity

## Future Enhancements

### Planned Features

1. **Predictive Analytics** - ML-powered learning outcome predictions
2. **Social Learning** - Peer comparison and collaborative insights
3. **Adaptive Difficulty** - Dynamic content difficulty based on performance
4. **Learning Path Optimization** - AI-optimized learning sequences
5. **Real-time Notifications** - Instant feedback and suggestions
6. **Advanced Visualizations** - Interactive charts and progress maps

### Integration Opportunities

- Learning Management System (LMS) compatibility
- Third-party analytics tools (Google Analytics, Mixpanel)
- Mobile app analytics synchronization
- Accessibility analytics and improvements