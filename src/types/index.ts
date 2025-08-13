// Type definitions for NeuroQuest

export interface Node {
  id: string;
  name: string;
  prereqs: string[];
  category: string;
  domain: string;
  difficulty: number;
  points: number;
  index?: number;
  x?: number;
  y?: number;
  // Hierarchical properties
  parentId?: string;
  subnodes?: Node[];
  isExpanded?: boolean;
  level?: number;
  isParent?: boolean;
}

export interface Connection {
  from: string;
  to: string;
}

export interface UserStats {
  pathfinderPoints: number;
  neuralLevel: number;
  memoryCrystals: number;
  synapticStreak: number;
  conqueredNodes: string[];
  neuralPower: number;
  title: string;
  totalPoints?: number;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

export interface AnswerFeedback {
  isCorrect: boolean;
  explanation: string;
}

export interface LearningPath {
  name: string;
  icon: React.ComponentType<{ size?: number; color?: string }>;
  nodes: string[];
  description: string;
}

export type NodeState = 'completed' | 'available' | 'locked';

// Authentication types
export interface User {
  id: string;
  email: string;
  username: string;
  displayName?: string;
  avatar?: string;
  photoURL?: string;
  createdAt: Date;
  lastLoginAt?: Date;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  username: string;
  displayName?: string;
}

export interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<{ success: boolean; error?: string }>;
  register: (credentials: RegisterCredentials) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  updateProfile: (updates: Partial<User>) => Promise<{ success: boolean; error?: string }>;
}