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

#### Difficulty Level Assignment Methodology

The spelling bee difficulty system is based on the Scripps National Spelling Bee standards, adapted for broader educational accessibility:

##### Dual-Rating System
1. **Source Difficulty**: Preserves the original classification from Scripps or other authoritative sources
2. **User-Friendly Difficulty**: Maps to a 5-level progressive system for intuitive understanding

##### Difficulty Levels

| Level | Name | Grade Equivalent | Characteristics | Example Words |
|-------|------|-----------------|-----------------|---------------|
| 1 | Beginner | Grades 1-3 | Common everyday vocabulary, phonetic spelling, basic patterns | friend, because, special |
| 2 | Elementary | Grades 4-5 | Standard school vocabulary, introduction to silent letters, common prefixes/suffixes | beautiful, knowledge, necessary |
| 3 | Intermediate | Grades 6-8 | Complex patterns, foreign borrowings, multiple syllables, irregular spellings | rhythm, conscience, restaurant |
| 4 | Advanced | Grades 9-12 (Regional) | Etymology-based spelling, uncommon letter combinations, technical vocabulary | pharaoh, silhouette, entrepreneur |
| 5 | Expert | Competition Level | Championship words, rare etymology, complex linguistic origins | pneumonia, onomatopoeia, schadenfreude |

##### Difficulty Assignment Criteria

Based on linguistic research (Ehri, 2005; Treiman, 1993), words are evaluated on:

1. **Phonetic Transparency** (40% weight)
   - Regular phoneme-grapheme correspondence = easier
   - Silent letters, irregular patterns = harder

2. **Word Frequency** (20% weight)
   - Based on corpus frequency data (Davies, 2008)
   - Common words = lower difficulty
   - Rare/technical words = higher difficulty

3. **Morphological Complexity** (20% weight)
   - Simple roots = easier
   - Multiple morphemes, affixes = harder

4. **Etymology** (20% weight)
   - Anglo-Saxon origin = typically easier
   - Greek/Latin = intermediate
   - Other languages (French, German, etc.) = typically harder

##### Implementation Formula

```typescript
function calculateSpellingDifficulty(word: SpellingWord): number {
  const phoneticScore = assessPhoneticTransparency(word); // 0-100
  const frequencyScore = getWordFrequency(word); // 0-100
  const morphologyScore = analyzeMorphology(word); // 0-100
  const etymologyScore = scoreEtymology(word); // 0-100
  
  const weightedScore = 
    (phoneticScore * 0.4) +
    (frequencyScore * 0.2) +
    (morphologyScore * 0.2) +
    (etymologyScore * 0.2);
  
  // Map to 1-5 scale
  if (weightedScore >= 80) return 1; // Beginner
  if (weightedScore >= 60) return 2; // Elementary
  if (weightedScore >= 40) return 3; // Intermediate
  if (weightedScore >= 20) return 4; // Advanced
  return 5; // Expert
}
```

##### Detailed Scoring Methodologies

###### Phonetic Transparency Score (0-100)
Assesses how closely spelling matches pronunciation. Higher scores indicate more transparent/regular spelling patterns.

**Calculation Method:**
- **Base Score**: 85 (assumes moderate transparency)
- **Silent Letter Patterns** (-15 points each):
  - Terminal clusters: mb$, bt$, ght
  - Initial clusters: kn, wr, gn, ps, pn
  - Medial patterns: alk, alf, alm, ould
  - Vowel patterns: igh, eigh
- **Double Consonants** (-5 points): Indicates spelling complexity
- **Complex Irregular Patterns** (-20 points):
  - ough, augh (highly irregular English patterns)
  - French patterns: eaux, ieux, oeuvre, aille, eille
- **Moderate Irregular Patterns** (-10 points):
  - Common suffixes: tion, sion, cian, ture, sure
- **Foreign Vowel Combinations** (-8 points):
  - ae, oe, eu, eau, ieu, oeu, ui, oi
- **Greek/Latin Combinations** (-12 points):
  - ph, ps, ch, rh, mn

**API Enhancement**: When pronunciation data is available from dictionary API, the score is adjusted based on the ratio of phonetic symbols to letters, indicating pronunciation complexity.

###### Word Frequency Score (0-100)
Estimates how common a word is in everyday usage. Higher scores indicate more common words.

**Calculation Method:**
- **Base Score by Source Difficulty**:
  - One Bee (Grade 1-3): 75 points
  - Two Bee (Grade 4-5): 45 points
  - Three Bee (Grade 6-8): 15 points
- **Word Length Adjustments**:
  - ≤4 letters: +15 points (very common)
  - ≤6 letters: +5 points (common)
  - ≥10 letters: -10 points (less common)
  - ≥13 letters: -20 points (rare)
- **Definition Complexity** (when available):
  - Short definitions (<50 chars): +10 points (simple concepts)
  - Long definitions (>150 chars): -10 points (complex concepts)
  - Technical terms in definition: -15 points

###### Morphology Score (0-100)
Evaluates word structure complexity. Higher scores indicate simpler morphological structure.

**Calculation Method:**
- **Base Score**: 80 (assumes moderate complexity)
- **Length Penalties**:
  - >12 letters: -15 points
  - >8 letters: -10 points
- **Affix Detection**:
  - Common prefixes (un-, re-, pre-, dis-): -5 points
  - Common suffixes (-ing, -ed, -er, -ly): -5 points
- **Compound Word Indicators**:
  - Hyphens: -10 points
  - Multiple capitals: -15 points
- **Multiple Meanings** (from API):
  - >3 meanings: -10 points
  - >5 meanings: -20 points

###### Etymology Score (0-100)
Assesses word origin complexity. Higher scores indicate simpler/more familiar origins.

**Calculation Method:**
- **Base Score**: 60 (neutral origin)
- **Language Origin Adjustments**:
  - Anglo-Saxon/Old English: +20 points (most familiar)
  - Germanic origins: +15 points
  - Latin/Greek: -10 points (classical languages)
  - Romance languages (French, Italian, Spanish): -15 points
  - Non-European languages: -25 points (least familiar)
- **Pattern Recognition** (when etymology unknown):
  - Anglo-Saxon patterns (th, wh, sh): +5 points
  - Greek/Latin patterns (ph, psy, chr): -10 points
  - French patterns (eau, oux, ieux): -15 points
- **Time Period** (from etymology):
  - Modern coinage: +5 points
  - Ancient/Classical: -10 points

##### Progressive Learning Path

Following the Zone of Proximal Development (Vygotsky, 1978):
- Start users at their assessed level
- Progress when achieving 80% accuracy at current level
- Introduce 20% words from next level for scaffolding
- Regression prevention through spaced repetition of mastered words

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