package main

import (
	"encoding/json"
	"net/http"
)

func FireHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		// expects pid and status either set to hired(1) or anything else sets to -1(not hired)
	}
	if r.Method == "GET" {
		hires, err := GetEmployees(">", 0)
		if err != nil {
			InfoLogger.Println("Couldn't get potential hires")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}

		InfoLogger.Println(hires[0])
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
