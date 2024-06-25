package main

import (
	"log"
	"net/http"
	"os"
	"time"
)

var (
	InfoLogger *log.Logger
)

func main() {
	file, err := os.OpenFile("./database/app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Failed to open log file: %v", err)
	}

	InfoLogger = log.New(file, "INFO: ", log.Ldate|log.Ltime|log.Lshortfile)

	InfoLogger.Println("Initialized:")
	go InitSQL()
	http.HandleFunc("/interviewStart", InterviewStartHandler)
	go http.ListenAndServe(":8080", nil)
	for {
		time.Sleep(1 * time.Second)
	}
}
