"""
Preview of the Complete Henle Latin Learning Path Structure
"""

learning_path = {
    "name": "Complete Henle Latin Program",
    "description": "Master Latin through the complete Henle Latin series",
    "total_hours": 420,
    "courses": [
        {
            "sequence": 1,
            "name": "Henle Latin First Year",
            "level": "Beginner",
            "hours": 60,
            "chapters": 5,
            "status": "Already in database",
            "topics": [
                "First and Second Declensions",
                "Basic verb conjugations",
                "Nominative and Accusative cases", 
                "Basic vocabulary",
                "Simple sentences"
            ]
        },
        {
            "sequence": 2,
            "name": "Henle Latin Second Year",
            "level": "Intermediate",
            "hours": 80,
            "chapters": 5,
            "status": "To be created",
            "topics": [
                "Subjunctive mood",
                "Participles",
                "Indirect discourse",
                "Caesar's De Bello Gallico",
                "Advanced syntax"
            ]
        },
        {
            "sequence": 3,
            "name": "Henle Latin Third Year",
            "level": "Advanced",
            "hours": 100,
            "chapters": 5,
            "status": "To be created",
            "topics": [
                "Cicero's Catiline Orations",
                "Advanced subjunctive uses",
                "Introduction to Virgil's Aeneid",
                "Prose composition",
                "Livy's histories"
            ]
        },
        {
            "sequence": 4,
            "name": "Henle Latin Fourth Year",
            "level": "Advanced",
            "hours": 120,
            "chapters": 5,
            "status": "To be created",
            "topics": [
                "Virgil's Aeneid Books I-VI",
                "Horace's Odes",
                "Ovid's Metamorphoses",
                "Tacitus's Annales",
                "Advanced poetry analysis"
            ]
        },
        {
            "sequence": 5,
            "name": "Henle Latin Grammar",
            "level": "Reference",
            "hours": 40,
            "chapters": 5,
            "status": "To be created (optional/reference)",
            "topics": [
                "Complete declension system",
                "Complete conjugation system",
                "Comprehensive syntax reference",
                "Irregular forms",
                "Advanced topics"
            ]
        }
    ]
}

def print_learning_path():
    print("\n" + "="*70)
    print("COMPLETE HENLE LATIN LEARNING PATH")
    print("="*70)
    print(f"\nPath Name: {learning_path['name']}")
    print(f"Description: {learning_path['description']}")
    print(f"Total Hours: {learning_path['total_hours']}")
    print(f"Total Courses: {len(learning_path['courses'])}")
    
    print("\n" + "-"*70)
    print("COURSE PROGRESSION:")
    print("-"*70)
    
    for course in learning_path['courses']:
        print(f"\n{course['sequence']}. {course['name']}")
        print(f"   Level: {course['level']}")
        print(f"   Duration: {course['hours']} hours")
        print(f"   Chapters: {course['chapters']}")
        print(f"   Status: {course['status']}")
        print(f"   Key Topics:")
        for topic in course['topics']:
            print(f"      • {topic}")
    
    print("\n" + "="*70)
    print("LEARNING PATH FEATURES:")
    print("="*70)
    print("✓ Sequential progression from beginner to advanced")
    print("✓ Each course unlocks after completing the previous one")
    print("✓ Grammar reference book available at any time")
    print("✓ Comprehensive coverage of Latin language and literature")
    print("✓ Includes readings from Caesar, Cicero, Virgil, Horace, Ovid, and Tacitus")
    print("✓ Progress tracking for each course and overall path")
    
    print("\n" + "="*70)
    print("DATABASE STRUCTURE:")
    print("="*70)
    print("Tables to be created/used:")
    print("1. learning_paths - Stores the main learning path")
    print("2. learning_path_courses - Links courses to the path with sequence")
    print("3. user_learning_path_progress - Tracks user progress")
    print("4. language_courses - Individual course details (some exist)")
    print("5. course_modules - Chapters within each course")
    print("6. module_content - Learning content within chapters")

if __name__ == "__main__":
    print_learning_path()