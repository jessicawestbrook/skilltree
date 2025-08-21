# Academic Ordering Schema for SkillTree

## Overview

This document defines the comprehensive academic ordering system for the SkillTree platform, ensuring that learning content follows proper educational progression from foundational concepts to advanced topics.

## Ordering Principles

### 1. Educational Progression
- **Foundation First**: Basic concepts precede advanced ones
- **Prerequisites**: Required knowledge comes before dependent topics
- **Cognitive Load**: Simple concepts before complex applications
- **Practical Application**: Theory before specialized applications

### 2. Academic Standards Alignment
- **K-12 Progression**: Early childhood through high school sequence
- **Higher Education**: College-level prerequisite chains
- **Professional Development**: Career progression pathways
- **Lifelong Learning**: Interest-based exploration paths

### 3. Cultural and Practical Considerations
- **Language Utility**: Modern practical languages before academic languages
- **Global Relevance**: Widely-used skills before specialized ones
- **Career Alignment**: Professional pathway progression
- **Accessibility**: Common topics before specialized ones

## Top-Level Category Ordering

```
Position | Category | Rationale
---------|----------|----------
10       | Mathematics | Foundation for all STEM fields
20       | Natural Sciences | Builds on mathematical concepts
30       | Computer Science | Requires math and logical thinking
40       | Applied Sciences | Applies natural sciences principles
50       | Social Sciences | Human behavior and society studies
60       | Languages | Communication and cultural understanding
70       | Humanities | Cultural, historical, philosophical studies
80       | Creative Skills | Artistic and creative expression
90       | Professional Skills | Career-specific applications
100      | Life Skills | Practical daily applications
110      | Technical Skills | Specialized tools and techniques
120      | Test Preparation | Evaluation and assessment
```

## Subject-Specific Ordering Schemas

### Mathematics (Parent ID: Mathematics)

```
Order | Subject | Prerequisites | Notes
------|---------|---------------|-------
10    | Early Math Concepts | None | Ages 3-6: Numbers, counting, shapes
20    | Arithmetic Foundations | Early Math | Basic operations, fractions
30    | Elementary Algebra | Arithmetic | Introduction to variables, equations
40    | Geometry | Arithmetic | Shapes, measurements, proofs
50    | Statistics and Probability | Arithmetic | Data analysis, basic probability
60    | Intermediate Algebra | Elementary Algebra | Advanced equations, functions
70    | Discrete Mathematics | Intermediate Algebra | Logic, sets, combinatorics
80    | Calculus | Intermediate Algebra | Limits, derivatives, integrals
90    | Applied Mathematics | Calculus | Real-world applications
100   | Abstract Algebra | Calculus | Advanced mathematical structures
```

### Languages (Parent ID: Languages)

```
Order | Language | Difficulty | Rationale
------|----------|------------|----------
10    | Spanish | Easy | Most practical for English speakers
20    | French | Easy-Medium | Romance language, cultural importance
30    | Italian | Easy-Medium | Romance language family
40    | Portuguese | Medium | Romance language, growing importance
50    | German | Medium | Important for academics/business
60    | Mandarin Chinese | Hard | Global importance, increasing relevance
70    | Japanese | Hard | Economic/cultural significance
80    | Korean | Hard | Growing cultural influence
90    | Arabic | Hard | Global religious/political importance
100   | Russian | Hard | Geopolitical significance
110   | Latin | Academic | Foundation for Romance languages
120   | Ancient Greek | Academic | Classical studies, philosophy
```

### Natural Sciences (Parent ID: Natural Sciences)

```
Order | Subject | Prerequisites | Notes
------|---------|---------------|-------
10    | Scientific Method | None | Foundation for all sciences
20    | Basic Physics | Arithmetic | Motion, forces, energy
30    | Chemistry Fundamentals | Basic Physics | Atoms, molecules, reactions
40    | Biology Basics | None | Living systems, cells
50    | Earth Science | Basic Physics | Geology, meteorology, astronomy
60    | Advanced Physics | Calculus | Quantum, relativity, thermodynamics
70    | Organic Chemistry | Chemistry + Biology | Carbon-based molecules
80    | Advanced Biology | Biology + Chemistry | Genetics, molecular biology
90    | Environmental Science | All Sciences | Interdisciplinary applications
```

### Computer Science (Parent ID: Computer Science)

```
Order | Subject | Prerequisites | Notes
------|---------|---------------|-------
10    | Computer Literacy | None | Basic computer operation
20    | Introduction to Programming | Computer Literacy | Concepts, logic
30    | Programming Fundamentals | Intro Programming | Specific languages
40    | Data Structures | Programming | Organization of data
50    | Algorithms | Data Structures | Problem-solving methods
60    | Software Engineering | Algorithms | Large-scale development
70    | Database Systems | Programming | Data management
80    | Computer Networks | Programming | Distributed systems
90    | Artificial Intelligence | Advanced Programming | Machine learning, AI
100   | Cybersecurity | Networks + Programming | Security principles
```

### Humanities (Parent ID: Humanities)

```
Order | Subject | Prerequisites | Notes
------|---------|---------------|-------
10    | World History Overview | None | Global historical context
20    | Ancient Civilizations | World History | Foundation cultures
30    | Classical Literature | Reading Skills | Literary foundations
40    | Philosophy Introduction | Critical Thinking | Basic philosophical concepts
50    | Art History | World History | Cultural artistic development
60    | Modern History | Ancient + World | Recent historical periods
70    | Advanced Literature | Classical Literature | Period-specific studies
80    | Ethics and Moral Philosophy | Philosophy Intro | Applied philosophy
90    | Cultural Studies | History + Literature | Interdisciplinary analysis
```

### Social Sciences (Parent ID: Social Sciences)

```
Order | Subject | Prerequisites | Notes
------|---------|---------------|-------
10    | Introduction to Psychology | None | Individual behavior
20    | Sociology Basics | Psychology | Group behavior, society
30    | Economics Fundamentals | Mathematics | Basic economic principles
40    | Political Science | Sociology | Government, politics
50    | Anthropology | Sociology + Psychology | Human cultures
60    | Advanced Psychology | Psychology Intro | Specialized areas
70    | Macroeconomics | Economics Fundamentals | Large-scale economics
80    | International Relations | Political Science | Global politics
90    | Research Methods | Statistics | Social science research
```

### Creative Skills (Parent ID: Creative Skills)

```
Order | Subject | Prerequisites | Notes
------|---------|---------------|-------
10    | Art Fundamentals | None | Basic drawing, color theory
20    | Music Theory Basics | None | Musical foundations
30    | Creative Writing | Language Skills | Storytelling, composition
40    | Design Principles | Art Fundamentals | Visual design concepts
50    | Digital Art | Art + Computer Literacy | Digital creation tools
60    | Advanced Music | Music Theory | Composition, performance
70    | Photography | Art + Technical Skills | Visual storytelling
80    | Video Production | Photography + Technology | Moving image creation
90    | Advanced Design | Design Principles | Specialized design fields
```

## Implementation Guidelines

### Database Structure
- Use `display_order` field with decimal spacing (10, 20, 30...)
- Allow for future insertions between existing items
- Maintain consistency within each hierarchical level
- Preserve flexibility for curriculum updates

### Ordering Algorithm
```sql
ORDER BY 
  COALESCE(display_order, 999999),  -- Explicit order first
  name                              -- Alphabetical fallback
```

### Validation Rules
1. **No Gaps**: Each level should have consecutive ordering
2. **No Duplicates**: Unique display_order within each parent
3. **Logical Progression**: Advanced topics after prerequisites
4. **Cultural Sensitivity**: Respectful ordering of cultural content

### Maintenance Process
1. **Regular Review**: Quarterly assessment of ordering effectiveness
2. **User Feedback**: Incorporate learner pathway data
3. **Curriculum Updates**: Adjust for educational standard changes
4. **A/B Testing**: Test ordering variations for effectiveness

## Special Considerations

### Multiple Valid Orderings
Some subjects may have multiple valid learning paths:
- **Concurrent Topics**: Sciences can be learned simultaneously
- **Interest-Driven**: Creative subjects may follow passion
- **Skill-Level**: Allow users to skip prerequisites with testing

### Cultural Adaptation
- **Regional Variations**: Allow different ordering by geography
- **Language Preferences**: Prioritize relevant languages by location
- **Educational Systems**: Adapt to different national curricula

### Accessibility
- **Learning Differences**: Alternative progression paths
- **Age Appropriateness**: Content suitable for target age groups
- **Prerequisite Flexibility**: Allow testing out of prerequisites

---

*Schema Version: 1.0*  
*Last Updated: 2025-08-21*  
*Next Review: 2025-11-21*