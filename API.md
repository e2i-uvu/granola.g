# Granola.g API Documentation

This document provides detailed information about the REST API endpoints available in the Granola.g platform.

## Authentication

All API endpoints require HTTP Basic Authentication:

```
Username: Username
Password: Password
```

These credentials are configured in the backend code. In a production environment, these should be changed to secure values provided via environment variables.

## Base URL

The base URL for all API endpoints is:

```
http://localhost:8081/
```

When deployed with Docker Compose, the URL would be:

```
http://go_server:8081/
```

## Employee Endpoints

### Get All Employees

Retrieves a list of all employees in the system.

- **URL**: `/employees`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**: JSON array of employee objects
  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "uvid": "10012345",
      "email": "john.doe@example.com",
      "speciality": "Backend",
      "aoi": "Web Development",
      "degreepercent": 75,
      "teambefore": 1,
      "major": "Computer Science",
      "majoralt": "",
      "social": 3,
      "status": 0
    },
    ...
  ]
  ```

### Create/Update Employee

Creates a new employee or updates an existing one.

- **URL**: `/employees`
- **Method**: `POST`
- **Request Body**: JSON object with employee data
  ```json
  {
    "name": "Jane Smith",
    "uvid": "10012346",
    "email": "jane.smith@example.com",
    "speciality": "Frontend",
    "aoi": "Mobile Development",
    "degreepercent": 50,
    "teambefore": 0,
    "major": "Information Technology",
    "majoralt": "Design",
    "social": 4,
    "status": 0
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: `{"message": "Employee created successfully"}`

### Bulk Import Employees

Imports multiple employees from a data source.

- **URL**: `/employeesIngest`
- **Method**: `POST`
- **Request Body**: JSON array of employee objects
- **Success Response**:
  - **Code**: 200
  - **Content**: Status message with count of imported records

## Team Endpoints

### Get Teams

Retrieves teams based on specified criteria.

- **URL**: `/teams`
- **Method**: `GET`
- **Request Body**: JSON object with team formation criteria
  ```json
  {
    "project_name": "Web Portal",
    "project_type": "Web",
    "total_employees": 5,
    "employees": [
      {"employee": "Frontend", "amount": 2},
      {"employee": "Backend", "amount": 2},
      {"employee": "Database", "amount": 1}
    ]
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: JSON array of employee objects matching the criteria

### Create Team

Creates a new team by assigning employees to a project.

- **URL**: `/teams`
- **Method**: `POST`
- **Request Body**: JSON object defining the team
  ```json
  {
    "project_name": "Mobile App",
    "project_type": "Mobile",
    "employees": [
      {"employee": 1},
      {"employee": 2},
      {"employee": 3}
    ]
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: Status message

## Project Endpoints

### Get Projects

Retrieves all projects or a specific project.

- **URL**: `/project`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**: JSON array of project objects
  ```json
  [
    {
      "id": 1,
      "name": "Web Portal",
      "project_type": "Web",
      "status": 0,
      "aoi": "Education",
      "leads": "[1, 2]"
    },
    ...
  ]
  ```

### Create/Update Project

Creates a new project or updates an existing one.

- **URL**: `/project`
- **Method**: `POST`
- **Request Body**: JSON object with project data
  ```json
  {
    "name": "Mobile App",
    "project_type": "Mobile",
    "status": 0,
    "aoi": "Healthcare",
    "leads": "[3, 4]"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: Status message

## Employee Status Endpoints

### Hire Employee

Processes a new employee hire.

- **URL**: `/hire`
- **Method**: `POST`
- **Request Body**: JSON object with employee data
- **Success Response**:
  - **Code**: 200
  - **Content**: Status message

### Fire Employee

Processes an employee termination.

- **URL**: `/fire`
- **Method**: `POST`
- **Request Body**: JSON object with employee ID
  ```json
  {
    "id": 1
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: Status message

### Update Employee Status

Updates an employee's status.

- **URL**: `/status`
- **Method**: `POST`
- **Request Body**: JSON object with employee ID and new status
  ```json
  {
    "id": 1,
    "status": 2
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: Status message

## Error Responses

All endpoints can return the following error responses:

### Unauthorized

- **Code**: 401
- **Content**: `Unauthorized`
- **Description**: Authentication credentials are missing or invalid

### Bad Request

- **Code**: 400
- **Content**: Error message detailing the issue
- **Description**: The request was malformed or contained invalid data

### Internal Server Error

- **Code**: 500
- **Content**: Error message
- **Description**: An error occurred on the server

## API Usage Examples

### Creating a Team Based on Project Requirements

```bash
curl -X GET http://localhost:8081/teams \
  -u "Username:Password" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "E-commerce Platform",
    "project_type": "Web",
    "total_employees": 6,
    "employees": [
      {"employee": "Frontend", "amount": 2},
      {"employee": "Backend", "amount": 2},
      {"employee": "Database", "amount": 1},
      {"employee": "Full stack", "amount": 1}
    ]
  }'
```

### Updating an Employee's Status

```bash
curl -X POST http://localhost:8081/status \
  -u "Username:Password" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 5,
    "status": 1
  }'
```

## Implementation Notes

- All endpoints are implemented in the corresponding handler files in the backend directory
- Request validation occurs in each handler function
- Database operations are abstracted in the db*.go files