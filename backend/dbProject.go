package main

import ()

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

// func GetAllProjects() ([]Project, error) {
// 	// returns all projects where the status is currently 0
// 	db := OpenDB()
// 	defer db.Close()
//
// 	result, err := db.Query(`SELECT *
// 	FROM projects p
// 	WHERE p.status = 0
// `)
// 	if err != nil {
// 		InfoLogger.Println("Unable to select projects", err)
// 		var projects []Project
// 		return projects, errors.New("Unable to open connection to db")
// 	}
// 	defer result.Close()
//
// 	var projects []Project
// 	for result.Next() {
// 		var project Project
// 		err := result.Scan(&project.ID, &project.Status, &project.Name, &project.Description, &project.Frontend, &project.Backend, &project.Database, &project.Game_dev, &project.Embedded)
// 		if err != nil {
// 			InfoLogger.Println("Unable to scan projects", err)
// 			var projects []Project
// 			return projects, errors.New("Unable to scan people")
// 		}
// 		InfoLogger.Println(project)
// 		projects = append(projects, project)
// 	}
// 	if len(projects) > 0 {
// 		return projects, nil
// 	}
// 	InfoLogger.Println("Didn't find anyone")
// 	return projects, errors.New("didn't find anyone")
// }
