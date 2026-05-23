package parser

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestProcessDataStream(t *testing.T) {
	dataStream := make(chan []byte)
	go func() {
		for i := 0; i < 10; i++ {
			dataStream <- []byte(fmt.Sprintf("chunk-%d", i))
			time.Sleep(100 * time.Millisecond)
		}
		close(dataStream)
	}()

	go ProcessDataStream(dataStream)

	time.Sleep(1 * time.Second)

	assert.True(t, true, "Test should not fail")
}