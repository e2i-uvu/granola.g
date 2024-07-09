package main

import (
	"fmt"
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
	http.HandleFunc("/interviewFinish", InterviewFinishHandler)
	go http.ListenAndServe(":8081", nil)
	InfoLogger.Println("View Server at Localhost:8081")
	fmt.Println("View Server at localhost:8081")
	for {
		time.Sleep(1 * time.Second)
	}
}
