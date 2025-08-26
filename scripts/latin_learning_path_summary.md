# Complete Henle Latin Learning Path

## Overview
- **Path Name**: Complete Henle Latin Program  
- **Total Duration**: 420 hours
- **Number of Courses**: 5
- **Progression**: Sequential from Beginner to Advanced

## Course Structure

### 1. Henle Latin First Year (Already in DB)
- **Level**: Beginner
- **Duration**: 60 hours
- **Chapters**: 5
- **Key Topics**:
  - First and Second Declensions
  - Basic verb conjugations
  - Nominative and Accusative cases
  - Basic vocabulary
  - Simple sentences

### 2. Henle Latin Second Year
- **Level**: Intermediate
- **Duration**: 80 hours
- **Chapters**: 5
- **Key Topics**:
  - Subjunctive mood
  - Participles
  - Indirect discourse
  - Caesar's De Bello Gallico readings
  - Advanced syntax

### 3. Henle Latin Third Year
- **Level**: Advanced
- **Duration**: 100 hours
- **Chapters**: 5
- **Key Topics**:
  - Cicero's Catiline Orations
  - Advanced subjunctive uses
  - Introduction to Virgil's Aeneid
  - Prose composition
  - Livy's histories

### 4. Henle Latin Fourth Year
- **Level**: Advanced
- **Duration**: 120 hours
- **Chapters**: 5
- **Key Topics**:
  - Virgil's Aeneid Books I-VI
  - Horace's Odes
  - Ovid's Metamorphoses
  - Tacitus's Annales
  - Advanced poetry analysis

### 5. Henle Latin Grammar (Reference)
- **Level**: Reference/Optional
- **Duration**: 40 hours
- **Chapters**: 5
- **Key Topics**:
  - Complete declension system
  - Complete conjugation system
  - Comprehensive syntax reference
  - Irregular forms
  - Advanced grammatical topics

## Database Changes

### New Tables to Create:
1. `learning_paths` - Main learning path definitions
2. `learning_path_courses` - Links courses to paths with sequence
3. `user_learning_path_progress` - User progress tracking

### Data to Insert:
1. 4 new Latin courses (Second Year through Grammar)
2. 1 learning path linking all 5 courses
3. 25 new chapters (5 per new course)
4. 75 new learning content sections

## Files Generated:
- `create_learning_paths_tables.sql` - Table structure
- `create_complete_henle_latin_path.sql` - All course and path data
- Learning Path ID: `97765ae5-4d73-43eb-8072-6b110a8c6a8a`

## Next Steps:
1. Review the generated SQL files
2. Execute `create_learning_paths_tables.sql` to create tables
3. Execute `create_complete_henle_latin_path.sql` to insert data
4. Update UI to display learning paths