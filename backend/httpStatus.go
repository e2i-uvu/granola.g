package main

import (
	"encoding/json"
	"net/http"
)

func StatusHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		// expects pid and status either set to hired(1) or anything else sets to -1(not hired)
	}
	if r.Method == "GET" {
		hires, err := GetEmployees("!=", 9999)
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
