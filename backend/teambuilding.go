package main

// import (
// 	// "Kunde21/numgo"
// 	"database/sql"
// 	// "encoding/json"
// 	"fmt"
// 	"strings"
// )
//
// type PotentialTeamMember struct {
// 	PID int    `json:"pid"`
// 	AOI string `json:"aoi"`
// }
//
// type Project struct {
// 	ID       int
// 	Frontend int
// 	Backend  int
// 	Database int
// 	Embedded int
// 	Gamedev  int
// }
//
// type Vector struct {
// 	ID   int
// 	Area [5]int
// }
//
// // TODO: Do I need a different struct PotentialTeamMembers parsed as an int?
//
// func TeamBuilding() {
// 	db, err := sql.Open("sqlite", "./database/database.db")
// 	if err != nil {
// 		// TODO: Add Logger
// 		fmt.Printf("The world is ending!")
// 	}
// 	defer db.Close()
//
// 	employee_result, err := db.Query(`SELECT id, lang, aoi FROM surveys`)
// 	if err != nil {
// 		// TODO: Add Logger
// 		fmt.Printf("The world is ending!")
// 	}
// 	defer employee_result.Close()
//
// 	var employees []PotentialTeamMember
// 	for employee_result.Next() {
// 		var employee PotentialTeamMember
// 		err := employee_result.Scan(&employee.PID, &employee.AOI)
// 		if err != nil {
// 			// TODO: Add Logger
// 			fmt.Printf("The world is ending 2.0")
// 		}
// 		employees = append(employees, employee)
// 	}
//
// 	// TODO:
// 	// 1. Parse AOI from string to integer array
// 	// 2.
//
// 	vector_dimensions := [5]string{"frontend", "backend", "database", "embedded", "gamedev"}
//
// 	var vector_employees []Vector
// 	for i := 0; i < len(employees); i++ {
// 		var vector_employee Vector
// 		vector_employee.PID = employees[i].PID
//
// 		for j := 0; i < len(vector_dimensions); j++ {
// 			if strings.Contains(employees[i].AOI, vector_dimensions[j]) {
// 				vector_employee.Area[j] = 1
// 			} else {
// 				vector_employee.Area = 0
// 			}
//
// 			vector_employees = append(vector_employees, vector_employee)
// 		}
//
// 		project_result, err := db.Query(`SELECT id, frontend, backend, database, game_dev, embedded FROM projects`)
// 		if err != nil {
// 			// TODO: Add Logger
// 			fmt.Printf("The world is ending!")
// 		}
// 		defer project_result.Close()
//
// 		var projects []Project
// 		for project_result.Next() {
// 			var project Project
// 			err := employee_result.Scan(project.ID, project.Frontend, project.Backend, project.Database, project.Embedded, project.Gamedev)
// 			if err != nil {
// 				fmt.Printf("The world is ending, again")
// 			}
// 			projects = append(projects, project)
// 		}
//
// 		fmt.Printf("Scores")
// 	}
// }
