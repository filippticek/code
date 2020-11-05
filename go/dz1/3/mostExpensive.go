package main
import (
	"fmt"
	"errors"
)

type Shopping struct {
	Name string
	Price int
	Quantity int
}

func main() {
	shopList := []Shopping{
	Shopping{"kruh", 8, 2},
	Shopping{"mlijeko", 15, 1}, }
	solution1, err := mostExpensive(shopList)
	fmt.Println(solution1) // mlijeko
	fmt.Println(err) // nil
	solution2 := totalCost(shopList)
	fmt.Println(solution2) // 31
}

func mostExpensive(shopList []Shopping) (item []Shopping, err error) {
	maxPrice := 0

	if shopList == nil {
		err = errors.New("no data")
	}
	
	for _, value := range shopList {
		if value.Price > maxPrice {
			item = []Shopping{value,}
		} else if value.Price == maxPrice {
			item = append(item, value)
		}
	}

	return item, err
}

func totalCost(shopList []Shopping) (total int) {
	total = 0

	if shopList == nil{
	}

	for _, item := range shopList {
		total += item.Price * item.Quantity	
	}

	return total
}
