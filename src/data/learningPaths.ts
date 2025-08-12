import { LearningPath } from '../types';
import { Home, Cpu, Briefcase, Hammer, BookOpen, Globe } from 'lucide-react';

export const learningPaths: Record<string, LearningPath> = {
  'self-sufficiency': {
    name: 'Self-Sufficient Living',
    icon: Home,
    nodes: ['cooking-fundamentals', 'gardening', 'basic-repairs', 'home-maintenance', 'first-aid'],
    description: 'Learn to be independent'
  },
  'digital-creator': {
    name: 'Digital Creator',
    icon: Cpu,
    nodes: ['digital-literacy', 'programming-basics', 'web-development', 'photography', 'creative-writing'],
    description: 'Create in the digital world'
  },
  'entrepreneur': {
    name: 'Entrepreneur Path',
    icon: Briefcase,
    nodes: ['money-management', 'entrepreneurship', 'marketing', 'accounting', 'project-management'],
    description: 'Start your business journey'
  },
  'maker': {
    name: 'Maker & Builder',
    icon: Hammer,
    nodes: ['tool-use-basic', 'woodworking', 'basic-repairs', 'home-maintenance'],
    description: 'Build and create with your hands'
  },
  'scholar': {
    name: 'Academic Scholar',
    icon: BookOpen,
    nodes: ['scientific-method', 'algebra-thinking', 'calculus-concepts', 'statistics-probability'],
    description: 'Deep theoretical knowledge'
  },
  'polyglot': {
    name: 'Language Master',
    icon: Globe,
    nodes: ['language-fundamentals', 'spanish', 'french', 'german', 'chinese'],
    description: 'Master multiple languages'
  }
};