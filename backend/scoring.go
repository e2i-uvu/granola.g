package main

import (
	"math/rand"
)

func GenerateScore(hire *PotentialHire) {

	hire.Score = int8(rand.Intn(0x0F))
}
