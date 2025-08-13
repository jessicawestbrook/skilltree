'use client';

import React, { useState } from 'react';
import { X, BookOpen, Brain, Trophy, ChevronRight } from 'lucide-react';
import CourseContent from './CourseContent';
// Quiz component is embedded below
import { QuizQuestion } from '@/types';

interface LearningModalProps {
  isOpen: boolean;
  onClose: () => void;
  nodeId: string;
  nodeTitle: string;
  questions: QuizQuestion[];
  onComplete: (passed: boolean, score: number) => void;
}

type LearningPhase = 'intro' | 'content' | 'quiz' | 'complete';

// Inline Quiz Component
interface QuizComponentProps {
  questions: QuizQuestion[];
  nodeTitle: string;
  onComplete: (passed: boolean, score: number) => void;
}

const QuizComponent: React.FC<QuizComponentProps> = ({ questions, nodeTitle, onComplete }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [showFeedback, setShowFeedback] = useState(false);

  const handleAnswerSelect = (answerIndex: number) => {
    setSelectedAnswer(answerIndex);
    setShowFeedback(true);
    
    if (answerIndex === questions[currentQuestion].correct) {
      setCorrectAnswers(correctAnswers + 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setShowFeedback(false);
    } else {
      const score = Math.round((correctAnswers / questions.length) * 100);
      onComplete(score >= 80, score);
    }
  };

  const question = questions[currentQuestion];
  const isCorrect = selectedAnswer === question.correct;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Question {currentQuestion + 1} of {questions.length}</span>
          <span>{correctAnswers} correct so far</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all"
            style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
          />
        </div>
      </div>

      <div className="bg-white rounded-lg p-6">
        <h3 className="text-xl font-bold mb-6">{question.question}</h3>
        
        <div className="space-y-3">
          {question.options.map((option, index) => (
            <button
              key={index}
              onClick={() => !showFeedback && handleAnswerSelect(index)}
              disabled={showFeedback}
              className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                !showFeedback 
                  ? 'hover:bg-purple-50 hover:border-purple-300 cursor-pointer border-gray-200'
                  : selectedAnswer === index
                    ? isCorrect
                      ? 'bg-green-50 border-green-500'
                      : 'bg-red-50 border-red-500'
                    : index === question.correct
                      ? 'bg-green-50 border-green-500'
                      : 'bg-gray-50 border-gray-200 opacity-50'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                  !showFeedback
                    ? 'border-gray-300'
                    : selectedAnswer === index
                      ? isCorrect
                        ? 'bg-green-500 border-green-500'
                        : 'bg-red-500 border-red-500'
                      : index === question.correct
                        ? 'bg-green-500 border-green-500'
                        : 'border-gray-300'
                }`}>
                  {showFeedback && (
                    selectedAnswer === index || index === question.correct
                  ) && (
                    <span className="text-white text-xs font-bold">
                      {(selectedAnswer === index && isCorrect) || index === question.correct ? '✓' : '✗'}
                    </span>
                  )}
                </div>
                <span className="flex-1">{option}</span>
              </div>
            </button>
          ))}
        </div>

        {showFeedback && question.explanation && (
          <div className={`mt-6 p-4 rounded-lg ${
            isCorrect ? 'bg-green-50 border-green-200' : 'bg-blue-50 border-blue-200'
          } border`}>
            <p className="text-sm">
              <strong>{isCorrect ? 'Correct!' : 'Not quite.'}</strong> {question.explanation}
            </p>
          </div>
        )}

        {showFeedback && (
          <button
            onClick={handleNext}
            className="mt-6 w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium hover:shadow-lg"
          >
            {currentQuestion < questions.length - 1 ? 'Next Question' : 'Complete Quiz'}
          </button>
        )}
      </div>
    </div>
  );
};

export default function LearningModal({
  isOpen,
  onClose,
  nodeId,
  nodeTitle,
  questions,
  onComplete
}: LearningModalProps) {
  const [phase, setPhase] = useState<LearningPhase>('intro');
  const [contentCompleted, setContentCompleted] = useState(false);
  const [quizScore, setQuizScore] = useState(0);

  if (!isOpen) return null;

  const handleContentComplete = () => {
    setContentCompleted(true);
    // Automatically transition to quiz after content
  };

  const handleStartQuiz = () => {
    setPhase('quiz');
  };

  const handleQuizComplete = (passed: boolean, score: number) => {
    setQuizScore(score);
    setPhase('complete');
    onComplete(passed, score);
  };

  const handleRestart = () => {
    setPhase('intro');
    setContentCompleted(false);
    setQuizScore(0);
  };

  const renderIntro = () => (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center p-8">
      <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center mb-6">
        <BookOpen className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-3xl font-bold mb-4">Ready to Learn?</h2>
      <p className="text-lg text-gray-600 mb-8 max-w-md">
        You'll start with the course content to understand the concepts, then test your knowledge with a quiz.
      </p>
      <div className="flex items-center gap-4 mb-8">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-purple-600" />
          </div>
          <span className="font-medium">Learn</span>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-400" />
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
            <Brain className="w-5 h-5 text-blue-600" />
          </div>
          <span className="font-medium">Practice</span>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-400" />
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
            <Trophy className="w-5 h-5 text-green-600" />
          </div>
          <span className="font-medium">Master</span>
        </div>
      </div>
      <button
        onClick={() => setPhase('content')}
        className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium hover:shadow-lg transform hover:-translate-y-0.5 transition-all"
      >
        Start Learning
      </button>
    </div>
  );

  const renderComplete = () => (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center p-8">
      <div className={`w-20 h-20 rounded-full flex items-center justify-center mb-6 ${
        quizScore >= 80 ? 'bg-gradient-to-br from-green-500 to-emerald-500' : 'bg-gradient-to-br from-yellow-500 to-orange-500'
      }`}>
        <Trophy className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-3xl font-bold mb-4">
        {quizScore >= 80 ? 'Excellent Work!' : 'Good Effort!'}
      </h2>
      <p className="text-lg text-gray-600 mb-4">
        You scored <span className="font-bold text-2xl">{quizScore}%</span>
      </p>
      <p className="text-gray-500 mb-8 max-w-md">
        {quizScore >= 80 
          ? "You've mastered this topic! Keep up the great work."
          : "You're making progress! Consider reviewing the material and trying again."}
      </p>
      <div className="flex gap-4">
        {quizScore < 80 && (
          <button
            onClick={handleRestart}
            className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Review Content
          </button>
        )}
        <button
          onClick={onClose}
          className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:shadow-lg"
        >
          Continue Learning
        </button>
      </div>
    </div>
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-5xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
              {phase === 'intro' && <BookOpen className="w-4 h-4" />}
              {phase === 'content' && <BookOpen className="w-4 h-4" />}
              {phase === 'quiz' && <Brain className="w-4 h-4" />}
              {phase === 'complete' && <Trophy className="w-4 h-4" />}
            </div>
            <div>
              <h2 className="font-bold text-lg">{nodeTitle}</h2>
              <p className="text-purple-100 text-sm">
                {phase === 'intro' && 'Introduction'}
                {phase === 'content' && 'Course Content'}
                {phase === 'quiz' && 'Knowledge Check'}
                {phase === 'complete' && 'Complete'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Progress Indicator */}
        <div className="bg-gray-100 p-2">
          <div className="flex items-center justify-center gap-2">
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm ${
              phase === 'content' ? 'bg-purple-600 text-white' : 
              contentCompleted ? 'bg-green-100 text-green-700' : 'bg-white text-gray-500'
            }`}>
              <BookOpen className="w-4 h-4" />
              <span>Content</span>
            </div>
            <ChevronRight className="w-4 h-4 text-gray-400" />
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm ${
              phase === 'quiz' ? 'bg-blue-600 text-white' : 
              phase === 'complete' ? 'bg-green-100 text-green-700' : 'bg-white text-gray-500'
            }`}>
              <Brain className="w-4 h-4" />
              <span>Quiz</span>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-140px)]">
          {phase === 'intro' && renderIntro()}
          
          {phase === 'content' && (
            <div className="p-6">
              <CourseContent
                nodeId={nodeId}
                nodeTitle={nodeTitle}
                onComplete={handleContentComplete}
                onStartQuiz={handleStartQuiz}
              />
            </div>
          )}
          
          {phase === 'quiz' && (
            <div className="p-6">
              <QuizComponent
                questions={questions}
                nodeTitle={nodeTitle}
                onComplete={handleQuizComplete}
              />
            </div>
          )}
          
          {phase === 'complete' && renderComplete()}
        </div>
      </div>
    </div>
  );
}