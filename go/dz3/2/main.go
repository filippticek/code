package main

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

type webResponseEven struct {
	Number int  `json:"n"`
	Even   bool `json:"even"`
}
type webResponseSquare struct {
	Number int `json:"n"`
	Square int `json:"s"`
}

func main() {
	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Get("/", hello)
	r.Get("/even/{n}", even)
	r.Get("/square/{n}", square)
	log.Panic(http.ListenAndServe(":3333", r))

}
func hello(w http.ResponseWriter, r *http.Request) {
	_, _ = w.Write([]byte("fergo!"))

}
func even(w http.ResponseWriter, r *http.Request) {
	var res webResponseEven
	var err error
	res.Number, err = strconv.Atoi(chi.URLParam(r, "n"))

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
	} else {
		if res.Number%2 == 0 {
			res.Even = true
		} else if res.Number%2 != 0 {
			res.Even = false
		}
		json.NewEncoder(w).Encode(res)
	}
}
func square(w http.ResponseWriter, r *http.Request) {
	// nadopuniti
	var res webResponseSquare
	var err error
	res.Number, err = strconv.Atoi(chi.URLParam(r, "n"))

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
	} else {
		res.Square = res.Number * res.Number
		json.NewEncoder(w).Encode(res)
	}

}
