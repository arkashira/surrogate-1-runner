package metadata

import (
	"database/sql"
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type MockDB struct {
	mock.Mock
}

func (m *MockDB) Exec(query string, args ...interface{}) (sql.Result, error) {
	args = append([]interface{}{query}, args...)
	return m.Called(args...).Get(0).(sql.Result), m.Called(args...).Error(1)
}

func TestExtractMetadata(t *testing.T) {
	modelArtifactJSON := []byte(`{
		"dataset_source": "example_dataset",
		"bias_metrics": {
			"metric1": 0.5,
			"metric2": 0.7
		}
	}`)

	expectedModelArtifact := &ModelArtifact{
		DatasetSource: "example_dataset",
		BiasMetrics: map[string]interface{}{
			"metric1": 0.5,
			"metric2": 0.7,
		},
	}

	actualModelArtifact, err := ExtractMetadata(modelArtifactJSON)
	assert.NoError(t, err)
	assert.Equal(t, expectedModelArtifact, actualModelArtifact)
}

func TestStoreMetadata(t *testing.T) {
	db := new(MockDB)
	db.On("Exec", mock.Anything, mock.Anything, mock.Anything).Return(nil, nil)

	modelArtifact := &ModelArtifact{
		DatasetSource: "example_dataset",
		BiasMetrics: map[string]interface{}{
			"metric1": 0.5,
			"metric2": 0.7,
		},
	}

	err := StoreMetadata(db, modelArtifact)
	assert.NoError(t, err)
}