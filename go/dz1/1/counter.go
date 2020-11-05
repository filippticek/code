package main

import "fmt"

func main() {
	numbers := []int{1, 2, 3, 4, 5, 1, 2, 3}
	solution := counter(numbers)
	fmt.Println(solution) 
}

func counter(numbers []int)  map[int]int {
	solution := make(map[int]int)

	for _, v := range numbers {
				
		if _, exist := solution[v]; exist == false {
			solution[v] = 1
		} else {
			solution[v] ++
		}	
	}
	
	return solution
}
