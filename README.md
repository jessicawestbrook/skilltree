# 🧠 NeuroQuest

An interactive knowledge learning platform that gamifies education across all domains of human knowledge. Master subjects from fundamental concepts to advanced topics through an engaging visual knowledge graph.

![NeuroQuest](https://img.shields.io/badge/version-0.1.0-blue)
![Next.js](https://img.shields.io/badge/Next.js-15.4.6-black)
![React](https://img.shields.io/badge/React-19.1.0-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![Supabase](https://img.shields.io/badge/Supabase-2.55.0-green)

## ✨ Features

### 🎮 Gamified Learning Experience
- **Visual Knowledge Graph**: Interactive node-based learning map
- **Hierarchical Learning Paths**: Progress from foundations to mastery
- **Achievement System**: Earn points, levels, and maintain learning streaks
- **Quiz Challenges**: Test your knowledge with interactive quizzes

### 📚 Comprehensive Knowledge Domains
- **Foundation**: Communication, Quantitative Reasoning, Practical Skills
- **Fundamentals**: Mathematics, Science, Digital Literacy
- **Specialized Domains**: 
  - Programming & Computer Science
  - Languages (World & Programming)
  - Arts & Music
  - Biology & Health
  - Business & Entrepreneurship
  - Advanced Physics & Mathematics

### 🔄 Dynamic Features
- **Expandable Knowledge Nodes**: Drill down into specific subtopics
- **Real-time Progress Tracking**: Visual progress bars and statistics
- **Prerequisite System**: Unlock advanced topics by mastering fundamentals
- **Responsive Design**: Works seamlessly on desktop and mobile

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Supabase account (for quiz questions database)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jessicawestbrook/neuroquest.git
   cd neuroquest
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the root directory:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. **Set up the database**
   - Go to your Supabase dashboard
   - Run the SQL from `scripts/create-quiz-table.sql` in the SQL editor
   - Run the migration to populate quiz questions:
     ```bash
     npm run migrate:questions
     ```

5. **Start the development server**
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) to see the app.

## 📖 Usage

### Navigation
- **Click nodes** to view details and start challenges
- **Click parent nodes** (purple) to expand/collapse subnodes
- **Complete prerequisites** to unlock new topics
- **Use the sidebar** to filter by domain or search topics

### Learning Flow
1. Start with foundation topics (unlocked by default)
2. Complete quizzes to earn points and unlock prerequisites
3. Progress through fundamentals to specialized domains
4. Achieve mastery by completing advanced topics

### Features
- **Search**: Find specific topics using the search bar
- **Filters**: Filter by domain (Mathematics, Science, Arts, etc.)
- **Learning Paths**: Follow suggested learning sequences
- **Profile**: Track your stats, achievements, and progress

## 🛠️ Tech Stack

- **Frontend Framework**: [Next.js 15](https://nextjs.org/) with App Router
- **UI Library**: [React 19](https://react.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Database**: [Supabase](https://supabase.com/)
- **Styling**: CSS-in-JS with inline styles
- **Icons**: [Lucide React](https://lucide.dev/)
- **Authentication**: Supabase Auth (ready for integration)

## 📁 Project Structure

```
neuroquest/
├── src/
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── contexts/         # React contexts (Auth, etc.)
│   ├── data/            # Static data (knowledge graph, icons)
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API services (Supabase)
│   ├── types/           # TypeScript type definitions
│   └── utils/           # Utility functions
├── scripts/             # Database and migration scripts
├── public/              # Static assets
└── docs/               # Documentation
```

## 🗄️ Database Schema

### Quiz Questions Table
```sql
CREATE TABLE quiz_questions (
  id UUID PRIMARY KEY,
  node_id VARCHAR(255),
  question TEXT,
  options JSONB,
  correct_answer INTEGER,
  explanation TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

## 📝 Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run migrate:questions  # Migrate quiz questions to Supabase
```

## 🎨 Customization

### Adding New Knowledge Nodes
Edit `src/data/hierarchicalKnowledgeGraph.ts` to add new topics:
```javascript
{
  id: 'your-topic-id',
  name: 'Your Topic Name',
  prereqs: ['prerequisite-id'],
  category: 'fundamentals',
  domain: 'your-domain',
  difficulty: 3,
  points: 150,
  level: 0,
  isParent: false
}
```

### Adding Quiz Questions
Use the QuizService to add questions programmatically:
```javascript
import { QuizService } from '@/services/quizService';

await QuizService.addQuestion('node-id', {
  question: 'Your question?',
  options: ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
  correct: 0,
  explanation: 'Explanation here'
});
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Icons by [Lucide](https://lucide.dev/)
- Database by [Supabase](https://supabase.com/)
- Framework by [Next.js](https://nextjs.org/)

## 📧 Contact

Jessica Westbrook - [GitHub](https://github.com/jessicawestbrook)

Project Link: [https://github.com/jessicawestbrook/neuroquest](https://github.com/jessicawestbrook/neuroquest)

---

Built with ❤️ and 🧠 to make learning an adventure!