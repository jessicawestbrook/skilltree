# Learning Content Template System Documentation

## Overview

The SkillTree learning content template system provides standardized, consistent formatting for all educational materials. This system ensures visual consistency, accessibility, and maintainability across all learning modules.

## Template Architecture

### 1. Core Templates

#### Standard Learning Content Template (`learningContentTemplate.html`)
- **Purpose**: Universal template for all subjects
- **Location**: `src/templates/learningContentTemplate.html`
- **Use Cases**: General educational content, language learning, science topics, history lessons

**Key Sections:**
- Module Header (metadata, title, description)
- Learning Objectives
- Prerequisites
- Introduction with real-world connections
- Concept sections with examples
- Practice problems with feedback
- Common mistakes to avoid
- Summary and quick checks
- Extension activities
- Progress tracking

#### Elementary Math Template (`elementaryMathTemplate.html`)
- **Purpose**: Math-specific extensions for K-8 content
- **Location**: `src/templates/elementaryMathTemplate.html`
- **Use Cases**: Arithmetic, geometry, fractions, algebra basics

**Additional Features:**
- Visual manipulatives and counters
- Number lines
- Math workspaces
- Step-by-step worked examples
- Mental math sections
- Strategy cards
- Parent/teacher notes

#### Money Counting Template (`moneyCountingTemplate.html`)
- **Purpose**: Specialized template for financial literacy
- **Location**: `src/templates/moneyCountingTemplate.html`
- **Use Cases**: Coin recognition, counting money, making change

**Unique Elements:**
- Interactive coin/bill graphics
- Running total displays
- Cash register simulations
- Skip counting patterns
- Shopping scenarios
- Piggy bank games

### 2. Supporting Files

#### Standard CSS (`standardLearningContent.css`)
- **Location**: `public/styles/standardLearningContent.css`
- **Features**:
  - Consistent color palette (Green primary #10b981, Gold secondary #f59e0b)
  - Responsive design with mobile-first approach
  - Dark mode support
  - Print-friendly styles
  - Accessibility features (WCAG AA compliant)

#### Currency Graphics
- **Location**: `public/images/currency/`
- **Files**:
  - `us-coins.svg`: All US coins (penny through dollar)
  - `us-bills.svg`: All US bills ($1-$100)
- **Format**: SVG for scalability and small file size

## Usage Guide

### Using the Template Generator

```typescript
import { LearningContentGenerator, ElementaryMathData } from '@/utils/learningContentGenerator';

// Create content data object
const lessonData: ElementaryMathData = {
  category: 'Elementary Math',
  mathSubcategory: 'Multiplication',
  gradeLevel: '3',
  difficultyLevel: 'Intermediate',
  estimatedTime: 25,
  moduleTitle: 'Multiplication Tables: 2s and 5s',
  moduleDescription: 'Master multiplication by 2 and 5',
  
  objectives: [
    'Memorize 2 and 5 times tables',
    'Identify patterns in multiplication',
    'Solve word problems using multiplication'
  ],
  
  // ... additional content data
};

// Generate HTML
const htmlContent = LearningContentGenerator.generateElementaryMathContent(lessonData);
```

### Manual Template Usage

1. **Copy the appropriate template file**
2. **Replace placeholder variables** (format: `{{VARIABLE_NAME}}`)
3. **Add custom interactive elements** as needed
4. **Include the standard CSS file**

### Template Placeholders

Common placeholders across all templates:
- `{{MODULE_TITLE}}`: Lesson title
- `{{MODULE_DESCRIPTION}}`: Brief description
- `{{CATEGORY}}`: Subject category
- `{{DIFFICULTY_LEVEL}}`: Beginner/Intermediate/Advanced
- `{{ESTIMATED_TIME}}`: Time in minutes

## Best Practices

### Content Creation

1. **Keep sections focused**: Each concept should have a single learning objective
2. **Use progressive disclosure**: Start simple, build complexity
3. **Include multiple representations**: Visual, textual, and interactive
4. **Provide immediate feedback**: Especially for practice problems
5. **Make it relevant**: Always include real-world connections

### Visual Design

1. **Maintain consistency**: Use the standard color palette
2. **Ensure readability**: Minimum 16px font size, good contrast
3. **Mobile-first**: Test on small screens first
4. **Limit cognitive load**: No more than 5-7 items per section
5. **Use meaningful icons**: Consistent iconography across modules

### Accessibility

1. **Semantic HTML**: Use proper heading hierarchy
2. **Alt text**: Describe all visual content
3. **Keyboard navigation**: All interactive elements must be keyboard accessible
4. **ARIA labels**: Add where semantic HTML isn't sufficient
5. **Color contrast**: Minimum 4.5:1 for normal text, 3:1 for large text

### Interactive Elements

1. **Progressive enhancement**: Content should work without JavaScript
2. **Clear feedback**: Visual and textual confirmation of actions
3. **Error prevention**: Validate input before submission
4. **Undo capability**: Allow users to change answers
5. **Save progress**: Store user state locally

## Template Customization

### Adding New Sections

```html
<!-- Add new section after existing content -->
<section class="custom-section">
  <h2>New Section Title</h2>
  <div class="section-content">
    <!-- Custom content here -->
  </div>
</section>
```

### Creating Subject-Specific Templates

1. **Extend the base template**: Start with `learningContentTemplate.html`
2. **Add subject-specific sections**: Keep core structure intact
3. **Create companion CSS**: Use `standardLearningContent.css` as base
4. **Document unique features**: Update this guide

### Custom Styling

```css
/* Add to subject-specific CSS file */
@import '/styles/standardLearningContent.css';

.custom-element {
  /* Subject-specific styles */
  background: var(--color-primary-light);
  /* Maintain design system variables */
}
```

## Content Guidelines

### Grade-Appropriate Language

**K-2 (Ages 5-7)**
- Simple sentences (5-8 words)
- Concrete concepts
- Lots of visuals
- Basic vocabulary

**3-5 (Ages 8-10)**
- Compound sentences
- Abstract concepts introduced
- Mixed media
- Subject-specific terms

**6-8 (Ages 11-13)**
- Complex sentences
- Abstract reasoning
- Text-heavy with supporting visuals
- Technical vocabulary

**9-12 (Ages 14-18)**
- Academic language
- Complex concepts
- Minimal hand-holding
- Professional terminology

### Problem Difficulty Progression

1. **Recognition**: Identify correct answer
2. **Recall**: Remember without hints
3. **Application**: Use in new context
4. **Analysis**: Break down complex problems
5. **Synthesis**: Combine concepts
6. **Evaluation**: Judge and justify

## Testing Templates

### Visual Testing
1. Check responsive design at 320px, 768px, 1024px, 1920px
2. Test dark mode toggle
3. Verify print layout
4. Check loading performance

### Interaction Testing
1. Test all buttons and inputs
2. Verify answer feedback
3. Check progress tracking
4. Test keyboard navigation

### Content Testing
1. Verify all placeholders replaced
2. Check for broken images/links
3. Validate learning objectives met
4. Review for age-appropriateness

## Template Maintenance

### Version Control
- Templates are versioned with the main application
- Breaking changes require migration guide
- Backward compatibility for 2 major versions

### Update Process
1. Test changes in development
2. Update affected content
3. Document changes in CHANGELOG
4. Notify content creators

### Performance Optimization
- Minimize template size (<50KB)
- Lazy load images and videos
- Use CSS animations over JavaScript
- Cache static content

## Common Issues and Solutions

### Issue: Content overflow on mobile
**Solution**: Use responsive units (rem, %, vw) and test at 320px width

### Issue: Dark mode colors incorrect
**Solution**: Use CSS variables for all colors, define both light and dark values

### Issue: Interactive elements not working
**Solution**: Check JavaScript console, ensure scripts loaded after DOM

### Issue: Print layout broken
**Solution**: Use print-specific CSS, hide interactive elements

### Issue: Slow loading
**Solution**: Optimize images, lazy load below-fold content, minimize CSS/JS

## Future Enhancements

### Planned Features
- Video integration templates
- Interactive simulations
- Collaborative learning sections
- Gamification elements
- AI-powered hints

### Template Roadmap
1. **Phase 1**: Science experiment templates
2. **Phase 2**: Language learning with audio
3. **Phase 3**: Programming tutorials with code editors
4. **Phase 4**: Music and art templates
5. **Phase 5**: Virtual lab simulations

## Support and Resources

### Documentation
- This guide: `/documentation/LEARNING_CONTENT_TEMPLATES.md`
- CSS variables: `/public/styles/standardLearningContent.css`
- Generator API: `/src/utils/learningContentGenerator.ts`

### Examples
- Money Counting: `/src/templates/moneyCountingTemplate.html`
- Basic Math: Generated via `generateExampleContent()`

### Tools
- Template Generator: `LearningContentGenerator` class
- Preview Server: `npm start`
- Template Validator: (planned)

## Appendix

### CSS Variable Reference

```css
/* Primary Colors */
--color-primary: #10b981;      /* Green */
--color-primary-dark: #059669;
--color-primary-light: #34d399;

/* Secondary Colors */
--color-secondary: #f59e0b;    /* Gold */
--color-secondary-dark: #d97706;
--color-secondary-light: #fbbf24;

/* Semantic Colors */
--color-success: #10b981;
--color-warning: #f59e0b;
--color-error: #ef4444;
--color-info: #3b82f6;

/* Spacing */
--space-xs: 0.25rem;
--space-sm: 0.5rem;
--space-md: 1rem;
--space-lg: 1.5rem;
--space-xl: 2rem;
--space-2xl: 3rem;
```

### Template Placeholder Reference

See inline comments in each template file for complete placeholder documentation.

### Migration Guide

When updating templates:
1. Back up existing content
2. Run migration script (if provided)
3. Test sample content
4. Update production content
5. Monitor for issues

---

*Last Updated: December 2024*
*Version: 1.0.0*