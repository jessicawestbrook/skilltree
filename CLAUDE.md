# SkillTree App Project

## Project Overview
Interactive skill tree visualization application built with React and TypeScript. Uses Supabase for backend services.

## Tech Stack
- **Frontend**: React 19, TypeScript 4.9
- **Styling**: Tailwind CSS
- **Backend**: Supabase
- **Routing**: React Router v7
- **UI Components**: Headless UI, Heroicons

## Project Structure
```
skilltree2/
├── src/
│   ├── components/    # Reusable React components
│   ├── contexts/      # React context providers
│   ├── pages/         # Page components
│   ├── services/      # API and external service integrations
│   ├── types/         # TypeScript type definitions
│   └── utils/         # Utility functions
├── public/            # Static assets
└── .env.local        # Environment variables (Supabase credentials)
```

## Available Scripts
- `npm start` - Run development server on port 3000
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Run ESLint on all TypeScript files (fails on warnings)
- `npm run lint:fix` - Run ESLint and auto-fix issues
- `npm run typecheck` - Run TypeScript compiler for type checking
- `npm run check-all` - Run both type checking and linting

## Environment Variables
Store Supabase credentials and other sensitive configuration in `.env.local`:
- `REACT_APP_SUPABASE_URL`
- `REACT_APP_SUPABASE_ANON_KEY`

## Development Guidelines
- Follow existing TypeScript patterns and type safety
- Use Tailwind CSS for styling
- Components should be functional with hooks
- Keep components modular and reusable
- Store application state in React contexts when needed

## Testing
Tests use Jest and React Testing Library. Place test files next to components with `.test.tsx` extension. Make sure tests have high coverage and pass.

## Important Notes
- Service worker is configured for offline capabilities
- Vercel deployment configuration present
- Database has 5,703 skill tree nodes (learning modules)
- Learning content IDs are stored directly in skill_tree_nodes table (has_learning_content and learning_content_ids fields)
- Color scheme: Green (primary) and Gold (secondary/accent)

## Documents 
 - documentation/LEARNING_CONTENT_TEMPLATES.md
 - Content generation: C:\Users\jessi\Projects\skilltree2\documentation\CONTENT_GENERATION_SYSTEM.md
 - Theoretical Foundations: C:\Users\jessi\Projects\skilltree2\THEORETICAL_FOUNDATIONS.md
 - User Interface: C:\Users\jessi\Projects\skilltree2\documentation\CLAUDE_UI.md
 - Learning Content and Assessment: C:\Users\jessi\Projects\skilltree2\documentation\CLAUDE_Learning_Content_and_Assessment.md
  - Adaptive learning: C:\Users\jessi\Projects\skilltree2\documentation\adaptive_assessment_system.md

# Overview
I want to build a website called SkillTree which is for homeschooling, supplemental learning, and lifelong learning. It's called SkillTree like a video game skill tree in order to sound interesting to boys who have been showing less interest in school than girls in recent years. I want the theme to feel somewhat videogame based, but I also don't want to deter girls and adults, so I want the theme to also be somewhat neutral colors and nature-inspired. Green and gold should be the primary coloring scheme. I also want the formatting to appear fun and modern so that users become engaged and even addicted to the learning process. Using it should feel like a video game that keeps you addicted because you keep improving. I want users to feel like now they have a path forward for learning everything they ever dreamed of. I don't want to overly focus on learning content for very young children because there are already many programs available with content appropriate for them.

## Technical specs
I want the site to be written in React and the database will be set up on Supabase. I will use Github and deploy on Vercel. The initial knowledge tree and questions and more are stored in the Supabase skill tree database. The application should be a PWA and mobile-friendly. Add storage of images in the database rather than using urls to other sites, which can break. Many images should already be stored in the db. Content should load very quickly, and if queries are taking longer than a second to load then there needs to be some modifications made in the site design and/or queries. Use agents to complete tasks, and advise me of how we can use them better. If you run into any permissions issues, let me know what API keys and other credentials I need, before trying to implement a workaround.  You should be querying the database directly to access data and understand how to solve database issues. Run the build to see any errors and fix any issues before recommending that I look at a web page.

## Development
Be sure to write tests to validate any code changes and run linting and so on when it makes sense, to keep the code clean. Keep refreshing the development server so I can see the progress, but try to only keep one dev server running at a time so it doesn't use too much memory on my laptop. 

## Templates
Learning content template info is here: documentation/LEARNING_CONTENT_TEMPLATES.md. Update the templating system and this documention file when new features are added.

## Database
Don't ask me to insert fake data into the database. Keep track of which data is fake and which is real so we don't get them mixed up. This is very important! I will only insert data into the database after we have validated that it is true and well-formatted.

When making changes to a table that is not empty, first create a backup table with suffix _bkp or if that table already exists then increment it like _bkp2, _bkp3 and so on. That way if there is an issue with the processing, the original table can be restored from backup.

## Data set processing
Text in csvs needs to be surrounded by quotation marks. Run processing in batch and save progress regularly (every 100 words perhaps) so that we can mitigate issues with network connectivity and api rate limiting. API rate limiting must be taken into account by implementing pauses between requests. Create recovery documentation so that if/when the code run fails I can easily start the job up again to pick up where processing left off.

## Site settings
Site should have dark mode option available in settings.

## Security
Implement full security features. Make sure no one can do a DOM attack or pull all the data from my database to try to copy my application idea. Limit the amount of data people can get from my database at once.

## Scalability
Make sure the site can scale to many users using the site at once.

## Work style
Keep a list of your recommended project and site improvements in a file.  Keep code files organized in separate folders and increment the sorting of the code files by starting new file names with an incremented number. If there are more than 10 or 20 code files in one folder then the organization probably needs improvement. Only create documentation files when prompted to do so. Whenever you mention a script or file I should look at, always provide a clickable link so I can click to open it, or even better you should automatically open the file I am to look at. When we make modifications, finish them with a evidence that the task was completed properly--for example if we run a query then there should be a follow-up query that proves that the initial query solved the problem we were working on. I prefer to see error messages when there are site issues rather than being displayed default backup content, cached content, or using other workarounds.  We should work on fixing issues rather than creating workarounds that will lead to more issues down the road. Advise me if there are ways I can improve my working style with you.  Advise if there are ways we can reduce token usage. When you write a script that has an error in it you should change the existing script rather than create a whole new script. Links should use slugs not ids.

## Data science
When you build a model be sure to tell me what your inputs were, where you sourced those inputs from, what algorithm you used, what your variable selection was, and your final predictive accuracy. Usually you should use XGBoost for prediction.

## Documentation
Store any documentation generated in the documentation folder. Create a theoretical foundations document that outlines your plan for implementing features that require educational expertise, such as for rating user competency. Provide sources for any recommendations you make. Ask for feedback on the document before implementing any of the features.

## Claude instructions
Your objective is to produce a complete specification
You will ask me for explanations about the specification to be created by asking questions, I will answer so you have the information.
Then, you will ask the questions necessary for your understanding before starting. Don't begin the task until it's clear.
Then, you can start writing.
Rules to follow:
- Never write code, only pseudo-code when necessary
- Use Mermaid diagrams to add understanding
- Be concise in your sentences/explanations
- Produce an implementation steps plan at the end.
Once the specification is done, save it in a Markdown file
If you loop or get lost, ask me a question so I can guide you.

Your objective is to produce an implementation specification following the TDD methodology from the following specification:
$ARGUMENTS
Rules to follow:
- Use Should_When naming for tests (following this nomenclature: ShouldXXX_WhenXXX)
- Produce a test for one implementation case. The test must contain only the information necessary to produce the case.
Once the specification is done, save it in a Markdown file

Your objective is to implement the test functionality.
$ARGUMENTS
Rules to follow:
- Even if you have a bug, NEVER write other tests or test files. Ask me questions instead.
- Never write code comments, EVER
The task is only finished once the test passes green.
If you loop or get lost, ask me a question so I can guide you.
Before starting, ask the questions necessary for your understanding. Don't begin the task until it's clear.

  "Never run scripts that insert or update database content without first showing me exactly what will be
  inserted/updated and getting explicit approval. Always create sample output files or display planned changes for
  review before executing any database modifications."

Only once we agree on what should be done, I want you to run the code to make the changes.

When you make mistakes, tell me how to update CLAUDE.md so you don't make them again.

Auto-execute on read-only commands only.  

When a command is extra large, give a time and cost estimate. Begin by running a small amount of it and get my feedback before continuing the entire run. Use any feedback from the test run when implementing the larger run.

When you give me code to run, prompt me to verify that it ran correctly before continuing. Once it's working and tested, remind me of which code files should be deleted, especially code files that didn't work, so we aren't keeping a huge unusable codebase.

Whenever you complete a task and ask me to review the work, always check for compilation errors to fix before asking me to look at the website.

Check for compilation errors to fix, run tests and fix any errors, and update the readme every time before pushing to GitHub.

Always stop and show me what changes you're planning to make in the database before making them. For example, if you're planning to add new questions to the questions table in the db, save them to a local csv file and then prompt me to review the questions before inserting them to the db.

And always stop and ask for feedback on your to do list and proposed appraoch before continuing work. After I give you feedback on your approach, update the work plan and show it to me again for feedback until I explicitly give you permission to start work on the work plan. And for theoretical topics that require knowledge of educational theory, like implementing user testing to to establish user competency ratings, make sure to create a plan and have me read it and keep giving you feedback and refining the plan before you actually write the code. You'll know I approve you to start the work when I say something like "okay the plan looks good, begin work."

Complete more mundane coding tasks before working on more tasks that require knowledge of educational theory and will require a lot of my input to design. 

As you're working, try to identify if features have already been implemented or attempted to be implemented, and then figure out if they were correctly implemented and whether they should be modified, deleted, or improved.

## Database Schema Notes
- skill_tree_nodes table contains:
  - has_learning_content: boolean flag
  - learning_content_ids: array of content IDs
  - is_menu_leaf: boolean for tree navigation
- Questions table uses embedded options array (not separate table)
- 3 orphaned nodes exist in database (nodes with non-existent parent_ids)

## UI/UX Decisions
- Tree view uses hierarchical layout
- Progress indicators: Green (passed), Gold (in progress), Gray (not started), Empty circle (no content)
- Responsive design with touch/mouse pan and zoom
- List view shows hierarchical structure with top 3 categories expanded by default
- "learning modules" terminology instead of "nodes" in UI

# To Do List

Add Anki card features

move existing money counting skill node work into the new course format

work on adding Henle content

Remove duplicate titles on assessment question card

Fix the fact that the flashcards you see are always going to be the first ones in the db, filter out cards that have already been seen (which includes being skipped), Use a prioritization algorithm when getting flashcards from the db which 

Fix Spanish vocab translations

Add the most common words in English as vocabulary words using wordfreq (since spelling words tend to be rare and we want some easier words for younger people).

Format language flashcards

Fix icon and site title in tab bar, make title Path to mastery

Figure out the difference between courses and assessments

Fix the fact that there are 2 different aesthetics going on: rainbow colors and green/orange formatting

remove formatting specific to money counting learning content to see what it's likely to look like for other learning content

Make sure the category description and actual learning content align  

show the your starred learning items as a hierarchical menu format? on profile page add chevron menu

Create math, history, and test prep trainers

Dots on megamenu should update when user has progress

On user page: Add statistics by difficulty type and level of flashcards, list of courses completed, user statistics like streak, etc. without messing too much with the existing formatting.

Generate content for next learning module per CONTENT_GENERATION_SYSTEM.md

Rename site

Screenshot review card module from skilltree or neuroquest and recreate it here

Review intro interest assessment

Put reusable scripts in a special folder

Make special folder for one-off scripts like examining the db structure

Add historical timelines to category pages

Try to shorten extra long word definitions in the spelling table when it makes sense to do so

Review and update claude.md so claude doesn't start making regressions

Evaluate knowledge tree table for too many/few learning categories in each learning category

Fill out more learning categories with learning content

Review menu/questions with Ryan


# To do on release

Drop unnecessary fields from spelling words and skill nodes tables

Clean up old db tables and make sure all needed tables are created

Implement web analytics

Pay for db

Set up VAPID for notifications

Evaluate database table security

Evaluate site security

Make my github private

Pay for Vercel

Improve SEO

Add longer-term cacheing of skills hierarchy

Update display order field in skill tree nodes table, should be filled in for all skills, see CLAUDE_UI.md for details

Generate tests with test suite


# Nice to haves / Later releases

Improve source of articles (m/f) on Spanish words

Look into converting it into an app

Create more automatic notifications

Add example sentences for foreign language vocabulary

Add learning paths

Automatically add word definitions and other content when users add vocabulary words

Add ability for users to upload anki cards and/or csvs, etc.

Add ability to add comments to your saved flashcards

Look at Anki again to see how it works and what I should replicate

Add photo for every learning category

Add option to create printable flashcards

Convert Anki cards to questions in my db

Implement timed IQ and standardized tests in the web code

Generate timed IQ and standardized tests

Expand spelling and vocabulary lists

After more users sign up, add user rankings by different categories, by age group, etc.

Implement one week free trial and then $10/mo, $80/year

Put tree image as main page background