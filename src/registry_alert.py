import winreg
import json
import os
from datetime import datetime
def generate_registry_alerts():
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    baseline_file = os.path.join(
        project_dir, "baseline", "registry_baseline.json"
    )
    logs_dir = os.path.join(project_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    alert_file = os.path.join(
        logs_dir, "registry_alerts.json"
    )
    if not os.path.exists(baseline_file):
        print("Error: Baseline file not found.")
        return
    try:
        with open(baseline_file, "r", encoding="utf-8") as file:
            baseline = json.load(file)
        registry_path = baseline["registry_path"]
        baseline_data = baseline["registry_data"]
        current_data = {}
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            registry_path
        ) as key:
            index = 0
            while True:
                try:
                    name, value, data_type = winreg.EnumValue(
                        key, index
                    )
                    current_data[name] = {
                        "value": value,
                        "type": data_type
                    }
                    index += 1
                except OSError as error:
                    if getattr(error, "winerror", None) == 259:
                        break
                    raise
        alerts = []
        detection_time = datetime.now().isoformat(
            timespec="seconds"
        )
        for name, data in current_data.items():
            if name not in baseline_data:
                change_type = "Added"
            elif data != baseline_data[name]:
                change_type = "Modified"
            else:
                continue
            alerts.append({
                "timestamp": detection_time,
                "registry_entry": name,
                "change_type": change_type,
                "status": "Requires Verification"
            })
        for name in baseline_data:
            if name not in current_data:
                alerts.append({
                    "timestamp": detection_time,
                    "registry_entry": name,
                    "change_type": "Deleted",
                    "status": "Requires Verification"
                })
        print("Registry Alert Generation Results")
        print("---------------------------------")
        if alerts:
            for alert in alerts:
                print(
                    f"WARNING: {alert['change_type']} - "
                    f"{alert['registry_entry']}"
                )
        else:
            print("No registry changes detected.")
            print("No security alerts generated.")
        with open(
            alert_file, "w", encoding="utf-8"
        ) as file:
            json.dump(alerts, file, indent=4)
        print("Total Alerts:", len(alerts))
        print("Alerts saved at:", alert_file)
        return alerts
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Registry alert generation error:", error)
if __name__ == "__main__":
    generate_registry_alerts()
