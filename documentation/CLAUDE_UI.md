# Appearance/Design
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

### Feedback
Add a feedback system, with different categories of feedback the user can select from, such as bug reports or learning content requests. Create an admin page for responding to the requests as well as a messaging history so users can see admin responses. Link the feedback system in the top menu. Add ability for user to flag content or questions that have issues.

### Admin
Make it so only admin users can see the admin dashboard. Make field to mark learning categories to hide it and all its children from users. Make this updatable in the admin section.

## Specs

### Home page
Add research-based learning facts to home page like years of schooling increases IQ. Use facts that will encourage users to want to use the site.  Make the sources clickable, link to outside pages which have high credibility and back up the claims.

### Learning category pages
Clicking on a learning category takes you to a standard category overview page that includes a category overview, a menu of child categories, and a link to a "Rate Your Knowledge" where you answer questions to earn points. Questions follow computer adaptive difficulty. Create point system that assigns points based on how many questions you've answered correctly of each difficulty level. That way you can compare points of different category types, and if the question bank changes over time, the points are still meaningful. It shows which items have been completed and allows the user to star/bookmark the category or child categories. Clicking on child categories opens the category page for that category. Clicking on child nodes takes you to the learning content modal for that content area. The url for the page should be the breadcrumb trail of the learning category hierarchy, like languages/spanish/spanish_vocabulary.

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

### Hero section
In the hero section, prompt the user to take an interests quiz to get recommended relevant learning content. If you've already taken the interests quiz then the prompt to take the interest quiz should no longer display on the home page.           

## Knowledge tree
The knowledge tree is very important, so we should always be looking to improve it for an organized structure, completeness, and alignment with most existing learning material and learning standards. We want to be aligned with educational standards for learning each individual topic.

### Category descriptions
Use the Claude API to generate descriptions for all the categories. The descriptions should make the content seem interesting, but they should also be specific enough to differentiate the categories and give detail about what people are likely to learn without using jargon. Make sure the descriptons don't make false assumptions like hands-on learning (this is an online platform) or that you'll become a professional as a result of learning the content (you can't become a medical doctor as a result of learning things on this site). Text should be targeted at a specific audience. For example, early math would be targeted at younger children, and physics would be targeted at teens, and business would be targeted toward adults. Foreign languages are usually targeted toward teens and adults.

### Ratings
Users earn ratings based on how well they do on tests, and ratings are at the content area level but can be aggregated up to content area categories. Make content assessments computer adaptive. Create point system that assigns points based on how many questions you've answered correctly of each difficulty level. That way you can compare points of different category types, and if the question bank changes over time, the points are still meaningful. Also you can quit the assessment after any number of questions, you just get more points if you answer more questions and more difficult questions. No points for answering repeat questions right. Reference documentation/adaptive_assessment_system.md.

## Authentication
Make it so that when a user tries to star a learning topic or start a learning module, they must be authenticated to continue. They should also be prompted to login after they have answered 10 random questions in the sidebar (the number of random questions should be a site settings stored in a config file). Authenticate user email when a user signs up, but having the email authenticated shouldn't be required to keep using the site.  Build out the authentication system to have full features such as password reset and password view. Users should create a username on signup, and the username should display in the login menu dropdown button after signing in. Users can change their username, and it will be shown when using social content on the site. After login user should go back to whatever page they were on before login.

## Notifications
Notifications help the user stay on track to continue learning with the site every day. Admins can also send notifications using the admin interface. User can adjust notifications under settings.

## About page
Add about page that describes the theory behind the site in broad terms, mention it's meant to be a memory palace where you can store knowledge, that it's a work in progress and be sure to contact us with feedback if you would like material added or changed and so on. Mention some of the broad learning theories cited in theoretical foundations.md, but don't go into detail about specific algorithms.