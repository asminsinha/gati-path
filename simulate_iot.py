# simulate_iot.py
import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000/gati-path"

FLEET_HARDWARE_SIMULATOR = {
    "TRK-01-MUMBAI": {
        "lat": 19.5500, "lng": 72.5100, "lat_step": -0.015, "lng_step": 0.011,
        "fuel": 220.0, "load": 4100.0, "hours": 2.2, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "MH-12-QW-8841",
        "destination_name": "JNPT Port Hub",
        "destination_lat": 18.95, "destination_lng": 72.95,
        "fuel_price": 94.5, "forecast": 120, "util": 0.35, "base_tx": 55000, "freq": 12
    },
    "TRK-02-DELHI": {
        "lat": 28.0200, "lng": 77.5500, "lat_step": 0.013, "lng_step": -0.007,
        "fuel": 140.0, "load": 7900.0, "hours": 3.6, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "DL-01-AA-1092",
        "destination_name": "Okhla Logistics Park",
        "destination_lat": 28.53, "destination_lng": 77.27,
        "fuel_price": 96.2, "forecast": 80, "util": 0.85, "base_tx": 12000, "freq": 3
    },
    "TRK-03-BANGALORE": {
        "lat": 12.5400, "lng": 77.2100, "lat_step": 0.011, "lng_step": 0.014,
        "fuel": 260.0, "load": 3500.0, "hours": 0.5, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "KA-03-MM-5672",
        "destination_name": "Whitefield Freight Terminal",
        "destination_lat": 12.97, "destination_lng": 77.75,
        "fuel_price": 92.8, "forecast": 210, "util": 0.15, "base_tx": 94000, "freq": 22
    },
    "TRK-04-KOLKATA": {
        "lat": 22.9800, "lng": 87.8500, "lat_step": -0.012, "lng_step": 0.019,
        "fuel": 195.0, "load": 6200.0, "hours": 4.1, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "WB-25-EF-4321",
        "destination_name": "Haldia Dock Complex",
        "destination_lat": 22.02, "destination_lng": 88.06,
        "fuel_price": 103.5, "forecast": 140, "util": 0.42, "base_tx": 42000, "freq": 8
    },
    "TRK-05-CHENNAI": {
        "lat": 13.4500, "lng": 79.8200, "lat_step": -0.009, "lng_step": 0.012,
        "fuel": 215.0, "load": 5100.0, "hours": 1.5, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "TN-07-BY-9012",
        "destination_name": "Ennore Cargo Terminal",
        "destination_lat": 13.21, "destination_lng": 80.33,
        "fuel_price": 102.6, "forecast": 175, "util": 0.61, "base_tx": 61000, "freq": 15
    },
    "TRK-06-HYDERABAD": {
        "lat": 17.6200, "lng": 78.1200, "lat_step": -0.018, "lng_step": 0.016,
        "fuel": 180.0, "load": 8500.0, "hours": 5.8, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "TS-09-EX-7743",
        "destination_name": "GMR Aerospace Aerospace Park",
        "destination_lat": 17.23, "destination_lng": 78.43,
        "fuel_price": 107.4, "forecast": 95, "util": 0.72, "base_tx": 33000, "freq": 5
    },
    "TRK-07-AHMEDABAD": {
        "lat": 22.6400, "lng": 72.1100, "lat_step": 0.014, "lng_step": 0.022,
        "fuel": 290.0, "load": 2900.0, "hours": 0.2, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "GJ-01-ZZ-3114",
        "destination_name": "Mundra Port Zone",
        "destination_lat": 22.84, "destination_lng": 69.70,
        "fuel_price": 92.1, "forecast": 310, "util": 0.22, "base_tx": 115000, "freq": 28
    },
    "TRK-08-PUNE": {
        "lat": 18.2100, "lng": 74.2200, "lat_step": 0.011, "lng_step": -0.015,
        "fuel": 110.0, "load": 9200.0, "hours": 6.2, "is_resting": False, "rest_duration": 0.0,
        "vehicle_no": "MH-14-EU-5519",
        "destination_name": "Chakan Auto Logistics Corridor",
        "destination_lat": 18.75, "destination_lng": 73.85,
        "fuel_price": 94.5, "forecast": 65, "util": 0.91, "base_tx": 18000, "freq": 2
    }
}

print("==================================================================")
print("📡 VITARAI ENGINE: PRODUCTION DECOUPLED TELEMETRY INITIALIZED")
print("==================================================================")

step = 1
try:
    while True:
        print(f"\n⚡ Telemetry Frame Network Cycle: {step}")
        
        for t_id, hardware in FLEET_HARDWARE_SIMULATOR.items():
            
            if hardware["is_resting"]:
                hardware["rest_duration"] += 0.2  # Simulate 12 minutes of real-world rest per cycle
                
                # Check if driver cuts their break short (Example: only resting for 0.4 hrs instead of 0.6)
                if hardware["rest_duration"] >= 0.6:
                    hardware["hours"] = 0.0
                    hardware["is_resting"] = False
                    hardware["rest_duration"] = 0.0
                    print(f"✅ [REST COMPLETE]: {t_id} driver fully rested. Resuming route tracking.")
                else:
                    # Partially decrement duty strain to simulate real timeline continuity
                    hardware["hours"] = max(0.0, round(hardware["hours"] - 0.2, 2))
                    print(f"💤 [REST IN PROGRESS]: {t_id} is stopped at parking hub.")
            else:
                # Normal road navigation: advance position metrics
                hardware["lat"] += hardware["lat_step"]
                hardware["lng"] += hardware["lng_step"]
                
                base_cruising_drain = 1.0
                weight_overhead_drain = (hardware["load"] / 5000.0)
                current_hop_drain = base_cruising_drain + weight_overhead_drain

                hardware["fuel"] = round(max(5.0, hardware["fuel"] - current_hop_drain), 1)
                hardware["hours"] = round(hardware["hours"] + 0.3, 2)
            
            payload = {
                "tracking_id": t_id,
                "lat": round(hardware["lat"], 4),
                "lng": round(hardware["lng"], 4),
                "current_fuel_liters": hardware["fuel"],
                "cargo_load_kg": hardware["load"],
                "hours_driven_without_rest": hardware["hours"],
                
                # Dynamic metadata inclusions mapped to your 'hardware' loop variable
                "vehicle_no": hardware["vehicle_no"],
                "destination_name": hardware["destination_name"],
                "destination_lat": hardware["destination_lat"],
                "destination_lng": hardware["destination_lng"],
                "fuel_price": hardware["fuel_price"],
                "forecast": hardware["forecast"],
                "util": hardware["util"],
                "base_tx": hardware["base_tx"],
                "freq": hardware["freq"]
            }
            
            try:
                # Issue the stateless telemetry sync ping
                response = requests.post(f"{BASE_URL}/iot-ping", json=payload)
                if response.status_code == 200:
                    analysis_res = response.json()
                    
                    # Read the compliance flag issued by our server's rules
                    if analysis_res.get("fatigue_lock", False) and not hardware["is_resting"]:
                        print(f"⚠️ [COMPLIANCE TRIGGER]: Driver of {t_id} forcing mandatory stop.")
                        hardware["is_resting"] = True
                    
                    print(f" 🚛 {t_id} -> GPS: ({payload['lat']}, {payload['lng']}) | Fuel: {payload['current_fuel_liters']}L")
                    print(f"    ↳ Executive Insight: {analysis_res.get('insight')}")
            
            except requests.exceptions.ConnectionError:
                print("❌ Pipeline Offline. Check your backend server state.")
                sys.exit(1)
                
        step += 1
        time.sleep(2.0)

except KeyboardInterrupt:
    print("\n🛑 Telemetry stream terminated safely.")