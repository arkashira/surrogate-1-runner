package main

import (
	"fmt"
	"log"

	"github.com/sendgrid/sendgrid-go"
	"github.com/sendgrid/sendgrid-go/helpers/mail"
)

type BudgetAlert struct {
	Threshold float64
	Email     string
}

func NewBudgetAlert(threshold float64, email string) *BudgetAlert {
	return &BudgetAlert{
		Threshold: threshold,
		Email:     email,
	}
}

func (ba *BudgetAlert) CheckAndSendAlert(currentCost float64) {
	if currentCost > ba.Threshold {
		ba.sendEmailAlert(currentCost)
	}
}

func (ba *BudgetAlert) sendEmailAlert(currentCost float64) {
	from := mail.NewEmail("Budget Alert System", "budget-alert@example.com")
	subject := "Budget Alert Notification"
	to := mail.NewEmail(ba.Email, ba.Email)
	plainContent := fmt.Sprintf("Your current cost of %.2f exceeds the set threshold of %.2f.", currentCost, ba.Threshold)
	message := mail.NewSingleEmail(from, subject, to, plainContent, "")

	client := sendgrid.NewSendClient("SENDGRID_API_KEY")
	response, err := client.Send(message)
	if err != nil {
		log.Println(err)
	} else {
		fmt.Println(response.StatusCode)
		fmt.Println(response.Body)
		fmt.Println(response.Headers)
	}
}

func main() {
	alert := NewBudgetAlert(1000.0, "user@example.com")
	alert.CheckAndSendAlert(1200.0)
}