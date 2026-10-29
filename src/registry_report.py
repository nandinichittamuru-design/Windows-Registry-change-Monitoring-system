import winreg
import json
import os
from datetime import datetime
def generate_registry_report():
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    baseline_file = os.path.join(
        project_dir, "baseline", "registry_baseline.json"
    )
    logs_dir = os.path.join(project_dir, "logs")
    reports_dir = os.path.join(project_dir, "reports")
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    log_file = os.path.join(
        logs_dir, "registry_monitoring_log.json"
    )
    report_file = os.path.join(
        reports_dir, "registry_security_report.txt"
    )
    if not os.path.exists(baseline_file):
        print("Error: Registry baseline file not found.")
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
        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )
        changes = []
        for name, data in current_data.items():
            if name not in baseline_data:
                change_type = "Added"
            elif data != baseline_data[name]:
                change_type = "Modified"
            else:
                continue
            changes.append({
                "timestamp": timestamp,
                "registry_entry": name,
                "change_type": change_type,
                "status": "Requires Verification"
            })
        for name in baseline_data:
            if name not in current_data:
                changes.append({
                    "timestamp": timestamp,
                    "registry_entry": name,
                    "change_type": "Deleted",
                    "status": "Requires Verification"
                })
        log_data = {
            "monitoring_time": timestamp,
            "registry_path": registry_path,
            "total_changes": len(changes),
            "detected_changes": changes
        }
        with open(log_file, "w", encoding="utf-8") as file:
            json.dump(log_data, file, indent=4)
        added = sum(
            c["change_type"] == "Added" for c in changes
        )
        modified = sum(
            c["change_type"] == "Modified" for c in changes
        )
        deleted = sum(
            c["change_type"] == "Deleted" for c in changes
        )
        with open(
            report_file, "w", encoding="utf-8"
        ) as file:
            file.write(
                "WINDOWS REGISTRY SECURITY REPORT\n"
            )
            file.write("=" * 40 + "\n")
            file.write(f"Monitoring Time: {timestamp}\n")
            file.write(
                f"Registry Path: HKCU\\{registry_path}\n"
            )
            file.write(f"Total Changes: {len(changes)}\n")
            file.write(f"Added Entries: {added}\n")
            file.write(f"Modified Entries: {modified}\n")
            file.write(f"Deleted Entries: {deleted}\n\n")
            file.write("DETECTED REGISTRY CHANGES\n")
            file.write("-" * 40 + "\n")
            if changes:
                for change in changes:
                    file.write(
                        f"Entry: {change['registry_entry']}\n"
                    )
                    file.write(
                        f"Change: {change['change_type']}\n"
                    )
                    file.write(
                        f"Status: {change['status']}\n\n"
                    )
            else:
                file.write(
                    "No registry changes detected.\n"
                )
        print("Registry Log and Report Generation")
        print("----------------------------------")
        print("Total Changes:", len(changes))
        print("Added Entries:", added)
        print("Modified Entries:", modified)
        print("Deleted Entries:", deleted)
        print("Log saved at:", log_file)
        print("Report saved at:", report_file)
        return log_data
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Report generation error:", error)
if __name__ == "__main__":
    generate_registry_report()
