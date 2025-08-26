"""
Apply slug fields to database tables
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
    
    for path in result.data:
        slug = generate_slug(path['name'])
        print(f"  {path['name']} -> {slug}")
        
        # Update with slug
        supabase.table('learning_paths').update({
            'slug': slug
        }).eq('id', path['id']).execute()
    
    print(f"Updated {len(result.data)} learning paths\n")

def update_language_courses():
    """Add slugs to language_courses table"""
    print("Updating language_courses table...")
    
    # Get all courses
    result = supabase.table('language_courses').select('id, name').execute()
    
    for course in result.data:
        slug = generate_slug(course['name'])
        print(f"  {course['name']} -> {slug}")
        
        # Update with slug
        supabase.table('language_courses').update({
            'slug': slug
        }).eq('id', course['id']).execute()
    
    print(f"Updated {len(result.data)} courses\n")

def verify_slugs():
    """Verify slugs were added correctly"""
    print("Verifying slugs...")
    
    # Check learning paths
    result = supabase.table('learning_paths').select('name, slug').limit(5).execute()
    print("\nLearning Paths:")
    for path in result.data:
        print(f"  {path['name']}: /{path.get('slug', 'NO SLUG')}")
    
    # Check courses
    result = supabase.table('language_courses').select('name, slug').limit(5).execute()
    print("\nLanguage Courses:")
    for course in result.data:
        print(f"  {course['name']}: /{course.get('slug', 'NO SLUG')}")

if __name__ == "__main__":
    print("Adding slug fields to database tables...\n")
    
    try:
        update_learning_paths()
        update_language_courses()
        verify_slugs()
        
        print("\n✅ Successfully added slugs to all tables!")
        print("\nURL examples:")
        print("  /learning-paths/complete-henle-latin-program")
        print("  /course/henle-latin-first-year/overview")
        print("  /course/henle-latin-first-year")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nYou may need to manually run the SQL script in Supabase:")
        print("  scripts/add_slug_fields.sql")