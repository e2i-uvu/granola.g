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
	PID      int    `json:"pid"`
	Name     string `json:"name"`
	Email    string `json:"email"`
	UvuID    int    `json:"uvuid"`
	PrevTeam bool   `json:"prevteam"`
	Major    string `json:"major"`
	AOI      string `json:"aoi"`
	Social   int8   `json:"social"`
	Status   int8   `json:"status"`
}

func GetEmployees(operator string, parameter int) ([]Employee, error) {
	// operator string is expected to be >, <, or some other comparison operator
	// parameter is the value you want to compare it by
	// IE ">", "1" will return everything is employees table with status greater than 1
	db := OpenDB()
	defer db.Close()

	query := fmt.Sprintf(`SELECT id, name, email, uvuid, prevteam, major, aoi, social, status
	FROM employees
	WHERE status %s ?`, operator)

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
		err := result.Scan(&user.PID, &user.Name, &user.Email, &user.UvuID, &user.PrevTeam, &user.Major, &user.AOI, &user.Social, &user.Status)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []Employee
			return potential, errors.New("Unable to scan people")
		}
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

func (user Employee) SaveNew() error {
	db := OpenDB()
	defer db.Close()

	stmt, err := db.Prepare("INSERT INTO employees (name, email, uvuid, prevteam, major, aoi, social, status) VALUES (?,?,?,?,?,?,?,?)")
	if err != nil {
	}
	defer stmt.Close()

	_, err = stmt.Exec(user.Name, user.Email, user.UvuID, user.PrevTeam, user.Major, user.AOI, user.Social, 0)
	if err != nil {
	}

	return nil
}
