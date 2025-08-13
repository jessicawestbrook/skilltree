import { BarChart3, Zap, Hammer, Leaf, Cpu, Heart, Briefcase, Palette, Globe, Brain, BookOpen } from 'lucide-react';

export const domainIcons: Record<string, React.ComponentType<{ size?: number; color?: string }>> = {
  mathematics: BarChart3,
  science: Zap,
  practical: Hammer,
  biology: Leaf,
  physics: Zap,
  computer_science: Cpu,
  health: Heart,
  business: Briefcase,
  arts: Palette,
  languages: Globe,
  advanced: Brain,
  communication: BookOpen,
  quantitative: BarChart3
};