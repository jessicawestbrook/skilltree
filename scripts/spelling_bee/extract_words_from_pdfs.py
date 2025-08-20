import PyPDF2
import csv
import re
import os
from typing import List, Dict, Set
from pathlib import Path

def extract_words_from_pdf(pdf_path: str) -> Dict[str, any]:
    """Extract spelling words from a PDF file."""
    words_with_source_difficulty = {}
    source_name = Path(pdf_path).stem
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            full_text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text += text + "\n"
            
            # Extract words and preserve any difficulty labels from the source
            words = extract_spelling_words(full_text)
            
            for word, source_difficulty in words.items():
                words_with_source_difficulty[word] = source_difficulty
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return {"words": {}, "source": source_name}
    
    return {
        "words": words_with_source_difficulty,
        "source": source_name
    }

def extract_spelling_words(text: str) -> Dict[str, str]:
    """Extract spelling words from PDF text, preserving any source difficulty labels."""
    words = {}
    
    # Clean up text
    lines = text.split('\n')
    
    current_difficulty = None
    
    for line in lines:
        line = line.strip()
        
        # Look for Scripps difficulty indicators (ONE BEE, TWO BEE, THREE BEE)
        bee_match = re.search(r'(ONE BEE|TWO BEE|THREE BEE)', line, re.IGNORECASE)
        if bee_match:
            current_difficulty = bee_match.group(1).upper()
        
        # Extract words - looking for standalone words that are likely spelling bee words
        # Typically these are single words on a line or in a list format
        word_pattern = r'^([a-z]+)$'
        match = re.match(word_pattern, line, re.IGNORECASE)
        
        if match:
            word = match.group(1).lower().strip()
            # Filter out very common words and very short words
            if len(word) >= 4 and not is_common_word(word):
                # Store with the difficulty label if we found one
                words[word] = current_difficulty if current_difficulty else ""
    
    return words

def is_common_word(word: str) -> bool:
    """Filter out common English words that are unlikely to be spelling bee words."""
    common_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'would', 
        'her', 'there', 'their', 'what', 'about', 'out', 'who', 'get',
        'which', 'when', 'make', 'can', 'like', 'time', 'just', 'him',
        'know', 'take', 'into', 'year', 'your', 'some', 'could', 'them',
        'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come',
        'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two',
        'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new',
        'want', 'because', 'any', 'these', 'give', 'day', 'most', 'word',
        'words', 'page', 'spelling', 'bee', 'champions', 'national', 'scripps',
        'round', 'level', 'study', 'list', 'grade', 'school', 'test', 'with',
        'this', 'that', 'from', 'have', 'been', 'will', 'more', 'very'
    }
    return word in common_words

def clean_and_deduplicate(all_data: List[Dict]) -> Dict:
    """Clean extracted words and remove duplicates, preserving source information."""
    unique_words = {}
    
    for data in all_data:
        for word, source_difficulty in data["words"].items():
            # Clean word - remove any remaining non-alphabetic characters
            cleaned_word = re.sub(r'[^a-z]', '', word.lower())
            
            if cleaned_word and len(cleaned_word) >= 3:
                if cleaned_word not in unique_words:
                    unique_words[cleaned_word] = {
                        "sources": [data["source"]],
                        "source_difficulties": [source_difficulty] if source_difficulty else []
                    }
                else:
                    if data["source"] not in unique_words[cleaned_word]["sources"]:
                        unique_words[cleaned_word]["sources"].append(data["source"])
                    if source_difficulty and source_difficulty not in unique_words[cleaned_word]["source_difficulties"]:
                        unique_words[cleaned_word]["source_difficulties"].append(source_difficulty)
    
    return unique_words

def save_to_csv(words_data: Dict, output_path: str):
    """Save the processed words to a CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        
        # Write header
        writer.writerow(['word', 'source_names', 'source_difficulties', 'original_source', 'source_access_date'])
        
        for word, data in sorted(words_data.items()):
            # Format source_names as PostgreSQL array format: {"item1","item2"}
            source_names_array = '{"' + '","'.join(data['sources']) + '"}'
            
            # Format source_difficulties as PostgreSQL array format: {"item1","item2"}
            source_difficulties_array = '{"' + '","'.join(data['source_difficulties']) + '"}' if data['source_difficulties'] else '{}'
            
            # Write row - arrays and date as strings, will be quoted properly by csv module
            writer.writerow([
                word,
                source_names_array,
                source_difficulties_array,
                'Scripps National Spelling Bee website',
                '2025-08-18'
            ])

def main():
    """Main function to process all PDF files."""
    input_dir = r"C:\Users\jessi\Projects\skilltree2\src\data\spelling_bee\input"
    output_file = r"C:\Users\jessi\Projects\skilltree2\src\data\spelling_bee\output\1_word_list.csv"
    
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    all_extracted_data = []
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        print(f"Processing: {pdf_file}")
        
        extracted_data = extract_words_from_pdf(pdf_path)
        all_extracted_data.append(extracted_data)
        print(f"  Extracted {len(extracted_data['words'])} potential words")
    
    # Clean and deduplicate
    print("\nCleaning and deduplicating words...")
    unique_words = clean_and_deduplicate(all_extracted_data)
    print(f"Total unique words after cleaning: {len(unique_words)}")
    
    # Save to CSV
    print(f"\nSaving to CSV: {output_file}")
    save_to_csv(unique_words, output_file)
    print("Done!")

if __name__ == "__main__":
    main()