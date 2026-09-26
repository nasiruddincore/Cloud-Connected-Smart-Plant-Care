from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime

from automation.watering_engine import WateringEngine
from automation.plant_profiles import PLANT_PROFILES

app = FastAPI(title="Cloud-Connected Smart Plant Care API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

watering_engine = WateringEngine()

# In-memory database store simulation for student/local run
DEVICES_DB = {
    "PLANT-001": {
        "device_id": "PLANT-001",
        "plant_name": "Tomato Plant",
        "plant_type": "TOMATO",
        "soil_moisture": 35.0,
        "temperature": 28.5,
        "humidity": 60.0,
        "light_level": 75.0,
        "pump_status": "OFF",
        "threshold": PLANT_PROFILES["TOMATO"]["moisture_threshold"],
        "last_seen": datetime.now().isoformat()
    }
}

READINGS_HISTORY = []
ALERTS_LIST = []

class SensorPayload(BaseModel):
    deviceId: str
    soil: float
    temp: float
    hum: float
    light: Optional[float] = 50.0

@app.post("/api/sensors/data")
def ingest_sensor_data(payload: SensorPayload, x_api_key: Optional[str] = Header(None)):
    expected_key = os.getenv("API_KEY", "your_secure_shared_api_key_12345")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    
    dev_id = payload.deviceId
    if dev_id not in DEVICES_DB:
        raise HTTPException(status_code=404, detail="Device not registered")

    timestamp = datetime.now().isoformat()
    
    # Update device state
    device = DEVICES_DB[dev_id]
    device["soil_moisture"] = payload.soil
    device["temperature"] = payload.temp
    device["humidity"] = payload.hum
    device["light_level"] = payload.light
    device["last_seen"] = timestamp

    # Log reading history
    reading = {
        "device_id": dev_id,
        "soil_moisture": payload.soil,
        "temperature": payload.temp,
        "humidity": payload.hum,
        "light_level": payload.light,
        "timestamp": timestamp
    }
    READINGS_HISTORY.append(reading)

    # Evaluate automated watering
    decision = watering_engine.evaluate_watering(payload.soil, device["threshold"])
    if decision["action"]:
        device["pump_status"] = "ON"
        ALERTS_LIST.append({
            "alert_id": len(ALERTS_LIST) + 1,
            "device_id": dev_id,
            "alert_type": "WARNING",
            "message": f"{device['plant_name']} moisture ({payload.soil}%) dropped below threshold ({device['threshold']}%). Pump activated.",
            "status": "ACTIVE",
            "created_at": timestamp
        })
    else:
        device["pump_status"] = "OFF"

    return {"status": "success", "pump_action": device["pump_status"], "evaluation": decision}

@app.get("/api/devices")
def get_devices():
    return list(DEVICES_DB.values())

@app.get("/api/devices/{device_id}/latest")
def get_latest_reading(device_id: str):
    if device_id not in DEVICES_DB:
        raise HTTPException(status_code=404, detail="Device not found")
    return DEVICES_DB[device_id]

@app.get("/api/devices/{device_id}/history")
def get_history(device_id: str):
    return [r for r in READINGS_HISTORY if r["device_id"] == device_id]

@app.post("/api/devices/{device_id}/water")
def manual_water(device_id: str):
    if device_id not in DEVICES_DB:
        raise HTTPException(status_code=404, detail="Device not found")
    DEVICES_DB[device_id]["pump_status"] = "ON"
    return {"status": "success", "message": "Manual watering triggered, pump ON"}

@app.get("/api/alerts")
def get_alerts():
    return ALERTS_LIST