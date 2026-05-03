curl -X PATCH \
  http://localhost:8000/requests/1/status \
  -H 'Content-Type: application/json' \
  -d '{"status": "in_progress", "actor": "John Doe"}'