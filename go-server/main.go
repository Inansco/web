package main

import (
	"bytes"
	"encoding/json"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

type Booking struct {
	Name       string `json:"name"`
	Phone      string `json:"phone"`
	Email      string `json:"email,omitempty"`
	Address    string `json:"address"`
	Service    string `json:"service"`
	PickupDate string `json:"pickup_date"`
	PickupTime string `json:"pickup_time"`
	Details    string `json:"details,omitempty"`
}

var tmpl = template.Must(template.ParseFiles("templates/index.html"))

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	http.Handle(
		"/static/",
		http.StripPrefix(
			"/static/",
			http.FileServer(http.Dir("static")),
		),
	)

	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/book", bookingHandler)

	log.Println("Website running on port", port)

	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}

	if err := tmpl.Execute(w, nil); err != nil {
		http.Error(w, "Unable to load website", http.StatusInternalServerError)
	}
}

func bookingHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	if err := r.ParseForm(); err != nil {
		http.Error(w, "Invalid form", http.StatusBadRequest)
		return
	}

	booking := Booking{
		Name:       r.FormValue("name"),
		Phone:      r.FormValue("phone"),
		Email:      r.FormValue("email"),
		Address:    r.FormValue("address"),
		Service:    r.FormValue("service"),
		PickupDate: r.FormValue("pickup_date"),
		PickupTime: r.FormValue("pickup_time"),
		Details:    r.FormValue("details"),
	}

	jsonData, err := json.Marshal(booking)
	if err != nil {
		http.Error(w, "Unable to process booking", http.StatusInternalServerError)
		return
	}

	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	resp, err := client.Post(
		"http://127.0.0.1:8000/bookings",
		"application/json",
		bytes.NewBuffer(jsonData),
	)

	if err != nil {
		log.Println("FastAPI error:", err)
		http.Error(
			w,
			"Unable to submit booking. Please try again.",
			http.StatusBadGateway,
		)
		return
	}

	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		body, _ := io.ReadAll(resp.Body)

		log.Printf(
			"FastAPI returned %d: %s",
			resp.StatusCode,
			string(body),
		)

		http.Error(
			w,
			"Booking service returned an error.",
			http.StatusBadGateway,
		)
		return
	}

	http.Redirect(
		w,
		r,
		"/?booking=success#booking",
		http.StatusSeeOther,
	)
}