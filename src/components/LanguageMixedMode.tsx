import React, { useState, useEffect, useCallback } from 'react';
import { languageCAL } from '../services/languageAdaptiveLearning';
import { useAuth } from '../contexts/AuthContext';
import {
  BeakerIcon,
  ChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  XMarkIcon,
  BookOpenIcon,
  PencilSquareIcon,
  SpeakerWaveIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline';

interface Props {
  selectedLanguage: { id: string; name: string; code: string };
  onBack: () => void;
}

interface Question {
  id: string;
  category: string;
  difficulty: number;
  question_text: string;
  question_type: string;
  options?: string[];
  correct_answer?: string;
  correct_answer_index?: number;
}

interface SessionStats {
  totalQuestions: number;
  correctAnswers: number;
  accuracy: number;
  categoryBreakdown: Map<string, { total: number; correct: number; accuracy: number }>;
}

const LanguageMixedMode: React.FC<Props> = ({ selectedLanguage, onBack }) => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<number | string | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [questionStartTime, setQuestionStartTime] = useState<number>(0);
  const [sessionStats, setSessionStats] = useState<SessionStats | null>(null);
  const [showStats, setShowStats] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadNextQuestion = useCallback(async () => {
    try {
      const question = await languageCAL.selectNextQuestion(selectedLanguage.id);
      if (question) {
        setCurrentQuestion(question);
        setSelectedAnswer(null);
        setShowResult(false);
        setQuestionStartTime(Date.now());
      } else {
        setError('No questions available');
      }
    } catch (error) {
      console.error('Error loading question:', error);
      setError('Failed to load next question');
    }
  }, [selectedLanguage.id]);

  const updateStats = useCallback(() => {
    const stats = languageCAL.getSessionStats();
    setSessionStats(stats);
  }, []);

  // Start or resume session
  useEffect(() => {
    if (!user || !selectedLanguage) return;

    const initSession = async () => {
      try {
        setLoading(true);
        await languageCAL.startSession(user.id, selectedLanguage.id);
        await loadNextQuestion();
        updateStats();
      } catch (error) {
        console.error('Error initializing CAL session:', error);
        setError('Failed to start adaptive learning session');
      } finally {
        setLoading(false);
      }
    };

    initSession();

    // Cleanup on unmount
    return () => {
      // Session remains active for resuming later
    };
  }, [user, selectedLanguage, loadNextQuestion, updateStats]);

  const handleAnswer = async () => {
    if (!currentQuestion || selectedAnswer === null) return;

    const responseTime = Date.now() - questionStartTime;
    let correct = false;

    // Check if answer is correct based on question type
    if (currentQuestion.question_type === 'translation' && currentQuestion.correct_answer) {
      correct = selectedAnswer === currentQuestion.correct_answer;
    } else if (typeof currentQuestion.correct_answer_index === 'number') {
      correct = selectedAnswer === currentQuestion.correct_answer_index;
    }

    setIsCorrect(correct);
    setShowResult(true);

    // Record the attempt
    await languageCAL.recordAttempt(
      currentQuestion.id,
      currentQuestion.category,
      correct,
      responseTime,
      currentQuestion.question_type,
      currentQuestion.difficulty
    );

    updateStats();
  };

  const handleNext = async () => {
    setLoading(true);
    await loadNextQuestion();
    setLoading(false);
  };

  const endSession = async () => {
    if (window.confirm('Are you sure you want to end this session?')) {
      await languageCAL.endSession();
      onBack();
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'vocabulary': return BookOpenIcon;
      case 'grammar': return PencilSquareIcon;
      case 'listening': return SpeakerWaveIcon;
      case 'reading': return DocumentTextIcon;
      default: return BeakerIcon;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'vocabulary': return 'text-blue-600 bg-blue-50 dark:text-blue-400 dark:bg-blue-900/20';
      case 'grammar': return 'text-green-600 bg-green-50 dark:text-green-400 dark:bg-green-900/20';
      case 'listening': return 'text-purple-600 bg-purple-50 dark:text-purple-400 dark:bg-purple-900/20';
      case 'reading': return 'text-orange-600 bg-orange-50 dark:text-orange-400 dark:bg-orange-900/20';
      default: return 'text-gray-600 bg-gray-50 dark:text-gray-400 dark:bg-gray-900/20';
    }
  };

  const getDifficultyLabel = (difficulty: number): string => {
    if (difficulty < 1) return 'Basic';
    if (difficulty < 2) return 'Elementary';
    if (difficulty < 3) return 'Intermediate';
    if (difficulty < 4) return 'Advanced';
    return 'Expert';
  };

  const getDifficultyColor = (difficulty: number): string => {
    if (difficulty < 1) return 'text-green-600';
    if (difficulty < 2) return 'text-blue-600';
    if (difficulty < 3) return 'text-yellow-600';
    if (difficulty < 4) return 'text-orange-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <ArrowPathIcon className="h-8 w-8 animate-spin mx-auto text-primary-600" />
          <p className="mt-2 text-gray-600 dark:text-gray-400">Loading adaptive learning...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 text-center">
        <p className="text-red-700 dark:text-red-400">{error}</p>
        <button
          onClick={onBack}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Go Back
        </button>
      </div>
    );
  }

  if (showStats) {
    return (
      <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <ChartBarIcon className="h-6 w-6" />
            Session Statistics
          </h3>
          <button
            onClick={() => setShowStats(false)}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {sessionStats && (
          <div className="space-y-6">
            {/* Overall Stats */}
            <div className="bg-gray-50 dark:bg-neutral-900 rounded-lg p-4">
              <h4 className="font-semibold mb-3">Overall Performance</h4>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-primary-600">
                    {sessionStats.totalQuestions}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Questions</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {sessionStats.correctAnswers}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Correct</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {sessionStats.accuracy.toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Accuracy</div>
                </div>
              </div>
            </div>

            {/* Category Breakdown */}
            <div>
              <h4 className="font-semibold mb-3">Performance by Category</h4>
              <div className="space-y-2">
                {Array.from(sessionStats.categoryBreakdown.entries()).map((entry) => {
                  const [category, stats] = entry;
                  const Icon = getCategoryIcon(category);
                  return (
                    <div key={category} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-neutral-900 rounded-lg">
                      <div className="flex items-center gap-2">
                        <Icon className="h-5 w-5 text-gray-600 dark:text-gray-400" />
                        <span className="font-medium capitalize">{category}</span>
                      </div>
                      <div className="flex items-center gap-4 text-sm">
                        <span className="text-gray-600 dark:text-gray-400">
                          {stats.correct}/{stats.total}
                        </span>
                        <span className={`font-medium ${
                          stats.accuracy >= 80 ? 'text-green-600' :
                          stats.accuracy >= 60 ? 'text-yellow-600' :
                          'text-red-600'
                        }`}>
                          {stats.accuracy.toFixed(0)}%
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={() => setShowStats(false)}
                className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                Continue Learning
              </button>
              <button
                onClick={endSession}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-700"
              >
                End Session
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-6 text-center">
        <p className="text-gray-600 dark:text-gray-400">No questions available</p>
        <button
          onClick={onBack}
          className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header with Stats Button */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <BeakerIcon className="h-6 w-6 text-primary-600" />
          <h2 className="text-lg font-semibold">Adaptive Learning</h2>
        </div>
        <div className="flex items-center gap-2">
          {sessionStats && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {sessionStats.correctAnswers}/{sessionStats.totalQuestions} correct
            </div>
          )}
          <button
            onClick={() => setShowStats(true)}
            className="p-2 text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <ChartBarIcon className="h-5 w-5" />
          </button>
          <button
            onClick={endSession}
            className="p-2 text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-6">
        {/* Question Metadata */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            {(() => {
              const Icon = getCategoryIcon(currentQuestion.category);
              return (
                <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(currentQuestion.category)}`}>
                  <Icon className="h-3 w-3" />
                  {currentQuestion.category}
                </span>
              );
            })()}
            <span className={`text-xs font-medium ${getDifficultyColor(currentQuestion.difficulty)}`}>
              {getDifficultyLabel(currentQuestion.difficulty)}
            </span>
          </div>
        </div>

        {/* Question */}
        <div className="mb-6">
          <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-4">
            {currentQuestion.question_type === 'translation' 
              ? `Translate: "${currentQuestion.question_text}"`
              : currentQuestion.question_text
            }
          </h3>

          {/* Answer Options */}
          {currentQuestion.options && (
            <div className="space-y-2">
              {currentQuestion.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => !showResult && setSelectedAnswer(index)}
                  disabled={showResult}
                  className={`w-full text-left p-3 rounded-lg border transition-all ${
                    showResult
                      ? index === currentQuestion.correct_answer_index
                        ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                        : selectedAnswer === index
                        ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                        : 'border-gray-200 dark:border-gray-700'
                      : selectedAnswer === index
                      ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                      : 'border-gray-200 dark:border-gray-700 hover:border-primary-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span>{option}</span>
                    {showResult && (
                      index === currentQuestion.correct_answer_index ? (
                        <CheckCircleIcon className="h-5 w-5 text-green-600" />
                      ) : selectedAnswer === index ? (
                        <XCircleIcon className="h-5 w-5 text-red-600" />
                      ) : null
                    )}
                  </div>
                </button>
              ))}
            </div>
          )}

          {/* Text Input for Translation */}
          {currentQuestion.question_type === 'translation' && currentQuestion.correct_answer && (
            <div className="space-y-2">
              {/* For now, show as multiple choice */}
              {(() => {
                const options = currentQuestion.options || [currentQuestion.correct_answer];
                return options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => !showResult && setSelectedAnswer(option)}
                    disabled={showResult}
                    className={`w-full text-left p-3 rounded-lg border transition-all ${
                      showResult
                        ? option === currentQuestion.correct_answer
                          ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                          : selectedAnswer === option
                          ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                          : 'border-gray-200 dark:border-gray-700'
                        : selectedAnswer === option
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                        : 'border-gray-200 dark:border-gray-700 hover:border-primary-300'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span>{option}</span>
                      {showResult && (
                        option === currentQuestion.correct_answer ? (
                          <CheckCircleIcon className="h-5 w-5 text-green-600" />
                        ) : selectedAnswer === option ? (
                          <XCircleIcon className="h-5 w-5 text-red-600" />
                        ) : null
                      )}
                    </div>
                  </button>
                ));
              })()}
            </div>
          )}
        </div>

        {/* Result Message */}
        {showResult && (
          <div className={`p-3 rounded-lg mb-4 ${
            isCorrect 
              ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400' 
              : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400'
          }`}>
            {isCorrect ? 'Correct! Well done!' : 'Incorrect. Keep practicing!'}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-3">
          {!showResult ? (
            <button
              onClick={handleAnswer}
              disabled={selectedAnswer === null}
              className={`flex-1 px-4 py-2 rounded-lg font-medium ${
                selectedAnswer !== null
                  ? 'bg-primary-600 text-white hover:bg-primary-700'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
              }`}
            >
              Check Answer
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700"
            >
              Next Question
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default LanguageMixedMode;