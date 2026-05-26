# backend/services/gati_path/tracker.py
from datetime import datetime

class GatiLiveTracker:
    def __init__(self):
        
        self.active_vehicles = {}

    def update_location(self, tracking_id, lat, lng, traffic_status):
        self.active_vehicles[tracking_id] = {
            "latitude": lat,
            "longitude": lng,
            "traffic_status": traffic_status,
            "last_ping": datetime.now().strftime("%H:%M:%S")
        }
        return self.active_vehicles[tracking_id]

    def get_vehicle_status(self, tracking_id):
        return self.active_vehicles.get(tracking_id)


tracker_store = GatiLiveTracker()