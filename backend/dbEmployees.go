package main

import (
	"errors"
	"fmt"
)

type EmployeeStatus struct {
	PID    int `json:"pid"`
	Status int `json:"status"`
}
type Employee struct {
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

func GetEmployees(operator string, parameter int) ([]Employee, error) {
	// operator string is expected to be >, <, or some other comparison operator
	// parameter is the value you want to compare it by
	// IE ">", "1" will return everything is employees table with status greater than 1
	db := OpenDB()
	defer db.Close()

	query := fmt.Sprintf(`SELECT e.id, s.uvuid, s.name, s.lang, s.aoi, e.cancode, e.enjoyment, e.social, e.status
	FROM employees e
	JOIN surveys s ON e.fk_survey = s.id
	WHERE e.status %s ?`, operator)

	result, err := db.Query(query, parameter)
	if err != nil {
		InfoLogger.Println("Unable to select people", err)
		var potential []Employee
		return potential, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var users []Employee
	for result.Next() {
		var user Employee
		err := result.Scan(&user.PID, &user.UvuID, &user.Name, &user.Lang, &user.AOI, &user.CanCode, &user.Enjoyment, &user.Social, &user.Status)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []Employee
			return potential, errors.New("Unable to scan people")
		}
		GenerateScore(&user)
		users = append(users, user)
	}
	if len(users) > 0 {
		return users, nil
	}
	InfoLogger.Println("Didn't find anyone")
	var potential []Employee
	return potential, errors.New("didn't find anyone")
}

func EmployeeStatusChange(changes []EmployeeStatus) error {
	db := OpenDB()
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
