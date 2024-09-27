package main

import "errors"

type ProjectAOI struct {
	Aoi    string `json:"employee"`
	Amount int    `json:"amount"`
}
type BuildProject struct {
	ID     int          `json:"id"`
	Name   string       `json:"project_name"`
	Type   string       `json:"project_type"`
	AOIs   []ProjectAOI `json:"employees"`
	Status int          `json:"status"`
}

func GetAllProjects() ([]map[string]interface{}, error) {
	// returns all projects
	db := OpenDB()
	defer db.Close()

	result, err := db.Query(
		`SELECT p.name, 
		p.type,
		e.*
		FROM projects p
		INNER JOIN
			teams t ON p.id = t.project_id
		INNER JOIN
			employees e ON t.employee_id = e.id`)
	if err != nil {
		InfoLogger.Println("Unable to select projects", err)
		return nil, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var teams []map[string]interface{}

	for result.Next() {
		InfoLogger.Println("You're a nerd")
		columns, err := result.Columns()
		if err != nil {
			InfoLogger.Fatal("Failed to get columns:", err)
		}

		values := make([]interface{}, len(columns))
		valuePtrs := make([]interface{}, len(columns))
		for i := range columns {
			valuePtrs[i] = &values[i]
		}

		if err := result.Scan(valuePtrs...); err != nil {
			InfoLogger.Fatal("Failed to scan row:", err)
		}

		resultMap := make(map[string]interface{})
		for i, colName := range columns {
			resultMap[colName] = values[i]
		}

		teams = append(teams, resultMap)
	}

	return teams, nil
}
