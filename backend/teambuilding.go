package main

import (
	"errors"
	"fmt"
)

//	func EmployeeStatusChange(changes []EmployeeStatus) error {
//		db := OpenDB()
//		defer db.Close()
//
//		query := "UPDATE employees SET status = ? WHERE id = ?"
//		for i := range changes {
//			_, err := db.Exec(query, changes[i].Status, changes[i].PID)
//			if err != nil {
//				return errors.New("Statement not executed")
//			}
//		}
//
//		return nil
//	}
func BuildTeams(project Project) ([]Employee, error) {
	var ret []Employee
	var temp []EmployeeStatus

	teamLead, err := GetEmployeeArbitrary(fmt.Sprintf("WHERE aoi LIKE '%%%s%%' AND prevTeam == 1 AND status = 0 AND speciality LIKE '%%%s%%'", project.AOIs[0].Aoi, project.Type))
	if err != nil {
		return nil, errors.New("Unable to find valid team lead")
	}

	ret = append(ret, teamLead[0])
	temp = append(temp, EmployeeStatus{teamLead[0].Id, 1})
	EmployeeStatusChange(temp)

	for i := 0; i < len(project.AOIs); i++ {
		people, err := GetEmployeeArbitrary(fmt.Sprintf("WHERE aoi LIKE '%%%v%%' AND status = 0 AND speciality LIKE '%%%v%%'", project.AOIs[i].Aoi, project.Type))
		if err != nil {
			return nil, errors.New("Not enough people to fill in team")
		}
		for j := 0; j < project.AOIs[i].Amount && j < len(people); j++ {
			ret = append(ret, people[j])
			temp = append(temp, EmployeeStatus{people[j].Id, 1})
			EmployeeStatusChange(temp)
		}
	}
	for i, _ := range temp {
		temp[i].Status = 0
	}
	EmployeeStatusChange(temp)
	return ret, nil
}
