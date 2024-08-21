- [ ] Plan the project
- [ ] Create a front end with [Streamlit](https://streamlit.io/) for gathering information
- [ ] Documents
- [ ] Meetings times
- [ ] Golang???
Here’s the list formatted with checkboxes for GitHub Markdown:

---

## Future Todos

- [ ] Extend `st.column_config` to replicate when to work
- [ ] What ports need to be open to traefik on backend?


---

All **TODO** ... **FIX** comments throughout project:

```
frontend/app.py|134 col 7| TODO: Will change to username and password
frontend/test/interviewFinish.py|19 col 3| TODO: Change parameter from string to dictionary/json
frontend/test/interviewFinish.py|56 col 7| FIX: Test cases where copied directly from the InterviewStartHandler test,
frontend/test/interviewFinish.py|89 col 7| FIX: Returning error. Is the "cancode" value wrong?
frontend/test/main.py|7 col 3| TODO: Add SQL Injection tests???
frontend/test/interviewStart.py|19 col 3| TODO: Change parameter from string to dictionary/json
frontend/test/interviewStart.py|55 col 7| FIX: The following test cases don't work
frontend/employees.py|220 col 3| TODO: Guts this will be the status page for current employees
frontend/weightConfig.py|8 col 3| TODO: Add logging functionality?
frontend/weightConfig.py|11 col 3| TODO:  Maybe make this configFilePath a env?
frontend/weightConfig.py|63 col 3| FIX: Couldn't find a way to modify the value of the sliders from outside of the sliders object
frontend/ai.py|137 col 25| TODO:
frontend/chat.py|60 col 58| TODO:
backend/teambuilding.go|1 col 4| TODO: Replace algorithm to include one carry over employee and the rest as randomized
backend/httpHire.go|1 col 4| TODO: update post so that there's additional checking logic
backend/scoring.go|1 col 4| TODO: Delete scoring algorith
backend/httpInterview.go|1 col 4| TODO: Get Rid of all this
backend/main.go|40 col 30| INFO: ", log.Ldate|log.Ltime|log.Lshortfile)
backend/dbInterview.go|1 col 4| TODO: Delete all of this
backend/dbSurveys.go|1 col 4| TODO: Update to update instead of reinsert information
backend/dbMain.go|1 col 4| TODO: edit surveys table to include qualtrics info and delete employees
backend/dbMain.go|2 col 4| TODO: create status table -2: fired; -1: not invited back; 0: Complted Surveyed; 1: Pending team; 2: Assigned to team
backend/dbMain.go|3 col 4| TODO: create project status 0: Waiting for paperwork; 1: Waiting for team; 2: Active with team assigned; 3: Finished
```


---

## Tasks: 6/24-7/1

### Noble:
- [ ] Talk to Nicole about the virtual machine
- [x] Get EPAF for Joshua Wright
- [ ] Deliver Qualtrics survey
- [x] Create RACI chart
- [x] Identify risks
- [x] Draft project scope statement and charter
- [x] Identify stakeholders

### Carlos:
- [x] Set up development environment
- [x] Work on Streamlit features
- [x] Create a simple application to get someone's UVU ID and make a request to the back end
- [x] Collaborate with Joshua

### Joshua Guts:
- [x] Set up development environment
- [x] Familiarize with Python and Streamlit
- [x] Create a simple application to get someone's UVU ID and make a request to the back end
- [x] Collaborate with Carlos

### Spencer:
- [x] Develop Docker containers
- [ ] Work on Streamlit integration
- [x] Ensure everything works on the VM
- [x] Get let's encrypt certs working

### Henry:
- [x] Implement server communication using Go
- [x] Work on database integration

---
## Tasks: 7/15-7/22 
# General:

- [ ]  Describe what our website is actually doing in markdown on the guide page
- [ ]  We just need to build out the pages
- [ ]  ???layer of abstraction for making requests to the backend (so that we can run it in dev mode to make it faster for prototyping)

### Noble:
- [x]  Update TODO list.
- [x]  Write a proposal for the need for Open AI.
- [x]  Set deadline for VM setup (latest by 31st).
- [ ]  Traefik setup without VM.
- [ ]  Need API and documentation for SkillKo ASAP.

### Henry:
- [x]  User authentication 
- [x]  Backend for Hiring page 
- [x]  Backend for Status 
- [x]  Backend for Firing 

### Spencer:
- [x]  Front end of the app.
- [x]  Front end AI chat page and manual entry.
- [x]  Front end Hiring and Status page.
- [x]  Front end Firing page.
- [ ]  Team building algorithm.
- [ ]  SkillKo integration.

### Carlos:
- [x]  Grading and hiring score.
- [x]  Displaying data with `ST.data_frame`.
- [x]  Collaborate with Spencer on code comments.
- [x]  Team building algorithm.
- [ ]  SkillKo integration.

### Guts:
- [x]  User experience for the front end.
- [x]  Development of pages.
- [x]  Collaborate with Spencer on code comments.
- [ ]  Team building algorithm.

---
### Tasks: 7/29/24 - 8/5/24

### Spencer:
  - [ ] Finish deployment
  - [x] Chat interface for AI
  - [x] Team building algorithm

### Henry:
  - [x] Team building algorithm
  - [ ] Back end for availability
  - [ ] GO Tests

### Carlos:
  - [x] Polish up front end
  - [x] Write tests
  - [x] Interviewing

### Guts:
  - [ ] Polish front end
  - [ ] Front end availability

### Noble:
  - [x] Send message to Nicole and Jeremiah about SkillKo not happening
  - [ ] Finish deployment
---
### Tasks: 8/12/24 - 8/19/24

### Spencer:
  - [ ] Create CSV data from Qualtrics survey
  - [ ] Make Data Pipeline
  - [ ] Add to database
  - [x] Refactor
  - [x] Open AI Chat bot
  - [x] Unblock e2i.live website on uvu wifi 

### Henry:
  - [ ] 
  - [ ] 
  - [ ] 

### Carlos:
  - [x] Playwright Testing
  - [x] Refactor Tests
  - [ ] Make bot to test AI chat bot
  - [ ] Ai chat box tests
  - [ ] Employee page tests
  - [ ] Availability tests
  - [ ] Team building tests
  - [ ] Payroll tests

### Guts:
  - [ ] Help Spencer make Data pipeline
  - [ ] Add to data base
  - [ ] Refactor code

### Noble:
  - [x] Message each team member
  - [x] Update TODO
  - [ ] Update timeline
  - [ ] Make documents explaining project scope changes
  - [x] Message Alsharif about getting website approved for UVU wifi
  - [ ] Contact Aaron Barrett about E2i Domain

