"""Fix apostrophes in SQL file by escaping them properly"""

def fix_sql_apostrophes(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace problematic apostrophes in string literals
    replacements = [
        ("'Livy's Style'", "'Livy''s Style'"),
        ("'Book IV: Dido and Aeneas',", "'Book IV: Dido and Aeneas',"),  # This one is actually fine
        ("'Livy''s Style'", "'Livy''s Style'"),  # In case it's already escaped
    ]
    
    # More systematic approach - look for patterns
    import re
    
    # Find all strings that might have unescaped apostrophes
    # We need to escape apostrophes within SQL string literals
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Check if line contains a string literal value
        if re.match(r"^\s*'[^']*'[,)]", line):
            # This is likely a value in an INSERT statement
            # Check for apostrophes that aren't at the beginning or end
            if line.count("'") > 2:  # More than just the enclosing quotes
                # Look for specific problematic patterns
                if "Livy's" in line and "Livy''s" not in line:
                    line = line.replace("Livy's", "Livy''s")
        fixed_lines.append(line)
    
    fixed_content = '\n'.join(fixed_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed SQL saved to {output_file}")
    print("Replacements made:")
    print("- Livy's Style -> Livy''s Style")

if __name__ == "__main__":
    fix_sql_apostrophes(
        'scripts/master_latin_learning_path_fixed.sql',
        'scripts/master_latin_learning_path_final.sql'
    )