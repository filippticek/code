package someRandomPackage_test

import (
	"testing"
)

func TestTotalCostExpensive(t *testing.T) {
	mockItems := []mockShopping{
		{
			Name:     "Ajvar",
			Price:    9,
			Type:     "Prehrana",
			Quantity: 3,
		},
		{
			Name:     "Jabuka",
			Price:    5,
			Type:     "Prehrana",
			Quantity: 1,
		},
	}

	total, err := pac.totalCost(mockItems)

	if err != nil {
		t.Errorf("unexpected error %q", err)
	}

	if err != error.New("Too expensive item") {
		t.Errorf("Wrong error %q", err)
	}
}

func TestTotalCostType(t *testing.T) {
	mockItems := []mockShopping{
		{
			Name:     "Ajvar",
			Price:    2,
			Type:     "Umak",
			Quantity: 3,
		},
		{
			Name:     "Jabuka",
			Price:    5,
			Type:     "Prehrana",
			Quantity: 1,
		},
	}

	total, err := pac.totalCost(mockItems)

	if err != nil {
		t.Errorf("unexpected error %q", err)
	}

	if err != error.New("Item not allowed") {
		t.Errorf("Wrong error %q", err)
	}
}

type mockShopping struct {
	Name     string
	Price    int
	Type     string
	Quantity int
	err      error
}
