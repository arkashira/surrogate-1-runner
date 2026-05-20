
package websocket

import (
	"encoding/json"
	"fmt"
	"log"
	"net/url"
	"sync"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type Collaboration struct {
	clients     map[*websocket.Conn]bool
	broadcast   chan []byte
	register    chan *websocket.Conn
	unregister  chan *websocket.Conn
	sync.RWMutex
}

func NewCollaboration() *Collaboration {
	return &Collaboration{
		clients:    make(map[*websocket.Conn]bool),
		broadcast:  make(chan []byte),
		register:   make(chan *websocket.Conn),
		unregister: make(chan *websocket.Conn),
	}
}

func (c *Collaboration) ServeWs(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		return
	}
	defer conn.Close()

	c.Lock()
	c.clients[conn] = true
	c.Unlock()

	for msg := range c.broadcast {
		err := conn.WriteMessage(websocket.TextMessage, msg)
		if err != nil {
			log.Println(err)
			return
		}
	}

	go func() {
		for {
			_, msg, err := conn.ReadMessage()
			if err != nil {
				log.Println(err)
				break
			}

			c.broadcast <- msg
		}

		c.Lock()
		delete(c.clients, conn)
		c.Unlock()
	}()
}

func (c *Collaboration) Register(conn *websocket.Conn) {
	c.Lock()
	c.register <- conn
	c.Unlock()
}

func (c *Collaboration) Unregister(conn *websocket.Conn) {
	c.Lock()
	c.unregister <- conn
	c.Unlock()
}

func (c *Collaboration) Broadcast(data []byte) {
	c.Lock()
	for client := range c.clients {
		client.WriteMessage(websocket.TextMessage, data)
	}
	c.Unlock()
}

func (c *Collaboration) Start() {
	http.HandleFunc("/collaboration", func(w http.ResponseWriter, r *http.Request) {
		c.ServeWs(w, r)
	})

	go func() {
		for {
			conn := <-c.register
			c.Lock()
			c.clients[conn] = true
			c.Unlock()
		}
	}()

	go func() {
		for {
			conn := <-c.unregister
			c.Lock()
			delete(c.clients, conn)
			c.Unlock()
		}
	}()
}