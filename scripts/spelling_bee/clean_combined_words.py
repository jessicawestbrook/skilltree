#!/usr/bin/env python3
"""
Clean up combined words in the extracted word list
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple, Set

def load_common_word_list() -> Set[str]:
    """Load a set of common English words to help identify word boundaries"""
    # Common spelling bee words and patterns to help identify splits
    common_words = {
        'abandon', 'beguile', 'able', 'about', 'above', 'absence', 'absolute', 'absorb',
        'abstract', 'accept', 'access', 'accident', 'accompany', 'accomplish', 'accord',
        'account', 'accurate', 'achieve', 'acquire', 'across', 'action', 'active', 'actual',
        'address', 'adequate', 'adjust', 'admit', 'advance', 'advantage', 'adventure', 'advice',
        'affect', 'afford', 'afraid', 'against', 'agency', 'agent', 'agree', 'ahead', 'allow',
        'almost', 'alone', 'along', 'already', 'although', 'always', 'among', 'amount',
        'analysis', 'analyze', 'ancient', 'animal', 'annual', 'another', 'answer', 'anyone',
        'anything', 'appear', 'apply', 'approach', 'appropriate', 'area', 'argue', 'around',
        'arrange', 'article', 'artist', 'aside', 'assert', 'assign', 'assist', 'assume',
        'attack', 'attempt', 'attend', 'attention', 'attitude', 'attract', 'audience', 'author',
        'authority', 'available', 'avoid', 'aware', 'balance', 'basis', 'battle', 'beauty',
        'become', 'before', 'begin', 'behavior', 'behind', 'believe', 'benefit', 'between',
        'beyond', 'billion', 'black', 'blue', 'board', 'break', 'brief', 'bring', 'broad',
        'brother', 'budget', 'build', 'business', 'camera', 'campaign', 'cancer', 'candidate',
        'capacity', 'capital', 'career', 'careful', 'carry', 'catch', 'cause', 'central',
        'century', 'certain', 'chair', 'challenge', 'chance', 'change', 'character', 'charge',
        'check', 'chemical', 'choice', 'choose', 'church', 'citizen', 'civil', 'claim',
        'class', 'clear', 'clearly', 'client', 'close', 'coach', 'collection', 'college',
        'color', 'column', 'combination', 'combine', 'commercial', 'commission', 'commit',
        'common', 'community', 'company', 'compare', 'competition', 'complete', 'computer',
        'concept', 'concern', 'condition', 'conference', 'congress', 'consider', 'consumer',
        'contain', 'content', 'continue', 'contract', 'control', 'conversation', 'corner',
        'corporate', 'correct', 'could', 'council', 'count', 'country', 'couple', 'course',
        'court', 'cover', 'create', 'crime', 'cultural', 'culture', 'current', 'customer',
        'daughter', 'death', 'debate', 'decade', 'decide', 'decision', 'deep', 'defense',
        'degree', 'democratic', 'describe', 'design', 'despite', 'detail', 'determine',
        'develop', 'development', 'difference', 'different', 'difficult', 'dinner', 'direction',
        'director', 'discover', 'discuss', 'disease', 'door', 'down', 'draw', 'dream',
        'drive', 'drop', 'drug', 'during', 'each', 'early', 'east', 'easy', 'economic',
        'economy', 'edge', 'education', 'effect', 'effective', 'effort', 'eight', 'either',
        'election', 'electric', 'electronic', 'element', 'else', 'employee', 'energy',
        'engage', 'enough', 'enter', 'entire', 'environment', 'environmental', 'equal',
        'especially', 'establish', 'even', 'evening', 'event', 'ever', 'every', 'everyone',
        'everything', 'evidence', 'exactly', 'example', 'executive', 'exist', 'expect',
        'experience', 'expert', 'explain', 'face', 'fact', 'factor', 'fail', 'fall',
        'family', 'father', 'fear', 'federal', 'feel', 'feeling', 'field', 'fight',
        'figure', 'fill', 'film', 'final', 'finally', 'financial', 'find', 'fine',
        'finger', 'finish', 'fire', 'firm', 'first', 'fish', 'five', 'floor',
        'focus', 'follow', 'food', 'foot', 'force', 'foreign', 'forget', 'form',
        'former', 'forward', 'four', 'free', 'friend', 'from', 'front', 'full',
        'fund', 'future', 'game', 'garden', 'general', 'generation', 'girl', 'give',
        'glass', 'goal', 'good', 'government', 'great', 'green', 'ground', 'group',
        'grow', 'growth', 'guess', 'gun', 'hair', 'half', 'hand', 'hang',
        'happen', 'happy', 'hard', 'have', 'head', 'health', 'hear', 'heart',
        'heat', 'heavy', 'help', 'here', 'high', 'himself', 'history', 'hold',
        'home', 'hope', 'hospital', 'hotel', 'hour', 'house', 'however', 'huge',
        'human', 'hundred', 'husband', 'idea', 'identify', 'image', 'imagine', 'impact',
        'important', 'improve', 'include', 'including', 'increase', 'indeed', 'indicate',
        'individual', 'industry', 'information', 'inside', 'instead', 'institution', 'interest',
        'interesting', 'international', 'interview', 'into', 'investment', 'involve', 'issue',
        'item', 'itself', 'join', 'just', 'keep', 'kill', 'kind', 'kitchen',
        'know', 'knowledge', 'land', 'language', 'large', 'last', 'late', 'later',
        'laugh', 'lawyer', 'lead', 'leader', 'learn', 'least', 'leave', 'left',
        'legal', 'less', 'letter', 'level', 'life', 'light', 'like', 'likely',
        'line', 'list', 'listen', 'little', 'live', 'local', 'long', 'look',
        'lose', 'loss', 'love', 'machine', 'magazine', 'main', 'maintain', 'major',
        'make', 'management', 'manager', 'many', 'market', 'marriage', 'material', 'matter',
        'maybe', 'mean', 'measure', 'media', 'medical', 'meet', 'meeting', 'member',
        'memory', 'mention', 'message', 'method', 'middle', 'might', 'military', 'million',
        'mind', 'minute', 'miss', 'mission', 'model', 'modern', 'moment', 'money',
        'month', 'more', 'morning', 'most', 'mother', 'mouth', 'move', 'movement',
        'movie', 'much', 'music', 'must', 'name', 'nation', 'national', 'natural',
        'nature', 'near', 'nearly', 'necessary', 'need', 'network', 'never', 'news',
        'newspaper', 'next', 'nice', 'night', 'none', 'north', 'note', 'nothing',
        'notice', 'number', 'occur', 'offer', 'office', 'officer', 'official', 'often',
        'once', 'only', 'onto', 'open', 'operation', 'opportunity', 'option', 'order',
        'organization', 'other', 'others', 'outside', 'over', 'own', 'owner', 'page',
        'pain', 'painting', 'paper', 'parent', 'part', 'participant', 'particular', 'particularly',
        'partner', 'party', 'pass', 'past', 'patient', 'pattern', 'peace', 'people',
        'perform', 'performance', 'perhaps', 'period', 'person', 'personal', 'phone', 'physical',
        'pick', 'picture', 'piece', 'place', 'plan', 'plant', 'play', 'player',
        'please', 'point', 'police', 'policy', 'political', 'politics', 'poor', 'popular',
        'population', 'position', 'positive', 'possible', 'power', 'practice', 'prepare', 'present',
        'president', 'pressure', 'pretty', 'prevent', 'price', 'private', 'probably', 'problem',
        'process', 'produce', 'product', 'production', 'professional', 'program', 'project', 'property',
        'protect', 'prove', 'provide', 'public', 'pull', 'purpose', 'push', 'quality',
        'question', 'quickly', 'quite', 'race', 'radio', 'raise', 'range', 'rate',
        'rather', 'reach', 'read', 'ready', 'real', 'reality', 'realize', 'really',
        'reason', 'receive', 'recent', 'recognize', 'record', 'reduce', 'reflect', 'region',
        'relate', 'relationship', 'religious', 'remain', 'remember', 'remove', 'report', 'represent',
        'republican', 'require', 'research', 'resource', 'respond', 'response', 'responsibility', 'rest',
        'result', 'return', 'reveal', 'rich', 'right', 'rise', 'risk', 'road',
        'rock', 'role', 'room', 'rule', 'safe', 'same', 'save', 'scene',
        'school', 'science', 'scientist', 'score', 'sea', 'season', 'seat', 'second',
        'section', 'security', 'seek', 'seem', 'sell', 'send', 'senior', 'sense',
        'series', 'serious', 'serve', 'service', 'seven', 'several', 'share', 'shoot',
        'short', 'shot', 'should', 'shoulder', 'show', 'side', 'sign', 'significant',
        'similar', 'simple', 'simply', 'since', 'sing', 'single', 'sister', 'site',
        'situation', 'size', 'skill', 'skin', 'small', 'smile', 'social', 'society',
        'soldier', 'some', 'somebody', 'someone', 'something', 'sometimes', 'song', 'soon',
        'sort', 'sound', 'source', 'south', 'southern', 'space', 'speak', 'special',
        'specific', 'speech', 'spend', 'sport', 'spring', 'staff', 'stage', 'stand',
        'standard', 'star', 'start', 'state', 'statement', 'station', 'stay', 'step',
        'still', 'stock', 'stop', 'store', 'story', 'strategy', 'street', 'strong',
        'structure', 'student', 'study', 'stuff', 'style', 'subject', 'success', 'successful',
        'such', 'suddenly', 'suffer', 'suggest', 'summer', 'support', 'sure', 'surface',
        'system', 'table', 'take', 'talk', 'task', 'teach', 'teacher', 'team',
        'technology', 'television', 'tell', 'tend', 'term', 'test', 'than', 'thank',
        'that', 'their', 'them', 'themselves', 'then', 'theory', 'there', 'these',
        'they', 'thing', 'think', 'third', 'this', 'those', 'though', 'thought',
        'thousand', 'threat', 'three', 'through', 'throughout', 'throw', 'thus', 'time',
        'today', 'together', 'tonight', 'total', 'tough', 'toward', 'town', 'trade',
        'traditional', 'training', 'travel', 'treat', 'treatment', 'tree', 'trial', 'trip',
        'trouble', 'true', 'truth', 'turn', 'type', 'under', 'understand', 'union',
        'unit', 'united', 'university', 'unless', 'until', 'upon', 'used', 'useful',
        'user', 'usually', 'value', 'various', 'very', 'victim', 'view', 'violence',
        'visit', 'voice', 'wait', 'walk', 'wall', 'want', 'watch', 'water',
        'weapon', 'wear', 'week', 'weight', 'well', 'west', 'western', 'what',
        'whatever', 'when', 'where', 'whether', 'which', 'while', 'white', 'whole',
        'whom', 'whose', 'wide', 'wife', 'will', 'wind', 'window', 'wish',
        'with', 'within', 'without', 'woman', 'wonder', 'word', 'work', 'worker',
        'working', 'world', 'worry', 'would', 'write', 'writer', 'wrong', 'yard',
        'year', 'young', 'your', 'yourself'
    }
    return common_words

def find_word_splits(combined_word: str, common_words: Set[str]) -> List[Tuple[str, ...]]:
    """Find possible ways to split a combined word"""
    if len(combined_word) < 6:  # Too short to be combined
        return []
    
    possible_splits = []
    
    # Try different split points
    for i in range(3, len(combined_word) - 2):  # Minimum 3 chars per word
        left = combined_word[:i]
        right = combined_word[i:]
        
        # Check if both parts could be valid words
        if (left in common_words and len(right) >= 3) or \
           (right in common_words and len(left) >= 3) or \
           (len(left) >= 4 and len(right) >= 4):  # Both reasonable length
            possible_splits.append((left, right))
        
        # Try three-way splits for very long words
        if len(combined_word) > 12:
            for j in range(i + 3, len(combined_word) - 2):
                middle = combined_word[i:j]
                right = combined_word[j:]
                if len(left) >= 3 and len(middle) >= 3 and len(right) >= 3:
                    possible_splits.append((left, middle, right))
    
    return possible_splits

def analyze_combined_words(csv_file: Path) -> List[Tuple[str, List[Tuple[str, ...]]]]:
    """Analyze the CSV to find words that might be combined"""
    common_words = load_common_word_list()
    potential_combined = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word']
            
            # Look for potential combined words
            if len(word) > 8:  # Long enough to potentially be combined
                splits = find_word_splits(word, common_words)
                if splits:
                    potential_combined.append((word, splits))
    
    return potential_combined

def generate_word_cleaning_report(csv_file: Path, output_file: Path):
    """Generate a report of words that need cleaning"""
    combined_words = analyze_combined_words(csv_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Spelling Bee Combined Words Analysis\n")
        f.write("=" * 50 + "\n\n")
        
        if not combined_words:
            f.write("No obvious combined words found.\n")
            return
        
        f.write(f"Found {len(combined_words)} potentially combined words:\n\n")
        
        for word, splits in combined_words:
            f.write(f"Word: {word}\n")
            f.write("Possible splits:\n")
            for split in splits[:3]:  # Show top 3 possibilities
                f.write(f"  → {' + '.join(split)}\n")
            f.write("-" * 30 + "\n")
        
        f.write(f"\nRECOMMENDATION:\n")
        f.write("Review these words manually and determine which should be split.\n")
        f.write("Most obvious cases like 'abnegationbeguile' should be split into separate words.\n")

def main():
    """Main function"""
    output_folder = Path("output")
    csv_file = output_folder / "extracted_words_for_review.csv"
    report_file = output_folder / "combined_words_analysis.txt"
    
    if not csv_file.exists():
        print(f"Error: {csv_file} not found. Run word extraction first.")
        return
    
    print("Analyzing combined words...")
    generate_word_cleaning_report(csv_file, report_file)
    
    print(f"Analysis complete! Check: {report_file}")

if __name__ == "__main__":
    main()