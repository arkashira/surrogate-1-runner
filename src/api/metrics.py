from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/metrics")
async def get_metrics():
    try:
        with open("metrics.json", 'r') as f:
            lines = f.readlines()
            metrics = [json.loads(line) for line in lines]
        return metrics
    except FileNotFoundError:
        return {"error": "Metrics file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid metrics data"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)