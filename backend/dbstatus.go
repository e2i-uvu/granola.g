package main

import (
	"database/sql"
	"errors"
)

type AllEmployee struct {
	PID       int    `json:"pid"`
	UvuID     int    `json:"uvuid"`
	Name      string `json:"name"`
	Lang      string `json:"lang"`
	AOI       string `json:"aoi"`
	CanCode   bool   `json:"cancode"`
	Enjoyment int8   `json:"enjoyment"`
	Social    int8   `json:"social"`
	Status    int8   `json:"status"`
}

func GetAllStatus() ([]AllEmployee, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var potential []AllEmployee
		return potential, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	result, err := db.Query(`SELECT e.id, s.name, s.uvuid, s.aoi, e.cancode, e.enjoyment, e.social, s.lang, e.status
	FROM employees e
	JOIN surveys s ON e.fk_survey = s.id`)
	if err != nil {
		InfoLogger.Println("Unable to select people", err)
		var potential []AllEmployee
		return potential, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var users []AllEmployee
	for result.Next() {
		var user AllEmployee
		err := result.Scan(&user.PID, &user.Name, &user.UvuID, &user.AOI, &user.CanCode, &user.Enjoyment, &user.Social, &user.Lang, &user.Status)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []AllEmployee
			return potential, errors.New("Unable to scan people")
		}
		users = append(users, user)
	}
	if len(users) > 0 {
		return users, nil
	}
	InfoLogger.Println("Didn't find anyone")
	var potential []AllEmployee
	return potential, errors.New("didn't find anyone")
}
