import csv
import os
import time
import random
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CSV_PATH = os.path.join(DATA_DIR, "plant_telemetry.csv")
CMD_PATH = os.path.join(DATA_DIR, "actuator_cmd.txt")

def init_system():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            csv.writer(f).writerow(["timestamp", "device_id", "soil_moisture", "temperature_c", "humidity", "light_lux", "pump_status"])
    if not os.path.exists(CMD_PATH):
        with open(CMD_PATH, "w") as f:
            f.write("AUTO")

def run_plant_node():
    init_system()
    print("🌱 Smart Plant Automated IoT Node Active. Press Ctrl+C to stop.")
    
    soil_moisture = 55.0
    temperature = 26.5
    humidity = 62.0
    light_lux = 650.0
    auto_pump_active = False

    while True:
        # Read dashboard command state (AUTO, PUMP_ON, PUMP_OFF)
        if os.path.exists(CMD_PATH):
            with open(CMD_PATH, "r") as f:
                mode = f.read().strip()
        else:
            mode = "AUTO"
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # --- AUTOMATED THRESHOLD & PHYSICS ENGINE ---
        if mode == "PUMP_ON":
            pump_status = "ON (Manual Override)"
            soil_moisture = min(100.0, soil_moisture + 5.0)
        elif mode == "PUMP_OFF":
            pump_status = "OFF (Manual Override)"
            soil_moisture = max(0.0, soil_moisture - 0.4)
        else:  # AUTO MODE (Closed-Loop Automation)
            if soil_moisture <= 30.0:
                auto_pump_active = True
            elif soil_moisture >= 75.0:
                auto_pump_active = False
                
            if auto_pump_active:
                pump_status = "ON (Automated)"
                soil_moisture = min(100.0, soil_moisture + 5.0)
            else:
                pump_status = "OFF (Automated)"
                soil_moisture = max(0.0, soil_moisture - 0.3)
            
        temperature = round(temperature + random.uniform(-0.3, 0.3), 2)
        humidity = round(humidity + random.uniform(-0.6, 0.6), 2)
        light_lux = random.randint(300, 950)
            
        with open(CSV_PATH, "a", newline="") as f:
            csv.writer(f).writerow([timestamp, "PLANT-001", round(soil_moisture, 1), temperature, humidity, light_lux, pump_status])
            
        print(f"[{timestamp}] Soil: {soil_moisture:.1f}% | Mode: {mode} | Pump: {pump_status}")
        time.sleep(2)

if __name__ == "__main__":
    run_plant_node()