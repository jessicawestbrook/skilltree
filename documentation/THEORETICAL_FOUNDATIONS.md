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

### Vocabulary Trainer Implementation

#### Vocabulary Difficulty Framework

The vocabulary trainer employs a **comprehension-based difficulty system** distinct from spelling complexity, focusing on semantic understanding and contextual usage rather than orthographic challenges.

##### Core Principles

Based on vocabulary acquisition research (Beck, McKeown & Kucan, 2002; Nagy & Scott, 2000), vocabulary difficulty is determined by:

1. **Semantic Complexity**: How abstract or concrete the concept is
2. **Contextual Frequency**: How often the word appears in academic/formal texts
3. **Conceptual Sophistication**: The cognitive complexity required to understand the concept
4. **Register Specificity**: Whether the word is domain-specific or general usage

##### Vocabulary Difficulty Levels

| Level | Name | Description | Characteristics | Example Words |
|-------|------|-------------|-----------------|---------------|
| 1 | Foundation | Basic everyday concepts | Concrete nouns, simple actions, common adjectives | happy, run, big, house, dog |
| 2 | Academic | School-level vocabulary | Abstract concepts, academic subjects, formal language | analyze, democracy, ecosystem, literature |
| 3 | Sophisticated | Advanced academic and professional | Complex abstractions, technical concepts, nuanced meanings | paradigm, synthesize, empirical, rhetoric |
| 4 | Specialized | Domain-specific terminology | Professional jargon, scientific terms, specialized fields | cytoplasm, jurisprudence, thermodynamics, epistemology |
| 5 | Scholarly | Research and expert-level | Highly specialized, theoretical concepts, academic discourse | phenomenology, hermeneutics, ontological, epistemic |

##### Vocabulary Difficulty Assessment Methodology

###### Multi-Dimensional Scoring System

Unlike spelling difficulty which focuses on orthographic patterns, vocabulary difficulty emphasizes **semantic and contextual factors**:

```typescript
function calculateVocabularyDifficulty(word: VocabularyWord): number {
  const semanticComplexity = assessSemanticComplexity(word); // 0-100
  const contextualFrequency = getContextualFrequency(word); // 0-100
  const conceptualSophistication = assessConceptualSophistication(word); // 0-100
  const registerSpecificity = assessRegisterSpecificity(word); // 0-100
  
  const vocabularyScore = 
    (semanticComplexity * 0.35) +
    (contextualFrequency * 0.25) +
    (conceptualSophistication * 0.25) +
    (registerSpecificity * 0.15);
  
  // Map to 1-5 scale (inverted from spelling - higher complexity = higher level)
  if (vocabularyScore <= 20) return 1; // Foundation
  if (vocabularyScore <= 40) return 2; // Academic
  if (vocabularyScore <= 60) return 3; // Sophisticated
  if (vocabularyScore <= 80) return 4; // Specialized
  return 5; // Scholarly
}
```

###### Detailed Scoring Methodologies

**Semantic Complexity Score (0-100)**
Measures the abstractness and conceptual depth of the word meaning.

- **Concrete Concepts** (0-20 points): Physical objects, actions, observable qualities
- **Abstract General** (21-40 points): Emotions, relationships, common ideas
- **Abstract Academic** (41-60 points): Theoretical concepts, complex relationships
- **Abstract Professional** (61-80 points): Specialized theoretical constructs
- **Abstract Philosophical** (81-100 points): Highly theoretical, meta-conceptual ideas

*Assessment Criteria:*
- Definition length and complexity
- Number of meaning layers/nuances
- Requirement for background knowledge
- Degree of abstraction from physical reality

**Contextual Frequency Score (0-100)**
Evaluates how commonly the word appears in formal/academic contexts vs. everyday speech.

- **Everyday Usage** (81-100 points): Common in casual conversation
- **Formal Speech** (61-80 points): Used in professional/formal contexts
- **Academic Writing** (41-60 points): Common in educational materials
- **Specialized Literature** (21-40 points): Found primarily in specific fields
- **Rare/Archaic** (0-20 points): Seldom used, historical, or highly specialized

*Assessment Criteria:*
- Frequency in academic corpus vs. conversational corpus
- Presence in different text types (news, academic papers, literature)
- Grade level of typical first exposure
- Subject area specificity

**Conceptual Sophistication Score (0-100)**
Measures the cognitive complexity required to understand the concept.

- **Basic Cognition** (0-20 points): Simple categorization, direct observation
- **Analytical Thinking** (21-40 points): Comparison, cause-effect, classification
- **Synthesis** (41-60 points): Combining ideas, drawing connections
- **Evaluation** (61-80 points): Critical judgment, assessment, critique
- **Creation/Theory** (81-100 points): Original thinking, theory building

*Assessment Criteria:*
- Bloom's Taxonomy level required for comprehension
- Number of prerequisite concepts needed
- Cognitive load for processing
- Interdisciplinary connections required

**Register Specificity Score (0-100)**
Assesses how domain-specific vs. cross-disciplinary the word is.

- **Universal** (0-20 points): Used across all domains and contexts
- **Cross-Disciplinary** (21-40 points): Common in multiple academic fields
- **Field-Specific** (41-60 points): Primarily used in one academic area
- **Sub-Specialty** (61-80 points): Specific to particular specializations
- **Highly Technical** (81-100 points): Extremely narrow, expert-only usage

*Assessment Criteria:*
- Number of academic disciplines using the term
- Requirement for specialized training to understand
- Presence in general vs. specialized dictionaries
- Technical definition complexity

##### Implementation Differences from Spelling Bee

1. **Focus Shift**: From orthographic accuracy to semantic comprehension
2. **Question Format**: Definition-to-word matching instead of audio-to-spelling
3. **Difficulty Progression**: Based on conceptual complexity rather than spelling patterns
4. **Assessment Criteria**: Emphasizes understanding over memorization
5. **Learning Support**: Provides semantic relationships and usage contexts

##### Adaptive Difficulty Adjustment

Based on research in vocabulary acquisition (Nation, 2001; Schmitt, 2000):

- **Initial Assessment**: Start with Academic level (Level 2) words
- **Success Threshold**: 75% accuracy to advance to next level
- **Failure Response**: Drop to previous level after 3 consecutive errors
- **Mixed Practice**: Include 20% words from adjacent levels for scaffolding
- **Spaced Repetition**: Emphasize semantic relationships over time intervals

### Adaptive Learning for Module Tests

#### Theoretical Foundation

The adaptive learning system for module tests is based on several established educational theories:

1. **Zone of Proximal Development (Vygotsky, 1978)**: Questions progress from what learners can do independently (easy questions) to what they can achieve with guidance (harder questions).

2. **Scaffolding Theory (Wood, Bruner, & Ross, 1976)**: Starting with easier questions provides the support structure needed for tackling more complex problems.

3. **Flow Theory (Csikszentmihalyi, 1990)**: Maintaining optimal challenge levels keeps learners engaged without causing anxiety or boredom.

4. **Item Response Theory (IRT)**: Questions are calibrated by difficulty to accurately assess learner ability across different performance levels.

#### Implementation Design

##### Question Difficulty Classification

Questions are categorized into four difficulty levels based on cognitive complexity (Bloom's Revised Taxonomy):

```typescript
interface DifficultyLevels {
  easy: {
    cognitiveLevel: 'Remember/Understand';
    complexity: 'Single concept, direct recall';
    timeEstimate: '< 30 seconds';
    pointMultiplier: 1.0;
  };
  medium: {
    cognitiveLevel: 'Apply';
    complexity: 'Multiple steps, standard procedures';
    timeEstimate: '30-60 seconds';
    pointMultiplier: 2.0;
  };
  hard: {
    cognitiveLevel: 'Analyze/Evaluate';
    complexity: 'Complex reasoning, multiple concepts';
    timeEstimate: '60-90 seconds';
    pointMultiplier: 3.0;
  };
  expert: {
    cognitiveLevel: 'Create/Synthesize';
    complexity: 'Novel problems, creative solutions';
    timeEstimate: '> 90 seconds';
    pointMultiplier: 4.0;
  };
}
```

##### Adaptive Question Selection Algorithm

The system employs a progressive difficulty model:

**Pre-Quiz Phase (Diagnostic)**:
- 2 easy questions: Establish baseline confidence
- 1 medium question: Probe higher-level understanding
- Purpose: Calibrate starting difficulty for main test

**Test Phase (Adaptive Progression)**:

Distribution based on test length:
- **Short tests (≤5 questions)**: 60% easy, 40% medium
- **Medium tests (6-10 questions)**: 40% easy, 40% medium, 20% hard
- **Long tests (>10 questions)**: 30% easy, 35% medium, 25% hard, 10% expert

Questions are sorted from easy to hard within the test to:
1. Build learner confidence early
2. Reduce test anxiety
3. Ensure foundational concepts are assessed first
4. Allow for natural progression of complexity

##### Performance-Based Adaptation

While the current implementation uses pre-sorted difficulty progression, the framework supports dynamic adaptation:

```typescript
interface AdaptationRules {
  difficultyAdjustment: {
    consecutiveCorrect: 2; // Advance difficulty after 2 correct
    consecutiveIncorrect: 2; // Reduce difficulty after 2 incorrect
    maxJump: 1; // Maximum difficulty change per adjustment
  };
  
  performanceTracking: {
    currentStreak: number;
    difficultyHistory: string[];
    responseTime: number[];
    confidenceScore: number; // Calculated from speed and accuracy
  };
}
```

##### Visual Feedback and Motivation

Difficulty indicators provide transparency and motivation:

- **Color Coding**: Green (Easy) → Blue (Medium) → Orange (Hard) → Red (Expert)
- **Progress Messaging**: Contextual feedback based on performance tiers
  - 100%: "Perfect Score!" - Mastery achieved
  - 80-99%: "Great Job!" - Strong understanding
  - 60-79%: "Good Progress!" - Solid foundation
  - <60%: "Keep Practicing!" - Encouragement to continue

##### Scoring Algorithm with Difficulty Weighting

Performance scoring accounts for question difficulty:

```typescript
calculateScore(question, answer) {
  const basePoints = 10 * difficultyMultiplier[question.difficulty];
  let earnedPoints = 0;
  
  if (answer.correct) {
    earnedPoints = basePoints;
    
    // Speed bonus for quick, correct answers
    if (answer.timeSpent < 30) {
      earnedPoints *= 1.2; // 20% bonus
    }
  }
  
  return {
    earned: earnedPoints,
    possible: basePoints,
    efficiency: earnedPoints / answer.timeSpent
  };
}
```

#### Pedagogical Benefits

1. **Reduced Cognitive Overload**: Starting with easier questions prevents overwhelming learners
2. **Increased Self-Efficacy**: Early successes build confidence (Bandura, 1977)
3. **Accurate Assessment**: Difficulty range provides better ability estimation
4. **Personalized Learning Path**: Performance data informs future content recommendations
5. **Engagement Maintenance**: Progressive challenge maintains flow state

#### Future Enhancements

1. **Real-time Adaptation**: Adjust difficulty during test based on performance
2. **Personalized Difficulty Curves**: Learn individual progression preferences
3. **Cross-module Calibration**: Use performance across topics for initial difficulty
4. **Predictive Modeling**: Anticipate optimal difficulty based on learning history
5. **Collaborative Filtering**: Use peer performance data for difficulty validation

##### Learning Analytics for Vocabulary

Track distinct metrics from spelling performance:

```typescript
interface VocabularyProgress {
  semanticUnderstanding: number; // Ability to grasp word meanings
  contextualUsage: number; // Understanding words in different contexts
  relationalKnowledge: number; // Connecting words to synonyms/antonyms
  retentionRate: number; // Long-term retention of learned vocabulary
  transferability: number; // Using vocabulary in new contexts
}
```

##### Validation and Calibration

Vocabulary difficulty levels should be validated against:

1. **Standardized Tests**: SAT, GRE, TOEFL vocabulary sections
2. **Academic Reading Levels**: Flesch-Kincaid, Lexile measures
3. **Corpus Analysis**: Academic Word List (Coxhead, 2000)
4. **Expert Judgment**: Language teachers and curriculum specialists
5. **Student Performance**: Empirical testing with target demographics

### Spelling Bee Implementation

Following Scripps National Spelling Bee format:

- **Audio pronunciation** using Web Speech API
- **Context sentence** with word blanked out
- **Etymology hints** available on request
- **Difficulty progression** based on word frequency data
- **Memory techniques** in feedback (mnemonics, word roots)

## References

1. Ausubel, D. P. (1968). *Educational Psychology: A Cognitive View*. Holt, Rinehart and Winston.

2. Bandura, A. (1977). "Self-efficacy: Toward a unifying theory of behavioral change." *Psychological Review*, 84(2), 191-215.

3. Bloom, B. S. (1968). "Learning for Mastery." *Evaluation Comment*, 1(2), 1-12.

4. Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row.

5. Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*. Teachers College, Columbia University.

6. Kintsch, W., & van Dijk, T. A. (1978). "Toward a model of text comprehension and production." *Psychological Review*, 85(5), 363-394.

7. Leitner, S. (1972). *So lernt man lernen*. Herder.

8. Mayer, R. E. (2009). *Multimedia Learning* (2nd ed.). Cambridge University Press.

9. Sweller, J. (1988). "Cognitive load during problem solving." *Cognitive Science*, 12(2), 257-285.

10. Vygotsky, L. S. (1978). *Mind in Society: The Development of Higher Psychological Processes*. Harvard University Press.

11. Wood, D., Bruner, J. S., & Ross, G. (1976). "The role of tutoring in problem solving." *Journal of Child Psychology and Psychiatry*, 17(2), 89-100.

12. Webb, N. L. (1997). "Criteria for alignment of expectations and assessments in mathematics and science education." Council of Chief State School Officers.

13. Beck, I. L., McKeown, M. G., & Kucan, L. (2002). *Bringing Words to Life: Robust Vocabulary Instruction*. Guilford Press.

14. Nagy, W. E., & Scott, J. A. (2000). "Vocabulary processes." In M. L. Kamil, P. B. Mosenthal, P. D. Pearson, & R. Barr (Eds.), *Handbook of reading research* (Vol. 3, pp. 269-284). Lawrence Erlbaum Associates.

15. Nation, I. S. P. (2001). *Learning Vocabulary in Another Language*. Cambridge University Press.

16. Schmitt, N. (2000). *Vocabulary in Language Teaching*. Cambridge University Press.

17. Coxhead, A. (2000). "A new academic word list." *TESOL Quarterly*, 34(2), 213-238.

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