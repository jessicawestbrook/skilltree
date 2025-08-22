# Archived Skill Tree Components

This folder contains skill tree visualization components that have been temporarily removed from the main application but preserved for potential future reintegration.

## Archived Components

### SkillTreePage.tsx
- **Purpose**: D3.js-based interactive skill tree visualization
- **Features**: 
  - Radial tree layout with zoom/pan functionality
  - Node filtering and search capabilities
  - Interactive node selection and learning content modal
  - Progress indicators and completion status
  - Responsive design with touch/mouse support

### TextOnlySkillTreePage.tsx
- **Purpose**: Text-based hierarchical view of the skill tree
- **Features**:
  - Expandable tree structure with categories and skills
  - Search and filtering capabilities
  - Progress indicators
  - Simpler interface for low-bandwidth or accessibility needs
  - Export to learning path functionality

## Original Routes (Removed)
- `/skill-tree` - Main visual skill tree page
- `/text-tree` - Text-only skill tree page

## Integration Points Redirected To:
- Navigation links → `/learning-paths`
- Breadcrumb links → `/learning-paths`
- Category-specific links → `/category/{id}`

## Dependencies Used
- D3.js for visualization
- React hooks for state management
- Supabase for data fetching
- Tailwind CSS for styling

## Reintegration Notes
If you want to restore these components:

1. Move files back to `src/pages/`
2. Add imports back to `src/App.tsx`:
   ```tsx
   import SkillTreePage from './pages/SkillTreePage'
   import TextOnlySkillTreePage from './pages/TextOnlySkillTreePage'
   ```
3. Add routes back to `src/App.tsx`:
   ```tsx
   <Route path="skill-tree" element={<SkillTreePage />} />
   <Route path="text-tree" element={<TextOnlySkillTreePage />} />
   ```
4. Restore navigation links in components as needed
5. Test functionality and update any deprecated dependencies

## Date Archived
August 20, 2025

## Reason for Archiving
User requested removal of links to skill tree pages while preserving code for potential future use.