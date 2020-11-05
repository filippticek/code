package main

import (
	"log"
	"net/http"
	"strconv"
	"time"
)

func main() {
	s := &http.Server{
		Addr:           ":9210",
		Handler:        handler(),
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	log.Fatal(s.ListenAndServe())
}

func handler() http.HandlerFunc {
	return myFooBarHandler
}

func myFooBarHandler(w http.ResponseWriter, req *http.Request) {
	q := req.URL.Query()

	if num, err := strconv.Atoi(q["n"][0]); err == nil {

		for i := 1; i <= num; i++ {
			if i%5 == 0 && i%3 == 0 {
				w.Write([]byte("buz"))
			} else if i%5 == 0 {
				w.Write([]byte("bar"))
			} else if i%3 == 0 {
				w.Write([]byte("foo"))
			} else {
				w.Write([]byte(strconv.Itoa(i)))
			}
			w.Write([]byte(" "))
		}
	} else {
		w.WriteHeader(http.StatusBadRequest)
	}
}
