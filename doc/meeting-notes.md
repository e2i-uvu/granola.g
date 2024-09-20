# Project Meeting Notes: Granola.g

## June 24th

### Project Overview
- **Project Name:** Granola.g
- **Timeline:** 6/24/24 - 8/15/24

### Sprints
- **7/1/24:** Prototype done
- **7/8/24:** Docker containers need to be done (front end and back end). Interviewing and hiring done. Everything running on VM.
- **7/15/24:** Database ready, Qualtrics survey integration.
- **7/22/24:** Team building feature ready.
- **7/29/24:** Finalize all features.
- **8/5/24:** Testing for bugs.
- **8/12/24:** Demo.

### Technology & Tools
- **Code Standards:** 
  - Function statements
  - Lots of comments
- **Tools:**
  - Discord notifications on
  - Git
  - SQLite
  - Python Black formatter (Confrom.nvim)
  - Qualtrics
  - Interview tool
  - Docker (containers for front end and back end)
  - AI for team building

### Users
- Interviewer
- Interviewee
- Team builder
- Admin

### Design Ideas

### Code Structure
- **granola.g**
  - `docker-compose.yml`
  - **Frontend (Python)**
    - `Dockerfile`
  - **Backend (Go)**

### Current Status
- Simple front end for interview process used by interviewer.
- Insert users for the Qualtrics endpoint.

### Qualtrics Survey
- Multiple choice
- Job application includes schedule submission.
- Measures:
  - Extraversion
  - Leadership and communication
  - Charisma (scale 1 to 5)

### Tasks
- **Noble:**
  - Talk to Nicole about virtual machine.
  - Get EPAF for Joshua Wright.
  - Deliver Qualtrics survey.
  - Create RACI chart.
  - Identify risks.
  - Develop project scope statement and charter.
  - Engage stakeholders.
- **Carlos:**
  - Set up development environment.
  - Work on Streamlit.
  - Collaborate with Joshua.
- **Joshua Guts:**
  - Set up development environment.
  - Familiarize with Python and Streamlit.
  - Create a feature to get someone's UVU ID and make a request to the back end.
- **Spencer:**
  - Develop Docker containers.
  - Work on Streamlit.
  - Ensure everything works on VM.
- **Henry:**
  - Develop server functions in Go to return data.
  - Work on database.

### Meeting Guidelines
- **Context Switching:**
  - Minimize subject changes.
  - Stay focused on the current topic.
  - Schedule specified times to answer questions.
  - Do initial research before asking questions.
- **Documentation:**
  - Create a file inside the repository.
  - Use Markdown for GitHub documentation.
  - Weekly task file with checkboxes.
  - Organize meeting notes for stakeholders.

## July 1st

### Questions & Decisions
- **Clocking In:**
  - If you're thinking about the project, clock in.
- **Commits:**
  - Aim for 1 commit per day per person.
  - Can include improving documentation.

## July 8th

### Meeting Structure
- **PR Review:** At the beginning of each meeting.
  - Spencer
  - Carlos
  - Guts
  - Henry

### Features & Tasks
- Qualtrics survey allows students to express their learning interests.
- Develop RACI chart.
- Carlos to develop scoring function from interview and survey data.
- AI determines when to call a function that builds a team.
- Set up a billing account for OpenAI.

## July 15th
# Granola.g Project Meeting Notes

## Meeting Agenda
- PRs
- Look at tasks, help with progress
- Questions and concerns
- Open AI billing account
- Qualtrics from Nicole
- SkillKo

## Key Points
- **PRs:**
  - Review and discuss any pull requests.
- **Tasks:**
  - Address progress and assist with any ongoing tasks.
- **Questions & Concerns:**
  - Address any questions or concerns from the team.
- **Open AI Billing Account:**
  - Discuss the need for setting up an Open AI billing account.
- **Qualtrics:**
  - Update from Nicole on the Qualtrics survey.
- **SkillKo:**
  - Discussion on the SkillKo tool.

## Task Status
- **Hiring Status:**
  - 1 hired, 0 nothing yet, -1, -2

## Tasks
- **Noble:**
  - Update TODO list.
  - Write a proposal for the need for Open AI.
  - Set deadline for VM setup: At the latest, the 31st, or we won't be able to continue without VM.
  - Traefik setup without VM.
  - Need API and documentation for SkillKo ASAP.

- **Henry:**
  - **Completed:**
    - User authentication
  - Backend for Hiring page
  - Backend for Status
  - Backend for Firing

- **Spencer:**
  - Front end of the app
  - Front end AI chat page and manual entry
  - Front end Hiring and Status page
  - Front end Firing page
  - Team building algorithm
  - SkillKo integration

- **Carlos:**
  - Grading and hiring score
  - Displaying data with `ST.data_frame`
  - Collaborate with Spencer on code comments
  - Team building algorithm
  - SkillKo integration

- **Guts:**
  - User experience for the front end
  - Development of pages
  - Collaborate with Spencer on code comments
  - Team building algorithm

## Comments
- The team building algorithm will improve over time; it doesn't need to be perfect for the first release, it just needs to build teams.
- We can't continue without VM by the end of the month.

## July 22nd

# Meeting Notes

### PR's
- Look at TODO list
- Roadblocks:
  - Qualtrics: What exactly do we need?

### Updates:
- **Henry**:
  - Did a bunch of back-end refactoring.
  - Created back-end functionality for hiring, firing, and status updates.
  - Made a way to fire an employee.
  - Pre-interview tasks.
  - TODO list.

- **Spencer**:
  - Worked on UI and AI tasks.

- **Carlos**:
  - Worked on the front-end for firing employees.

- **Noble**:
  - Send message about updating the TODO list.

### Action Items:
- TODO: We need to complete the back end.

### Additional Notes:
- Meeting with Jeremiah and Nicole:
  - Virtual machine: We can't do anything beyond a certain point. We technically shouldn't have proceeded this far without the virtual machine to test everything.
  - Qualtrics survey: Remove this and add a Streamlit survey on the back end.

# Meeting Notes: Nicole and Jeremiah

### Topics Discussed:

- **VM Machine**:
  - Focus on security and testing.
  - Necessary for moving forward with the project due to security and FERPA regulations.

- **SkillKo**:
  - Comparison between Qualtrics and Streamlit for the survey platform.

- **Future Involvement**:
  - Potential collaboration with marketing and business students.

### Key Points:

- Due to **security and FERPA regulations**, we can't continue without the virtual machine (VM).
- We've only been provided with basic information so far.
- Exploring options such as **Google Cloud** and **Amazon AWS**.
  - AWS EC2 instance might cost around $5 per month.
  - No personal data will be collected; participants must opt in.

### Action Items:

- Write a proposal outlining the need for a virtual machine (VM).
- Develop the **team-building algorithm** into a science.

### July 29th
# Team Meeting Notes

### Passwords:
- Admin password: `innovation`
- Developer password: `arch`

### Tasks:
- Finish the **team building algorithm**.

### Deployment:
- Push to **dev** branch before pushing to **main** branch.
- Final push:
  - Need a function to call when **Team Building** is finished, returning a team.
  - Polish up the front end.
  - **Interviewing SkillKo** won't happen; instead, use info students provide, such as Wolverine Track percentages.
  - **AI Chat** feature.
  - **Optimal** team configurations.
  - Write tests for the software.
  - Address **availability** aspects.

### TODO:

- **Spencer**:
  - Added different pages for students, admins, and developers.
  - Chat interface for AI.
  - Team building algorithm.

- **Henry**:
  - Team building algorithm.
  - Back end for availability.
  - Write Go tests.

- **Carlos**:
  - Polish the front end.
  - Write tests.
  - Interviewing tasks.

- **Guts**:
  - Polish the front end.
  - Front end availability functionality.

- **Noble**:
  - Send a message to Nicole and Jeremiah about **SkillKo** not happening.
  - Coordinate communication for deployment meeting.

### August 5th 
# Meeting Notes

### General Notes:
- Tasks are broad and mostly provide direction. If you're unsure whether your task is complete, break it down into smaller tasks and add them to the TODO list.
- Need a front-end form, and an entry point API for surveys and projects.
- If issues arise, get on calls this week. We don’t want one person feeling overwhelmed at the last minute.
- Let's discuss progress this week, and if you need help, communicate early.

### Deployment:
- Consider scores for enjoyment, social interaction, coding ability, and Wolverine Track.

### TODO:

- **Henry**:
  - (No specific tasks listed)

- **Spencer**:
  - Generate number scores, send back JSON with 2 strings and 5 integers.
  - Work on deployment.

- **Carlos**:
  - (No specific tasks listed)

- **Guts**:
  - (No specific tasks listed)

- **Noble**:
  - Help Nicole and Jeremiah understand that the team-building part of the project won't be possible without an OpenAI key.

### Issues:
- (No specific issues listed)

### Status Report:
- (No specific updates provided)

### Progress Report:
- (No specific updates provided)

### August 8th
# Major Change of Scope

### No More Interviews:
- No more students interviewing other students.

### Qualtrics:
- We'll use a Qualtrics survey for every student. We can sit down to design the questions, ensuring we control the data.
- Brainstorm potential questions.
- Give Jeremiah a list of what data points we think will be useful.

### OpenAI API:
- Proceed with the plan assuming a **yes** for using the API.
- How much will it cost for just the team-building part? Ask Spencer.
- Only use the API for the **team-building** aspect.

### Hours:
- Remind the team not to exceed 28 hours per week.
- If someone goes over a third time, there's no way to prevent them from being fired — it will happen automatically.
- He’s using up all his favors; aim for 25 hours to be safe.

### Study Groups:
- Meeting with Jackson:
  - End the current project, restart, and recruit a new team.
  - Jackson can either be the team lead and start from scratch in the fall, or the project can be done.
  - Determine the progress, scope, and resources required.
  - Ask: Do you want to continue? If so, would you like to be the team lead for the project?

### Major Details:
- **Major**: Computer Science.

### Meeting with Jeremiah and Spencer:
- We need to **change the due date** of the project.

### August 12th 
# Meeting Notes - August 12th

### Changes:
- Changes to the algorithm: Less data from Qualtrics.
- We need to focus on completing the team-building feature with the AI chatbot.

### Timeline:
- Deadline: End of August.

### Budget:
- (No specific budget details provided)

### Scope:
- (No specific scope details provided)

### Refactoring Data:
- Teams must have at least one person with experience, and the rest of the team will be formed randomly if they meet the requirements.

### TODO:

- **Noble**:
  - (No specific tasks listed)

- **Spencer**:
  - Generate CSV data from Qualtrics survey.
  - Create a data pipeline to take data from Qualtrics and insert it into the database.
  - Refactor code.
  - Work on OpenAI chatbot integration.

- **Guts**:
  - Help Spencer with the data pipeline.
  - Add data to the database.
  - Refactor code.

- **Henry**:
  - (No specific tasks listed)

- **Carlos**:
  - Work on Playwright testing.
  - Refactor testing code.
  - Create a bot to test the AI chatbot.

### August 19th 
# Meeting Notes - August 19th

### Agenda:

1. **Walkthrough of Website**:
   - Reviewed the current state of the website.
   - Discussed the functionality and any issues that need to be addressed.
   - Identified future steps for further development and improvements.

2. **Accountability Plan**:
   - Establish a clear **accountability plan** to ensure all team members stay on track.
   - Define specific tasks and deadlines for each team member.
   - Regular check-ins to monitor progress and address roadblocks.
   - Encourage transparency in reporting challenges or delays.

3. **Communication Plan**:
   - Set up a structured **communication plan** to keep the team aligned.
   - Use a combination of regular meetings and asynchronous communication (emails, chats).
   - Define escalation paths for any urgent issues.
   - Ensure open channels for feedback and collaboration across the team.
### Request to allow on wifi
# Subject: Request to Allow Domain "E2i.live" on UVU Wi-Fi Network

Hey Aaron,

I work for the Innovation Academy in the E2i program as a project manager. One of the teams I am on created the domain **E2i.live** for a project. I am writing to request that the domain "E2i.live" be allowed on the UVU Wi-Fi network.

Please let me know if you need any further information or if there are any additional steps I need to take.

Best regards,  
Noble Beazel

### August 29th 
# Team Building Project: Defining Future Scope and Key Features

### 1. Introduction

#### Purpose of the Meeting:
- Define the future direction of the Team Building project.
- Identify key features and priorities.
- Establish communication processes with students.

### 2. Key Action Items:

- **Marketing Integration**:
  - Marketing should be added by Friday at the latest.

- **Communication with Students**:
  - Automate email communication through the chatbot to handle availability and team assignments.
  - The chatbot will:
    - Send emails on our behalf.
    - Collect and manage availability.
    - Insert student IDs and present teams by UVU ID number in a spreadsheet.
  
- **Email Management**:
  - Allow **Nicole** to edit the emails if needed before sending.
  - Determine the necessary information for the email.
  - Define the schedule for when the emails will be sent.

### 3. Team Assignment Process:
- Teams will be assigned based on availability and other criteria.
- The system should send an email to each team, but there will be an opportunity for review before the emails are sent.

### 4. Student Involvement:
- Ensure the system is easy to use for students participating in the team-building process.
