import winreg
import json
import os
def detect_registry_changes():
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    baseline_file = os.path.join(
        project_dir, "baseline", "registry_baseline.json"
    )
    if not os.path.exists(baseline_file):
        print("Baseline file not found.")
        return
    with open(baseline_file, "r") as file:
        baseline = json.load(file)
    registry_path = baseline["registry_path"]
    old_data = baseline["registry_data"]
    current_data = {}
    try:
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
                except OSError:
                    break
    except OSError as error:
        print("Registry access error:", error)
        return
    added = {}
    modified = {}
    deleted = {}
    for name, data in current_data.items():
        if name not in old_data:
            added[name] = data
        elif data != old_data[name]:
            modified[name] = {
                "old": old_data[name],
                "new": data
            }
    for name, data in old_data.items():
        if name not in current_data:
            deleted[name] = data
    print("Registry Change Detection Results")
    print("---------------------------------")
    print("Added Entries:", len(added))
    print("Modified Entries:", len(modified))
    print("Deleted Entries:", len(deleted))
    results = {
        "added": added,
        "modified": modified,
        "deleted": deleted
    }
    print(json.dumps(results, indent=4, default=str))
    return results
if __name__ == "__main__":
    detect_registry_changes()
