package memory

import (
	"sync"
)

type MemoryPool struct {
	pool sync.Pool
}

func NewMemoryPool() *MemoryPool {
	return &MemoryPool{
		pool: sync.Pool{
			New: func() interface{} {
				return make([]byte, 0)
			},
		},
	}
}

func (p *MemoryPool) Get(size int) []byte {
	buf := p.pool.Get().([]byte)
	if cap(buf) < size {
		buf = make([]byte, size)
	} else {
		buf = buf[:size]
	}
	return buf
}

func (p *MemoryPool) Put(buf []byte) {
	p.pool.Put(buf)
}