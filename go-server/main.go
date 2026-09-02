package main

import (
	"html/template"
	"log"
	"net/http"
	"os"
)

type Service struct {
	Title       string
	Description string
	Icon        string
}

type Pricing struct {
	Name     string
	Price    string
	Features []string
}

type Testimonial struct {
	Name   string
	Review string
}

type PageData struct {
	Services     []Service
	Pricing      []Pricing
	Testimonials []Testimonial
}

func main() {

	tmpl := template.Must(template.ParseFiles("templates/index.html"))

	services := []Service{
		{
			Title:       "Wash & Fold",
			Description: "Professional washing and folding for everyday clothes.",
			Icon:        "🧺",
		},
		{
			Title:       "Dry Cleaning",
			Description: "Premium care for suits and delicate fabrics.",
			Icon:        "👔",
		},
		{
			Title:       "Ironing Service",
			Description: "Perfectly pressed and wrinkle-free clothes.",
			Icon:        "✨",
		},
	}

	pricing := []Pricing{
		{
			Name:  "Basic Wash",
			Price: "$5",
			Features: []string{
				"5kg laundry",
				"Folded clothes",
				"24hr delivery",
			},
		},
		{
			Name:  "Premium Care",
			Price: "$10",
			Features: []string{
				"Dry cleaning",
				"Ironing included",
				"Same-day delivery",
			},
		},
		{
			Name:  "Business Package",
			Price: "$20",
			Features: []string{
				"Hotels & Offices",
				"Bulk laundry",
				"Priority support",
			},
		},
	}

	testimonials := []Testimonial{
		{
			Name:   "Blessing Okoye.",
			Review: "Excellent service and fast delivery.",
		},
		{
			Name:   "Efada Mary.",
			Review: "Affordable and professional service.",
		},
		{
			Name:   "Mercy Izekor.",
			Review: "The ironing service is top-notch!",
		},
	}

	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("static"))))

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {

		data := PageData{
			Services:     services,
			Pricing:      pricing,
			Testimonials: testimonials,
		}

		err := tmpl.Execute(w, data)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	})

	port := os.Getenv("PORT")

	if port == "" {
		port = "8080"
	}

	log.Println("Server running on port", port)

	http.ListenAndServe(":"+port, nil)

}
