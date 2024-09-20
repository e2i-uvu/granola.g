package main

import (
	"fmt"
)

func BuildTeams(project Project) ([]Employee, error) {
	GetEmployeeArbitrary(fmt.Sprintf("WHERE aoi LIKE %%s% AND prevTeam == 1 AND status == 0 AND speciality LIKE %%s%", project.AOIs[0].Aoi, project.Type))
	var ret []Employee
	for i := 0; i < len(project.AOIs); i++ {
		people, err := GetEmployeeArbitrary(fmt.Sprintf("WHERE aoi LIKE %%s% AND status == 0 AND speciality LIKE %%s%", project.AOIs[i].Aoi, project.Type))
		if err != nil {
			InfoLogger.Printf("You did something terribly wrong, %s\n", err)
		}
		for j := 0; j < project.AOIs[i].Amount && j < len(people); j++ {
			ret = append(ret, people[j])
		}
		InfoLogger.Printf(fmt.Sprintf("%s, %s", people, err))
	}
	return ret, nil
}
