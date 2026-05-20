package models

type Alert struct {
	ID        string
	Message   string
	Timestamp time.Time
}