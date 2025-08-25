
// Spelling Difficulty Predictor
// Accuracy: 40.3%

function predictSpellingDifficulty(word) {
  const features = extractFeatures(word);
  const score = calculateDifficultyScore(features);
  
  // Predict bee rating
  let beePrediction;
  if (score < -1.4) {
    beePrediction = 'One Bee';
  } else if (score < 6.5) {
    beePrediction = 'Two Bee';
  } else {
    beePrediction = 'Three Bee';
  }
  
  // Map to 1-5 scale for adaptive learning
  let difficultyLevel;
  if (score < -0.7) {
    difficultyLevel = 1; // Very easy
  } else if (score < -1.4) {
    difficultyLevel = 2; // Easy (One Bee)
  } else if (score < 6.5) {
    difficultyLevel = 3; // Medium (Two Bee)
  } else if (score < 9.7) {
    difficultyLevel = 4; // Hard (Three Bee)
  } else {
    difficultyLevel = 5; // Very hard
  }
  
  return {
    score: score,
    beePrediction: beePrediction,
    difficultyLevel: difficultyLevel
  };
}
