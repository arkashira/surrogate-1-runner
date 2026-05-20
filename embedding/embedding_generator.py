from .logger import EmbeddingLogger

class EmbeddingGenerator:
    def __init__(self, model):
        self.model = model
        self.logger = EmbeddingLogger()

    def generate_embeddings(self, document_chunks):
        try:
            embeddings = [self.model(chunk) for chunk in document_chunks]
            self.logger.log_success("Embeddings generated successfully.")
            return embeddings
        except Exception as e:
            self.logger.log_error(f"Error generating embeddings: {str(e)}")
            return None