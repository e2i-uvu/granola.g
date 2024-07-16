package main

import (
	"database/sql"
	"errors"
)

type PotentialHire struct {
	PID       int    `json:"pid"`
	UvuID     int    `json:"uvuid"`
	Name      string `json:"name"`
	Lang      string `json:"lang"`
	AOI       string `json:"aoi"`
	CanCode   bool   `json:"cancode"`
	Enjoyment int8   `json:"enjoyment"`
	Social    int8   `json:"social"`
	Score     int8   `json:"score"`
}

func GetPotentialHires() ([]PotentialHire, error) {
	db, err := sql.Open("sqlite3", "./database/database.db")
	if err != nil {
		InfoLogger.Println("sql.open", err)
		var potential []PotentialHire
		return potential, errors.New("Unable to open connection to db")
	}
	defer db.Close()

	result, err := db.Query(`SELECT i.id, u.name, u.uvuid, u.aoi, i.cancode, i.enjoyment, i.social, u.lang
	FROM interviews i
	JOIN users u ON i.fkusers = u.id
	WHERE i.hired = 0`)
	if err != nil {
		InfoLogger.Println("Unable to select people", err)
		var potential []PotentialHire
		return potential, errors.New("Unable to open connection to db")
	}
	defer result.Close()

	var users []PotentialHire
	for result.Next() {
		var user PotentialHire
		err := result.Scan(&user.PID, &user.Name, &user.UvuID, &user.AOI, &user.CanCode, &user.Enjoyment, &user.Social, &user.Lang)
		if err != nil {
			InfoLogger.Println("Unable to scan people", err)
			var potential []PotentialHire
			return potential, errors.New("Unable to scan people")
		}
		GenerateScore(&user)
		users = append(users, user)
	}
	if len(users) > 0 {
		return users, nil
	}
	InfoLogger.Println("Didn't find anyone")
	var potential []PotentialHire
	return potential, errors.New("didn't find anyone")
}

// take interview pid set flag to appropriate position(1 for hired 0 for not)
// func Hire()

// define later based on a multitude of factors
// func GetHired()
