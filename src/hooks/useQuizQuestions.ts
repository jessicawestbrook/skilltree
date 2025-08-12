import { useState, useEffect } from 'react';
import { QuizQuestion } from '../types';
import { QuizService } from '../services/quizService';

export function useQuizQuestions(nodeId: string | null) {
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!nodeId) {
      setQuestions([]);
      return;
    }

    const fetchQuestions = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const fetchedQuestions = await QuizService.getQuestionsForNode(nodeId);
        setQuestions(fetchedQuestions);
      } catch (err) {
        console.error('Error fetching quiz questions:', err);
        setError('Failed to load quiz questions');
        // Use fallback questions on error
        setQuestions([{
          question: "What is the primary purpose of this topic?",
          options: ["To learn", "To practice", "To master", "All of the above"],
          correct: 3,
          explanation: "Learning involves all aspects: understanding, practicing, and mastering"
        }]);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [nodeId]);

  return { questions, loading, error };
}

export function useAllQuizQuestions() {
  const [questions, setQuestions] = useState<Record<string, QuizQuestion[]>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAllQuestions = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const allQuestions = await QuizService.getAllQuestions();
        setQuestions(allQuestions);
      } catch (err) {
        console.error('Error fetching all quiz questions:', err);
        setError('Failed to load quiz questions');
      } finally {
        setLoading(false);
      }
    };

    fetchAllQuestions();
  }, []);

  return { questions, loading, error };
}