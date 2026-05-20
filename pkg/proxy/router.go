package proxy

import (
	"net"
	"sync"
)

type Router struct {
	rules []Rule
	mu    sync.RWMutex
}

func NewRouter(rules []Rule) *Router {
	return &Router{
		rules: rules,
	}
}

func (r *Router) Route(conn net.Conn) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	for _, rule := range r.rules {
		if rule.Matches(conn) {
			go rule.Handle(conn)
			return
		}
	}
}

func (r *Router) AddRule(rule Rule) {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.rules = append(r.rules, rule)
}