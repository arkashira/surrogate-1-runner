
import logging
from datetime import datetime

class VectorStoreLogger:
    def __init__(self, log_file='vector_store.log'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_storage(self, success, message):
        log_level = logging.INFO if success else logging.ERROR
        self.logger.log(log_level, f"[{datetime.now()}] Storage process - {message}")

# opt/axentx/surrogate-1/vector_store/vector_store.py

# ... (other imports and classes)

class VectorStore:
    # ... (other methods)

    def store_embedding(self, embedding, metadata):
        logger = VectorStoreLogger()
        try:
            # Store embedding logic here
            logger.log_storage(True, f"Successfully stored embedding - {metadata['id']}")
        except Exception as e:
            logger.log_storage(False, f"Failed to store embedding - {metadata['id']}: {str(e)}")

# opt/axentx/surrogate-1/tests/test_vector_store.py

# ... (other imports and tests)

def test_vector_store_logging(mocker):
    logger_mock = mocker.patch('vector_store.VectorStoreLogger')
    vector_store = VectorStore()

    # Test successful storage
    vector_store.store_embedding('test_embedding', {'id': 'test_id'})
    logger_mock().log_storage.assert_called_with(True, "Successfully stored embedding - test_id")

    # Test failed storage
    vector_store.store_embedding('test_embedding', {'id': 'test_id'})  # This should fail
    logger_mock().log_storage.assert_called_with(False, "Failed to store embedding - test_id: 'test_embedding' does not match any known schema")

## Summary
- Added a `VectorStoreLogger` class to handle logging for the vector store.
- Integrated the logger into the `VectorStore` class for storing embeddings.
- Created a test to verify that the logger is called correctly in both success and failure scenarios.