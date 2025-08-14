/**
 * Grade-Level Standards System for Educational Content Tagging
 * 
 * This file defines comprehensive educational standards aligned with:
 * - Common Core State Standards (CCSS)
 * - Next Generation Science Standards (NGSS)
 * - National Council for Social Studies (NCSS) Standards
 * - College, Career, and Civic Life (C3) Framework
 */

export type GradeLevel = 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
export type Subject = 'math' | 'ela' | 'science' | 'social-studies';

export interface LearningStandard {
  id: string;
  subject: Subject;
  gradeLevel: GradeLevel;
  domain: string;
  subdomain?: string;
  title: string;
  description: string;
  keywords: string[];
  prerequisiteStandardIds?: string[];
  complexityLevel: 1 | 2 | 3 | 4 | 5; // 1=recall, 2=skill, 3=application, 4=analysis, 5=synthesis
  bloomsLevel: 'remember' | 'understand' | 'apply' | 'analyze' | 'evaluate' | 'create';
}

export interface GradeLevelProgression {
  gradeLevel: GradeLevel;
  cognitiveCapabilities: string[];
  typicalSkills: string[];
  readingLevel: string;
  mathLevel: string;
  abstractionLevel: 'concrete' | 'semi-abstract' | 'abstract';
}

// Grade Level Progressions based on developmental psychology and educational research
export const GRADE_PROGRESSIONS: GradeLevelProgression[] = [
  {
    gradeLevel: 3,
    cognitiveCapabilities: ['concrete operational thinking', 'classification', 'conservation'],
    typicalSkills: ['basic reading fluency', 'addition/subtraction mastery', 'simple problem solving'],
    readingLevel: '3rd grade (DRA 30-38)',
    mathLevel: 'whole numbers to 1000, basic operations',
    abstractionLevel: 'concrete'
  },
  {
    gradeLevel: 4,
    cognitiveCapabilities: ['logical reasoning', 'categorization', 'sequencing'],
    typicalSkills: ['reading comprehension', 'multi-digit arithmetic', 'basic fractions'],
    readingLevel: '4th grade (DRA 40)',
    mathLevel: 'place value, multiplication/division',
    abstractionLevel: 'concrete'
  },
  {
    gradeLevel: 5,
    cognitiveCapabilities: ['systematic thinking', 'hypothesis formation', 'pattern recognition'],
    typicalSkills: ['advanced reading comprehension', 'decimal operations', 'basic geometry'],
    readingLevel: '5th grade (DRA 50)',
    mathLevel: 'fractions, decimals, basic algebra concepts',
    abstractionLevel: 'semi-abstract'
  },
  {
    gradeLevel: 6,
    cognitiveCapabilities: ['early formal operations', 'abstract reasoning begins', 'proportional thinking'],
    typicalSkills: ['analytical reading', 'advanced arithmetic', 'scientific method understanding'],
    readingLevel: '6th grade (DRA 60)',
    mathLevel: 'ratios, percentages, basic algebra',
    abstractionLevel: 'semi-abstract'
  },
  {
    gradeLevel: 7,
    cognitiveCapabilities: ['developing abstract thought', 'hypothetical reasoning', 'metacognition'],
    typicalSkills: ['critical reading', 'pre-algebra', 'scientific inquiry'],
    readingLevel: '7th grade (DRA 70)',
    mathLevel: 'algebraic thinking, linear equations',
    abstractionLevel: 'semi-abstract'
  },
  {
    gradeLevel: 8,
    cognitiveCapabilities: ['formal operational thinking', 'logical deduction', 'systems thinking'],
    typicalSkills: ['advanced literary analysis', 'algebra mastery', 'experimental design'],
    readingLevel: '8th grade (DRA 80)',
    mathLevel: 'algebra I, geometric reasoning',
    abstractionLevel: 'abstract'
  },
  {
    gradeLevel: 9,
    cognitiveCapabilities: ['abstract reasoning', 'complex problem solving', 'independent thinking'],
    typicalSkills: ['literary criticism', 'advanced algebra', 'scientific analysis'],
    readingLevel: '9th grade (Lexile 1050-1260)',
    mathLevel: 'algebra I/II, geometry',
    abstractionLevel: 'abstract'
  },
  {
    gradeLevel: 10,
    cognitiveCapabilities: ['sophisticated reasoning', 'synthesis across domains', 'critical evaluation'],
    typicalSkills: ['research writing', 'geometric proofs', 'data analysis'],
    readingLevel: '10th grade (Lexile 1080-1305)',
    mathLevel: 'geometry, advanced algebra',
    abstractionLevel: 'abstract'
  },
  {
    gradeLevel: 11,
    cognitiveCapabilities: ['advanced critical thinking', 'interdisciplinary connections', 'creative problem solving'],
    typicalSkills: ['college-level analysis', 'trigonometry/pre-calculus', 'research methods'],
    readingLevel: '11th grade (Lexile 1185-1385)',
    mathLevel: 'pre-calculus, statistics',
    abstractionLevel: 'abstract'
  },
  {
    gradeLevel: 12,
    cognitiveCapabilities: ['expert reasoning', 'meta-cognitive awareness', 'synthesis and creation'],
    typicalSkills: ['advanced composition', 'calculus readiness', 'independent research'],
    readingLevel: '12th grade (Lexile 1185-1385)',
    mathLevel: 'calculus, advanced statistics',
    abstractionLevel: 'abstract'
  }
];

// Mathematics Standards (Common Core aligned)
export const MATH_STANDARDS: LearningStandard[] = [
  // Grade 3 Math
  {
    id: 'CCSS.MATH.3.OA.A.1',
    subject: 'math',
    gradeLevel: 3,
    domain: 'Operations and Algebraic Thinking',
    subdomain: 'Represent and solve problems involving multiplication and division',
    title: 'Multiplication and Division Word Problems',
    description: 'Interpret products of whole numbers and solve word problems involving multiplication and division',
    keywords: ['multiplication', 'division', 'word problems', 'arrays', 'groups'],
    complexityLevel: 2,
    bloomsLevel: 'apply'
  },
  {
    id: 'CCSS.MATH.3.NBT.A.1',
    subject: 'math',
    gradeLevel: 3,
    domain: 'Number and Operations in Base Ten',
    subdomain: 'Use place value understanding',
    title: 'Rounding Whole Numbers',
    description: 'Use place value understanding to round whole numbers to the nearest 10 or 100',
    keywords: ['place value', 'rounding', 'nearest ten', 'nearest hundred'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  
  // Grade 4 Math
  {
    id: 'CCSS.MATH.4.OA.A.1',
    subject: 'math',
    gradeLevel: 4,
    domain: 'Operations and Algebraic Thinking',
    subdomain: 'Use the four operations with whole numbers',
    title: 'Multi-step Word Problems',
    description: 'Interpret multi-step word problems with whole numbers and assess reasonableness of answers',
    keywords: ['multi-step', 'word problems', 'four operations', 'reasonableness'],
    complexityLevel: 3,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.MATH.4.NF.A.1',
    subject: 'math',
    gradeLevel: 4,
    domain: 'Number and Operations—Fractions',
    subdomain: 'Extend understanding of fraction equivalence',
    title: 'Equivalent Fractions',
    description: 'Explain why a fraction a/b is equivalent to a fraction (n×a)/(n×b)',
    keywords: ['fractions', 'equivalent', 'numerator', 'denominator'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },

  // Grade 5 Math
  {
    id: 'CCSS.MATH.5.NBT.A.1',
    subject: 'math',
    gradeLevel: 5,
    domain: 'Number and Operations in Base Ten',
    subdomain: 'Understand the place value system',
    title: 'Place Value Patterns',
    description: 'Recognize that in a multi-digit number, a digit in one place represents 10 times as much as it represents in the place to its right',
    keywords: ['place value', 'patterns', 'multi-digit', 'ten times'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  {
    id: 'CCSS.MATH.5.NF.B.3',
    subject: 'math',
    gradeLevel: 5,
    domain: 'Number and Operations—Fractions',
    subdomain: 'Use equivalent fractions as a strategy',
    title: 'Interpreting Fractions as Division',
    description: 'Interpret a fraction as division of the numerator by the denominator',
    keywords: ['fractions', 'division', 'numerator', 'denominator', 'quotient'],
    complexityLevel: 3,
    bloomsLevel: 'apply'
  },

  // Grade 6 Math
  {
    id: 'CCSS.MATH.6.RP.A.1',
    subject: 'math',
    gradeLevel: 6,
    domain: 'Ratios and Proportional Relationships',
    subdomain: 'Understand ratio concepts',
    title: 'Understanding Ratios',
    description: 'Understand the concept of a ratio and use ratio language to describe relationships',
    keywords: ['ratios', 'proportional relationships', 'rate', 'unit rate'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  {
    id: 'CCSS.MATH.6.EE.A.1',
    subject: 'math',
    gradeLevel: 6,
    domain: 'Expressions and Equations',
    subdomain: 'Apply and extend previous understandings',
    title: 'Numerical Expressions with Exponents',
    description: 'Write and evaluate numerical expressions involving whole-number exponents',
    keywords: ['exponents', 'expressions', 'evaluate', 'order of operations'],
    complexityLevel: 2,
    bloomsLevel: 'apply'
  },

  // Grade 7 Math
  {
    id: 'CCSS.MATH.7.RP.A.2',
    subject: 'math',
    gradeLevel: 7,
    domain: 'Ratios and Proportional Relationships',
    subdomain: 'Analyze proportional relationships',
    title: 'Proportional Relationships',
    description: 'Recognize and represent proportional relationships between quantities',
    keywords: ['proportional', 'relationships', 'constant', 'rate of change'],
    complexityLevel: 3,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.MATH.7.EE.B.3',
    subject: 'math',
    gradeLevel: 7,
    domain: 'Expressions and Equations',
    subdomain: 'Solve real-life mathematical problems',
    title: 'Multi-step Linear Equations',
    description: 'Solve multi-step real-life and mathematical problems posed with positive and negative rational numbers',
    keywords: ['linear equations', 'multi-step', 'rational numbers', 'real-life problems'],
    complexityLevel: 3,
    bloomsLevel: 'apply'
  },

  // Grade 8 Math
  {
    id: 'CCSS.MATH.8.EE.A.1',
    subject: 'math',
    gradeLevel: 8,
    domain: 'Expressions and Equations',
    subdomain: 'Work with radicals and integer exponents',
    title: 'Laws of Exponents',
    description: 'Know and apply the properties of integer exponents to generate equivalent numerical expressions',
    keywords: ['exponents', 'properties', 'equivalent expressions', 'laws of exponents'],
    complexityLevel: 3,
    bloomsLevel: 'apply'
  },
  {
    id: 'CCSS.MATH.8.F.A.1',
    subject: 'math',
    gradeLevel: 8,
    domain: 'Functions',
    subdomain: 'Define, evaluate, and compare functions',
    title: 'Understanding Functions',
    description: 'Understand that a function is a rule that assigns to each input exactly one output',
    keywords: ['functions', 'input', 'output', 'rule', 'relationship'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },

  // High School Math (Grades 9-12)
  {
    id: 'CCSS.MATH.HSA.SSE.A.1',
    subject: 'math',
    gradeLevel: 9,
    domain: 'Algebra',
    subdomain: 'Seeing Structure in Expressions',
    title: 'Interpreting Algebraic Expressions',
    description: 'Interpret expressions that represent a quantity in terms of its context',
    keywords: ['algebraic expressions', 'interpret', 'context', 'terms', 'factors'],
    complexityLevel: 3,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.MATH.HSG.CO.A.1',
    subject: 'math',
    gradeLevel: 10,
    domain: 'Geometry',
    subdomain: 'Congruence',
    title: 'Geometric Constructions',
    description: 'Know precise definitions of angle, circle, perpendicular, parallel, and line segment',
    keywords: ['geometry', 'constructions', 'angle', 'circle', 'perpendicular', 'parallel'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  {
    id: 'CCSS.MATH.HSA.APR.A.1',
    subject: 'math',
    gradeLevel: 11,
    domain: 'Algebra',
    subdomain: 'Arithmetic with Polynomials',
    title: 'Polynomial Operations',
    description: 'Understand that polynomials form a system analogous to the integers',
    keywords: ['polynomials', 'operations', 'addition', 'subtraction', 'multiplication'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.MATH.HSF.IF.C.7',
    subject: 'math',
    gradeLevel: 12,
    domain: 'Functions',
    subdomain: 'Interpreting Functions',
    title: 'Advanced Function Analysis',
    description: 'Graph functions expressed symbolically and show key features of the graph',
    keywords: ['functions', 'graphing', 'domain', 'range', 'intercepts', 'asymptotes'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  }
];

// English Language Arts Standards (Common Core aligned)
export const ELA_STANDARDS: LearningStandard[] = [
  // Grade 3 ELA
  {
    id: 'CCSS.ELA.3.RL.1',
    subject: 'ela',
    gradeLevel: 3,
    domain: 'Reading Literature',
    subdomain: 'Key Ideas and Details',
    title: 'Ask and Answer Questions',
    description: 'Ask and answer questions to demonstrate understanding of a text',
    keywords: ['reading comprehension', 'questions', 'text evidence', 'understanding'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  {
    id: 'CCSS.ELA.3.W.1',
    subject: 'ela',
    gradeLevel: 3,
    domain: 'Writing',
    subdomain: 'Text Types and Purposes',
    title: 'Opinion Writing',
    description: 'Write opinion pieces on topics or texts, supporting a point of view with reasons',
    keywords: ['opinion writing', 'point of view', 'reasons', 'supporting details'],
    complexityLevel: 3,
    bloomsLevel: 'create'
  },

  // Grade 4 ELA
  {
    id: 'CCSS.ELA.4.RL.2',
    subject: 'ela',
    gradeLevel: 4,
    domain: 'Reading Literature',
    subdomain: 'Key Ideas and Details',
    title: 'Theme and Summary',
    description: 'Determine a theme of a story, drama, or poem and summarize the text',
    keywords: ['theme', 'summary', 'main idea', 'supporting details', 'literature'],
    complexityLevel: 3,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.ELA.4.L.4',
    subject: 'ela',
    gradeLevel: 4,
    domain: 'Language',
    subdomain: 'Vocabulary Acquisition and Use',
    title: 'Context Clues',
    description: 'Determine or clarify the meaning of unknown words using context clues',
    keywords: ['vocabulary', 'context clues', 'unknown words', 'meaning'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },

  // Grade 5 ELA
  {
    id: 'CCSS.ELA.5.RI.8',
    subject: 'ela',
    gradeLevel: 5,
    domain: 'Reading Informational Text',
    subdomain: 'Integration of Knowledge and Ideas',
    title: 'Evaluate Arguments',
    description: 'Explain how an author uses reasons and evidence to support particular points',
    keywords: ['arguments', 'evidence', 'reasons', 'author\'s purpose', 'informational text'],
    complexityLevel: 4,
    bloomsLevel: 'evaluate'
  },
  {
    id: 'CCSS.ELA.5.W.2',
    subject: 'ela',
    gradeLevel: 5,
    domain: 'Writing',
    subdomain: 'Text Types and Purposes',
    title: 'Informative Writing',
    description: 'Write informative/explanatory texts to examine a topic with facts and examples',
    keywords: ['informative writing', 'explanatory', 'facts', 'examples', 'topic'],
    complexityLevel: 3,
    bloomsLevel: 'create'
  },

  // Grade 6 ELA
  {
    id: 'CCSS.ELA.6.RL.4',
    subject: 'ela',
    gradeLevel: 6,
    domain: 'Reading Literature',
    subdomain: 'Craft and Structure',
    title: 'Figurative Language',
    description: 'Determine the meaning of words and phrases including figurative language',
    keywords: ['figurative language', 'metaphor', 'simile', 'connotation', 'word choice'],
    complexityLevel: 3,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.ELA.6.SL.4',
    subject: 'ela',
    gradeLevel: 6,
    domain: 'Speaking and Listening',
    subdomain: 'Presentation of Knowledge and Ideas',
    title: 'Oral Presentations',
    description: 'Present claims and findings with relevant evidence and sound reasoning',
    keywords: ['oral presentation', 'claims', 'evidence', 'reasoning', 'speaking'],
    complexityLevel: 3,
    bloomsLevel: 'create'
  },

  // Grade 7 ELA
  {
    id: 'CCSS.ELA.7.RL.3',
    subject: 'ela',
    gradeLevel: 7,
    domain: 'Reading Literature',
    subdomain: 'Key Ideas and Details',
    title: 'Character Analysis',
    description: 'Analyze how particular elements interact and affect each other in a story',
    keywords: ['character analysis', 'plot', 'setting', 'interactions', 'literary elements'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.ELA.7.W.1',
    subject: 'ela',
    gradeLevel: 7,
    domain: 'Writing',
    subdomain: 'Text Types and Purposes',
    title: 'Argumentative Writing',
    description: 'Write arguments to support claims with clear reasons and relevant evidence',
    keywords: ['argumentative writing', 'claims', 'evidence', 'counterclaims', 'reasoning'],
    complexityLevel: 4,
    bloomsLevel: 'create'
  },

  // Grade 8 ELA
  {
    id: 'CCSS.ELA.8.RI.6',
    subject: 'ela',
    gradeLevel: 8,
    domain: 'Reading Informational Text',
    subdomain: 'Craft and Structure',
    title: 'Author\'s Point of View',
    description: 'Determine an author\'s point of view and analyze how they respond to conflicting evidence',
    keywords: ['point of view', 'bias', 'conflicting evidence', 'author\'s purpose', 'perspective'],
    complexityLevel: 4,
    bloomsLevel: 'evaluate'
  },

  // High School ELA (Grades 9-12)
  {
    id: 'CCSS.ELA.9-10.RL.4',
    subject: 'ela',
    gradeLevel: 9,
    domain: 'Reading Literature',
    subdomain: 'Craft and Structure',
    title: 'Advanced Literary Analysis',
    description: 'Determine the meaning of words and phrases as they are used in text including figurative meanings',
    keywords: ['literary analysis', 'figurative language', 'tone', 'mood', 'diction'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },
  {
    id: 'CCSS.ELA.9-10.W.1',
    subject: 'ela',
    gradeLevel: 10,
    domain: 'Writing',
    subdomain: 'Text Types and Purposes',
    title: 'Complex Argumentative Writing',
    description: 'Write arguments to support claims in an analysis of substantive topics using valid reasoning',
    keywords: ['complex arguments', 'substantive topics', 'valid reasoning', 'counterclaims'],
    complexityLevel: 5,
    bloomsLevel: 'create'
  },
  {
    id: 'CCSS.ELA.11-12.RI.7',
    subject: 'ela',
    gradeLevel: 11,
    domain: 'Reading Informational Text',
    subdomain: 'Integration of Knowledge and Ideas',
    title: 'Multiple Source Analysis',
    description: 'Integrate and evaluate multiple sources of information in different media or formats',
    keywords: ['multiple sources', 'integration', 'evaluation', 'media formats', 'information literacy'],
    complexityLevel: 5,
    bloomsLevel: 'evaluate'
  },
  {
    id: 'CCSS.ELA.11-12.SL.4',
    subject: 'ela',
    gradeLevel: 12,
    domain: 'Speaking and Listening',
    subdomain: 'Presentation of Knowledge and Ideas',
    title: 'Advanced Presentations',
    description: 'Present information clearly and concisely using appropriate organization and style',
    keywords: ['advanced presentations', 'organization', 'style', 'audience', 'purpose'],
    complexityLevel: 5,
    bloomsLevel: 'create'
  }
];

// Science Standards (NGSS aligned)
export const SCIENCE_STANDARDS: LearningStandard[] = [
  // Grade 3 Science
  {
    id: '3-LS1-1',
    subject: 'science',
    gradeLevel: 3,
    domain: 'Life Science',
    subdomain: 'Organisms and Environments',
    title: 'Life Cycles',
    description: 'Develop models to describe that organisms have unique and diverse life cycles',
    keywords: ['life cycles', 'organisms', 'development', 'reproduction', 'survival'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  {
    id: '3-PS2-1',
    subject: 'science',
    gradeLevel: 3,
    domain: 'Physical Science',
    subdomain: 'Forces and Interactions',
    title: 'Balanced and Unbalanced Forces',
    description: 'Plan and conduct investigations to provide evidence of the effects of balanced and unbalanced forces',
    keywords: ['forces', 'balanced', 'unbalanced', 'motion', 'investigation'],
    complexityLevel: 3,
    bloomsLevel: 'apply'
  },

  // Grade 4 Science
  {
    id: '4-ESS3-2',
    subject: 'science',
    gradeLevel: 4,
    domain: 'Earth and Space Science',
    subdomain: 'Earth and Human Activity',
    title: 'Natural Resources',
    description: 'Generate and compare multiple solutions to reduce the impacts of natural Earth processes on humans',
    keywords: ['natural resources', 'Earth processes', 'solutions', 'human impact', 'environment'],
    complexityLevel: 4,
    bloomsLevel: 'evaluate'
  },
  {
    id: '4-PS3-2',
    subject: 'science',
    gradeLevel: 4,
    domain: 'Physical Science',
    subdomain: 'Energy',
    title: 'Energy Transfer',
    description: 'Make observations to provide evidence that energy can be transferred from place to place',
    keywords: ['energy', 'transfer', 'motion', 'sound', 'heat', 'electric current'],
    complexityLevel: 3,
    bloomsLevel: 'apply'
  },

  // Grade 5 Science
  {
    id: '5-ESS1-1',
    subject: 'science',
    gradeLevel: 5,
    domain: 'Earth and Space Science',
    subdomain: 'Earth\'s Place in the Universe',
    title: 'Sun\'s Brightness',
    description: 'Develop a model to describe that the sun is a star that appears larger and brighter than other stars',
    keywords: ['sun', 'star', 'brightness', 'distance', 'solar system'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  {
    id: '5-LS2-1',
    subject: 'science',
    gradeLevel: 5,
    domain: 'Life Science',
    subdomain: 'Ecosystems: Interactions, Energy, and Dynamics',
    title: 'Plant Growth Requirements',
    description: 'Develop a model to describe the movement of matter among plants, animals, decomposers, and the environment',
    keywords: ['plants', 'matter', 'decomposers', 'environment', 'ecosystem'],
    complexityLevel: 3,
    bloomsLevel: 'analyze'
  },

  // Middle School Science (Grades 6-8)
  {
    id: 'MS-LS1-1',
    subject: 'science',
    gradeLevel: 6,
    domain: 'Life Science',
    subdomain: 'From Molecules to Organisms: Structures and Processes',
    title: 'Cell Structure and Function',
    description: 'Conduct an investigation to provide evidence that living things are made of cells',
    keywords: ['cells', 'organisms', 'structure', 'function', 'investigation'],
    complexityLevel: 3,
    bloomsLevel: 'apply'
  },
  {
    id: 'MS-PS1-1',
    subject: 'science',
    gradeLevel: 7,
    domain: 'Physical Science',
    subdomain: 'Matter and Its Interactions',
    title: 'Atomic Structure',
    description: 'Develop models to describe the atomic composition of simple molecules and extended structures',
    keywords: ['atoms', 'molecules', 'composition', 'structure', 'matter'],
    complexityLevel: 3,
    bloomsLevel: 'understand'
  },
  {
    id: 'MS-ESS3-3',
    subject: 'science',
    gradeLevel: 8,
    domain: 'Earth and Space Science',
    subdomain: 'Earth and Human Activity',
    title: 'Human Impact on Environment',
    description: 'Apply scientific principles to design a method for monitoring and minimizing human impact',
    keywords: ['human impact', 'environment', 'monitoring', 'scientific principles', 'sustainability'],
    complexityLevel: 4,
    bloomsLevel: 'create'
  },

  // High School Science (Grades 9-12)
  {
    id: 'HS-PS1-1',
    subject: 'science',
    gradeLevel: 9,
    domain: 'Physical Science',
    subdomain: 'Matter and Its Interactions',
    title: 'Periodic Table Patterns',
    description: 'Use the periodic table as a model to predict the relative properties of elements',
    keywords: ['periodic table', 'elements', 'properties', 'patterns', 'atomic structure'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },
  {
    id: 'HS-LS1-1',
    subject: 'science',
    gradeLevel: 10,
    domain: 'Life Science',
    subdomain: 'From Molecules to Organisms: Structures and Processes',
    title: 'Biomolecules',
    description: 'Construct an explanation for how the structure of DNA determines the structure of proteins',
    keywords: ['DNA', 'proteins', 'structure', 'function', 'biomolecules'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },
  {
    id: 'HS-ESS2-1',
    subject: 'science',
    gradeLevel: 11,
    domain: 'Earth and Space Science',
    subdomain: 'Earth\'s Systems',
    title: 'Earth System Interactions',
    description: 'Develop a model to illustrate how Earth\'s internal and surface processes operate',
    keywords: ['Earth systems', 'processes', 'interactions', 'geosphere', 'atmosphere'],
    complexityLevel: 5,
    bloomsLevel: 'create'
  },
  {
    id: 'HS-PS3-3',
    subject: 'science',
    gradeLevel: 12,
    domain: 'Physical Science',
    subdomain: 'Energy',
    title: 'Energy in Chemical Processes',
    description: 'Design, build, and refine a device that works within given constraints to convert one form of energy into another',
    keywords: ['energy conversion', 'chemical processes', 'design', 'constraints', 'engineering'],
    complexityLevel: 5,
    bloomsLevel: 'create'
  }
];

// Social Studies Standards (C3 Framework and NCSS aligned)
export const SOCIAL_STUDIES_STANDARDS: LearningStandard[] = [
  // Grade 3 Social Studies
  {
    id: 'NCSS.3.CIVICS.1',
    subject: 'social-studies',
    gradeLevel: 3,
    domain: 'Civics',
    subdomain: 'Civic Ideals and Practices',
    title: 'Community Rules and Laws',
    description: 'Identify and explain the importance of rules and laws in the school and community',
    keywords: ['rules', 'laws', 'community', 'authority', 'consequences'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },
  {
    id: 'NCSS.3.GEOGRAPHY.1',
    subject: 'social-studies',
    gradeLevel: 3,
    domain: 'Geography',
    subdomain: 'People, Places, and Environments',
    title: 'Geographic Features',
    description: 'Use maps and other geographic tools to identify and describe places and regions',
    keywords: ['maps', 'geographic tools', 'places', 'regions', 'location'],
    complexityLevel: 2,
    bloomsLevel: 'apply'
  },

  // Grade 4 Social Studies
  {
    id: 'NCSS.4.HISTORY.1',
    subject: 'social-studies',
    gradeLevel: 4,
    domain: 'History',
    subdomain: 'Time, Continuity, and Change',
    title: 'Local and State History',
    description: 'Analyze how people, events, and ideas have shaped local and state history',
    keywords: ['local history', 'state history', 'people', 'events', 'change over time'],
    complexityLevel: 3,
    bloomsLevel: 'analyze'
  },
  {
    id: 'NCSS.4.ECONOMICS.1',
    subject: 'social-studies',
    gradeLevel: 4,
    domain: 'Economics',
    subdomain: 'Production, Distribution, and Consumption',
    title: 'Economic Systems',
    description: 'Describe how people in different regions earn a living and meet their needs',
    keywords: ['economic systems', 'production', 'distribution', 'needs', 'wants'],
    complexityLevel: 2,
    bloomsLevel: 'understand'
  },

  // Grade 5 Social Studies
  {
    id: 'NCSS.5.HISTORY.2',
    subject: 'social-studies',
    gradeLevel: 5,
    domain: 'History',
    subdomain: 'Time, Continuity, and Change',
    title: 'Early American History',
    description: 'Analyze the causes and effects of major events in early American history',
    keywords: ['American history', 'causes', 'effects', 'colonial period', 'revolution'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },
  {
    id: 'NCSS.5.CIVICS.2',
    subject: 'social-studies',
    gradeLevel: 5,
    domain: 'Civics',
    subdomain: 'Civic Ideals and Practices',
    title: 'Democratic Principles',
    description: 'Explain the basic principles of democracy and how they are reflected in founding documents',
    keywords: ['democracy', 'principles', 'founding documents', 'Constitution', 'rights'],
    complexityLevel: 3,
    bloomsLevel: 'understand'
  },

  // Grade 6 Social Studies
  {
    id: 'NCSS.6.HISTORY.3',
    subject: 'social-studies',
    gradeLevel: 6,
    domain: 'History',
    subdomain: 'Time, Continuity, and Change',
    title: 'Ancient Civilizations',
    description: 'Compare and contrast characteristics of ancient civilizations and their lasting contributions',
    keywords: ['ancient civilizations', 'compare', 'contrast', 'contributions', 'culture'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },
  {
    id: 'NCSS.6.GEOGRAPHY.2',
    subject: 'social-studies',
    gradeLevel: 6,
    domain: 'Geography',
    subdomain: 'People, Places, and Environments',
    title: 'Human-Environment Interaction',
    description: 'Analyze how physical geography influences human activities and settlement patterns',
    keywords: ['physical geography', 'human activities', 'settlement patterns', 'environment'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },

  // Grade 7 Social Studies
  {
    id: 'NCSS.7.HISTORY.4',
    subject: 'social-studies',
    gradeLevel: 7,
    domain: 'History',
    subdomain: 'Time, Continuity, and Change',
    title: 'Medieval and Renaissance Periods',
    description: 'Evaluate the impact of the Medieval and Renaissance periods on modern society',
    keywords: ['medieval', 'renaissance', 'impact', 'modern society', 'cultural change'],
    complexityLevel: 4,
    bloomsLevel: 'evaluate'
  },
  {
    id: 'NCSS.7.ECONOMICS.2',
    subject: 'social-studies',
    gradeLevel: 7,
    domain: 'Economics',
    subdomain: 'Production, Distribution, and Consumption',
    title: 'Trade and Commerce',
    description: 'Analyze the development of trade routes and their impact on cultural exchange',
    keywords: ['trade routes', 'commerce', 'cultural exchange', 'economic systems'],
    complexityLevel: 4,
    bloomsLevel: 'analyze'
  },

  // Grade 8 Social Studies
  {
    id: 'NCSS.8.HISTORY.5',
    subject: 'social-studies',
    gradeLevel: 8,
    domain: 'History',
    subdomain: 'Time, Continuity, and Change',
    title: 'American Revolution to Civil War',
    description: 'Analyze major events and movements from the American Revolution through the Civil War',
    keywords: ['American Revolution', 'Civil War', 'major events', 'movements', 'national development'],
    complexityLevel: 5,
    bloomsLevel: 'analyze'
  },
  {
    id: 'NCSS.8.CIVICS.3',
    subject: 'social-studies',
    gradeLevel: 8,
    domain: 'Civics',
    subdomain: 'Civic Ideals and Practices',
    title: 'Constitutional Government',
    description: 'Evaluate how the Constitution establishes a framework for government and protects individual rights',
    keywords: ['Constitution', 'government framework', 'individual rights', 'checks and balances'],
    complexityLevel: 4,
    bloomsLevel: 'evaluate'
  },

  // High School Social Studies (Grades 9-12)
  {
    id: 'NCSS.9.HISTORY.6',
    subject: 'social-studies',
    gradeLevel: 9,
    domain: 'History',
    subdomain: 'Time, Continuity, and Change',
    title: 'World History',
    description: 'Analyze patterns of social, political, and economic change in world history',
    keywords: ['world history', 'patterns', 'social change', 'political change', 'economic change'],
    complexityLevel: 5,
    bloomsLevel: 'analyze'
  },
  {
    id: 'NCSS.10.CIVICS.4',
    subject: 'social-studies',
    gradeLevel: 10,
    domain: 'Civics',
    subdomain: 'Civic Ideals and Practices',
    title: 'Comparative Government',
    description: 'Compare and evaluate different forms of government and their effectiveness',
    keywords: ['comparative government', 'forms of government', 'effectiveness', 'political systems'],
    complexityLevel: 5,
    bloomsLevel: 'evaluate'
  },
  {
    id: 'NCSS.11.ECONOMICS.3',
    subject: 'social-studies',
    gradeLevel: 11,
    domain: 'Economics',
    subdomain: 'Production, Distribution, and Consumption',
    title: 'Economic Policy',
    description: 'Analyze the role of government in regulating and promoting economic activity',
    keywords: ['economic policy', 'government regulation', 'economic activity', 'market systems'],
    complexityLevel: 5,
    bloomsLevel: 'analyze'
  },
  {
    id: 'NCSS.12.HISTORY.7',
    subject: 'social-studies',
    gradeLevel: 12,
    domain: 'History',
    subdomain: 'Time, Continuity, and Change',
    title: 'Contemporary Issues',
    description: 'Evaluate contemporary issues using historical perspective and critical thinking skills',
    keywords: ['contemporary issues', 'historical perspective', 'critical thinking', 'analysis'],
    complexityLevel: 5,
    bloomsLevel: 'evaluate'
  }
];

// Combined standards array
export const ALL_STANDARDS: LearningStandard[] = [
  ...MATH_STANDARDS,
  ...ELA_STANDARDS,
  ...SCIENCE_STANDARDS,
  ...SOCIAL_STUDIES_STANDARDS
];

// Grade level mapping for easy access
export const STANDARDS_BY_GRADE: Record<GradeLevel, LearningStandard[]> = {
  3: ALL_STANDARDS.filter(s => s.gradeLevel === 3),
  4: ALL_STANDARDS.filter(s => s.gradeLevel === 4),
  5: ALL_STANDARDS.filter(s => s.gradeLevel === 5),
  6: ALL_STANDARDS.filter(s => s.gradeLevel === 6),
  7: ALL_STANDARDS.filter(s => s.gradeLevel === 7),
  8: ALL_STANDARDS.filter(s => s.gradeLevel === 8),
  9: ALL_STANDARDS.filter(s => s.gradeLevel === 9),
  10: ALL_STANDARDS.filter(s => s.gradeLevel === 10),
  11: ALL_STANDARDS.filter(s => s.gradeLevel === 11),
  12: ALL_STANDARDS.filter(s => s.gradeLevel === 12)
};

// Subject mapping for easy access
export const STANDARDS_BY_SUBJECT: Record<Subject, LearningStandard[]> = {
  'math': MATH_STANDARDS,
  'ela': ELA_STANDARDS,
  'science': SCIENCE_STANDARDS,
  'social-studies': SOCIAL_STUDIES_STANDARDS
};

/**
 * Content Analysis Configuration for Grade Level Assignment
 */
export interface ContentAnalysisConfig {
  keywordWeights: {
    exact: number;
    partial: number;
    related: number;
  };
  complexityIndicators: {
    vocabularyLevel: number;
    conceptualDepth: number;
    prerequisiteComplexity: number;
    cognitiveLoad: number;
  };
  subjectBias: Record<Subject, number>;
}

export const DEFAULT_ANALYSIS_CONFIG: ContentAnalysisConfig = {
  keywordWeights: {
    exact: 1.0,
    partial: 0.6,
    related: 0.3
  },
  complexityIndicators: {
    vocabularyLevel: 0.25,
    conceptualDepth: 0.3,
    prerequisiteComplexity: 0.25,
    cognitiveLoad: 0.2
  },
  subjectBias: {
    'math': 1.0,
    'ela': 1.0,
    'science': 1.0,
    'social-studies': 1.0
  }
};