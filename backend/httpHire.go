// TODO: update post so that there's additional checking logic
package main

import (
	"encoding/json"
	"net/http"
)

func HireHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var changes []EmployeeStatus
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&changes)
		if err != nil {
			InfoLogger.Println(err)
		}
		EmployeeStatusChange(changes)
	}
	if r.Method == "GET" {
		hires, err := GetEmployees("=", 0)
		if err != nil {
			InfoLogger.Println("Couldn't get potential hires")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}

		response, err := json.Marshal(hires)
		if err != nil {
			InfoLogger.Println("Couldn't marshal data for hires")
			http.Error(w, "Invalid input", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	}
}
