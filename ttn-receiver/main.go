package main

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

// Note: Data is written to /data, mount that volume to get it.

func writeFile(w http.ResponseWriter, r *http.Request) {
	if r.Header.Get("Content-Type") != "application/json" {
		return
	}

    dataBytes, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Println(err)
		return
	}

	f, err := os.OpenFile("/data/data.json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Println(err)
		return
	}
	defer f.Close()

	if _, err := f.Write(dataBytes); err != nil {
		log.Println(err)
		return
	}

	if _, err := f.WriteString("\n"); err != nil {
		log.Println(err)
	}

	log.Println("New data written")
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", writeFile)
    log.Println("Started")
    err := http.ListenAndServe(":8080", mux)
    log.Fatal(err)
}
