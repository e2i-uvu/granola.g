package main

import (
	// "Kunde21/numgo"
	"database/sql"
	// "encoding/json"
	"fmt"
)

type PotentialTeamMember struct {
	PID  int    `json:"pid"`
	Lang string `json:"lang"`
	AOI  string `json:"aoi"`
}

// TODO: Do I need a different struct PotentialTeamMembers parsed as an int?

func TeamBuilding() {
	db, err := sql.Open("sqlite", "./database/database.db")
	if err != nil {
		// TODO: Add Logger
		fmt.Printf("The world is ending!")
	}
	defer db.Close()

	employee_result, err := db.Query(`SELECT id, lang, aoi FROM surveys`)
	if err != nil {
		// TODO: Add Logger
		fmt.Printf("The world is ending!")
	}
	defer employee_result.Close()

	project_result, err := db.Query(`SELECT id, frontend, backend, database, game_dev, embedded FROM projects`)
	if err != nil {
		// TODO: Add Logger
		fmt.Printf("The world is ending!")
	}
	defer project_result.Close()

	var employees []PotentialTeamMember
	for employee_result.Next() {
		var employee PotentialTeamMember
		err := employee_result.Scan(&employee.PID, &employee.Lang, &employee.AOI)
		if err != nil {
			// TODO: Add Logger
			fmt.Printf("The world is ending 2.0")
		}
		employees = append(employees, employee)
	}

	fmt.Printf("Scores")
}
