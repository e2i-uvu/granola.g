# Granola.g

Team Building Platform for UVU Innovation Academy

## Overview

Granola.g is a comprehensive team building interface designed specifically for the Innovation Academy at Utah Valley University (UVU). The platform leverages AI to intelligently build and manage teams based on project requirements, employee skills, and organizational needs.

### Target Audience
- Academy Leaders
- Tech-adjacent Leads
- Developers
- Program Administrators

### Key Features
- **AI-Powered Team Building**: Create teams based on natural language descriptions
- **PDF Charter Parsing**: Upload project charter PDFs to automatically extract requirements and build teams
- **Interactive Chat**: A context-aware chatbot that understands the organization
- **Payroll Management**: Streamlined payroll processing that exceeds UVU's internal accounting department in speed and accuracy
- **Team Management**: Track and adjust team compositions in real-time

## System Architecture

The application follows a modern, containerized architecture:

- **Frontend**: Python Streamlit application providing an interactive user interface
- **Backend**: Go server exposing RESTful APIs for data access and business logic
- **Database**: SQLite database for persistent storage
- **Deployment**: Docker and Docker Compose for containerization and orchestration

## Installation & Setup

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- Environment variables configuration

### Deployment
1. Clone the repository
2. Configure environment variables (see `frontend/template.env`)
3. Run with Docker Compose:
```bash
docker-compose up -d
```

See the development, staging, and production YAML files for different deployment configurations.

## Configuration
The application requires several environment variables to be set:
- Backend authentication credentials
- OpenAI API keys
- System configuration parameters

Configuration is managed through TOML files for the AI components and environment variables for system settings.

## Current Status

Following administrative changes at UVU, development has significantly slowed. The original vision was to create a fully-featured management tool for the Innovation Academy that would handle everything from team formation to time and budget management.

## Documentation

For more detailed information, please refer to the docs directory:
- `/doc/` - Project documentation and proposals
- `/frontend/README.md` - Frontend specific documentation

## License
See LICENSE file for details.