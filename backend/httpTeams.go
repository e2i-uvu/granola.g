package main

import (
	"encoding/json"
	"net/http"
)

type AOI struct {
	Aoi    string `json:"employee"`
	Amount int    `json:"amount"`
}

type Project struct {
	ProjectName    string `json:"project_name"`
	Type           string `json:"project_type"`
	AOIs           []AOI  `json:"employees"`
	TotalEmployees int    `json:"total_employees"`
}

type SaveProject struct {
	ProjectName string          `json:"project_name"`
	Type        string          `json:"project_type"`
	Employees   []SaveEmployees `json:"employees"`
}

type SaveEmployees struct {
	Employee string `json:"employee"`
}

func TeamsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var project SaveProject
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&project)
		if err != nil {
			InfoLogger.Println("Error decoding JSON:", err)
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		db := OpenDB()
		defer db.Close()

		result, err := db.Exec(`INSERT INTO projects (status, name, type) VALUES (?, ?, ?)`, 0, project.ProjectName, project.Type)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			InfoLogger.Fatal("Failed to insert record:", err)
		}

		lastID, err := result.LastInsertId()
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			InfoLogger.Fatal("Failed to get last insert ID:", err)
		}

		for _, id := range project.Employees {

			_, err := db.Exec(`INSERT INTO teams (employee_id, project_id, project_manager) VALUES (?, ?, ?)`, id.Employee, lastID, 0)
			if err != nil {
				w.WriteHeader(http.StatusBadRequest)
				InfoLogger.Fatal("Failed to insert record:", err)
			}

			update := []EmployeeStatus{
				{PID: id.Employee, Status: 1},
			}
			EmployeeStatusChange(update)
		}

		w.WriteHeader(http.StatusOK)
	}
	if r.Method == "GET" && r.Header.Get("Content-Type") == "application/json" {
		var project Project
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&project)
		if err != nil {
			InfoLogger.Println("Error decoding JSON:", err)
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		team, err := BuildTeams(project)
		if err != nil {
			InfoLogger.Println("Couldn't build teams")
			w.WriteHeader(http.StatusOK)
			return
		}

		response, err := json.Marshal(team)
		if err != nil {
			InfoLogger.Println("Couldn't marshal data for hires")
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	}
}
