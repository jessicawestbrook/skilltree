import { Node } from '../types';

export interface KnowledgeCategory {
  id: string;
  name: string;
  icon?: string;
  color: string;
  description: string;
  subcategories?: KnowledgeCategory[];
  nodes?: Node[];
}

export const knowledgeStructure: KnowledgeCategory = {
  id: 'root',
  name: 'Knowledge Universe',
  color: '#ffffff',
  description: 'The complete universe of human knowledge',
  subcategories: [
    {
      id: 'mathematics',
      name: 'Mathematics',
      color: '#3b82f6',
      description: 'The language of patterns and logic',
      subcategories: [
        {
          id: 'algebra',
          name: 'Algebra',
          color: '#60a5fa',
          description: 'Study of mathematical symbols and rules',
          nodes: [
            { id: 'basic-algebra', name: 'Basic Algebra', domain: 'algebra', prereqs: [], difficulty: 2, points: 100 },
            { id: 'linear-algebra', name: 'Linear Algebra', domain: 'algebra', prereqs: ['basic-algebra'], difficulty: 3, points: 150 },
            { id: 'abstract-algebra', name: 'Abstract Algebra', domain: 'algebra', prereqs: ['linear-algebra'], difficulty: 5, points: 250 }
          ]
        },
        {
          id: 'analysis',
          name: 'Calculus & Analysis',
          color: '#60a5fa',
          description: 'Study of continuous change and limits',
          nodes: [
            { id: 'calculus-1', name: 'Calculus I', domain: 'analysis', prereqs: ['basic-algebra'], difficulty: 3, points: 150 },
            { id: 'calculus-2', name: 'Calculus II', domain: 'analysis', prereqs: ['calculus-1'], difficulty: 3, points: 150 },
            { id: 'real-analysis', name: 'Real Analysis', domain: 'analysis', prereqs: ['calculus-2'], difficulty: 5, points: 250 },
            { id: 'complex-analysis', name: 'Complex Analysis', domain: 'analysis', prereqs: ['real-analysis'], difficulty: 5, points: 300 }
          ]
        },
        {
          id: 'geometry',
          name: 'Geometry & Topology',
          color: '#60a5fa',
          description: 'Study of shapes, spaces, and structures',
          nodes: [
            { id: 'euclidean-geometry', name: 'Euclidean Geometry', domain: 'geometry', prereqs: [], difficulty: 2, points: 100 },
            { id: 'analytic-geometry', name: 'Analytic Geometry', domain: 'geometry', prereqs: ['euclidean-geometry'], difficulty: 3, points: 150 },
            { id: 'differential-geometry', name: 'Differential Geometry', domain: 'geometry', prereqs: ['calculus-2'], difficulty: 5, points: 250 },
            { id: 'topology', name: 'Topology', domain: 'geometry', prereqs: ['real-analysis'], difficulty: 5, points: 300 }
          ]
        },
        {
          id: 'statistics',
          name: 'Statistics & Probability',
          color: '#60a5fa',
          description: 'Analysis of data and uncertainty',
          nodes: [
            { id: 'descriptive-stats', name: 'Descriptive Statistics', domain: 'statistics', prereqs: [], difficulty: 2, points: 100 },
            { id: 'probability', name: 'Probability Theory', domain: 'statistics', prereqs: ['descriptive-stats'], difficulty: 3, points: 150 },
            { id: 'inferential-stats', name: 'Inferential Statistics', domain: 'statistics', prereqs: ['probability'], difficulty: 4, points: 200 },
            { id: 'bayesian-statistics', name: 'Bayesian Statistics', domain: 'statistics', prereqs: ['inferential-stats'], difficulty: 5, points: 250 }
          ]
        },
        {
          id: 'number-theory',
          name: 'Number Theory',
          color: '#60a5fa',
          description: 'Study of integers and their properties',
          nodes: [
            { id: 'elementary-number-theory', name: 'Elementary Number Theory', domain: 'number-theory', prereqs: [], difficulty: 3, points: 150 },
            { id: 'analytic-number-theory', name: 'Analytic Number Theory', domain: 'number-theory', prereqs: ['complex-analysis'], difficulty: 6, points: 350 },
            { id: 'algebraic-number-theory', name: 'Algebraic Number Theory', domain: 'number-theory', prereqs: ['abstract-algebra'], difficulty: 6, points: 350 }
          ]
        },
        {
          id: 'optimization',
          name: 'Optimization & Operations Research',
          color: '#60a5fa',
          description: 'Finding optimal solutions to mathematical problems',
          nodes: [
            { id: 'linear-programming', name: 'Linear Programming', domain: 'optimization', prereqs: ['linear-algebra'], difficulty: 3, points: 150 },
            { id: 'nonlinear-optimization', name: 'Nonlinear Optimization', domain: 'optimization', prereqs: ['calculus-2'], difficulty: 4, points: 200 },
            { id: 'convex-optimization', name: 'Convex Optimization', domain: 'optimization', prereqs: ['nonlinear-optimization'], difficulty: 5, points: 250 }
          ]
        }
      ]
    },
    {
      id: 'sciences',
      name: 'Natural Sciences',
      color: '#10b981',
      description: 'Understanding the natural world',
      subcategories: [
        {
          id: 'physics',
          name: 'Physics',
          color: '#34d399',
          description: 'Study of matter, energy, and their interactions',
          subcategories: [
            {
              id: 'classical-physics',
              name: 'Classical Physics',
              color: '#6ee7b7',
              description: 'Traditional physics concepts',
              nodes: [
                { id: 'mechanics', name: 'Classical Mechanics', domain: 'classical-physics', prereqs: ['calculus-1'], difficulty: 3, points: 150 },
                { id: 'thermodynamics', name: 'Thermodynamics', domain: 'classical-physics', prereqs: ['mechanics'], difficulty: 4, points: 200 },
                { id: 'electromagnetism', name: 'Electromagnetism', domain: 'classical-physics', prereqs: ['mechanics', 'calculus-2'], difficulty: 4, points: 200 },
                { id: 'optics', name: 'Optics', domain: 'classical-physics', prereqs: ['electromagnetism'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'modern-physics',
              name: 'Modern Physics',
              color: '#6ee7b7',
              description: '20th century physics and beyond',
              nodes: [
                { id: 'special-relativity', name: 'Special Relativity', domain: 'modern-physics', prereqs: ['mechanics'], difficulty: 4, points: 200 },
                { id: 'general-relativity', name: 'General Relativity', domain: 'modern-physics', prereqs: ['special-relativity', 'differential-geometry'], difficulty: 6, points: 350 },
                { id: 'quantum-mechanics', name: 'Quantum Mechanics', domain: 'modern-physics', prereqs: ['linear-algebra', 'mechanics'], difficulty: 5, points: 300 },
                { id: 'quantum-field-theory', name: 'Quantum Field Theory', domain: 'modern-physics', prereqs: ['quantum-mechanics'], difficulty: 6, points: 400 }
              ]
            },
            {
              id: 'astrophysics',
              name: 'Astrophysics',
              color: '#6ee7b7',
              description: 'Physics of celestial objects',
              nodes: [
                { id: 'stellar-physics', name: 'Stellar Physics', domain: 'astrophysics', prereqs: ['thermodynamics'], difficulty: 4, points: 200 },
                { id: 'cosmology', name: 'Cosmology', domain: 'astrophysics', prereqs: ['general-relativity'], difficulty: 5, points: 300 },
                { id: 'black-holes', name: 'Black Hole Physics', domain: 'astrophysics', prereqs: ['general-relativity'], difficulty: 6, points: 350 }
              ]
            }
          ]
        },
        {
          id: 'chemistry',
          name: 'Chemistry',
          color: '#34d399',
          description: 'Study of matter and its properties',
          subcategories: [
            {
              id: 'general-chemistry',
              name: 'General Chemistry',
              color: '#6ee7b7',
              description: 'Fundamental chemical concepts',
              nodes: [
                { id: 'atomic-structure', name: 'Atomic Structure', domain: 'general-chemistry', prereqs: [], difficulty: 2, points: 100 },
                { id: 'chemical-bonding', name: 'Chemical Bonding', domain: 'general-chemistry', prereqs: ['atomic-structure'], difficulty: 2, points: 100 },
                { id: 'stoichiometry', name: 'Stoichiometry', domain: 'general-chemistry', prereqs: ['atomic-structure'], difficulty: 3, points: 150 },
                { id: 'chemical-equilibrium', name: 'Chemical Equilibrium', domain: 'general-chemistry', prereqs: ['stoichiometry'], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'organic-chemistry',
              name: 'Organic Chemistry',
              color: '#6ee7b7',
              description: 'Chemistry of carbon compounds',
              nodes: [
                { id: 'hydrocarbons', name: 'Hydrocarbons', domain: 'organic-chemistry', prereqs: ['chemical-bonding'], difficulty: 3, points: 150 },
                { id: 'functional-groups', name: 'Functional Groups', domain: 'organic-chemistry', prereqs: ['hydrocarbons'], difficulty: 3, points: 150 },
                { id: 'organic-synthesis', name: 'Organic Synthesis', domain: 'organic-chemistry', prereqs: ['functional-groups'], difficulty: 4, points: 200 },
                { id: 'biochemistry', name: 'Biochemistry', domain: 'organic-chemistry', prereqs: ['organic-synthesis'], difficulty: 5, points: 250 }
              ]
            },
            {
              id: 'physical-chemistry',
              name: 'Physical Chemistry',
              color: '#6ee7b7',
              description: 'Physics applied to chemistry',
              nodes: [
                { id: 'chemical-thermodynamics', name: 'Chemical Thermodynamics', domain: 'physical-chemistry', prereqs: ['thermodynamics', 'chemical-equilibrium'], difficulty: 4, points: 200 },
                { id: 'chemical-kinetics', name: 'Chemical Kinetics', domain: 'physical-chemistry', prereqs: ['chemical-equilibrium'], difficulty: 4, points: 200 },
                { id: 'quantum-chemistry', name: 'Quantum Chemistry', domain: 'physical-chemistry', prereqs: ['quantum-mechanics', 'chemical-bonding'], difficulty: 5, points: 300 }
              ]
            }
          ]
        },
        {
          id: 'biology',
          name: 'Biology',
          color: '#34d399',
          description: 'Study of living organisms',
          subcategories: [
            {
              id: 'molecular-biology',
              name: 'Molecular Biology',
              color: '#6ee7b7',
              description: 'Life at the molecular level',
              nodes: [
                { id: 'cell-structure', name: 'Cell Structure', domain: 'molecular-biology', prereqs: [], difficulty: 2, points: 100 },
                { id: 'dna-rna', name: 'DNA & RNA', domain: 'molecular-biology', prereqs: ['cell-structure'], difficulty: 3, points: 150 },
                { id: 'protein-synthesis', name: 'Protein Synthesis', domain: 'molecular-biology', prereqs: ['dna-rna'], difficulty: 3, points: 150 },
                { id: 'gene-regulation', name: 'Gene Regulation', domain: 'molecular-biology', prereqs: ['protein-synthesis'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'organismal-biology',
              name: 'Organismal Biology',
              color: '#6ee7b7',
              description: 'Study of complete organisms',
              nodes: [
                { id: 'anatomy', name: 'Anatomy', domain: 'organismal-biology', prereqs: [], difficulty: 2, points: 100 },
                { id: 'physiology', name: 'Physiology', domain: 'organismal-biology', prereqs: ['anatomy'], difficulty: 3, points: 150 },
                { id: 'neurobiology', name: 'Neurobiology', domain: 'organismal-biology', prereqs: ['physiology'], difficulty: 4, points: 200 },
                { id: 'immunology', name: 'Immunology', domain: 'organismal-biology', prereqs: ['physiology'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'ecology-evolution',
              name: 'Ecology & Evolution',
              color: '#6ee7b7',
              description: 'Life in context',
              nodes: [
                { id: 'population-biology', name: 'Population Biology', domain: 'ecology-evolution', prereqs: ['descriptive-stats'], difficulty: 3, points: 150 },
                { id: 'community-ecology', name: 'Community Ecology', domain: 'ecology-evolution', prereqs: ['population-biology'], difficulty: 4, points: 200 },
                { id: 'evolutionary-biology', name: 'Evolutionary Biology', domain: 'ecology-evolution', prereqs: ['population-biology'], difficulty: 4, points: 200 },
                { id: 'conservation-biology', name: 'Conservation Biology', domain: 'ecology-evolution', prereqs: ['community-ecology'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'earth-sciences',
          name: 'Earth Sciences',
          color: '#34d399',
          description: 'Study of Earth and its systems',
          subcategories: [
            {
              id: 'geology',
              name: 'Geology',
              color: '#6ee7b7',
              description: 'Study of Earth\'s structure',
              nodes: [
                { id: 'mineralogy', name: 'Mineralogy', domain: 'geology', prereqs: ['atomic-structure'], difficulty: 3, points: 150 },
                { id: 'petrology', name: 'Petrology', domain: 'geology', prereqs: ['mineralogy'], difficulty: 3, points: 150 },
                { id: 'structural-geology', name: 'Structural Geology', domain: 'geology', prereqs: ['petrology'], difficulty: 4, points: 200 },
                { id: 'plate-tectonics', name: 'Plate Tectonics', domain: 'geology', prereqs: ['structural-geology'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'atmospheric-sciences',
              name: 'Atmospheric Sciences',
              color: '#6ee7b7',
              description: 'Study of Earth\'s atmosphere',
              nodes: [
                { id: 'meteorology', name: 'Meteorology', domain: 'atmospheric-sciences', prereqs: ['thermodynamics'], difficulty: 3, points: 150 },
                { id: 'climatology', name: 'Climatology', domain: 'atmospheric-sciences', prereqs: ['meteorology'], difficulty: 4, points: 200 },
                { id: 'atmospheric-chemistry', name: 'Atmospheric Chemistry', domain: 'atmospheric-sciences', prereqs: ['chemical-kinetics'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'oceanography',
              name: 'Oceanography',
              color: '#6ee7b7',
              description: 'Study of Earth\'s oceans',
              nodes: [
                { id: 'physical-oceanography', name: 'Physical Oceanography', domain: 'oceanography', prereqs: ['mechanics'], difficulty: 3, points: 150 },
                { id: 'marine-biology', name: 'Marine Biology', domain: 'oceanography', prereqs: ['community-ecology'], difficulty: 4, points: 200 },
                { id: 'ocean-chemistry', name: 'Ocean Chemistry', domain: 'oceanography', prereqs: ['chemical-equilibrium'], difficulty: 4, points: 200 }
              ]
            }
          ]
        }
      ]
    },
    {
      id: 'languages',
      name: 'Languages',
      color: '#f59e0b',
      description: 'Human and computer languages',
      subcategories: [
        {
          id: 'natural-languages',
          name: 'Natural Languages',
          color: '#fbbf24',
          description: 'Human spoken and written languages',
          subcategories: [
            {
              id: 'romance-languages',
              name: 'Romance Languages',
              color: '#fde68a',
              description: 'Languages derived from Latin',
              nodes: [
                { id: 'spanish', name: 'Spanish', domain: 'romance-languages', prereqs: [], difficulty: 3, points: 200 },
                { id: 'french', name: 'French', domain: 'romance-languages', prereqs: [], difficulty: 3, points: 200 },
                { id: 'italian', name: 'Italian', domain: 'romance-languages', prereqs: [], difficulty: 3, points: 200 },
                { id: 'portuguese', name: 'Portuguese', domain: 'romance-languages', prereqs: [], difficulty: 3, points: 200 },
                { id: 'romanian', name: 'Romanian', domain: 'romance-languages', prereqs: [], difficulty: 4, points: 250 }
              ]
            },
            {
              id: 'germanic-languages',
              name: 'Germanic Languages',
              color: '#fde68a',
              description: 'Languages of Germanic origin',
              nodes: [
                { id: 'german', name: 'German', domain: 'germanic-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'dutch', name: 'Dutch', domain: 'germanic-languages', prereqs: [], difficulty: 3, points: 200 },
                { id: 'swedish', name: 'Swedish', domain: 'germanic-languages', prereqs: [], difficulty: 3, points: 200 },
                { id: 'norwegian', name: 'Norwegian', domain: 'germanic-languages', prereqs: [], difficulty: 3, points: 200 },
                { id: 'danish', name: 'Danish', domain: 'germanic-languages', prereqs: [], difficulty: 3, points: 200 }
              ]
            },
            {
              id: 'slavic-languages',
              name: 'Slavic Languages',
              color: '#fde68a',
              description: 'Languages of Slavic peoples',
              nodes: [
                { id: 'russian', name: 'Russian', domain: 'slavic-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'polish', name: 'Polish', domain: 'slavic-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'czech', name: 'Czech', domain: 'slavic-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'ukrainian', name: 'Ukrainian', domain: 'slavic-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'serbian', name: 'Serbian', domain: 'slavic-languages', prereqs: [], difficulty: 4, points: 250 }
              ]
            },
            {
              id: 'asian-languages',
              name: 'Asian Languages',
              color: '#fde68a',
              description: 'Languages of Asia',
              nodes: [
                { id: 'mandarin', name: 'Mandarin Chinese', domain: 'asian-languages', prereqs: [], difficulty: 5, points: 350 },
                { id: 'japanese', name: 'Japanese', domain: 'asian-languages', prereqs: [], difficulty: 5, points: 350 },
                { id: 'korean', name: 'Korean', domain: 'asian-languages', prereqs: [], difficulty: 5, points: 350 },
                { id: 'hindi', name: 'Hindi', domain: 'asian-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'thai', name: 'Thai', domain: 'asian-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'vietnamese', name: 'Vietnamese', domain: 'asian-languages', prereqs: [], difficulty: 4, points: 250 }
              ]
            },
            {
              id: 'semitic-languages',
              name: 'Semitic Languages',
              color: '#fde68a',
              description: 'Languages of the Middle East',
              nodes: [
                { id: 'arabic', name: 'Arabic', domain: 'semitic-languages', prereqs: [], difficulty: 5, points: 350 },
                { id: 'hebrew', name: 'Hebrew', domain: 'semitic-languages', prereqs: [], difficulty: 4, points: 250 },
                { id: 'aramaic', name: 'Aramaic', domain: 'semitic-languages', prereqs: [], difficulty: 5, points: 350 }
              ]
            }
          ]
        },
        {
          id: 'programming-languages',
          name: 'Programming Languages',
          color: '#fbbf24',
          description: 'Computer programming languages',
          subcategories: [
            {
              id: 'low-level',
              name: 'Low-Level Languages',
              color: '#fde68a',
              description: 'Close to hardware',
              nodes: [
                { id: 'assembly', name: 'Assembly', domain: 'low-level', prereqs: [], difficulty: 5, points: 300 },
                { id: 'c-lang', name: 'C', domain: 'low-level', prereqs: [], difficulty: 4, points: 250 },
                { id: 'cpp-lang', name: 'C++', domain: 'low-level', prereqs: ['c-lang'], difficulty: 5, points: 300 },
                { id: 'rust-lang', name: 'Rust', domain: 'low-level', prereqs: ['c-lang'], difficulty: 5, points: 300 }
              ]
            },
            {
              id: 'high-level',
              name: 'High-Level Languages',
              color: '#fde68a',
              description: 'Abstract from hardware',
              nodes: [
                { id: 'python-lang', name: 'Python', domain: 'high-level', prereqs: [], difficulty: 2, points: 150 },
                { id: 'javascript-lang', name: 'JavaScript', domain: 'high-level', prereqs: [], difficulty: 3, points: 200 },
                { id: 'java-lang', name: 'Java', domain: 'high-level', prereqs: [], difficulty: 4, points: 250 },
                { id: 'csharp-lang', name: 'C#', domain: 'high-level', prereqs: [], difficulty: 4, points: 250 },
                { id: 'go-lang', name: 'Go', domain: 'high-level', prereqs: [], difficulty: 3, points: 200 },
                { id: 'swift-lang', name: 'Swift', domain: 'high-level', prereqs: [], difficulty: 4, points: 250 }
              ]
            },
            {
              id: 'functional',
              name: 'Functional Languages',
              color: '#fde68a',
              description: 'Functional programming paradigm',
              nodes: [
                { id: 'haskell', name: 'Haskell', domain: 'functional', prereqs: [], difficulty: 5, points: 300 },
                { id: 'scala', name: 'Scala', domain: 'functional', prereqs: [], difficulty: 4, points: 250 },
                { id: 'clojure', name: 'Clojure', domain: 'functional', prereqs: [], difficulty: 4, points: 250 },
                { id: 'erlang', name: 'Erlang', domain: 'functional', prereqs: [], difficulty: 4, points: 250 },
                { id: 'fsharp', name: 'F#', domain: 'functional', prereqs: [], difficulty: 4, points: 250 }
              ]
            }
          ]
        },
        {
          id: 'linguistics',
          name: 'Linguistics',
          color: '#fbbf24',
          description: 'Scientific study of language',
          nodes: [
            { id: 'phonetics', name: 'Phonetics', domain: 'linguistics', prereqs: [], difficulty: 3, points: 150 },
            { id: 'phonology', name: 'Phonology', domain: 'linguistics', prereqs: ['phonetics'], difficulty: 3, points: 150 },
            { id: 'morphology', name: 'Morphology', domain: 'linguistics', prereqs: [], difficulty: 3, points: 150 },
            { id: 'syntax', name: 'Syntax', domain: 'linguistics', prereqs: ['morphology'], difficulty: 4, points: 200 },
            { id: 'semantics', name: 'Semantics', domain: 'linguistics', prereqs: ['syntax'], difficulty: 4, points: 200 },
            { id: 'pragmatics', name: 'Pragmatics', domain: 'linguistics', prereqs: ['semantics'], difficulty: 4, points: 200 }
          ]
        }
      ]
    },
    {
      id: 'arts',
      name: 'Arts & Humanities',
      color: '#ec4899',
      description: 'Creative and cultural expression',
      subcategories: [
        {
          id: 'visual-arts',
          name: 'Visual Arts',
          color: '#f472b6',
          description: 'Art perceived by sight',
          subcategories: [
            {
              id: 'drawing-painting',
              name: 'Drawing & Painting',
              color: '#fbbf24',
              description: 'Traditional 2D arts',
              nodes: [
                { id: 'drawing-fundamentals', name: 'Drawing Fundamentals', domain: 'drawing-painting', prereqs: [], difficulty: 2, points: 100 },
                { id: 'figure-drawing', name: 'Figure Drawing', domain: 'drawing-painting', prereqs: ['drawing-fundamentals'], difficulty: 3, points: 150 },
                { id: 'watercolor', name: 'Watercolor Painting', domain: 'drawing-painting', prereqs: ['drawing-fundamentals'], difficulty: 3, points: 150 },
                { id: 'oil-painting', name: 'Oil Painting', domain: 'drawing-painting', prereqs: ['drawing-fundamentals'], difficulty: 4, points: 200 },
                { id: 'digital-painting', name: 'Digital Painting', domain: 'drawing-painting', prereqs: ['drawing-fundamentals'], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'sculpture-3d',
              name: 'Sculpture & 3D Art',
              color: '#fbbf24',
              description: 'Three-dimensional art forms',
              nodes: [
                { id: 'clay-sculpture', name: 'Clay Sculpture', domain: 'sculpture-3d', prereqs: [], difficulty: 3, points: 150 },
                { id: 'wood-carving', name: 'Wood Carving', domain: 'sculpture-3d', prereqs: [], difficulty: 3, points: 150 },
                { id: 'metal-sculpture', name: 'Metal Sculpture', domain: 'sculpture-3d', prereqs: [], difficulty: 4, points: 200 },
                { id: '3d-modeling', name: '3D Modeling', domain: 'sculpture-3d', prereqs: [], difficulty: 3, points: 150 },
                { id: '3d-printing', name: '3D Printing Art', domain: 'sculpture-3d', prereqs: ['3d-modeling'], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'photography-film',
              name: 'Photography & Film',
              color: '#fbbf24',
              description: 'Lens-based arts',
              nodes: [
                { id: 'photography-basics', name: 'Photography Basics', domain: 'photography-film', prereqs: [], difficulty: 2, points: 100 },
                { id: 'portrait-photography', name: 'Portrait Photography', domain: 'photography-film', prereqs: ['photography-basics'], difficulty: 3, points: 150 },
                { id: 'landscape-photography', name: 'Landscape Photography', domain: 'photography-film', prereqs: ['photography-basics'], difficulty: 3, points: 150 },
                { id: 'video-production', name: 'Video Production', domain: 'photography-film', prereqs: ['photography-basics'], difficulty: 4, points: 200 },
                { id: 'film-editing', name: 'Film Editing', domain: 'photography-film', prereqs: ['video-production'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'music',
          name: 'Music',
          color: '#f472b6',
          description: 'Art of sound and time',
          subcategories: [
            {
              id: 'music-theory',
              name: 'Music Theory',
              color: '#fbbf24',
              description: 'Understanding music structure',
              nodes: [
                { id: 'music-notation', name: 'Music Notation', domain: 'music-theory', prereqs: [], difficulty: 2, points: 100 },
                { id: 'scales-modes', name: 'Scales & Modes', domain: 'music-theory', prereqs: ['music-notation'], difficulty: 3, points: 150 },
                { id: 'harmony', name: 'Harmony', domain: 'music-theory', prereqs: ['scales-modes'], difficulty: 4, points: 200 },
                { id: 'counterpoint', name: 'Counterpoint', domain: 'music-theory', prereqs: ['harmony'], difficulty: 5, points: 250 },
                { id: 'orchestration', name: 'Orchestration', domain: 'music-theory', prereqs: ['harmony'], difficulty: 5, points: 250 }
              ]
            },
            {
              id: 'instruments',
              name: 'Musical Instruments',
              color: '#fbbf24',
              description: 'Playing musical instruments',
              nodes: [
                { id: 'piano', name: 'Piano', domain: 'instruments', prereqs: ['music-notation'], difficulty: 3, points: 200 },
                { id: 'guitar', name: 'Guitar', domain: 'instruments', prereqs: [], difficulty: 3, points: 200 },
                { id: 'violin', name: 'Violin', domain: 'instruments', prereqs: ['music-notation'], difficulty: 4, points: 250 },
                { id: 'drums', name: 'Drums', domain: 'instruments', prereqs: [], difficulty: 3, points: 150 },
                { id: 'voice', name: 'Voice/Singing', domain: 'instruments', prereqs: [], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'music-production',
              name: 'Music Production',
              color: '#fbbf24',
              description: 'Creating and recording music',
              nodes: [
                { id: 'audio-engineering', name: 'Audio Engineering', domain: 'music-production', prereqs: [], difficulty: 3, points: 150 },
                { id: 'mixing', name: 'Mixing', domain: 'music-production', prereqs: ['audio-engineering'], difficulty: 4, points: 200 },
                { id: 'mastering', name: 'Mastering', domain: 'music-production', prereqs: ['mixing'], difficulty: 5, points: 250 },
                { id: 'electronic-music', name: 'Electronic Music Production', domain: 'music-production', prereqs: ['audio-engineering'], difficulty: 3, points: 150 },
                { id: 'sound-design', name: 'Sound Design', domain: 'music-production', prereqs: ['audio-engineering'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'literature',
          name: 'Literature',
          color: '#f472b6',
          description: 'Written artistic expression',
          subcategories: [
            {
              id: 'creative-writing',
              name: 'Creative Writing',
              color: '#fbbf24',
              description: 'Original written works',
              nodes: [
                { id: 'fiction-writing', name: 'Fiction Writing', domain: 'creative-writing', prereqs: [], difficulty: 3, points: 150 },
                { id: 'poetry', name: 'Poetry', domain: 'creative-writing', prereqs: [], difficulty: 3, points: 150 },
                { id: 'screenwriting', name: 'Screenwriting', domain: 'creative-writing', prereqs: ['fiction-writing'], difficulty: 4, points: 200 },
                { id: 'playwriting', name: 'Playwriting', domain: 'creative-writing', prereqs: ['fiction-writing'], difficulty: 4, points: 200 },
                { id: 'creative-nonfiction', name: 'Creative Nonfiction', domain: 'creative-writing', prereqs: [], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'literary-studies',
              name: 'Literary Studies',
              color: '#fbbf24',
              description: 'Analysis of literature',
              nodes: [
                { id: 'literary-theory', name: 'Literary Theory', domain: 'literary-studies', prereqs: [], difficulty: 4, points: 200 },
                { id: 'comparative-literature', name: 'Comparative Literature', domain: 'literary-studies', prereqs: ['literary-theory'], difficulty: 4, points: 200 },
                { id: 'world-literature', name: 'World Literature', domain: 'literary-studies', prereqs: [], difficulty: 3, points: 150 },
                { id: 'literary-criticism', name: 'Literary Criticism', domain: 'literary-studies', prereqs: ['literary-theory'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'performing-arts',
          name: 'Performing Arts',
          color: '#f472b6',
          description: 'Live artistic performances',
          nodes: [
            { id: 'acting', name: 'Acting', domain: 'performing-arts', prereqs: [], difficulty: 3, points: 150 },
            { id: 'dance-ballet', name: 'Ballet', domain: 'performing-arts', prereqs: [], difficulty: 4, points: 250 },
            { id: 'dance-modern', name: 'Modern Dance', domain: 'performing-arts', prereqs: [], difficulty: 3, points: 200 },
            { id: 'dance-jazz', name: 'Jazz Dance', domain: 'performing-arts', prereqs: [], difficulty: 3, points: 200 },
            { id: 'theater-production', name: 'Theater Production', domain: 'performing-arts', prereqs: [], difficulty: 4, points: 200 },
            { id: 'improv', name: 'Improvisation', domain: 'performing-arts', prereqs: ['acting'], difficulty: 3, points: 150 }
          ]
        }
      ]
    },
    {
      id: 'technology',
      name: 'Technology & Engineering',
      color: '#8b5cf6',
      description: 'Applied sciences and engineering',
      subcategories: [
        {
          id: 'computer-science',
          name: 'Computer Science',
          color: '#a78bfa',
          description: 'Study of computation and information',
          subcategories: [
            {
              id: 'algorithms',
              name: 'Algorithms & Data Structures',
              color: '#c4b5fd',
              description: 'Computational problem solving',
              nodes: [
                { id: 'basic-algorithms', name: 'Basic Algorithms', domain: 'algorithms', prereqs: ['python-lang'], difficulty: 3, points: 150 },
                { id: 'data-structures', name: 'Data Structures', domain: 'algorithms', prereqs: ['basic-algorithms'], difficulty: 3, points: 150 },
                { id: 'algorithm-analysis', name: 'Algorithm Analysis', domain: 'algorithms', prereqs: ['data-structures'], difficulty: 4, points: 200 },
                { id: 'advanced-algorithms', name: 'Advanced Algorithms', domain: 'algorithms', prereqs: ['algorithm-analysis'], difficulty: 5, points: 250 }
              ]
            },
            {
              id: 'software-engineering',
              name: 'Software Engineering',
              color: '#c4b5fd',
              description: 'Building software systems',
              nodes: [
                { id: 'software-design', name: 'Software Design', domain: 'software-engineering', prereqs: ['data-structures'], difficulty: 3, points: 150 },
                { id: 'design-patterns', name: 'Design Patterns', domain: 'software-engineering', prereqs: ['software-design'], difficulty: 4, points: 200 },
                { id: 'software-architecture', name: 'Software Architecture', domain: 'software-engineering', prereqs: ['design-patterns'], difficulty: 5, points: 250 },
                { id: 'devops', name: 'DevOps', domain: 'software-engineering', prereqs: ['software-design'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'ai-ml',
              name: 'AI & Machine Learning',
              color: '#c4b5fd',
              description: 'Artificial intelligence',
              nodes: [
                { id: 'ml-basics', name: 'Machine Learning Basics', domain: 'ai-ml', prereqs: ['linear-algebra', 'probability'], difficulty: 4, points: 200 },
                { id: 'deep-learning', name: 'Deep Learning', domain: 'ai-ml', prereqs: ['ml-basics'], difficulty: 5, points: 300 },
                { id: 'computer-vision', name: 'Computer Vision', domain: 'ai-ml', prereqs: ['deep-learning'], difficulty: 5, points: 300 },
                { id: 'nlp', name: 'Natural Language Processing', domain: 'ai-ml', prereqs: ['deep-learning'], difficulty: 5, points: 300 },
                { id: 'reinforcement-learning', name: 'Reinforcement Learning', domain: 'ai-ml', prereqs: ['ml-basics'], difficulty: 6, points: 350 }
              ]
            },
            {
              id: 'systems',
              name: 'Computer Systems',
              color: '#c4b5fd',
              description: 'Low-level computing',
              nodes: [
                { id: 'computer-architecture', name: 'Computer Architecture', domain: 'systems', prereqs: [], difficulty: 3, points: 150 },
                { id: 'operating-systems', name: 'Operating Systems', domain: 'systems', prereqs: ['computer-architecture'], difficulty: 4, points: 200 },
                { id: 'distributed-systems', name: 'Distributed Systems', domain: 'systems', prereqs: ['operating-systems'], difficulty: 5, points: 300 },
                { id: 'databases', name: 'Database Systems', domain: 'systems', prereqs: ['data-structures'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'engineering',
          name: 'Engineering',
          color: '#a78bfa',
          description: 'Applied physical sciences',
          subcategories: [
            {
              id: 'electrical-engineering',
              name: 'Electrical Engineering',
              color: '#c4b5fd',
              description: 'Electricity and electronics',
              nodes: [
                { id: 'circuit-analysis', name: 'Circuit Analysis', domain: 'electrical-engineering', prereqs: ['electromagnetism'], difficulty: 3, points: 150 },
                { id: 'digital-logic', name: 'Digital Logic', domain: 'electrical-engineering', prereqs: ['circuit-analysis'], difficulty: 3, points: 150 },
                { id: 'microprocessors', name: 'Microprocessors', domain: 'electrical-engineering', prereqs: ['digital-logic'], difficulty: 4, points: 200 },
                { id: 'power-systems', name: 'Power Systems', domain: 'electrical-engineering', prereqs: ['circuit-analysis'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'mechanical-engineering',
              name: 'Mechanical Engineering',
              color: '#c4b5fd',
              description: 'Mechanical systems',
              nodes: [
                { id: 'statics', name: 'Statics', domain: 'mechanical-engineering', prereqs: ['mechanics'], difficulty: 3, points: 150 },
                { id: 'dynamics', name: 'Dynamics', domain: 'mechanical-engineering', prereqs: ['statics'], difficulty: 4, points: 200 },
                { id: 'fluid-mechanics', name: 'Fluid Mechanics', domain: 'mechanical-engineering', prereqs: ['dynamics'], difficulty: 4, points: 200 },
                { id: 'heat-transfer', name: 'Heat Transfer', domain: 'mechanical-engineering', prereqs: ['thermodynamics'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'civil-engineering',
              name: 'Civil Engineering',
              color: '#c4b5fd',
              description: 'Infrastructure and construction',
              nodes: [
                { id: 'structural-analysis', name: 'Structural Analysis', domain: 'civil-engineering', prereqs: ['statics'], difficulty: 4, points: 200 },
                { id: 'geotechnical', name: 'Geotechnical Engineering', domain: 'civil-engineering', prereqs: ['mechanics'], difficulty: 4, points: 200 },
                { id: 'transportation', name: 'Transportation Engineering', domain: 'civil-engineering', prereqs: [], difficulty: 3, points: 150 },
                { id: 'environmental-eng', name: 'Environmental Engineering', domain: 'civil-engineering', prereqs: ['fluid-mechanics'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'biomedical-engineering',
              name: 'Biomedical Engineering',
              color: '#c4b5fd',
              description: 'Engineering for medicine',
              nodes: [
                { id: 'biomechanics', name: 'Biomechanics', domain: 'biomedical-engineering', prereqs: ['dynamics', 'physiology'], difficulty: 4, points: 200 },
                { id: 'biomaterials', name: 'Biomaterials', domain: 'biomedical-engineering', prereqs: ['chemistry'], difficulty: 4, points: 200 },
                { id: 'medical-imaging', name: 'Medical Imaging', domain: 'biomedical-engineering', prereqs: ['circuit-analysis'], difficulty: 5, points: 250 },
                { id: 'tissue-engineering', name: 'Tissue Engineering', domain: 'biomedical-engineering', prereqs: ['cell-structure'], difficulty: 5, points: 250 }
              ]
            }
          ]
        }
      ]
    },
    {
      id: 'history',
      name: 'History',
      color: '#a0522d',
      description: 'Study of past events and civilizations',
      subcategories: [
        {
          id: 'ancient-history',
          name: 'Ancient History',
          color: '#cd853f',
          description: 'Early civilizations and antiquity',
          subcategories: [
            {
              id: 'ancient-civilizations',
              name: 'Ancient Civilizations',
              color: '#daa520',
              description: 'Early human civilizations',
              nodes: [
                { id: 'mesopotamia', name: 'Mesopotamian Civilizations', domain: 'ancient-civilizations', prereqs: [], difficulty: 3, points: 150 },
                { id: 'ancient-egypt', name: 'Ancient Egypt', domain: 'ancient-civilizations', prereqs: [], difficulty: 3, points: 150 },
                { id: 'ancient-greece', name: 'Ancient Greece', domain: 'ancient-civilizations', prereqs: [], difficulty: 3, points: 150 },
                { id: 'ancient-rome', name: 'Ancient Rome', domain: 'ancient-civilizations', prereqs: [], difficulty: 3, points: 150 },
                { id: 'ancient-china', name: 'Ancient China', domain: 'ancient-civilizations', prereqs: [], difficulty: 3, points: 150 },
                { id: 'ancient-india', name: 'Ancient India', domain: 'ancient-civilizations', prereqs: [], difficulty: 3, points: 150 },
                { id: 'maya-aztec-inca', name: 'Maya, Aztec & Inca', domain: 'ancient-civilizations', prereqs: [], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'classical-antiquity',
              name: 'Classical Antiquity',
              color: '#daa520',
              description: 'Greek and Roman periods',
              nodes: [
                { id: 'greek-classical', name: 'Classical Greece', domain: 'classical-antiquity', prereqs: ['ancient-greece'], difficulty: 4, points: 200 },
                { id: 'hellenistic-period', name: 'Hellenistic Period', domain: 'classical-antiquity', prereqs: ['greek-classical'], difficulty: 4, points: 200 },
                { id: 'roman-republic', name: 'Roman Republic', domain: 'classical-antiquity', prereqs: ['ancient-rome'], difficulty: 4, points: 200 },
                { id: 'roman-empire', name: 'Roman Empire', domain: 'classical-antiquity', prereqs: ['roman-republic'], difficulty: 4, points: 200 },
                { id: 'byzantine-empire', name: 'Byzantine Empire', domain: 'classical-antiquity', prereqs: ['roman-empire'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'medieval-history',
          name: 'Medieval History',
          color: '#cd853f',
          description: 'Middle Ages period',
          nodes: [
            { id: 'early-middle-ages', name: 'Early Middle Ages', domain: 'medieval-history', prereqs: ['roman-empire'], difficulty: 3, points: 150 },
            { id: 'viking-age', name: 'Viking Age', domain: 'medieval-history', prereqs: [], difficulty: 3, points: 150 },
            { id: 'crusades', name: 'The Crusades', domain: 'medieval-history', prereqs: ['early-middle-ages'], difficulty: 4, points: 200 },
            { id: 'medieval-europe', name: 'Medieval Europe', domain: 'medieval-history', prereqs: ['early-middle-ages'], difficulty: 3, points: 150 },
            { id: 'islamic-golden-age', name: 'Islamic Golden Age', domain: 'medieval-history', prereqs: [], difficulty: 3, points: 150 },
            { id: 'mongol-empire', name: 'Mongol Empire', domain: 'medieval-history', prereqs: [], difficulty: 3, points: 150 }
          ]
        },
        {
          id: 'modern-history',
          name: 'Modern History',
          color: '#cd853f',
          description: 'Early modern to contemporary',
          subcategories: [
            {
              id: 'early-modern',
              name: 'Early Modern Period',
              color: '#daa520',
              description: 'Renaissance to Enlightenment',
              nodes: [
                { id: 'renaissance', name: 'Renaissance', domain: 'early-modern', prereqs: ['medieval-europe'], difficulty: 3, points: 150 },
                { id: 'age-exploration', name: 'Age of Exploration', domain: 'early-modern', prereqs: ['renaissance'], difficulty: 3, points: 150 },
                { id: 'reformation', name: 'Protestant Reformation', domain: 'early-modern', prereqs: ['renaissance'], difficulty: 3, points: 150 },
                { id: 'scientific-revolution', name: 'Scientific Revolution', domain: 'early-modern', prereqs: ['renaissance'], difficulty: 4, points: 200 },
                { id: 'enlightenment', name: 'The Enlightenment', domain: 'early-modern', prereqs: ['scientific-revolution'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'revolutionary-period',
              name: 'Age of Revolutions',
              color: '#daa520',
              description: 'Political and industrial revolutions',
              nodes: [
                { id: 'american-revolution', name: 'American Revolution', domain: 'revolutionary-period', prereqs: ['enlightenment'], difficulty: 3, points: 150 },
                { id: 'french-revolution', name: 'French Revolution', domain: 'revolutionary-period', prereqs: ['enlightenment'], difficulty: 4, points: 200 },
                { id: 'napoleonic-wars', name: 'Napoleonic Wars', domain: 'revolutionary-period', prereqs: ['french-revolution'], difficulty: 4, points: 200 },
                { id: 'industrial-revolution', name: 'Industrial Revolution', domain: 'revolutionary-period', prereqs: ['enlightenment'], difficulty: 4, points: 200 },
                { id: 'latin-american-independence', name: 'Latin American Independence', domain: 'revolutionary-period', prereqs: ['enlightenment'], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'contemporary-history',
              name: 'Contemporary History',
              color: '#daa520',
              description: '19th-21st centuries',
              nodes: [
                { id: 'imperialism-colonialism', name: 'Imperialism & Colonialism', domain: 'contemporary-history', prereqs: ['industrial-revolution'], difficulty: 4, points: 200 },
                { id: 'world-war-1', name: 'World War I', domain: 'contemporary-history', prereqs: ['imperialism-colonialism'], difficulty: 4, points: 200 },
                { id: 'interwar-period', name: 'Interwar Period', domain: 'contemporary-history', prereqs: ['world-war-1'], difficulty: 3, points: 150 },
                { id: 'world-war-2', name: 'World War II', domain: 'contemporary-history', prereqs: ['interwar-period'], difficulty: 4, points: 200 },
                { id: 'cold-war', name: 'Cold War', domain: 'contemporary-history', prereqs: ['world-war-2'], difficulty: 4, points: 200 },
                { id: 'decolonization', name: 'Decolonization', domain: 'contemporary-history', prereqs: ['world-war-2'], difficulty: 3, points: 150 },
                { id: 'post-cold-war', name: 'Post-Cold War Era', domain: 'contemporary-history', prereqs: ['cold-war'], difficulty: 3, points: 150 }
              ]
            }
          ]
        },
        {
          id: 'regional-history',
          name: 'Regional History',
          color: '#cd853f',
          description: 'History by geographic region',
          subcategories: [
            {
              id: 'american-history',
              name: 'American History',
              color: '#daa520',
              description: 'History of the Americas',
              nodes: [
                { id: 'pre-columbian', name: 'Pre-Columbian Americas', domain: 'american-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'colonial-america', name: 'Colonial America', domain: 'american-history', prereqs: ['age-exploration'], difficulty: 3, points: 150 },
                { id: 'us-history', name: 'United States History', domain: 'american-history', prereqs: ['american-revolution'], difficulty: 3, points: 150 },
                { id: 'canadian-history', name: 'Canadian History', domain: 'american-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'latin-american-history', name: 'Latin American History', domain: 'american-history', prereqs: [], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'european-history',
              name: 'European History',
              color: '#daa520',
              description: 'History of Europe',
              nodes: [
                { id: 'british-history', name: 'British History', domain: 'european-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'french-history', name: 'French History', domain: 'european-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'german-history', name: 'German History', domain: 'european-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'russian-history', name: 'Russian History', domain: 'european-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'spanish-history', name: 'Spanish History', domain: 'european-history', prereqs: [], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'asian-history',
              name: 'Asian History',
              color: '#daa520',
              description: 'History of Asia',
              nodes: [
                { id: 'chinese-history', name: 'Chinese History', domain: 'asian-history', prereqs: ['ancient-china'], difficulty: 4, points: 200 },
                { id: 'japanese-history', name: 'Japanese History', domain: 'asian-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'indian-history', name: 'Indian History', domain: 'asian-history', prereqs: ['ancient-india'], difficulty: 3, points: 150 },
                { id: 'southeast-asian-history', name: 'Southeast Asian History', domain: 'asian-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'middle-eastern-history', name: 'Middle Eastern History', domain: 'asian-history', prereqs: ['mesopotamia'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'african-history',
              name: 'African History',
              color: '#daa520',
              description: 'History of Africa',
              nodes: [
                { id: 'ancient-africa', name: 'Ancient African Kingdoms', domain: 'african-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'north-african-history', name: 'North African History', domain: 'african-history', prereqs: ['ancient-egypt'], difficulty: 3, points: 150 },
                { id: 'sub-saharan-history', name: 'Sub-Saharan History', domain: 'african-history', prereqs: [], difficulty: 3, points: 150 },
                { id: 'african-colonialism', name: 'African Colonialism', domain: 'african-history', prereqs: ['imperialism-colonialism'], difficulty: 4, points: 200 },
                { id: 'modern-africa', name: 'Modern African History', domain: 'african-history', prereqs: ['decolonization'], difficulty: 3, points: 150 }
              ]
            }
          ]
        },
        {
          id: 'thematic-history',
          name: 'Thematic History',
          color: '#cd853f',
          description: 'History by theme',
          nodes: [
            { id: 'military-history', name: 'Military History', domain: 'thematic-history', prereqs: [], difficulty: 3, points: 150 },
            { id: 'economic-history', name: 'Economic History', domain: 'thematic-history', prereqs: ['supply-demand'], difficulty: 4, points: 200 },
            { id: 'social-history', name: 'Social History', domain: 'thematic-history', prereqs: [], difficulty: 3, points: 150 },
            { id: 'cultural-history', name: 'Cultural History', domain: 'thematic-history', prereqs: [], difficulty: 3, points: 150 },
            { id: 'history-science-tech', name: 'History of Science & Technology', domain: 'thematic-history', prereqs: ['scientific-revolution'], difficulty: 4, points: 200 },
            { id: 'womens-history', name: "Women's History", domain: 'thematic-history', prereqs: [], difficulty: 3, points: 150 },
            { id: 'history-ideas', name: 'History of Ideas', domain: 'thematic-history', prereqs: ['enlightenment'], difficulty: 4, points: 200 }
          ]
        }
      ]
    },
    {
      id: 'social-sciences',
      name: 'Social Sciences',
      color: '#06b6d4',
      description: 'Study of human society',
      subcategories: [
        {
          id: 'psychology',
          name: 'Psychology',
          color: '#22d3ee',
          description: 'Study of mind and behavior',
          subcategories: [
            {
              id: 'cognitive-psychology',
              name: 'Cognitive Psychology',
              color: '#67e8f9',
              description: 'Mental processes',
              nodes: [
                { id: 'perception', name: 'Perception', domain: 'cognitive-psychology', prereqs: [], difficulty: 3, points: 150 },
                { id: 'memory', name: 'Memory', domain: 'cognitive-psychology', prereqs: [], difficulty: 3, points: 150 },
                { id: 'attention', name: 'Attention', domain: 'cognitive-psychology', prereqs: [], difficulty: 3, points: 150 },
                { id: 'language-cognition', name: 'Language & Cognition', domain: 'cognitive-psychology', prereqs: ['memory'], difficulty: 4, points: 200 },
                { id: 'decision-making', name: 'Decision Making', domain: 'cognitive-psychology', prereqs: ['attention'], difficulty: 4, points: 200 }
              ]
            },
            {
              id: 'developmental-psychology',
              name: 'Developmental Psychology',
              color: '#67e8f9',
              description: 'Human development',
              nodes: [
                { id: 'child-development', name: 'Child Development', domain: 'developmental-psychology', prereqs: [], difficulty: 3, points: 150 },
                { id: 'adolescent-psychology', name: 'Adolescent Psychology', domain: 'developmental-psychology', prereqs: ['child-development'], difficulty: 3, points: 150 },
                { id: 'adult-development', name: 'Adult Development', domain: 'developmental-psychology', prereqs: [], difficulty: 3, points: 150 },
                { id: 'aging-psychology', name: 'Psychology of Aging', domain: 'developmental-psychology', prereqs: ['adult-development'], difficulty: 3, points: 150 }
              ]
            },
            {
              id: 'clinical-psychology',
              name: 'Clinical Psychology',
              color: '#67e8f9',
              description: 'Mental health and therapy',
              nodes: [
                { id: 'abnormal-psychology', name: 'Abnormal Psychology', domain: 'clinical-psychology', prereqs: [], difficulty: 3, points: 150 },
                { id: 'psychotherapy', name: 'Psychotherapy', domain: 'clinical-psychology', prereqs: ['abnormal-psychology'], difficulty: 4, points: 200 },
                { id: 'psychological-assessment', name: 'Psychological Assessment', domain: 'clinical-psychology', prereqs: ['abnormal-psychology'], difficulty: 4, points: 200 },
                { id: 'neuropsychology', name: 'Neuropsychology', domain: 'clinical-psychology', prereqs: ['neurobiology'], difficulty: 5, points: 250 }
              ]
            }
          ]
        },
        {
          id: 'sociology',
          name: 'Sociology',
          color: '#22d3ee',
          description: 'Study of society',
          nodes: [
            { id: 'social-theory', name: 'Social Theory', domain: 'sociology', prereqs: [], difficulty: 3, points: 150 },
            { id: 'social-research', name: 'Social Research Methods', domain: 'sociology', prereqs: ['descriptive-stats'], difficulty: 3, points: 150 },
            { id: 'social-stratification', name: 'Social Stratification', domain: 'sociology', prereqs: ['social-theory'], difficulty: 4, points: 200 },
            { id: 'urban-sociology', name: 'Urban Sociology', domain: 'sociology', prereqs: ['social-theory'], difficulty: 3, points: 150 },
            { id: 'cultural-sociology', name: 'Cultural Sociology', domain: 'sociology', prereqs: ['social-theory'], difficulty: 3, points: 150 }
          ]
        },
        {
          id: 'economics',
          name: 'Economics',
          color: '#22d3ee',
          description: 'Study of resource allocation',
          subcategories: [
            {
              id: 'microeconomics',
              name: 'Microeconomics',
              color: '#67e8f9',
              description: 'Individual economic behavior',
              nodes: [
                { id: 'supply-demand', name: 'Supply & Demand', domain: 'microeconomics', prereqs: [], difficulty: 2, points: 100 },
                { id: 'consumer-theory', name: 'Consumer Theory', domain: 'microeconomics', prereqs: ['supply-demand'], difficulty: 3, points: 150 },
                { id: 'producer-theory', name: 'Producer Theory', domain: 'microeconomics', prereqs: ['supply-demand'], difficulty: 3, points: 150 },
                { id: 'market-structures', name: 'Market Structures', domain: 'microeconomics', prereqs: ['producer-theory'], difficulty: 4, points: 200 },
                { id: 'game-theory', name: 'Game Theory', domain: 'microeconomics', prereqs: ['market-structures'], difficulty: 5, points: 250 }
              ]
            },
            {
              id: 'macroeconomics',
              name: 'Macroeconomics',
              color: '#67e8f9',
              description: 'Economy-wide phenomena',
              nodes: [
                { id: 'national-accounts', name: 'National Accounts', domain: 'macroeconomics', prereqs: [], difficulty: 2, points: 100 },
                { id: 'monetary-policy', name: 'Monetary Policy', domain: 'macroeconomics', prereqs: ['national-accounts'], difficulty: 3, points: 150 },
                { id: 'fiscal-policy', name: 'Fiscal Policy', domain: 'macroeconomics', prereqs: ['national-accounts'], difficulty: 3, points: 150 },
                { id: 'international-trade', name: 'International Trade', domain: 'macroeconomics', prereqs: ['supply-demand'], difficulty: 4, points: 200 },
                { id: 'economic-growth', name: 'Economic Growth', domain: 'macroeconomics', prereqs: ['national-accounts'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'political-science',
          name: 'Political Science',
          color: '#22d3ee',
          description: 'Study of politics and government',
          nodes: [
            { id: 'political-theory', name: 'Political Theory', domain: 'political-science', prereqs: [], difficulty: 3, points: 150 },
            { id: 'comparative-politics', name: 'Comparative Politics', domain: 'political-science', prereqs: ['political-theory'], difficulty: 3, points: 150 },
            { id: 'international-relations', name: 'International Relations', domain: 'political-science', prereqs: ['political-theory'], difficulty: 4, points: 200 },
            { id: 'public-policy', name: 'Public Policy', domain: 'political-science', prereqs: ['political-theory'], difficulty: 3, points: 150 },
            { id: 'political-economy', name: 'Political Economy', domain: 'political-science', prereqs: ['political-theory', 'supply-demand'], difficulty: 4, points: 200 }
          ]
        },
        {
          id: 'anthropology',
          name: 'Anthropology',
          color: '#22d3ee',
          description: 'Study of humanity',
          nodes: [
            { id: 'cultural-anthropology', name: 'Cultural Anthropology', domain: 'anthropology', prereqs: [], difficulty: 3, points: 150 },
            { id: 'physical-anthropology', name: 'Physical Anthropology', domain: 'anthropology', prereqs: ['evolutionary-biology'], difficulty: 4, points: 200 },
            { id: 'archaeology', name: 'Archaeology', domain: 'anthropology', prereqs: [], difficulty: 3, points: 150 },
            { id: 'linguistic-anthropology', name: 'Linguistic Anthropology', domain: 'anthropology', prereqs: ['linguistics'], difficulty: 4, points: 200 },
            { id: 'ethnography', name: 'Ethnography', domain: 'anthropology', prereqs: ['cultural-anthropology'], difficulty: 4, points: 200 }
          ]
        }
      ]
    },
    {
      id: 'practical-skills',
      name: 'Practical Skills',
      color: '#14b8a6',
      description: 'Real-world applied skills',
      subcategories: [
        {
          id: 'culinary',
          name: 'Culinary Arts',
          color: '#2dd4bf',
          description: 'Cooking and food preparation',
          nodes: [
            { id: 'knife-skills', name: 'Knife Skills', domain: 'culinary', prereqs: [], difficulty: 2, points: 100 },
            { id: 'basic-cooking', name: 'Basic Cooking Techniques', domain: 'culinary', prereqs: ['knife-skills'], difficulty: 2, points: 100 },
            { id: 'baking', name: 'Baking', domain: 'culinary', prereqs: ['basic-cooking'], difficulty: 3, points: 150 },
            { id: 'international-cuisine', name: 'International Cuisine', domain: 'culinary', prereqs: ['basic-cooking'], difficulty: 3, points: 150 },
            { id: 'pastry', name: 'Pastry Arts', domain: 'culinary', prereqs: ['baking'], difficulty: 4, points: 200 },
            { id: 'molecular-gastronomy', name: 'Molecular Gastronomy', domain: 'culinary', prereqs: ['basic-cooking', 'chemistry'], difficulty: 5, points: 250 }
          ]
        },
        {
          id: 'crafts',
          name: 'Crafts & Making',
          color: '#2dd4bf',
          description: 'Handmade crafts and DIY',
          nodes: [
            { id: 'woodworking', name: 'Woodworking', domain: 'crafts', prereqs: [], difficulty: 3, points: 150 },
            { id: 'metalworking', name: 'Metalworking', domain: 'crafts', prereqs: [], difficulty: 4, points: 200 },
            { id: 'sewing', name: 'Sewing', domain: 'crafts', prereqs: [], difficulty: 2, points: 100 },
            { id: 'knitting', name: 'Knitting', domain: 'crafts', prereqs: [], difficulty: 2, points: 100 },
            { id: 'pottery', name: 'Pottery', domain: 'crafts', prereqs: [], difficulty: 3, points: 150 },
            { id: 'jewelry-making', name: 'Jewelry Making', domain: 'crafts', prereqs: [], difficulty: 3, points: 150 }
          ]
        },
        {
          id: 'home-skills',
          name: 'Home & Life Skills',
          color: '#2dd4bf',
          description: 'Essential life skills',
          nodes: [
            { id: 'home-repair', name: 'Basic Home Repair', domain: 'home-skills', prereqs: [], difficulty: 2, points: 100 },
            { id: 'plumbing-basics', name: 'Basic Plumbing', domain: 'home-skills', prereqs: ['home-repair'], difficulty: 3, points: 150 },
            { id: 'electrical-basics', name: 'Basic Electrical', domain: 'home-skills', prereqs: ['home-repair'], difficulty: 3, points: 150 },
            { id: 'gardening', name: 'Gardening', domain: 'home-skills', prereqs: [], difficulty: 2, points: 100 },
            { id: 'auto-maintenance', name: 'Auto Maintenance', domain: 'home-skills', prereqs: [], difficulty: 3, points: 150 },
            { id: 'personal-finance', name: 'Personal Finance', domain: 'home-skills', prereqs: [], difficulty: 2, points: 100 }
          ]
        },
        {
          id: 'outdoor-skills',
          name: 'Outdoor & Survival',
          color: '#2dd4bf',
          description: 'Outdoor and survival skills',
          nodes: [
            { id: 'camping', name: 'Camping', domain: 'outdoor-skills', prereqs: [], difficulty: 2, points: 100 },
            { id: 'hiking', name: 'Hiking & Navigation', domain: 'outdoor-skills', prereqs: [], difficulty: 2, points: 100 },
            { id: 'wilderness-survival', name: 'Wilderness Survival', domain: 'outdoor-skills', prereqs: ['camping'], difficulty: 4, points: 200 },
            { id: 'fishing', name: 'Fishing', domain: 'outdoor-skills', prereqs: [], difficulty: 2, points: 100 },
            { id: 'hunting', name: 'Hunting', domain: 'outdoor-skills', prereqs: [], difficulty: 3, points: 150 },
            { id: 'rock-climbing', name: 'Rock Climbing', domain: 'outdoor-skills', prereqs: [], difficulty: 3, points: 150 }
          ]
        }
      ]
    },
    {
      id: 'health-fitness',
      name: 'Health & Fitness',
      color: '#ef4444',
      description: 'Physical and mental wellbeing',
      subcategories: [
        {
          id: 'physical-fitness',
          name: 'Physical Fitness',
          color: '#f87171',
          description: 'Exercise and physical health',
          nodes: [
            { id: 'strength-training', name: 'Strength Training', domain: 'physical-fitness', prereqs: [], difficulty: 2, points: 100 },
            { id: 'cardiovascular', name: 'Cardiovascular Training', domain: 'physical-fitness', prereqs: [], difficulty: 2, points: 100 },
            { id: 'flexibility', name: 'Flexibility & Mobility', domain: 'physical-fitness', prereqs: [], difficulty: 2, points: 100 },
            { id: 'calisthenics', name: 'Calisthenics', domain: 'physical-fitness', prereqs: ['strength-training'], difficulty: 3, points: 150 },
            { id: 'powerlifting', name: 'Powerlifting', domain: 'physical-fitness', prereqs: ['strength-training'], difficulty: 4, points: 200 },
            { id: 'marathon-training', name: 'Marathon Training', domain: 'physical-fitness', prereqs: ['cardiovascular'], difficulty: 4, points: 200 }
          ]
        },
        {
          id: 'sports',
          name: 'Sports',
          color: '#f87171',
          description: 'Athletic activities',
          nodes: [
            { id: 'swimming', name: 'Swimming', domain: 'sports', prereqs: [], difficulty: 2, points: 100 },
            { id: 'tennis', name: 'Tennis', domain: 'sports', prereqs: [], difficulty: 3, points: 150 },
            { id: 'basketball', name: 'Basketball', domain: 'sports', prereqs: [], difficulty: 3, points: 150 },
            { id: 'soccer', name: 'Soccer', domain: 'sports', prereqs: [], difficulty: 3, points: 150 },
            { id: 'martial-arts', name: 'Martial Arts', domain: 'sports', prereqs: [], difficulty: 3, points: 150 },
            { id: 'cycling', name: 'Cycling', domain: 'sports', prereqs: [], difficulty: 2, points: 100 }
          ]
        },
        {
          id: 'nutrition',
          name: 'Nutrition',
          color: '#f87171',
          description: 'Diet and nutritional science',
          nodes: [
            { id: 'basic-nutrition', name: 'Basic Nutrition', domain: 'nutrition', prereqs: [], difficulty: 2, points: 100 },
            { id: 'macronutrients', name: 'Macronutrients', domain: 'nutrition', prereqs: ['basic-nutrition'], difficulty: 3, points: 150 },
            { id: 'micronutrients', name: 'Micronutrients', domain: 'nutrition', prereqs: ['basic-nutrition'], difficulty: 3, points: 150 },
            { id: 'sports-nutrition', name: 'Sports Nutrition', domain: 'nutrition', prereqs: ['macronutrients'], difficulty: 4, points: 200 },
            { id: 'clinical-nutrition', name: 'Clinical Nutrition', domain: 'nutrition', prereqs: ['micronutrients', 'biochemistry'], difficulty: 5, points: 250 }
          ]
        },
        {
          id: 'mental-health',
          name: 'Mental Health',
          color: '#f87171',
          description: 'Mental and emotional wellbeing',
          nodes: [
            { id: 'stress-management', name: 'Stress Management', domain: 'mental-health', prereqs: [], difficulty: 2, points: 100 },
            { id: 'mindfulness', name: 'Mindfulness', domain: 'mental-health', prereqs: [], difficulty: 2, points: 100 },
            { id: 'meditation', name: 'Meditation', domain: 'mental-health', prereqs: ['mindfulness'], difficulty: 3, points: 150 },
            { id: 'cognitive-behavioral', name: 'Cognitive Behavioral Techniques', domain: 'mental-health', prereqs: [], difficulty: 3, points: 150 },
            { id: 'emotional-intelligence', name: 'Emotional Intelligence', domain: 'mental-health', prereqs: [], difficulty: 3, points: 150 }
          ]
        }
      ]
    },
    {
      id: 'philosophy-religion',
      name: 'Philosophy & Religion',
      color: '#64748b',
      description: 'Fundamental questions and beliefs',
      subcategories: [
        {
          id: 'philosophy',
          name: 'Philosophy',
          color: '#94a3b8',
          description: 'Love of wisdom',
          subcategories: [
            {
              id: 'metaphysics',
              name: 'Metaphysics',
              color: '#cbd5e1',
              description: 'Nature of reality',
              nodes: [
                { id: 'ontology', name: 'Ontology', domain: 'metaphysics', prereqs: [], difficulty: 4, points: 200 },
                { id: 'philosophy-mind', name: 'Philosophy of Mind', domain: 'metaphysics', prereqs: ['ontology'], difficulty: 4, points: 200 },
                { id: 'free-will', name: 'Free Will & Determinism', domain: 'metaphysics', prereqs: ['philosophy-mind'], difficulty: 4, points: 200 },
                { id: 'philosophy-time', name: 'Philosophy of Time', domain: 'metaphysics', prereqs: ['ontology'], difficulty: 5, points: 250 }
              ]
            },
            {
              id: 'epistemology',
              name: 'Epistemology',
              color: '#cbd5e1',
              description: 'Theory of knowledge',
              nodes: [
                { id: 'theory-knowledge', name: 'Theory of Knowledge', domain: 'epistemology', prereqs: [], difficulty: 4, points: 200 },
                { id: 'skepticism', name: 'Skepticism', domain: 'epistemology', prereqs: ['theory-knowledge'], difficulty: 4, points: 200 },
                { id: 'philosophy-science', name: 'Philosophy of Science', domain: 'epistemology', prereqs: ['theory-knowledge'], difficulty: 4, points: 200 },
                { id: 'philosophy-language', name: 'Philosophy of Language', domain: 'epistemology', prereqs: ['theory-knowledge'], difficulty: 5, points: 250 }
              ]
            },
            {
              id: 'ethics',
              name: 'Ethics',
              color: '#cbd5e1',
              description: 'Moral philosophy',
              nodes: [
                { id: 'moral-theory', name: 'Moral Theory', domain: 'ethics', prereqs: [], difficulty: 3, points: 150 },
                { id: 'applied-ethics', name: 'Applied Ethics', domain: 'ethics', prereqs: ['moral-theory'], difficulty: 3, points: 150 },
                { id: 'political-philosophy', name: 'Political Philosophy', domain: 'ethics', prereqs: ['moral-theory'], difficulty: 4, points: 200 },
                { id: 'bioethics', name: 'Bioethics', domain: 'ethics', prereqs: ['applied-ethics'], difficulty: 4, points: 200 }
              ]
            }
          ]
        },
        {
          id: 'religious-studies',
          name: 'Religious Studies',
          color: '#94a3b8',
          description: 'Study of world religions',
          nodes: [
            { id: 'comparative-religion', name: 'Comparative Religion', domain: 'religious-studies', prereqs: [], difficulty: 3, points: 150 },
            { id: 'theology', name: 'Theology', domain: 'religious-studies', prereqs: [], difficulty: 4, points: 200 },
            { id: 'religious-history', name: 'Religious History', domain: 'religious-studies', prereqs: ['comparative-religion'], difficulty: 3, points: 150 },
            { id: 'mythology', name: 'Mythology', domain: 'religious-studies', prereqs: [], difficulty: 3, points: 150 },
            { id: 'religious-philosophy', name: 'Religious Philosophy', domain: 'religious-studies', prereqs: ['theology', 'moral-theory'], difficulty: 5, points: 250 }
          ]
        },
        {
          id: 'logic',
          name: 'Logic',
          color: '#94a3b8',
          description: 'Principles of reasoning',
          nodes: [
            { id: 'propositional-logic', name: 'Propositional Logic', domain: 'logic', prereqs: [], difficulty: 3, points: 150 },
            { id: 'predicate-logic', name: 'Predicate Logic', domain: 'logic', prereqs: ['propositional-logic'], difficulty: 4, points: 200 },
            { id: 'modal-logic', name: 'Modal Logic', domain: 'logic', prereqs: ['predicate-logic'], difficulty: 5, points: 250 },
            { id: 'mathematical-logic', name: 'Mathematical Logic', domain: 'logic', prereqs: ['predicate-logic'], difficulty: 5, points: 250 },
            { id: 'computational-logic', name: 'Computational Logic', domain: 'logic', prereqs: ['mathematical-logic'], difficulty: 5, points: 250 }
          ]
        }
      ]
    },
    {
      id: 'business',
      name: 'Business & Finance',
      color: '#059669',
      description: 'Commerce and financial management',
      subcategories: [
        {
          id: 'business-fundamentals',
          name: 'Business Fundamentals',
          color: '#10b981',
          description: 'Core business concepts',
          nodes: [
            { id: 'business-strategy', name: 'Business Strategy', domain: 'business-fundamentals', prereqs: [], difficulty: 3, points: 150 },
            { id: 'marketing', name: 'Marketing', domain: 'business-fundamentals', prereqs: [], difficulty: 3, points: 150 },
            { id: 'operations-management', name: 'Operations Management', domain: 'business-fundamentals', prereqs: [], difficulty: 3, points: 150 },
            { id: 'human-resources', name: 'Human Resources', domain: 'business-fundamentals', prereqs: [], difficulty: 3, points: 150 },
            { id: 'business-law', name: 'Business Law', domain: 'business-fundamentals', prereqs: [], difficulty: 3, points: 150 }
          ]
        },
        {
          id: 'finance',
          name: 'Finance',
          color: '#10b981',
          description: 'Financial management',
          nodes: [
            { id: 'financial-accounting', name: 'Financial Accounting', domain: 'finance', prereqs: [], difficulty: 3, points: 150 },
            { id: 'corporate-finance', name: 'Corporate Finance', domain: 'finance', prereqs: ['financial-accounting'], difficulty: 4, points: 200 },
            { id: 'investments', name: 'Investments', domain: 'finance', prereqs: ['corporate-finance'], difficulty: 4, points: 200 },
            { id: 'derivatives', name: 'Derivatives', domain: 'finance', prereqs: ['investments'], difficulty: 5, points: 250 },
            { id: 'risk-management', name: 'Risk Management', domain: 'finance', prereqs: ['probability', 'investments'], difficulty: 5, points: 250 }
          ]
        },
        {
          id: 'entrepreneurship',
          name: 'Entrepreneurship',
          color: '#10b981',
          description: 'Starting and running businesses',
          nodes: [
            { id: 'startup-fundamentals', name: 'Startup Fundamentals', domain: 'entrepreneurship', prereqs: [], difficulty: 3, points: 150 },
            { id: 'product-development', name: 'Product Development', domain: 'entrepreneurship', prereqs: ['startup-fundamentals'], difficulty: 3, points: 150 },
            { id: 'venture-capital', name: 'Venture Capital', domain: 'entrepreneurship', prereqs: ['startup-fundamentals'], difficulty: 4, points: 200 },
            { id: 'business-scaling', name: 'Business Scaling', domain: 'entrepreneurship', prereqs: ['product-development'], difficulty: 4, points: 200 },
            { id: 'exit-strategies', name: 'Exit Strategies', domain: 'entrepreneurship', prereqs: ['business-scaling'], difficulty: 4, points: 200 }
          ]
        }
      ]
    }
  ]
};

export function flattenKnowledgeStructure(
  category: KnowledgeCategory,
  parentPath: string[] = [],
  expandedCategories: Set<string> = new Set()
): Node[] {
  const nodes: Node[] = [];
  const currentPath = [...parentPath, category.id];
  
  if (category.nodes) {
    category.nodes.forEach(node => {
      nodes.push({
        ...node,
        domain: category.id,
        path: currentPath,
        level: currentPath.length - 1,
        isVisible: parentPath.every(id => expandedCategories.has(id))
      } as Node);
    });
  }
  
  if (category.subcategories && (parentPath.length === 0 || expandedCategories.has(category.id))) {
    category.subcategories.forEach(subcategory => {
      nodes.push(...flattenKnowledgeStructure(subcategory, currentPath, expandedCategories));
    });
  }
  
  return nodes;
}

export function getCategoryHierarchy(
  category: KnowledgeCategory,
  depth: number = 0,
  expandedCategories: Set<string> = new Set()
): any[] {
  const result: any = {
    id: category.id,
    name: category.name,
    color: category.color,
    description: category.description,
    depth,
    hasChildren: !!(category.subcategories && category.subcategories.length > 0),
    hasNodes: !!(category.nodes && category.nodes.length > 0),
    isExpanded: expandedCategories.has(category.id),
    nodeCount: category.nodes?.length || 0
  };
  
  if (category.subcategories && expandedCategories.has(category.id)) {
    result.children = category.subcategories.map(sub => 
      getCategoryHierarchy(sub, depth + 1, expandedCategories)
    );
  }
  
  return [result];
}