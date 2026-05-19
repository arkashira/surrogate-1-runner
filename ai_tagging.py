import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class AiTagging:
    def __init__(self, model_name='distilbert-base-uncased'):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tag(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return torch.softmax(outputs.logits, dim=-1).numpy()[0]  # Return probability distribution

# /opt/axentx/surrogate-1/search.py
import time
from whoosh.qparser import QueryParser
from whoosh import index
from ai_tagging import AiTagging

class Search:
    def __init__(self, index_path='indexdir'):
        self.index = index.open_dir(index_path)
        self.ai_tagging = AiTagging()

    def search(self, query):
        start_time = time.time()
        parser = QueryParser("content", self.index.schema)
        q = parser.parse(query)
        with self.index.searcher() as searcher:
            results = searcher.search(q)
        
        # Apply AI tagging and calculate combined score
        scored_results = []
        for result in results:
            content = result['content']
            tag_scores = self.ai_tagging.tag(content)
            # Combine Whoosh relevance with AI tagging (weighted average)
            combined_score = 0.7 * result.score + 0.3 * max(tag_scores)  # Adjust weights as needed
            scored_results.append({
                'text': result['content'],
                'whoosh_score': result.score,
                'ai_score': max(tag_scores),
                'combined_score': combined_score
            })
        
        # Sort by combined score
        scored_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        end_time = time.time()
        print(f'Search completed in {end_time - start_time:.2f} seconds')
        return scored_results