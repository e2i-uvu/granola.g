package main

import (
	"math/rand"
)

func GenerateScore(hire *PotentialHire) {
	score := int8(rand.Intn(0x0F))
	hire.Score = score
}
