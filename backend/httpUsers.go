package main

import (
	"errors"
	"net/http"
)

func LoginHandler(w http.ResponseWriter, r *http.Request) error {
	return errors.New("Unimplemented function")
	// if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
	// 	// TODO: copying your code lol
	// }
	// if r.Method == "GET" {
	// 	// TODO: copying your code lol
	// }
}

func LogoutHandler(w http.ResponseWriter, r *http.Request) error {
	return errors.New("Unimplemented function")
	// if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
	// 	// TODO: copying your code lol
	// }
	// if r.Method == "GET" {
	// 	// TODO: copying your code lol
	// }
}
