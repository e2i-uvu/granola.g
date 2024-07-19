package main

import (
	"database/sql"
	"errors"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

type Survey struct {
	PID    int    `json:"pid"`
	UvuID  int    `json:"uvuid"`
	Name   string `json:"name"`
	Lang   string `json:"lang"`
	AOI    string `json:"aoi"`
	Degree int    `json:"degree"`
	Email  string `json:"email"`
}

func GetAllPotentialInterviewees() ([]Survey, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var potential []Survey
		return potential, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	result, err := db.Query(`SELECT *
	FROM surveys s1
	WHERE NOT EXISTS (
		SELECT 1
		FROM employees e
		WHERE e.fk_survey = s1.id
		)
	AND (s1.ID = (
		SELECT MAX(ID)
		FROM surveys s2
		WHERE s2.uvuid = s1.uvuid
	))`)
	if err != nil {
		InfoLogger.Println("Unable to select people", err)
		var potential []Survey
		return potential, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var users []Survey
	for result.Next() {
		var user Survey
		err := result.Scan(&user.PID, &user.UvuID, &user.Name, &user.Lang, &user.AOI, &user.Degree, &user.Email)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []Survey
			return potential, errors.New("Unable to scan people")
		}
		users = append(users, user)
	}
	if len(users) > 0 {
		return users, nil
	}
	InfoLogger.Println("Didn't find anyone")
	return users, errors.New("didn't find anyone")
}
func GetPotential(uvuid int) (Survey, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var person Survey
		return person, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	query := "SELECT * FROM surveys WHERE uvuid = ?"
	stmt, err := db.Prepare(query)
	if err != nil {
		InfoLogger.Println("db.prepare", err)
		var person Survey
		return person, errors.New("No users match ID")
	}
	defer stmt.Close()

	rows, err := stmt.Query(uvuid)
	if err != nil {
		InfoLogger.Println("stmt.query", err)
		var person Survey
		errorString := fmt.Sprintf("No users match ID %d", uvuid)
		return person, errors.New(errorString)
	}
	defer rows.Close()

	var users []Survey
	for rows.Next() {
		var user Survey
		err := rows.Scan(&user.PID, &user.UvuID, &user.Name, &user.Lang, &user.AOI, &user.Degree, &user.Email)
		if err != nil {
			InfoLogger.Println("Rows.scan", err)
			var person Survey
			return person, errors.New("No users match ID")
		}
		users = append(users, user)
	}
	if len(users) > 1 {
		return users[len(users)-1], nil
	}
	var person Survey
	return person, errors.New("No users match ID")
}

func (user Survey) Save() error {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
	}
	defer db.Close()

	stmt, err := db.Prepare("INSERT INTO users (uvuid, name, lang, aoi, degree, email) VALUES (?,?,?,?,?,?)")
	if err != nil {
	}
	defer stmt.Close()

	_, err = stmt.Exec(user.UvuID, user.Name, user.Lang, user.AOI, user.Degree, user.Email)
	if err != nil {
	}

	return nil
}
