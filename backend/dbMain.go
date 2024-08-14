// TODO: edit surveys table to include qualtrics info and delete employees
// TODO: create status table -2: fired; -1: not invited back; 0: Complted Surveyed; 1: Pending team; 2: Assigned to team
// TODO: create project status 0: Waiting for paperwork; 1: Waiting for team; 2: Active with team assigned; 3: Finished
package main

import (
	"database/sql"
	"fmt"

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
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS surveys 
		(id INTEGER PRIMARY KEY, 
		uvuid INTEGER, 
		name TEXT, 
		lang TEXT, 
		aoi TEXT,
		degree DECIMAL(3,0),
		email TEXT)`)
	if err != nil {
		InfoLogger.Println("surveys table did not setup")
	}
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS employees
		(id INTEGER PRIMARY KEY,
		fk_survey INTEGER, 
		cancode BOOLEAN, 
		enjoyment DECIMAL(2, 0), 
		social DECIMAL(2,0), 
		status DECIMAL(2,0),
		CONSTRAINT fk_survey FOREIGN KEY (fk_survey) REFERENCES surveys(id))`)
	if err != nil {
		InfoLogger.Println("employees table did not setup")
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

	TestInserts()
}

func TestInserts() {
	db := OpenDB()
	defer db.Close()
	_, err := db.Exec(`INSERT OR IGNORE INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10955272, "Henry", "Golang", "frontend", 99.0, "nerd@nerd.com")
	if err != nil {
		fmt.Println("Did not insert 1")
	}
	_, err = db.Exec(`INSERT OR IGNORE INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 42069, "John Doe", "Javascript Quiche Eater", "backend", 99.0, "nerd@nerd.com")
	if err != nil {
		fmt.Println("Did not insert 2")
	}
	_, err = db.Exec(`INSERT OR IGNORE INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10810570, "Guts", "Python", "game_dev", 99.0, "nerd@nerd.com")
	if err != nil {
		fmt.Println("Did not insert 3")
	}
	_, err = db.Exec(`INSERT OR IGNORE INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10976160, "Spencer", "Mystique", "frontend, backend", 99.0, "nerd@nerd.com")
	if err != nil {
		fmt.Println("Did not insert 4")
	}
	db.Exec(`INSERT OR IGNORE INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 11006941, "Carlos", "Python Electric Boogaloo", "embedded", 99.0, "nerd@nerd.com")
	db.Exec(`INSERT OR IGNORE INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10985171, "Noble", "Project Management", "database", 99.0, "nerd@nerd.com")
	db.Exec(`INSERT OR IGNORE INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 1, true, 5.0, 5.0, 0.0)
	db.Exec(`INSERT OR IGNORE INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 4, true, 5.0, 5.0, 1.0)
	db.Exec(`INSERT OR IGNORE INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 5, true, 5.0, 5.0, 1.0)
	db.Exec(`INSERT OR IGNORE INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 2, true, 5.0, 5.0, 1.0)
	db.Exec(`INSERT OR IGNORE INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 3, true, 5.0, 5.0, -1.0)
	_, err = db.Exec(`INSERT OR IGNORE INTO projects (status, name, description, frontend, backend, database, game_dev, embedded) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`, 0, "Test", "Example", 1, 1, 1, 1, 1)

	if err != nil {
		InfoLogger.Printf("Didn't insert into projects %s", err)
	}
	db.Exec(`INSERT OR IGNORE INTO projects (status, name, description, frontend, backend, database, game_dev, embedded) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`, 0, "Test1", "Example1", 2, 2, 2, 2, 2)

}
