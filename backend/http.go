package main

import (
	"encoding/json"
	"net/http"
	"strconv"
)

func InterviewStartHandler(w http.ResponseWriter, r *http.Request) {
	InfoLogger.Println("InterviewStartHandler Called")
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var data map[string]interface{}
		err := json.NewDecoder(r.Body).Decode(&data)
		if err != nil {
			http.Error(w, "Invalid input", http.StatusNotAcceptable)
			return
		}
		id, err := strconv.ParseInt(data["uvuid"].(string), 10, 0)
		if err != nil {
			InfoLogger.Println("received invalid input")
			http.Error(w, "Invalid input", http.StatusNotAcceptable)
		}
		uvuid := int(id)
		person, err := GetUser(uvuid)
		if err != nil {
			InfoLogger.Println("GetUser", err)
			http.Error(w, "Invalid input", http.StatusNotAcceptable)
			return
		}
		response, err := json.Marshal(person)
		if err != nil {
			InfoLogger.Println("Json Marshal", err)
			http.Error(w, "Person not found", http.StatusNotAcceptable)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	} else {
		InfoLogger.Println("Received non-post function")
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}
