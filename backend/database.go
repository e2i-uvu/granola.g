package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

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

	_, err = db.Exec(`INSERT INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10955272, "Henry", "Golang", "Anything", 99.0, "nerd@nerd.com")
	db.Exec(`INSERT INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 42069, "John Doe", "Javascript Quiche Eater", "Web Dev", 99.0, "nerd@nerd.com")
	db.Exec(`INSERT INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10810570, "Guts", "Python", "Front End", 99.0, "nerd@nerd.com")
	db.Exec(`INSERT INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10976160, "Spencer", "Mystique", "Devops", 99.0, "nerd@nerd.com")
	db.Exec(`INSERT INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 11006941, "Carlos", "Python Electric Boogaloo", "AI", 99.0, "nerd@nerd.com")
	db.Exec(`INSERT INTO surveys (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)`, 10985171, "Noble", "Project Management", "IOS App Dev", 99.0, "nerd@nerd.com")
	_, err = db.Exec(`INSERT INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 1, true, 5.0, 5.0, 0.0)
	if err != nil {
		InfoLogger.Println(err)
	}
	db.Exec(`INSERT INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 2, true, 5.0, 5.0, 1.0)
	db.Exec(`INSERT INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?,?,?,?,?)`, 3, true, 5.0, 5.0, -1.0)
}
