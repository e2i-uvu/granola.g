package main

import (
	"errors"
	"fmt"
)

func BuildTeams(project Project) ([]Employee, error) {
	var ret []Employee
	teamLead, err := GetEmployeeArbitrary(fmt.Sprintf("WHERE aoi LIKE '%%%s%%' AND prevTeam == 1 AND status = 0 AND speciality LIKE '%%%s%%'", project.AOIs[0].Aoi, project.Type))
	if err != nil {
		return nil, errors.New("Unable to find valid team lead")
	}

	ret = append(ret, teamLead[0])

	for i := 0; i < len(project.AOIs); i++ {
		people, err := GetEmployeeArbitrary(fmt.Sprintf("WHERE aoi LIKE '%%%v%%' AND status = 0 AND speciality LIKE '%%%v%%'", project.AOIs[i].Aoi, project.Type))
		if err != nil {
			return nil, errors.New("Not enough people to fill in team")
		}
		for j := 0; j < project.AOIs[i].Amount && j < len(people); j++ {
			ret = append(ret, people[j])
		}
	}
	return ret, nil
}
