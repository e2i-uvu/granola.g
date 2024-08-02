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

const (
	validUserName = "Username"
	validPassword = "Password"
)

func authMiddleWare(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		user, pass, ok := r.BasicAuth()

		if !ok || user != validUserName || pass != validPassword {
			w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)

	})
}

func main() {
	file, err := os.OpenFile("./database/app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Failed to open log file: %v", err)
	}

	InfoLogger = log.New(file, "INFO: ", log.Ldate|log.Ltime|log.Lshortfile)

	InfoLogger.Println("Initialized:")
	go InitSQL()
	mux := http.NewServeMux()
	mux.HandleFunc("/interviewStart", InterviewStartHandler)
	mux.Handle("/interviewFinish", authMiddleWare(http.HandlerFunc(InterviewFinishHandler)))
	mux.Handle("/hire", authMiddleWare(http.HandlerFunc(HireHandler)))
	mux.Handle("/status", authMiddleWare(http.HandlerFunc(StatusHandler)))
	mux.Handle("/preinterview", authMiddleWare(http.HandlerFunc(SurveyHandler)))
	mux.Handle("/project", authMiddleWare(http.HandlerFunc(ProjectHandler)))
	mux.Handle("/fire", authMiddleWare(http.HandlerFunc(FireHandler)))
	mux.Handle("/teams", authMiddleWare(http.HandlerFunc(TeamsHandler)))
	go http.ListenAndServe(":8081", mux)
	InfoLogger.Println("View Server at Localhost:8081")
	fmt.Println("View Server at localhost:8081")
	for {
		time.Sleep(1 * time.Second)
	}
}
