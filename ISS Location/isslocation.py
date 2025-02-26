import requests
import json
from datetime import datetime

def fetch_iss_location():
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.utcfromtimestamp(data["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
            latitude = float(data["iss_position"]["latitude"])
            longitude = float(data["iss_position"]["longitude"])
            
            location = {
                "date_time": timestamp,
                "latitude": latitude,
                "longitude": longitude,
                "connectors": {"connectorType": "ISS_Tracker"}
            }
            
            return {"isslocation": [location]}
        else:
            print("Failed to fetch ISS position")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_data_to_dataminer(data):
    if data:
        url = "http://localhost:34567/api/data/parameters"
        header_params = {
            "identifier": "ISS_Tracker",
            "type": "ISS_Tracker"
        }
        
        try:
            response = requests.put(url, headers=header_params, json=data)
            if response.status_code == 200:
                print("Data successfully sent to DataMiner")
            else:
                print(f"Failed to send data: {response.status_code}")
        except Exception as e:
            print(f"Error sending data: {e}")

if __name__ == "__main__":
    iss_data = fetch_iss_location()
    send_data_to_dataminer(iss_data)