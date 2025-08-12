import { Node } from '../types';

// Hierarchical Knowledge Graph with nested subnodes
export const hierarchicalKnowledgeGraph = {
  foundation: {
    communication: [
      { 
        id: 'symbols-meaning', 
        name: 'Symbols & Meaning', 
        prereqs: [], 
        category: 'foundation', 
        domain: 'communication', 
        difficulty: 1, 
        points: 50,
        level: 0,
        isParent: false
      },
      { 
        id: 'sound-patterns', 
        name: 'Sound Patterns', 
        prereqs: [], 
        category: 'foundation', 
        domain: 'communication', 
        difficulty: 1, 
        points: 50,
        level: 0,
        isParent: false
      },
      { 
        id: 'visual-literacy', 
        name: 'Visual Literacy', 
        prereqs: ['symbols-meaning'], 
        category: 'foundation', 
        domain: 'communication', 
        difficulty: 1, 
        points: 75,
        level: 0,
        isParent: false
      },
      { 
        id: 'written-expression', 
        name: 'Written Expression', 
        prereqs: ['symbols-meaning'], 
        category: 'foundation', 
        domain: 'communication', 
        difficulty: 2, 
        points: 100,
        level: 0,
        isParent: false
      }
    ],
    quantitative: [
      { id: 'quantity-concept', name: 'Quantity & Counting', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'patterns-sequences', name: 'Pattern Recognition', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'spatial-reasoning', name: 'Spatial Reasoning', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75, level: 0, isParent: false },
      { id: 'measurement-basics', name: 'Basic Measurement', prereqs: ['quantity-concept'], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75, level: 0, isParent: false }
    ],
    practical: [
      { id: 'self-care', name: 'Personal Care', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 25, level: 0, isParent: false },
      { id: 'tool-use-basic', name: 'Basic Tool Use', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'safety-awareness', name: 'Safety Awareness', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50, level: 0, isParent: false }
    ]
  },
  fundamentals: {
    mathematics: [
      { id: 'number-systems', name: 'Number Systems', prereqs: ['quantity-concept'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'operations', name: 'Math Operations', prereqs: ['number-systems'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'algebra-thinking', name: 'Algebraic Thinking', prereqs: ['operations'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'geometric-thinking', name: 'Geometric Thinking', prereqs: ['spatial-reasoning'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150, level: 0, isParent: false }
    ],
    science: [
      { id: 'scientific-method', name: 'Scientific Method', prereqs: [], category: 'fundamentals', domain: 'science', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'matter-energy', name: 'Matter & Energy', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'living-systems', name: 'Living Systems', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'forces-motion', name: 'Forces & Motion', prereqs: ['matter-energy'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150, level: 0, isParent: false }
    ],
    practical_skills: [
      { id: 'cooking-fundamentals', name: 'Cooking Basics', prereqs: ['measurement-basics', 'safety-awareness'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'digital-literacy', name: 'Digital Literacy', prereqs: [], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'money-management', name: 'Money Management', prereqs: ['operations'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'basic-repairs', name: 'Basic Repairs', prereqs: ['tool-use-basic'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false }
    ]
  },
  domains: {
    mathematics: [
      {
        id: 'calculus-parent',
        name: 'Calculus',
        prereqs: ['algebra-thinking'],
        category: 'domains',
        domain: 'mathematics',
        difficulty: 4,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'limits', name: 'Limits & Continuity', parentId: 'calculus-parent', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'derivatives', name: 'Derivatives', parentId: 'calculus-parent', prereqs: ['limits'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'integrals', name: 'Integrals', parentId: 'calculus-parent', prereqs: ['derivatives'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'differential-equations', name: 'Differential Equations', parentId: 'calculus-parent', prereqs: ['integrals'], category: 'domains', domain: 'mathematics', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'multivariable-calc', name: 'Multivariable Calculus', parentId: 'calculus-parent', prereqs: ['integrals'], category: 'domains', domain: 'mathematics', difficulty: 5, points: 300, level: 1, isParent: false }
        ]
      },
      {
        id: 'statistics-parent',
        name: 'Statistics & Probability',
        prereqs: ['algebra-thinking'],
        category: 'domains',
        domain: 'mathematics',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'descriptive-stats', name: 'Descriptive Statistics', parentId: 'statistics-parent', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 2, points: 125, level: 1, isParent: false },
          { id: 'probability-theory', name: 'Probability Theory', parentId: 'statistics-parent', prereqs: ['descriptive-stats'], category: 'domains', domain: 'mathematics', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'hypothesis-testing', name: 'Hypothesis Testing', parentId: 'statistics-parent', prereqs: ['probability-theory'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'regression-analysis', name: 'Regression Analysis', parentId: 'statistics-parent', prereqs: ['hypothesis-testing'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'bayesian-stats', name: 'Bayesian Statistics', parentId: 'statistics-parent', prereqs: ['probability-theory'], category: 'domains', domain: 'mathematics', difficulty: 5, points: 250, level: 1, isParent: false }
        ]
      },
      { id: 'linear-systems', name: 'Linear Algebra', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 0, isParent: false }
    ],
    physics: [
      { id: 'quantum-mechanics', name: 'Quantum Mechanics', prereqs: ['forces-motion', 'calculus-concepts'], category: 'domains', domain: 'physics', difficulty: 5, points: 300, level: 0, isParent: false },
      { id: 'thermodynamics', name: 'Thermodynamics', prereqs: ['matter-energy'], category: 'domains', domain: 'physics', difficulty: 4, points: 200, level: 0, isParent: false },
      { id: 'electromagnetism', name: 'Electromagnetism', prereqs: ['forces-motion'], category: 'domains', domain: 'physics', difficulty: 4, points: 200, level: 0, isParent: false }
    ],
    biology: [
      {
        id: 'cell-biology-parent',
        name: 'Cell Biology',
        prereqs: ['living-systems'],
        category: 'domains',
        domain: 'biology',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'cell-structure', name: 'Cell Structure', parentId: 'cell-biology-parent', prereqs: ['living-systems'], category: 'domains', domain: 'biology', difficulty: 2, points: 125, level: 1, isParent: false },
          { id: 'cell-membrane', name: 'Cell Membrane', parentId: 'cell-biology-parent', prereqs: ['cell-structure'], category: 'domains', domain: 'biology', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'cellular-respiration', name: 'Cellular Respiration', parentId: 'cell-biology-parent', prereqs: ['cell-structure'], category: 'domains', domain: 'biology', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'photosynthesis', name: 'Photosynthesis', parentId: 'cell-biology-parent', prereqs: ['cellular-respiration'], category: 'domains', domain: 'biology', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'cell-division', name: 'Cell Division', parentId: 'cell-biology-parent', prereqs: ['cell-structure'], category: 'domains', domain: 'biology', difficulty: 3, points: 175, level: 1, isParent: false }
        ]
      },
      {
        id: 'genetics-parent',
        name: 'Genetics',
        prereqs: ['cell-biology-parent'],
        category: 'domains',
        domain: 'biology',
        difficulty: 4,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'mendelian-genetics', name: 'Mendelian Genetics', parentId: 'genetics-parent', prereqs: ['cell-biology-parent'], category: 'domains', domain: 'biology', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'molecular-genetics', name: 'Molecular Genetics', parentId: 'genetics-parent', prereqs: ['mendelian-genetics'], category: 'domains', domain: 'biology', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'gene-expression', name: 'Gene Expression', parentId: 'genetics-parent', prereqs: ['molecular-genetics'], category: 'domains', domain: 'biology', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'genetic-engineering', name: 'Genetic Engineering', parentId: 'genetics-parent', prereqs: ['gene-expression'], category: 'domains', domain: 'biology', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'genomics', name: 'Genomics', parentId: 'genetics-parent', prereqs: ['molecular-genetics'], category: 'domains', domain: 'biology', difficulty: 5, points: 250, level: 1, isParent: false }
        ]
      },
      { id: 'ecology', name: 'Ecology', prereqs: ['living-systems'], category: 'domains', domain: 'biology', difficulty: 3, points: 175, level: 0, isParent: false },
      { id: 'evolution', name: 'Evolution', prereqs: ['genetics-parent', 'ecology'], category: 'domains', domain: 'biology', difficulty: 4, points: 200, level: 0, isParent: false }
    ],
    computer_science: [
      { id: 'programming-basics', name: 'Programming Fundamentals', prereqs: ['digital-literacy'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150, level: 0, isParent: false },
      {
        id: 'algorithms-parent',
        name: 'Algorithms & Data Structures',
        prereqs: ['programming-basics'],
        category: 'domains',
        domain: 'computer_science',
        difficulty: 4,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'arrays-lists', name: 'Arrays & Lists', parentId: 'algorithms-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'computer_science', difficulty: 2, points: 100, level: 1, isParent: false },
          { id: 'trees-graphs', name: 'Trees & Graphs', parentId: 'algorithms-parent', prereqs: ['arrays-lists'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'sorting-algorithms', name: 'Sorting Algorithms', parentId: 'algorithms-parent', prereqs: ['arrays-lists'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'search-algorithms', name: 'Search Algorithms', parentId: 'algorithms-parent', prereqs: ['trees-graphs'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'dynamic-programming', name: 'Dynamic Programming', parentId: 'algorithms-parent', prereqs: ['sorting-algorithms'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'graph-algorithms', name: 'Graph Algorithms', parentId: 'algorithms-parent', prereqs: ['trees-graphs'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200, level: 1, isParent: false }
        ]
      },
      {
        id: 'machine-learning-parent',
        name: 'Machine Learning',
        prereqs: ['algorithms-parent', 'statistics-parent'],
        category: 'domains',
        domain: 'computer_science',
        difficulty: 5,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'supervised-learning', name: 'Supervised Learning', parentId: 'machine-learning-parent', prereqs: ['statistics-parent'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'unsupervised-learning', name: 'Unsupervised Learning', parentId: 'machine-learning-parent', prereqs: ['supervised-learning'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'neural-networks', name: 'Neural Networks', parentId: 'machine-learning-parent', prereqs: ['supervised-learning'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'deep-learning', name: 'Deep Learning', parentId: 'machine-learning-parent', prereqs: ['neural-networks'], category: 'domains', domain: 'computer_science', difficulty: 6, points: 300, level: 1, isParent: false },
          { id: 'reinforcement-learning', name: 'Reinforcement Learning', parentId: 'machine-learning-parent', prereqs: ['supervised-learning'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 275, level: 1, isParent: false },
          { id: 'nlp', name: 'Natural Language Processing', parentId: 'machine-learning-parent', prereqs: ['deep-learning'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 275, level: 1, isParent: false }
        ]
      },
      {
        id: 'web-dev-parent',
        name: 'Web Development',
        prereqs: ['programming-basics'],
        category: 'domains',
        domain: 'computer_science',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'html-css', name: 'HTML & CSS', parentId: 'web-dev-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'computer_science', difficulty: 2, points: 100, level: 1, isParent: false },
          { id: 'javascript-dom', name: 'JavaScript & DOM', parentId: 'web-dev-parent', prereqs: ['html-css'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'frontend-frameworks', name: 'Frontend Frameworks', parentId: 'web-dev-parent', prereqs: ['javascript-dom'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'backend-development', name: 'Backend Development', parentId: 'web-dev-parent', prereqs: ['javascript-dom'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'databases', name: 'Databases', parentId: 'web-dev-parent', prereqs: ['backend-development'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 175, level: 1, isParent: false },
          { id: 'devops', name: 'DevOps & Deployment', parentId: 'web-dev-parent', prereqs: ['backend-development'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 225, level: 1, isParent: false }
        ]
      }
    ],
    practical_living: [
      { id: 'gardening', name: 'Gardening', prereqs: ['living-systems'], category: 'domains', domain: 'practical', difficulty: 2, points: 125, level: 0, isParent: false },
      { id: 'home-maintenance', name: 'Home Maintenance', prereqs: ['basic-repairs'], category: 'domains', domain: 'practical', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'woodworking', name: 'Woodworking', prereqs: ['tool-use-basic', 'geometric-thinking'], category: 'domains', domain: 'practical', difficulty: 3, points: 175, level: 0, isParent: false },
      { id: 'auto-mechanics', name: 'Auto Mechanics', prereqs: ['forces-motion', 'basic-repairs'], category: 'domains', domain: 'practical', difficulty: 4, points: 200, level: 0, isParent: false }
    ],
    health_wellness: [
      { id: 'nutrition', name: 'Nutrition Science', prereqs: ['cooking-fundamentals', 'cellular-processes'], category: 'domains', domain: 'health', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'exercise-physiology', name: 'Exercise Science', prereqs: ['living-systems'], category: 'domains', domain: 'health', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'mental-health', name: 'Mental Health', prereqs: [], category: 'domains', domain: 'health', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'first-aid', name: 'First Aid', prereqs: ['safety-awareness'], category: 'domains', domain: 'health', difficulty: 2, points: 100, level: 0, isParent: false }
    ],
    business: [
      { id: 'entrepreneurship', name: 'Entrepreneurship', prereqs: ['money-management'], category: 'domains', domain: 'business', difficulty: 3, points: 175, level: 0, isParent: false },
      { id: 'marketing', name: 'Marketing', prereqs: ['written-expression'], category: 'domains', domain: 'business', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'accounting', name: 'Accounting', prereqs: ['money-management'], category: 'domains', domain: 'business', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'project-management', name: 'Project Management', prereqs: [], category: 'domains', domain: 'business', difficulty: 3, points: 150, level: 0, isParent: false }
    ],
    arts: [
      {
        id: 'visual-arts-parent',
        name: 'Visual Arts',
        prereqs: ['visual-literacy'],
        category: 'domains',
        domain: 'arts',
        difficulty: 2,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'drawing-basics', name: 'Drawing Basics', parentId: 'visual-arts-parent', prereqs: ['visual-literacy'], category: 'domains', domain: 'arts', difficulty: 2, points: 100, level: 1, isParent: false },
          { id: 'painting', name: 'Painting', parentId: 'visual-arts-parent', prereqs: ['drawing-basics'], category: 'domains', domain: 'arts', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'sculpture', name: 'Sculpture', parentId: 'visual-arts-parent', prereqs: ['drawing-basics'], category: 'domains', domain: 'arts', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'digital-art', name: 'Digital Art', parentId: 'visual-arts-parent', prereqs: ['drawing-basics'], category: 'domains', domain: 'arts', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'art-history', name: 'Art History', parentId: 'visual-arts-parent', prereqs: ['visual-literacy'], category: 'domains', domain: 'arts', difficulty: 2, points: 125, level: 1, isParent: false }
        ]
      },
      {
        id: 'music-parent',
        name: 'Music',
        prereqs: ['sound-patterns'],
        category: 'domains',
        domain: 'arts',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'music-theory-basics', name: 'Music Theory Basics', parentId: 'music-parent', prereqs: ['sound-patterns'], category: 'domains', domain: 'arts', difficulty: 2, points: 125, level: 1, isParent: false },
          { id: 'instrument-piano', name: 'Piano', parentId: 'music-parent', prereqs: ['music-theory-basics'], category: 'domains', domain: 'arts', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'instrument-guitar', name: 'Guitar', parentId: 'music-parent', prereqs: ['music-theory-basics'], category: 'domains', domain: 'arts', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'composition', name: 'Music Composition', parentId: 'music-parent', prereqs: ['music-theory-basics'], category: 'domains', domain: 'arts', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'music-production', name: 'Music Production', parentId: 'music-parent', prereqs: ['composition'], category: 'domains', domain: 'arts', difficulty: 4, points: 200, level: 1, isParent: false }
        ]
      },
      { id: 'creative-writing', name: 'Creative Writing', prereqs: ['written-expression'], category: 'domains', domain: 'arts', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'photography', name: 'Photography', prereqs: ['visual-arts-parent'], category: 'domains', domain: 'arts', difficulty: 2, points: 125, level: 0, isParent: false }
    ],
    // Hierarchical Languages Node with Subnodes
    languages: [
      { 
        id: 'language-fundamentals', 
        name: 'Language Learning Basics', 
        prereqs: ['written-expression'], 
        category: 'domains', 
        domain: 'languages', 
        difficulty: 2, 
        points: 100,
        level: 0,
        isParent: false
      },
      {
        id: 'languages-parent',
        name: 'World Languages',
        prereqs: ['language-fundamentals'],
        category: 'domains',
        domain: 'languages',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          // European Languages
          { id: 'spanish', name: 'Spanish', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200, level: 1, isParent: false },
          { id: 'french', name: 'French', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200, level: 1, isParent: false },
          { id: 'german', name: 'German', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 4, points: 225, level: 1, isParent: false },
          { id: 'italian', name: 'Italian', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200, level: 1, isParent: false },
          { id: 'portuguese', name: 'Portuguese', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200, level: 1, isParent: false },
          { id: 'russian', name: 'Russian', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 4, points: 250, level: 1, isParent: false },
          // Asian Languages
          { id: 'chinese', name: 'Chinese (Mandarin)', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300, level: 1, isParent: false },
          { id: 'japanese', name: 'Japanese', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300, level: 1, isParent: false },
          { id: 'korean', name: 'Korean', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300, level: 1, isParent: false },
          { id: 'hindi', name: 'Hindi', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 4, points: 250, level: 1, isParent: false },
          // Middle Eastern & African Languages
          { id: 'arabic', name: 'Arabic', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300, level: 1, isParent: false },
          { id: 'hebrew', name: 'Hebrew', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 4, points: 250, level: 1, isParent: false },
          { id: 'swahili', name: 'Swahili', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200, level: 1, isParent: false }
        ]
      },
      {
        id: 'programming-languages-parent',
        name: 'Programming Languages',
        prereqs: ['programming-basics'],
        category: 'domains',
        domain: 'languages',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        isExpanded: false,
        subnodes: [
          { id: 'javascript', name: 'JavaScript', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'python', name: 'Python', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'java', name: 'Java', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'csharp', name: 'C#', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'cpp', name: 'C++', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'rust', name: 'Rust', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'go', name: 'Go', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'swift', name: 'Swift', parentId: 'programming-languages-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'languages', difficulty: 4, points: 200, level: 1, isParent: false }
        ]
      }
    ]
  },
  mastery: [
    { id: 'quantum-computing', name: 'Quantum Computing', prereqs: ['quantum-mechanics', 'algorithms-parent'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500, level: 0, isParent: false },
    { id: 'artificial-general-intelligence', name: 'AGI', prereqs: ['machine-learning-parent'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500, level: 0, isParent: false },
    { id: 'master-gardener', name: 'Master Gardener', prereqs: ['gardening', 'ecology'], category: 'mastery', domain: 'practical', difficulty: 5, points: 400, level: 0, isParent: false },
    { id: 'master-chef', name: 'Master Chef', prereqs: ['cooking-fundamentals', 'nutrition'], category: 'mastery', domain: 'practical', difficulty: 5, points: 400, level: 0, isParent: false },
    {
      id: 'polyglot-master',
      name: 'Polyglot Master',
      prereqs: ['spanish', 'french', 'german', 'chinese', 'japanese'],
      category: 'mastery',
      domain: 'languages',
      difficulty: 6,
      points: 1000,
      level: 0,
      isParent: false
    }
  ]
};

// Helper function to get all nodes including subnodes
export const getAllHierarchicalNodes = (expandedNodes: Set<string> = new Set()): Node[] => {
  const nodes: Node[] = [];
  let index = 0;
  let globalY = 80; // Start with some padding from top
  
  // Add category labels as special nodes
  const categoryLabels: { [key: string]: { y: number, name: string } } = {};
  
  // Process each category
  Object.entries(hierarchicalKnowledgeGraph).forEach(([categoryName, domains]) => {
    // Store category position for label
    categoryLabels[categoryName] = { y: globalY - 40, name: categoryName.toUpperCase() };
    let categoryMaxY = globalY;
    
    if (typeof domains === 'object' && !Array.isArray(domains)) {
      // Process each domain in the category
      Object.entries(domains).forEach(([, domainNodes], domainIndex) => {
        const domainX = 50 + (domainIndex % 3) * 400; // 3 columns max, better spacing
        const domainY = globalY + Math.floor(domainIndex / 3) * 400; // Row spacing for domains
        let currentY = domainY;
        
        // Process nodes in this domain
        (domainNodes as Node[]).forEach((node, nodeIndex) => {
          // Position main nodes
          const nodeX = domainX + (nodeIndex % 2) * 150; // 2 nodes per row in domain
          const nodeY = currentY + Math.floor(nodeIndex / 2) * 130;
          
          const processedNode = {
            ...node,
            index: index++,
            x: nodeX,
            y: nodeY
          };
          nodes.push(processedNode);
          
          // Track max Y for this node
          let nodeMaxY = nodeY;
          
          // If this is an expanded parent node, add its subnodes
          if (node.isParent && node.subnodes && expandedNodes.has(node.id)) {
            const subnodesPerRow = 3;
            const subnodeY = nodeY + 110; // Space below parent
            
            node.subnodes.forEach((subnode, subIndex) => {
              const row = Math.floor(subIndex / subnodesPerRow);
              const col = subIndex % subnodesPerRow;
              
              const processedSubnode = {
                ...subnode,
                index: index++,
                x: nodeX + col * 95, // Tighter spacing for subnodes
                y: subnodeY + row * 95
              };
              nodes.push(processedSubnode);
              
              // Update max Y based on subnode position
              nodeMaxY = Math.max(nodeMaxY, processedSubnode.y);
            });
            
            // Update currentY to account for expanded subnodes
            const totalRows = Math.ceil(node.subnodes.length / subnodesPerRow);
            currentY = subnodeY + totalRows * 95 + 30; // Add padding after subnodes
          }
          
          // Update category max Y
          categoryMaxY = Math.max(categoryMaxY, nodeMaxY + 100);
        });
      });
    } else if (Array.isArray(domains)) {
      // Process mastery nodes (single array)
      const currentX = 50;
      (domains as Node[]).forEach((node, nodeIndex) => {
        const processedNode = {
          ...node,
          index: index++,
          x: currentX + nodeIndex * 180,
          y: globalY
        };
        nodes.push(processedNode);
        categoryMaxY = Math.max(categoryMaxY, globalY + 120);
      });
    }
    
    // Move to next category with proper spacing
    globalY = categoryMaxY + 80; // Add spacing between categories
  });
  
  // Add category labels to the export
  const nodesWithLabels = nodes as Node[] & { categoryLabels: typeof categoryLabels };
  nodesWithLabels.categoryLabels = categoryLabels;
  
  return nodesWithLabels;
};

// Helper to get category labels
export const getCategoryLabels = (nodes: Node[]): { [key: string]: { y: number, name: string } } => {
  const nodesWithLabels = nodes as Node[] & { categoryLabels?: { [key: string]: { y: number, name: string } } };
  return nodesWithLabels.categoryLabels || {};
};