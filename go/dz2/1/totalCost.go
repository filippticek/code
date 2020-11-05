package main

import (
	"errors"
	"fmt"
)

//Shopping ...
type Shopping struct {
	Name     string
	Price    int
	Quantity int
}

var ToExpensiveErr = errors.New("Too expensive item")

func sendData(numbers chan Shopping) {
	shopList := []Shopping{
		Shopping{"Kruh", 8, 2},
		//	Shopping{"Gitara", 150, 1}, // ovo je pogreska
		Shopping{"Mlijeko", 15, 1},
	}

	for _, item := range shopList {
		numbers <- item
	}

	close(numbers)
}

func main() {
	num := make(chan Shopping, 1)
	go sendData(num)
	mostCommon, err := totalCost(100, num)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println("Total cost is", mostCommon) // rezultat primjera je 31
	}
}

func totalCost(maxPrice int, numbers chan Shopping) (int, error) {
	total := 0
	var err error

	for shop := range numbers {
		if shop.Price > maxPrice {
			err = ToExpensiveErr
		}
		total += shop.Price * shop.Quantity
	}
	return total, err
}
