package main

import (
	"database/sql"
	"errors"
	_ "github.com/mattn/go-sqlite3"
	"log"
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
	db.Exec(`INSERT INTO users (uvuid, name, lang, aoi) VALUES (?,?,?,?)`, 10955272, "Henry", "Python", "Anything")
}

func GetUser(uvuid int) (Person, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
	}
	defer db.Close()

	query := "SELECT * FROM users WHERE uvuid = ?"
	stmt, err := db.Prepare(query)
	if err != nil {
	}
	defer stmt.Close()

	rows, err := stmt.Query(uvuid)
	if err != nil {
	}
	defer rows.Close()

	var users []Person
	for rows.Next() {
		var user Person
		log.Println(rows)
		err := rows.Scan(&user.PID, &user.UvuID, &user.Name, &user.AOI, &user.Lang)
		if err != nil {
			person := Person{UvuID: 0, PID: 0, Name: "", AOI: "", Lang: ""}
			return person, errors.New("No users match ID")
		}
		log.Println(user)
		users = append(users, user)
	}

	return users[len(users)-1], nil
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
