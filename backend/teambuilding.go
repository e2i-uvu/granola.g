package main

import (
	"fmt"
	"sort"
	"strings"
)

type Assignment struct {
	Person   PotentialHire `json:"person"`
	Position string        `json:"position"`
}

type sortPendingEmployee []PotentialHire

func (p sortPendingEmployee) Len() int           { return len(p) }
func (p sortPendingEmployee) Less(i, j int) bool { return p[i].Score > p[j].Score }
func (p sortPendingEmployee) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }

func BuildTeams(people []PotentialHire, projects []Project) (map[int][]Assignment, error) {
	teams := make(map[int][]Assignment)
	InfoLogger.Println(people[0])
	sort.Sort(sortPendingEmployee(people))
	InfoLogger.Println(people[0])
	flag := true
	for _, toBeKey := range projects {
		var value []Assignment
		teams[toBeKey.ID] = value
	}
	for len(projects) > 0 && len(people) > 0 {
		for i, value := range projects {
			fmt.Printf("Currently on project, %s - ", value.Name)
			if value.Frontend > 0 && len(people) > 0 {
				fmt.Printf("Assigning frontend, ")
				for iperson, person := range people {
					if strings.Contains(strings.ToLower(person.AOI), "frontend") {
						fmt.Printf("Assigned %s ", person.Name)
						projects[i].Frontend -= 1
						teams[value.ID] = append(teams[value.ID], Assignment{person, "frontend"})
						people = append(people[:iperson], people[iperson+1:]...)
						flag = false
						break
					}
				}
				if flag {
					teams[value.ID] = append(teams[value.ID], Assignment{people[len(people)-1], "frontend"})
					fmt.Printf("Assigned %s ", people[len(people)-1].Name)
					projects[i].Frontend -= 1
					people = people[:len(people)-1]
				}
				flag = true
			}
			if value.Backend > 0 && len(people) > 0 {
				fmt.Printf("Assigning Backend, ")
				for iperson, person := range people {
					if strings.Contains(strings.ToLower(person.AOI), "backend") {
						projects[i].Backend -= 1
						teams[value.ID] = append(teams[value.ID], Assignment{person, "backend"})
						people = append(people[:iperson], people[iperson+1:]...)
						flag = false
						break
					}
				}
				if flag {
					teams[value.ID] = append(teams[value.ID], Assignment{people[len(people)-1], "backend"})
					fmt.Printf("Assigned %s ", people[len(people)-1].Name)
					projects[i].Backend -= 1
					people = people[:len(people)-1]
				}
				flag = true
			}
			if value.Database > 0 && len(people) > 0 {
				for iperson, person := range people {
					if strings.Contains(strings.ToLower(person.AOI), "database") {
						projects[i].Database -= 1
						teams[value.ID] = append(teams[value.ID], Assignment{person, "database"})
						people = append(people[:iperson], people[iperson+1:]...)
						flag = false
						break
					}
				}
				if flag {
					teams[value.ID] = append(teams[value.ID], Assignment{people[len(people)-1], "database"})
					fmt.Printf("Assigned %s ", people[len(people)-1].Name)
					projects[i].Database -= 1
					people = people[:len(people)-1]
				}
				flag = true
			}
			if value.Embedded > 0 && len(people) > 0 {
				for iperson, person := range people {
					if strings.Contains(strings.ToLower(person.AOI), "embedded") {
						projects[i].Embedded -= 1
						teams[value.ID] = append(teams[value.ID], Assignment{person, "embedded"})
						people = append(people[:iperson], people[iperson+1:]...)
						flag = false
						break
					}
				}
				if flag {
					teams[value.ID] = append(teams[value.ID], Assignment{people[len(people)-1], "embedded"})
					fmt.Printf("Assigned %s ", people[len(people)-1].Name)
					projects[i].Embedded -= 1
					people = people[:len(people)-1]
				}
				flag = true
			}
			if value.Game_dev > 0 && len(people) > 0 {
				for iperson, person := range people {
					if strings.Contains(strings.ToLower(person.AOI), "game_dev") {
						projects[i].Game_dev -= 1
						teams[value.ID] = append(teams[value.ID], Assignment{person, "game_dev"})
						people = append(people[:iperson], people[iperson+1:]...)
						flag = false
						break
					}
				}
				if flag {
					teams[value.ID] = append(teams[value.ID], Assignment{people[len(people)-1], "game_dev"})
					fmt.Printf("Assigned %s ", people[len(people)-1].Name)
					projects[i].Game_dev -= 1
					people = people[:len(people)-1]
				}
				flag = true
			}
			fmt.Printf("current sizes projects: %d, people: %d\n", len(projects), len(people))
			if value.Backend == 0 && value.Frontend == 0 && value.Embedded == 0 && value.Game_dev == 0 && value.Database == 0 {
				projects = append(projects[:i], projects[i+1:]...)
			}
		}
	}
	return teams, nil
}
