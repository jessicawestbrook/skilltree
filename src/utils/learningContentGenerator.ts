/**
 * Learning Content Generator Utility
 * 
 * This utility helps generate standardized learning content HTML
 * using the predefined templates for different content types.
 */

export interface LearningContentData {
  // Module metadata
  category: string;
  subcategory?: string;
  gradeLevel?: string;
  difficultyLevel: string;
  estimatedTime: number;
  moduleTitle: string;
  moduleDescription: string;
  
  // Learning objectives
  objectives: string[];
  prerequisites?: string[];
  
  // Introduction
  introductionText: string;
  realWorldConnection?: string;
  
  // Content sections
  concepts: Array<{
    title: string;
    explanation: string;
    visual?: string; // HTML or SVG content
    example?: string;
    keyPoints?: string[];
  }>;
  
  // Practice problems
  guidedProblems?: Array<{
    question: string;
    solutionSteps: string;
  }>;
  
  problems: Array<{
    question: string;
    choices: Array<{
      text: string;
      isCorrect: boolean;
    }>;
    hint?: string;
    explanation?: string;
  }>;
  
  // Common mistakes
  commonMistakes?: Array<{
    title: string;
    description: string;
    correctApproach: string;
  }>;
  
  // Summary
  summaryPoints: string[];
  checkItems?: string[];
  
  // Extensions
  challengeProblem?: string;
  extensions?: string[];
  
  // Next steps
  nextLessonTitle?: string;
  nextLessonDescription?: string;
}

export interface ElementaryMathData extends LearningContentData {
  mathSubcategory: string;
  warmUpPrompt?: string;
  warmUpActivity?: string;
  
  vocabulary?: Array<{
    term: string;
    definition: string;
    example: string;
  }>;
  
  visualIntro?: string;
  concreteExamples?: string;
  mathEquation?: string;
  
  workedExamples?: Array<{
    problem: string;
    steps: Array<{
      description: string;
      visual?: string;
    }>;
    answer: string;
  }>;
  
  strategies?: Array<{
    name: string;
    description: string;
    example: string;
  }>;
  
  activities?: Array<{
    name: string;
    description: string;
  }>;
  
  realWorldScenarios?: Array<{
    scenario: string;
    description: string;
    activity: string;
  }>;
  
  basicProblems?: string[];
  challengeProblems?: string[];
  
  reflectionPrompt?: string;
  reflectionQuestions?: string[];
  
  parentTips?: string[];
  extensionIdeas?: string[];
}

export interface MoneyCountingData {
  coins: Array<{
    name: string;
    value: number; // in cents
    color: string;
    size: 'small' | 'medium' | 'large';
    funFact?: string;
  }>;
  
  bills?: Array<{
    value: number; // in dollars
    color: string;
  }>;
  
  skipCountingPatterns?: Array<{
    name: string;
    sequence: number[];
  }>;
  
  countingActivities?: Array<{
    title: string;
    instructions: string;
    targetAmount?: number;
  }>;
  
  shoppingScenarios?: Array<{
    item: string;
    price: number; // in cents
    paymentAmount: number; // in cents
    changeAmount: number; // in cents
  }>;
  
  moneyTips?: Array<{
    title: string;
    description: string;
  }>;
  
  games?: Array<{
    name: string;
    description: string;
    challenges?: string[];
  }>;
}

export class LearningContentGenerator {
  /**
   * Generate standard learning content HTML
   */
  static generateStandardContent(data: LearningContentData): string {
    const template = this.getTemplate('standard');
    return this.populateTemplate(template, {
      CATEGORY: data.category,
      DIFFICULTY_LEVEL: data.difficultyLevel,
      ESTIMATED_TIME: data.estimatedTime.toString(),
      MODULE_TITLE: data.moduleTitle,
      MODULE_DESCRIPTION: data.moduleDescription,
      
      // Objectives
      ...this.generateListItems('OBJECTIVE', data.objectives),
      
      // Prerequisites
      ...this.generateListItems('PREREQUISITE', data.prerequisites || []),
      
      // Introduction
      INTRODUCTION_TEXT: data.introductionText,
      REAL_WORLD_CONNECTION: data.realWorldConnection || '',
      
      // Concepts
      ...this.generateConcepts(data.concepts),
      
      // Problems
      ...this.generateProblems(data.problems),
      
      // Common mistakes
      ...this.generateMistakes(data.commonMistakes || []),
      
      // Summary
      ...this.generateListItems('SUMMARY_POINT', data.summaryPoints),
      ...this.generateListItems('CHECK_ITEM', data.checkItems || []),
      
      // Extensions
      CHALLENGE_PROBLEM: data.challengeProblem || '',
      ...this.generateListItems('EXTENSION', data.extensions || []),
      
      // Next steps
      NEXT_LESSON_TITLE: data.nextLessonTitle || '',
      NEXT_LESSON_DESCRIPTION: data.nextLessonDescription || '',
      
      PROGRESS_PERCENTAGE: '0',
      PROGRESS_TEXT: 'Ready to begin'
    });
  }
  
  /**
   * Generate elementary math content HTML
   */
  static generateElementaryMathContent(data: ElementaryMathData): string {
    const template = this.getTemplate('elementaryMath');
    return this.populateTemplate(template, {
      MATH_SUBCATEGORY: data.mathSubcategory,
      GRADE_LEVEL: data.gradeLevel || '',
      ESTIMATED_TIME: data.estimatedTime.toString(),
      MODULE_TITLE: data.moduleTitle,
      MODULE_DESCRIPTION: data.moduleDescription,
      
      // Warm-up
      WARM_UP_PROMPT: data.warmUpPrompt || '',
      WARM_UP_ACTIVITY: data.warmUpActivity || '',
      
      // Vocabulary
      ...this.generateVocabulary(data.vocabulary || []),
      
      // Concept introduction
      CONCEPT_TITLE: data.concepts[0]?.title || '',
      VISUAL_INTRO: data.visualIntro || '',
      CONCRETE_EXAMPLES: data.concreteExamples || '',
      MATH_EQUATION: data.mathEquation || '',
      
      // Worked examples
      ...this.generateWorkedExamples(data.workedExamples || []),
      
      // Strategies
      ...this.generateStrategies(data.strategies || []),
      
      // Activities
      ...this.generateActivities(data.activities || []),
      
      // Real world
      ...this.generateRealWorldScenarios(data.realWorldScenarios || []),
      
      // Practice problems
      ...this.generateListItems('BASIC_PROBLEM', data.basicProblems || [], 5),
      ...this.generateListItems('CHALLENGE_PROBLEM', data.challengeProblems || [], 3),
      
      // Reflection
      REFLECTION_PROMPT: data.reflectionPrompt || '',
      ...this.generateListItems('REFLECTION_QUESTION', data.reflectionQuestions || []),
      
      // Parent/Teacher notes
      ...this.generateListItems('PARENT_TIP', data.parentTips || []),
      ...this.generateListItems('EXTENSION_IDEA', data.extensionIdeas || []),
      
      // Progress
      PROBLEMS_SOLVED: '0',
      ACCURACY_PERCENTAGE: '0',
      BADGES_EARNED: ''
    });
  }
  
  /**
   * Generate money counting specific content
   */
  static generateMoneyCountingContent(data: MoneyCountingData): string {
    // For money counting, we use the specific template that's already highly specialized
    // This would primarily be used to generate variations or updates
    const template = this.getTemplate('moneyCounting');
    
    // The money counting template is already quite specific,
    // but we can still parameterize certain elements
    const replacements: Record<string, string> = {};
    
    // Generate coin HTML if custom coins provided
    if (data.coins) {
      replacements.CUSTOM_COINS = this.generateCoinHTML(data.coins);
    }
    
    // Generate skip counting patterns
    if (data.skipCountingPatterns) {
      replacements.SKIP_PATTERNS = this.generateSkipPatterns(data.skipCountingPatterns);
    }
    
    // Generate shopping scenarios
    if (data.shoppingScenarios) {
      replacements.SHOPPING_SCENARIOS = this.generateShoppingScenarios(data.shoppingScenarios);
    }
    
    return this.populateTemplate(template, replacements);
  }
  
  // Helper methods
  
  private static getTemplate(type: 'standard' | 'elementaryMath' | 'moneyCounting'): string {
    // In production, these would be loaded from files
    // For now, return template structure
    const templates: Record<string, string> = {
      standard: '<!-- Standard Learning Content Template -->',
      elementaryMath: '<!-- Elementary Math Template -->',
      moneyCounting: '<!-- Money Counting Template -->'
    };
    return templates[type];
  }
  
  private static populateTemplate(template: string, replacements: Record<string, string>): string {
    let result = template;
    for (const [key, value] of Object.entries(replacements)) {
      const regex = new RegExp(`{{${key}}}`, 'g');
      result = result.replace(regex, value);
    }
    return result;
  }
  
  private static generateListItems(
    prefix: string,
    items: string[],
    maxItems?: number
  ): Record<string, string> {
    const result: Record<string, string> = {};
    const itemsToProcess = maxItems ? items.slice(0, maxItems) : items;
    
    itemsToProcess.forEach((item, index) => {
      result[`${prefix}_${index + 1}`] = item;
    });
    
    // Fill remaining slots if maxItems specified
    if (maxItems) {
      for (let i = items.length; i < maxItems; i++) {
        result[`${prefix}_${i + 1}`] = '';
      }
    }
    
    return result;
  }
  
  private static generateConcepts(concepts: LearningContentData['concepts']): Record<string, string> {
    const result: Record<string, string> = {};
    
    concepts.forEach((concept, index) => {
      const num = index + 1;
      result[`CONCEPT_${num}_TITLE`] = concept.title;
      result[`CONCEPT_${num}_EXPLANATION`] = concept.explanation;
      result[`CONCEPT_${num}_VISUAL`] = concept.visual || '';
      result[`CONCEPT_${num}_EXAMPLE`] = concept.example || '';
      
      if (concept.keyPoints) {
        concept.keyPoints.forEach((point, pointIndex) => {
          result[`KEY_POINT_${pointIndex + 1}`] = point;
        });
      }
    });
    
    return result;
  }
  
  private static generateProblems(problems: LearningContentData['problems']): Record<string, string> {
    const result: Record<string, string> = {};
    
    problems.forEach((problem, index) => {
      const num = index + 1;
      result[`PROBLEM_${num}_QUESTION`] = problem.question;
      result[`PROBLEM_${num}_HINT`] = problem.hint || '';
      result[`PROBLEM_${num}_EXPLANATION`] = problem.explanation || '';
      
      const correctIndex = problem.choices.findIndex(c => c.isCorrect);
      result[`PROBLEM_${num}_CORRECT`] = correctIndex === 0 ? 'true' : 'false';
      
      ['A', 'B', 'C', 'D'].forEach((letter, choiceIndex) => {
        if (problem.choices[choiceIndex]) {
          result[`PROBLEM_${num}_CHOICE_${letter}`] = problem.choices[choiceIndex].text;
        }
      });
    });
    
    return result;
  }
  
  private static generateMistakes(
    mistakes: NonNullable<LearningContentData['commonMistakes']>
  ): Record<string, string> {
    const result: Record<string, string> = {};
    
    mistakes.forEach((mistake, index) => {
      const num = index + 1;
      result[`MISTAKE_${num}_TITLE`] = mistake.title;
      result[`MISTAKE_${num}_DESCRIPTION`] = mistake.description;
      result[`CORRECT_APPROACH_${num}`] = mistake.correctApproach;
    });
    
    return result;
  }
  
  private static generateVocabulary(
    vocabulary: NonNullable<ElementaryMathData['vocabulary']>
  ): Record<string, string> {
    const result: Record<string, string> = {};
    
    vocabulary.forEach((vocab, index) => {
      const num = index + 1;
      result[`VOCAB_TERM_${num}`] = vocab.term;
      result[`VOCAB_DEFINITION_${num}`] = vocab.definition;
      result[`VOCAB_EXAMPLE_${num}`] = vocab.example;
    });
    
    return result;
  }
  
  private static generateWorkedExamples(
    examples: NonNullable<ElementaryMathData['workedExamples']>
  ): Record<string, string> {
    const result: Record<string, string> = {};
    
    examples.forEach((example, index) => {
      const num = index + 1;
      result[`EXAMPLE_${num}_PROBLEM`] = example.problem;
      result[`EXAMPLE_${num}_ANSWER`] = example.answer;
      
      example.steps.forEach((step, stepIndex) => {
        const stepNum = stepIndex + 1;
        result[`EXAMPLE_${num}_STEP_${stepNum}`] = step.description;
        result[`EXAMPLE_${num}_VISUAL_${stepNum}`] = step.visual || '';
      });
    });
    
    return result;
  }
  
  private static generateStrategies(
    strategies: NonNullable<ElementaryMathData['strategies']>
  ): Record<string, string> {
    const result: Record<string, string> = {};
    
    strategies.forEach((strategy, index) => {
      const num = index + 1;
      result[`STRATEGY_${num}_NAME`] = strategy.name;
      result[`STRATEGY_${num}_DESCRIPTION`] = strategy.description;
      result[`STRATEGY_${num}_EXAMPLE`] = strategy.example;
    });
    
    return result;
  }
  
  private static generateActivities(
    activities: NonNullable<ElementaryMathData['activities']>
  ): Record<string, string> {
    const result: Record<string, string> = {};
    
    if (activities.length > 0) {
      result.ACTIVITY_NAME = activities[0].name;
      result.ACTIVITY_DESCRIPTION = activities[0].description;
    }
    
    return result;
  }
  
  private static generateRealWorldScenarios(
    scenarios: NonNullable<ElementaryMathData['realWorldScenarios']>
  ): Record<string, string> {
    const result: Record<string, string> = {};
    
    scenarios.forEach((scenario, index) => {
      const num = index + 1;
      result[`REAL_WORLD_SCENARIO_${num}`] = scenario.scenario;
      result[`REAL_WORLD_DESCRIPTION_${num}`] = scenario.description;
      result[`REAL_WORLD_ACTIVITY_${num}`] = scenario.activity;
    });
    
    return result;
  }
  
  private static generateCoinHTML(coins: MoneyCountingData['coins']): string {
    return coins.map(coin => `
      <div class="coin-card">
        <h3>${coin.name}</h3>
        <div class="money-display">
          <svg width="80" height="80" viewBox="0 0 80 80">
            <circle cx="40" cy="40" r="35" fill="${coin.color}" stroke="#444" stroke-width="2"/>
            <text x="40" y="45" text-anchor="middle" font-size="24" font-weight="bold" fill="white">
              ${coin.value}¢
            </text>
          </svg>
        </div>
        <p><strong>Value:</strong> ${coin.value} cent${coin.value !== 1 ? 's' : ''}</p>
        ${coin.funFact ? `<p><strong>Fun Fact:</strong> ${coin.funFact}</p>` : ''}
      </div>
    `).join('\n');
  }
  
  private static generateSkipPatterns(
    patterns: NonNullable<MoneyCountingData['skipCountingPatterns']>
  ): string {
    return patterns.map(pattern => `
      <div class="skip-pattern">
        <h3>${pattern.name}</h3>
        <div class="number-sequence">
          ${pattern.sequence.map(num => `<span>${num}</span>`).join(' → ')}
        </div>
      </div>
    `).join('\n');
  }
  
  private static generateShoppingScenarios(
    scenarios: NonNullable<MoneyCountingData['shoppingScenarios']>
  ): string {
    return scenarios.map((scenario, index) => `
      <div class="shopping-scenario">
        <h3>Scenario ${index + 1}</h3>
        <p>A customer buys ${scenario.item} for ${this.formatMoney(scenario.price)}.</p>
        <p>They give you ${this.formatMoney(scenario.paymentAmount)}.</p>
        <p class="question">How much change do they get?</p>
        <div class="answer-choices">
          <button class="answer-choice" data-correct="${scenario.changeAmount === scenario.paymentAmount - scenario.price}">
            ${this.formatMoney(scenario.changeAmount)}
          </button>
          <!-- Add more choice options -->
        </div>
      </div>
    `).join('\n');
  }
  
  private static formatMoney(cents: number): string {
    if (cents >= 100) {
      const dollars = Math.floor(cents / 100);
      const remainingCents = cents % 100;
      return remainingCents > 0 
        ? `$${dollars}.${remainingCents.toString().padStart(2, '0')}`
        : `$${dollars}.00`;
    }
    return `${cents}¢`;
  }
}

// Export example usage function
export function generateExampleContent(): void {
  // Example: Generate a basic addition lesson
  const additionLesson: ElementaryMathData = {
    category: 'Elementary Math',
    mathSubcategory: 'Addition',
    gradeLevel: '1',
    difficultyLevel: 'Beginner',
    estimatedTime: 20,
    moduleTitle: 'Adding Numbers to 10',
    moduleDescription: 'Learn to add single-digit numbers with sums up to 10',
    
    objectives: [
      'Add single-digit numbers with sums up to 10',
      'Use counting strategies to solve addition problems',
      'Recognize addition patterns'
    ],
    
    prerequisites: [
      'Count to 10',
      'Recognize numbers 0-10'
    ],
    
    introductionText: 'Addition means putting groups together to find how many in all!',
    realWorldConnection: 'We use addition when counting toys, sharing snacks, or saving money.',
    
    warmUpPrompt: 'How many fingers do you have on both hands? Let\'s count!',
    warmUpActivity: '<div class="finger-counting">Count: 5 fingers + 5 fingers = ?</div>',
    
    vocabulary: [
      {
        term: 'Addition',
        definition: 'Putting numbers together to find the total',
        example: '2 + 3 = 5'
      },
      {
        term: 'Sum',
        definition: 'The answer when we add numbers',
        example: 'The sum of 4 + 2 is 6'
      }
    ],
    
    concepts: [
      {
        title: 'Understanding Addition',
        explanation: 'When we add, we combine groups to find out how many we have altogether.',
        visual: '<div class="visual-blocks">🟦🟦 + 🟦🟦🟦 = 🟦🟦🟦🟦🟦</div>',
        example: '2 blocks + 3 blocks = 5 blocks total',
        keyPoints: ['Addition makes numbers bigger', 'The + sign means add']
      }
    ],
    
    workedExamples: [
      {
        problem: 'Find 3 + 4',
        steps: [
          { description: 'Start with 3', visual: '🔵🔵🔵' },
          { description: 'Add 4 more', visual: '🔵🔵🔵 + 🔴🔴🔴🔴' },
          { description: 'Count them all', visual: '1, 2, 3, 4, 5, 6, 7' }
        ],
        answer: '3 + 4 = 7'
      }
    ],
    
    problems: [
      {
        question: 'What is 2 + 3?',
        choices: [
          { text: '4', isCorrect: false },
          { text: '5', isCorrect: true },
          { text: '6', isCorrect: false },
          { text: '7', isCorrect: false }
        ],
        hint: 'Start with 2 and count up 3 more',
        explanation: '2 + 3 = 5. We start with 2 and add 3 more to get 5.'
      }
    ],
    
    summaryPoints: [
      'Addition means combining groups',
      'We use the + sign for addition',
      'Counting helps us add'
    ],
    
    checkItems: [
      'Add numbers to 10',
      'Use counting to check your answer',
      'Recognize the + and = signs'
    ],
    
    parentTips: [
      'Practice addition with everyday objects like toys or snacks',
      'Use your fingers for counting - it\'s a great tool!',
      'Make addition fun with games and stories'
    ],
    
    extensionIdeas: [
      'Try adding three numbers together',
      'Find different ways to make 10'
    ]
  };
  
  const html = LearningContentGenerator.generateElementaryMathContent(additionLesson);
  console.log('Generated content length:', html.length);
}