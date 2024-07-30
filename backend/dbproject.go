package main

import (
	"database/sql"
	"errors"
)

type Project struct {
	ID          int    `json:"id"`
	Status      int    `json:"status"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Frontend    int    `json:"frontend"`
	Backend     int    `json:"backend"`
	Database    int    `json:"database"`
	Game_dev    int    `json:"game_dev"`
	Embedded    int    `json:"embedded"`
}

func GetAllProjects() ([]Project, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var projects []Project
		return projects, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	result, err := db.Query(`SELECT *
	FROM projects p
	WHERE p.status = 0
`)
	if err != nil {
		InfoLogger.Println("Unable to select projects", err)
		var projects []Project
		return projects, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var projects []Project
	for result.Next() {
		var project Project
		err := result.Scan(&project.ID, &project.Status, &project.Name, &project.Description, &project.Frontend, &project.Backend, &project.Database, &project.Game_dev, &project.Embedded)
		if err != nil {
			InfoLogger.Println("Unable to scan projects", err)
			var projects []Project
			return projects, errors.New("Unable to scan people")
		}
		InfoLogger.Println(project)
		projects = append(projects, project)
	}
	if len(projects) > 0 {
		return projects, nil
	}
	InfoLogger.Println("Didn't find anyone")
	return projects, errors.New("didn't find anyone")
}
