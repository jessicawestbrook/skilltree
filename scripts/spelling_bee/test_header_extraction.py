#!/usr/bin/env python3
"""
Test script for proper header extraction on a single PDF
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from extract_with_proper_headers import ProperHeaderExtractor
import logging

# Set up simple logging for testing
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_single_pdf():
    """Test extraction on a single PDF file"""
    extractor = ProperHeaderExtractor()
    
    # List available PDFs
    pdf_files = list(extractor.input_dir.glob("*.pdf"))
    
    if not pdf_files:
        logger.error(f"No PDF files found in {extractor.input_dir}")
        return
    
    logger.info(f"Available PDF files:")
    for i, pdf_file in enumerate(pdf_files):
        logger.info(f"  {i + 1}. {pdf_file.name}")
    
    # Test with the first PDF file
    test_pdf = pdf_files[0]
    logger.info(f"\nTesting extraction with: {test_pdf.name}")
    
    # Extract words
    words = extractor.extract_words_from_pdf(test_pdf)
    
    if words:
        logger.info(f"\n✅ Extracted {len(words)} words")
        
        # Show difficulty distribution
        difficulty_counts = {}
        for word in words:
            difficulty_counts[word.source_difficulty] = difficulty_counts.get(word.source_difficulty, 0) + 1
        
        logger.info(f"\nDifficulty Distribution:")
        for diff, count in sorted(difficulty_counts.items()):
            logger.info(f"  {diff}: {count} words")
        
        # Show first 20 words with their difficulties
        logger.info(f"\nFirst 20 extracted words:")
        for word in words[:20]:
            logger.info(f"  {word.word} -> {word.source_difficulty} (page {word.page_number})")
        
        # Show last 20 words
        if len(words) > 20:
            logger.info(f"\nLast 20 extracted words:")
            for word in words[-20:]:
                logger.info(f"  {word.word} -> {word.source_difficulty} (page {word.page_number})")
                
    else:
        logger.error("❌ No words extracted - check the extraction logic")

if __name__ == "__main__":
    test_single_pdf()