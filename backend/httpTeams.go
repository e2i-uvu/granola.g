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

func TeamsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		// Takes in
		//{
		//   "project_name": "Video Game and Website",
		//   "project_type": "Tech",
		//   "employees": [
		//   "id":""
		//   "id":""
		//   "id":""
		//   ]
		// }
		// saves project to projects and then adds the employee ids and project ids to many to many table
	}
	if r.Method == "GET" && r.Header.Get("Content-Type") == "application/json" {
		var project Project
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&project)
		if err != nil {
			InfoLogger.Println("Error decoding JSON:", err)
			return
		}

		team, err := BuildTeams(project)
		if err != nil {
			InfoLogger.Println("Couldn't build teams")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}

		response, err := json.Marshal(team)
		if err != nil {
			InfoLogger.Println("Couldn't marshal data for hires")
			http.Error(w, "Invalid input", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	}
}
