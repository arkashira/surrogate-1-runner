
package models

import (
	"encoding/csv"
	"encoding/xml"
	"io"
	"os"
	"path/filepath"
)

type Invoice struct {
	ID          string   `json:"id"`
	Date        string   `json:"date"`
	Total       float64  `json:"total"`
	Items       []Item   `json:"items"`
	Vendor      string   `json:"vendor"`
	Format      string   `json:"format"`
	File        string   `json:"file"`
}

type Item struct {
	ID          string `json:"id"`
	Description string `json:"description"`
	Quantity    int    `json:"quantity"`
	Price       float64 `json:"price"`
}

func NewInvoice(r io.Reader) (*Invoice, error) {
	var invoice Invoice
	switch invoice.Format {
	case "csv":
		reader := csv.NewReader(r)
		if err := reader.Read(); err != nil {
			return nil, err
		}
		invoice.Items = []Item{}
		for {
			record, err := reader.Read()
			if err == io.EOF {
				break
			}
			if err != nil {
				return nil, err
			}
			item := Item{
				ID:          record[0],
				Description: record[1],
				Quantity:    int(record[2][:len(record[2])-2]), // Remove trailing comma
				Price:       record[3][:len(record[3])-2],       // Remove trailing comma
			}
			invoice.Items = append(invoice.Items, item)
		}
	case "pdf":
		// TODO: Implement PDF parsing
		return nil, ErrUnsupportedFormat
	case "xml":
		decoder := xml.NewDecoder(r)
		if err := decoder.Decode(&invoice); err != nil {
			return nil, err
		}
	default:
		return nil, ErrUnsupportedFormat
	}
	return &invoice, nil
}

func (i *Invoice) Save() error {
	dir := filepath.Join(os.Getenv("DATA_DIR"), "invoices")
	err := os.MkdirAll(dir, 0755)
	if err != nil {
		return err
	}
	file, err := os.Create(filepath.Join(dir, i.ID+".json"))
	if err != nil {
		return err
	}
	defer file.Close()
	return json.NewEncoder(file).Encode(i)
}