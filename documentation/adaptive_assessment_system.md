# Computer Adaptive Testing (CAT) System Design

## Overview

This document outlines the design for a computer adaptive testing system that adjusts question difficulty based on user performance and awards points based on both correct answers and difficulty levels achieved.

## Core Principles

### 1. Computer Adaptive Testing (CAT)
- **Dynamic Difficulty Adjustment**: Questions get harder after correct answers, easier after incorrect ones
- **Efficient Assessment**: Reaches accurate ability estimates with fewer questions
- **Personalized Experience**: Each user gets a unique question sequence based on their responses
- **Early Termination**: Users can quit at any time while still earning meaningful points

### 2. Difficulty-Based Point System
- **Consistent Scoring**: Points reflect actual demonstrated ability regardless of question bank changes
- **Comparable Across Categories**: Same difficulty level = same base points across all subjects
- **Incremental Rewards**: More questions answered = more opportunities for points
- **Quality over Quantity**: Higher difficulty questions worth more points

## Difficulty Levels

### Standard 5-Level System
```
Level 1: Beginner      (Base: 10 points)
Level 2: Elementary    (Base: 25 points) 
Level 3: Intermediate  (Base: 50 points)
Level 4: Advanced      (Base: 100 points)
Level 5: Expert        (Base: 200 points)
```

### Point Multipliers
- **Correct Answer**: Full points for the difficulty level
- **Consecutive Correct**: 1.1x multiplier for 3+ consecutive correct answers
- **Quick Response**: 1.05x multiplier for answers within 15 seconds
- **Repeat Questions**: No points for answering questions already answered correctly

## Adaptive Algorithm

### Starting Point
- **New Users**: Start at Level 2 (Elementary)
- **Returning Users**: Start at last demonstrated level - 1
- **Category-Specific**: Each subject area maintains separate ability estimates

### Question Selection Rules
1. **Select difficulty** based on current ability estimate
2. **Prioritize new questions** that user hasn't answered correctly before
3. **Include previously incorrect questions** for redemption opportunities
4. **Fall back** to adjacent difficulty levels if needed
5. **Track response patterns** to avoid repetitive content within same session

### Difficulty Adjustment Logic
```javascript
// After each response:
if (correct) {
  if (consecutiveCorrect >= 2) {
    increaseDifficulty()
  }
  abilityEstimate += difficultyPoints * 0.1
} else {
  if (consecutiveIncorrect >= 1) {
    decreaseDifficulty()
  }
  abilityEstimate -= difficultyPoints * 0.15
}
```

### Termination Conditions
- **User Choice**: User can quit after any question
- **Confidence Reached**: Standard error drops below threshold (optional)
- **Maximum Questions**: Hard cap at 50 questions per session
- **Time Limit**: Optional 30-minute session limit

## Point Calculation System

### Base Point Formula
```
Question Points = Base Points × Multipliers
```

### Repeat Question Scoring
- **First Time Correct**: Full base points + applicable multipliers
- **Previously Correct Questions**: 0 points (no points for questions already answered correctly)
- **Previously Incorrect Questions**: Full points if answered correctly (redemption opportunity)
- **Learning Focus**: Encourages exploring new content and mastering previously missed material

### Session Score Calculation
```
Total Points = Sum of all question points in session
```

### Category Score Calculation
```
Category Score = Sum of best session scores + Bonus for consistency
```

### Cross-Category Comparison
Since all categories use the same difficulty scale and point values:
- Mathematics Level 3 = 50 points = Science Level 3 = 50 points
- Direct comparison of ability across subjects
- Meaningful aggregation for overall skill assessment

## Database Schema Requirements

### Assessment Sessions Table
```sql
assessment_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  category_id UUID REFERENCES skill_tree_nodes(id),
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  total_points INTEGER,
  questions_answered INTEGER,
  highest_difficulty_reached INTEGER,
  final_ability_estimate DECIMAL(5,2),
  session_type VARCHAR(20) -- 'practice', 'assessment', 'quick_test'
)
```

### Question Responses Table
```sql
question_responses (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES assessment_sessions(id),
  question_id UUID REFERENCES questions(id),
  user_response TEXT,
  is_correct BOOLEAN,
  response_time_ms INTEGER,
  difficulty_level INTEGER,
  points_earned INTEGER,
  question_sequence INTEGER,
  answered_at TIMESTAMP
)
```

### User Category Scores Table
```sql
user_category_scores (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  category_id UUID REFERENCES skill_tree_nodes(id),
  current_ability_estimate DECIMAL(5,2),
  total_points INTEGER,
  best_session_points INTEGER,
  questions_answered_total INTEGER,
  last_assessment_date TIMESTAMP,
  mastery_level INTEGER, -- 1-5 based on demonstrated ability
  updated_at TIMESTAMP
)
```

### Questions Table Enhancement
```sql
-- Add to existing questions table:
ALTER TABLE questions ADD COLUMN difficulty_level INTEGER DEFAULT 2;
ALTER TABLE questions ADD COLUMN estimated_time_seconds INTEGER DEFAULT 60;
ALTER TABLE questions ADD COLUMN cognitive_load_rating INTEGER DEFAULT 3;
```

## Implementation Strategy

### Phase 1: Core Algorithm
1. Implement basic CAT algorithm for question selection
2. Create point calculation system
3. Build session management

### Phase 2: User Interface
1. Design adaptive assessment interface
2. Real-time scoring display
3. Progress indicators and feedback

### Phase 3: Analytics & Optimization
1. Performance tracking and analytics
2. Algorithm tuning based on user data
3. Question difficulty calibration

### Phase 4: Advanced Features
1. Multi-dimensional adaptive testing (multiple skills per question)
2. Learning progress prediction
3. Personalized study recommendations

## User Experience Design

### Assessment Flow
1. **Start Screen**: Category selection, difficulty preview, time estimate
2. **Question Display**: Clean interface with progress indicator
3. **Immediate Feedback**: Correct/incorrect with brief explanation
4. **Real-time Scoring**: Current points and difficulty level shown
5. **Flexible Exit**: "Stop Assessment" button always available
6. **Results Summary**: Points earned, difficulty reached, next steps

### Motivation Elements
- **Progress Visualization**: Difficulty level climbed during session
- **Point Accumulation**: Running total with celebration animations
- **Achievement Badges**: First time reaching each difficulty level
- **Leaderboards**: Optional comparison with other users (anonymous)
- **Personal Bests**: Track improvement over time

## Quality Assurance

### Algorithm Testing
- **Simulation Studies**: Test with known ability levels
- **Bias Detection**: Ensure fairness across different user groups
- **Reliability Testing**: Consistent results across multiple sessions
- **Performance Monitoring**: Response times and system load

### Content Quality
- **Question Calibration**: Regular review of difficulty ratings
- **Expert Review**: Subject matter experts validate question quality
- **User Feedback**: Flag inappropriate or confusing questions
- **Statistical Analysis**: Item response theory to optimize questions

## Success Metrics

### User Engagement
- **Session Completion Rate**: Percentage who finish vs. quit early
- **Return Rate**: Users coming back for more assessments
- **Time Spent**: Average session duration and engagement
- **User Satisfaction**: Surveys and feedback scores

### System Effectiveness
- **Accuracy**: How well estimated ability predicts performance
- **Efficiency**: Questions needed to reach reliable estimate
- **Fairness**: Equal opportunity across different user groups
- **Stability**: Consistent estimates across sessions

---

*Version: 1.0*  
*Created: 2025-08-21*  
*Next Review: 2025-09-21*