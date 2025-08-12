import { QuizQuestion } from '../types';

export const quizQuestions: Record<string, QuizQuestion[]> = {
  'symbols-meaning': [
    {
      question: "What is the primary purpose of symbols?",
      options: ["To represent ideas", "To look pretty", "To confuse", "To take up space"],
      correct: 0,
      explanation: "Symbols are visual representations of ideas, concepts, or objects"
    }
  ],
  'quantity-concept': [
    {
      question: "Which represents 'more'?",
      options: ["3 < 5", "5 > 3", "3 = 3", "None"],
      correct: 1,
      explanation: "The symbol > means 'greater than', so 5 > 3 means 5 is more than 3"
    }
  ],
  'cooking-fundamentals': [
    {
      question: "What happens to water at 100°C?",
      options: ["It freezes", "It boils", "Nothing", "It disappears"],
      correct: 1,
      explanation: "Water boils at 100°C (212°F) at sea level"
    }
  ],
  'spanish': [
    {
      question: "How do you say 'Hello' in Spanish?",
      options: ["Bonjour", "Hola", "Ciao", "Guten Tag"],
      correct: 1,
      explanation: "Hola is the Spanish greeting for 'Hello'"
    }
  ],
  'french': [
    {
      question: "What does 'Bonjour' mean in French?",
      options: ["Goodbye", "Hello", "Please", "Thank you"],
      correct: 1,
      explanation: "Bonjour means 'Hello' or 'Good day' in French"
    }
  ],
  'programming-basics': [
    {
      question: "What is a variable in programming?",
      options: ["A fixed number", "A storage location with a name", "A type of loop", "An error"],
      correct: 1,
      explanation: "A variable is a storage location that has a name and can hold data"
    }
  ]
};