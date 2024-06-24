package main

import (
	"log"
	"net/http"
	"os"
	"time"
)

func main() {
	file, err := os.OpenFile("logfile.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Set the output of log package to the file
	log.SetOutput(file)

	log.Println("Initialized:")
	go InitSQL()
	http.HandleFunc("/interviewStart", InterviewStartHandler)
	go http.ListenAndServe(":8080", nil)
	for {
		time.Sleep(1 * time.Second)
	}
}
