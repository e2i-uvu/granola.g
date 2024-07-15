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
