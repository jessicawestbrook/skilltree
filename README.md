# 🧠 NeuroQuest

An interactive knowledge learning platform that gamifies education across all domains of human knowledge. Master subjects from fundamental concepts to advanced topics through an engaging visual knowledge graph.

![NeuroQuest](https://img.shields.io/badge/version-0.2.0-blue)
![Next.js](https://img.shields.io/badge/Next.js-15.4.6-black)
![React](https://img.shields.io/badge/React-19.1.0-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4.0-38B2AC)
![Supabase](https://img.shields.io/badge/Supabase-2.55.0-green)

## ✨ Features

### 🎮 Gamified Learning Experience
- **Visual Knowledge Graph**: Interactive node-based learning map with 100+ topics
- **Hierarchical Learning Paths**: Progress from foundations to mastery
- **Achievement System**: Earn points, levels, badges, and maintain learning streaks
- **Quiz Challenges**: Test your knowledge with interactive quizzes
- **Expandable Parent Nodes**: Drill down into subtopics (Calculus, Statistics, Algorithms, Languages)

### 📚 Comprehensive Knowledge Domains
- **Foundation**: Communication, Quantitative Reasoning, Practical Skills
- **Fundamentals**: Mathematics, Science, Digital Literacy
- **Specialized Domains**: 
  - Mathematics (Calculus, Statistics, Linear Algebra)
  - Computer Science (Algorithms, Data Structures)
  - World Languages (Spanish, French, German, Chinese, Japanese)
  - Sciences (Biology, Chemistry, Physics)
  - Practical Skills (Cooking, Money Management, Repairs)

### 🔄 Dynamic Features
- **Expandable Knowledge Nodes**: Click parent nodes to reveal detailed subtopics
- **Real-time Progress Tracking**: Visual progress bars and statistics
- **Prerequisite System**: Unlock advanced topics by mastering fundamentals
- **User Profiles**: Track achievements, neural level, and learning streaks
- **Leaderboard**: Compete with other learners
- **Learning Paths**: 7 curated paths for different learning goals
- **Course Content System**: Rich learning materials with sections, resources, and tips
- **Learning Modal**: Integrated content delivery with quiz challenges
- **Dark Mode Support**: Full theme support across the application

### 🏠 Landing Page
- **Modern Homepage**: Beautiful landing page for non-authenticated users
- **Feature Highlights**: Showcase platform capabilities
- **Call-to-Action**: Easy signup/signin flow
- **Responsive Design**: Mobile-first approach with Tailwind CSS

### 🛠️ Admin Interface
- **Dashboard**: Real-time statistics and quick actions
- **Question Management**: CRUD operations, inline editing, search and filter
- **Batch Upload**: Import questions via CSV/JSON files or web interface
- **Knowledge Nodes**: Manage nodes, prerequisites, and availability
- **Learning Paths**: Configure paths, manage nodes, and publication status
- **User Management**: View user profiles, progress, and activity
- **Settings Panel**: System configuration and maintenance tools

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Supabase account (free tier works)

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
   
   Run these SQL scripts in your Supabase SQL editor in order:
   
   ```sql
   -- Run each script in the Supabase SQL editor:
   00-prepare-for-migration.sql    # Disables RLS for migration
   01-create-core-tables.sql        # Core tables
   02-create-dependent-tables.sql   # Dependent tables
   03-create-user-tables.sql        # User profile tables
   04-create-views-and-functions.sql # Views and triggers
   ```

5. **Migrate the data**
   ```bash
   npm run migrate:all
   ```
   
   This will populate:
   - 100+ knowledge nodes
   - 50+ prerequisite relationships
   - 7 learning paths
   - Quiz questions for various topics

6. **Re-enable security**
   ```sql
   -- Run in Supabase SQL editor:
   05-enable-security.sql
   ```

7. **Start the development server**
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) to see the app.

8. **Access the admin interface**
   ```
   http://localhost:3000/admin
   ```

## 📖 Usage

### Navigation
- **Click nodes** to view details and start challenges
- **Click parent nodes** (with +/- icons) to expand/collapse subnodes
- **Complete prerequisites** to unlock new topics (locked nodes show 🔒)
- **Use the sidebar** to:
  - Search for specific topics
  - Filter by domain
  - Select learning paths
  - View your profile stats

### Learning Flow
1. Start with foundation topics (unlocked by default)
2. Complete quizzes to earn points and unlock prerequisites
3. Progress through fundamentals to specialized domains
4. Expand parent nodes to explore detailed subtopics
5. Achieve mastery by completing advanced topics

### Game Elements
- **Points**: Earn 25-300 points per completed topic
- **Neural Level**: Level up every 500 points
- **Memory Crystals**: Special rewards for achievements
- **Synaptic Streak**: Maintain daily learning habits
- **Achievements**: Unlock 8 different badges

## 🛠️ Tech Stack

- **Frontend Framework**: [Next.js 15](https://nextjs.org/) with App Router
- **UI Library**: [React 19](https://react.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL)
- **Styling**: CSS-in-JS with inline styles
- **Icons**: [Lucide React](https://lucide.dev/)
- **Authentication**: Supabase Auth (ready for integration)

## 📁 Project Structure

```
neuroquest/
├── src/
│   ├── app/              # Next.js app router pages
│   │   ├── page.tsx      # Main knowledge graph view
│   │   └── admin/        # Admin dashboard
│   ├── components/       # React components
│   │   ├── Header.tsx    # Top navigation with stats
│   │   ├── Sidebar.tsx   # Domain filters and paths
│   │   └── AuthModal.tsx # Login/signup modal
│   ├── contexts/         # React contexts
│   ├── data/            # Static data files
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API services (Supabase)
│   ├── types/           # TypeScript definitions
│   └── utils/           # Utility functions
├── scripts/             # Database setup and migrations
│   ├── 00-05*.sql      # Step-by-step schema setup
│   └── migrate-*.js    # Data migration scripts
├── public/              # Static assets
└── docs/               # Documentation
    ├── STEP_BY_STEP_SETUP.md    # Detailed setup guide
    └── SUPABASE_SETUP_GUIDE.md  # Database setup guide
```

## 🗄️ Database Schema

### Core Tables
- `knowledge_nodes` - All learning topics with hierarchy
- `node_prerequisites` - Prerequisite relationships
- `quiz_questions` - Questions for each node
- `learning_paths` - Curated learning sequences
- `learning_path_nodes` - Nodes in each path

### User Tables
- `user_profiles` - Extended user profiles with stats
- `user_progress` - Tracks completed nodes
- `achievements` - Available achievements
- `user_achievements` - Earned achievements
- `user_connections` - Friend system

## 📝 Available Scripts

```bash
npm run dev                # Start development server
npm run build             # Build for production
npm run lint              # Run ESLint
npm run type-check        # Run TypeScript compiler
npm run start             # Start production server
npm run lint              # Run ESLint
npm run migrate:all       # Run all data migrations
npm run migrate:knowledge # Migrate knowledge nodes
npm run migrate:paths     # Migrate learning paths
npm run migrate:questions # Migrate quiz questions
```

## 🎨 Customization

### Adding New Knowledge Nodes
Edit `scripts/migrate-knowledge-graph.js` to add new topics:
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

#### Method 1: Admin Interface
1. Navigate to `/admin/questions/new` to add individual questions
2. Use `/admin/upload` for batch uploading via CSV or JSON

#### Method 2: Batch Upload Script
```bash
# Generate sample files
node scripts/batch-load-questions.js --generate-sample

# Load from file
node scripts/batch-load-questions.js sample-questions.json
node scripts/batch-load-questions.js sample-questions.csv
```

#### Method 3: Direct Database Edit
Edit `scripts/migrate-questions.js` to add questions:
```javascript
'your-topic-id': [
  {
    question: "Your question?",
    options: ["Option 1", "Option 2", "Option 3", "Option 4"],
    correct: 0,
    explanation: "Explanation here"
  }
]
```

### Creating Learning Paths
Edit `scripts/migrate-learning-paths.js`:
```javascript
{
  name: 'Path Name',
  icon: 'IconName',
  description: 'Path description',
  nodes: ['node-1', 'node-2', 'node-3']
}
```

## 🚧 Roadmap

- [ ] User authentication and profiles
- [ ] Social features (friends, study groups)
- [ ] More quiz question types
- [ ] Progress certificates
- [ ] Mobile app version
- [ ] Content creator tools
- [ ] AI-powered learning recommendations
- [ ] Multiplayer challenges

## 📊 Recent Updates (v0.2.0)

### New Features
- 🏠 **Landing Page**: Beautiful homepage for non-authenticated users
- 🎨 **Modern UI Components**: Redesigned header, sidebar, and layout
- 📚 **Course Content System**: Rich learning materials integrated with quiz system
- 🌙 **Dark Mode**: Full theme support with ThemeContext
- 🔧 **Code Quality**: Fixed all ESLint errors, improved TypeScript types
- 📱 **Responsive Design**: Mobile-first approach with Tailwind CSS v3

### Improvements
- ✅ Cleaned up unused imports and variables
- ✅ Fixed React Hook dependencies
- ✅ Improved TypeScript type safety
- ✅ Enhanced component modularity
- ✅ Better error handling throughout

### Tech Stack Updates
- Migrated to Tailwind CSS v3.4.0
- Updated PostCSS configuration
- Improved build performance

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
- UI inspiration from skill trees in RPG games

## 📧 Contact

Jessica Westbrook - [GitHub](https://github.com/jessicawestbrook)

Project Link: [https://github.com/jessicawestbrook/neuroquest](https://github.com/jessicawestbrook/neuroquest)

---

Built with ❤️ and 🧠 to make learning an adventure!