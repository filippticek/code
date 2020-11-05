package main

import (
	"fergo.info.tm/homework3/pets/animals"
)

type Parrot struct {
	parrotName string
}

func (c *Parrot) Color() string { // leave this also here to see if we have a problem with it
	return "multicolor"
}

func (c *Parrot) NameSet(name string) {
	c.parrotName = name
}

func (c *Parrot) NameGet() string {
	return c.parrotName
}

func (c *Parrot) Species() string {
	return "Parrot"
}

func (c *Parrot) Sound() string {
	return "squak"
}

func count_animals(pets []animals.Animal) map[string]int {
	count := make(map[string]int)

	for _, pet := range pets {
		pet_type := pet.Species()
		if _, exist := count[pet_type]; exist == false {
			count[pet_type] = 1
		} else {
			count[pet_type]++
		}

	}
	return count
}

func count_cats(pets []animals.Animal) int {
	count := 0

	for _, pet := range pets {
		if pet.Species() == "Cat" {
			count++
		}
	}
	return count
}
