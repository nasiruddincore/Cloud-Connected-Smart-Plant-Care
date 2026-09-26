import os
import time
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Smart Plant Care Dashboard", page_icon="🌿", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "plant_telemetry.csv")
CMD_FILE = os.path.join(DATA_DIR, "actuator_cmd.txt")

def set_command(cmd: str):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CMD_FILE, "w") as f:
        f.write(cmd)

st.title("🌿 Cloud-Connected Smart Plant Care & Automation Portal")
st.markdown("Monitor real-time sensor streams and manage automated threshold irrigation rules.")

st.sidebar.header("⚙️ Automation & Control")

# Control Buttons
if st.sidebar.button("🤖 Enable AUTO Mode"):
    set_command("AUTO")
    st.sidebar.success("System set to Automated Threshold Mode")

if st.sidebar.button("🌊 Force Pump ON"):
    set_command("PUMP_ON")
    st.sidebar.warning("Manual Override: Pump Activated")

if st.sidebar.button("🛑 Force Pump OFF"):
    set_command("PUMP_OFF")
    st.sidebar.error("Manual Override: Pump Stopped")

placeholder = st.empty()

while True:
    if os.path.exists(DATA_FILE) and os.stat(DATA_FILE).st_size > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            if not df.empty:
                latest = df.iloc[-1]
                
                with placeholder.container():
                    st.subheader(f"Live Node Status: {latest['device_id']}")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Soil Moisture", f"{latest['soil_moisture']}%")
                    c2.metric("Temperature", f"{latest['temperature_c']}°C")
                    c3.metric("Humidity", f"{latest['humidity']}%")
                    c4.metric("Pump Status", latest['pump_status'])
                    
                    # Real-time automated health check banner
                    if latest['soil_moisture'] < 30.0:
                        st.error("⚠️ AUTOMATION ALERT: Soil moisture below 30% threshold! Irrigation active or required.")
                    elif latest['soil_moisture'] > 75.0:
                        st.info("ℹ️ Optimal Moisture: Target threshold reached. System maintaining health.")
                    else:
                        st.success("✅ Plant Status: Healthy & Stable")
                    
                    st.markdown("### 📊 Environmental & Moisture Analytics")
                    chart_data = df.tail(30)
                    
                    colA, colB = st.columns(2)
                    with colA:
                        fig_moisture = px.line(chart_data, x="timestamp", y="soil_moisture", title="Soil Moisture Trend (%)", color_discrete_sequence=["#1E90FF"])
                        st.plotly_chart(fig_moisture, use_container_width=True)
                    with colB:
                        fig_temp = px.line(chart_data, x="timestamp", y=["temperature_c", "humidity"], title="Temperature & Humidity Profiles", color_discrete_sequence=["#FF4500", "#32CD32"])
                        st.plotly_chart(fig_temp, use_container_width=True)
                        
        except Exception as e:
            st.warning(f"Synchronizing telemetry logs... ({e})")
    else:
        st.info("⏳ Waiting for simulator data logs... Run `python python_simulation/sensor_sim.py` in Terminal 1.")
                
    time.sleep(2)