import winreg
import json
import os
def compare_registry_baseline():
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    baseline_file = os.path.join(
        project_dir, "baseline", "registry_baseline.json"
    )
    if not os.path.exists(baseline_file):
        print("Baseline file not found.")
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
                    if getattr(error, "winerror", None) != 259:
                        raise
                    break
        if current_data == baseline_data:
            print("Registry Baseline Comparison Results")
            print("------------------------------------")
            print("Registry integrity check passed.")
            print("No changes detected.")
        else:
            added = set(current_data) - set(baseline_data)
            deleted = set(baseline_data) - set(current_data)
            modified = {
                name for name in current_data
                if name in baseline_data
                and current_data[name] != baseline_data[name]
            }
            print("Registry Baseline Comparison Results")
            print("------------------------------------")
            print("Registry changes detected.")
            print("Added Entries:", len(added))
            print("Modified Entries:", len(modified))
            print("Deleted Entries:", len(deleted))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Baseline comparison error:", error)
if __name__ == "__main__":
    compare_registry_baseline()

