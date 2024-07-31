package main

import (
	"database/sql"
	"errors"
)

type PotentialHire struct {
	PID       int    `json:"pid"`
	UvuID     int    `json:"uvuid"`
	Name      string `json:"name"`
	Lang      string `json:"lang"`
	AOI       string `json:"aoi"`
	CanCode   bool   `json:"cancode"`
	Enjoyment int8   `json:"enjoyment"`
	Social    int8   `json:"social"`
	Status    int8   `json:"status"`
	Score     int8   `json:"score"`
}

type EmployeeStatus struct {
	PID    int `json:"pid"`
	Status int `json:"status"`
}

func GetPendingEmployee() ([]PotentialHire, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var potential []PotentialHire
		return potential, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	result, err := db.Query(`SELECT e.id, s.name, s.uvuid, s.aoi, e.cancode, e.enjoyment, e.social, s.lang, e.status
	FROM employees e
	JOIN surveys s ON e.fk_survey = s.id
	WHERE e.status = 1`)
	if err != nil {
		InfoLogger.Println("Unable to select people", err)
		var potential []PotentialHire
		return potential, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var users []PotentialHire
	for result.Next() {
		var user PotentialHire
		err := result.Scan(&user.PID, &user.Name, &user.UvuID, &user.AOI, &user.CanCode, &user.Enjoyment, &user.Social, &user.Lang, &user.Status)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []PotentialHire
			return potential, errors.New("Unable to scan people")
		}
		GenerateScore(&user)
		users = append(users, user)
	}
	if len(users) > 0 {
		return users, nil
	}
	InfoLogger.Println("Didn't find anyone")
	var potential []PotentialHire
	return potential, errors.New("didn't find anyone")
}
func GetPotentialHires() ([]PotentialHire, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var potential []PotentialHire
		return potential, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	result, err := db.Query(`SELECT e.id, s.name, s.uvuid, s.aoi, e.cancode, e.enjoyment, e.social, s.lang, e.status
	FROM employees e
	JOIN surveys s ON e.fk_survey = s.id
	WHERE e.status = 0.0`)
	if err != nil {
		InfoLogger.Println("Unable to select people", err)
		var potential []PotentialHire
		return potential, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var users []PotentialHire
	for result.Next() {
		var user PotentialHire
		err := result.Scan(&user.PID, &user.Name, &user.UvuID, &user.AOI, &user.CanCode, &user.Enjoyment, &user.Social, &user.Lang, &user.Status)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []PotentialHire
			return potential, errors.New("Unable to scan people")
		}
		GenerateScore(&user)
		users = append(users, user)
	}
	if len(users) > 0 {
		return users, nil
	}
	InfoLogger.Println("Didn't find anyone")
	var potential []PotentialHire
	return potential, errors.New("didn't find anyone")
}

func EmployeeStatusChange(changes []EmployeeStatus) error {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		return errors.New("Unable to open connection to db")
	}
	defer db.Close()

	query := "UPDATE employees SET status = ? WHERE id = ?"
	for i := range changes {
		_, err := db.Exec(query, changes[i].Status, changes[i].PID)
		if err != nil {
			return errors.New("Statement not executed")
		}
	}

	return nil
}
