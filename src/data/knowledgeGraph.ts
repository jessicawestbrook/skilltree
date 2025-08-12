import { Node } from '../types';

// Comprehensive Knowledge Graph
export const knowledgeGraph = {
  foundation: {
    communication: [
      { id: 'symbols-meaning', name: 'Symbols & Meaning', prereqs: [], category: 'foundation', domain: 'communication', difficulty: 1, points: 50 },
      { id: 'sound-patterns', name: 'Sound Patterns', prereqs: [], category: 'foundation', domain: 'communication', difficulty: 1, points: 50 },
      { id: 'visual-literacy', name: 'Visual Literacy', prereqs: ['symbols-meaning'], category: 'foundation', domain: 'communication', difficulty: 1, points: 75 },
      { id: 'written-expression', name: 'Written Expression', prereqs: ['symbols-meaning'], category: 'foundation', domain: 'communication', difficulty: 2, points: 100 }
    ],
    quantitative: [
      { id: 'quantity-concept', name: 'Quantity & Counting', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50 },
      { id: 'patterns-sequences', name: 'Pattern Recognition', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50 },
      { id: 'spatial-reasoning', name: 'Spatial Reasoning', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75 },
      { id: 'measurement-basics', name: 'Basic Measurement', prereqs: ['quantity-concept'], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75 }
    ],
    practical: [
      { id: 'self-care', name: 'Personal Care', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 25 },
      { id: 'tool-use-basic', name: 'Basic Tool Use', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50 },
      { id: 'safety-awareness', name: 'Safety Awareness', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50 }
    ]
  },
  fundamentals: {
    mathematics: [
      { id: 'number-systems', name: 'Number Systems', prereqs: ['quantity-concept'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100 },
      { id: 'operations', name: 'Math Operations', prereqs: ['number-systems'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100 },
      { id: 'algebra-thinking', name: 'Algebraic Thinking', prereqs: ['operations'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150 },
      { id: 'geometric-thinking', name: 'Geometric Thinking', prereqs: ['spatial-reasoning'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150 }
    ],
    science: [
      { id: 'scientific-method', name: 'Scientific Method', prereqs: [], category: 'fundamentals', domain: 'science', difficulty: 2, points: 100 },
      { id: 'matter-energy', name: 'Matter & Energy', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150 },
      { id: 'living-systems', name: 'Living Systems', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150 },
      { id: 'forces-motion', name: 'Forces & Motion', prereqs: ['matter-energy'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150 }
    ],
    practical_skills: [
      { id: 'cooking-fundamentals', name: 'Cooking Basics', prereqs: ['measurement-basics', 'safety-awareness'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 },
      { id: 'digital-literacy', name: 'Digital Literacy', prereqs: [], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 },
      { id: 'money-management', name: 'Money Management', prereqs: ['operations'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 },
      { id: 'basic-repairs', name: 'Basic Repairs', prereqs: ['tool-use-basic'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100 }
    ]
  },
  domains: {
    mathematics: [
      { id: 'calculus-concepts', name: 'Calculus', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200 },
      { id: 'statistics-probability', name: 'Statistics', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 3, points: 175 },
      { id: 'linear-systems', name: 'Linear Algebra', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200 }
    ],
    physics: [
      { id: 'quantum-mechanics', name: 'Quantum Mechanics', prereqs: ['forces-motion', 'calculus-concepts'], category: 'domains', domain: 'physics', difficulty: 5, points: 300 },
      { id: 'thermodynamics', name: 'Thermodynamics', prereqs: ['matter-energy'], category: 'domains', domain: 'physics', difficulty: 4, points: 200 },
      { id: 'electromagnetism', name: 'Electromagnetism', prereqs: ['forces-motion'], category: 'domains', domain: 'physics', difficulty: 4, points: 200 }
    ],
    biology: [
      { id: 'cellular-processes', name: 'Cell Biology', prereqs: ['living-systems'], category: 'domains', domain: 'biology', difficulty: 3, points: 175 },
      { id: 'genetics', name: 'Genetics', prereqs: ['cellular-processes'], category: 'domains', domain: 'biology', difficulty: 4, points: 200 },
      { id: 'ecology', name: 'Ecology', prereqs: ['living-systems'], category: 'domains', domain: 'biology', difficulty: 3, points: 175 },
      { id: 'evolution', name: 'Evolution', prereqs: ['genetics', 'ecology'], category: 'domains', domain: 'biology', difficulty: 4, points: 200 }
    ],
    computer_science: [
      { id: 'programming-basics', name: 'Programming', prereqs: ['digital-literacy'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150 },
      { id: 'algorithms', name: 'Algorithms', prereqs: ['programming-basics'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200 },
      { id: 'machine-learning', name: 'Machine Learning', prereqs: ['algorithms', 'statistics-probability'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 300 },
      { id: 'web-development', name: 'Web Development', prereqs: ['programming-basics'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150 }
    ],
    practical_living: [
      { id: 'gardening', name: 'Gardening', prereqs: ['living-systems'], category: 'domains', domain: 'practical', difficulty: 2, points: 125 },
      { id: 'home-maintenance', name: 'Home Maintenance', prereqs: ['basic-repairs'], category: 'domains', domain: 'practical', difficulty: 3, points: 150 },
      { id: 'woodworking', name: 'Woodworking', prereqs: ['tool-use-basic', 'geometric-thinking'], category: 'domains', domain: 'practical', difficulty: 3, points: 175 },
      { id: 'auto-mechanics', name: 'Auto Mechanics', prereqs: ['forces-motion', 'basic-repairs'], category: 'domains', domain: 'practical', difficulty: 4, points: 200 }
    ],
    health_wellness: [
      { id: 'nutrition', name: 'Nutrition Science', prereqs: ['cooking-fundamentals', 'cellular-processes'], category: 'domains', domain: 'health', difficulty: 3, points: 150 },
      { id: 'exercise-physiology', name: 'Exercise Science', prereqs: ['living-systems'], category: 'domains', domain: 'health', difficulty: 3, points: 150 },
      { id: 'mental-health', name: 'Mental Health', prereqs: [], category: 'domains', domain: 'health', difficulty: 3, points: 150 },
      { id: 'first-aid', name: 'First Aid', prereqs: ['safety-awareness'], category: 'domains', domain: 'health', difficulty: 2, points: 100 }
    ],
    business: [
      { id: 'entrepreneurship', name: 'Entrepreneurship', prereqs: ['money-management'], category: 'domains', domain: 'business', difficulty: 3, points: 175 },
      { id: 'marketing', name: 'Marketing', prereqs: ['written-expression'], category: 'domains', domain: 'business', difficulty: 3, points: 150 },
      { id: 'accounting', name: 'Accounting', prereqs: ['money-management'], category: 'domains', domain: 'business', difficulty: 3, points: 150 },
      { id: 'project-management', name: 'Project Management', prereqs: [], category: 'domains', domain: 'business', difficulty: 3, points: 150 }
    ],
    arts: [
      { id: 'visual-composition', name: 'Visual Arts', prereqs: ['visual-literacy'], category: 'domains', domain: 'arts', difficulty: 2, points: 125 },
      { id: 'music-theory', name: 'Music Theory', prereqs: ['sound-patterns'], category: 'domains', domain: 'arts', difficulty: 3, points: 150 },
      { id: 'creative-writing', name: 'Creative Writing', prereqs: ['written-expression'], category: 'domains', domain: 'arts', difficulty: 3, points: 150 },
      { id: 'photography', name: 'Photography', prereqs: ['visual-composition'], category: 'domains', domain: 'arts', difficulty: 2, points: 125 }
    ],
    languages: [
      { id: 'language-fundamentals', name: 'Language Learning Basics', prereqs: ['written-expression'], category: 'domains', domain: 'languages', difficulty: 2, points: 100 },
      { id: 'spanish', name: 'Spanish', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200 },
      { id: 'french', name: 'French', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200 },
      { id: 'german', name: 'German', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 4, points: 225 },
      { id: 'chinese', name: 'Chinese (Mandarin)', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300 },
      { id: 'japanese', name: 'Japanese', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300 },
      { id: 'arabic', name: 'Arabic', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300 },
      { id: 'portuguese', name: 'Portuguese', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200 },
      { id: 'italian', name: 'Italian', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200 },
      { id: 'russian', name: 'Russian', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 4, points: 250 }
    ]
  },
  mastery: [
    { id: 'quantum-computing', name: 'Quantum Computing', prereqs: ['quantum-mechanics', 'algorithms'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500 },
    { id: 'artificial-general-intelligence', name: 'AGI', prereqs: ['machine-learning'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500 },
    { id: 'master-gardener', name: 'Master Gardener', prereqs: ['gardening', 'ecology'], category: 'mastery', domain: 'practical', difficulty: 5, points: 400 },
    { id: 'master-chef', name: 'Master Chef', prereqs: ['cooking-fundamentals', 'nutrition'], category: 'mastery', domain: 'practical', difficulty: 5, points: 400 }
  ]
};

// Flatten all nodes for easier access
export const getAllNodes = (): Node[] => {
  const nodes: Node[] = [];
  let index = 0;
  
  // Process each category
  Object.entries(knowledgeGraph).forEach(([, domains]) => {
    if (typeof domains === 'object' && !Array.isArray(domains)) {
      Object.entries(domains).forEach(([, domainNodes]) => {
        domainNodes.forEach((node: Node) => {
          nodes.push({
            ...node,
            index: index++,
            x: 100 + (index % 8) * 120,
            y: 100 + Math.floor(index / 8) * 120
          });
        });
      });
    } else if (Array.isArray(domains)) {
      domains.forEach((node: Node) => {
        nodes.push({
          ...node,
          index: index++,
          x: 100 + (index % 8) * 120,
          y: 100 + Math.floor(index / 8) * 120
        });
      });
    }
  });
  
  return nodes;
};