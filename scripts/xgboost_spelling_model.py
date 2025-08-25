"""
XGBoost model to predict spelling difficulty (1-5 scale)
Uses real word frequency data and linguistic features
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Install required packages if needed
packages = ['xgboost', 'scikit-learn', 'wordfreq', 'supabase', 'pandas', 'numpy']
for package in packages:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from wordfreq import zipf_frequency
from supabase import create_client

def get_supabase_client():
    """Create Supabase client"""
    url = os.getenv('REACT_APP_SUPABASE_URL')
    key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
    return create_client(url, key)

def extract_features(word, freq=None):
    """Extract features for a single word"""
    w = word.lower()
    
    # Get frequency if not provided
    if freq is None:
        freq = zipf_frequency(w, 'en')
    
    features = {
        # Frequency (MOST IMPORTANT)
        'zipf_frequency': freq,
        'is_very_common': 1 if freq >= 6 else 0,
        'is_common': 1 if 4 <= freq < 6 else 0,
        'is_uncommon': 1 if 2 <= freq < 4 else 0,
        'is_rare': 1 if freq < 2 else 0,
        
        # Length features
        'length': len(w),
        'length_squared': len(w) ** 2,
        'is_short': 1 if len(w) <= 4 else 0,
        'is_medium': 1 if 5 <= len(w) <= 8 else 0,
        'is_long': 1 if len(w) >= 9 else 0,
        
        # Vowel/consonant patterns
        'vowel_count': len([c for c in w if c in 'aeiou']),
        'consonant_count': len([c for c in w if c in 'bcdfghjklmnpqrstvwxyz']),
        'vowel_ratio': len([c for c in w if c in 'aeiou']) / len(w),
        'consecutive_vowels': len([i for i in range(len(w)-1) if w[i] in 'aeiou' and w[i+1] in 'aeiou']),
        'consecutive_consonants': len([i for i in range(len(w)-2) if all(c not in 'aeiou' for c in w[i:i+3])]),
        
        # Double letters
        'has_double': 1 if any(w[i] == w[i+1] for i in range(len(w)-1)) else 0,
        'double_count': sum(1 for i in range(len(w)-1) if w[i] == w[i+1]),
        
        # Silent letter patterns
        'has_silent_e': 1 if w.endswith('e') and len(w) > 2 else 0,
        'has_gh': 1 if 'gh' in w else 0,
        'has_silent_letters': 1 if any(p in w for p in ['kn', 'gn', 'wr', 'mb', 'ps', 'pn']) else 0,
        
        # Complex patterns
        'has_ough': 1 if 'ough' in w else 0,
        'has_eigh': 1 if 'eigh' in w else 0,
        'has_augh': 1 if 'augh' in w else 0,
        'has_ph': 1 if 'ph' in w else 0,
        'has_tion': 1 if 'tion' in w else 0,
        'has_sion': 1 if 'sion' in w else 0,
        
        # Morphological
        'has_common_prefix': 1 if any(w.startswith(p) for p in ['un', 're', 'in', 'dis', 'pre', 'non']) else 0,
        'has_common_suffix': 1 if any(w.endswith(s) for s in ['ing', 'ed', 'er', 'est', 'ly', 'ness', 'ment']) else 0,
        
        # Letter frequency score (common letters = easier)
        'avg_letter_commonness': sum(zipf_frequency(c, 'en') for c in w) / len(w) if len(w) > 0 else 0,
        
        # Syllable estimate
        'syllable_count': max(1, len([c for c in w if c in 'aeiou']) - (1 if w.endswith('e') else 0))
    }
    
    return features

def prepare_data():
    """Load and prepare training data"""
    print("=== PREPARING DATA ===\n")
    
    supabase = get_supabase_client()
    
    # Get words with bee ratings
    print("Loading words with bee ratings...")
    response = supabase.table('spelling_words').select(
        'word, source_difficulty, frequency'
    ).filter('source_difficulty', 'in', '("One Bee","Two Bee","Three Bee")').execute()
    
    words_data = response.data
    print(f"Loaded {len(words_data)} words\n")
    
    # Create feature matrix
    print("Extracting features...")
    X = []
    y = []
    words = []
    
    for word_data in words_data:
        # Skip words with multiple ratings
        if ';' in word_data['source_difficulty']:
            continue
            
        features = extract_features(word_data['word'], word_data.get('frequency'))
        X.append(list(features.values()))
        
        # Map bee rating to 1-5 scale
        # We'll use a distribution that spreads across 1-5
        if word_data['source_difficulty'] == 'One Bee':
            # One Bee -> mostly 1-2
            if features['zipf_frequency'] >= 5:  # Very common
                y.append(1)
            else:
                y.append(2)
        elif word_data['source_difficulty'] == 'Two Bee':
            # Two Bee -> mostly 3
            y.append(3)
        else:  # Three Bee
            # Three Bee -> mostly 4-5
            if features['length'] >= 10 or features['has_ough'] or features['has_eigh']:
                y.append(5)
            else:
                y.append(4)
        
        words.append(word_data['word'])
    
    feature_names = list(extract_features('test').keys())
    
    return np.array(X), np.array(y), words, feature_names

def train_xgboost_model():
    """Train XGBoost model"""
    print("=== TRAINING XGBOOST MODEL ===\n")
    
    # Prepare data
    X, y, words, feature_names = prepare_data()
    
    print(f"Features: {len(feature_names)}")
    print(f"Samples: {len(X)}")
    print(f"Target distribution: {dict(zip(*np.unique(y, return_counts=True)))}\n")
    
    # Split data
    X_train, X_test, y_train, y_test, words_train, words_test = train_test_split(
        X, y, words, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train XGBoost
    print("Training XGBoost...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        objective='multi:softprob',
        num_class=6,  # 0-5 (we use 1-5 but need to account for 0-indexing)
        random_state=42,
        use_label_encoder=False
    )
    
    # Adjust labels for 0-indexing
    model.fit(X_train, y_train - 1)
    
    # Predict
    y_pred = model.predict(X_test) + 1  # Convert back to 1-5
    
    # Evaluate
    print("\n=== MODEL PERFORMANCE ===\n")
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2%}\n")
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print("Actual\\Predicted  1    2    3    4    5")
    for i, row in enumerate(cm, 1):
        print(f"Level {i}:      {str(row).replace('[', '').replace(']', '')}")
    
    # Feature importance
    print("\n=== TOP 10 MOST IMPORTANT FEATURES ===\n")
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1][:10]
    
    for i, idx in enumerate(indices, 1):
        print(f"{i}. {feature_names[idx]}: {importance[idx]:.3f}")
    
    # Cross-validation
    print("\n=== CROSS-VALIDATION ===\n")
    cv_scores = cross_val_score(model, X, y - 1, cv=5, scoring='accuracy')
    print(f"CV Accuracy: {cv_scores.mean():.2%} (+/- {cv_scores.std() * 2:.2%})")
    
    # Save model
    model.save_model('xgboost_spelling_model.json')
    print("\nModel saved to xgboost_spelling_model.json")
    
    # Save feature names
    with open('feature_names.json', 'w') as f:
        json.dump(feature_names, f)
    print("Feature names saved to feature_names.json")
    
    return model, feature_names

def predict_all_words(model, feature_names):
    """Generate predictions for all words in database"""
    print("\n=== GENERATING PREDICTIONS FOR ALL WORDS ===\n")
    
    supabase = get_supabase_client()
    
    # Get all words
    response = supabase.table('spelling_words').select('id, word, frequency').execute()
    all_words = response.data
    
    print(f"Generating predictions for {len(all_words)} words...")
    
    predictions = []
    for word_data in all_words:
        features = extract_features(word_data['word'], word_data.get('frequency'))
        X = np.array([list(features.values())])
        
        # Predict
        pred = model.predict(X)[0] + 1  # Convert from 0-indexed to 1-5
        
        predictions.append({
            'id': word_data['id'],
            'word': word_data['word'],
            'predicted_difficulty': int(pred)
        })
    
    # Save predictions
    df = pd.DataFrame(predictions)
    df.to_csv('spelling_difficulty_predictions.csv', index=False)
    print(f"Predictions saved to spelling_difficulty_predictions.csv")
    
    # Show distribution
    print("\nPredicted distribution:")
    for level in range(1, 6):
        count = sum(1 for p in predictions if p['predicted_difficulty'] == level)
        pct = (count / len(predictions)) * 100
        print(f"  Level {level}: {count} words ({pct:.1f}%)")
    
    return predictions

def generate_update_sql(predictions):
    """Generate SQL to update database"""
    print("\n=== GENERATING UPDATE SQL ===\n")
    
    sql = """-- Update spelling_difficulty_level using XGBoost predictions
-- Model accuracy: Cross-validated accuracy reported above

-- Create backup first
CREATE TABLE IF NOT EXISTS spelling_words_bkp_xgboost AS 
SELECT * FROM spelling_words;

"""
    
    # Group by difficulty level for efficiency
    by_level = {}
    for pred in predictions:
        level = pred['predicted_difficulty']
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(pred['id'])
    
    # Generate updates
    for level in sorted(by_level.keys()):
        ids = by_level[level]
        # Split into batches
        for i in range(0, len(ids), 500):
            batch = ids[i:i+500]
            id_list = "'" + "','".join(batch) + "'"
            sql += f"\nUPDATE spelling_words SET spelling_difficulty_level = {level} WHERE id IN ({id_list});\n"
    
    # Save SQL
    with open('update_xgboost_predictions.sql', 'w') as f:
        f.write(sql)
    
    print("SQL saved to update_xgboost_predictions.sql")
    print(f"  Updates {len(predictions)} words")

if __name__ == "__main__":
    # Train model
    model, feature_names = train_xgboost_model()
    
    # Generate predictions for all words
    predictions = predict_all_words(model, feature_names)
    
    # Generate SQL
    generate_update_sql(predictions)