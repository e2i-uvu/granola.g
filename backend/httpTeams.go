package main

import (
	"net/http"
)

func TeamsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.Header.Get("Content-Type") == "application/json" {
		// Takes in
		//{
		//   "project_name": "Video Game and Website",
		//   "project_type": "Tech",
		//   "employees": [
		//   "id":""
		//   "id":""
		//   "id":""
		//   ]
		// }
		// saves project to projects and then adds the employee ids and project ids to many to many table
	}
	if r.Method == "GET" && r.Header.Get("Content-Type") == "application/json" {
		// BuildTeams()
	}
}
