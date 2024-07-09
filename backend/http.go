package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"
)

func InterviewStartHandler(w http.ResponseWriter, r *http.Request) {
	InfoLogger.Println("InterviewStartHandler Called")
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

func InterviewFinishHandler(w http.ResponseWriter, r *http.Request) {
	InfoLogger.Println("InterviewFinishHandler Called")
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		body, err := io.ReadAll(r.Body)
		if err != nil {
			InfoLogger.Println("Unable to decode body")
			http.Error(w, "Invalid Input", http.StatusNotAcceptable)
			return
		}
		var interview map[string]interface{}
		err = json.Unmarshal([]byte(body), &interview)
		if err != nil {
			message := fmt.Sprintf("Error: %s, Data %s", err, body)
			InfoLogger.Println(message)
			println(message)
			http.Error(w, "Invalid input", http.StatusNotAcceptable)
			return
		}
		// fkuser, err := strconv.ParseInt(data["fkuser"].(string), 10, 0)
		// if err != nil {
		// 	InfoLogger.Println("received invalid input fkuser")
		// 	http.Error(w, "Invalid input", http.StatusNotAcceptable)
		// }
		// cancode, ok := data["cancode"].(bool)
		// if !ok {
		// 	InfoLogger.Println("received invalid input cancode")
		// 	http.Error(w, "Invalid input", http.StatusNotAcceptable)
		// }
		// enjoyment, err := strconv.ParseInt(data["enjoyment"].(string), 10, 8)
		// if err != nil {
		// 	InfoLogger.Println("received invalid input enjoyment value")
		// 	http.Error(w, "Invalid input", http.StatusNotAcceptable)
		// }
		// social, err := strconv.ParseInt(data["social"].(string), 10, 8)
		// if err != nil {
		// 	InfoLogger.Println("received invalid input social value")
		// 	http.Error(w, "Invalid input", http.StatusNotAcceptable)
		// }
		// inter := InterviewResult{
		// 	FKUser:    int(fkuser),
		// 	CanCode:   cancode,
		// 	Enjoyment: int8(enjoyment),
		// 	Social:    int8(social),
		// }
		// err = interview.Save()
		// if err != nil {
		// 	http.Error(w, "Invalid input", http.StatusNotAcceptable)
		// }

		w.WriteHeader(http.StatusOK)
	} else {
		InfoLogger.Println("Received non-post function")
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}
