import pickle
import numpy as np
import os
from transformers import BertModel, BertTokenizer

class Ranker:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None

    def load_model(self):
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def score_build(self, build):
        inputs = self.tokenizer.encode_plus(
            build,
            add_special_tokens=True,
            max_length=512,
            return_token_type_ids=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        outputs = self.model(**inputs)
        return np.squeeze(outputs.last_hidden_state.mean(dim=1)).item()

    def rank_builds(self, builds):
        scores = [self.score_build(build) for build in builds]
        return sorted(zip(builds, scores), key=lambda x: x[1], reverse=True)[:3]

# /opt/axentx/surrogate-1/api/recommendations_test.py
import unittest
from api.recommendations import Ranker

class TestRanker(unittest.TestCase):
    def setUp(self):
        self.ranker = Ranker('/opt/axentx/surrogate-1/models/ranker.pkl')
        self.ranker.load_model()

    def test_score_build(self):
        build = "build with component A and B"
        score = self.ranker.score_build(build)
        self.assertIsNotNone(score)

    def test_rank_builds(self):
        builds = ["build with component A and B", "build with component C and D", "build with component E and F"]
        ranked_builds = self.ranker.rank_builds(builds)
        self.assertEqual(len(ranked_builds), 3)

## Summary
- Implemented `Ranker` class to load and use the ranking model.
- Added methods to score a build and rank multiple builds.
- Created a test suite for the `Ranker` class.
- Model inference time is expected to be <300 ms per build, depending on the specific model and hardware.