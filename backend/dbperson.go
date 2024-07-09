package main

import (
	"database/sql"
	"errors"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

type Person struct {
	PID   int    `json:"pid"`
	UvuID int    `json:"uvuid"`
	Name  string `json:"name"`
	Lang  string `json:"lang"`
	AOI   string `json:"aoi"`
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
		person := Person{UvuID: 0, PID: 0, Name: "", Lang: "", AOI: ""}
		return person, errors.New("No users match ID")
	}
	defer stmt.Close()

	rows, err := stmt.Query(uvuid)
	if err != nil {
		InfoLogger.Println("stmt.query", err)
		person := Person{UvuID: 0, PID: 0, Name: "", Lang: "", AOI: ""}
		errorString := fmt.Sprintf("No users match ID %d", uvuid)
		return person, errors.New(errorString)
	}
	defer rows.Close()

	var users []Person
	for rows.Next() {
		var user Person
		err := rows.Scan(&user.PID, &user.UvuID, &user.Name, &user.Lang, &user.AOI)
		if err != nil {
			InfoLogger.Println("Rows.scan", err)
			person := Person{UvuID: 0, PID: 0, Name: "", Lang: "", AOI: ""}
			return person, errors.New("No users match ID")
		}
		users = append(users, user)
	}
	if len(users) > 1 {
		return users[len(users)-1], nil
	}
	person := Person{UvuID: 0, PID: 0, Name: "", Lang: "", AOI: ""}
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
