package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"strings"
)

func EmployeeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var changes []EmployeeStatus
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&changes)
		if err != nil {
			InfoLogger.Println(err)
		}
		EmployeeStatusChange(changes)
	}
	if name := r.URL.Query().Get("name"); r.Method == "GET" && name != "" {
		hires, err := GetEmployee(name)

		if err != nil {
			InfoLogger.Println("Unable to collect surveys")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}

		InfoLogger.Println(hires[0])
		response, err := json.Marshal(hires)
		if err != nil {
			InfoLogger.Println("Couldn't marshal data for hires")
			http.Error(w, "Invalid input", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	} else if r.Method == "GET" {
		hires, err := GetEmployees("<", 9999)
		if err != nil {
			InfoLogger.Println("Unable to collect surveys")
			http.Error(w, "Invalid input", http.StatusBadRequest)
			return
		}

		InfoLogger.Println(hires[0])
		response, err := json.Marshal(hires)
		if err != nil {
			InfoLogger.Println("Couldn't marshal data for hires")
			http.Error(w, "Invalid input", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	}
}

func EmployeeIngestHandler(w http.ResponseWriter, r *http.Request) {

	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		var surveys []map[string]interface{}
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&surveys)
		if err != nil {
			InfoLogger.Println(err)
		}
		for _, survey := range surveys {
			var emp Employee
			var social int
			var aoi string
			for key, value := range survey {
				switch key {
				case "ResponseId":
					emp.Id = value.(string)
				case "QID4":
					emp.Name = value.(string)
				case "QID29":
					emp.Email = value.(string)
				case "QID11_1":
					emp.DegreePercent, err = strconv.Atoi(value.(string))
					if err != nil {
						emp.DegreePercent = 0
						InfoLogger.Println(fmt.Sprintf("Degree percent for survey %s failed for: \n %s", emp.Id, err))
					}
				case "QID27":
					emp.TeamBefore = parseBool(value.(string))
				case "Q37":
					emp.Speciality = value.(string)
				case "Q32", "QID10":
					emp.Major = emp.Major + value.(string)
				case "Q32_10_TEXT", "QID10_10_TEXT":
					emp.MajorAlt = emp.MajorAlt + value.(string)
				case "QID26_1", "QID22_1":
					soc, err := strconv.Atoi(value.(string))
					if err != nil {
						InfoLogger.Println(fmt.Sprintf("Social score for survey %s failed for: \n %s", emp.Id, err))
						soc = 0
					}
					social += soc / 2
				case "QID23_2":
					project, err := strconv.Atoi(value.(string))
					if err != nil {
						InfoLogger.Println(fmt.Sprintf("Project count for survey %s failed for: \n %s", emp.Id, err))
						project = 0
					}
					social += project
				case "Q34_1", "Q34_2", "Q34_3", "Q34_4", "Q34_5", "Q34_6", "QID15_1", "QID15_2", "QID15_3", "QID15_4", "QID15_5", "QID15_6":
					for i := 1; i < 7; i++ {
						marketList := []string{"Branding", "ContentCreation", "DigitalMarketing", "GraphicDesign", "SocialMediaManagement", "VideoPhotography"}
						techList := []string{"Fullstack", "Frontend", "Backend", "Database", "Embedded", "Game"}
						keyMatch := fmt.Sprintf("Q34_%d", i)
						if key == keyMatch && value != "" {
							maoi, err := strconv.Atoi(value.(string))
							if err != nil {
								maoi = 0
								InfoLogger.Println(fmt.Sprintf("AOI %d failed to parse on survey %s\n %s", i, emp.Id, err))
							}
							if maoi > 5 {
								aoi += marketList[i-1] + ", "
							}
						}
						keyMatch = fmt.Sprintf("QID15_%d", i)
						if key == keyMatch && value != "" {
							taoi, err := strconv.Atoi(value.(string))
							if err != nil {
								taoi = 0
								InfoLogger.Println(fmt.Sprintf("AOI %d failed to parse on survey %s\n %s", i, emp.Id, err))
							}
							if taoi > 5 {
								aoi += techList[i-1] + ", "
							}
						}
					}
				}
			}
			emp.Social = social
			emp.Status = 0
			emp.AOI = aoi
			emp.SaveNew()
		}
		w.WriteHeader(http.StatusOK)
	}
}

func parseBool(a string) bool {
	if strings.TrimSpace(strings.ToLower(a)) == "yes" {
		return true
	}
	return false
}
