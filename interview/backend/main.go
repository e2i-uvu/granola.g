package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	response := Response{Name: "John", Lang: "Python", AOI: "Embedded, Web"}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	go InitSQL()
	fmt.Print("Hello")
	http.HandleFunc("/", handler)
	go http.ListenAndServe(":8080", nil)
	for {
		time.Sleep(1 * time.Second)
	}
}
