package main

import (
	"encoding/json"
	"net/http"
)

func InterviewStartHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var data map[string]interface{}
		err := json.NewDecoder(r.Body).Decode(&data)
		if err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}
		id, ok := data["uvuid"].(float64)
		uvuid := int(id)
		if ok {
			person, err := GetUser(uvuid)
			if err != nil {
				http.Error(w, "Invalid input", http.StatusNotAcceptable)
				return
			}
			response, err := json.Marshal(person)
			if err != nil {
			}
			w.Header().Set("Content-Type", "application/json")
			w.Write(response)
		} else {
			http.Error(w, "Invalid input", http.StatusNotAcceptable)
		}
	} else {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}
