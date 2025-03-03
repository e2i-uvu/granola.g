# Granola.g Documentation

## Project Overview

Granola.g is an AI-powered team building and management platform specifically designed for the Innovation Academy at Utah Valley University. The system helps leaders form optimal teams based on project requirements, employee skills, and organizational constraints.

The name "Granola.g" represents the project's focus on team composition ("granola" as a mix of ingredients) and its implementation in Go (".g").

### Mission Statement
To streamline the formation and management of technical teams at UVU's Innovation Academy through intelligent, AI-driven matching of skills to project requirements.

## Core Features

### Team Building
- **Natural Language Team Creation**: Define project requirements using plain English
- **PDF Charter Parsing**: Upload project charter PDFs to automatically extract requirements
- **Skill-Based Matching**: Intelligently match employees to projects based on skills and specialties
- **Team Editing**: Fine-tune automatically generated teams through an intuitive interface
- **Team History**: Track past team compositions for analysis and improvement

### AI Assistant
- **Context-Aware Chat**: Intelligent chatbot that understands organizational structure
- **Team Building Tools**: AI functions to generate team compositions based on requirements
- **Knowledge Base**: Maintains information about the Innovation Academy and its workflows

### Payroll Management
- **Efficient Processing**: Faster and more accurate than UVU's internal accounting department
- **Employee Records**: Manage employee payment information
- **Payment Tracking**: Monitor and report on payments to team members

## System Architecture

### Frontend (Streamlit)
The user interface is built with Python Streamlit, providing a responsive and interactive experience:
- **app.py**: Main application entry point and navigation
- **teams.py**: Team management interface
- **chat.py**: AI chat functionality
- **ai.py**: OpenAI integration and function calling
- **payroll.py**: Payroll processing interface
- **users.py**: User management
- **file_upload.py**: PDF and data upload handling

### Backend (Go)
A Go HTTP server provides REST APIs for data access and business logic:
- **main.go**: Server initialization and routing
- **dbMain.go**: Database initialization and core functions
- **dbEmployees.go**: Employee data management
- **dbProject.go**: Project data handling
- **teambuilding.go**: Core team matching algorithms
- **HTTP Handlers**: Various handler functions for API endpoints

### Database (SQLite)
Persistent storage using SQLite with the following main tables:
- **employees**: Employee records including skills and availability
- **projects**: Project information and requirements
- **teams**: Team compositions linking employees to projects

### Deployment
The application is containerized using Docker and orchestrated with Docker Compose:
- **docker-compose.yml**: Main deployment configuration
- **development.yaml, staging.yaml, production.yaml**: Environment-specific configurations
- **Traefik**: Used for reverse proxy and SSL termination

## User Roles and Permissions

Granola.g implements a role-based access control system with three primary roles:

### Admin
- Full system access
- Manage users and permissions
- Run payroll operations
- Create and edit teams
- Upload project charters and employee data

### Student
- View team information
- Limited chat functionality
- View own assignments and projects

### Developer
- Enhanced system visibility
- Access to debugging information
- View system messages and raw data

## API Documentation

### Authentication
All API endpoints require HTTP Basic Authentication.

### Employee Endpoints
- `GET /employees`: Retrieve all employees
- `POST /employees`: Create or update employee records
- `POST /employeesIngest`: Bulk import employee data

### Project Endpoints
- `GET /project`: Retrieve projects
- `POST /project`: Create or update projects

### Team Endpoints
- `GET /teams`: Retrieve teams based on criteria
- `POST /teams`: Create or update team compositions

### Status Management
- `POST /hire`: Process new employee onboarding
- `POST /fire`: Handle employee offboarding
- `POST /status`: Update employee status

## Database Structure

### employees Table
Stores comprehensive employee information:
- Basic details (name, ID, email)
- Skills and specialties
- Areas of interest
- Status and availability

### projects Table
Tracks project information:
- Project name and type
- Required skills and specialties
- Team size requirements
- Project status

### teams Table
Maps employees to projects:
- Employee IDs
- Project IDs
- Team role assignments

## Installation and Configuration

### Prerequisites
- Docker and Docker Compose
- OpenAI API key with function calling capabilities

### Configuration Files
- **frontend/template.env**: Template for environment variables
- **ai.toml**: AI configuration settings

### Deployment Steps
1. Clone the repository
2. Copy template.env to .env and configure variables
3. Run with Docker Compose:
```bash
docker-compose up -d
```

## Development Guidelines

### Adding New Features
1. Implement backend logic in Go
2. Create corresponding frontend components in Streamlit
3. Update AI tools if needed

### Testing
- Backend logic can be tested using the test suite in the test directory
- Frontend should be manually tested for functionality

### Code Style
- Go code follows standard Go conventions
- Python code uses common Python best practices

## Future Roadmap

Before administrative changes at UVU slowed development, the vision for Granola.g included:
- **Complete Organizational Management**: Expansion to handle all operational aspects
- **Time Management**: Tracking and optimization of employee time allocation
- **Budget Management**: Financial planning and oversight tools
- **Advanced Analytics**: Deeper insights into team performance
- **Enhanced AI Capabilities**: More sophisticated team formation algorithms

While development has slowed, these features represent the original vision for the system.

## Troubleshooting

### Common Issues
- **Authentication Failures**: Check credentials in environment variables
- **Database Errors**: Ensure proper permissions for SQLite file
- **OpenAI Connectivity**: Verify API key and network connectivity

### Logging
- Backend logs are stored in `backend/database/app.log`
- Frontend logs through Streamlit's logging mechanisms

## Contact Information

For issues or questions, contact the Innovation Academy administrators at UVU.