
import subprocess
import time
import sys
import socket
import os

def is_backend_ready(host="127.0.0.1", port=8000):
    """Actively checks if the FastAPI socket port is open and accepting traffic."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            return True
        except (ConnectionRefusedError, OSError):
            return False

def launch_system():
    print("==============================================================")
    print(" GATI-PATH: INTELLIGENT LOGISTICS ENGINE CORE ORCHESTRATOR")
    print("==============================================================")
    print("\nSelect your live data ingestion architecture:")
    print(" [1] SIMULATION MODE   - Generate programmatic telemetry tracks (8 trucks)")
    print(" [2] PRODUCTION MODE   - Activate cellular MQTT hardware listeners")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice not in ['1', '2']:
        print(" Invalid selection. Aborting startup.")
        sys.exit(1)
        
    print("\n Initializing core FastAPI App Engine in a NEW terminal window...")
    
   
    backend_cmd = f'start "Gati-Path Core Backend Server" {sys.executable} -m uvicorn app:app --host 127.0.0.1 --port 8000'
    subprocess.Popen(backend_cmd, shell=True)
    
    print(" Waiting for Random Forest training & SHAP engine instantiation to complete...")
    
    attempts = 0
    max_attempts = 45  
    while not is_backend_ready():
        time.sleep(1.0)
        attempts += 1
        if attempts >= max_attempts:
            print("\n Critical Timeout: Backend server failed to boot within 45 seconds.")
            sys.exit(1)
            
    print("Backend Engine Socket Online!")
    
    try:
        if choice == '1':
            print("\n Launching Telemetry Programmatic Simulator in a NEW terminal window...")
            simulator_cmd = f'start "Gati-Path 8-Asset Fleet Simulator" {sys.executable} simulate_iot.py'
            subprocess.Popen(simulator_cmd, shell=True)
        else:
            print("\n Activating Real Wireless Hardware Ingestion Layer in a NEW terminal window...")
            listener_cmd = f'start "Gati-Path Cellular MQTT Listener" {sys.executable} real_hardware_listener.py'
            subprocess.Popen(listener_cmd, shell=True)
            
        print("\n All systems distributed successfully across dedicated screens!")
        print("  Main Application Dashboard: http://127.0.0.1:8000/gati-path/dashboard")
        print("\nYou can close this master manager terminal now; your operational windows will remain active.")
        
    except Exception as e:
        print(f" Error distributing child tasks: {e}")

if __name__ == "__main__":
    launch_system()