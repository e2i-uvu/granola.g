# Granola.g Database Documentation

This document outlines the database structure and relationships for the Granola.g team building platform.

## Overview

Granola.g uses SQLite as its database engine, chosen for simplicity, minimal configuration requirements, and ease of deployment. The database file is located at:

```
backend/database/database.db
```

## Database Schema

### employees Table

Stores information about all employees in the Innovation Academy.

| Column         | Type    | Description                                           |
|----------------|---------|-------------------------------------------------------|
| id             | INTEGER | Primary key, unique identifier for employee           |
| name           | TEXT    | Employee's full name                                  |
| uvid           | TEXT    | UVU ID number                                         |
| email          | TEXT    | Employee's email address                              |
| speciality     | TEXT    | Primary technical specialty                           |
| aoi            | TEXT    | Area of interest                                      |
| degreepercent  | INTEGER | Percentage of degree completion                       |
| teambefore     | INTEGER | Boolean (0/1) indicating previous team experience     |
| major          | TEXT    | Primary major or field of study                       |
| majoralt       | TEXT    | Secondary major or field of study                     |
| social         | INTEGER | Social preference score (1-5)                         |
| status         | INTEGER | Current status (0=available, 1=assigned, 2=inactive)  |

### projects Table

Stores information about projects in the Innovation Academy.

| Column        | Type    | Description                                        |
|---------------|---------|---------------------------------------------------|
| id            | INTEGER | Primary key, unique identifier for project         |
| name          | TEXT    | Project name                                       |
| project_type  | TEXT    | Type of project (Web, Mobile, etc.)                |
| status        | INTEGER | Project status (0=active, 1=completed, 2=cancelled)|
| aoi           | TEXT    | Area of interest for the project                   |
| leads         | TEXT    | JSON array of employee IDs serving as leads        |

### teams Table

Maps employees to projects, creating team compositions.

| Column      | Type    | Description                                     |
|-------------|---------|------------------------------------------------|
| id          | INTEGER | Primary key, unique identifier for team mapping |
| employee_id | INTEGER | Foreign key reference to employees.id           |
| project_id  | INTEGER | Foreign key reference to projects.id            |
| role        | TEXT    | Role of the employee on the team               |

## Relationships

- One employee can be part of multiple teams (one-to-many)
- One project can have multiple team members (one-to-many)
- The teams table implements a many-to-many relationship between employees and projects

## Data Management

### Data Import

Employee data can be imported in bulk using the `/employeesIngest` endpoint, which expects CSV or JSON data with the appropriate fields.

### Data Integrity

- The database maintains referential integrity through foreign key constraints
- Employee status is tracked to prevent over-allocation to teams
- Project status is used to filter active vs. completed projects

## Query Patterns

The most common query patterns include:

1. Finding available employees with specific skills
   ```sql
   SELECT * FROM employees WHERE status = 0 AND speciality = ?
   ```

2. Retrieving all members of a specific team
   ```sql
   SELECT e.* FROM employees e 
   JOIN teams t ON e.id = t.employee_id
   WHERE t.project_id = ?
   ```

3. Retrieving all projects for a specific employee
   ```sql
   SELECT p.* FROM projects p
   JOIN teams t ON p.id = t.project_id
   WHERE t.employee_id = ?
   ```

## Database Maintenance

### Backup

Regular backups of the database should be performed, especially before deployment or major changes:

```bash
cp backend/database/database.db backend/database/database.db.bak
```

### Schema Updates

The database schema is initialized in `dbMain.go`. Any schema changes should be carefully managed to preserve existing data.