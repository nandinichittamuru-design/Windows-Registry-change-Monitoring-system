import winreg
import json
def collect_registry_info():
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
        print("Registry information collected successfully")
        print(json.dumps(
            registry_data,
            indent=4,
            default=str
        ))
    except OSError as error:
        print("Registry access error:", error)
    return registry_data
if __name__ == "__main__":
    collect_registry_info()
