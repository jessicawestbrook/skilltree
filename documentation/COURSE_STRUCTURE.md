# Course Structure Documentation

## Overview
Courses in SkillTree are implemented using the existing `skill_tree_nodes` table structure, where courses are child nodes of skill nodes. This provides a clean hierarchical organization without requiring separate tables.

## Database Structure

### Hierarchy
```
Category (skill_tree_node)
  └─ Skill (skill_tree_node with parent = category)
      └─ Course (skill_tree_node with parent = skill)
          └─ Module/Lesson (optional further nesting)
```

### Example: Latin Language
```
Languages (Category)
  └─ Latin Language (Skill) 
      ├─ Henle Latin: First Year (Course)
      ├─ Henle Latin: Second Year (Course)
      ├─ Henle Latin: Third Year (Course)
      └─ Henle Latin: Fourth Year (Course)
```

## Key Tables

### skill_tree_nodes
- **Courses** are nodes where `parent_id` points to a skill node
- **Skills** are nodes where `parent_id` points to a category node
- **Categories** are nodes where `parent_id` is NULL or points to root

### learning_paths
- Collections of courses that users can follow
- Can include courses from different skill areas
- Example: "Complete Language Program" could include Latin, Spanish, and linguistics courses

### learning_path_courses
- Junction table linking learning paths to course nodes
- Fields:
  - `learning_path_id`: References learning_paths
  - `course_id`: References skill_tree_nodes (course nodes)
  - `sequence_number`: Order in the learning path
  - `is_required`: Whether course is mandatory
  - `unlock_after_course_id`: Prerequisites

### user_module_progress
- Tracks user progress through courses
- `module_id` references the course node ID in skill_tree_nodes

## Benefits of This Structure

1. **Simplicity**: No need for separate courses table
2. **Consistency**: Uses existing skill tree hierarchy
3. **Flexibility**: Learning paths can combine courses from any skills
4. **Clear Organization**: Natural parent-child relationships
5. **Existing Infrastructure**: Leverages current permissions, queries, and UI

## SQL to Set Up Latin Courses

Execute `scripts/fix_latin_courses_as_nodes.sql` to:
1. Create course nodes under Latin Language skill
2. Fix orphaned references in learning_path_courses
3. Create helpful views for querying

## Querying Courses

### Find all courses for a skill:
```sql
SELECT * FROM skill_tree_nodes 
WHERE parent_id = '[skill_node_id]'
ORDER BY display_order;
```

### Find all courses in a learning path:
```sql
SELECT stn.*, lpc.sequence_number 
FROM learning_path_courses lpc
JOIN skill_tree_nodes stn ON lpc.course_id = stn.id
WHERE lpc.learning_path_id = '[path_id]'
ORDER BY lpc.sequence_number;
```

### Get course with its skill:
```sql
SELECT 
  course.name as course_name,
  skill.name as skill_name
FROM skill_tree_nodes course
JOIN skill_tree_nodes skill ON course.parent_id = skill.id
WHERE course.id = '[course_id]';
```

## Important Notes

- Each course MUST have a `parent_id` pointing to a skill node
- Skills are identified by having a parent that is a category
- The same course node can be referenced by multiple learning paths
- Course content is stored in `learning_content` table, referenced via `learning_content_ids` field