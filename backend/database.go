package main

import (
	"database/sql"
	"errors"
	_ "github.com/mattn/go-sqlite3"
)

type Person struct {
	PID   int    `json:"pid"`
	UvuID int    `json:"uvuid"`
	Name  string `json:"name"`
	Lang  string `json:"lang"`
	AOI   string `json:"aoi"`
}

func InitSQL() {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		panic("Database not initiated properly")
	}
	defer db.Close()
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS users 
		(id INTEGER PRIMARY KEY, uvuid INTEGER, name TEXT, lang TEXT, aoi Text)`)
	if err != nil {
	}
	if err != nil {
	}
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10955272, "Henry", "Golang", "Anything")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 42069, "John Doe", "Javascript Quiche Eater", "Web Dev")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10810570, "Guts", "Python", "Front End")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10976160, "Spencer", "Mystique", "Devops")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 11006941, "Carlos", "Python Electric Boogaloo", "AI")
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10985171, "Noble", "Project Management", "IOS App Dev")
}

func GetUser(uvuid int) (Person, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		person := Person{UvuID: 0, PID: 0, Name: "", AOI: "", Lang: ""}
		return person, errors.New("No users match ID")
	}
	defer db.Close()

	query := "SELECT * FROM users WHERE uvuid = ?"
	stmt, err := db.Prepare(query)
	if err != nil {
		InfoLogger.Println("db.prepare", err)
		person := Person{UvuID: 0, PID: 0, Name: "", AOI: "", Lang: ""}
		return person, errors.New("No users match ID")
	}
	defer stmt.Close()

	rows, err := stmt.Query(uvuid)
	if err != nil {
		InfoLogger.Println("stmt.query", err)
		person := Person{UvuID: 0, PID: 0, Name: "", AOI: "", Lang: ""}
		return person, errors.New("No users match ID")
	}
	defer rows.Close()

	var users []Person
	for rows.Next() {
		var user Person
		err := rows.Scan(&user.PID, &user.UvuID, &user.Name, &user.AOI, &user.Lang)
		if err != nil {
			InfoLogger.Println("Rows.scan", err)
			person := Person{UvuID: 0, PID: 0, Name: "", AOI: "", Lang: ""}
			return person, errors.New("No users match ID")
		}
		users = append(users, user)
	}
	if len(users) > 1 {
		return users[len(users)-1], nil
	}
	person := Person{UvuID: 0, PID: 0, Name: "", AOI: "", Lang: ""}
	return person, errors.New("No users match ID")
}

func (user Person) Save() error {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
	}
	defer db.Close()

	stmt, err := db.Prepare("INSERT INTO users (uvuid, name, lang, aoi) VALUES (?, ?,?,?)")
	if err != nil {
	}
	defer stmt.Close()

	_, err = stmt.Exec(user.UvuID, user.Name, user.Lang, user.AOI)
	if err != nil {
	}

	return nil
}
