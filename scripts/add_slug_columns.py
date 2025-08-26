"""
Add slug columns to database tables
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

print("IMPORTANT: You need to add the slug columns to the database first.")
print("\nPlease run this SQL in your Supabase SQL Editor:")
print("=" * 60)

sql_script = """
-- Add slug column to learning_paths
ALTER TABLE learning_paths 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Add slug column to language_courses
ALTER TABLE language_courses 
ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_learning_paths_slug ON learning_paths(slug);
CREATE INDEX IF NOT EXISTS idx_language_courses_slug ON language_courses(slug);
"""

print(sql_script)
print("=" * 60)
print("\nAfter running the SQL above, run: python scripts/populate_slugs.py")

# Also save to a file for easy copying
with open('scripts/add_slug_columns_only.sql', 'w') as f:
    f.write(sql_script)
print("\nSQL also saved to: scripts/add_slug_columns_only.sql")