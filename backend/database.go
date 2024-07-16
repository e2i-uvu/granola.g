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
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS users 
		(id INTEGER PRIMARY KEY, 
		uvuid INTEGER, 
		name TEXT, 
		lang TEXT, 
		aoi Text)`)
	if err != nil {
	}
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS interviews
		(id INTEGER PRIMARY KEY,
		fkuser INTEGER, 
		cancode BOOLEAN, 
		enjoyment DECIMAL(2, 0), 
		social DECIMAL(2,0), 
		hired DECIMAL(2,0), 
		CONSTRAINT fk_user FOREIGN KEY (fkuser) REFERENCES users(id))`)
	if err != nil {
	}

	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10955272, "Henry", "Golang", "Anything")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 42069, "John Doe", "Javascript Quiche Eater", "Web Dev")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10810570, "Guts", "Python", "Front End")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10976160, "Spencer", "Mystique", "Devops")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 11006941, "Carlos", "Python Electric Boogaloo", "AI")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10985171, "Noble", "Project Management", "IOS App Dev")
	db.Exec(`INSERT INTO interviews (fkuser, cancode, enjoyment, social, hired) VALUES (?,?,?,?, ?)`, 1, true, 5.0, 5.0, 0.0)
	db.Exec(`INSERT INTO interviews (fkuser, cancode, enjoyment, social, hired) VALUES (?,?,?,?, ?)`, 2, true, 5.0, 5.0, 1.0)
	db.Exec(`INSERT INTO interviews (fkuser, cancode, enjoyment, social, hired) VALUES (?,?,?,?, ?)`, 3, true, 5.0, 5.0, -1.0)
}
