
import winreg
import json
import os
from datetime import datetime

def create_baseline():
    registry_path = (
        r"Software\Microsoft\Windows"
        r"\CurrentVersion\Run"
    )

    registry_data = {}

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

                    registry_data[name] = {
                        "value": value,
                        "type": data_type
                    }

                    index += 1

                except OSError:
                    break

        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        baseline_dir = os.path.join(
            project_dir, "baseline"
        )

        os.makedirs(baseline_dir, exist_ok=True)

        baseline_file = os.path.join(
            baseline_dir, "registry_baseline.json"
        )

        if os.path.exists(baseline_file):
            print("Baseline already exists.")
            return

        baseline = {
            "registry_path": registry_path,
            "created_at": datetime.now().isoformat(),
            "registry_data": registry_data
        }

        with open(baseline_file, "w") as file:
            json.dump(
                baseline, file,
                indent=4, default=str
            )

        print("Registry baseline created successfully")
        print("Baseline saved at:", baseline_file)

    except OSError as error:
        print("Registry access error:", error)


if __name__ == "__main__":
    create_baseline()
