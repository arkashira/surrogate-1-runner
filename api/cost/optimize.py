ec2_optimize/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── config.py        # env vars + defaults
│   ├── models.py        # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ec2_optimizer.py   # core logic
│   │   ├── audit.py           # DynamoDB audit helper
│   │   └── slack.py           # Slack notifier
│   └── utils/
│       ├── __init__.py
│       └── pricing.py         # Pricing cache
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_optimize.py
├── requirements.txt
└── Dockerfile