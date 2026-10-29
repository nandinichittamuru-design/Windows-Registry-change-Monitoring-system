import winreg
import json
import os
def detect_unauthorized_modifications():
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    baseline_file = os.path.join(
        project_dir, "baseline", "registry_baseline.json"
    )
    if not os.path.exists(baseline_file):
        print("Error: Registry baseline file not found.")
        return
    try:
        with open(baseline_file, "r") as file:
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
                    name, value, data_type = (
                        winreg.EnumValue(key, index)
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
        warnings = []
        for name, data in current_data.items():
            if name not in baseline_data:
                warnings.append({
                    "entry": name,
                    "change": "Added",
                    "status": "Requires Verification"
                })
            elif data != baseline_data[name]:
                warnings.append({
                    "entry": name,
                    "change": "Modified",
                    "status": "Requires Verification"
                })
        for name in baseline_data:
            if name not in current_data:
                warnings.append({
                    "entry": name,
                    "change": "Deleted",
                    "status": "Requires Verification"
                })
        print("Unauthorized Registry Modification Detection")
        print("------------------------------------------")
        if warnings:
            print("Warning: Registry changes detected!")
            print("Total changes:", len(warnings))
            print(json.dumps(warnings, indent=4))
        else:
            print("No registry modifications detected.")
            print("Registry values match the baseline.")
        return warnings
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Registry monitoring error:", error)
if __name__ == "__main__":
    detect_unauthorized_modifications()
