
from fastapi import FastAPI

app = FastAPI(
    title="Intelligent Industrial Spare Parts Demand Prediction Platform"
)

spare_parts = [
    {
        "id": 1,
        "name": "Motor Bearing",
        "stock": 20,
        "criticality": "High"
    },
    {
        "id": 2,
        "name": "Air Filter",
        "stock": 50,
        "criticality": "Medium"
    }
]


@app.get("/")
def home():
    return {
        "message": "Spare Parts Demand Prediction Platform",
        "status": "Application is running"
    }


@app.get("/spare-parts")
def get_spare_parts():
    return spare_parts


@app.get("/alerts")
def get_alerts():
    return [
        part for part in spare_parts
        if part["stock"] < 10
    ]
