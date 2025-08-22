# SkillTree App Project

## Project Overview
Interactive skill tree visualization application built with React, TypeScript, and D3.js. Uses Supabase for backend services.

## Tech Stack
- **Frontend**: React 19, TypeScript 4.9
- **Styling**: Tailwind CSS
- **Data Visualization**: D3.js
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
- Use D3.js for skill tree visualizations
- Store application state in React contexts when needed

## Testing
Tests use Jest and React Testing Library. Place test files next to components with `.test.tsx` extension. Make sure tests have high coverage and pass.

## Important Notes
- Service worker is configured for offline capabilities
- Vercel deployment configuration present
- Database has 5,703 skill tree nodes (learning modules)
- Learning content IDs are stored directly in skill_tree_nodes table (learning_content_ids field)
- Color scheme: Green (primary) and Gold (secondary/accent)

## Documents
 - Theoretical Foundations: C:\Users\jessi\Projects\skilltree2\THEORETICAL_FOUNDATIONS.md

# Overview
I want to build a website called SkillTree which is for homeschooling, supplemental learning, and lifelong learning. It's called SkillTree like a video game skill tree in order to sound interesting to boys who have been showing less interest in school than girls in recent years. I want the theme to feel somewhat videogame based, but I also don't want to deter girls and adults, so I want the theme to also be somewhat neutral colors and nature-inspired. Green and gold should be the primary coloring scheme. I also want the formatting to appear fun and modern so that users become engaged and even addicted to the learning process. Using it should feel like a video game that keeps you addicted because you keep improving. I want users to feel like now they have a path forward for learning everything they ever dreamed of. I don't want to overly focus on learning content for very young children because there are already many programs available with content appropriate for them.

## Technical specs
I want the site to be written in React and the database will be set up on Supabase. I will use Github and deploy on Vercel. Make visualizations with the D3 library. The initial knowledge tree and questions and more are stored in the Supabase skill tree database. The application should be a PWA and mobile-friendly. Add storage of images in the database rather than using urls to other sites, which can break. Many images should already be stored in the db. Content should load very quickly, and if queries are taking longer than a second to load then there needs to be some modifications made in the site design and/or queries. Use agents to complete tasks, and advise me of how we can use them better. If you run into any permissions issues, let me know what API keys and other credentials I need, before trying to implement a workaround.  You should be querying the database directly to access data and understand how to solve database issues. Run the build to see any errors and fix any issues before recommending that I look at a web page.

## Appearance/Design
I'm a fan of having less content on the page when it makes sense because people's brains can't handle too much "stuff" at once, so generally avoid unnecessary text or other objects being displayed at once. For example, don't have duplicate Home links on the menu bar. But I also don't want to make the user have to do a lot of clicking to go from page to page to get to the material they want--I'd rather it all be readily accessible on one page.

Use trees and tree theming for logo and site learning tree design. The logo in the brand and in the favicon should be very similar if not the same.

The whole question text and question options should be viewable on the typical laptop or mobile screen without having to scroll, unless it's a really long question.

## Site
Users can click on a category of interest to go to a separate page and learn about the overall learning content within that category. Users will be able to log in and save categories of interest they want to learn about.  Then there are recommend content areas for them to learn about next. 

## Features

### Tree viz
Initiate the list view with the top 3 categories already opened, and remove category subheaders. There should be a way so that when you click a category in the mind map, it takes you to the list view with the category as the root node and any children opened up and visible.  The skill tree looks like a radial layout, decision tree, or mind map format but more attractive. Make the tree clickable and easy to navigate. 

Obviously the tree is too big to display the whole (5,000 nodes) thing in one component, so only show a limited number of tree items at once, and make it easy to star categories of interest. Show the entire tree component on the screen without having to scroll. They can then filter their own personalized mind map so that only their starred items of interest are displayed. The symbol for bookmarking should be a star. There should also be a text-only view for people who don't want to navigate a strange viz and for users who don't have a lot of internet bandwidth for loading a lot of complex content. The tree viz and list view should be tied together and displayed side by side and work together so that when someone opens content in one, it is also displayed in the other at the same time, along with the immediate ancestor and child nodes.

Use a colored circle completion indicator for your progress on a topic--gray means not started, yellow means in progress, green means you passed the test for that topic, while a circle that is filled in white with a gray outline represents a topic that does not yet have learning content. 

### Content searching
Search bar to easily find content categories, learning content, and questions. Don't just use text matching, use a more sophisticated search engine. This should already be implemented.

## Learning content
When a user clicks a content area they want to learn about next, it opens a modal that gives a brief (perhaps 3-question) quiz, then it shows a learning content page which includes one or more pictures and a short text to learn about the topic.  The short text can be around 200-1000 words, or however long it makes sense to learn about the topic. It should be easy to learn the learning content in 10-30 minutes. Visualizations can help learners, so wherever possible include relevant pictures, for example pictures of art or AI-generated pictures representing math explanations and/or quiz questions. Book summaries can be longer. Then it will give a test to show mastery of the content. Some content areas are high-level categories that have that may or may not have their own learning content and testing. Leaf nodes always have their own learning content and testing.

### IQ testing
Organize the IQ test flow as just a series of timed tests without a prequiz or learning content.  Try to find actual IQ tests from the internet with the actual time limits. IQ tests should not be randomly selected from the question bank but rather should be in the specific order that it was created in. Evaluate the person's IQ at the end based on the evaluation metrics for that IQ test. Try to use more recent (last 10-20 years) IQ tests when available because IQ test results are standardized around the answers of other people from a particular time period, and IQ test results have been changing over time. Keep track of how users performed on a specific IQ test and the resultant IQ that was assigned, rather than tracking typical test metrics like percent correct. Also keep track of how many times a user took a particular IQ test and their score history for it. 

### Standardized testing
Standardized Testing subcategories can include different popular standardized tests such as the ACT, SAT, and LSAT. Fill out the questions similarly to what has been done for the IQ test category, trying to use actual tests found online and timing the test and evaluating the results based on the specific answers provided by the source with that test. Try to go with old tests that were actually administered to students, not similar example tests written by other people or organizations. When someone begins a test, provide a source and link to where you got the learning material from. Keep track of how users performed on a specific test and the resultant score that was assigned, rather than tracking typical test metrics like percent correct. Also keep track of how many times a user took a particular test and their score history for it. 

### Learning paths
There are recommended learning paths. Some topics, especially in math, have prerequisits for advancement. Users can pass out of prerequisits by taking short mastery tests. Mastery tests can be at the course or learning content area level.

### Reading comprehension
For Reading Comprehension, don't show the questions in the Quick Practice box, and make it so multiple questions can be associated with one reading. Try to get reading comprehension questions from online question banks, and save the url where the material and questions were sourced.

### Spelling Bee Trainer
Add spelling bee practice where a word is said aloud, and the user is given an example sentence using the word (with the word replaced by a blank) as well as background information on the word, and then the user to type in the spelling. After the user submits their answer, provide the answer along with tips to remember how to spell it next time including history of the etymological roots.  Spelling bee audio should be based on a computer voice, there should be APIs available to do this, and the audio files should be saved to database. You can get the spelling bee questions based on the Scripps National Spelling Bee and other spelling bees, where available online. Make sure to save the name and url where the information was sourced from and assign a difficulty level for words based on how the Scripps National Spelling Bee would assign difficulty to a word.  Look at how scripps assigns word difficulty levels and make your approach comparable but use more user-friendly standard difficulty names. Also save the source's assigned difficulty to db. When inserting new words to the table make sure the word doesn't already exist there. Add options to the spelling bee interface for whether to use computer adaptive testing or a min/max filter so spelling bee users can set the difficulty of words they want to focus on.  Display percent accuracy by difficulty level to show the user how they're improving over time. Remove the maximum number of spelling words to be practiced in a session. Users can star flashcards/questions and save to custom study lists. Make word definitions and example sentences short and pithy but meaningful.

### Vocabulary Trainer
Add vocabulary practice where an example sentence and word definition are displayed, and the user has to guess the word from a list of choices (multiple choice questions). It can use the same data set as the Spelling Bee trainer. The answer choices will be drawn randomly from the input table, and plausible alternatives are displayed, such as words in the same difficulty rating. Functionality is otherwise similar to the spelling bee trainer. Users can star flashcards/questions and save to custom study lists. Create different difficulty levels for vocabulary trainer than what was done for spelling trainer. Create a framework for how to evaluate vocabulary difficulty level, and add this plan to the documentation/THEORETICAL_FOUNDATIONS.md. Make word definitions and example sentences short and pithy but meaningful.

### Language Trainer
Foreign language flashcards application where the user can pick from a dropdown which language to study. There is a menu for the user to select study categories by difficulty level, topic, etc. Questions are multiple choice and answer options are stored as an array. Questions could be sentence completion, vocabulary translation, reading comprehension, or matching a word to a picture. Similar page structure to the Vocabulary trainer. Users can star flashcards/questions and save to custom study lists. 

### User page
After login user should be redirected to user/profile page. User can view their recommended content, saved content, and flashcards. Can create new study lists from this page. They can also update their settings such as interest level in various categories. Can also set info like career path and age group.

#### Starred flashcards
Users can star/bookmark flashcards they want to keep working on.

#### Custom study lists
This is where the user can access all their custom study lists across the entire site. They can specify study strategies such setting reminders to review particular content. 

#### Custom flashcards
User can create custom flashcards.

#### Custom flashcard lists
User can create custom flashcard lists that can combine flashcards from the site and their own custom flashcards. Flashcards should have a mechanism for starring/saving them as well as an option to add them to a particular study list.

### Feedback
Add a feedback system, with different categories of feedback the user can select from, such as bug reports or learning content requests. Create an admin page for responding to the requests as well as a messaging history so users can see admin responses. Link the feedback system in the top menu. Add ability for user to flag content or questions that have issues.

### Admin
Make it so only admin users can see the admin dashboard.

### Random question box
Sidebar which gives a randomly selected question from content areas the user has starred or worked on in the past. For new users it can display a simple random question. After a question is submitted, the answer explanation pops up, and the user can choose to move on to the next question. Display the knowledge hierarchy path so the user knows where the question is coming from. Don't show the random question box on mobile.

### Intro interests assessment
Assessment that gathers user information for the purpose of recommending learning content. Evaluates approximate skill level and interest level in various categories.

### Node test
You pass the test for a topic if you get 100% of the questions correct. Save the url where the IQ test, standardized test, reading comprehension content, etc. was sourced from. If any individual questions were sourced from a site online, save that to the database as well.

### Question bank
See documentation/CONTENT_GENERATION_SYSTEM.md.

It's important to organize the learning content areas and hierarchy of knowledge well before writing questions in the question bank so that you don't have to move questions to different categories as the categorization system evolves. For that reason, writing the question banks should come as a final task in the project. Also, it will take a long time to run and require my input for each learning category, so we should estimate costs and validate with me before you start a question bank creation task. You will need to write a question bank for each content area to draw from for these questions and tests. Each content area should generally have at least 20 questions to draw from, but more is generally better if you're able to create good questions that make sense and aren't too similar to each other. These questions will be stored in the db. Always stop and show me what questions you're planning to add to the db before adding them. 

These questions should usually be multiple choice but can also be in other formats. Questions should usually be answerable without doing a lot of calculating--they should usually be conceptual questions rather than cranking out calculations (for example, calculus questions can become very involved, but try to make most questions answerable just by thinking about the concept). Try to make questions test the content being taught, and not other unrelated content. For example, "Which article is correct: ___ nieto?" this question is not good for the Spanish Family section because it's testing about articles and word gender rather than about the family relationships themselves. Each question should only have one correct answer.  Questions should work as standalone content with answer explanations that teach the users more whether they got the question right or wrong.  Avoid vague/simplified questions like "How did the Catholic church impact the economy during the Gilded Age?" since these sorts of questions are too general, and it could be argued many different ways. Try to make questions more specific to actual events and problem types rather than summarizing events in such a simplistic manner. Make questions work as standalone questions rather than being what are presumably meant to be reading comprehension questions of some summary textbook-type content. Create a detailed answer to the question so that the user can learn from the answer, whether they got the question right or wrong. Try to provide an explanation for not only the correct answer but also an explanation about the incorrect answers and why they're incorrect. Also try to add a relevant picture to each one in order to make the content more memorable. It may be difficult to do this with a lot of the math problems, but where possible try to turn the math problems into story problems with a relevant picture to help explain the content. The picture can be either a good quality, fair use one found online that doesn't have any watermarks on it, an icon/graphic, or it can be AI generated. Ensure that if the question specifically talks about an image then the relevant image exists for it, such as for questions where it asks the number of objects in the picture.  

Questions should be given a difficulty rating which is relative to the difficulty of other questions in that learning content area. The questions should be answerable by reading the learning content.

Keep track of which questions the user has seen before and whether they got it right or wrong--this information can be used in algorithms for recommending review questions. The number of questions in the question bank should be as large as makes sense, but more is generally better. For example, vocabulary banks could be based on hundreds or thousands of words, learning the multiplication table could be up to a hundred questions, etc. 

Preferentially show questions in quizzes which have been previously viewed the least number of times by that user in that question bank. For example, if someone has taken a quiz multiple times and some questions have already been viewed or viewed multiple times, when they take it again show them questions which they have not seen as many times previously. Don't show a question in the content area test that was just shown in the intro quiz.

Create an initial set of 15 questions per topic for immediate use, then generate more questions on-demand or during low-usag
e periods. If a user gets a question recommended to them which they have already got correct within the past few days or past use then it is time to generate more questions for that topic.

#### Question explanations
You will also need to write answer explanations for every question. Be complete and thorough when explaining your reasoning for why that is the correct answer. When it makes sense, such as for humanities, social sciences, and sciences content, include links to external learning content that explains your answer. (This would not make sense for learning languages or reading comprehension questions.)

After each question answer is submitted, show an explanation for the answer before moving on to the next question.  You can draw a lot of examples for building these question banks from content already found on the internet.  There can be an infinite number of review questions because it will just keep drawing randomly from the question bank. 

### Learning content generator
For batch processing, write a script which goes through each learning category's skill tree. For each learning content area, it calls the Claude API to create about 10-30 minutes of learning content, at least 50-100 quesions with multiple choice answers related to learning that content area, as well as the question explanations. Then it saves the results to the db. The learning content should be attractively formatted into sections and use visualizations when available. Would it make sense for the learning content to be stored in the db as html? Make sure to use engaging language with specific details without being overly academic. Storytelling is very important, with concrete details. It can also be useful to have a "so what" section--how did this change the future, or how does it change how we live today, or why is this important? I'm also considering adding a button that uses a computer to read the content aloud to you so you don't have to read it yourself.

## Specs

### Home page
Add research-based learning facts to home page like years of schooling increases IQ. Use facts that will encourage users to want to use the site.  Make the sources clickable, link to outside pages which have high credibility and back up the claims.

### Learning category pages
Clicking on a learning category takes you to a standard category overview page that includes a category overview, a menu of child categories, and a link to a "Rate Your Knowledge" where you answer questions to earn points. Questions follow computer adaptive difficulty. Create point system that assigns points based on how many questions you've answered correctly of each difficulty level. That way you can compare points of different category types, and if the question bank changes over time, the points are still meaningful. It shows which items have been completed and allows the user to star/bookmark the category or child categories. Clicking on child categories opens the category page for that category. Clicking on child nodes takes you to the learning content modal for that content area. 

### Menu bar
Put key site components on the upper menu bar. A menu dropdown should be combined with the profile button so the dropdown is on the right side of the button. It should say sign up/login, or if the user is already logged in it should display "My Learning" which takes the user to their profile when clicked. The right side of the button is a dropdown that displays the dropdown menu.

### Mega menu
Home page should have a mega menu to view the first 3 nodes in the skills tree and be able to click them to go to a page dedicated to that learning category. Menu should automatically update if the skill tree updates in the db. Within a hierarchical level, categories should be sorted by their typical order in academic programs or by difficulty, or otherwise by their popularity. For example, the Spanish language should come before Ancient Greek and Elementary Algebra should come before Abstract Algebra.

### Tree view
Add a checkbox on the list view page which allows user to expand the whole menu. 

In tree view, while the user should be able to drill down to lower tree depths, only the previous and immediate child nodes should be displayed at once. you shouldn't display the whole tree at once. All the text in the tree view should be visible and not cut off. Don't limit the final tree depth in tree view, make it so I can navigate all the way down to leaf nodes. Show parent node in tree view so user can navigating back in the hierarchy.  Show the entire tree component on the screen without having to scroll. Remove ability to pan on the skill tree, since this will be handled automatically.

Initiate the list view with the top 3 categories already opened and don't show the Knowledge root node. Users should be able to click the chevron to drill deeper or click a node to go to a list view with content and a list view just for that category.

### Footer
On the page footer put a link to the site documentation.

### Header
User should be able to reduce the top header to a hamburger button. X button should be on the far right in order to get rid of the top menu. User should be able to toggle back and forth between them.

## Knowledge tree
The knowledge tree is very important, so we should always be looking to improve it for an organized structure, completeness, and alignment with most existing learning material and learning standards. We want to be aligned with educational standards for learning each individual topic.

### Category descriptions
Use the Claude API to generate descriptions for all the 2nd and 3rd level categories. The descriptions should make the content seem interesting, but they should also be specific enough to differentiate the categories and give detail about what people are likely to learn without using jargon. Make sure the descriptons don't make false assumptions like hands-on learning (this is an online platform) or that you'll become a professional as a result of learning the content (you can't become a medical doctor as a result of learning things on this site). Text should be targeted at a specific audience. For example, early math would be targeted at younger children, and physics would be targeted at teens, and business would be targeted toward adults. Foreign languages are usually targeted toward teens and adults.

### Ratings
Users earn ratings based on how well they do on tests, and ratings are at the content area level but can be aggregated up to content area categories. Make content assessments computer adaptive. Create point system that assigns points based on how many questions you've answered correctly of each difficulty level. That way you can compare points of different category types, and if the question bank changes over time, the points are still meaningful. Also you can quit the assessment after any number of questions, you just get more points if you answer more questions and more difficult questions. No points for answering repeat questions right. Reference documentation/adaptive_assessment_system.md.

## Development
Be sure to write tests to validate any code changes and run linting and so on when it makes sense, to keep the code clean. Keep refreshing the development server so I can see the progress, but try to only keep one dev server running at a time so it doesn't use too much memory on my laptop. 

## Notifications
Notifications help the user stay on track to continue learning with the site every day. Admins can also send notifications using the admin interface. User can adjust notifications under settings.

## Database
Don't ask me to insert fake data into the database. Keep track of which data is fake and which is real so we don't get them mixed up. This is very important! I will only insert data into the database after we have validated that it is true and well-formatted.

When making changes to a table that is not empty, first create a backup table with suffix _bkp or if that table already exists then increment it like _bkp2, _bkp3 and so on. That way if there is an issue with the processing, the original table can be restored from backup.

## Data set processing
Text in csvs needs to be surrounded by quotation marks. Run processing in batch and save progress regularly (every 100 words perhaps) so that we can mitigate issues with network connectivity and api rate limiting. API rate limiting must be taken into account by implementing pauses between requests. Create recovery documentation so that if/when the code run fails I can easily start the job up again to pick up where processing left off.

### Spelling bee data
You must create a csv file to be uploaded into the spelling_words table, so the csv fields must match the names and formats found in the db. The file must be UTF-8 encoding to handle special characters in the pronunciation data. But actually the pronunciation should be phonetic respelling so that it is easier for students to remember (e.g., "able" is AY-bul). Spelling bee words are sourced from the pdfs in data/spelling_bee which were sourced from the Scripps National Spelling Bee website on 2025-08-19. You need to write code which parses the pdfs using a pdf parser, and then you clean the data by removing duplicate words, separating words that were combined with no whitespace, and deleting invalid words. You will get the dictionary definition and pronunciation from the free Dictionary API, the example sentence comes from the Claude API, and the etymology and language origins come from the Wiktionary API. You must run processing in batch and save progress regularly (every 100 words perhaps) so that we can mitigate issues with network connectivity and api rate limiting. API rate limiting must be taken into account by implementing pauses between requests. If the word doesn't return a definition from the Dictionary API then we must evaluate if it's a real spelling word--it probably isn't and needs some sort of cleaning. Exlude these words from the csv that will be uploaded to the db and instead put them in a separate csv for my review. Example sentences must use blanks instead of the word being in the sentence, and they must be contextual to the meaning of the word. Evaluate the quality of example sentences and create new, better ones if needed--use your judgment about the example sentences. You must gather the data from the APIs before assigning a word difficulty rating. Save any scripts generated to the scripts/spelling_bee folder already created. The difficulty levels need to match those found in THEORETICAL_FOUNDATIONS.md. Do not fill in missing data with generic placeholder text, but rather either leave data missing if we can't get it, or generate it with your sophisticated AI if you are able. For example, if the API does not return the etymology of a word but you know the actual origins of the word then you can generate it and add to the file--just make sure to document where you got it from by putting the source in the appropriate field in the output file. For example, if you got the etymology from Wiktionary then the etymology source field should be Wiktionary, but if you generated it using your knowledge of word histories then the etymology source field should say Claude. Valid source difficulties are "One Bee", "Two Bee", "Three Bee". Extract the full word list and process it and save it to file for my review before we start working on next steps using APIs.

## Site settings
Site should have dark mode option available in settings.

## Authentication
Make it so that when a user tries to star a learning topic or start a learning module, they must be authenticated to continue. They should also be prompted to login after they have answered 10 random questions in the sidebar (the number of random questions should be a site settings stored in a config file). Authenticate user email when a user signs up, but having the email authenticated shouldn't be required to keep using the site.  Build out the authentication system to have full features such as password reset and password view. Users should create a username on signup, and the username should display in the login menu dropdown button after signing in. Users can change their username, and it will be shown when using social content on the site.

## Security
Implement full security features. Make sure no one can do a DOM attack or pull all the data from my database to try to copy my application idea. Limit the amount of data people can get from my database at once.

## Scalability
Make sure the site can scale to many users using the site at once.

## Work style
Keep a list of your recommended project and site improvements in a file.  Keep code files organized in separate folders and increment the sorting of the code files by starting new file names with an incremented number. If there are more than 10 or 20 code files in one folder then the organization probably needs improvement. Only create documentation files when prompted to do so. Whenever you mention a script or file I should look at, always provide a clickable link so I can click to open it, or even better you should automatically open the file I am to look at. When we make modifications, finish them with a evidence that the task was completed properly--for example if we run a query then there should be a follow-up query that proves that the initial query solved the problem we were working on. I prefer to see error messages when there are site issues rather than being displayed default backup content, cached content, or using other workarounds.  We should work on fixing issues rather than creating workarounds that will lead to more issues down the road. Advise me if there are ways I can improve my working style with you.  Advise if there are ways we can reduce token usage. When you write a script that has an error in it you should change the existing script rather than create a whole new script.

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

Only once we agree on what should be done, I want you to run the code to make the changes.

When you make mistakes, tell me how to update CLAUDE.md so you don't make them again.

Auto-execute on read-only commands only.  

When a command is extra large, give a time and cost estimate. Begin by running a small amount of it and get my feedback before continuing the entire run. Use any feedback from the test run when implementing the larger run.

When you give me code to run, prompt me to verify that it ran correctly before continuing. Once it's work, remind me of which code files should be deleted, especially code files that didn't work, so we aren't keeping a huge unusable codebase.

When you give me code to run, prompt me to verify that it ran correctly before continuing. Once it's working and tested, remind me of which code files should be deleted, especially code files that didn't work, so we aren't keeping a huge unusable codebase.

Whenever you complete a task and ask me to review the work, always check for compilation errors to fix before asking me to look at the website.

Check for compilation errors to fix, run tests and fix any errors, and update the readme every time before pushing to GitHub.

Always stop and show me what changes you're planning to make in the database before making them. For example, if you're planning to add new questions to the questions table in the db, save them to a local csv file and then prompt me to review the questions before inserting them to the db.

And always stop and ask for feedback on your to do list and proposed appraoch before continuing work. After I give you feedback on your approach, update the work plan and show it to me again for feedback until I explicitly give you permission to start work on the work plan. And for theoretical topics that require knowledge of educational theory, like implementing user testing to to establish user competency ratings, make sure to create a plan and have me read it and keep giving you feedback and refining the plan before you actually write the code. You'll know I approve you to start the work when I say something like "okay the plan looks good, begin work."

Complete more mundane coding tasks before working on more tasks that require knowledge of educational theory and will require a lot of my input to design. 

As you're working, try to identify if features have already been implemented or attempted to be implemented, and then figure out if they were correctly implemented and whether they should be modified, deleted, or improved.

## Database Schema Notes
- skill_tree_nodes table contains:
  - learning_content_ids: array of content IDs
  - is_menu_leaf: boolean for tree navigation
- Questions table uses embedded options array (not separate table)
- 3 orphaned nodes exist in database (nodes with non-existent parent_ids)

## UI/UX Decisions
- Tree view uses radial/cluster layout with D3.js
- Progress indicators: Green (passed), Gold (in progress), Gray (not started), Empty circle (no content)
- Responsive design with touch/mouse pan and zoom
- List view shows hierarchical structure with top 3 categories expanded by default
- "learning modules" terminology instead of "nodes" in UI