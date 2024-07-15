package main

import ()

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

// base the PID off the interview and not the person
// return only people with hired value of 0
// generate score for each row
// generate json
func potentialHires() (PotentialHire, error) {
	_ = `SELECT i.id, u.name, u.uvuid, u.aoi, i.cancode, i.enjoyment, i.social, u.lang
	FROM interviews i
	JOIN users u ON i.fkusers = u.id
	WHERE i.hired = 0`

	// generate score for each row of above output

	// marshal each row with score

	// return marshalled data
	var hire PotentialHire
	return hire, nil
}

// take interview pid set flag to appropriate position(1 for hired 0 for not)
// func Hire()

// define later based on a multitude of factors
// func GetHired()
