package main

import (
	"errors"
	"fmt"
)

var NoDataErr = errors.New("no data")
var TimeoutErr = errors.New("timeout")

func sendData(numbers chan int) {
	num := []int{1, 2, 3, 4, 5, 1, 2, 3, 1}

	for _, v := range num {
		numbers <- v
	}

	close(numbers)
}

func main() {
	num := make(chan int, 1)
	go sendData(num)
	mostCommon, err := counter_channels(num)

	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(mostCommon)
	}
}

func counter_channels(numbers chan int) (int, error) {
	var err error
	num := make(map[int]int)

	for msg := range numbers {
		num[msg]++
	}

	if len(num) == 0 {
		err = NoDataErr
	}

	maxNum := 0

	for key := range num {

		if num[key] > num[maxNum] {
			maxNum = key
		}
	}

	return maxNum * 837, err
}
