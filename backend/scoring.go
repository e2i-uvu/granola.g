package main

import (
	"math/rand"
)

func GenerateScore() (num int8) {

	return int8(rand.Intn(0x0F))
}
