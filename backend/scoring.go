package main

import (
// "github.com/Kunde21/numgo"
// "math/rand"
// "fmt"
)

// NOTE: numgo data types/arrays only accept float64 or bool values as elements. Good news: we don't need to use them to find a dot product between two arrays of int8 :D.

func GenerateScore(hire *PotentialHire) {
	// Mock arrays
	weights := [2]int8{3, 2}
	candidateScores := [2]int8{hire.Enjoyment, hire.Social}
	// fmt.Printf("%d, %d", candidateScores[0], candidateScores[1])

	// Validate arrays
	if len(weights) != len(candidateScores) {
		// panic()
	}

	// Calcualte score
	var score int8

	for i := 0; i < 2; i++ {
		score += weights[i] * candidateScores[i] // fmt.Println(score)
	}

	//score := int8(rand.Intn(0x0F))
	hire.Score = score
}
