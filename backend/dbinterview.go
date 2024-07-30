package main

import (
	"database/sql"
	"errors"
	"fmt"
)

type InterviewResultIn struct {
	FKSurvey  int  `json:"fksurvey"`
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

	stmt, err := db.Prepare("INSERT INTO employees (fk_survey, cancode, enjoyment, social, status) VALUES (?, ?, ?, ?, ?)")
	if err != nil {
		InfoLogger.Fatal(fmt.Sprintf("Unable to prepare statement, %s", err))
	}
	defer stmt.Close()

	_, err = stmt.Exec(inter.FKSurvey, inter.CanCode, inter.Enjoyment, inter.Social, 0)
	if err != nil {
		return errors.New("Invalid information has been sent")
	}

	return nil
}
