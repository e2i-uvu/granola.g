package main

import (
	"encoding/json"
	"net/http"
)

func SurveyHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var changes Survey
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&changes)
		if err != nil {
			InfoLogger.Println(err)
		}
		err = changes.Save()
		if err != nil {
			InfoLogger.Println(err)
		}
	}
	if r.Method == "GET" {
		hires, err := GetAllSurveys()
		if err != nil {
			InfoLogger.Println("Unable to collect surveys")
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
