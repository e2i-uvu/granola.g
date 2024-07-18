package main

import (
	"database/sql"
	"errors"
)

type potentialFire struct {
	PID       int    `json:"pid"`
	UvuID     int    `json:"uvuid"`
	Name      string `json:"name"`
	Lang      string `json:"lang"`
	AOI       string `json:"aoi"`
	CanCode   bool   `json:"cancode"`
	Enjoyment int8   `json:"enjoyment"`
	Social    int8   `json:"social"`
}

func GetPotentialFires() ([]potentialFire, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var potential []potentialFire
		return potential, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	result, err := db.Query(`SELECT e.id, s.name, s.uvuid, s.aoi, e.cancode, e.enjoyment, e.social, s.lang
	FROM employees e
	JOIN surveys s ON e.fk_survey = s.id
	WHERE e.status > 0`)
	if err != nil {
		InfoLogger.Println("Unable to select people", err)
		var potential []potentialFire
		return potential, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var users []potentialFire
	for result.Next() {
		var user potentialFire
		err := result.Scan(&user.PID, &user.Name, &user.UvuID, &user.AOI, &user.CanCode, &user.Enjoyment, &user.Social, &user.Lang)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []potentialFire
			return potential, errors.New("Unable to scan people")
		}
		users = append(users, user)
	}
	if len(users) > 0 {
		return users, nil
	}
	InfoLogger.Println("Didn't find anyone")
	var potential []potentialFire
	return potential, errors.New("didn't find anyone")
}
