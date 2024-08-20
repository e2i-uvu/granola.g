// TODO: Replace algorithm to include one carry over employee and the rest as randomized
package main

import (
	"errors"
)

type Assignment struct {
	Person   Employee `json:"person"`
	Position string   `json:"position"`
}

type sortPendingEmployee []Employee

func BuildTeams(people []Employee, projects []Project) (map[int][]Assignment, error) {
	return nil, errors.New("Unimplemented function")
}
