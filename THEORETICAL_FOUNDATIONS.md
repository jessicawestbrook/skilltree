# SkillTree Theoretical Foundations Document

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Learning Theory Framework](#learning-theory-framework)
3. [User Competency Rating System](#user-competency-rating-system)
4. [Assessment and Testing Theory](#assessment-and-testing-theory)
5. [Recommendation Algorithm Design](#recommendation-algorithm-design)
6. [Implementation Specifications](#implementation-specifications)
7. [References](#references)

## Executive Summary

This document outlines the theoretical foundations for implementing educationally sound features in the SkillTree platform. The recommendations are based on established educational theories, cognitive science research, and modern adaptive learning methodologies.

## Learning Theory Framework

### Constructivist Approach
The SkillTree platform employs a **constructivist learning approach** where learners build knowledge through active engagement rather than passive reception. This is implemented through:

- **Pre-quiz assessments** to activate prior knowledge (Ausubel, 1968)
- **Interactive learning modules** that require active participation
- **Immediate feedback** on assessments to reinforce learning

### Cognitive Load Theory
Based on Sweller's Cognitive Load Theory (1988), we optimize learning by:

- **Chunking content** into 10-30 minute modules (intrinsic load management)
- **Progressive difficulty** levels to avoid overwhelming learners
- **Multimedia integration** with images to support dual-channel processing (Mayer, 2009)

### Mastery Learning
Following Bloom's Mastery Learning model (1968):

- **100% accuracy requirement** for topic mastery ensures complete understanding
- **Multiple attempt opportunities** allow learners to achieve mastery at their own pace
- **Prerequisite tracking** ensures foundational knowledge before advancing

## User Competency Rating System

### Multi-Dimensional Rating Model

The competency rating system uses a weighted composite score based on:

```
Overall Rating = (0.4 × Accuracy) + (0.3 × Consistency) + (0.2 × Difficulty) + (0.1 × Speed)
```

Where:
- **Accuracy**: Percentage of correct answers (0-100)
- **Consistency**: Standard deviation of performance across attempts
- **Difficulty**: Weighted average of question difficulty levels attempted
- **Speed**: Time efficiency compared to estimated completion time

### Rating Levels

Based on educational assessment standards (Webb's Depth of Knowledge):

| Rating Range | Level | Description |
|-------------|-------|-------------|
| 90-100 | Expert | Can teach others, creates connections between concepts |
| 80-89 | Proficient | Applies knowledge in various contexts |
| 70-79 | Competent | Understands and can apply in familiar contexts |
| 60-69 | Developing | Basic understanding with some gaps |
| 0-59 | Novice | Beginning to understand fundamentals |

### Dynamic Rating Adjustment

Ratings adjust based on:
1. **Recency weighting**: Recent performance weighted more heavily (exponential decay factor of 0.9)
2. **Confidence intervals**: Ratings become more reliable with more data points
3. **Forgetting curve**: Ratings decay over time without practice (Ebbinghaus, 1885)

## Assessment and Testing Theory

### Pre-Quiz Design (Diagnostic Assessment)

**Purpose**: Activate prior knowledge and assess readiness
- **3 questions** covering key prerequisites
- **No penalty** for incorrect answers
- **Immediate feedback** with explanations

### Node Test Design (Summative Assessment)

**Purpose**: Verify mastery of learning objectives
- **Minimum 5 questions** per node (increases with complexity)
- **Question selection algorithm**:
  ```
  1. Prioritize unviewed questions
  2. Include previously incorrect questions (spaced repetition)
  3. Balance difficulty levels
  ```
- **Pass requirement**: 100% accuracy for mastery badge

### Question Tracking System

Track for each user-question pair:
- View count
- Attempt history (correct/incorrect)
- Time to answer
- Last seen date

Use this data for:
- **Spaced repetition scheduling** (Leitner system)
- **Difficulty calibration** (Item Response Theory)
- **Personalized question selection**

## Recommendation Algorithm Design

### Content Recommendation Engine

Based on **Zone of Proximal Development** (Vygotsky, 1978):

```python
def calculate_recommendation_score(node, user):
    # Factors and weights
    readiness = calculate_readiness(node.prerequisites, user.completed) * 0.35
    interest = calculate_interest_match(node.category, user.starred) * 0.25
    difficulty_fit = calculate_difficulty_fit(node.level, user.rating) * 0.20
    recency = calculate_topic_recency(node.category, user.history) * 0.10
    completion_path = calculate_path_efficiency(node, user.goals) * 0.10
    
    return readiness + interest + difficulty_fit + recency + completion_path
```

### Recommendation Categories

1. **Ready to Learn**: Prerequisites met, appropriate difficulty
2. **Challenge Yourself**: Slightly above current level
3. **Review & Strengthen**: Previously learned, needs reinforcement
4. **Interest Exploration**: Based on starred categories
5. **Skill Gaps**: Important prerequisites for starred content

### Intro Skill Assessment Test

**Adaptive Testing Implementation**:
- Start with medium difficulty questions
- Adjust difficulty based on performance:
  - Correct answer → increase difficulty by 0.5 levels
  - Incorrect answer → decrease difficulty by 0.7 levels
- Stop after 20 questions or confidence interval < 5%

**Coverage Areas**:
- Mathematics (numerical, algebraic, geometric reasoning)
- Verbal (vocabulary, reading comprehension, analogies)
- Logical (pattern recognition, deductive reasoning)
- Spatial (visualization, rotation, relationships)

## Implementation Specifications

### Learning Content Modal with Pre-Quiz

```typescript
interface LearningSession {
  phases: ['pre-quiz', 'content', 'test', 'results'];
  
  preQuiz: {
    questions: Question[3]; // Exactly 3 questions
    purpose: 'diagnostic';
    scoring: 'informational'; // No pass/fail
  };
  
  content: {
    displayTime: number; // Minimum time before test available
    images: Image[];
    interactionPoints: InteractionPoint[]; // Click to reveal, hover info
  };
  
  test: {
    questions: Question[]; // 5-20 based on content complexity
    passingScore: 100; // Percentage
    attemptsAllowed: unlimited;
  };
  
  results: {
    score: number;
    rating: number; // Updated user rating
    recommendations: Node[]; // Next learning suggestions
  };
}
```

### Question Selection Algorithm

```typescript
function selectQuestions(
  questionBank: Question[],
  user: User,
  count: number,
  phase: 'pre-quiz' | 'test'
): Question[] {
  // Sort by priority
  const prioritized = questionBank.map(q => ({
    question: q,
    priority: calculatePriority(q, user, phase)
  })).sort((a, b) => b.priority - a.priority);
  
  return prioritized.slice(0, count).map(p => p.question);
}

function calculatePriority(
  question: Question,
  user: User,
  phase: string
): number {
  const viewCount = user.questionHistory[question.id]?.views || 0;
  const lastSeen = user.questionHistory[question.id]?.lastSeen || 0;
  const wasIncorrect = user.questionHistory[question.id]?.incorrect || false;
  
  let priority = 100;
  
  // Prefer unviewed questions
  priority -= viewCount * 20;
  
  // Boost if previously incorrect (spaced repetition)
  if (wasIncorrect && phase === 'test') {
    const daysSince = (Date.now() - lastSeen) / (1000 * 60 * 60 * 24);
    if (daysSince > 3) priority += 30;
  }
  
  // Avoid recent questions
  const hoursSince = (Date.now() - lastSeen) / (1000 * 60 * 60);
  if (hoursSince < 24) priority -= 50;
  
  return priority;
}
```

### User Rating Calculation

```typescript
function updateUserRating(
  currentRating: number,
  testResult: TestResult,
  user: User
): number {
  const accuracy = testResult.score;
  const difficulty = testResult.averageDifficulty;
  const timeEfficiency = Math.min(100, 
    (testResult.estimatedTime / testResult.actualTime) * 100
  );
  
  // Calculate performance score for this test
  const performanceScore = 
    (accuracy * 0.5) + 
    (difficulty * 10) + // Scale 1-10 to 0-100
    (timeEfficiency * 0.2);
  
  // Bayesian average with prior performances
  const priorWeight = Math.min(user.totalTests, 20); // Cap at 20
  const newRating = 
    (currentRating * priorWeight + performanceScore) / 
    (priorWeight + 1);
  
  // Apply time decay to old rating
  const daysSinceLastTest = 
    (Date.now() - user.lastTestDate) / (1000 * 60 * 60 * 24);
  const decayFactor = Math.exp(-daysSinceLastTest / 30); // 30-day half-life
  
  return newRating * (0.7 + 0.3 * decayFactor);
}
```

## Testing Methodology Specifications

### IQ Test Implementation

Based on standardized IQ testing protocols:

- **Timed sections** with strict limits
- **No ability to return** to previous questions
- **Progressive difficulty** within categories
- **Scoring based on age-normalized tables**
- **Categories**: Pattern recognition, spatial reasoning, verbal, numerical, logical

### Standardized Test Implementation

For ACT/SAT/LSAT:

- **Authentic past exams** with source attribution
- **Original time limits** enforced
- **Section-based scoring** matching official rubrics
- **Performance tracking** across multiple attempts
- **Score prediction** based on section performance

### Reading Comprehension System

Based on research by Kintsch & van Dijk (1978):

- **Multiple questions per passage** (5-8 questions)
- **Question types**:
  - Main idea (20%)
  - Supporting details (30%)
  - Inference (25%)
  - Vocabulary in context (15%)
  - Author's purpose/tone (10%)
- **Passage selection** based on user reading level (Flesch-Kincaid)

### Spelling Bee Implementation

Following Scripps National Spelling Bee format:

- **Audio pronunciation** using Web Speech API
- **Context sentence** with word blanked out
- **Etymology hints** available on request
- **Difficulty progression** based on word frequency data
- **Memory techniques** in feedback (mnemonics, word roots)

## References

1. Ausubel, D. P. (1968). *Educational Psychology: A Cognitive View*. Holt, Rinehart and Winston.

2. Bloom, B. S. (1968). "Learning for Mastery." *Evaluation Comment*, 1(2), 1-12.

3. Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*. Teachers College, Columbia University.

4. Kintsch, W., & van Dijk, T. A. (1978). "Toward a model of text comprehension and production." *Psychological Review*, 85(5), 363-394.

5. Leitner, S. (1972). *So lernt man lernen*. Herder.

6. Mayer, R. E. (2009). *Multimedia Learning* (2nd ed.). Cambridge University Press.

7. Sweller, J. (1988). "Cognitive load during problem solving." *Cognitive Science*, 12(2), 257-285.

8. Vygotsky, L. S. (1978). *Mind in Society: The Development of Higher Psychological Processes*. Harvard University Press.

9. Webb, N. L. (1997). "Criteria for alignment of expectations and assessments in mathematics and science education." Council of Chief State School Officers.

---

## Implementation Plan

### Phase 1: Core Assessment System (Week 1-2)
1. Implement pre-quiz system in learning modal
2. Create node test with 100% pass requirement
3. Develop question tracking database schema
4. Build question selection algorithm

### Phase 2: Rating System (Week 3-4)
1. Implement user rating calculation
2. Add rating decay over time
3. Create rating visualization components
4. Build performance history tracking

### Phase 3: Recommendation Engine (Week 5-6)
1. Develop recommendation scoring algorithm
2. Create recommendation categories UI
3. Implement learning path optimization
4. Build interest-based recommendations

### Phase 4: Advanced Testing (Week 7-8)
1. Create intro skill assessment with adaptive testing
2. Implement IQ test framework with timing
3. Add standardized test support
4. Build reading comprehension system
5. Develop spelling bee with audio

### Phase 5: Analytics & Refinement (Week 9-10)
1. Add learning analytics dashboard
2. Implement A/B testing framework
3. Create performance reports
4. Optimize algorithms based on data

---

## Approval Request

This document outlines the theoretical foundations and implementation approach for the educational features of SkillTree. Please review and provide feedback on:

1. The competency rating algorithm and weighting factors
2. The assessment methodology and pass requirements
3. The recommendation engine logic and priorities
4. Any adjustments needed for your specific educational goals

Once approved, we will begin implementing these features according to the specifications outlined above.