package websocket

import (
	"fmt"
	"log"
	"sync"

	"github.com/gorilla/websocket"
)

type Collaboration struct {
	clients    map[*websocket.Conn]bool
	broadcast  chan []byte
	register   chan *websocket.Conn
	unregister chan *websocket.Conn
	mu         sync.Mutex
}

func NewCollaboration() *Collaboration {
	return &Collaboration{
		clients:    make(map[*websocket.Conn]bool),
		broadcast:  make(chan []byte),
		register:   make(chan *websocket.Conn),
		unregister: make(chan *websocket.Conn),
	}
}

func (c *Collaboration) Run() {
	for {
		select {
		case client := <-c.register:
			c.mu.Lock()
			c.clients[client] = true
			c.mu.Unlock()
		case client := <-c.unregister:
			c.mu.Lock()
			if _, ok := c.clients[client]; ok {
				delete(c.clients, client)
				close(client)
			}
			c.mu.Unlock()
		case message := <-c.broadcast:
			c.mu.Lock()
			for client := range c.clients {
				err := client.WriteMessage(websocket.TextMessage, message)
				if err != nil {
					log.Printf("error: %v", err)
					client.Close()
					delete(c.clients, client)
				}
			}
			c.mu.Unlock()
		}
	}
}

func (c *Collaboration) Serve(ws *websocket.Conn) {
	defer ws.Close()

	c.register <- ws
	defer func() { c.unregister <- ws }()

	for {
		_, message, err := ws.ReadMessage()
		if err != nil {
			break
		}
		c.broadcast <- message
	}
}

func ExampleCollaboration() {
	c := NewCollaboration()
	go c.Run()

	ws, _, _ := websocket.DefaultDialer.Dial("ws://localhost:8080/ws", nil)
	defer ws.Close()

	c.Serve(ws)

	fmt.Println("Example completed")
}