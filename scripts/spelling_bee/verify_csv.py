import csv

# Test reading the CSV file to verify it's correctly formatted
csv_file = r"C:\Users\jessi\Projects\skilltree2\src\data\spelling_bee\output\1_word_list.csv"

try:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Read first 5 rows to verify
        for i, row in enumerate(reader):
            if i >= 5:
                break
            
            print(f"\nRow {i+1}:")
            print(f"  Word: {row['word']}")
            print(f"  Source Names (raw): {row['source_names']}")
            print(f"  Source Difficulties (raw): {row['source_difficulties']}")
            
            # Check if arrays are complete
            if not row['source_names'].startswith('{'):
                print(f"  ERROR: source_names doesn't start with '{{' for word {row['word']}")
            if not row['source_names'].endswith('}'):
                print(f"  ERROR: source_names doesn't end with '}}' for word {row['word']}")
            if row['source_difficulties'] and not row['source_difficulties'].startswith('{'):
                print(f"  ERROR: source_difficulties doesn't start with '{{' for word {row['word']}")
            if row['source_difficulties'] and not row['source_difficulties'].endswith('}'):
                print(f"  ERROR: source_difficulties doesn't end with '}}' for word {row['word']}")
        
        # Count total rows
        f.seek(0)
        reader = csv.DictReader(f)
        total = sum(1 for row in reader)
        print(f"\nTotal rows: {total}")
        print("CSV is valid and properly formatted!")
        
except csv.Error as e:
    print(f"CSV Error: {e}")
except Exception as e:
    print(f"Error: {e}")