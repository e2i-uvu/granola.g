package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

type Response struct {
	Name string `json:"name"`
	Lang string `json:"lang"`
	AOI  string `json:"aoi"`
}

func InitSQL() {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		panic("Database not initiated properly")
	}
	defer db.Close()
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS users 
		(id INTEGER PRIMARY KEY, name TEXT, lang TEXT, aoi Text)`)
	if err != nil {
	}
	_, err = db.Exec("INSERT INTO users (name, lang, aoi) VALUES (?, ?, ?)", "Alice", "Python", "Embedded")
	if err != nil {
	} // Handle error
}

func InputUser(user Response) error {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		panic("Database not initiated properly")
	}
	defer db.Close()

	stmt, err := db.Prepare("INSERT INTO users (name, lang, aoi) VALUES (?,?,?)")
	if err != nil {
	}
	stmt.Exec(user.Name, user.Lang, user.AOI)
	return nil
}
