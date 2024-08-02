package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
)

func InterviewStartHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var data map[string]interface{}
		err := json.NewDecoder(r.Body).Decode(&data)
		if err != nil {
			message := fmt.Sprintf("Error: %s", err)
			InfoLogger.Println(message)
			http.Error(w, "Invalid input", http.StatusNotAcceptable)
			return
		}
		id, err := strconv.ParseInt(data["uvuid"].(string), 10, 0)
		if err != nil {
			InfoLogger.Println("received invalid input")
			http.Error(w, "Invalid input", http.StatusNotAcceptable)
		}
		uvuid := int(id)
		person, err := GetSurveyByUVUID(uvuid)
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

func InterviewFinishHandler(w http.ResponseWriter, r *http.Request) {

	type RequestBody struct {
		Fkuser    string `json:"fkuser"`
		Cancode   string `json:"cancode"`
		Enjoyment string `json:"enjoyment"`
		Social    string `json:"social"`
	}

	InfoLogger.Println("InterviewFinishHandler Called")
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var requestBody RequestBody
		err := json.NewDecoder(r.Body).Decode(&requestBody)
		if err != nil {
			InfoLogger.Println("Improper Data into Interviewfinishhandler")
			http.Error(w, err.Error(), http.StatusBadRequest)
		}

		fk, err := strconv.ParseInt(requestBody.Fkuser, 10, 0)
		if err != nil {
			InfoLogger.Println("Improper Data into Interviewfinishhandler")
			http.Error(w, err.Error(), http.StatusBadRequest)
		}
		cancode, err := strconv.ParseBool(requestBody.Cancode)
		if err != nil {
			InfoLogger.Println("Improper Data into Interviewfinishhandler")
			http.Error(w, err.Error(), http.StatusBadRequest)
		}
		enjoyment, err := strconv.ParseInt(requestBody.Enjoyment, 10, 8)
		if err != nil {
			InfoLogger.Println("Improper Data into Interviewfinishhandler")
			http.Error(w, err.Error(), http.StatusBadRequest)
		}
		social, err := strconv.ParseInt(requestBody.Social, 10, 8)
		if err != nil {
			InfoLogger.Println("Improper Data into Interviewfinishhandler")
			http.Error(w, err.Error(), http.StatusBadRequest)
		}

		var inter InterviewResultIn
		inter.FKSurvey = int(fk)
		inter.CanCode = cancode
		inter.Enjoyment = int8(enjoyment)
		inter.Social = int8(social)
		err = inter.Save()
		if err != nil {
			InfoLogger.Println("Things did not properly save.")
			http.Error(w, err.Error(), http.StatusBadRequest)
		}

		w.WriteHeader(http.StatusOK)
	} else {
		InfoLogger.Println("Received non-post function")
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}
