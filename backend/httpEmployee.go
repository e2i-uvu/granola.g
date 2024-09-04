package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
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
		body, err := io.ReadAll(r.Body)
		if err != nil {
			InfoLogger.Println("Error reading body:", err)
			return
		}
		InfoLogger.Printf("Raw JSON body: %s", body)

		// Reset the body for decoding
		r.Body = io.NopCloser(bytes.NewReader(body))
		var surveys []map[string]interface{}
		decoder := json.NewDecoder(r.Body)
		err = decoder.Decode(&surveys)
		if err != nil {
			InfoLogger.Println(err)
		}
		for i, survey := range surveys {
			InfoLogger.Printf("\nSurvey %d:\n", i+1)
			for key, value := range survey {
				InfoLogger.Printf("  %s: %v\n", key, value)
			}
		}
		InfoLogger.Printf("%s%", surveys)
		for _, person := range surveys {
			var emp Employee
			emp.Id = person["ResponseID"].(string)
			emp.Name = person["QID4"].(string)
			emp.Email = person["QID29"].(string)
			emp.DegreePercent, err = strconv.Atoi(person["QID11_1"].(string))
			if err != nil {
				emp.DegreePercent = 0
				InfoLogger.Println(fmt.Sprintf("Degree percent for survey %s failed for: \n %s", emp.Id, err))
			}
			emp.TeamBefore = parseBool(person["QID27"].(string))
			emp.Speciality = person["Q37"].(string)
			emp.Major = person["Q32"].(string) + person["QID10"].(string)
			emp.MajorAlt = person["Q32_10_TEXT"].(string) + person["QID10_10_TEXT"].(string)
			var aoi string
			for i := 1; i < 7; i++ {
				marketList := []string{"Branding", "ContentCreation", "DigitalMarketing", "GraphicDesign", "SocialMediaManagement", "VideoPhotography"}
				techList := []string{"Fullstack", "Frontend", "Backend", "Database", "Embedded", "Game"}
				maoi, err := strconv.Atoi(person[fmt.Sprintf("Q34_%d", i)].(string))
				if err != nil {
					maoi = 0
					InfoLogger.Println(fmt.Sprintf("AOI %d failed to parse on survey %s", i, emp.Id))
				}
				taoi, err := strconv.Atoi(person[fmt.Sprintf("QID15_%d", i)].(string))
				if err != nil {
					taoi = 0
					InfoLogger.Println(fmt.Sprintf("AOI %d failed to parse on survey %s", i, emp.Id))
				}
				if maoi > 5 {
					aoi = aoi + marketList[i-1]
				}
				if taoi > 5 {
					aoi = aoi + techList[i-1]
				}
			}
			emp.AOI = aoi
			soc1, err := strconv.Atoi(person["QID26_1"].(string))
			if err != nil {
				InfoLogger.Println(fmt.Sprintf("Social score 1 for survey %s failed for: \n %s", emp.Id, err))
				soc1 = 0
			}
			soc2, err := strconv.Atoi(person["QID22_1"].(string))
			if err != nil {
				InfoLogger.Println(fmt.Sprintf("Social score 2 for survey %s failed for: \n %s", emp.Id, err))
				soc2 = 0
			}
			project, err := strconv.Atoi(person["QID23_2"].(string))
			if err != nil {
				InfoLogger.Println(fmt.Sprintf("Project count for survey %s failed for: \n %s", emp.Id, err))
				project = 0
			}
			emp.Social = (soc1+soc2)/2 + project
			emp.Status = 0
			emp.SaveNew()
		}
	}
}

func parseBool(a string) bool {
	if strings.TrimSpace(strings.ToLower(a)) == "yes" {
		return true
	}
	return false
}
