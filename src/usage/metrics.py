from datetime import datetime, timedelta
from pymongo import MongoClient
import os

client = MongoClient(os.getenv('MONGO_URI'))
db = client['usage']
metrics = db['metrics']

def record_usage(model: str, endpoint: str, token_count: int, cost: float, user_id: int, team_id: int):
    metrics.insert_one({
        'timestamp': datetime.now(),
        'model': model,
        'endpoint': endpoint,
        'token_count': token_count,
        'cost': cost,
        'user_id': user_id,
        'team_id': team_id
    })

def aggregate_daily_totals():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    totals = metrics.aggregate([
        {'$match': {'timestamp': {'$gte': yesterday, '$lt': today}}},
        {'$group': {'_id': {'model': '$model', 'user_id': '$user_id', 'team_id': '$team_id'},
                    'total_token_count': {'$sum': '$token_count'},
                    'total_cost': {'$sum': '$cost'}}}
    ])

    # Save or expose totals via REST endpoint
    # ...