
// ... (existing imports)

func (c *Controller) StartDashboard() {
	http.HandleFunc("/", dashboardHandler)
	http.HandleFunc("/agent/connect", agentConnectHandler)

	go func() {
		if err := http.ListenAndServe(":8080", nil); err != nil {
			fmt.Println(err)
		}
	}()
}