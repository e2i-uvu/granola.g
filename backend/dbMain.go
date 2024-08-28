// TODO: edit surveys table to include qualtrics info and delete employees
// TODO: create status table -2: fired; -1: not invited back; 0: Complted Surveyed; 1: Pending team; 2: Assigned to team
// TODO: create project status 0: Waiting for paperwork; 1: Waiting for team; 2: Active with team assigned; 3: Finished
package main

import (
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

func OpenDB() *sql.DB {
	// Returns a database object, make sure you defer close it
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		panic("Database not initiated properly")
	}
	return db
}

func InitSQL() {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		panic("Database not initiated properly")
	}
	defer db.Close()
	// _, err = db.Exec(`CREATE TABLE IF NOT EXISTS users
	// 	(id INTEGER PRIMARY KEY,
	// 	uvuid INTEGER,
	// 	first TEXT,
	// 	last TEXT,
	// 	role TEXT default "student",
	// 	verified TINYINT`)
	// if err != nil {
	// 	InfoLogger.Println("Users table did not setup")
	// }
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS employees 
		(id INTEGER PRIMARY KEY, 
		name TEXT, 
		email TEXT,
		uvuid INTEGER, 
		prevTeam TINYINT,
		major TEXT,
		degree DECIMAL(3,0),
		aoi TEXT,
		social Decimal(2,0),
		status INTEGER)`)
	if err != nil {
		InfoLogger.Println("Employees table did not setup")
	}
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS hours
		(fk_employee INTEGER, 
		start INTEGER,
		end INTEGER,
		CONSTRAINT fk_employee FOREIGN KEY (fk_employee) REFERENCES employees(id))`)
	if err != nil {
		InfoLogger.Println("hours table did not setup")
	}
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS projects
		(id INTEGER PRIMARY KEY, 
		status INTEGER,
		name TEXT,
		description TEXT,
		frontend INTEGER,
		backend INTEGER,
		database INTEGER,
		game_dev INTEGER,
		embedded INTEGER)`)
	if err != nil {
		InfoLogger.Println("projects table did not setup")
	}
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS teams
		(employee_id INTEGER, 
		project_id INTEGER,
		project_manager BOOLEAN,
		constraint employee_id FOREIGN KEY (employee_id) REFERENCES employees(id),
		constraint project_id FOREIGN KEY (project_id) REFERENCES projects(id))`)
	if err != nil {
		InfoLogger.Println("team table did not setup")
	}
}
