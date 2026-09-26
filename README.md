# 🌿 Cloud-Connected Smart Plant Care & Watering System

![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end cloud-connected IoT platform designed to monitor environmental parameters—including soil moisture, air temperature, relative humidity, and light intensity—and automate plant irrigation through closed-loop threshold logic.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [System Objectives](#-system-objectives)
- [Industry Relevance & Use Cases](#-industry-relevance--use-cases)
- [System Architecture & Data Flow](#-system-architecture--data-flow)
- [Folder Structure](#-folder-structure)
- [Installation & Setup Guide](#-installation--setup-guide)
- [How to Run (Simulation Workflow)](#-how-to-run-simulation-workflow)
- [Author & License](#-author--license)

---

## 📌 Project Overview
Manual plant watering is inconsistent, frequently resulting in plant distress caused by over-watering or under-watering. This project solves these challenges by combining continuous sensor data collection with automated cloud-driven decisions, real-time threshold alert banners, and remote manual overrides via an interactive web dashboard.

---

## ⚠️ Problem Statement
* **Inconsistent Manual Watering:** Human schedules lack precision, leading to root rot or drought stress.
* **Lack of Visibility:** Traditional setups lack historical time-series data tracking and remote accessibility.
* **Hardware Barriers:** Students often lack physical microcontrollers to build IoT systems. This project solves this by providing a fully functional virtual IoT simulation engine.

---

## 🎯 System Objectives
1. **Real-Time Telemetry Tracking:** Monitor soil moisture, temperature, humidity, and light continuously.
2. **Closed-Loop Automation:** Evaluate sensor streams against a 30% moisture threshold to automatically trigger irrigation.
3. **Hardware-Free Execution:** Simulate microcontrollers and physical actuators purely through local Python processes.
4. **Interactive Dashboard:** Render dynamic Plotly trend charts and live KPI metrics via Streamlit.

---

## 🏭 Industry Relevance & Use Cases
* **Smart Agriculture & Precision Farming:** Optimizes water distribution across large agricultural grids.
* **Greenhouses & Nurseries:** Maintains automated climate and moisture control for sensitive crops.
* **Smart Homes & Indoor Gardening:** Powers automated residential plant companions and green walls.

---

## 📐 System Architecture & Data Flow
```text
[ Python IoT Sensor Simulator ]
               │
               ▼ (File Stream / Telemetry Log)
       [ data/plant_telemetry.csv ]
               │
               ▼
[ Interactive Streamlit Dashboard ] ◄── (Remote Commands) ──► [ actuator_cmd.txt ]
