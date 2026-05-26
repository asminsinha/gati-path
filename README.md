# Gati-Path: Real-Time IoT Telemetry Processing and Predictive Transit Delay Engine

Gati-Path is an operational backend framework designed to process high-frequency IoT telemetry streams from a commercial transport fleet. The system ingests spatial and vehicular diagnostic payloads, tracks asset states dynamically in memory, and evaluates potential transit risk boundaries using a tabular Random Forest classifier coupled with local SHAP (SHapley Additive exPlanations) feature attribution.

---

# Architecture Overview

The system is engineered as a decoupled, multi-tier data processing pipeline capable of handling simultaneous inbound data streams.

## Ingestion and Network Routing Layer

### Production Mode (MQTT Protocol)

Real-world deployment relies on vehicle-mounted hardware telemetry units containing a 4G LTE/5G cellular modem and GNSS/GPS receivers. Telemetry parameters are serialized into lightweight JSON packets and broadcast over the air to an MQTT broker (e.g., HiveMQ / Mosquitto).

A dedicated `real_hardware_listener.py` script acts as a persistent background client, subscribing to the fleet wildcard topic:

```plaintext
vitarai/fleet/telemetry/#
```

It decodes inbound telemetry packets and maps them into HTTP POST requests forwarded concurrently to the FastAPI application layer.

### Simulation Mode

For development and testing environments, `simulate_iot.py` programmatically replicates the same telemetry behavior while preserving the exact production payload schema and network flow.

---

# Core Processing and Analytics Layer

The backend is built using FastAPI and exposes a unified telemetry endpoint:

```plaintext
/gati-path/iot-ping
```

The endpoint is managed through an asynchronous processing layer defined in `router.py`.

The processing pipeline performs:

- Telemetry ingestion
- Route metadata enrichment
- Driver fatigue evaluation
- Delay probability estimation
- SHAP explainability analysis
- Dynamic operational analytics
- Live fleet state synchronization

All active vehicle contexts are maintained inside an in-memory fleet state engine for real-time dashboard rendering.

---

# Machine Learning & Predictive Modeling

The predictive engine evaluates operational transit risk using tabular machine learning and feature attribution analysis.

---

## Dataset and Training Profile

### Source

The underlying dataset was derived from logistics transport records obtained through the Kaggle Core repository.

### Data Partitioning

The training workflow follows a strict dataset split:

- **80% Training Set**
- **20% Validation / Testing Set**

This ensures proper generalization evaluation during inference.

---

## Model Selection

A **500-Tree Random Forest Classifier** was selected for production deployment due to:

- Robustness against multi-collinear sensor features
- Stable decision boundary generation
- Strong tabular classification performance
- Resistance to localized overfitting
- Reliable handling of nonlinear operational constraints

---

# Explainable AI Layer

The ML engine integrates SHAP (SHapley Additive exPlanations) for transparent operational reasoning.

The explainability layer identifies:

- Dominant delay contributors
- Traffic pressure influence
- Driver fatigue escalation
- Weather-based operational risk
- Structural routing anomalies

Each prediction is coupled with localized feature attribution scores for dashboard interpretability.

---

# Core Engineering Domains Demonstrated

This project combines multiple interdisciplinary engineering domains into a unified operational platform:

- Real-Time IoT Telemetry Processing
- Explainable Machine Learning (SHAP-based inference reasoning)
- Predictive Transit Delay Analytics
- Fleet Intelligence & Operational Risk Modeling
- Stateful Streaming Data Simulation
- FastAPI Backend Systems Engineering
- MQTT-Based Distributed Telemetry Routing
- Dynamic Driver Behavioral Analytics
- Infrastructure-Aware Route Intelligence
- Real-Time Visualization & Monitoring Dashboards
- Multi-Layer Operational Alert Systems
- Applied Systems Architecture for Logistics Technology


# Performance Analysis

## Validation Accuracy

The Random Forest model stabilizes between:

```plaintext
75.33% → 78.50%
```

validation accuracy across multiple retraining cycles.

---

## Why Accuracy Is Intentionally Capped Around 75–80%

Real-world logistics systems contain stochastic variables not entirely represented within historical telemetry datasets.

These include:

- Sudden traffic bottlenecks
- Weather anomalies
- Dock-side customs delays
- Road surface degradation
- Infrastructure rerouting
- Mechanical exceptions
- Human behavioral variance

Artificially pushing the model toward extremely high accuracy risks localized overfitting and operational instability.

Maintaining this range preserves better real-world generalization behavior.

---

# Simulation Mechanics and Asset Logic

The `simulate_iot.py` subsystem models the behavioral physics of multiple freight vehicles traveling across major Indian economic corridors.

---

## Simulation State Engine

Each vehicle updates independently inside a continuous telemetry loop.

The simulation dynamically evolves:

- GPS coordinates
- Fuel consumption
- Cargo impact
- Driver fatigue
- Delay accumulation
- Rest-cycle behavior

---

## GPS Translation Dynamics

Vehicle movement is simulated using directional coordinate step vectors:

```python
lat_step
lng_step
```

Each cycle advances the truck toward designated logistics terminals such as:

- Mumbai
- Delhi
- Bangalore
- Kolkata

---

## Fuel Consumption Model

Fuel depletion scales dynamically against cargo weight.

### Formula

```math
Fuel Consumption Rate = 1.0 + (Cargo Load / 5000)
```

Heavier payloads produce accelerated fuel drain and higher idling loss exposure.

---

## Driver Fatigue Modeling

The variable:

```python
hours_driven_without_rest
```

continuously accumulates over operational cycles.

When the analytics engine detects a compliance breach:

- The backend activates a fatigue lock
- The simulator halts route progression
- The vehicle transitions into a mandatory rest state
- Movement resumes only after cooldown completion

---

# Time Compression Engine

To enable realistic stress-testing without requiring multi-hour execution windows:

- Real-world driving timelines are compressed
- Every simulation cycle spans roughly 15–20 minutes of operational progression
- Telemetry packets are emitted every 2 seconds

This enables rapid dashboard evolution and analytics validation.

---

# Behavioral Analytics Engine

The backend dynamically computes operational metrics using rolling telemetry windows.

---

## Fuel Efficiency Index

Measures:

- Idling overhead
- Cargo weight impact
- Financial fuel waste
- Congestion-induced burn rates

The score degrades during heavy traffic stagnation and inefficient routing.

---

## Safety & Smoothness Score

Computed using rolling speed variance calculations.

The system penalizes:

- Sudden acceleration
- Harsh braking
- Fatigue escalation
- Speed instability

This models real-world operational driving smoothness.

---

## Operational Agility Score

Derived from:

- GPS displacement vectors
- Movement continuity
- Traffic stagnation
- Detour maneuvering

Vehicles trapped in congestion experience reduced agility scores, while successful rerouting increases operational mobility metrics.

---

# Installation & Environment Setup

---

## 1. Prerequisites

Ensure the host machine contains:

- Python 3.10+
- pip package manager
- Node.js (only required for frontend compilation)

Tested up to:

```plaintext
Python 3.14
```

---

## 2. Create Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install fastapi uvicorn httpx paho-mqtt scikit-learn shap pandas numpy requests
```

---

# Frontend Static Integration

To allow the platform to run completely standalone without requiring a separate frontend development server:

1. Build the frontend project:

```bash
npm run build
```

2. Locate the generated `dist/` directory.

3. Move the compiled `dist/` folder into the backend root directory alongside:

```plaintext
app.py
```

The FastAPI static layer will automatically expose the dashboard UI.

---

# Execution Manual

The project includes a centralized orchestration framework:

```plaintext
run.py
```

This launcher coordinates:

- Backend initialization
- ML engine loading
- Telemetry synchronization
- MQTT listener startup
- Simulation startup
- Process lifecycle management

---

# Starting the System

Launch the orchestrator:

```bash
python run.py
```

---

# Runtime Lifecycle Flow

## 1. Backend Initialization

The orchestrator launches the FastAPI backend through Uvicorn.

---

## 2. ML Engine Bootstrap

The backend:

- Loads the logistics dataset
- Trains the 500-tree Random Forest
- Initializes the SHAP TreeExplainer
- Builds inference feature mappings

---

## 3. Active Socket Polling

The orchestrator continuously checks:

```plaintext
127.0.0.1:8000
```

Telemetry injection remains paused until the backend becomes reachable.

---

## 4. Execution Mode Selection

Once initialization completes:

```plaintext
==============================================================
 GATI-PATH: INTELLIGENT LOGISTICS ENGINE CORE ORCHESTRATOR
==============================================================

Select your live data ingestion architecture:

 [1] SIMULATION MODE   - Generate programmatic telemetry tracks
 [2] PRODUCTION MODE   - Activate cellular MQTT hardware listeners

Enter your choice (1 or 2):
```

---

# Execution Modes

## Simulation Mode

Selecting:

```plaintext
1
```

launches:

- Programmatic fleet telemetry generation
- Continuous truck motion simulation
- Real-time dashboard updates
- Autonomous fatigue state transitions

---

## Production Mode

Selecting:

```plaintext
2
```

launches:

- MQTT subscriber listeners
- Real hardware telemetry ingestion
- Cellular IoT packet decoding
- Live over-the-air fleet synchronization

---

# Dashboard Access

Once services stabilize:

## Live Fleet Dashboard

```plaintext
http://127.0.0.1:8000/gati-path/dashboard
```

---

## Raw Fleet JSON Endpoint

```plaintext
http://127.0.0.1:8000/
```

---

# System Shutdown

To terminate all background processes safely:

1. Focus the master orchestration terminal
2. Execute:

```plaintext
CTRL + C
```

This broadcasts a termination signal across all managed child processes.

---

# Technology Stack

## Backend

- FastAPI
- Uvicorn
- Python AsyncIO

## Machine Learning

- Scikit-learn
- Random Forest Classifier
- SHAP Explainability

## Data Engineering

- Pandas
- NumPy

## IoT & Networking

- MQTT
- HTTP Telemetry Streams
- JSON Payload Serialization

## Frontend

- HTML
- CSS
- JavaScript
- Chart.js

---

# Future Expansion Roadmap

Planned architectural upgrades include:

- PostgreSQL fleet persistence
- Redis telemetry caching
- WebSocket live streaming
- Kafka event queues
- Real GPS map overlays
- ETA forecasting
- LSTM temporal sequence models
- Predictive maintenance analytics
- Reinforcement-learning route optimization

---

# Author

Developed and engineered by **Asmin Sinha**


# License

This project is intended for educational, research, and systems-engineering demonstration purposes.
