package main

import (
	"encoding/json"
	"net/http"
)

func TeamsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		// expects pid and status either set to hired(1) or anything else sets to -1(not hired)
	}
	if r.Method == "GET" {
		hires, err := GetPendingEmployee()
		if err != nil {
			InfoLogger.Println("Teambuild error 1")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return

		}
		projects, err := GetAllProjects()
		if err != nil {
			InfoLogger.Println("Teambuild error 2")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}
		teams, err := BuildTeams(hires, projects)
		if err != nil {
			InfoLogger.Println("Teambuild error 3")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}

		response, err := json.Marshal(teams)
		if err != nil {
			InfoLogger.Println("Couldn't marshal data for hires")
			http.Error(w, "Invalid input", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	}
}
