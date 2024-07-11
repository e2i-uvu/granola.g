package main

import (
	"database/sql"
	"errors"
	_ "github.com/mattn/go-sqlite3"
)

type InterviewResult struct {
	PID       int  `json:"pid"`
	FKUser    int  `json:"fkuser"`
	CanCode   bool `json:"cancode"`
	Enjoyment int8 `json:"enjoyment"`
	Social    int8 `json:"social"`
}

type InterviewResultIn struct {
	FKUser    int  `json:"fkuser"`
	CanCode   bool `json:"cancode"`
	Enjoyment int8 `json:"enjoyment"`
	Social    int8 `json:"social"`
}

func (inter InterviewResultIn) Save() error {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Fatal("Unable to connect to database")
	}
	defer db.Close()

	stmt, err := db.Prepare("INSERT INTO interviews (fkuser, cancode, enjoyment, social) VALUES (?, ?, ?, ?)")
	if err != nil {
		InfoLogger.Fatal("Unable to prepare statement to save interview result to database")
	}
	defer stmt.Close()

	_, err = stmt.Exec(inter.FKUser, inter.CanCode, inter.Enjoyment, inter.Social)
	if err != nil {
		return errors.New("Invalid information has been sent")
	}

	return nil
}
