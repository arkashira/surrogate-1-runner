
package main

import (
	"fmt"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type Agent struct {
	ID      string
	Status  string
	SyncCh  chan string
	wsc     *websocket.Conn
	mu      sync.Mutex
	connected bool
}

func (a *Agent) Connect(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer conn.Close()

	a.wsc = conn
	a.connected = true

	for {
		_, message, err := conn.ReadMessage()
		if err != nil {
			fmt.Println(err)
			break
		}

		a.SyncCh <- message
	}
}

func (a *Agent) Send(message string) {
	a.mu.Lock()
	defer a.mu.Unlock()

	if a.connected {
		err := a.wsc.WriteMessage(websocket.TextMessage, []byte(message))
		if err != nil {
			fmt.Println(err)
			a.connected = false
		}
	}
}

func main() {
	// ... (existing code)

	http.HandleFunc("/agent/connect", func(w http.ResponseWriter, r *http.Request) {
		for _, agent := range agents {
			agent.Connect(w, r)
		}
	})

	// ... (existing code)
}