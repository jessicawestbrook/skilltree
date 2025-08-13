#!/usr/bin/env node

/**
 * Migration script for course content
 * Run this after creating the course_content tables
 */

require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing environment variables. Please check your .env.local file');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Sample course content for different nodes
const courseContents = [
  {
    node_id: 'symbols-meaning',
    title: 'Understanding Symbols and Their Meaning',
    overview: 'Learn how symbols are used to represent ideas, concepts, and objects in various contexts.',
    learning_objectives: [
      'Understand what symbols are and their purpose',
      'Identify different types of symbols in everyday life',
      'Analyze how symbols convey meaning across cultures',
      'Create and interpret symbolic representations'
    ],
    estimated_time: 20,
    difficulty_level: 'beginner',
    sections: [
      {
        section_order: 0,
        section_type: 'introduction',
        title: 'What Are Symbols?',
        content: `Symbols are marks, signs, or words that indicate, signify, or represent an idea, object, or relationship. They are fundamental to human communication and understanding.

Throughout history, humans have used symbols to convey complex ideas in simple forms. From ancient cave paintings to modern digital icons, symbols help us communicate across language barriers and express abstract concepts.

In this lesson, we'll explore how symbols work, why they're important, and how they shape our understanding of the world.`
      },
      {
        section_order: 1,
        section_type: 'concept',
        title: 'Types of Symbols',
        content: `Symbols can be categorized into several types:

1. **Visual Symbols**: Icons, logos, traffic signs, and emojis that communicate through images.

2. **Written Symbols**: Letters, numbers, and punctuation marks that form our written language.

3. **Mathematical Symbols**: Plus (+), minus (-), equals (=), and other symbols that express mathematical relationships.

4. **Cultural Symbols**: Flags, religious icons, and traditional patterns that represent cultural identity.

5. **Universal Symbols**: Hearts for love, skulls for danger, and other symbols understood across cultures.

Each type serves a specific purpose in communication and understanding.`
      },
      {
        section_order: 2,
        section_type: 'example',
        title: 'Symbols in Daily Life',
        content: `Let's examine some common symbols you encounter every day:

**Traffic Lights**: Red means stop, yellow means caution, green means go. These colors have become universal symbols for these actions.

**App Icons**: The envelope symbol for email, the camera for photos, the gear for settings - these visual symbols help us navigate digital interfaces quickly.

**Currency Symbols**: $, €, £, ¥ - these symbols instantly communicate which currency is being referenced.

**Weather Symbols**: A sun for sunny weather, clouds for cloudy, raindrops for rain - meteorologists use these standardized symbols worldwide.

Notice how these symbols transcend language barriers and communicate instantly.`
      },
      {
        section_order: 3,
        section_type: 'practice',
        title: 'Creating Your Own Symbols',
        content: `Now let's practice creating symbols. Consider these guidelines:

1. **Simplicity**: Effective symbols are simple and easily recognizable.

2. **Relevance**: The symbol should relate to what it represents.

3. **Distinctiveness**: It should be unique enough to avoid confusion.

4. **Scalability**: Good symbols work at different sizes.

Try creating symbols for:
- A new social media platform focused on learning
- A warning sign for a slippery floor
- An icon representing "collaboration"

Remember, the best symbols are intuitive and memorable.`
      },
      {
        section_order: 4,
        section_type: 'summary',
        title: 'Key Takeaways',
        content: `In this lesson, we've learned that:

• Symbols are powerful tools for communication that transcend language barriers
• Different types of symbols serve various purposes in our daily lives
• Effective symbols are simple, relevant, and distinctive
• Understanding symbols helps us navigate the world more effectively
• Creating good symbols requires thoughtful design and consideration of the audience

As you continue learning, pay attention to the symbols around you and consider how they influence your understanding and actions.`
      }
    ],
    key_concepts: [
      {
        term: 'Symbol',
        definition: 'A mark, sign, or word that indicates or represents an idea, object, or relationship',
        example: 'The @ symbol represents "at" in email addresses'
      },
      {
        term: 'Icon',
        definition: 'A pictorial representation of an object or concept',
        example: 'The trash can icon on your computer represents deleting files'
      },
      {
        term: 'Semiotics',
        definition: 'The study of signs and symbols and their use or interpretation',
        example: 'Analyzing how different cultures interpret the color red'
      }
    ],
    learning_tips: [
      {
        tip_type: 'general',
        content: 'Start a symbol journal - sketch or photograph interesting symbols you encounter daily'
      },
      {
        tip_type: 'best_practice',
        content: 'When designing symbols, test them with people unfamiliar with your concept to ensure clarity'
      },
      {
        tip_type: 'common_mistake',
        content: 'Avoid making symbols too complex - if it takes more than a second to understand, simplify it'
      }
    ],
    resources: [
      {
        resource_type: 'article',
        title: 'The History of Symbols in Human Communication',
        description: 'Explore how symbols evolved from cave paintings to digital icons',
        url: 'https://example.com/history-of-symbols',
        is_required: false
      },
      {
        resource_type: 'video',
        title: 'TED Talk: The Power of Visual Communication',
        description: 'Learn how symbols and visual language shape our thinking',
        url: 'https://example.com/ted-visual-communication',
        is_required: true
      }
    ]
  },
  {
    node_id: 'patterns-basics',
    title: 'Introduction to Patterns',
    overview: 'Discover how patterns appear in nature, mathematics, art, and everyday life.',
    learning_objectives: [
      'Define what patterns are and their characteristics',
      'Identify patterns in various contexts',
      'Understand the role of repetition and regularity',
      'Create and extend simple patterns'
    ],
    estimated_time: 25,
    difficulty_level: 'beginner',
    sections: [
      {
        section_order: 0,
        section_type: 'introduction',
        title: 'The World of Patterns',
        content: `Patterns are everywhere - in the spirals of seashells, the rhythm of music, the cycles of seasons, and the designs in art. A pattern is a repeated or regular arrangement of elements that follows a rule or principle.

Understanding patterns helps us make predictions, solve problems, and appreciate the underlying order in seemingly chaotic systems. From the Fibonacci sequence in nature to the patterns in computer algorithms, recognizing patterns is a fundamental cognitive skill.

In this lesson, we'll explore different types of patterns and learn how to identify and create them.`
      },
      {
        section_order: 1,
        section_type: 'concept',
        title: 'Elements of Patterns',
        content: `Every pattern has key elements:

**Repetition**: The core of any pattern is repetition. Elements repeat in a predictable way.

**Rule or Principle**: Patterns follow specific rules that determine how elements repeat.

**Unit of Repeat**: The smallest complete sequence that repeats to form the pattern.

**Predictability**: Once you understand the rule, you can predict what comes next.

Types of patterns include:
- Sequential (1, 2, 3, 4...)
- Alternating (A, B, A, B...)
- Growing (1, 2, 4, 8...)
- Symmetrical (mirror patterns)
- Tessellations (shapes that fit together without gaps)`
      },
      {
        section_order: 2,
        section_type: 'example',
        title: 'Patterns in Nature',
        content: `Nature is full of fascinating patterns:

**Fibonacci Sequence**: Found in sunflower seeds, pine cones, and nautilus shells. The sequence (1, 1, 2, 3, 5, 8, 13...) appears when each number is the sum of the two before it.

**Fractals**: Self-similar patterns that repeat at different scales. Examples include snowflakes, ferns, and coastlines.

**Symmetry**: Butterfly wings, flowers, and human faces exhibit bilateral symmetry.

**Waves and Spirals**: Ocean waves, sand dunes, and galaxy spirals follow mathematical patterns.

**Hexagons**: Honeycomb structures and basalt columns form hexagonal patterns for maximum efficiency.

These patterns aren't random - they emerge from physical and mathematical principles.`
      },
      {
        section_order: 3,
        section_type: 'summary',
        title: 'Pattern Recognition Skills',
        content: `You've learned that patterns are:

• Repeated arrangements following specific rules
• Found throughout nature, mathematics, and human design
• Essential for prediction and problem-solving
• Based on principles like repetition, symmetry, and growth

Developing pattern recognition helps in:
- Mathematics and coding
- Music and art
- Scientific observation
- Problem-solving and logical thinking

Keep observing the world around you - patterns are waiting to be discovered!`
      }
    ],
    key_concepts: [
      {
        term: 'Pattern',
        definition: 'A repeated or regular arrangement of elements following a rule',
        example: 'The pattern 2, 4, 6, 8 follows the rule "add 2"'
      },
      {
        term: 'Tessellation',
        definition: 'A pattern of shapes that fit together without gaps or overlaps',
        example: 'Hexagonal tiles in a honeycomb'
      },
      {
        term: 'Fractal',
        definition: 'A pattern that repeats at every scale',
        example: 'A fern leaf where each small part resembles the whole leaf'
      }
    ],
    learning_tips: [
      {
        tip_type: 'general',
        content: 'Look for patterns in your daily routine - they can help you optimize your time'
      },
      {
        tip_type: 'warning',
        content: 'Don\'t force patterns where they don\'t exist - sometimes randomness is just randomness'
      }
    ]
  }
];

async function migrateContent() {
  console.log('Starting course content migration...');
  
  for (const content of courseContents) {
    try {
      console.log(`\nMigrating content for node: ${content.node_id}`);
      
      // Extract nested data
      const { sections, key_concepts, learning_tips, resources, ...mainContent } = content;
      
      // Insert main content
      const { data: contentData, error: contentError } = await supabase
        .from('course_content')
        .upsert(mainContent, { onConflict: 'node_id' })
        .select()
        .single();
      
      if (contentError) {
        console.error(`Error inserting content for ${content.node_id}:`, contentError);
        continue;
      }
      
      console.log(`✓ Created content: ${contentData.title}`);
      
      // Insert sections
      if (sections && sections.length > 0) {
        const sectionsWithContentId = sections.map(s => ({
          ...s,
          content_id: contentData.id
        }));
        
        const { error: sectionsError } = await supabase
          .from('course_sections')
          .insert(sectionsWithContentId);
        
        if (sectionsError) {
          console.error(`Error inserting sections:`, sectionsError);
        } else {
          console.log(`  ✓ Added ${sections.length} sections`);
        }
      }
      
      // Insert key concepts
      if (key_concepts && key_concepts.length > 0) {
        const conceptsWithContentId = key_concepts.map(c => ({
          ...c,
          content_id: contentData.id
        }));
        
        const { error: conceptsError } = await supabase
          .from('key_concepts')
          .insert(conceptsWithContentId);
        
        if (!conceptsError) {
          console.log(`  ✓ Added ${key_concepts.length} key concepts`);
        }
      }
      
      // Insert learning tips
      if (learning_tips && learning_tips.length > 0) {
        const tipsWithContentId = learning_tips.map(t => ({
          ...t,
          content_id: contentData.id
        }));
        
        const { error: tipsError } = await supabase
          .from('learning_tips')
          .insert(tipsWithContentId);
        
        if (!tipsError) {
          console.log(`  ✓ Added ${learning_tips.length} learning tips`);
        }
      }
      
      // Insert resources
      if (resources && resources.length > 0) {
        const resourcesWithContentId = resources.map(r => ({
          ...r,
          content_id: contentData.id
        }));
        
        const { error: resourcesError } = await supabase
          .from('course_resources')
          .insert(resourcesWithContentId);
        
        if (!resourcesError) {
          console.log(`  ✓ Added ${resources.length} resources`);
        }
      }
      
    } catch (error) {
      console.error(`Error migrating content for ${content.node_id}:`, error);
    }
  }
  
  console.log('\n✅ Course content migration complete!');
}

// Run migration
migrateContent().catch(console.error);