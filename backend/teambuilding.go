package main

import ()

type Assignment struct {
	Person   PotentialHire `json:"person"`
	Position string        `json:"position"`
}

func BuildTeams(people []PotentialHire, project []Project) ([]Assignment, error) {
	var teams []Assignment
	return teams, nil
}
