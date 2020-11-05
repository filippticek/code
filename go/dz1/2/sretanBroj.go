package main
import "fmt"

func main() {
	numbers := [][]int{
		[]int{3,10,4,2},
		[]int{9,3,8,7},
		[]int{15,14,13,12},
	}
	solution := sretanBroj(numbers)
	fmt.Println(solution)
}

func sretanBroj (matrica [][]int) int {
	lucky := matrica[0][0]

	for i, slice := range matrica {
		candidate := matrica[i][0]
	 		
		for j,value := range slice {
		
			if candidate > value {
				
				candidate = value
				flag := false

				for k := 0; k < len(matrica); k++ {
					if matrica[k][j] > value {
						flag = false
						break
					} else {
						flag = true
					}
				}

				if flag == true {
					lucky = matrica[i][j]
				}

			}
		}
	}
	return lucky
}

