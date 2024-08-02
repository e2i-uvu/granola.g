package main

import (
	"encoding/json"
	"net/http"
)

func ProjectHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		// expects pid and status either set to hired(1) or anything else sets to -1(not hired)
	}
	if r.Method == "GET" {
		projects, err := GetAllProjects()
		if err != nil {
			InfoLogger.Println("Couldn't get pending projects")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}

		response, err := json.Marshal(projects)
		if err != nil {
			InfoLogger.Println("Couldn't marshal data for pending projects")
			http.Error(w, "Invalid input", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	}
}
