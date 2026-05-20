
from fastapi import FastAPI, Response, HTTP_200_OK
from fastapi.responses import CSVResponse
from typing import List
import csv
import datetime
from app.models.spend import Spend

app = FastAPI()

@app.get("/cost-insights/export", response_model=List[Spend])
async def export_spend():
    # Fetch spend data from the database
    # (Assuming you have a function `get_spend_data()` that returns a list of `Spend` objects)
    spend_data = get_spend_data()

    # Prepare CSV response
    csv_response = CSVResponse(
        media_type="text/csv",
        headers=[{"name": "date", "title": "Date"}, {"name": "account_id", "title": "Account ID"}, {"name": "spend", "title": "Spend"}],
    )

    # Write data to CSV response
    writer = csv.writer(csv_response)
    writer.writerow(["date", "account_id", "spend"])
    for spend in spend_data:
        writer.writerow([spend.date.strftime("%Y-%m-%d"), spend.account_id, spend.spend])

    # Set response status to 200 OK and return the CSV response
    return csv_response