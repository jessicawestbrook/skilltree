"""
Populate slug fields in database tables
"""
import os
import re
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

def generate_slug(text):
    """Generate a URL-friendly slug from text"""
    # Convert to lowercase
    slug = text.lower()
    # Remove special characters except spaces and hyphens
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Replace multiple hyphens with single hyphen
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def update_learning_paths():
    """Add slugs to learning_paths table"""
    print("Updating learning_paths table...")
    
    # Get all learning paths
    result = supabase.table('learning_paths').select('id, name').execute()
    
    success_count = 0
    for path in result.data:
        slug = generate_slug(path['name'])
        print(f"  {path['name']} -> {slug}")
        
        try:
            # Update with slug
            supabase.table('learning_paths').update({
                'slug': slug
            }).eq('id', path['id']).execute()
            success_count += 1
        except Exception as e:
            print(f"    ERROR: Could not update - {str(e)[:50]}")
    
    print(f"Successfully updated {success_count}/{len(result.data)} learning paths\n")
    return success_count == len(result.data)

def update_language_courses():
    """Add slugs to language_courses table"""
    print("Updating language_courses table...")
    
    # Get all courses
    result = supabase.table('language_courses').select('id, name').execute()
    
    success_count = 0
    for course in result.data:
        slug = generate_slug(course['name'])
        print(f"  {course['name']} -> {slug}")
        
        try:
            # Update with slug
            supabase.table('language_courses').update({
                'slug': slug
            }).eq('id', course['id']).execute()
            success_count += 1
        except Exception as e:
            print(f"    ERROR: Could not update - {str(e)[:50]}")
    
    print(f"Successfully updated {success_count}/{len(result.data)} courses\n")
    return success_count == len(result.data)

def verify_slugs():
    """Verify slugs were added correctly"""
    print("\nVerifying slugs...")
    
    # Check learning paths
    result = supabase.table('learning_paths').select('name, slug').execute()
    print(f"\nLearning Paths ({len(result.data)} total):")
    for i, path in enumerate(result.data[:3]):
        slug = path.get('slug', 'NO SLUG')
        print(f"  {path['name']}: /learning-paths/{slug}")
    if len(result.data) > 3:
        print(f"  ... and {len(result.data) - 3} more")
    
    # Check courses
    result = supabase.table('language_courses').select('name, slug').execute()
    print(f"\nLanguage Courses ({len(result.data)} total):")
    for i, course in enumerate(result.data[:5]):
        slug = course.get('slug', 'NO SLUG')
        print(f"  {course['name']}: /course/{slug}")
    if len(result.data) > 5:
        print(f"  ... and {len(result.data) - 5} more")

if __name__ == "__main__":
    print("Populating slug fields in database tables...\n")
    
    paths_success = update_learning_paths()
    courses_success = update_language_courses()
    
    if paths_success and courses_success:
        verify_slugs()
        print("\n✓ Successfully added slugs to all tables!")
        print("\nNew URL structure:")
        print("  /learning-paths/complete-henle-latin-program")
        print("  /course/henle-latin-first-year/overview")
        print("  /course/henle-latin-first-year")
    else:
        print("\n! Some updates failed. Please check the errors above.")
        print("\nMake sure you've run the SQL to add slug columns first:")
        print("  Run scripts/add_slug_columns_only.sql in Supabase SQL Editor")